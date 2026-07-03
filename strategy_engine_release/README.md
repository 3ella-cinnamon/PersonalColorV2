# Personal Strategy Engine — v0.2

FastAPI backend with **user accounts**, **stored profiles**, and **DB-driven decision rules** for MBTI and Human Design types.

## What's new in v0.2

- **Auth** — JWT-based signup / login / `/me`
- **Stored profiles** — birthdate, time, place, MBTI, HD type, blood type live in the DB
- **Auto-skip onboarding** — login response includes `has_profile`; the frontend reads it and goes straight to the dashboard
- **Criteria tables** — `mbti_criteria` and `hd_criteria` hold preference→decision rules; `/api/daily-calc` returns them alongside the score so they show up in the UI

## Tech stack

- FastAPI + SQLAlchemy 2.0
- Auth: bcrypt + JWT (`python-jose`)
- Database: **SQLite** by default for local dev (zero install), **MySQL** in production via the same code

## Project layout

```
strategy_engine/
├── main.py                  FastAPI app, router wiring, auto-create tables
├── seed.py                  Creates tables + seeds example criteria rows
├── requirements.txt
├── .env.example             Copy → .env
├── core/
│   ├── config.py            Pydantic Settings from .env
│   ├── database.py          SQLAlchemy engine + Session + Base
│   ├── security.py          Password hashing + JWT
│   └── deps.py              get_current_user dependency
├── api/
│   ├── auth.py              POST /signup, POST /login, GET /me
│   ├── profile.py           POST/PUT/GET /api/profile, GET /api/profile/blueprint
│   └── daily.py             POST /api/daily-calc (uses logged-in user's profile)
├── models/
│   ├── domain.py            Element, Strategy, Goal, InteractionType enums
│   ├── orm.py               User, UserProfile, MbtiCriterion, HdCriterion
│   └── schemas.py           Pydantic DTOs
└── services/
    ├── elements.py          Five Elements cycles
    ├── saju.py              BaZi pillar derivation (placeholder)
    ├── mbti.py              MBTI → cognitive function → Element
    ├── multipliers.py       E_mian, M_hd, M_cog placeholders
    ├── scoring.py           Daily Action Score formula
    └── criteria.py          DB lookups for MBTI/HD decisions
```

## Quick start (local dev with SQLite — zero install)

```bash
pip install -r requirements.txt
cp .env.example .env       # default DATABASE_URL is SQLite
python seed.py             # creates tables + example criteria
uvicorn main:app --reload
```

Open <http://localhost:8000/docs>. Use the **Authorize** button in Swagger after `/login` to call protected endpoints.

## Switching to MySQL (production or staging)

1. Install MySQL locally **or** create a free MySQL DB on PlanetScale, Aiven, or AWS RDS.
2. Create a database named `strategy_engine`:
   ```sql
   CREATE DATABASE strategy_engine CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Edit `.env`:
   ```
   DATABASE_URL=mysql+pymysql://USER:PASSWORD@HOST:3306/strategy_engine
   ```
4. Re-run `python seed.py` (it's idempotent — won't duplicate rows).
5. `uvicorn main:app --reload`. Same code, different DB.

## API summary

| Endpoint                          | Auth required | Purpose                                          |
|-----------------------------------|:-------------:|--------------------------------------------------|
| `POST /api/auth/signup`           | no            | Create account, return JWT                       |
| `POST /api/auth/login`            | no            | Email + password (form data) → JWT + has_profile |
| `GET  /api/auth/me`               | yes           | Current user                                     |
| `POST /api/profile`               | yes           | Create profile (first time)                      |
| `PUT  /api/profile`               | yes           | Update profile                                   |
| `GET  /api/profile`               | yes           | Read raw profile                                 |
| `GET  /api/profile/blueprint`     | yes           | Computed Energy Blueprint                        |
| `POST /api/daily-calc`            | yes           | Today's score + MBTI/HD decisions                |

## Frontend integration flow

1. App loads → check `localStorage.token`. If present, call `GET /api/auth/me`:
   - 401 → token expired, show login
   - 200 + `has_profile: true`  → **skip onboarding**, go to dashboard
   - 200 + `has_profile: false` → show onboarding form
2. After signup or login, store `access_token` and `has_profile` from the response.
3. On all protected calls, send `Authorization: Bearer <token>` header.
4. Onboarding form posts to `POST /api/profile` (not `/onboarding` anymore).
5. Dashboard "Generate" calls `POST /api/daily-calc` with `{target_date, goal, energy_level}`.

## Editing decision rules without a redeploy

The MBTI and HD decision rules are rows in the `mbti_criteria` and `hd_criteria` tables. To change them:

- **Direct SQL** — `UPDATE mbti_criteria SET decision='...' WHERE mbti_type='INTJ' AND preference='energy';`
- **Re-seed from code** — edit the lists in `seed.py`, run `python seed.py --reset`.

The next `/api/daily-calc` call returns the new rules immediately.

## Production hardening (when you deploy)

1. Generate a real `JWT_SECRET`:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
2. Tighten CORS in `main.py` (replace `["*"]` with your real frontend domain).
3. Switch `Base.metadata.create_all` to **Alembic migrations** for schema changes.
4. Add HTTPS termination at the load balancer / reverse proxy.
