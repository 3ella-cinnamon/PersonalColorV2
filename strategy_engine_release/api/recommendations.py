"""Recommendations history and feedback endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user
from models.orm import User, Recommendation
from models.schemas import CoachingResponse, FeedbackRequest
from services.recommendation_service import save_feedback, get_user_recommendations


router = APIRouter()


@router.get("", response_model=list[CoachingResponse])
def list_recommendations(
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    rows = get_user_recommendations(db, current.id)
    return [CoachingResponse.from_orm_row(r) for r in rows]


@router.post("/{rec_id}/feedback", status_code=201)
def submit_feedback(
    rec_id: int,
    req: FeedbackRequest,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = db.query(Recommendation).filter_by(id=rec_id, user_id=current.id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Recommendation not found.")
    save_feedback(db, rec_id, current.id, req.rating, req.feedback_text)
    return {"status": "ok"}
