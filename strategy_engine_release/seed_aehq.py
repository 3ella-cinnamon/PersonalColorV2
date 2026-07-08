"""Seed the AEHQ v2.0 knowledge base into the database.

The source of truth is the module-level content in services/aehq_service.py
(SITUATIONS, FRAMEWORKS, FRAMEWORK_RULES, SITUATION_PRIORS, and the score-delta
maps). This script mirrors that content into the aehq_* reference tables so the
engine can load it from the DB as an in-memory cache.

Usage:
    python seed_aehq.py            # create tables + seed (idempotent, skips if present)
    python seed_aehq.py --reset    # wipe the aehq_* content tables first, then re-seed

Only the AEHQ *content* tables are touched. User sessions / responses / results
are NEVER modified by this script.
"""

import json
import sys

from core.database import Base, SessionLocal, engine
import models.orm  # noqa: F401  (ensure all tables are registered before create_all)
from models.orm import (
    AEHQFramework, AEHQSituation, AEHQSituationItem, AEHQFrameworkRule, AEHQScoreDelta,
)


def _wipe(db) -> None:
    db.query(AEHQSituationItem).delete()
    db.query(AEHQSituation).delete()
    db.query(AEHQFramework).delete()
    db.query(AEHQFrameworkRule).delete()
    db.query(AEHQScoreDelta).delete()
    db.commit()


def seed_aehq(db, reset: bool = False) -> dict:
    """Populate the aehq_* content tables. Returns a dict of row counts.

    Idempotent: if frameworks already exist and reset is False, does nothing.
    """
    # Imported here (not at top) so this also works when called from inside
    # the running service via aehq_service._ensure_cache().
    import services.aehq_service as svc

    if reset:
        _wipe(db)
    elif db.query(AEHQFramework).count() > 0:
        return {"skipped": True}

    # ── Frameworks ────────────────────────────────────────────
    for code, f in svc.FRAMEWORKS.items():
        db.add(AEHQFramework(
            code=code, name=f["name"], evidence=f.get("evidence"),
            tier=f.get("tier"), technique=f["technique"],
        ))

    # ── Situations + their questions ──────────────────────────
    n_items = 0
    for order, (key, s) in enumerate(svc.SITUATIONS.items()):
        db.add(AEHQSituation(
            key=key, label=s["label"], icon=s["icon"],
            emotion_words_json=json.dumps(s.get("emotion_words", [])),
            unmet_needs_json=json.dumps(s.get("unmet_need_options", [])),
            self_compassion=s["self_compassion"],
            ifthen_template=s["ifthen_template"],
            priors_json=json.dumps(svc.SITUATION_PRIORS.get(key, {})),
            sort_order=order,
        ))
        item_order = 0
        for track in ("S", "D", "R"):
            for item in s["items"].get(track, []):
                slider_json = None
                if item.get("input_type") == "slider":
                    slider_json = json.dumps({
                        "min":    item.get("slider_min", 0),
                        "max":    item.get("slider_max", 100),
                        "step":   item.get("slider_step", 10),
                        "labels": item.get("slider_labels", {}),
                    })
                db.add(AEHQSituationItem(
                    situation_key=key, item_key=item["id"], track=track,
                    sort_order=item_order,
                    input_type=item.get("input_type", "text"),
                    skippable=item.get("skippable", False),
                    question=item["question"], subtext=item.get("subtext"),
                    options_json=json.dumps(item["options"]) if item.get("options") else None,
                    slider_json=slider_json,
                    score_deltas_json=json.dumps(item.get("score_deltas", {})),
                    value_scoring=item.get("value_scoring"),
                ))
                item_order += 1
                n_items += 1

    # ── Framework-selection mapping rules ─────────────────────
    for order, rule in enumerate(svc.FRAMEWORK_RULES):
        db.add(AEHQFrameworkRule(
            sort_order=order, priority_label=rule["priority_label"],
            score_var=rule["score_var"], min_val=rule["min_val"],
            max_val=rule["max_val"], framework_code=rule["framework_code"],
        ))

    # ── Score-delta maps (emotion / body quality / body location / unmet need) ──
    delta_sources = [
        ("emotion",  svc.EMOTION_WORD_DELTAS),
        ("body",     svc.BODY_QUALITY_DELTAS),
        ("body_loc", svc.BODY_LOCATION_DELTAS),
        ("need",     svc.UNMET_NEED_DELTAS),
    ]
    n_deltas = 0
    for kind, source in delta_sources:
        for key, deltas in source.items():
            db.add(AEHQScoreDelta(kind=kind, trigger_key=key, deltas_json=json.dumps(deltas)))
            n_deltas += 1

    db.commit()
    return {
        "frameworks":  len(svc.FRAMEWORKS),
        "situations":  len(svc.SITUATIONS),
        "items":       n_items,
        "rules":       len(svc.FRAMEWORK_RULES),
        "deltas":      n_deltas,
    }


def main():
    reset = "--reset" in sys.argv

    print("-> Creating tables (if missing)...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if reset:
            print("-> --reset: clearing aehq_* content tables...")
        counts = seed_aehq(db, reset=reset)
        if counts.get("skipped"):
            print("OK Already seeded - nothing to do (use --reset to rebuild).")
        else:
            print(f"OK Inserted {counts['frameworks']} frameworks.")
            print(f"OK Inserted {counts['situations']} situations, {counts['items']} questions.")
            print(f"OK Inserted {counts['rules']} framework-selection rules.")
            print(f"OK Inserted {counts['deltas']} score-delta rows.")
        print("OK Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
