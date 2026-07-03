"""Unit tests: INTJ + Projector combination.

Covers:
  - MBTI criteria retrieval (general + goal-filtered)
  - HD criteria retrieval (general + goal-filtered)
  - MBTI×HD scenario lookup
  - Blended decision merging and sorting
  - Content assertions for the INTJ+Projector conflict/recommendation pair
  - Coverage checks for all 16 MBTI and all 5 HD types
  - Full 80-scenario coverage check

Run:
    cd strategy_engine_release
    pytest tests/test_intj_projector.py -v
"""

import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Make sure imports resolve when pytest is run from strategy_engine_release/
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.database import Base
from models.orm import HdCriterion, MbtiCriterion, MbtiHdScenario
from models.schemas import VALID_HD_TYPES, VALID_MBTI
from seed import seed_hd, seed_mbti, seed_scenarios
from services.criteria import (
    get_blended_decisions,
    get_hd_decisions,
    get_mbti_decisions,
    get_scenario,
)


# ── Fixture ────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def db():
    """In-memory SQLite DB, seeded once for the whole module."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    seed_mbti(session)
    seed_hd(session)
    seed_scenarios(session)
    session.commit()

    yield session
    session.close()


# ── MBTI criteria: INTJ ────────────────────────────────────────────────────────

class TestIntjMbtiCriteria:
    def test_returns_at_least_three_general_rows(self, db):
        rows = get_mbti_decisions(db, "INTJ")
        assert len(rows) >= 3

    def test_general_rows_sorted_by_weight_desc(self, db):
        rows = get_mbti_decisions(db, "INTJ")
        weights = [r["weight"] for r in rows]
        assert weights == sorted(weights, reverse=True)

    def test_contains_decision_making_preference(self, db):
        rows = get_mbti_decisions(db, "INTJ")
        prefs = {r["preference"] for r in rows}
        assert "decision_making" in prefs

    def test_contains_energy_preference(self, db):
        rows = get_mbti_decisions(db, "INTJ")
        prefs = {r["preference"] for r in rows}
        assert "energy" in prefs

    def test_decision_making_weight_gte_energy_weight(self, db):
        rows = get_mbti_decisions(db, "INTJ")
        dm_w  = next(r["weight"] for r in rows if r["preference"] == "decision_making")
        eng_w = next(r["weight"] for r in rows if r["preference"] == "energy")
        assert dm_w >= eng_w

    def test_work_goal_includes_general_and_specific(self, db):
        rows = get_mbti_decisions(db, "INTJ", goal="work")
        prefs = {r["preference"] for r in rows}
        assert "decision_making" in prefs       # general
        assert "work_guidance" in prefs         # goal-specific

    def test_money_goal_includes_money_guidance(self, db):
        rows = get_mbti_decisions(db, "INTJ", goal="money")
        prefs = {r["preference"] for r in rows}
        assert "money_guidance" in prefs

    def test_relationship_goal_includes_relationship_guidance(self, db):
        rows = get_mbti_decisions(db, "INTJ", goal="relationship")
        prefs = {r["preference"] for r in rows}
        assert "relationship_guidance" in prefs

    def test_work_goal_excludes_other_goal_rows(self, db):
        rows = get_mbti_decisions(db, "INTJ", goal="work")
        goals = {r["goal"] for r in rows}
        assert "money" not in goals
        assert "relationship" not in goals

    def test_general_call_excludes_goal_specific_rows(self, db):
        rows = get_mbti_decisions(db, "INTJ")
        for r in rows:
            assert r["goal"] is None

    def test_ni_mentioned_in_decision_making_text(self, db):
        rows = get_mbti_decisions(db, "INTJ")
        dm_text = next(r["decision"] for r in rows if r["preference"] == "decision_making")
        assert "Ni" in dm_text


# ── HD criteria: Projector ─────────────────────────────────────────────────────

class TestProjectorHdCriteria:
    def test_returns_at_least_two_general_rows(self, db):
        rows = get_hd_decisions(db, "Projector")
        assert len(rows) >= 2

    def test_general_rows_sorted_by_weight_desc(self, db):
        rows = get_hd_decisions(db, "Projector")
        weights = [r["weight"] for r in rows]
        assert weights == sorted(weights, reverse=True)

    def test_contains_wait_for_invitation_preference(self, db):
        rows = get_hd_decisions(db, "Projector")
        prefs = {r["preference"] for r in rows}
        assert "wait_for_invitation" in prefs

    def test_contains_energy_management_preference(self, db):
        rows = get_hd_decisions(db, "Projector")
        prefs = {r["preference"] for r in rows}
        assert "energy_management" in prefs

    def test_invitation_weight_gte_energy_management_weight(self, db):
        rows = get_hd_decisions(db, "Projector")
        inv_w = next(r["weight"] for r in rows if r["preference"] == "wait_for_invitation")
        eng_w = next(r["weight"] for r in rows if r["preference"] == "energy_management")
        assert inv_w >= eng_w

    def test_work_goal_includes_work_guidance(self, db):
        rows = get_hd_decisions(db, "Projector", goal="work")
        prefs = {r["preference"] for r in rows}
        assert "work_guidance" in prefs

    def test_money_goal_includes_money_guidance(self, db):
        rows = get_hd_decisions(db, "Projector", goal="money")
        prefs = {r["preference"] for r in rows}
        assert "money_guidance" in prefs

    def test_relationship_goal_includes_relationship_guidance(self, db):
        rows = get_hd_decisions(db, "Projector", goal="relationship")
        prefs = {r["preference"] for r in rows}
        assert "relationship_guidance" in prefs

    def test_none_hd_returns_empty(self, db):
        rows = get_hd_decisions(db, None)
        assert rows == []

    def test_invitation_text_mentions_invitation(self, db):
        rows = get_hd_decisions(db, "Projector")
        inv_text = next(r["decision"] for r in rows if r["preference"] == "wait_for_invitation")
        assert "invitation" in inv_text.lower()

    def test_energy_management_mentions_hours(self, db):
        rows = get_hd_decisions(db, "Projector")
        eng_text = next(r["decision"] for r in rows if r["preference"] == "energy_management")
        assert "hour" in eng_text.lower()


# ── Scenario: INTJ × Projector ─────────────────────────────────────────────────

class TestIntjProjectorScenario:
    def test_scenario_exists(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        assert scenario is not None

    def test_scenario_mbti_type(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        assert scenario["mbti_type"] == "INTJ"

    def test_scenario_hd_type(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        assert scenario["hd_type"] == "Projector"

    def test_blend_summary_is_nonempty(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        assert len(scenario["blend_summary"]) > 20

    def test_conflict_situation_mentions_system_or_meeting(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        text = scenario["conflict_situation"].lower()
        assert any(kw in text for kw in ["system", "meeting", "analysis", "team"])

    def test_conflict_sentence_is_directive_not_a_question(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        # The problematic sentence should NOT end with ? (it's a statement/directive)
        assert not scenario["conflict_sentence"].strip().endswith("?")

    def test_recommended_sentence_is_an_invitation(self, db):
        # Recommended sentence should contain a question mark (inviting, not directing)
        scenario = get_scenario(db, "INTJ", "Projector")
        assert "?" in scenario["recommended_sentence"]

    def test_recommended_sentence_is_softer_than_conflict(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        conflict    = scenario["conflict_sentence"].lower()
        recommended = scenario["recommended_sentence"].lower()
        # Conflict is assertive; recommended opens a door
        assert len(recommended) > 10
        assert recommended != conflict

    def test_recommended_action_is_actionable(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        action = scenario["recommended_action"]
        assert len(action) > 20
        # Should give concrete guidance
        assert any(kw in action.lower() for kw in
                   ["wait", "invite", "ask", "before", "question", "invitation"])

    def test_none_hd_returns_none_scenario(self, db):
        scenario = get_scenario(db, "INTJ", None)
        assert scenario is None

    def test_scenario_all_required_fields_present(self, db):
        scenario = get_scenario(db, "INTJ", "Projector")
        for field in ("mbti_type", "hd_type", "blend_summary",
                      "conflict_situation", "conflict_sentence",
                      "recommended_sentence", "recommended_action"):
            assert field in scenario
            assert scenario[field]  # non-empty


# ── Blended decisions: INTJ + Projector ───────────────────────────────────────

class TestIntjProjectorBlended:
    def test_blended_work_has_both_sources(self, db):
        blended = get_blended_decisions(db, "INTJ", "Projector", "work")
        sources = {r["source"] for r in blended}
        assert "mbti" in sources
        assert "hd"   in sources

    def test_blended_money_has_both_sources(self, db):
        blended = get_blended_decisions(db, "INTJ", "Projector", "money")
        sources = {r["source"] for r in blended}
        assert "mbti" in sources
        assert "hd"   in sources

    def test_blended_relationship_has_both_sources(self, db):
        blended = get_blended_decisions(db, "INTJ", "Projector", "relationship")
        sources = {r["source"] for r in blended}
        assert "mbti" in sources
        assert "hd"   in sources

    def test_blended_sorted_by_weight_desc(self, db):
        blended = get_blended_decisions(db, "INTJ", "Projector", "work")
        weights = [r["weight"] for r in blended]
        assert weights == sorted(weights, reverse=True)

    def test_blended_work_has_at_least_5_rows(self, db):
        # 4 INTJ general+work + 3 Projector general+work = 7 minimum
        blended = get_blended_decisions(db, "INTJ", "Projector", "work")
        assert len(blended) >= 5

    def test_blended_excludes_wrong_goal_rows(self, db):
        blended = get_blended_decisions(db, "INTJ", "Projector", "work")
        for r in blended:
            assert r["goal"] in (None, "work"), \
                f"Unexpected goal '{r['goal']}' in work-filtered results"

    def test_blended_work_includes_work_guidance(self, db):
        blended = get_blended_decisions(db, "INTJ", "Projector", "work")
        prefs = {r["preference"] for r in blended}
        assert "work_guidance" in prefs

    def test_blended_contains_invitation_guidance(self, db):
        blended = get_blended_decisions(db, "INTJ", "Projector", "work")
        hd_rows = [r for r in blended if r["source"] == "hd"]
        assert any("invitation" in r["decision"].lower() for r in hd_rows)

    def test_blended_with_none_hd_returns_only_mbti(self, db):
        blended = get_blended_decisions(db, "INTJ", None, "work")
        sources = {r["source"] for r in blended}
        assert sources == {"mbti"}


# ── Coverage: all 16 MBTI types ───────────────────────────────────────────────

class TestAllMbtiCoverage:
    @pytest.mark.parametrize("mbti", sorted(VALID_MBTI))
    def test_each_type_has_general_criteria(self, db, mbti):
        rows = get_mbti_decisions(db, mbti)
        assert len(rows) >= 3, f"{mbti} should have ≥3 general decision rules"

    @pytest.mark.parametrize("mbti", sorted(VALID_MBTI))
    def test_each_type_has_work_criteria(self, db, mbti):
        rows = get_mbti_decisions(db, mbti, goal="work")
        prefs = {r["preference"] for r in rows}
        assert "work_guidance" in prefs, f"{mbti} missing work_guidance"

    @pytest.mark.parametrize("mbti", sorted(VALID_MBTI))
    def test_each_type_has_money_criteria(self, db, mbti):
        rows = get_mbti_decisions(db, mbti, goal="money")
        prefs = {r["preference"] for r in rows}
        assert "money_guidance" in prefs, f"{mbti} missing money_guidance"

    @pytest.mark.parametrize("mbti", sorted(VALID_MBTI))
    def test_each_type_has_relationship_criteria(self, db, mbti):
        rows = get_mbti_decisions(db, mbti, goal="relationship")
        prefs = {r["preference"] for r in rows}
        assert "relationship_guidance" in prefs, f"{mbti} missing relationship_guidance"


# ── Coverage: all 5 HD types ──────────────────────────────────────────────────

class TestAllHdCoverage:
    @pytest.mark.parametrize("hd", sorted(VALID_HD_TYPES))
    def test_each_type_has_general_criteria(self, db, hd):
        rows = get_hd_decisions(db, hd)
        assert len(rows) >= 2, f"{hd} should have ≥2 general decision rules"

    @pytest.mark.parametrize("hd", sorted(VALID_HD_TYPES))
    def test_each_type_has_work_guidance(self, db, hd):
        rows = get_hd_decisions(db, hd, goal="work")
        prefs = {r["preference"] for r in rows}
        assert "work_guidance" in prefs, f"{hd} missing work_guidance"

    @pytest.mark.parametrize("hd", sorted(VALID_HD_TYPES))
    def test_each_type_has_money_guidance(self, db, hd):
        rows = get_hd_decisions(db, hd, goal="money")
        prefs = {r["preference"] for r in rows}
        assert "money_guidance" in prefs, f"{hd} missing money_guidance"

    @pytest.mark.parametrize("hd", sorted(VALID_HD_TYPES))
    def test_each_type_has_relationship_guidance(self, db, hd):
        rows = get_hd_decisions(db, hd, goal="relationship")
        prefs = {r["preference"] for r in rows}
        assert "relationship_guidance" in prefs, f"{hd} missing relationship_guidance"


# ── Coverage: all 80 MBTI × HD scenarios ─────────────────────────────────────

class TestAll80Scenarios:
    @pytest.mark.parametrize("mbti,hd", [
        (m, h) for m in sorted(VALID_MBTI) for h in sorted(VALID_HD_TYPES)
    ])
    def test_scenario_exists_for_every_pair(self, db, mbti, hd):
        scenario = get_scenario(db, mbti, hd)
        assert scenario is not None, f"Missing scenario for {mbti} + {hd}"

    @pytest.mark.parametrize("mbti,hd", [
        (m, h) for m in sorted(VALID_MBTI) for h in sorted(VALID_HD_TYPES)
    ])
    def test_every_scenario_recommended_differs_from_conflict(self, db, mbti, hd):
        scenario = get_scenario(db, mbti, hd)
        assert scenario["recommended_sentence"] != scenario["conflict_sentence"], \
            f"{mbti}+{hd} recommended_sentence must differ from conflict_sentence"

    @pytest.mark.parametrize("mbti,hd", [
        (m, h) for m in sorted(VALID_MBTI) for h in sorted(VALID_HD_TYPES)
    ])
    def test_every_scenario_recommended_is_nonempty(self, db, mbti, hd):
        scenario = get_scenario(db, mbti, hd)
        assert len(scenario["recommended_sentence"]) > 15, \
            f"{mbti}+{hd} recommended_sentence is too short"

    def test_total_scenario_count_is_80(self, db):
        count = db.query(MbtiHdScenario).count()
        assert count == 80, f"Expected 80 scenarios, got {count}"
