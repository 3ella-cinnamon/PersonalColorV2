"""Translate a coaching recommendation EN → TH using the available AI provider.

Translates all text fields in one API call to minimise token usage.
Stores results back to the recommendation row and commits.
"""

import json
from sqlalchemy.orm import Session
from models.orm import Recommendation
from agents.pipeline import _call_ai

_SYSTEM = """You are a professional Thai translator specialising in coaching and personal development content.

Rules:
- Translate naturally — not word-for-word. Sound like a Thai life coach.
- Keep proper nouns (MBTI types, Human Design types, BaZi, Personal Color) in English.
- Pipe-separated lists must stay pipe-separated in the output.
- Respond in JSON only, same keys as input.
- Use formal but warm Thai (ภาษาไทยสุภาพแต่เป็นกันเอง).
"""


def _join(items: list[str]) -> str:
    return " | ".join(items) if items else ""


def translate_recommendation(db: Session, rec: Recommendation) -> Recommendation:
    """Translate EN fields → TH, save to DB, return updated rec."""

    def _split(val: str | None) -> list[str]:
        return [x.strip() for x in val.split("|")] if val else []

    payload = {
        "behavior_recommendation": rec.behavior_recommendation or "",
        "timing_guidance":         rec.timing_guidance or "",
        "communication_strategy":  rec.communication_strategy or "",
        "warnings":                rec.warnings or "",
        "practical_tips":          rec.practical_tips or "",
        "sample_sentences":        rec.sample_sentences or "",
        "alternative_responses":   rec.alternative_responses or "",
        "coaching_summary":        rec.coaching_summary or "",
    }

    user_prompt = (
        "Translate all values in this JSON object to Thai. "
        "Return the same JSON structure with Thai values.\n\n"
        + json.dumps(payload, ensure_ascii=False)
    )

    try:
        result, _ = _call_ai(_SYSTEM, user_prompt)
    except Exception as e:
        print(f"[translation] Failed: {e}")
        return rec

    rec.behavior_recommendation_th = result.get("behavior_recommendation", "")
    rec.timing_guidance_th         = result.get("timing_guidance", "")
    rec.communication_strategy_th  = result.get("communication_strategy", "")
    rec.warnings_th                = result.get("warnings", "")
    rec.practical_tips_th          = result.get("practical_tips", "")
    rec.sample_sentences_th        = result.get("sample_sentences", "")
    rec.alternative_responses_th   = result.get("alternative_responses", "")
    rec.coaching_summary_th        = result.get("coaching_summary", "")

    db.commit()
    db.refresh(rec)
    return rec
