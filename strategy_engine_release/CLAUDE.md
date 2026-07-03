# CLAUDE.md — Boong Strategy Engine

This file provides guidance to Claude Code when working with this repository.

---

## Project Overview

### Product Vision

**Boong** is an AI-powered daily personality coaching engine.

It combines four personality/energy frameworks:

- **MBTI** — 16 types, cognitive stack, decision style, communication preference
- **Human Design** — 5 types (Manifestor, Generator, Manifesting Generator, Projector, Reflector) with strategy + authority
- **Personal Color** — 4 seasons (Spring, Summer, Autumn, Winter) with energy tone + language style
- **BaZi (四柱推命)** — Day master + day pillar computed from birth data for daily timing score

to generate **fresh, personalized daily coaching** that feels different every session — including behavioral guidance, communication strategy, timing recommendations, and sample sentences.

This is **NOT** a personality test app.
This is **NOT** a horoscope app.

This is an **AI coaching engine** that uses personality data as context to produce **actionable daily guidance**.

---

### Core User Flow

1. User registers + enters birth data, MBTI, Human Design type, Personal Color
2. User selects today's goal (e.g. Business Negotiation, Leadership, Dating)
3. System computes BaZi day score + action multiplier
4. AI agent pipeline assembles profile context → goal context → coaching → sample sentences
5. User receives: behavior recommendation, timing guidance, communication strategy, warnings, 3–5 sample sentences, 2–3 alternatives
6. User rates output → feedback stored → informs future variation

Every generation for the same profile + goal must feel **different**. Repetition is a bug.

---

### Example Output

**Profile:** ENTJ + Projector + Winter

**Goal:** Business Negotiation

```
Behavior Recommendation:
As an ENTJ Projector, your power is strategic recognition — not volume.
Let the other party open. Wait for an invitation before delivering your core position.
When recognized, speak with precision.

Timing Guidance:
Projectors should avoid initiating. Let them raise the issue first.
Today's BaZi action score: 7.2/10 — favorable for decisive moves after 2pm.

Communication Style (Winter energy):
Lead with structure and depth. Avoid overly warm or casual framing.
Use declarative sentences. End with a question that returns control to them.

Sample Sentences:
1. "Based on what you've outlined, here's the structure I'd propose..."
2. "I want to make sure this works for both sides — what's the constraint I should know about?"
3. "Let me summarize what I'm hearing, then offer an alternative framing."
4. "Before we finalize, I'd like to understand your priority — timeline or scope?"
5. "Here's where I see mutual value, and here's where I need clarity from you."

Warnings:
- Don't rush to fill silence. Projectors who over-talk lose authority.
- Avoid vague language — ENTJ + Winter energy requires precision to land.
- Don't initiate the close. Let them signal readiness first.
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Runtime | Python 3.11+ |
| Framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (dev) / MySQL (prod) |
| Auth | JWT (bcrypt + python-jose) |
| AI | OpenAI API (GPT-4o) |
| Validation | Pydantic v2 |
| Testing | pytest |
| Server | uvicorn |

---

## Commands

All commands run from `strategy_engine_release/`.

```bash
# First-time setup
pip install -r requirements.txt
cp .env.example .env          # DATABASE_URL defaults to SQLite

# Seed DB — personality dictionaries, criteria, scenarios, personal color
python seed.py                # idempotent — skips existing rows
python seed.py --reset        # wipe criteria/profile tables and re-seed
python seed.py --migrate --reset  # adds missing columns then re-seeds (schema upgrade)

# Run server
uvicorn main:app --reload     # http://localhost:8000/docs

# Tests
pytest tests/test_intj_projector.py -v            # full test suite
pytest tests/test_intj_projector.py -v -k "Scenario"  # single class
pytest tests/ -v                                   # all tests
```

---

## Directory Structure

```
strategy_engine_release/
├── main.py                    # FastAPI app, router registration, startup
├── seed.py                    # Source of truth for all DB content
├── requirements.txt
├── .env.example
│
├── api/                       # Route handlers only — no business logic
│   ├── auth.py                # POST /signup, POST /login
│   ├── daily.py               # POST /api/daily-calc (main endpoint)
│   ├── profile.py             # GET/PUT /api/profile
│   ├── goals.py               # GET /api/goals
│   ├── recommendations.py     # GET /api/recommendations, POST /feedback
│   ├── mbti_types.py          # GET /api/mbti-types, /api/mbti-types/{code}
│   ├── hd_types.py            # GET /api/hd-types, /api/hd-types/{type}
│   └── color_types.py         # GET /api/color-types, /api/color-types/{season}
│
├── agents/                    # AI orchestration layer
│   ├── pipeline.py            # Runs 4-agent sequence
│   ├── profile_agent.py       # Agent 1: build unified profile context
│   ├── goal_agent.py          # Agent 2: activate goal-specific context
│   ├── coaching_agent.py      # Agent 3: generate behavior + strategy
│   └── dialogue_agent.py      # Agent 4: generate sample sentences
│
├── prompts/                   # Prompt templates and builders
│   ├── system/
│   │   ├── profile_agent.py
│   │   ├── coaching_agent.py
│   │   └── dialogue_agent.py
│   └── builders/
│       ├── build_profile_prompt.py
│       ├── build_goal_prompt.py
│       ├── build_coaching_prompt.py
│       └── build_dialogue_prompt.py
│
├── services/                  # Business logic + DB queries
│   ├── criteria.py            # get_mbti_decisions(), get_hd_decisions(), get_scenario()
│   ├── scoring.py             # BaZi + MBTI + HD score multipliers (stub → production)
│   ├── saju.py                # BaZi chart: day master + day pillar from birth data (stub)
│   ├── multipliers.py         # Score multiplier tables (stub)
│   ├── elements.py            # BaZi element relationships (stub)
│   ├── color_service.py       # Personal Color data queries
│   ├── recommendation_service.py  # Save/load recommendations
│   └── memory_service.py      # Agent memories: track used strategies
│
├── models/                    # SQLAlchemy ORM models
│   ├── user.py
│   ├── profile.py
│   ├── criteria.py
│   ├── scenario.py
│   ├── type_profiles.py       # mbti_type_profiles, hd_type_profiles, personal_color_profiles
│   ├── recommendation.py
│   └── memory.py
│
├── schemas/                   # Pydantic request/response schemas
│   ├── auth.py
│   ├── profile.py
│   ├── daily.py
│   └── recommendation.py
│
├── core/
│   ├── deps.py                # get_current_user dependency
│   ├── database.py            # engine, SessionLocal, Base
│   └── config.py              # Settings from .env
│
└── tests/
    ├── test_intj_projector.py
    ├── test_agents.py
    ├── test_criteria.py
    └── test_variation.py
```

---

## Database Schema

### Source of Truth

**All content lives in `seed.py`.** To change coaching data, decision rules, or profiles: edit the seed list, run `python seed.py --reset`. The next API call returns updated content immediately.

Tables are auto-created by `Base.metadata.create_all()` on app startup. No Alembic.

---

### Personality Dictionary Tables

These are seeded once. They are the knowledge base the AI agents pull from.

---

#### `mbti_type_profiles`

1 row per MBTI type (16 rows total). ~50 fields.

| Column | Type | Description |
|---|---|---|
| `type_code` | TEXT PK | e.g. `"ENTJ"` |
| `type_name` | TEXT | e.g. `"The Commander"` |
| `cognitive_stack` | TEXT | Pipe-separated: `"Te\|Ni\|Se\|Fi"` |
| `population_pct` | REAL | e.g. `1.8` |
| `core_traits` | TEXT | Pipe-separated trait list |
| `communication_style` | TEXT | e.g. `"direct, structured, goal-first"` |
| `decision_pattern` | TEXT | e.g. `"logic-first, data-driven, fast closure"` |
| `decision_under_pressure` | TEXT | How decision style shifts under stress |
| `negotiation_style` | TEXT | e.g. `"assertive, anchor-first, goal-anchored"` |
| `negotiation_entry` | TEXT | How to open a negotiation |
| `negotiation_concession` | TEXT | How to handle pushback |
| `negotiation_close` | TEXT | How to close |
| `stress_trigger` | TEXT | What causes stress response |
| `stress_behavior` | TEXT | How they behave under stress |
| `stress_warning_signs` | TEXT | Pipe-separated early warning signals |
| `stress_recovery` | TEXT | Recovery strategy |
| `blind_spots` | TEXT | Pipe-separated: `"ignores emotional signals\|over-plans"` |
| `strengths` | TEXT | Pipe-separated |
| `weaknesses` | TEXT | Pipe-separated |
| `career_patterns` | TEXT | Pipe-separated |
| `language_tone` | TEXT | e.g. `"declarative, assertive, minimal filler"` |
| `sample_openers` | TEXT | Pipe-separated opener templates |
| `sample_closers` | TEXT | Pipe-separated closing templates |
| `coaching_notes` | TEXT | Additional AI coaching context |

> List fields stored as pipe-separated strings `"A | B | C"`. Frontend splits on `" | "`.

---

#### `hd_type_profiles`

1 row per Human Design type (5 rows total). ~17 fields.

| Column | Type | Description |
|---|---|---|
| `type_name` | TEXT PK | `"Manifestor"` / `"Generator"` / `"Manifesting Generator"` / `"Projector"` / `"Reflector"` |
| `strategy` | TEXT | e.g. `"Wait for the invitation"` |
| `authority_types` | TEXT | Pipe-separated: `"Emotional\|Splenic\|Mental"` |
| `energy_type` | TEXT | `"initiating"` / `"responding"` / `"waiting"` |
| `aura_description` | TEXT | e.g. `"Focused and absorbing"` |
| `negotiation_timing` | TEXT | When to engage vs. wait in negotiation |
| `negotiation_entry` | TEXT | Ideal entry point in a conversation |
| `communication_role` | TEXT | e.g. `"guide when recognized, not initiator"` |
| `common_mistakes` | TEXT | Pipe-separated: `"initiating without recognition\|over-explaining"` |
| `ideal_conditions` | TEXT | When this type performs best |
| `coaching_notes` | TEXT | Additional AI coaching context |

---

#### `personal_color_profiles`

1 row per Personal Color season (4 rows total). **New table — add to seed.py.**

| Column | Type | Description |
|---|---|---|
| `season` | TEXT PK | `"Spring"` / `"Summer"` / `"Autumn"` / `"Winter"` |
| `sub_types` | TEXT | Pipe-separated: `"True Winter\|Soft Winter\|Bright Winter"` |
| `energy_tone` | TEXT | `"warm-light"` / `"cool-muted"` / `"warm-deep"` / `"cool-clear"` |
| `impression` | TEXT | Pipe-separated: `"authoritative\|elegant\|intense"` |
| `communication_vibe` | TEXT | e.g. `"depth and authority over warmth"` |
| `language_style` | TEXT | e.g. `"declarative, structured, minimal small talk"` |
| `best_colors` | TEXT | Pipe-separated presentation palette |
| `avoid_styles` | TEXT | Pipe-separated: what clashes with this color energy |
| `social_energy` | TEXT | e.g. `"commanding presence, few words land harder"` |
| `coaching_notes` | TEXT | Additional AI coaching context |

---

### Criteria Tables

These drive the actual `/api/daily-calc` response. Goal-filtered decision rules.

---

#### `mbti_criteria`

MBTI type → preference → decision rule (goal-aware).

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK |  |
| `mbti_type` | TEXT | e.g. `"ENTJ"` |
| `preference` | TEXT | e.g. `"decision"` / `"communication"` / `"stress"` |
| `decision_rule` | TEXT | The coaching rule text |
| `goal` | TEXT NULL | `NULL` = general / `"work"` / `"money"` / `"relationship"` |
| `weight` | REAL | Scoring weight (0.0–1.0) |
| `variation_angle` | TEXT NULL | Coaching angle tag: `"timing-first"` / `"behavior-first"` / `"warning-first"` |

Each MBTI type has:
- 3 general rows (`goal IS NULL`)
- 3 goal-specific rows per goal context (`work` / `money` / `relationship`)

---

#### `hd_criteria`

HD type → preference → decision rule (goal-aware). Same structure as `mbti_criteria`.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK |  |
| `hd_type` | TEXT | e.g. `"Projector"` |
| `preference` | TEXT | e.g. `"timing"` / `"entry"` / `"communication"` |
| `decision_rule` | TEXT | The coaching rule text |
| `goal` | TEXT NULL | `NULL` = general / goal-specific |
| `weight` | REAL | Scoring weight |
| `variation_angle` | TEXT NULL | Coaching angle tag |

---

#### `mbti_hd_scenarios`

80 rows (16 MBTI × 5 HD). The blend/conflict table — most important for AI context.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK |  |
| `mbti_type` | TEXT | e.g. `"ENTJ"` |
| `hd_type` | TEXT | e.g. `"Projector"` |
| `blend_summary` | TEXT | How these two types amplify each other |
| `conflict_summary` | TEXT | Where these two types create internal tension |
| `negotiation_recommendation` | TEXT | Combined negotiation strategy |
| `communication_recommendation` | TEXT | Combined communication strategy |
| `timing_recommendation` | TEXT | When to act, when to wait |
| `sample_phrases` | TEXT | Pipe-separated phrase seeds (AI uses as inspiration, not templates) |
| `warnings` | TEXT | Pipe-separated: what this combo tends to get wrong |
| `coaching_notes` | TEXT | Additional synthesis notes |

---

### Operational Tables

---

#### `users`

Auth credentials.

| Column | Type |
|---|---|
| `id` | INTEGER PK |
| `email` | TEXT UNIQUE |
| `hashed_password` | TEXT |
| `created_at` | DATETIME |

---

#### `user_profiles`

One per user. Personality configuration.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK |  |
| `user_id` | INTEGER FK → users |  |
| `mbti_type` | TEXT | e.g. `"ENTJ"` |
| `hd_type` | TEXT | e.g. `"Projector"` |
| `personal_color` | TEXT | e.g. `"Winter"` |
| `birth_date` | DATE | For BaZi computation |
| `birth_time` | TIME NULL | Optional — improves BaZi precision |
| `blood_type` | TEXT NULL | Optional |
| `onboarding_complete` | BOOLEAN | Default false |
| `created_at` | DATETIME |  |
| `updated_at` | DATETIME |  |

---

#### `recommendations`

Generated coaching outputs.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK |  |
| `user_id` | INTEGER FK → users |  |
| `goal` | TEXT | Goal slug at time of generation |
| `variation_seed` | TEXT | Seed used to drive variation |
| `variation_angle` | TEXT | Which angle was selected |
| `bazi_score` | REAL | Action score at time of generation |
| `behavior_recommendation` | TEXT |  |
| `timing_guidance` | TEXT |  |
| `communication_strategy` | TEXT |  |
| `warnings` | TEXT | Pipe-separated |
| `sample_sentences` | TEXT | Pipe-separated (3–5) |
| `alternative_responses` | TEXT | Pipe-separated (2–3) |
| `coaching_summary` | TEXT |  |
| `generation_model` | TEXT | e.g. `"gpt-4o"` |
| `generation_ms` | INTEGER | Latency in ms |
| `created_at` | DATETIME |  |

---

#### `recommendation_feedback`

User ratings.

| Column | Type |
|---|---|
| `id` | INTEGER PK |
| `recommendation_id` | INTEGER FK → recommendations |
| `user_id` | INTEGER FK → users |
| `rating` | INTEGER (1–5) |
| `feedback_text` | TEXT NULL |
| `created_at` | DATETIME |

---

#### `agent_memories`

Tracks used strategies per user to prevent repetition. Expires after 30 days.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK |  |
| `user_id` | INTEGER FK → users |  |
| `memory_type` | TEXT | `"used_angle"` / `"used_sentence_pattern"` / `"used_strategy"` |
| `content` | TEXT | The strategy or pattern that was used |
| `goal_context` | TEXT NULL | Which goal it was used for |
| `created_at` | DATETIME |  |
| `expires_at` | DATETIME | `created_at + 30 days` |

---

## Request Flow — `/api/daily-calc`

```
POST /api/daily-calc
    │
    ├─ 1. Auth: validate JWT → resolve user + profile
    ├─ 2. BaZi: saju.py computes day master + day pillar from birth data
    ├─ 3. Score: scoring.py combines BaZi + MBTI + HD multipliers → action_score
    │
    ├─ 4. DB Queries:
    │      criteria.get_mbti_decisions(mbti_type, goal)
    │      criteria.get_hd_decisions(hd_type, goal)
    │      criteria.get_scenario(mbti_type, hd_type)
    │      color_service.get_color_profile(personal_color)
    │      memory_service.get_active_memories(user_id)  ← exclude used angles
    │
    └─ 5. AI Pipeline: agents/pipeline.py
               │
               ├─ Agent 1: Profile Agent
               ├─ Agent 2: Goal Agent
               ├─ Agent 3: Coaching Agent
               └─ Agent 4: Dialogue Agent
                         │
                         └─ Response assembled + saved to recommendations table
```

> `saju.py`, `scoring.py`, `multipliers.py`, `elements.py` are currently placeholder stubs.
> Core production logic lives in the DB-driven criteria, scenario, and AI agent layers.

---

## Goal-Aware Criteria Queries

`criteria.py` applies a consistent pattern:

```python
# goal=None → only rows where goal IS NULL (general rules)
get_mbti_decisions(mbti_type="ENTJ", goal=None)

# goal='work' → goal IS NULL OR goal='work'
get_mbti_decisions(mbti_type="ENTJ", goal="work")
```

Each MBTI/HD type has:
- 3 general rows (`goal IS NULL`)
- 3 goal-specific rows per goal context (`work` / `money` / `relationship`)

---

## AI Agent Architecture

### Overview

4 agents run in sequence. Each agent reads the shared state and writes its output back.

```
[Agent 1: Profile Agent]
    ↓ ProfileContext
[Agent 2: Goal Agent]
    ↓ GoalContext
[Agent 3: Coaching Agent]
    ↓ CoachingOutput
[Agent 4: Dialogue Agent]
    ↓ DialogueOutput
→ Final recommendation assembled
```

---

### Agent 1: Profile Agent

**File:** `agents/profile_agent.py`

**Purpose:** Build unified personality context from all three frameworks.

**Inputs:**
- `mbti_type_profiles` row for user's MBTI type
- `hd_type_profiles` row for user's HD type
- `personal_color_profiles` row for user's color season
- `mbti_hd_scenarios` row for this MBTI × HD combo
- `agent_memories` for this user — recently used angles to exclude

**Process:**
1. Load all personality dictionary data from DB
2. Cross-reference `mbti_hd_scenarios` for blend + conflict
3. Check `agent_memories` — identify excluded angles
4. Select variation angle (see Randomization Rules)
5. Build `ProfileContext` object

**Output:**

```python
@dataclass
class ProfileContext:
    mbti_code: str                   # "ENTJ"
    mbti_core_traits: list[str]
    mbti_communication_style: str
    mbti_decision_pattern: str
    mbti_negotiation_style: str
    mbti_blind_spots: list[str]
    mbti_sample_openers: list[str]

    hd_type_name: str                # "Projector"
    hd_strategy: str                 # "Wait for the invitation"
    hd_energy_type: str
    hd_negotiation_timing: str
    hd_negotiation_entry: str
    hd_common_mistakes: list[str]

    color_season: str                # "Winter"
    color_communication_vibe: str
    color_language_style: str
    color_impression: list[str]

    scenario_blend: str              # from mbti_hd_scenarios
    scenario_conflict: str
    scenario_sample_phrases: list[str]  # phrase seeds only — AI will rephrase

    variation_angle: str             # selected for this generation
    excluded_angles: list[str]       # from agent_memories
```

---

### Agent 2: Goal Agent

**File:** `agents/goal_agent.py`

**Purpose:** Load goal-specific coaching context.

**Inputs:**
- Goal slug (e.g. `"work"`, `"money"`, `"relationship"`)
- `ProfileContext` from Agent 1
- `mbti_criteria` rows for this MBTI + goal
- `hd_criteria` rows for this HD type + goal

**Output:**

```python
@dataclass
class GoalContext:
    goal_slug: str
    goal_label: str
    mbti_decisions: list[CriteriaRow]
    hd_decisions: list[CriteriaRow]
    scenario: ScenarioRow
    coaching_focus_areas: list[str]  # e.g. ["timing", "assertiveness", "listening"]
```

---

### Agent 3: Coaching Agent

**File:** `agents/coaching_agent.py`

**Purpose:** Generate behavior, timing, communication strategy, and warnings.

**Inputs:**
- `ProfileContext`
- `GoalContext`
- `bazi_score` (from scoring.py)
- `variation_seed` (random string injected per request)

**Process:**
1. Build coaching prompt via `prompts/builders/build_coaching_prompt.py`
2. Inject variation directives (angle, lens, tone — see Randomization Rules)
3. Call OpenAI API
4. Parse and validate response with Pydantic
5. Record used angle in `agent_memories`

**Output:**

```python
@dataclass
class CoachingOutput:
    behavior_recommendation: str
    timing_guidance: str
    communication_strategy: str
    warnings: list[str]
    coaching_summary: str
    variation_angle_used: str
```

---

### Agent 4: Dialogue Agent

**File:** `agents/dialogue_agent.py`

**Purpose:** Generate sample sentences and alternative responses.

**Inputs:**
- `ProfileContext` (including `scenario_sample_phrases` as seeds)
- `GoalContext`
- `CoachingOutput`

**Process:**
1. Load phrase seeds from `scenario_sample_phrases` and `mbti_criteria.sample_openers`
2. Instruct model: use seeds as **inspiration only** — rephrase, do not copy
3. Generate 3–5 sample sentences matching goal + MBTI tone + color energy
4. Generate 2–3 alternative phrasings for different scenarios within same goal
5. Check `agent_memories` — avoid sentence patterns used in last 5 generations

**Output:**

```python
@dataclass
class DialogueOutput:
    sample_sentences: list[str]       # 3–5
    alternative_responses: list[str]  # 2–3
    sentence_notes: list[str]         # brief "when to use this" per sentence
```

---

## Randomization Rules

**Repetition is a bug.** Every generation for the same profile + goal must produce different output.

### Variation Dimensions

Each generation randomly selects across 5 dimensions:

| Dimension | Options |
|---|---|
| Coaching Angle | `timing-first` / `behavior-first` / `language-first` / `warning-first` |
| Communication Lens | `mbti-dominant` / `hd-dominant` / `color-dominant` / `balanced` |
| Sentence Style | `declarative` / `interrogative` / `assertive-open` / `collaborative` |
| Tone Register | `direct` / `measured` / `analytical` / `empathetic-strategic` |
| Entry Point | `open-with-context` / `open-with-recommendation` / `open-with-question` |

### Implementation

```python
import random, hashlib

def generate_variation_seed(user_id: int, timestamp: str) -> str:
    return hashlib.md5(f"{user_id}-{timestamp}".encode()).hexdigest()

def select_variation(seed: str, excluded_angles: list[str]) -> dict:
    rng = random.Random(seed)
    angles = ["timing-first", "behavior-first", "language-first", "warning-first"]
    available = [a for a in angles if a not in excluded_angles]
    return {
        "angle": rng.choice(available),
        "lens": rng.choice(["mbti-dominant", "hd-dominant", "color-dominant", "balanced"]),
        "style": rng.choice(["declarative", "interrogative", "assertive-open", "collaborative"]),
        "tone": rng.choice(["direct", "measured", "analytical", "empathetic-strategic"]),
        "entry": rng.choice(["open-with-context", "open-with-recommendation", "open-with-question"]),
    }
```

### Variation Prompt Directive

Inject into every coaching prompt:

```
This is generation #{n} for this user profile.
Coaching angle for this session: {angle}
Communication lens: {lens}
Sentence style: {style}
Tone register: {tone}
Entry point: {entry}

Previously used angles for this user: {excluded_angles}
Do NOT use any of the above angles or sentence patterns.

Even if the profile and goal are identical to a past session,
vary your approach, examples, framing, and sentence structures.
Output must feel fresh and context-aware.
```

### Memory Management

```python
# After successful generation, record used angle
memory_service.record(
    user_id=user_id,
    memory_type="used_angle",
    content=variation_angle_used,
    goal_context=goal_slug,
    expires_at=datetime.utcnow() + timedelta(days=30)
)

# Clean expired memories on each request
memory_service.purge_expired(user_id)
```

---

## Prompt Architecture

### System Prompts

```
prompts/system/profile_agent.py    # How to synthesize 3 frameworks into unified context
prompts/system/coaching_agent.py   # Output structure, variation rules, forbidden language
prompts/system/dialogue_agent.py   # Sentence generation rules, seed usage policy
```

### Prompt Builders

```
prompts/builders/build_profile_prompt.py    # Takes ProfileContext → prompt string
prompts/builders/build_goal_prompt.py       # Takes GoalContext → prompt string
prompts/builders/build_coaching_prompt.py   # Takes both + variation → full prompt
prompts/builders/build_dialogue_prompt.py   # Takes CoachingOutput + seeds → prompt
```

**Rules for prompt builders:**
- Never hardcode personality data — always pull from context objects
- Always inject variation directives
- Produce fully formed prompt strings ready for OpenAI API call
- Keep system prompt and user prompt separate

---

## API Endpoints

### Auth

| Method | Path | Description |
|---|---|---|
| POST | `/signup` | Register new user |
| POST | `/login` | Get JWT token |

---

### Profile

| Method | Path | Description |
|---|---|---|
| GET | `/api/profile` | Get current user profile |
| PUT | `/api/profile` | Update MBTI, HD type, Personal Color, birth data |

**PUT body:**
```json
{
  "mbti_type": "ENTJ",
  "hd_type": "Projector",
  "personal_color": "Winter",
  "birth_date": "1990-04-15",
  "birth_time": "14:30"
}
```

---

### Daily Coaching

| Method | Path | Description |
|---|---|---|
| POST | `/api/daily-calc` | Generate full coaching recommendation |

**POST body:**
```json
{
  "goal": "work"
}
```

**Response:**
```json
{
  "id": 42,
  "bazi_score": 7.2,
  "behavior_recommendation": "...",
  "timing_guidance": "...",
  "communication_strategy": "...",
  "warnings": ["...", "..."],
  "sample_sentences": ["...", "...", "..."],
  "alternative_responses": ["...", "..."],
  "coaching_summary": "..."
}
```

---

### Reference Data

| Method | Path | Description |
|---|---|---|
| GET | `/api/goals` | List available goals |
| GET | `/api/mbti-types` | List all MBTI type profiles |
| GET | `/api/mbti-types/{type_code}` | Single MBTI profile (case-insensitive) |
| GET | `/api/hd-types` | List all HD type profiles |
| GET | `/api/hd-types/{hd_type}` | Single HD type profile |
| GET | `/api/color-types` | List all Personal Color profiles |
| GET | `/api/color-types/{season}` | Single Personal Color profile |

---

### Feedback

| Method | Path | Description |
|---|---|---|
| POST | `/api/recommendations/{id}/feedback` | Submit rating (1–5) |

**POST body:**
```json
{
  "rating": 4,
  "feedback_text": "Good timing advice but sentences felt similar to yesterday"
}
```

---

## Auth Flow

JWT tokens issued on signup/login via `api/auth.py`.

All protected endpoints use `get_current_user` dependency (`core/deps.py`):
- Validates Bearer token
- Returns `User` ORM object with `profile` relationship eagerly loaded
- **Never trust client-provided user IDs** — always resolve from token

---

## Content vs. Criteria Tables

| Table type | Tables | Purpose |
|---|---|---|
| **Criteria** | `mbti_criteria`, `hd_criteria` | Actionable decision rules returned by `/daily-calc`, weighted and goal-filtered |
| **Reference** | `mbti_type_profiles`, `hd_type_profiles`, `personal_color_profiles` | Static profiles served by read-only type endpoints |
| **Scenario** | `mbti_hd_scenarios` | Cross-type blend/conflict context — primary AI input |
| **Operational** | `users`, `user_profiles`, `recommendations`, `recommendation_feedback`, `agent_memories` | Runtime data |

---

## Seed Data — `seed.py`

### Seed Lists

```python
MBTI_PROFILES_SEED   # 16 rows — mbti_type_profiles
HD_PROFILES_SEED     # 5 rows — hd_type_profiles
COLOR_PROFILES_SEED  # 4 rows — personal_color_profiles  ← ADD THIS
MBTI_SEED            # mbti_criteria rows (general + goal-specific)
HD_SEED              # hd_criteria rows (general + goal-specific)
SCENARIO_SEED        # 80 rows — mbti_hd_scenarios
```

### Adding New Coaching Content

1. Edit the relevant seed list in `seed.py`
2. Run `python seed.py --reset`
3. Next API call returns updated content

### Adding a New Column

1. Add column to ORM model in `models/`
2. Add column to seed list
3. Run `python seed.py --migrate --reset`

### Variation Angle Tags on Criteria Rows

Each `mbti_criteria` and `hd_criteria` row can have a `variation_angle` tag:

```python
{"mbti_type": "ENTJ", "preference": "timing", "decision_rule": "...", "goal": "work",
 "weight": 0.8, "variation_angle": "timing-first"}
```

Agent 3 selects criteria rows matching the chosen angle. This ties DB content to the variation system.

---

## Safety Rules

Do NOT modify without explicit approval:

| Area | Location |
|---|---|
| Auth dependency | `core/deps.py` |
| JWT logic | `api/auth.py` |
| System prompts | `prompts/system/` |
| BaZi computation | `services/saju.py` |
| Score multipliers | `services/multipliers.py` |

If changes are required: **STOP. Explain impact. Request approval.**

---

## Security Rules

- Never commit `.env` or `.env.local`
- Never expose `OPENAI_API_KEY` or `DATABASE_URL` to client responses
- All `/api/` endpoints except `/signup` and `/login` require valid JWT
- Never trust client-provided `user_id` — always use `get_current_user`
- CORS is currently `allow_origins=["*"]` — **tighten to real frontend domain before deploying**
- Never log passwords, tokens, or personal identification data
- Do not send unnecessary PII to OpenAI — send only data required for recommendation

---

## Environment

| Var | Description |
|---|---|
| `DATABASE_URL` | SQLite (default: `sqlite:///strategy_engine.db`) or MySQL (prod) |
| `OPENAI_API_KEY` | Required for AI agent pipeline |
| `SECRET_KEY` | JWT signing secret |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Default: `1440` (24h) |

---

## Testing

### Run Tests

```bash
pytest tests/ -v                                        # all tests
pytest tests/test_intj_projector.py -v                  # INTJ Projector suite
pytest tests/test_intj_projector.py -v -k "Scenario"    # scenario class only
pytest tests/test_agents.py -v                          # agent pipeline tests
pytest tests/test_variation.py -v                       # randomization tests
```

### Required Test Coverage

| Area | Test File |
|---|---|
| MBTI × HD scenario combos | `test_intj_projector.py` (extend for all combos) |
| Agent pipeline (unit) | `test_agents.py` |
| Criteria queries | `test_criteria.py` |
| Variation — same input, different output | `test_variation.py` |
| Auth flow | `test_auth.py` |

### States to Test

- Auth: valid token / expired token / missing token
- Profile: complete / incomplete / missing color field
- Daily calc: each goal type / missing goal / invalid goal
- Agents: each agent in isolation + full pipeline
- Variation: run same profile + goal 5× — assert no two outputs are identical
- Feedback: valid rating / out-of-range rating

---

## Definition of Done

A task is complete only when:

1. Requirements implemented
2. All existing tests still pass
3. New tests added for new behavior
4. `seed.py` updated if new DB columns or content added
5. No secrets or PII exposed in responses or logs
6. No duplicated logic — refactor before creating new files
7. CORS remains restricted (no `allow_origins=["*"]` in production)
8. AI output variation confirmed — same input must produce different output across runs
9. API docs (`/docs`) reflect updated request/response shapes
