"""Relationship sub-goal specific personality content — Thai Gen Z style."""

MBTI_RELATIONSHIP: dict[tuple[str, str], dict] = {

    # ═══════════════ create_attraction ═══════════════
    ("NT", "create_attraction"): {
        "mbti_context": "NT น่าประทับใจมากทางสติปัญญา แต่บางทีมา intense หรือ analytical เกินจนอีกฝ่ายรู้สึกถูก interview มากกว่าถูก court Attraction สร้างจาก fun และ playfulness ไม่ใช่จาก impressing เขาด้วยความฉลาด",
        "tension": "NT แสดง intelligence เป็นหลัก แต่ attraction ต้องการ warmth และ lightness ที่ NT มักข้ามไป",
        "conflict_example": 'คุณ: "ฉัน notice ว่าคุณ mentioned [topic] ก่อนหน้า ซึ่งน่าสนใจมากเพราะ [analysis ยาว]"\nอีกฝ่าย: "อ๋อ... ใช่ นั่นก็เป็นมุมที่ interesting นะ"\nคุณ: "แล้วคุณคิดยังไงกับ [deeper aspect] ด้วย?"\nอีกฝ่าย: [เริ่มรู้สึกเหนื่อย] "ก็ยังไม่ได้คิดลึกขนาดนั้น"\nคุณ: "เดี๋ยวฉัน walk through rationale ของฉันให้ฟัง"\nอีกฝ่าย: [อยากออกไปแล้ว]\n\nคุณ fascinating มาก แต่ conversation รู้สึกเป็น lecture ไม่ใช่ connection',
        "why_fails": "NT ใช้ intellectual depth เป็น way ของการ show interest แต่อีกฝ่ายรู้สึกว่าถูก analyzed ไม่ใช่ understood — มันสร้าง admiration ไม่ใช่ attraction",
        "recommended_example": 'คุณ: "ฉัน notice คุณ mention [topic] ฉัน curious มาก — สิ่งที่ทำให้คุณสนใจเรื่องนั้นคืออะไร?"\nอีกฝ่าย: "จริงๆ เริ่มจาก [เรื่องส่วนตัว]"\nคุณ: [ฟังจริงๆ แล้ว laugh] "โห นั่นมันเป็นแบบนั้นด้วยเหรอ? ฉันก็เจอ [relatable experience] เหมือนกัน"\nอีกฝ่าย: [เริ่ม open up มากขึ้น]',
        "the_shift": "เปลี่ยนจาก 'ฉัน impressive' เป็น 'คุณ interesting' — ถามมากขึ้น วิเคราะห์น้อยลง ฟังด้วยความ genuine curiosity",
    },
    ("NF", "create_attraction"): {
        "mbti_context": "NF ให้ความสนใจและ warmth ได้อย่าง genuine มาก แต่บางทีให้เร็วเกินจน อีกฝ่ายรู้สึกว่า 'มันเร็วเกินไป' Attraction ต้องการ mystery และ tension เล็กน้อย ไม่ใช่ instant full openness",
        "tension": "NF เปิดตัวเองและให้ attention อย่างสมบูรณ์เร็วเกินไป ทำให้ tension ที่ create attraction หายไป",
        "conflict_example": 'อีกฝ่าย: "เล่าเรื่องตัวเองให้ฟังหน่อย"\nคุณ: [เล่าทุกอย่างอย่าง genuine] "...แล้วก็ฉัน really value [deep value] และ dream ของฉันคือ [personal dream]"\nอีกฝ่าย: [รับข้อมูลเยอะมาก] "โอ้... interesting มากเลย"\nคุณ: "แล้วคุณล่ะ? เล่าได้เลยนะ ฉัน want to know everything"\nอีกฝ่าย: [รู้สึก overwhelmed] "ก็... เดี๋ยวค่อยเล่ากัน"\n\nคุณ genuine มาก แต่มัน too much too soon',
        "why_fails": "NF เปิด fully เพราะ feel ว่ามันเป็น authentic connection แต่ attraction อาศัย pace ที่ค่อยๆ reveal มีความ look forward to ทุกครั้งที่เจอ",
        "recommended_example": 'อีกฝ่าย: "เล่าเรื่องตัวเองให้ฟังหน่อย"\nคุณ: "ฉัน [brief interesting thing] แต่อยากถามคุณก่อน สิ่งที่ทำให้คุณ excited ที่สุดตอนนี้คืออะไร?"\nอีกฝ่าย: [เล่า]\nคุณ: [ฟังจริงๆ ตอบน้อยพอที่จะ leave them wanting more]',
        "the_shift": "เปิดตัวเองทีละ layer ไม่ใช่ทั้งหมดทีเดียว — ให้เขามีเหตุผลที่อยาก know more ในครั้งต่อไป",
    },
    ("SJ", "create_attraction"): {
        "mbti_context": "SJ reliable และ consistent ซึ่งเป็น quality ที่ดีมากสำหรับ relationship ระยะยาว แต่ attract ในช่วงแรกต้องการ spark และ spontaneity บ้าง ไม่ใช่แค่ predictability ต้องหาวิธีสร้าง surprise เล็กๆ บ้าง",
        "tension": "SJ ทำทุกอย่าง predictably ดีมาก แต่ attraction ต้องการ element ของ surprise ที่ SJ ไม่ค่อย comfortable กับ",
        "conflict_example": 'อีกฝ่าย: "คืนนี้ทำอะไรดีนะ?"\nคุณ: "เดิม dinner ที่ [ร้านเดิม] แล้วก็กลับบ้าน 10 โมง เหมือนที่ทำทุกอาทิตย์"\nอีกฝ่าย: "อ๋อ... predictable ดีนะ"\nคุณ: "ใช่ routine ช่วยให้จัดการเวลาได้ดี"\nอีกฝ่าย: [internal] ทำไมมันน่าเบื่อแบบนี้\n\nReliable มาก แต่ไม่มี spark',
        "why_fails": "SJ ให้ความมั่นคงซึ่งคนต้องการในระยะยาว แต่ตอน early attraction คนต้องการรู้สึก excited ด้วย ไม่ใช่แค่ comfortable",
        "recommended_example": 'อีกฝ่าย: "คืนนี้ทำอะไรดีนะ?"\nคุณ: "ฉันเจอ [place/activity] ที่ดูน่าสนใจมาก อยากลองไหม? ถ้าไม่ ok ก็ flexible นะ"\nอีกฝ่าย: "โอ้ จริงเหรอ อยากลอง!"\n[หรือ plan เล็กๆ ที่ unexpected]\nคุณ: [เซอร์ไพรส์ด้วย thoughtful gesture เล็กๆ]',
        "the_shift": "Reliability เป็น foundation ที่ดี แต่ add surprise เล็กๆ เป็นครั้งคราว — one unexpected thing ต่อ meeting สร้าง anticipation",
    },
    ("SP", "create_attraction"): {
        "mbti_context": "SP สนุก exciting และ present ซึ่ง attractive มาก แต่บางทีขาด depth ที่ทำให้อีกฝ่ายรู้สึกว่า connection มีความหมาย ต้องการ moments ที่ show ว่าคุณ genuinely สนใจในตัวเขา ไม่ใช่แค่ enjoy being together",
        "tension": "SP สร้าง fun และ excitement ดีมาก แต่ขาด depth ที่ทำให้อีกฝ่ายรู้สึกว่า seen และ understood",
        "conflict_example": 'คุณ: [ทั้ง date] สนุกมาก เล่น joke เยอะ energy สูง\nอีกฝ่าย: [enjoy แต่ไม่แน่ใจว่าคุณ actually แคร์เขาหรือเปล่า]\nคุณ: "สนุกมากเลย เจอกันอีกครั้งนะ!"\nอีกฝ่าย: [internal] เขา like ฉันจริงๆ หรือแค่ enjoy ที่มีคนมาสนุกด้วย?\n\nFun มาก แต่อีกฝ่ายไม่แน่ใจว่า connection จริง',
        "why_fails": "SP create great moments แต่ moments ที่ไม่มี depth ทำให้อีกฝ่ายสงสัยว่า special จริงๆ ไหม หรือ SP แค่สนุกกับทุกคนแบบนี้",
        "recommended_example": 'คุณ: [ระหว่าง date ที่สนุก] "รู้อะไรไหม ฉัน notice ว่าคุณ [specific observation เกี่ยวกับตัวเขา] มันน่าสนใจมาก ทำไมถึงเป็นแบบนั้น?"\nอีกฝ่าย: [รู้สึกว่าถูก seen จริงๆ] "โห ไม่เคยมีใคร notice เรื่องนั้นมาก่อน..."\n[แล้วเปิดขึ้นมากกว่าเดิม]',
        "the_shift": "Add one genuine, specific observation เกี่ยวกับเขาต่อ date — ทำให้เขารู้ว่าคุณ actually pay attention ไม่ใช่แค่ enjoy the fun",
    },

    # ═══════════════ build_connection ═══════════════
    ("NT", "build_connection"): {
        "mbti_context": "NT มักอยู่ใน head ตลอดเวลาและ analyze แทนที่จะ feel ร่วม Connection ที่ลึกเกิดจากการที่อีกฝ่ายรู้สึกว่าคุณ present กับเขาจริงๆ ไม่ใช่กำลัง process information ของเขาอยู่",
        "tension": "NT อยู่ใน intellectual space มากจน miss emotional presence ที่ connection ต้องการ",
        "conflict_example": 'อีกฝ่าย: "ฉันเครียดมากเรื่องนี้เลย"\nคุณ: "โอเค ถ้าวิเคราะห์ situation จะเห็นว่า option ที่ดีที่สุดคือ [analysis]"\nอีกฝ่าย: "ก็แต่ฉันแค่รู้สึกหนักมาก"\nคุณ: "ฉันเข้าใจ แต่ถ้า approach มันแบบ systematic จะจัดการง่ายขึ้น"\nอีกฝ่าย: [ถอยออก] "ก็ใช่นะ..."\n\nคุณ helpful มาก แต่อีกฝ่ายต้องการ heard ไม่ใช่ fixed',
        "why_fails": "NT กระโดดไปที่ solution เพราะนั่นคือวิธีที่ care แต่ตอนที่คนเล่าความรู้สึก พวกเขาต้องการ witnessed ก่อน ไม่ใช่ solved",
        "recommended_example": 'อีกฝ่าย: "ฉันเครียดมากเรื่องนี้เลย"\nคุณ: "ฟังดูหนักมากเลยนะ บอกให้ฟังได้ เกิดอะไรขึ้น?"\nอีกฝ่าย: [เล่าต่อ]\nคุณ: [ฟังจริงๆ ไม่ interrupt ด้วย solution]\nคุณ: "นั่นมันยากมากเลยนะ รู้สึกยังไงบ้างกับมัน?"\n[ถ้าอีกฝ่าย ask หา advice ค่อย give]',
        "the_shift": "ก่อน offer solution ถามก่อนว่า 'อยากระบาย หรืออยากหาทางออก?' — คนต้องการถูกถามก่อน",
    },
    ("NF", "build_connection"): {
        "mbti_context": "NF มี empathy สูงมาก แต่บางทีเริ่ม project ความรู้สึกของตัวเองเข้าไปในเรื่องของอีกฝ่ายแทนที่จะฟังว่าเขา actually feel อะไร Connection ที่แท้จริงต้องการให้อีกฝ่าย feel understood ด้วยภาษาของเขา ไม่ใช่ภาษาของคุณ",
        "tension": "NF empathize มากจนบางทีเริ่ม project feeling แทนที่จะ listen to what's actually there",
        "conflict_example": 'อีกฝ่าย: "ฉันหยุดงานนั้นแล้ว"\nคุณ: "โห ต้องรู้สึก relieved มากเลยนะ ในที่สุดก็ได้ออกมาจาก toxic situation"\nอีกฝ่าย: "จริงๆ... ฉันเศร้านะ ชอบทีมมาก"\nคุณ: "โอ้ ก็แต่ที่บอกว่า manager แย่—"\nอีกฝ่าย: "ก็แย่ แต่มันก็มีส่วนดีด้วยนะ"\nคุณ: "ฉันเข้าใจ แต่ระยะยาวมันดีกว่าแน่นอน"\nอีกฝ่าย: [รู้สึกว่าไม่ถูก heard จริงๆ]',
        "why_fails": "NF เห็น narrative ที่ควรเป็นแล้ว impose ลงไป แทนที่จะฟังว่า narrative จริงๆ ของอีกฝ่ายเป็นอะไร ทำให้อีกฝ่ายรู้สึกว่า 'คุณฟังฉัน แต่ไม่ได้ยินฉัน'",
        "recommended_example": 'อีกฝ่าย: "ฉันหยุดงานนั้นแล้ว"\nคุณ: "โห จริงเหรอ รู้สึกยังไงบ้าง?"\nอีกฝ่าย: "ปนกัน ทั้ง relieved ทั้งเศร้า"\nคุณ: "เศร้าเรื่องอะไรบ้าง?"\nอีกฝ่าย: [เล่าต่อ ด้วยความรู้สึกของเขาเอง]',
        "the_shift": "ถามว่า 'รู้สึกยังไง?' ก่อน assume ว่ารู้ว่าเขารู้สึกอะไร — ให้เขา tell you ด้วยภาษาของเขาเอง",
    },
    ("SJ", "build_connection"): {
        "mbti_context": "SJ มักแชร์ facts เกี่ยวกับตัวเอง แต่ connection ที่ลึกเกิดจากการแชร์ feelings ด้วย ต้องฝึกพูดว่า 'ตอนนั้นฉันรู้สึก...' มากกว่า 'ตอนนั้นฉันทำ...' เพราะ feelings คือสิ่งที่สร้าง real bond",
        "tension": "SJ share experiences แต่ filter out feelings ทำให้ conversations เป็น informational ไม่ใช่ connective",
        "conflict_example": 'อีกฝ่าย: "เล่าเรื่อง job แรกของคุณให้ฟังหน่อย"\nคุณ: "ฉันเริ่มทำงานที่ [company] ปี [year] ทำ [role] เงินเดือน [X] อยู่ที่นั่น 3 ปี แล้วย้ายมา [next company]"\nอีกฝ่าย: "ตอนนั้นรู้สึกยังไงบ้าง?"\nคุณ: "ก็ทำงานดี บรรลุเป้าหมายที่ตั้งไว้"\nอีกฝ่าย: "แต่ตอนเริ่มแรกเลย... กลัวไหม? ตื่นเต้นไหม?"\nคุณ: "ก็ normal ที่จะ adjust สักพัก"\n\nTimeline ชัด แต่ connection ไม่เกิด',
        "why_fails": "SJ comfortable กับ facts ไม่ comfortable กับ feelings แต่ people connect ผ่าน feelings ไม่ใช่ timeline",
        "recommended_example": 'อีกฝ่าย: "เล่าเรื่อง job แรกให้ฟัง"\nคุณ: "ฉันจำได้ว่าวันแรกกลัวมากเลย ก็ pretend ว่า confident แต่ข้างในสั่นอยู่ตลอด [laugh] มีอยู่วันนึงที่ [memorable moment] ตอนนั้นนึกว่าจะ survive ไม่ได้แล้ว แต่สุดท้ายก็..."\nอีกฝ่าย: [lean in] "โห เล่าต่อ!"',
        "the_shift": "เพิ่ม 'ตอนนั้นฉันรู้สึก...' เข้าไปในทุก story — feelings เป็น part ที่ทำให้คนอยากฟังต่อ",
    },
    ("SP", "build_connection"): {
        "mbti_context": "SP เก่งการสร้าง fun shared experiences แต่ connection ที่ลึกต้องการ moments ที่ slow down และ go deep บ้าง ไม่ใช่แค่ next adventure ต่อไปเรื่อยๆ ต้องฝึก sit with someone ในความเงียบและในบทสนทนาที่หนักขึ้นบ้าง",
        "tension": "SP เติม space ด้วย activity และ fun แต่ connection ที่ลึกต้องการ stillness ที่ SP ไม่ comfortable กับ",
        "conflict_example": '[ทั้ง date เต็มไปด้วย activity]\nอีกฝ่าย: "บางทีอยากแค่นั่งคุยกันเฉยๆ นะ"\nคุณ: "โอ้ ก็ได้ แล้วไป [bar ใหม่] เลยไหม? มีดนตรีสดด้วย"\nอีกฝ่าย: "ฉัน mean นั่งคุยจริงๆ"\nคุณ: "อ๋อ... ก็ทำได้ แต่ที่นั่นก็ [keep moving]"\nอีกฝ่าย: [รู้สึกว่าคุณไม่ comfortable กับ stillness]\n\nFun มาก แต่ไม่มีโอกาส connect ในระดับที่ลึกกว่า',
        "why_fails": "SP เติม silence ด้วย activity เพราะ feel uncomfortable กับ stillness แต่ deep conversations เกิดใน moments ที่ slow down ไม่ใช่ moments ที่ rush ไปหา next thing",
        "recommended_example": 'คุณ: [plan date ที่มีทั้ง activity และ time ที่ quieter]\n"เดี๋ยวไปทำ [activity] ก่อน แล้วก็มา [chill spot] นั่งคุยกัน อยากได้ยินว่าช่วงนี้เป็นยังไงบ้าง"\nอีกฝ่าย: "โห คิดถึงการ plan นี้ไหม"\nคุณ: [ใน chill spot] ถาม genuine question แล้วฟังจริงๆ โดยไม่ check phone',
        "the_shift": "Plan time สำหรับ slow conversation เข้าไปใน date — มันไม่เกิดเองถ้าคุณไม่ make space สำหรับมัน",
    },

    # ═══════════════ deepen_trust ═══════════════
    ("NT", "deepen_trust"): {
        "mbti_context": "NT เชื่อว่า trust มาจาก reliability และ consistency ซึ่งถูก แต่ trust ที่ลึกยังต้องการ vulnerability ด้วย คนจะ trust คุณในระดับที่ลึกเมื่อพวกเขาเห็นว่าคุณก็เป็นมนุษย์ที่มีความกลัวและ uncertainty เหมือนกัน",
        "tension": "NT reliable มาก แต่ emotional invulnerability ทำให้อีกฝ่ายรู้สึกว่า trust flow แค่ทางเดียว",
        "conflict_example": 'อีกฝ่าย: [share สิ่งที่ตัวเองกลัว] "ฉันบอกเรื่องนี้ไม่ค่อยได้กับใครนะ"\nคุณ: "ฉัน appreciate ที่ share กัน มันฟังดู challenging"\nอีกฝ่าย: "คุณกลัวอะไรบ้าง?"\nคุณ: "ฉัน generally จัดการกับ challenges ได้ดี ไม่ค่อยมีสิ่งที่ทำให้กลัว"\nอีกฝ่าย: [รู้สึก disconnected] "โอ้... ok"\n\nอีกฝ่าย share vulnerability คุณ respond ด้วยความ invulnerable',
        "why_fails": "NT กลัวว่า showing weakness ทำให้ดูน่าเชื่อถือน้อยลง แต่มันทำให้ trust ลึกขึ้น — vulnerability คือ language ของ intimacy",
        "recommended_example": 'อีกฝ่าย: "คุณกลัวอะไรบ้าง?"\nคุณ: [pause] "จริงๆ ฉัน... กลัวว่าจะ disappoint คนที่ฉัน care เรื่องที่สำคัญ ไม่ค่อยพูดเรื่องนี้เหมือนกัน"\nอีกฝ่าย: [leaned in] "โห ฉันไม่รู้ว่าคุณ feel แบบนั้นด้วย"\nคุณ: "ก็บางครั้ง คุณล่ะ เป็นยังไงกับเรื่องที่เล่า?"',
        "the_shift": "Share ความกลัวหรือ uncertainty ที่ specific อย่างน้อยหนึ่งอย่าง ต่อ conversation — vulnerability สร้าง trust มากกว่า consistency",
    },
    ("NF", "deepen_trust"): {
        "mbti_context": "NF เปิดตัวเองได้เร็วมาก ซึ่งเป็น gift แต่บางทีแชร์สิ่งที่ลึกมากเร็วเกินไปจน อีกฝ่ายรู้สึก overwhelmed แล้วก็ pull back Trust ที่ลึกสร้างช้าๆ ทีละ layer ไม่ใช่ dump ทั้งหมดครั้งเดียว",
        "tension": "NF เปิดตัวเองทั้งหมดเร็วเกินไป ทำให้อีกฝ่าย overwhelmed และ pull back",
        "conflict_example": 'อีกฝ่าย: "เราคุยกันได้สนิทดีนะ"\nคุณ: "ใช่ ฉัน feel safe มากกับคุณ จริงๆ ฉัน... [เล่าสิ่งที่ deeply personal มาก]"\nอีกฝ่าย: "โอ้... [uncomfortable] ขอบคุณที่ share นะ"\nคุณ: "ฉันรู้สึก connected กับคุณมาก อยากรู้เรื่องนั้นของคุณบ้าง"\nอีกฝ่าย: [pull back] "เดี๋ยวค่อยเล่ากัน"\n\nคุณ genuine มาก แต่ pace เร็วเกินจน overwhelm',
        "why_fails": "NF interpret emotional safety ว่าคือ signal ให้เปิดทั้งหมด แต่ intimacy ต้องการ reciprocal pace — ถ้า share ล้ำหน้าอีกฝ่ายมากเกิน พวกเขา retreat",
        "recommended_example": 'คุณ: [share สิ่งที่ personal แต่ไม่ deepest] "จริงๆ เรื่องนี้ฉันไม่ค่อยบอกใครนะ" [share แล้วหยุด]\nอีกฝ่าย: [respond กลับ]\nคุณ: [ฟัง และ share อีกนิดต่อเมื่อ feel ว่า reciprocal]\n[ค่อยๆ deepen ตาม pace ของทั้งคู่]',
        "the_shift": "Share ทีละ layer และรอดูว่าอีกฝ่าย match ก่อน — intimacy เป็น dance ไม่ใช่ monologue",
    },
    ("SJ", "deepen_trust"): {
        "mbti_context": "SJ สร้าง trust ผ่าน actions ที่สม่ำเสมอได้ดีมาก แต่ trust ที่ลึกยังต้องการให้อีกฝ่ายรู้สึกว่าคุณ closed เป็นครั้งคราว ได้ยอมรับว่าไม่ ok บ้าง ได้เปิดส่วนที่ vulnerable ของตัวเอง",
        "tension": "SJ reliable มากแต่ closed เกิน — อีกฝ่ายรู้ว่า trust ได้ในเรื่อง consistency แต่ไม่รู้สึกว่า truly known",
        "conflict_example": '[หลัง difficult week]\nอีกฝ่าย: "ดูเหนื่อยๆ นะ ช่วงนี้เป็นยังไงบ้าง?"\nคุณ: "โอเค จัดการได้ ขอบคุณที่ถาม"\nอีกฝ่าย: "จริงๆ เป็นยังไง?"\nคุณ: "ก็มีหลายอย่าง แต่ manage ได้ ไม่ต้องเป็นห่วง"\nอีกฝ่าย: [รู้สึกว่า shut out] "โอ้ ok"\n\nคุณ protect อีกฝ่ายจาก burden แต่อีกฝ่ายรู้สึกว่า kept at distance',
        "why_fails": "SJ คิดว่า protect อีกฝ่ายจาก problems ของตัวเองคือการ care แต่อีกฝ่ายที่อยากรู้สึก trusted จะ interpret มันว่าถูก excluded",
        "recommended_example": '[หลัง difficult week]\nอีกฝ่าย: "ช่วงนี้เป็นยังไงบ้าง?"\nคุณ: "จริงๆ... หนักนิดนึง เรื่อง [X] มันไม่ง่ายเท่าที่คิด ปกติฉันไม่ค่อยพูดเรื่องแบบนี้ แต่ก็ดีที่มีคุณถาม"\nอีกฝ่าย: "เล่าให้ฟังได้เลยนะ"',
        "the_shift": "อนุญาตให้ตัวเองพูดว่า 'หนักนิดนึง' ได้ — มันไม่ใช่ burden มันคือ invitation ให้อีกฝ่าย show up สำหรับคุณ",
    },
    ("SP", "deepen_trust"): {
        "mbti_context": "SP trust คนเร็วในช่วงเวลาสด แต่บางที inconsistent ในเรื่องเล็กๆ ที่สะสมเป็น doubt Trust ไม่ได้สร้างจาก big gestures มันสร้างจาก small commitments ที่ keep ได้ทุกครั้ง",
        "tension": "SP trust building ใน big moments ดี แต่ inconsistent ใน small commitments ซึ่งค่อยๆ erode trust",
        "conflict_example": 'คุณ: "โอเค เจอกันวันศุกร์ 7 โมงเย็นนะ!"\n[วันศุกร์ 6.30]\nคุณ: "โทษที เพิ่งรู้ว่ามีเรื่อง push late เป็น 8 โมงได้ไหม?"\n[วันต่อๆ ไป เกิดแบบนี้อีก 3 ครั้ง]\nอีกฝ่าย: [เริ่มไม่แน่ใจว่า reliable จริงๆ ไหม]\n\nไม่ได้ bad intention แต่ small patterns สร้าง doubt',
        "why_fails": "SP ไม่ได้ตั้งใจ unreliable แต่ respond ต่อ immediate demands ได้เร็วกว่า honor prior commitments ซึ่งค่อยๆ สร้าง pattern ที่อีกฝ่าย trust น้อยลง",
        "recommended_example": 'คุณ: [ก่อน commit] "ฉัน plan วันศุกร์ไว้บ้างแล้ว ขอ check ก่อนนะ" [check จริงๆ]\n"โอเค 7 โมงได้" [set reminder ทันที]\n[ถ้ามี conflict เกิดขึ้น] บอกล่วงหน้า 24 ชั่วโมง ไม่ใช่ 30 นาทีก่อน\n[Protect commitment นี้จาก interruptions ที่ไม่ urgent]',
        "the_shift": "Over-commit น้อยลง under-deliver น้อยลง — trust มาจาก small promises ที่ keep ได้ทุกครั้ง",
    },

    # ═══════════════ define_relationship ═══════════════
    ("NT", "define_relationship"): {
        "mbti_context": "NT approach 'what are we?' conversation เหมือนการ negotiate contract มีข้อกำหนด criteria และต้องการ clarity ครบ ซึ่งฆ่า vibe และทำให้อีกฝ่ายรู้สึกว่ากำลัง sign terms of service ไม่ใช่ define ความสัมพันธ์",
        "tension": "NT frame DTR เหมือน negotiation มีข้อกำหนดชัดเจนจน อีกฝ่ายรู้สึกว่าถูก processed ไม่ใช่ loved",
        "conflict_example": 'คุณ: "อยากคุยเรื่อง status ของเราหน่อย ตอนนี้เราเป็นอะไรกัน?"\nอีกฝ่าย: "คือ..."\nคุณ: "ฉัน define ความสัมพันธ์ว่าควรมี exclusivity, regular contact, และ mutual goals ที่ aligned คุณ see มันแบบเดียวกันไหม?"\nอีกฝ่าย: [uncomfortable มาก] "โห... มันเหมือน job interview ไปหน่อยนะ"\n\nClarity ที่ถูกต้อง แต่ framing ผิด',
        "why_fails": "NT ต้องการ clarity ซึ่งเป็นสิ่งที่ดี แต่ delivery ที่เป็น structured discussion ทำให้ conversation รู้สึก formal และ unromantic ซึ่ง undermine ความรู้สึกที่อยู่เบื้องหลัง",
        "recommended_example": 'คุณ: [ในช่วงเวลาที่ natural และ connected] "บอกตรงๆ นะ ฉัน enjoy เวลาที่ได้คุยกับคุณมาก และอยาก know ว่าเราอยู่ในหน้าเดียวกันไหมเรื่องนี้"\nอีกฝ่าย: "ฉันก็ enjoy เหมือนกัน"\nคุณ: "ดีมาก ฉัน want ให้มัน exclusive สำหรับฉัน คุณรู้สึกยังไงกับเรื่องนั้น?"',
        "the_shift": "Share feeling ก่อน ask question — 'ฉัน feel X' นำไปสู่ honest conversation ที่ดีกว่า 'เราควร define X' เสมอ",
    },
    ("NF", "define_relationship"): {
        "mbti_context": "NF รู้สึกในใจชัดมากว่าต้องการอะไร แต่กลัว rejection จนเลือก drop hints แทนที่จะพูดตรงๆ ซึ่งทำให้อีกฝ่ายสับสนหรือไม่รู้เลย การพูดตรงๆ ว่าต้องการอะไรคือการ respect ตัวเองและอีกฝ่ายพร้อมกัน",
        "tension": "NF รู้ว่าต้องการอะไร แต่ hint แทน ask โดยตรง ทำให้อีกฝ่ายไม่รู้หรือสับสน",
        "conflict_example": 'คุณ: [social media post เกี่ยวกับ relationship goals]\nอีกฝ่าย: [ไม่ได้ notice]\nคุณ: "คิดไหมว่าคนที่คุยกันอยู่ควรจะ... official บ้าง?"\nอีกฝ่าย: "ก็ขึ้นอยู่กับสถานการณ์ไหม"\nคุณ: "ก็ใช่นะ แค่ hypothetical"\n[สามเดือนต่อมา ยังไม่ชัดเจน]\n\nคุณต้องการ define แต่ไม่เคย ask ตรงๆ',
        "why_fails": "NF hint เพราะกลัว rejection แต่ hints ที่ไม่ clear สร้าง ambiguity ที่ยิ่งน่ากลัวกว่า การรู้ answer จริงๆ ดีกว่าการ wonder อยู่นานๆ",
        "recommended_example": 'คุณ: [ในช่วงเวลาที่ connection ดี] "ฉันอยากพูดตรงๆ สักเรื่อง ฉัน enjoy เวลาที่ได้อยู่กับคุณมาก และอยากรู้ว่าคุณ see เราไปในทิศทางไหน"\nอีกฝ่าย: "ฉัน feel แบบเดียวกัน อยากให้ exclusive"\nคุณ: "ดีมากเลย ฉันก็ต้องการแบบนั้น"',
        "the_shift": "Fear of rejection ที่ยาวนาน มักเจ็บปวดกว่า rejection จริงๆ — พูดตรงๆ แล้วรู้เลย ดีกว่า wonder นานๆ",
    },
    ("SJ", "define_relationship"): {
        "mbti_context": "SJ อยากให้ทุกอย่าง official และชัดเจน ซึ่งดี แต่บางทีนำเรื่องนี้ขึ้นมา seriously เกินจนอีกฝ่ายรู้สึกกดดัน การ define ความสัมพันธ์ไม่จำเป็นต้องเป็น formal discussion สามารถเกิดขึ้นใน natural moment ได้",
        "tension": "SJ approach DTR อย่าง formal เกิน ทำให้ serious เกินความจำเป็นและ intimidate อีกฝ่าย",
        "conflict_example": 'คุณ: "ฉันอยากนัดคุยเรื่อง status ของความสัมพันธ์เราอย่างเป็นทางการ ว่างเย็นวันศุกร์ไหม?"\nอีกฝ่าย: "โอ้... [anxiety spike] เรื่องอะไร?\nคุณ: "อยากให้ชัดเจนเรื่องที่เราอยู่กัน"\nอีกฝ่าย: [spend วันศุกร์ทั้งวันเครียดว่าคืออะไร]\n[ในการ meeting — awkward มาก ทั้งสองฝ่าย defensive]\n\nIntent ดี แต่ framing สร้าง anxiety โดยไม่จำเป็น',
        "why_fails": "SJ ชอบ formal process แต่ relationship conversations ที่ work ที่สุดมักเกิดใน casual moments ไม่ใช่ scheduled meetings",
        "recommended_example": '[ระหว่าง casual nice moment]\nคุณ: "รู้อะไรไหม ฉัน like เวลาที่ได้อยู่กับคุณมาก อยากให้มัน official ระหว่างเรา คุณรู้สึกยังไง?"\nอีกฝ่าย: "ฉันก็ feel แบบนั้น"\nคุณ: "โอเค งั้นก็เป็น official แล้ว"',
        "the_shift": "ในช่วง natural moment ที่ดี พูดง่ายๆ — ไม่ต้องมี agenda setting หรือ formal meeting",
    },
    ("SP", "define_relationship"): {
        "mbti_context": "SP enjoy ความสัมพันธ์ใน present moment มากและ avoid การ define เพราะรู้สึกว่า label ทำให้ connection รู้สึก heavy ขึ้น แต่การไม่ define ทำให้อีกฝ่ายไม่แน่ใจ และ uncertainty ค่อยๆ erode connection",
        "tension": "SP avoid defining เพราะรู้สึกว่า label ทำให้ free น้อยลง แต่ ambiguity ค่อยๆ ทำให้อีกฝ่ายหาย",
        "conflict_example": '[คุยกันมา 3 เดือน]\nอีกฝ่าย: "เราเป็นอะไรกัน?"\nคุณ: "ก็... เราก็ enjoy กันอยู่นะ ต้องนิยามเหรอ?"\nอีกฝ่าย: "ฉัน need รู้ว่าเราอยู่ที่ไหน"\nคุณ: "อย่า overthink เลย เดี๋ยวก็รู้เอง"\nอีกฝ่าย: [รู้สึก dismisssed] "งั้นฉัน out ดีกว่า"\n\nคุณ lost คนที่ like เพราะ avoid conversation ที่ไม่ยากขนาดนั้น',
        "why_fails": "SP avoid labels เพราะ feel restrictive แต่อีกฝ่ายไม่ได้ต้องการ restrict เขาต้องการรู้สึกว่า safe และ chosen",
        "recommended_example": 'อีกฝ่าย: "เราเป็นอะไรกัน?"\nคุณ: "ฉัน like คุณมาก และ want ให้นี่เป็น exclusive ระหว่างเราสองคน มันตอบคำถามคุณได้ไหม?"\nอีกฝ่าย: "ได้ ฉัน want แบบเดียวกัน"\nคุณ: "โอเค งั้นก็โอเค"',
        "the_shift": "แทนที่จะ define ด้วย label พูดว่า 'ฉัน want ให้นี่เป็น X' — มันเป็น feeling statement ไม่ใช่ contract",
    },

    # ═══════════════ sustain_bond ═══════════════
    ("NT", "sustain_bond"): {
        "mbti_context": "NT มักหยุดลงทุนใน relationship หลังจากที่รู้สึกว่า 'established' แล้ว เหมือนกับว่า relationship solve แล้วก็ไม่ต้องทำอะไรอีก แต่ relationships ต้องการ ongoing investment ไม่ใช่แค่ initial effort",
        "tension": "NT treat relationship เหมือน problem ที่ solved แล้ว แต่จริงๆ ต้องการ continuous care",
        "conflict_example": '[relationship ผ่านมา 2 ปี]\nคู่รัก: "รู้สึกว่าช่วงนี้เราไม่ค่อย connect กันนะ"\nคุณ: "ก็เราไม่ได้ fight กันนะ ทุกอย่างก็ดี"\nคู่รัก: "ก็ใช่ แต่ฉัน miss เมื่อก่อน"\nคุณ: "เมื่อก่อน situation ต่างกัน ตอนนี้เราก็ stable ดีแล้วนะ"\nคู่รัก: "Stable ไม่ใช่ connection"\n\nคุณ solve relationship แล้วคิดว่าเสร็จ',
        "why_fails": "NT ใช้ energy เยอะตอน early stage แล้ว shift ไปที่ other priorities โดยคิดว่า relationship secure แล้ว แต่ connection ต้องการ ongoing attention ไม่ใช่ periodic maintenance",
        "recommended_example": 'คุณ: [schedule regular 1:1 time กับคู่รัก]\n"เย็นวันศุกร์ไม่มี screen เวลาของเราสองคน"\n[ใน time นั้น]\nคุณ: "สัปดาห์นี้มีอะไรที่ทำให้ excited หรือ happy ที่สุด?"\n[ฟัง share กลับ ทำ regularly ไม่ใช่เฉพาะตอน crisis]',
        "the_shift": "Schedule connection ไม่ใช่แค่ problem-solving — relationship ที่ดีต้องการ regular investment ไม่ใช่แค่ emergency repair",
    },
    ("NF", "sustain_bond"): {
        "mbti_context": "NF ให้มากกว่าที่รับในความสัมพันธ์และมักไม่บอกว่าตัวเองต้องการอะไร จนเริ่ม resent ความ imbalance ที่เขาสร้างขึ้นเอง การ sustain bond ต้องการการพูดว่าตัวเองต้องการอะไรด้วย ไม่ใช่แค่ give เรื่อยๆ",
        "tension": "NF ให้มากกว่ารับ และไม่บอก need ของตัวเองจน resentment เกิดขึ้นเงียบๆ",
        "conflict_example": '[ผ่านมา 1 ปี]\nคุณ: [เหนื่อยมาก แต่ยังให้อยู่ทุกอย่าง]\nคู่รัก: "คุณ OK ไหม?"\nคุณ: "โอเค ทุกอย่าง fine"\n[อีก 3 เดือน]\nคุณ: "จริงๆ ฉัน... ไม่โอเค มาได้สักพักแล้ว"\nคู่รัก: "ทำไมไม่บอกก่อน? ฉันจะช่วยได้นะ"\nคุณ: "กลัวจะ burden"\n\nคุณ care มาก แต่ไม่ยอมให้ตัวเองถูก cared for',
        "why_fails": "NF ปกป้องอีกฝ่ายจาก needs ของตัวเอง แต่การไม่ allow อีกฝ่ายให้ช่วยทำให้พวกเขา feel excluded และ relationship menjadi one-sided",
        "recommended_example": 'คุณ: [เมื่อรู้สึกว่าต้องการ support] "ฉันจะบอกตรงๆ นะ ช่วงนี้ฉัน struggling กับ [X] อยู่ ไม่ได้ต้องการ solution แค่อยากให้รู้ว่ามีคนที่ hear"\nคู่รัก: "บอกให้ฟัง ฉัน here"\n[ให้อีกฝ่าย show up สำหรับคุณบ้าง]',
        "the_shift": "Bond ที่ sustain ได้ต้องการ give และ receive — ให้อีกฝ่าย care คุณบ้าง มันไม่ใช่ burden มันคือ intimacy",
    },
    ("SJ", "sustain_bond"): {
        "mbti_context": "SJ สร้าง relationship routine ที่ดีมาก แต่ routine โดยไม่มี novelty ค่อยๆ ทำให้เบื่อ ต้องหาวิธีเพิ่ม unexpected elements เข้าไปใน routine ที่ reliable บ้าง",
        "tension": "SJ reliable routine ดีมาก แต่ predictability โดยไม่มี surprise ทำให้ connection รู้สึก stale",
        "conflict_example": '[routine ที่เหมือนกันทุกอาทิตย์]\nคู่รัก: "เราทำแบบเดิมทุกอาทิตย์เลยนะ"\nคุณ: "ก็เราชอบมันนี่ มันwork ดี"\nคู่รัก: "ใช่ แต่บางทีอยากลองอะไรใหม่ๆ บ้าง"\nคุณ: "แต่ทำไมต้องเปลี่ยนถ้ามันดีอยู่แล้ว?"\nคู่รัก: [รู้สึกว่า relationship ไม่ grow]\n\nStable มาก แต่ flat',
        "why_fails": "SJ optimize ให้ relationship ทำงานได้ดี แต่ relationships ต้องการ growth และ novelty ด้วย ไม่ใช่แค่ efficiency",
        "recommended_example": 'คุณ: [เซอร์ไพรส์ด้วย something unexpected เดือนละครั้ง]\n"เตรียม [new experience] ไว้ให้แล้วเย็นนี้ไม่ได้บอกก่อนนะ"\nคู่รัก: "โห ไม่คาดคิดเลย!"\n[หรือ] "เดือนนี้เราลองทำ [สิ่งใหม่] กันไหม? ฉัน research ไว้แล้ว"',
        "the_shift": "Plan surprise เล็กๆ เดือนละอย่าง — ให้ routine เป็น foundation แต่ add novelty เป็น ingredient ที่ทำให้ relationship มีชีวิต",
    },
    ("SP", "sustain_bond"): {
        "mbti_context": "SP ต้องการความ variety และ spontaneity ซึ่งทำให้ relationship exciting แต่ inconsistency ทำให้คู่รัก feel insecure ต้องหาสมดุลระหว่าง adventure และ stability ที่อีกฝ่ายต้องการเพื่อ feel safe",
        "tension": "SP ต้องการ variety มากจนบางครั้ง disrupt stability ที่คู่รัก need เพื่อ feel secure",
        "conflict_example": 'คู่รัก: "อยากให้เราวางแผนอนาคตด้วยกัน"\nคุณ: "ก็ดี แต่ฉัน don\'t like plan ไกลเกินไป ขอ flexible ไว้"\nคู่รัก: "แต่ฉัน need รู้ว่าเราอยู่ที่ไหนในอีก 1 ปี"\nคุณ: "ปีหน้ายังไกลมาก เดี๋ยวค่อยดูกัน"\nคู่รัก: "ฉัน can\'t build life กับคนที่ไม่ plan อะไรเลย"\n\nSP คิดว่า flexible = free แต่คู่รัก feel ว่า uncertain = unsafe',
        "why_fails": "SP interpret ความ commitment ว่าเป็นการ limit freedom แต่คู่รัก interpret มันว่าเป็น safety พวกเขาต้องการรู้ว่าคุณ choosing them consistently ไม่ใช่แค่ in the moment",
        "recommended_example": 'คุณ: "ฉันเข้าใจว่าคุณ need ความชัดเจนมากกว่าฉัน มาหาจุด middle ไหม ฉัน commit ในเรื่อง [X, Y] ที่สำคัญกับคุณ และมีพื้นที่ flexible ใน [Z] สำหรับฉัน คิดว่า work ได้ไหม?"\nคู่รัก: "ถ้าแบบนั้นก็ได้นะ"',
        "the_shift": "Commit ในเรื่องที่ matter ที่สุดกับอีกฝ่าย แล้วหา flexibility ใน areas อื่น — ไม่ต้องเปลี่ยน nature แค่ honor needs ของอีกฝ่ายในส่วนที่สำคัญ",
    },
}

HD_RELATIONSHIP: dict[tuple[str, str], str] = {

    # create_attraction
    ("Generator", "create_attraction"): "ทำสิ่งที่คุณ genuinely enjoy และ let people find you ใน flow ของมัน attraction ที่ genuine ที่สุดมาจากการเห็นใครบางคน fully alive ใน passion ของตัวเอง ไม่ต้อง try to attract แค่ be lit up",
    ("Manifesting Generator", "create_attraction"): "Energy ของคุณดึงดูดอยู่แล้วตอนที่คุณ in motion อย่าชะลอตัวเองเพื่อ appear more 'normal' — authenticity ของ MG ที่กำลัง doing many things ด้วย genuine excitement คือ magnetic มาก",
    ("Manifestor", "create_attraction"): "คุณ initiate ด้วยความ confidence ที่ natural ซึ่ง attractive มาก แต่หลังจาก initiate ให้ space สำหรับ response บ้าง อย่า steamroll — attraction ต้องการ dance ระหว่างสองคน",
    ("Projector", "create_attraction"): "คุณ attractive ที่สุดตอนที่ใครบางคนรู้สึกว่าถูก truly seen โดยคุณ ใช้ gift ในการ read คนเพื่อ notice สิ่งที่ unique ในอีกฝ่าย แล้ว reflect มันกลับไปให้เขา — คนไม่เคยลืมคนที่ทำให้พวกเขารู้สึกว่าถูก understood",
    ("Reflector", "create_attraction"): "คุณ reflect energy ของสภาพแวดล้อม — อยู่ใน environment ที่ดีและ authentic จะช่วยให้ best version ของคุณปรากฏ attraction เกิดเมื่อคุณอยู่ใน environment ที่ fit กับ who you are",

    # build_connection
    ("Generator", "build_connection"): "Connection เกิดตอนที่คุณ respond จาก genuine interest ในอีกฝ่าย ถ้า Sacral บอกว่าอยากรู้เรื่องนี้ของเขา follow นั้น — genuine curiosity สร้าง connection ที่ real กว่า calculated questions",
    ("Manifesting Generator", "build_connection"): "คุณ connect เร็วมาก แต่ make sure อีกฝ่ายรู้สึกว่าถูก heard ไม่ใช่แค่ processed อย่าข้ามไป topic ต่อไปเร็วเกินไป บางทีนั่งกับ single thing ที่เขาพูดนานขึ้น",
    ("Manifestor", "build_connection"): "Connection เกิดเมื่อ inform อีกฝ่ายด้วยสิ่งที่คุณ genuinely feel และ want บอกเขาว่าคุณ value connection นี้ตรงๆ ความ directness ของ Manifestor สร้าง intimacy ที่ unexpected",
    ("Projector", "build_connection"): "คุณ connect ลึกมากตอนที่ได้ focus กับ one person ที่ตอบรับ energy ของคุณ รอให้เขา open ก่อนแล้วค่อย guide deeper — อย่า force connection ให้เป็น natural unfolding",
    ("Reflector", "build_connection"): "คุณรับ energy ของอีกฝ่ายได้ลึกมาก แต่ต้อง protect ตัวเองจาก absorbing สิ่งที่ไม่ใช่ของคุณ connection ที่ดีเกิดกับคนที่ make คุณรู้สึก better ไม่ใช่ drained",

    # deepen_trust
    ("Generator", "deepen_trust"): "Trust ลึกขึ้นเมื่อคุณ honor Sacral response ของตัวเองและ communicate มันตรงๆ ถ้า gut บอกว่า not ok บอกอีกฝ่ายแทนที่จะ suppress ความ honest ใน needs สร้าง trust มากกว่า perfect behavior",
    ("Manifesting Generator", "deepen_trust"): "Inform อีกฝ่ายก่อน pivot เสมอ ทั้งใน life decisions และใน relationship ความรู้สึกว่า 'จะไม่โดน surprise' คือ foundation ของ trust สำหรับ MG relationship",
    ("Manifestor", "deepen_trust"): "Trust เกิดเมื่อ inform ก่อน move ในทุกสิ่งที่ affect อีกฝ่าย อีกฝ่ายจะ trust คุณแม้ไม่เห็นด้วยกับ decision เมื่อพวกเขา feel ว่า loop-in อยู่เสมอ",
    ("Projector", "deepen_trust"): "Trust ลึกขึ้นเมื่อคุณ share insight ของคุณตอนที่ถูกถาม และ honor ตัวเองพอที่จะ say no เมื่อ energy ไม่มี อีกฝ่ายจะ trust คุณมากขึ้นเมื่อเห็นว่าคุณ know ตัวเองดี",
    ("Reflector", "deepen_trust"): "Trust ลึกขึ้นเมื่อคุณ communicate ว่า need time สำหรับ major decisions และอีกฝ่าย understand ว่า process ของคุณคืออะไร ความ transparency เกี่ยวกับ how คุณ work สร้าง trust",

    # define_relationship
    ("Generator", "define_relationship"): "ถาม Sacral ก่อนว่า 'ใช่' กับ commitment นี้จริงๆ ไหม ถ้าใช่ บอกตรงๆ ด้วยความ genuine enthusiasm นั้น ถ้าไม่ใช่ honest answer เป็นสิ่งที่ kind กว่าในระยะยาว",
    ("Manifesting Generator", "define_relationship"): "ตอนที่ decide ที่จะ define บอกอีกฝ่ายชัดๆ ว่าคุณ want อะไร แล้ว move ไปเลย MG ไม่ต้อง build up ยาวๆ แค่ informed decision + clear communication",
    ("Manifestor", "define_relationship"): "บอกตรงๆ ว่าคุณ want อะไร ไม่ต้องรอให้อีกฝ่าย bring it up Manifestor initiation ใน relationship conversations สร้าง clarity ที่ทั้งคู่ deserve",
    ("Projector", "define_relationship"): "รอให้มีช่วงที่อีกฝ่าย open และ invite conversation ก่อน DTR conversation ที่ถูก timing จะ smooth กว่ามาก ถ้า force timing มัน rarely goes well",
    ("Reflector", "define_relationship"): "ให้เวลาตัวเองเพียงพอก่อน commit อย่าถูก pressure ให้ decide เร็วกว่าที่ feel ready ถ้า need time บอกอีกฝ่ายตรงๆ ว่าทำไม",

    # sustain_bond
    ("Generator", "sustain_bond"): "ทำ activities ด้วยกันที่คุณ both genuinely lit up ไม่ใช่แค่ obligation relationship sustain ได้เมื่อทั้งคู่ bring genuine energy มา ถ้า something รู้สึกว่า drained ให้ address มันก่อนที่มันจะสะสม",
    ("Manifesting Generator", "sustain_bond"): "Inform อีกฝ่ายเมื่อ life changes หรือ direction shifts ก่อนที่มันจะ affect relationship Long-term bond ของ MG sustain ได้เมื่ออีกฝ่ายรู้สึกว่า always in the loop ไม่ใช่ always catching up",
    ("Manifestor", "sustain_bond"): "Inform อีกฝ่ายเกี่ยวกับ life direction ของคุณ regularly ไม่ใช่แค่เมื่อมี major decision Long-term bond ต้องการให้อีกฝ่าย feel ว่าเป็นส่วนหนึ่งของ life ของคุณ ไม่ใช่แค่ recipient ของ updates",
    ("Projector", "sustain_bond"): "Long-term bond sustain ได้เมื่อคุณ feel recognized และ appreciated ถ้ารู้สึกว่า contribution ไม่ถูก seen ให้ communicate มันก่อนที่จะ withdraw อีกฝ่ายอาจไม่รู้ว่า recognition สำคัญขนาดไหนสำหรับคุณ",
    ("Reflector", "sustain_bond"): "Bond sustain ได้เมื่อ environment ของความสัมพันธ์ healthy ถ้า relationship environment รู้สึก toxic หรือ heavy trust นั้น — Reflector absorbs สิ่งเหล่านั้น และมันจะ show ใน wellbeing ของคุณ",
}
