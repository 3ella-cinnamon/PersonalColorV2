"""Agent memory + variation selection service.

Tracks recently-used coaching angles per user so the pipeline can avoid repetition.
Records expire automatically after 30 days.
"""

import hashlib
import random
from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from models.orm import AgentMemory


VARIATION_ANGLES  = ["timing-first", "behavior-first", "language-first", "warning-first"]
VARIATION_LENSES  = ["mbti-dominant", "hd-dominant", "color-dominant", "balanced"]
VARIATION_STYLES  = ["declarative", "interrogative", "assertive-open", "collaborative"]
VARIATION_TONES   = ["direct", "measured", "analytical", "empathetic-strategic"]
VARIATION_ENTRIES = ["open-with-context", "open-with-recommendation", "open-with-question"]


def generate_variation_seed(user_id: int) -> str:
    timestamp = datetime.utcnow().isoformat()
    return hashlib.md5(f"{user_id}-{timestamp}".encode()).hexdigest()


def select_variation(seed: str, excluded_angles: list[str]) -> dict:
    rng = random.Random(seed)
    available = [a for a in VARIATION_ANGLES if a not in excluded_angles] or VARIATION_ANGLES
    return {
        "angle":  rng.choice(available),
        "lens":   rng.choice(VARIATION_LENSES),
        "style":  rng.choice(VARIATION_STYLES),
        "tone":   rng.choice(VARIATION_TONES),
        "entry":  rng.choice(VARIATION_ENTRIES),
    }


def get_active_memories(
    db: Session, user_id: int, goal_context: Optional[str] = None
) -> list[dict]:
    purge_expired(db, user_id)
    q = db.query(AgentMemory).filter(
        AgentMemory.user_id == user_id,
        AgentMemory.expires_at > datetime.utcnow(),
    )
    if goal_context:
        q = q.filter(AgentMemory.goal_context == goal_context)
    return [
        {"type": m.memory_type, "content": m.content, "goal": m.goal_context}
        for m in q.all()
    ]


def record_memory(
    db: Session,
    user_id: int,
    memory_type: str,
    content: str,
    goal_context: Optional[str] = None,
) -> None:
    db.add(
        AgentMemory(
            user_id=user_id,
            memory_type=memory_type,
            content=content,
            goal_context=goal_context,
            expires_at=datetime.utcnow() + timedelta(days=30),
        )
    )
    db.commit()


def purge_expired(db: Session, user_id: int) -> None:
    db.query(AgentMemory).filter(
        AgentMemory.user_id == user_id,
        AgentMemory.expires_at <= datetime.utcnow(),
    ).delete()
    db.commit()
