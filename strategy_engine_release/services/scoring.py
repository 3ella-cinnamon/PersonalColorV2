"""Daily Action Score (S) — the integration model.

Equation from the architecture spec:

    S = (W_B · E_bazi  +  W_M · E_mian) · M_hd · M_cog

with constants:
    W_B = 0.8    (BaZi / time-environment weight)
    W_M = 0.2    (Mian Xiang / hardware weight)

Thresholds:
    S >= 75  →  ATTACK
    40 <= S <  75  →  OPTIMIZE
    S <  40  →  RETREAT
"""

from typing import Optional

from models.domain import Element, InteractionType, Strategy
from services.elements import classify_interaction
from services.multipliers import (
    cognitive_efficiency_multiplier,
    hardware_resonance,
    human_design_multiplier,
)


# Doc-specified weights
W_BAZI: float = 0.8
W_MIAN: float = 0.2

# E_bazi value range per interaction class. The doc specifies only the
# supportive (80-100) and destructive (10-30) ranges; the others are
# interpolations that preserve ordering.
_BAZI_ENERGY_RANGES: dict[InteractionType, tuple[float, float]] = {
    InteractionType.RESOURCE:  (80.0, 100.0),
    InteractionType.WEALTH:    (80.0, 100.0),
    InteractionType.COMPANION: (50.0,  65.0),
    InteractionType.OUTPUT:    (45.0,  60.0),
    InteractionType.OFFICER:   (10.0,  30.0),
}


def _compute_e_bazi(interaction: InteractionType, energy_input: int) -> float:
    """Pick a deterministic value within the doc-specified E_bazi range,
    modulated by the user's self-reported energy level (1-10).

    Rationale: the cosmic range is fixed by the interaction type; the user's
    subjective state determines where they fall *within* that range.
    """
    lo, hi = _BAZI_ENERGY_RANGES[interaction]
    pct = (energy_input - 1) / 9.0  # 0.0 .. 1.0
    return lo + (hi - lo) * pct


def threshold_strategy(score: float) -> Strategy:
    if score >= 75:
        return Strategy.ATTACK
    if score >= 40:
        return Strategy.OPTIMIZE
    return Strategy.RETREAT


def calculate_action_score(
    *,
    day_master:    Element,
    daily_element: Element,
    mbti_element:  Element,
    mbti_dominant: str,
    goal:          str,
    energy_input:  int,
    hd_aligned:    Optional[bool] = None,
) -> dict:
    """Run the full integration pipeline and return a structured result.

    Returns:
        {
            "score":            float,            # clamped to [0, 100]
            "strategy":         Strategy,
            "interaction_type": InteractionType,
            "components":       {E_bazi, E_mian, M_hd, M_cog, weighted_base},
        }
    """
    interaction = classify_interaction(daily_element, day_master)

    e_bazi = _compute_e_bazi(interaction, energy_input)
    e_mian = hardware_resonance(mbti_element, daily_element)
    m_hd   = human_design_multiplier(hd_aligned)
    m_cog  = cognitive_efficiency_multiplier(mbti_dominant, goal)

    base  = W_BAZI * e_bazi + W_MIAN * e_mian
    raw   = base * m_hd * m_cog
    score = max(0.0, min(100.0, raw))

    return {
        "score":            round(score, 2),
        "strategy":         threshold_strategy(score),
        "interaction_type": interaction,
        "components": {
            "E_bazi":        round(e_bazi, 2),
            "E_mian":        round(e_mian, 2),
            "M_hd":          m_hd,
            "M_cog":         m_cog,
            "weighted_base": round(base, 2),
        },
    }
