# Boong — Application Architecture

```mermaid
flowchart TD
    USER(["👤 User"])

    subgraph FRONTEND["🖥️  React Dashboard  (Vite · port 5173)"]
        AUTH["Login / Signup"]
        PROFILE["Profile Setup\nMBTI · HD · Personal Color · Birthdate"]
        INPUT["Select Goal + Energy Level\nLanguage EN / TH"]
        BTN["[ Generate ]"]
    end

    subgraph BACKEND["⚙️  FastAPI Backend  (port 8000)"]
        MW["Middleware\n→ logs/YYYY-MM-DD.txt"]
        JWT["JWT Auth\n→ resolve user + profile"]

        subgraph CACHE["Cache Check"]
            CK["Key: user_id + goal\n+ mbti + hd + birthdate + date"]
            HIT["✅ Cache HIT\nreturn stored result\n0 AI tokens"]
            MISS["❌ Cache MISS\ngenerate new"]
        end

        BAZI["BaZi Calculator\nday_master · daily_element\nfrom birthdate + target_date"]
        SCORE["Scoring Engine\nbazi_score 0–10"]
    end

    subgraph PIPELINE["🤖  AI Pipeline"]
        A1["Agent 1 — Profile Context\nDB only · no AI call\nmbti + hd + color + scenario"]
        A2["Agent 2 — Goal Context\nDB only · no AI call\nmbti_criteria + hd_criteria"]
        A3["Agent 3 — Coaching AI\nbehavior · timing · communication\nwarnings · practical_tips\n── EN + TH in 1 response ──"]
        A4["Agent 4 — Dialogue AI\nScenario :: Bold sentence\nsample_sentences · alternatives\n── EN + TH in 1 response ──"]
    end

    subgraph AI["🔑  AI Provider  (priority order)"]
        G["1️⃣  Gemini 2.0 Flash\nfree tier"]
        C["2️⃣  Claude Sonnet\npaid"]
        O["3️⃣  GPT-4o\npaid"]
        FB["4️⃣  DB Fallback\n0 cost"]
    end

    subgraph DB["🗄️  SQLite Database"]
        REC["recommendations\n├─ EN fields\n├─ TH fields _th\n└─ cache key snapshot"]
        LOG["api_logs\n└─ logs/YYYY-MM-DD.txt"]
        MEM["agent_memories\nused angles · 30d TTL"]
        USR["users + user_profiles"]
    end

    RESP["📦 Response\nbehavior · timing · communication\nwarnings · practical_tips\nsample sentences · EN or TH"]

    USER --> AUTH
    AUTH --> PROFILE --> INPUT --> BTN
    BTN -->|"POST /api/daily-calc\ngoal · energy · lang\nAuthorization: Bearer JWT"| MW
    MW --> JWT
    JWT --> CK
    CK -->|"HIT + has_lang"| HIT
    HIT --> RESP
    CK -->|"MISS or TH missing"| MISS
    MISS --> BAZI --> SCORE
    SCORE --> A1 --> A2 --> A3 --> A4
    A3 & A4 --> G
    G -->|"fails"| C
    C -->|"fails"| O
    O -->|"fails"| FB
    G & C & O & FB --> REC
    REC --> RESP
    MW --> LOG
    A3 --> MEM
    RESP -->|"render EN or TH\nbased on lang toggle"| USER
```

---

## Data Flow Summary

| Step | Where | What happens |
|------|--------|-------------|
| 1 | Frontend | User selects goal + energy + lang → POST /api/daily-calc |
| 2 | Middleware | Log URL + request + response + ms → .txt file |
| 3 | Auth | Validate JWT → load user profile |
| 4 | Cache | Check DB by (user + goal + mbti + hd + birthdate + date) |
| 4a | Cache HIT | Return stored EN or TH immediately — **0 AI tokens** |
| 4b | Cache MISS | Continue to pipeline |
| 5 | BaZi | Compute day_master + daily_element from birthdate |
| 6 | Scoring | Calculate bazi_score 0–10 |
| 7 | Agent 1 | Build profile context from DB (no AI) |
| 8 | Agent 2 | Build goal context from DB (no AI) |
| 9 | Agent 3 | AI call → coaching output **EN + TH** in 1 response |
| 10 | Agent 4 | AI call → sentences in `Scenario :: Bold sentence` format **EN + TH** |
| 11 | AI Priority | Gemini → Claude Sonnet → GPT-4o → DB Fallback |
| 12 | DB | Save EN + TH + cache key to recommendations table |
| 13 | Frontend | Render requested language, show EN/TH toggle |

---

## Database Tables

```
recommendations          ← coaching outputs + cache
  ├─ profile_mbti        ← cache key
  ├─ profile_hd_type     ← cache key
  ├─ profile_birthdate   ← cache key
  ├─ behavior_recommendation     + behavior_recommendation_th
  ├─ timing_guidance             + timing_guidance_th
  ├─ communication_strategy      + communication_strategy_th
  ├─ warnings                    + warnings_th
  ├─ practical_tips              + practical_tips_th
  ├─ sample_sentences            + sample_sentences_th
  ├─ alternative_responses       + alternative_responses_th
  └─ coaching_summary            + coaching_summary_th

api_logs                 ← every HTTP request
  ├─ method, url, status_code
  ├─ request_body, response_body (4KB cap)
  └─ duration_ms, created_at

agent_memories           ← prevents repeated coaching angles
  └─ expires after 30 days

users                    ← auth
user_profiles            ← MBTI · HD · Personal Color · birthdate
```

---

## Token Cost Model

| Scenario | AI Calls | Cost |
|----------|----------|------|
| First request (new day) | 2 calls (Agent 3 + 4) | ~$0.01 |
| Same goal, same day | 0 calls — cache hit | **$0.00** |
| Switch EN → TH | 0 calls — already in DB | **$0.00** |
| New goal, same day | 2 calls | ~$0.01 |
