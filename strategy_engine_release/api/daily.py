"""POST /api/daily-calc — generate today's coaching using the 4-agent pipeline.

Cache logic:
  - Cache key: (user_id, goal, profile_mbti, profile_hd_type, profile_birthdate, target_date)
  - On cache hit  → return stored result (0 AI tokens)
  - On TH request → translate EN→TH on first request, cache TH for subsequent calls
"""

from datetime import date as date_type

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from agents.pipeline import run_pipeline
from core.database import get_db
from core.deps import get_current_user
from models.orm import Recommendation, User
from models.schemas import CoachingResponse, DailyCalcRequest
from services.energy_context import compute_energy_context
from services.mbti import mbti_to_element
from services.recommendation_service import save_recommendation
from services.saju import calculate_birth_chart, calculate_day_pillar
from services.scoring import calculate_action_score

router = APIRouter()


def _dominant_function(mbti: str) -> str:
    from services.mbti import get_dominant_function
    return get_dominant_function(mbti)


@router.post("/daily-calc", response_model=CoachingResponse)
def daily_calc(
    req: DailyCalcRequest,
    current: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> CoachingResponse:
    profile = current.profile
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_412_PRECONDITION_FAILED,
            detail="Create a profile first via POST /api/profile.",
        )

    lang = req.lang  # "en" or "th"

    # ── Cache check ──────────────────────────────────────────────────────────
    cached = db.query(Recommendation).filter(
        Recommendation.user_id          == current.id,
        Recommendation.goal             == req.goal.value,
        Recommendation.profile_mbti     == profile.mbti,
        Recommendation.profile_hd_type  == profile.hd_type,
        Recommendation.profile_birthdate == profile.birthdate,
        func.date(Recommendation.created_at) == req.target_date,
    ).first()

    if cached:
        # If TH requested but cache has no TH content → fall through to regenerate
        if lang == "th" and not cached.coaching_summary_th:
            pass  # regenerate below
        else:
            return CoachingResponse.from_orm_row(cached, lang=lang)
    # ────────────────────────────────────────────────────────────────────────

    # BaZi chart + day pillar
    chart         = calculate_birth_chart(profile.birthdate, profile.birth_time)
    day_master    = chart["day_master"]
    mbti_element  = mbti_to_element(profile.mbti)
    day_stem, _   = calculate_day_pillar(req.target_date)
    daily_element = day_stem

    score_result = calculate_action_score(
        day_master    = day_master,
        daily_element = daily_element,
        mbti_element  = mbti_element,
        mbti_dominant = _dominant_function(profile.mbti),
        goal          = req.goal.value,
        energy_input  = req.energy_level,
        hd_aligned    = req.hd_aligned,
    )
    bazi_score = round(score_result["score"] / 10.0, 2)
    goal_str   = req.goal.value

    # ── DB-first energy context (zero AI tokens) ─────────────────────────────
    # Computes stance, planetary hour, direction, colour — all from calendar math.
    # The LLM receives pre-resolved values and synthesises narrative only.
    energy = compute_energy_context(
        day_master=day_master,
        day_element=daily_element,
        birthdate=profile.birthdate,
        goal=goal_str,
        target_date=req.target_date,
        hd_type=profile.hd_type,
    )

    # Run AI pipeline
    pipeline_result = run_pipeline(
        db=db,
        user_id=current.id,
        mbti_type=profile.mbti,
        hd_type=profile.hd_type,
        personal_color=getattr(profile, "personal_color", None),
        goal=goal_str,
        bazi_score=bazi_score,
        day_master=str(day_master),
        daily_element=str(daily_element),
        # ── New pre-computed fields ──
        stance=energy.stance,
        stance_th=energy.stance_th,
        strong_day=energy.strong_day,
        lead_colour=energy.lead_colour,
        lead_colour_hex=energy.lead_colour_hex,
        secondary_colour=energy.secondary_colour,
        power_direction=energy.power_direction,
        planetary_hour_ruler=energy.planetary_hour_ruler,
        planetary_hour_best_for=energy.planetary_hour_best_for,
        planetary_hour_avoid=energy.planetary_hour_avoid,
        peak_hour_window=energy.peak_hour_window,
        thai_day_ruler=energy.thai_day_ruler,
        saturn_note=energy.saturn_note,
    )

    # Save EN + TH together (both generated in single AI call)
    saved_rec = save_recommendation(
        db=db,
        user_id=current.id,
        goal=goal_str,
        bazi_score=pipeline_result.bazi_score,
        variation_seed=pipeline_result.variation_seed,
        variation_angle=pipeline_result.variation_angle,
        behavior_recommendation=pipeline_result.behavior_recommendation,
        timing_guidance=pipeline_result.timing_guidance,
        communication_strategy=pipeline_result.communication_strategy,
        warnings=pipeline_result.warnings,
        practical_tips=pipeline_result.practical_tips,
        sample_sentences=pipeline_result.sample_sentences,
        alternative_responses=pipeline_result.alternative_responses,
        coaching_summary=pipeline_result.coaching_summary,
        generation_model=pipeline_result.generation_model,
        generation_ms=pipeline_result.generation_ms,
        profile_mbti=profile.mbti,
        profile_hd_type=profile.hd_type,
        profile_birthdate=profile.birthdate,
        behavior_recommendation_th=pipeline_result.behavior_recommendation_th,
        timing_guidance_th=pipeline_result.timing_guidance_th,
        communication_strategy_th=pipeline_result.communication_strategy_th,
        warnings_th=pipeline_result.warnings_th,
        practical_tips_th=pipeline_result.practical_tips_th,
        sample_sentences_th=pipeline_result.sample_sentences_th,
        alternative_responses_th=pipeline_result.alternative_responses_th,
        coaching_summary_th=pipeline_result.coaching_summary_th,
    )

    return CoachingResponse.from_orm_row(saved_rec, lang=lang)
