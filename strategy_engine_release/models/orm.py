"""SQLAlchemy ORM models — the database schema.

Tables:
  - users              : auth credentials (email + bcrypt hash)
  - user_profiles      : user's static birth/personality data
  - mbti_criteria      : MBTI type → preference → decision rule (goal-aware)
  - hd_criteria        : Human Design type → preference → decision rule (goal-aware)
  - mbti_hd_scenarios  : 16×5 = 80 MBTI+HD blend/conflict/recommendation rows
"""

from datetime import date, datetime, time
from typing import Optional

from sqlalchemy import (
    Date, DateTime, Float, ForeignKey, String, Text, Time, func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    profile: Mapped[Optional["UserProfile"]] = relationship(
        "UserProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id:      Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)

    birthdate:  Mapped[date] = mapped_column(Date, nullable=False)
    birth_time: Mapped[time] = mapped_column(Time, nullable=False)
    birthplace: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    mbti:       Mapped[str] = mapped_column(String(4), nullable=False)
    hd_type:    Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    personal_color: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    blood_type: Mapped[Optional[str]] = mapped_column(String(3), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship("User", back_populates="profile")


class MbtiCriterion(Base):
    """Lookup rule: for an MBTI type, what's the preference, and what decision applies?

    goal=None  → general rule, returned for every goal.
    goal='work'/'money'/'relationship' → returned only when that goal is active.
    """
    __tablename__ = "mbti_criteria"

    id:         Mapped[int] = mapped_column(primary_key=True)
    mbti_type:  Mapped[str] = mapped_column(String(4), index=True, nullable=False)
    preference: Mapped[str] = mapped_column(String(100), nullable=False)
    decision:   Mapped[str] = mapped_column(Text, nullable=False)
    weight:     Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    goal:       Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)


class HdCriterion(Base):
    """Lookup rule: for a Human Design type, what's the preference, and what decision applies?

    goal=None  → general rule, returned for every goal.
    goal='work'/'money'/'relationship' → returned only when that goal is active.
    """
    __tablename__ = "hd_criteria"

    id:         Mapped[int] = mapped_column(primary_key=True)
    hd_type:    Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    preference: Mapped[str] = mapped_column(String(100), nullable=False)
    decision:   Mapped[str] = mapped_column(Text, nullable=False)
    weight:     Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    goal:       Mapped[Optional[str]] = mapped_column(String(20), nullable=True, index=True)


class MbtiTypeProfile(Base):
    """Rich reference profile for each MBTI type. Arrays stored as pipe-separated text."""
    __tablename__ = "mbti_type_profiles"

    id:         Mapped[int] = mapped_column(primary_key=True)
    type_code:  Mapped[str] = mapped_column(String(4),  unique=True, index=True, nullable=False)
    type_name:  Mapped[str] = mapped_column(String(50), nullable=False)
    group_name: Mapped[str] = mapped_column(String(50), nullable=False)
    population_percent: Mapped[str] = mapped_column(String(100), nullable=False)

    dominant_function:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    auxiliary_function: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tertiary_function:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    inferior_function:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    core_motivation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    core_desire:     Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    core_fear:       Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    worldview:       Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    information_processing:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    decision_making:         Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    communication_style:     Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    leadership_style:        Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    conflict_style:          Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    relationship_style:      Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    parenting_style:         Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    learning_style:          Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    work_style:              Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Pipe-separated list fields
    career_patterns:    Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    strengths:          Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    weaknesses:         Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    blind_spots:        Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    stress_behavior:    Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    growth_path:        Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ideal_environment:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    burnout_pattern:         Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    emotional_pattern:       Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    team_role:               Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    ideal_manager:           Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    worst_manager:           Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    financial_behavior:      Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    innovation_style:        Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    change_management_style: Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    risk_tolerance:          Mapped[Optional[str]] = mapped_column(Text,        nullable=True)
    scientific_evidence_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    long_description:        Mapped[Optional[str]] = mapped_column(Text,        nullable=True)


class HdTypeProfile(Base):
    """Static reference profile for each Human Design type (one row per type)."""
    __tablename__ = "hd_type_profiles"

    id:                 Mapped[int] = mapped_column(primary_key=True)
    hd_type:            Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    population_percent: Mapped[str] = mapped_column(String(50), nullable=False)
    core_purpose:       Mapped[str] = mapped_column(Text, nullable=False)
    energy_pattern:     Mapped[str] = mapped_column(Text, nullable=False)
    strategy:           Mapped[str] = mapped_column(Text, nullable=False)
    signature:          Mapped[str] = mapped_column(Text, nullable=False)
    not_self:           Mapped[str] = mapped_column(Text, nullable=False)
    strengths:          Mapped[str] = mapped_column(Text, nullable=False)
    challenges:         Mapped[str] = mapped_column(Text, nullable=False)
    work_style:         Mapped[str] = mapped_column(Text, nullable=False)
    leadership_style:   Mapped[str] = mapped_column(Text, nullable=False)
    decision_making:    Mapped[str] = mapped_column(Text, nullable=False)
    relationship_style: Mapped[str] = mapped_column(Text, nullable=False)
    growth_path:        Mapped[str] = mapped_column(Text, nullable=False)
    environment_needs:  Mapped[str] = mapped_column(Text, nullable=False)
    stress_behavior:    Mapped[str] = mapped_column(Text, nullable=False)
    long_description:   Mapped[str] = mapped_column(Text, nullable=False)


class MbtiHdScenario(Base):
    """One blend/conflict/recommendation row per (MBTI type × HD type) pair.

    80 rows total: 16 MBTI × 5 HD types.
    Surfaced in /api/daily-calc when a user's profile has both MBTI and HD set.
    """
    __tablename__ = "mbti_hd_scenarios"

    id:                   Mapped[int] = mapped_column(primary_key=True)
    mbti_type:            Mapped[str] = mapped_column(String(4), index=True, nullable=False)
    hd_type:              Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    blend_summary:        Mapped[str] = mapped_column(Text, nullable=False)
    conflict_situation:   Mapped[str] = mapped_column(Text, nullable=False)
    conflict_sentence:    Mapped[str] = mapped_column(Text, nullable=False)
    recommended_sentence: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action:   Mapped[str] = mapped_column(Text, nullable=False)


class PersonalColorProfile(Base):
    __tablename__ = "personal_color_profiles"
    season: Mapped[str] = mapped_column(String(20), primary_key=True)
    sub_types: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    energy_tone: Mapped[str] = mapped_column(String(50), nullable=False)
    impression: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    communication_vibe: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    language_style: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    best_colors: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    avoid_styles: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    social_energy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coaching_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class Recommendation(Base):
    __tablename__ = "recommendations"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    goal: Mapped[str] = mapped_column(String(50), nullable=False)
    variation_seed: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    variation_angle: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    bazi_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # ── EN content ───────────────────────────────────────────
    behavior_recommendation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timing_guidance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    communication_strategy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    warnings: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    practical_tips: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sample_sentences: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alternative_responses: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coaching_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── TH translations (populated on first TH request) ──────
    behavior_recommendation_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    timing_guidance_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    communication_strategy_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    warnings_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    practical_tips_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sample_sentences_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    alternative_responses_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    coaching_summary_th: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # ── Cache key snapshot ────────────────────────────────────
    profile_mbti: Mapped[Optional[str]] = mapped_column(String(4), nullable=True)
    profile_hd_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    profile_birthdate: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    generation_model: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    generation_ms: Mapped[Optional[int]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    user: Mapped["User"] = relationship("User")


class APILog(Base):
    """One row per inbound API request — URL, response snapshot, timing."""
    __tablename__ = "api_logs"

    id:            Mapped[int]           = mapped_column(primary_key=True)
    method:        Mapped[str]           = mapped_column(String(10),  nullable=False)
    url:           Mapped[str]           = mapped_column(String(500), nullable=False, index=True)
    status_code:   Mapped[int]           = mapped_column(nullable=False, index=True)
    request_body:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    response_body: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # truncated at 4 KB
    duration_ms:   Mapped[int]           = mapped_column(nullable=False)
    created_at:    Mapped[datetime]      = mapped_column(DateTime, server_default=func.now(), index=True)


class RecommendationFeedback(Base):
    __tablename__ = "recommendation_feedback"
    id: Mapped[int] = mapped_column(primary_key=True)
    recommendation_id: Mapped[int] = mapped_column(ForeignKey("recommendations.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    feedback_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())


class AgentMemory(Base):
    __tablename__ = "agent_memories"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    memory_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    goal_context: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)


# ── Consult & Healing — Adaptive Assessment ──────────────────────────────────

class AssessmentNode(Base):
    """One row per node in the adaptive decision tree.

    node_type: single_select | scale_set | likert_set | checkbox_set | terminal
    scale_labels_json / scale_values_json: JSON arrays, null for single_select.
    scoring_rules_json: JSON object describing how to score answers and pick next node.
    """
    __tablename__ = "assessment_nodes"

    node_id:            Mapped[str]           = mapped_column(String(60), primary_key=True)
    node_type:          Mapped[str]           = mapped_column(String(20), nullable=False)
    instrument:         Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    label:              Mapped[str]           = mapped_column(Text, nullable=False)
    rationale:          Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence:           Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    trigger_warning:    Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scale_labels_json:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scale_values_json:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    scoring_rules_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    questions: Mapped[list["AssessmentQuestion"]] = relationship(
        "AssessmentQuestion", back_populates="node",
        order_by="AssessmentQuestion.sort_order",
        cascade="all, delete-orphan",
    )
    options: Mapped[list["AssessmentOption"]] = relationship(
        "AssessmentOption", back_populates="node",
        order_by="AssessmentOption.sort_order",
        cascade="all, delete-orphan",
    )


class AssessmentQuestion(Base):
    """One row per item within a scale/likert/checkbox node."""
    __tablename__ = "assessment_questions"

    id:             Mapped[int]           = mapped_column(primary_key=True)
    node_id:        Mapped[str]           = mapped_column(ForeignKey("assessment_nodes.node_id"), nullable=False, index=True)
    question_id:    Mapped[str]           = mapped_column(String(30), nullable=False)
    text:           Mapped[str]           = mapped_column(Text, nullable=False)
    subscale:       Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    reverse_scored: Mapped[bool]          = mapped_column(default=False, nullable=False)
    safety_item:    Mapped[bool]          = mapped_column(default=False, nullable=False)
    sort_order:     Mapped[int]           = mapped_column(default=0, nullable=False)

    node: Mapped["AssessmentNode"] = relationship("AssessmentNode", back_populates="questions")


class AssessmentOption(Base):
    """One row per choice in a single_select or checkbox_set node."""
    __tablename__ = "assessment_options"

    id:           Mapped[int]           = mapped_column(primary_key=True)
    node_id:      Mapped[str]           = mapped_column(ForeignKey("assessment_nodes.node_id"), nullable=False, index=True)
    option_id:    Mapped[str]           = mapped_column(String(40), nullable=False)
    label:        Mapped[str]           = mapped_column(Text, nullable=False)
    next_node_id: Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    flag:         Mapped[Optional[str]] = mapped_column(String(60), nullable=True)
    sort_order:   Mapped[int]           = mapped_column(default=0, nullable=False)

    node: Mapped["AssessmentNode"] = relationship("AssessmentNode", back_populates="options")


class AssessmentSession(Base):
    """Tracks one user's in-progress or completed assessment run."""
    __tablename__ = "assessment_sessions"

    id:                  Mapped[int]           = mapped_column(primary_key=True)
    user_id:             Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    current_node_id:     Mapped[str]           = mapped_column(String(60), nullable=False)
    flags_json:          Mapped[str]           = mapped_column(Text, default="[]", nullable=False)
    scores_json:         Mapped[str]           = mapped_column(Text, default="{}", nullable=False)
    visited_nodes_json:  Mapped[str]           = mapped_column(Text, default="[]", nullable=False)
    status:              Mapped[str]           = mapped_column(String(20), default="in_progress", nullable=False)
    created_at:          Mapped[datetime]      = mapped_column(DateTime, server_default=func.now())
    updated_at:          Mapped[datetime]      = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user:    Mapped["User"]                    = relationship("User")
    answers: Mapped[list["AssessmentAnswer"]]  = relationship(
        "AssessmentAnswer", back_populates="session", cascade="all, delete-orphan"
    )
    profile: Mapped[Optional["AssessmentProfile"]] = relationship(
        "AssessmentProfile", back_populates="session", uselist=False, cascade="all, delete-orphan"
    )


class AssessmentAnswer(Base):
    """One row per answered item (question or option selection)."""
    __tablename__ = "assessment_answers"

    id:          Mapped[int]           = mapped_column(primary_key=True)
    session_id:  Mapped[int]           = mapped_column(ForeignKey("assessment_sessions.id"), nullable=False, index=True)
    node_id:     Mapped[str]           = mapped_column(String(60), nullable=False)
    question_id: Mapped[str]           = mapped_column(String(30), nullable=False)
    value:       Mapped[float]         = mapped_column(Float, nullable=False)
    text_value:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at:  Mapped[datetime]      = mapped_column(DateTime, server_default=func.now())

    session: Mapped["AssessmentSession"] = relationship("AssessmentSession", back_populates="answers")


class AssessmentProfile(Base):
    """Completed psychological profile — generated once all nodes are visited."""
    __tablename__ = "assessment_profiles"

    id:           Mapped[int]           = mapped_column(primary_key=True)
    session_id:   Mapped[int]           = mapped_column(ForeignKey("assessment_sessions.id"), unique=True, nullable=False)
    user_id:      Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    profile_json: Mapped[str]           = mapped_column(Text, nullable=False)
    ai_summary:   Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at:   Mapped[datetime]      = mapped_column(DateTime, server_default=func.now())

    session: Mapped["AssessmentSession"] = relationship("AssessmentSession", back_populates="profile")
    user:    Mapped["User"]              = relationship("User")


# ── AEHQ v2.0 — Adaptive Emotional Self-Reflection Questionnaire ──────────────

class AEHQSession(Base):
    """One AEHQ session per emotional check-in.

    state_json stores the full mutable state: track (D/S/R), running scores,
    question queue, emotion words, body data, if-then text, etc.
    """
    __tablename__ = "aehq_sessions"

    id:         Mapped[int]           = mapped_column(primary_key=True)
    user_id:    Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    next_step:  Mapped[str]           = mapped_column(String(40), default="CONSENT", nullable=False)
    state_json: Mapped[str]           = mapped_column(Text, default="{}", nullable=False)
    status:     Mapped[str]           = mapped_column(String(20), default="active", nullable=False)
    # status: active | complete | crisis_exit | grounding_pause

    # ── Informed consent (PDPA) — captured at the CONSENT gate ──
    consent_agreed:  Mapped[bool] = mapped_column(default=False, nullable=False)   # required to proceed
    training_opt_in: Mapped[bool] = mapped_column(default=False, nullable=False)   # SEPARATE opt-in
    consent_at:      Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    user:      Mapped["User"]                 = relationship("User")
    responses: Mapped[list["AEHQResponse"]]   = relationship(
        "AEHQResponse", back_populates="session",
        cascade="all, delete-orphan", order_by="AEHQResponse.created_at",
    )
    result: Mapped[Optional["AEHQResult"]] = relationship(
        "AEHQResult", back_populates="session", uselist=False, cascade="all, delete-orphan",
    )


class AEHQResponse(Base):
    """One row per screen answered within an AEHQ session."""
    __tablename__ = "aehq_responses"

    id:          Mapped[int]  = mapped_column(primary_key=True)
    session_id:  Mapped[int]  = mapped_column(ForeignKey("aehq_sessions.id"), nullable=False, index=True)
    step:        Mapped[str]  = mapped_column(String(40), nullable=False)
    answer_json: Mapped[str]  = mapped_column(Text, nullable=False)
    # Provenance — required to make consented answers usable as training data
    content_version: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)  # e.g. "aehq-2.2.1"
    lang_shown:      Mapped[Optional[str]] = mapped_column(String(8),  nullable=True)  # th / en — what the user saw
    created_at:  Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    session: Mapped["AEHQSession"] = relationship("AEHQSession", back_populates="responses")


class AEHQResult(Base):
    """Final computed result for a completed AEHQ session."""
    __tablename__ = "aehq_results"

    id:         Mapped[int]           = mapped_column(primary_key=True)
    session_id: Mapped[int]           = mapped_column(ForeignKey("aehq_sessions.id"), unique=True, nullable=False)
    user_id:    Mapped[int]           = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    framework_code: Mapped[Optional[str]] = mapped_column(String(20),  nullable=True)
    framework_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    situation_key:  Mapped[Optional[str]] = mapped_column(String(40),  nullable=True)
    track:          Mapped[Optional[str]] = mapped_column(String(2),   nullable=True)

    hypothesis_text:    Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    technique_text:     Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    evidence_text:      Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ifthen_text:        Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    selfcompassion_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    closure_text:       Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    suds_start:  Mapped[Optional[int]] = mapped_column(nullable=True)
    suds_end:    Mapped[Optional[int]] = mapped_column(nullable=True)
    scores_json: Mapped[str]           = mapped_column(Text, default="{}", nullable=False)
    exit_type:   Mapped[str]           = mapped_column(String(20), default="complete", nullable=False)

    # Trauma-informed flags (detect/route, never probe)
    trauma_flagged:   Mapped[bool] = mapped_column(default=False, nullable=False)
    referral_offered: Mapped[bool] = mapped_column(default=False, nullable=False)
    # 2Q-derived low-mood pattern (support routing, never a diagnosis label)
    low_mood_flagged: Mapped[bool] = mapped_column(default=False, nullable=False)
    # TDS-grounded chasing/gambling-harm pattern (trading situation only)
    chasing_flagged:  Mapped[bool] = mapped_column(default=False, nullable=False)
    # Client's own-words goal (S1 anchor) — stored raw + its language tag
    goal_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    goal_lang: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)  # th / en / mixed
    # Content provenance — which content version produced this result
    content_version: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # Bottom Line (S2 formulation) — the negative core belief + belief-strength %
    bottom_line_text:   Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    bottom_line_belief: Mapped[Optional[int]] = mapped_column(nullable=True)   # 0–100 %
    bottom_line_lang:   Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    # Automatic thought (S3-S4) — the user's own-words thought; with trigger +
    # emotion_words + suds pre/post this completes the structured thought record.
    thought_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    thought_lang: Mapped[Optional[str]] = mapped_column(String(8), nullable=True)
    # Inner critic (S5) — Branch C classification + hated-self escalation flag
    critic_function:      Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    critic_protects_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    hated_self_flagged:   Mapped[bool] = mapped_column(default=False, nullable=False)
    # Self-compassion (S6-S7) — fear-of-compassion + Branch D + soothing feedback
    foc_level:      Mapped[Optional[str]] = mapped_column(String(12), nullable=True)  # natural/awkward/undeserved
    compassion_mode: Mapped[Optional[str]] = mapped_column(String(12), nullable=True) # direct/others_first
    soothe_rating:  Mapped[Optional[int]] = mapped_column(nullable=True)  # 0–10 post-practice
    # Goal-attainment (S12 closure) — how much closer to the S1 own-words goal
    goal_attainment: Mapped[Optional[int]] = mapped_column(nullable=True)  # 0–10

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    session: Mapped["AEHQSession"] = relationship("AEHQSession", back_populates="result")
    user:    Mapped["User"]        = relationship("User")


# ── AEHQ v2.0 — Knowledge base (DB-stored, loaded into an in-memory cache) ─────
# These reference tables hold the content + mapping logic the engine used to
# hard-code. Seeded by seed_aehq.py; the service reads them once and caches.

class AEHQFramework(Base):
    """One therapeutic framework — its technique summary and evidence tier."""
    __tablename__ = "aehq_frameworks"

    code:      Mapped[str]           = mapped_column(String(20), primary_key=True)  # e.g. "F3_CFT"
    name:      Mapped[str]           = mapped_column(String(120), nullable=False)
    evidence:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tier:      Mapped[Optional[str]] = mapped_column(String(4), nullable=True)      # A / B / C
    technique: Mapped[str]           = mapped_column(Text, nullable=False)


class AEHQSituation(Base):
    """One emotional situation card. List/dict fields are stored as JSON text."""
    __tablename__ = "aehq_situations"

    key:                Mapped[str]           = mapped_column(String(40), primary_key=True)  # e.g. "grief"
    label:              Mapped[str]           = mapped_column(String(120), nullable=False)
    icon:               Mapped[str]           = mapped_column(String(8),  nullable=False)
    emotion_words_json: Mapped[str]           = mapped_column(Text, default="[]", nullable=False)
    unmet_needs_json:   Mapped[str]           = mapped_column(Text, default="[]", nullable=False)
    self_compassion:    Mapped[str]           = mapped_column(Text, nullable=False)
    ifthen_template:    Mapped[str]           = mapped_column(Text, nullable=False)
    priors_json:        Mapped[str]           = mapped_column(Text, default="{}", nullable=False)
    followup_json:      Mapped[str]           = mapped_column(Text, default="{}", nullable=False)
    sort_order:         Mapped[int]           = mapped_column(default=0, nullable=False)

    items: Mapped[list["AEHQSituationItem"]] = relationship(
        "AEHQSituationItem", back_populates="situation",
        cascade="all, delete-orphan", order_by="AEHQSituationItem.sort_order",
    )


class AEHQSituationItem(Base):
    """One question within a situation, tagged by adaptive track (S / D / R)."""
    __tablename__ = "aehq_situation_items"

    id:            Mapped[int]           = mapped_column(primary_key=True)
    situation_key: Mapped[str]           = mapped_column(ForeignKey("aehq_situations.key"), nullable=False, index=True)
    item_key:      Mapped[str]           = mapped_column(String(30), nullable=False)   # e.g. "g_s1"
    track:         Mapped[str]           = mapped_column(String(2),  nullable=False)   # S / D / R
    sort_order:    Mapped[int]           = mapped_column(default=0, nullable=False)
    input_type:    Mapped[str]           = mapped_column(String(20), nullable=False)   # text/single_select/slider
    skippable:     Mapped[bool]          = mapped_column(default=False, nullable=False)
    question:      Mapped[str]           = mapped_column(Text, nullable=False)
    subtext:       Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    options_json:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # single_select choices
    slider_json:   Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # {min,max,step,labels}
    score_deltas_json: Mapped[str]       = mapped_column(Text, default="{}", nullable=False)
    value_scoring: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    # Bottom Line template for text items, e.g. "I am {}" (S2 formulation)
    bottom_line:   Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    # Structured-capture tag, e.g. "critic_protects" (S5) — routes the answer
    # into a dedicated field instead of only free text.
    capture:       Mapped[Optional[str]] = mapped_column(String(40), nullable=True)

    situation: Mapped["AEHQSituation"] = relationship("AEHQSituation", back_populates="items")


class AEHQFrameworkRule(Base):
    """One row of the framework-selection priority stack (the mapping logic).

    Evaluated in ascending sort_order; the first rule whose score satisfies
    [min_val, max_val) wins. score_var='__default__' is the always-match fallback.
    """
    __tablename__ = "aehq_framework_rules"

    id:             Mapped[int]           = mapped_column(primary_key=True)
    sort_order:     Mapped[int]           = mapped_column(nullable=False, index=True)
    priority_label: Mapped[str]           = mapped_column(String(10), nullable=False)  # P1, P3m, DEFAULT
    score_var:      Mapped[str]           = mapped_column(String(40), nullable=False)
    min_val:        Mapped[float]         = mapped_column(Float, default=0.0, nullable=False)
    max_val:        Mapped[Optional[float]] = mapped_column(Float, nullable=True)  # None = open-ended
    framework_code: Mapped[str]           = mapped_column(String(20), nullable=False)


class AEHQScoreDelta(Base):
    """Score nudges keyed by an emotion word or body-quality chip."""
    __tablename__ = "aehq_score_deltas"

    id:          Mapped[int] = mapped_column(primary_key=True)
    kind:        Mapped[str] = mapped_column(String(10), nullable=False, index=True)  # emotion / body
    trigger_key: Mapped[str] = mapped_column(String(60), nullable=False, index=True)
    deltas_json: Mapped[str] = mapped_column(Text, default="{}", nullable=False)


class AEHQTranslation(Base):
    """Translated AEHQ copy, keyed by the exact source (EN) string.

    src conventions:  plain EN string → UI/question/label copy;
    "technique:<code>" → framework technique text; "note:<NAME>" → long scripts.
    Editing dst in the DB changes the served copy after a cache reload.
    """
    __tablename__ = "aehq_translations"

    id:   Mapped[int] = mapped_column(primary_key=True)
    lang: Mapped[str] = mapped_column(String(8), nullable=False, index=True)  # e.g. "th"
    src:  Mapped[str] = mapped_column(Text, nullable=False)
    dst:  Mapped[str] = mapped_column(Text, nullable=False)


# ── Card Deck — projective reflection readings (Stage 3: saving readings) ─────

class CardReading(Base):
    """One saved Card Deck reading.

    A reading is a completed draw the user chose to keep: the deck + spread,
    the drawn cards (with their spread positions), and the user's own words.
    Aligned with the Session_Logic / App_Data_Schema catalogue so it can grow
    into the fuller guided flow (activation before/after, intention, etc.).

    cards_json is a list of {card_id, position} in draw order, e.g.
    [{"card_id": "neuro_33", "position": "Open image"}].
    """
    __tablename__ = "card_readings"

    id:      Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)

    deck:        Mapped[str] = mapped_column(String(20), nullable=False)   # tarot | neuro | nature
    spread_id:   Mapped[str] = mapped_column(String(20), nullable=False)   # one | three
    spread_name: Mapped[str] = mapped_column(String(80), nullable=False)   # display name at save time
    cards_json:  Mapped[str] = mapped_column(Text, default="[]", nullable=False)

    # The user's own words — the heart of a projective reading.
    reflection: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Optional session focus (Session_Logic stage 2) captured at save time.
    intention:  Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Optional self-reported activation 0–10 (stage 1) — reserved for the fuller flow.
    activation_before: Mapped[Optional[int]] = mapped_column(nullable=True)

    lang:       Mapped[Optional[str]] = mapped_column(String(8), nullable=True)  # th / en at save time
    created_at: Mapped[datetime]      = mapped_column(DateTime, server_default=func.now())

    user: Mapped["User"] = relationship("User")
