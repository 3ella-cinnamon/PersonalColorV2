# BaZi Five-Element reference — injected into every coaching prompt
_ELEMENT_GUIDE = {
    "WOOD":  {
        "power_colors":   "green, teal, olive",
        "support_colors": "black, navy (Water feeds Wood)",
        "drain_colors":   "white, grey, silver (Metal chops Wood)",
        "direction":      "East",
        "peak_hours":     "6 am – 10 am",
        "energy_tone":    "growth, expansion, new starts",
    },
    "FIRE":  {
        "power_colors":   "red, orange, hot pink",
        "support_colors": "green, teal (Wood feeds Fire)",
        "drain_colors":   "dark blue, black (Water extinguishes Fire)",
        "direction":      "South",
        "peak_hours":     "10 am – 2 pm",
        "energy_tone":    "momentum, visibility, high-energy action",
    },
    "EARTH": {
        "power_colors":   "yellow, mustard, beige, terracotta",
        "support_colors": "red, orange (Fire produces Earth)",
        "drain_colors":   "green (Wood breaks Earth)",
        "direction":      "Center / Southwest",
        "peak_hours":     "1 pm – 4 pm",
        "energy_tone":    "stability, grounding, trust-building",
    },
    "METAL": {
        "power_colors":   "white, gold, silver, champagne",
        "support_colors": "yellow, beige (Earth produces Metal)",
        "drain_colors":   "red, orange (Fire melts Metal)",
        "direction":      "West",
        "peak_hours":     "4 pm – 8 pm",
        "energy_tone":    "precision, decisiveness, cutting through noise",
    },
    "WATER": {
        "power_colors":   "black, dark navy, deep blue",
        "support_colors": "white, grey (Metal produces Water)",
        "drain_colors":   "yellow, brown (Earth dams Water)",
        "direction":      "North",
        "peak_hours":     "8 pm – 10 pm  or  early 5 am – 7 am",
        "energy_tone":    "flow, adaptability, deep listening",
    },
}

_GOAL_FOCUS = {
    "work": {
        "label":    "Work & Leadership",
        "focus":    "authority, decision timing, team influence, when to push vs. hold back",
        "key_move": "establish your frame early; speak last when consensus-building; speak first when setting direction",
        "avoid":    "explaining your reasoning before stating your position — it signals uncertainty",
    },
    "money": {
        "label":    "Money & Negotiation",
        "focus":    "opening position, silence as power, concession timing, recognising closing signals",
        "key_move": "let the other side speak first; anchor high/low before any counter; go silent after your number",
        "avoid":    "filling silence with justifications — silence is leverage, not awkwardness",
    },
    "relationship": {
        "label":    "Relationship & Connection",
        "focus":    "emotional pacing, listening ratio, trust-building sequence, repair moves",
        "key_move": "match their energy for 90 seconds before introducing your own rhythm",
        "avoid":    "problem-solving before the other person feels fully heard",
    },
}


def build_coaching_prompt(
    profile_ctx: dict,
    goal_ctx: dict,
    bazi_score: float,
    variation: dict,
    generation_count: int,
    excluded_angles: list[str],
    day_master: str = "UNKNOWN",
    daily_element: str = "UNKNOWN",
    # ── New DB-computed fields (token-free pre-computation) ──────────────
    stance: str = "NEUTRAL",              # ADVANCE / DEFEND / RESTRAIN / AVOID / NEUTRAL
    stance_th: str = "ปกติ",              # Thai label
    strong_day: bool = False,             # True only when stance=ADVANCE + planetary hour suits goal
    lead_colour: str = "",                # from BaZi favourable element
    lead_colour_hex: str = "",
    secondary_colour: str = "",
    power_direction: str = "",            # Qimen-style compass direction
    planetary_hour_ruler: str = "",       # current planetary hour ruler (Jupiter/Mercury/Venus/etc.)
    planetary_hour_best_for: str = "",    # what this ruler is best for
    planetary_hour_avoid: str = "",       # what to avoid in this ruler
    peak_hour_window: str = "",           # e.g. "10:00–12:00"
    thai_day_ruler: str = "",             # Thai day planet (พฤหัส / พุธ / etc.)
    saturn_note: str = "",                # Saturn placement coaching note
) -> str:

    goal_slug = goal_ctx["goal_slug"]
    gf        = _GOAL_FOCUS.get(goal_slug, {"label": goal_slug.title(),
                                             "focus": goal_slug, "key_move": "", "avoid": ""})

    dm_guide    = _ELEMENT_GUIDE.get(str(day_master).upper(),  {})
    day_guide   = _ELEMENT_GUIDE.get(str(daily_element).upper(), {})

    # Derive lead colour from element guide if not explicitly passed
    _lead_colour = lead_colour or dm_guide.get('power_colors', 'your power color')
    _direction   = power_direction or dm_guide.get('direction', 'N/A')

    # Strong day label
    strong_day_label = "★ STRONG DAY — stance ADVANCE + planetary hour aligned" if strong_day else ""

    # Element interaction hint
    if day_master == daily_element:
        element_note = f"Today's element ({daily_element}) matches your Day Master — high alignment, energy flows naturally."
    else:
        element_note = (
            f"Today's element ({daily_element}) vs your Day Master ({day_master}) — "
            f"requires conscious calibration. Lean on {_lead_colour}."
        )

    bazi_band = (
        "HIGH energy day — decisive action favoured. Move early, close deals."
        if bazi_score >= 7 else
        "MODERATE energy — calibrate pace. Prepare thoroughly before acting."
        if bazi_score >= 4 else
        "LOW energy day — observe more, speak less. Conserve for essential moves only."
    )

    return f"""════════════════════════════════════════════════════
TODAY'S ENERGY TIER  {strong_day_label}
════════════════════════════════════════════════════
STANCE        : {stance} ({stance_th})  ← ALL behavior must follow this stance
BaZi Score    : {bazi_score:.1f}/10  →  {bazi_band}
Strong Day    : {'YES — ADVANCE + planetary hour aligned for this goal' if strong_day else 'No'}

LAYER 1 — ASTRONOMY (foundation)
  Planetary Hour    : {planetary_hour_ruler}  (ยาม {thai_day_ruler})
  Best for          : {planetary_hour_best_for}
  Avoid during this hour: {planetary_hour_avoid or '—'}
  Peak window today : {peak_hour_window or dm_guide.get('peak_hours', 'N/A')}

LAYER 2 — BAZI (primary)
  Day Master        : {day_master}
  Today's Element   : {daily_element}  →  {day_guide.get('energy_tone', 'N/A')}
  Lead colour       : {_lead_colour}{f'  ({lead_colour_hex})' if lead_colour_hex else ''}
  Secondary colour  : {secondary_colour or dm_guide.get('support_colors', 'N/A')}
  Drain colours     : {dm_guide.get('drain_colors', 'N/A')}
  Element note      : {element_note}

LAYER 3 — QIMEN DIRECTION
  Power direction   : {_direction}  ← Use in practical_tip #2

LAYER 4 — THAI ASTROLOGY
  Day ruler         : {thai_day_ruler}
  Saturn note       : {saturn_note or 'Discipline and patience rewarded — avoid shortcuts.'}

════════════════════════════════════════════════════
PROFILE
════════════════════════════════════════════════════
LAYER 5 — HUMAN DESIGN  (HOW to decide — process overlay)
  Type + Authority  : {profile_ctx['hd_type_name']}
  Strategy          : {profile_ctx['hd_strategy']}
  Energy type       : {profile_ctx['hd_energy_type']}
  Timing principle  : {profile_ctx['hd_negotiation_timing']}
  Common mistakes   : {', '.join(profile_ctx['hd_common_mistakes'])}
  ⚠ PROJECTOR RULE  : Never initiate without invitation/recognition.
                      On ADVANCE days: await the right invitation, then move decisively.
                      On DEFEND/AVOID days: prepare, observe, conserve.

LAYER 6 — MBTI  (communication style overlay only)
  Type              : {profile_ctx['mbti_code']}
  Communication     : {profile_ctx['mbti_communication_style']}
  Decision pattern  : {profile_ctx['mbti_decision_pattern']}
  Blind spots       : {', '.join(profile_ctx['mbti_blind_spots'])}

Personal Color
  Season            : {profile_ctx['color_season']}
  Communication vibe: {profile_ctx['color_communication_vibe']}
  Language style    : {profile_ctx['color_language_style']}
  Impression        : {', '.join(profile_ctx['color_impression'])}

MBTI + HD Dynamic
  Blend             : {profile_ctx['scenario_blend']}
  Tension           : {profile_ctx['scenario_conflict']}

════════════════════════════════════════════════════
GOAL: {gf['label'].upper()}
════════════════════════════════════════════════════
Focus area    : {gf['focus']}
Key move today: {gf['key_move']}
Critical avoid: {gf['avoid']}

MBTI decision rules for {gf['label']}:
{chr(10).join(f'  • {r["decision"]}' for r in goal_ctx['mbti_decisions'][:3])}

HD decision rules for {gf['label']}:
{chr(10).join(f'  • {r["decision"]}' for r in goal_ctx['hd_decisions'][:3])}

════════════════════════════════════════════════════
STANCE + GOAL SYNTHESIS RULES
════════════════════════════════════════════════════
Stance {stance} × Goal {gf['label']}:
{'→ TODAY IS ACTIVE. Move with the invitation. Speak with precision. Use planetary hour window: ' + peak_hour_window if stance == 'ADVANCE' else
 '→ TODAY IS PROTECTIVE. Hold ground. Do not open new negotiations. Prepare positions.' if stance == 'DEFEND' else
 '→ TODAY IS RESTRAINED. Opportunity exists but the risk of overreach is high. Observe, do not act.' if stance == 'RESTRAIN' else
 '→ TODAY IS A CLASH DAY. No irreversible commitments. Postpone, reschedule, preserve optionality.' if stance == 'AVOID' else
 '→ TODAY IS NEUTRAL. Routine work over bold moves. Build, do not pitch.'}

════════════════════════════════════════════════════
VARIATION DIRECTIVES  (generation #{generation_count})
════════════════════════════════════════════════════
Coaching angle    : {variation['angle']}
Communication lens: {variation['lens']}
Sentence style    : {variation['style']}
Tone register     : {variation['tone']}
Entry point       : {variation['entry']}
Angles to AVOID   : {', '.join(excluded_angles) or 'none yet'}

Generate fresh output. Do NOT reuse framing from previous sessions.
practical_tips MUST use the pre-computed colour, direction, and planetary hour — do not invent alternatives."""


def build_dialogue_prompt(
    profile_ctx: dict,
    goal_ctx: dict,
    coaching_output: dict,
    stance: str = "NEUTRAL",
    stance_th: str = "ปกติ",
) -> str:
    goal_slug = goal_ctx["goal_slug"]
    gf        = _GOAL_FOCUS.get(goal_slug, {"label": goal_slug.title(), "key_move": ""})
    seed_phrases = profile_ctx.get('scenario_sample_phrases', [])

    return f"""STANCE   : {stance} ({stance_th})  ← sentence register must match this stance
PROFILE  : {profile_ctx['mbti_code']} + {profile_ctx['hd_type_name']} + {profile_ctx['color_season']}
GOAL     : {gf['label']}
MBTI tone: {profile_ctx['mbti_communication_style']}
HD timing: {profile_ctx['hd_negotiation_entry']}
Color    : {profile_ctx['color_language_style']}

KEY MOVE FOR THIS GOAL: {gf['key_move']}

COACHING CONTEXT:
{coaching_output.get('behavior_recommendation', '')}
{coaching_output.get('communication_strategy', '')}

SEED PHRASES (inspiration only — rephrase completely, never copy):
{chr(10).join(f'  - {p}' for p in seed_phrases[:4])}

TASK:
Generate 4–5 sample sentences and 2–3 alternatives for {gf['label']} context.
ALL sentences must match STANCE = {stance}:
{'- Use assertive, frame-setting openers. Speak first where appropriate.' if stance == 'ADVANCE' else
 '- Use measured, protective language. Do not open new ground.' if stance == 'DEFEND' else
 '- Use patient, observational language. Do not claim or commit.' if stance == 'RESTRAIN' else
 '- Use deferral language. Gracefully postpone or reschedule.' if stance == 'AVOID' else
 '- Use steady, process-oriented language. No bold claims today.'}
- Each sentence must reflect MBTI tone + HD timing + Color language simultaneously.
- Sentences must be usable TODAY, not abstract.
- For MONEY goal: include one silence-trigger sentence (ends the ball in their court).
- For WORK goal: include one authority-frame sentence (establishes frame, not asks permission).
- For RELATIONSHIP goal: include one pacing sentence (follows their energy, not leads).
- Vary sentence length. Mix short punchy lines with one longer structured line."""
