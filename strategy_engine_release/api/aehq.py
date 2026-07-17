"""AEHQ v2.0 API router — /api/aehq/*"""

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session as DBSession

from core.database import get_db
from core.deps import get_current_user
from models.orm import User
from services import aehq_service

router = APIRouter()


class AnswerIn(BaseModel):
    step: str
    answer: Any
    lang: str = "en"   # language the client was showing when the user answered


@router.post("/start")
def start_session(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    return aehq_service.create_session(current_user.id, db)


@router.get("/history")
def history(
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    return aehq_service.list_results(current_user.id, db)


@router.get("/{session_id}")
def get_screen(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    return aehq_service.get_current_screen(session_id, current_user.id, db)


@router.post("/{session_id}/answer")
def submit_answer(
    session_id: int,
    body: AnswerIn,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    return aehq_service.submit_answer(session_id, current_user.id, body.step, body.answer, db, lang=body.lang)


@router.get("/{session_id}/result")
def get_result(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: DBSession = Depends(get_db),
):
    return aehq_service.get_result(session_id, current_user.id, db)
