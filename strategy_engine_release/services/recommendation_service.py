"""Persist and retrieve coaching recommendations + user feedback."""

from typing import Optional

from sqlalchemy.orm import Session

from models.orm import Recommendation, RecommendationFeedback


def save_recommendation(
    db: Session,
    user_id: int,
    goal: str,
    bazi_score: float,
    variation_seed: str,
    variation_angle: str,
    behavior_recommendation: str,
    timing_guidance: str,
    communication_strategy: str,
    warnings: list[str],
    practical_tips: list[str],
    sample_sentences: list[str],
    alternative_responses: list[str],
    coaching_summary: str,
    generation_model: str,
    generation_ms: int,
    profile_mbti: Optional[str] = None,
    profile_hd_type: Optional[str] = None,
    profile_birthdate=None,
    # TH translations
    behavior_recommendation_th: str = "",
    timing_guidance_th: str = "",
    communication_strategy_th: str = "",
    warnings_th: list[str] = None,
    practical_tips_th: list[str] = None,
    sample_sentences_th: list[str] = None,
    alternative_responses_th: list[str] = None,
    coaching_summary_th: str = "",
) -> Recommendation:
    def _join(lst): return " | ".join(lst) if lst else ""
    rec = Recommendation(
        user_id=user_id,
        goal=goal,
        variation_seed=variation_seed,
        variation_angle=variation_angle,
        bazi_score=bazi_score,
        behavior_recommendation=behavior_recommendation,
        timing_guidance=timing_guidance,
        communication_strategy=communication_strategy,
        warnings=" | ".join(warnings),
        practical_tips=" | ".join(practical_tips),
        sample_sentences=" | ".join(sample_sentences),
        alternative_responses=" | ".join(alternative_responses),
        coaching_summary=coaching_summary,
        generation_model=generation_model,
        generation_ms=generation_ms,
        profile_mbti=profile_mbti,
        profile_hd_type=profile_hd_type,
        profile_birthdate=profile_birthdate,
        behavior_recommendation_th=behavior_recommendation_th,
        timing_guidance_th=timing_guidance_th,
        communication_strategy_th=communication_strategy_th,
        warnings_th=_join(warnings_th or []),
        practical_tips_th=_join(practical_tips_th or []),
        sample_sentences_th=_join(sample_sentences_th or []),
        alternative_responses_th=_join(alternative_responses_th or []),
        coaching_summary_th=coaching_summary_th,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec


def save_feedback(
    db: Session,
    recommendation_id: int,
    user_id: int,
    rating: int,
    feedback_text: Optional[str],
) -> RecommendationFeedback:
    fb = RecommendationFeedback(
        recommendation_id=recommendation_id,
        user_id=user_id,
        rating=rating,
        feedback_text=feedback_text,
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


def get_user_recommendations(
    db: Session, user_id: int, limit: int = 10
) -> list[Recommendation]:
    return (
        db.query(Recommendation)
          .filter_by(user_id=user_id)
          .order_by(Recommendation.created_at.desc())
          .limit(limit)
          .all()
    )
