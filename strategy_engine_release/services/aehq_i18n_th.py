# -*- coding: utf-8 -*-
"""Thai translations for the AEHQ v2.2 content.

One dict, keyed by the exact English source string. Seeded into the
aehq_translations table by seed_aehq.py and loaded back into the cache, so
operators can edit Thai copy in the DB without a deploy.

Tone rules (matching the EN voice): ภาษาอบอุ่น เป็นกันเอง ใช้ "คุณ" สุภาพ
ไม่มีศัพท์คลินิก ไม่สั่ง ไม่ตัดสิน ประโยคสั้น อ่านง่ายบนจอมือถือ.
"""

TH_STRINGS: dict[str, str] = {

    # ═══ Consent gate (PDPA) ═══════════════════════════════════
    "Before we begin": "ก่อนเริ่มกัน",
    "A quick, honest heads-up": "ขอบอกตามตรงสั้น ๆ ก่อน",
    "This is a **self-reflection tool — not therapy, and not a diagnosis.**\n\n"
    "• **Your privacy:** your answers are stored privately in your account so you can look back on them.\n"
    "• **Safety:** if you mention thoughts of self-harm, we'll pause and show support options — nothing is reported anywhere.\n"
    "• **Not a substitute:** in a crisis, please contact a professional or a helpline (Thailand 1323).\n\n"
    "Tapping **“I understand — begin”** means you agree to the above.":
        "นี่คือ**เครื่องมือสะท้อนใจ — ไม่ใช่การบำบัด และไม่ใช่การวินิจฉัย**\n\n"
        "• **ความเป็นส่วนตัว:** คำตอบของคุณถูกเก็บไว้เป็นส่วนตัวในบัญชีของคุณ เพื่อให้กลับมาดูย้อนหลังได้\n"
        "• **ความปลอดภัย:** ถ้าคุณพูดถึงความคิดทำร้ายตัวเอง เราจะหยุดพักและแสดงช่องทางช่วยเหลือ — โดยไม่มีการรายงานไปที่ไหนทั้งนั้น\n"
        "• **ไม่ใช่สิ่งทดแทน:** ในภาวะวิกฤต โปรดติดต่อผู้เชี่ยวชาญหรือสายด่วน (ประเทศไทย 1323)\n\n"
        "การแตะ **“เข้าใจแล้ว — เริ่มเลย”** ถือว่าคุณยอมรับข้อความข้างต้น",
    "You may use my anonymized answers to improve this tool (optional).":
        "อนุญาตให้ใช้คำตอบของฉันแบบไม่ระบุตัวตนเพื่อพัฒนาเครื่องมือนี้ (ไม่บังคับ)",
    "I understand — begin": "เข้าใจแล้ว — เริ่มเลย",

    # ═══ Fear-of-compassion + soothing feedback (S6-S7) ════════
    "One gentle gauge first.": "ขอวัดใจเบา ๆ ก่อนหนึ่งข้อ",
    "When you try to turn kindness toward yourself — what usually happens?":
        "เวลาคุณลองหันความเมตตาเข้าหาตัวเอง — ปกติมันเป็นยังไง?",
    "However it lands is useful. There's no wrong answer.":
        "รู้สึกยังไงก็มีประโยชน์ ไม่มีคำตอบที่ผิด",
    "It feels okay — natural enough": "รู้สึกโอเค — ค่อนข้างเป็นธรรมชาติ",
    "A bit awkward or uncomfortable": "รู้สึกเขิน ๆ หรืออึดอัดนิดหน่อย",
    "Like I don't deserve it, or it feels fake": "เหมือนฉันไม่คู่ควร หรือรู้สึกปลอม",
    "One small reminder.": "ขอฝากเตือนเล็ก ๆ",
    "Take a breath with it. You don't have to believe it fully — just let it land.":
        "หายใจไปกับมันสักครั้ง ไม่ต้องเชื่อทั้งหมดก็ได้ — แค่ปล่อยให้มันได้แวะพัก",
    "Okay": "โอเค", "Skip this one": "ขอข้ามข้อนี้",
    "This is bringing up a lot — pause": "มันกระตุ้นอะไรขึ้นมาเยอะ — ขอพัก",
    "Quick check.": "เช็คเร็ว ๆ",
    "Did that soothe things even a little?": "เมื่อกี้ช่วยให้ใจนิ่งขึ้นบ้างไหม แม้แค่นิดเดียว?",
    "0 = not at all · 10 = a real settling. Whatever's true is fine.":
        "0 = ไม่เลย · 10 = สงบลงจริง ๆ ตอบตามจริงได้เลย",
    "Not at all": "ไม่เลย", "A little": "นิดหน่อย", "A real settling": "สงบลงจริง ๆ",

    # ═══ Bottom-line belief rating ═════════════════════════════
    "One quick reading.": "ขออ่านค่าเร็ว ๆ หนึ่งครั้ง",
    "Don't believe it": "ไม่เชื่อเลย",
    "Half and half": "ครึ่ง ๆ",
    "Completely true": "จริงสุด ๆ",

    # ═══ Goal anchor ═══════════════════════════════════════════
    "Before we dig in — in one sentence, what made you open this today?":
        "ก่อนจะเริ่มลงลึก — ในหนึ่งประโยค อะไรทำให้คุณเปิดแอปนี้วันนี้?",
    "Your own words, any language. You can skip this if nothing comes.":
        "ในคำของคุณเอง ภาษาอะไรก็ได้ ถ้ายังนึกไม่ออกจะข้ามก็ได้",

    # ═══ Shared-core screens ═══════════════════════════════════
    "One thing first.": "ขอถามเรื่องสำคัญก่อนหนึ่งข้อ",
    "Right now, are you having thoughts of hurting yourself, or feeling that life isn't worth living?":
        "ตอนนี้คุณมีความคิดอยากทำร้ายตัวเอง หรือรู้สึกว่าชีวิตไม่น่าอยู่ต่อไหม?",
    "This question is always asked — not because it's expected, just to make sure you're safe.":
        "คำถามนี้ถามทุกครั้งกับทุกคน — ไม่ใช่เพราะคิดว่าคุณเป็น แค่อยากแน่ใจว่าคุณปลอดภัย",
    "No, I'm okay": "ไม่มี ฉันโอเค",
    "Yes, I am": "มี",
    "Not sure": "ไม่แน่ใจ",

    "How intense is the feeling right now — on a scale of 0 to 10?":
        "ตอนนี้ความรู้สึกหนักแค่ไหน — จาก 0 ถึง 10?",
    "0 = completely calm · 10 = the most distressed you can imagine. Your gut read is the right answer.":
        "0 = สงบสนิท · 10 = หนักที่สุดเท่าที่นึกออก ตอบตามความรู้สึกแรกได้เลย",
    "Completely calm": "สงบสนิท", "Moderate": "ปานกลาง", "Overwhelming": "ท่วมท้น",
    "Calm": "สงบ",

    "Let's slow things down a little first.": "ค่อย ๆ ช้าลงกันสักนิดก่อน",
    "4-7-8 breathing": "หายใจแบบ 4-7-8",
    "Check back in.": "กลับมาเช็คกันอีกครั้ง",
    "Where is the intensity now?": "ตอนนี้ความรู้สึกอยู่ที่เท่าไหร่?",
    "0 = completely calm · 10 = overwhelming.": "0 = สงบสนิท · 10 = ท่วมท้น",
    "Done": "เสร็จแล้ว",
    "Take as long as you need.": "ใช้เวลาได้เท่าที่ต้องการเลย",
    "One more round — you're doing well.": "อีกหนึ่งรอบ — คุณทำได้ดีมากแล้ว",

    "Which of these is closest to what you're carrying right now?":
        "เรื่องไหนใกล้เคียงกับสิ่งที่คุณแบกอยู่ตอนนี้ที่สุด?",
    "Pick the one that fits best — even if it's only partly right.":
        "เลือกอันที่ตรงที่สุด — ตรงแค่บางส่วนก็ได้",

    "Where do you feel it most in your body?": "คุณรู้สึกถึงมันตรงไหนของร่างกายมากที่สุด?",
    "Pick as many as fit. Your body often knows before words do.":
        "เลือกได้หลายจุด ร่างกายมักรู้ก่อนคำพูดเสมอ",
    "Chest": "หน้าอก", "Throat": "ลำคอ", "Stomach": "ท้อง",
    "Shoulders / jaw": "บ่า / กราม", "Head": "หัว",
    "Everywhere": "ทั่วทั้งตัว", "Nowhere — numb": "ไม่รู้สึกเลย — ชาไปหมด",

    "What quality does it have?": "ความรู้สึกนั้นเป็นแบบไหน?",
    "Tight / constricted": "แน่น / บีบรัด", "Heavy": "หนักอึ้ง",
    "Hot / burning": "ร้อนผ่าว", "Buzzing / restless": "ยุกยิก / อยู่ไม่สุข",
    "Hollow / empty": "กลวง / ว่างเปล่า", "Frozen / numb": "แข็งค้าง / ชา",

    "Which of these words fit? Pick up to three.": "คำไหนตรงกับความรู้สึกบ้าง? เลือกได้สามคำ",
    "You don't have to pick any if none fit — just leave them all unselected.":
        "ถ้าไม่มีคำไหนตรงเลย ไม่ต้องเลือกก็ได้",

    "Which of these feels most like what's missing right now?":
        "ข้อไหนใกล้เคียงกับสิ่งที่ขาดหายไปตอนนี้ที่สุด?",
    "Pick the one that resonates, even if imperfectly.":
        "เลือกอันที่ใช่ที่สุด แม้จะไม่เป๊ะก็ตาม",
    "None of these quite fit": "ไม่มีข้อไหนตรงเลย",

    "One small reminder.": "ขอฝากไว้สักนิด",
    "Take a breath with it. You don't have to believe it fully — just let it land.":
        "หายใจไปกับประโยคนี้สักครั้ง ไม่ต้องเชื่อทั้งหมดก็ได้ แค่ให้มันได้แวะพัก",
    "Okay": "โอเค", "Skip this one": "ขอข้ามข้อนี้",

    "One small if-then.": "แผนเล็ก ๆ หนึ่งข้อ: ถ้า…ฉันจะ…",
    "What's the smallest concrete thing you could do in the next 24 hours?":
        "อะไรคือสิ่งเล็กที่สุดที่ทำได้จริงใน 24 ชั่วโมงข้างหน้า?",
    "Edit the suggestion below or write your own — as small and specific as possible.":
        "แก้ข้อความด้านล่างหรือเขียนเองก็ได้ — ยิ่งเล็กและชัดเท่าไหร่ยิ่งดี",

    "Almost there.": "ใกล้เสร็จแล้ว",
    "Where is the intensity now — after all of this?":
        "ผ่านมาทั้งหมดนี้แล้ว ตอนนี้ความรู้สึกอยู่ที่เท่าไหร่?",

    # ═══ Mood check (2Q-derived) ═══════════════════════════════
    "Checking the weather, not judging it.": "แค่เช็คสภาพอากาศในใจ ไม่ได้ตัดสินอะไร",
    "One gentle check before we wrap the questions — over the last two weeks, counting today, have there been days your mood sat low: heavy, sad, or drained of hope?":
        "ขอถามเบา ๆ อีกข้อก่อนจบ — ช่วงสองสัปดาห์ที่ผ่านมารวมวันนี้ มีวันที่ใจหม่น หนัก เศร้า หรือท้อบ้างไหม?",
    "Not about today only — the general weather of the last two weeks.":
        "ไม่ใช่แค่วันนี้ — มองภาพรวมสองสัปดาห์ที่ผ่านมา",
    "Not really": "ไม่ค่อยนะ",
    "Some days, yes": "มีบางวัน",
    "Most days, honestly": "เกือบทุกวันเลย ตามตรง",
    "And in those same two weeks — the things you usually enjoy: have they gone quiet? Less pull, less fun, less taste?":
        "แล้วช่วงสองสัปดาห์เดียวกันนี้ — สิ่งที่เคยชอบ มันเงียบลงไหม? สนุกน้อยลง ดึงดูดน้อยลง จืดลง?",
    "Food, music, people, hobbies — anything that normally gives you something back.":
        "อาหาร เพลง ผู้คน งานอดิเรก — อะไรก็ตามที่ปกติเติมใจเราได้",
    "Not really — they still land": "ไม่นะ — ยังรู้สึกดีอยู่",
    "Somewhat — dimmer than usual": "ก็บ้าง — จางกว่าปกติ",
    "Yes — almost nothing lands lately": "ใช่ — ช่วงนี้แทบไม่รู้สึกอะไรเลย",

    # ═══ Situations: labels ════════════════════════════════════
    "Work or study pressure": "ความกดดันจากงานหรือการเรียน",
    "Feeling invisible or dismissed": "รู้สึกไร้ตัวตน ถูกมองข้าม",
    "Conflict with someone in authority": "ขัดแย้งกับคนที่มีอำนาจเหนือกว่า",
    "Self-criticism or shame": "เสียงตำหนิตัวเอง หรือความละอายใจ",
    "Worry about the future": "กังวลเรื่องอนาคต",
    "Grief or a painful loss": "ความโศกเศร้า หรือการสูญเสีย",
    "Anger that might be hiding something": "ความโกรธที่อาจซ่อนอะไรบางอย่าง",
    "Feeling numb or emotionally flat": "รู้สึกชา ด้านไปหมด",
    "Anxiety in a relationship": "ความกังวลในความสัมพันธ์",
    "Feeling trapped or unable to say no": "รู้สึกติดกับ ปฏิเสธใครไม่ได้",
    "Trading or investment stress": "ความเครียดจากการเทรดหรือการลงทุน",
    "Something else": "เรื่องอื่น",

    # ═══ Work items ════════════════════════════════════════════
    "When you finish work for the day — does your mind clock out with you?":
        "พอเลิกงานแต่ละวัน — ใจของคุณได้เลิกงานไปด้วยไหม?",
    "Evenings and weekends count. Just your honest average.":
        "นับตอนเย็นและวันหยุดด้วย ตอบตามความจริงโดยเฉลี่ย",
    "Mostly yes — work stays at work": "ส่วนใหญ่เลิก — งานอยู่ที่งาน",
    "It follows me home some evenings": "มันตามกลับบ้านมาบางคืน",
    "It never really switches off": "มันไม่เคยปิดเครื่องเลย",
    "What's actually on the pile right now? Telegraph style — just the things, no full sentences needed.":
        "ตอนนี้มีอะไรกองอยู่บ้าง? เขียนสั้น ๆ เป็นคำ ๆ ได้เลย ไม่ต้องเป็นประโยค",
    "Listing it usually helps. Rough words are fine.":
        "การได้ลิสต์ออกมามักช่วยได้ คำห้วน ๆ ก็ใช้ได้",
    "Under the pressure there's sometimes a quieter sentence. If yours is there, finish it: \"If I don't get this done, it means I am ___\"":
        "ใต้ความกดดันบางทีมีประโยคเงียบ ๆ ซ่อนอยู่ ถ้าของคุณมี ลองเติมให้จบ: \"ถ้าฉันทำไม่เสร็จ แปลว่าฉันเป็นคน ___\"",
    "Only if something rings true — there's no right answer here.":
        "เฉพาะถ้ามีอะไรตรงใจ — ข้อนี้ไม่มีคำตอบที่ถูก",
    "By the time you finish a normal workday — how much is left in your tank?":
        "พอจบวันทำงานปกติ — พลังในถังเหลือเท่าไหร่?",
    "0 means completely empty, 100 means plenty left for your own life.":
        "0 คือหมดเกลี้ยง 100 คือเหลือเยอะพอสำหรับชีวิตตัวเอง",
    "Completely empty": "หมดเกลี้ยง", "About half": "ราวครึ่งถัง", "Plenty left": "เหลือเยอะ",
    "If you were watching a friend in exactly this situation — what's the first thing a decent manager would take off their plate?":
        "ถ้าคุณมองเพื่อนที่อยู่ในสถานการณ์เดียวกันนี้เป๊ะ — สิ่งแรกที่หัวหน้าที่ดีควรยกออกจากมือเขาคืออะไร?",
    "Stepping back sometimes shows what's actually movable.":
        "การถอยออกมามองบางทีก็เห็นว่าอะไรขยับได้จริง",
    "Is this a season with an end date, or a structure with no exit? What's the evidence for each?":
        "นี่คือช่วงเวลาที่มีวันสิ้นสุด หรือโครงสร้างที่ไม่มีทางออก? มีอะไรสนับสนุนแต่ละแบบบ้าง?",
    "Take your time — no need to be certain.": "ค่อย ๆ คิดได้ ไม่ต้องมั่นใจร้อยเปอร์เซ็นต์",
    "Put what you give on one side of the scale — effort, hours, care. On the other side, what comes back: pay, thanks, recognition. How do the scales sit?":
        "วางสิ่งที่คุณให้ไว้ข้างหนึ่งของตาชั่ง — แรง เวลา ความใส่ใจ อีกข้างคือสิ่งที่ได้กลับมา: ค่าตอบแทน คำขอบคุณ การมองเห็น ตาชั่งเอียงไปทางไหน?",
    "Your gut read is the right answer.": "ความรู้สึกแรกคือคำตอบที่ใช่",
    "Roughly balanced": "ราว ๆ สมดุล",
    "More goes out than comes back": "ให้ออกไปมากกว่าที่ได้กลับมา",
    "It's one-sided — and it's been that way a while": "มันข้างเดียวมาตลอด — และเป็นแบบนี้มาสักพักแล้ว",

    # ═══ Dismissed items ═══════════════════════════════════════
    "What happened — camera-view only. Who said or didn't say what?":
        "เกิดอะไรขึ้น — เล่าแบบภาพจากกล้อง ใครพูดหรือไม่พูดอะไร?",
    "Just the facts of the moment, no interpretation needed yet.":
        "เอาแค่ข้อเท็จจริงของตอนนั้น ยังไม่ต้องตีความ",
    "Which landed harder: what they did, or what it seemed to say about your place with them?":
        "อะไรกระแทกใจกว่ากัน: สิ่งที่เขาทำ หรือสิ่งที่มันเหมือนบอกว่าคุณอยู่ตรงไหนสำหรับเขา?",
    "Did it sting more in the moment, or in what it hinted about where you stand?":
        "มันเจ็บตรงเหตุการณ์ หรือเจ็บตรงความหมายที่ซ่อนอยู่?",
    "What they did in the moment": "สิ่งที่เขาทำตอนนั้น",
    "What it seemed to say about where I stand": "สิ่งที่มันบอกว่าฉันอยู่ตรงไหนสำหรับเขา",
    "Both felt equally hard": "หนักพอ ๆ กันทั้งคู่",
    "A kind observer watches that moment. What do they see you needing that nobody noticed?":
        "ถ้ามีคนใจดีเฝ้ามองเหตุการณ์นั้นอยู่ เขาจะเห็นว่าคุณต้องการอะไรที่ไม่มีใครสังเกต?",
    "What would they say about what you were carrying?":
        "เขาจะพูดถึงสิ่งที่คุณแบกอยู่ว่ายังไง?",
    "When you're NOT being ignored — who notices you, and what do they notice?":
        "เวลาที่คุณ *ไม่ได้* ถูกมองข้าม — ใครที่มองเห็นคุณ และเขาเห็นอะไรในตัวคุณ?",
    "Take your time. Even one person counts.": "ค่อย ๆ นึกได้ แค่คนเดียวก็นับ",

    # ═══ Authority items ═══════════════════════════════════════
    "What exactly did they say or decide — and at which word did your body react?":
        "เขาพูดหรือตัดสินใจอะไรกันแน่ — และร่างกายคุณสะดุ้งตรงคำไหน?",
    "Rough memory is fine. What stood out?": "จำคร่าว ๆ ก็พอ อะไรที่เด่นขึ้นมา?",
    "Which is louder right now: the unfairness of it, or the danger of pushing back?":
        "ตอนนี้เสียงไหนดังกว่า: ความไม่แฟร์ของเรื่องนี้ หรือความเสี่ยงถ้าจะสู้กลับ?",
    "Both are real. Which is taking up more space?": "ทั้งคู่มีจริง แต่อันไหนกินพื้นที่ใจมากกว่า?",
    "The unfairness — this wasn't right": "ความไม่แฟร์ — เรื่องนี้มันไม่ถูกต้อง",
    "The risk — pushing back feels dangerous": "ความเสี่ยง — การสู้กลับดูอันตราย",
    "Both are equally loud": "ดังพอ ๆ กันทั้งคู่",
    "If a colleague you respect were treated this way — what would you say was unfair about it?":
        "ถ้าเพื่อนร่วมงานที่คุณนับถือโดนแบบนี้ — คุณจะบอกว่าอะไรที่ไม่แฟร์?",
    "Stepping outside the moment sometimes makes it clearer.":
        "การถอยออกจากเหตุการณ์บางทีก็ทำให้เห็นชัดขึ้น",
    "What have you already swallowed with this person? How much of today's weight is today's, and how much is the accumulated pile?":
        "กับคนนี้ คุณกลืนอะไรลงไปแล้วบ้าง? น้ำหนักของวันนี้เป็นของวันนี้เท่าไหร่ และเป็นของที่สะสมมาเท่าไหร่?",
    "Does this rhyme with other times?": "มันคล้ายกับครั้งก่อน ๆ ไหม?",

    # ═══ Self-criticism items ══════════════════════════════════
    "When you think about what happened, which feels closer right now?":
        "พอนึกถึงสิ่งที่เกิดขึ้น ข้อไหนใกล้ความรู้สึกตอนนี้กว่า?",
    "There's no right answer — just whichever rings truer this moment.":
        "ไม่มีคำตอบที่ถูก — แค่อันไหนจริงกว่าในตอนนี้",
    "I did something bad": "ฉันทำสิ่งที่ไม่ดีลงไป",
    "I am the mistake": "ฉันนี่แหละคือความผิดพลาด",
    "Honestly, both": "ตามตรง…ทั้งสองอย่าง",
    "What are the critic's exact words? Quote it — or paraphrase if that's easier.":
        "เสียงตำหนิในหัวพูดว่าอะไรคำต่อคำ? ยกมาเลย — หรือเล่าคร่าว ๆ ก็ได้",
    "Only if you're willing. Naming the voice often weakens it a little.":
        "เฉพาะถ้าคุณโอเค การได้เรียกชื่อเสียงนั้นมักทำให้มันเบาลงนิดหนึ่ง",
    "Whose voice does the critic borrow? Does the accent belong to someone from your past?":
        "เสียงตำหนินั้นยืมน้ำเสียงของใครมา? สำเนียงนั้นคุ้นเหมือนใครในอดีตไหม?",
    "Just a rough guess. Even 'not sure' is useful.": "เดาคร่าว ๆ ก็ได้ ตอบว่า 'ไม่แน่ใจ' ก็มีประโยชน์",
    "If your closest friend said those exact words about themselves — what's the first thing you'd feel toward them?":
        "ถ้าเพื่อนสนิทพูดคำเดียวกันนี้กับตัวเอง — สิ่งแรกที่คุณจะรู้สึกต่อเขาคืออะไร?",
    "Take your time with this one.": "ข้อนี้ค่อย ๆ คิดได้เลย",
    "What is the critic trying to protect you from? It usually has a job — even if it does it badly.":
        "เสียงตำหนินั้นพยายามปกป้องคุณจากอะไร? มันมักมีหน้าที่ของมัน — แม้จะทำได้ไม่ดีนัก",
    "When the critic fires — what job does it think it's doing?":
        "เวลาเสียงตำหนิทำงาน — มันคิดว่าตัวเองกำลังทำหน้าที่อะไรอยู่?",
    "Most critics have a job, even when they do it cruelly.":
        "เสียงตำหนิส่วนใหญ่มีหน้าที่ของมัน แม้จะทำหน้าที่นั้นอย่างโหดร้ายก็ตาม",
    "Pushing me so I don't fail or fall behind":
        "ผลักดันฉันเพื่อไม่ให้ล้มเหลวหรือตามคนอื่นไม่ทัน",
    "Warning me before other people judge me":
        "เตือนฉันก่อนที่คนอื่นจะตัดสิน",
    "Not protecting anything — it's just contempt":
        "ไม่ได้ปกป้องอะไรเลย — มันแค่รังเกียจ",
    "A rough guess is more than enough.": "เดาคร่าว ๆ ก็เกินพอแล้ว",

    # ═══ Anxiety items ═════════════════════════════════════════
    "Name the unknown in one line: \"I don't know whether ___\"":
        "ตั้งชื่อสิ่งที่ไม่รู้ในหนึ่งบรรทัด: \"ฉันไม่รู้ว่า ___ หรือเปล่า\"",
    "Just the thing you're most unsure about right now.": "เอาเรื่องที่ไม่แน่ใจที่สุดตอนนี้",
    "Roughly what % of this worry is actually inside your control?":
        "ความกังวลนี้ อยู่ในมือคุณจริง ๆ ประมาณกี่เปอร์เซ็นต์?",
    "A rough number is fine — 0 means nothing, 100 means most of it is up to you.":
        "ตัวเลขคร่าว ๆ ก็พอ — 0 คือไม่อยู่ในมือเลย 100 คือส่วนใหญ่ขึ้นอยู่กับคุณ",
    "Nothing — all out of my hands": "ไม่เลย — อยู่นอกมือทั้งหมด",
    "Most is up to me": "ส่วนใหญ่ขึ้นอยู่กับฉัน",
    "Picture yourself five years from now, on the other side, having coped. What does that version of you know that you can't quite see yet?":
        "ลองนึกภาพตัวเองอีกห้าปีข้างหน้า ที่ผ่านเรื่องนี้มาแล้ว เขารู้อะไรที่คุณตอนนี้ยังมองไม่เห็น?",
    "A rough guess is enough.": "เดาคร่าว ๆ ก็พอ",
    "What decision are you postponing until you feel certain — and what is the waiting costing?":
        "มีการตัดสินใจไหนที่คุณเลื่อนไว้จนกว่าจะแน่ใจ — แล้วการรอนั้นมีราคาเท่าไหร่?",
    "No need to solve it here — just naming it is enough.": "ไม่ต้องแก้ตรงนี้ — แค่เรียกชื่อมันได้ก็พอ",

    # ═══ Grief items ═══════════════════════════════════════════
    "What did you lose? One plain sentence — you don't have to explain or justify it.":
        "คุณสูญเสียอะไรไป? ประโยคเดียวง่าย ๆ — ไม่ต้องอธิบายหรือให้เหตุผล",
    "Is there a feeling you think you're not allowed to have here — relief, anger, nothing at all? All of those are documented, normal grief.":
        "มีความรู้สึกไหนที่คุณคิดว่าตัวเองไม่ควรมีไหม — โล่งใจ โกรธ หรือไม่รู้สึกอะไรเลย? ทั้งหมดนั้นคือความโศกเศร้าปกติที่มีบันทึกไว้จริง",
    "If one of yours feels forbidden, you can name it here.":
        "ถ้ามีความรู้สึกไหนที่เหมือนต้องห้าม เขียนไว้ตรงนี้ได้",
    "Watching yourself from across the room this week — what are you carrying that most people haven't noticed?":
        "ถ้ามองตัวเองจากอีกฝั่งห้องในสัปดาห์นี้ — คุณแบกอะไรอยู่ที่คนส่วนใหญ่ไม่ทันสังเกต?",
    "What would an outside observer see?": "คนที่มองจากข้างนอกจะเห็นอะไร?",
    "What did they — or it — make possible in your life? Which doors are truly closed, and which are only closed for now?":
        "เขา — หรือสิ่งนั้น — เคยทำให้อะไรในชีวิตคุณเป็นไปได้บ้าง? ประตูไหนปิดสนิทจริง ๆ และบานไหนแค่ปิดชั่วคราว?",
    "Take your time. There's no right answer.": "ค่อย ๆ คิดได้ ไม่มีคำตอบที่ถูก",

    # ═══ Anger items ═══════════════════════════════════════════
    "Replay the moment. What happened one second before the anger arrived?":
        "ลองกรอเหตุการณ์กลับไป หนึ่งวินาทีก่อนความโกรธจะมา เกิดอะไรขึ้น?",
    "Anger is often the second emotion. What came first?":
        "ความโกรธมักเป็นความรู้สึกลำดับที่สอง อะไรมาก่อน?",
    "If the anger could only speak one sentence starting with \"It hurt when…\" — what would it say?":
        "ถ้าความโกรธพูดได้แค่ประโยคเดียวที่ขึ้นต้นว่า \"มันเจ็บตอนที่…\" — มันจะพูดว่าอะไร?",
    "Only if it rings true. Some anger is just anger — that's a full answer too.":
        "เฉพาะถ้ามันตรงใจ ความโกรธบางอย่างก็คือความโกรธเฉย ๆ — นั่นก็เป็นคำตอบที่สมบูรณ์เหมือนกัน",
    "A fly on the wall watches the scene. What does it see you feeling first — before the anger armor goes on?":
        "ถ้ามีใครแอบดูเหตุการณ์นั้นอยู่ เขาจะเห็นคุณรู้สึกอะไรก่อน — ก่อนเกราะความโกรธจะสวมทับ?",
    "Step back from it for a moment.": "ถอยออกมามองสักครู่",
    "What does the anger protect? What would be at risk if you showed the hurt instead?":
        "ความโกรธนั้นปกป้องอะไรอยู่? ถ้าคุณแสดงความเจ็บออกมาแทน อะไรจะเสี่ยง?",
    "No judgment on the answer.": "ไม่มีการตัดสินคำตอบ",

    # ═══ Numbness items ════════════════════════════════════════
    "On the outside of the numbness — is there 1% of anything? Heaviness, static, tiredness? Zero is also a real answer.":
        "ตรงขอบ ๆ ของความชา — มีความรู้สึกสัก 1% ไหม? หนัก ๆ ซ่า ๆ เหนื่อย ๆ? ศูนย์ก็เป็นคำตอบจริงเหมือนกัน",
    "No demand to feel. Even noticing the absence is something.":
        "ไม่มีใครบังคับให้รู้สึก แค่สังเกตเห็นความว่างก็นับแล้ว",
    "When did the volume go down — after one event, or slowly over weeks?":
        "เสียงในใจเบาลงตั้งแต่เมื่อไหร่ — หลังเหตุการณ์หนึ่ง หรือค่อย ๆ เบาลงเป็นสัปดาห์?",
    "Just a rough sense.": "ความรู้สึกคร่าว ๆ ก็พอ",
    "After something specific happened": "หลังจากมีเรื่องบางอย่างเกิดขึ้น",
    "Gradually, over time": "ค่อย ๆ เป็นไปตามเวลา",
    "I'm not sure when it started": "ไม่แน่ใจว่าเริ่มเมื่อไหร่",
    "If a documentary narrator described your last two weeks, what would they say you've been through?":
        "ถ้ามีผู้บรรยายสารคดีเล่าชีวิตคุณสองสัปดาห์ที่ผ่านมา เขาจะบอกว่าคุณผ่านอะไรมาบ้าง?",
    "You don't have to feel it — just describe it from the outside.":
        "ไม่ต้องรู้สึกตามก็ได้ — แค่บรรยายจากมุมคนนอก",
    "What did you used to feel most — which feeling went quiet first?":
        "เมื่อก่อนคุณรู้สึกอะไรมากที่สุด — แล้วความรู้สึกไหนเงียบไปก่อนเพื่อน?",
    "Only if something comes up. 'I don't know' is a real answer.":
        "เฉพาะถ้ามีอะไรผุดขึ้นมา ตอบว่า 'ไม่รู้' ก็เป็นคำตอบจริง",

    # ═══ Relationship items ════════════════════════════════════
    "What was the trigger — a message, a silence, a tone? Camera-view only.":
        "จุดที่จุดชนวนคืออะไร — ข้อความ ความเงียบ หรือน้ำเสียง? เล่าแบบภาพจากกล้อง",
    "Just the event, not yet what it means.": "เอาแค่เหตุการณ์ ยังไม่ต้องแปลความหมาย",
    "Finish this: \"It felt like it meant ___\"": "เติมให้จบ: \"มันรู้สึกเหมือนแปลว่า ___\"",
    "What did the silence or tone seem to say?": "ความเงียบหรือน้ำเสียงนั้นเหมือนกำลังบอกอะไร?",
    "If your most secure friend read this situation — what would they bet is actually going on?":
        "ถ้าเพื่อนที่ใจนิ่งที่สุดของคุณอ่านสถานการณ์นี้ — เขาจะเดาว่าจริง ๆ แล้วเกิดอะไรขึ้น?",
    "Not the scary story, but the calm read.": "ไม่ใช่เวอร์ชันน่ากลัว แต่เป็นเวอร์ชันใจเย็น",
    "When the fear says \"they're leaving\" — how often has that alarm been right before? What's its track record, gently reviewed?":
        "เวลาความกลัวบอกว่า \"เขากำลังจะไป\" — ที่ผ่านมาสัญญาณเตือนนี้ถูกบ่อยแค่ไหน? ลองทบทวนสถิติของมันเบา ๆ",
    "Just a rough sense — no need to count every time.": "แค่ความรู้สึกคร่าว ๆ — ไม่ต้องนับทุกครั้ง",

    # ═══ Trapped items ═════════════════════════════════════════
    "What did you say yes to that your body said no to? Name the most recent one.":
        "คุณตอบตกลงเรื่องไหนทั้งที่ร่างกายบอกว่าไม่? เอาครั้งล่าสุด",
    "Specific is more useful than the general pattern.": "เรื่องเฉพาะเจาะจงมีประโยชน์กว่าภาพรวม",
    "Finish this: \"If I say no, then ___\"": "เติมให้จบ: \"ถ้าฉันปฏิเสธ แล้ว ___\"",
    "First guess is enough — what's the scary ending after the no?":
        "เดาแรกก็พอ — ฉากจบน่ากลัวหลังคำว่าไม่คืออะไร?",
    "If you watched a friend carrying this exact obligation load — what would you tell them they're allowed to put down?":
        "ถ้าเห็นเพื่อนแบกภาระหน้าที่ก้อนเดียวกันนี้ — คุณจะบอกเขาว่าอันไหนวางลงได้บ้าง?",
    "What would you say to them that you haven't said to yourself?":
        "อะไรที่คุณจะพูดกับเขา แต่ยังไม่เคยพูดกับตัวเอง?",
    "Whose rule is \"a good person doesn't refuse\"? Did you ever choose it — or did it just arrive with you?":
        "กฎที่ว่า \"คนดีต้องไม่ปฏิเสธ\" เป็นกฎของใคร? คุณเคยเลือกมันเอง — หรือมันแค่ติดตัวมา?",
    "Where did that rule come from?": "กฎนั้นมาจากไหน?",

    # ═══ Trading items ═════════════════════════════════════════
    "Which is closest to what just happened?": "ข้อไหนใกล้เคียงกับสิ่งที่เพิ่งเกิดขึ้นที่สุด?",
    "Rough category is enough — the details can stay yours.":
        "เลือกหมวดคร่าว ๆ ก็พอ — รายละเอียดเก็บไว้เป็นของคุณได้",
    "A loss — bigger than it should have been, and it stings":
        "ขาดทุน — หนักกว่าที่ควรจะเป็น และมันเจ็บ",
    "Missed the move — watched it go without me": "ตกรถ — ได้แต่มองมันวิ่งไปโดยไม่มีเรา",
    "Frozen — my plan says go and my hand won't": "ชะงัก — แผนบอกให้เข้า แต่มือไม่กดสักที",
    "Won big, then gave it all back": "ได้มาก้อนใหญ่ แล้วคืนหมดเกลี้ยง",
    "Right now — what's the strongest pull?": "ตอนนี้ — แรงดึงไหนแรงที่สุด?",
    "Honest answer beats the correct-sounding one.": "คำตอบจริงใจดีกว่าคำตอบที่ฟังดูถูกต้อง",
    "Get it back — today, now": "เอาคืนให้ได้ — วันนี้ เดี๋ยวนี้",
    "Replaying every candle on loop": "ดูแท่งเทียนซ้ำ ๆ วนอยู่ในหัว",
    "Never opening that app again": "ไม่อยากเปิดแอปนั้นอีกเลย",
    "Nothing — just numbly scrolling charts": "ไม่มีอะไรเลย — แค่ไถกราฟไปเรื่อย ๆ อย่างด้านชา",
    "Some losses come with a quiet sentence attached. If yours does, finish it: \"This loss means I am ___\"":
        "การขาดทุนบางครั้งมาพร้อมประโยคเงียบ ๆ ที่แนบมา ถ้าของคุณมี ลองเติมให้จบ: \"ขาดทุนครั้งนี้แปลว่าฉันเป็นคน ___\"",
    "Only if something rings true. A number on a screen often smuggles in a verdict about us.":
        "เฉพาะถ้ามีอะไรตรงใจ ตัวเลขบนหน้าจอมักแอบพ่วงคำตัดสินตัวเรามาด้วย",
    "If a trader you respect took this exact trade, with the same information you had at the time — what would you say happened?":
        "ถ้าเทรดเดอร์ที่คุณนับถือเข้าเทรดไม้เดียวกันนี้ ด้วยข้อมูลเท่าที่คุณมีตอนนั้น — คุณจะบอกว่าเกิดอะไรขึ้น?",
    "Judge the decision with what was knowable then, not with the chart you can see now.":
        "ตัดสินการตัดสินใจด้วยสิ่งที่รู้ได้ ณ ตอนนั้น ไม่ใช่ด้วยกราฟที่เห็นตอนนี้",
    "Set the result aside for a second. Looking only at the decision — how close did it stay to your own plan?":
        "วางผลลัพธ์ไว้ก่อนสักครู่ มองเฉพาะการตัดสินใจ — มันใกล้เคียงแผนของคุณเองแค่ไหน?",
    "Good decisions lose sometimes; bad ones win sometimes. That's exactly why the result can't answer this one.":
        "การตัดสินใจที่ดีก็ขาดทุนได้ การตัดสินใจแย่ก็กำไรได้ — เพราะแบบนี้ผลลัพธ์เลยตอบข้อนี้แทนไม่ได้",
    "Close — the plan was fine, the market did market things":
        "ใกล้เคียง — แผนโอเคแล้ว ตลาดก็แค่ทำตัวเป็นตลาด",
    "It drifted — I crossed a rule I'd set for myself": "มันเบี้ยวไป — ฉันข้ามกฎที่ตัวเองตั้งไว้",
    "There wasn't really a plan yet": "จริง ๆ แล้วยังไม่มีแผน",
    "If this has visited before — the loss, the promise, the repeat — what usually sets the loop going?":
        "ถ้าวงจรนี้เคยแวะมาก่อน — ขาดทุน สัญญากับตัวเอง แล้วก็วนซ้ำ — อะไรที่มักเป็นตัวสตาร์ทลูป?",
    "If it's a first, that counts as an answer too. Patterns only need to be seen once to start loosening.":
        "ถ้าเป็นครั้งแรกก็นับเป็นคำตอบเหมือนกัน แพทเทิร์นแค่ถูกมองเห็นครั้งเดียวก็เริ่มคลายแล้ว",

    # ═══ Other items ═══════════════════════════════════════════
    "In your own words — what's sitting with you right now? Rough is fine.":
        "ในคำของคุณเอง — ตอนนี้มีอะไรค้างอยู่ในใจ? เขียนหยาบ ๆ ได้เลย",
    "There's no category for this one, so the words are all yours.":
        "เรื่องนี้ไม่มีหมวดสำเร็จรูป คำทั้งหมดเป็นของคุณ",
    "If this feeling had a message for you, what would it be trying to say?":
        "ถ้าความรู้สึกนี้มีข้อความถึงคุณ มันน่าจะพยายามบอกอะไร?",
    "First guess counts. Skip if nothing comes.": "เดาแรกก็นับ ถ้าไม่มีอะไรผุดขึ้นมา ข้ามได้",
    "If a kind stranger watched your week from the outside — what would they say you've been carrying?":
        "ถ้าคนแปลกหน้าใจดีเฝ้าดูสัปดาห์ของคุณจากข้างนอก — เขาจะบอกว่าคุณแบกอะไรอยู่?",
    "Describe it from across the room.": "บรรยายจากอีกฝั่งของห้อง",
    "When did you first notice this? Has anything like it visited before?":
        "คุณสังเกตเห็นความรู้สึกนี้ครั้งแรกเมื่อไหร่? เคยมีอะไรคล้าย ๆ กันแวะมาก่อนไหม?",
    "Just a rough timeline — patterns sometimes show themselves.":
        "ไทม์ไลน์คร่าว ๆ ก็พอ — บางทีแพทเทิร์นจะโผล่มาให้เห็นเอง",

    # ═══ Unmet needs (all situations) ══════════════════════════
    "Rest — I'm genuinely depleted": "การพักผ่อน — ฉันหมดแรงจริง ๆ",
    "Control over my own time": "อำนาจควบคุมเวลาของตัวเอง",
    "Feeling capable again": "ความรู้สึกว่าตัวเองทำได้ อีกครั้ง",
    "Permission to say no": "การอนุญาตให้ปฏิเสธได้",
    "Being seen and acknowledged": "การถูกมองเห็นและรับรู้",
    "Being taken seriously": "การถูกเอาจริงเอาจังด้วย",
    "Belonging here": "ความรู้สึกว่าเป็นส่วนหนึ่งของที่นี่",
    "Knowing I matter to them": "การรู้ว่าฉันสำคัญกับเขา",
    "Fairness — something wasn't right": "ความยุติธรรม — บางอย่างมันไม่ถูกต้อง",
    "Respect — being treated as a person": "ความเคารพ — การถูกปฏิบัติอย่างมนุษย์คนหนึ่ง",
    "Safety to speak without consequences": "ความปลอดภัยที่จะพูดโดยไม่โดนอะไรกลับ",
    "Room to make my own decisions": "พื้นที่ให้ตัดสินใจเอง",
    "Acceptance — as I already am": "การยอมรับ — ในแบบที่ฉันเป็นอยู่แล้ว",
    "A standard I actually chose myself": "มาตรฐานที่ฉันเลือกเองจริง ๆ",
    "Rest from watching myself so closely": "การได้พักจากการจับผิดตัวเองตลอดเวลา",
    "Evidence that counts — not just reassurance": "หลักฐานที่นับได้จริง — ไม่ใช่แค่คำปลอบ",
    "Certainty — even knowing I can rarely have it": "ความแน่นอน — แม้จะรู้ว่าแทบไม่มีทางได้",
    "Confidence I could cope either way": "ความมั่นใจว่าจะรับมือได้ ไม่ว่าผลจะออกทางไหน",
    "A plan for the part I can control": "แผนสำหรับส่วนที่ควบคุมได้",
    "Company in the waiting — not being alone with it": "เพื่อนร่วมรอ — ไม่ต้องอยู่กับมันคนเดียว",
    "Permission to grieve at my own pace": "การอนุญาตให้เศร้าตามจังหวะของตัวเอง",
    "Someone to remember with me": "ใครสักคนที่ร่วมระลึกถึงไปด้วยกัน",
    "Rest — I'm exhausted by it": "การพัก — ฉันเหนื่อยกับมันมาก",
    "A way to honor them or it": "วิธีให้เกียรติเขาหรือสิ่งนั้น",
    "Acknowledgment of the hurt": "การยอมรับว่าความเจ็บนี้มีจริง",
    "An apology — something to be made right": "คำขอโทษ — การได้แก้ไขให้ถูกต้อง",
    "Mattering to them": "การมีความหมายกับเขา",
    "Safety to be soft without it being used against me": "ความปลอดภัยที่จะอ่อนโยนโดยไม่ถูกใช้ย้อนมาทำร้าย",
    "Rest — real rest, not just a break": "การพักจริง ๆ — ไม่ใช่แค่หยุดชั่วคราว",
    "Safety to feel again slowly, without being rushed": "ความปลอดภัยที่จะค่อย ๆ กลับมารู้สึก โดยไม่ถูกเร่ง",
    "Connection — even one small moment of it": "ความเชื่อมโยง — แม้แค่ช่วงเวลาสั้น ๆ",
    "Time without demands or expectations": "เวลาที่ไม่มีข้อเรียกร้องหรือความคาดหวัง",
    "Reassurance I can actually trust": "ความมั่นใจที่เชื่อได้จริง",
    "Consistency — knowing where I stand": "ความสม่ำเสมอ — รู้ว่าตัวเองยืนอยู่ตรงไหน",
    "Feeling secure inside myself, not just from them": "ความมั่นคงจากข้างในตัวเอง ไม่ใช่จากเขาอย่างเดียว",
    "The relationship itself to feel safe": "ความสัมพันธ์ที่รู้สึกปลอดภัย",
    "Permission — my own, to say no": "การอนุญาต — จากตัวเอง ให้ปฏิเสธได้",
    "Room to actually choose, not just comply": "พื้นที่ให้ได้เลือกจริง ๆ ไม่ใช่แค่ทำตาม",
    "Rest — from the relentlessness of it": "การพัก — จากความไม่หยุดหย่อนของมัน",
    "A relationship that can survive a no": "ความสัมพันธ์ที่รอดได้แม้มีคำว่าไม่",
    "Making the money back — nothing else matters right now": "เอาเงินคืนมา — ตอนนี้อย่างอื่นไม่สำคัญ",
    "Feeling like I know what I'm doing again": "ความรู้สึกว่าตัวเองรู้ว่ากำลังทำอะไร อีกครั้ง",
    "Deciding calmly — not from the edge": "การตัดสินใจอย่างใจนิ่ง — ไม่ใช่จากขอบเหว",
    "Permission to step away for a while": "การอนุญาตให้ถอยห่างออกมาสักพัก",
    "Being understood": "การมีคนเข้าใจ",
    "Rest — a real pause": "การพัก — การหยุดจริง ๆ",
    "Clarity about what this even is": "ความชัดเจนว่านี่คืออะไรกันแน่",
    "Not being alone with it": "การไม่ต้องอยู่กับมันคนเดียว",

    # ═══ Emotion words ═════════════════════════════════════════
    "overwhelmed": "ท่วมหัว", "pressured": "โดนกดดัน", "depleted": "หมดแรง",
    "burned out": "หมดไฟ", "running on empty": "วิ่งด้วยถังเปล่า",
    "trapped": "ติดกับ", "resentful": "คับข้องใจ", "dread": "หวั่นใจ",
    "foggy": "สมองตื้อ", "inadequate": "ไม่เก่งพอ",
    "invisible": "ไร้ตัวตน", "unimportant": "ไม่สำคัญ", "hurt": "เจ็บ",
    "deflated": "ใจฝ่อ", "quietly angry": "โกรธเงียบ ๆ", "lonely": "เหงา",
    "resigned": "ปลง", "embarrassed": "อาย",
    "powerless": "ทำอะไรไม่ได้", "unfairly treated": "ถูกปฏิบัติไม่แฟร์",
    "intimidated": "เกร็งกลัว", "angry": "โกรธ", "humiliated": "ถูกหักหน้า",
    "anxious": "กังวล", "defiant": "อยากขัดขืน", "torn": "ลังเลฉีกเป็นสองใจ",
    "ashamed": "ละอายใจ", "small": "ตัวลีบเล็ก", "exposed": "เหมือนถูกจับได้",
    "worthless": "ไร้ค่า", "fraudulent": "เหมือนตัวปลอม",
    "disgusted with myself": "เอือมตัวเอง", "tired of myself": "เหนื่อยกับตัวเอง",
    "restless": "กระสับกระส่าย", "frozen": "ชะงักค้าง", "scattered": "คิดฟุ้งกระจาย",
    "on-edge": "ประสาทตึง", "braced": "เกร็งรอ",
    "yearning": "คิดถึงจนปวดใจ", "hollow": "กลวงข้างใน", "heavy": "หนักอึ้ง",
    "guilty": "รู้สึกผิด", "relieved-then-guilty": "โล่งใจแล้วก็รู้สึกผิด",
    "disbelief": "ยังไม่อยากเชื่อ", "tender": "ใจบอบบาง", "empty": "ว่างเปล่า",
    "furious": "โกรธจัด", "betrayed": "ถูกหักหลัง", "unappreciated": "ไม่ถูกเห็นค่า",
    "bitter": "ขมขื่น", "protective": "ต้องคอยป้องกันตัว",
    "hurt underneath": "เจ็บอยู่ข้างใต้", "wounded": "บาดเจ็บข้างใน",
    "numb": "ชา", "flat": "เรียบด้านชา", "distant": "ห่างออกจากทุกอย่าง",
    "disconnected": "หลุดขาดจากทุกอย่าง", "nothing at all": "ไม่รู้สึกอะไรเลย",
    "unwanted": "ไม่เป็นที่ต้องการ", "jealous": "หึงหวง",
    "unsure of my place": "ไม่แน่ใจว่าตัวเองอยู่ตรงไหน",
    "clingy-then-ashamed": "เกาะติดแล้วก็อายตัวเอง",
    "braced for the ending": "เตรียมใจรอวันจบ", "scared": "กลัว",
    "suffocated": "หายใจไม่ออก", "obligated": "จำใจต้องทำ",
    "guilty-in-advance": "รู้สึกผิดล่วงหน้า", "exhausted": "เหนื่อยล้า",
    "cornered": "จนมุม",
    "tilted": "หัวร้อน (tilt)", "wiped out": "พอร์ตพัง", "regret": "เสียดายไม่หาย",
    "FOMO": "FOMO กลัวตกรถ", "frozen at the screen": "ค้างอยู่หน้าจอ",
    "revenge mode": "โหมดเอาคืน", "greedy-then-ashamed": "โลภแล้วก็อายตัวเอง",
    "it's unfair": "มันไม่แฟร์", "can't look away": "ละสายตาไม่ได้",
    "sick of the charts": "เอียนกราฟเต็มทน",
    "unsettled": "ใจไม่สงบ", "confused": "สับสน", "sad": "เศร้า",
    "tense": "ตึงเครียด", "raw": "ใจสด ๆ บอบบาง", "stuck": "ติดค้างอยู่",
    "tired": "เหนื่อย",

    # ═══ Self-compassion lines ═════════════════════════════════
    "You're not behind on being a person. Anyone carrying this load would feel it.":
        "คุณไม่ได้ล้าหลังในการเป็นมนุษย์ ใครแบกเท่านี้ก็รู้สึกแบบนี้ทั้งนั้น",
    "Being overlooked hurts because mattering matters. Your need to be seen is not too much.":
        "การถูกมองข้ามมันเจ็บ เพราะการมีความหมายนั้นสำคัญจริง ความต้องการถูกมองเห็นของคุณไม่ได้มากเกินไปเลย",
    "Feeling small in front of power is a human reflex, not weakness. Your read on unfairness deserves a hearing.":
        "การรู้สึกตัวเล็กต่อหน้าอำนาจคือปฏิกิริยาธรรมชาติของมนุษย์ ไม่ใช่ความอ่อนแอ มุมมองของคุณต่อความไม่แฟร์สมควรได้รับการรับฟัง",
    "Try, in your own words: \"This is a moment of struggle. Struggle is human. May I be on my own side today.\"":
        "ลองพูดในแบบของคุณเอง: \"นี่คือช่วงเวลาที่ยากลำบาก ความยากลำบากคือเรื่องธรรมดาของมนุษย์ ขอให้วันนี้ฉันอยู่ข้างตัวเองบ้าง\"",
    "A mind that scans the future is trying to keep you safe. You can be scared and still choose your next step.":
        "สมองที่คอยสแกนอนาคตกำลังพยายามปกป้องคุณ คุณกลัวได้ และยังเลือกก้าวต่อไปได้ไปพร้อมกัน",
    "Grief is love with nowhere to go yet. You're allowed to take this at your own speed — including the okay days.":
        "ความโศกเศร้าคือความรักที่ยังไม่มีที่ไป คุณมีสิทธิ์ใช้เวลากับมันตามจังหวะของตัวเอง — รวมถึงวันที่โอเคด้วย",
    "Anger that guards a wound is loyalty to yourself. The hurt under it is allowed to exist.":
        "ความโกรธที่เฝ้าแผลคือความภักดีต่อตัวเอง และความเจ็บที่อยู่ข้างใต้ก็มีสิทธิ์มีอยู่",
    "Numbness is often the mind's circuit-breaker, not a defect. Something in you decided to protect you — you can thank it and still want the feeling back.":
        "ความชามักเป็นเบรกเกอร์ตัดไฟของใจ ไม่ใช่ความบกพร่อง บางส่วนในตัวคุณตัดสินใจปกป้องคุณ — ขอบคุณมันได้ พร้อมกับอยากได้ความรู้สึกกลับคืนมาด้วยก็ได้",
    "Wanting to feel secure with someone is wiring, not weakness. Your need for steadiness is legitimate.":
        "การอยากรู้สึกมั่นคงกับใครสักคนคือธรรมชาติของมนุษย์ ไม่ใช่ความอ่อนแอ ความต้องการความมั่นคงของคุณชอบธรรม",
    "A no to them is often a yes to you — that's not selfish, it's a boundary. Your limits are information, not betrayal.":
        "คำว่าไม่กับเขา มักคือคำว่าใช่กับตัวเอง — นั่นไม่ใช่ความเห็นแก่ตัว แต่คือขอบเขต ลิมิตของคุณคือข้อมูล ไม่ใช่การทรยศ",
    "A red day is a fact about a trade — not a verdict on you. The account and your worth are two different ledgers.":
        "วันที่พอร์ตแดงคือข้อเท็จจริงของการเทรดหนึ่งครั้ง — ไม่ใช่คำตัดสินตัวคุณ พอร์ตกับคุณค่าของคุณคือบัญชีคนละเล่มกัน",
    "You showed up for this without even a name for it — that takes honesty. Whatever it is, it's allowed to take up space.":
        "คุณมานั่งตรงนี้ทั้งที่ยังเรียกชื่อมันไม่ถูก — นั่นต้องใช้ความจริงใจ ไม่ว่ามันคืออะไร มันมีสิทธิ์มีพื้นที่",

    # ═══ If-then templates ═════════════════════════════════════
    "If I sit down tomorrow, then I do only the first 25 minutes of my smallest task.":
        "ถ้าพรุ่งนี้ฉันนั่งลงทำงาน ฉันจะทำแค่ 25 นาทีแรกของงานชิ้นเล็กที่สุด",
    "If I feel invisible this week, I will say one sentence out loud within the first ten minutes.":
        "ถ้าสัปดาห์นี้ฉันรู้สึกไร้ตัวตน ฉันจะพูดออกมาหนึ่งประโยคภายในสิบนาทีแรก",
    "If I decide to raise it, I'll write one factual sentence — what happened + what I'm asking for — before the conversation.":
        "ถ้าฉันตัดสินใจจะพูด ฉันจะเขียนหนึ่งประโยคที่เป็นข้อเท็จจริง — เกิดอะไรขึ้น + ฉันขออะไร — ก่อนเริ่มคุย",
    "If the critic starts tonight, I'll write down one thing from the last 7 days it is conveniently ignoring.":
        "ถ้าคืนนี้เสียงตำหนิเริ่มทำงาน ฉันจะเขียนหนึ่งอย่างจาก 7 วันที่ผ่านมาที่มันแกล้งมองข้าม",
    "If the worry starts tonight, I write it in the worry list and close the notebook — it gets its 15 minutes tomorrow.":
        "ถ้าคืนนี้ความกังวลเริ่มมา ฉันจะจดลงลิสต์ความกังวลแล้วปิดสมุด — พรุ่งนี้ค่อยให้เวลามัน 15 นาที",
    "If the hard moment arrives this week, I will light a candle / play a song / write them three lines.":
        "ถ้าสัปดาห์นี้ช่วงเวลาที่ยากมาถึง ฉันจะจุดเทียน / เปิดเพลง / เขียนถึงเขาสักสามบรรทัด",
    "If I'm still hot in an hour, I write the \"It hurt when…\" sentence somewhere private before deciding anything.":
        "ถ้าอีกหนึ่งชั่วโมงยังร้อนอยู่ ฉันจะเขียนประโยค \"มันเจ็บตอนที่…\" ไว้ในที่ส่วนตัว ก่อนตัดสินใจอะไรทั้งนั้น",
    "If I make tea tomorrow, I hold the cup for 30 seconds and just notice warm.":
        "ถ้าพรุ่งนี้ฉันชงชา ฉันจะถือแก้วไว้ 30 วินาที แล้วแค่รับรู้ความอุ่น",
    "If the urge to check or re-ask hits, I wait 20 minutes and write the fear down first — then decide.":
        "ถ้าเกิดอยากเช็คหรือถามซ้ำ ฉันจะรอ 20 นาที เขียนความกลัวลงไปก่อน — แล้วค่อยตัดสินใจ",
    "If a request lands this week, my first sentence is \"Let me check and come back to you\" — the no gets to be a two-step.":
        "ถ้าสัปดาห์นี้มีคำขอเข้ามา ประโยคแรกของฉันคือ \"ขอเช็คก่อนแล้วจะตอบกลับ\" — ให้คำว่าไม่ได้เดินสองจังหวะ",
    "If I take a loss, then I close the platform for 20 minutes before any new order — timer on, screen off.":
        "ถ้าฉันขาดทุน ฉันจะปิดแพลตฟอร์ม 20 นาทีก่อนส่งออเดอร์ใหม่ — ตั้งเวลา ปิดจอ",
    "If this feeling returns tomorrow, I will write three rough lines about it before doing anything else.":
        "ถ้าพรุ่งนี้ความรู้สึกนี้กลับมา ฉันจะเขียนถึงมันสักสามบรรทัดหยาบ ๆ ก่อนทำอย่างอื่น",

    # ═══ Frameworks ════════════════════════════════════════════
    "Grounding & Regulation (DBT-informed)": "ตั้งหลักและปรับสมดุลใจ (แนว DBT)",
    "Somatic Grounding": "กลับมาอยู่กับร่างกาย (Somatic Grounding)",
    "Self-Compassion (CFT / MSC)": "ความเมตตาต่อตัวเอง (CFT / Self-Compassion)",
    "Emotion-Focused (Primary Emotion Access)": "เข้าถึงความรู้สึกที่แท้จริง (EFT)",
    "Grief — Dual Process Normalization": "อยู่กับความสูญเสียอย่างเข้าใจ (Dual Process)",
    "Attachment-Informed Regulation": "ความมั่นคงในความสัมพันธ์ (แนว Attachment)",
    "Cognitive Reappraisal (CBT)": "ปรับมุมคิด (CBT)",
    "Mindful Observation (MBCT-informed)": "สังเกตความคิดอย่างมีสติ (แนว MBCT)",
    "Problem-Solving (PST)": "แก้ปัญหาทีละก้าว (Problem-Solving)",
    "Acceptance & Values (ACT)": "ยอมรับและเลือกตามคุณค่า (ACT)",
    "Behavioural Activation": "ขยับก่อน ใจตามมา (Behavioural Activation)",
    "Implementation Intention": "แผน ถ้า…ฉันจะ… (If-Then)",

    # ═══ Validation pool ═══════════════════════════════════════
    "That makes sense, given what you just described.": "ฟังจากที่คุณเล่ามา ความรู้สึกนี้สมเหตุสมผลมาก",
    "You put that into words — that's harder than it looks.": "คุณเรียบเรียงมันออกมาเป็นคำได้ — ซึ่งยากกว่าที่เห็น",
    "Rough words are fine. There's no grading here.": "คำห้วน ๆ ก็ใช้ได้ ที่นี่ไม่มีการให้คะแนน",
    "Noticing it counts, even when it's hard to name.": "แค่สังเกตเห็นก็นับแล้ว แม้จะยังเรียกชื่อไม่ถูก",
    "You showed up for this — that matters.": "คุณมานั่งอยู่ตรงนี้ — นั่นมีความหมายแล้ว",
    "That took something to write. Take your time with the next one.": "การเขียนแบบนั้นต้องใช้ใจ ข้อต่อไปค่อย ๆ ตอบได้",

    # ═══ Followup check-ins ════════════════════════════════════
    "How are your evenings this week — any easier to switch off?": "สัปดาห์นี้ตอนเย็นเป็นยังไงบ้าง — ปิดสวิตช์ง่ายขึ้นไหม?",
    "Since we talked, did you get to say the thing you wanted seen?": "หลังจากคราวก่อน คุณได้พูดสิ่งที่อยากให้ถูกมองเห็นไหม?",
    "Did you find a way to name what felt unfair — even to yourself?": "คุณได้เรียกชื่อสิ่งที่ไม่แฟร์นั้นไหม — แม้แค่กับตัวเอง?",
    "How has the critic's volume been this week?": "สัปดาห์นี้เสียงตำหนิดังแค่ไหน?",
    "Is the worry still taking the same amount of room?": "ความกังวลยังกินพื้นที่ใจเท่าเดิมไหม?",
    "How has it been to carry this lately — any okay days?": "ช่วงนี้แบกมันเป็นยังไงบ้าง — มีวันที่โอเคบ้างไหม?",
    "When the anger showed up again, could you find the hurt under it?": "ตอนความโกรธกลับมา คุณหาความเจ็บที่อยู่ข้างใต้เจอไหม?",
    "Have you noticed even one small thing you could feel this week?": "สัปดาห์นี้มีสักอย่างเล็ก ๆ ที่คุณพอรู้สึกได้ไหม?",
    "When the fear said 'they're leaving' this week — was it right?": "สัปดาห์นี้ตอนความกลัวบอกว่า 'เขากำลังจะไป' — มันพูดถูกไหม?",
    "Did a two-step 'let me get back to you' get any easier?": "ประโยค 'ขอเช็คก่อนแล้วจะตอบกลับ' ใช้ง่ายขึ้นบ้างไหม?",
    "Did the 20-minute pause rule survive contact with the market this week?": "กฎพัก 20 นาทีรอดจากการเจอตลาดจริงในสัปดาห์นี้ไหม?",
    "How has this been sitting with you since we talked?": "ตั้งแต่คุยกันคราวก่อน เรื่องนี้อยู่กับคุณยังไงบ้าง?",

    # ═══ Hypothesis fragments ══════════════════════════════════
    "some self-criticism": "เสียงตำหนิตัวเองอยู่บ้าง",
    "worry about what happens next": "ความกังวลว่าต่อไปจะเป็นยังไง",
    "hurt underneath the surface": "ความเจ็บที่ซ่อนอยู่ใต้ผิว",
    "a real sense of loss": "ความรู้สึกสูญเสียที่มีอยู่จริง",
    "some emotional flatness": "ความด้านชาทางความรู้สึกอยู่บ้าง",
    "worry about your place in this relationship": "ความกังวลถึงที่ทางของคุณในความสัมพันธ์นี้",
    "tension around choices": "ความอึดอัดเรื่องการต้องเลือก",
}


# ═══ Framework technique texts (TH) — keyed by framework code ═══
TH_TECHNIQUES: dict[str, str] = {
    "F5_DBT": (
        "**TIPP:** อุณหภูมิ · ออกแรงสั้น ๆ · หายใจช้า ๆ · คลายกล้ามเนื้อ\n\n"
        "เริ่มได้เลยตอนนี้: หายใจเข้านับ 4 หายใจออกนับ 6 ทำ 8 รอบ "
        "ครบแล้วลองเช็คตัวเลขความรู้สึกอีกครั้ง"
    ),
    "F8_somatic": (
        "**หลัก 5-4-3-2-1:** บอกชื่อ 5 สิ่งที่เห็น · 4 สิ่งที่สัมผัสได้ · 3 เสียงที่ได้ยิน · "
        "2 กลิ่นที่ได้กลิ่น · 1 รสที่รับรู้\n\n"
        "หรือ: ถืออะไรอุ่น ๆ ไว้ 30 วินาที — รับรู้แค่ความอุ่นอย่างเดียว"
    ),
    "F3_CFT": (
        "**แผนที่สั้น ๆ — ระบบสามวงในใจ:** อารมณ์ทำงานผ่านสามระบบ — ระบบ**เตือนภัย** "
        "(สัญญาณอันตราย เสียงตำหนิตัวเอง) ระบบ**ขับเคลื่อน** (ไล่ล่า ทำให้สำเร็จ) และ"
        "ระบบ**ปลอบประโลม** (ความปลอดภัย ความอบอุ่น) การโจมตีตัวเองคือตอนที่ระบบเตือนภัยดังลั่น "
        "ส่วนระบบปลอบประโลมปิดอยู่ การฝึกนี้คือการเปิดระบบปลอบประโลมกลับมา — มันคือทักษะ ไม่ใช่อารมณ์\n\n"
        "**พักด้วยความเมตตาต่อตัวเอง (3 นาที):**\n"
        "1. วางมือบนหัวใจ พูดว่า: \"นี่คือช่วงเวลาที่ยากลำบาก\"\n"
        "2. พูดว่า: \"ความยากลำบากคือส่วนหนึ่งของการเป็นมนุษย์ ฉันไม่ได้เจอสิ่งนี้คนเดียว\"\n"
        "3. ถามตัวเอง: \"ถ้าเพื่อนสนิทรู้สึกแบบนี้ ฉันจะพูดกับเขาว่าอะไร?\" — แล้วพูดคำนั้นกับตัวเอง"
    ),
    "F6_EFT": (
        "**ย้อนหาหนึ่งวินาทีก่อนหน้า:**\n"
        "กรอเหตุการณ์กลับไป อะไรมาก่อนความโกรธหนึ่งวินาที?\n\n"
        "ถ้าเจอ: เขียนหนึ่งประโยคขึ้นต้นว่า \"มันเจ็บตอนที่...\" ไว้ในที่ส่วนตัว "
        "ยังไม่ต้องตัดสินใจอะไรทั้งนั้น"
    ),
    "F14_grief": (
        "**โมเดลการแกว่งไปมา:** ความโศกเศร้าเคลื่อนไปมาระหว่างโหมดคิดถึง "
        "(ร้องไห้ คิดถึง รู้สึก) กับโหมดใช้ชีวิต (จัดการชีวิต มีช่วงโอเค หรือแม้แต่ยิ้มได้)\n\n"
        "วันที่โอเคไม่ใช่การทรยศ มันคือความโศกเศร้าที่แข็งแรงกำลังทำหน้าที่ของมัน\n\n"
        "สัปดาห์นี้: อนุญาตให้ตัวเองมีหนึ่งชั่วโมงของการใช้ชีวิต โดยไม่ต้องรู้สึกผิด"
    ),
    "F15_attachment": (
        "**ตรวจสอบสัญญาณเตือน:**\n"
        "เขียนว่า: \"สัญญาณเตือนบอกว่า [สิ่งที่กลัว]\"\n"
        "แล้วเขียนสถิติของมัน — ที่ผ่านมาสัญญาณเตือนแบบนี้ถูกบ่อยแค่ไหน?\n\n"
        "เวลาอยากเช็คหรือถามซ้ำ: รอ 20 นาที เขียนความกลัวลงไปก่อน แล้วค่อยตัดสินใจ"
    ),
    "F1_CBT": (
        "**เช็คความน่าจะเป็น:**\n"
        "เขียนกรณีเลวร้ายที่สุดในหนึ่งประโยค แล้วถาม:\n"
        "1. โอกาสเกิดขึ้นจริงกี่เปอร์เซ็นต์?\n"
        "2. ถ้าเกิดจริง — ฉันจะทำยังไง?\n"
        "3. กรณีที่สมจริงที่สุดคืออะไร?\n\n"
        "เป้าหมายคือคิดให้แม่น ไม่ใช่คิดบวก"
    ),
    "F9_MBCT": (
        "**ดูความคิด แต่ไม่ขึ้นรถไปกับมัน:**\n"
        "นั่งเงียบ ๆ 2 นาที พอความคิดมา ให้ติดป้ายชื่อ: 'นั่นไง ความกังวลมาแล้ว' "
        "'นั่นเสียงตำหนิตัวเอง' ไม่ต้องแก้ — แค่เห็นว่ามันคือความคิด ไม่ใช่ความจริง\n\n"
        "ตั้งเวลาไว้ พอเสียงเตือนดังก็จบ"
    ),
    "F10_PST": (
        "**สี่ขั้นกับเรื่องเดียว:**\n"
        "1. นิยามปัญหาในหนึ่งประโยค (ปัญหาจริง ๆ ไม่ใช่ทุกอย่างพร้อมกัน)\n"
        "2. ลิสต์ 3 ทางเลือก — รวมทางที่ไม่สมบูรณ์แบบด้วย\n"
        "3. เลือกทางที่เล็กที่สุดที่ลองได้ในสัปดาห์นี้\n"
        "4. เขียนแผน ถ้า…ฉันจะ…: ถ้า [สถานการณ์] ฉันจะ [การกระทำ]"
    ),
    "F4_ACT": (
        "**คำถามคุณค่า:** \"ถ้าความกลัวไม่มีสิทธิ์โหวต — คุณจะเลือกอะไร?\"\n\n"
        "**คลายพันธนาการความคิด:** พอความคิดที่เจ็บมา ลองพูดว่า "
        "'ฉันกำลังมีความคิดว่า [ความคิดนั้น]' สังเกตช่องว่างระหว่างคุณกับความคิด\n\n"
        "**ความเต็มใจ:** ลองให้ความอึดอัดอยู่ตรงนี้อีก 10 วินาที โดยไม่ต้องสู้กับมัน"
    ),
    "F2_BA": (
        "**ลงมือก่อน อารมณ์ตามมา** เวลาใจหม่น กับดักคือการรอให้อยากทำก่อน — "
        "จริง ๆ แล้วการทำมาก่อนความรู้สึก\n\n"
        "**1. หนึ่งอย่างเล็ก ๆ 5 นาที** ที่เคยให้อะไรกลับมาแม้แค่ 1% "
        "ไม่ต้องรู้สึกดีก็ได้ — นัดเวลา ทำ แล้วสังเกต: หลังทำกับก่อนทำ มีอะไรขยับไหม?\n\n"
        "**2. เพิ่มการขยับร่างกาย — แบบไหนก็นับ** หลักฐานชัดที่สุดคือเดินเร็วหรือวิ่งเบา ๆ "
        "เวทเทรนนิ่ง โยคะ หรือเต้น — แค่ 20 นาทีก็ได้ เลือกอันที่เป็นไปได้ที่สุดในสัปดาห์นี้\n\n"
        "**3. พรุ่งนี้ทำซ้ำ** อย่างเดิมหรืออย่างใหม่ก็ได้ "
        "เป้าหมายคือกลับมาเชื่อมต่อ ยังไม่ใช่ความสนุก — ความสนุกจะตามมาทีหลัง"
    ),
    "F12_ifthen": (
        "**แผน ถ้า…ฉันจะ…:**\n"
        "ถ้า [ตัวกระตุ้นที่ชัดเจน] ฉันจะ [การกระทำที่ชัดเจน]\n\n"
        "ยิ่งตัวกระตุ้นและการกระทำชัดเท่าไหร่ แผนยิ่งได้ผล เริ่มจากแผนที่คุณเขียนไว้ด้านบน"
    ),
}


# ═══ Long scripts / notes (TH) ═════════════════════════════════
SAFETY_SCRIPT_TH = (
    "ขอบคุณที่บอกเรา ความปลอดภัยของคุณสำคัญกว่าทุกเซสชัน\n\n"
    "ตอนนี้ อยากให้คุณติดต่อใครสักคน:\n"
    "• **ประเทศไทย:** สายด่วนสุขภาพจิต 1323 (กรมสุขภาพจิต ฟรี ตลอด 24 ชม.)\n"
    "• **ต่างประเทศ:** findahelpline.com\n\n"
    "ถ้าอยู่ในอันตรายเฉพาะหน้า โปรดโทรหาหน่วยฉุกเฉินทันที\n\n"
    "เซสชันนี้ขอพักไว้ก่อน กลับมาได้เสมอเมื่อคุณปลอดภัยแล้ว"
)

GROUNDING_PAUSE_SCRIPT_TH = (
    "ร่างกายของคุณกำลังบอกอะไรบางอย่างที่สำคัญ — เราฟังมันกันเถอะ\n\n"
    "คำถามพวกนี้รอได้เสมอ ตอนนี้เอาแค่นี้พอ:\n\n"
    "**หายใจแบบ 4-7-8:** เข้านับ 4 · กลั้นนับ 7 · ออกนับ 8\n\n"
    "ทำสามรอบ แล้วหาอะไรอุ่น ๆ มาถือไว้\n\n"
    "กลับมาได้เมื่อพร้อม ไม่ต้องรีบเลย"
)

REFERRAL_SCRIPT_TH = (
    "บางอย่างที่คุณเล่ามาฟังดูหนักจริง ๆ — หนักกว่าที่เครื่องมือสะท้อนใจถูกออกแบบมาให้รองรับ\n\n"
    "เครื่องมือนี้แทนการคุยกับคนที่ถูกฝึกมาเพื่อเรื่องนี้ไม่ได้ "
    "และการขอความช่วยเหลือคือความเข้มแข็ง ไม่ใช่ความล้มเหลว ถ้าช่วยได้ นี่คือทางเลือก:\n"
    "• **ประเทศไทย:** สายด่วนสุขภาพจิต 1323 (ฟรี ตลอด 24 ชม.)\n"
    "• **ต่างประเทศ:** findahelpline.com\n\n"
    "คุณเป็นคนคุมว่าอะไรจะเกิดต่อ — ที่นี่ไม่มีอะไรที่คุณต้องอธิบาย"
)

TRAUMA_ACK_TH = (
    "บางอย่างที่คุณเล่ามาฟังดูหนักมากจริง ๆ แทนที่จะลงลึกต่อ "
    "เราค่อย ๆ ช้าลงและช่วยให้ใจนิ่งก่อนดีกว่า — นั่นคือทางที่อ่อนโยนกว่าเวลาความรู้สึกใหญ่ขนาดนี้"
)

LOW_MOOD_NOTE_TH = (
    "มีเรื่องหนึ่งที่อยากบอกตรง ๆ อย่างอ่อนโยน: คุณบอกเราว่าช่วงสองสัปดาห์นี้ "
    "ใจหม่นเกือบทุกวัน และสิ่งที่เคยชอบก็เงียบลง สองอย่างนี้รวมกันเป็นสัญญาณที่ควรใส่ใจ — "
    "ไม่ใช่คำตัดสิน แต่คือสัญญาณ\n\n"
    "ถ้ามันอยู่นานเกินสองสัปดาห์ การคุยกับผู้เชี่ยวชาญช่วยได้จริง ๆ — ยิ่งเร็วยิ่งเบาแรง\n"
    "• **ประเทศไทย:** สายด่วนสุขภาพจิต 1323 (กรมสุขภาพจิต ฟรี ตลอด 24 ชม.)\n"
    "• **ต่างประเทศ:** findahelpline.com\n\n"
    "ระหว่างนี้ เทคนิคด้านล่างถูกเลือกมาสำหรับแพทเทิร์นนี้โดยเฉพาะ — "
    "เริ่มจากการกระทำเล็ก ๆ ก่อน แล้วอารมณ์จะตามมา การขยับร่างกายก็ช่วย: "
    "แค่เดินวันละ 20 นาที ก็ยกระดับอารมณ์ได้จริงในไม่กี่สัปดาห์"
)

OTHERS_FIRST_LEAD_TH = (
    "ความเมตตาที่เล็งตรงมาที่ตัวเองอาจรู้สึกปลอมหรือไม่คู่ควร — นั่นเป็นเรื่องปกติ ไม่ใช่ข้อบกพร่อง "
    "งั้นเราเริ่มจากด้านข้างก่อน: ลองนึกภาพคนที่คุณรักกำลังรู้สึกแบบเดียวกับที่คุณรู้สึกอยู่ "
    "คุณอยากให้เขาได้ยินอะไร? ตอนนี้ ขอแค่ชั่วครู่ ลองให้ประโยคเดียวกันนั้นหันมาหาตัวคุณเอง:"
)
BACKDRAFT_NOTE_TH = (
    "ขอเตือนเบา ๆ ว่า พอหันความอบอุ่นเข้าหาตัวเอง บางทีคลื่นบางอย่างจะพุ่งขึ้นมา — "
    "ความเศร้า หรือเสียงคม ๆ ว่า \"ฉันไม่คู่ควรกับสิ่งนี้\" นั่นเรียกว่า **backdraft** — "
    "ความเจ็บเก่าที่กำลังละลาย ไม่ใช่ความล้มเหลว ถ้าตอนนี้มันเยอะเกินไป แตะพัก แล้วเราจะช่วยให้ใจนิ่งแทน"
)

CRITIC_DRIVER_TH = (
    "เสียงตำหนิของคุณคือ**ตัวเร่ง** — มันผลักเพื่อไม่ให้คุณล้มเหลว เชื้อเพลิงที่เป็น"
    "ความกลัวมันได้ผลจริง แต่มันเผาเครื่องยนต์จนไหม้ คุณมีสิทธิ์เก็บมาตรฐานไว้และวาง"
    "แส้ลง — แรงผลักเดียวกันมาจากการอยากได้สิ่งดี ๆ ให้ตัวเองก็ได้ ไม่ใช่จากความหวาดกลัว"
)

CRITIC_SOCIAL_THREAT_TH = (
    "เสียงตำหนิของคุณคือ**ยาม** — มันคอยสแกนคำตัดสินของคนอื่น แล้วพยายามจับให้ได้ก่อน "
    "เพื่อไม่ให้คำปฏิเสธมาโจมตีคุณแบบไม่ทันตั้งตัว มันเฝ้าความกลัวที่มีจริง แต่ราคาที่ซ่อน"
    "อยู่คือ เพื่อจะนำหน้าคำตัดสินของพวกเขา คุณเลยตัดสินตัวเองก่อนทุกวัน"
)

CRITIC_ATTACKER_TH = (
    "เสียงนี้ไม่ได้ปกป้องอะไรเลย — มันคือ**ความรังเกียจที่คุณเรียนรู้มา** บ่อยครั้งเป็น"
    "น้ำเสียงที่ยืมมาจากใครบางคน นั่นคือชนิดที่ยากที่สุดที่จะเผชิญคนเดียว และคุณไม่จำเป็น"
    "ต้องเผชิญคนเดียว การได้คุยเรื่องนี้กับคนที่ถูกฝึกมาช่วยได้จริง ๆ"
)

HATED_SELF_NOTE_TH = (
    "วิธีที่คุณพูดกับตัวเองตอนนี้ ใกล้เคียงกับการโจมตีมากกว่าการแก้ไข — และนั่นเป็นเรื่องที่"
    "ควรใส่ใจอย่างอ่อนโยน คุณคงไม่ได้รับเสียงแบบนี้มา ถ้าไม่มีอะไรสอนมันให้คุณ "
    "คนที่ถูกฝึกมาช่วยให้คุณวางมันลงได้ คุณไม่ต้องแบกมันไว้คนเดียว\n"
    "• **ประเทศไทย:** สายด่วนสุขภาพจิต 1323 (ฟรี ตลอด 24 ชม.)\n"
    "• **ต่างประเทศ:** findahelpline.com"
)

CHASING_NOTE_TH = (
    "มีแพทเทิร์นหนึ่งในสิ่งที่คุณเล่าที่อยากเรียกชื่อเบา ๆ: แรงดึงที่อยาก \"เอาคืน\" "
    "งานวิจัยเรียกสิ่งนี้ว่า **การไล่ตามความเสียหาย (chasing)** — "
    "และมันคือแพทเทิร์นที่เชื่อมโยงกับการสูญเสียที่บานปลายมากที่สุด "
    "มันไม่ใช่ข้อบกพร่องของนิสัย แต่คือวิธีที่การขาดทุนต่อสายความเร่งด่วนเข้าไปในใจของทุกคน\n\n"
    "**แรงกระตุ้นนั้นผ่านไปเองได้** มันขึ้นและลงเหมือนคลื่น — ส่วนใหญ่ภายใน 20 นาที "
    "ตั้งเวลา ปิดแพลตฟอร์ม แล้วเฝ้าดูแรงกระตุ้นโดยไม่ต้องทำตาม "
    "โต้คลื่นสำเร็จหนึ่งครั้ง คลื่นลูกต่อไปจะเบาลง\n\n"
    "ถ้าความเครียดเรื่องเงินจากการเทรดเริ่มแตะค่าเช่า หนี้ หรือเรื่องที่เก็บเป็นความลับ — "
    "นั่นคือน้ำหนักที่ควรแบ่งให้คนที่รู้จักเส้นทางนี้ช่วยถือ:\n"
    "• **ประเทศไทย:** สายด่วนสุขภาพจิต 1323 (ฟรี ตลอด 24 ชม.)\n"
    "• **ต่างประเทศ:** findahelpline.com — มีสายด่วนเรื่องการพนันแยกตามประเทศ\n\n"
    "ไม่มีคำตัดสินที่นี่ แค่แพทเทิร์นที่จับได้เร็วยิ่งดี"
)
