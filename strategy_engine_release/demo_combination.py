"""Quick demo: show blended output for any MBTI + HD + Goal combination.

Usage:
    python demo_combination.py                          # default: ISFJ + Generator + work
    python demo_combination.py ISFJ Generator money
    python demo_combination.py ENTJ Projector relationship
"""

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.database import Base
from seed import seed_hd, seed_mbti, seed_scenarios
from services.criteria import get_blended_decisions, get_hd_decisions, get_mbti_decisions, get_scenario

DIVIDER  = "=" * 64
SUBDIV   = "-" * 64

GOAL_LABEL = {"work": "WORK", "money": "MONEY", "relationship": "RELATIONSHIP"}
HD_EMOJI   = {
    "Generator":             "Generator",
    "Manifesting Generator": "Manifesting Generator",
    "Manifestor":            "Manifestor",
    "Projector":             "Projector",
    "Reflector":             "Reflector",
}


def build_db():
    engine  = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db      = Session()
    seed_mbti(db)
    seed_hd(db)
    seed_scenarios(db)
    db.commit()
    return db


def print_report(mbti: str, hd: str, goal: str, db):
    blended  = get_blended_decisions(db, mbti, hd, goal)
    scenario = get_scenario(db, mbti, hd)

    goal_label = GOAL_LABEL.get(goal, goal.upper())
    hd_label   = HD_EMOJI.get(hd, hd)

    print()
    print(DIVIDER)
    print(f"  INPUT  ->  {mbti}  +  {hd_label}  +  {goal_label}")
    print(DIVIDER)

    # ── Blend Summary ────────────────────────────────────────────
    if scenario:
        print()
        print("[ BLEND SUMMARY ]")
        print(f"  {scenario['blend_summary']}")

    # ── Blended Decision Rules ────────────────────────────────────
    print()
    print("[ BLENDED CRITERIA  (sorted by priority) ]")
    print(SUBDIV)
    mbti_rows = [r for r in blended if r["source"] == "mbti"]
    hd_rows   = [r for r in blended if r["source"] == "hd"]

    print(f"  -- {mbti} (MBTI) --")
    for r in mbti_rows:
        tag = f"[{r['goal']}]" if r["goal"] else "[general]"
        print(f"  * {r['preference']:<28} {tag}")
        print(f"    {r['decision']}")
        print()

    print(f"  -- {hd} (Human Design) --")
    for r in hd_rows:
        tag = f"[{r['goal']}]" if r["goal"] else "[general]"
        print(f"  * {r['preference']:<28} {tag}")
        print(f"    {r['decision']}")
        print()

    # ── Conflict Scenario ─────────────────────────────────────────
    if scenario:
        print(SUBDIV)
        print("[ CONFLICT SCENARIO ]")
        print()
        print("  [SITUATION]")
        print(f"  {scenario['conflict_situation']}")
        print()
        print("  [X] WHAT THEY SAID  (creates friction)")
        print(f'  "{scenario["conflict_sentence"]}"')
        print()
        print("  [OK] RECOMMENDED SENTENCE  (what to say instead)")
        print(f'  "{scenario["recommended_sentence"]}"')
        print()
        print("  [!] RECOMMENDED ACTION")
        print(f"  {scenario['recommended_action']}")

    print()
    print(DIVIDER)
    print()


def main():
    args = sys.argv[1:]
    mbti = args[0].upper() if len(args) > 0 else "ISFJ"
    hd   = args[1]         if len(args) > 1 else "Generator"
    goal = args[2].lower() if len(args) > 2 else None

    db = build_db()

    goals = [goal] if goal else ["work", "money", "relationship"]
    for g in goals:
        print_report(mbti, hd, g, db)

    db.close()


if __name__ == "__main__":
    main()
