"""Work sub-goal specific personality content — Thai Gen Z style."""

MBTI_WORK: dict[tuple[str, str], dict] = {

    # ═══════════════ get_buyin ═══════════════
    ("NT", "get_buyin"): {
        "mbti_context": "NT เตรียม data มาแน่นมาก แต่ลืมว่าคนส่วนใหญ่ตัดสินใจด้วยความรู้สึกก่อน แล้วค่อย rationalize ทีหลัง ก่อน pitch ต้องรู้ก่อนว่าเขา care อะไร แล้วเชื่อม case เข้ากับสิ่งนั้น ไม่ใช่แค่ dump ตัวเลขลงไป",
        "tension": "NT เตรียม case ครบ แต่ข้าม step validate concern ของอีกฝ่ายก่อน",
        "conflict_example": 'คุณ: "ดูตัวเลขพวกนี้ — ประสิทธิภาพเพิ่ม 40% ROI คืนทุน 8 เดือน ชัดมาก"\nอีกฝ่าย: "ขอคิดดูก่อนนะ"\nคุณ: "คิดอะไรอีก? ตัวเลขชัดอยู่แล้ว"\nอีกฝ่าย: "มีหลายอย่างต้องพิจารณา"\nคุณ: "อย่างเช่น?"\nอีกฝ่าย: [อึดอัด] "เดี๋ยวดูก่อน"\n\nเขาไม่ได้สงสัยตัวเลข เขากังวลเรื่องภาระทีม แต่คุณไม่ได้ถามเลย',
        "why_fails": "NT assume ว่าถ้า logic ดี คนจะ buy-in อัตโนมัติ แต่ buy-in เป็นเรื่องว่า concern ของเขาถูก hear ไหม ตัวเลขดีแค่ไหนก็ตาม",
        "recommended_example": 'คุณ: "ก่อนแชร์ข้อมูล ขอถามก่อนว่า ถ้าไม่ move forward กับ idea นี้ เหตุผลหลักจะเป็นเรื่องอะไร?"\nอีกฝ่าย: "ทีมเหนื่อยมาก เปลี่ยนอะไรใหม่ตอนนี้ยาก"\nคุณ: "เข้าใจมาก สิ่งที่ฉันมาคือทำให้ภาระเบาลง ไม่ใช่เพิ่ม ขอแสดงให้ดูได้ไหม?"\nอีกฝ่าย: "ถ้าแบบนั้นก็ฟังได้"',
        "the_shift": "ฟัง concern ก่อน แล้วค่อย present ที่ address concern นั้นโดยตรง — เปลี่ยน sequence นี้แล้ว buy-rate จะขึ้น",
    },
    ("NF", "get_buyin"): {
        "mbti_context": "NF build rapport ได้ดีมาก แต่มักไม่กล้า make the ask ชัดๆ จนหลุด window คุณต้องเชื่อว่า idea ของคุณมีคุณค่าพอที่จะขอ yes ได้ การ ask ชัดๆ ไม่ใช่การ push มันคือการเคารพเวลาของเขา",
        "tension": "NF สร้าง connection ดีมาก แต่กลัว push จนไม่ยอม make the clear ask",
        "conflict_example": 'คุณ: "ฉันชอบ project นี้มาก คิดว่า impact ได้จริงเลย"\nอีกฝ่าย: "ใช่ ฟัง interesting นะ"\nคุณ: "ดีใจมากที่คิดแบบนี้ ถ้ามีโอกาสก็น่าลองนะ"\nอีกฝ่าย: "ใช่ เดี๋ยวดูก่อน"\n[จบ meeting โดยไม่มี commitment]\n\nคุณ build rapport ดีมาก แต่ไม่เคย ask ชัดๆ เขาก็เลยไม่มีอะไรต้องตอบ',
        "why_fails": "NF กลัว push มากจน avoid making the clear ask สิ่งที่คุณมองว่าสุภาพ อีกฝ่ายมองว่าคุณไม่ได้ต้องการ yes จริงๆ",
        "recommended_example": 'คุณ: [หลัง build rapport] "ฉันเชื่อใน project นี้จริงๆ และ ready จะ run มัน สิ่งที่ต้องการตอนนี้คือไฟเขียวจากคุณ คุณ comfortable กับการ move forward ไหม?"\nอีกฝ่าย: "มีอะไรอยากรู้ก่อนไหม?"\nคุณ: "ถามมาเลย ฉัน happy ที่จะตอบ"',
        "the_shift": "คุณให้ care แล้ว ตอนนี้ให้ clarity ด้วย — การ ask ชัดๆ เป็นการเคารพเวลาของอีกฝ่าย ไม่ใช่การ push",
    },
    ("SJ", "get_buyin"): {
        "mbti_context": "SJ มาพร้อม documentation และ precedent ที่แน่น แต่มักพลาดตรงที่ไม่รู้ว่าอีกฝ่าย block อยู่เรื่องอะไรจริงๆ ก่อน present solution ต้องถาม real blocker ก่อน แล้วเชื่อม answer เข้ากับ concern นั้นโดยตรง",
        "tension": "SJ present solutions ครบทุกด้าน แต่พลาด hidden concern ที่อีกฝ่ายไม่ได้พูดออกมา",
        "conflict_example": 'คุณ: "วิธีนี้ใช้มาสำเร็จแล้ว นี่คือ documentation ครบ พร้อม timeline"\nอีกฝ่าย: "แต่ project เราต่างกัน"\nคุณ: "โครงสร้างเหมือนกัน แค่ scale ต่าง"\nอีกฝ่าย: "ต้อง check budget ก่อน"\nคุณ: "Budget มี ฉัน prepared ไว้แล้ว"\nอีกฝ่าย: "ขอคิดดูก่อนนะ"\n\nคุณตอบทุก objection แต่ concern จริงๆ คือ team adoption ซึ่งยังไม่ได้พูดถึงเลย',
        "why_fails": "SJ focus ที่การ present ครบถ้วน แต่ real blocker มักเป็น unstated concern ที่ต้องถาม ไม่ใช่ตอบ",
        "recommended_example": 'คุณ: "ก่อน walk through plan ขอถามก่อนว่า ถ้าจะไม่ move forward กับ project นี้ เหตุผลหลักจะเป็นเรื่องอะไร?"\nอีกฝ่าย: "จริงๆ กังวลว่าทีมจะ adopt ได้ไหม"\nคุณ: "ขอบคุณที่บอก นั่นแหละที่ฉันอยากจะ address โดยตรง นี่คือ adoption plan ที่เตรียมไว้..."',
        "the_shift": "ถาม real blocker ก่อน แล้วค่อย present ที่ตรงจุดนั้น — ไม่ใช่ present ทุกอย่างแล้วหวังว่ามันจะโดน",
    },
    ("SP", "get_buyin"): {
        "mbti_context": "SP เก่งการ read ห้องและ improvise แต่มักเข้า meeting โดยไม่ได้ setup context ก่อน คนจะฟัง pitch เมื่อรู้ว่ามันเกี่ยวกับ problem ของพวกเขา ไม่ใช่ idea ของคุณ",
        "tension": "SP เชื่อว่า energy และ idea ดีพอ แต่ buy-in ต้องการ setup ที่ทำให้เขาเห็น relevance ก่อน",
        "conflict_example": 'คุณ: [เจอในห้องประชุม] "เฮ้ มีไอเดียดีๆ อยากแชร์ คุยไหม?"\nอีกฝ่าย: "โอเค... ว่าอะไร?"\nคุณ: [เล่า idea สดๆ]\nอีกฝ่าย: "ฟัง interesting นะ แต่ต้อง check กับทีมก่อน"\nคุณ: "Check อะไร? ดีชัดๆ เลย"\nอีกฝ่าย: "ก็ต้อง align กันก่อน..."\n\nคุณ pitch ดี แต่ไม่ได้ build context ว่าทำไมมันสำคัญสำหรับเขาโดยเฉพาะ',
        "why_fails": "SP มักข้าม setup phase แล้วกระโดดเข้า pitch เลย แต่คนต้องรู้ว่า 'ทำไมฉันควรฟัง' ก่อน ถึงจะ evaluate ได้",
        "recommended_example": '[ส่ง message ล่วงหน้า]\nคุณ: "มีเรื่องอยากคุยที่น่าจะ solve [pain ที่เขากังวล] ได้ ขอ 15 นาทีได้ไหม?"\n[ใน meeting]\nคุณ: "ฉันรู้ว่าตอนนี้ [pain point] เป็นเรื่องสำคัญ ฉันเจอ approach ที่น่าจะ address ได้โดยตรง"\nอีกฝ่าย: "เล่าให้ฟัง"',
        "the_shift": "เปลี่ยน opening จาก 'ฉันมีไอเดีย' เป็น 'ฉันเจอวิธีที่จะ solve [เรื่องที่คุณกังวล]' — frame ต่าง ผลต่าง",
    },

    # ═══════════════ build_trust_work ═══════════════
    ("NT", "build_trust_work"): {
        "mbti_context": "NT แสดง competence ได้ดีมาก แต่ trust ที่ลึกต้องการอะไรมากกว่านั้น มันต้องการให้คนเห็นว่าคุณเป็นมนุษย์ด้วย ไม่ใช่แค่เครื่องคิดเลข บางทีการยอมรับว่าไม่รู้หรือพลาดไป สร้าง trust ได้มากกว่าการ defend ทุกอย่าง",
        "tension": "NT แสดง competence สูง แต่ขาด human moments ที่ทำให้คนรู้สึกว่าคุณ safe ที่จะ rely on",
        "conflict_example": 'เพื่อนร่วมงาน: "คิดว่า approach นี้จะ work ไหม?"\nคุณ: "Work แน่นอน ฉันวิเคราะห์แล้ว ตัวเลขรองรับ"\nเพื่อนร่วมงาน: "แต่มีความเสี่ยงตรงนั้นนะ"\nคุณ: "ฉันคิดถึงแล้ว ไม่ใช่ปัญหา"\nเพื่อนร่วมงาน: [นิ่ง ไม่ค่อย share อีก]\n\nเขาไม่ได้ไม่เชื่อ competence คุณ เขาแค่รู้สึกว่าคุยกับคุณแล้วความเห็นเขาไม่ค่อย matter',
        "why_fails": "NT defend ทุก position เต็มที่จนคนรู้สึกว่า input ของเขาไม่มีผล แล้วก็หยุด engage ความไว้วางใจไม่ได้มาจาก being always right แต่จากการทำให้คนรู้สึกว่าพวกเขามี voice",
        "recommended_example": 'เพื่อนร่วมงาน: "คิดว่า approach นี้จะ work ไหม?"\nคุณ: "ฉันเชื่อว่า work แต่ส่วนที่ยังไม่แน่ใจ 100% คือตรงนั้น คุณเห็นความเสี่ยงตรงไหนบ้าง?"\nเพื่อนร่วมงาน: "ตรงที่ X อาจเป็นปัญหา"\nคุณ: "นั่นเป็นจุดที่ดีมาก ต้องคิดเรื่องนั้นด้วย"',
        "the_shift": "ยอมรับ uncertainty บางส่วนไม่ได้ทำให้คุณดูอ่อนแอ มันทำให้คนรู้สึกว่า safe ที่จะ think alongside คุณ",
    },
    ("NF", "build_trust_work"): {
        "mbti_context": "NF ให้ความห่วงใยมาก แต่ถ้าให้มากโดยไม่มีขอบเขต คนจะ take for granted และ respect ลดลง Trust จากการทำงานต้องการทั้ง warmth และ reliability พร้อมกัน ต้องทำตามที่พูดไว้อย่างสม่ำเสมอ",
        "tension": "NF ให้มากเกิน จน boundary ไม่ชัด คนเริ่มรู้สึกว่าจะ rely on ได้แค่ไหนกันแน่",
        "conflict_example": 'เพื่อนร่วมงาน: "ช่วย review งานให้หน่อยได้ไหม?"\nคุณ: "ได้เลย ส่งมา" [รับงานชิ้นที่ 5 ของสัปดาห์]\n[ส่ง feedback ล่าช้าเพราะ overloaded]\nเพื่อนร่วมงาน: "ได้ feedback แล้วยัง?"\nคุณ: "โทษที ยุ่งมาก เดี๋ยวส่งให้"\n[สัปดาห์ต่อมา — เพื่อนร่วมงานไม่ ask อีก ไป ask คนอื่นแทน]\n\nคุณเป็น nice แต่ไม่ reliable พอที่จะ trust ในสิ่งสำคัญ',
        "why_fails": "NF รับปากเยอะเพราะไม่อยากปฏิเสธ แต่ over-commit แล้ว under-deliver ทำลาย trust มากกว่าการบอกตรงๆ ว่ารับไม่ได้",
        "recommended_example": 'เพื่อนร่วมงาน: "ช่วย review งานให้หน่อยได้ไหม?"\nคุณ: "ได้ แต่ตอนนี้ยุ่งอยู่ ส่งมาได้เลย แต่ฉันจะ review ได้พุธนะ ถ้า deadline คุณรอได้ก็โอเค ถ้าต้องการเร็วกว่านั้นลอง [ชื่อคนอื่น] ได้นะ"\nเพื่อนร่วมงาน: "พุธได้เลย ขอบคุณ"',
        "the_shift": "Commit น้อยลง deliver ครบทุกครั้ง — นั่นคือ trust จริงๆ ไม่ใช่การพยักหน้าทุกครั้ง",
    },
    ("SJ", "build_trust_work"): {
        "mbti_context": "SJ เป็นคนที่น่าเชื่อถือมาก deliver ตรงเวลาเสมอ แต่บางทีรู้สึก 'professional เกินไป' จนคนรู้สึก distance Trust ที่ลึกต้องการ moments ที่คุณแสดงความเป็นมนุษย์บ้าง ไม่ใช่แค่ process ที่ดีตลอด",
        "tension": "SJ reliable มาก แต่ closed เกินจน relationship ไม่ไป beyond transactional",
        "conflict_example": '[ประชุมทีม หลัง project สำเร็จ]\nเพื่อนร่วมงาน: "project นี้ยากมากเลยนะ คุณรู้สึกยังไงบ้าง?"\nคุณ: "ทุกอย่าง on track ตาม plan ที่วางไว้"\nเพื่อนร่วมงาน: "เออ แต่... ส่วนตัวล่ะ?"\nคุณ: "ก็ทำงานให้ดีที่สุด ผลออกมาดี"\nเพื่อนร่วมงาน: [หมดอยากคุย]\n\nทุกคน respect คุณ แต่ไม่ค่อยมีใคร feel ว่า know จริงๆ',
        "why_fails": "SJ ปกป้องตัวเองด้วยความ professional ตลอดเวลา แต่ trust ที่ลึกต้องการ vulnerability บ้าง คนจะ trust คนที่พวกเขา feel ว่า know ไม่ใช่แค่คนที่ deliver ครบ",
        "recommended_example": 'เพื่อนร่วมงาน: "project นี้ยากมากเลยนะ คุณรู้สึกยังไงบ้าง?"\nคุณ: "จริงๆ ช่วง week 3 นั้นหนักมาก ฉัน stress เรื่อง deadline เหมือนกัน แต่ดีใจที่ทีมช่วยกันผ่านมาได้"\nเพื่อนร่วมงาน: "เออ ฉันก็ stress มากเลย ดีใจที่คุณ feel แบบเดียวกัน"',
        "the_shift": "Share ความรู้สึกจริงๆ บางครั้งไม่ได้ทำให้คุณดูอ่อนแอ มันทำให้คนรู้สึกว่า connect ได้ และ trust ลึกขึ้น",
    },
    ("SP", "build_trust_work"): {
        "mbti_context": "SP สร้าง connection ได้ดีในช่วงเวลานั้นมาก แต่ trust ในการทำงานสร้างจาก consistency ของ small actions ไม่ใช่ big moments ถ้า follow through เล็กๆ ไม่สม่ำเสมอ คนจะ hesitate ที่จะ depend on คุณในสิ่งสำคัญ",
        "tension": "SP เก่งในช่วงเวลาสด แต่ inconsistent follow-through ทำให้คนไม่แน่ใจว่าจะ rely on ได้ไหม",
        "conflict_example": 'คุณ: [ใน meeting] "โอเค ฉันจะส่งข้อมูลนั้นให้ภายในพรุ่งนี้เลย"\n[วันรุ่งขึ้น — ลืม เพราะเจอ task ใหม่ที่ exciting กว่า]\nเพื่อนร่วมงาน: "ข้อมูลที่บอกว่าจะส่งล่ะ?"\nคุณ: "โอ้โห โทษที ลืมไปเลย เดี๋ยวส่งให้เร็วๆ นี้"\n[เกิดแบบนี้ 3 ครั้ง]\n\nคนชอบคุณ แต่ไม่ assign งานสำคัญให้แล้ว',
        "why_fails": "SP ตอบรับสิ่งใหม่ด้วยความ genuine แต่ attention ไปที่ next thing ไวมาก ทำให้ commitment เล็กๆ หลุดบ่อย และมัน compound เป็น 'ไม่น่าเชื่อถือ' ในสายตาคนอื่น",
        "recommended_example": 'คุณ: "โอเค ฉันจะส่งข้อมูลนั้นให้" [pause] [จดลงมือถือทันที] "โอเค set reminder ไว้แล้ว จะส่งพรุ่งนี้ก่อน 12.00 น."\n[ส่งตรงเวลา]\nเพื่อนร่วมงาน: [เริ่ม assign งานสำคัญให้มากขึ้น]',
        "the_shift": "จดทันทีที่ commit ไม่ใช่หลังจากนั้น ระบบเล็กๆ นี้ทำให้ trust สะสมได้โดยไม่ต้องเปลี่ยน personality",
    },

    # ═══════════════ secure_agreement ═══════════════
    ("NT", "secure_agreement"): {
        "mbti_context": "NT มักวิเคราะห์ต่อหลังจากที่ควรจะ close แล้ว เมื่อ signals บอกว่าอีกฝ่าย ready ต้อง ask ชัดๆ ไม่ใช่เปิด discussion ใหม่ การ over-analyze หลัง buying signal คือการ talk yourself out of a yes",
        "tension": "NT keep presenting แม้อีกฝ่าย ready แล้ว เพราะไม่แน่ใจว่า case ครบหรือยัง",
        "conflict_example": 'อีกฝ่าย: "ฟังแล้วน่าสนใจมากเลย"\nคุณ: "ดีมาก แล้วก็ยังมีอีก factor หนึ่งที่อยากให้รู้คือ..."\nอีกฝ่าย: "จริงๆ ตอนนี้พร้อม move forward แล้ว"\nคุณ: "โอเค แต่ก่อนอื่น ขอ clarify เรื่อง timeline ก่อนนะ..."\n[อีกฝ่ายเริ่ม cool down]\n\nเขา ready แล้ว แต่คุณยังไม่ยอม close',
        "why_fails": "NT กลัว commitment ที่ไม่ complete ทำให้ keep adding information แม้อีกฝ่าย already convinced ทำให้ momentum หาย",
        "recommended_example": 'อีกฝ่าย: "ฟังแล้วน่าสนใจมากเลย"\nคุณ: "ดีมาก คุณ comfortable enough ที่จะ move forward เลยไหม หรือยังมีอะไรที่ต้องการรู้ก่อน?"\nอีกฝ่าย: "ไม่มี ready เลย"\nคุณ: "ดีมาก งั้น step ต่อไปคือ [X] ทำได้เลยไหม?"',
        "the_shift": "ตอนเห็น buying signal หยุด present และ ask ทันที — จะ present ต่อก็ต่อเมื่อเขา ask คุณ",
    },
    ("NF", "secure_agreement"): {
        "mbti_context": "NF กลัวการ pressure อีกฝ่ายมาก จนได้ soft yes แล้วก็ไม่กล้า nail down ผลคือ agreement ค่อยๆ ระเหยไปหลัง meeting Agreement ที่แท้จริงต้องการ specifics ไม่ใช่แค่ good vibes",
        "tension": "NF ได้ yes แล้วแต่กลัว push เพื่อ lock down specifics จน agreement ไม่ solidify",
        "conflict_example": 'อีกฝ่าย: "ใช่ ฟังดู ok นะ ลองคุยกันต่อได้"\nคุณ: "ดีมาก ขอบคุณที่ open-minded มากเลย"\nอีกฝ่าย: "เดี๋ยว reach out ไปนะ"\nคุณ: "ได้เลย ขอบคุณมากๆ"\n[สองอาทิตย์ผ่านไป ไม่มีการ reach out]\n\nคุณได้ warm yes แต่ไม่ได้ next step ที่ชัด มันเลยไปไม่ต่อ',
        "why_fails": "NF interpret good energy ว่าคือ commitment แต่ 'เดี๋ยวคุยกัน' ไม่ใช่ agreement มันคือ polite non-commitment",
        "recommended_example": 'อีกฝ่าย: "ใช่ ลองคุยกันต่อได้"\nคุณ: "ดีมาก อยากให้ concrete มากขึ้นหน่อยนะ สัปดาห์หน้าวันไหนสะดวก 30 นาที? ฉันจะ send invite เลย"\nอีกฝ่าย: "วันพุธ 10 โมงได้"\nคุณ: "โอเค จะ send ให้เลยนะ"',
        "the_shift": "ก่อนจบ meeting ทุกครั้ง ต้องมี next step ที่ชัด — ใคร ทำอะไร เมื่อไหร่ ถ้าไม่มี ก็ยังไม่มี agreement",
    },
    ("SJ", "secure_agreement"): {
        "mbti_context": "SJ อยากให้ทุกอย่างเป็น formal และ documented เร็ว แต่บางทีอีกฝ่าย need เวลา feel comfortable ก่อน ถ้า push paperwork ก่อน emotional close จะเจอ resistance ที่ไม่จำเป็น",
        "tension": "SJ รีบ formalize ก่อนที่อีกฝ่ายจะ feel fully committed ทาง emotional",
        "conflict_example": 'อีกฝ่าย: "ฉัน interested ใน proposal นี้"\nคุณ: "ดีมาก ฉัน prepare contract ไว้แล้ว เซ็นได้เลยไหม?"\nอีกฝ่าย: [surprised] "โอ้... เร็วหน่อยนะ"\nคุณ: "ก็ทุกอย่าง agree กันแล้ว ก็ sign ได้เลย"\nอีกฝ่าย: "ขอคิดดูก่อนนะ"\n\nเขา interested แต่รู้สึกถูก rush ก็เลย pull back',
        "why_fails": "SJ เห็นว่า decision มาแล้วก็อยากทำให้ official ทันที แต่คนต้อง feel ว่าตัวเองตัดสินใจด้วยตัวเอง ไม่ใช่ถูก process บังคับ",
        "recommended_example": 'อีกฝ่าย: "ฉัน interested ใน proposal นี้"\nคุณ: "ดีมากเลย มีอะไรที่ยังอยากให้ชัดขึ้นก่อนที่เราจะ move forward ไหม?"\nอีกฝ่าย: "ไม่มี ฉัน comfortable แล้ว"\nคุณ: "โอเค งั้น step ต่อไปที่ง่ายที่สุดคือ... คุณ OK กับ step นั้นไหม?"',
        "the_shift": "Confirm ความรู้สึกก่อน paperwork — 'คุณ comfortable แล้ว?' ต้องได้ยินก่อนเสมอ",
    },
    ("SP", "secure_agreement"): {
        "mbti_context": "SP close ได้ดีมากในช่วงเวลาสด แต่มักออกจาก meeting โดยไม่ได้ lock down specifics เพราะ moment รู้สึกดีแล้ว ผลคือ verbal yes ที่ไม่มีโครงสร้าง รองรับ แล้วก็ระเหยไปเอง",
        "tension": "SP ได้ yes ในช่วงเวลาสด แต่ไม่ได้ nail down details ก่อนออกไป",
        "conflict_example": 'อีกฝ่าย: "โอเค ฉันสนใจ ลองไปต่อดูนะ"\nคุณ: "ดีมาก! แล้วจะคุยกันต่อนะ"\nอีกฝ่าย: "ได้เลย"\n[ทั้งคู่ออกจาก meeting ด้วย good energy แต่ไม่มี next step]\n[สัปดาห์ต่อมา — momentum หายไปหมดแล้ว]\n\nคุณได้ yes ในช่วงเวลาสด แต่ไม่มีโครงสร้างรองรับมัน',
        "why_fails": "SP ไว้วางใจใน energy ของ moment แต่ agreement ต้องการโครงสร้าง ไม่ใช่แค่ vibe ที่ดี",
        "recommended_example": 'อีกฝ่าย: "โอเค ฉันสนใจ"\nคุณ: "ดีมาก เพื่อให้ต่อจากนี้ง่ายขึ้น ขอ clarify สองอย่างก่อนเราแยกกัน — [X] และ [Y] เราเห็นตรงกันไหม?"\nอีกฝ่าย: "ใช่ เห็นด้วย"\nคุณ: "โอเค ฉัน send summary ให้ภายในวันนี้ แล้วเราเริ่มจาก [next action] ได้เลย"',
        "the_shift": "ก่อนออกจาก meeting ทุกครั้ง ถาม 'ขอ confirm สองอย่างก่อน' — สองนาทีนี้ทำให้ yes ไม่หาย",
    },

    # ═══════════════ drive_urgency ═══════════════
    ("NT", "drive_urgency"): {
        "mbti_context": "NT สร้าง logical urgency ได้ดีมาก แต่บางทีมันฟัง 'fabricated' เพราะขาด emotional weight คนตอบสนองต่อ urgency เมื่อมันเกี่ยวกับ loss ที่พวกเขา feel ได้จริงๆ ไม่ใช่แค่ตัวเลขที่จะพลาดไป",
        "tension": "NT frame urgency ด้วย logic แต่ urgency ที่ work ต้องการ emotional connection กับสิ่งที่เขาจะเสีย",
        "conflict_example": 'คุณ: "ถ้าไม่ decide ภายในสัปดาห์นี้ window ปิดในวันศุกร์"\nอีกฝ่าย: "ก็สร้าง deadline ใหม่ได้นะ"\nคุณ: "ราคาจะขึ้น 20% หลังจากนั้น"\nอีกฝ่าย: "ก็ 20% ไม่ใช่โลกแตก"\nคุณ: "ก็แต่... ประสิทธิภาพที่เสียไปทุกอาทิตย์..."\nอีกฝ่าย: "เดี๋ยวค่อยดู"\n\nUrgency ของคุณเป็นข้อมูล ไม่ใช่ pressure ที่เขา feel',
        "why_fails": "NT present urgency เป็น facts แต่ facts ไม่ move คน emotion ที่เชื่อมกับ cost จริงๆ ต่างหากที่ move",
        "recommended_example": 'คุณ: "ฉันอยากให้คุณคิดถึงสิ่งนี้ — ทุกอาทิตย์ที่เราไม่ได้ start คือทีมคุณยังแบกภาระ [X] อยู่ต่อ คุณบอกว่า [X] เป็นเรื่องที่ stress ทีมมากที่สุด deadline ของฉันคือปลายสัปดาห์นี้ แต่ decision เป็นของคุณ ฉันแค่อยากให้รู้ว่า cost ของการรอคืออะไร"\nอีกฝ่าย: "ถ้าแบบนั้นรีบ move เลยดีกว่า"',
        "the_shift": "เชื่อม urgency เข้ากับ pain ที่เขาพูดถึงอยู่แล้ว ไม่ใช่สร้าง deadline ใหม่",
    },
    ("NF", "drive_urgency"): {
        "mbti_context": "NF รู้สึกไม่สบายใจกับการ create pressure เพราะกลัวทำให้อีกฝ่ายรู้สึกถูก manipulate แต่ urgency ที่ honest ไม่ใช่ manipulation มันคือข้อมูลที่เขา deserve ที่จะรู้ ถ้าคุณไม่บอก คุณกำลัง withhold สิ่งที่เป็นประโยชน์กับเขา",
        "tension": "NF กลัว pressure อีกฝ่าย จน frame urgency อ่อนเกินจนไม่มีใครรู้สึกว่าต้องรีบ",
        "conflict_example": 'คุณ: "ไม่ urgent อะไรหรอก แค่คิดว่าถ้าสะดวกก็น่าลองดูนะ"\nอีกฝ่าย: "โอเค เดี๋ยวดูเวลาก่อน"\nคุณ: "ได้เลย ไม่รีบ ตอนสะดวกค่อย—"\nอีกฝ่าย: [ไม่เคย follow up]\n\nคุณ frame มันว่าไม่สำคัญ เขาก็ treat มันว่าไม่สำคัญ',
        "why_fails": "NF over-soften จน message ที่ออกไปไม่มี urgency เลย คนจะ prioritize สิ่งที่ urgent และสำคัญ ถ้าคุณบอกว่ามันไม่ urgent เขาก็จะ deprioritize มัน",
        "recommended_example": 'คุณ: "อยากให้รู้ว่า deadline ของ offer นี้คือ [วันที่] หลังจากนั้น [เงื่อนไขเปลี่ยน] ฉันไม่ได้พูดเพื่อ pressure คุณ แต่เพราะอยากให้คุณมีข้อมูลครบก่อนตัดสินใจ คุณต้องการอะไรจากฉันเพื่อให้ decide ได้ก่อนวันนั้น?"\nอีกฝ่าย: "โอเค ถ้าแบบนั้นรีบ sort out ดีกว่า"',
        "the_shift": "Urgency ที่ honest ไม่ใช่ manipulation มันคือ information ที่ช่วยให้เขา decide อย่างมีข้อมูลครบ",
    },
    ("SJ", "drive_urgency"): {
        "mbti_context": "SJ present deadline จริงๆ ได้ครบถ้วน แต่มักขาด emotional layer ที่ทำให้คนรู้สึกว่า 'ต้องรีบจริงๆ' Deadline เป็น fact แต่ urgency เป็น feeling — ต้องทำทั้งสองอย่าง",
        "tension": "SJ present deadline อย่าง accurate แต่ขาด emotional framing ที่ทำให้มัน feel urgent",
        "conflict_example": 'คุณ: "Offer นี้ valid ถึงวันที่ 30 หลังจากนั้น pricing structure เปลี่ยน"\nอีกฝ่าย: "โอเค รับทราบ"\nคุณ: "ราคาจะขึ้น 15% ถ้าหลังจากนั้น"\nอีกฝ่าย: "โอเค เดี๋ยวดู"\n[วันที่ 31 ยังไม่ตัดสินใจ]\n\nเขา heard แต่ไม่ felt ว่ามันสำคัญ',
        "why_fails": "SJ deliver facts ครบแต่ facts อย่างเดียวไม่ move คน ต้องเชื่อม deadline กับ impact ที่เขา care จริงๆ",
        "recommended_example": 'คุณ: "วันที่ 30 คือ deadline ของ pricing นี้ แต่ที่สำคัญกว่านั้นคือ [pain ที่เขา mention ไว้] ที่คุณบอกว่ากำลังเป็นปัญหา ถ้า start ก่อนวันที่ 30 เราสามารถ address มันได้ใน [timeframe] ถ้า start หลัง มันจะอยู่กับทีมไปอีก [timeframe] คุณอยากให้มันอยู่ถึงเมื่อไหร่?"\nอีกฝ่าย: "ไม่อยากให้อยู่นานแบบนั้น รีบ decide ดีกว่า"',
        "the_shift": "เชื่อม deadline กับ pain ที่เขามีอยู่แล้ว ทำให้ urgency เป็นของเขา ไม่ใช่ของ calendar",
    },
    ("SP", "drive_urgency"): {
        "mbti_context": "SP เก่งการสร้าง energy ในช่วงเวลาสด แต่บางที push urgency แรงเกินจนอีกฝ่ายรู้สึกถูก pressure แล้วก็ pull back Urgency ที่ดีทำให้เขา want to move ไม่ใช่ feel ว่าต้อง move",
        "tension": "SP create urgency ด้วย energy สูง แต่บางที cross line จาก exciting เป็น pressure",
        "conflict_example": 'คุณ: "โอกาสแบบนี้ไม่ได้มีบ่อย ถ้าไม่คว้าตอนนี้ก็พลาดแน่นอน!"\nอีกฝ่าย: "ก็ต้องคิดดูก่อน"\nคุณ: "คิดอะไรอีก? Opportunity cost สูงมากถ้ารอ!"\nอีกฝ่าย: "ฉันต้องการเวลา ไม่ชอบถูก rush"\n\nUrgency กลายเป็น pressure กลายเป็น resistance',
        "why_fails": "SP ใช้ energy สูงสร้าง urgency แต่คนที่ถูก pressure รู้สึกว่าต้องป้องกันตัวเอง ซึ่งตรงข้ามกับสิ่งที่ต้องการ",
        "recommended_example": 'คุณ: "ฉันอยากให้รู้ว่า offer นี้ available ถึง [วันที่] แต่ไม่ได้บอกเพื่อ pressure นะ บอกเพราะอยากให้มีเวลาตัดสินใจอย่างมีข้อมูลครบ สิ่งที่ยังทำให้ลังเลคืออะไร?"\nอีกฝ่าย: "ก็ยังมีเรื่อง [X]"\nคุณ: "เรา solve ตรงนั้นได้เลย นี่คือวิธี..."',
        "the_shift": "Urgency ที่ดีเปิดประตูให้เขา move ไม่ใช่ push เขาออกไป — ถามว่าอะไรที่ทำให้ยัง wait แล้ว address ตรงนั้น",
    },

    # ═══════════════ win_commitment ═══════════════
    ("NT", "win_commitment"): {
        "mbti_context": "NT มักคิดว่า 'ตกลงกันแล้ว' เท่ากับ committed แล้ว แต่ agreement ในห้องกับ commitment จริงๆ ต่างกัน ต้องการ specific accountability — ใคร ทำอะไร เมื่อไหร่ ไม่งั้นเป็นแค่ intention ไม่ใช่ commitment",
        "tension": "NT คิดว่า logical agreement = commitment แต่ขาด accountability structure ที่ทำให้มัน stick",
        "conflict_example": 'คุณ: "งั้นเราเห็นตรงกันแล้วว่าจะ proceed?"\nอีกฝ่าย: "ใช่ เห็นด้วย"\n[สองอาทิตย์ต่อมา ไม่มีอะไรเกิดขึ้น]\nคุณ: "เรา agree กันแล้วว่าจะ move ไปทิศทางนั้น ทำไมยังไม่ start?"\nอีกฝ่าย: "ยังหา resource ไม่ได้ ยุ่งมาก"\n\nเขา agree แต่ไม่เคย commit จริงๆ ตัว accountability ไม่มี',
        "why_fails": "NT ถือว่า verbal agreement ใน room เพียงพอ แต่ commitment ต้องการ ownership ที่ชัด — เขาต้อง own action ที่ specific ไม่ใช่แค่ agree กับ direction",
        "recommended_example": 'คุณ: "ดีมากที่เห็นตรงกัน ก่อนจบ meeting ขอ clarify ownership หน่อย — คุณจะรับผิดชอบ [X] ภายใน [วันที่] ถูกไหม?"\nอีกฝ่าย: "ได้ ฉัน confirm"\nคุณ: "โอเค ฉัน note ไว้นะ แล้วจะ check in ตอน [วันที่]"',
        "the_shift": "ก่อนจาก meeting ทุกครั้ง ต้องได้ชื่อ + action + date — นั่นคือ commitment ที่แท้จริง ไม่ใช่แค่ 'ใช่'",
    },
    ("NF", "win_commitment"): {
        "mbti_context": "NF กลัว pressure อีกฝ่ายมาก จน accept vague commitment ไว้ก่อน แล้วรู้สึกไม่ดีเมื่อมันไม่เกิดขึ้น การขอ commitment ที่ specific ไม่ใช่การ distrust เขา มันเป็นการ respect เขาและตัวเอง",
        "tension": "NF accept 'เดี๋ยวดู' เพราะกลัว awkward — แต่มันไม่ใช่ commitment",
        "conflict_example": 'อีกฝ่าย: "ฉันจะ think about it นะ"\nคุณ: "ได้เลย ไม่รีบ ค่อยๆ คิด"\nอีกฝ่าย: "โอเค ขอบคุณ"\n[สามอาทิตย์ผ่านไป ไม่มี follow up]\nคุณ: [ไม่กล้า follow เพราะกลัวดู pushy]\n\nทั้งคู่ comfortable ใน meeting แต่ไม่มีอะไรเกิดขึ้น',
        "why_fails": "NF interpret 'จะ think' ว่าเป็นความก้าวหน้า แต่มันคือ deferral ถ้าไม่ specify ว่าจะ think อะไร เมื่อไหร่ และจะ report ยังไง ก็จะไม่ไปต่อ",
        "recommended_example": 'อีกฝ่าย: "ฉันจะ think about it นะ"\nคุณ: "ได้เลย อยากให้มันไม่หล่น ขอถามว่าคุณ plan จะ decide ภายในเมื่อไหร่? แล้วฉันจะ follow up ตอนนั้น"\nอีกฝ่าย: "อาทิตย์หน้าน่าจะรู้แล้ว"\nคุณ: "โอเค งั้น check in กันวันจันทร์หน้าเลยนะ"',
        "the_shift": "เปลี่ยน 'เดี๋ยวดู' เป็น 'เมื่อไหร่จะรู้?' ทุกครั้ง — นั่นคือความต่างระหว่าง commitment กับ good intention",
    },
    ("SJ", "win_commitment"): {
        "mbti_context": "SJ อยาก formalize commitment เร็วมาก แต่บางทีอีกฝ่าย need เวลา feel ว่าตัวเองเลือก ไม่ใช่ถูก commit เข้าไป ถ้า rush paperwork ก่อน emotional commitment จะเจอ 'ขอคิดดูก่อน' ทุกครั้ง",
        "tension": "SJ อยาก lock down commitment ด้วย process ก่อนที่อีกฝ่ายจะ feel ready",
        "conflict_example": 'อีกฝ่าย: "ฟังแล้วน่าสนใจมาก"\nคุณ: "ดีมาก งั้น sign ที่นี่ได้เลย ฉันมี contract มาด้วย"\nอีกฝ่าย: [uncomfortable] "โอ้... เร็วหน่อยนะ ขอ review ก่อนได้ไหม?"\nคุณ: "มีอะไรให้ review? ทุกอย่าง agree กันแล้ว"\nอีกฝ่าย: "ก็... ขอคิดดูก่อน"\n\nเขา interested แต่รู้สึกถูก rush แล้วก็ pull back',
        "why_fails": "SJ ใช้ paperwork เป็น signal ของ trust แต่อีกฝ่ายใช้มันเป็น signal ว่า 'ฉันถูกดัน' ต้องให้เขา arrive ที่ commitment ด้วยตัวเอง",
        "recommended_example": 'อีกฝ่าย: "ฟังแล้วน่าสนใจมาก"\nคุณ: "ดีมาก ก่อนที่จะ move ไปขั้นต่อไป มีอะไรที่ยังอยากให้ชัดขึ้นไหม?"\nอีกฝ่าย: "ไม่มี ฉัน comfortable แล้ว"\nคุณ: "โอเค งั้น step ต่อไปง่ายๆ คือ [X] ก่อน แล้วเราค่อย sort ส่วนอื่นทีหลัง คุณ OK กับ [X] ไหม?"',
        "the_shift": "ให้เขาเดิน step ทีละ step ด้วยตัวเอง ไม่ใช่เอา contract มาวางตรงหน้าทันที",
    },
    ("SP", "win_commitment"): {
        "mbti_context": "SP สร้าง excitement และ momentum ได้ดีมาก แต่มักออกจาก meeting ด้วย good energy โดยไม่มี specific commitment ผลคือ ทั้งคู่รู้สึกดี แต่ไม่มีอะไรเกิดขึ้น ต้อง anchor commitment ก่อน energy จะหาย",
        "tension": "SP ได้ emotional commitment แต่ไม่ได้ specific one — แล้วทั้งคู่ก็ลืมไป",
        "conflict_example": 'คุณ: "สนุกมากเลยที่ได้คุย เรา totally ควร work ด้วยกัน!"\nอีกฝ่าย: "ใช่ ฉันก็คิดแบบนี้เลย!"\nคุณ: "เยี่ยมเลย เดี๋ยวจะ reach out นะ!"\n[ทั้งคู่ออกไปด้วย high energy]\n[สองอาทิตย์ต่อมา — ไม่มีใคร reach out]\n\nEnergy จริง intention จริง แต่ไม่มี structure รองรับ',
        "why_fails": "SP trust ว่า momentum จะ carry itself แต่ไม่ได้ commitment ไม่ได้มาจาก good feeling มันต้องการ specific action ที่ตกลงกันก่อน moment จะหาย",
        "recommended_example": 'คุณ: "เราจะ work ด้วยกันแน่นอน ก่อนจากกัน ขอ lock สองอย่าง — คุณ ok กับ [next step] ก่อน วันที่ [date] ไหม?"\nอีกฝ่าย: "ได้เลย"\nคุณ: "โอเค [นำมือถือออกมา] ฉัน set reminder ให้เราทั้งคู่เลยนะ" [ส่ง calendar invite ทันที]',
        "the_shift": "Lock commitment ก่อน energy หาย — calendar invite ที่ส่งทันทีดีกว่า promise ที่ดีที่สุด",
    },
}

HD_WORK: dict[tuple[str, str], str] = {

    # get_buyin
    ("Generator", "get_buyin"): "ตอนขอ buy-in อย่า pitch อย่างเดียว รอให้เขา show interest ก่อน แล้ว respond จากความตื่นเต้นจริงๆ ของคุณ คนรู้สึกได้เวลา energy แท้จริง และ genuine enthusiasm ซื้อ buy-in ได้ดีกว่า prepared pitch",
    ("Manifesting Generator", "get_buyin"): "ตอบสนองต่อ interest ที่เห็น แล้วขยับเร็ว แต่ inform ทุกคนที่ involved ก่อน move อย่าให้ใครรู้สึกว่าถูก surprise ด้วย idea ที่คุณ pitch ไปแล้ว — ทำให้พวกเขา feel เป็น part of it ก่อน",
    ("Manifestor", "get_buyin"): "คุณ initiate ได้เลย แต่บอกก่อนว่าคุณกำลังจะ move ไปทิศทางนี้ การ inform ล่วงหน้าทำให้เขา feel included ไม่ใช่โดน impose — ต่างกันมากในสายตาของคนที่คุณต้องการ buy-in",
    ("Projector", "get_buyin"): "ก่อน pitch สร้าง context ให้เขา invite คุณก่อน เช่น ถามว่า 'มีเรื่อง X ที่อยากคุย ฉันมี perspective ที่น่าจะ useful — อยากฟังไหม?' ตอนที่ถูกเชิญ insight ของคุณจะ land ได้แทนที่จะถูก defend",
    ("Reflector", "get_buyin"): "Observe ก่อนว่า vibe ในทีมหรือ meeting วันนั้นเป็นยังไง วันที่พลังงานดี คนเปิดรับมากกว่า — เลือก timing ของการขอ buy-in ตาม environment ไม่ใช่แค่ตาม calendar",

    # build_trust_work
    ("Generator", "build_trust_work"): "Trust สร้างได้ดีที่สุดตอน respond งานจากความ genuine แทนที่จะรับทุกอย่างจาก obligation คนรู้สึกได้เวลาคุณ all-in กับงาน และนั่นสร้าง trust มากกว่าการยิ้มแย้มตลอดเวลา",
    ("Manifesting Generator", "build_trust_work"): "Trust สร้างจาก inform before you move — ทุกครั้งที่คุณ pivot หรือ shift direction บอกทีมก่อนเสมอ คนที่รู้ว่าคุณจะบอกเสมอจะ trust คุณแม้ในช่วง transition",
    ("Manifestor", "build_trust_work"): "Trust สร้างจาก informing ไม่ใช่จาก consensus ทุกครั้งที่คุณ initiate บอกคนที่ involved ก่อน ประโยคเดียวนั้นทำให้คุณ feel เหมือน leader ไม่ใช่ agent ที่ทำตามใจตัวเอง",
    ("Projector", "build_trust_work"): "Trust ของคุณสร้างจากการ wait และ read ได้แม่น ตอนที่คนมาหาคุณและคุณให้ guidance ที่ตรงจุด นั่นสร้าง reputation ที่ทรงพลังที่สุด อย่า force insight — ให้มันมาตอนที่ถูกถาม",
    ("Reflector", "build_trust_work"): "Trust ของคุณสร้างจากการ observe และ reflect ได้แม่น แชร์สิ่งที่คุณสังเกตเห็นในทีมบ้าง ไม่ต้องรอให้มันสมบูรณ์ 100% การ mirror ความจริงของ environment อย่างซื่อสัตย์คือ contribution ที่ทรงพลังของคุณ",

    # secure_agreement
    ("Generator", "secure_agreement"): "ก่อน close ตรวจสอบว่า gut ของคุณ respond ต่อ deal นี้จริงๆ ไหม ถ้าใช่ ความ genuine enthusiasm ของคุณในตอน close จะ infectious ถ้าไม่ใช่ คนจะรู้สึกได้ — close ตอนที่คุณ genuinely excited",
    ("Manifesting Generator", "secure_agreement"): "Close เร็วเมื่อ signal มา แต่ก่อน close inform ทุกคนที่ต้อง know ว่า agreement กำลังจะ happen อย่าให้ใครรู้สึก surprised หลัง sign",
    ("Manifestor", "secure_agreement"): "ตอน close บอกชัดว่า 'ฉันจะ move forward' ไม่ต้อง ask permission แต่ inform ว่ากำลัง proceed การ announce ชัดๆ ทำให้ close smooth ขึ้น",
    ("Projector", "secure_agreement"): "ก่อน close ตรวจสอบว่าคุณ read อีกฝ่าย correctly ไหม ถามว่า 'คุณ comfortable กับทุกอย่างแล้วจริงๆ ไหม?' — Projector อ่านคนได้แม่น ใช้ gift นั้นตอน close",
    ("Reflector", "secure_agreement"): "สำหรับ agreement ใหญ่ อย่าถูก rush ให้ sign เร็วเกินไป ขอเวลา review ก่อน และตรวจสอบว่าคุณ feel ดีกับมันในหลายช่วงเวลา ไม่ใช่แค่ในห้องประชุม",

    # drive_urgency
    ("Generator", "drive_urgency"): "Drive urgency จาก genuine concern ของคุณ ถ้าคุณ truly เห็นว่าการรอมี cost จริงๆ ความ authentic ของ concern นั้นจะ come through ได้เอง อย่า manufacture urgency ที่คุณไม่ feel จริงๆ",
    ("Manifesting Generator", "drive_urgency"): "คุณ move เร็วตามธรรมชาติ ใช้ energy นั้นให้ advantage — show เขาว่าคุณ ready จะ move ทันที และ gap เพียงอย่างเดียวคือ decision ของเขา ความ readiness ของคุณเองเป็น urgency ที่ powerful",
    ("Manifestor", "drive_urgency"): "บอกตรงๆ ว่าคุณกำลัง move ไปทิศทางนี้ และ window ที่เขาจะ join คือตอนนี้ การ inform เขาเกี่ยวกับ direction ที่คุณจะไป สร้าง urgency ที่ natural โดยไม่ต้อง manipulate",
    ("Projector", "drive_urgency"): "ใช้ ability ในการ read สถานการณ์ เพื่อ identify moment ที่อีกฝ่าย most receptive แล้ว share insight ว่าทำไมต้องรีบ ตอนที่ถูก invite ให้ guide timing ของคุณจะ sharp มาก",
    ("Reflector", "drive_urgency"): "Urgency ที่คุณ drive ได้ดีที่สุดมาจากการ reflect สิ่งที่คุณ observe เห็นจริงๆ 'ฉันสังเกตว่า [pattern] กำลัง cost มากขึ้น' มักมีน้ำหนักกว่า deadline ที่ถูกสร้าง",

    # win_commitment
    ("Generator", "win_commitment"): "Commitment ที่ยั่งยืนมาจากการที่คุณ genuinely want ให้มันเกิด ตรวจสอบว่า gut ของคุณ say yes กับ commitment นี้จริงๆ ก่อน ask อีกฝ่าย เพราะ energy ของคุณจะบอก",
    ("Manifesting Generator", "win_commitment"): "ตอน win commitment บอกทันทีว่า next step คืออะไรแล้ว move ไปเลย แต่ให้ระวัง inform ทุกคนที่เกี่ยวข้องว่า commitment เกิดขึ้นแล้ว ก่อนที่คุณจะ pivot ไปทำอย่างอื่น",
    ("Manifestor", "win_commitment"): "เมื่อได้ commitment แล้ว announce plan ต่อไปชัดๆ ว่าคุณจะทำอะไร ความ clarity ของ direction หลัง commitment ทำให้คนรู้สึก safe ที่จะ stay committed",
    ("Projector", "win_commitment"): "ก่อน ask for commitment ให้แน่ใจว่าคุณ invited และ recognized ก่อน Commitment ที่ขอจากคน invited คุณจะ solid กว่า commitment ที่ขอจากคนที่ยังไม่ fully engaged",
    ("Reflector", "win_commitment"): "สำหรับ commitment ที่สำคัญ ให้เวลาตัวเองด้วย ไม่ใช่แค่อีกฝ่าย สำหรับ commitment ที่ไม่ใหญ่มาก ใช้การ observe ว่าคนพร้อมไหม แล้วค่อย ask",
}
