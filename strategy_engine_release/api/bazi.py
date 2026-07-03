"""GET /api/bazi — Full BaZi chart + Qi Men Dun Jia hour analysis.

Two usage modes:
  1. Authenticated user  → uses profile birthdate automatically
  2. Query params        → ?birthdate=1990-04-15&birth_time=14:30&target_date=2026-06-04

Response includes:
  - Four Pillars (四柱) with stems, branches, elements
  - Day Master element + description
  - Element counts + dominant/weak analysis
  - Daily element + interaction type + bazi_score
  - Qi Men Dun Jia: 12 two-hour windows classified as auspicious/mixed/avoid
  - Best 3 windows with gate name, direction, activities (EN + TH)
"""

from datetime import date, time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.database import get_db
from core.deps import get_current_user_optional
from models.domain import Element, InteractionType
from models.orm import User
from services.elements import classify_interaction
from services.qimen import BRANCHES, POWER_DIRECTION, calculate_qimen, get_current_window
from services.saju import (
    HEAVENLY_STEM_ELEMENTS, EARTHLY_BRANCH_ELEMENTS,
    calculate_birth_chart, calculate_day_pillar, _ordinal_day,
)
from services.scoring import calculate_action_score, threshold_strategy
from services.mbti import mbti_to_element

router = APIRouter()


# ── Chinese Heavenly Stem names (天干) ───────────────────────────────────────
_STEM_NAMES = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
_STEM_POLARITY = ["Yang", "Yin"] * 5

_DAY_MASTER_DESC_EN = {
    Element.WOOD:  "甲/乙 Wood — visionary, growth-driven, compassionate",
    Element.FIRE:  "丙/丁 Fire — expressive, charismatic, passionate",
    Element.EARTH: "戊/己 Earth — reliable, nurturing, stabilising",
    Element.METAL: "庚/辛 Metal — principled, decisive, disciplined",
    Element.WATER: "壬/癸 Water — perceptive, adaptive, deeply intuitive",
}

_DAY_MASTER_DESC_TH = {
    Element.WOOD:  "甲/乙 ไม้ — มีวิสัยทัศน์ ขับเคลื่อนด้วยการเติบโต เมตตา",
    Element.FIRE:  "丙/丁 ไฟ — แสดงออก มีเสน่ห์ หลงใหล",
    Element.EARTH: "戊/己 ดิน — เชื่อถือได้ ดูแลเอาใจใส่ สร้างความมั่นคง",
    Element.METAL: "庚/辛 ทอง — มีหลักการ เด็ดขาด มีวินัย",
    Element.WATER: "壬/癸 น้ำ — มีความรู้สึกไว ปรับตัวได้ มีสัญชาตญาณลึกซึ้ง",
}

_STRATEGY_DESC_EN = {
    "ATTACK":   "High energy — take decisive action, initiate, lead.",
    "OPTIMIZE": "Moderate — calibrate your approach, build momentum steadily.",
    "RETREAT":  "Low energy — observe, protect judgment, avoid major decisions.",
}

_STRATEGY_DESC_TH = {
    "ATTACK":   "พลังงานสูง — ลงมือด้วยความเด็ดขาด ริเริ่ม นำหน้า",
    "OPTIMIZE": "ปานกลาง — ปรับแนวทาง สร้างแรงผลักดันอย่างสม่ำเสมอ",
    "RETREAT":  "พลังงานต่ำ — สังเกต ปกป้องการตัดสินใจ หลีกเลี่ยงการตัดสินใจสำคัญ",
}


def _stem_name(n: int) -> str:
    return _STEM_NAMES[n % 10]

def _branch_name(b) -> str:
    return BRANCHES[b.index if hasattr(b, 'index') else 0].name_cn if False else {
        0: "子", 1: "丑", 2: "寅", 3: "卯", 4: "辰", 5: "巳",
        6: "午", 7: "未", 8: "申", 9: "酉", 10: "戌", 11: "亥",
    }.get(list(EARTHLY_BRANCH_ELEMENTS).index(b) if b in EARTHLY_BRANCH_ELEMENTS else 0, "?")


def _pillar_dict(stem_el: Element, branch_el: Element, day_offset: int, pillar_type: str) -> dict:
    """Build a pillar dict with stem name, branch name, elements."""
    stem_idx = {Element.WOOD: 0, Element.FIRE: 2, Element.EARTH: 4,
                Element.METAL: 6, Element.WATER: 8}[stem_el]
    branch_idx = list(EARTHLY_BRANCH_ELEMENTS).index(branch_el) if branch_el in EARTHLY_BRANCH_ELEMENTS else 0

    branch_names = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
    return {
        "stem_element":   stem_el.value.upper(),
        "branch_element": branch_el.value.upper(),
        "stem_cn":        _STEM_NAMES[stem_idx % 10],
        "branch_cn":      branch_names[branch_idx % 12],
        "polarity":       _STEM_POLARITY[stem_idx % 10],
    }


@router.get("")
def get_bazi(
    birthdate:   Optional[date] = Query(None, description="Override birthdate YYYY-MM-DD"),
    birth_time:  Optional[time] = Query(None, description="Override birth time HH:MM"),
    target_date: date            = Query(default_factory=date.today, description="Date to analyse (default today)"),
    energy:      int             = Query(7, ge=1, le=10, description="Self-reported energy level 1-10"),
    current:     Optional[User]  = Depends(get_current_user_optional),
    db:          Session         = Depends(get_db),
):
    # Resolve birthdate — prefer query param, fallback to profile
    if birthdate is None:
        if current is None or current.profile is None:
            raise HTTPException(400, "Provide ?birthdate=YYYY-MM-DD or authenticate with a profile.")
        birthdate  = current.profile.birthdate
        birth_time = current.profile.birth_time if birth_time is None else birth_time

    birth_time = birth_time or time(12, 0)  # default noon if not provided

    # ── BaZi Four Pillars ────────────────────────────────────────────────────
    chart = calculate_birth_chart(birthdate, birth_time)
    day_master: Element = chart["day_master"]
    pillars = chart["pillars"]

    n_birth = _ordinal_day(birthdate)
    stem_names = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
    branch_names = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

    four_pillars = {}
    for name, p in pillars.items():
        s_el: Element = p["stem"]
        b_el: Element = p["branch"]
        s_idx = {Element.WOOD:0,Element.FIRE:2,Element.EARTH:4,Element.METAL:6,Element.WATER:8}[s_el]
        b_idx = list(EARTHLY_BRANCH_ELEMENTS).index(b_el) if b_el in EARTHLY_BRANCH_ELEMENTS else 0
        four_pillars[name] = {
            "stem_element":   s_el.value.upper(),
            "branch_element": b_el.value.upper(),
            "stem_cn":        stem_names[s_idx % 10],
            "branch_cn":      branch_names[b_idx % 12],
            "polarity":       "Yang" if s_idx % 2 == 0 else "Yin",
        }

    element_counts = {k.value.upper(): v for k, v in chart["element_counts"].items()}
    dominant       = [e.value.upper() for e in chart["dominant_elements"]]
    weak           = [e.value.upper() for e in chart["weak_elements"]]

    # ── Today's element + interaction ────────────────────────────────────────
    day_stem, day_branch = calculate_day_pillar(target_date)
    daily_element: Element = day_stem
    interaction = classify_interaction(daily_element, day_master)

    # Simplified bazi score (use energy=energy, no MBTI context here)
    from services.scoring import _compute_e_bazi, W_BAZI, W_MIAN
    from services.multipliers import hardware_resonance
    e_bazi = _compute_e_bazi(interaction, energy)
    e_mian = hardware_resonance(day_master, daily_element)
    base   = W_BAZI * e_bazi + W_MIAN * e_mian
    score  = max(0.0, min(100.0, base))
    strategy = threshold_strategy(score)

    # ── Qi Men Dun Jia ────────────────────────────────────────────────────────
    qm = calculate_qimen(target_date, day_master, daily_element)
    current_win = get_current_window(qm)

    # ── Power direction for today ─────────────────────────────────────────────
    pd = POWER_DIRECTION[day_master]

    return {
        "birthdate":     birthdate.isoformat(),
        "target_date":   target_date.isoformat(),

        "day_master": {
            "element":     day_master.value.upper(),
            "description_en": _DAY_MASTER_DESC_EN[day_master],
            "description_th": _DAY_MASTER_DESC_TH[day_master],
            "power_direction_en": pd["en"],
            "power_direction_th": pd["th"],
        },

        "four_pillars": four_pillars,

        "element_analysis": {
            "counts":   element_counts,
            "dominant": dominant,
            "weak":     weak,
            "balance_tip_en": (
                f"Strong in {', '.join(dominant)}. "
                + (f"Weak/missing: {', '.join(weak)}." if weak else "All elements present.")
            ),
        },

        "today": {
            "target_date":      target_date.isoformat(),
            "daily_element":    daily_element.value.upper(),
            "interaction_type": interaction.value.upper(),
            "bazi_score":       round(score / 10, 2),
            "raw_score":        round(score, 1),
            "strategy":         strategy.value,
            "strategy_desc_en": _STRATEGY_DESC_EN[strategy.value],
            "strategy_desc_th": _STRATEGY_DESC_TH[strategy.value],
        },

        "qimen": {
            "summary_en": (
                f"Day Master {day_master.value.upper()} on a {daily_element.value.upper()} day — "
                f"{interaction.value.upper()} interaction. "
                f"{len(qm.auspicious)} auspicious windows, {len(qm.avoid)} windows to avoid."
            ),
            "summary_th": (
                f"Day Master {day_master.value.upper()} ในวัน {daily_element.value.upper()} — "
                f"ความสัมพันธ์แบบ {interaction.value.upper()} "
                f"{len(qm.auspicious)} ช่วงเวลาดี, {len(qm.avoid)} ช่วงที่ควรหลีกเลี่ยง"
            ),
            "current_window":   current_win.to_dict() if current_win else None,
            "best_windows":     [h.to_dict() for h in qm.auspicious[:3]],
            "auspicious_hours": [h.to_dict() for h in qm.auspicious],
            "mixed_hours":      [h.to_dict() for h in qm.mixed],
            "avoid_hours":      [h.to_dict() for h in qm.avoid],
        },
    }
