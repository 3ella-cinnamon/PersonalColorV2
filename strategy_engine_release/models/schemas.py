"""Pydantic v2 request/response schemas.

Three groups:
  1. Auth        : signup, login, token, current-user
  2. Profile     : create / update / read user profile + computed blueprint
  3. Daily calc  : runtime inputs and the score response
"""

from datetime import date, datetime, time
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from models.domain import Element, Goal, InteractionType, Strategy


VALID_MBTI = {
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
}

VALID_HD_TYPES = {
    "Generator", "Manifesting Generator", "Manifestor", "Projector", "Reflector",
}


# ============================================================
# 1.  Auth   (ProfileRead forward-ref resolved after its definition)
# ============================================================

class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class LoginResponse(BaseModel):
    """Response to /api/auth/login and /api/auth/signup.

    `profile` is populated on login when a profile already exists so the
    client never needs a separate GET /api/profile call.
    """
    access_token: str
    token_type: str = "bearer"
    has_profile: bool = Field(
        default=False,
        description="True if the user already has a profile — frontend can skip onboarding.",
    )
    profile: Optional["ProfileRead"] = Field(
        default=None,
        description="Populated on login when a profile exists; None otherwise.",
    )


class CurrentUser(BaseModel):
    """Returned by GET /api/auth/me."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    created_at: datetime
    has_profile: bool = False


# ============================================================
# 2.  Profile
# ============================================================

class ProfileCreate(BaseModel):
    """Body for POST /api/profile and PUT /api/profile."""
    birthdate:  date
    birth_time: time = Field(..., alias="time")
    birthplace: Optional[str] = Field(default=None, max_length=200)
    mbti:       str = Field(..., min_length=4, max_length=4)
    hd_type:    Optional[str] = None
    personal_color: Optional[str] = None
    blood_type: Optional[str] = Field(default=None, max_length=3)

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("mbti")
    @classmethod
    def _v_mbti(cls, v: str) -> str:
        v = v.upper()
        if v not in VALID_MBTI:
            raise ValueError(f"Invalid MBTI type: {v}")
        return v

    @field_validator("hd_type")
    @classmethod
    def _v_hd(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return None
        if v not in VALID_HD_TYPES:
            raise ValueError(
                f"Invalid HD type: {v}. Must be one of {sorted(VALID_HD_TYPES)}"
            )
        return v


class ProfileRead(BaseModel):
    """Raw profile record."""
    model_config = ConfigDict(from_attributes=True)

    birthdate:  date
    birth_time: time
    birthplace: Optional[str]
    mbti:       str
    hd_type:    Optional[str]
    personal_color: Optional[str] = None
    blood_type: Optional[str]
    updated_at: datetime


# --- Computed blueprint (the same shape v1 returned from /api/onboarding) ---

class Pillar(BaseModel):
    stem: Element
    branch: Element


class BirthChart(BaseModel):
    day_master: Element
    pillars: dict[str, Pillar]
    element_counts: dict[Element, int]
    dominant_elements: list[Element]
    weak_elements: list[Element]


class EnergyBlueprint(BaseModel):
    """Computed from the user's stored profile. Returned by GET /api/profile/blueprint."""
    mbti: str
    mbti_dominant_function: str
    mbti_element: Element
    hd_type: Optional[str]
    birth_chart: BirthChart


# ============================================================
# 3.  Daily calc
# ============================================================

class DailyCalcRequest(BaseModel):
    target_date: date
    goal: Goal
    energy_level: int = Field(..., ge=1, le=10)
    hd_aligned: Optional[bool] = None
    sub_goal: Optional[str] = None
    lang: str = Field(default="en", pattern="^(en|th)$")


class ScoreComponents(BaseModel):
    E_bazi: float
    E_mian: float
    M_hd: float
    M_cog: float
    weighted_base: float


class DecisionRule(BaseModel):
    """One row from the criteria tables, surfaced in the daily response."""
    preference: str
    decision: str
    weight: float


class BlendedDecisionRule(BaseModel):
    """A single decision rule tagged with its source (mbti or hd) and optional goal."""
    source: str
    preference: str
    decision: str
    weight: float
    goal: Optional[str] = None


class ConflictScenario(BaseModel):
    """Blend summary + conflict/recommendation pair for a specific MBTI × HD combination."""
    mbti_type: str
    hd_type: str
    blend_summary: str
    conflict_situation: str
    conflict_sentence: str
    recommended_sentence: str
    recommended_action: str


class DailyCalcResponse(BaseModel):
    interaction_score: float
    todays_dominant_element: Element
    interaction_type: InteractionType
    strategy_mode: Strategy
    day_master: Element
    components: ScoreComponents
    mbti_decisions: list[DecisionRule] = []
    hd_decisions: list[DecisionRule] = []
    blended_decisions: list[BlendedDecisionRule] = []
    scenario: Optional[ConflictScenario] = None
    mbti_sub_tip: Optional[str] = None
    hd_sub_tip: Optional[str] = None
    mbti_description:    Optional[str] = None
    hd_description:      Optional[str] = None
    tension:             Optional[str] = None
    conflict_example:    Optional[str] = None
    why_fails:           Optional[str] = None
    recommended_example: Optional[str] = None
    the_shift:           Optional[str] = None


class MbtiTypeProfileOut(BaseModel):
    """Rich reference profile for an MBTI type. Pipe-separated fields are arrays."""
    model_config = ConfigDict(from_attributes=True)

    type_code:  str
    type_name:  str
    group_name: str
    population_percent: str

    dominant_function:  Optional[str] = None
    auxiliary_function: Optional[str] = None
    tertiary_function:  Optional[str] = None
    inferior_function:  Optional[str] = None

    core_motivation: Optional[str] = None
    core_desire:     Optional[str] = None
    core_fear:       Optional[str] = None
    worldview:       Optional[str] = None

    information_processing:  Optional[str] = None
    decision_making:         Optional[str] = None
    communication_style:     Optional[str] = None
    leadership_style:        Optional[str] = None
    conflict_style:          Optional[str] = None
    relationship_style:      Optional[str] = None
    parenting_style:         Optional[str] = None
    learning_style:          Optional[str] = None
    work_style:              Optional[str] = None

    career_patterns:   Optional[str] = None
    strengths:         Optional[str] = None
    weaknesses:        Optional[str] = None
    blind_spots:       Optional[str] = None
    stress_behavior:   Optional[str] = None
    growth_path:       Optional[str] = None
    ideal_environment: Optional[str] = None

    burnout_pattern:         Optional[str] = None
    emotional_pattern:       Optional[str] = None
    team_role:               Optional[str] = None
    ideal_manager:           Optional[str] = None
    worst_manager:           Optional[str] = None
    financial_behavior:      Optional[str] = None
    innovation_style:        Optional[str] = None
    change_management_style: Optional[str] = None
    risk_tolerance:          Optional[str] = None
    scientific_evidence_level: Optional[str] = None
    long_description:        Optional[str] = None


class HdTypeProfileOut(BaseModel):
    """Full reference profile for a Human Design type."""
    model_config = ConfigDict(from_attributes=True)

    hd_type:            str
    population_percent: str
    core_purpose:       str
    energy_pattern:     str
    strategy:           str
    signature:          str
    not_self:           str
    strengths:          str
    challenges:         str
    work_style:         str
    leadership_style:   str
    decision_making:    str
    relationship_style: str
    growth_path:        str
    environment_needs:  str
    stress_behavior:    str
    long_description:   str


class PersonalColorProfileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    season: str
    sub_types: Optional[str] = None
    energy_tone: str
    impression: Optional[str] = None
    communication_vibe: Optional[str] = None
    language_style: Optional[str] = None
    best_colors: Optional[str] = None
    avoid_styles: Optional[str] = None
    social_energy: Optional[str] = None
    coaching_notes: Optional[str] = None


class CoachingResponse(BaseModel):
    id: int
    goal: str
    lang: str = "en"
    bazi_score: Optional[float] = None
    behavior_recommendation: Optional[str] = None
    timing_guidance: Optional[str] = None
    communication_strategy: Optional[str] = None
    warnings: list[str] = []
    practical_tips: list[str] = []
    sample_sentences: list[str] = []
    alternative_responses: list[str] = []
    coaching_summary: Optional[str] = None
    has_thai: bool = False                  # tells frontend whether TH version is ready
    generation_model: Optional[str] = None
    generation_ms: Optional[int] = None
    created_at: Optional[datetime] = None

    @classmethod
    def from_orm_row(cls, row, lang: str = "en") -> "CoachingResponse":
        def _split(val):
            return [x.strip() for x in val.split("|")] if val else []

        has_th = bool(row.coaching_summary_th)

        if lang == "th" and has_th:
            return cls(
                id=row.id, goal=row.goal, lang="th",
                bazi_score=row.bazi_score,
                behavior_recommendation=row.behavior_recommendation_th,
                timing_guidance=row.timing_guidance_th,
                communication_strategy=row.communication_strategy_th,
                warnings=_split(row.warnings_th),
                practical_tips=_split(row.practical_tips_th),
                sample_sentences=_split(row.sample_sentences_th),
                alternative_responses=_split(row.alternative_responses_th),
                coaching_summary=row.coaching_summary_th,
                has_thai=True,
                generation_model=row.generation_model,
                generation_ms=row.generation_ms,
                created_at=row.created_at,
            )
        return cls(
            id=row.id, goal=row.goal, lang="en",
            bazi_score=row.bazi_score,
            behavior_recommendation=row.behavior_recommendation,
            timing_guidance=row.timing_guidance,
            communication_strategy=row.communication_strategy,
            warnings=_split(row.warnings),
            practical_tips=_split(row.practical_tips),
            sample_sentences=_split(row.sample_sentences),
            alternative_responses=_split(row.alternative_responses),
            coaching_summary=row.coaching_summary,
            has_thai=has_th,
            generation_model=row.generation_model,
            generation_ms=row.generation_ms,
            created_at=row.created_at,
        )


class FeedbackRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    feedback_text: Optional[str] = None


class GoalDefinition(BaseModel):
    id: str
    label: str
    description: str


# Resolve the forward reference in LoginResponse → ProfileRead
LoginResponse.model_rebuild()
