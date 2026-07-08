"""AEHQ v2.0 — Adaptive Emotional Self-Reflection Questionnaire engine.

Screen flow:
  SAFETY → SUDS_INIT → [GROUNDING → SUDS_RERATE] → SITUATION
  → BODY_LOC → BODY_QUAL → EMOTIONS → QUESTION(s)
  → UNMET_NEED → COMPASSION → IFTHEN → RERATE → DONE
"""

from __future__ import annotations

import json
from typing import Any, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from models.orm import (
    AEHQSession, AEHQResponse, AEHQResult,
    AEHQFramework, AEHQSituation, AEHQSituationItem, AEHQFrameworkRule, AEHQScoreDelta,
)


# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE — 10 situations
# ═══════════════════════════════════════════════════════════════

SITUATIONS: dict[str, dict] = {
    "work": {
        "label": "Work or study pressure",
        "icon": "💼",
        "emotion_words": ["overwhelmed", "pressured", "depleted", "trapped", "resentful", "dread", "foggy", "inadequate"],
        "items": {
            "S": [
                {
                    "id": "w_s1", "input_type": "text", "skippable": False,
                    "question": "What's actually on the pile right now? Telegraph style — just the things, no full sentences needed.",
                    "subtext": "Listing it usually helps. Rough words are fine.",
                    "score_deltas": {"problem_control": 2},
                },
                {
                    "id": "w_s2", "input_type": "text", "skippable": True,
                    "question": "Finish this honestly: \"If I don't get this done, it means I am ___\"",
                    "subtext": "Only if something rings true — there's no right answer here.",
                    "score_deltas": {"shame_selfattack": 2, "anxiety_catastrophising": 1},
                },
            ],
            "D": [
                {
                    "id": "w_d1", "input_type": "text", "skippable": False,
                    "question": "If you were watching a friend in exactly this situation — what's the first thing a decent manager would take off their plate?",
                    "subtext": "Stepping back sometimes shows what's actually movable.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "w_r1", "input_type": "text", "skippable": False,
                    "question": "Is this a season with an end date, or a structure with no exit? What's the evidence for each?",
                    "subtext": "Take your time — no need to be certain.",
                    "score_deltas": {"problem_control": 2},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "rest",       "label": "Rest — I'm genuinely depleted"},
            {"id": "control",    "label": "Control over my own time"},
            {"id": "capable",    "label": "Feeling capable again"},
            {"id": "permission", "label": "Permission to say no"},
        ],
        "self_compassion": "You're not behind on being a person. Anyone carrying this load would feel it.",
        "ifthen_template": "If I sit down tomorrow, then I do only the first 25 minutes of my smallest task.",
    },
    "dismissed": {
        "label": "Feeling invisible or dismissed",
        "icon": "👻",
        "emotion_words": ["invisible", "unimportant", "hurt", "deflated", "quietly angry", "lonely", "resigned", "embarrassed"],
        "items": {
            "S": [
                {
                    "id": "di_s1", "input_type": "text", "skippable": False,
                    "question": "What happened — camera-view only. Who said or didn't say what?",
                    "subtext": "Just the facts of the moment, no interpretation needed yet.",
                    "score_deltas": {},
                },
                {
                    "id": "di_s2", "input_type": "single_select", "skippable": False,
                    "question": "Which landed harder: what they did, or what it seemed to say about your place with them?",
                    "subtext": "Did it sting more in the moment, or in what it hinted about where you stand?",
                    "options": [
                        {"id": "the_act",      "label": "What they did in the moment",
                         "score_deltas": {"anger_hidden_hurt": 1}},
                        {"id": "what_it_means","label": "What it seemed to say about where I stand",
                         "score_deltas": {"relationship_threat": 2, "shame_selfattack": 2}},
                        {"id": "both_equal",   "label": "Both felt equally hard",
                         "score_deltas": {"relationship_threat": 1, "shame_selfattack": 1, "anger_hidden_hurt": 1}},
                    ],
                    "score_deltas": {"relationship_threat": 1},
                },
            ],
            "D": [
                {
                    "id": "di_d1", "input_type": "text", "skippable": False,
                    "question": "A kind observer watches that moment. What do they see you needing that nobody noticed?",
                    "subtext": "What would they say about what you were carrying?",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "di_r1", "input_type": "text", "skippable": False,
                    "question": "When you're NOT being ignored — who notices you, and what do they notice?",
                    "subtext": "Take your time. Even one person counts.",
                    "score_deltas": {},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "seen",           "label": "Being seen and acknowledged"},
            {"id": "taken_seriously","label": "Being taken seriously"},
            {"id": "belonging",      "label": "Belonging here"},
            {"id": "mattering",      "label": "Knowing I matter to them"},
        ],
        "self_compassion": "Being overlooked hurts because mattering matters. Your need to be seen is not too much.",
        "ifthen_template": "If I feel invisible this week, I will say one sentence out loud within the first ten minutes.",
    },
    "authority": {
        "label": "Conflict with someone in authority",
        "icon": "⚡",
        "emotion_words": ["powerless", "unfairly treated", "intimidated", "angry", "humiliated", "anxious", "defiant", "torn"],
        "items": {
            "S": [
                {
                    "id": "au_s1", "input_type": "text", "skippable": False,
                    "question": "What exactly did they say or decide — and at which word did your body react?",
                    "subtext": "Rough memory is fine. What stood out?",
                    "score_deltas": {},
                },
                {
                    "id": "au_s2", "input_type": "single_select", "skippable": False,
                    "question": "Which is louder right now: the unfairness of it, or the danger of pushing back?",
                    "subtext": "Both are real. Which is taking up more space?",
                    "options": [
                        {"id": "unfairness", "label": "The unfairness — this wasn't right",
                         "score_deltas": {"anger_hidden_hurt": 2}},
                        {"id": "danger",     "label": "The risk — pushing back feels dangerous",
                         "score_deltas": {"anxiety_catastrophising": 2}},
                        {"id": "both",       "label": "Both are equally loud",
                         "score_deltas": {"anxiety_catastrophising": 1, "anger_hidden_hurt": 1}},
                    ],
                    "score_deltas": {"anger_hidden_hurt": 1},
                },
            ],
            "D": [
                {
                    "id": "au_d1", "input_type": "text", "skippable": False,
                    "question": "If a colleague you respect were treated this way — what would you say was unfair about it?",
                    "subtext": "Stepping outside the moment sometimes makes it clearer.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "au_r1", "input_type": "text", "skippable": False,
                    "question": "What have you already swallowed with this person? How much of today's weight is today's, and how much is the accumulated pile?",
                    "subtext": "Does this rhyme with other times?",
                    "score_deltas": {"rumination": 2},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "fairness",  "label": "Fairness — something wasn't right"},
            {"id": "respect",   "label": "Respect — being treated as a person"},
            {"id": "safety",    "label": "Safety to speak without consequences"},
            {"id": "autonomy",  "label": "Room to make my own decisions"},
        ],
        "self_compassion": "Feeling small in front of power is a human reflex, not weakness. Your read on unfairness deserves a hearing.",
        "ifthen_template": "If I decide to raise it, I'll write one factual sentence — what happened + what I'm asking for — before the conversation.",
    },
    "self_criticism": {
        "label": "Self-criticism or shame",
        "icon": "🌀",
        "emotion_words": ["ashamed", "small", "exposed", "worthless", "fraudulent", "disgusted with myself", "tired of myself", "humiliated"],
        "items": {
            "S": [
                {
                    "id": "sc_s1", "input_type": "text", "skippable": True,
                    "question": "What are the critic's exact words? Quote it — or paraphrase if that's easier.",
                    "subtext": "Only if you're willing. Naming the voice often weakens it a little.",
                    "score_deltas": {"shame_selfattack": 3},
                },
                {
                    "id": "sc_s2", "input_type": "text", "skippable": False,
                    "question": "Whose voice does the critic borrow? Does the accent belong to someone from your past?",
                    "subtext": "Just a rough guess. Even 'not sure' is useful.",
                    "score_deltas": {"shame_selfattack": 1},
                },
            ],
            "D": [
                {
                    "id": "sc_d1", "input_type": "text", "skippable": False,
                    "question": "If your closest friend said those exact words about themselves — what's the first thing you'd feel toward them?",
                    "subtext": "Take your time with this one.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "sc_r1", "input_type": "text", "skippable": False,
                    "question": "What is the critic trying to protect you from? It usually has a job — even if it does it badly.",
                    "subtext": "A rough guess is more than enough.",
                    "score_deltas": {},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "acceptance",        "label": "Acceptance — as I already am"},
            {"id": "my_standard",       "label": "A standard I actually chose myself"},
            {"id": "rest_from_watching","label": "Rest from watching myself so closely"},
            {"id": "proof",             "label": "Evidence that counts — not just reassurance"},
        ],
        "self_compassion": "Try, in your own words: \"This is a moment of struggle. Struggle is human. May I be on my own side today.\"",
        "ifthen_template": "If the critic starts tonight, I'll write down one thing from the last 7 days it is conveniently ignoring.",
    },
    "anxiety": {
        "label": "Worry about the future",
        "icon": "🌪",
        "emotion_words": ["dread", "restless", "frozen", "scattered", "powerless", "on-edge", "braced", "overwhelmed"],
        "items": {
            "S": [
                {
                    "id": "ax_s1", "input_type": "text", "skippable": False,
                    "question": "Name the unknown in one line: \"I don't know whether ___\"",
                    "subtext": "Just the thing you're most unsure about right now.",
                    "score_deltas": {"anxiety_catastrophising": 2},
                },
                {
                    "id": "ax_s2", "input_type": "slider", "skippable": False,
                    "question": "Roughly what % of this worry is actually inside your control?",
                    "subtext": "A rough number is fine — 0 means nothing, 100 means most of it is up to you.",
                    "slider_min": 0, "slider_max": 100, "slider_step": 10,
                    "slider_labels": {"0": "Nothing — all out of my hands", "50": "About half", "100": "Most is up to me"},
                    "score_deltas": {},
                    "value_scoring": "percent_control",
                },
            ],
            "D": [
                {
                    "id": "ax_d1", "input_type": "text", "skippable": False,
                    "question": "Picture yourself five years from now, on the other side, having coped. What does that version of you know that you can't quite see yet?",
                    "subtext": "A rough guess is enough.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "ax_r1", "input_type": "text", "skippable": False,
                    "question": "What decision are you postponing until you feel certain — and what is the waiting costing?",
                    "subtext": "No need to solve it here — just naming it is enough.",
                    "score_deltas": {"anxiety_catastrophising": 2, "avoidance": 2},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "certainty",   "label": "Certainty — even knowing I can rarely have it"},
            {"id": "confidence",  "label": "Confidence I could cope either way"},
            {"id": "plan",        "label": "A plan for the part I can control"},
            {"id": "company",     "label": "Company in the waiting — not being alone with it"},
        ],
        "self_compassion": "A mind that scans the future is trying to keep you safe. You can be scared and still choose your next step.",
        "ifthen_template": "If the worry starts tonight, I write it in the worry list and close the notebook — it gets its 15 minutes tomorrow.",
    },
    "grief": {
        "label": "Grief or a painful loss",
        "icon": "🕯",
        "emotion_words": ["yearning", "hollow", "heavy", "guilty", "relieved-then-guilty", "disbelief", "tender", "empty"],
        "items": {
            "S": [
                {
                    "id": "g_s1", "input_type": "text", "skippable": False,
                    "question": "What did you lose? One plain sentence — you don't have to explain or justify it.",
                    "subtext": None,
                    "score_deltas": {"grief_meaningloss": 3},
                },
                {
                    "id": "g_s2", "input_type": "text", "skippable": True,
                    "question": "Is there a feeling you think you're not allowed to have here — relief, anger, nothing at all? All of those are documented, normal grief.",
                    "subtext": "If one of yours feels forbidden, you can name it here.",
                    "score_deltas": {"shame_selfattack": 1},
                },
            ],
            "D": [
                {
                    "id": "g_d1", "input_type": "text", "skippable": False,
                    "question": "Watching yourself from across the room this week — what are you carrying that most people haven't noticed?",
                    "subtext": "What would an outside observer see?",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "g_r1", "input_type": "text", "skippable": False,
                    "question": "What did they — or it — make possible in your life? Which doors are truly closed, and which are only closed for now?",
                    "subtext": "Take your time. There's no right answer.",
                    "score_deltas": {"grief_meaningloss": 2},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "permission",    "label": "Permission to grieve at my own pace"},
            {"id": "remember_with", "label": "Someone to remember with me"},
            {"id": "rest",          "label": "Rest — I'm exhausted by it"},
            {"id": "honor",         "label": "A way to honor them or it"},
        ],
        "self_compassion": "Grief is love with nowhere to go yet. You're allowed to take this at your own speed — including the okay days.",
        "ifthen_template": "If the hard moment arrives this week, I will light a candle / play a song / write them three lines.",
    },
    "anger": {
        "label": "Anger that might be hiding something",
        "icon": "🔥",
        "emotion_words": ["furious", "betrayed", "unappreciated", "bitter", "protective", "hurt underneath", "wounded", "resentful"],
        "items": {
            "S": [
                {
                    "id": "an_s1", "input_type": "text", "skippable": False,
                    "question": "Replay the moment. What happened one second before the anger arrived?",
                    "subtext": "Anger is often the second emotion. What came first?",
                    "score_deltas": {"anger_hidden_hurt": 3},
                },
                {
                    "id": "an_s2", "input_type": "text", "skippable": True,
                    "question": "If the anger could only speak one sentence starting with \"It hurt when…\" — what would it say?",
                    "subtext": "Only if it rings true. Some anger is just anger — that's a full answer too.",
                    "score_deltas": {"anger_hidden_hurt": 2},
                },
            ],
            "D": [
                {
                    "id": "an_d1", "input_type": "text", "skippable": False,
                    "question": "A fly on the wall watches the scene. What does it see you feeling first — before the anger armor goes on?",
                    "subtext": "Step back from it for a moment.",
                    "score_deltas": {"anger_hidden_hurt": 2},
                },
            ],
            "R": [
                {
                    "id": "an_r1", "input_type": "text", "skippable": False,
                    "question": "What does the anger protect? What would be at risk if you showed the hurt instead?",
                    "subtext": "No judgment on the answer.",
                    "score_deltas": {},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "acknowledgment",     "label": "Acknowledgment of the hurt"},
            {"id": "apology",            "label": "An apology — something to be made right"},
            {"id": "mattering",          "label": "Mattering to them"},
            {"id": "safety_to_be_soft",  "label": "Safety to be soft without it being used against me"},
        ],
        "self_compassion": "Anger that guards a wound is loyalty to yourself. The hurt under it is allowed to exist.",
        "ifthen_template": "If I'm still hot in an hour, I write the \"It hurt when…\" sentence somewhere private before deciding anything.",
    },
    "numbness": {
        "label": "Feeling numb or emotionally flat",
        "icon": "🌫",
        "emotion_words": ["numb", "empty", "flat", "distant", "foggy", "disconnected", "nothing at all", "hollow"],
        "items": {
            "S": [
                {
                    "id": "n_s1", "input_type": "text", "skippable": False,
                    "question": "On the outside of the numbness — is there 1% of anything? Heaviness, static, tiredness? Zero is also a real answer.",
                    "subtext": "No demand to feel. Even noticing the absence is something.",
                    "score_deltas": {"numbness_shutdown": 2},
                },
                {
                    "id": "n_s2", "input_type": "single_select", "skippable": False,
                    "question": "When did the volume go down — after one event, or slowly over weeks?",
                    "subtext": "Just a rough sense.",
                    "options": [
                        {"id": "one_event", "label": "After something specific happened",
                         "score_deltas": {"numbness_shutdown": 2, "grief_meaningloss": 1}},
                        {"id": "gradually", "label": "Gradually, over time",
                         "score_deltas": {"numbness_shutdown": 2}},
                        {"id": "not_sure",  "label": "I'm not sure when it started",
                         "score_deltas": {"numbness_shutdown": 1}},
                    ],
                    "score_deltas": {"numbness_shutdown": 1},
                },
            ],
            "D": [
                {
                    "id": "n_d1", "input_type": "text", "skippable": False,
                    "question": "If a documentary narrator described your last two weeks, what would they say you've been through?",
                    "subtext": "You don't have to feel it — just describe it from the outside.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "n_r1", "input_type": "text", "skippable": False,
                    "question": "What did you used to feel most — which feeling went quiet first?",
                    "subtext": "Only if something comes up. 'I don't know' is a real answer.",
                    "score_deltas": {"numbness_shutdown": 1},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "rest",            "label": "Rest — real rest, not just a break"},
            {"id": "safety_to_feel",  "label": "Safety to feel again slowly, without being rushed"},
            {"id": "connection",      "label": "Connection — even one small moment of it"},
            {"id": "no_demands",      "label": "Time without demands or expectations"},
        ],
        "self_compassion": "Numbness is often the mind's circuit-breaker, not a defect. Something in you decided to protect you — you can thank it and still want the feeling back.",
        "ifthen_template": "If I make tea tomorrow, I hold the cup for 30 seconds and just notice warm.",
    },
    "relationship": {
        "label": "Anxiety in a relationship",
        "icon": "💔",
        "emotion_words": ["anxious", "unwanted", "jealous", "on-edge", "unsure of my place", "clingy-then-ashamed", "braced for the ending", "scared"],
        "items": {
            "S": [
                {
                    "id": "r_s1", "input_type": "text", "skippable": False,
                    "question": "What was the trigger — a message, a silence, a tone? Camera-view only.",
                    "subtext": "Just the event, not yet what it means.",
                    "score_deltas": {"relationship_threat": 2},
                },
                {
                    "id": "r_s2", "input_type": "text", "skippable": False,
                    "question": "Finish this: \"It felt like it meant ___\"",
                    "subtext": "What did the silence or tone seem to say?",
                    "score_deltas": {"relationship_threat": 3, "anxiety_catastrophising": 1},
                },
            ],
            "D": [
                {
                    "id": "r_d1", "input_type": "text", "skippable": False,
                    "question": "If your most secure friend read this situation — what would they bet is actually going on?",
                    "subtext": "Not the scary story, but the calm read.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "r_r1", "input_type": "text", "skippable": False,
                    "question": "When the fear says \"they're leaving\" — how often has that alarm been right before? What's its actual track record?",
                    "subtext": "Just a rough sense — no need to count every time.",
                    "score_deltas": {"relationship_threat": 1},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "reassurance",  "label": "Reassurance I can actually trust"},
            {"id": "consistency",  "label": "Consistency — knowing where I stand"},
            {"id": "security",     "label": "Feeling secure inside myself, not just from them"},
            {"id": "steadiness",   "label": "The relationship itself to feel safe"},
        ],
        "self_compassion": "Wanting to feel secure with someone is wiring, not weakness. Your need for steadiness is legitimate.",
        "ifthen_template": "If the urge to check or re-ask hits, I wait 20 minutes and write the fear down first — then decide.",
    },
    "trapped": {
        "label": "Feeling trapped or unable to say no",
        "icon": "🔒",
        "emotion_words": ["trapped", "suffocated", "resentful", "obligated", "guilty-in-advance", "invisible", "exhausted", "cornered"],
        "items": {
            "S": [
                {
                    "id": "t_s1", "input_type": "text", "skippable": False,
                    "question": "What did you say yes to that your body said no to? Name the most recent one.",
                    "subtext": "Specific is more useful than the general pattern.",
                    "score_deltas": {"avoidance": 2, "problem_control": -1},
                },
                {
                    "id": "t_s2", "input_type": "text", "skippable": False,
                    "question": "Finish this: \"If I say no, then ___\"",
                    "subtext": "First guess is enough — what's the scary ending after the no?",
                    "score_deltas": {"anxiety_catastrophising": 2, "shame_selfattack": 1},
                },
            ],
            "D": [
                {
                    "id": "t_d1", "input_type": "text", "skippable": False,
                    "question": "If you watched a friend carrying this exact obligation load — what would you tell them they're allowed to put down?",
                    "subtext": "What would you say to them that you haven't said to yourself?",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "t_r1", "input_type": "text", "skippable": False,
                    "question": "Whose rule is \"a good person doesn't refuse\"? Did you ever actually agree to it?",
                    "subtext": "Where did that rule come from?",
                    "score_deltas": {"shame_selfattack": 1, "avoidance": 1},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "permission",          "label": "Permission — my own, to say no"},
            {"id": "room_to_choose",      "label": "Room to actually choose, not just comply"},
            {"id": "rest",                "label": "Rest — from the relentlessness of it"},
            {"id": "relationship_survives","label": "A relationship that can survive a no"},
        ],
        "self_compassion": "A no to them is often a yes to you — that's not selfish, it's a boundary. Your limits are information, not betrayal.",
        "ifthen_template": "If a request lands this week, my first sentence is \"Let me check and come back to you\" — the no gets to be a two-step.",
    },
    "other": {
        "label": "Something else",
        "icon": "💬",
        "emotion_words": ["heavy", "unsettled", "confused", "sad", "tense", "raw", "stuck", "tired"],
        "items": {
            "S": [
                {
                    "id": "o_s1", "input_type": "text", "skippable": False,
                    "question": "In your own words — what's sitting with you right now? Rough is fine.",
                    "subtext": "There's no category for this one, so the words are all yours.",
                    "score_deltas": {},
                },
                {
                    "id": "o_s2", "input_type": "text", "skippable": True,
                    "question": "If this feeling had a message for you, what would it be trying to say?",
                    "subtext": "First guess counts. Skip if nothing comes.",
                    "score_deltas": {},
                },
            ],
            "D": [
                {
                    "id": "o_d1", "input_type": "text", "skippable": False,
                    "question": "If a kind stranger watched your week from the outside — what would they say you've been carrying?",
                    "subtext": "Describe it from across the room.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    "id": "o_r1", "input_type": "text", "skippable": False,
                    "question": "When did you first notice this? Has anything like it visited before?",
                    "subtext": "Just a rough timeline — patterns sometimes show themselves.",
                    "score_deltas": {"rumination": 1},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "understood", "label": "Being understood"},
            {"id": "rest",       "label": "Rest — a real pause"},
            {"id": "clarity",    "label": "Clarity about what this even is"},
            {"id": "company",    "label": "Not being alone with it"},
        ],
        "self_compassion": "You showed up for this without even a name for it — that takes honesty. Whatever it is, it's allowed to take up space.",
        "ifthen_template": "If this feeling returns tomorrow, I will write three rough lines about it before doing anything else.",
    },
}


# Choosing a situation is itself strong signal — seed the matching scores
# so the priority stack can actually reach its thresholds.
SITUATION_PRIORS: dict[str, dict[str, float]] = {
    "work":           {"problem_control": 3},
    "dismissed":      {"relationship_threat": 3, "shame_selfattack": 1},
    "authority":      {"anger_hidden_hurt": 2, "problem_control": 2},
    "self_criticism": {"shame_selfattack": 4},
    "anxiety":        {"anxiety_catastrophising": 4},
    "grief":          {"grief_meaningloss": 4},
    "anger":          {"anger_hidden_hurt": 4},
    "numbness":       {"numbness_shutdown": 4},
    "relationship":   {"relationship_threat": 4},
    "trapped":        {"avoidance": 3, "problem_control": 1},
    "other":          {},
}

# Body quality carries signal too (spec: somatic markers feed scoring).
BODY_QUALITY_DELTAS: dict[str, dict[str, float]] = {
    "hot":     {"anger_hidden_hurt": 1},
    "buzzing": {"anxiety_catastrophising": 1},
    "hollow":  {"numbness_shutdown": 1, "grief_meaningloss": 0.5},
    "frozen":  {"numbness_shutdown": 1.5},
}

# Where the feeling sits in the body is signal as well (kept mild: 0.5–2).
BODY_LOCATION_DELTAS: dict[str, dict[str, float]] = {
    "throat":        {"anger_hidden_hurt": 0.5},          # the classic held-back voice
    "stomach":       {"anxiety_catastrophising": 1},
    "shoulders_jaw": {"anger_hidden_hurt": 0.5, "anxiety_catastrophising": 0.5},
    "chest":         {"grief_meaningloss": 0.5},
    "everywhere":    {"anxiety_catastrophising": 0.5},
    "nowhere_numb":  {"numbness_shutdown": 2},            # the strongest single marker
}

# The unmet need is the user's own explicit statement of what's wrong —
# it must feed framework selection. Keyed "situation:need_id" because the
# same id means different things in different situations (rest in work =
# depletion; rest in grief = exhausted grieving).
UNMET_NEED_DELTAS: dict[str, dict[str, float]] = {
    # work
    "work:rest":                    {"numbness_shutdown": 2, "problem_control": -1},
    "work:control":                 {"problem_control": 2},
    "work:capable":                 {"shame_selfattack": 2},
    # "permission to say no" is an explicit boundary need — strong ACT signal,
    # and it means the pile itself is not the problem, so damp problem_control.
    "work:permission":              {"avoidance": 4, "problem_control": -2},
    # dismissed
    "dismissed:seen":               {"relationship_threat": 1},
    "dismissed:taken_seriously":    {"anger_hidden_hurt": 1.5},
    "dismissed:belonging":          {"relationship_threat": 2},
    "dismissed:mattering":          {"relationship_threat": 1.5, "shame_selfattack": 0.5},
    # authority
    "authority:fairness":           {"anger_hidden_hurt": 2},
    "authority:respect":            {"anger_hidden_hurt": 1.5, "shame_selfattack": 0.5},
    "authority:safety":             {"anxiety_catastrophising": 2},
    "authority:autonomy":           {"problem_control": 1.5},
    # self_criticism
    "self_criticism:acceptance":    {"shame_selfattack": 1},
    "self_criticism:my_standard":   {"shame_selfattack": 0.5, "problem_control": 1},
    "self_criticism:rest_from_watching": {"shame_selfattack": 1, "rumination": 2},
    "self_criticism:proof":         {"anxiety_catastrophising": 1},
    # anxiety
    "anxiety:certainty":            {"anxiety_catastrophising": 1},
    "anxiety:confidence":           {"anxiety_catastrophising": 0.5, "shame_selfattack": 1},
    "anxiety:plan":                 {"problem_control": 2},
    "anxiety:company":              {"relationship_threat": 1},
    # grief
    "grief:permission":             {"grief_meaningloss": 1, "shame_selfattack": 1},
    "grief:remember_with":          {"grief_meaningloss": 1, "relationship_threat": 0.5},
    "grief:rest":                   {"grief_meaningloss": 0.5, "numbness_shutdown": 1.5},
    "grief:honor":                  {"grief_meaningloss": 1.5},
    # anger
    "anger:acknowledgment":         {"anger_hidden_hurt": 1.5},
    "anger:apology":                {"anger_hidden_hurt": 1},
    "anger:mattering":              {"anger_hidden_hurt": 0.5, "relationship_threat": 1.5},
    "anger:safety_to_be_soft":      {"anger_hidden_hurt": 1, "relationship_threat": 1},
    # numbness
    "numbness:rest":                {"numbness_shutdown": 1},
    "numbness:safety_to_feel":      {"numbness_shutdown": 1.5},
    "numbness:connection":          {"relationship_threat": 1.5, "numbness_shutdown": 0.5},
    "numbness:no_demands":          {"numbness_shutdown": 1, "avoidance": 1},
    # relationship
    "relationship:reassurance":     {"relationship_threat": 1.5},
    "relationship:consistency":     {"relationship_threat": 1},
    "relationship:security":        {"relationship_threat": 1, "shame_selfattack": 0.5},
    "relationship:steadiness":      {"relationship_threat": 1},
    # trapped
    "trapped:permission":           {"avoidance": 1.5},
    "trapped:room_to_choose":       {"avoidance": 1, "problem_control": 1},
    "trapped:rest":                 {"avoidance": 0.5, "numbness_shutdown": 1.5},
    "trapped:relationship_survives":{"relationship_threat": 2},
    # other
    "other:understood":             {"relationship_threat": 1},
    "other:rest":                   {"numbness_shutdown": 1},
    "other:clarity":                {"rumination": 1.5},
    "other:company":                {"relationship_threat": 1},
}


# ═══════════════════════════════════════════════════════════════
# FRAMEWORK LIBRARY
# ═══════════════════════════════════════════════════════════════

FRAMEWORKS: dict[str, dict] = {
    "F5_DBT": {
        "name": "Grounding & Regulation (DBT-informed)",
        "evidence": "Linehan (1993); Linehan et al. (2006)",
        "tier": "A",
        "technique": (
            "**TIPP:** Temperature · Intense exercise · Paced breathing · Progressive relaxation\n\n"
            "Start right now: breathe in for 4 counts, out for 6 counts. Do eight rounds. "
            "When the eight rounds are done, check your number again."
        ),
    },
    "F8_somatic": {
        "name": "Somatic Grounding",
        "evidence": "Zaccaro et al. (2018); Farb et al. (2015)",
        "tier": "B",
        "technique": (
            "**5-4-3-2-1 anchor:** Name 5 things you can see · 4 you can touch · 3 you can hear · "
            "2 you can smell · 1 you can taste.\n\n"
            "Alternatively: hold something warm for 30 seconds — notice only the warmth."
        ),
    },
    "F3_CFT": {
        "name": "Self-Compassion (CFT / MSC)",
        "evidence": "Neff & Germer (2013) RCT; Kirby et al. (2017) meta-analysis",
        "tier": "A",
        "technique": (
            "**Self-Compassion Break (3 minutes):**\n"
            "1. Place a hand on your heart. Say: \"This is a moment of suffering.\"\n"
            "2. Say: \"Suffering is part of being human. I am not alone in this.\"\n"
            "3. Ask: \"What would I say to a close friend feeling this?\" — then say that to yourself."
        ),
    },
    "F6_EFT": {
        "name": "Emotion-Focused (Primary Emotion Access)",
        "evidence": "Greenberg (2002); Greenberg & Watson (2006)",
        "tier": "B",
        "technique": (
            "**One-second-before probe:**\n"
            "Replay the moment. What came one second before the anger?\n\n"
            "If it lands: write one sentence starting \"It hurt when...\" — somewhere private. "
            "Don't decide anything yet."
        ),
    },
    "F14_grief": {
        "name": "Grief — Dual Process Normalization",
        "evidence": "Stroebe & Schut (1999); Shear et al. (2005) RCT",
        "tier": "B",
        "technique": (
            "**The oscillation model:** Grief moves between loss-focus (missing them, crying, feeling it) "
            "and restoration-focus (managing life, okay moments, even smiling).\n\n"
            "The okay days are not betrayal. They are healthy grief doing its job.\n\n"
            "This week: allow one restoration hour without guilt."
        ),
    },
    "F15_attachment": {
        "name": "Attachment-Informed Regulation",
        "evidence": "Mikulincer & Shaver (2007); Johnson (2019)",
        "tier": "B",
        "technique": (
            "**The alarm audit:**\n"
            "Write: \"The alarm says [feared thing].\"\n"
            "Then write its track record — how often has this exact alarm been right before?\n\n"
            "When the urge to check or ask arrives: wait 20 minutes. Write the fear first. Then decide."
        ),
    },
    "F1_CBT": {
        "name": "Cognitive Reappraisal (CBT)",
        "evidence": "Butler et al. (2006) meta-analysis; Hofmann et al. (2012)",
        "tier": "A",
        "technique": (
            "**Likelihood check:**\n"
            "Write the worst-case in one sentence. Then:\n"
            "1. What's the actual % chance this happens?\n"
            "2. If it did happen — what would I do?\n"
            "3. What's the realistic case?\n\n"
            "The goal is accurate thinking, not positive thinking."
        ),
    },
    "F9_MBCT": {
        "name": "Mindful Observation (MBCT-informed)",
        "evidence": "Kuyken et al. (2016) individual patient-data meta-analysis",
        "tier": "A",
        "technique": (
            "**Watch the thought, don't board it:**\n"
            "Sit for 2 minutes. When a thought arrives, label it: 'There's the worry.' "
            "'There's the self-criticism.' Don't try to solve it — just notice it as a thought, not a fact.\n\n"
            "Set a timer. When it goes off, you're done."
        ),
    },
    "F10_PST": {
        "name": "Problem-Solving (PST)",
        "evidence": "Malouff et al. (2007) meta-analysis",
        "tier": "A",
        "technique": (
            "**Four steps on the one thing:**\n"
            "1. Define it in one sentence (the actual problem, not everything)\n"
            "2. List 3 options — including imperfect ones\n"
            "3. Pick the smallest one you could try this week\n"
            "4. Write the if-then: If [situation], then I will [action]."
        ),
    },
    "F4_ACT": {
        "name": "Acceptance & Values (ACT)",
        "evidence": "Hayes et al. (2006); A-Tjak et al. (2015) meta-analysis",
        "tier": "A",
        "technique": (
            "**Values question:** \"If the fear had no vote — what would you choose?\"\n\n"
            "**Defusion:** When a painful thought arrives, try: "
            "'I'm having the thought that [thought].' Notice the gap between you and the thought.\n\n"
            "**Willingness:** Can you let the discomfort be here for 10 more seconds, without fighting it?"
        ),
    },
    "F2_BA": {
        "name": "Behavioural Activation",
        "evidence": "Ekers et al. (2014) meta-analysis; Jacobson et al. (1996)",
        "tier": "A",
        "technique": (
            "**One 5-minute thing** that used to give even 1% of something:\n\n"
            "It doesn't have to feel good — just schedule it. Do it. "
            "Then notice: did your mood shift even slightly after vs before?\n\n"
            "The goal is re-engagement, not enjoyment yet."
        ),
    },
    "F12_ifthen": {
        "name": "Implementation Intention",
        "evidence": "Gollwitzer & Sheeran (2006) meta-analysis (k=94)",
        "tier": "A",
        "technique": (
            "**If-then plan:**\n"
            "If [specific trigger], then I will [specific action].\n\n"
            "The more concrete the trigger and action, the more effective the plan. "
            "Start with the plan you wrote above."
        ),
    },
}

# ── Framework-selection mapping (the priority stack, now data) ────────────────
# Evaluated in listed order; first rule whose score(var) is in [min, max) wins.
# max=None means open-ended (>= min). score_var "__default__" always matches.
# High band = 7–10, Medium band = 4–7. Kept identical to the previous if-chain.
FRAMEWORK_RULES: list[dict] = [
    {"priority_label": "P1",   "score_var": "suds",                    "min_val": 8, "max_val": None, "framework_code": "F5_DBT"},
    {"priority_label": "P2",   "score_var": "numbness_shutdown",       "min_val": 7, "max_val": None, "framework_code": "F8_somatic"},
    {"priority_label": "P3",   "score_var": "shame_selfattack",        "min_val": 7, "max_val": None, "framework_code": "F3_CFT"},
    {"priority_label": "P4",   "score_var": "anger_hidden_hurt",       "min_val": 7, "max_val": None, "framework_code": "F6_EFT"},
    {"priority_label": "P5",   "score_var": "grief_meaningloss",       "min_val": 7, "max_val": None, "framework_code": "F14_grief"},
    {"priority_label": "P6",   "score_var": "relationship_threat",     "min_val": 7, "max_val": None, "framework_code": "F15_attachment"},
    {"priority_label": "P7",   "score_var": "anxiety_catastrophising", "min_val": 7, "max_val": None, "framework_code": "F1_CBT"},
    {"priority_label": "P8",   "score_var": "rumination",              "min_val": 7, "max_val": None, "framework_code": "F9_MBCT"},
    {"priority_label": "P9",   "score_var": "problem_control",         "min_val": 7, "max_val": None, "framework_code": "F10_PST"},
    {"priority_label": "P10",  "score_var": "avoidance",               "min_val": 7, "max_val": None, "framework_code": "F4_ACT"},
    {"priority_label": "P3m",  "score_var": "shame_selfattack",        "min_val": 4, "max_val": 7,    "framework_code": "F3_CFT"},
    {"priority_label": "P4m",  "score_var": "anger_hidden_hurt",       "min_val": 4, "max_val": 7,    "framework_code": "F6_EFT"},
    {"priority_label": "P7m",  "score_var": "anxiety_catastrophising", "min_val": 4, "max_val": 7,    "framework_code": "F1_CBT"},
    {"priority_label": "P2m",  "score_var": "numbness_shutdown",       "min_val": 4, "max_val": 7,    "framework_code": "F2_BA"},
    {"priority_label": "P5m",  "score_var": "grief_meaningloss",       "min_val": 4, "max_val": 7,    "framework_code": "F14_grief"},
    {"priority_label": "P6m",  "score_var": "relationship_threat",     "min_val": 4, "max_val": 7,    "framework_code": "F15_attachment"},
    {"priority_label": "P8m",  "score_var": "rumination",              "min_val": 4, "max_val": 7,    "framework_code": "F9_MBCT"},
    {"priority_label": "P9m",  "score_var": "problem_control",         "min_val": 4, "max_val": 7,    "framework_code": "F10_PST"},
    {"priority_label": "P10m", "score_var": "avoidance",               "min_val": 4, "max_val": 7,    "framework_code": "F4_ACT"},
    {"priority_label": "DEFAULT", "score_var": "__default__",          "min_val": 0, "max_val": None, "framework_code": "F12_ifthen"},
]

VALIDATION_POOL = [
    "That makes sense, given what you just described.",
    "You put that into words — that's harder than it looks.",
    "Rough words are fine. There's no grading here.",
    "Noticing it counts, even when it's hard to name.",
    "You showed up for this — that matters.",
    "That took something to write. Take your time with the next one.",
]

SAFETY_SCRIPT = (
    "Thank you for telling me. Your safety matters more than any session.\n\n"
    "Please reach out to someone right now:\n"
    "• **Crisis text:** Text HOME to 741741\n"
    "• **Lifeline:** 988 (call or text, US)\n"
    "• **Thailand:** 1323 (กรมสุขภาพจิต)\n"
    "• **International:** findahelpline.com\n\n"
    "If you are in immediate danger, please call emergency services.\n\n"
    "This session is paused. Please come back when you're safe."
)

GROUNDING_PAUSE_SCRIPT = (
    "Your body is telling us something important — let's honor that.\n\n"
    "The questions will be here another time. For now, just this:\n\n"
    "**4-7-8 breathing:** In for 4 · Hold for 7 · Out for 8\n\n"
    "Do that three times, then find something warm to hold.\n\n"
    "Come back when you're ready. There's no rush."
)


# Emotion-word picks each carry +1 toward the variable they signal.
EMOTION_WORD_DELTAS: dict[str, dict[str, float]] = {
    # shame / self-attack
    "ashamed": {"shame_selfattack": 1}, "small": {"shame_selfattack": 1},
    "exposed": {"shame_selfattack": 1}, "worthless": {"shame_selfattack": 1.5},
    "fraudulent": {"shame_selfattack": 1}, "disgusted with myself": {"shame_selfattack": 1.5},
    "humiliated": {"shame_selfattack": 1}, "tired of myself": {"shame_selfattack": 1},
    "inadequate": {"shame_selfattack": 1}, "embarrassed": {"shame_selfattack": 0.5},
    "clingy-then-ashamed": {"shame_selfattack": 1, "relationship_threat": 1},
    "guilty-in-advance": {"shame_selfattack": 1},
    # anger / hidden hurt
    "furious": {"anger_hidden_hurt": 1}, "betrayed": {"anger_hidden_hurt": 1},
    "bitter": {"anger_hidden_hurt": 1}, "resentful": {"anger_hidden_hurt": 1},
    "hurt underneath": {"anger_hidden_hurt": 1.5}, "wounded": {"anger_hidden_hurt": 1},
    "quietly angry": {"anger_hidden_hurt": 1}, "defiant": {"anger_hidden_hurt": 0.5},
    "unappreciated": {"anger_hidden_hurt": 1},
    # anxiety / catastrophising
    "dread": {"anxiety_catastrophising": 1}, "restless": {"anxiety_catastrophising": 1},
    "on-edge": {"anxiety_catastrophising": 1}, "braced": {"anxiety_catastrophising": 1},
    "scattered": {"anxiety_catastrophising": 1}, "anxious": {"anxiety_catastrophising": 1},
    "scared": {"anxiety_catastrophising": 1}, "intimidated": {"anxiety_catastrophising": 1},
    "braced for the ending": {"anxiety_catastrophising": 1, "relationship_threat": 1},
    # numbness / shutdown
    "numb": {"numbness_shutdown": 1.5}, "empty": {"numbness_shutdown": 1},
    "flat": {"numbness_shutdown": 1}, "disconnected": {"numbness_shutdown": 1},
    "nothing at all": {"numbness_shutdown": 1.5}, "frozen": {"numbness_shutdown": 1},
    "hollow": {"numbness_shutdown": 1, "grief_meaningloss": 0.5},
    "foggy": {"numbness_shutdown": 0.5}, "distant": {"numbness_shutdown": 1},
    # grief / meaning loss
    "yearning": {"grief_meaningloss": 1.5}, "heavy": {"grief_meaningloss": 0.5},
    "guilty": {"grief_meaningloss": 0.5, "shame_selfattack": 0.5},
    "relieved-then-guilty": {"grief_meaningloss": 1}, "disbelief": {"grief_meaningloss": 1},
    "tender": {"grief_meaningloss": 1},
    # relationship threat
    "unwanted": {"relationship_threat": 1}, "jealous": {"relationship_threat": 1},
    "unsure of my place": {"relationship_threat": 1}, "lonely": {"relationship_threat": 1},
    "invisible": {"relationship_threat": 1}, "unimportant": {"relationship_threat": 1},
    "mattering": {"relationship_threat": 1},
    # control / trapped
    "trapped": {"avoidance": 1, "problem_control": -0.5}, "powerless": {"problem_control": -1},
    "cornered": {"avoidance": 1}, "suffocated": {"avoidance": 1},
    "overwhelmed": {"anxiety_catastrophising": 0.5}, "depleted": {"numbness_shutdown": 0.5},
    "exhausted": {"numbness_shutdown": 0.5},
}


def _apply_deltas(state: dict, deltas: dict[str, float]) -> None:
    """Add deltas into the running scores, clamped to 0–10."""
    for k, v in deltas.items():
        if k in state["scores"] and k != "suds":
            state["scores"][k] = round(min(10.0, max(0.0, state["scores"][k] + v)), 1)


# ═══════════════════════════════════════════════════════════════
# INITIAL STATE
# ═══════════════════════════════════════════════════════════════

def _initial_state() -> dict:
    return {
        "next_step": "SAFETY",
        "track": None,
        "situation_key": None,
        "suds_start": None,
        "suds_current": None,
        "grounding_rounds": 0,
        "questions_queue": [],
        "question_index": 0,
        "emotion_words": [],
        "body_location": None,
        "body_quality": None,
        "unmet_need": None,
        "ifthen_text": None,
        "validation_index": 0,
        "scores": {
            "suds": 0,
            "shame_selfattack": 0.0,
            "rumination": 0.0,
            "avoidance": 0.0,
            "anxiety_catastrophising": 0.0,
            "anger_hidden_hurt": 0.0,
            "numbness_shutdown": 0.0,
            "problem_control": 0.0,
            "relationship_threat": 0.0,
            "grief_meaningloss": 0.0,
            "readiness_depth": 0.0,
        },
    }


# ═══════════════════════════════════════════════════════════════
# SCREEN BUILDERS
# ═══════════════════════════════════════════════════════════════

def _screen(step: str, **kw) -> dict:
    return {"step": step, "done": False, **kw}


def _build_safety() -> dict:
    return _screen(
        "SAFETY", type="button_choice",
        heading="One thing first.",
        question="Right now, are you having thoughts of hurting yourself, or feeling that life isn't worth living?",
        subtext="This question is always asked — not because it's expected, just to make sure you're safe.",
        options=[
            {"id": "no",       "label": "No, I'm okay"},
            {"id": "yes",      "label": "Yes, I am"},
            {"id": "not_sure", "label": "Not sure"},
        ],
        validation_copy=None, skippable=False,
    )


def _build_suds_initial() -> dict:
    return _screen(
        "SUDS_INIT", type="slider",
        heading=None,
        question="How intense is the feeling right now — on a scale of 0 to 10?",
        subtext="0 = completely calm · 10 = the most distressed you can imagine. Your gut read is the right answer.",
        slider_min=0, slider_max=10, slider_step=1,
        slider_labels={"0": "Completely calm", "5": "Moderate", "10": "Overwhelming"},
        validation_copy=None, skippable=False,
    )


def _build_grounding(round_num: int) -> dict:
    hint = "Take as long as you need." if round_num == 1 else "One more round — you're doing well."
    return _screen(
        "GROUNDING", type="grounding",
        heading="Let's slow things down a little first.",
        question="4-7-8 breathing",
        subtext=(
            f"Breathe **in** for 4 counts.\nHold for 7 counts.\nBreathe **out** for 8 counts.\n\n"
            f"Round {round_num} of 2. Tap 'Done' when you've finished."
        ),
        options=[{"id": "done", "label": "Done"}],
        validation_copy=hint, skippable=False,
    )


def _build_suds_rerate() -> dict:
    return _screen(
        "SUDS_RERATE", type="slider",
        heading="Check back in.",
        question="Where is the intensity now?",
        subtext="0 = completely calm · 10 = overwhelming.",
        slider_min=0, slider_max=10, slider_step=1,
        slider_labels={"0": "Calm", "5": "Moderate", "10": "Overwhelming"},
        validation_copy=None, skippable=False,
    )


def _build_situation() -> dict:
    options = [{"id": k, "label": v["label"], "icon": v["icon"]} for k, v in SITUATIONS.items()]
    return _screen(
        "SITUATION", type="grid_select",
        heading=None,
        question="Which of these is closest to what you're carrying right now?",
        subtext="Pick the one that fits best — even if it's only partly right.",
        options=options,
        validation_copy=None, skippable=False,
    )


def _build_body_location() -> dict:
    return _screen(
        "BODY_LOC", type="chip_select",
        heading=None,
        question="Where do you feel it most in your body?",
        subtext="Pick as many as fit. Your body often knows before words do.",
        options=[
            {"id": "chest",         "label": "Chest"},
            {"id": "throat",        "label": "Throat"},
            {"id": "stomach",       "label": "Stomach"},
            {"id": "shoulders_jaw", "label": "Shoulders / jaw"},
            {"id": "head",          "label": "Head"},
            {"id": "everywhere",    "label": "Everywhere"},
            {"id": "nowhere_numb",  "label": "Nowhere — numb"},
        ],
        max_select=3,
        validation_copy=None, skippable=True,
    )


def _build_body_quality() -> dict:
    return _screen(
        "BODY_QUAL", type="chip_select",
        heading=None,
        question="What quality does it have?",
        subtext=None,
        options=[
            {"id": "tight",   "label": "Tight / constricted"},
            {"id": "heavy",   "label": "Heavy"},
            {"id": "hot",     "label": "Hot / burning"},
            {"id": "buzzing", "label": "Buzzing / restless"},
            {"id": "hollow",  "label": "Hollow / empty"},
            {"id": "frozen",  "label": "Frozen / numb"},
        ],
        max_select=2,
        validation_copy=None, skippable=True,
    )


def _build_emotions(situation_key: str) -> dict:
    words = SITUATIONS.get(situation_key, {}).get("emotion_words", [])
    return _screen(
        "EMOTIONS", type="chip_select",
        heading=None,
        question="Which of these words fit? Pick up to three.",
        subtext="You don't have to pick any if none fit — just leave them all unselected.",
        options=[{"id": w, "label": w} for w in words],
        max_select=3,
        validation_copy=None, skippable=True,
    )


def _build_question(item: dict, q_num: int, q_total: int, validation: Optional[str]) -> dict:
    base = _screen(
        "QUESTION",
        heading=None,
        question=item["question"],
        subtext=item.get("subtext"),
        validation_copy=validation,
        skippable=item.get("skippable", False),
        question_id=item["id"],
        q_num=q_num,
        q_total=q_total,
        type=item.get("input_type", "text"),
    )
    if item.get("input_type") == "single_select":
        base["options"] = item.get("options", [])
    elif item.get("input_type") == "slider":
        base["slider_min"]    = item.get("slider_min", 0)
        base["slider_max"]    = item.get("slider_max", 100)
        base["slider_step"]   = item.get("slider_step", 10)
        base["slider_labels"] = item.get("slider_labels", {})
    return base


def _build_unmet_need(situation_key: str) -> dict:
    opts = list(SITUATIONS.get(situation_key, {}).get("unmet_need_options", []))
    opts.append({"id": "none", "label": "None of these quite fit"})
    return _screen(
        "UNMET_NEED", type="button_choice",
        heading=None,
        question="Which of these feels most like what's missing right now?",
        subtext="Pick the one that resonates, even if imperfectly.",
        options=opts,
        validation_copy=None, skippable=True,
    )


def _build_self_compassion(situation_key: str) -> dict:
    text = SITUATIONS.get(situation_key, {}).get("self_compassion", "")
    return _screen(
        "COMPASSION", type="display_confirm",
        heading="One small reminder.",
        question=text,
        subtext="Take a breath with it. You don't have to believe it fully — just let it land.",
        options=[
            {"id": "ok",   "label": "Okay"},
            {"id": "skip", "label": "Skip this one"},
        ],
        validation_copy=None, skippable=True,
    )


def _build_ifthen(situation_key: str, current_text: Optional[str]) -> dict:
    template = SITUATIONS.get(situation_key, {}).get("ifthen_template", "If ___, then I will ___.")
    return _screen(
        "IFTHEN", type="text_prefilled",
        heading="One small if-then.",
        question="What's the smallest concrete thing you could do in the next 24 hours?",
        subtext="Edit the suggestion below or write your own — as small and specific as possible.",
        prefill=current_text or template,
        validation_copy=None, skippable=True,
    )


def _build_rerate(suds_start: int) -> dict:
    return _screen(
        "RERATE", type="slider",
        heading="Almost there.",
        question="Where is the intensity now — after all of this?",
        subtext=f"You started at {suds_start}. There's no right answer for where it lands.",
        slider_min=0, slider_max=10, slider_step=1,
        slider_labels={"0": "Calm", "5": "Moderate", "10": "Overwhelming"},
        validation_copy=None, skippable=False,
    )


# ═══════════════════════════════════════════════════════════════
# FRAMEWORK SELECTION — priority stack P0–P10
# ═══════════════════════════════════════════════════════════════

def _select_framework(scores: dict) -> tuple[str, str]:
    """Walk FRAMEWORK_RULES (DB-driven cache) and return the first match."""
    for rule in FRAMEWORK_RULES:
        var = rule["score_var"]
        if var == "__default__":
            return rule["framework_code"], rule["priority_label"]
        val = float(scores.get(var, 0))
        lo  = rule["min_val"]
        hi  = rule["max_val"]
        if val >= lo and (hi is None or val < hi):
            return rule["framework_code"], rule["priority_label"]
    return "F12_ifthen", "DEFAULT"


def _build_hypothesis(situation_key: str, scores: dict, fw_code: str,
                      emotion_words: Optional[list] = None,
                      need_label: str = "") -> str:
    """Compose the pattern hypothesis from the user's OWN selections —
    their emotion words and their chosen unmet need — not just the scores."""
    sit = SITUATIONS.get(situation_key, {})
    sit_label = sit.get("label", "what you described")
    fw_name   = FRAMEWORKS.get(fw_code, {}).get("name", "a supportive approach")

    threads = []
    s = scores
    if s.get("shame_selfattack", 0) >= 4:    threads.append("some self-criticism")
    if s.get("anxiety_catastrophising", 0) >= 4: threads.append("worry about what happens next")
    if s.get("anger_hidden_hurt", 0) >= 4:   threads.append("hurt underneath the surface")
    if s.get("grief_meaningloss", 0) >= 4:   threads.append("a real sense of loss")
    if s.get("numbness_shutdown", 0) >= 4:   threads.append("some emotional flatness")
    if s.get("relationship_threat", 0) >= 4: threads.append("worry about your place in this relationship")
    if s.get("avoidance", 0) >= 4:           threads.append("tension around choices")

    parts: list[str] = []
    if threads:
        parts.append(f"It sounds like {sit_label.lower()} is bringing up {' and '.join(threads[:2])}.")
    else:
        parts.append(f"You've just described {sit_label.lower()} in your own words.")

    # Their words, reflected back — the strongest personalisation signal.
    words = [w for w in (emotion_words or []) if w][:2]
    if words:
        quoted = " and ".join(f"“{w}”" for w in words)
        parts.append(f"You named it yourself: {quoted}.")

    # Their chosen unmet need, folded into the reading.
    if need_label:
        short_need = need_label.split(" — ")[0].split(" – ")[0].strip().lower()
        parts.append(f"And underneath it, what's missing right now is {short_need}.")

    parts.append(
        f"The approach that fits best here is **{fw_name}** — "
        f"it works with exactly this kind of pattern."
    )
    return " ".join(parts)


def _build_closure(suds_start: int, suds_end: int) -> str:
    delta = suds_start - suds_end
    if delta >= 3:
        return f"You arrived at {suds_start} and you're leaving at {suds_end} — you did that with words alone. That counts."
    if delta >= 1:
        return f"You started at {suds_start}, you're at {suds_end} now — even a small shift is real. The technique above is yours to use again."
    if delta == 0:
        return f"The number stayed at {suds_end} — that's okay. Sometimes naming something is the whole point, and the shift comes later."
    return (
        f"You're at {suds_end} now, which is up from {suds_start}. "
        "That can happen — putting words to something sometimes stirs it up before it settles. "
        "The technique above will help. Please come back if you need more support."
    )


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def _question_queue(situation_key: str, track: str) -> list[str]:
    sit = SITUATIONS.get(situation_key)
    if not sit:
        return []
    items = sit["items"]
    if track == "D":
        return [q["id"] for q in items.get("D", [])]
    if track == "S":
        return [q["id"] for q in items.get("S", [])]
    return [q["id"] for q in items.get("S", [])] + [q["id"] for q in items.get("R", [])]


def _item_by_id(situation_key: str, item_id: str) -> Optional[dict]:
    for track_items in (SITUATIONS.get(situation_key) or {}).get("items", {}).values():
        for item in track_items:
            if item["id"] == item_id:
                return item
    return None


def _next_validation(state: dict) -> str:
    idx = state.get("validation_index", 0) % len(VALIDATION_POOL)
    state["validation_index"] = idx + 1
    return VALIDATION_POOL[idx]


# ═══════════════════════════════════════════════════════════════
# TRANSITION ENGINE
# ═══════════════════════════════════════════════════════════════

def _transition(step: str, answer: Any, state: dict) -> tuple[dict, dict]:
    """Apply answer, update state, return (next_screen_payload, updated_state)."""

    if step == "SAFETY":
        if answer in ("yes", "not_sure"):
            state["next_step"] = "CRISIS"
            return {
                "step": "CRISIS", "done": True, "exit_type": "crisis_exit",
                "type": "crisis_exit", "heading": "Your safety comes first.",
                "question": SAFETY_SCRIPT, "options": [],
            }, state
        state["next_step"] = "SUDS_INIT"
        return _build_suds_initial(), state

    if step == "SUDS_INIT":
        suds = int(answer)
        state["scores"]["suds"] = suds
        state["suds_start"] = suds
        state["suds_current"] = suds
        if suds >= 8:
            state["grounding_rounds"] = 0
            state["next_step"] = "GROUNDING"
            return _build_grounding(1), state
        state["track"] = "R" if suds <= 3 else "S"
        state["next_step"] = "SITUATION"
        return _build_situation(), state

    if step == "GROUNDING":
        state["grounding_rounds"] = state.get("grounding_rounds", 0) + 1
        state["next_step"] = "SUDS_RERATE"
        return _build_suds_rerate(), state

    if step == "SUDS_RERATE":
        suds = int(answer)
        state["scores"]["suds"] = suds
        state["suds_current"] = suds
        if suds >= 8:
            if state.get("grounding_rounds", 0) >= 2:
                state["next_step"] = "PAUSE"
                return {
                    "step": "PAUSE", "done": True, "exit_type": "grounding_pause",
                    "type": "grounding_pause", "heading": "Let's pause here.",
                    "question": GROUNDING_PAUSE_SCRIPT, "options": [],
                }, state
            state["next_step"] = "GROUNDING"
            return _build_grounding(state["grounding_rounds"] + 1), state
        state["track"] = "D"
        state["next_step"] = "SITUATION"
        return _build_situation(), state

    if step == "SITUATION":
        sit_key = answer if answer in SITUATIONS else "other"
        state["situation_key"] = sit_key
        _apply_deltas(state, SITUATION_PRIORS.get(sit_key, {}))
        state["next_step"] = "BODY_LOC"
        return _build_body_location(), state

    if step == "BODY_LOC":
        locs = answer if isinstance(answer, list) else ([answer] if answer else [])
        state["body_location"] = locs
        for loc in locs:
            _apply_deltas(state, BODY_LOCATION_DELTAS.get(loc, {}))
        if "nowhere_numb" in locs and int(state.get("suds_current") or 0) >= 6:
            state["track"] = "D"
        state["next_step"] = "BODY_QUAL"
        return _build_body_quality(), state

    if step == "BODY_QUAL":
        quals = answer if isinstance(answer, list) else ([answer] if answer else [])
        state["body_quality"] = quals
        for q in quals:
            _apply_deltas(state, BODY_QUALITY_DELTAS.get(q, {}))
        sit_key = state.get("situation_key") or "other"
        state["next_step"] = "EMOTIONS"
        return _build_emotions(sit_key), state

    if step == "EMOTIONS":
        words = answer if isinstance(answer, list) else ([answer] if answer else [])
        state["emotion_words"] = words
        for w in words:
            _apply_deltas(state, EMOTION_WORD_DELTAS.get(w, {}))
        sit_key = state.get("situation_key") or "other"
        track   = state.get("track") or "S"
        # readiness_depth reflects how deep the session is allowed to go
        state["scores"]["readiness_depth"] = {"D": 2, "S": 5, "R": 8}.get(track, 5)
        queue   = _question_queue(sit_key, track)
        state["questions_queue"] = queue
        state["question_index"]  = 0
        if queue:
            state["next_step"] = "QUESTION"
            item = _item_by_id(sit_key, queue[0])
            return _build_question(item, 1, len(queue), _next_validation(state)), state
        state["next_step"] = "UNMET_NEED"
        return _build_unmet_need(sit_key), state

    if step == "QUESTION":
        sit_key = state.get("situation_key") or "other"
        queue   = state.get("questions_queue", [])
        q_idx   = state.get("question_index", 0)
        if q_idx < len(queue):
            item = _item_by_id(sit_key, queue[q_idx])
            if item and answer != "__skip__":
                _apply_deltas(state, item.get("score_deltas", {}))
                # per-option deltas: the chosen option carries its own signal
                if item.get("input_type") == "single_select":
                    for opt in item.get("options", []):
                        if opt["id"] == answer:
                            _apply_deltas(state, opt.get("score_deltas", {}))
                            break
                # value scoring: the slider's number IS the signal
                elif item.get("value_scoring") == "percent_control":
                    try:
                        pct = float(answer)
                    except (TypeError, ValueError):
                        pct = 50.0
                    # high perceived control → solvable problem → PST territory;
                    # very low control → the pull is toward acceptance work
                    _apply_deltas(state, {"problem_control": pct / 25.0})
                    if pct <= 20:
                        _apply_deltas(state, {"avoidance": 1, "anxiety_catastrophising": 1})
        next_idx = q_idx + 1
        state["question_index"] = next_idx
        if next_idx < len(queue):
            state["next_step"] = "QUESTION"
            next_item = _item_by_id(sit_key, queue[next_idx])
            return _build_question(next_item, next_idx + 1, len(queue), _next_validation(state)), state
        state["next_step"] = "UNMET_NEED"
        return _build_unmet_need(sit_key), state

    if step == "UNMET_NEED":
        state["unmet_need"] = answer
        sit_key = state.get("situation_key") or "other"
        if answer and answer != "none":
            _apply_deltas(state, UNMET_NEED_DELTAS.get(f"{sit_key}:{answer}", {}))
        state["next_step"] = "COMPASSION"
        return _build_self_compassion(sit_key), state

    if step == "COMPASSION":
        sit_key = state.get("situation_key") or "other"
        state["next_step"] = "IFTHEN"
        return _build_ifthen(sit_key, None), state

    if step == "IFTHEN":
        if answer and answer != "__skip__":
            state["ifthen_text"] = str(answer)
        state["next_step"] = "RERATE"
        return _build_rerate(state.get("suds_start") or 5), state

    if step == "RERATE":
        suds_end   = int(answer)
        suds_start = state.get("suds_start") or suds_end
        state["suds_end"]        = suds_end
        state["scores"]["suds"]  = suds_end
        fw_code, priority        = _select_framework(state["scores"])
        fw                       = FRAMEWORKS.get(fw_code, FRAMEWORKS["F12_ifthen"])
        sit_key                  = state.get("situation_key") or "other"
        sit                      = SITUATIONS.get(sit_key, {})
        need_id    = state.get("unmet_need")
        if need_id in (None, "", "none"):
            need_label = ""
        else:
            need_label = next(
                (o["label"] for o in sit.get("unmet_need_options", []) if o["id"] == need_id),
                need_id,
            )
        state["next_step"] = "DONE"
        return {
            "step": "DONE", "done": True, "exit_type": "complete",
            "type": "result",
            "closure_text": _build_closure(suds_start, suds_end),
            "result": {
                "framework_code":    fw_code,
                "framework_name":    fw["name"],
                "evidence":          fw.get("evidence"),
                "tier":              fw.get("tier"),
                "hypothesis":        _build_hypothesis(
                    sit_key, state["scores"], fw_code,
                    emotion_words=state.get("emotion_words"),
                    need_label=need_label,
                ),
                "technique":         fw["technique"],
                "ifthen_action":     state.get("ifthen_text") or sit.get("ifthen_template", ""),
                "selfcompassion_text": sit.get("self_compassion", ""),
                "situation_label":   sit.get("label", ""),
                "situation_icon":    sit.get("icon", ""),
                "emotion_words":     state.get("emotion_words", []),
                "unmet_need":        need_label,
                "suds_start":        suds_start,
                "suds_end":          suds_end,
                "track":             state.get("track"),
                "scores":            state["scores"],
                "priority":          priority,
            },
        }, state

    # Unknown step — restart
    state["next_step"] = "SAFETY"
    return _build_safety(), state


def _rebuild_current(step: str, state: dict) -> dict:
    sit = state.get("situation_key") or "other"
    if step == "SAFETY":     return _build_safety()
    if step == "SUDS_INIT":  return _build_suds_initial()
    if step == "GROUNDING":  return _build_grounding(state.get("grounding_rounds", 0) + 1)
    if step == "SUDS_RERATE":return _build_suds_rerate()
    if step == "SITUATION":  return _build_situation()
    if step == "BODY_LOC":   return _build_body_location()
    if step == "BODY_QUAL":  return _build_body_quality()
    if step == "EMOTIONS":   return _build_emotions(sit)
    if step == "UNMET_NEED": return _build_unmet_need(sit)
    if step == "COMPASSION": return _build_self_compassion(sit)
    if step == "IFTHEN":     return _build_ifthen(sit, state.get("ifthen_text"))
    if step == "RERATE":     return _build_rerate(state.get("suds_start") or 5)
    if step == "QUESTION":
        queue = state.get("questions_queue", [])
        idx   = state.get("question_index", 0)
        if idx < len(queue):
            item = _item_by_id(sit, queue[idx])
            if item:
                return _build_question(item, idx + 1, len(queue), None)
    return _build_safety()


# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE-BASE CACHE (loaded from DB once per process)
# ═══════════════════════════════════════════════════════════════
#
# The module-level dicts above (SITUATIONS, FRAMEWORKS, FRAMEWORK_RULES,
# SITUATION_PRIORS, EMOTION_WORD_DELTAS, BODY_QUALITY_DELTAS) double as the
# seed source AND the runtime cache. On first use we ensure the DB is seeded,
# then reload these globals from the DB so operator edits take effect without
# a code change. seed_aehq.py reads the same globals as its source of truth.

_CACHE_LOADED = False


def _load_globals_from_db(db: DBSession) -> None:
    """Refresh the in-memory knowledge base from the DB tables."""
    global SITUATIONS, SITUATION_PRIORS, FRAMEWORKS, FRAMEWORK_RULES
    global EMOTION_WORD_DELTAS, BODY_QUALITY_DELTAS, BODY_LOCATION_DELTAS, UNMET_NEED_DELTAS

    situations: dict[str, dict] = {}
    priors: dict[str, dict] = {}
    for srow in db.query(AEHQSituation).order_by(AEHQSituation.sort_order).all():
        items: dict[str, list] = {"S": [], "D": [], "R": []}
        for it in srow.items:  # ordered by sort_order via relationship
            d: dict = {
                "id": it.item_key,
                "input_type": it.input_type,
                "skippable": it.skippable,
                "question": it.question,
                "subtext": it.subtext,
                "score_deltas": json.loads(it.score_deltas_json or "{}"),
            }
            if it.options_json:
                d["options"] = json.loads(it.options_json)
            if it.slider_json:
                sj = json.loads(it.slider_json)
                d["slider_min"]    = sj.get("min", 0)
                d["slider_max"]    = sj.get("max", 100)
                d["slider_step"]   = sj.get("step", 10)
                d["slider_labels"] = sj.get("labels", {})
            if it.value_scoring:
                d["value_scoring"] = it.value_scoring
            items.setdefault(it.track, []).append(d)
        situations[srow.key] = {
            "label": srow.label,
            "icon": srow.icon,
            "emotion_words": json.loads(srow.emotion_words_json or "[]"),
            "items": items,
            "unmet_need_options": json.loads(srow.unmet_needs_json or "[]"),
            "self_compassion": srow.self_compassion,
            "ifthen_template": srow.ifthen_template,
        }
        priors[srow.key] = json.loads(srow.priors_json or "{}")

    frameworks = {
        r.code: {"name": r.name, "evidence": r.evidence, "tier": r.tier, "technique": r.technique}
        for r in db.query(AEHQFramework).all()
    }
    rules = [
        {"priority_label": r.priority_label, "score_var": r.score_var,
         "min_val": r.min_val, "max_val": r.max_val, "framework_code": r.framework_code}
        for r in db.query(AEHQFrameworkRule).order_by(AEHQFrameworkRule.sort_order).all()
    ]
    by_kind: dict[str, dict[str, dict]] = {"emotion": {}, "body": {}, "body_loc": {}, "need": {}}
    for row in db.query(AEHQScoreDelta).all():
        by_kind.setdefault(row.kind, {})[row.trigger_key] = json.loads(row.deltas_json or "{}")

    # Only replace globals if the DB actually held content — never blank the
    # engine because of an empty table.
    if situations:           SITUATIONS = situations; SITUATION_PRIORS = priors
    if frameworks:           FRAMEWORKS = frameworks
    if rules:                FRAMEWORK_RULES = rules
    if by_kind["emotion"]:   EMOTION_WORD_DELTAS = by_kind["emotion"]
    if by_kind["body"]:      BODY_QUALITY_DELTAS = by_kind["body"]
    if by_kind["body_loc"]:  BODY_LOCATION_DELTAS = by_kind["body_loc"]
    if by_kind["need"]:      UNMET_NEED_DELTAS = by_kind["need"]


def _ensure_cache(db: DBSession) -> None:
    """Seed the DB from the module defaults if empty, then load the cache once."""
    global _CACHE_LOADED
    if _CACHE_LOADED:
        return
    if db.query(AEHQFramework).count() == 0:
        from seed_aehq import seed_aehq  # lazy import avoids an import cycle
        seed_aehq(db)
    _load_globals_from_db(db)
    _CACHE_LOADED = True


def reload_cache(db: DBSession) -> None:
    """Force a re-read from the DB (call after re-seeding in a live process)."""
    global _CACHE_LOADED
    _CACHE_LOADED = False
    _ensure_cache(db)


# ═══════════════════════════════════════════════════════════════
# PUBLIC API
# ═══════════════════════════════════════════════════════════════

def create_session(user_id: int, db: DBSession) -> dict:
    _ensure_cache(db)
    state = _initial_state()
    sess = AEHQSession(user_id=user_id, next_step="SAFETY", state_json=json.dumps(state), status="active")
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return {"session_id": sess.id, **_build_safety()}


def get_current_screen(session_id: int, user_id: int, db: DBSession) -> dict:
    _ensure_cache(db)
    sess  = _load(session_id, user_id, db)
    state = json.loads(sess.state_json)

    # Finished sessions don't get replayed from the SAFETY screen.
    if sess.status == "complete":
        return get_result(session_id, user_id, db) | {"done": True, "type": "result"}
    if sess.status == "crisis_exit":
        return {"session_id": sess.id, "step": "CRISIS", "done": True, "exit_type": "crisis_exit",
                "type": "crisis_exit", "heading": "Your safety comes first.",
                "question": SAFETY_SCRIPT, "options": []}
    if sess.status == "grounding_pause":
        return {"session_id": sess.id, "step": "PAUSE", "done": True, "exit_type": "grounding_pause",
                "type": "grounding_pause", "heading": "Let's pause here.",
                "question": GROUNDING_PAUSE_SCRIPT, "options": []}

    return {"session_id": sess.id, **_rebuild_current(state.get("next_step", "SAFETY"), state)}


def submit_answer(session_id: int, user_id: int, step: str, answer: Any, db: DBSession) -> dict:
    _ensure_cache(db)
    sess  = _load(session_id, user_id, db)
    state = json.loads(sess.state_json)

    if state.get("next_step") != step:
        raise HTTPException(400, f"Expected step {state.get('next_step')!r}, got {step!r}")

    db.add(AEHQResponse(session_id=sess.id, step=step, answer_json=json.dumps(answer)))

    payload, state = _transition(step, answer, state)
    sess.state_json = json.dumps(state)
    sess.next_step  = state.get("next_step", "SAFETY")

    if payload.get("done"):
        exit_type   = payload.get("exit_type", "complete")
        sess.status = exit_type
        if exit_type == "complete" and payload.get("result"):
            r = payload["result"]
            db.add(AEHQResult(
                session_id=sess.id, user_id=user_id,
                framework_code=r.get("framework_code"),
                framework_name=r.get("framework_name"),
                situation_key=state.get("situation_key"),
                track=state.get("track"),
                hypothesis_text=r.get("hypothesis"),
                technique_text=r.get("technique"),
                evidence_text=r.get("evidence"),
                ifthen_text=r.get("ifthen_action"),
                selfcompassion_text=r.get("selfcompassion_text"),
                closure_text=payload.get("closure_text"),
                suds_start=state.get("suds_start"),
                suds_end=state.get("suds_end"),
                scores_json=json.dumps(state.get("scores", {})),
                exit_type=exit_type,
            ))

    db.commit()
    return {"session_id": sess.id, **payload}


def get_result(session_id: int, user_id: int, db: DBSession) -> dict:
    sess = _load(session_id, user_id, db)
    if not sess.result:
        raise HTTPException(404, "Session not complete")
    r = sess.result
    return {
        "session_id":    sess.id,
        "exit_type":     r.exit_type,
        "framework_code":r.framework_code,
        "framework_name":r.framework_name,
        "situation_key": r.situation_key,
        "track":         r.track,
        "hypothesis":    r.hypothesis_text,
        "technique":     r.technique_text,
        "evidence":      r.evidence_text,
        "ifthen_action": r.ifthen_text,
        "selfcompassion_text": r.selfcompassion_text,
        "closure_text":  r.closure_text,
        "suds_start":    r.suds_start,
        "suds_end":      r.suds_end,
        "scores":        json.loads(r.scores_json) if r.scores_json else {},
        "created_at":    r.created_at.isoformat() if r.created_at else None,
    }


def list_results(user_id: int, db: DBSession) -> list[dict]:
    rows = db.execute(
        select(AEHQResult)
        .where(AEHQResult.user_id == user_id)
        .order_by(AEHQResult.created_at.desc())
        .limit(20)
    ).scalars().all()
    return [
        {
            "session_id":    r.session_id,
            "framework_code":r.framework_code,
            "framework_name":r.framework_name,
            "situation_key": r.situation_key,
            "track":         r.track,
            "suds_start":    r.suds_start,
            "suds_end":      r.suds_end,
            "exit_type":     r.exit_type,
            "created_at":    r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


def _load(session_id: int, user_id: int, db: DBSession) -> AEHQSession:
    sess = db.execute(
        select(AEHQSession).where(AEHQSession.id == session_id, AEHQSession.user_id == user_id)
    ).scalar_one_or_none()
    if not sess:
        raise HTTPException(404, "Session not found")
    return sess
