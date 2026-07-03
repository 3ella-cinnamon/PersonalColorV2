"""Sub-goal decision tips: specific actionable advice per MBTI category and HD type."""
from typing import Optional

SUB_GOAL_TO_MAIN: dict[str, str] = {
    "get_buyin":           "work",
    "build_trust_work":    "work",
    "secure_agreement":    "work",
    "drive_urgency":       "work",
    "win_commitment":      "work",
    "close_deal":          "money",
    "bargain_discount":    "money",
    "handle_objections":   "money",
    "increase_value":      "money",
    "upsell_expand":       "money",
    "create_attraction":   "relationship",
    "build_connection":    "relationship",
    "deepen_trust":        "relationship",
    "define_relationship": "relationship",
    "sustain_bond":        "relationship",
}

MBTI_CATEGORY: dict[str, str] = {
    "INTJ": "NT", "INTP": "NT", "ENTJ": "NT", "ENTP": "NT",
    "INFJ": "NF", "INFP": "NF", "ENFJ": "NF", "ENFP": "NF",
    "ISTJ": "SJ", "ISFJ": "SJ", "ESTJ": "SJ", "ESFJ": "SJ",
    "ISTP": "SP", "ISFP": "SP", "ESTP": "SP", "ESFP": "SP",
}

MBTI_TIPS: dict[str, dict[str, str]] = {
    "NT": {
        "communication_pitching":      "Lead with your conclusion, not your reasoning chain — state the outcome first, then offer the logic. Executives decide on direction, not derivations.",
        "productivity_time":           "Block 90-minute deep-work windows and treat interruptions as system bugs — log them, then eliminate their root cause.",
        "career_growth":               "Identify one adjacent skill that makes you irreplaceable in 18 months and invest 20 minutes daily — compounding beats sprinting.",
        "job_security":                "Make your thinking visible and transferable — document your frameworks, not just your outputs. Systems outlast individuals.",
        "teamwork_stakeholders":       "Over-communicate your reasoning, not just your conclusions. Others follow logic better when they see your steps, not just your destination.",
        "increasing_income":           "Map the exact skill gap between your current income and your target, then close it systematically over 90 days.",
        "saving_budgeting":            "Automate transfers to savings on payday — your system runs without willpower and decision fatigue never touches your reserves.",
        "investing_wealth":            "Research asymmetric bets where downside is capped and upside is open. Build a thesis, commit to it, review quarterly — not daily.",
        "financial_security":          "Build a 6-month expense reserve in a separate account. Treat it as infrastructure, not savings — never touch it for wants.",
        "financial_freedom":           "Model your exact number — the investment portfolio that generates your baseline income passively. Then reverse-engineer the savings rate needed.",
        "communication_understanding": "State your emotional need once, clearly, without softening it. 'I need X' lands better than 'it would be nice if maybe you could.'",
        "love_connection":             "Schedule intentional connection time — it doesn't feel romantic to plan, but showing up consistently signals priority better than grand gestures.",
        "trust_emotional_security":    "Consistency in small promises builds trust faster than grand gestures. Do exactly what you said, every time, even for minor things.",
        "work_life_balance":           "Create a hard-stop ritual that signals end-of-work to your nervous system — a physical action, not just closing a laptop.",
        "emotional_healing":           "Journal your thought loops externally to make them visible enough to analyze. Write the recurring pattern, then question its core premise.",
    },
    "NF": {
        "communication_pitching":      "Anchor your pitch in shared values and human impact before you touch numbers. One real story makes data feel alive — lead with it.",
        "productivity_time":           "Your focus surges when work feels meaningful. Write one sentence connecting today's task list to your larger purpose before you start.",
        "career_growth":               "Look for roles where your people insight is treated as strategy, not soft skill. Seek sponsors who name you in rooms — not only mentors.",
        "job_security":                "Deepen your relationship capital — people protect colleagues they feel loyal to. Be the person who listens and then follows through.",
        "teamwork_stakeholders":       "Use your natural empathy to translate between stakeholders. The person who makes everyone feel heard becomes indispensable.",
        "increasing_income":           "Identify the intersection of what you're uniquely good at and what someone pays a premium for — package your insight, not your time.",
        "saving_budgeting":            "Name your savings goals emotionally — 'freedom fund' lands better than 'savings account.' Meaning sustains discipline when motivation fades.",
        "investing_wealth":            "Invest in alignment with your values — sustained conviction holds through volatility better than pure math when markets get ugly.",
        "financial_security":          "Financial security is emotional safety for you. Name the specific number that would feel like 'enough' — then build toward it deliberately.",
        "financial_freedom":           "Freedom for you is creative autonomy, not just early retirement. Design income streams that fund the work you'd do regardless.",
        "communication_understanding": "Ask before advising — 'do you want input or just to vent?' buys enormous goodwill and prevents the most common connection breakdown.",
        "love_connection":             "Your deepest connection comes from being fully seen. Risk vulnerability in one small, specific way this week — share one real fear.",
        "trust_emotional_security":    "Name your emotional needs explicitly — people who love you can't meet needs they don't know exist. 'When X happens, I need Y' is a gift.",
        "work_life_balance":           "Protect personal time with the same firmness you protect commitments to others. 'I have a prior commitment' applies to commitments to yourself.",
        "emotional_healing":           "Apply the compassion you'd give a close friend directly to your own situation right now — your empathy for yourself is the gap to close.",
    },
    "SJ": {
        "communication_pitching":      "Prepare your evidence before the room — data, precedent, and a clear process. For your profile, reliability IS the most compelling pitch.",
        "productivity_time":           "Time-block with 15-minute buffers between tasks and review your list the night before so you wake up already knowing your first move.",
        "career_growth":               "Volunteer for high-visibility projects that let you demonstrate reliability at scale, then document your results in specific, concrete numbers.",
        "job_security":                "Become the institutional memory — know the processes, the history, the compliance requirements. That depth is the deepest job security there is.",
        "teamwork_stakeholders":       "Send the meeting agenda 24 hours ahead. Follow up with clear owners and deadlines. Reliability at this level builds trust faster than charisma.",
        "increasing_income":           "Research the salary band for your exact role and ask with specific documented evidence. Ask annually — not only when you're already desperate.",
        "saving_budgeting":            "Track every spending category for 30 days before cutting anything. Data first, decisions second — you'll spot the real leaks clearly.",
        "investing_wealth":            "Index funds with consistent monthly contributions beat market timing for your profile. Start with low-cost broad-market exposure and stay consistent.",
        "financial_security":          "Ensure insurance coverage, emergency fund, and estate basics are locked in before optimizing for yield. Foundation before return.",
        "financial_freedom":           "Financial freedom is earned through consistency over decades — maximize tax-advantaged accounts annually. Boring is winning for your profile.",
        "communication_understanding": "Schedule regular check-ins — a 10-minute daily debrief builds more mutual understanding over time than sporadic deep conversations.",
        "love_connection":             "Consistency is your love language to give and receive. Show up reliably in small daily ways — they accumulate into deep, lasting security.",
        "trust_emotional_security":    "Trustworthiness is your natural currency. Make it visible by following through on the small things other people conveniently forget.",
        "work_life_balance":           "Draw one clear boundary per week — leave at a specific time, keep one day device-free, protect one meal. Pick it, defend it, repeat.",
        "emotional_healing":           "Healing happens through structure for you — create a small daily ritual (10 minutes, same time, same space) that belongs entirely to your inner world.",
    },
    "SP": {
        "communication_pitching":      "Skip the long deck — open with the result, show your proof-of-concept in 3 minutes, then ask for the specific next step.",
        "productivity_time":           "Work in 25–50 minute sprints with physical breaks. Batch admin into one daily slot so your deep work windows stay uninterrupted.",
        "career_growth":               "Bias toward hands-on stretch projects over credentials — your portfolio of visible, completed work grows careers faster than certificates.",
        "job_security":                "Keep your skills current and your external network active. The optionality of being hireable elsewhere is the truest form of job security.",
        "teamwork_stakeholders":       "Step into conflict early — your pragmatism makes you a natural neutral party when tensions rise before they harden into sides.",
        "increasing_income":           "Test one income stream with the lowest possible startup cost before planning anything elaborate — fast iteration beats long preparation.",
        "saving_budgeting":            "Cut one specific thing today rather than building an elaborate plan — quick wins sustain momentum better than a perfect budget document.",
        "investing_wealth":            "Open one real position today rather than researching indefinitely. Small real stakes teach more than any simulation.",
        "financial_security":          "Keep a small liquid fund always accessible — the security of knowing you can handle a surprise is worth more than the best interest rate.",
        "financial_freedom":           "Define what freedom looks like for you today, not in 30 years. Build a life you'd love at every stage, not just at the finish line.",
        "communication_understanding": "Lead with what you observed before what you concluded. 'I noticed you went quiet' opens dialogue — 'you were upset' closes it.",
        "love_connection":             "Plan a shared physical experience — activities build connection faster for you than extended conversations. Do something new together.",
        "trust_emotional_security":    "Show up in moments of crisis — your problem-solving nature makes you uniquely valuable when security is actually threatened.",
        "work_life_balance":           "Presence is your strength — when you're home, be home. Physical recovery (moving, building, playing) restores you faster than passive rest.",
        "emotional_healing":           "Physical movement is your fastest path to emotional release. Run, train, build — your body processes what your mind loops on endlessly.",
    },
}

HD_TIPS: dict[str, dict[str, str]] = {
    "Generator": {
        "communication_pitching":      "Wait for the genuine question, then respond with full energy — your authentic enthusiasm is more persuasive than any rehearsed slide.",
        "productivity_time":           "Track which tasks make you say 'uh-huh' vs. which drain you — concentrate your hardest work in windows of genuine interest.",
        "career_growth":               "Let opportunities respond to your real interests — the work you love naturally attracts the recognition that grows careers.",
        "job_security":                "Sustainable energy around your work is itself a signal — people who love what they do are rarely the first to be let go.",
        "teamwork_stakeholders":       "Share what genuinely excites you about the project — your authentic enthusiasm is contagious and rallies the team without effort.",
        "increasing_income":           "Increase income by doubling down on work that truly energizes you — you're most productive and most valuable in that zone.",
        "saving_budgeting":            "Automate what you can — your energy is far better spent on satisfying work than on manual expense tracking.",
        "investing_wealth":            "Invest in industries you genuinely respond to — you'll monitor them naturally and won't miss warning signs the way you would with obligatory positions.",
        "financial_security":          "A buffer lets you wait for work that truly resonates — it means you can say no out of preference rather than yes out of fear.",
        "financial_freedom":           "Freedom means doing only work that lights you up. Build passive income that covers your baseline — then every yes becomes a genuine choice.",
        "communication_understanding": "Respond honestly when asked how you feel — your gut response is data your partner needs, not a reaction to manage or suppress.",
        "love_connection":             "Let connection happen in response to what genuinely delights you — your authentic enthusiasm is magnetic and draws love naturally toward you.",
        "trust_emotional_security":    "When you genuinely agree, say so fully and clearly. When you don't, a clear 'no' is far kinder than a slow, hedged 'yes.'",
        "work_life_balance":           "If work is genuinely satisfying, some blur is natural — but ensure at least one daily activity that has nothing to do with output.",
        "emotional_healing":           "Healing happens through doing for you, not analyzing. Find what feels satisfying to your body today and follow it, without justification.",
    },
    "Manifesting Generator": {
        "communication_pitching":      "Trim your pitch to the 3 strongest points — your energy peaks in the first 5 minutes, so use it before you naturally switch tracks.",
        "productivity_time":           "Commit each day to one primary output — everything else is secondary. Your multi-track nature is an asset, not a license to scatter.",
        "career_growth":               "Make your cross-functional speed visible — write brief, regular updates that show your output across multiple domains.",
        "job_security":                "Be known across more than one team or project. Multi-purpose people are more resilient when roles are eliminated.",
        "teamwork_stakeholders":       "Brief your team when you change direction — what feels like natural speed to you reads as chaos to others. A quick update resets that.",
        "increasing_income":           "Package your multi-skill range into a single offer — one project using 3 of your skills is worth more than three separate single-skill gigs.",
        "saving_budgeting":            "Simplify your budget to 3 categories: essentials, savings, guilt-free spending. Complexity in budgeting kills follow-through for MGs.",
        "investing_wealth":            "Diversify across your genuine areas of interest — your multi-domain awareness is a portfolio advantage most people don't naturally have.",
        "financial_security":          "Your income often comes in bursts — move a fixed percentage of every large payment into a separate stability fund to smooth it out.",
        "financial_freedom":           "Design freedom as multi-stream income — you don't thrive on a single source anyway. Multiple streams match your multi-track nature perfectly.",
        "communication_understanding": "Slow your verbal pace in important conversations — your mind processes faster than others speak. Wait for the full sentence before responding.",
        "love_connection":             "Be present in focused bursts of complete attention — your partner needs quality over duration. 20 minutes fully present beats 2 hours half-there.",
        "trust_emotional_security":    "Communicate your pivots before your partner has to ask — predictable updates build the trust your natural pace can otherwise erode.",
        "work_life_balance":           "Designate specific spaces as work-free and enforce them. Your multi-track nature makes every hour feel like potential work time — break that pattern.",
        "emotional_healing":           "Give yourself permission to stop mid-process — abandoning what no longer works is healthy course correction for your type. Trust it.",
    },
    "Manifestor": {
        "communication_pitching":      "State your idea with authority early — inform, don't ask permission. Follow with 'here's specifically what I need from you' to close the loop.",
        "productivity_time":           "Initiate your top priority before anyone asks anything of you today — once your momentum is set, the rest of the day flows behind it.",
        "career_growth":               "Seek roles with genuine autonomy and real impact. Propose new initiatives rather than waiting for a career path to be designed for you.",
        "job_security":                "Inform your manager of your wins before someone else frames the narrative. Proactive visibility is your protection — silence creates vulnerability.",
        "teamwork_stakeholders":       "Inform before you move — a brief heads-up before a significant action prevents the resentment that quietly slows teams and kills trust.",
        "increasing_income":           "Initiate the income conversation directly — propose the raise, pitch the project, name your rate first. Every day you wait costs you money.",
        "saving_budgeting":            "Set your budget parameters once with strong rules, then let it run. Check monthly, not daily — you are not built for micro-managing yourself.",
        "investing_wealth":            "Make bold decisions after research — but inform your financial advisor or partner before moving significant capital. Surprises erode trust.",
        "financial_security":          "Security lets you initiate from strength, not desperation. Fund your independence reserve before any other financial goal.",
        "financial_freedom":           "Freedom for you means impact without friction. Build enough independence to act without approval from anyone or any financial constraint.",
        "communication_understanding": "Before a hard truth, say: 'I want to share something directly — is now a good moment?' This one move dramatically reduces resistance.",
        "love_connection":             "Initiate affection and closeness deliberately — your partner cannot always tell you need connection if you don't reach out first.",
        "trust_emotional_security":    "Inform consistently, even when updates feel minor — your silence reads as withdrawal to people who care about you.",
        "work_life_balance":           "Apply your initiating nature to personal life — plan the trip, propose the date, initiate the shutdown. Don't wait for permission to rest.",
        "emotional_healing":           "Anger signals that something is blocking your nature. Name what's constraining you specifically, then decide: inform, change it, or leave it.",
    },
    "Projector": {
        "communication_pitching":      "Only pitch when genuinely invited or explicitly asked. When the invitation comes, go deep — your insight is the pitch; don't dilute it with filler.",
        "productivity_time":           "Work in focused 3–4 hour maximum windows. Build in more recovery than you think you need — rest is not a reward, it is your productivity.",
        "career_growth":               "You grow fastest when recognized and invited forward. Cultivate relationships with people who see your depth — they open the right doors.",
        "job_security":                "Your security comes from being the person who sees what others consistently miss. Invest in 1-on-1 relationships with key decision-makers.",
        "teamwork_stakeholders":       "Ask guiding questions rather than directing — 'what do you think is really happening here?' gets more buy-in than a statement does.",
        "increasing_income":           "Price your guidance, not your hours. Your insight is the value — charge for outcomes and transformations, not time spent.",
        "saving_budgeting":            "Protect your discretionary fund for quality over quantity — one excellent restorative experience returns more than ten cheap ones.",
        "investing_wealth":            "Invest deeply in assets you genuinely understand — your strength is insight, not volume. Quality concentrated positions suit you better than broad passive-only.",
        "financial_security":          "Build a fund specifically for unscheduled recovery time. Rest is not a luxury for Projectors — it is the foundation of your next contribution.",
        "financial_freedom":           "Freedom means working by invitation only. Build toward financial independence that lets you wait for the right invitations without desperation.",
        "communication_understanding": "You often see what the other person needs before they do. Ask a question to guide them there — 'what do you think is really happening?' — rather than stating it.",
        "love_connection":             "Receive love by allowing others to support you without deflecting — you give so much guidance; practice accepting care as deeply as you offer it.",
        "trust_emotional_security":    "Trust builds fastest when you ask before advising — 'can I share what I'm observing?' signals respect and dramatically lowers resistance.",
        "work_life_balance":           "Rest is non-negotiable — not a reward for productivity but a baseline requirement. Schedule recovery before you schedule any output.",
        "emotional_healing":           "Bitterness signals over-giving without recognition. Stop, rest fully, and wait for genuine appreciation before giving again — the pause is healthy.",
    },
    "Reflector": {
        "communication_pitching":      "Sample the room before committing to your angle — the approach that resonates with this group today may differ from what worked last week.",
        "productivity_time":           "Protect your physical environment ruthlessly — a chaotic space scatters your output. Consistency in your setup sustains focus over time.",
        "career_growth":               "Prioritize team health and environment over titles — where you work matters more than what you're called. Your peak emerges in healthy cultures.",
        "job_security":                "You often sense organizational instability before it surfaces in data — act on what you sense early. Your perception is your competitive advantage.",
        "teamwork_stakeholders":       "Name what you're absorbing in group settings: 'I'm noticing tension around X — should we address it?' Your reflection is data the team needs.",
        "increasing_income":           "Sample different income models over a full lunar cycle before committing. The right model will feel clear once the environmental noise settles.",
        "saving_budgeting":            "Wait 48 hours on impulsive purchases — environmental triggers drive your spending more than actual need. The urge rarely survives the pause.",
        "investing_wealth":            "Don't invest during emotionally turbulent periods. Wait for a clear, calm window — your best financial decisions reliably come from stillness.",
        "financial_security":          "Create financial buffers that give you time — rushed financial decisions rarely serve you. Your clarity comes with space and patience.",
        "financial_freedom":           "Freedom is environmental flexibility for you. Build toward being able to change your setting freely — your best self emerges in the right place.",
        "communication_understanding": "Share what you've been absorbing from the relationship: 'Lately I've been sensing X — I think it's coming from Y.' Your reflections are valuable data.",
        "love_connection":             "Notice how you consistently feel after time with someone. Sustained joy over multiple encounters is the clearest signal that the connection is right.",
        "trust_emotional_security":    "Name the conditions that make you feel safe and ask for them directly — your emotional security is deeply tied to your environment.",
        "work_life_balance":           "Daily solitude and time in nature are not optional — they are how you decompress what you've absorbed from others. Protect this time as sacred.",
        "emotional_healing":           "Disappointment is your emotional signal. Rather than pushing through, take your full lunar cycle to evaluate any significant change — clarity will come.",
    },
}


def _mbti_category(mbti: str) -> str:
    return MBTI_CATEGORY.get(mbti.upper(), "NT")


def get_sub_goal_tips(
    mbti: str,
    hd_type: Optional[str],
    sub_goal: str,
) -> tuple[str, str]:
    """Return (mbti_tip, hd_tip) for the given MBTI + HD + sub-goal combination."""
    cat      = _mbti_category(mbti)
    mbti_tip = MBTI_TIPS.get(cat, {}).get(sub_goal, "")
    hd_tip   = HD_TIPS.get(hd_type, {}).get(sub_goal, "") if hd_type else ""
    return mbti_tip, hd_tip


def main_goal_for(sub_goal: str) -> str:
    """Map a sub-goal ID to its parent main goal ID."""
    return SUB_GOAL_TO_MAIN.get(sub_goal, "work")
