"""4-agent coaching pipeline.

Primary AI: Anthropic Claude (claude-opus-4-5).
Fallback   : OpenAI GPT-4o  (if ANTHROPIC_API_KEY is empty but OPENAI_API_KEY is set).
DB fallback: If neither key is set, assembles from DB content only.
"""

import json
import time
from dataclasses import dataclass, field  # noqa: F401 (field used in PipelineResult)
from typing import Optional

from sqlalchemy.orm import Session

from core.config import settings
from services.criteria import get_mbti_decisions, get_hd_decisions, get_scenario
from services.color_service import get_color_profile
from services.memory_service import (
    generate_variation_seed, select_variation, get_active_memories, record_memory,
)
from prompts.system.coaching_agent import SYSTEM_PROMPT as COACHING_SYSTEM
from prompts.system.dialogue_agent import SYSTEM_PROMPT as DIALOGUE_SYSTEM
from prompts.builders.build_coaching_prompt import build_coaching_prompt, build_dialogue_prompt


@dataclass
class PipelineResult:
    bazi_score: float
    # English
    behavior_recommendation: str
    timing_guidance: str
    communication_strategy: str
    warnings: list[str]
    practical_tips: list[str]
    sample_sentences: list[str]
    alternative_responses: list[str]
    coaching_summary: str
    # Thai (always populated together with EN)
    behavior_recommendation_th: str = ""
    timing_guidance_th: str = ""
    communication_strategy_th: str = ""
    warnings_th: list[str] = field(default_factory=list)
    practical_tips_th: list[str] = field(default_factory=list)
    sample_sentences_th: list[str] = field(default_factory=list)
    alternative_responses_th: list[str] = field(default_factory=list)
    coaching_summary_th: str = ""
    # Meta
    variation_seed: str = ""
    variation_angle: str = ""
    generation_model: str = ""
    generation_ms: int = 0


# ── AI call helpers ────────────────────────────────────────────────────────────

def _call_claude(system: str, user: str) -> dict:
    import anthropic
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    msg = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2500,
        temperature=1,          # claude uses default temperature via top_p; set to 1 for max variation
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    text = msg.content[0].text
    # Strip markdown code fences if present
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return json.loads(text)


def _call_gemini(system: str, user: str) -> dict:
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=user,
        config=types.GenerateContentConfig(
            system_instruction=system,
            response_mime_type="application/json",
        ),
    )
    return json.loads(response.text)


def _call_openai(system: str, user: str) -> dict:
    from openai import OpenAI
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    resp = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": user},
        ],
        temperature=0.9,
        max_tokens=2500,
    )
    return json.loads(resp.choices[0].message.content)


def _call_ai(system: str, user: str) -> tuple[dict, str]:
    """Priority: Gemini (free) → Claude Sonnet → OpenAI GPT-4o.
    Each step falls through on any error so the pipeline never crashes."""
    if settings.GEMINI_API_KEY:
        try:
            return _call_gemini(system, user), "gemini-2.0-flash"
        except Exception as e:
            print(f"[pipeline] Gemini failed ({type(e).__name__}), trying next...")
    if settings.ANTHROPIC_API_KEY:
        try:
            return _call_claude(system, user), "claude-sonnet-4-5"
        except Exception as e:
            print(f"[pipeline] Claude failed ({type(e).__name__}), trying next...")
    if settings.OPENAI_API_KEY:
        try:
            return _call_openai(system, user), "gpt-4o"
        except Exception as e:
            print(f"[pipeline] OpenAI failed ({type(e).__name__}), trying next...")
    raise RuntimeError("All AI providers failed or no key configured")


# ── HD type → strategy lookup ─────────────────────────────────────────────────
_HD_STRATEGY = {
    "Manifestor":             ("Inform before you act",           "แจ้งให้คนรอบข้างทราบก่อนลงมือ"),
    "Generator":              ("Wait to respond",                 "รอตอบสนองต่อสิ่งที่เข้ามา"),
    "Manifesting Generator":  ("Wait to respond, then inform",    "รอตอบสนองก่อน แล้วจึงแจ้งให้ทราบ"),
    "Projector":              ("Wait for the invitation",         "รอการเชิญชวนก่อนเริ่มต้น"),
    "Reflector":              ("Wait a lunar cycle",              "รอให้ครบรอบจันทร์ก่อนตัดสินใจใหญ่"),
}

def _hd_warning_en(hd_type: Optional[str]) -> str:
    name = hd_type or "your Human Design type"
    strategy, _ = _HD_STRATEGY.get(hd_type or "", ("follow your Human Design strategy", ""))
    return (
        f"You are a Human Design {name} — your strategy is to {strategy}. "
        f"Why: acting against this burns your energy and creates unnecessary resistance, "
        f"even when your intentions are right."
    )

def _hd_warning_th(hd_type: Optional[str]) -> str:
    name = hd_type or "ประเภทของคุณ"
    _, strategy_th = _HD_STRATEGY.get(hd_type or "", ("", "ทำตาม strategy ของ Human Design คุณ"))
    return (
        f"Human Design ของคุณคือ {name} — strategy ของคุณคือ{strategy_th} "
        f"เพราะ: การฝืน strategy นี้จะดูดพลังงานของคุณและสร้างแรงต้านโดยไม่จำเป็น "
        f"แม้เจตนาของคุณจะถูกต้องก็ตาม"
    )

# ── Context builders ───────────────────────────────────────────────────────────

def _build_profile_ctx(
    db: Session, mbti_type: str, hd_type: Optional[str],
    personal_color: Optional[str], goal: str,
) -> dict:
    from models.orm import MbtiTypeProfile, HdTypeProfile

    mbti_row = db.query(MbtiTypeProfile).filter_by(type_code=mbti_type).first()
    hd_row   = db.query(HdTypeProfile).filter_by(hd_type=hd_type).first() if hd_type else None
    color    = get_color_profile(db, personal_color)
    scenario = get_scenario(db, mbti_type, hd_type)

    def _split(val: Optional[str]) -> list[str]:
        return [x.strip() for x in val.split("|")] if val else []

    return {
        "mbti_code":               mbti_type,
        "mbti_communication_style": getattr(mbti_row, "communication_style", "") or "",
        "mbti_decision_pattern":    getattr(mbti_row, "decision_making", "") or "",
        "mbti_blind_spots":         _split(getattr(mbti_row, "blind_spots", "")),
        "mbti_sample_openers":      [],

        "hd_type_name":          hd_type or "None",
        "hd_strategy":           getattr(hd_row, "strategy", "") or "",
        "hd_energy_type":        getattr(hd_row, "energy_pattern", "") or "",
        "hd_negotiation_timing": getattr(hd_row, "decision_making", "") or "",
        "hd_negotiation_entry":  getattr(hd_row, "strategy", "") or "",
        "hd_common_mistakes":    _split(getattr(hd_row, "challenges", "")),

        "color_season":            personal_color or "None",
        "color_communication_vibe": color.get("communication_vibe", "") if color else "",
        "color_language_style":    color.get("language_style", "") if color else "",
        "color_impression":        _split(color.get("impression", "")) if color else [],

        "scenario_blend":         scenario.get("blend_summary", "") if scenario else "",
        "scenario_conflict":      scenario.get("conflict_situation", "") if scenario else "",
        "scenario_sample_phrases": [scenario.get("recommended_sentence", "")] if scenario else [],
    }


def _build_goal_ctx(db: Session, mbti_type: str, hd_type: Optional[str], goal: str) -> dict:
    goal_labels = {
        "work":         "Work & Leadership",
        "money":        "Money & Negotiation",
        "relationship": "Relationship & Connection",
    }
    return {
        "goal_slug":      goal,
        "goal_label":     goal_labels.get(goal, goal.title()),
        "mbti_decisions": get_mbti_decisions(db, mbti_type, goal=goal),
        "hd_decisions":   get_hd_decisions(db, hd_type, goal=goal),
        "scenario":       get_scenario(db, mbti_type, hd_type),
    }


# ── DB-only fallback (no AI key) ───────────────────────────────────────────────

_GOAL_FALLBACK = {
    "work": {
        "behavior":    "Lead from your cognitive strengths. Establish your frame before the meeting starts.",
        "behavior_th": "นำด้วยจุดแข็งทางความคิดของคุณ กำหนดกรอบการสนทนาก่อนที่การประชุมจะเริ่ม",
        "timing":      "Use the first 30 minutes of your peak BaZi window for the key decision.",
        "timing_th":   "ใช้ 30 นาทีแรกของช่วง BaZi สูงสุดสำหรับการตัดสินใจสำคัญ",
        "comm":        "Speak with precision. State the outcome before the rationale.",
        "comm_th":     "พูดอย่างตรงจุด บอกผลลัพธ์ที่ต้องการก่อนอธิบายเหตุผล",
        "tips": [
            "Dress in your Day Master power color for authority presence.",
            "Sit facing your power direction during the key meeting.",
            "Open with the outcome, not the process — set the frame early.",
            "Your peak window: use the BaZi element peak hours for final decisions.",
            "Avoid over-explaining — state position once, then hold silence.",
        ],
        "tips_th": [
            "แต่งกายด้วยสี Day Master ของคุณเพื่อสร้างความน่าเชื่อถือ",
            "นั่งหันหน้าไปทิศทางพลังงานของคุณระหว่างการประชุมสำคัญ",
            "เปิดด้วยผลลัพธ์ ไม่ใช่กระบวนการ — กำหนดกรอบตั้งแต่ต้น",
            "ช่วงเวลาสูงสุด: ใช้ช่วงเวลา BaZi element สำหรับการตัดสินใจขั้นสุดท้าย",
            "อย่าอธิบายมากเกินไป — พูดจุดยืนครั้งเดียว แล้วเงียบ",
        ],
        "sentences": [
            "Opening the meeting :: What I intend to leave this room with is absolute clarity on three things — let me articulate them now.",
            "Setting direction :: The deliberation is concluded. Here is the direction, and here is precisely why it is the most defensible path forward.",
            "Handling pushback :: I appreciate the candour — and I'd invite you to consider whether that objection addresses the core constraint, or a peripheral one.",
            "Closing the discussion :: We are aligned. I will assume ownership of the outcome and revert with a structured update at a cadence that serves you.",
        ],
        "sentences_th": [
            "เปิดการประชุม :: สิ่งที่ผมต้องการจะออกจากห้องนี้ไปด้วยคือความชัดเจนอย่างสมบูรณ์ใน 3 ประเด็น — ขอชี้แจงตอนนี้เลย",
            "กำหนดทิศทาง :: การพิจารณาสิ้นสุดแล้ว นี่คือทิศทาง และนี่คือเหตุผลว่าทำไมมันถึงเป็นเส้นทางที่ถูกต้องที่สุด",
            "รับมือข้อโต้แย้ง :: ขอบคุณที่พูดตรงๆ — และขอเชิญพิจารณาว่าข้อโต้แย้งนั้นตอบข้อจำกัดหลัก หรือเพียงแค่ปัญหารอง",
            "ปิดการสนทนา :: เราเห็นพ้องกันแล้ว ผมจะรับผิดชอบผลลัพธ์และรายงานความคืบหน้าในรูปแบบที่ชัดเจนตามเวลาที่เหมาะสม",
        ],
        "alts":    ["Before we close :: Before we adjourn, I'd welcome any outstanding reservations — better surfaced now than compounded later.", "Testing alignment :: What conditions would need to hold for this to be considered unambiguously successful in your view?"],
        "alts_th": ["ก่อนจบการประชุม :: ก่อนที่เราจะสรุป ผมยินดีรับฟังความกังวลที่ยังคงอยู่ — ดีกว่าให้มันสะสมในภายหลัง", "ทดสอบความเห็นตรงกัน :: ในมุมมองของคุณ อะไรคือเงื่อนไขที่ต้องเป็นจริงเพื่อให้สิ่งนี้ถือว่าประสบความสำเร็จอย่างชัดเจน?"],
        "summary":    "Lead with your frame, hold silence, let your position do the work.",
        "summary_th": "นำด้วยกรอบของคุณ เงียบให้เป็น แล้วปล่อยให้จุดยืนทำงานแทน",
    },
    "money": {
        "behavior":    "Let them speak first. Your silence after naming a number is your strongest tool.",
        "behavior_th": "ให้อีกฝ่ายพูดก่อน ความเงียบหลังจากบอกตัวเลขคืออาวุธที่แข็งแกร่งที่สุดของคุณ",
        "timing":      "Avoid initiating the negotiation in the first hour of the day. Wait for your BaZi peak.",
        "timing_th":   "อย่าเริ่มการเจรจาในชั่วโมงแรกของวัน รอจนถึงช่วง BaZi สูงสุด",
        "comm":        "Use fewer words than feels natural. Precision over volume.",
        "comm_th":     "ใช้คำน้อยกว่าที่รู้สึกว่าควรจะพูด ความแม่นยำสำคัญกว่าปริมาณ",
        "tips": [
            "Dress in your Day Master power color — it signals stability and authority.",
            "Let them make the first offer. Silence is not awkward — it is leverage.",
            "After stating your number, count to 5 before speaking again.",
            "Sit with your back to the wall, facing the door — power position.",
            "Avoid negotiating when BaZi score is below 4 — reschedule if possible.",
        ],
        "tips_th": [
            "แต่งกายด้วยสี Day Master — มันส่งสัญญาณความมั่นคงและอำนาจ",
            "ให้อีกฝ่ายเสนอราคาก่อน ความเงียบไม่ใช่ความอึดอัด — มันคืออำนาจต่อรอง",
            "หลังจากบอกตัวเลขแล้ว นับ 1-5 ก่อนพูดอีกครั้ง",
            "นั่งโดยให้หลังชิดกำแพง หันหน้าไปทางประตู — ตำแหน่งแห่งอำนาจ",
            "หลีกเลี่ยงการเจรจาเมื่อคะแนน BaZi ต่ำกว่า 4 — เลื่อนนัดถ้าเป็นไปได้",
        ],
        "sentences": [
            "Anchoring your position :: The figure I'm prepared to commit to is [X] — and I'd ask that we treat that as our foundation rather than our opening.",
            "After they counter :: I'd need that proposal to be considerably more precise before I can offer a considered response.",
            "Holding the line :: That particular structure doesn't serve the outcome I'm working toward — I'm curious what latitude you actually have here.",
            "Deploying silence :: [State your number with measured composure — then hold the silence. Let them feel the weight of it.]",
        ],
        "sentences_th": [
            "ยึดจุดยืน :: ตัวเลขที่ผมพร้อมยืนยันคือ [X] — และขอให้เราถือว่านี่เป็นจุดเริ่มต้น ไม่ใช่ตัวเลขเปิด",
            "หลังอีกฝ่าย counter :: ผมต้องการให้ข้อเสนอนั้นชัดเจนยิ่งกว่านี้มาก ก่อนที่จะสามารถตอบสนองได้อย่างถี่ถ้วน",
            "ยืนหยัดจุดยืน :: โครงสร้างแบบนั้นไม่ตอบโจทย์ที่ผมมุ่งไป — สงสัยว่าคุณมีความยืดหยุ่นอยู่เท่าไหร่จริงๆ",
            "ใช้ความเงียบ :: [บอกตัวเลขด้วยความสงบ — แล้วถือความเงียบไว้ ให้อีกฝ่ายรู้สึกถึงน้ำหนักของมัน]",
        ],
        "alts":    ["Reading their hesitation :: I'd welcome some transparency on the reasoning that underpins that particular figure.", "Reopening the space :: I'm genuinely open to a more creative structure — what are the parameters you're actually working within?"],
        "alts_th": ["อ่านความลังเล :: ผมยินดีที่จะรับฟังเหตุผลเบื้องหลังตัวเลขนั้นอย่างตรงไปตรงมา", "เปิดพื้นที่ใหม่ :: ผมเปิดใจต่อโครงสร้างที่สร้างสรรค์กว่านี้ — คุณทำงานอยู่ภายในเงื่อนไขอะไรบ้าง?"],
        "summary":    "Silence after your number is leverage — use it.",
        "summary_th": "ความเงียบหลังบอกตัวเลขคืออำนาจต่อรอง — ใช้มันให้เป็น",
    },
    "relationship": {
        "behavior":    "Match their pace for the first 90 seconds before introducing your own rhythm.",
        "behavior_th": "ปรับจังหวะให้เข้ากับอีกฝ่ายใน 90 วินาทีแรก ก่อนที่จะนำจังหวะของตัวเองเข้าไป",
        "timing":      "Deep conversations land better after 4pm when the day's pressure has passed.",
        "timing_th":   "การสนทนาลึกจะได้ผลดีกว่าหลัง 4 โมงเย็น เมื่อแรงกดดันของวันผ่านไปแล้ว",
        "comm":        "Listen to understand, not to respond. Ask one question at a time.",
        "comm_th":     "ฟังเพื่อเข้าใจ ไม่ใช่เพื่อตอบ ถามทีละคำถาม",
        "tips": [
            "Wear warm tones today — they signal openness and approachability.",
            "Mirror their speaking pace for the first 2 minutes before shifting.",
            "Ask one question, then give them full space to answer.",
            "Sit at a 90-degree angle rather than directly facing — less confrontational.",
            "Avoid problem-solving until they feel fully heard — ask 'is there more?' first.",
        ],
        "tips_th": [
            "สวมใส่โทนสีอบอุ่นวันนี้ — มันส่งสัญญาณความเปิดใจและเป็นมิตร",
            "สะท้อนจังหวะการพูดของอีกฝ่ายใน 2 นาทีแรกก่อนเปลี่ยน",
            "ถามคำถามเดียว แล้วให้พื้นที่เต็มที่กับเขาในการตอบ",
            "นั่งทำมุม 90 องศาแทนการหันหน้าเผชิญกัน — ลดความรู้สึกเผชิญหน้า",
            "อย่าแก้ปัญหาจนกว่าอีกฝ่ายจะรู้สึกว่าถูกรับฟังอย่างเต็มที่ — ถาม 'มีอะไรอีกไหม?' ก่อน",
        ],
        "sentences": [
            "Opening the conversation :: I'd genuinely love to understand — not just the situation, but what it felt like from where you were standing.",
            "Before sharing your view :: Before I offer my perspective, I want to be certain I've done justice to yours — is there more you'd like me to hold?",
            "Finding what matters :: Beneath all of this, what is it that you're most deeply invested in preserving?",
            "After they finish :: That lands with more weight than I anticipated — give me a moment to sit with it before I respond.",
        ],
        "sentences_th": [
            "เปิดบทสนทนา :: ผมอยากเข้าใจจริงๆ — ไม่ใช่แค่สถานการณ์ แต่รวมถึงความรู้สึกจากมุมของคุณด้วย",
            "ก่อนแชร์มุมมอง :: ก่อนที่จะแสดงความคิดเห็น อยากแน่ใจว่าผมเข้าใจมุมมองของคุณอย่างถ่องแท้ — มีอะไรเพิ่มเติมที่อยากให้ผมรับรู้ไหม?",
            "ค้นหาสิ่งสำคัญ :: ลึกๆ แล้ว สิ่งที่คุณให้ความสำคัญและต้องการปกป้องมากที่สุดคืออะไร?",
            "หลังอีกฝ่ายพูดจบ :: สิ่งที่คุณพูดมีน้ำหนักมากกว่าที่ผมคาดไว้ — ขอเวลาสักครู่เพื่อตกตะกอนก่อนตอบ",
        ],
        "alts":    ["When they seem stuck :: I wonder if the answer lives somewhere between both of our stated positions — what would you be willing to explore?", "Reflecting back :: What I'm hearing, beneath the words, is [X] — am I perceiving that with any accuracy?"],
        "alts_th": ["เมื่ออีกฝ่ายดูติด :: คำตอบอาจอยู่ตรงกลางระหว่างจุดยืนของเราทั้งสองฝ่าย — คุณพร้อมจะสำรวจแนวทางนั้นไหม?", "สะท้อนกลับ :: สิ่งที่ผมได้ยินเบื้องหลังคำพูดคือ [X] — ผมเข้าใจถูกต้องไหม?"],
        "summary":    "Be present, match their pace, and ask before you advise.",
        "summary_th": "อยู่กับปัจจุบัน ปรับจังหวะให้เข้ากัน และถามก่อนให้คำแนะนำ",
    },
}


# ── Main pipeline ──────────────────────────────────────────────────────────────

def run_pipeline(
    db: Session,
    user_id: int,
    mbti_type: str,
    hd_type: Optional[str],
    personal_color: Optional[str],
    goal: str,
    bazi_score: float,
    day_master: str = "UNKNOWN",
    daily_element: str = "UNKNOWN",
    # ── New DB-computed energy fields (token-free pre-computation) ───────
    stance: str = "NEUTRAL",
    stance_th: str = "ปกติ",
    strong_day: bool = False,
    lead_colour: str = "",
    lead_colour_hex: str = "",
    secondary_colour: str = "",
    power_direction: str = "",
    planetary_hour_ruler: str = "",
    planetary_hour_best_for: str = "",
    planetary_hour_avoid: str = "",
    peak_hour_window: str = "",
    thai_day_ruler: str = "",
    saturn_note: str = "",
) -> PipelineResult:
    t_start = time.time()

    # Agent 1 + 2: build contexts (no AI call)
    profile_ctx = _build_profile_ctx(db, mbti_type, hd_type, personal_color, goal)
    goal_ctx    = _build_goal_ctx(db, mbti_type, hd_type, goal)

    # Variation
    memories        = get_active_memories(db, user_id, goal_context=goal)
    excluded_angles = [m["content"] for m in memories if m["type"] == "used_angle"]
    variation_seed  = generate_variation_seed(user_id)
    variation       = select_variation(variation_seed, excluded_angles)
    gen_count       = len(memories) + 1

    # DB-only fallback when no AI key is configured
    if not settings.ANTHROPIC_API_KEY and not settings.OPENAI_API_KEY and not settings.GEMINI_API_KEY:
        fb = _GOAL_FALLBACK.get(goal, _GOAL_FALLBACK["work"])
        return PipelineResult(
            bazi_score=bazi_score,
            behavior_recommendation=fb["behavior"],
            timing_guidance=fb["timing"] + f" (BaZi score today: {bazi_score:.1f}/10)",
            communication_strategy=fb["comm"],
            warnings=[
                _hd_warning_en(hd_type),
                "Wear your Day Master power color today. Why: your Day Master element needs visual reinforcement to stay dominant — without it, opposing elements in today's energy can suppress your natural authority.",
                "Avoid colors that clash with today's Element energy. Why: drain colors create an energetic imbalance that subtly undermines your confidence and how others perceive your credibility.",
            ],
            practical_tips=fb["tips"],
            sample_sentences=fb["sentences"],
            alternative_responses=fb.get("alts", ["Adapt as the conversation evolves."]),
            coaching_summary=fb.get("summary", f"{mbti_type} + {hd_type or 'no HD'} — {goal.title()} session."),
            # TH
            behavior_recommendation_th=fb["behavior_th"],
            timing_guidance_th=fb["timing_th"] + f" (BaZi score วันนี้: {bazi_score:.1f}/10)",
            communication_strategy_th=fb["comm_th"],
            warnings_th=[
                _hd_warning_th(hd_type),
                "สวมสี Day Master power color วันนี้ เพราะ: Element ของ Day Master ต้องการการเสริมแรงทางสายตา — หากไม่มี Element ที่ขัดแย้งในพลังงานวันนี้อาจกดทับอำนาจตามธรรมชาติของคุณลง",
                "หลีกเลี่ยงสีที่ขัดแย้งกับพลัง Element วันนี้ เพราะ: สีที่ดูดพลังงานสร้างความไม่สมดุลที่บั่นทอนความมั่นใจของคุณอย่างแนบเนียนและส่งผลต่อการรับรู้ความน่าเชื่อถือของคุณในสายตาคนอื่น",
            ],
            practical_tips_th=fb["tips_th"],
            sample_sentences_th=fb.get("sentences_th", []),
            alternative_responses_th=fb.get("alts_th", ["ปรับตัวตามสถานการณ์"]),
            coaching_summary_th=fb.get("summary_th", ""),
            variation_seed=variation_seed,
            variation_angle=variation["angle"],
            generation_model="db-fallback",
            generation_ms=int((time.time() - t_start) * 1000),
        )

    # Agent 3: Coaching (AI call — returns EN + TH in one response)
    coaching_prompt = build_coaching_prompt(
        profile_ctx, goal_ctx, bazi_score, variation, gen_count, excluded_angles,
        day_master=str(day_master), daily_element=str(daily_element),
        stance=stance, stance_th=stance_th, strong_day=strong_day,
        lead_colour=lead_colour, lead_colour_hex=lead_colour_hex,
        secondary_colour=secondary_colour, power_direction=power_direction,
        planetary_hour_ruler=planetary_hour_ruler,
        planetary_hour_best_for=planetary_hour_best_for,
        planetary_hour_avoid=planetary_hour_avoid,
        peak_hour_window=peak_hour_window,
        thai_day_ruler=thai_day_ruler, saturn_note=saturn_note,
    )
    try:
        coaching_raw, model_used = _call_ai(COACHING_SYSTEM, coaching_prompt)
    except RuntimeError:
        # All AI providers failed — use db-fallback
        fb = _GOAL_FALLBACK.get(goal, _GOAL_FALLBACK["work"])
        return PipelineResult(
            bazi_score=bazi_score,
            behavior_recommendation=fb["behavior"],
            timing_guidance=fb["timing"] + f" (BaZi score today: {bazi_score:.1f}/10)",
            communication_strategy=fb["comm"],
            warnings=[
                _hd_warning_en(hd_type),
                "Wear your Day Master power color today. Why: your Day Master element needs visual reinforcement to stay dominant — without it, opposing elements in today's energy can suppress your natural authority.",
                "Avoid colors that clash with today's Element energy. Why: drain colors create an energetic imbalance that subtly undermines your confidence and how others perceive your credibility.",
            ],
            practical_tips=fb["tips"],
            sample_sentences=fb["sentences"],
            alternative_responses=fb.get("alts", ["Adapt as the conversation evolves."]),
            coaching_summary=fb.get("summary", f"{mbti_type} + {hd_type or 'no HD'} — {goal.title()} session."),
            behavior_recommendation_th=fb["behavior_th"],
            timing_guidance_th=fb["timing_th"] + f" (BaZi score วันนี้: {bazi_score:.1f}/10)",
            communication_strategy_th=fb["comm_th"],
            warnings_th=[
                _hd_warning_th(hd_type),
                "สวมสี Day Master power color วันนี้ เพราะ: Element ของ Day Master ต้องการการเสริมแรงทางสายตา — หากไม่มี Element ที่ขัดแย้งในพลังงานวันนี้อาจกดทับอำนาจตามธรรมชาติของคุณลง",
                "หลีกเลี่ยงสีที่ขัดแย้งกับพลัง Element วันนี้ เพราะ: สีที่ดูดพลังงานสร้างความไม่สมดุลที่บั่นทอนความมั่นใจของคุณอย่างแนบเนียนและส่งผลต่อการรับรู้ความน่าเชื่อถือของคุณในสายตาคนอื่น",
            ],
            practical_tips_th=fb["tips_th"],
            sample_sentences_th=fb.get("sentences_th", []),
            alternative_responses_th=fb.get("alts_th", ["ปรับตัวตามสถานการณ์"]),
            coaching_summary_th=fb.get("summary_th", ""),
            variation_seed=variation_seed,
            variation_angle=variation["angle"],
            generation_model="db-fallback",
            generation_ms=int((time.time() - t_start) * 1000),
        )

    # Agent 4: Dialogue (AI call — returns EN + TH in one response)
    dialogue_prompt = build_dialogue_prompt(
        profile_ctx, goal_ctx, coaching_raw,
        stance=stance, stance_th=stance_th,
    )
    dialogue_raw, _ = _call_ai(DIALOGUE_SYSTEM, dialogue_prompt)

    # Record used angle
    record_memory(db, user_id, "used_angle", variation["angle"], goal_context=goal)

    return PipelineResult(
        bazi_score=bazi_score,
        # EN
        behavior_recommendation=coaching_raw.get("behavior_recommendation", ""),
        timing_guidance=coaching_raw.get("timing_guidance", ""),
        communication_strategy=coaching_raw.get("communication_strategy", ""),
        warnings=coaching_raw.get("warnings", []),
        practical_tips=coaching_raw.get("practical_tips", []),
        sample_sentences=dialogue_raw.get("sample_sentences", []),
        alternative_responses=dialogue_raw.get("alternative_responses", []),
        coaching_summary=coaching_raw.get("coaching_summary", ""),
        # TH — from same response, no extra call needed
        behavior_recommendation_th=coaching_raw.get("behavior_recommendation_th", ""),
        timing_guidance_th=coaching_raw.get("timing_guidance_th", ""),
        communication_strategy_th=coaching_raw.get("communication_strategy_th", ""),
        warnings_th=coaching_raw.get("warnings_th", []),
        practical_tips_th=coaching_raw.get("practical_tips_th", []),
        sample_sentences_th=dialogue_raw.get("sample_sentences_th", []),
        alternative_responses_th=dialogue_raw.get("alternative_responses_th", []),
        coaching_summary_th=coaching_raw.get("coaching_summary_th", ""),
        # Meta
        variation_seed=variation_seed,
        variation_angle=variation["angle"],
        generation_model=model_used,
        generation_ms=int((time.time() - t_start) * 1000),
    )
