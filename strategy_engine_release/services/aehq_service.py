"""AEHQ v2.0 — Adaptive Emotional Self-Reflection Questionnaire engine.

Screen flow:
  SAFETY → SUDS_INIT → [GROUNDING → SUDS_RERATE] → SITUATION
  → BODY_LOC → BODY_QUAL → EMOTIONS → QUESTION(s)
  → UNMET_NEED → COMPASSION → IFTHEN → RERATE → DONE
"""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession

from models.orm import (
    AEHQSession, AEHQResponse, AEHQResult,
    AEHQFramework, AEHQSituation, AEHQSituationItem, AEHQFrameworkRule, AEHQScoreDelta,
    AEHQTranslation,
)
from services import aehq_i18n_th as _i18n_th

# Version of the AEHQ content/question bank. Bump on any content change so
# consented training records stay attributable to exactly what was shown —
# AND so _ensure_cache auto-reseeds stale DBs on deploy (self-migrating).
CONTENT_VERSION = "aehq-2.4.0"

# Thai copy — module defaults double as seed source; the DB copy (loaded by
# the cache) wins once seeded, so operators can edit Thai text without a deploy.
TH_STRINGS:    dict[str, str] = dict(_i18n_th.TH_STRINGS)
TH_TECHNIQUES: dict[str, str] = dict(_i18n_th.TH_TECHNIQUES)
TH_NOTES:      dict[str, str] = {
    "SAFETY_SCRIPT":          _i18n_th.SAFETY_SCRIPT_TH,
    "GROUNDING_PAUSE_SCRIPT": _i18n_th.GROUNDING_PAUSE_SCRIPT_TH,
    "REFERRAL_SCRIPT":        _i18n_th.REFERRAL_SCRIPT_TH,
    "TRAUMA_ACK":             _i18n_th.TRAUMA_ACK_TH,
    "LOW_MOOD_NOTE":          _i18n_th.LOW_MOOD_NOTE_TH,
    "CHASING_NOTE":           _i18n_th.CHASING_NOTE_TH,
    "critic_driver":               _i18n_th.CRITIC_DRIVER_TH,
    "critic_social_threat":        _i18n_th.CRITIC_SOCIAL_THREAT_TH,
    "critic_internalized_attacker":_i18n_th.CRITIC_ATTACKER_TH,
    "HATED_SELF_NOTE":             _i18n_th.HATED_SELF_NOTE_TH,
    "OTHERS_FIRST_LEAD":           _i18n_th.OTHERS_FIRST_LEAD_TH,
    "BACKDRAFT_NOTE":              _i18n_th.BACKDRAFT_NOTE_TH,
}


def _th(s: Any) -> Optional[str]:
    return TH_STRINGS.get(s) if isinstance(s, str) else None


def _localize(payload: dict) -> dict:
    """Attach *_th fields for every translatable string in a screen payload.
    English always remains; Thai rides alongside so the client can toggle."""
    for k in ("question", "subtext", "heading", "validation_copy", "prefill", "body", "optin_label"):
        t = _th(payload.get(k))
        if t:
            payload[k + "_th"] = t
    for opt in (payload.get("options") or []):
        t = _th(opt.get("label"))
        if t:
            opt["label_th"] = t
    if payload.get("slider_labels"):
        payload["slider_labels_th"] = {
            k2: (_th(v2) or v2) for k2, v2 in payload["slider_labels"].items()
        }
    return payload


# ═══════════════════════════════════════════════════════════════
# KNOWLEDGE BASE — 10 situations
# ═══════════════════════════════════════════════════════════════

SITUATIONS: dict[str, dict] = {
    "work": {
        "label": "Work or study pressure",
        "icon": "💼",
        "emotion_words": ["overwhelmed", "pressured", "depleted", "burned out", "running on empty",
                          "trapped", "resentful", "dread", "foggy", "inadequate"],
        "items": {
            "S": [
                {
                    # Detachment probe — the single most discriminating work item.
                    # Psychological detachment is the recovery experience most
                    # protective against fatigue (meta-analysis, 54 samples,
                    # N=26,592); its absence (work rumination) is the bridge
                    # from job stress to poor sleep and low mood.
                    "id": "w_s0", "input_type": "single_select", "skippable": False,
                    "question": "When you finish work for the day — does your mind clock out with you?",
                    "subtext": "Evenings and weekends count. Just your honest average.",
                    "options": [
                        {"id": "clocks_out", "label": "Mostly yes — work stays at work",
                         "score_deltas": {"problem_control": 1}},
                        {"id": "follows",    "label": "It follows me home some evenings",
                         "score_deltas": {"rumination": 2}},
                        {"id": "never_off",  "label": "It never really switches off",
                         "score_deltas": {"rumination": 4, "anxiety_catastrophising": 1}},
                    ],
                    "score_deltas": {},
                },
                {
                    "id": "w_s1", "input_type": "text", "skippable": False,
                    "question": "What's actually on the pile right now? Telegraph style — just the things, no full sentences needed.",
                    "subtext": "Listing it usually helps. Rough words are fine.",
                    "score_deltas": {"problem_control": 2},
                },
                {
                    "id": "w_s2", "input_type": "text", "skippable": True,
                    "question": "Under the pressure there's sometimes a quieter sentence. If yours is there, finish it: \"If I don't get this done, it means I am ___\"",
                    "subtext": "Only if something rings true — there's no right answer here.",
                    "score_deltas": {"shame_selfattack": 2, "anxiety_catastrophising": 1},
                    "bottom_line": "I am {}",
                },
                {
                    # Energy-depletion gauge — burnout presents as depletion, not
                    # "overwhelm" (exhaustion-disorder literature). Low tank feeds
                    # numbness_shutdown, the engine's depletion channel.
                    "id": "w_s3", "input_type": "slider", "skippable": False,
                    "question": "By the time you finish a normal workday — how much is left in your tank?",
                    "subtext": "0 means completely empty, 100 means plenty left for your own life.",
                    "slider_min": 0, "slider_max": 100, "slider_step": 10,
                    "slider_labels": {"0": "Completely empty", "50": "About half", "100": "Plenty left"},
                    "score_deltas": {},
                    "value_scoring": "energy_left",
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
                {
                    # Effort–reward imbalance probe (Siegrist): unreciprocated
                    # effort prospectively predicts depressive-disorder onset
                    # (8 cohorts, N=84,963). Imbalance reads as hidden hurt +
                    # unrecognised-effort shame, not as a workload problem.
                    "id": "w_r2", "input_type": "single_select", "skippable": False,
                    "question": "Put what you give on one side of the scale — effort, hours, care. On the other side, what comes back: pay, thanks, recognition. How do the scales sit?",
                    "subtext": "Your gut read is the right answer.",
                    "options": [
                        {"id": "balanced",  "label": "Roughly balanced",
                         "score_deltas": {}},
                        {"id": "tilted",    "label": "More goes out than comes back",
                         "score_deltas": {"anger_hidden_hurt": 2, "shame_selfattack": 1}},
                        {"id": "one_sided", "label": "It's one-sided — and it's been that way a while",
                         "score_deltas": {"anger_hidden_hurt": 3, "shame_selfattack": 1, "numbness_shutdown": 1}},
                    ],
                    "score_deltas": {},
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
                    # Guilt vs. shame — the single highest-leverage routing item.
                    # "I did something bad" (guilt) → problem-solving / behavioural.
                    # "I am bad" (shame) → self-compassion (CFT).
                    "id": "sc_s0", "input_type": "single_select", "skippable": False,
                    "question": "When you think about what happened, which feels closer right now?",
                    "subtext": "There's no right answer — just whichever rings truer this moment.",
                    "options": [
                        # Guilt is behaviour-focused and reparative → problem-solving.
                        {"id": "did_bad", "label": "I did something bad",
                         "score_deltas": {"problem_control": 5}},
                        # Shame is self-focused → self-compassion (CFT).
                        # The shame answers surface a negative core belief (Bottom Line).
                        {"id": "am_bad",  "label": "I am the mistake",
                         "score_deltas": {"shame_selfattack": 6}, "bottom_line": "I am the mistake"},
                        {"id": "both",    "label": "Honestly, both",
                         "score_deltas": {"shame_selfattack": 3, "problem_control": 2}, "bottom_line": "I am the mistake"},
                    ],
                    "score_deltas": {},
                },
                {
                    # Branch C — classify the critic's FUNCTION and route on it.
                    # driver / social-threat / internalized-attacker each fork.
                    "id": "sc_c", "input_type": "single_select", "skippable": False,
                    "question": "When the critic fires — what job does it think it's doing?",
                    "subtext": "Most critics have a job, even when they do it cruelly.",
                    "options": [
                        {"id": "driver", "label": "Pushing me so I don't fail or fall behind",
                         "score_deltas": {"problem_control": 1}, "critic_function": "driver"},
                        {"id": "social_threat", "label": "Warning me before other people judge me",
                         "score_deltas": {"relationship_threat": 2, "shame_selfattack": 1}, "critic_function": "social_threat"},
                        {"id": "attacker", "label": "Not protecting anything — it's just contempt",
                         "score_deltas": {"shame_selfattack": 2}, "critic_function": "internalized_attacker", "hated_self": True},
                    ],
                    "score_deltas": {},
                },
                {
                    "id": "sc_s1", "input_type": "text", "skippable": True,
                    "question": "What are the critic's exact words? Quote it — or paraphrase if that's easier.",
                    "subtext": "Only if you're willing. Naming the voice often weakens it a little.",
                    # Light: this describes the critic, it shouldn't outvote sc_s0.
                    "score_deltas": {"shame_selfattack": 1.5},
                },
                {
                    "id": "sc_s2", "input_type": "text", "skippable": False,
                    "question": "Whose voice does the critic borrow? Does the accent belong to someone from your past?",
                    "subtext": "Just a rough guess. Even 'not sure' is useful.",
                    "score_deltas": {"shame_selfattack": 0.5},
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
                    "capture": "critic_protects",
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
                    "question": "When the fear says \"they're leaving\" — how often has that alarm been right before? What's its track record, gently reviewed?",
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
                    "question": "Whose rule is \"a good person doesn't refuse\"? Did you ever choose it — or did it just arrive with you?",
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
    "trading": {
        # Grounded in: Lo/Repin/Steenbarger 2005 (emotional reactivity ↔ worse
        # performance), Odean 1998 (disposition effect), Palomäki 2013 (tilt:
        # loss → unfairness → chasing), Fenton-O'Creevy (reappraisal works,
        # suppression doesn't; experts close charts + journal).
        "label": "Trading or investment stress",
        "icon": "📉",
        "emotion_words": ["tilted", "wiped out", "regret", "FOMO", "frozen at the screen",
                          "revenge mode", "greedy-then-ashamed", "it's unfair",
                          "can't look away", "sick of the charts"],
        "items": {
            "S": [
                {
                    # The four canonical trader wounds — each routes differently.
                    "id": "tr_s0", "input_type": "single_select", "skippable": False,
                    "question": "Which is closest to what just happened?",
                    "subtext": "Rough category is enough — the details can stay yours.",
                    "options": [
                        {"id": "took_loss",  "label": "A loss — bigger than it should have been, and it stings",
                         "score_deltas": {"shame_selfattack": 1, "anger_hidden_hurt": 1}},
                        {"id": "missed_move","label": "Missed the move — watched it go without me",
                         "score_deltas": {"anxiety_catastrophising": 2, "rumination": 1}},
                        {"id": "cant_pull",  "label": "Frozen — my plan says go and my hand won't",
                         "score_deltas": {"avoidance": 2, "anxiety_catastrophising": 1}},
                        {"id": "gave_back",  "label": "Won big, then gave it all back",
                         "score_deltas": {"shame_selfattack": 2, "anger_hidden_hurt": 1}},
                    ],
                    "score_deltas": {},
                },
                {
                    # Tilt / chasing check — the load-bearing item. "Win it back
                    # now" is within-session chasing (Palomäki; TDS criterion).
                    "id": "tr_s1", "input_type": "single_select", "skippable": False,
                    "question": "Right now — what's the strongest pull?",
                    "subtext": "Honest answer beats the correct-sounding one.",
                    "options": [
                        {"id": "win_back",   "label": "Get it back — today, now",
                         "score_deltas": {"anger_hidden_hurt": 2, "anxiety_catastrophising": 1, "problem_control": -1}},
                        {"id": "replay",     "label": "Replaying every candle on loop",
                         "score_deltas": {"rumination": 3}},
                        {"id": "step_away",  "label": "Never opening that app again",
                         "score_deltas": {"avoidance": 2, "numbness_shutdown": 0.5}},
                        {"id": "numb_scroll","label": "Nothing — just numbly scrolling charts",
                         "score_deltas": {"numbness_shutdown": 2}},
                    ],
                    "score_deltas": {},
                },
                {
                    # P&L–self-worth fusion — the trading version of the shame gate.
                    "id": "tr_s2", "input_type": "text", "skippable": True,
                    "question": "Some losses come with a quiet sentence attached. If yours does, finish it: \"This loss means I am ___\"",
                    "subtext": "Only if something rings true. A number on a screen often smuggles in a verdict about us.",
                    "score_deltas": {"shame_selfattack": 2},
                    "bottom_line": "I am {}",
                },
            ],
            "D": [
                {
                    # Distanced reappraisal — the exact strategy shown to reduce
                    # the disposition effect (suppression doesn't).
                    "id": "tr_d1", "input_type": "text", "skippable": False,
                    "question": "If a trader you respect took this exact trade, with the same information you had at the time — what would you say happened?",
                    "subtext": "Judge the decision with what was knowable then, not with the chart you can see now.",
                    "score_deltas": {},
                },
            ],
            "R": [
                {
                    # Process vs outcome — the core trading-psychology distinction.
                    "id": "tr_r1", "input_type": "single_select", "skippable": False,
                    "question": "Set the result aside for a second. Looking only at the decision — how close did it stay to your own plan?",
                    "subtext": "Good decisions lose sometimes; bad ones win sometimes. That's exactly why the result can't answer this one.",
                    "options": [
                        {"id": "followed", "label": "Close — the plan was fine, the market did market things",
                         "score_deltas": {"problem_control": 2}},
                        {"id": "broke",    "label": "It drifted — I crossed a rule I'd set for myself",
                         "score_deltas": {"shame_selfattack": 1, "rumination": 1, "avoidance": 1}},
                        {"id": "no_rules", "label": "There wasn't really a plan yet",
                         "score_deltas": {"problem_control": 2, "anxiety_catastrophising": 0.5}},
                    ],
                    "score_deltas": {},
                },
                {
                    "id": "tr_r2", "input_type": "text", "skippable": False,
                    "question": "If this has visited before — the loss, the promise, the repeat — what usually sets the loop going?",
                    "subtext": "If it's a first, that counts as an answer too. Patterns only need to be seen once to start loosening.",
                    "score_deltas": {"rumination": 1},
                },
            ],
        },
        "unmet_need_options": [
            {"id": "make_it_back",    "label": "Making the money back — nothing else matters right now"},
            {"id": "competent",       "label": "Feeling like I know what I'm doing again"},
            {"id": "calm_decisions",  "label": "Deciding calmly — not from the edge"},
            {"id": "permission_pause","label": "Permission to step away for a while"},
        ],
        "self_compassion": "A red day is a fact about a trade — not a verdict on you. The account and your worth are two different ledgers.",
        "ifthen_template": "If I take a loss, then I close the platform for 20 minutes before any new order — timer on, screen off.",
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
    # Deliberately faint: the guilt-vs-shame item (sc_s0) decides this route.
    # A heavy prior here would drown the distinction and send guilt to CFT too.
    "self_criticism": {"shame_selfattack": 1},
    "anxiety":        {"anxiety_catastrophising": 4},
    "grief":          {"grief_meaningloss": 4},
    "anger":          {"anger_hidden_hurt": 4},
    "numbness":       {"numbness_shutdown": 4},
    "relationship":   {"relationship_threat": 4},
    "trapped":        {"avoidance": 3, "problem_control": 1},
    # Faint on purpose — tr_s0/tr_s1 differentiate the four trader wounds;
    # a heavy prior would flatten them into one route.
    "trading":        {"anxiety_catastrophising": 1.5, "rumination": 1.5},
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
    # trading
    "trading:make_it_back":         {"anger_hidden_hurt": 1, "anxiety_catastrophising": 1},  # + chasing hit (handled in transition)
    "trading:competent":            {"shame_selfattack": 1.5},
    "trading:calm_decisions":       {"anxiety_catastrophising": 1.5},
    "trading:permission_pause":     {"avoidance": 1, "numbness_shutdown": 1},
    # other
    "other:understood":             {"relationship_threat": 1},
    "other:rest":                   {"numbness_shutdown": 1},
    "other:clarity":                {"rumination": 1.5},
    "other:company":                {"relationship_threat": 1},
}


# Per-situation follow-up (Part 3). Intervals are construct-appropriate — action
# checks in days, symptom/affect tracks in weeks, grief in months — but framed
# warmly (no instrument jargon). Every session is self-contained; the check-in is
# strictly opt-in, because most users won't return (median 15-day retention ~3.9%,
# Baumel et al. 2019). action_check_hours reflects implementation-intention
# research (24–72h; Sheeran & Gollwitzer 2024).
FOLLOWUP_CONFIG: dict[str, dict] = {
    "work":           {"interval_days": 7,  "action_check_hours": 48,
                       "checkin": "How are your evenings this week — any easier to switch off?"},
    "dismissed":      {"interval_days": 10, "action_check_hours": 48,
                       "checkin": "Since we talked, did you get to say the thing you wanted seen?"},
    "authority":      {"interval_days": 10, "action_check_hours": 48,
                       "checkin": "Did you find a way to name what felt unfair — even to yourself?"},
    "self_criticism": {"interval_days": 17, "action_check_hours": 48,
                       "checkin": "How has the critic's volume been this week?"},
    "anxiety":        {"interval_days": 14, "action_check_hours": 48,
                       "checkin": "Is the worry still taking the same amount of room?"},
    "grief":          {"interval_days": 90, "action_check_hours": 72,
                       "checkin": "How has it been to carry this lately — any okay days?"},
    "anger":          {"interval_days": 14, "action_check_hours": 48,
                       "checkin": "When the anger showed up again, could you find the hurt under it?"},
    "numbness":       {"interval_days": 10, "action_check_hours": 48,
                       "checkin": "Have you noticed even one small thing you could feel this week?"},
    "relationship":   {"interval_days": 14, "action_check_hours": 48,
                       "checkin": "When the fear said 'they're leaving' this week — was it right?"},
    "trapped":        {"interval_days": 10, "action_check_hours": 48,
                       "checkin": "Did a two-step 'let me get back to you' get any easier?"},
    "trading":        {"interval_days": 7,  "action_check_hours": 48,
                       "checkin": "Did the 20-minute pause rule survive contact with the market this week?"},
    "other":          {"interval_days": 14, "action_check_hours": 48,
                       "checkin": "How has this been sitting with you since we talked?"},
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
            "**A quick map — your three systems:** emotion runs on three systems — a "
            "**threat** system (alarms, self-criticism), a **drive** system (chasing, "
            "achieving), and a **soothing** system (safeness, warmth). Self-attack means "
            "the threat system is loud and the soothing one is offline. This practice "
            "switches soothing back on — it's a skill, not a mood.\n\n"
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
        "evidence": "Ekers et al. (2014) meta-analysis; NICE NG222 first-line; Noetel et al. (2024) BMJ exercise NMA",
        "tier": "A",
        "technique": (
            "**Action first, mood second.** When mood is low, waiting to feel like it "
            "is the trap — doing comes before feeling.\n\n"
            "**1. One 5-minute thing** that used to give even 1% of something. "
            "It doesn't have to feel good — schedule it, do it, then notice: "
            "did anything shift, even slightly, after vs before?\n\n"
            "**2. Add movement — any kind counts.** The strongest evidence is for "
            "brisk walking or jogging, strength training, yoga, or dance — even "
            "20 minutes, and a bit of intensity helps more. Pick the one that feels "
            "least impossible this week.\n\n"
            "**3. Repeat tomorrow.** Same small thing or a new one. "
            "The goal is re-engagement, not enjoyment yet — enjoyment comes back later."
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

# ── Trauma-pattern recognition (Tier C — suggestive, NEVER diagnostic) ────────
# Detected from the user's OWN free text. The flag only ADDS caution: it caps
# depth (grounding-first), offers a warm referral, and locks deep-processing
# frameworks. It never unlocks a deeper track and never asks the user to
# recount anything. (Pennebaker/LIWC markers; SAMHSA 2014 four Rs / six
# principles; PC-PTSD-5 & ITQ inform the domains, not a probing screen.)
TRAUMA_MARKERS: dict[str, list[str]] = {
    "dissociation": [
        "not real", "wasn't real", "watching myself", "outside my body",
        "out of my body", "far away", "floating", "detached", "like a dream",
        "unreal", "disconnected", "numb all over", "not really here", "on autopilot",
    ],
    "hyperarousal": [
        "on edge", "can't switch off", "cant switch off", "can't relax", "cant relax",
        "jumpy", "startle", "on guard", "always alert", "heart pounding",
        "constantly scanning", "bracing", "waiting for it to happen again",
    ],
    "intrusion": [
        "keeps replaying", "can't stop seeing", "cant stop seeing", "flashback",
        "keeps coming back", "over and over", "haunts me", "nightmares",
        "keeps happening in my head", "can't get it out of my head",
    ],
    "avoidance": [
        "can't talk about", "cant talk about", "won't go there", "wont go there",
        "block it out", "push it down", "can't go back", "cant go back",
        "don't want to remember", "shut it away",
    ],
    "foreshortened_future": [
        "no point planning", "no future", "don't see a future", "dont see a future",
        "no point in trying", "nothing ahead",
    ],
}

# Categories that on their own are strong enough to raise caution.
_STRONG_TRAUMA_CATEGORIES = {"dissociation", "intrusion", "foreshortened_future"}

# Warm, choice-preserving referral (SAMHSA: empowerment, voice & choice).
REFERRAL_SCRIPT = (
    "Some of what you've described sounds genuinely heavy — heavier than a "
    "self-reflection tool is built to hold.\n\n"
    "This isn't a substitute for talking with a person trained for this, and "
    "reaching out is a strength, not a failure. If it would help, here are some options:\n"
    "• **Crisis text:** Text HOME to 741741\n"
    "• **Lifeline:** 988 (call or text, US)\n"
    "• **Thailand:** 1323 (กรมสุขภาพจิต)\n"
    "• **International:** findahelpline.com\n\n"
    "You're in control of what happens next — there's nothing you have to explain here."
)

# Trauma-safe acknowledgment: names the weight, then steadies. Never probes.
TRAUMA_ACK = (
    "Some of what you're describing sounds really heavy. Rather than going "
    "deeper, let's slow down and focus on steadying things right now — that's "
    "the kinder move when a feeling is this big."
)


# ── Low-mood pattern check (2Q-derived soft gate — detect, never diagnose) ────
# Grounded in the Thai DMH 2Q screener (หดหู่/เศร้า/ท้อแท้ + เบื่อ ทำอะไรก็ไม่
# เพลิดเพลิน, 2-week window) and PHQ-2. AEHQ detects the PATTERN only: both
# items endorsed "most days" → route to Behavioural Activation (NICE NG222
# first-line for less severe depression) + a warm, normalising note. The word
# "depression" is never used as a verdict. A "no" is not safety; a "yes" is
# not illness — the flag only adds support, never a label.
MOOD_CHECK_QUESTIONS: dict[str, dict] = {
    "MOOD1": {
        "question": "One gentle check before we wrap the questions — over the last two weeks, counting today, have there been days your mood sat low: heavy, sad, or drained of hope?",
        "subtext": "Not about today only — the general weather of the last two weeks.",
        "options": [
            {"id": "not_really", "label": "Not really", "weight": 0},
            {"id": "some_days",  "label": "Some days, yes", "weight": 0.5},
            {"id": "most_days",  "label": "Most days, honestly", "weight": 1},
        ],
    },
    "MOOD2": {
        "question": "And in those same two weeks — the things you usually enjoy: have they gone quiet? Less pull, less fun, less taste?",
        "subtext": "Food, music, people, hobbies — anything that normally gives you something back.",
        "options": [
            {"id": "not_really", "label": "Not really — they still land", "weight": 0},
            {"id": "some_days",  "label": "Somewhat — dimmer than usual", "weight": 0.5},
            {"id": "most_days",  "label": "Yes — almost nothing lands lately", "weight": 1},
        ],
    },
}

# Situations where the mood check is offered. Grief is deliberately excluded —
# low mood inside grief is normal grief, and screening it risks medicalising
# a healthy process (per the contested PGD timing thresholds). Trading is
# included: excessive trading co-occurs with depression and anxiety.
MOOD_CHECK_SITUATIONS = {"work", "numbness", "other", "trapped", "trading"}

# ── Chasing / gambling-harm pattern (TDS-grounded — detect, never probe) ─────
# Markers mirror the validated Trading Disorder Scale criteria (13 items,
# cutoff ≥5; concealment, borrowing, escalation, preoccupation, chasing) and
# the tilt→chasing sequence (Palomäki 2013). Scanned ONLY inside the trading
# situation, from the user's own free text. Graded: one strong category flags;
# otherwise hits accumulate (weak text categories + structural answers) and
# flag at 3. The flag only adds caution: urge-focused routing + a warm note.
CHASING_MARKERS: dict[str, list[str]] = {
    "concealment": [  # strong — TDS deception criterion
        "hiding it from", "haven't told", "havent told", "lied about", "lying about",
        "secret account", "she doesn't know", "he doesn't know", "no one knows",
        "don't know how much i've lost", "dont know how much",
    ],
    "borrowing": [    # strong — TDS financial-dependence criterion
        "borrowed", "loan to trade", "credit card", "in debt", "owe",
        "margin call", "rent money", "savings are gone", "borrowed money",
        "emergency fund",
    ],
    "escalation": [   # weak alone — tolerance / chasing
        "double down", "doubled my position", "all in", "one more trade",
        "win it back", "make it back", "chasing", "bigger size", "revenge trade",
    ],
    "preoccupation": [  # weak alone — salience
        "can't sleep", "cant sleep", "first thing i check", "checking all night",
        "dreaming about charts", "can't stop checking", "cant stop checking",
    ],
}
_STRONG_CHASING_CATEGORIES = {"concealment", "borrowing"}

CHASING_NOTE = (
    "One pattern in what you shared is worth naming gently: the pull to win it "
    "back. Research on traders and players calls this **chasing** — and it's the "
    "single pattern most strongly linked to losses getting away from people. "
    "It's not a character flaw; it's how loss wires urgency into anyone.\n\n"
    "**The urge itself passes.** Urges crest and fall like waves — usually within "
    "20 minutes. Timer on, platform closed, and watch the urge without obeying "
    "it. Surfing one urge, once, weakens the next one.\n\n"
    "If money stress from trading is touching rent, debt, or things you're "
    "keeping private — that's a weight worth sharing with someone who knows "
    "this territory:\n"
    "• **Thailand:** สายด่วนสุขภาพจิต 1323 (free, 24 hrs)\n"
    "• **International:** findahelpline.com — gambling-support lines listed by country\n\n"
    "No verdicts here. Just a pattern worth catching early."
)

# ── Inner critic (S5) — Branch C reframes + hated-self escalation ────────────
# The critic's protective-intention card. Names the job, keeps the standard,
# drops the cruelty. The internalized-attacker (hated-self) branch routes to a
# warm referral — the unguided-tool equivalent of a supervision flag.
CRITIC_FUNCTION_REFRAMES: dict[str, str] = {
    "driver": (
        "Your critic is a **driver** — it pushes so you won't fail. The fear-fuel "
        "does work, but it burns the engine out. You're allowed to keep the standard "
        "and drop the whip: the same push can come from wanting good things for yourself, "
        "not from dread."
    ),
    "social_threat": (
        "Your critic is a **lookout** — it scans for other people's judgment and tries "
        "to catch it first, so the rejection won't blindside you. It's guarding a real "
        "fear. The hidden cost: to stay ahead of their verdict, you deliver it to "
        "yourself first, every day."
    ),
    "internalized_attacker": (
        "This one isn't protecting anything — it's **contempt you learned**, often in a "
        "voice borrowed from someone else. That's the hardest kind to face alone, and "
        "you don't have to. Talking it through with someone trained genuinely helps here."
    ),
}

HATED_SELF_NOTE = (
    "The way you're talking to yourself right now is closer to an attack than a "
    "correction — and that's worth taking seriously, gently. You wouldn't be handed "
    "this voice if something hadn't taught it to you. A trained person can help you "
    "set it down; you don't have to carry it alone.\n"
    "• **Thailand:** สายด่วนสุขภาพจิต 1323 (free, 24 hrs)\n"
    "• **International:** findahelpline.com"
)

# ── Self-compassion (S6-S7) — fear-of-compassion, Branch D, backdraft ────────
# High fear-of-compassion → deliver kindness OTHERS-FIRST (imagine a loved one,
# then turn it inward). Backdraft = the grief/pain surge that can rise when
# warmth turns inward; named as normal, with a visible pause pathway.
OTHERS_FIRST_LEAD = (
    "Kindness aimed straight at yourself can feel fake or undeserved — that's "
    "common, not a flaw. So let's start sideways: picture someone you love feeling "
    "exactly what you're feeling. What would you want them to hear? Now, just for a "
    "moment, let that same sentence turn toward you:"
)
BACKDRAFT_NOTE = (
    "A heads-up: turning warmth inward can make a wave rise — grief, or a sharp "
    "\"I don't deserve this.\" That's called **backdraft** — old pain thawing, not "
    "failure. If it's a lot right now, tap pause and we'll steady instead."
)

# Warm, normalising note attached to the result when the pattern is present.
LOW_MOOD_NOTE = (
    "One thing worth saying plainly, and kindly: you told us your mood has been "
    "low most days for a couple of weeks, and that things you enjoy have gone "
    "quiet. That combination is worth taking seriously — not as a verdict, but "
    "as a signal.\n\n"
    "When it sticks around past two weeks, talking to someone trained really "
    "does help — earlier is easier.\n"
    "• **Thailand:** สายด่วนสุขภาพจิต 1323 (กรมสุขภาพจิต, free, 24 hrs)\n"
    "• **International:** findahelpline.com\n\n"
    "Meanwhile, the technique below is chosen for exactly this pattern — small "
    "scheduled actions first, mood follows after. Movement helps too: even a "
    "daily 20-minute walk measurably lifts mood over a few weeks."
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
    # burnout-core words — exhaustion is the depression-adjacent core of
    # burnout (Bianchi 14-sample meta-analytic/bifactor work)
    "burned out": {"numbness_shutdown": 1.5},
    "running on empty": {"numbness_shutdown": 1.5},
    # trading — tilt vocabulary (Palomäki: loss → unfairness → chasing)
    "tilted": {"anger_hidden_hurt": 1.5},
    "wiped out": {"numbness_shutdown": 1, "grief_meaningloss": 0.5},
    "regret": {"rumination": 1, "shame_selfattack": 0.5},
    "FOMO": {"anxiety_catastrophising": 1},
    "frozen at the screen": {"numbness_shutdown": 1, "avoidance": 0.5},
    "revenge mode": {"anger_hidden_hurt": 1.5},
    "greedy-then-ashamed": {"shame_selfattack": 1.5},
    "it's unfair": {"anger_hidden_hurt": 1},
    "can't look away": {"rumination": 1, "anxiety_catastrophising": 0.5},
    "sick of the charts": {"numbness_shutdown": 1},
}


def _apply_deltas(state: dict, deltas: dict[str, float]) -> None:
    """Add deltas into the running scores, clamped to 0–10."""
    for k, v in deltas.items():
        if k in state["scores"] and k != "suds":
            state["scores"][k] = round(min(10.0, max(0.0, state["scores"][k] + v)), 1)


def _scan_trauma(state: dict, text: Any) -> None:
    """Scan the user's own free text for trauma-pattern markers and, if found,
    raise the trauma flag. Suggestive only — this never probes, never diagnoses,
    and only ever ADDS caution downstream."""
    if not text or not isinstance(text, str):
        return
    low = text.lower()
    hits = state.setdefault("trauma_markers", [])
    categories = set(state.setdefault("trauma_categories", []))
    for category, phrases in TRAUMA_MARKERS.items():
        for phrase in phrases:
            if phrase in low:
                if phrase not in hits:
                    hits.append(phrase)
                categories.add(category)
                break
    state["trauma_categories"] = sorted(categories)
    # Flag when a strong category appears, or when any two categories co-occur.
    strong = bool(categories & _STRONG_TRAUMA_CATEGORIES)
    if strong or len(categories) >= 2:
        state["trauma_flag"] = True


def _scan_chasing(state: dict, text: Any) -> None:
    """Scan trading free text for gambling-harm markers (TDS-grounded).
    Strong category (concealment/borrowing) flags immediately; weak text
    categories add hits that combine with structural answers (win_back,
    make_it_back). Total hits >= 3 flags. Caution-only, never a verdict."""
    if not text or not isinstance(text, str):
        return
    low = text.lower()
    cats = set(state.setdefault("chasing_categories", []))
    for category, phrases in CHASING_MARKERS.items():
        for phrase in phrases:
            if phrase in low and category not in cats:
                cats.add(category)
                state["chasing_hits"] = state.get("chasing_hits", 0) + 1
                break
    state["chasing_categories"] = sorted(cats)
    if cats & _STRONG_CHASING_CATEGORIES or state.get("chasing_hits", 0) >= 3:
        state["chasing_flag"] = True


def _chasing_structural_hit(state: dict) -> None:
    """A chasing-pattern answer (not text): win_back pull, make_it_back need."""
    state["chasing_hits"] = state.get("chasing_hits", 0) + 1
    if state["chasing_hits"] >= 3:
        state["chasing_flag"] = True


# ═══════════════════════════════════════════════════════════════
# INITIAL STATE
# ═══════════════════════════════════════════════════════════════

def _detect_lang(text: str) -> str:
    """Cheap language tag for stored free text: th / en / mixed / unknown."""
    if not text or not isinstance(text, str):
        return "unknown"
    has_thai = any("฀" <= ch <= "๿" for ch in text)
    has_latin = any("a" <= ch.lower() <= "z" for ch in text)
    if has_thai and has_latin:
        return "mixed"
    if has_thai:
        return "th"
    if has_latin:
        return "en"
    return "unknown"


def _initial_state() -> dict:
    return {
        "next_step": "CONSENT",
        "consent_agreed": False,
        "training_opt_in": False,
        "goal_text": None,
        "goal_lang": None,
        "bottom_line_text": None,
        "bottom_line_belief": None,
        "bottom_line_lang": None,
        "bottom_line_rated": False,
        "thought_text": None,
        "thought_lang": None,
        "critic_function": None,
        "critic_protects_text": None,
        "hated_self_flag": False,
        "foc_level": None,
        "compassion_mode": None,
        "soothe_rating": None,
        "goal_attainment": None,
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
        "trauma_flag": False,
        "trauma_markers": [],
        "trauma_categories": [],
        "low_mood_flag": False,
        "mood_answers": {},
        "chasing_flag": False,
        "chasing_hits": 0,
        "chasing_categories": [],
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
    return _localize({"step": step, "done": False, **kw})


def _build_consent() -> dict:
    # Informed consent gate (PDPA). A required agreement to proceed + a SEPARATE
    # optional opt-in for anonymized service/model improvement. The primary
    # button IS the agreement; the checkbox carries the training opt-in only.
    return _screen(
        "CONSENT", type="consent",
        heading="Before we begin",
        question="A quick, honest heads-up",
        body=(
            "This is a **self-reflection tool — not therapy, and not a diagnosis.**\n\n"
            "• **Your privacy:** your answers are stored privately in your account so you can look back on them.\n"
            "• **Safety:** if you mention thoughts of self-harm, we'll pause and show support options — nothing is reported anywhere.\n"
            "• **Not a substitute:** in a crisis, please contact a professional or a helpline (Thailand 1323).\n\n"
            "Tapping **“I understand — begin”** means you agree to the above."
        ),
        # the one separate, optional, default-off opt-in
        optin_label="You may use my anonymized answers to improve this tool (optional).",
        options=[{"id": "agree", "label": "I understand — begin"}],
        validation_copy=None, skippable=False,
    )


def _build_goal() -> dict:
    return _screen(
        "GOAL", type="text",
        heading=None,
        question="Before we dig in — in one sentence, what made you open this today?",
        subtext="Your own words, any language. You can skip this if nothing comes.",
        validation_copy=None, skippable=True,
        question_id="GOAL",
    )


def _build_belief(belief_text: str) -> dict:
    # Belief-strength rating on the Bottom Line — a cheap, sensitive progress
    # metric (S2). The belief text is the user's own words, shown verbatim.
    scr = _screen(
        "BELIEF", type="slider",
        heading="One quick reading.",
        question=f"“{belief_text}” — right now, how much do you believe that?",
        subtext="0% = not at all · 100% = completely. Just today's number — it's a snapshot, not a fact.",
        slider_min=0, slider_max=100, slider_step=10,
        slider_labels={"0": "Don't believe it", "50": "Half and half", "100": "Completely true"},
        validation_copy=None, skippable=False,
    )
    scr["belief_text"] = belief_text
    scr["question_th"] = f"“{belief_text}” — ตอนนี้คุณเชื่อประโยคนี้แค่ไหน?"
    scr["subtext_th"]  = "0% = ไม่เชื่อเลย · 100% = เชื่อสุด ๆ เอาแค่ตัวเลขของวันนี้ — มันคือภาพช็อตหนึ่ง ไม่ใช่ความจริง"
    return scr


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
    scr = _screen(
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
    scr["subtext_th"] = (
        f"หายใจ**เข้า**นับ 4\nกลั้นไว้นับ 7\nหายใจ**ออก**นับ 8\n\n"
        f"รอบที่ {round_num} จาก 2 — เสร็จแล้วแตะ 'เสร็จแล้ว'"
    )
    return scr


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
    # body_map: rendered as a tappable body silhouette (S3-S4 interoception).
    # zone=None options render as buttons below the figure. Same IDs as before,
    # so BODY_LOCATION_DELTAS scoring is unchanged.
    return _screen(
        "BODY_LOC", type="body_map",
        heading=None,
        question="Where do you feel it most in your body?",
        subtext="Tap where it sits. Your body often knows before words do.",
        options=[
            {"id": "head",          "label": "Head",           "zone": "head"},
            {"id": "throat",        "label": "Throat",         "zone": "throat"},
            {"id": "shoulders_jaw", "label": "Shoulders / jaw","zone": "shoulders"},
            {"id": "chest",         "label": "Chest",          "zone": "chest"},
            {"id": "stomach",       "label": "Stomach",        "zone": "stomach"},
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
    # Build the raw payload first, attach options/slider, THEN localize — so
    # option labels and slider labels get their *_th counterparts too.
    base = {
        "step": "QUESTION", "done": False,
        "heading": None,
        "question": item["question"],
        "subtext": item.get("subtext"),
        "validation_copy": validation,
        "skippable": item.get("skippable", False),
        "question_id": item["id"],
        "q_num": q_num,
        "q_total": q_total,
        "type": item.get("input_type", "text"),
    }
    if item.get("input_type") == "single_select":
        # copy options so we never mutate the cached situation dict
        base["options"] = [dict(o) for o in item.get("options", [])]
    elif item.get("input_type") == "slider":
        base["slider_min"]    = item.get("slider_min", 0)
        base["slider_max"]    = item.get("slider_max", 100)
        base["slider_step"]   = item.get("slider_step", 10)
        base["slider_labels"] = item.get("slider_labels", {})
    return _localize(base)


def _build_mood_check(step: str) -> dict:
    q = MOOD_CHECK_QUESTIONS[step]
    return _screen(
        step, type="button_choice",
        heading="Checking the weather, not judging it.",
        question=q["question"],
        subtext=q["subtext"],
        options=[{"id": o["id"], "label": o["label"]} for o in q["options"]],
        validation_copy=None, skippable=False,
    )


def _mood_check_eligible(state: dict) -> bool:
    """Offer the 2-item mood check when depletion signals warrant it.
    Grief is excluded — see MOOD_CHECK_SITUATIONS."""
    sit = state.get("situation_key") or "other"
    if sit == "grief":
        return False
    if sit in MOOD_CHECK_SITUATIONS:
        return True
    return float(state["scores"].get("numbness_shutdown", 0)) >= 4


def _mood_weight(step: str, answer: Any) -> float:
    for o in MOOD_CHECK_QUESTIONS[step]["options"]:
        if o["id"] == answer:
            return o["weight"]
    return 0.0


def _compassion_relevant(state: dict) -> bool:
    """Gauge fear-of-compassion only when self-kindness is the focus — high
    shame or the self-criticism situation. Keeps low-shame sessions fast."""
    if state.get("situation_key") == "self_criticism":
        return True
    return float(state["scores"].get("shame_selfattack", 0)) >= 4


def _next_after_belief(state: dict) -> dict:
    """Route from the end of the belief step onward: mood check → unmet need."""
    sit_key = state.get("situation_key") or "other"
    if _mood_check_eligible(state):
        state["next_step"] = "MOOD1"
        return _build_mood_check("MOOD1")
    state["next_step"] = "UNMET_NEED"
    return _build_unmet_need(sit_key)


def _next_after_questions(state: dict) -> dict:
    """After the situation questions: rate the Bottom Line (if one surfaced),
    then continue to the mood check / unmet need."""
    if state.get("bottom_line_text") and not state.get("bottom_line_rated"):
        state["next_step"] = "BELIEF"
        return _build_belief(state["bottom_line_text"])
    return _next_after_belief(state)


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


def _build_foc() -> dict:
    # Fear-of-Compassion probe (Gilbert) — runs before the compassion practice
    # when self-kindness is the focus. Routes Branch D (others-first sequencing).
    return _screen(
        "FOC", type="button_choice",
        heading="One gentle gauge first.",
        question="When you try to turn kindness toward yourself — what usually happens?",
        subtext="However it lands is useful. There's no wrong answer.",
        options=[
            {"id": "natural",    "label": "It feels okay — natural enough"},
            {"id": "awkward",    "label": "A bit awkward or uncomfortable"},
            {"id": "undeserved", "label": "Like I don't deserve it, or it feels fake"},
        ],
        validation_copy=None, skippable=False,
    )


def _build_self_compassion(situation_key: str, mode: str = "direct", with_pause: bool = False) -> dict:
    text = SITUATIONS.get(situation_key, {}).get("self_compassion", "")
    question = f"{OTHERS_FIRST_LEAD}\n\n{text}" if mode == "others_first" else text
    opts = [
        {"id": "ok",   "label": "Okay"},
        {"id": "skip", "label": "Skip this one"},
    ]
    scr = _screen(
        "COMPASSION", type="display_confirm",
        heading="One small reminder.",
        question=question,
        subtext="Take a breath with it. You don't have to believe it fully — just let it land.",
        options=opts,
        validation_copy=None, skippable=True,
    )
    if with_pause:
        # backdraft-aware: offer a visible pause pathway to grounding.
        scr["options"] = opts + [{"id": "pause", "label": "This is bringing up a lot — pause"}]
        scr["backdraft_note"] = BACKDRAFT_NOTE
        scr["backdraft_note_th"] = TH_NOTES.get("BACKDRAFT_NOTE")
        if mode == "others_first":
            # the lead-in is generic; give it its own TH so the whole screen localizes
            th_lead = TH_NOTES.get("OTHERS_FIRST_LEAD", "")
            th_text = _th(text) or text
            scr["question_th"] = f"{th_lead}\n\n{th_text}" if th_lead else scr.get("question_th")
    return scr


def _build_soothe() -> dict:
    # Post-practice 2-tap feedback (soothing 0–10) — feeds Branch D pacing +
    # creates outcome-labelled data.
    scr = _screen(
        "SOOTHE", type="slider",
        heading="Quick check.",
        question="Did that soothe things even a little?",
        subtext="0 = not at all · 10 = a real settling. Whatever's true is fine.",
        slider_min=0, slider_max=10, slider_step=1,
        slider_labels={"0": "Not at all", "5": "A little", "10": "A real settling"},
        validation_copy=None, skippable=False,
    )
    return scr


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


def _build_goal_attain(goal_text: str) -> dict:
    # Goal-attainment scaling (S12 closure) against the S1 own-words goal.
    scr = _screen(
        "GOAL_ATTAIN", type="slider",
        heading="Back to why you came.",
        question=f"You opened this hoping: “{goal_text}”. Any closer, right now?",
        subtext="0 = no change · 10 = right there. Small movement counts.",
        slider_min=0, slider_max=10, slider_step=1,
        slider_labels={"0": "No change", "5": "A little closer", "10": "Right there"},
        validation_copy=None, skippable=False,
    )
    scr["question_th"] = f"คุณเปิดแอปนี้ด้วยความหวังว่า “{goal_text}” — ตอนนี้ใกล้ขึ้นบ้างไหม?"
    scr["subtext_th"]  = "0 = ไม่เปลี่ยน · 10 = ถึงแล้ว การขยับเล็กน้อยก็นับ"
    return scr


def _build_rerate(suds_start: int) -> dict:
    scr = _screen(
        "RERATE", type="slider",
        heading="Almost there.",
        question="Where is the intensity now — after all of this?",
        subtext=f"You started at {suds_start}. There's no right answer for where it lands.",
        slider_min=0, slider_max=10, slider_step=1,
        slider_labels={"0": "Calm", "5": "Moderate", "10": "Overwhelming"},
        validation_copy=None, skippable=False,
    )
    scr["subtext_th"] = f"คุณเริ่มมาที่ {suds_start} — จะลงตรงไหนก็ไม่มีคำตอบที่ผิด"
    return scr


# ═══════════════════════════════════════════════════════════════
# FRAMEWORK SELECTION — priority stack P0–P10
# ═══════════════════════════════════════════════════════════════

# Frameworks that involve deeper emotional processing — LOCKED when the
# trauma flag is on (Tier-C rule: the flag may only add caution, never depth).
_DEEP_FRAMEWORKS = {"F6_EFT", "F3_CFT", "F15_attachment", "F14_grief"}
# The grounding / self-distancing subset the trauma flag routes into instead.
_GROUNDING_FRAMEWORKS = {"F8_somatic", "F5_DBT", "F9_MBCT"}


def _select_framework(scores: dict, trauma_flag: bool = False,
                      low_mood_flag: bool = False,
                      chasing_flag: bool = False) -> tuple[str, str]:
    """Walk FRAMEWORK_RULES (DB-driven cache) and return the first match.

    Two flags sit above the score-driven stack (below crisis, in this order):
    - trauma_flag: restricts selection to the grounding / self-distancing
      subset (+ warm referral, added by the caller). Caps depth, never adds it.
    - low_mood_flag: the 2Q pattern (low mood + anhedonia, most days, 2 weeks)
      routes to Behavioural Activation — NICE NG222 first-line for less severe
      depression, SMD ≈ -0.74 vs control — plus a normalising note.
    """
    if trauma_flag:
        # Dissociation/numbness → somatic grounding; high arousal → DBT skills;
        # otherwise mindful self-distancing. All shallow, all safe.
        if float(scores.get("numbness_shutdown", 0)) >= 4:
            return "F8_somatic", "T-ground"
        if int(scores.get("suds", 0)) >= 7:
            return "F5_DBT", "T-ground"
        return "F9_MBCT", "T-ground"

    if chasing_flag:
        # Chasing is an urge problem before it is a thinking problem:
        # high arousal → DBT regulation; otherwise ACT urge/willingness work.
        # The caller attaches CHASING_NOTE (urge-surfing + support lines).
        if int(scores.get("suds", 0)) >= 7:
            return "F5_DBT", "GH"
        return "F4_ACT", "GH"

    if low_mood_flag:
        # Acute distress still takes precedence over the activation plan.
        if int(scores.get("suds", 0)) >= 8:
            return "F5_DBT", "P1"
        return "F2_BA", "LM"

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


def _build_hypothesis_th(situation_key: str, scores: dict, fw_code: str,
                         emotion_words: Optional[list] = None,
                         need_label: str = "") -> str:
    """Thai mirror of _build_hypothesis — composed from translated fragments."""
    sit = SITUATIONS.get(situation_key, {})
    sit_th = _th(sit.get("label", "")) or "สิ่งที่คุณเล่ามา"
    fw_en  = FRAMEWORKS.get(fw_code, {}).get("name", "")
    fw_th  = _th(fw_en) or fw_en

    threads = []
    s = scores
    if s.get("shame_selfattack", 0) >= 4:        threads.append("some self-criticism")
    if s.get("anxiety_catastrophising", 0) >= 4: threads.append("worry about what happens next")
    if s.get("anger_hidden_hurt", 0) >= 4:       threads.append("hurt underneath the surface")
    if s.get("grief_meaningloss", 0) >= 4:       threads.append("a real sense of loss")
    if s.get("numbness_shutdown", 0) >= 4:       threads.append("some emotional flatness")
    if s.get("relationship_threat", 0) >= 4:     threads.append("worry about your place in this relationship")
    if s.get("avoidance", 0) >= 4:               threads.append("tension around choices")
    threads_th = [(_th(t) or t) for t in threads[:2]]

    parts: list[str] = []
    if threads_th:
        parts.append(f"ฟังดูเหมือนเรื่อง{sit_th} กำลังพา{('และ'.join(threads_th))}ขึ้นมาด้วย")
    else:
        parts.append(f"คุณเพิ่งเล่าเรื่อง{sit_th}ออกมาในคำของคุณเอง")

    words = [w for w in (emotion_words or []) if w][:2]
    if words:
        quoted = " และ ".join(f"“{_th(w) or w}”" for w in words)
        parts.append(f"คุณเรียกชื่อมันเองว่า {quoted}")

    if need_label:
        need_th = _th(need_label) or need_label
        short = need_th.split(" — ")[0].strip()
        parts.append(f"และลึกลงไป สิ่งที่ขาดหายตอนนี้คือ{short}")

    parts.append(f"แนวทางที่เข้ากับแพทเทิร์นนี้ที่สุดคือ **{fw_th}** — มันทำงานกับแพทเทิร์นแบบนี้โดยตรง")
    return " ".join(parts)


def _build_closure_th(suds_start: int, suds_end: int) -> str:
    delta = suds_start - suds_end
    if delta >= 3:
        return f"คุณเข้ามาที่ {suds_start} และกำลังจะกลับที่ {suds_end} — คุณทำได้ด้วยคำพูดล้วน ๆ นั่นมีความหมายมาก"
    if delta >= 1:
        return f"คุณเริ่มที่ {suds_start} ตอนนี้อยู่ที่ {suds_end} — การขยับแม้เล็กน้อยก็เป็นของจริง เทคนิคด้านบนเป็นของคุณ ใช้ซ้ำได้เสมอ"
    if delta == 0:
        return f"ตัวเลขยังอยู่ที่ {suds_end} — ไม่เป็นไรเลย บางครั้งการได้เรียกชื่อความรู้สึกก็คือประเด็นทั้งหมด แล้วการเปลี่ยนแปลงจะตามมาทีหลัง"
    return (
        f"ตอนนี้อยู่ที่ {suds_end} สูงขึ้นจาก {suds_start} — เกิดขึ้นได้ "
        "การพูดถึงบางเรื่องทำให้มันขุ่นขึ้นก่อนจะตกตะกอน เทคนิคด้านบนช่วยได้ "
        "และกลับมาได้เสมอเมื่อต้องการ"
    )


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

    if step == "CONSENT":
        # answer: {"agreed": bool, "training": bool} — must agree to proceed.
        agreed = bool(answer.get("agreed")) if isinstance(answer, dict) else bool(answer)
        if not agreed:
            # cannot pass the gate without agreement — re-present it.
            state["next_step"] = "CONSENT"
            return _build_consent(), state
        state["consent_agreed"] = True
        state["training_opt_in"] = bool(answer.get("training")) if isinstance(answer, dict) else False
        state["next_step"] = "SAFETY"
        return _build_safety(), state

    if step == "GOAL":
        if answer and answer != "__skip__":
            state["goal_text"] = str(answer).strip()[:1000]
            state["goal_lang"] = _detect_lang(state["goal_text"])
        state["next_step"] = "BODY_LOC"
        return _build_body_location(), state

    if step == "SAFETY":
        if answer in ("yes", "not_sure"):
            state["next_step"] = "CRISIS"
            return {
                "step": "CRISIS", "done": True, "exit_type": "crisis_exit",
                "type": "crisis_exit", "heading": "Your safety comes first.",
                "question": SAFETY_SCRIPT, "question_th": TH_NOTES["SAFETY_SCRIPT"], "options": [],
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
                    "question": GROUNDING_PAUSE_SCRIPT, "question_th": TH_NOTES["GROUNDING_PAUSE_SCRIPT"], "options": [],
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
        # Capture the client's own-words goal once the context is chosen.
        state["next_step"] = "GOAL"
        return _build_goal(), state

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
        return _next_after_questions(state), state

    if step == "BELIEF":
        try:
            state["bottom_line_belief"] = int(answer)
        except (TypeError, ValueError):
            state["bottom_line_belief"] = None
        state["bottom_line_rated"] = True
        return _next_after_belief(state), state

    if step == "QUESTION":
        sit_key = state.get("situation_key") or "other"
        queue   = state.get("questions_queue", [])
        q_idx   = state.get("question_index", 0)
        if q_idx < len(queue):
            item = _item_by_id(sit_key, queue[q_idx])
            if item and answer != "__skip__":
                # Pattern recognition from the user's own words (text items).
                if item.get("input_type") == "text":
                    _scan_trauma(state, answer)
                    if sit_key == "trading":
                        _scan_chasing(state, answer)
                    # Structured thought record: keep the first own-words thought.
                    if not state.get("thought_text") and isinstance(answer, str) and len(answer.strip()) >= 3:
                        state["thought_text"] = answer.strip()[:500]
                        state["thought_lang"] = _detect_lang(answer)
                _apply_deltas(state, item.get("score_deltas", {}))
                # capture the critic's protective intention (S5 formulation)
                if item.get("capture") == "critic_protects" and isinstance(answer, str) and answer.strip():
                    state["critic_protects_text"] = answer.strip()[:400]
                # per-option deltas: the chosen option carries its own signal
                if item.get("input_type") == "single_select":
                    for opt in item.get("options", []):
                        if opt["id"] == answer:
                            _apply_deltas(state, opt.get("score_deltas", {}))
                            # Branch C: classify the critic's function; the
                            # contemptuous attacker raises the hated-self flag.
                            if opt.get("critic_function"):
                                state["critic_function"] = opt["critic_function"]
                            if opt.get("hated_self"):
                                state["hated_self_flag"] = True
                            break
                    # "get it back now" is within-session chasing (structural hit)
                    if sit_key == "trading" and answer == "win_back":
                        _chasing_structural_hit(state)
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
                elif item.get("value_scoring") == "energy_left":
                    # empty tank = depletion — the burnout/low-mood channel
                    try:
                        energy = float(answer)
                    except (TypeError, ValueError):
                        energy = 50.0
                    _apply_deltas(state, {"numbness_shutdown": (100 - energy) / 33.0})
                # ── Bottom Line capture (S2 formulation) ──
                if not state.get("bottom_line_text"):
                    tmpl = item.get("bottom_line")
                    if tmpl and isinstance(answer, str) and answer.strip() and "{}" in tmpl:
                        # text elicitor, e.g. "I am {}" ← user's blank
                        state["bottom_line_text"] = tmpl.format(answer.strip())[:300]
                        state["bottom_line_lang"] = _detect_lang(answer)
                    elif item.get("input_type") == "single_select":
                        # the chosen option may carry its own Bottom Line
                        for opt in item.get("options", []):
                            if opt["id"] == answer and opt.get("bottom_line"):
                                state["bottom_line_text"] = opt["bottom_line"]
                                state["bottom_line_lang"] = "en"
                                break
        next_idx = q_idx + 1
        state["question_index"] = next_idx
        if next_idx < len(queue):
            state["next_step"] = "QUESTION"
            next_item = _item_by_id(sit_key, queue[next_idx])
            return _build_question(next_item, next_idx + 1, len(queue), _next_validation(state)), state
        return _next_after_questions(state), state

    if step == "MOOD1":
        state["mood_answers"]["MOOD1"] = answer
        state["next_step"] = "MOOD2"
        return _build_mood_check("MOOD2"), state

    if step == "MOOD2":
        state["mood_answers"]["MOOD2"] = answer
        w1 = _mood_weight("MOOD1", state["mood_answers"].get("MOOD1"))
        w2 = _mood_weight("MOOD2", answer)
        # Both "most days" (2Q-positive on both gates) → the full pattern.
        if w1 + w2 >= 2:
            state["low_mood_flag"] = True
        # Partial endorsement nudges the depletion channel without overriding.
        elif w1 + w2 >= 1:
            _apply_deltas(state, {"numbness_shutdown": 2})
        sit_key = state.get("situation_key") or "other"
        state["next_step"] = "UNMET_NEED"
        return _build_unmet_need(sit_key), state

    if step == "UNMET_NEED":
        state["unmet_need"] = answer
        sit_key = state.get("situation_key") or "other"
        if answer and answer != "none":
            _apply_deltas(state, UNMET_NEED_DELTAS.get(f"{sit_key}:{answer}", {}))
            if sit_key == "trading" and answer == "make_it_back":
                _chasing_structural_hit(state)
        # When self-kindness is the therapeutic focus, gauge fear-of-compassion
        # first (Branch D). Otherwise deliver the compassion line directly.
        if _compassion_relevant(state):
            state["next_step"] = "FOC"
            return _build_foc(), state
        state["next_step"] = "COMPASSION"
        return _build_self_compassion(sit_key), state

    if step == "FOC":
        state["foc_level"] = answer
        # high fear-of-compassion → others-first sequencing (Branch D)
        state["compassion_mode"] = "others_first" if answer in ("awkward", "undeserved") else "direct"
        sit_key = state.get("situation_key") or "other"
        state["next_step"] = "COMPASSION"
        return _build_self_compassion(sit_key, mode=state["compassion_mode"], with_pause=True), state

    if step == "COMPASSION":
        sit_key = state.get("situation_key") or "other"
        # backdraft pause pathway → grounding, no re-entry this session
        if answer == "pause":
            state["status"] = "grounding_pause"
            state["next_step"] = "PAUSE"
            return {
                "step": "PAUSE", "done": True, "exit_type": "grounding_pause",
                "type": "grounding_pause", "heading": "Let's pause here.",
                "question": GROUNDING_PAUSE_SCRIPT, "question_th": TH_NOTES["GROUNDING_PAUSE_SCRIPT"], "options": [],
            }, state
        # if we gauged fear-of-compassion, close the loop with 2-tap feedback
        if state.get("foc_level"):
            state["next_step"] = "SOOTHE"
            return _build_soothe(), state
        state["next_step"] = "IFTHEN"
        return _build_ifthen(sit_key, None), state

    if step == "SOOTHE":
        try:
            state["soothe_rating"] = int(answer)
        except (TypeError, ValueError):
            state["soothe_rating"] = None
        sit_key = state.get("situation_key") or "other"
        state["next_step"] = "IFTHEN"
        return _build_ifthen(sit_key, None), state

    if step == "IFTHEN":
        if answer and answer != "__skip__":
            state["ifthen_text"] = str(answer)
        # If the user named a goal at S1, close with goal-attainment scaling.
        if state.get("goal_text"):
            state["next_step"] = "GOAL_ATTAIN"
            return _build_goal_attain(state["goal_text"]), state
        state["next_step"] = "RERATE"
        return _build_rerate(state.get("suds_start") or 5), state

    if step == "GOAL_ATTAIN":
        try:
            state["goal_attainment"] = int(answer)
        except (TypeError, ValueError):
            state["goal_attainment"] = None
        state["next_step"] = "RERATE"
        return _build_rerate(state.get("suds_start") or 5), state

    if step == "RERATE":
        suds_end   = int(answer)
        suds_start = state.get("suds_start") or suds_end
        state["suds_end"]        = suds_end
        state["scores"]["suds"]  = suds_end
        trauma_flag              = bool(state.get("trauma_flag"))
        low_mood_flag            = bool(state.get("low_mood_flag"))
        chasing_flag             = bool(state.get("chasing_flag"))
        fw_code, priority        = _select_framework(state["scores"], trauma_flag, low_mood_flag, chasing_flag)
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
        # A warm referral is offered when the trauma flag is on, OR when severity
        # is high enough that a person trained for this would serve them better.
        hated_self_flag = bool(state.get("hated_self_flag"))
        refer = (trauma_flag or suds_end >= 8
                 or state["scores"].get("shame_selfattack", 0) >= 9 or hated_self_flag)
        critic_fn = state.get("critic_function")
        ifthen_action = state.get("ifthen_text") or sit.get("ifthen_template", "")
        followup = FOLLOWUP_CONFIG.get(sit_key)
        if followup:
            followup = {**followup, "checkin_th": _th(followup.get("checkin")) or followup.get("checkin")}
        state["next_step"] = "DONE"
        return {
            "step": "DONE", "done": True, "exit_type": "complete",
            "type": "result",
            "closure_text": _build_closure(suds_start, suds_end),
            "closure_text_th": _build_closure_th(suds_start, suds_end),
            "result": {
                "framework_code":    fw_code,
                "framework_name":    fw["name"],
                "framework_name_th": _th(fw["name"]) or fw["name"],
                "evidence":          fw.get("evidence"),
                "tier":              fw.get("tier"),
                "hypothesis":        _build_hypothesis(
                    sit_key, state["scores"], fw_code,
                    emotion_words=state.get("emotion_words"),
                    need_label=need_label,
                ),
                "hypothesis_th":     _build_hypothesis_th(
                    sit_key, state["scores"], fw_code,
                    emotion_words=state.get("emotion_words"),
                    need_label=need_label,
                ),
                "technique":         fw["technique"],
                "technique_th":      TH_TECHNIQUES.get(fw_code, fw["technique"]),
                "ifthen_action":     ifthen_action,
                "ifthen_action_th":  _th(ifthen_action) or ifthen_action,
                # client's own-words goal — the S1 outcome anchor (raw, not translated)
                "goal_text":         state.get("goal_text"),
                "goal_lang":         state.get("goal_lang"),
                # Bottom Line + belief-strength (S2 formulation)
                "bottom_line_text":   state.get("bottom_line_text"),
                "bottom_line_belief": state.get("bottom_line_belief"),
                "bottom_line_lang":   state.get("bottom_line_lang"),
                # Automatic thought (S3-S4) — completes the structured record
                "thought_text":      state.get("thought_text"),
                "thought_lang":      state.get("thought_lang"),
                # Inner critic (S5) — Branch C reframe + hated-self escalation
                "critic_function":   critic_fn,
                "critic_reframe":    CRITIC_FUNCTION_REFRAMES.get(critic_fn) if critic_fn else None,
                "critic_reframe_th": TH_NOTES.get(f"critic_{critic_fn}") if critic_fn else None,
                "critic_protects_text": state.get("critic_protects_text"),
                "hated_self_flagged": hated_self_flag,
                "hated_self_note":    HATED_SELF_NOTE if hated_self_flag else None,
                "hated_self_note_th": TH_NOTES.get("HATED_SELF_NOTE") if hated_self_flag else None,
                # Self-compassion (S6-S7) — FOC/Branch D + soothing feedback
                "foc_level":         state.get("foc_level"),
                "compassion_mode":   state.get("compassion_mode"),
                "soothe_rating":     state.get("soothe_rating"),
                # Goal-attainment (S12 closure) — vs the S1 goal
                "goal_attainment":   state.get("goal_attainment"),
                "selfcompassion_text": sit.get("self_compassion", ""),
                "selfcompassion_text_th": _th(sit.get("self_compassion", "")) or sit.get("self_compassion", ""),
                "situation_key":     sit_key,
                "situation_label":   sit.get("label", ""),
                "situation_label_th": _th(sit.get("label", "")) or sit.get("label", ""),
                "situation_icon":    sit.get("icon", ""),
                "emotion_words":     state.get("emotion_words", []),
                "emotion_words_th":  [(_th(w) or w) for w in state.get("emotion_words", [])],
                "unmet_need":        need_label,
                "unmet_need_th":     _th(need_label) or need_label,
                "suds_start":        suds_start,
                "suds_end":          suds_end,
                "track":             state.get("track"),
                "scores":            state["scores"],
                "priority":          priority,
                # ── Trauma-informed additions (detect, never probe) ──
                "trauma_flagged":    trauma_flag,
                "trauma_ack":        TRAUMA_ACK if trauma_flag else None,
                "trauma_ack_th":     TH_NOTES.get("TRAUMA_ACK") if trauma_flag else None,
                "referral":          REFERRAL_SCRIPT if refer else None,
                "referral_th":       TH_NOTES.get("REFERRAL_SCRIPT") if refer else None,
                # ── Low-mood pattern (2Q-derived; support, never a label) ──
                "low_mood_flagged":  low_mood_flag,
                "low_mood_note":     LOW_MOOD_NOTE if low_mood_flag else None,
                "low_mood_note_th":  TH_NOTES.get("LOW_MOOD_NOTE") if low_mood_flag else None,
                # ── Chasing pattern (TDS-grounded; urge support, no verdict) ──
                "chasing_flagged":   chasing_flag,
                "chasing_note":      CHASING_NOTE if chasing_flag else None,
                "chasing_note_th":   TH_NOTES.get("CHASING_NOTE") if chasing_flag else None,
                # ── Follow-up (self-contained session; check-in is opt-in) ──
                "followup":          followup,
            },
        }, state

    # Unknown step — restart
    state["next_step"] = "SAFETY"
    return _build_safety(), state


def _rebuild_current(step: str, state: dict) -> dict:
    sit = state.get("situation_key") or "other"
    if step == "CONSENT":    return _build_consent()
    if step == "GOAL":       return _build_goal()
    if step == "SAFETY":     return _build_safety()
    if step == "SUDS_INIT":  return _build_suds_initial()
    if step == "GROUNDING":  return _build_grounding(state.get("grounding_rounds", 0) + 1)
    if step == "SUDS_RERATE":return _build_suds_rerate()
    if step == "SITUATION":  return _build_situation()
    if step == "BODY_LOC":   return _build_body_location()
    if step == "BODY_QUAL":  return _build_body_quality()
    if step == "EMOTIONS":   return _build_emotions(sit)
    if step == "BELIEF":     return _build_belief(state.get("bottom_line_text") or "")
    if step == "MOOD1":      return _build_mood_check("MOOD1")
    if step == "MOOD2":      return _build_mood_check("MOOD2")
    if step == "UNMET_NEED": return _build_unmet_need(sit)
    if step == "FOC":        return _build_foc()
    if step == "SOOTHE":     return _build_soothe()
    if step == "COMPASSION":
        return _build_self_compassion(sit, mode=state.get("compassion_mode") or "direct",
                                      with_pause=bool(state.get("foc_level")))
    if step == "IFTHEN":     return _build_ifthen(sit, state.get("ifthen_text"))
    if step == "GOAL_ATTAIN": return _build_goal_attain(state.get("goal_text") or "")
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
    global FOLLOWUP_CONFIG

    situations: dict[str, dict] = {}
    priors: dict[str, dict] = {}
    followups: dict[str, dict] = {}
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
            if it.bottom_line:
                d["bottom_line"] = it.bottom_line
            if it.capture:
                d["capture"] = it.capture
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
        fu = json.loads(srow.followup_json or "{}")
        if fu:
            followups[srow.key] = fu

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
    if followups:            FOLLOWUP_CONFIG = followups

    # Translations: DB copy wins so operators can edit Thai without a deploy.
    global TH_STRINGS, TH_TECHNIQUES, TH_NOTES
    tr_strings: dict[str, str] = {}
    tr_techniques: dict[str, str] = {}
    tr_notes: dict[str, str] = {}
    for row in db.query(AEHQTranslation).filter(AEHQTranslation.lang == "th").all():
        if row.src.startswith("technique:"):
            tr_techniques[row.src.split(":", 1)[1]] = row.dst
        elif row.src.startswith("note:"):
            tr_notes[row.src.split(":", 1)[1]] = row.dst
        else:
            tr_strings[row.src] = row.dst
    if tr_strings:    TH_STRINGS = tr_strings
    if tr_techniques: TH_TECHNIQUES = tr_techniques
    if tr_notes:      TH_NOTES = tr_notes


def _ensure_cache(db: DBSession) -> None:
    """Seed/refresh the DB content, then load the cache once per process.

    Self-migrating: a meta row stores the content version that last seeded the
    DB. When the running code carries a newer CONTENT_VERSION (a deploy), the
    content tables are refreshed automatically — no manual reseed step.
    User sessions/results are never touched by the refresh."""
    global _CACHE_LOADED
    if _CACHE_LOADED:
        return
    from seed_aehq import seed_aehq, ensure_aehq_columns  # lazy — avoids a cycle
    # Bring late-added columns in on already-seeded DBs (prod upgrade path).
    ensure_aehq_columns(db.get_bind())
    stored_version = db.execute(
        select(AEHQTranslation.dst).where(
            AEHQTranslation.lang == "meta", AEHQTranslation.src == "content_version")
    ).scalar_one_or_none()
    if db.query(AEHQFramework).count() == 0 or stored_version != CONTENT_VERSION:
        seed_aehq(db, reset=True)
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
    sess = AEHQSession(user_id=user_id, next_step="CONSENT", state_json=json.dumps(state), status="active")
    db.add(sess)
    db.commit()
    db.refresh(sess)
    return {"session_id": sess.id, **_build_consent()}


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
                "question": SAFETY_SCRIPT, "question_th": TH_NOTES["SAFETY_SCRIPT"], "options": []}
    if sess.status == "grounding_pause":
        return {"session_id": sess.id, "step": "PAUSE", "done": True, "exit_type": "grounding_pause",
                "type": "grounding_pause", "heading": "Let's pause here.",
                "question": GROUNDING_PAUSE_SCRIPT, "question_th": TH_NOTES["GROUNDING_PAUSE_SCRIPT"], "options": []}

    return {"session_id": sess.id, **_rebuild_current(state.get("next_step", "SAFETY"), state)}


def submit_answer(session_id: int, user_id: int, step: str, answer: Any, db: DBSession,
                  lang: str = "en") -> dict:
    _ensure_cache(db)
    sess  = _load(session_id, user_id, db)
    state = json.loads(sess.state_json)

    if state.get("next_step") != step:
        raise HTTPException(400, f"Expected step {state.get('next_step')!r}, got {step!r}")

    lang_shown = lang if lang in ("th", "en") else "en"
    db.add(AEHQResponse(
        session_id=sess.id, step=step, answer_json=json.dumps(answer),
        content_version=CONTENT_VERSION, lang_shown=lang_shown,
    ))

    payload, state = _transition(step, answer, state)
    sess.state_json = json.dumps(state)
    sess.next_step  = state.get("next_step", "CONSENT")

    # Persist consent immediately at the gate (PDPA auditability).
    if step == "CONSENT" and state.get("consent_agreed"):
        sess.consent_agreed  = True
        sess.training_opt_in = bool(state.get("training_opt_in"))
        sess.consent_at      = datetime.utcnow()

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
                trauma_flagged=bool(r.get("trauma_flagged")),
                referral_offered=bool(r.get("referral")),
                low_mood_flagged=bool(r.get("low_mood_flagged")),
                chasing_flagged=bool(r.get("chasing_flagged")),
                goal_text=state.get("goal_text"),
                goal_lang=state.get("goal_lang"),
                content_version=CONTENT_VERSION,
                bottom_line_text=state.get("bottom_line_text"),
                bottom_line_belief=state.get("bottom_line_belief"),
                bottom_line_lang=state.get("bottom_line_lang"),
                thought_text=state.get("thought_text"),
                thought_lang=state.get("thought_lang"),
                critic_function=state.get("critic_function"),
                critic_protects_text=state.get("critic_protects_text"),
                hated_self_flagged=bool(state.get("hated_self_flag")),
                foc_level=state.get("foc_level"),
                compassion_mode=state.get("compassion_mode"),
                soothe_rating=state.get("soothe_rating"),
                goal_attainment=state.get("goal_attainment"),
            ))

    db.commit()

    # S11 — attach the belief trajectory vs. prior sessions with the same Bottom Line.
    if payload.get("result") and payload["result"].get("bottom_line_text"):
        payload["result"]["belief_trajectory"] = _belief_trajectory(
            user_id, payload["result"]["bottom_line_text"],
            payload["result"].get("bottom_line_belief"), db, sess.id,
        )
    return {"session_id": sess.id, **payload}


def get_result(session_id: int, user_id: int, db: DBSession) -> dict:
    sess = _load(session_id, user_id, db)
    if not sess.result:
        raise HTTPException(404, "Session not complete")
    r = sess.result
    scores = json.loads(r.scores_json) if r.scores_json else {}
    followup = FOLLOWUP_CONFIG.get(r.situation_key)
    if followup:
        followup = {**followup, "checkin_th": _th(followup.get("checkin")) or followup.get("checkin")}
    sit = SITUATIONS.get(r.situation_key or "", {})
    return {
        "session_id":    sess.id,
        "exit_type":     r.exit_type,
        "framework_code":r.framework_code,
        "framework_name":r.framework_name,
        "framework_name_th": _th(r.framework_name) or r.framework_name,
        "situation_key": r.situation_key,
        "situation_label_th": _th(sit.get("label", "")) or sit.get("label", ""),
        "track":         r.track,
        "hypothesis":    r.hypothesis_text,
        "hypothesis_th": _build_hypothesis_th(r.situation_key or "other", scores, r.framework_code or "F12_ifthen"),
        "technique":     r.technique_text,
        "technique_th":  TH_TECHNIQUES.get(r.framework_code or "", r.technique_text),
        "evidence":      r.evidence_text,
        "ifthen_action": r.ifthen_text,
        "ifthen_action_th": _th(r.ifthen_text) or r.ifthen_text,
        "goal_text":     r.goal_text,
        "goal_lang":     r.goal_lang,
        "bottom_line_text":   r.bottom_line_text,
        "bottom_line_belief": r.bottom_line_belief,
        "bottom_line_lang":   r.bottom_line_lang,
        "thought_text":       r.thought_text,
        "thought_lang":       r.thought_lang,
        "critic_function":    r.critic_function,
        "critic_reframe":     CRITIC_FUNCTION_REFRAMES.get(r.critic_function) if r.critic_function else None,
        "critic_reframe_th":  TH_NOTES.get(f"critic_{r.critic_function}") if r.critic_function else None,
        "critic_protects_text": r.critic_protects_text,
        "hated_self_flagged": r.hated_self_flagged,
        "hated_self_note":    HATED_SELF_NOTE if r.hated_self_flagged else None,
        "hated_self_note_th": TH_NOTES.get("HATED_SELF_NOTE") if r.hated_self_flagged else None,
        "foc_level":         r.foc_level,
        "compassion_mode":   r.compassion_mode,
        "soothe_rating":     r.soothe_rating,
        "goal_attainment":   r.goal_attainment,
        "belief_trajectory": _belief_trajectory(user_id, r.bottom_line_text, r.bottom_line_belief, db, sess.id),
        "selfcompassion_text": r.selfcompassion_text,
        "selfcompassion_text_th": _th(r.selfcompassion_text) or r.selfcompassion_text,
        "closure_text":  r.closure_text,
        "closure_text_th": _build_closure_th(r.suds_start or 0, r.suds_end or 0),
        "suds_start":    r.suds_start,
        "suds_end":      r.suds_end,
        "scores":        scores,
        "trauma_flagged": r.trauma_flagged,
        "trauma_ack":    TRAUMA_ACK if r.trauma_flagged else None,
        "trauma_ack_th": TH_NOTES.get("TRAUMA_ACK") if r.trauma_flagged else None,
        "referral":      REFERRAL_SCRIPT if r.referral_offered else None,
        "referral_th":   TH_NOTES.get("REFERRAL_SCRIPT") if r.referral_offered else None,
        "low_mood_flagged": r.low_mood_flagged,
        "low_mood_note": LOW_MOOD_NOTE if r.low_mood_flagged else None,
        "low_mood_note_th": TH_NOTES.get("LOW_MOOD_NOTE") if r.low_mood_flagged else None,
        "chasing_flagged": r.chasing_flagged,
        "chasing_note": CHASING_NOTE if r.chasing_flagged else None,
        "chasing_note_th": TH_NOTES.get("CHASING_NOTE") if r.chasing_flagged else None,
        "followup":      followup,
        "created_at":    r.created_at.isoformat() if r.created_at else None,
    }


def _belief_trajectory(user_id: int, bottom_line_text: Optional[str],
                       current_belief: Optional[int], db: DBSession,
                       exclude_session_id: int) -> Optional[dict]:
    """S11 — if the same Bottom Line was rated in a PRIOR session, return the
    movement so the client can show 'visible change consolidates identity shift.'"""
    if not bottom_line_text or current_belief is None:
        return None
    prior = db.execute(
        select(AEHQResult)
        .where(AEHQResult.user_id == user_id,
               AEHQResult.bottom_line_text == bottom_line_text,
               AEHQResult.bottom_line_belief.is_not(None),
               AEHQResult.session_id != exclude_session_id)
        .order_by(AEHQResult.created_at.desc())
        .limit(1)
    ).scalar_one_or_none()
    if not prior:
        return None
    return {
        "belief": bottom_line_text,
        "prior_belief": prior.bottom_line_belief,
        "prior_at": prior.created_at.isoformat() if prior.created_at else None,
        "current_belief": current_belief,
        "delta": current_belief - prior.bottom_line_belief,  # negative = belief loosened
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
            # longitudinal fields (S11/S12) — belief %, soothing, goal-attainment
            "bottom_line_text":   r.bottom_line_text,
            "bottom_line_belief": r.bottom_line_belief,
            "soothe_rating":      r.soothe_rating,
            "goal_attainment":    r.goal_attainment,
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
