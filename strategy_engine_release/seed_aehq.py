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

from sqlalchemy import inspect, text

from core.database import Base, SessionLocal, engine
import models.orm  # noqa: F401  (ensure all tables are registered before create_all)
from models.orm import (
    AEHQFramework, AEHQSituation, AEHQSituationItem, AEHQFrameworkRule, AEHQScoreDelta,
    AEHQTranslation,
)


# Columns added after the tables first shipped. create_all() won't add columns
# to an existing table (SQLite & Postgres alike), so we ALTER them in when
# missing — idempotent, dialect-aware. Runs on every seed and on cache warm-up.
_ADDED_COLUMNS: list[tuple[str, str, str, str]] = [
    # (table, column, sqlite_ddl_type_default, postgres_ddl_type_default)
    ("aehq_situations", "followup_json",    "TEXT DEFAULT '{}'",   "TEXT DEFAULT '{}'"),
    ("aehq_results",    "trauma_flagged",   "BOOLEAN DEFAULT 0",   "BOOLEAN DEFAULT false"),
    ("aehq_results",    "referral_offered", "BOOLEAN DEFAULT 0",   "BOOLEAN DEFAULT false"),
    ("aehq_results",    "low_mood_flagged", "BOOLEAN DEFAULT 0",   "BOOLEAN DEFAULT false"),
    ("aehq_results",    "chasing_flagged",  "BOOLEAN DEFAULT 0",   "BOOLEAN DEFAULT false"),
    ("aehq_results",    "goal_text",        "TEXT",                "TEXT"),
    ("aehq_results",    "goal_lang",        "VARCHAR(8)",          "VARCHAR(8)"),
    ("aehq_sessions",   "consent_agreed",   "BOOLEAN DEFAULT 0",   "BOOLEAN DEFAULT false"),
    ("aehq_sessions",   "training_opt_in",  "BOOLEAN DEFAULT 0",   "BOOLEAN DEFAULT false"),
    ("aehq_sessions",   "consent_at",       "DATETIME",            "TIMESTAMP"),
    ("aehq_responses",  "content_version",  "VARCHAR(20)",         "VARCHAR(20)"),
    ("aehq_responses",  "lang_shown",       "VARCHAR(8)",          "VARCHAR(8)"),
    ("aehq_results",    "content_version",  "VARCHAR(20)",         "VARCHAR(20)"),
    ("aehq_results",    "bottom_line_text",   "TEXT",              "TEXT"),
    ("aehq_results",    "bottom_line_belief", "INTEGER",           "INTEGER"),
    ("aehq_results",    "bottom_line_lang",   "VARCHAR(8)",        "VARCHAR(8)"),
    ("aehq_results",    "thought_text",       "TEXT",              "TEXT"),
    ("aehq_results",    "thought_lang",       "VARCHAR(8)",        "VARCHAR(8)"),
    ("aehq_results",    "critic_function",    "VARCHAR(30)",       "VARCHAR(30)"),
    ("aehq_results",    "critic_protects_text","TEXT",             "TEXT"),
    ("aehq_results",    "hated_self_flagged", "BOOLEAN DEFAULT 0", "BOOLEAN DEFAULT false"),
    ("aehq_situation_items", "bottom_line",   "VARCHAR(80)",       "VARCHAR(80)"),
    ("aehq_situation_items", "capture",       "VARCHAR(40)",       "VARCHAR(40)"),
    ("aehq_results",    "foc_level",         "VARCHAR(12)",        "VARCHAR(12)"),
    ("aehq_results",    "compassion_mode",   "VARCHAR(12)",        "VARCHAR(12)"),
    ("aehq_results",    "soothe_rating",     "INTEGER",            "INTEGER"),
    ("aehq_results",    "goal_attainment",   "INTEGER",            "INTEGER"),
]


def ensure_aehq_columns(bind) -> int:
    """Add any missing AEHQ columns to existing tables. Idempotent."""
    insp = inspect(bind)
    existing_tables = set(insp.get_table_names())
    is_pg = bind.dialect.name == "postgresql"
    added = 0
    with bind.begin() as conn:
        for table, column, sqlite_ddl, pg_ddl in _ADDED_COLUMNS:
            if table not in existing_tables:
                continue  # create_all will build it fresh with all columns
            cols = {c["name"] for c in insp.get_columns(table)}
            if column in cols:
                continue
            ddl = pg_ddl if is_pg else sqlite_ddl
            conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))
            added += 1
    return added


def _wipe(db) -> None:
    db.query(AEHQSituationItem).delete()
    db.query(AEHQSituation).delete()
    db.query(AEHQFramework).delete()
    db.query(AEHQFrameworkRule).delete()
    db.query(AEHQScoreDelta).delete()
    db.query(AEHQTranslation).delete()
    db.commit()


def seed_aehq(db, reset: bool = False) -> dict:
    """Populate the aehq_* content tables. Returns a dict of row counts.

    Idempotent: if frameworks already exist and reset is False, does nothing.
    """
    # Imported here (not at top) so this also works when called from inside
    # the running service via aehq_service._ensure_cache().
    import services.aehq_service as svc

    # Make sure late-added columns exist before we write to them.
    ensure_aehq_columns(db.get_bind())

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
            followup_json=json.dumps(svc.FOLLOWUP_CONFIG.get(key, {})),
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
                    bottom_line=item.get("bottom_line"),
                    capture=item.get("capture"),
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

    # ── Thai translations (strings + framework techniques + long notes) ──
    n_tr = 0
    for src, dst in svc.TH_STRINGS.items():
        db.add(AEHQTranslation(lang="th", src=src, dst=dst)); n_tr += 1
    for code, dst in svc.TH_TECHNIQUES.items():
        db.add(AEHQTranslation(lang="th", src=f"technique:{code}", dst=dst)); n_tr += 1
    for name, dst in svc.TH_NOTES.items():
        db.add(AEHQTranslation(lang="th", src=f"note:{name}", dst=dst)); n_tr += 1

    # Meta row: records which content version seeded this DB. _ensure_cache
    # compares it against the running code's CONTENT_VERSION and auto-refreshes
    # on mismatch — making deploys self-migrating.
    db.add(AEHQTranslation(lang="meta", src="content_version", dst=svc.CONTENT_VERSION))

    db.commit()
    return {
        "frameworks":  len(svc.FRAMEWORKS),
        "situations":  len(svc.SITUATIONS),
        "items":       n_items,
        "rules":       len(svc.FRAMEWORK_RULES),
        "deltas":      n_deltas,
        "translations": n_tr,
    }


def main():
    reset = "--reset" in sys.argv

    print("-> Creating tables (if missing)...")
    Base.metadata.create_all(bind=engine)

    added = ensure_aehq_columns(engine)
    if added:
        print(f"-> Migrated: added {added} missing column(s) to existing AEHQ tables.")

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
            print(f"OK Inserted {counts['translations']} Thai translation rows.")
        print("OK Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
