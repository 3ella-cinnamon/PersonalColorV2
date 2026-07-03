"""Lookups against the criteria tables (mbti_criteria, hd_criteria, mbti_hd_scenarios).

goal-aware queries:
  - goal=None  → returns all general rows (goal IS NULL)
  - goal='work' → returns general rows + work-specific rows

get_blended_decisions merges MBTI + HD rows sorted by weight, tagged with source.
get_scenario returns the MBTI×HD blend/conflict row (or None if HD not set).
"""

from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.orm import HdCriterion, MbtiCriterion, MbtiHdScenario


def get_mbti_decisions(
    db: Session, mbti_type: str, goal: Optional[str] = None
) -> list[dict]:
    q = db.query(MbtiCriterion).filter(MbtiCriterion.mbti_type == mbti_type)
    if goal:
        q = q.filter(
            or_(MbtiCriterion.goal.is_(None), MbtiCriterion.goal == goal)
        )
    else:
        q = q.filter(MbtiCriterion.goal.is_(None))
    rows = q.order_by(MbtiCriterion.weight.desc()).all()
    return [
        {"preference": r.preference, "decision": r.decision,
         "weight": r.weight, "goal": r.goal}
        for r in rows
    ]


def get_hd_decisions(
    db: Session, hd_type: Optional[str], goal: Optional[str] = None
) -> list[dict]:
    if not hd_type:
        return []
    q = db.query(HdCriterion).filter(HdCriterion.hd_type == hd_type)
    if goal:
        q = q.filter(
            or_(HdCriterion.goal.is_(None), HdCriterion.goal == goal)
        )
    else:
        q = q.filter(HdCriterion.goal.is_(None))
    rows = q.order_by(HdCriterion.weight.desc()).all()
    return [
        {"preference": r.preference, "decision": r.decision,
         "weight": r.weight, "goal": r.goal}
        for r in rows
    ]


def get_scenario(
    db: Session, mbti_type: str, hd_type: Optional[str]
) -> Optional[dict]:
    if not hd_type:
        return None
    row = (
        db.query(MbtiHdScenario)
          .filter_by(mbti_type=mbti_type, hd_type=hd_type)
          .first()
    )
    if row is None:
        return None
    return {
        "mbti_type":            row.mbti_type,
        "hd_type":              row.hd_type,
        "blend_summary":        row.blend_summary,
        "conflict_situation":   row.conflict_situation,
        "conflict_sentence":    row.conflict_sentence,
        "recommended_sentence": row.recommended_sentence,
        "recommended_action":   row.recommended_action,
    }


def get_blended_decisions(
    db: Session, mbti_type: str, hd_type: Optional[str], goal: str
) -> list[dict]:
    """Merge MBTI and HD criteria for a given goal, sorted by weight descending."""
    mbti_rows = get_mbti_decisions(db, mbti_type, goal=goal)
    hd_rows   = get_hd_decisions(db, hd_type, goal=goal)

    blended = [
        {"source": "mbti", **r} for r in mbti_rows
    ] + [
        {"source": "hd", **r} for r in hd_rows
    ]
    blended.sort(key=lambda r: r["weight"], reverse=True)
    return blended
