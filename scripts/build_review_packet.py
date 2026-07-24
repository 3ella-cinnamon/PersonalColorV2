"""Generate a human-review packet for the Card Deck's Thai copy and framework mapping.

Everything in this packet was written or inferred by an AI (Claude), NOT by a
native Thai speaker or a clinician. This script collects it in one place so a
qualified human can check it before the tool reaches real users.

Run:  python scripts/build_review_packet.py
Out:  Improve/<YYYY-MM-DD>_content_review_packet.md
"""

import json
import os
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "strategy_engine_release"))

from services import cards_i18n_th as th  # noqa: E402


def _row(en: str, thai: str) -> str:
    """One markdown table row, pipes escaped."""
    e = (en or "").replace("|", "\\|").replace("\n", " ")
    t = (thai or "").replace("|", "\\|").replace("\n", " ")
    return f"| {e} | {t} |  |\n"


def main() -> None:
    cards = json.load(open(os.path.join(ROOT, "cards.json"), encoding="utf-8"))["cards"]
    mapping = json.load(open(os.path.join(ROOT, "neuro_framework_mapping.json"), encoding="utf-8"))

    out_dir = os.path.join(ROOT, "Improve")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{date.today().isoformat()}_content_review_packet.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Card Deck — content review packet ({date.today().isoformat()})\n\n")
        f.write(
            "**Everything below was written or inferred by an AI, not by a native Thai\n"
            "speaker or a clinician.** This is a therapeutic-adjacent tool, so please have\n"
            "a qualified human check it before real users see it. Add notes in the last\n"
            "column; anything you change can be edited directly in the `card_translations`\n"
            "table (no deploy needed) or in `services/cards_i18n_th.py` for the seed.\n\n"
        )

        # ── Priority 1: safety-critical, NOT in the DB ──
        f.write("## ⚠️ Priority 1 — verify these first (safety-critical)\n\n")
        f.write(
            "These live in `dashboard/src/GuidedSession.jsx`, **not** in the DB, and were\n"
            "written by an AI from general knowledge. Wrong crisis details in a mental-health\n"
            "tool are the highest-risk item here.\n\n"
            "| Item | Value in the app | Please verify |\n| --- | --- | --- |\n"
            "| Mental Health Hotline (TH) | **1323** | Correct number? Still 24h and free? |\n"
            "| Samaritans Thailand | **02-113-6789** | Correct and current? |\n"
            "| Emergency (medical) | **1669** | Correct for medical emergency? |\n"
            "| Crisis wording (TH + EN) | see `crisis` screen | Is the tone right? Anything to add/remove? |\n"
            "| Crisis keyword list | `CRISIS_TERMS` | Naive substring match — which Thai/English\n"
            "  phrases are missing? Any that false-positive? |\n\n"
            "Also worth a clinician's eye: the **activation routing** (0-3 / 4-6 / 7-8 thresholds)\n"
            "and the decision to show grounding before imagery at activation >= 7.\n\n"
        )

        # ── Thai copy ──
        f.write("## 1. Micro-interventions (\"A small thing to try\") — 40 Neuro cards\n\n")
        f.write("These are shown as an action the user may take. Check both the translation\n"
                "and whether the action itself is safe/appropriate.\n\n")
        f.write("| English (source) | Thai (AI translation) | Reviewer notes |\n| --- | --- | --- |\n")
        for en, thai in th.MICRO_TH.items():
            f.write(_row(en, thai))

        f.write("\n## 2. Clinical caution\n\n")
        f.write("| English (source) | Thai (AI translation) | Reviewer notes |\n| --- | --- | --- |\n")
        for en, thai in th.CAUTION_TH.items():
            f.write(_row(en, thai))

        f.write("\n## 3. Workshop copy (per framework)\n\n")
        f.write("The interactive exercise shown with each card. `prompt` is what the user is\n"
                "asked; `hints` are example answers that visibly steer them — check for leading\n"
                "or presumptuous phrasing.\n\n")
        for fw, entry in th.WORKSHOP_TH.items():
            f.write(f"\n### {fw}\n\n")
            f.write("| Field | Thai | Reviewer notes |\n| --- | --- | --- |\n")
            f.write(f"| short | {entry['short']} |  |\n")
            f.write(f"| prompt | {entry['prompt']} |  |\n")
            for i, hint in enumerate(entry["hints"]):
                f.write(f"| hint {i + 1} | {hint} |  |\n")

        f.write("\n## 4. \"In short\" summary templates\n\n")
        f.write("`{name}` / `{theme}` / `{lines}` are filled in at runtime.\n\n")
        f.write("| Key | Thai template | Reviewer notes |\n| --- | --- | --- |\n")
        for key, tpl in th.SUMMARY_TH.items():
            f.write(f"| {key} | {tpl.replace('|', chr(92) + '|')} |  |\n")

        f.write("\n## 5. Reading guide (\"Intuition First, Knowledge Second\")\n\n")
        f.write("| Field | Thai | Reviewer notes |\n| --- | --- | --- |\n")
        f.write(f"| label | {th.GUIDE_TH['label']} |  |\n")
        for i, sec in enumerate(th.GUIDE_TH["sections"]):
            f.write(f"| section {i + 1} title | {sec['title']} |  |\n")
            f.write(f"| section {i + 1} body | {sec['body']} |  |\n")

        # ── Framework mapping ──
        proposed = [m for m in mapping if m["framework_status"] == "proposed"]
        unmapped = [m for m in mapping if m["framework_status"] == "unmapped"]
        f.write("\n## 6. Neuro card -> framework mapping (needs clinical validation)\n\n")
        f.write(
            f"`proposed_framework` was **inferred by a keyword rule**, not taken from the\n"
            f"literature. {len(proposed)} proposed, {len(unmapped)} unmapped. Please confirm or\n"
            f"correct each against a named model (ACT, IFS, polyvagal-informed regulation,\n"
            f"behavioural activation, self-compassion, ...), then update `FRAMEWORK_RULES` in\n"
            f"`scripts/build_neuro_mapping.py`.\n\n"
        )
        f.write("| Card | Archetype | Proposed framework | Correct? |\n| --- | --- | --- | --- |\n")
        for m in proposed:
            f.write(f"| {m['name_en']} | {m['archetype']} | {m['proposed_framework']} |  |\n")

        f.write(f"\n### Unmapped — no framework rule matched ({len(unmapped)})\n\n")
        f.write("| Card | Archetype | Which framework should this be? |\n| --- | --- | --- |\n")
        for m in unmapped:
            f.write(f"| {m['name_en']} | {m['archetype']} |  |\n")

        # ── Card text already bilingual in the catalogue ──
        neuro = [c for c in cards if c["deck"] == "neuro"]
        f.write(
            f"\n## 7. Out of scope for this packet\n\n"
            f"- The {len(neuro)} Neuro cards' `name_th` / `meaning_th` / `reflect_prompt_th` came\n"
            f"  with your catalogue (healing_card_system_mapping.xlsx), so they are **your** copy,\n"
            f"  not AI translation — reviewed separately if you wish.\n"
            f"- Tarot ({len([c for c in cards if c['deck'] == 'tarot'])}) and Nature\n"
            f"  ({len([c for c in cards if c['deck'] == 'nature'])}) card text likewise.\n"
        )

    print(f"wrote {path}")
    print(f"  micro-interventions: {len(th.MICRO_TH)} | workshops: {len(th.WORKSHOP_TH)} | "
          f"framework proposed/unmapped: {len(proposed)}/{len(unmapped)}")


if __name__ == "__main__":
    main()
