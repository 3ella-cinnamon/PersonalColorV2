"""Money sub-goal specific personality content — Thai Gen Z style."""

MBTI_MONEY: dict[tuple[str, str], dict] = {

    # ═══════════════ close_deal ═══════════════
    ("NT", "close_deal"): {
        "mbti_context": "NT มักวิเคราะห์ต่อแม้หลังจากที่อีกฝ่าย ready จะ close แล้ว พอเห็น buying signal ต้อง stop presenting และ ask ทันที การ present ต่อหลังจาก yes signal คือการ talk yourself out of a deal",
        "tension": "NT keep presenting information แม้อีกฝ่าย ready แล้ว เพราะกลัวว่า case ยังไม่ครบ",
        "conflict_example": 'ลูกค้า: "ฉัน like มันมากเลย ดูดี"\nคุณ: "ดีมาก แล้วยังมี feature อีกอย่างที่อยากให้รู้คือ..."\nลูกค้า: "จริงๆ พร้อม move forward แล้วนะ"\nคุณ: "โอเค แต่ก่อน อยากให้รู้เรื่อง pricing tier ต่างๆ ด้วยว่า..."\nลูกค้า: [ความ enthusiasm เริ่มลด] "ขอคิดดูก่อนแล้วกัน"\n\nเขา ready แล้ว แต่คุณยังไม่ยอม close',
        "why_fails": "NT กลัว commit ก่อนที่ทุกอย่างจะ perfect จน miss the moment คนที่ ready จะซื้อต้องการให้คุณ confirm ว่า ok ไม่ใช่ information เพิ่ม",
        "recommended_example": 'ลูกค้า: "ฉัน like มันมากเลย ดูดี"\nคุณ: "ดีมาก คุณ ready จะ start เลยไหม หรือยังมีอะไรที่ต้องการรู้ก่อน?"\nลูกค้า: "ไม่มี ready เลย"\nคุณ: "โอเค step ต่อไปคือ [X] เราทำได้เลยไหม?"',
        "the_shift": "เห็น buying signal = หยุด present = ask ทันที สูตรนี้ตายตัว",
    },
    ("NF", "close_deal"): {
        "mbti_context": "NF กลัวว่าการ ask ให้ buy คือการ pressure อีกฝ่าย แต่ถ้าคุณ believe จริงๆ ว่า product/service นี้ดีสำหรับเขา การไม่ ask คือการ withhold สิ่งที่ดีจากเขา Ask ด้วย care ไม่ใช่ด้วย pressure",
        "tension": "NF trail off แทนที่จะ make the ask เพราะกลัวว่า ask = push",
        "conflict_example": 'ลูกค้า: "ฟังแล้ว น่าสนใจมากเลย"\nคุณ: "ดีใจมากที่ชอบ ฉันคิดว่ามันจะ work ดีมากสำหรับสถานการณ์ของคุณ"\nลูกค้า: "ใช่ ดูดีนะ"\nคุณ: "ถ้ามีอะไร feel free ถามได้เลยนะ"\nลูกค้า: "โอเค จะ keep in mind"\n[ไม่มี follow up]\n\nคุณ present ดีมาก แต่ไม่เคย ask',
        "why_fails": "NF คิดว่า interest = decision แต่คนต้องการ permission ที่จะ say yes อยู่บ่อยๆ การ ask คือการให้ permission นั้น",
        "recommended_example": 'ลูกค้า: "ฟังแล้วน่าสนใจมากเลย"\nคุณ: "ดีมาก ฉัน genuinely คิดว่ามันจะ help ได้จริงๆ คุณ ready จะ move forward เลยไหม?"\nลูกค้า: "อ๋อ ได้เลย"\nคุณ: "เยี่ยม เรา start ด้วย [next step] ได้เลย"',
        "the_shift": "Ask ด้วย care — 'ฉัน believe มันจะ help คุณ คุณ ready ไหม?' ไม่ใช่ manipulation มันคือ genuine invitation",
    },
    ("SJ", "close_deal"): {
        "mbti_context": "SJ follow process ได้ดีมาก แต่บางทีตาม script เกินจน miss emotional buying signal ของอีกฝ่าย ตอนที่เขา show excitement ต้อง respond ต่อ emotion นั้น ไม่ใช่ continue ไปยัง bullet point ต่อไปใน script",
        "tension": "SJ follow presentation script อย่างครบถ้วน แต่ miss จังหวะที่ emotion ของอีกฝ่าย peak",
        "conflict_example": 'ลูกค้า: [ตาสว่าง] "โห นี่แหละที่ฉันตามหามาตลอด!"\nคุณ: "ดีมาก แล้วก็ส่วนที่สี่ของ proposal คือเรื่อง implementation timeline ซึ่งประกอบด้วย..."\nลูกค้า: [enthusiasm ลด ระหว่างที่ฟัง timeline ยาว]\nคุณ: "...และสุดท้ายคือเรื่อง support package"\nลูกค้า: "โอเค ขอเอา proposal ไปอ่านก่อนนะ"\n\nเขา peak แล้ว แต่คุณ continue present แทนที่จะ close',
        "why_fails": "SJ comfortable กับ process มากจน process กลายเป็น barrier ต่อ natural close moment ที่เกิดขึ้นก่อน script จะจบ",
        "recommended_example": 'ลูกค้า: [ตาสว่าง] "โห นี่แหละที่ฉันตามหามาตลอด!"\nคุณ: [หยุด script ทันที] "ฉัน glad มากที่ได้ยินแบบนี้ นั่นหมายความว่า ready จะ move forward เลยไหม? หรือยังมีอะไรที่ต้องการรู้ก่อน?"\nลูกค้า: "Move forward เลย ต้องทำอะไรบ้าง?"',
        "the_shift": "Script คือ guide ไม่ใช่ jail — ตอนเห็น emotional peak ให้ deviate และ close ทันที",
    },
    ("SP", "close_deal"): {
        "mbti_context": "SP read ห้องได้ดีมาก และรู้สึกได้เมื่ออีกฝ่าย ready แต่บางทีตื่นเต้นเกินจน rush close ก่อนที่เขาจะ arrive ที่ yes ด้วยตัวเอง ต้องให้เขา feel ว่าตัวเองตัดสินใจ ไม่ใช่ถูก close",
        "tension": "SP sense the moment แต่บางทีเข้า close เร็วเกินจนอีกฝ่าย feel pressured แทนที่จะ ready",
        "conflict_example": 'ลูกค้า: [ดูสนใจ ถามคำถามเยอะ]\nคุณ: [sense momentum] "ดูเหมือนคุณ love มัน sign วันนี้เลยนะ!"\nลูกค้า: "โอ้ ยังไม่ถึงขนาดนั้น"\nคุณ: "Deal นี้ดีมากแน่นอน มาทำเอกสารกันเลย"\nลูกค้า: "ฉันต้องการเวลา ไม่ชอบถูก rush"\n\nคุณ read momentum ถูก แต่ push เร็วเกินจน broke it',
        "why_fails": "SP บางทีสับสนระหว่าง interest กับ readiness คำถามเยอะไม่ใช่ yes signal เสมอ บางทีเป็นแค่ curiosity",
        "recommended_example": 'ลูกค้า: [ถามคำถามเยอะ]\nคุณ: [ตอบครบ] "ฟังดูคุณ interested มาก มีอะไรที่ยังอยากให้ชัดขึ้นก่อนที่จะ decide ไหม?"\nลูกค้า: "ไม่มีแล้ว ฉัน OK"\nคุณ: "โอเค งั้น next step คือ [X] คุณ OK ไหม?"',
        "the_shift": "Check readiness ก่อน close — 'ยังมีอะไรที่อยากให้ชัดไหม?' ถ้า no ค่อย close",
    },

    # ═══════════════ bargain_discount ═══════════════
    ("NT", "bargain_discount"): {
        "mbti_context": "NT negotiate ด้วย logic และ data ได้ดีมาก แต่บางทีมา armed กับ competing quotes จนทำให้บรรยากาศเป็น adversarial ซึ่ง seller ก็จะ dig in เช่นกัน การ negotiate ที่ได้ผลต้องให้อีกฝ่ายอยากช่วย ไม่ใช่รู้สึกถูก challenge",
        "tension": "NT frame การ negotiate เป็น battle of logic จน seller feel ถูก attack และ dig in มากขึ้น",
        "conflict_example": 'คุณ: "ฉันมีใบเสนอราคาจาก 3 competitor และพวกเขา offer ได้ราคาต่ำกว่า 20%"\nSeller: "Pricing ของเราสะท้อน quality ที่ต่างกัน"\nคุณ: "ฉันวิเคราะห์แล้ว spec ใกล้เคียงมาก ราคาควรต่ำกว่านี้"\nSeller: "เราไม่สามารถ match ราคา low-quality competitor ได้"\nคุณ: "ฉันไม่ได้บอกว่า low-quality แค่บอกว่าราคาสูงเกินไป"\nSeller: [defensive] "นี่คือ pricing ที่ดีที่สุดที่เราให้ได้"\n\nทั้งคู่ lock กัน ไม่มีใครได้ในสิ่งที่ต้องการ',
        "why_fails": "NT approach negotiation เหมือน debate ซึ่งทำให้ seller defend position แทนที่จะหา creative solution ด้วยกัน",
        "recommended_example": 'คุณ: "ฉัน genuinely ต้องการ work กับคุณ quality ชัดเจน แต่ budget ของฉัน limited ที่ [X] มีวิธีไหนที่เราจะ structure ได้ให้ fit budget นั้นบ้าง?"\nSeller: "งั้นลองดู option นี้ไหม..."\nคุณ: "โอเค บอกให้ฟัง"',
        "the_shift": "ถามว่า 'เราจะหาวิธีไหนด้วยกันได้บ้าง?' แทน 'คุณต้องลดราคา' — เปลี่ยนจาก battle เป็น collaboration",
    },
    ("NF", "bargain_discount"): {
        "mbti_context": "NF รู้สึกผิดกับการขอ discount เพราะกังวลว่าจะทำให้อีกฝ่ายรู้สึกไม่ดี แต่การ negotiate ไม่ใช่การ insult คนขาย มันเป็น normal business ที่เขาคาดหวังอยู่แล้ว การ accept ราคาแรกโดยไม่ถามเลยคือการ leave money on the table",
        "tension": "NF รู้สึกผิดที่จะ ask จน accept ราคาแรกทุกครั้ง",
        "conflict_example": 'Seller: "ราคา package นี้คือ [X] บาท"\nคุณ: [รู้สึกว่าแพงไป แต่] "โอเค ได้เลย"\nSeller: "ตัดสินใจเร็วดีนะ"\nคุณ: "ก็ มันดูดีนะ"\n[หลังจากนั้น คุณเสียใจที่ไม่ได้ถาม]\n\nคุณรู้สึกผิดที่จะขอ เลยไม่ขอ แล้วก็เสียใจทีหลัง',
        "why_fails": "NF interpret การขอ discount ว่า rude แต่ seller บิลล์ราคาโดยคาดว่าจะมีการ negotiate อยู่แล้ว การไม่ขอไม่ได้ทำให้คุณ nicer มันแค่ทำให้จ่ายแพงกว่า",
        "recommended_example": 'Seller: "ราคา package นี้คือ [X] บาท"\nคุณ: "ขอบคุณมาก ฉัน interested จริงๆ แต่ budget ของฉันคือ [Y] มีวิธีไหนที่เราจะ work ในงบนั้นได้บ้าง?"\nSeller: "งั้นลอง option นี้หรือ adjust package แบบนี้ไหม"\nคุณ: "โอ้ แบบนั้นก็ work ได้"',
        "the_shift": "การ ask ว่า 'มีวิธีไหน work ในงบนี้ได้บ้าง?' สุภาพ ปกติ และ expected — ไม่มีอะไรต้องรู้สึกผิด",
    },
    ("SJ", "bargain_discount"): {
        "mbti_context": "SJ follow formal negotiation process ได้ดี แต่บางทีแข็งเกินจน miss creative trade-offs ที่ win-win กว่า เช่น ลด scope บางส่วน เพิ่ม volume commitment หรือ adjust payment terms แทนที่จะ negotiate แค่ราคา",
        "tension": "SJ focus ที่ราคาเป็นหลัก แต่พลาด creative trades ที่ทำให้ทั้งคู่ได้มากกว่า",
        "conflict_example": 'คุณ: "ราคานี้เกิน budget ฉัน 15% ลดได้ไหม?"\nSeller: "ราคานี้ already ต่ำที่สุดที่เราทำได้"\nคุณ: "แต่มัน over budget จริงๆ"\nSeller: "เราทำราคาพิเศษไม่ได้แล้ว"\nคุณ: "งั้นก็ต้องคิดใหม่"\n[การ negotiate ติดตัน]\n\nทั้งคู่ focus ที่ price อย่างเดียวจน stuck',
        "why_fails": "SJ treat negotiation เป็น fixed-sum game แต่ส่วนใหญ่มี variables อื่นๆ ที่ negotiate ได้ เช่น timeline, scope, payment, หรือ volume",
        "recommended_example": 'คุณ: "ราคานี้เกิน budget ฉัน 15% ถ้า adjust ราคาตรงๆ ไม่ได้ มีวิธีอื่นไหมที่เราจะ structure ให้ fit budget ได้? เช่น ถ้าฉัน commit volume มากกว่า หรือ payment terms ต่างกัน?"\nSeller: "ถ้า commit 6 เดือน เราให้ rate ดีกว่านี้ได้"\nคุณ: "โอ้ แบบนั้น work ได้"',
        "the_shift": "Negotiate ทั้ง deal ไม่ใช่แค่ราคา — volume, terms, scope, timeline ทุกอย่าง negotiate ได้",
    },
    ("SP", "bargain_discount"): {
        "mbti_context": "SP บางทีพูดตัวเลขออกไปก่อนจะ anchor position ที่ดี หรือ negotiate ด้วย energy สูงจน สับสนระหว่าง enthusiasm กับ leverage ก่อน negotiate ต้องรู้ว่า walkaway number คืออะไร แล้วค่อย move",
        "tension": "SP negotiate ด้วย instinct และ energy แต่บางทีขาด anchor position ที่ชัดก่อน",
        "conflict_example": 'Seller: "ราคา package นี้คือ [X]"\nคุณ: [gut react] "โอ้ แพงไปหน่อย ลดเหลือ [Y] ได้ไหม?" [Y ต่ำเกินไปโดยไม่มี rationale]\nSeller: "ไม่ได้เลย"\nคุณ: "งั้น [Z]?" [เพิ่มขึ้น]\nSeller: "ก็ยังไม่ได้"\nคุณ: [หมด leverage แล้ว] "งั้น... [X] ก็ได้"\n\nคุณ anchor ต่ำเกินไปโดยไม่มี rationale แล้วก็ retreat ทั้งหมด',
        "why_fails": "SP negotiate จาก gut reaction แทนที่จะจาก prepared position ทำให้ number ที่ throw ออกไปมีน้ำหนักน้อยและ easy ที่จะ push back",
        "recommended_example": '[ก่อน meeting คิดไว้ก่อน]\nTarget: [X], Acceptable: [Y], Walkaway: [Z]\n\nSeller: "ราคา [A]"\nคุณ: "ฉัน interested จริงๆ budget ของฉันคือ [X] ซึ่งต่ำกว่านั้น [%] เราจะหาวิธี meet กันตรงกลางได้ไหม?"\nSeller: "งั้นเราลองที่ [B] ดูไหม?"\nคุณ: "ถ้า [B] มา พร้อม [condition] ได้เลย"',
        "the_shift": "เตรียม 3 numbers ก่อน negotiate ทุกครั้ง — ideal, acceptable, walkaway แล้ว open ด้วย ideal เสมอ",
    },

    # ═══════════════ handle_objections ═══════════════
    ("NT", "handle_objections"): {
        "mbti_context": "NT ตอบ price objection ด้วย ROI data ได้ดีมาก แต่บางทีลืมว่า 'แพงเกินไป' มักไม่ใช่เรื่อง math มันเป็นเรื่อง fear of risk หรือ ความไม่มั่นใจ ต้อง address emotion นั้นก่อน แล้ว data จึงจะ land",
        "tension": "NT respond ต่อ price objection ด้วย logic แต่ objection จริงๆ มักเป็น emotional concern",
        "conflict_example": 'ลูกค้า: "ราคาแพงเกินไปสำหรับฉัน"\nคุณ: "ถ้า calculate ROI แล้ว คุ้มภายใน 8 เดือน จาก savings ตรงนี้..."\nลูกค้า: "ก็แต่ upfront cost สูงมาก"\nคุณ: "ถ้าเทียบกับ cost ของการไม่ทำ มันต่ำกว่ามาก"\nลูกค้า: "ฉันเข้าใจ logic แต่รู้สึกว่ายังไม่ ready"\n\nLOGIC ถูกหมด แต่ missed ว่าเขา กลัว risk ไม่ใช่ไม่เข้าใจ math',
        "why_fails": "NT treat price objection เป็นปัญหา arithmetic แต่ส่วนใหญ่มันเป็นปัญหา emotional — fear of making a mistake, uncertainty ว่าจะ work ไหม",
        "recommended_example": 'ลูกค้า: "ราคาแพงเกินไปสำหรับฉัน"\nคุณ: "เข้าใจมาก เวลาพูดว่าแพงเกิน ช่วยให้ฉัน understand ได้ไหมว่า concern หลักคืออะไร? ราคาจริงๆ หรือ ความไม่แน่ใจว่าจะ worth it?"\nลูกค้า: "จริงๆ ก็กลัวว่าจะไม่ได้ใช้เต็มที่"\nคุณ: "ขอบคุณที่บอก นั่นคือ concern ที่เราจัดการได้เลย..."',
        "the_shift": "ถามก่อนตอบ — 'concern หลักคืออะไร?' จะได้ตอบตรง เรื่องที่ block จริงๆ ไม่ใช่สิ่งที่คิดเอง",
    },
    ("NF", "handle_objections"): {
        "mbti_context": "NF รู้สึก empathy กับ price concern ของลูกค้ามาก จน cave และเสนอ discount ทันทีโดยไม่จำเป็น ซึ่งสอนให้ลูกค้ารู้ว่า 'ถ้า object ก็จะได้ราคาดีกว่า' ต้อง validate concern ก่อน แต่ stand ที่ value ก่อน discount",
        "tension": "NF empathize กับ price concern เต็มที่จน cave เร็วเกิน — สอนให้ลูกค้า object มากขึ้น",
        "conflict_example": 'ลูกค้า: "ราคาสูงกว่าที่คาดไว้นะ"\nคุณ: "โอ้ เข้าใจเลย ถ้างั้นฉันให้ discount 15% ได้นะ"\nลูกค้า: "จริงเหรอ? ถ้าแบบนั้นก็น่าสนใจขึ้น"\n[อาทิตย์ต่อมา]\nลูกค้าใหม่: "ราคาสูงกว่าที่คาดนะ"\nคุณ: [จะ offer discount อีกแล้ว]\n\nคุณสอน pattern ที่ไม่ดีทั้งกับลูกค้าและตัวเอง',
        "why_fails": "NF ไม่ชอบเห็น discomfort ของอีกฝ่ายจน offer solution ก่อนที่จะรู้ว่า concern จริงๆ คืออะไร discount ที่ไม่จำเป็น = เสีย margin และ เสีย credibility",
        "recommended_example": 'ลูกค้า: "ราคาสูงกว่าที่คาดไว้นะ"\nคุณ: "เข้าใจเลย บอกให้ฉัน understand ได้ไหมว่า concern หลักคืออะไร? Budget จริงๆ หรือ value ที่ได้รับ?"\nลูกค้า: "จริงๆ ก็ไม่แน่ใจว่าจะ worth it ไหม"\nคุณ: "นั่นเป็น concern ที่ valid มาก ขอ walk through สิ่งที่คุณจะได้รับจริงๆ..."\n[แสดง value ก่อน — ถ้ายังต้องการ adjust ค่อยคุยทีหลัง]',
        "the_shift": "Validate concern ก่อน reinforce value ก่อน discount เป็นสิ่งสุดท้ายที่ offer ไม่ใช่สิ่งแรก",
    },
    ("SJ", "handle_objections"): {
        "mbti_context": "SJ defend ราคาด้วย logic และ process ได้ดี แต่บางทีลืม address feeling ที่อยู่ใต้ objection เมื่อลูกค้าบอกว่าแพง พวกเขาไม่ได้แค่ต้องการ justification พวกเขาต้องการรู้สึกว่าการตัดสินใจนี้ safe",
        "tension": "SJ defend ราคาด้วย logic ครบ แต่ไม่ได้ address ความรู้สึกไม่ปลอดภัยที่อยู่ใต้ objection",
        "conflict_example": 'ลูกค้า: "ราคานี้แพงเกินไป"\nคุณ: "ราคานี้ reflect ทั้ง quality, support ตลอด 24/7 และ track record ที่ proven มาแล้ว"\nลูกค้า: "ก็แต่ยังแพงอยู่ดี"\nคุณ: "เมื่อเทียบกับ cost ของปัญหาที่คุณมีอยู่ มัน make sense"\nลูกค้า: "ก็รู้นะ แต่รู้สึกว่ายังไม่ชัวร์"\n\nLogic ครบ แต่ feeling ของความ uncertain ยังอยู่',
        "why_fails": "SJ พยายาม out-logic ความรู้สึก แต่ feelings ไม่หายไปด้วย logic พวกเขาหายไปเมื่อถูก acknowledge และ address ตรงๆ",
        "recommended_example": 'ลูกค้า: "ราคานี้แพงเกินไป"\nคุณ: "เข้าใจเลย เวลา invest เยอะ มันต้องรู้สึก comfortable ว่า risk น้อย อยากให้รู้ว่า [guarantee/proof point] ซึ่งทำให้ risk ลดลง แต่ถ้ายัง concern อยู่ มีส่วนไหนที่อยากให้ชัดขึ้นไหม?"\nลูกค้า: "จริงๆ อยากรู้เรื่อง [X]"\nคุณ: "โอเค นั่นเป็น concern ที่ดีมาก..."',
        "the_shift": "Address ความรู้สึกก่อน — 'ฉันเข้าใจว่าการ invest เยอะต้องการ confidence สูง' แล้วค่อย reinforce",
    },
    ("SP", "handle_objections"): {
        "mbti_context": "SP บางทีรู้สึก personal กับ price objection และตอบด้วย defensiveness หรือ 'take it or leave it' energy ซึ่งทำให้ลูกค้า feel ถูก challenge แล้วก็ leave Objection ไม่ใช่ attack มันเป็น invitation ให้ help เขา decide",
        "tension": "SP รู้สึก defensive ต่อ price objection จน respond ด้วย energy ที่ escalate แทนที่จะ de-escalate",
        "conflict_example": 'ลูกค้า: "ราคานี้แพงเกินไปนะ"\nคุณ: "ราคานี้ fair มากแล้วนะ เมื่อเทียบกับ value ที่ได้"\nลูกค้า: "ก็แต่สำหรับฉันมันสูงอยู่"\nคุณ: "ก็ถ้า budget ไม่พอจริงๆ ก็ไม่รู้จะทำยังไงได้"\nลูกค้า: "งั้นก็... ไม่แล้วกัน"\n\nคุณ technically ไม่ได้ผิด แต่ energy ที่ออกมาปิดประตู',
        "why_fails": "SP interpret price objection ว่าเป็น criticism และ defend ด้วย energy ที่ makes the customer feel wrong for asking — ซึ่งทำให้เขา leave",
        "recommended_example": 'ลูกค้า: "ราคานี้แพงเกินไปนะ"\nคุณ: "เข้าใจเลย อยากรู้ว่า concern คืออะไร? Budget limit หรือ ไม่แน่ใจว่าจะ worth it?"\nลูกค้า: "ก็ไม่แน่ใจว่าจะ worth it"\nคุณ: "โอเค นั่นเป็น fair concern มาก ขอ show ให้ดูได้ไหมว่า [specific value] มัน work ยังไงสำหรับสถานการณ์ของคุณโดยเฉพาะ?"',
        "the_shift": "Objection = ลูกค้ายังอยู่ในการสนทนา ถามว่า concern คืออะไรแทนที่จะ defend — แล้ว address ตรงนั้น",
    },

    # ═══════════════ increase_value ═══════════════
    ("NT", "increase_value"): {
        "mbti_context": "NT เก่งการ show features และ specs แต่บางทีลืมว่าลูกค้าไม่ได้ care features ของคุณ เขา care outcomes ของตัวเอง ต้อง translate features เป็น 'สิ่งที่จะเกิดขึ้นกับชีวิต/งานของคุณ' เสมอ",
        "tension": "NT present features ที่มี แต่พลาด translate เป็น outcomes ที่ลูกค้า care จริงๆ",
        "conflict_example": 'คุณ: "ระบบนี้มี 47 features รวมถึง real-time analytics, AI-powered recommendations, และ cross-platform sync"\nลูกค้า: "อืม..."\nคุณ: "และ API integration รองรับ 200+ platforms"\nลูกค้า: "ฟังดูเยอะดี แต่ฉันต้องการอะไรอย่างนี้จริงๆ ไหมนะ"\n\nลูกค้า overwhelmed ด้วย features แต่ไม่เห็น personal value',
        "why_fails": "NT สนใจว่าสินค้ามีอะไรบ้าง แต่ลูกค้าสนใจว่าชีวิตของเขาจะดีขึ้นยังไง — เป็นคนละ conversation กัน",
        "recommended_example": 'คุณ: "ก่อน walk through features ขอถามก่อนว่า ตอนนี้ pain หลักที่ทีมเจออยู่คืออะไร?"\nลูกค้า: "ข้อมูล manual เยอะมาก ทีมเสียเวลา"\nคุณ: "โอเค งั้น features ที่ directly address เรื่องนั้นคือ [X] ซึ่งทำให้ทีมประหยัดเวลาได้ประมาณ [Y] ต่ออาทิตย์ นั่นหมายความว่า [concrete outcome สำหรับเขา]"',
        "the_shift": "Feature → Benefit → Outcome ที่ personal ต้อง connect ทุก feature เข้ากับ 'สิ่งที่คุณจะได้' โดยเฉพาะ",
    },
    ("NF", "increase_value"): {
        "mbti_context": "NF เล่าเรื่องได้ emotionally compelling มาก แต่บางทีขาด concrete proof ที่ทำให้ลูกค้ามั่นใจ ต้องผสม emotional story กับ specific evidence เพราะ feeling เปิดใจ แต่ proof คือสิ่งที่ปิด deal",
        "tension": "NF สร้าง emotional connection ดีมาก แต่ขาด proof points ที่ทำให้ลูกค้า justify ต่อตัวเองได้",
        "conflict_example": 'คุณ: "ลูกค้าคนหนึ่งบอกว่ามันเปลี่ยนชีวิตเลยนะ เธอ transform business ได้จริงๆ"\nลูกค้า: "ฟังดูดี"\nคุณ: "และอีกคนบอกว่าเขาไม่รู้จะทำยังไงถ้าไม่มี service นี้"\nลูกค้า: "อืม..."\nคุณ: "เราจะ transform คุณด้วยเหมือนกัน!"\nลูกค้า: "ขอคิดดูก่อนนะ"\n\nStory ดี แต่ไม่มี hard proof ให้ลูกค้า justify การตัดสินใจ',
        "why_fails": "NF บอกว่า value ดีแต่ไม่ให้ specific numbers หรือ proof points ที่ทำให้ลูกค้ารู้สึกว่า decision นี้ defensible",
        "recommended_example": 'คุณ: "ขอ share case ที่ specific ไหม ลูกค้าที่มี situation คล้ายคุณ ใน 90 วันแรก [specific result] และ ตลอด 6 เดือน [specific outcome] นี่คือ case study ที่มีตัวเลขจริง... คิดว่าสถานการณ์ของคุณ similar ไหม?"\nลูกค้า: "ใช่ คล้ายมากเลย"',
        "the_shift": "Story + Number ต้องมีทั้งคู่ — Story เปิดใจ Number ปิด deal",
    },
    ("SJ", "increase_value"): {
        "mbti_context": "SJ แสดง track record และ reliability ได้ดีมาก แต่บางทีพลาดตรงที่ไม่ได้ paint vision ว่าอนาคตจะดียังไง ลูกค้าบาง type ซื้อ future state ไม่ได้ซื้อ past performance",
        "tension": "SJ present proof of past แต่บางลูกค้าต้องการ vision of future ไม่ใช่แค่ track record",
        "conflict_example": 'คุณ: "เราทำงานกับ company แบบนี้มา 15 ปี มี certification ครบ และ 98% client retention"\nลูกค้า: "ฟังดู solid นะ"\nคุณ: "และ team เราผ่านการ training ครบทุก module"\nลูกค้า: "แต่อยากรู้ว่า จะทำให้ business ฉันเปลี่ยนยังไงบ้าง?"\nคุณ: "เราทำให้ client ทุกคนพอใจมาตลอด"\nลูกค้า: "ขอคิดดูก่อน"\n\nลูกค้าอยากเห็น future ไม่ใช่ past',
        "why_fails": "SJ ตอบคำถาม 'ทำไมต้องเลือกคุณ?' ด้วย past performance แต่บางลูกค้าถามว่า 'ฉันจะได้อะไร?' ซึ่งต้องการ answer เกี่ยวกับ future ของพวกเขา",
        "recommended_example": 'คุณ: "ขอ paint ภาพ 6 เดือนข้างหน้าให้ฟัง สมมติเราเริ่ม project นี้ด้วยกัน เดือน 1-2 จะเกิดอะไรขึ้น เดือน 3-4 คุณจะเริ่ม see [outcome] และ 6 เดือน คุณจะอยู่ในจุดที่ [vision ที่ specific] ภาพนี้ตรงกับสิ่งที่คุณ want ไหม?"\nลูกค้า: "ใช่ นั่นแหละที่ฉันต้องการ"',
        "the_shift": "ต้องทำทั้งสอง: proof from past + vision of future คนซื้อเมื่อ trust ว่าคุณทำได้ AND เห็นว่าชีวิตจะดียังไง",
    },
    ("SP", "increase_value"): {
        "mbti_context": "SP สร้าง excitement และ energy รอบๆ product ได้ดีมาก แต่บางทีขาด substance ที่ทำให้ enthusiasm คงอยู่หลัง meeting ต้องให้ทั้ง excitement สำหรับ emotional buy-in AND depth สำหรับ rational confirmation",
        "tension": "SP สร้าง excitement ดีมาก แต่ depth ไม่พอทำให้ enthusiasm หายหลัง meeting",
        "conflict_example": 'คุณ: "นี่มันเจ๋งมากเลย! ลองดูสิ!" [demo อย่าง energetic]\nลูกค้า: [excited] "ว้าว ดูดีมาก!"\n[หลัง meeting ลูกค้า googled เอง ไม่เจอ proof points ที่ต้องการ]\nลูกค้า: [cool down] "อ่า ขอ review อีกรอบก่อนนะ"\n[ไม่ตัดสินใจ]\n\nExcitement จริง แต่หายเร็วเพราะไม่มี substance รองรับ',
        "why_fails": "SP ทำให้ moment สนุกและ exciting แต่ customer decision มักเกิดหลัง meeting ตอนที่ excitement หายแล้ว ถ้าไม่มี substance ที่ solid มัน won't survive the reflection",
        "recommended_example": 'คุณ: [demo อย่าง energetic] "เจ๋งใช่ไหม? และที่ทำให้มัน reliable ไม่ใช่แค่ exciting คือ [specific proof] นี่คือ case ที่ [similar company] ทำแล้ว result คือ [numbers] อยากให้ [เปิด case study ให้ดู] ภาพรวมชัดขึ้นไหม?"',
        "the_shift": "Excitement เปิดใจ Substance ปิด deal — ต้องมีทั้งคู่ใน presentation เดียว",
    },

    # ═══════════════ upsell_expand ═══════════════
    ("NT", "upsell_expand"): {
        "mbti_context": "NT pitch upgrade ด้วย ROI logic ได้ดีมาก แต่ถ้า pitch ก่อนที่จะ establish ว่าลูกค้า happy กับ current product มันจะ sound ว่าคุณแค่อยากได้เงินมากขึ้น ต้องรอให้มี proof of success ก่อนแล้วค่อย expand",
        "tension": "NT pitch upgrade ด้วย logic ก่อนที่จะ validate ว่าลูกค้า satisfied กับ current solution",
        "conflict_example": 'ลูกค้า: [ใช้ product มาได้ 1 เดือน]\nคุณ: "ตอนนี้ ROI จาก basic plan ชัดแล้ว ลอง upgrade ไป premium ได้แล้ว จะได้ [features] เพิ่ม"\nลูกค้า: "เพิ่งซื้อมาเดือนเดียวเองนะ"\nคุณ: "แต่ถ้า calculate แล้ว premium จะ cost-effective กว่าที่ scale นี้"\nลูกค้า: "ขอ settle กับ current ก่อน"\n\nTiming ผิด ทำให้ดู sales-y มากกว่า advisory',
        "why_fails": "NT ฉลาดพอที่จะ see opportunity แต่ pitch ก่อน customer experience ทำให้ดูเหมือน money-motivated ไม่ใช่ customer-success motivated",
        "recommended_example": '[หลังลูกค้าใช้ไป 2-3 เดือน และแสดง satisfaction]\nคุณ: "ดีมากที่เห็นว่า [result ที่เกิด] จากสิ่งที่ใช้อยู่ ฉันสังเกตว่าตอนนี้คุณ scale ถึง [point] แล้ว ซึ่งตรงกับ scenario ที่ premium plan จะ unlock value มากกว่า อยากให้ดู breakdown ไหม?"\nลูกค้า: "โอ้ จริงเหรอ อยากรู้"',
        "the_shift": "Upsell ที่ดีเกิดหลัง success ไม่ใช่หลัง purchase — รอให้เขา win แล้วขยาย win นั้น",
    },
    ("NF", "upsell_expand"): {
        "mbti_context": "NF กลัวว่าการ upsell จะทำให้ดูเหมือน 'แค่อยากได้เงิน' แต่ถ้าคุณ genuinely เชื่อว่า upgrade จะ help เขามากขึ้น การไม่บอกเขาคือการ withhold สิ่งที่ดีจากเขา Upsell จาก care ไม่ใช่จาก commission",
        "tension": "NF กลัวว่า upsell = greedy จน ไม่ ask และลูกค้าพลาดโอกาสที่ดีกว่า",
        "conflict_example": 'ลูกค้า: "ฉัน love product นี้มาก ช่วยได้จริงๆ!"\nคุณ: [อยากเสนอ premium แต่กลัว awkward] "ดีมากเลย ยินดีที่ help ได้"\nลูกค้า: "ถ้ามีอะไร recommend ก็บอกได้นะ"\nคุณ: "ก็... ทุกอย่างดีอยู่แล้วนะ"\n[3 เดือนต่อมา ลูกค้า upgrade กับ competitor เพราะไม่รู้ว่าคุณมี option ดีกว่า]\n\nคุณกลัว awkward แต่ลูกค้าเสียโอกาส',
        "why_fails": "NF interpret 'don't want to seem pushy' ว่า 'don't mention it at all' แต่ถ้าลูกค้า love product อยู่แล้ว การแชร์ว่ามี option ที่ดีกว่าคือ caring ไม่ใช่ pushy",
        "recommended_example": 'ลูกค้า: "ฉัน love product นี้มาก ช่วยได้จริงๆ!"\nคุณ: "ดีใจมากเลย เห็นว่าคุณ getting value จาก [X] ฉัน genuinely คิดว่ามีวิธีที่คุณจะได้ประโยชน์มากขึ้นอีก ขอแชร์ได้ไหม? ไม่ต้อง decide ตอนนี้ แค่อยากให้รู้ว่ามี option"\nลูกค้า: "โอ้ ได้เลย tell me more"',
        "the_shift": "Frame upsell ว่า 'ฉัน care พอที่จะบอกคุณว่ามีวิธีที่ดีกว่า' ไม่ใช่ 'ฉัน want เงินมากขึ้น'",
    },
    ("SJ", "upsell_expand"): {
        "mbti_context": "SJ รอให้ถึง 'right moment' ที่ชัดเจนก่อนจะ upsell แต่ moment นั้นบางทีไม่มาด้วยตัวเอง ต้อง create มันด้วยการ review regularly และ note เมื่อลูกค้าถึง threshold ที่ upgrade จะ make sense",
        "tension": "SJ รอ perfect timing จน moment ผ่านไปและลูกค้าไปซื้อ upgrade จากที่อื่น",
        "conflict_example": "[ลูกค้าใช้ basic plan มา 6 เดือน ใกล้ limit แล้ว]\nคุณ: [รู้ แต่ยังไม่ mention เพราะรอให้ถึงเวลาที่ 'เหมาะสม']\n[ลูกค้า hit limit]\nลูกค้า: \"ระบบ cap แล้วนะ ทำไมไม่บอกก่อน?\"\nคุณ: \"โทษที ฉันก็เพิ่งรู้...\"\nลูกค้า: \"เสียเวลามาก ขอ switch provider ที่ proactive กว่านี้\"\n\nรอ perfect timing จน missed the moment",
        "why_fails": "SJ ไม่ชอบ 'interrupt' ลูกค้าโดยไม่จำเป็น แต่การ proactive บอก upgrade opportunity คือ good service ไม่ใช่ interruption",
        "recommended_example": '[monitor ลูกค้าถึง 70% ของ limit]\nคุณ: "ฉันสังเกตว่าคุณ reaching 70% ของ limit แล้ว ตามประสบการณ์ที่ rate นี้จะถึง limit ภายใน [X weeks] ขอ walk through upgrade options ก่อนถึง point นั้นได้ไหม?"\nลูกค้า: "โห ขอบคุณมากที่บอกก่อน ใช่ มา review กัน"',
        "the_shift": "Proactive upgrade conversation = good service ไม่ใช่ pushy sales — track usage และ initiate ก่อน ไม่ใช่หลัง",
    },
    ("SP", "upsell_expand"): {
        "mbti_context": "SP บางที ask for upgrade เร็วเกินไปหลังจาก initial sale ตาม excitement ของ moment แต่ลูกค้าต้อง experience ความสำเร็จจาก current purchase ก่อน ถึงจะ open ต่อ more รอให้เขา win แล้วค่อย expand win นั้น",
        "tension": "SP ตาม energy และ ask สำหรับ more เร็วเกินไปก่อนลูกค้า experience success",
        "conflict_example": '[ลูกค้าเพิ่ง sign up เมื่อวาน]\nคุณ: [excited] "ดีมากเลยที่เลือก plan นี้! แล้วคุณรู้ไหม premium plan มี [features] ที่จะ amazing มากกว่าอีก?"\nลูกค้า: "เพิ่งซื้อมาเมื่อวาน..."\nคุณ: "ก็แต่ถ้า upgrade ตอนนี้ จะได้ rate ที่ดีกว่า"\nลูกค้า: "ขอดูก่อนว่า basic ใช้เป็นยังไงก่อนนะ"\n\nToo early ทำให้ดูเหมือนไม่ได้แคร์ว่าเขาจะ succeed กับ product จริงๆ',
        "why_fails": "SP ตาม momentum แต่ upsell ก่อน success ทำให้ดูเหมือน greedy มากกว่า advisor",
        "recommended_example": '[รอจนลูกค้าใช้ได้ผลจริงๆ]\nลูกค้า: "ใช้ได้ดีมากเลย ชอบมาก!"\nคุณ: "เยี่ยมเลย! เห็นว่า [specific thing] ทำงานดี ตอนนี้ที่คุณ see value แล้ว อยากให้รู้ว่ามี option ที่จะ [specific uplift] ได้ อยากให้ฉัน walk through ไหม?"\nลูกค้า: "ได้เลย ตอนนี้ interested แล้ว"',
        "the_shift": "รอจน win แล้วค่อย upsell — 'ตอนนี้ที่เห็น value แล้ว มีวิธีที่จะ win มากขึ้นอีก' คือ timing ที่ถูกต้อง",
    },
}

HD_MONEY: dict[tuple[str, str], str] = {

    # close_deal
    ("Generator", "close_deal"): "Close ตอนที่ gut บอกว่า deal นี้ right ถ้าคุณ genuinely excited กับ outcome ของลูกค้า ความ authentic นั้นจะ come through ตอน ask อย่า force close deal ที่ตัวเองไม่ feel ว่า win-win",
    ("Manifesting Generator", "close_deal"): "ตอนเห็น buying signal ขยับเร็วเลย แต่ก่อน close ให้แน่ใจว่าทุกคนที่ต้อง know รู้แล้ว บางทีลูกค้ามี partner หรือ team ที่ต้อง loop in ก่อน — inform ก่อน finalize",
    ("Manifestor", "close_deal"): "บอกชัดเลยว่า 'ถ้าคุณ ready เราทำได้เลย' การ announce ว่าคุณ ready จะ move สร้าง clarity ที่ทำให้ลูกค้า decide ง่ายขึ้น",
    ("Projector", "close_deal"): "ก่อน close ตรวจสอบว่าลูกค้า fully understand และ comfortable จริงๆ ถามว่า 'มีอะไรที่ยังอยากให้ชัดขึ้นไหม?' Projector อ่านคนได้แม่น ใช้ gift นั้นตรวจสอบ readiness ก่อน ask",
    ("Reflector", "close_deal"): "อย่า rush ตัวเองให้ close ถ้า feel ว่า something is off ถ้า environment หรือ conversation รู้สึกไม่ right trust นั้น — deal ที่ดีจะ feel ดีตลอด ไม่ใช่แค่ในบางช่วง",

    # bargain_discount
    ("Generator", "bargain_discount"): "Negotiate จาก place ของความ genuine interest ใน outcome ที่ดีสำหรับทั้งคู่ ถ้า gut บอกว่า deal นี้ fair ก็ commit ถ้า feel ว่าไม่ fair บอกตรงๆ ว่า need อะไรจึงจะ yes",
    ("Manifesting Generator", "bargain_discount"): "คุณ move เร็วและ creative ใช้ energy นั้นใน negotiation — propose trade-offs ใหม่ๆ ที่คนอื่นไม่คิด แต่ก่อน commit ให้ inform ทุก stakeholder ก่อน",
    ("Manifestor", "bargain_discount"): "บอกตรงๆ ว่า budget คือเท่าไหร่และต้องการอะไร ไม่ต้องอ้อมค้อม Manifestor directness ใน negotiation มักได้ผลดีมาก เพราะ seller รู้ชัดว่าต้องทำอะไรเพื่อ close",
    ("Projector", "bargain_discount"): "อ่านสถานการณ์ก่อนว่า seller มี flexibility จริงๆ ไหม Projector เห็น dynamics ได้ชัด — ถ้าเห็นว่ามี room ค่อย ask ถ้าเห็นว่าไม่มี focus ที่ value proposition แทน",
    ("Reflector", "bargain_discount"): "สังเกตว่า negotiation environment รู้สึก collaborative หรือ adversarial ถ้า adversarial นั้นคือ signal ที่สำคัญ — deal ที่ start ด้วย friction มักจะมี friction ต่อไป",

    # handle_objections
    ("Generator", "handle_objections"): "ตอบ price objection จาก place ของ genuine belief ว่า product จะ help ถ้าคุณ truly believe มัน worth it ความ conviction นั้นจะ come through ถ้าไม่ believe จริงๆ ก็ไม่ควร push",
    ("Manifesting Generator", "handle_objections"): "Pivot เร็วตอนได้ยิน objection — อย่าติดอยู่กับ point เดิม สร้าง reframe ใหม่หรือ propose alternative ที่ address concern ได้ MG strength คือการเห็น multiple paths ใช้มันตรงนี้",
    ("Manifestor", "handle_objections"): "Address objection ตรงๆ อย่าอ้อมค้อม ถ้า concern valid ก็ acknowledge ถ้าไม่ valid ก็ explain ทำไม ความ directness ของ Manifestor ทำให้ลูกค้ารู้สึกว่าได้คุยกับคนที่ honest",
    ("Projector", "handle_objections"): "อ่านว่า objection ข้างใต้ จริงๆ คืออะไร Projector เห็น motivation ที่คนซ่อนไว้ได้ดี ถามคำถามที่ดีเพื่อ uncover real concern แล้ว address ตรงนั้น",
    ("Reflector", "handle_objections"): "สังเกตว่า objection เป็น real concern หรือเป็นแค่ habit ของการ negotiate Reflector mirror environment ได้ดี — ถ้ารู้สึกว่า objection ไม่ genuine อาจ reflect กลับว่า 'ดูเหมือนมี concern อื่นอยู่ด้วยใช่ไหม?'",

    # increase_value
    ("Generator", "increase_value"): "เล่าสิ่งที่คุณ genuinely excited กับ product ของคุณ ความ authentic enthusiasm เป็น value demonstration ที่ทรงพลังที่สุด คนซื้อจากคนที่ genuinely believe ใน product มากกว่า polished pitch",
    ("Manifesting Generator", "increase_value"): "Show multiple angles ของ value ได้เร็วมาก แต่ focus ที่ 2-3 points ที่ most relevant กับ customer คนนั้นโดยเฉพาะ ไม่ใช่ dump ทุก feature — MG speed เป็น asset แต่ needs direction",
    ("Manifestor", "increase_value"): "State value directly โดยไม่ over-qualify ความ confidence ของ Manifestor ใน delivery ทำให้ value statement มีน้ำหนัก บอกตรงๆ ว่า 'นี่คือ impact ที่คุณจะได้' ไม่ต้องอ้อม",
    ("Projector", "increase_value"): "อ่านว่าลูกค้า value อะไรจริงๆ แล้ว personalize value proposition ให้ตรงกับสิ่งนั้นโดยเฉพาะ Projector strength คือ reading people ใช้มันเพื่อ tailor message ไม่ใช่ generic pitch",
    ("Reflector", "increase_value"): "Reflect ว่าคุณเห็น value ในตัวลูกค้าและสถานการณ์ของเขาอย่างไร 'จากที่คุณเล่า ฉันเห็นว่า [insight]' — Reflector insight เกี่ยวกับ environment ของลูกค้ามักเป็น value ที่ unexpected มาก",

    # upsell_expand
    ("Generator", "upsell_expand"): "Upsell ตอนที่ gut บอกว่า upgrade จะ genuinely help ลูกค้ามากขึ้น ถ้า feel ว่ามัน right timing ให้ respond ต่อ feeling นั้น ถ้าไม่ feel รอก่อน ความ authenticity ของ timing สำคัญมาก",
    ("Manifesting Generator", "upsell_expand"): "ตอน see opportunity สำหรับ expansion inform ลูกค้าทันที แต่ give ข้อมูลครบก่อนที่จะ move เร็ว ลูกค้าต้องรู้สึกว่า you thought of them ไม่ใช่ you thought of revenue",
    ("Manifestor", "upsell_expand"): "เมื่อเห็น opportunity สำหรับ expansion บอกตรงๆ ว่าคุณเห็นอะไรและ recommend อะไร ความ directness ทำให้ลูกค้าเชื่อถือ recommendation มากกว่าการ soft-sell",
    ("Projector", "upsell_expand"): "รอให้ลูกค้าถามหรือแสดง signal ว่า ready ก่อน Projector upsell ที่ทรงพลังที่สุดคือตอนที่ลูกค้า come to you และถามว่า 'มีวิธีอื่นที่จะได้มากกว่านี้ไหม?' — build relationship ที่ดีจนถึง moment นั้น",
    ("Reflector", "upsell_expand"): "สังเกตว่าลูกค้าอยู่ในช่วง positive ของ cycle ไหม ตอนที่ environment ดี ลูกค้า receptive กับ expansion มากขึ้น Reflector timing ของการ upsell ตาม environment มักแม่นกว่า calendar",
}
