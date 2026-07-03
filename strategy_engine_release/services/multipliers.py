"""Multiplier and resonance placeholders.

Per the architecture doc:
  E_mian — Mian Xiang facial-morphology resonance with the daily element.
  M_hd   — Human Design strategy alignment multiplier (1.2 / 0.5 / 1.0).
  M_cog  — MBTI cognitive efficiency multiplier (1.15 / 1.0).

These are isolated here so they can be swapped for real implementations
(e.g. CV-based face shape analysis, full HD bodygraph) without touching the
scoring formula or API surface.
"""

from typing import Optional

from models.domain import Element, InteractionType
from services.elements import classify_interaction


# ---------- E_mian (Hardware Resonance) ----------

# Score map: how a daily element interacts with the user's "hardware" element.
# Same shape as BaZi interaction since the architecture maps face morphology
# to the same Five-Element space.
_MIAN_SCORE_BY_INTERACTION: dict[InteractionType, float] = {
    InteractionType.RESOURCE:  85.0,
    InteractionType.WEALTH:    75.0,
    InteractionType.COMPANION: 60.0,
    InteractionType.OUTPUT:    50.0,
    InteractionType.OFFICER:   25.0,
}


def hardware_resonance(mbti_element: Element, daily_element: Element) -> float:
    """E_mian ∈ [0, 100].

    PLACEHOLDER: derives a proxy from the MBTI-mapped element. A real version
    would use the user's actual face shape (Long, Pointed, Square, Oval, Round).
    """
    interaction = classify_interaction(daily_element, mbti_element)
    return _MIAN_SCORE_BY_INTERACTION[interaction]


# ---------- M_hd (Human Design Multiplier) ----------

def human_design_multiplier(hd_aligned: Optional[bool]) -> float:
    """M_hd per the architecture doc:
       True  → 1.2  (acting per HD strategy)
       False → 0.5  (acting against HD strategy)
       None  → 1.0  (no HD data; neutral)
    """
    if hd_aligned is None:
        return 1.0
    return 1.2 if hd_aligned else 0.5


# ---------- M_cog (MBTI Cognitive Efficiency) ----------

# Goals → cognitive functions whose dominance amplifies execution efficiency.
# Tunable; not specified in the architecture doc beyond the example
# "Ti for structural organization → 1.15".
_GOAL_FUNCTION_AFFINITY: dict[str, set[str]] = {
    "work":         {"Te", "Ti", "Ni"},
    "money":        {"Te", "Ni", "Si"},
    "relationship": {"Fe", "Fi", "Ne"},
}


def cognitive_efficiency_multiplier(mbti_dominant: str, goal: str) -> float:
    """M_cog per the architecture doc:
       1.15 if the dominant cognitive function aligns with the goal's required
       cognition, else 1.0.
    """
    affinity = _GOAL_FUNCTION_AFFINITY.get(goal, set())
    return 1.15 if mbti_dominant in affinity else 1.0
