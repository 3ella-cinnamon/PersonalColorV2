"""Seed script: creates tables and populates criteria + scenario rows.

Usage:
    python seed.py            # creates tables + seeds (idempotent)
    python seed.py --reset    # drops criteria/scenario rows first, then re-seeds

Schema migration note:
    If you're upgrading from a previous version that didn't have the 'goal'
    column or the mbti_hd_scenarios table, run:
        python seed.py --migrate --reset
    This adds the new columns to existing tables before re-seeding.

User accounts and profiles are NEVER touched by this script.
"""

import sys
from typing import Optional

from sqlalchemy import inspect, text

from core.database import Base, SessionLocal, engine
from models.orm import (
    AgentMemory,
    HdCriterion,
    HdTypeProfile,
    MbtiCriterion,
    MbtiHdScenario,
    MbtiTypeProfile,
    PersonalColorProfile,
    Recommendation,
    RecommendationFeedback,
)


# ── MBTI criteria ──────────────────────────────────────────────────────────────
# (mbti_type, preference, decision_text, weight, goal)
# goal=None -> applies to every goal; goal='work'/'money'/'relationship' -> goal-specific.

MBTI_SEED: list[tuple[str, str, str, float, Optional[str]]] = [

    # ── INTJ ──────────────────────────────────────────────────────────────────
    ("INTJ", "decision_making",
     "Trust your initial Ni hit. Refine with Te logic, but don't relitigate the same call twice.",
     1.0, None),
    ("INTJ", "energy",
     "Front-load deep work in the morning. Treat afternoon meetings as a tax — minimize them.",
     0.9, None),
    ("INTJ", "communication",
     "Lead with the conclusion, then the reasoning. Skip the preamble.",
     0.8, None),
    ("INTJ", "work_guidance",
     "Map the outcome first, then the minimum viable path. You don't need to solve every edge case before starting.",
     1.0, "work"),
    ("INTJ", "money_guidance",
     "Run the numbers with Te precision, then let Ni gut-check the direction. If both say yes, move.",
     1.0, "money"),
    ("INTJ", "relationship_guidance",
     "Schedule 1:1 depth conversations deliberately — you need quality, not frequency. One real talk beats five surface ones.",
     1.0, "relationship"),

    # ── INTP ──────────────────────────────────────────────────────────────────
    ("INTP", "decision_making",
     "Set a hard deadline before you analyze — otherwise the analysis never closes.",
     1.0, None),
    ("INTP", "energy",
     "Protect long uninterrupted blocks. Context-switching costs you twice what it costs others.",
     0.9, None),
    ("INTP", "communication",
     "State your conclusion, then offer the proof. The listener needs the destination before the map.",
     0.8, None),
    ("INTP", "work_guidance",
     "Timeboxed sprints work better than open-ended analysis. Set a timer, then ship the 80% solution.",
     1.0, "work"),
    ("INTP", "money_guidance",
     "Model the math, set your confidence threshold (80% is enough), then act. Don't wait for certainty.",
     1.0, "money"),
    ("INTP", "relationship_guidance",
     "Listen to completion before analyzing. Your pattern-matching can cut people off before they feel heard.",
     1.0, "relationship"),

    # ── ENTJ ──────────────────────────────────────────────────────────────────
    ("ENTJ", "decision_making",
     "Decide fast, adjust faster. Speed of correction beats accuracy of first call.",
     1.0, None),
    ("ENTJ", "energy",
     "Protect strategic-thinking blocks. Running meetings all day is management, not leadership.",
     0.9, None),
    ("ENTJ", "communication",
     "State the outcome you want first, then ask for what you need to get there.",
     0.85, None),
    ("ENTJ", "work_guidance",
     "Assign ownership with a named deadline before tactics. System before execution, always.",
     1.0, "work"),
    ("ENTJ", "money_guidance",
     "Calculate downside before upside. Your drive can skip the risk math — don't let it.",
     1.0, "money"),
    ("ENTJ", "relationship_guidance",
     "Ask one genuine question and wait for the full answer before responding. Your instinct to direct can silence others.",
     1.0, "relationship"),

    # ── ENTP ──────────────────────────────────────────────────────────────────
    ("ENTP", "decision_making",
     "Pick the option that keeps the most doors open early; close them only when forced.",
     1.0, None),
    ("ENTP", "energy",
     "Use morning for divergent ideation, afternoon for execution. Do not flip the order.",
     0.9, None),
    ("ENTP", "communication",
     "Lead with your strongest argument, not your most interesting one. Your audience isn't energized by uncertainty the way you are.",
     0.8, None),
    ("ENTP", "work_guidance",
     "Pair with someone who closes. Your job is to open the right doors; let others lock them.",
     1.0, "work"),
    ("ENTP", "money_guidance",
     "After the brainstorm, pick ONE financial move and commit to it for 90 days before evaluating.",
     1.0, "money"),
    ("ENTP", "relationship_guidance",
     "Slow down when the other person goes quiet — that's when the real conversation starts.",
     1.0, "relationship"),

    # ── INFJ ──────────────────────────────────────────────────────────────────
    ("INFJ", "decision_making",
     "If your gut says no but the spreadsheet says yes, take 24 h before deciding.",
     1.0, None),
    ("INFJ", "energy",
     "Schedule recovery before you need it. Burnout for INFJs is a cliff, not a slope.",
     0.95, None),
    ("INFJ", "communication",
     "Write your thoughts before sharing in group settings. The gap between inner clarity and verbal expression is wider than you think.",
     0.8, None),
    ("INFJ", "work_guidance",
     "Attach the task to its long-term meaning. Work without purpose drains you faster than any workload.",
     1.0, "work"),
    ("INFJ", "money_guidance",
     "Trust your Ni read on value trends, then verify with real data. Your intuition is often right; overconfidence is the risk.",
     1.0, "money"),
    ("INFJ", "relationship_guidance",
     "Speak your own needs first, then address the other person's. Self-erasure doesn't help anyone long-term.",
     1.0, "relationship"),

    # ── INFP ──────────────────────────────────────────────────────────────────
    ("INFP", "decision_making",
     "Align the choice with a value you can name in one sentence. If you can't, it's not your call to make yet.",
     1.0, None),
    ("INFP", "energy",
     "Protect creative/reflective morning time. Don't let others colonize your best thinking hours.",
     0.9, None),
    ("INFP", "communication",
     "Write before you speak on hard topics. The clarity gap is large for you.",
     0.85, None),
    ("INFP", "work_guidance",
     "Connect the task to something you genuinely care about. Motivation through values outperforms discipline.",
     1.0, "work"),
    ("INFP", "money_guidance",
     "Separate 'what I feel good about' from 'what makes financial sense.' They can coexist — but check both.",
     1.0, "money"),
    ("INFP", "relationship_guidance",
     "Say the hard thing once, clearly, then give space. Repeated gentle hints rarely land.",
     1.0, "relationship"),

    # ── ENFJ ──────────────────────────────────────────────────────────────────
    ("ENFJ", "decision_making",
     "Check that 'helping' isn't a substitute for your own decision. Make yours first.",
     1.0, None),
    ("ENFJ", "energy",
     "Limit the number of people you carry today to three. Past three, you give worse to everyone.",
     0.9, None),
    ("ENFJ", "communication",
     "Be direct about disagreement. Your warmth can make people miss that you've said no.",
     0.85, None),
    ("ENFJ", "work_guidance",
     "Lead with the shared goal, then assign ownership. People follow you because of vision, not authority.",
     1.0, "work"),
    ("ENFJ", "money_guidance",
     "Don't optimize for what feels good for the group. Run the numbers for yourself first.",
     1.0, "money"),
    ("ENFJ", "relationship_guidance",
     "Your empathy is a gift — give it to yourself first today. Then others.",
     1.0, "relationship"),

    # ── ENFP ──────────────────────────────────────────────────────────────────
    ("ENFP", "decision_making",
     "Pick the option that excites you AND has a stakeholder who will hold you to it. Excitement alone fades.",
     1.0, None),
    ("ENFP", "energy",
     "Front-load social ideation. Protect afternoon for execution — phone face-down.",
     0.9, None),
    ("ENFP", "communication",
     "Compress before you deliver. Three points, max. Your audience can't hold seven.",
     0.8, None),
    ("ENFP", "work_guidance",
     "Commit to one thing publicly before starting the next. You generate better than you complete.",
     1.0, "work"),
    ("ENFP", "money_guidance",
     "Automate savings so excitement-based spending doesn't derail the plan.",
     1.0, "money"),
    ("ENFP", "relationship_guidance",
     "Slow down and let the other person lead the conversation for one full exchange. Then bring your energy.",
     1.0, "relationship"),

    # ── ISTJ ──────────────────────────────────────────────────────────────────
    ("ISTJ", "decision_making",
     "Use precedent as the default; deviate only with a written reason.",
     1.0, None),
    ("ISTJ", "energy",
     "Predictable cadence beats heroics. Same start time, same end time, same review ritual.",
     0.9, None),
    ("ISTJ", "communication",
     "Lead with the facts, then the recommendation. Skip the feelings track unless explicitly asked.",
     0.8, None),
    ("ISTJ", "work_guidance",
     "Document as you go. Future-you will thank present-you every single time.",
     1.0, "work"),
    ("ISTJ", "money_guidance",
     "Consistent small contributions outperform periodic large ones. Trust the system you built.",
     1.0, "money"),
    ("ISTJ", "relationship_guidance",
     "Ask one question about the other person's inner state before moving to facts. It changes the whole conversation.",
     1.0, "relationship"),

    # ── ISFJ ──────────────────────────────────────────────────────────────────
    ("ISFJ", "decision_making",
     "Ask: 'If I weren't trying to keep the peace, what would I choose?' Choose that.",
     1.0, None),
    ("ISFJ", "energy",
     "Block one solo hour daily. It's not optional — it's how you pay your own bills first.",
     0.9, None),
    ("ISFJ", "communication",
     "State your need directly once, without apology. If it wasn't heard, say it again differently — not more softly.",
     0.85, None),
    ("ISFJ", "work_guidance",
     "Delegate one thing today that you've been holding. Your thoroughness is valuable; your bottlenecking isn't.",
     1.0, "work"),
    ("ISFJ", "money_guidance",
     "Review your recurring expenses monthly. Your loyalty to the familiar can cost real money.",
     1.0, "money"),
    ("ISFJ", "relationship_guidance",
     "Your care is most impactful when it's wanted, not assumed. Ask what the other person actually needs.",
     1.0, "relationship"),

    # ── ESTJ ──────────────────────────────────────────────────────────────────
    ("ESTJ", "decision_making",
     "Commit publicly with a deadline. Your follow-through compounds when others are watching.",
     1.0, None),
    ("ESTJ", "energy",
     "Block time for thinking that isn't meeting-shaped. Strategy requires solitude.",
     0.9, None),
    ("ESTJ", "communication",
     "Lead with the plan, the owner, and the date. Skip the why unless asked.",
     0.85, None),
    ("ESTJ", "work_guidance",
     "Clarify accountability before starting any project. Vague ownership is your biggest execution risk.",
     1.0, "work"),
    ("ESTJ", "money_guidance",
     "Run the ROI before committing resources. Your action instinct can move before the math is done.",
     1.0, "money"),
    ("ESTJ", "relationship_guidance",
     "Listen for what isn't being said. Your efficiency instinct can shortcut past someone's actual message.",
     1.0, "relationship"),

    # ── ESFJ ──────────────────────────────────────────────────────────────────
    ("ESFJ", "decision_making",
     "Separate 'what's right for the group' from 'what keeps everyone comfortable.' They diverge often.",
     1.0, None),
    ("ESFJ", "energy",
     "Cap caretaking time; protect 90 minutes for your own work first.",
     0.9, None),
    ("ESFJ", "communication",
     "Be direct about what you want. Hinting rarely works as well as asking.",
     0.85, None),
    ("ESFJ", "work_guidance",
     "Volunteer for the visible role, not just the support role. Your contribution deserves credit.",
     1.0, "work"),
    ("ESFJ", "money_guidance",
     "Make at least one financial decision purely for yourself today, not for the group.",
     1.0, "money"),
    ("ESFJ", "relationship_guidance",
     "You give well — practice receiving today. Let someone do something for you.",
     1.0, "relationship"),

    # ── ISTP ──────────────────────────────────────────────────────────────────
    ("ISTP", "decision_making",
     "Touch the problem before deciding. One real attempt beats an hour of theorizing.",
     1.0, None),
    ("ISTP", "energy",
     "Rotate tasks every 90 min. Variety is your fuel, not a distraction.",
     0.85, None),
    ("ISTP", "communication",
     "Give one more sentence of context than feels necessary. Your efficiency reads as curt to others.",
     0.8, None),
    ("ISTP", "work_guidance",
     "Tackle the hardest technical constraint first. Once that's solved, the rest is execution.",
     1.0, "work"),
    ("ISTP", "money_guidance",
     "Test your financial assumption on a small scale before full commitment.",
     1.0, "money"),
    ("ISTP", "relationship_guidance",
     "Show up in practical ways, then verbalize the intention. Actions land — but saying it once amplifies them.",
     1.0, "relationship"),

    # ── ISFP ──────────────────────────────────────────────────────────────────
    ("ISFP", "decision_making",
     "Choose the option that feels right in your body, not the one that sounds best on paper.",
     1.0, None),
    ("ISFP", "energy",
     "Sensory environment matters more for you than for most. Fix the room before fixing the work.",
     0.85, None),
    ("ISFP", "communication",
     "Write it if you can't say it. Your written expression often outperforms your verbal.",
     0.8, None),
    ("ISFP", "work_guidance",
     "Work in short focused bursts with sensory breaks. Quality over sustained grind.",
     1.0, "work"),
    ("ISFP", "money_guidance",
     "Check if the purchase aligns with your actual values, not an aspirational identity.",
     1.0, "money"),
    ("ISFP", "relationship_guidance",
     "Your presence is your gift. You don't need the perfect words — just be fully there.",
     1.0, "relationship"),

    # ── ESTP ──────────────────────────────────────────────────────────────────
    ("ESTP", "decision_making",
     "Make the call in the room with full info, not later in your head with half of it.",
     1.0, None),
    ("ESTP", "energy",
     "Stack high-stakes activity in the first 4 hours. After that, your edge softens.",
     0.9, None),
    ("ESTP", "communication",
     "Lead with the impact, not the story. Your audience decides in the first sentence.",
     0.85, None),
    ("ESTP", "work_guidance",
     "Take the action, then document it. In-the-moment decisions are your strength — just leave a trail.",
     1.0, "work"),
    ("ESTP", "money_guidance",
     "Set a 24-hour rule for purchases over your threshold. Your in-the-moment confidence can be expensive.",
     1.0, "money"),
    ("ESTP", "relationship_guidance",
     "After the fun, ask one real question. The depth is there — you just need to open the door.",
     1.0, "relationship"),

    # ── ESFP ──────────────────────────────────────────────────────────────────
    ("ESFP", "decision_making",
     "Decide with one trusted person present. You think out loud — use it deliberately.",
     1.0, None),
    ("ESFP", "energy",
     "Schedule wind-down time after high-energy social output. You need it more than you think.",
     0.9, None),
    ("ESFP", "communication",
     "Bring presence, not a script. Your warmth carries the message further than the words.",
     0.85, None),
    ("ESFP", "work_guidance",
     "Make the routine fun or you'll avoid it. Environment and aesthetics aren't trivial for you.",
     1.0, "work"),
    ("ESFP", "money_guidance",
     "Automate one saving mechanism so impulse and planning don't compete.",
     1.0, "money"),
    ("ESFP", "relationship_guidance",
     "Your presence makes people feel seen — that IS the gift. Don't undervalue it.",
     1.0, "relationship"),
]


# ── HD criteria ────────────────────────────────────────────────────────────────
# (hd_type, preference, decision_text, weight, goal)

HD_SEED: list[tuple[str, str, str, float, Optional[str]]] = [

    # ── Generator ─────────────────────────────────────────────────────────────
    ("Generator", "response_first",
     "Wait for the sacral 'uh-huh' before saying yes. Initiating cold drains you and stalls.",
     1.0, None),
    ("Generator", "energy_management",
     "Work to satisfaction, not exhaustion. Stop when the gut signal fades, even if the task isn't done.",
     0.9, None),
    ("Generator", "work_guidance",
     "Only take on projects that generate a clear sacral yes. Doing work you begrudgingly said yes to depletes you faster than any workload.",
     1.0, "work"),
    ("Generator", "money_guidance",
     "Let financial opportunities come to you and respond with your gut. Chasing without a sacral yes leads to expensive mistakes.",
     1.0, "money"),
    ("Generator", "relationship_guidance",
     "Say yes only to people who genuinely light up your sacral. Obligated connection drains your generator faster than solitude.",
     1.0, "relationship"),

    # ── Manifesting Generator ─────────────────────────────────────────────────
    ("Manifesting Generator", "response_first",
     "Wait for the response, then move fast. Skip steps when the path is obvious — that's the design, not a mistake.",
     1.0, None),
    ("Manifesting Generator", "energy_management",
     "Multi-tracking is correct for you. Don't apologize for non-linear progress — just inform teammates of pivots.",
     0.85, None),
    ("Manifesting Generator", "work_guidance",
     "Move fast between tracks, but give your teammates a 2-minute heads-up before each pivot. Your speed is an asset when others can keep up.",
     1.0, "work"),
    ("Manifesting Generator", "money_guidance",
     "When your gut says a financial path is obvious, move — but verify one datapoint first. Your instinct is accurate; due diligence keeps it defensible.",
     1.0, "money"),
    ("Manifesting Generator", "relationship_guidance",
     "Your energy is magnetic but intense. Let the other person set the pace for depth of connection — they may need more time than you.",
     1.0, "relationship"),

    # ── Manifestor ────────────────────────────────────────────────────────────
    ("Manifestor", "inform_before",
     "Inform the people your decision affects BEFORE you act, not after. Then act freely.",
     1.0, None),
    ("Manifestor", "energy_management",
     "Honor your impulse-then-rest cycle. Sustained linear effort is not your operating mode.",
     0.9, None),
    ("Manifestor", "work_guidance",
     "Initiate the thing only you can see needs doing. Then inform quickly and act. Your superpower is starting what others didn't know was possible.",
     1.0, "work"),
    ("Manifestor", "money_guidance",
     "Trust your financial instincts, but loop in one trusted person before moving. Your impulse is usually right; a second set of eyes catches blind spots.",
     1.0, "money"),
    ("Manifestor", "relationship_guidance",
     "Inform, don't ask permission. 'I'm going to do X — wanted you to know' builds more trust than surprising people after the fact.",
     1.0, "relationship"),

    # ── Projector ─────────────────────────────────────────────────────────────
    ("Projector", "wait_for_invitation",
     "Wait for the invitation in the big things (work, love, place). Don't push your guidance uninvited — it creates resistance.",
     1.0, None),
    ("Projector", "energy_management",
     "You have roughly 4 productive hours. Plan the day around them; don't fight the design by grinding past your limit.",
     0.95, None),
    ("Projector", "work_guidance",
     "Make your expertise visible without forcing it. The right work invitation comes when people can see what you offer — show the work, then wait.",
     1.0, "work"),
    ("Projector", "money_guidance",
     "Your best financial moves come through invitation — a referral, a recommendation, the right connection. Build the network, then let it work.",
     1.0, "money"),
    ("Projector", "relationship_guidance",
     "Deepen connections when genuinely invited to do so. Offering too much guidance uninvited creates distance, not closeness.",
     1.0, "relationship"),

    # ── Reflector ─────────────────────────────────────────────────────────────
    ("Reflector", "lunar_cycle",
     "Sleep on big decisions for one full lunar cycle (~28 days). The clarity comes with time; the rush misleads.",
     1.0, None),
    ("Reflector", "energy_management",
     "Your environment is your engine. Choose where you are before you choose what you do.",
     0.9, None),
    ("Reflector", "work_guidance",
     "Choose your work environment as carefully as you choose the work itself. Wrong environment = wrong output, every time.",
     1.0, "work"),
    ("Reflector", "money_guidance",
     "Never make a major financial decision in a charged or high-energy environment. Sample the decision across different days and settings before committing.",
     1.0, "money"),
    ("Reflector", "relationship_guidance",
     "Notice who you feel most like yourself around. That is your most important relationship data — everything else is secondary.",
     1.0, "relationship"),
]


# ── MBTI × HD Scenarios ────────────────────────────────────────────────────────
# 80 rows: all 16 MBTI × 5 HD combinations.
# (mbti_type, hd_type, blend_summary, conflict_situation, conflict_sentence,
#  recommended_sentence, recommended_action)

SCENARIO_SEED: list[tuple[str, str, str, str, str, str, str]] = [

    # ════════════════════════════════════════════════════════════
    # GENERATOR (16 combos)
    # ════════════════════════════════════════════════════════════

    ("INTJ", "Generator",
     "INTJ's systematic plans and Generator's responsive energy: powerful when INTJ waits for genuine gut buy-in before assigning.",
     "INTJ hands the Generator a fully-mapped project plan without asking for input first.",
     "Here's the plan. Just execute the steps.",
     "I've drafted a plan — does any part of this feel right to you before we commit?",
     "Present your framework as a starting point, not a directive. Generator's sacral confirmation is the fuel for execution."),

    ("INTP", "Generator",
     "INTP's deep analysis meets Generator's gut response — great together when analysis closes into a single clear choice.",
     "INTP presents nine possible approaches; Generator can't form a clear sacral response to any of them.",
     "Let me just walk through all the scenarios before we decide which direction.",
     "Here's the core option — does this pull you in, or does something feel off?",
     "Compress your analysis to one clear choice before asking the Generator to respond. Clarity creates the sacral signal."),

    ("ENTJ", "Generator",
     "ENTJ's decisive drive meets Generator's gut wisdom — strong when ENTJ slows to let the sacral response land.",
     "In a meeting, ENTJ calls for immediate commitment before Generator has checked in with their gut.",
     "We need an answer now. Are you in or not?",
     "Take a breath — what's your gut telling you right now?",
     "Build in 60 seconds of pause before Generator gives any major yes. Speed is your asset; invitation is theirs."),

    ("ENTP", "Generator",
     "ENTP's idea flood and Generator's response rhythm — great when ENTP narrows to one clear choice to respond to.",
     "ENTP presents seven project concepts; Generator becomes overwhelmed and can't feel into any of them clearly.",
     "What if we did A, or B, or C combined with a bit of D?",
     "Which of these pulls you the most — just your first instinct, no thinking?",
     "Give the Generator one clear thing to respond to at a time. Clarity creates the sacral signal."),

    ("INFJ", "Generator",
     "INFJ's long-range vision and Generator's responsive energy — works when INFJ invites rather than projects.",
     "INFJ assumes the Generator will love a project because it aligns with INFJ's vision, without checking.",
     "I already know this will excite you. Trust my read on this.",
     "This feels aligned to me — what does your gut say when you hear it?",
     "Your vision may be right. Still ask. Generator's sacral confirmation is the fuel for execution."),

    ("INFP", "Generator",
     "Both introspective — INFP brings values alignment, Generator brings gut wisdom. Double passivity can stall progress.",
     "Both wait for the other to initiate or validate; a good project stalls from mutual inaction.",
     "I'm not sure if this is right for me either. I'll know when I know.",
     "Let's each give our gut a moment, then share what came up — even if it's just a feeling.",
     "Name a specific time to reconvene with your gut check. Mutual passivity isn't the same as wisdom."),

    ("ENFJ", "Generator",
     "ENFJ's contagious enthusiasm can trigger Generator's social yes instead of the real sacral yes.",
     "ENFJ's excitement about a cause makes Generator say yes to a commitment that isn't a real gut pull.",
     "Everyone's so excited — I guess I'm in too!",
     "I love the energy here. Let me take a quiet moment to check my own gut before I say yes.",
     "ENFJ: invite the Generator to check in privately, separate from the group enthusiasm. The sacral signal is quieter than a crowd."),

    ("ENFP", "Generator",
     "Both energetic responders — can confuse mutual excitement with a real sacral yes-signal.",
     "Both get hyped about a venture in conversation, commit publicly, then the energy fades.",
     "Yes! Let's do all of it right now!",
     "This feels exciting — let me sit with it overnight before we make the final call.",
     "Excitement is a starting signal, not a confirmation. Sleep on it; the sacral response holds through morning."),

    ("ISTJ", "Generator",
     "ISTJ's proven process and Generator's gut response — works when ISTJ's systems leave room for sacral pivots.",
     "ISTJ applies a legacy process to a situation Generator knows in their gut no longer fits.",
     "This is how we've always done it. Just follow the process.",
     "Does this process still feel right to you, or is something telling you it needs to change?",
     "Build 'gut check' steps into your process milestones. Generator's instinct is real data, not a disruption."),

    ("ISFJ", "Generator",
     "ISFJ's warmth and Generator's responsive nature — genuine care, but ISFJ's people-pleasing can cloud Generator's authentic signal.",
     "Generator says yes to helping ISFJ because ISFJ seems to need it, not because of a real sacral pull.",
     "Of course I'll help, even if I'm not sure I really want to.",
     "I want to support you and honor my own energy. Let me check if I have a real yes here.",
     "ISFJ: give Generator explicit permission to say no without guilt. It keeps the Generator's energy sustainable."),

    ("ESTJ", "Generator",
     "ESTJ's authority and Generator's responsive energy — Generator may comply without a genuine sacral yes.",
     "ESTJ assigns a task; Generator complies out of authority-deference, not gut alignment, leading to burnout.",
     "It's assigned. Just get it done.",
     "Before you fully commit — does this feel sustainable to you?",
     "ESTJ: build in a brief gut-check step when assigning. Generator's sustainable yes outperforms reluctant compliance."),

    ("ESFJ", "Generator",
     "ESFJ's group warmth and Generator's response — Generator can mistake group approval for their own sacral yes.",
     "Everyone on the team agrees; Generator goes along despite no clear gut signal.",
     "Everyone agrees, so this must be the right call.",
     "Let me check what my gut says, separate from the group agreement.",
     "Generator: always separate your sacral response from group pressure. The quiet moment before the room's energy is your real answer."),

    ("ISTP", "Generator",
     "ISTP's action-first approach meets Generator's response rhythm — friction when ISTP skips the sacral check.",
     "ISTP jumps into execution; Generator hasn't had a moment to feel the yes or no.",
     "Just start. You'll know what feels right once you're in it.",
     "Before we dive in — what's your gut saying right now?",
     "A 30-second pause before starting is enough for Generator's signal. ISTP: it's not slow — it's fuel."),

    ("ISFP", "Generator",
     "Both quiet — ISFP's presence and Generator's gut energy work well together when someone creates the invitation.",
     "A great collaboration is possible, but neither person initiates or creates conditions for the other to respond.",
     "I'll just wait and see what happens. Something will emerge.",
     "I have an idea — does any part of this resonate with you?",
     "ISFP: offer the option; don't wait for it to appear. Generator can't respond to a blank space."),

    ("ESTP", "Generator",
     "ESTP's fast action and Generator's response pace — friction when ESTP moves before Generator has confirmed.",
     "ESTP acts and moves on; Generator is still forming their sacral response and feels left behind.",
     "I've already started. Catch up when you're ready.",
     "Give me 30 seconds — I need a clear yes before I move with you on this.",
     "ESTP: a 30-second gut-check window costs nothing and ensures Generator's sustainable commitment."),

    ("ESFP", "Generator",
     "ESFP's social warmth and Generator's sacral response — joy is real, but excitement and gut-yes need distinguishing.",
     "A fun environment leads Generator to say yes to a long-term commitment they'd decline in a quieter moment.",
     "This is SO fun — of course I'm in for the long haul!",
     "I love the energy here. Let me check if my gut agrees with my enthusiasm before I commit fully.",
     "ESFP: ask for a 'let me sleep on it' after the fun. Generator's yes from joy doesn't always hold."),

    # ════════════════════════════════════════════════════════════
    # MANIFESTING GENERATOR (16 combos)
    # ════════════════════════════════════════════════════════════

    ("INTJ", "Manifesting Generator",
     "INTJ's linear precision and MG's multi-track speed — friction when INTJ's rigid plan blocks MG's intuitive shortcuts.",
     "INTJ presents a step-by-step project plan; MG has already jumped to step 7 and looped back.",
     "You skipped phase 3. The whole plan depends on it being done sequentially.",
     "Walk me through your sequence — I'll adapt the plan to match your intuitive path.",
     "INTJ: treat MG's shortcuts as data, not errors. Ask MG to trace their path; it often reveals a faster route."),

    ("INTP", "Manifesting Generator",
     "INTP's depth and MG's speed — great when analysis serves the sprint, friction when it stalls it.",
     "INTP is still modeling edge cases on step 2 while MG has already moved to step 6.",
     "We need to fully think this through before we move any further.",
     "Flag the risks as we go — your speed will surface them faster than my models anyway.",
     "INTP: accept that MG's in-action learning is valid analysis. Compress your check-ins to critical risks only."),

    ("ENTJ", "Manifesting Generator",
     "Two fast-movers — powerful when aligned, competitive when both try to own direction.",
     "ENTJ and MG each present competing plans; the meeting becomes a tug-of-war for direction.",
     "My approach is clearly faster. We should do it my way.",
     "Your instinct on the path plus my structure for execution — want to combine them?",
     "Name roles before the project starts: who sets direction, who executes. Ambiguity is the conflict, not personality."),

    ("ENTP", "Manifesting Generator",
     "Both love divergence — together they can keep branching forever without landing.",
     "Project keeps expanding; every meeting adds new branches; nothing ships.",
     "But what if we also added this other layer? It would make it so much better.",
     "We have three strong directions — pick one now and let's close the loop on it.",
     "Set a hard convergence gate. After a set date, no new branches. Both of you need someone to hold this."),

    ("INFJ", "Manifesting Generator",
     "INFJ's deep Ni vision and MG's fast skipping — INFJ's insights risk being missed at MG's pace.",
     "INFJ shares a subtle but important insight; MG has already moved past the topic.",
     "Right, noted. What's the next item?",
     "Wait — let me sit with what you just said. That might be the key insight here.",
     "MG: build in a 'hold' signal for when INFJ slows down. Their Ni observations are often ahead of the pace."),

    ("INFP", "Manifesting Generator",
     "INFP's values-gate and MG's momentum — INFP's need to feel aligned can feel like a block to MG.",
     "MG is ready to pivot direction; INFP hasn't finished aligning with the new path.",
     "I can't move forward until this feels right to my values.",
     "Where is your gut pulling you? Give me 5 minutes to align with that direction.",
     "INFP: compress alignment checks to a single value-question. MG: hold for one answer before moving."),

    ("ENFJ", "Manifesting Generator",
     "ENFJ's team cohesion and MG's pivoting speed — MG's detours create confusion ENFJ has to repair.",
     "MG pivots the project direction mid-sprint; team loses orientation; ENFJ spends energy on damage control.",
     "I already changed direction. Can you explain it to the team?",
     "Before I shift — let's spend 2 minutes so you can set context for the team first.",
     "MG: route pivots through ENFJ before announcing. ENFJ's 2-minute framing prevents 2-hour confusion."),

    ("ENFP", "Manifesting Generator",
     "Maximum energy and enthusiasm — both excel at starting; together they need external accountability to finish.",
     "Seven projects launched; zero completed; team asks what the actual priority is.",
     "This new idea is way more interesting than what we were doing before.",
     "Before we add another — which existing one is closest to done? Let's ship that first.",
     "Institute a 'one in, one out' rule. Neither of you will enforce it — build it into your process with a third party."),

    ("ISTJ", "Manifesting Generator",
     "ISTJ's procedural rigor and MG's non-linear leaps — ISTJ sees shortcuts as errors; MG sees steps as unnecessary.",
     "MG skips phase 2 of a documented process; ISTJ marks the work as non-compliant.",
     "You can't skip phase 2. That's the protocol. Go back.",
     "I know my path looks non-linear. Let me show you the output first — then we can check if phase 2 was needed.",
     "ISTJ: add an outcome-validation step. If MG's shortcut produces the right output, the process needs updating."),

    ("ISFJ", "Manifesting Generator",
     "ISFJ's careful steadiness and MG's fast multi-track — MG's pace creates anxiety; ISFJ's caution creates friction.",
     "MG moves at full speed; ISFJ feels rushed, quality suffers, and stress rises.",
     "Can you please slow down? We're going to miss something important.",
     "I'll keep my pace and meet you at the checkpoint with my part done.",
     "Set clear checkpoint moments where MG waits for ISFJ's thorough contribution. Speed + care beats speed alone."),

    ("ESTJ", "Manifesting Generator",
     "ESTJ's structural authority and MG's skip-adapt style — both decisive, clash on who owns the process.",
     "ESTJ enforces process compliance; MG keeps detouring based on intuition.",
     "Every deviation from the process requires documented approval. No exceptions.",
     "I'll document my detours in real time so the outcome is always traceable.",
     "MG: create a deviation log. ESTJ: accept documented detours that produce the right outcome."),

    ("ESFJ", "Manifesting Generator",
     "ESFJ's social harmony and MG's pivot speed — MG's sudden changes upset the cohesion ESFJ maintains.",
     "MG announces a project direction change; team is upset; ESFJ manages the emotional fallout.",
     "I just changed the direction. Why is everyone so upset? It's clearly better.",
     "Before I announce the change, let me run it by you so you can prep the team.",
     "MG: route announcements through ESFJ for 60 seconds of framing. ESFJ: trust MG's instinct on direction."),

    ("ISTP", "Manifesting Generator",
     "Both practical and fast — MG generates problems faster than ISTP can solve them.",
     "MG's rapid pivots leave disconnected components; ISTP spends time debugging instead of building.",
     "I've moved to the next phase. Can you handle what got left behind?",
     "Before I move to the next track — 2-minute handoff so you know exactly what needs connecting.",
     "MG: standardize handoff notes. ISTP: accept MG's non-linearity as valid and triage accordingly."),

    ("ISFP", "Manifesting Generator",
     "MG's intensity and ISFP's quiet depth — ISFP can become invisible in MG's energy field.",
     "MG moves at full speed; ISFP's quieter contributions get skipped over in the pace.",
     "You're moving too fast. I can't feel into this properly when things change this quickly.",
     "ISFP, I'm going to pause for 3 minutes — tell me what feels off before I keep going.",
     "MG: schedule deliberate ISFP check-ins. ISFP's felt-sense catches what MG's speed misses."),

    ("ESTP", "Manifesting Generator",
     "Maximum execution speed — powerful in crisis, risk of recklessness without pause.",
     "Both move fast; no one checks quality; accumulated problems create a larger crisis later.",
     "We'll clean it up after. Keep moving — momentum matters most right now.",
     "30-second quality gate before we advance — worth the stop to avoid a rebuild?",
     "Build mandatory fast-review checkpoints. Neither will enjoy them; both will benefit from them."),

    ("ESFP", "Manifesting Generator",
     "High energy and fun — can confuse a great collaborative vibe with actual productive output.",
     "Excellent working relationship; meetings feel productive; deliverables are behind.",
     "This collaboration is amazing. We're crushing it!",
     "Love the energy. Quick 5-minute check: what have we actually shipped this week?",
     "End every session with a 2-minute output review. Fun is a feature, not a measure of progress."),

    # ════════════════════════════════════════════════════════════
    # MANIFESTOR (16 combos)
    # ════════════════════════════════════════════════════════════

    ("INTJ", "Manifestor",
     "Both independent visionaries — INTJ's precision + Manifestor's initiation = powerful when informing is built in.",
     "INTJ Manifestor launches a major project redesign without telling any stakeholders first.",
     "I didn't think I needed to announce it. I just implemented it.",
     "Before I move on this, I'm going to ping the three people affected so they're not caught off guard.",
     "Informing is not asking permission. It's a 5-minute action that prevents hours of repair."),

    ("INTP", "Manifestor",
     "INTP's analysis phase can stall Manifestor's impulse — delay without informing creates conflict.",
     "INTP keeps finding more to analyze; the Manifestor impulse is ready to move but stuck waiting.",
     "Just give me two more days to think through three more edge cases before we go.",
     "I'll analyze in parallel while we inform the stakeholders. No need to wait for perfect clarity.",
     "Inform before you're 100% ready. Waiting for perfect analysis before informing is procrastination in disguise."),

    ("ENTJ", "Manifestor",
     "Two decisive initiators — extraordinary output when aligned; bridge-burning risk when informing is skipped.",
     "ENTJ Manifestor launches a product feature without cross-team communication.",
     "I knew it was the right move. They'll catch up when they see the results.",
     "Fast loop to three stakeholders before launch — ten minutes saves ten alignment meetings.",
     "Inform speed matters as much as decision speed. Build informing into your definition of 'done deciding.'"),

    ("ENTP", "Manifestor",
     "Idea generation + initiation impulse — many launches, insufficient follow-through communication.",
     "Five initiatives launched this quarter; no team knows which is the current priority.",
     "I already started a better approach. We're pivoting from what I just announced.",
     "Announce the current initiative clearly to the affected people before the next idea launches.",
     "One active initiative at a time. Announce completion or abandonment before the next one starts."),

    ("INFJ", "Manifestor",
     "INFJ's vision-depth and Manifestor's initiation — tension between wanting full clarity before informing and the need to just act.",
     "INFJ Manifestor delays informing people because the vision isn't fully articulated yet.",
     "I'll tell everyone once I have the whole thing figured out.",
     "I'm informing with a rough draft of the vision — your input will help shape it.",
     "Inform with 70% clarity. The remaining 30% is shaped by the conversation, not before it."),

    ("INFP", "Manifestor",
     "Manifestor's impulse to act and INFP's need for deep value-alignment — can act impulsively, then regret.",
     "Manifestor impulse to quit a job fires; INFP's values haven't been consulted.",
     "I just had to leave. I couldn't stay. I can't fully explain it yet.",
     "Give the values-check 24 hours before the Manifestor impulse takes action. If it still holds, move.",
     "Build a 24-hour buffer between Manifestor impulse and execution. Values and impulse need to align."),

    ("ENFJ", "Manifestor",
     "ENFJ's consensus-building and Manifestor's inform-and-act — ENFJ may misread informing as insufficient inclusion.",
     "Manifestor informs the team of a decision; ENFJ wants to reopen it for group input.",
     "You told us, but you didn't actually ask us. That's different.",
     "I'm going to do X. I'm informing, not requesting approval. If there are critical blockers, speak now — I'm listening.",
     "Make the 'inform' explicit: 'This is decided. What I need is awareness, not permission.'"),

    ("ENFP", "Manifestor",
     "Both initiators — together they launch big; but informing must come before the crowd, not after.",
     "Big public announcement made; infrastructure and team weren't briefed first.",
     "Let's announce it now and figure out the details as we go!",
     "Who needs to know before we go public? Let's inform those people first — then announce.",
     "Draft a 'who needs to know' list before every launch. Informing is not slowing down; it's preventing chaos."),

    ("ISTJ", "Manifestor",
     "ISTJ's process compliance and Manifestor's bypass instinct — Manifestor's informing reads as skipping approval.",
     "Manifestor sends an 'FYI' email on a major change; ISTJ expects the change management process.",
     "This should have gone through the proper approval workflow, not just an email.",
     "Heads up on a major change — brief window for critical objections before I finalize.",
     "Reframe 'informing' as 'final check before action.' ISTJ can live with it; Manifestor keeps their speed."),

    ("ISFJ", "Manifestor",
     "ISFJ's need to feel included and Manifestor's independent nature — Manifestor's autonomy can feel cold.",
     "Manifestor makes a significant personal decision without including ISFJ in any part of the process.",
     "Why didn't you tell me beforehand? I could have helped. I feel shut out.",
     "I'm going to move on this. You're one of the first people I'm telling — wanted you to know.",
     "Informing ISFJ first (even briefly) creates loyalty. They don't need veto power — just to feel seen."),

    ("ESTJ", "Manifestor",
     "Both decisive, but ESTJ uses hierarchical authority; Manifestor acts regardless of hierarchy.",
     "Manifestor goes directly to the end client without routing through ESTJ first.",
     "You went around the chain of command. That's not how we operate.",
     "I'm bypassing the normal path because of time sensitivity. Heads up — here's why and what happened.",
     "Inform before bypassing, even briefly. ESTJ can accept speed when given context; surprises create conflict."),

    ("ESFJ", "Manifestor",
     "ESFJ's group buy-in need and Manifestor's inform-and-move — ESFJ interprets informing as steamrolling.",
     "Manifestor announces a decision; ESFJ wants to revisit it with the group for genuine input.",
     "The decision's already made. I don't understand why we're reopening it.",
     "Direction is set. What I'd love your help with is how to communicate it well to the team.",
     "Give ESFJ a role in the execution (communication, rollout) not the decision. Both feel respected."),

    ("ISTP", "Manifestor",
     "Both independent — ISTP may disengage when informed instead of consulted.",
     "Manifestor informs ISTP of a direction change; ISTP quietly does it their own way.",
     "You didn't ask me. I've already started solving it differently.",
     "I'm doing X. I'm not asking permission — I want your technical input to make it better.",
     "Invite ISTP's input explicitly within the inform. They'll engage when their expertise is genuinely needed."),

    ("ISFP", "Manifestor",
     "Manifestor's solo decisions and ISFP's need for felt-connection to work — ISFP disengages when excluded.",
     "Manifestor makes a creative direction decision alone; ISFP loses emotional investment in the work.",
     "I guess the direction's decided. I'm not sure I care about it the same way anymore.",
     "Here's what I'm doing and why it matters to me — does any part of this excite you?",
     "ISFP needs to feel something about the work. Share the why behind the decision, not just the what."),

    ("ESTP", "Manifestor",
     "Two action-starters — without coordination, both initiate and create competing directions.",
     "Both start their own version of a project; discover the collision mid-execution.",
     "I was literally about to start that. You should have told me first.",
     "I'm initiating X. Five-minute check — are you working on anything that overlaps?",
     "Build a 'heads up before launch' habit. Two initiators thrive with a quick sync loop."),

    ("ESFP", "Manifestor",
     "Manifestor's independence and ESFP's social warmth — ESFP feels left out of Manifestor's world.",
     "Manifestor makes plans and executes without looping in ESFP at any stage.",
     "Why wasn't I included? This affects me and I only found out at the end.",
     "Here's what I'm planning — want to be part of how we roll it out?",
     "Give ESFP a role in the visible part of the initiative. Inclusion in execution is enough."),

    # ════════════════════════════════════════════════════════════
    # PROJECTOR (16 combos)
    # ════════════════════════════════════════════════════════════

    ("INTJ", "Projector",
     "Both strategic — INTJ's confidence can override the invitation Projector needs to guide effectively.",
     "INTJ Projector gives detailed unsolicited analysis of a colleague's system during a team meeting.",
     "I can already see three flaws in this system. Let me walk you through them.",
     "I've been watching this system — would it help if I shared what I'm noticing?",
     "Wait for the question before giving the answer. Your read is accurate; the invitation makes it land."),

    ("INTP", "Projector",
     "INTP's analytical precision and Projector's systemic view — powerful when invited, alienating when not.",
     "INTP Projector walks into a conversation and immediately identifies the logical flaw without being asked.",
     "Actually, that reasoning doesn't work because of this fundamental inconsistency.",
     "Interesting problem — are you open to a different angle on the underlying logic?",
     "Preface your analysis with an invitation check. One sentence to ask is not weak — it's the access key."),

    ("ENTJ", "Projector",
     "Biggest tension combo: ENTJ's drive-to-direct conflicts with Projector's wait-for-invitation design.",
     "In a leadership meeting, ENTJ Projector takes over direction without being given the floor.",
     "Here's what we're all going to do. I've already mapped out the path.",
     "I have a systems view on this — who wants to hear it before we commit to a direction?",
     "Channel ENTJ's drive into making yourself visible until the invitation comes. The invitation gives more leverage than taking the floor."),

    ("ENTP", "Projector",
     "ENTP's idea generation and Projector's guidance — Projector disperses energy by engaging with every thread.",
     "ENTP Projector offers insights on every topic raised, exhausting their energy before the real need emerges.",
     "And another thing you should consider is... and also this...",
     "Of everything we've touched on — where would my input actually move the needle for you today?",
     "Projector's energy is finite. Pick the one place your guidance has maximum leverage and go deep there."),

    ("INFJ", "Projector",
     "Both depth-oriented — mutual under-contribution is the risk; neither surfaces insights without invitation.",
     "Both hold back deep insights in a meeting; the group makes a mediocre decision.",
     "I didn't think this was the right moment to share what I was seeing.",
     "I notice we're both holding back — who wants to go first? I'll follow.",
     "Create explicit space for depth. The invitation that doesn't come verbally sometimes needs to be built structurally."),

    ("INFP", "Projector",
     "Both invitation-aware and values-driven — mutual passivity can stall projects indefinitely.",
     "Project needs guidance; INFP doesn't impose; Projector doesn't guide without invitation; nothing moves.",
     "I don't want to push my ideas unless they're genuinely wanted.",
     "I'll write up my perspective so the invitation is easier to give — just reach out when you're ready.",
     "Written guidance is a low-pressure invitation. Projector: put it on paper and let them reach for it."),

    ("ENFJ", "Projector",
     "ENFJ gives; Projector guides — together they can both over-extend for others and burn out simultaneously.",
     "Both spend all available energy supporting others; neither protects their own restoration window.",
     "I have to be there for everyone, even when I'm running on empty.",
     "I'm protecting my first 4 hours today. After that, I'm available to guide and support.",
     "Name your protected window out loud. Permission to conserve is needed by both types — give it to yourself explicitly."),

    ("ENFP", "Projector",
     "ENFP's enthusiasm creates a natural invitation environment — good for Projector. Conflict: direction changes too fast.",
     "ENFP pivots the project; Projector's guidance was perfectly calibrated to the previous direction.",
     "Wait — I had the perfect insight for where you were headed, but you've already moved on.",
     "Before we shift direction — let me offer one guiding observation on where we were. Then we move.",
     "Projector: compress your guidance to one sentence at pivot moments. ENFP will catch it."),

    ("ISTJ", "Projector",
     "ISTJ's task-focus and Projector's systems-view — Projector's big-picture advice feels out-of-scope to ISTJ.",
     "Projector offers a systemic redesign recommendation while ISTJ is focused on one specific task.",
     "We just need to fix this one thing. Why are you talking about the whole system?",
     "For just this task: here's the one thing that will help most right now.",
     "Projector: calibrate scope to what's invited. Save the full system view for when the big-picture invitation arrives."),

    ("ISFJ", "Projector",
     "ISFJ's warmth creates a natural invitation for Projector — good pair. Conflict: ISFJ warmth reads as full invitation when it's partial.",
     "ISFJ's openness makes Projector feel fully invited; Projector redesigns ISFJ's entire workflow without being asked.",
     "Since you seemed so open, I went ahead and mapped out your whole process.",
     "You've invited me into the specific thing — let me stay focused there and see if you want more.",
     "Projector: read the scope of the invitation accurately. Warmth does not equal permission to expand scope."),

    ("ESTJ", "Projector",
     "ESTJ's results-focus and Projector's insight — Projector's guidance must be framed as value, not critique.",
     "Projector identifies a systemic inefficiency in ESTJ's domain; ESTJ becomes defensive.",
     "The whole process needs to be redesigned. It's fundamentally inefficient.",
     "I noticed something that could significantly speed this up — interested in hearing it?",
     "Projector: lead with benefit, not diagnosis. ESTJ responds to 'here's what this gives you,' not 'here's what's wrong.'"),

    ("ESFJ", "Projector",
     "ESFJ's social warmth and Projector's systems guidance — Projector's group-dynamic insights can feel undermining.",
     "Projector points out a group dynamic issue during ESFJ's facilitation; ESFJ feels undermined.",
     "The group dynamic isn't working because of how you're facilitating this.",
     "Could I share an observation about the group energy that might help? It's working — just one pattern I'm seeing.",
     "Projector: the ask-first sentence is not optional with ESFJ. It converts critique into collaboration."),

    ("ISTP", "Projector",
     "ISTP's self-reliance and Projector's guidance — Projector's systems input feels intrusive to independent ISTP.",
     "Projector offers process improvements; ISTP is already solving it in their own way.",
     "I've got it. I don't need advice on how to do my own work.",
     "I see a pattern that might be relevant — can I share it? No pressure to use it.",
     "Projector: offer once, clearly, with explicit opt-out. ISTP: acknowledge when a Projector's observation is useful — it reinforces the invitation loop."),

    ("ISFP", "Projector",
     "Both quiet — Projector's guidance and ISFP's need go unspoken; collaboration stays on the surface.",
     "ISFP needs real guidance on a stuck project; Projector sees the issue; neither speaks up.",
     "I didn't want to intrude. It's not my place to say.",
     "I've been watching this. I think I see what's stuck — can I say it?",
     "Projector: the single permission-ask sentence is the unlock. ISFP will say yes and feel genuinely helped."),

    ("ESTP", "Projector",
     "ESTP's present-focus and Projector's systemic view — ESTP won't slow down for big-picture guidance.",
     "ESTP handles the immediate fire; Projector sees the root cause but can't get ESTP to pause.",
     "You're dealing with the symptom. You keep missing the actual problem underneath.",
     "When you have 5 minutes, I can show you why this keeps happening — would save you the next fire.",
     "Projector: time your guidance to ESTP's natural pause points, not mid-action. The insight lands in the debrief."),

    ("ESFP", "Projector",
     "ESFP's natural warmth creates good invitation conditions for Projector. Conflict: invitations appear and close fast.",
     "ESFP warmly invites Projector's input; moves on before Projector can fully deliver.",
     "Wait — you asked for my perspective and then we moved on before I finished.",
     "Quick version: one sentence. The full insight is ready whenever you want to go deeper.",
     "Projector: develop a one-sentence version of your key insights for fast-moving environments. The depth is still there."),

    # ════════════════════════════════════════════════════════════
    # REFLECTOR (16 combos)
    # ════════════════════════════════════════════════════════════

    ("INTJ", "Reflector",
     "INTJ's decisiveness and Reflector's lunar-cycle clarity — INTJ's speed pushes Reflector before their clarity arrives.",
     "INTJ gives a 48-hour deadline on a major career decision the Reflector needs weeks to process.",
     "We need an answer by Friday or the opportunity closes.",
     "What's the minimum commitment right now that keeps the option open for another 3 weeks?",
     "Find the partial commitment that preserves optionality. Reflector's full clarity is worth protecting."),

    ("INTP", "Reflector",
     "INTP's logic and Reflector's environmental clarity — analysis alone doesn't produce Reflector's decision.",
     "INTP presents a fully logical case for a decision; Reflector still can't commit.",
     "The logic clearly supports this choice. Why is it still not clear to you?",
     "The logic checks out. What does your environment tell you — different settings, different days?",
     "Reflector doesn't decide through logic alone. They decide through sustained environmental sampling. Provide both."),

    ("ENTJ", "Reflector",
     "Highest speed-clash: ENTJ wants outcomes now; Reflector needs a full lunar cycle for major decisions.",
     "ENTJ demands a decision on a partnership deal by end of the business week.",
     "You've had more than enough time. Make the call. We can't wait any longer.",
     "What partial commitment can you make right now while the full clarity develops over the next 3 weeks?",
     "Identify what can move forward without the full Reflector decision. Protect the clarity window for the real question."),

    ("ENTP", "Reflector",
     "ENTP's idea flood and Reflector's environmental sampling — too many options prevent any from settling.",
     "ENTP presents five new directions; Reflector needs weeks to process each against different environments.",
     "They're all strong options — just pick the most exciting one!",
     "Which one do you want to sit with first? One at a time, and let it breathe.",
     "ENTP: present one option per session. Reflector: indicate which one you're sampling this cycle."),

    ("INFJ", "Reflector",
     "Both deeply intuitive — INFJ's Ni pulls forward; Reflector's environmental process moves differently.",
     "INFJ feels strongly about a path; assumes shared intuition means the Reflector agrees.",
     "You must feel what I'm feeling. This is clearly the right direction for both of us.",
     "I feel strongly about this direction. What does your environment say when you check it separately?",
     "Reflector's clarity process is environmental, not purely intuitive. Give it space to be different from yours."),

    ("INFP", "Reflector",
     "Both need internal alignment — together they can wait indefinitely with no decision ever made.",
     "Both waiting for the right feeling; project stays stuck for months.",
     "I'll know when it feels right. It just doesn't feel right yet.",
     "Let's set a date to revisit — even if neither of us feels fully ready, we'll check in then.",
     "Set a hard reconnect date. Both of you need external structure to move when internal readiness is the standard."),

    ("ENFJ", "Reflector",
     "ENFJ facilitates decisions; Reflector needs environment, not facilitation, to get clear.",
     "ENFJ organizes a decision-making meeting to help Reflector gain clarity; Reflector still isn't clear after.",
     "I set up this whole session to help you work through it. Are you closer to a decision now?",
     "What environment would help you get clear on this? Let me help you create that instead.",
     "Facilitate the environment, not the decision. Reflector's clarity comes from where they are, not what they're asked."),

    ("ENFP", "Reflector",
     "ENFP's enthusiasm temporarily lifts Reflector; Reflector's read changes when the energy field settles.",
     "Reflector says yes in ENFP's enthusiastic presence; calls to reverse the decision a week later.",
     "You seemed so excited about it when we talked. What changed?",
     "Let's check back in after you've had some time away from the group energy — your read may be different.",
     "Reflector: flag when decisions are made in high-energy environments. ENFP: build in a follow-up confirmation window."),

    ("ISTJ", "Reflector",
     "ISTJ's process-consistency and Reflector's variable responses — Reflector's week-to-week shifts feel like unreliability.",
     "Reflector gives different answers across two consecutive weeks; ISTJ is frustrated by the inconsistency.",
     "You said yes last week. Now you're saying no. I need to know which one is real.",
     "My read varies week to week — it's not inconsistency, it's calibration. The lunar cycle brings consistent clarity.",
     "ISTJ: build a Reflector check-in window into your timeline. Reflector: communicate your calibration process proactively."),

    ("ISFJ", "Reflector",
     "ISFJ's warmth is a good environment for Reflector — gentle pressure risk when ISFJ internalizes Reflector's moods.",
     "Reflector absorbs ISFJ's low energy and reflects it back amplified; ISFJ thinks they've done something wrong.",
     "Why are you acting stressed? Is this about something I did?",
     "I might be reflecting your energy right now. Shall we both take a breath and reset?",
     "Reflector: name when you might be reflecting someone else's state. ISFJ: don't take amplified reflection personally."),

    ("ESTJ", "Reflector",
     "ESTJ's efficiency expectations and Reflector's variable timing — ESTJ reads flexibility as inconsistency.",
     "ESTJ creates tight uniform timelines; Reflector needs flexible windows for big decisions.",
     "I can't run a team on 'I'll know when I know.' I need a commitment.",
     "Give me a soft check-in date and a hard deadline. I'll be clear by the hard one.",
     "Soft-hard deadline structure works for both. ESTJ gets commitment; Reflector gets the process they need."),

    ("ESFJ", "Reflector",
     "ESFJ's social warmth is good environment for Reflector — Reflector can amplify ESFJ's group anxiety.",
     "ESFJ is anxious about team morale; Reflector mirrors and amplifies the anxiety without realizing it.",
     "Everyone seems really stressed. The whole team energy feels off.",
     "I might be amplifying what I'm picking up from the group. Is the team actually this stressed right now?",
     "Reflector: check the source before reflecting amplified group states. ESFJ: receive the Reflector's signal as data, not verdict."),

    ("ISTP", "Reflector",
     "ISTP's independent focus and Reflector's environmental need — disconnected environment leaves Reflector without signal.",
     "ISTP works in isolation; Reflector drifts without sufficient environmental input to form a perspective.",
     "I'm not sure what I think about any of this. I don't have enough to go on.",
     "I need more environmental engagement before I can give you a useful read. Can we bring in more context?",
     "Reflector: name when you need richer environmental input. ISTP: share more context; your efficiency instinct cuts information Reflector needs."),

    ("ISFP", "Reflector",
     "Both sensitive and environment-driven — beautiful space together, but neither drives decisions or momentum.",
     "Both deeply in their feeling-states; nothing gets decided; time passes.",
     "It just doesn't feel like the right time yet. I need more time.",
     "Let's name what we're each feeling right now and see if a decision emerges from that shared clarity.",
     "Name feelings explicitly; it moves them from ambient state to usable information. Then decide."),

    ("ESTP", "Reflector",
     "ESTP's high-stimulus pace overwhelms Reflector's environmental sampling capacity.",
     "ESTP's fast environment exhausts Reflector; Reflector loses their own clear signal in the noise.",
     "I can't tell what I actually think. Everything is moving too fast for me to get a read.",
     "I need a quiet hour after this to settle before I can give you an accurate read on anything.",
     "Reflector: protect decompression time after ESTP sessions. ESTP: schedule the debrief check-in, not just the action."),

    ("ESFP", "Reflector",
     "ESFP's social warmth is good for Reflector — Reflector mirrors ESFP's mood and mistakes it for their own.",
     "ESFP is excited about a plan; Reflector says yes in the moment; uncertainty arrives later.",
     "You were completely on board yesterday. What happened?",
     "I was reflecting your excitement. Let me sit with it alone and give you my real read tomorrow.",
     "Reflector: always flag when a yes came from someone else's energy field. ESFP: build in a next-day confirmation."),
]


# ── HD type profiles ──────────────────────────────────────────────────────────

HD_PROFILES_SEED: list[dict] = [
    {
        "hd_type": "Manifestor",
        "population_percent": "Approximately 9%",
        "core_purpose": (
            "Manifestors are designed to initiate movement and create new directions. Their purpose is not "
            "to maintain existing systems, optimize processes, or continuously produce output. Instead, they "
            "act as catalysts who introduce new ideas, projects, businesses, movements, and innovations into "
            "the world. They often feel a natural urge to act independently and can become frustrated when "
            "required to seek excessive approval before taking action."
        ),
        "energy_pattern": (
            "Manifestors do not possess sustainable workforce energy like Generators. Their energy arrives in "
            "powerful bursts of inspiration and action. During these periods they can accomplish extraordinary "
            "amounts of work quickly. Afterward they often require significant rest and recovery. Their "
            "productivity is cyclical rather than continuous."
        ),
        "strategy": (
            "Inform before acting. This does not mean asking permission. It means communicating intentions to "
            "those affected by their actions. Informing reduces resistance because people understand what is "
            "happening and why. Manifestors often discover that many conflicts disappear when they simply "
            "communicate their plans beforehand."
        ),
        "signature": (
            "Peace. When functioning correctly, Manifestors experience a sense of freedom, autonomy, and "
            "internal peace. They feel unconstrained and capable of moving toward their goals without "
            "unnecessary obstacles."
        ),
        "not_self": (
            "Anger. When blocked, controlled, micromanaged, or prevented from acting independently, "
            "Manifestors often experience anger. This anger is usually a signal that their autonomy is "
            "being restricted."
        ),
        "strengths": (
            "Strong independence, courage to act without certainty, ability to create momentum, willingness "
            "to challenge existing systems, comfort with risk, natural influence, and ability to inspire "
            "action in others. They often see possibilities before other people recognize them."
        ),
        "challenges": (
            "Difficulty accepting authority, impatience with bureaucracy, tendency to isolate themselves, "
            "resistance from others who feel excluded, inconsistent energy levels, and frustration when "
            "required to explain every decision."
        ),
        "work_style": (
            "Works best in environments with autonomy and authority. They thrive when responsible for "
            "creating new initiatives, entering new markets, launching products, or solving previously "
            "unsolved problems. Repetitive maintenance work often drains them."
        ),
        "leadership_style": (
            "Visionary and directional. They lead by initiating and inspiring rather than by managing "
            "details. They excel at setting direction and creating momentum but may need support from "
            "other types for execution and operational management."
        ),
        "decision_making": (
            "Manifestors typically experience decisions as internal impulses or urges. Their challenge is "
            "distinguishing authentic impulses from emotional reactions."
        ),
        "relationship_style": (
            "They require freedom, trust, and respect. Relationships become difficult when partners attempt "
            "to control them. Healthy relationships allow both independence and connection."
        ),
        "growth_path": (
            "Learn that informing others increases influence rather than reducing freedom. Develop patience "
            "and communication skills while maintaining independence."
        ),
        "environment_needs": "Freedom, flexibility, authority, trust, and reduced micromanagement.",
        "stress_behavior": "Withdrawal, isolation, anger, rebellion, impulsive actions, or attempts to regain control.",
        "long_description": (
            "Manifestors are the initiators of the Human Design system. Their role is to bring new energy "
            "into the world. Historically they resemble explorers, founders, inventors, revolutionaries, "
            "and pioneers. They are often several steps ahead of others and may become frustrated when "
            "people cannot immediately understand their vision. Because their energy is not designed for "
            "continuous output, they often alternate between intense activity and recovery periods. Success "
            "comes when they embrace their role as initiators rather than attempting to become full-time "
            "operators or managers."
        ),
    },
    {
        "hd_type": "Generator",
        "population_percent": "Approximately 37%",
        "core_purpose": (
            "Generators are designed to build, sustain, improve, and master. They provide much of the "
            "productive energy that keeps organizations, communities, and societies functioning. Their "
            "purpose is to engage deeply with work, relationships, and experiences that genuinely excite them."
        ),
        "energy_pattern": (
            "Sustainable and renewable. Unlike Manifestors, Generators possess a reliable source of energy "
            "that can operate consistently over long periods when aligned with meaningful activities."
        ),
        "strategy": (
            "Wait to respond. Generators are designed to react to opportunities rather than force them into "
            "existence. Life presents options, invitations, questions, and circumstances. Their role is to "
            "notice which opportunities create genuine excitement."
        ),
        "signature": (
            "Satisfaction. Satisfaction indicates that a Generator is investing energy into activities "
            "aligned with their true interests."
        ),
        "not_self": (
            "Frustration. Frustration signals that energy is being spent on something misaligned, "
            "forced, or unwanted."
        ),
        "strengths": (
            "Consistency, endurance, mastery, reliability, patience, craftsmanship, expertise, and sustained "
            "effort. Generators can become world-class experts because they are willing to invest years into "
            "skill development."
        ),
        "challenges": (
            "Difficulty saying no, remaining in jobs they dislike, overcommitting, ignoring internal signals, "
            "and confusing external expectations with genuine enthusiasm."
        ),
        "work_style": (
            "Best suited for long-term projects requiring consistent improvement and execution. They excel "
            "in professions where mastery develops over time."
        ),
        "leadership_style": (
            "Leads through expertise, reliability, and demonstration. Their authority comes from competence "
            "and results."
        ),
        "decision_making": "Uses bodily responses and instinctive reactions. The body often knows before the mind.",
        "relationship_style": (
            "Loyal, committed, and stable when emotionally invested. Problems arise when they remain in "
            "relationships solely out of obligation."
        ),
        "growth_path": (
            "Learn to trust genuine excitement and stop investing energy into activities that consistently "
            "create frustration."
        ),
        "environment_needs": "Meaningful work, opportunities for mastery, clear feedback, and sustainable pacing.",
        "stress_behavior": "Complaining, frustration, procrastination, exhaustion, and resentment.",
        "long_description": (
            "Generators are the builders of the world. Their purpose is not necessarily to invent entirely "
            "new directions but to take opportunities and develop them into tangible results. They possess "
            "extraordinary capacity for improvement and mastery. When engaged in meaningful work, they often "
            "outperform other types through persistence alone. Their challenge is learning that success comes "
            "from responding to the right opportunities rather than forcing every opportunity."
        ),
    },
    {
        "hd_type": "Manifesting Generator",
        "population_percent": "Approximately 33%",
        "core_purpose": (
            "Manifesting Generators combine the sustainable energy of Generators with the initiating "
            "qualities of Manifestors. Their purpose is to build, optimize, accelerate, and innovate "
            "simultaneously."
        ),
        "energy_pattern": "High-volume, fast-moving, multidirectional energy.",
        "strategy": "Wait to respond first, then act rapidly.",
        "signature": "Satisfaction and Peace.",
        "not_self": "Frustration and Anger.",
        "strengths": (
            "Speed, adaptability, multitasking, efficiency, creativity, entrepreneurship, rapid learning, "
            "and innovation."
        ),
        "challenges": (
            "Skipping steps, impatience, inconsistency, boredom, unfinished projects, and communication "
            "breakdowns."
        ),
        "work_style": "Prefers variety, multiple projects, experimentation, and fast execution.",
        "leadership_style": "Leads through momentum and visible action.",
        "decision_making": "Response first, action second.",
        "relationship_style": "Needs flexibility, freedom, and room to evolve.",
        "growth_path": "Learn that speed is valuable but not at the expense of essential steps.",
        "environment_needs": "Dynamic environments with autonomy and variety.",
        "stress_behavior": "Scattered focus, abandoning projects, impulsive changes.",
        "long_description": (
            "Manifesting Generators are often described as 'high-performance hybrids.' They possess both "
            "the capacity to build and the desire to move quickly. They naturally seek efficiency and often "
            "discover shortcuts others miss. However, their speed can create errors if they fail to validate "
            "assumptions. Their life path often appears non-linear because they evolve rapidly and frequently "
            "outgrow previous interests."
        ),
    },
    {
        "hd_type": "Projector",
        "population_percent": "Approximately 20%",
        "core_purpose": (
            "To guide people, resources, systems, and organizations toward greater efficiency and "
            "effectiveness."
        ),
        "energy_pattern": "Focused rather than sustainable.",
        "strategy": "Wait for recognition and invitation.",
        "signature": "Success.",
        "not_self": "Bitterness.",
        "strengths": (
            "Insight, strategy, leadership, coaching, pattern recognition, talent development, and "
            "organizational awareness."
        ),
        "challenges": "Overworking, lack of recognition, feeling overlooked, burnout.",
        "work_style": "Strategic and advisory.",
        "leadership_style": "Guides rather than directs.",
        "decision_making": "Recognition provides access to influence.",
        "relationship_style": "Desires deep appreciation and mutual understanding.",
        "growth_path": "Stop competing with Generators on productivity and embrace strategic value.",
        "environment_needs": "Recognition, respect, meaningful influence.",
        "stress_behavior": "Bitterness, criticism, withdrawal.",
        "long_description": (
            "Projectors are the natural guides of the Human Design system. They possess a unique ability "
            "to understand people, systems, and resources. While others focus on doing, Projectors focus "
            "on optimizing. They can often identify inefficiencies that others overlook. Their challenge "
            "is that insight alone is insufficient. Others must recognize and invite their guidance. When "
            "this occurs, Projectors frequently become exceptional managers, consultants, coaches, and leaders."
        ),
    },
    {
        "hd_type": "Reflector",
        "population_percent": "Approximately 1%",
        "core_purpose": "To reflect the health, truth, and condition of communities and environments.",
        "energy_pattern": "Highly variable and environmentally influenced.",
        "strategy": "Wait one lunar cycle for major decisions.",
        "signature": "Surprise.",
        "not_self": "Disappointment.",
        "strengths": "Objectivity, perspective, adaptability, awareness, community sensing.",
        "challenges": "Inconsistency, sensitivity, identity confusion.",
        "work_style": "Flexible and observational.",
        "leadership_style": "Provides perspective rather than direction.",
        "decision_making": "Requires time and environmental clarity.",
        "relationship_style": "Highly sensitive to relationship quality.",
        "growth_path": "Understand that changing experiences are normal rather than problematic.",
        "environment_needs": "Healthy communities and positive environments.",
        "stress_behavior": "Disappointment, confusion, withdrawal.",
        "long_description": (
            "Reflectors are the rarest type in Human Design. Rather than operating from a fixed energetic "
            "identity, they mirror and amplify the qualities of their environment. This makes them uniquely "
            "valuable as evaluators of team culture, organizational health, and social dynamics. They often "
            "perceive problems long before others recognize them. Their quality of life is strongly "
            "determined by the environments they inhabit, making conscious selection of people, workplaces, "
            "and communities especially important."
        ),
    },
]


# ── MBTI type profiles ─────────────────────────────────────────────────────────

MBTI_PROFILES_SEED: list[dict] = [
    {
        "type_code": "INTJ",
        "type_name": "Architect",
        "group_name": "Analyst",
        "population_percent": "Overall: 2-3%, Male: 3-5%, Female: 1-2%",
        "dominant_function": "Introverted Intuition (Ni): Focuses on long-term patterns, underlying systems, future implications, and strategic foresight.",
        "auxiliary_function": "Extraverted Thinking (Te): Organizes resources, structures plans, measures outcomes, and drives execution.",
        "tertiary_function": "Introverted Feeling (Fi): Maintains internal values, personal integrity, and individual standards.",
        "inferior_function": "Extraverted Sensing (Se): Awareness of immediate reality, sensory details, and present-moment opportunities.",
        "core_motivation": "Build highly effective systems and achieve mastery through strategic understanding.",
        "core_desire": "Competence, autonomy, and long-term impact.",
        "core_fear": "Incompetence, dependency, and wasted potential.",
        "worldview": "Everything can be understood, optimized, and improved through deep analysis and strategic planning.",
        "information_processing": "Absorbs information broadly, then unconsciously synthesizes patterns into future-oriented insights.",
        "decision_making": "Prefers objective logic, measurable outcomes, and long-term optimization over short-term comfort.",
        "communication_style": "Direct, concise, analytical, and often focused on ideas rather than emotions.",
        "leadership_style": "Strategic architect who creates direction, designs systems, and delegates execution.",
        "conflict_style": "Challenges assumptions, focuses on root causes, and prioritizes effectiveness over harmony.",
        "relationship_style": "Selective, loyal, intellectually engaged, and deeply committed once trust is established.",
        "parenting_style": "Encourages independence, critical thinking, self-sufficiency, and intellectual development.",
        "learning_style": "Prefers conceptual understanding, systems thinking, and self-directed learning.",
        "work_style": "Independent, structured, future-focused, and driven by continuous improvement.",
        "career_patterns": "Strategy | Technology | Engineering | Research | Finance | Consulting | Architecture | Executive Leadership",
        "strengths": "Strategic vision | Long-term planning | Systems thinking | Independent learning | Problem solving | High standards | Intellectual rigor",
        "weaknesses": "Perfectionism | Impatience | Emotional detachment | Over-analysis | Difficulty delegating",
        "blind_spots": "Underestimating emotional factors | Assuming logic persuades everyone | Neglecting relationship maintenance",
        "stress_behavior": "Withdrawal | Excessive criticism | Isolation | Obsessive focus on flaws",
        "burnout_pattern": "Occurs when forced into excessive social demands, repetitive bureaucracy, or environments that reward politics over competence.",
        "growth_path": "Develop emotional intelligence | Improve interpersonal communication | Accept imperfection | Build collaborative influence",
        "emotional_pattern": "Processes emotions privately and often requires significant time before expressing them.",
        "team_role": "Strategist and architect.",
        "ideal_manager": "Competent, autonomous, objective, and outcome-focused.",
        "worst_manager": "Micromanaging, inconsistent, politically driven.",
        "ideal_environment": "Autonomy | Intellectual challenge | Meritocracy | Long-term projects",
        "financial_behavior": "Often focuses on long-term wealth creation, investment logic, and strategic allocation of resources.",
        "innovation_style": "Creates entirely new frameworks and systems.",
        "change_management_style": "Prefers proactive transformation based on future forecasting.",
        "risk_tolerance": "Moderate; willing to accept calculated risks when supported by analysis.",
        "scientific_evidence_level": "Moderate",
        "long_description": (
            "INTJs are often driven by a desire to understand how complex systems function and how those "
            "systems can be improved. Their dominant intuitive process naturally identifies patterns, trends, "
            "and future implications. Rather than reacting to immediate circumstances, they focus on creating "
            "long-term strategies that produce sustainable results. They are frequently drawn toward fields "
            "that reward expertise, innovation, and independent thinking. Their challenge is balancing "
            "strategic clarity with emotional awareness and recognizing that people are not purely rational actors."
        ),
    },
    {
        "type_code": "INTP",
        "type_name": "Logician",
        "group_name": "Analyst",
        "population_percent": "Overall: 3-4%",
        "dominant_function": "Introverted Thinking (Ti): Builds internal logical models and seeks conceptual precision.",
        "auxiliary_function": "Extraverted Intuition (Ne): Explores possibilities, alternatives, and connections.",
        "tertiary_function": "Introverted Sensing (Si): Stores detailed experiences and reference points.",
        "inferior_function": "Extraverted Feeling (Fe): Awareness of social harmony and group dynamics.",
        "core_motivation": "Understand how reality works through logic and conceptual analysis.",
        "core_desire": "Truth, understanding, and intellectual freedom.",
        "core_fear": "Being intellectually limited, controlled, or wrong.",
        "worldview": "Every assumption should be questioned and every model can be improved.",
        "information_processing": "Analyzes concepts deeply and explores multiple possibilities simultaneously.",
        "decision_making": "Prioritizes internal logical consistency above convention.",
        "communication_style": "Analytical, exploratory, curious, and often theoretical.",
        "leadership_style": "Leads through expertise, ideas, and problem-solving.",
        "conflict_style": "Debates concepts rather than people.",
        "relationship_style": "Values intellectual compatibility and personal freedom.",
        "parenting_style": "Encourages curiosity, questioning, and independent thought.",
        "learning_style": "Self-directed, experimental, theory-driven.",
        "work_style": "Flexible, idea-oriented, innovation-focused.",
        "career_patterns": "Research | Data Science | Software Development | Academia | Philosophy | Engineering",
        "strengths": "Analytical reasoning | Creativity | Conceptual thinking | Innovation | Problem solving",
        "weaknesses": "Procrastination | Overthinking | Difficulty finishing projects | Social awkwardness",
        "blind_spots": "Ignoring emotional impact | Analysis paralysis | Overvaluing theory",
        "stress_behavior": "Withdrawal | Obsessive analysis | Emotional outbursts",
        "burnout_pattern": "Occurs when creativity is restricted or excessive structure removes autonomy.",
        "growth_path": "Execute more consistently | Develop emotional awareness | Prioritize completion",
        "emotional_pattern": "Often intellectualizes emotions before experiencing them directly.",
        "team_role": "Innovator and analyst.",
        "ideal_manager": "Flexible, intelligent, non-controlling.",
        "worst_manager": "Rigid, bureaucratic, authoritarian.",
        "ideal_environment": "Freedom | Complex problems | Intellectual stimulation",
        "financial_behavior": "Varies widely; may focus more on ideas than financial optimization.",
        "innovation_style": "Generates novel theories and frameworks.",
        "change_management_style": "Explores possibilities before committing.",
        "risk_tolerance": "Moderate to high in intellectual pursuits.",
        "scientific_evidence_level": "Moderate",
        "long_description": (
            "INTPs seek understanding above certainty. Their minds naturally deconstruct assumptions, "
            "investigate principles, and construct increasingly refined models of reality. They are often "
            "fascinated by systems, theories, and abstract problems. Their challenge lies not in generating "
            "ideas but in consistently executing them."
        ),
    },
    {
        "type_code": "ENTJ",
        "type_name": "Commander",
        "group_name": "Analyst",
        "population_percent": "Overall: 2-3%",
        "core_motivation": "Achieve ambitious goals through leadership, organization, and execution.",
        "core_desire": "Achievement, influence, and effectiveness.",
        "core_fear": "Inefficiency, weakness, and lack of control.",
        "worldview": "Success comes from strategic action, discipline, and competent leadership.",
        "communication_style": "Direct, decisive, and outcome-oriented.",
        "leadership_style": "Commanding, strategic, and performance-focused.",
        "relationship_style": "Loyal, growth-oriented, and intellectually demanding.",
        "strengths": "Leadership | Execution | Decision making | Strategic planning",
        "weaknesses": "Impatience | Dominance | Insensitivity",
        "team_role": "Executive and organizer.",
        "financial_behavior": "Strong focus on growth, investment, and achievement.",
        "long_description": (
            "ENTJs naturally gravitate toward positions of responsibility because they are motivated to "
            "organize people and resources toward ambitious objectives. They excel at making difficult "
            "decisions and maintaining momentum during uncertainty. Their challenge is balancing performance "
            "expectations with empathy and relationship management."
        ),
    },
    {
        "type_code": "ENTP",
        "type_name": "Debater",
        "group_name": "Analyst",
        "population_percent": "Overall: 3-4%",
        "core_motivation": "Explore possibilities, challenge assumptions, and innovate.",
        "core_desire": "Freedom, discovery, and intellectual stimulation.",
        "core_fear": "Restriction, stagnation, and boredom.",
        "worldview": "Every system can be questioned and improved.",
        "communication_style": "Energetic, persuasive, curious, and provocative.",
        "leadership_style": "Visionary, entrepreneurial, opportunity-focused.",
        "relationship_style": "Playful, intellectually engaged, freedom-seeking.",
        "strengths": "Innovation | Adaptability | Persuasion | Creative problem solving",
        "weaknesses": "Impulsiveness | Inconsistency | Difficulty finishing",
        "team_role": "Innovator and challenger.",
        "financial_behavior": "Comfortable with calculated risk and experimentation.",
        "long_description": (
            "ENTPs thrive on novelty, possibility, and intellectual exploration. They enjoy identifying "
            "flaws in assumptions, generating unconventional solutions, and connecting ideas from different "
            "domains. Their energy often drives innovation and entrepreneurship. Their greatest challenge "
            "is maintaining focus long enough to fully execute their ideas."
        ),
    },
]


# ── Personal Color profiles ───────────────────────────────────────────────────

COLOR_PROFILES_SEED: list[dict] = [
    {
        "season": "Spring",
        "sub_types": "True Spring | Warm Spring | Light Spring",
        "energy_tone": "warm-light",
        "impression": "fresh | bright | approachable | optimistic",
        "communication_vibe": "warmth and enthusiasm over formality",
        "language_style": "conversational, energetic, positive framing, natural storytelling",
        "best_colors": "warm coral | peach | golden yellow | warm ivory | light camel",
        "avoid_styles": "heavy black | icy tones | overly formal structure | muted greys",
        "social_energy": "naturally inviting, easy warmth, generates enthusiasm in others",
        "coaching_notes": "Spring energy opens conversations easily. Leverage natural approachability. Avoid coming across as too casual in high-stakes situations — add structure deliberately.",
    },
    {
        "season": "Summer",
        "sub_types": "True Summer | Light Summer | Soft Summer",
        "energy_tone": "cool-muted",
        "impression": "calm | refined | trustworthy | understated elegant",
        "communication_vibe": "depth and thoughtfulness over volume",
        "language_style": "measured, empathetic, carefully worded, avoids confrontation",
        "best_colors": "soft rose | dusty blue | lavender | soft white | cool taupe",
        "avoid_styles": "harsh contrast | aggressive colour | loud statements | overly direct framing",
        "social_energy": "creates comfort and safety, others open up naturally around Summer energy",
        "coaching_notes": "Summer energy builds trust quietly. Use this as a strategic asset — people reveal more. Be careful not to over-soften important messages; directness is still needed.",
    },
    {
        "season": "Autumn",
        "sub_types": "True Autumn | Warm Autumn | Deep Autumn",
        "energy_tone": "warm-deep",
        "impression": "grounded | authoritative | reliable | natural leader",
        "communication_vibe": "substance and depth over style",
        "language_style": "narrative, grounded, rich detail, values-based framing",
        "best_colors": "warm brown | rust | deep olive | mustard | rich camel",
        "avoid_styles": "icy colours | overly bright | minimalist coldness | rushed impressions",
        "social_energy": "commands respect naturally, people trust Autumn energy with serious matters",
        "coaching_notes": "Autumn energy carries natural gravitas. Use deliberate pacing — pauses land well. Avoid rushing or lightening tone under pressure; the depth is the asset.",
    },
    {
        "season": "Winter",
        "sub_types": "True Winter | Bright Winter | Dark Winter",
        "energy_tone": "cool-clear",
        "impression": "authoritative | elegant | intense | precise",
        "communication_vibe": "depth and authority over warmth",
        "language_style": "declarative, structured, minimal small talk, precision over approximation",
        "best_colors": "pure white | true black | royal blue | deep burgundy | cool charcoal",
        "avoid_styles": "warm beige tones | excessive softness | vague language | casual framing",
        "social_energy": "commanding presence — few words land harder than most people's paragraphs",
        "coaching_notes": "Winter energy is naturally high-contrast and memorable. Silence is a tool — use it. Avoid over-explaining; Winter credibility erodes with excess words.",
    },
]


# ── Migration helper ───────────────────────────────────────────────────────────

def _ensure_goal_columns(eng) -> None:
    """Add missing columns to existing tables (idempotent)."""
    insp = inspect(eng)

    # 'goal' column on criteria tables
    for table in ("mbti_criteria", "hd_criteria"):
        existing = {c["name"] for c in insp.get_columns(table)}
        if "goal" not in existing:
            with eng.connect() as conn:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN goal VARCHAR(20)"))
                conn.commit()
            print(f"-> Added 'goal' column to {table}")

    # 'personal_color' column on user_profiles
    if "user_profiles" in insp.get_table_names():
        existing = {c["name"] for c in insp.get_columns("user_profiles")}
        if "personal_color" not in existing:
            with eng.connect() as conn:
                conn.execute(text("ALTER TABLE user_profiles ADD COLUMN personal_color VARCHAR(30)"))
                conn.commit()
            print("-> Added 'personal_color' column to user_profiles")


# ── Seed functions ─────────────────────────────────────────────────────────────

def seed_mbti(db) -> int:
    inserted = 0
    for mbti_type, pref, decision, weight, goal in MBTI_SEED:
        exists = (
            db.query(MbtiCriterion)
              .filter_by(mbti_type=mbti_type, preference=pref, goal=goal)
              .first()
        )
        if exists is None:
            db.add(MbtiCriterion(
                mbti_type=mbti_type, preference=pref,
                decision=decision, weight=weight, goal=goal,
            ))
            inserted += 1
    return inserted


def seed_hd(db) -> int:
    inserted = 0
    for hd_type, pref, decision, weight, goal in HD_SEED:
        exists = (
            db.query(HdCriterion)
              .filter_by(hd_type=hd_type, preference=pref, goal=goal)
              .first()
        )
        if exists is None:
            db.add(HdCriterion(
                hd_type=hd_type, preference=pref,
                decision=decision, weight=weight, goal=goal,
            ))
            inserted += 1
    return inserted


def seed_hd_profiles(db) -> int:
    inserted = 0
    for profile in HD_PROFILES_SEED:
        exists = db.query(HdTypeProfile).filter_by(hd_type=profile["hd_type"]).first()
        if exists is None:
            db.add(HdTypeProfile(**profile))
            inserted += 1
    return inserted


def seed_mbti_profiles(db) -> int:
    inserted = 0
    for profile in MBTI_PROFILES_SEED:
        exists = db.query(MbtiTypeProfile).filter_by(type_code=profile["type_code"]).first()
        if exists is None:
            db.add(MbtiTypeProfile(**profile))
            inserted += 1
    return inserted


def seed_color_profiles(db) -> int:
    inserted = 0
    for profile in COLOR_PROFILES_SEED:
        exists = db.query(PersonalColorProfile).filter_by(season=profile["season"]).first()
        if exists is None:
            db.add(PersonalColorProfile(**profile))
            inserted += 1
    return inserted


def seed_scenarios(db) -> int:
    inserted = 0
    for (mbti_type, hd_type, blend_summary, conflict_situation,
         conflict_sentence, recommended_sentence, recommended_action) in SCENARIO_SEED:
        exists = (
            db.query(MbtiHdScenario)
              .filter_by(mbti_type=mbti_type, hd_type=hd_type)
              .first()
        )
        if exists is None:
            db.add(MbtiHdScenario(
                mbti_type=mbti_type,
                hd_type=hd_type,
                blend_summary=blend_summary,
                conflict_situation=conflict_situation,
                conflict_sentence=conflict_sentence,
                recommended_sentence=recommended_sentence,
                recommended_action=recommended_action,
            ))
            inserted += 1
    return inserted


def main():
    reset   = "--reset"   in sys.argv
    migrate = "--migrate" in sys.argv

    print("-> Creating tables (if missing)…")
    Base.metadata.create_all(bind=engine)

    if migrate:
        print("-> --migrate: ensuring goal columns exist on criteria tables…")
        _ensure_goal_columns(engine)

    db = SessionLocal()
    try:
        if reset:
            print("-> --reset: clearing criteria, scenario, profile, recommendation, and memory tables…")
            db.query(RecommendationFeedback).delete()
            db.query(Recommendation).delete()
            db.query(AgentMemory).delete()
            db.query(MbtiHdScenario).delete()
            db.query(MbtiCriterion).delete()
            db.query(HdCriterion).delete()
            db.query(HdTypeProfile).delete()
            db.query(MbtiTypeProfile).delete()
            db.query(PersonalColorProfile).delete()
            db.commit()

        m  = seed_mbti(db)
        h  = seed_hd(db)
        s  = seed_scenarios(db)
        hp = seed_hd_profiles(db)
        mp = seed_mbti_profiles(db)
        cp = seed_color_profiles(db)
        db.commit()
        print(f"OK Inserted {m}  MBTI criteria rows.")
        print(f"OK Inserted {h}  HD criteria rows.")
        print(f"OK Inserted {s}  MBTI×HD scenario rows ({s}/80).")
        print(f"OK Inserted {hp} HD type profile rows ({hp}/5).")
        print(f"OK Inserted {mp} MBTI type profile rows ({mp}/16 planned).")
        print(f"OK Inserted {cp} Personal Color profile rows ({cp}/4).")
        print("OK Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
