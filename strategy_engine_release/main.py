"""Personal Strategy Engine — FastAPI entry point (v2 with auth + DB).

Run locally:
    cp .env.example .env          # one-time
    pip install -r requirements.txt
    python seed.py                # creates tables, seeds criteria rows
    uvicorn main:app --reload

Then visit http://localhost:8000/docs
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth, aehq, bazi, cards, color_types, consult, daily, goals, hd_types, logs, mbti_types, profile, recommendations
from core.database import Base, engine
from core.middleware import APILoggingMiddleware
from core.schema_patch import apply_additive_columns

# Importing models here ensures they're registered with Base.metadata
# before create_all runs.
import models.orm  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create tables on startup. For production with migrations, swap this for Alembic.
    Base.metadata.create_all(bind=engine)
    # Add any columns added to existing tables after they first shipped (additive only).
    apply_additive_columns(engine)
    yield


app = FastAPI(
    title="Personal Strategy Engine",
    description=(
        "Daily Action Score across BaZi (SaJu), MBTI cognitive functions, "
        "Mian Xiang, and Human Design — now with user accounts, stored profiles, "
        "and DB-driven MBTI / HD decision rules."
    ),
    version="0.2.0",
    lifespan=lifespan,
)

import os as _os
_FRONTEND_ORIGIN = _os.getenv("FRONTEND_ORIGIN", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[_FRONTEND_ORIGIN] if _FRONTEND_ORIGIN != "*" else ["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(APILoggingMiddleware)

app.include_router(auth.router,            prefix="/api/auth",            tags=["auth"])
app.include_router(profile.router,         prefix="/api/profile",         tags=["profile"])
app.include_router(daily.router,           prefix="/api",                 tags=["daily"])
app.include_router(hd_types.router,        prefix="/api/hd-types",        tags=["hd-types"])
app.include_router(mbti_types.router,      prefix="/api/mbti-types",      tags=["mbti-types"])
app.include_router(color_types.router,     prefix="/api/color-types",     tags=["color-types"])
app.include_router(goals.router,           prefix="/api/goals",           tags=["goals"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(logs.router,            prefix="/api/logs",            tags=["logs"])
app.include_router(bazi.router,            prefix="/api/bazi",            tags=["bazi"])
app.include_router(consult.router,         prefix="/api/consult",         tags=["consult"])
app.include_router(aehq.router,           prefix="/api/aehq",            tags=["aehq"])
app.include_router(cards.router,          prefix="/api/cards",           tags=["cards"])


@app.get("/health", tags=["meta"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
