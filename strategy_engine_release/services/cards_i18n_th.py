# -*- coding: utf-8 -*-
"""Thai translations for Card Deck content whose source data is English-only.

Two dicts, each keyed by the exact English source string. Seeded into the
card_translations table by cards_service.py so operators can edit Thai copy
in the DB without a deploy — same pattern as services/aehq_i18n_th.py.

Tone rules (matching the AEHQ Thai voice): ภาษาอบอุ่น เป็นกันเอง ใช้ "คุณ" สุภาพ
ไม่มีศัพท์คลินิก ไม่สั่ง ไม่ตัดสิน ประโยคสั้น อ่านง่ายบนจอมือถือ.
"""

# ── Per-card micro_intervention ("A small thing to try") — 40 Neuro cards ──
MICRO_TH: dict[str, str] = {
    "Orient to five things you see; lengthen the exhale.":
        "มองหาห้าสิ่งรอบตัวที่เห็น แล้วหายใจออกให้ยาวขึ้น",
    "Name the near side, far side, and next plank.":
        "บอกชื่อฝั่งที่คุณอยู่ ฝั่งที่จะไป และก้าวถัดไป",
    "Ask what safety would make opening possible.":
        "ลองถามตัวเองว่าอะไรจะทำให้รู้สึกปลอดภัยพอที่จะเปิดใจ",
    "Identify one old prediction and one present-day fact.":
        "หาคำทำนายเก่าหนึ่งอย่าง และข้อเท็จจริงของวันนี้อีกหนึ่งอย่าง",
    "Name what helped the repair hold.":
        "บอกชื่อสิ่งที่ช่วยให้การซ่อมแซมนั้นยังคงอยู่",
    "Speak one sentence to the empty chair; then answer gently.":
        "พูดหนึ่งประโยคกับเก้าอี้ว่าง แล้วตอบกลับตัวเองอย่างอ่อนโยน",
    "Describe without adjectives for thirty seconds.":
        "ลองบรรยายโดยไม่ใช้คำคุณศัพท์ สักสามสิบวินาที",
    "Choose only the next safe step.":
        "เลือกแค่ก้าวถัดไปที่ปลอดภัยพอ ไม่ต้องมองไกลกว่านั้น",
    "Separate facts, feelings, needs, and requests.":
        "แยกให้ออกว่าอะไรคือข้อเท็จจริง อะไรคือความรู้สึก อะไรคือความต้องการ และอะไรคือคำขอ",
    "Choose one safe context for greater authenticity.":
        "เลือกสักบริบทหนึ่งที่ปลอดภัยพอจะเป็นตัวเองมากขึ้น",
    "Reduce the task until motivation can meet it.":
        "ย่องานให้เล็กลงจนแรงจูงใจที่มีอยู่พอจะทำไหว",
    "Sort one burden into keep, share, release.":
        "แยกภาระหนึ่งอย่างว่าอะไรควรเก็บไว้ อะไรควรแบ่งปัน อะไรควรปล่อยวาง",
    "Use two columns: observed / inferred.":
        "แบ่งเป็นสองช่อง: สิ่งที่สังเกตเห็นจริง กับสิ่งที่ตีความเอาเอง",
    "Move physically to another viewpoint and notice.":
        "ลองขยับร่างกายไปมองจากมุมอื่น แล้วสังเกตว่าเห็นอะไรต่าง",
    "Thank the defence; design a small gate.":
        "ขอบคุณเกราะป้องกันนี้ แล้วลองออกแบบประตูเล็ก ๆ ให้มันเปิดได้บ้าง",
    "State today's date, place, and present evidence.":
        "บอกวันที่วันนี้ สถานที่ที่อยู่ และหลักฐานที่เห็นอยู่ตอนนี้",
    "Write for five minutes; decide later.":
        "เขียนไปเรื่อย ๆ สักห้านาที ยังไม่ต้องตัดสินใจตอนนี้",
    "Choose one value-consistent micro-action.":
        "เลือกก้าวเล็ก ๆ สักอย่างที่สอดคล้องกับคุณค่าที่คุณเชื่อ",
    "List gain, cost, fear, and value for each.":
        "ลองไล่ดูแต่ละทาง: ได้อะไร เสียอะไร กลัวอะไร และอะไรคือคุณค่าที่ยึดถือ",
    "Name one skill you did not have before.":
        "บอกชื่อทักษะหนึ่งอย่างที่ตอนนั้นคุณยังไม่มี แต่ตอนนี้มีแล้ว",
    "Slow down and add one human support.":
        "ค่อย ๆ ช้าลง แล้วลองหาคนสักคนมาช่วยประคอง",
    "Keep the stabilising function; loosen the excess weight.":
        "เก็บส่วนที่ช่วยให้มั่นคงไว้ แล้วค่อย ๆ ปลดน้ำหนักส่วนเกินออก",
    "Name one previously missed detail.":
        "บอกชื่อรายละเอียดหนึ่งอย่างที่เพิ่งสังเกตเห็น",
    "Unclench hands on the exhale.":
        "คลายกำมือลงพร้อมกับหายใจออก",
    "Open the hand and name one permission.":
        "แบมือออก แล้วให้อนุญาตตัวเองในเรื่องหนึ่งอย่าง",
    "Let each part speak one sentence without debate.":
        "ให้แต่ละส่วนในใจได้พูดหนึ่งประโยค โดยยังไม่ต้องเถียงกัน",
    "Use warmth, pressure, and slow exhale; do not force insight.":
        "ใช้ความอบอุ่น แรงกดเบา ๆ และหายใจออกช้า ๆ ยังไม่ต้องเร่งหาคำตอบ",
    "Mark known, unknown, and unknowable.":
        "แยกให้เห็นว่าอะไรที่รู้แล้ว อะไรที่ยังไม่รู้ และอะไรที่อาจไม่มีทางรู้",
    "Add backup, rehearsal, or a smaller consequence.":
        "เพิ่มแผนสำรอง ลองซ้อมดูก่อน หรือลดผลที่ตามมาให้เล็กลง",
    "Create a three-item personal safety cue list.":
        "ลองทำรายการสามอย่างที่ทำให้คุณรู้สึกปลอดภัย",
    "Trace three moments linked by one value.":
        "ลองย้อนดูสามช่วงเวลาที่เชื่อมกันด้วยคุณค่าเดียวกัน",
    "Name then and now; note one difference.":
        "บอกชื่อ 'ตอนนั้น' กับ 'ตอนนี้' แล้วสังเกตว่าต่างกันตรงไหนหนึ่งอย่าง",
    "Protect the process from premature evaluation.":
        "ปกป้องกระบวนการนี้ไว้ก่อน ยังไม่ต้องรีบตัดสินว่าดีหรือไม่ดี",
    "Define the missing resource concretely.":
        "ลองระบุให้ชัดว่าสิ่งที่ขาดไปคืออะไรกันแน่",
    "Acknowledge one long-term influence.":
        "ยอมรับแรงส่งผลระยะยาวหนึ่งอย่างที่มีต่อคุณ",
    "Add one cue of comfort or predictability.":
        "เพิ่มสิ่งเล็ก ๆ ที่ทำให้รู้สึกสบายใจหรือคาดเดาได้",
    "Seek one clarifying fact before concluding.":
        "หาข้อเท็จจริงมายืนยันสักอย่างก่อนจะสรุป",
    "Set a small trial and a review point.":
        "ลองทำแบบเล็ก ๆ ดูก่อน แล้วค่อยกลับมาทบทวน",
    "Name one condition of readiness already present.":
        "บอกชื่อสิ่งหนึ่งที่บ่งบอกว่าคุณพร้อมอยู่แล้ว",
    "Inhale naturally; exhale slowly; delay response by one breath.":
        "หายใจเข้าตามธรรมชาติ หายใจออกช้า ๆ แล้วรอหนึ่งลมหายใจก่อนตอบสนอง",
}

CAUTION_TH: dict[str, str] = {
    "Do not use imagery to recover memories or establish factual truth.":
        "ภาพนี้ไม่ได้มีไว้เพื่อรื้อฟื้นความทรงจำ หรือใช้ยืนยันว่าเหตุการณ์ใดเป็นความจริง",
}

# ── "In short" summary templates (placeholders: {name} {theme} {lines}) ──
# Warm, empowering, easy to read. Edit here (or in the DB) without touching code.
SUMMARY_TH: dict[str, str] = {
    "one":   "การ์ดที่คุณเลือกคือ “{name}”{theme} เชื่อในสิ่งที่คุณมองเห็น เพราะคำตอบอยู่ในตัวคุณเองแล้ว",
    "multi": "การ์ดที่คุณเลือกเล่าเรื่องราวของคุณ: {lines} มองภาพรวมทั้งหมด แล้วคุณจะเห็นทางของตัวเองชัดขึ้น",
}

# ── Interactive workshop content (frontend TOOL_WORKSHOPS keys) ──
# Each entry: short label, the guiding prompt, and >=3 sample hint answers.
WORKSHOP_TH: dict[str, dict] = {
    "Affect regulation (window of tolerance)": {
        "short": "การปรับสมดุลอารมณ์",
        "prompt": "ลองทำสิ่งเล็ก ๆ ข้างต้นดู แล้วสังเกตว่าร่างกายเปลี่ยนไปบ้างไหม แม้แค่นิดเดียว",
        "hints": ["การหายใจของฉันช้าลงนิดหน่อย", "ไหล่ของฉันคลายลง", "ยังตึงอยู่ แต่ไม่เร่งด่วนเท่าเดิม"],
    },
    "Perception & cognitive defusion (perception vs interpretation)": {
        "short": "การแยกแยะการรับรู้",
        "prompt": "แยกให้ออกระหว่างสิ่งที่คุณ 'เห็นจริง' กับ 'เรื่องราว' ที่คุณเติมเข้าไป",
        "hints": ["สิ่งที่เห็น: รูปทรงมืด ๆ เรื่องที่เติม: 'มันอันตราย'", "ฉันด่วนสรุปไปเองโดยไม่มีหลักฐาน", "ยังมีอีกมุมหนึ่งที่มองเรื่องนี้ได้"],
    },
    "Behavioural activation & agency": {
        "short": "ก้าวเล็ก ๆ ที่ลงมือทำได้",
        "prompt": "บอกก้าวที่เล็กที่สุดที่คุณทำได้ภายใน 10 นาทีข้างหน้า",
        "hints": ["ส่งข้อความสั้น ๆ หนึ่งข้อความ", "ลุกขึ้นยืดเส้นยืดสายสัก 2 นาที", "เขียนแค่ประโยคแรกก็พอ"],
    },
    "Values clarification": {
        "short": "คุณค่าที่ยึดถือ",
        "prompt": "คุณค่าอะไรอยากเป็นผู้นำทางในเรื่องนี้",
        "hints": ["ความจริงใจ — พูดสิ่งที่จริงด้วยความอ่อนโยน", "ความกล้า — ลงมือทำสิ่งเล็ก ๆ ที่กล้าหาญ", "ความเอาใจใส่ — ใจดีกับตัวเองก่อน"],
    },
    "Protective parts & boundaries": {
        "short": "ส่วนที่คอยปกป้อง",
        "prompt": "รูปแบบนี้เคยปกป้องคุณมาก่อน มันพยายามปกป้องอะไรอยู่",
        "hints": ["มันป้องกันไม่ให้ถูกปฏิเสธ", "มันช่วยไม่ให้เจ็บซ้ำอีก", "มันอยากควบคุมเมื่อรู้สึกไม่แน่นอน"],
    },
    "Resourcing & co-regulation": {
        "short": "แหล่งพลังและการประคองใจ",
        "prompt": "บอกชื่อสิ่งหนึ่งที่ช่วยให้คุณรู้สึกมั่นคงได้ตอนนี้",
        "hints": ["เพื่อนที่ทักหาได้", "สถานที่ที่รู้สึกปลอดภัย", "ความทรงจำตอนที่มีคนคอยประคอง"],
    },
    "Self-compassion & acceptance": {
        "short": "ความเมตตาต่อตนเอง",
        "prompt": "ถ้าเพื่อนสนิทตกอยู่ในจุดนี้พอดี คุณจะพูดอะไรกับเขา",
        "hints": ["“เรื่องนี้มันหนักจริง ๆ และคุณก็พยายามเต็มที่แล้ว”", "“ไม่ต้องรู้คำตอบทั้งหมดตอนนี้ก็ได้”", "“เข้าใจได้ที่รู้สึกแบบนี้”"],
    },
    "_generic": {
        "short": "การทบทวนใจ",
        "prompt": "มีอะไรเล็ก ๆ ที่จริงใจสักอย่างที่คุณอยากเก็บไว้จากไพ่ใบนี้",
        "hints": ["คำหนึ่งคำที่อยากยึดไว้วันนี้", "สิ่งเล็ก ๆ ที่ลองทำได้", "สิ่งที่แค่อยากสังเกต ไม่ต้องแก้ไข"],
    },
}
