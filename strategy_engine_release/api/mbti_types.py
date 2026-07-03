"""MBTI type profile endpoints.

  GET /api/mbti-types              list all MBTI type profiles
  GET /api/mbti-types/{type_code}  single MBTI type profile
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from models.orm import MbtiTypeProfile
from models.schemas import MbtiTypeProfileOut

router = APIRouter()


@router.get("", response_model=list[MbtiTypeProfileOut])
def list_mbti_profiles(db: Session = Depends(get_db)) -> list[MbtiTypeProfileOut]:
    rows = db.query(MbtiTypeProfile).order_by(MbtiTypeProfile.type_code).all()
    return [MbtiTypeProfileOut.model_validate(r) for r in rows]


@router.get("/{type_code}", response_model=MbtiTypeProfileOut)
def get_mbti_profile(type_code: str, db: Session = Depends(get_db)) -> MbtiTypeProfileOut:
    row = db.query(MbtiTypeProfile).filter_by(type_code=type_code.upper()).first()
    if row is None:
        raise HTTPException(status_code=404, detail=f"MBTI type '{type_code}' not found.")
    return MbtiTypeProfileOut.model_validate(row)
