"""GET /api/logs — view API call history (admin / debug use)."""

from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user
from models.orm import APILog, User
from pydantic import BaseModel, ConfigDict
from datetime import datetime

router = APIRouter()


class APILogOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:            int
    method:        str
    url:           str
    status_code:   int
    request_body:  Optional[str]
    response_body: Optional[str]
    duration_ms:   int
    created_at:    datetime


@router.get("", response_model=list[APILogOut])
def list_logs(
    url_contains: Optional[str] = Query(None, description="Filter by URL substring"),
    status_code:  Optional[int] = Query(None, description="Filter by HTTP status code"),
    on_date:      Optional[date] = Query(None, description="Filter by date (YYYY-MM-DD)"),
    limit:        int            = Query(50, ge=1, le=500),
    _: User = Depends(get_current_user),   # must be logged in
    db: Session = Depends(get_db),
):
    q = db.query(APILog).order_by(APILog.created_at.desc())

    if url_contains:
        q = q.filter(APILog.url.contains(url_contains))
    if status_code:
        q = q.filter(APILog.status_code == status_code)
    if on_date:
        from sqlalchemy import func
        q = q.filter(func.date(APILog.created_at) == on_date)

    return q.limit(limit).all()
