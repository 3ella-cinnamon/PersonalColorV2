"""Card Deck — Thai translation cache for English-only source content.

Same self-migrating pattern as services/aehq_service.py's translation layer:
module dicts (services/cards_i18n_th.py) are the seed defaults; the DB copy
(card_translations table) wins once seeded, so operators can edit Thai copy
without a deploy. A meta row records the content version so a code deploy
with new/changed strings re-seeds automatically.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from models.orm import CardTranslation
from services import cards_i18n_th as _i18n_th

# Bump when cards_i18n_th.py's dicts change so _ensure_cache re-seeds on deploy.
CARDS_I18N_VERSION = "cards-i18n-3"

# Flat English -> Thai map (micro_intervention + clinical_caution). Module
# defaults double as seed source; DB rows win once seeded (see _load_from_db).
# Workshop copy (framework short/prompt/hints) is nested, not flat — see
# get_th_bundle() — since it's keyed by framework name, not English source text.
TH_MAP: dict[str, str] = {
    **_i18n_th.MICRO_TH,
    **_i18n_th.CAUTION_TH,
}

_CACHE_LOADED = False


def _load_from_db(db: DBSession) -> None:
    global TH_MAP
    rows = db.query(CardTranslation).filter(CardTranslation.lang == "th").all()
    merged: dict[str, str] = {**_i18n_th.MICRO_TH, **_i18n_th.CAUTION_TH}
    for row in rows:
        if row.src.startswith(("workshop:", "summary:", "guide:")):
            continue  # nested/templated — served separately by get_th_bundle()
        merged[row.src] = row.dst
    TH_MAP = merged


def _seed(db: DBSession) -> None:
    db.query(CardTranslation).filter(CardTranslation.lang.in_(["th", "meta"])).delete(synchronize_session=False)
    rows = []
    for src, dst in {**_i18n_th.MICRO_TH, **_i18n_th.CAUTION_TH}.items():
        rows.append(CardTranslation(lang="th", src=src, dst=dst))
    for fw, entry in _i18n_th.WORKSHOP_TH.items():
        rows.append(CardTranslation(lang="th", src=f"workshop:{fw}:short",  dst=entry["short"]))
        rows.append(CardTranslation(lang="th", src=f"workshop:{fw}:prompt", dst=entry["prompt"]))
        for i, hint in enumerate(entry["hints"]):
            rows.append(CardTranslation(lang="th", src=f"workshop:{fw}:hint:{i}", dst=hint))
    for key, tpl in _i18n_th.SUMMARY_TH.items():
        rows.append(CardTranslation(lang="th", src=f"summary:{key}", dst=tpl))
    rows.append(CardTranslation(lang="th", src="guide:label", dst=_i18n_th.GUIDE_TH["label"]))
    for i, sec in enumerate(_i18n_th.GUIDE_TH["sections"]):
        rows.append(CardTranslation(lang="th", src=f"guide:{i}:title", dst=sec["title"]))
        rows.append(CardTranslation(lang="th", src=f"guide:{i}:body", dst=sec["body"]))
    rows.append(CardTranslation(lang="meta", src="content_version", dst=CARDS_I18N_VERSION))
    db.add_all(rows)
    db.commit()


def _ensure_cache(db: DBSession) -> None:
    """Seed/refresh the DB content, then load the cache once per process.
    Self-migrating: a meta row stores the content version that last seeded
    the DB; a newer CARDS_I18N_VERSION (a deploy) triggers a re-seed."""
    global _CACHE_LOADED
    if _CACHE_LOADED:
        return
    stored_version = db.execute(
        select(CardTranslation.dst).where(
            CardTranslation.lang == "meta", CardTranslation.src == "content_version")
    ).scalar_one_or_none()
    if stored_version != CARDS_I18N_VERSION:
        _seed(db)
    _load_from_db(db)
    _CACHE_LOADED = True


def reload_cache(db: DBSession) -> None:
    global _CACHE_LOADED
    _CACHE_LOADED = False
    _ensure_cache(db)


def get_th_bundle(db: DBSession) -> dict:
    """Everything the frontend needs for one request: flat micro/caution map
    plus the workshop copy keyed by framework name."""
    _ensure_cache(db)
    workshops: dict[str, dict] = {}
    rows = db.query(CardTranslation).filter(
        CardTranslation.lang == "th", CardTranslation.src.like("workshop:%")
    ).all()
    for row in rows:
        parts = row.src.split(":", 2)  # ["workshop", fw, field]
        fw, field = parts[1], parts[2]
        entry = workshops.setdefault(fw, {"short": None, "prompt": None, "hints": []})
        if field == "short":
            entry["short"] = row.dst
        elif field == "prompt":
            entry["prompt"] = row.dst
        elif field.startswith("hint:"):
            idx = int(field.split(":")[1])
            while len(entry["hints"]) <= idx:
                entry["hints"].append(None)
            entry["hints"][idx] = row.dst

    summaries: dict[str, str] = {}
    for row in db.query(CardTranslation).filter(
        CardTranslation.lang == "th", CardTranslation.src.like("summary:%")
    ).all():
        summaries[row.src.split(":", 1)[1]] = row.dst

    # Reading guide: guide:label + guide:{i}:title / guide:{i}:body
    guide: dict = {"label": None, "sections": []}
    for row in db.query(CardTranslation).filter(
        CardTranslation.lang == "th", CardTranslation.src.like("guide:%")
    ).all():
        rest = row.src.split(":", 1)[1]
        if rest == "label":
            guide["label"] = row.dst
            continue
        idx_str, field = rest.split(":", 1)
        idx = int(idx_str)
        while len(guide["sections"]) <= idx:
            guide["sections"].append({"title": None, "body": None})
        guide["sections"][idx][field] = row.dst

    return {
        "strings": dict(TH_MAP),
        "workshops": workshops,
        "summaries": summaries,
        "guide": guide,
    }
