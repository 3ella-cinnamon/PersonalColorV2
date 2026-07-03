"""Energy Context — DB-first pre-computation layer.

Computes ALL daily energy fields from calendar math and element logic alone.
Zero AI tokens consumed. Results are injected into the prompt builder so
the LLM synthesises narrative only — it never re-derives these values.

Layers computed:
  1. Astronomy  — approximate Bangkok sunrise/sunset + planetary hour (ยาม)
  2. BaZi       — stance from interaction type; lead colour from Day Master
  3. Qimen-style — power direction from Day Master element
  4. Thai        — weekday planet ruler
  5. Strong Day  — ADVANCE stance + planetary hour aligned with goal
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date, datetime, time as time_type
from typing import Optional

from models.domain import Element, InteractionType
from services.elements import classify_interaction


# ── Bangkok constants ─────────────────────────────────────────────────────────

_BKK_LAT = 13.7563   # degrees N
_BKK_LON = 100.5018  # degrees E
_BKK_UTC_OFFSET = 7  # hours


# ── Chaldean planetary order ──────────────────────────────────────────────────
# Index 0 = slowest (Saturn) → 6 = fastest (Moon)

CHALDEAN_PLANETS = ["Saturn", "Jupiter", "Mars", "Sun", "Venus", "Mercury", "Moon"]

# Thai planet names (ยาม)
THAI_PLANET_NAMES = {
    "Saturn":  "เสาร์",
    "Jupiter": "พฤหัส",
    "Mars":    "อังคาร",
    "Sun":     "อาทิตย์",
    "Venus":   "ศุกร์",
    "Mercury": "พุธ",
    "Moon":    "จันทร์",
}

# What each planet hour is best for / what to avoid (from decision_compass_logic.xlsx)
PLANET_BEST_FOR = {
    "Jupiter": "Deals, contracts, interviews, important signings",
    "Mercury": "Negotiation, discussions, paperwork, presentations",
    "Venus":   "Dating, social connection, proposals, creative work",
    "Sun":     "Launches, leadership, authority meetings, visibility",
    "Mars":    "Bold action, competition, assertive negotiation",
    "Moon":    "Family, intuition, short trips, reflective planning",
    "Saturn":  "Discipline, long-term planning, endings, consolidation",
}

PLANET_AVOID = {
    "Jupiter": "—",
    "Mercury": "—",
    "Venus":   "Conflict, confrontation",
    "Sun":     "—",
    "Mars":    "Delicate or emotional conversations",
    "Moon":    "Big irreversible commitments",
    "Saturn":  "New beginnings, romance, creative launches",
}

# Which planetary rulers suit each goal (used for strong_day logic)
_GOAL_SUITED_PLANETS = {
    "work":         {"Sun", "Jupiter", "Mars"},
    "money":        {"Jupiter", "Mercury", "Sun"},
    "relationship": {"Venus", "Moon", "Jupiter"},
}

# First day hour planet index per weekday (Python weekday(): Mon=0 … Sun=6)
# Chaldean indices: Saturn=0, Jupiter=1, Mars=2, Sun=3, Venus=4, Mercury=5, Moon=6
_WEEKDAY_START_PLANET: list[int] = [6, 2, 5, 1, 4, 0, 3]
#                                   Mon Tue Wed Thu Fri Sat Sun


# ── Colour & direction tables ─────────────────────────────────────────────────

_ELEMENT_COLOURS = {
    Element.WOOD:  {"lead": "Green / Teal",          "hex": "#2E7D32", "secondary": "Black / Navy"},
    Element.FIRE:  {"lead": "Red / Purple",           "hex": "#C0392B", "secondary": "Green / Teal"},
    Element.EARTH: {"lead": "Yellow / Mustard / Beige", "hex": "#B7950B", "secondary": "Red / Orange"},
    Element.METAL: {"lead": "White / Gold / Silver",  "hex": "#BDC3C7", "secondary": "Yellow / Beige"},
    Element.WATER: {"lead": "Black / Deep Blue",      "hex": "#1F3A5F", "secondary": "White / Gold"},
}

_ELEMENT_DIRECTION = {
    Element.WOOD:  "East",
    Element.FIRE:  "South",
    Element.EARTH: "Southwest (Center)",
    Element.METAL: "West",
    Element.WATER: "North",
}

# Stance mapping from interaction type
_INTERACTION_STANCE: dict[InteractionType, tuple[str, str]] = {
    InteractionType.RESOURCE:  ("ADVANCE",  "รุก"),
    InteractionType.COMPANION: ("ADVANCE",  "รุก"),
    InteractionType.WEALTH:    ("RESTRAIN", "ถ่อมตน"),
    InteractionType.OUTPUT:    ("NEUTRAL",  "ปกติ"),
    InteractionType.OFFICER:   ("DEFEND",   "ตั้งรับ"),
}

# Day branch clash pairs (六冲) — index pairs in 0-11 range
_CLASH_PAIRS: set[frozenset] = {
    frozenset({0, 6}),   # Zi ↔ Wu  (Rat ↔ Horse)
    frozenset({1, 7}),   # Chou ↔ Wei (Ox ↔ Goat)
    frozenset({2, 8}),   # Yin ↔ Shen (Tiger ↔ Monkey)
    frozenset({3, 9}),   # Mao ↔ You  (Rabbit ↔ Rooster)
    frozenset({4, 10}),  # Chen ↔ Xu  (Dragon ↔ Dog)
    frozenset({5, 11}),  # Si ↔ Hai   (Snake ↔ Pig)
}

# Saturn note per HD profile (keyed by hd_type)
_SATURN_NOTE = {
    "Projector": (
        "Saturn rewards patient, disciplined effort over time. "
        "As a Projector, your Saturn-backed authority comes through consistent mastery — "
        "not urgency. Avoid shortcuts that undermine long-term credibility."
    ),
}
_SATURN_NOTE_DEFAULT = (
    "Discipline and patient effort are rewarded today. Avoid shortcuts. "
    "Saturn favours those who play the long game."
)


# ── Result dataclass ──────────────────────────────────────────────────────────

@dataclass
class EnergyContext:
    # Stance
    stance: str          # ADVANCE / DEFEND / RESTRAIN / AVOID / NEUTRAL
    stance_th: str       # รุก / ตั้งรับ / ถ่อมตน / หลีกเลี่ยง / ปกติ
    strong_day: bool

    # Colour (from BaZi Day Master)
    lead_colour: str
    lead_colour_hex: str
    secondary_colour: str

    # Direction (Qimen-style, from Day Master element)
    power_direction: str

    # Astronomy — planetary hour
    planetary_hour_ruler: str     # e.g. "Jupiter"
    planetary_hour_ruler_th: str  # e.g. "พฤหัส"
    planetary_hour_best_for: str
    planetary_hour_avoid: str
    peak_hour_window: str         # e.g. "09:30–11:00"

    # Thai weekday ruler
    thai_day_ruler: str           # e.g. "พฤหัส"

    # Saturn note
    saturn_note: str


# ── Astronomy helpers ─────────────────────────────────────────────────────────

def _approx_sunrise_sunset(d: date) -> tuple[float, float]:
    """Approximate Bangkok sunrise and sunset as decimal hours (local UTC+7).

    Uses a simplified sinusoidal approximation calibrated to BKK (13.75°N).
    Accuracy: ±15 minutes. Sufficient for 2-hour planetary hour windows.
    """
    doy = d.timetuple().tm_yday
    angle = 2 * math.pi * (doy - 172) / 365   # 0 at summer solstice ~Jun 21
    sunrise = 6.25 - 0.33 * math.cos(angle)   # ranges ~5.92 → 6.58
    sunset  = 18.21 + 0.38 * math.cos(angle)  # ranges ~17.83 → 18.59
    return sunrise, sunset


def _decimal_hour(t: datetime) -> float:
    return t.hour + t.minute / 60.0 + t.second / 3600.0


def _get_planetary_hour(d: date, now: Optional[datetime] = None) -> tuple[str, str, float, float]:
    """Return (planet_en, planet_th, window_start_h, window_end_h) for the current time.

    Uses unequal planetary hours (traditional method):
      - Day hours  = (sunset - sunrise) / 6 each, starting at sunrise
      - Night hours = (24 - sunset + sunrise) / 6 each, starting at sunset
      - 12 day hours + 12 night hours = 24 hour sequence
    """
    sunrise, sunset = _approx_sunrise_sunset(d)
    current_h = _decimal_hour(now or datetime.now())

    weekday = d.weekday()  # Mon=0 … Sun=6
    start_planet_idx = _WEEKDAY_START_PLANET[weekday]

    day_len   = sunset - sunrise
    night_len = 24.0 - day_len
    day_hr    = day_len / 6.0    # length of one day planetary hour
    night_hr  = night_len / 6.0  # length of one night planetary hour

    # Build 12 day windows then 12 night windows
    windows: list[tuple[float, float, int]] = []  # (start, end, planet_idx)
    for i in range(12):
        s = sunrise + i * day_hr
        e = s + day_hr
        p = (start_planet_idx + i) % 7
        windows.append((s, e, p))
    for i in range(12):
        s = sunset + i * night_hr
        e = s + night_hr
        p = (start_planet_idx + 6 + i) % 7  # night starts 6 hours after day start
        windows.append((s, e, p))

    # Find the window containing current_h (handle midnight wraparound)
    for s, e, p in windows:
        if s <= current_h < e:
            return (
                CHALDEAN_PLANETS[p],
                THAI_PLANET_NAMES[CHALDEAN_PLANETS[p]],
                s, e,
            )

    # Fallback: return the first day hour
    s, e, p = windows[0]
    return CHALDEAN_PLANETS[p], THAI_PLANET_NAMES[CHALDEAN_PLANETS[p]], s, e


def _format_hour_window(start_h: float, end_h: float) -> str:
    """Convert decimal hours to 'HH:MM–HH:MM' string."""
    def _fmt(h: float) -> str:
        h = h % 24
        hh = int(h)
        mm = int((h - hh) * 60)
        return f"{hh:02d}:{mm:02d}"
    return f"{_fmt(start_h)}–{_fmt(end_h)}"


# ── Stance helpers ────────────────────────────────────────────────────────────

def _compute_stance(
    day_element: Element,
    day_master: Element,
    natal_day_branch: int,
    today_day_branch: int,
) -> tuple[str, str]:
    """Return (stance_en, stance_th).

    Clash check takes priority over interaction type.
    """
    # Clash day → AVOID
    if frozenset({natal_day_branch, today_day_branch}) in _CLASH_PAIRS:
        return "AVOID", "หลีกเลี่ยง"

    interaction = classify_interaction(day_element, day_master)
    return _INTERACTION_STANCE[interaction]


def _get_day_branch_index(d: date) -> int:
    """Return earthly branch index (0-11) for a given date (simplified BaZi)."""
    from services.saju import _ordinal_day
    return _ordinal_day(d) % 12


# ── Main factory ──────────────────────────────────────────────────────────────

def compute_energy_context(
    day_master: Element,
    day_element: Element,
    birthdate: date,
    goal: str,
    target_date: Optional[date] = None,
    now: Optional[datetime] = None,
    hd_type: Optional[str] = None,
) -> EnergyContext:
    """Compute the full energy context. Zero AI tokens consumed.

    Args:
        day_master:   User's BaZi Day Master element (from birth chart).
        day_element:  Today's heavenly stem element (from day pillar).
        birthdate:    User's birth date (for natal branch clash check).
        goal:         "work" | "money" | "relationship"
        target_date:  Date to compute for (defaults to today).
        now:          Current time (defaults to datetime.now()).
        hd_type:      Human Design type (for Saturn note lookup).
    """
    td = target_date or date.today()

    # 1. Stance ────────────────────────────────────────────────────────────────
    natal_branch = _get_day_branch_index(birthdate)
    today_branch = _get_day_branch_index(td)
    stance, stance_th = _compute_stance(day_element, day_master, natal_branch, today_branch)

    # 2. Colour (from Day Master — represents the user's core personal element) ─
    colour_data      = _ELEMENT_COLOURS.get(day_master, {})
    lead_colour      = colour_data.get("lead", "")
    lead_colour_hex  = colour_data.get("hex", "")
    secondary_colour = colour_data.get("secondary", "")

    # 3. Power direction (Qimen-style: face your Day Master element direction) ──
    power_direction = _ELEMENT_DIRECTION.get(day_master, "")

    # 4. Planetary hour ────────────────────────────────────────────────────────
    planet_en, planet_th, win_start, win_end = _get_planetary_hour(td, now)
    best_for    = PLANET_BEST_FOR.get(planet_en, "")
    avoid_note  = PLANET_AVOID.get(planet_en, "—")
    peak_window = _format_hour_window(win_start, win_end)

    # Thai weekday ruler (day ruler = planet that rules the first hour)
    thai_day_ruler = THAI_PLANET_NAMES[
        CHALDEAN_PLANETS[_WEEKDAY_START_PLANET[td.weekday()]]
    ]

    # 5. Strong day: ADVANCE stance + planetary hour suits the goal ────────────
    suited_planets = _GOAL_SUITED_PLANETS.get(goal, set())
    strong_day = (stance == "ADVANCE") and (planet_en in suited_planets)

    # 6. Saturn note ───────────────────────────────────────────────────────────
    saturn_note = _SATURN_NOTE.get(hd_type or "", _SATURN_NOTE_DEFAULT)

    return EnergyContext(
        stance=stance,
        stance_th=stance_th,
        strong_day=strong_day,
        lead_colour=lead_colour,
        lead_colour_hex=lead_colour_hex,
        secondary_colour=secondary_colour,
        power_direction=power_direction,
        planetary_hour_ruler=planet_en,
        planetary_hour_ruler_th=planet_th,
        planetary_hour_best_for=best_for,
        planetary_hour_avoid=avoid_note,
        peak_hour_window=peak_window,
        thai_day_ruler=thai_day_ruler,
        saturn_note=saturn_note,
    )
