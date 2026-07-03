"""Personal Color type reference endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from models.orm import PersonalColorProfile
from models.schemas import PersonalColorProfileOut


router = APIRouter()


@router.get("", response_model=list[PersonalColorProfileOut])
def list_color_profiles(db: Session = Depends(get_db)):
    rows = db.query(PersonalColorProfile).order_by(PersonalColorProfile.season).all()
    return [PersonalColorProfileOut.model_validate(r) for r in rows]


@router.get("/{season}", response_model=PersonalColorProfileOut)
def get_color_profile(season: str, db: Session = Depends(get_db)):
    row = db.query(PersonalColorProfile).filter_by(season=season.title()).first()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Color season '{season}' not found.")
    return PersonalColorProfileOut.model_validate(row)
