"""Adaptive assessment branching engine.

All scoring and routing is done in pure Python against seeded DB data.
No AI/LLM calls happen here — the AI is only called once, at the end,
when POST /api/consult/{session_id}/generate-profile is invoked.

Flow per answer submission:
  1. Load current node + scoring rules from DB.
  2. Score the submitted answers (sum / mean / subscale logic).
  3. Collect any flags triggered by the scores.
  4. Determine next_node_id from cutoff rules.
  5. Persist answers + updated session state.
  6. Return next node payload for the frontend to render.
"""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy.orm import Session

from models.orm import (
    AssessmentAnswer,
    AssessmentNode,
    AssessmentOption,
    AssessmentProfile,
    AssessmentSession,
)

ENTRY_NODE = "L1_DOMAIN"


# ── Session helpers ───────────────────────────────────────────────────────────

def create_session(user_id: int, db: Session) -> AssessmentSession:
    session = AssessmentSession(
        user_id=user_id,
        current_node_id=ENTRY_NODE,
        flags_json="[]",
        scores_json="{}",
        visited_nodes_json="[]",
        status="in_progress",
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(session_id: int, user_id: int, db: Session) -> AssessmentSession:
    s = db.query(AssessmentSession).filter_by(id=session_id, user_id=user_id).first()
    if not s:
        raise ValueError("Session not found")
    return s


def _load_flags(session: AssessmentSession) -> list[str]:
    return json.loads(session.flags_json or "[]")


def _load_scores(session: AssessmentSession) -> dict:
    return json.loads(session.scores_json or "{}")


def _save_state(
    session: AssessmentSession,
    flags: list[str],
    scores: dict,
    visited: list[str],
    next_node_id: str,
    db: Session,
    done: bool = False,
) -> None:
    session.flags_json = json.dumps(flags)
    session.scores_json = json.dumps(scores)
    session.visited_nodes_json = json.dumps(visited)
    session.current_node_id = next_node_id
    if done:
        session.status = "completed"
    db.commit()


# ── Node payload builder ──────────────────────────────────────────────────────

def build_node_payload(node_id: str, db: Session) -> dict[str, Any]:
    """Return everything the frontend needs to render the next question screen."""
    node: AssessmentNode | None = db.get(AssessmentNode, node_id)
    if not node:
        raise ValueError(f"Node not found: {node_id}")

    payload: dict[str, Any] = {
        "node_id":       node.node_id,
        "node_type":     node.node_type,
        "instrument":    node.instrument,
        "label":         node.label,
        "rationale":     node.rationale,
        "evidence":      node.evidence,
        "trigger_warning": node.trigger_warning,
        "scale_labels":  json.loads(node.scale_labels_json)  if node.scale_labels_json  else None,
        "scale_values":  json.loads(node.scale_values_json)  if node.scale_values_json  else None,
        "questions":     [],
        "options":       [],
        "done":          node.node_type == "terminal",
    }

    for q in node.questions:
        payload["questions"].append({
            "question_id":    q.question_id,
            "text":           q.text,
            "subscale":       q.subscale,
            "reverse_scored": q.reverse_scored,
            "safety_item":    q.safety_item,
        })

    for o in node.options:
        payload["options"].append({
            "option_id": o.option_id,
            "label":     o.label,
        })

    return payload


# ── Answer submission & routing ───────────────────────────────────────────────

def submit_answers(
    session: AssessmentSession,
    node_id: str,
    answers: dict[str, float],   # {question_id: numeric_value}
    text_values: dict[str, str], # {question_id: display text}  — optional
    db: Session,
) -> dict[str, Any]:
    """
    Score answers for `node_id`, persist them, advance the session,
    and return the next node payload (or done=True with profile stub).
    """
    node: AssessmentNode | None = db.get(AssessmentNode, node_id)
    if not node:
        raise ValueError(f"Node not found: {node_id}")

    flags   = _load_flags(session)
    scores  = _load_scores(session)
    visited = json.loads(session.visited_nodes_json or "[]")

    # 1. Persist raw answers
    for qid, val in answers.items():
        db.add(AssessmentAnswer(
            session_id=session.id,
            node_id=node_id,
            question_id=qid,
            value=val,
            text_value=text_values.get(qid),
        ))

    # 2. Store node scores
    scores[node_id] = answers
    if node_id not in visited:
        visited.append(node_id)

    # 3. Route
    safety_triggered = _check_safety(node, answers)
    next_node_id, new_flags = _route(node, answers, db)
    flags.extend(f for f in new_flags if f not in flags)

    done = next_node_id == "GENERATE_PROFILE"
    _save_state(session, flags, scores, visited, next_node_id, db, done=done)
    db.commit()

    if done:
        profile_data = _compute_profile(scores, flags)
        summary      = generate_summary(profile_data)
        profile = AssessmentProfile(
            session_id=session.id,
            user_id=session.user_id,
            profile_json=json.dumps(profile_data),
            ai_summary=summary,
        )
        db.add(profile)
        db.commit()
        return {
            "done":             True,
            "safety_triggered": safety_triggered,
            "profile":          profile_data,
            "ai_summary":       summary,
        }

    payload = build_node_payload(next_node_id, db)
    payload["safety_triggered"] = safety_triggered
    return payload


# ── Scoring / routing internals ───────────────────────────────────────────────

def _check_safety(node: AssessmentNode, answers: dict[str, float]) -> bool:
    """Return True if any safety item (PHQ-9 item 9) was answered >= 1."""
    for q in node.questions:
        if q.safety_item and answers.get(q.question_id, 0) >= 1:
            return True
    return False


def _route(
    node: AssessmentNode,
    answers: dict[str, float],
    db: Session,
) -> tuple[str, list[str]]:
    """Return (next_node_id, new_flags) based on node type and scoring rules."""

    if node.node_type == "single_select":
        return _route_single_select(node, answers, db)

    rules: dict = json.loads(node.scoring_rules_json or "{}")

    if node.node_type in ("scale_set", "likert_set"):
        return _route_scored(node, answers, rules, db)

    if node.node_type == "checkbox_set":
        return _route_checkbox(node, answers, rules)

    # terminal — should not be submitted, but handle gracefully
    return "GENERATE_PROFILE", []


def _route_single_select(
    node: AssessmentNode,
    answers: dict[str, float],
    db: Session,
) -> tuple[str, list[str]]:
    # answers = {option_id: 1}
    selected_id = next((k for k, v in answers.items() if v == 1), None)
    if not selected_id:
        raise ValueError("No option selected for single_select node")

    opt: AssessmentOption | None = db.query(AssessmentOption).filter_by(
        node_id=node.node_id, option_id=selected_id
    ).first()
    if not opt:
        raise ValueError(f"Option {selected_id} not found in node {node.node_id}")

    next_id = opt.next_node_id or "GENERATE_PROFILE"
    new_flags = [opt.flag] if opt.flag else []
    return next_id, new_flags


def _route_scored(
    node: AssessmentNode,
    answers: dict[str, float],
    rules: dict,
    db: Session,
) -> tuple[str, list[str]]:
    """Handle sum/mean/subscale scoring and match against cutoff rules."""
    questions = {q.question_id: q for q in node.questions}
    flags: list[str] = []

    # ── Apply reverse scoring ─────────────────────────────────
    scale_values = json.loads(node.scale_values_json or "[]")
    scored: dict[str, float] = {}
    for qid, raw in answers.items():
        q = questions.get(qid)
        if q and q.reverse_scored and scale_values:
            min_v, max_v = min(scale_values), max(scale_values)
            scored[qid] = min_v + max_v - raw
        else:
            scored[qid] = raw

    # ── Compute aggregate stats ───────────────────────────────
    all_vals = list(scored.values())
    total = sum(all_vals)
    mean  = total / len(all_vals) if all_vals else 0

    # Subscale means
    subscale_means: dict[str, float] = {}
    for q in questions.values():
        if q.subscale:
            grp = subscale_means.setdefault(q.subscale, [])
            grp.append(scored.get(q.question_id, 0))  # type: ignore[arg-type]
    subscale_means = {k: sum(v) / len(v) for k, v in subscale_means.items()}  # type: ignore[assignment]

    # ── Per-item flags (YSQ schemas) ──────────────────────────
    if rules.get("per_item"):
        threshold = 4
        for q in questions.values():
            val = scored.get(q.question_id, 0)
            if val >= threshold and q.subscale:
                flag = f"schema_{q.subscale.lower().replace('/', '_').replace(' ', '_')}"
                if flag not in flags:
                    flags.append(flag)

    # ── Secondary shame/score-only cutoffs (no routing) ──────
    # Used by L4_SHAME to set shame flags independently of flag_routing.
    for range_str, flag_name in rules.get("shame_cutoffs", {}).items():
        if _is_range(range_str):
            lo, hi = map(int, range_str.split("-"))
            if lo <= total <= hi and flag_name and flag_name not in flags:
                flags.append(flag_name)

    # ── Collect next_node from score-based cutoffs ────────────
    cutoffs = rules.get("cutoffs", {})
    next_node = _match_cutoff(total, mean, subscale_means, cutoffs, flags)

    # ── Flag-based routing override (L4_SHAME → Q8_*) ────────
    # When scoring_rules contains flag_routing, accumulated session flags
    # (not score) decide which node comes next. Priority order is respected.
    flag_routing = rules.get("flag_routing")
    if flag_routing:
        next_node = _route_by_flags(flag_routing, flags)

    # ── Subscale-level flags (DERS, MBI, FMPS) ───────────────
    sub_flags = rules.get("subscale_flags", {})
    for flag_name, condition in sub_flags.items():
        if _eval_subscale_condition(condition, scored, subscale_means):
            if flag_name not in flags:
                flags.append(flag_name)

    return next_node or "GENERATE_PROFILE", flags


def _route_by_flags(routing: dict, session_flags: list[str]) -> str:
    """Select next node based on which session flags are set, in priority order.

    routing dict shape (from scoring_rules_json.flag_routing):
      {
        "priority": ["burnout_risk", "anxious_attachment", ...],
        "burnout_risk":       "Q8_BURNOUT",
        "anxious_attachment": "Q8_ATTACHMENT",
        ...
        "default": "Q8_DEFAULT"
      }
    """
    priority: list[str] = routing.get("priority", [])
    # Walk priority list first
    for flag in priority:
        if flag in session_flags and flag in routing:
            return routing[flag]
    # Fall back to any matching flag outside priority list
    for flag in session_flags:
        if flag in routing and flag != "priority" and flag != "default":
            return routing[flag]
    return routing.get("default", "GENERATE_PROFILE")


def _route_checkbox(
    node: AssessmentNode,
    answers: dict[str, float],
    rules: dict,
) -> tuple[str, list[str]]:
    count = sum(1 for v in answers.values() if v == 1)
    flags: list[str] = []
    cutoffs = rules.get("cutoffs", {})
    next_node = _match_cutoff(count, count, {}, cutoffs, flags)
    return next_node or "GENERATE_PROFILE", flags


def _match_cutoff(
    total: float,
    mean: float,
    subscale_means: dict[str, float],
    cutoffs: dict,
    flags: list[str],
) -> str | None:
    """Walk cutoff entries and return next_node for the first matching rule."""
    for key, rule in cutoffs.items():
        if not isinstance(rule, dict):
            continue
        condition = rule.get("condition", "")
        matched = _eval_condition(condition, total, mean, subscale_means)
        if matched or not condition:
            if "flag" in rule and rule["flag"] not in flags:
                flags.append(rule["flag"])
            return rule.get("next") or rule.get("next_node")
    return None


def _eval_condition(
    condition: str,
    total: float,
    mean: float,
    subscale_means: dict[str, float],
) -> bool:
    """Evaluate simple scoring conditions stored as strings.

    Supported forms:
      "0-4"               → total in range 0..4
      "mean >= 3.5"       → mean comparison
      "sum < 25"          → total alias
      "ace_count >= 4"    → treated as total
      Combined conditions are checked individually (first match wins in the loop).
    """
    c = condition.strip()
    if not c:
        return True

    # Range notation "0-4" or "10-14" (integers)
    if _is_range(c):
        lo, hi = map(int, c.split("-"))
        return lo <= total <= hi

    # Keyword comparisons — map to computed values
    replacements = {
        "mean": mean,
        "sum":  total,
        "ace_count": total,
        "count": total,
        "ratio": total,
    }
    # subscale means: e.g. "demands_mean >= 3 AND control_mean <= 2"
    for sk, sv in subscale_means.items():
        replacements[f"{sk}_mean"] = sv

    try:
        expr = c
        for name, val in sorted(replacements.items(), key=lambda x: -len(x[0])):
            expr = expr.replace(name, str(val))
        # Safe eval — only numbers and comparison operators
        expr = expr.replace(" AND ", " and ").replace(" OR ", " or ")
        return bool(eval(expr, {"__builtins__": {}}))  # noqa: S307
    except Exception:
        return False


def _is_range(s: str) -> bool:
    parts = s.split("-")
    return len(parts) == 2 and all(p.strip().lstrip("-").isdigit() for p in parts)


def _eval_subscale_condition(condition: str, scored: dict, subscale_means: dict) -> bool:
    """Evaluate DERS-style subscale flag conditions like 'DERS_1 + DERS_7 >= 6'."""
    try:
        expr = condition
        # Replace item IDs with their scored values
        for qid, val in sorted(scored.items(), key=lambda x: -len(x[0])):
            expr = expr.replace(qid, str(val))
        return bool(eval(expr, {"__builtins__": {}}))  # noqa: S307
    except Exception:
        return False


# ── Rule-based narrative summary (no AI, no API key) ─────────────────────────

def generate_summary(profile_data: dict) -> str:
    """Produce a warm, research-grounded narrative from the structured profile.

    Completely deterministic. No external calls. Generated once at completion
    and stored in assessment_profiles.ai_summary.

    Structure:
      Para 1 — Domain focus + overall mood / anxiety finding
      Para 2 — Domain-specific pattern (burnout / attachment / neglect / shame…)
      Para 3 — Core belief schema + shame level
      Para 4 — Inner resources (self-compassion, emotion regulation)
      Para 5 — Concrete next steps
    """
    flags    = profile_data.get("flags", [])
    p        = profile_data.get("profile", {})
    referral = profile_data.get("referral_recommended", False)

    def has(*f: str) -> bool:
        return any(x in flags for x in f)

    paras: list[str] = []

    # ── Para 1: Domain + mood screen ─────────────────────────────────────────
    # Scored flags are checked first (threshold crossed = confirmed finding).
    # Domain selection flags (domain_*) are the fallback when scoring threshold
    # was not crossed — the user's stated concern is always captured.
    domain_labels = {
        "burnout_risk":       "work stress and burnout",
        "anxious_attachment": "romantic relationships and attachment",
        "emotional_neglect":  "family and early emotional experiences",
        "low_self_esteem":    "self-worth and identity",
        "social_isolation":   "social connection and loneliness",
        "somatic_stress":     "stress showing up in your body",
        "financial_shame":    "money and financial shame",
        "domain_work":        "work and career",
        "domain_relationship":"romantic relationships",
        "domain_family":      "family dynamics",
        "domain_self":        "self-worth and inner world",
        "domain_friends":     "friendships and social connection",
        "domain_health":      "physical health and wellness",
        "domain_money":       "finances and money",
    }
    primary_domain = next(
        (domain_labels[f] for f in domain_labels if f in flags),
        "your inner world",
    )

    dep = p.get("depression_level", "none")
    anx = p.get("anxiety_level", "minimal")

    mood_parts: list[str] = []
    if dep == "moderate_to_severe":
        mood_parts.append("significant low mood and reduced interest in things you normally enjoy")
    elif dep == "mild":
        mood_parts.append("some low mood")

    if anx == "moderate_to_severe":
        mood_parts.append("elevated anxiety and worry that is hard to switch off")
    elif anx == "mild":
        mood_parts.append("some anxiety")

    if mood_parts:
        mood_str = " and ".join(mood_parts)
        paras.append(
            f"This assessment focused on {primary_domain}. "
            f"Alongside that, your responses show {mood_str}. "
            f"These feelings are real, and they make sense given what you are carrying. "
            f"They are also a signal — not a verdict on who you are."
        )
    else:
        paras.append(
            f"This assessment focused on {primary_domain}. "
            f"Your mood and anxiety screens came back in the normal range, "
            f"which suggests your current difficulty is more about ingrained patterns and chronic pressure "
            f"than a clinical mood episode — though patterns can be just as exhausting."
        )

    # ── Para 2: Domain-specific finding ──────────────────────────────────────
    domain_findings: list[str] = []

    if has("burnout_risk"):
        domain_findings.append(
            "In your work, you are showing clear signs of emotional exhaustion — "
            "what researchers call burnout. This is not weakness; it is what happens "
            "when demand chronically outpaces recovery. The research is clear: "
            "the body and mind eventually go into conservation mode, and pushing harder makes it worse, not better."
        )
    if has("anxious_attachment"):
        domain_findings.append(
            "In your relationships, you show an anxious attachment pattern — "
            "a heightened sensitivity to the possibility of abandonment or disconnection. "
            "This often develops when early closeness felt unpredictable or conditional. "
            "It can make relationships feel urgent or precarious even when they are not, "
            "and can drive behaviours (reassurance-seeking, monitoring, withdrawal) that create the very distance you fear."
        )
    if has("emotional_neglect"):
        domain_findings.append(
            "Your early family experiences suggest you may not have felt consistently seen "
            "or emotionally supported growing up. "
            "Emotional neglect — even without obvious mistreatment — leaves a quiet wound: "
            "a sense that your feelings don't fully matter, or that you must manage everything alone. "
            "This often shows up in adulthood as difficulty asking for help or trusting that support will come."
        )
    if has("low_self_esteem"):
        domain_findings.append(
            "You are carrying a tendency to see yourself as inadequate or as a failure. "
            "This is not an accurate picture of who you are — it is a learned lens, "
            "typically formed through early experiences of criticism, comparison, or love that felt conditional on performance."
        )
    if has("social_isolation"):
        domain_findings.append(
            "You described feeling lonely even when around others. "
            "This kind of emotional isolation — being physically present but not truly seen or connected — "
            "is one of the most painful human experiences, and one that quietly erodes wellbeing over time. "
            "The research on loneliness is striking: its health impact is comparable to smoking."
        )
    if has("financial_shame"):
        domain_findings.append(
            "Your financial stress is tangled with shame — a sense that your money situation "
            "reflects your worth as a person. Financial shame is extremely common and rarely spoken about. "
            "It tends to lead to avoidance, which amplifies the underlying problem. "
            "Separating your financial situation from your identity is one of the most important moves you can make."
        )
    if has("somatic_stress"):
        domain_findings.append(
            "Your stress is expressing itself physically — through tension, fatigue, digestive changes, "
            "or other somatic symptoms. This is the body's honest report: it is carrying more than it can process. "
            "The mind-body connection here is not metaphorical; it is well-documented physiologically."
        )

    # Soft domain findings — domain chosen in Q1 but scored threshold not crossed.
    # These ensure the user's stated concern always appears in the summary.
    if has("domain_work") and not has("burnout_risk"):
        domain_findings.append(
            "You identified work as your primary concern. "
            "While your burnout score sits below the clinical threshold right now, "
            "the fact that work is weighing on you is worth taking seriously — "
            "early warning signs often precede full burnout by months. "
            "Monitoring your energy, motivation, and cynicism levels is protective."
        )
    if has("domain_relationship") and not has("anxious_attachment"):
        domain_findings.append(
            "You flagged romantic relationships as your main area of concern. "
            "Your attachment anxiety score is currently below clinical range, "
            "which may reflect situational stress rather than a deep attachment pattern. "
            "Relational difficulties often sit at the intersection of current circumstance "
            "and earlier experiences of closeness — both are worth exploring."
        )
    if has("domain_family") and not has("emotional_neglect"):
        domain_findings.append(
            "You identified family as your primary concern. "
            "Family stress can operate through many channels — current conflict, "
            "unresolved relational dynamics, grief, or caregiving strain — "
            "without necessarily involving measurable early emotional neglect. "
            "If family dynamics are weighing on you, that weight is real regardless of its origin."
        )
    if has("domain_self") and not has("low_self_esteem"):
        domain_findings.append(
            "You identified your inner world and sense of self as your primary concern. "
            "This kind of self-inquiry is itself a sign of psychological awareness. "
            "The areas worth exploring further include your relationship to achievement, "
            "identity stability, and what gives your life meaning beyond external markers."
        )
    if has("domain_friends") and not has("social_isolation"):
        domain_findings.append(
            "You flagged friendships and social connection as an area of concern. "
            "Social wellbeing operates on both quantity and quality — "
            "you can have many connections and still feel a gap in deep, mutual understanding. "
            "The longing for more genuine connection is one of the most human experiences there is."
        )
    if has("domain_health") and not has("somatic_stress"):
        domain_findings.append(
            "You identified physical health as your primary concern. "
            "Chronic stress affects the body in ways that often precede clinical measurement thresholds — "
            "disrupted sleep, lowered immunity, tension, and fatigue. "
            "The concern itself is data worth acting on."
        )
    if has("domain_money") and not has("financial_shame"):
        domain_findings.append(
            "You identified finances as your primary area of concern. "
            "Financial stress is one of the most underrecognised sources of psychological burden. "
            "Even below the level of shame, financial anxiety — "
            "the background sense that money is precarious — "
            "consumes cognitive resources and quietly affects sleep, relationships, and decision-making."
        )

    if domain_findings:
        paras.append(domain_findings[0])

    # ── Para 3: Core belief pattern (schema) + shame ──────────────────────────
    schema_texts = {
        "unrelenting_standards": (
            "A key pattern emerging from your responses is what schema therapy calls Unrelenting Standards — "
            "a deeply held belief that you must perform at the highest level to be acceptable, to others or to yourself. "
            "This can drive achievement, but it means you can never quite rest or feel 'enough.' "
            "The bar keeps moving. Rest feels dangerous. And mistakes feel catastrophic rather than instructive."
        ),
        "abandonment": (
            "An Abandonment schema appears active — a core belief, usually formed early, "
            "that the people you love will eventually leave or let you down. "
            "This is not a rational fear you can argue yourself out of; it lives in the nervous system "
            "and shapes how you read other people's behaviour, often turning neutral signals into threats."
        ),
        "approval_seeking": (
            "An Approval-Seeking pattern is present — your sense of worth is closely tied to "
            "what others think of you. This can make it genuinely hard to know what you want "
            "(versus what others want from you), and makes saying no feel dangerous. "
            "It often begins in environments where love felt conditional on being pleasing, useful, or impressive."
        ),
        "maladaptive_perfectionism": (
            "Perfectionism is showing up in a self-critical way — where partial success registers as failure, "
            "and mistakes feel disproportionately large. "
            "This often begins as a protection (if I'm perfect, I'm safe from criticism) "
            "and becomes its own source of chronic anxiety, because perfection is never actually available."
        ),
        "emotional_inhibition": (
            "You tend to contain or suppress your emotions — holding feelings back "
            "because expressing them feels unsafe, inappropriate, or burdensome to others. "
            "This takes significant energy and often creates a background sense of emptiness or disconnection. "
            "Emotions suppressed tend to find other exits: physical tension, sudden overwhelm, or shutdown."
        ),
    }

    active_schemas = p.get("active_schemas", [])
    schema_para_parts: list[str] = []

    for schema in active_schemas:
        if schema in schema_texts:
            schema_para_parts.append(schema_texts[schema])
            break  # one schema per paragraph to keep readable

    shame_level = p.get("shame_level", "low")
    if shame_level == "high":
        schema_para_parts.append(
            "Alongside these patterns, you are carrying a significant level of shame — "
            "not guilt (which is about behaviour) but shame (which is about identity): "
            "a felt sense that something is fundamentally wrong with you as a person. "
            "Shame is one of the most painful and least-spoken-about human experiences. "
            "It is also highly responsive to the right kind of support."
        )
    elif shame_level == "moderate":
        schema_para_parts.append(
            "There is also a moderate level of shame present — a background sense of being flawed "
            "or not quite good enough. This often amplifies other difficulties and is worth addressing directly."
        )

    if schema_para_parts:
        paras.append(" ".join(schema_para_parts))

    # ── Para 4: Inner resources ───────────────────────────────────────────────
    resource_parts: list[str] = []

    scs = p.get("self_compassion_level", "moderate")
    er  = p.get("emotion_regulation_difficulty", "low")

    if scs == "low":
        resource_parts.append(
            "Your self-compassion is currently low — when things go wrong, "
            "your default is harshness toward yourself rather than the understanding you might offer a friend. "
            "Self-compassion is one of the most robustly evidenced protective factors in psychology: "
            "it predicts lower depression, lower anxiety, and greater resilience — "
            "more reliably than self-esteem."
        )
    elif scs == "moderate":
        resource_parts.append(
            "Your self-compassion is moderate — you have some capacity for self-kindness, "
            "but it is inconsistent, and may disappear precisely when you need it most. "
            "Strengthening it is one of the highest-leverage psychological investments you can make."
        )
    else:
        resource_parts.append(
            "Your self-compassion is a genuine strength — "
            "you can meet yourself with understanding during difficult times. "
            "This is one of the most important protective factors for long-term wellbeing "
            "and will serve you well as you work through the other areas identified here."
        )

    if has("poor_ER_strategies") or er == "high":
        resource_parts.append(
            "A significant finding is that when you are upset, you tend to believe nothing can help — "
            "a kind of emotional helplessness. Research shows this belief is itself the main obstacle: "
            "it closes down the search for regulation strategies before they are tried. "
            "Even a small, consistent toolkit of skills can break this pattern."
        )
    elif has("moderate_ER_difficulty") or er == "moderate":
        resource_parts.append(
            "You sometimes struggle to regulate your emotions when distress is high. "
            "This is something that responds well to consistent practice."
        )

    if resource_parts:
        paras.append(" ".join(resource_parts))

    # ── Para 5: Next steps ────────────────────────────────────────────────────
    steps: list[str] = []

    if referral or (has("phq2_elevated") and has("anxiety_elevated")):
        steps.append(
            "Given the levels identified, speaking with a licensed counsellor or psychotherapist "
            "is genuinely recommended — not as a last resort, but as the most efficient path. "
            "Early support consistently leads to better outcomes."
        )

    if active_schemas:
        steps.append(
            "The core belief patterns identified respond well to Schema Therapy, "
            "Compassion-Focused Therapy (CFT), or structured CBT — "
            "all have strong evidence bases and are available in individual or group formats."
        )

    if scs in ("low", "moderate"):
        steps.append(
            "Daily self-compassion practice — even 5 minutes — has shown measurable reductions "
            "in depression and anxiety in randomised trials. "
            "Kristin Neff's work (self-compassion.org) offers free, validated exercises."
        )

    if has("poor_ER_strategies", "moderate_ER_difficulty"):
        steps.append(
            "For emotion regulation, DBT skills — particularly TIPP (Temperature, Intense exercise, "
            "Paced breathing, Progressive relaxation) — are evidence-based and can be practised independently."
        )

    if has("burnout_risk"):
        steps.append(
            "For burnout: recovery requires genuine rest, not just shorter hours. "
            "The research on burnout recovery consistently shows that meaningful disconnection — "
            "not passive rest, but active recovery activities — restores the emotional reserves that work depletes."
        )

    if not steps:
        steps.append(
            "Your profile shows resilience. Continue paying attention to the patterns identified here — "
            "awareness is itself the beginning of change."
        )

    paras.append(
        "Some concrete directions based on your profile: "
        + " ".join(steps)
    )

    return "\n\n".join(paras)


# ── Profile compiler (pure Python — no AI) ───────────────────────────────────

def _compute_profile(scores: dict, flags: list[str]) -> dict:
    """Build the structured profile from collected flags and raw scores.

    The AI summary is added later when generate-profile is called.
    """
    def has(*f: str) -> bool:
        return any(x in flags for x in f)

    def score_val(node_id: str, qid: str) -> float:
        return scores.get(node_id, {}).get(qid, 0)

    # PHQ-2 + safety item
    phq2_total = score_val("L3_PHQ2", "PHQ_1") + score_val("L3_PHQ2", "PHQ_2")
    safety_score = score_val("L3_SAFETY", "PHQ_9")

    # GAD-2 total
    gad2_total = score_val("L3_GAD2", "GAD_1") + score_val("L3_GAD2", "GAD_2")

    # Domain-specific score (single item per L2 node)
    burnout_score    = score_val("L2_WORK",    "BURNOUT_1")
    attachment_score = score_val("L2_REL",     "ECR_AX1")
    neglect_raw      = score_val("L2_FAM",     "CTQ_EN3")  # reverse scored
    self_esteem_score= score_val("L2_SELF",    "RSES_9")
    loneliness_score = score_val("L2_FRIENDS", "UCLA_1")

    # Q7 shame score
    shame_score = score_val("L4_SHAME", "ISS_2")

    # Q9 self-compassion (single item, 1–5)
    scs_score = score_val("L5_SELF_COMPASSION", "SCS_SK1")

    # Q10 emotion regulation (single item, 1–5)
    er_score = score_val("L5_EMOTION_REG", "DERS_6")

    # Schema from Q8 (whichever variant was visited)
    q8_nodes = ["Q8_BURNOUT", "Q8_ATTACHMENT", "Q8_NEGLECT", "Q8_SHAME_SCHEMA", "Q8_DEFAULT"]
    schema_score: float = 0.0
    schema_node_visited: str = ""
    for q8 in q8_nodes:
        if q8 in scores:
            schema_score = next(iter(scores[q8].values()), 0)
            schema_node_visited = q8
            break

    def phq2_level() -> str:
        if phq2_total <= 1: return "none"
        if phq2_total <= 2: return "mild"
        return "moderate_to_severe"

    def gad2_level() -> str:
        if gad2_total <= 1: return "minimal"
        if gad2_total <= 2: return "mild"
        return "moderate_to_severe"

    def scs_level() -> str:
        if scs_score == 0:  return "not_assessed"
        if scs_score <= 2:  return "low"
        if scs_score <= 3:  return "moderate"
        return "high"

    def er_level() -> str:
        if er_score == 0:  return "not_assessed"
        if er_score <= 2:  return "low"
        if er_score <= 3:  return "moderate"
        return "high"

    referral = (
        phq2_total >= 3
        or gad2_total >= 3
        or safety_score >= 1
        or has("phq2_elevated") and has("anxiety_elevated")
    )

    # Active schemas — from Q8 flag + any per-item flags on L4_SHAME
    active_schemas = [f.replace("schema_", "") for f in flags if f.startswith("schema_")]
    schema_flag_map = {
        "Q8_BURNOUT":       "unrelenting_standards",
        "Q8_ATTACHMENT":    "abandonment",
        "Q8_NEGLECT":       "approval_seeking",
        "Q8_SHAME_SCHEMA":  "maladaptive_perfectionism",
        "Q8_DEFAULT":       "emotional_inhibition",
    }
    if schema_node_visited and schema_score >= 4:
        schema_label = schema_flag_map.get(schema_node_visited)
        if schema_label and schema_label not in active_schemas:
            active_schemas.append(schema_label)

    return {
        "flags": flags,
        "scores_summary": {
            "phq2_total":       round(phq2_total, 1),
            "gad2_total":       round(gad2_total, 1),
            "safety_item":      round(safety_score, 1),
            "domain_score":     round(burnout_score or attachment_score or neglect_raw or self_esteem_score or loneliness_score, 1),
            "shame_score":      round(shame_score, 1),
            "schema_score":     round(schema_score, 1),
            "schema_node":      schema_node_visited,
            "self_compassion":  round(scs_score, 1),
            "emotion_regulation": round(er_score, 1),
        },
        "profile": {
            "depression_level":               phq2_level(),
            "anxiety_level":                  gad2_level(),
            "safety_flag":                    safety_score >= 1,
            "self_compassion_level":          scs_level(),
            "emotion_regulation_difficulty":  er_level(),
            "attachment_style":               _attachment_style(flags),
            "active_schemas":                 active_schemas,
            "domain_flags": {
                "burnout_risk":       has("burnout_risk"),
                "anxious_attachment": has("anxious_attachment"),
                "emotional_neglect":  has("emotional_neglect"),
                "low_self_esteem":    has("low_self_esteem"),
                "social_isolation":   has("social_isolation"),
                "somatic_stress":     has("somatic_stress"),
                "financial_shame":    has("financial_shame"),
            },
            "shame_level":      "high" if has("high_shame") else ("moderate" if has("moderate_shame") else "low"),
            "need_for_approval": has("approval_seeking_schema"),
            "perfectionism":    has("maladaptive_perfectionism"),
            "poor_er_strategies": has("poor_ER_strategies"),
            "low_self_compassion": has("low_self_compassion"),
        },
        "referral_recommended": referral,
        "ai_summary": None,
        "disclaimer": (
            "This profile is based on validated self-report screening instruments only. "
            "It is not a clinical diagnosis. Please discuss results with a licensed "
            "mental health professional."
        ),
    }


def _attachment_style(flags: list[str]) -> str:
    if "fearful_attachment"    in flags: return "fearful"
    if "anxious_attachment"    in flags: return "preoccupied"
    if "avoidant_attachment"   in flags: return "dismissing"
    return "not_assessed"
