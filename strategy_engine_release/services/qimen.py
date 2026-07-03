"""Qi Men Dun Jia (奇門遁甲) — Simplified daily hour analysis.

NOTE: This is a structurally faithful but algorithmically simplified
implementation. Real QMDJ requires solar-term-anchored palace rotation,
full 9-star/8-deity overlay, and hour-specific Jiazi offset.

What this module provides:
  - All 12 two-hour periods classified by element interaction with Day Master
  - Gate assignment (8 Gates / 八門)
  - Power direction per period + branch compass direction
  - One-liner summary per window: activity + best direction
  - Activity recommendations in EN + TH
  - current_window: the active 2-hour block right now
  - best_windows: top 3 auspicious windows
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from models.domain import Element, InteractionType
from services.elements import classify_interaction
from services.saju import EARTHLY_BRANCH_ELEMENTS, HEAVENLY_STEM_ELEMENTS, _ordinal_day


# ── 12 Earthly Branches (地支) ──────────────────────────────────────────────

@dataclass
class Branch:
    index: int          # 0-11
    name_cn: str
    name_en: str
    time_range: str
    start_hour: int
    element: Element
    animal: str


BRANCHES: list[Branch] = [
    Branch(0,  "子", "Zi",   "23:00 - 01:00", 23, Element.WATER, "Rat"),
    Branch(1,  "丑", "Chou", "01:00 - 03:00",  1, Element.EARTH, "Ox"),
    Branch(2,  "寅", "Yin",  "03:00 - 05:00",  3, Element.WOOD,  "Tiger"),
    Branch(3,  "卯", "Mao",  "05:00 - 07:00",  5, Element.WOOD,  "Rabbit"),
    Branch(4,  "辰", "Chen", "07:00 - 09:00",  7, Element.EARTH, "Dragon"),
    Branch(5,  "巳", "Si",   "09:00 - 11:00",  9, Element.FIRE,  "Snake"),
    Branch(6,  "午", "Wu",   "11:00 - 13:00", 11, Element.FIRE,  "Horse"),
    Branch(7,  "未", "Wei",  "13:00 - 15:00", 13, Element.EARTH, "Goat"),
    Branch(8,  "申", "Shen", "15:00 - 17:00", 15, Element.METAL, "Monkey"),
    Branch(9,  "酉", "You",  "17:00 - 19:00", 17, Element.METAL, "Rooster"),
    Branch(10, "戌", "Xu",   "19:00 - 21:00", 19, Element.EARTH, "Dog"),
    Branch(11, "亥", "Hai",  "21:00 - 23:00", 21, Element.WATER, "Pig"),
]


# ── 8 Gates (八門) ──────────────────────────────────────────────────────────

@dataclass
class Gate:
    index: int
    name_cn: str
    name_en: str
    name_th: str
    quality: str        # "auspicious" | "mixed" | "avoid"
    suitable_en: list[str]
    suitable_th: list[str]
    avoid_en: list[str]
    avoid_th: list[str]


GATES: list[Gate] = [
    Gate(0, "開門", "Open Gate",   "ประตูเปิด",
         "auspicious",
         ["Start important negotiations", "Sign contracts", "Launch new ventures", "Meet influential people"],
         ["เริ่มการเจรจาสำคัญ", "เซ็นสัญญา", "เปิดตัวกิจการใหม่", "พบปะผู้มีอิทธิพล"],
         ["Passive activities", "Hiding or retreating"],
         ["กิจกรรมเชิงรับ", "การหลบเลี่ยงหรือถอยหนี"]),

    Gate(1, "休門", "Rest Gate",   "ประตูพักผ่อน",
         "auspicious",
         ["Strategic planning", "Deep work", "Relationship nurturing", "Healing and recovery"],
         ["วางแผนกลยุทธ์", "ทำงานเชิงลึก", "บ่มเพาะความสัมพันธ์", "พักฟื้นและฟื้นตัว"],
         ["Aggressive confrontation", "Risky financial moves"],
         ["การเผชิญหน้าที่รุนแรง", "การเคลื่อนไหวทางการเงินที่เสี่ยง"]),

    Gate(2, "生門", "Life Gate",   "ประตูชีวิต",
         "auspicious",
         ["Business deals", "Financial transactions", "New partnerships", "Investment decisions"],
         ["ทำธุรกรรมทางธุรกิจ", "ธุรกรรมการเงิน", "พันธมิตรใหม่", "การตัดสินใจลงทุน"],
         ["Ending relationships", "Destructive activities"],
         ["การยุติความสัมพันธ์", "กิจกรรมที่สร้างความเสียหาย"]),

    Gate(3, "傷門", "Injury Gate", "ประตูบาดเจ็บ",
         "mixed",
         ["Competition", "Assertive negotiations", "Legal proceedings", "Athletic performance"],
         ["การแข่งขัน", "การเจรจาที่แข็งกร้าว", "กระบวนการทางกฎหมาย", "ผลการแข่งขันกีฬา"],
         ["Delicate negotiations", "Medical procedures if avoidable"],
         ["การเจรจาที่ละเอียดอ่อน", "หัตถการทางการแพทย์ถ้าหลีกเลี่ยงได้"]),

    Gate(4, "杜門", "Block Gate",  "ประตูกีดขวาง",
         "avoid",
         ["Meditation", "Private reflection only"],
         ["นั่งสมาธิ", "การใคร่ครวญส่วนตัวเท่านั้น"],
         ["Important meetings", "Contracts", "Travel", "Financial decisions"],
         ["การประชุมสำคัญ", "สัญญา", "การเดินทาง", "การตัดสินใจทางการเงิน"]),

    Gate(5, "景門", "Scene Gate",  "ประตูทัศนียภาพ",
         "mixed",
         ["Creative work", "Marketing", "Public speaking", "Social media", "Art and writing"],
         ["งานสร้างสรรค์", "การตลาด", "การพูดในที่สาธารณะ", "โซเชียลมีเดีย", "ศิลปะและการเขียน"],
         ["Secret negotiations", "Private matters"],
         ["การเจรจาลับ", "เรื่องส่วนตัว"]),

    Gate(6, "死門", "Death Gate",  "ประตูมรณะ",
         "avoid",
         ["Only for rituals, funerals, or endings you intentionally seek"],
         ["เฉพาะพิธีกรรม งานศพ หรือการสิ้นสุดที่คุณตั้งใจ"],
         ["New beginnings", "Contracts", "Travel", "Medical procedures", "All important activities"],
         ["การเริ่มต้นใหม่", "สัญญา", "การเดินทาง", "หัตถการทางการแพทย์", "กิจกรรมสำคัญทั้งหมด"]),

    Gate(7, "驚門", "Shock Gate",  "ประตูตกใจ",
         "avoid",
         ["Uncovering hidden information", "Investigation only"],
         ["การเปิดเผยข้อมูลที่ซ่อนอยู่", "การสืบสวนเท่านั้น"],
         ["Presenting proposals", "Meetings", "Travel", "Financial commitments"],
         ["การนำเสนอข้อเสนอ", "การประชุม", "การเดินทาง", "ความมุ่งมั่นทางการเงิน"]),
]

GATE_BY_INTERACTION: dict[InteractionType, int] = {
    InteractionType.RESOURCE:  2,  # Life Gate
    InteractionType.WEALTH:    0,  # Open Gate
    InteractionType.COMPANION: 1,  # Rest Gate
    InteractionType.OUTPUT:    5,  # Scene Gate
    InteractionType.OFFICER:   6,  # Death Gate
}

# Modifiers: shift gate index based on hour branch offset for variety
_HOUR_GATE_SHIFT: list[int] = [0, 1, 2, 3, 0, 1, 7, 4, 2, 3, 6, 5]

# Short activity labels per gate — used in one_liner output
_GATE_SHORT_LABEL_EN: dict[int, str] = {
    0: "Great for initiating — sign, launch, lead",
    1: "Great for deep work — plan, strategise, heal",
    2: "Great for deals — money, partnerships, investments",
    3: "Suited for competition — push hard, negotiate assertively",
    4: "Low energy — avoid key decisions",
    5: "Creative window — present, write, pitch",
    6: "Avoid all action — rest or routine only",
    7: "Caution — observe, do not commit",
}

_GATE_SHORT_LABEL_TH: dict[int, str] = {
    0: "ดีสำหรับการริเริ่ม — เซ็น เปิดตัว นำ",
    1: "ดีสำหรับงานลึก — วางแผน กลยุทธ์ พักฟื้น",
    2: "ดีสำหรับดีล — การเงิน พันธมิตร ลงทุน",
    3: "เหมาะสำหรับการแข่งขัน — ผลักดัน เจรจาแข็งกร้าว",
    4: "พลังงานต่ำ — หลีกเลี่ยงการตัดสินใจสำคัญ",
    5: "หน้าต่างสร้างสรรค์ — นำเสนอ เขียน พิตช์",
    6: "หลีกเลี่ยงทุกอย่าง — พักผ่อนหรืองานประจำเท่านั้น",
    7: "ระวัง — สังเกต อย่าผูกมัด",
}

# Compass direction for each earthly branch (energy arriving from this direction)
_BRANCH_DIRECTION_EN: dict[int, str] = {
    0:  "North",      # Zi
    1:  "Northeast",  # Chou
    2:  "Northeast",  # Yin
    3:  "East",       # Mao
    4:  "Southeast",  # Chen
    5:  "Southeast",  # Si
    6:  "South",      # Wu
    7:  "Southwest",  # Wei
    8:  "Southwest",  # Shen
    9:  "West",       # You
    10: "Northwest",  # Xu
    11: "Northwest",  # Hai
}

_BRANCH_DIRECTION_TH: dict[int, str] = {
    0:  "เหนือ",
    1:  "ตะวันออกเฉียงเหนือ",
    2:  "ตะวันออกเฉียงเหนือ",
    3:  "ตะวันออก",
    4:  "ตะวันออกเฉียงใต้",
    5:  "ตะวันออกเฉียงใต้",
    6:  "ใต้",
    7:  "ตะวันตกเฉียงใต้",
    8:  "ตะวันตกเฉียงใต้",
    9:  "ตะวันตก",
    10: "ตะวันตกเฉียงเหนือ",
    11: "ตะวันตกเฉียงเหนือ",
}


# ── Power directions by element ─────────────────────────────────────────────

POWER_DIRECTION: dict[Element, dict] = {
    Element.WOOD:  {"en": "East",      "th": "ทิศตะวันออก"},
    Element.FIRE:  {"en": "South",     "th": "ทิศใต้"},
    Element.EARTH: {"en": "Southwest", "th": "ทิศตะวันตกเฉียงใต้"},
    Element.METAL: {"en": "West",      "th": "ทิศตะวันตก"},
    Element.WATER: {"en": "North",     "th": "ทิศเหนือ"},
}

# Day master power color reinforcement by element interaction
_INTERACTION_TIP_EN: dict[InteractionType, str] = {
    InteractionType.RESOURCE:  "Favourable — this element nourishes your Day Master. Act with confidence.",
    InteractionType.WEALTH:    "Productive — your Day Master dominates this energy. Channel it into results.",
    InteractionType.COMPANION: "Stable — aligned energy. Collaborative efforts excel.",
    InteractionType.OUTPUT:    "Expressive — your energy flows outward. Good for creation and communication.",
    InteractionType.OFFICER:   "Challenging — this element presses against your Day Master. Conserve, observe, do not initiate.",
}

_INTERACTION_TIP_TH: dict[InteractionType, str] = {
    InteractionType.RESOURCE:  "เป็นใจ — ธาตุนี้หล่อเลี้ยง Day Master ของคุณ ลงมือได้อย่างมั่นใจ",
    InteractionType.WEALTH:    "เกื้อกูล — Day Master ของคุณควบคุมพลังงานนี้ได้ ชี้นำมันสู่ผลลัพธ์",
    InteractionType.COMPANION: "มั่นคง — พลังงานสอดคล้องกัน ความร่วมมือจะให้ผลดี",
    InteractionType.OUTPUT:    "แสดงออก — พลังงานของคุณไหลออกสู่ภายนอก เหมาะสำหรับการสร้างสรรค์และสื่อสาร",
    InteractionType.OFFICER:   "ท้าทาย — ธาตุนี้กดทับ Day Master ของคุณ รักษาพลัง สังเกต อย่าริเริ่ม",
}


# ── Main output types ────────────────────────────────────────────────────────

@dataclass
class HourWindow:
    branch: Branch
    element: Element
    interaction: InteractionType
    gate: Gate
    power_direction_en: str
    power_direction_th: str
    tip_en: str
    tip_th: str

    def to_dict(self) -> dict:
        gate_short_en = _GATE_SHORT_LABEL_EN.get(self.gate.index, self.gate.name_en)
        gate_short_th = _GATE_SHORT_LABEL_TH.get(self.gate.index, self.gate.name_th)
        hour_dir_en   = _BRANCH_DIRECTION_EN[self.branch.index]
        hour_dir_th   = _BRANCH_DIRECTION_TH[self.branch.index]

        if self.gate.quality == "avoid":
            one_liner_en = f"{self.branch.time_range}  {gate_short_en}"
            one_liner_th = f"{self.branch.time_range}  {gate_short_th}"
        else:
            one_liner_en = (
                f"{self.branch.time_range}  {gate_short_en}"
                f"  |  {hour_dir_en} best direction for you"
            )
            one_liner_th = (
                f"{self.branch.time_range}  {gate_short_th}"
                f"  |  ทิศ{hour_dir_th} ดีที่สุดสำหรับคุณ"
            )

        return {
            "one_liner_en":       one_liner_en,
            "one_liner_th":       one_liner_th,
            "time_range":         self.branch.time_range,
            "branch":             f"{self.branch.name_cn} {self.branch.name_en} ({self.branch.animal})",
            "element":            self.element.value.upper(),
            "interaction":        self.interaction.value.upper(),
            "gate_cn":            self.gate.name_cn,
            "gate_en":            self.gate.name_en,
            "gate_th":            self.gate.name_th,
            "gate_short_en":      gate_short_en,
            "gate_short_th":      gate_short_th,
            "quality":            self.gate.quality,
            "hour_direction_en":  hour_dir_en,
            "hour_direction_th":  f"ทิศ{hour_dir_th}",
            "power_direction_en": self.power_direction_en,
            "power_direction_th": self.power_direction_th,
            "suitable_en":        self.gate.suitable_en,
            "suitable_th":        self.gate.suitable_th,
            "avoid_en":           self.gate.avoid_en,
            "avoid_th":           self.gate.avoid_th,
            "tip_en":             self.tip_en,
            "tip_th":             self.tip_th,
        }


@dataclass
class QiMenResult:
    date: date
    day_master: Element
    daily_element: Element
    auspicious: list[HourWindow]
    mixed: list[HourWindow]
    avoid: list[HourWindow]
    all_hours: list[HourWindow]

    def to_dict(self) -> dict:
        return {
            "date":           self.date.isoformat(),
            "day_master":     self.day_master.value.upper(),
            "daily_element":  self.daily_element.value.upper(),
            "best_windows":   [h.to_dict() for h in self.auspicious[:3]],
            "auspicious_hours": [h.to_dict() for h in self.auspicious],
            "mixed_hours":      [h.to_dict() for h in self.mixed],
            "avoid_hours":      [h.to_dict() for h in self.avoid],
            "all_hours":        [h.to_dict() for h in self.all_hours],
        }


# ── Calculator ───────────────────────────────────────────────────────────────

def get_current_window(result: QiMenResult, now: Optional[datetime] = None) -> Optional[HourWindow]:
    """Return the HourWindow that is active right now (or at `now` if provided).

    Handles Zi (子) branch which crosses midnight: 23:00–01:00.
    """
    h = (now or datetime.now()).hour
    for w in result.all_hours:
        start = w.branch.start_hour
        if start == 23:
            if h == 23 or h == 0:
                return w
        elif start <= h < start + 2:
            return w
    return None


def calculate_qimen(target_date: date, day_master: Element, daily_element: Element) -> QiMenResult:
    """Generate 12 two-hour windows for target_date with QMDJ classification."""
    n = _ordinal_day(target_date)
    day_stem_idx = n % 10  # 0-9

    all_windows: list[HourWindow] = []

    for branch in BRANCHES:
        hour_element = branch.element
        interaction  = classify_interaction(hour_element, day_master)

        # Gate selection: base from interaction type, shifted by hour branch for variety
        base_gate_idx = GATE_BY_INTERACTION[interaction]
        shift         = _HOUR_GATE_SHIFT[branch.index]
        # Apply shift only for mixed/avoid gates to create richer variety
        if interaction in (InteractionType.OUTPUT, InteractionType.OFFICER):
            gate_idx = (base_gate_idx + (day_stem_idx % 2) + shift) % 8
            # Re-check: don't accidentally make OFFICER → auspicious
            if interaction == InteractionType.OFFICER and GATES[gate_idx].quality == "auspicious":
                gate_idx = 6  # Force Death Gate for strong clashes
        else:
            gate_idx = base_gate_idx

        gate      = GATES[gate_idx]
        direction = POWER_DIRECTION[day_master]  # face your power direction for max effect

        window = HourWindow(
            branch=branch,
            element=hour_element,
            interaction=interaction,
            gate=gate,
            power_direction_en=direction["en"],
            power_direction_th=direction["th"],
            tip_en=_INTERACTION_TIP_EN[interaction],
            tip_th=_INTERACTION_TIP_TH[interaction],
        )
        all_windows.append(window)

    auspicious = [w for w in all_windows if w.gate.quality == "auspicious"]
    mixed      = [w for w in all_windows if w.gate.quality == "mixed"]
    avoid      = [w for w in all_windows if w.gate.quality == "avoid"]

    return QiMenResult(
        date=target_date,
        day_master=day_master,
        daily_element=daily_element,
        auspicious=auspicious,
        mixed=mixed,
        avoid=avoid,
        all_hours=all_windows,
    )
