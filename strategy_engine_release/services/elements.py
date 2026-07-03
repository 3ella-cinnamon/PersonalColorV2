"""Five Elements (Wu Xing) interaction logic.

Two canonical cycles drive every interaction in BaZi:
  - Generation (sheng):    Wood → Fire → Earth → Metal → Water → Wood
  - Destruction (ke):      Wood → Earth → Water → Fire → Metal → Wood

Given the daily element and the user's Day Master, we classify the relationship
into one of the Five "Ten Gods" categories used by the scoring engine.
"""

from models.domain import Element, InteractionType


GENERATION: dict[Element, Element] = {
    Element.WOOD:  Element.FIRE,
    Element.FIRE:  Element.EARTH,
    Element.EARTH: Element.METAL,
    Element.METAL: Element.WATER,
    Element.WATER: Element.WOOD,
}

DESTRUCTION: dict[Element, Element] = {
    Element.WOOD:  Element.EARTH,
    Element.EARTH: Element.WATER,
    Element.WATER: Element.FIRE,
    Element.FIRE:  Element.METAL,
    Element.METAL: Element.WOOD,
}


def classify_interaction(daily: Element, day_master: Element) -> InteractionType:
    """Classify how the daily element interacts with the user's Day Master.

    Returns one of:
      - RESOURCE  — daily generates Day Master   (supportive)
      - WEALTH    — Day Master controls daily    (supportive)
      - COMPANION — same element                 (neutral+)
      - OUTPUT    — Day Master generates daily   (neutral)
      - OFFICER   — daily controls Day Master    (destructive clash)
    """
    if daily == day_master:
        return InteractionType.COMPANION
    if GENERATION[daily] == day_master:
        return InteractionType.RESOURCE
    if GENERATION[day_master] == daily:
        return InteractionType.OUTPUT
    if DESTRUCTION[daily] == day_master:
        return InteractionType.OFFICER
    if DESTRUCTION[day_master] == daily:
        return InteractionType.WEALTH
    raise ValueError(f"Unclassified interaction: {daily} vs {day_master}")
