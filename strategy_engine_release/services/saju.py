"""BaZi (Chinese) / SaJu (Korean) Four Pillars of Destiny — placeholder.

PLACEHOLDER NOTICE
------------------
A faithful BaZi engine requires:
  1. Solar-term boundaries (the year/month change on solar terms, not Jan 1 / month 1).
  2. The 60 Jiazi cycle anchored to a known reference day with proper offset.
  3. True solar time correction for the hour pillar.
  4. Rules for the "hidden stems" inside each Earthly Branch.

This module returns deterministic placeholder values that respect the
*shape* of a BaZi result so the rest of the system can be wired up and tested.
Swap `calculate_birth_chart` and `calculate_day_pillar` for a real implementation
(e.g. via lunar-python or sxtwl) without touching scoring or API code.
"""

from datetime import date, time

from models.domain import Element


# Heavenly Stems → Element. 10 stems, two per element (yang then yin).
HEAVENLY_STEM_ELEMENTS: list[Element] = [
    Element.WOOD,  Element.WOOD,
    Element.FIRE,  Element.FIRE,
    Element.EARTH, Element.EARTH,
    Element.METAL, Element.METAL,
    Element.WATER, Element.WATER,
]

# Earthly Branches → primary Element. 12 branches.
EARTHLY_BRANCH_ELEMENTS: list[Element] = [
    Element.WATER,  # 0  Zi   (rat)
    Element.EARTH,  # 1  Chou (ox)
    Element.WOOD,   # 2  Yin  (tiger)
    Element.WOOD,   # 3  Mao  (rabbit)
    Element.EARTH,  # 4  Chen (dragon)
    Element.FIRE,   # 5  Si   (snake)
    Element.FIRE,   # 6  Wu   (horse)
    Element.EARTH,  # 7  Wei  (goat)
    Element.METAL,  # 8  Shen (monkey)
    Element.METAL,  # 9  You  (rooster)
    Element.EARTH,  # 10 Xu   (dog)
    Element.WATER,  # 11 Hai  (pig)
]

_REFERENCE_DAY = date(1900, 1, 1)


def _ordinal_day(d: date) -> int:
    return (d - _REFERENCE_DAY).days


def calculate_day_pillar(d: date) -> tuple[Element, Element]:
    """Return (day_stem_element, day_branch_element) for a given date.

    PLACEHOLDER: linear modulo over an ordinal day count. Real BaZi anchors
    the 60 Jiazi cycle to a specific historical day with a fixed offset.
    """
    n = _ordinal_day(d)
    stem = HEAVENLY_STEM_ELEMENTS[n % 10]
    branch = EARTHLY_BRANCH_ELEMENTS[n % 12]
    return stem, branch


def _hour_to_branch_index(t: time) -> int:
    """Map clock hour to one of 12 earthly branches (2-hour blocks).
    Branch 0 (Zi) covers 23:00–01:00, branch 1 covers 01:00–03:00, etc."""
    return ((t.hour + 1) // 2) % 12


def calculate_birth_chart(birthdate: date, birth_time: time) -> dict:
    """Compute the Four Pillars chart and derive dominant/weak elements.

    Returns a dict with keys:
      - day_master:        Element  (the stem of the Day Pillar; the user's core self)
      - pillars:           {year, month, day, hour: {stem, branch}}
      - element_counts:    Element → int
      - dominant_elements: elements with the highest count
      - weak_elements:     elements with count == 0
    """
    n = _ordinal_day(birthdate)

    year_stem    = HEAVENLY_STEM_ELEMENTS[(birthdate.year - 4) % 10]
    year_branch  = EARTHLY_BRANCH_ELEMENTS[(birthdate.year - 4) % 12]

    month_stem   = HEAVENLY_STEM_ELEMENTS[(birthdate.month * 2) % 10]
    month_branch = EARTHLY_BRANCH_ELEMENTS[(birthdate.month + 1) % 12]

    day_stem, day_branch = calculate_day_pillar(birthdate)

    hour_idx     = _hour_to_branch_index(birth_time)
    hour_stem    = HEAVENLY_STEM_ELEMENTS[(n * 12 + hour_idx) % 10]
    hour_branch  = EARTHLY_BRANCH_ELEMENTS[hour_idx]

    pillars = {
        "year":  {"stem": year_stem,  "branch": year_branch},
        "month": {"stem": month_stem, "branch": month_branch},
        "day":   {"stem": day_stem,   "branch": day_branch},
        "hour":  {"stem": hour_stem,  "branch": hour_branch},
    }

    counts: dict[Element, int] = {e: 0 for e in Element}
    for p in pillars.values():
        counts[p["stem"]]   += 1
        counts[p["branch"]] += 1

    max_count = max(counts.values())
    dominant = [e for e, c in counts.items() if c == max_count]
    weak     = [e for e, c in counts.items() if c == 0]

    return {
        "day_master":        day_stem,
        "pillars":           pillars,
        "element_counts":    counts,
        "dominant_elements": dominant,
        "weak_elements":     weak,
    }
