"""Card Deck — saved readings API (Stage 3: session logic / saving readings).

Endpoints:
  POST   /api/cards/readings        → save a completed reading
  GET    /api/cards/readings        → list the current user's readings (newest first)
  GET    /api/cards/readings/{id}   → one reading
  DELETE /api/cards/readings/{id}   → delete one reading (user has full agency)
  GET    /api/cards/i18n/th         → Thai copy for English-only card content (public)

A reading is a draw the user chose to keep: deck + spread, the drawn cards with
their spread positions, and the user's own words. No interpretation is stored on
the user's behalf — the reflection is authored by the user.
"""

from __future__ import annotations

import json
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user
from models.orm import CardReading, User
from services import cards_service

router = APIRouter()


# ── Schemas ───────────────────────────────────────────────────────────────────

class DrawnCard(BaseModel):
    card_id:  str
    position: Optional[str] = None      # spread position label, e.g. "Feeling"


class ReadingCreate(BaseModel):
    deck:        str
    spread_id:   str
    spread_name: str
    cards:       list[DrawnCard] = Field(default_factory=list)
    reflection:  Optional[str] = None
    intention:   Optional[str] = None
    activation_before: Optional[int] = Field(default=None, ge=0, le=10)
    lang:        Optional[str] = None
    mode:        str = "quick"                       # quick | guided
    session:     Optional[dict[str, Any]] = None     # full guided-session record


class ReadingOut(BaseModel):
    id:          int
    deck:        str
    spread_id:   str
    spread_name: str
    cards:       list[DrawnCard]
    reflection:  Optional[str]
    intention:   Optional[str]
    activation_before: Optional[int]
    lang:        Optional[str]
    mode:        str
    session:     Optional[dict[str, Any]]
    created_at:  str


def _serialize(r: CardReading) -> ReadingOut:
    return ReadingOut(
        id=r.id,
        deck=r.deck,
        spread_id=r.spread_id,
        spread_name=r.spread_name,
        cards=[DrawnCard(**c) for c in json.loads(r.cards_json or "[]")],
        reflection=r.reflection,
        intention=r.intention,
        activation_before=r.activation_before,
        lang=r.lang,
        mode=r.session_mode or "quick",
        session=json.loads(r.session_json) if r.session_json else None,
        created_at=r.created_at.isoformat() if r.created_at else "",
    )


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/readings", status_code=status.HTTP_201_CREATED, response_model=ReadingOut)
def create_reading(
    payload: ReadingCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """Persist one reading for the authenticated user."""
    reading = CardReading(
        user_id=user.id,
        deck=payload.deck,
        spread_id=payload.spread_id,
        spread_name=payload.spread_name,
        cards_json=json.dumps([c.model_dump() for c in payload.cards], ensure_ascii=False),
        reflection=payload.reflection,
        intention=payload.intention,
        activation_before=payload.activation_before,
        lang=payload.lang,
        session_mode=payload.mode or "quick",
        session_json=json.dumps(payload.session, ensure_ascii=False) if payload.session else None,
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return _serialize(reading)


@router.get("/readings", response_model=list[ReadingOut])
def list_readings(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """List the user's saved readings, newest first."""
    rows = (
        db.query(CardReading)
        .filter(CardReading.user_id == user.id)
        .order_by(CardReading.created_at.desc(), CardReading.id.desc())
        .all()
    )
    return [_serialize(r) for r in rows]


def _owned_reading(reading_id: int, user: User, db: Session) -> CardReading:
    reading = db.query(CardReading).filter(CardReading.id == reading_id).first()
    if reading is None or reading.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reading not found")
    return reading


@router.get("/readings/{reading_id}", response_model=ReadingOut)
def get_reading(
    reading_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    return _serialize(_owned_reading(reading_id, user, db))


@router.delete("/readings/{reading_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reading(
    reading_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    db.delete(_owned_reading(reading_id, user, db))
    db.commit()


@router.get("/i18n/th")
def get_th_i18n(db: Session = Depends(get_db)) -> Any:
    """Thai copy for card content whose source is English-only (micro-
    interventions, clinical cautions, workshop framework copy). Public —
    static localized reference text, not user data."""
    return cards_service.get_th_bundle(db)
