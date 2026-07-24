# Card Deck — content review packet (2026-07-24)

**Everything below was written or inferred by an AI, not by a native Thai
speaker or a clinician.** This is a therapeutic-adjacent tool, so please have
a qualified human check it before real users see it. Add notes in the last
column; anything you change can be edited directly in the `card_translations`
table (no deploy needed) or in `services/cards_i18n_th.py` for the seed.

## ⚠️ Priority 1 — verify these first (safety-critical)

These live in `dashboard/src/GuidedSession.jsx`, **not** in the DB, and were
written by an AI from general knowledge. Wrong crisis details in a mental-health
tool are the highest-risk item here.

| Item | Value in the app | Please verify |
| --- | --- | --- |
| Mental Health Hotline (TH) | **1323** | Correct number? Still 24h and free? |
| Samaritans Thailand | **02-113-6789** | Correct and current? |
| Emergency (medical) | **1669** | Correct for medical emergency? |
| Crisis wording (TH + EN) | see `crisis` screen | Is the tone right? Anything to add/remove? |
| Crisis keyword list | `CRISIS_TERMS` | Naive substring match — which Thai/English
  phrases are missing? Any that false-positive? |

Also worth a clinician's eye: the **activation routing** (0-3 / 4-6 / 7-8 thresholds)
and the decision to show grounding before imagery at activation >= 7.

## 1. Micro-interventions ("A small thing to try") — 40 Neuro cards

These are shown as an action the user may take. Check both the translation
and whether the action itself is safe/appropriate.

| English (source) | Thai (AI translation) | Reviewer notes |
| --- | --- | --- |
| Orient to five things you see; lengthen the exhale. | มองหาห้าสิ่งรอบตัวที่เห็น แล้วหายใจออกให้ยาวขึ้น |  |
| Name the near side, far side, and next plank. | บอกชื่อฝั่งที่คุณอยู่ ฝั่งที่จะไป และก้าวถัดไป |  |
| Ask what safety would make opening possible. | ลองถามตัวเองว่าอะไรจะทำให้รู้สึกปลอดภัยพอที่จะเปิดใจ |  |
| Identify one old prediction and one present-day fact. | หาคำทำนายเก่าหนึ่งอย่าง และข้อเท็จจริงของวันนี้อีกหนึ่งอย่าง |  |
| Name what helped the repair hold. | บอกชื่อสิ่งที่ช่วยให้การซ่อมแซมนั้นยังคงอยู่ |  |
| Speak one sentence to the empty chair; then answer gently. | พูดหนึ่งประโยคกับเก้าอี้ว่าง แล้วตอบกลับตัวเองอย่างอ่อนโยน |  |
| Describe without adjectives for thirty seconds. | ลองบรรยายโดยไม่ใช้คำคุณศัพท์ สักสามสิบวินาที |  |
| Choose only the next safe step. | เลือกแค่ก้าวถัดไปที่ปลอดภัยพอ ไม่ต้องมองไกลกว่านั้น |  |
| Separate facts, feelings, needs, and requests. | แยกให้ออกว่าอะไรคือข้อเท็จจริง อะไรคือความรู้สึก อะไรคือความต้องการ และอะไรคือคำขอ |  |
| Choose one safe context for greater authenticity. | เลือกสักบริบทหนึ่งที่ปลอดภัยพอจะเป็นตัวเองมากขึ้น |  |
| Reduce the task until motivation can meet it. | ย่องานให้เล็กลงจนแรงจูงใจที่มีอยู่พอจะทำไหว |  |
| Sort one burden into keep, share, release. | แยกภาระหนึ่งอย่างว่าอะไรควรเก็บไว้ อะไรควรแบ่งปัน อะไรควรปล่อยวาง |  |
| Use two columns: observed / inferred. | แบ่งเป็นสองช่อง: สิ่งที่สังเกตเห็นจริง กับสิ่งที่ตีความเอาเอง |  |
| Move physically to another viewpoint and notice. | ลองขยับร่างกายไปมองจากมุมอื่น แล้วสังเกตว่าเห็นอะไรต่าง |  |
| Thank the defence; design a small gate. | ขอบคุณเกราะป้องกันนี้ แล้วลองออกแบบประตูเล็ก ๆ ให้มันเปิดได้บ้าง |  |
| State today's date, place, and present evidence. | บอกวันที่วันนี้ สถานที่ที่อยู่ และหลักฐานที่เห็นอยู่ตอนนี้ |  |
| Write for five minutes; decide later. | เขียนไปเรื่อย ๆ สักห้านาที ยังไม่ต้องตัดสินใจตอนนี้ |  |
| Choose one value-consistent micro-action. | เลือกก้าวเล็ก ๆ สักอย่างที่สอดคล้องกับคุณค่าที่คุณเชื่อ |  |
| List gain, cost, fear, and value for each. | ลองไล่ดูแต่ละทาง: ได้อะไร เสียอะไร กลัวอะไร และอะไรคือคุณค่าที่ยึดถือ |  |
| Name one skill you did not have before. | บอกชื่อทักษะหนึ่งอย่างที่ตอนนั้นคุณยังไม่มี แต่ตอนนี้มีแล้ว |  |
| Slow down and add one human support. | ค่อย ๆ ช้าลง แล้วลองหาคนสักคนมาช่วยประคอง |  |
| Keep the stabilising function; loosen the excess weight. | เก็บส่วนที่ช่วยให้มั่นคงไว้ แล้วค่อย ๆ ปลดน้ำหนักส่วนเกินออก |  |
| Name one previously missed detail. | บอกชื่อรายละเอียดหนึ่งอย่างที่เพิ่งสังเกตเห็น |  |
| Unclench hands on the exhale. | คลายกำมือลงพร้อมกับหายใจออก |  |
| Open the hand and name one permission. | แบมือออก แล้วให้อนุญาตตัวเองในเรื่องหนึ่งอย่าง |  |
| Let each part speak one sentence without debate. | ให้แต่ละส่วนในใจได้พูดหนึ่งประโยค โดยยังไม่ต้องเถียงกัน |  |
| Use warmth, pressure, and slow exhale; do not force insight. | ใช้ความอบอุ่น แรงกดเบา ๆ และหายใจออกช้า ๆ ยังไม่ต้องเร่งหาคำตอบ |  |
| Mark known, unknown, and unknowable. | แยกให้เห็นว่าอะไรที่รู้แล้ว อะไรที่ยังไม่รู้ และอะไรที่อาจไม่มีทางรู้ |  |
| Add backup, rehearsal, or a smaller consequence. | เพิ่มแผนสำรอง ลองซ้อมดูก่อน หรือลดผลที่ตามมาให้เล็กลง |  |
| Create a three-item personal safety cue list. | ลองทำรายการสามอย่างที่ทำให้คุณรู้สึกปลอดภัย |  |
| Trace three moments linked by one value. | ลองย้อนดูสามช่วงเวลาที่เชื่อมกันด้วยคุณค่าเดียวกัน |  |
| Name then and now; note one difference. | บอกชื่อ 'ตอนนั้น' กับ 'ตอนนี้' แล้วสังเกตว่าต่างกันตรงไหนหนึ่งอย่าง |  |
| Protect the process from premature evaluation. | ปกป้องกระบวนการนี้ไว้ก่อน ยังไม่ต้องรีบตัดสินว่าดีหรือไม่ดี |  |
| Define the missing resource concretely. | ลองระบุให้ชัดว่าสิ่งที่ขาดไปคืออะไรกันแน่ |  |
| Acknowledge one long-term influence. | ยอมรับแรงส่งผลระยะยาวหนึ่งอย่างที่มีต่อคุณ |  |
| Add one cue of comfort or predictability. | เพิ่มสิ่งเล็ก ๆ ที่ทำให้รู้สึกสบายใจหรือคาดเดาได้ |  |
| Seek one clarifying fact before concluding. | หาข้อเท็จจริงมายืนยันสักอย่างก่อนจะสรุป |  |
| Set a small trial and a review point. | ลองทำแบบเล็ก ๆ ดูก่อน แล้วค่อยกลับมาทบทวน |  |
| Name one condition of readiness already present. | บอกชื่อสิ่งหนึ่งที่บ่งบอกว่าคุณพร้อมอยู่แล้ว |  |
| Inhale naturally; exhale slowly; delay response by one breath. | หายใจเข้าตามธรรมชาติ หายใจออกช้า ๆ แล้วรอหนึ่งลมหายใจก่อนตอบสนอง |  |

## 2. Clinical caution

| English (source) | Thai (AI translation) | Reviewer notes |
| --- | --- | --- |
| Do not use imagery to recover memories or establish factual truth. | ภาพนี้ไม่ได้มีไว้เพื่อรื้อฟื้นความทรงจำ หรือใช้ยืนยันว่าเหตุการณ์ใดเป็นความจริง |  |

## 3. Workshop copy (per framework)

The interactive exercise shown with each card. `prompt` is what the user is
asked; `hints` are example answers that visibly steer them — check for leading
or presumptuous phrasing.


### Affect regulation (window of tolerance)

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | การปรับสมดุลอารมณ์ |  |
| prompt | ลองทำสิ่งเล็ก ๆ ข้างต้นดู แล้วสังเกตว่าร่างกายเปลี่ยนไปบ้างไหม แม้แค่นิดเดียว |  |
| hint 1 | การหายใจของฉันช้าลงนิดหน่อย |  |
| hint 2 | ไหล่ของฉันคลายลง |  |
| hint 3 | ยังตึงอยู่ แต่ไม่เร่งด่วนเท่าเดิม |  |

### Perception & cognitive defusion (perception vs interpretation)

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | การแยกแยะการรับรู้ |  |
| prompt | แยกให้ออกระหว่างสิ่งที่คุณ 'เห็นจริง' กับ 'เรื่องราว' ที่คุณเติมเข้าไป |  |
| hint 1 | สิ่งที่เห็น: รูปทรงมืด ๆ เรื่องที่เติม: 'มันอันตราย' |  |
| hint 2 | ฉันด่วนสรุปไปเองโดยไม่มีหลักฐาน |  |
| hint 3 | ยังมีอีกมุมหนึ่งที่มองเรื่องนี้ได้ |  |

### Behavioural activation & agency

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | ก้าวเล็ก ๆ ที่ลงมือทำได้ |  |
| prompt | บอกก้าวที่เล็กที่สุดที่คุณทำได้ภายใน 10 นาทีข้างหน้า |  |
| hint 1 | ส่งข้อความสั้น ๆ หนึ่งข้อความ |  |
| hint 2 | ลุกขึ้นยืดเส้นยืดสายสัก 2 นาที |  |
| hint 3 | เขียนแค่ประโยคแรกก็พอ |  |

### Values clarification

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | คุณค่าที่ยึดถือ |  |
| prompt | คุณค่าอะไรอยากเป็นผู้นำทางในเรื่องนี้ |  |
| hint 1 | ความจริงใจ — พูดสิ่งที่จริงด้วยความอ่อนโยน |  |
| hint 2 | ความกล้า — ลงมือทำสิ่งเล็ก ๆ ที่กล้าหาญ |  |
| hint 3 | ความเอาใจใส่ — ใจดีกับตัวเองก่อน |  |

### Protective parts & boundaries

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | ส่วนที่คอยปกป้อง |  |
| prompt | รูปแบบนี้เคยปกป้องคุณมาก่อน มันพยายามปกป้องอะไรอยู่ |  |
| hint 1 | มันป้องกันไม่ให้ถูกปฏิเสธ |  |
| hint 2 | มันช่วยไม่ให้เจ็บซ้ำอีก |  |
| hint 3 | มันอยากควบคุมเมื่อรู้สึกไม่แน่นอน |  |

### Resourcing & co-regulation

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | แหล่งพลังและการประคองใจ |  |
| prompt | บอกชื่อสิ่งหนึ่งที่ช่วยให้คุณรู้สึกมั่นคงได้ตอนนี้ |  |
| hint 1 | เพื่อนที่ทักหาได้ |  |
| hint 2 | สถานที่ที่รู้สึกปลอดภัย |  |
| hint 3 | ความทรงจำตอนที่มีคนคอยประคอง |  |

### Self-compassion & acceptance

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | ความเมตตาต่อตนเอง |  |
| prompt | ถ้าเพื่อนสนิทตกอยู่ในจุดนี้พอดี คุณจะพูดอะไรกับเขา |  |
| hint 1 | “เรื่องนี้มันหนักจริง ๆ และคุณก็พยายามเต็มที่แล้ว” |  |
| hint 2 | “ไม่ต้องรู้คำตอบทั้งหมดตอนนี้ก็ได้” |  |
| hint 3 | “เข้าใจได้ที่รู้สึกแบบนี้” |  |

### _generic

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| short | การทบทวนใจ |  |
| prompt | มีอะไรเล็ก ๆ ที่จริงใจสักอย่างที่คุณอยากเก็บไว้จากไพ่ใบนี้ |  |
| hint 1 | คำหนึ่งคำที่อยากยึดไว้วันนี้ |  |
| hint 2 | สิ่งเล็ก ๆ ที่ลองทำได้ |  |
| hint 3 | สิ่งที่แค่อยากสังเกต ไม่ต้องแก้ไข |  |

## 4. "In short" summary templates

`{name}` / `{theme}` / `{lines}` are filled in at runtime.

| Key | Thai template | Reviewer notes |
| --- | --- | --- |
| one | การ์ดที่คุณเลือกคือ “{name}”{theme} เชื่อในสิ่งที่คุณมองเห็น เพราะคำตอบอยู่ในตัวคุณเองแล้ว |  |
| multi | การ์ดที่คุณเลือกเล่าเรื่องราวของคุณ: {lines} มองภาพรวมทั้งหมด แล้วคุณจะเห็นทางของตัวเองชัดขึ้น |  |

## 5. Reading guide ("Intuition First, Knowledge Second")

| Field | Thai | Reviewer notes |
| --- | --- | --- |
| label | วิธีอ่านไพ่: ใช้ใจรู้สึกก่อน แล้วค่อยดูความหมาย |  |
| section 1 title | ความรู้สึกแรกที่เห็น |  |
| section 1 body | ก่อนเปิดดูความหมาย ลองมองภาพบนการ์ด สีหน้าตัวละคร บรรยากาศ และสีสัน — สิ่งเหล่านี้ทำให้คุณรู้สึกอย่างไร |  |
| section 2 title | สัญลักษณ์ |  |
| section 2 body | สังเกตรายละเอียดเล็ก ๆ เช่น สัตว์ สิ่งของ หรือตัวเลข แล้วเชื่อมโยงกับสถานการณ์ปัจจุบันของคุณ |  |
| section 3 title | ตั้งคำถามสะท้อนตัวตน |  |
| section 3 body | ลองถามลึกลงไปว่าภาพนี้กำลังสะท้อนอะไรในตัวคุณ ไม่ใช่การทำนายอนาคต |  |
| section 4 title | จดบันทึก |  |
| section 4 body | เขียนความคิดและความรู้สึกของคุณไว้ เมื่อเวลาผ่านไป บันทึกจะช่วยให้เห็นรูปแบบของตัวเอง |  |

## 6. Neuro card -> framework mapping (needs clinical validation)

`proposed_framework` was **inferred by a keyword rule**, not taken from the
literature. 29 proposed, 11 unmapped. Please confirm or
correct each against a named model (ACT, IFS, polyvagal-informed regulation,
behavioural activation, self-compassion, ...), then update `FRAMEWORK_RULES` in
`scripts/build_neuro_mapping.py`.

| Card | Archetype | Proposed framework | Correct? |
| --- | --- | --- | --- |
| The Storm | Emotional activation | Affect regulation (window of tolerance) |  |
| The Bridge | Transition / connection | Behavioural activation & agency |  |
| The Locked Door | Protection / blocked access | Behavioural activation & agency |  |
| The Cage with an Open Door | Learned limitation | Protective parts & boundaries |  |
| The Mended Bowl | Repair / integration | Self-compassion & acceptance |  |
| The Mirror | Self-perception | Perception & cognitive defusion (perception vs interpretation) |  |
| The Fog | Uncertainty | Perception & cognitive defusion (perception vs interpretation) |  |
| The Mask | Role / protection | Protective parts & boundaries |  |
| The Small Flame | Motivation | Behavioural activation & agency |  |
| The Heavy Backpack | Burden / accumulated load | Self-compassion & acceptance |  |
| The Tangle of Threads | Multiple narratives | Perception & cognitive defusion (perception vs interpretation) |  |
| The Protective Wall | Defence / boundary | Protective parts & boundaries |  |
| The Echo | Repetition / memory | Perception & cognitive defusion (perception vs interpretation) |  |
| The Compass | Values / orientation | Values clarification |  |
| The Crossroads | Decision / ambivalence | Behavioural activation & agency |  |
| The Cracked Ice | Fragility / caution | Self-compassion & acceptance |  |
| The Lantern | Awareness | Perception & cognitive defusion (perception vs interpretation) |  |
| The Closed Fist | Control / readiness | Behavioural activation & agency |  |
| The Open Palm | Receiving / release | Resourcing & co-regulation |  |
| The Frozen River | Shutdown / conservation | Affect regulation (window of tolerance) |  |
| The Safe Harbour | Co-regulation / refuge | Affect regulation (window of tolerance) |  |
| The Red Thread | Continuity / connection | Resourcing & co-regulation |  |
| The Seed in Darkness | Incubation | Self-compassion & acceptance |  |
| The Missing Step | Gap / support need | Resourcing & co-regulation |  |
| The Nest | Belonging / preparation | Resourcing & co-regulation |  |
| The Shadow on the Wall | Projection / uncertainty | Perception & cognitive defusion (perception vs interpretation) |  |
| The Paper Boat | Vulnerability / play | Self-compassion & acceptance |  |
| The Turning Key | Readiness / access | Behavioural activation & agency |  |
| The Breathing Space | Pause / regulation | Affect regulation (window of tolerance) |  |

### Unmapped — no framework rule matched (11)

| Card | Archetype | Which framework should this be? |
| --- | --- | --- |
| The Empty Chair | Absence / unfinished dialogue |  |
| The Knot | Complexity / entanglement |  |
| The Window | Perspective / possibility |  |
| The Unsent Letter | Expression / inhibition |  |
| The Spiral Staircase | Revisiting / growth |  |
| The Anchor | Stability / stuckness |  |
| The Two Wolves | Competing impulses |  |
| The Unfinished Puzzle | Incomplete meaning |  |
| The Tightrope | Balance / performance pressure |  |
| The Broken Clock | Time / stuck moment |  |
| The River Stone | Shaping / persistence |  |

## 7. Out of scope for this packet

- The 40 Neuro cards' `name_th` / `meaning_th` / `reflect_prompt_th` came
  with your catalogue (healing_card_system_mapping.xlsx), so they are **your** copy,
  not AI translation — reviewed separately if you wish.
- Tarot (78) and Nature
  (30) card text likewise.
