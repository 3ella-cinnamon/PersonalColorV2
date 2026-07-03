"""HD type profile endpoints.

  GET /api/hd-types           list all HD type profiles
  GET /api/hd-types/{hd_type} single HD type profile
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from models.orm import HdTypeProfile
from models.schemas import HdTypeProfileOut

router = APIRouter()


@router.get("", response_model=list[HdTypeProfileOut])
def list_hd_profiles(db: Session = Depends(get_db)) -> list[HdTypeProfileOut]:
    rows = db.query(HdTypeProfile).order_by(HdTypeProfile.hd_type).all()
    return [HdTypeProfileOut.model_validate(r) for r in rows]


@router.get("/{hd_type}", response_model=HdTypeProfileOut)
def get_hd_profile(hd_type: str, db: Session = Depends(get_db)) -> HdTypeProfileOut:
    row = db.query(HdTypeProfile).filter_by(hd_type=hd_type).first()
    if row is None:
        raise HTTPException(status_code=404, detail=f"HD type '{hd_type}' not found.")
    return HdTypeProfileOut.model_validate(row)
