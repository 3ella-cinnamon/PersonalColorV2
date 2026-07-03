"""Personal Color profile lookups."""

from typing import Optional

from sqlalchemy.orm import Session

from models.orm import PersonalColorProfile


def get_color_profile(db: Session, season: Optional[str]) -> Optional[dict]:
    if not season:
        return None
    row = db.query(PersonalColorProfile).filter_by(season=season).first()
    if row is None:
        return None
    return {
        "season": row.season,
        "energy_tone": row.energy_tone,
        "impression": row.impression,
        "communication_vibe": row.communication_vibe,
        "language_style": row.language_style,
        "social_energy": row.social_energy,
        "coaching_notes": row.coaching_notes,
    }


def list_color_profiles(db: Session) -> list[dict]:
    rows = db.query(PersonalColorProfile).order_by(PersonalColorProfile.season).all()
    return [get_color_profile(db, r.season) for r in rows]
