"""API tests for the Card Deck endpoints (/api/cards/*).

Covers:
  - Saving / listing / fetching / deleting readings (quick + guided)
  - Auth requirement and per-user ownership isolation
  - Newest-first ordering
  - activation_before range validation
  - Guided full vs. minimal session round-trip (the consent-gated shapes the
    frontend sends: full session when opted in, short summary when not)
  - The public Thai i18n bundle + its DB seeding

The whole test app runs against a throwaway temp-file SQLite DB, and the
`get_db` dependency is overridden so the real project DB is never touched.
TestClient is used WITHOUT its context manager on purpose, so the app's
lifespan (which would create_all on the real engine) does not run.

Run:
    cd strategy_engine_release
    pytest tests/test_cards_api.py -v
"""

import os
import sys
import tempfile
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Resolve imports when pytest runs from strategy_engine_release/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.database import Base, get_db  # noqa: E402
from main import app  # noqa: E402
import services.cards_service as cards_service  # noqa: E402


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def client():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    engine = create_engine(f"sqlite:///{path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)  # models.orm is imported via main -> all tables registered
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    # Let the i18n cache seed into THIS test DB on first use.
    cards_service._CACHE_LOADED = False

    c = TestClient(app)   # not a context manager -> app lifespan is not triggered
    yield c

    app.dependency_overrides.clear()
    cards_service._CACHE_LOADED = False
    engine.dispose()
    os.unlink(path)


def _register(client) -> dict:
    """Create a fresh user and return its auth header."""
    email = f"cards_{uuid.uuid4().hex[:10]}@example.com"
    r = client.post("/api/auth/signup", json={"email": email, "password": "testpass123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
def auth(client):
    """A unique authenticated user per test, so reading lists stay isolated."""
    return _register(client)


QUICK_READING = {
    "deck": "neuro",
    "spread_id": "one",
    "spread_name": "What Do You See?",
    "cards": [{"card_id": "neuro_36", "position": "Open image"}],
    "reflection": "I see a nest — somewhere to rest.",
    "intention": "a decision I am sitting with",
    "activation_before": 3,
    "lang": "en",
    "mode": "quick",
    "session": {"summary": "You drew The Nest.", "workshops": []},
}


# ── Auth ────────────────────────────────────────────────────────────────────

class TestAuth:
    def test_list_requires_auth(self, client):
        assert client.get("/api/cards/readings").status_code == 401

    def test_create_requires_auth(self, client):
        assert client.post("/api/cards/readings", json=QUICK_READING).status_code == 401


# ── CRUD ────────────────────────────────────────────────────────────────────

class TestReadingCrud:
    def test_create_returns_serialized_reading(self, client, auth):
        r = client.post("/api/cards/readings", json=QUICK_READING, headers=auth)
        assert r.status_code == 201, r.text
        body = r.json()
        assert body["deck"] == "neuro"
        assert body["mode"] == "quick"
        assert body["cards"] == [{"card_id": "neuro_36", "position": "Open image"}]
        assert body["reflection"] == QUICK_READING["reflection"]
        assert body["session"]["summary"] == "You drew The Nest."
        assert isinstance(body["id"], int)
        assert body["created_at"]

    def test_list_returns_only_own_readings(self, client, auth):
        client.post("/api/cards/readings", json=QUICK_READING, headers=auth)
        rows = client.get("/api/cards/readings", headers=auth).json()
        assert len(rows) == 1
        assert rows[0]["deck"] == "neuro"

    def test_get_by_id(self, client, auth):
        created = client.post("/api/cards/readings", json=QUICK_READING, headers=auth).json()
        r = client.get(f"/api/cards/readings/{created['id']}", headers=auth)
        assert r.status_code == 200
        assert r.json()["id"] == created["id"]

    def test_delete_removes_reading(self, client, auth):
        created = client.post("/api/cards/readings", json=QUICK_READING, headers=auth).json()
        assert client.delete(f"/api/cards/readings/{created['id']}", headers=auth).status_code == 204
        assert client.get("/api/cards/readings", headers=auth).json() == []

    def test_get_missing_returns_404(self, client, auth):
        assert client.get("/api/cards/readings/999999", headers=auth).status_code == 404

    def test_delete_missing_returns_404(self, client, auth):
        assert client.delete("/api/cards/readings/999999", headers=auth).status_code == 404

    def test_list_is_newest_first(self, client, auth):
        first = client.post("/api/cards/readings", json={**QUICK_READING, "reflection": "first"}, headers=auth).json()
        second = client.post("/api/cards/readings", json={**QUICK_READING, "reflection": "second"}, headers=auth).json()
        rows = client.get("/api/cards/readings", headers=auth).json()
        assert [r["id"] for r in rows] == [second["id"], first["id"]]


# ── Ownership isolation ─────────────────────────────────────────────────────

class TestOwnership:
    def test_other_user_cannot_read_or_delete(self, client):
        owner = _register(client)
        other = _register(client)
        created = client.post("/api/cards/readings", json=QUICK_READING, headers=owner).json()

        # other user must not see it in their list
        assert client.get("/api/cards/readings", headers=other).json() == []
        # nor fetch it by id (404, not 403 — don't leak existence)
        assert client.get(f"/api/cards/readings/{created['id']}", headers=other).status_code == 404
        # nor delete it
        assert client.delete(f"/api/cards/readings/{created['id']}", headers=other).status_code == 404
        # owner still has it intact
        assert client.get(f"/api/cards/readings/{created['id']}", headers=owner).status_code == 200


# ── Validation ──────────────────────────────────────────────────────────────

class TestValidation:
    def test_activation_before_out_of_range_rejected(self, client, auth):
        bad = {**QUICK_READING, "activation_before": 15}
        assert client.post("/api/cards/readings", json=bad, headers=auth).status_code == 422

    def test_activation_before_may_be_null(self, client, auth):
        ok = {**QUICK_READING, "activation_before": None}
        assert client.post("/api/cards/readings", json=ok, headers=auth).status_code == 201


# ── Guided sessions: full vs. minimal (consent-gated) shapes ────────────────

class TestGuidedSession:
    def test_full_session_round_trips(self, client, auth):
        payload = {
            "deck": "neuro", "spread_id": "guided", "spread_name": "Guided session",
            "cards": [{"card_id": "neuro_04", "position": "Guided"}],
            "reflection": "raw words the user typed",
            "intention": "work stress",
            "activation_before": 4,
            "lang": "en", "mode": "guided",
            "session": {
                "consent_version": "cards-guided-1",
                "observations": {"notice": "a cage", "feeling": "trapped", "association": None},
                "body_state": "tight chest",
                "user_meaning": "I feel stuck",
                "session_summary": "stuck but a door is open",
                "anchor": "the door is open",
                "feedback": {"consent_to_store": True},
            },
        }
        created = client.post("/api/cards/readings", json=payload, headers=auth).json()
        got = client.get(f"/api/cards/readings/{created['id']}", headers=auth).json()
        assert got["mode"] == "guided"
        assert got["session"]["observations"]["notice"] == "a cage"
        assert got["session"]["body_state"] == "tight chest"
        assert got["reflection"] == "raw words the user typed"

    def test_minimal_session_keeps_only_summary(self, client, auth):
        """The shape the frontend sends when the user does NOT consent to
        storing the full session — only the short summary is present."""
        payload = {
            "deck": "neuro", "spread_id": "guided", "spread_name": "Guided session",
            "cards": [{"card_id": "neuro_04", "position": "Guided"}],
            "reflection": None,
            "intention": None,
            "activation_before": 4,
            "lang": "en", "mode": "guided",
            "session": {
                "consent_to_store": False,
                "session_summary": "a short line I chose to keep",
                "anchor": "steady",
                "activation_before": 4,
                "activation_after": 3,
                "lang": "en",
            },
        }
        created = client.post("/api/cards/readings", json=payload, headers=auth).json()
        got = client.get(f"/api/cards/readings/{created['id']}", headers=auth).json()
        assert got["session"]["consent_to_store"] is False
        assert got["session"]["session_summary"] == "a short line I chose to keep"
        # The sensitive, detailed fields must not be present at all.
        assert "observations" not in got["session"]
        assert "body_state" not in got["session"]
        assert got["reflection"] is None
        assert got["intention"] is None


# ── Thai i18n bundle (public) ───────────────────────────────────────────────

class TestI18n:
    def test_bundle_is_public_and_seeds_db(self, client):
        r = client.get("/api/cards/i18n/th")   # no auth header
        assert r.status_code == 200
        body = r.json()
        assert "strings" in body and "workshops" in body and "summaries" in body
        # a known English micro-intervention has a Thai translation
        assert body["strings"]["Unclench hands on the exhale."]
        # workshops carry short label + prompt + >= 3 hints
        ws = body["workshops"]["Resourcing & co-regulation"]
        assert ws["short"] and ws["prompt"]
        assert len([h for h in ws["hints"] if h]) >= 3

    def test_summary_templates_present(self, client):
        summaries = client.get("/api/cards/i18n/th").json()["summaries"]
        assert "{name}" in summaries["one"] and "{theme}" in summaries["one"]
        assert "{lines}" in summaries["multi"]
        assert summaries["one"].startswith("การ์ดที่คุณเลือก")   # not the old "คุณจั่วได้"

    def test_bundle_is_stable_across_calls(self, client):
        a = client.get("/api/cards/i18n/th").json()
        b = client.get("/api/cards/i18n/th").json()
        assert a == b
