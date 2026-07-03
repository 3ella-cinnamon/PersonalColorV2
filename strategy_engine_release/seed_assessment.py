"""Seed the 10-question adaptive assessment tree into the database.

Run once (idempotent):
    python seed_assessment.py

Reset and re-seed:
    python seed_assessment.py --reset

Per-session question count: 10 (+ 1 optional safety item if PHQ-2 ≥ 3).
All questions, scale labels, routing rules, and citations stored in DB.
No question text lives in application code.

Path per session:
  L1_DOMAIN (Q1)
    → one of L2_WORK / L2_REL / L2_FAM / L2_SELF / L2_FRIENDS / L2_HEALTH / L2_MONEY (Q2)
      → L3_PHQ2  (Q3 + Q4)
        → [L3_SAFETY (Q*) — only if PHQ-2 total ≥ 3]
          → L3_GAD2  (Q5 + Q6)
            → L4_SHAME  (Q7)
              → one of Q8_BURNOUT / Q8_ATTACHMENT / Q8_NEGLECT / Q8_SHAME_SCHEMA / Q8_DEFAULT (Q8)
                → L5_SELF_COMPASSION  (Q9)
                  → L5_EMOTION_REG  (Q10)
                    → GENERATE_PROFILE
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from core.database import Base, SessionLocal, engine
from models.orm import (
    AssessmentAnswer,
    AssessmentNode,
    AssessmentOption,
    AssessmentProfile,
    AssessmentQuestion,
    AssessmentSession,
)

Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────────────────────────────────────
# Node definitions
#
# Each entry:
#   id           : str   — node key used as PK and in routing
#   type         : str   — single_select | scale_set | terminal
#   instrument   : str | None
#   label        : str   — heading shown to user
#   rationale    : str | None  — displayed with a (?) icon
#   evidence     : str | None  — citation for clinicians / export
#   trigger_warning : str | None
#   scale_labels : list | None
#   scale_values : list | None
#   scoring      : dict | None — stored as scoring_rules_json
#   questions    : list[dict]  — items within the node
#   options      : list[dict]  — choices for single_select nodes
#
# scoring dict keys:
#   cutoffs      : {range_str: {flag?, next?}}  — score-based routing
#   flag_routing : {flag_name: next_node_id, ..., default: node_id}
#                  — overrides cutoff next when present; uses accumulated flags
#   shame_cutoffs: {range_str: flag_name}  — secondary flag-only cutoffs (L4_SHAME)
# ─────────────────────────────────────────────────────────────────────────────

NODES: list[dict] = [

    # ── Q1: Domain selector ───────────────────────────────────────────────────
    {
        "id": "L1_DOMAIN",
        "type": "single_select",
        "instrument": None,
        "label": "Which area of your life feels heaviest right now?",
        "rationale": (
            "Selects the adaptive path — you will only be asked questions relevant "
            "to the domain you choose."
        ),
        "evidence": (
            "Lazarus RS, Folkman S (1984). Stress, Appraisal, and Coping. Springer. / "
            "Holmes TH, Rahe RH (1967). The Social Readjustment Rating Scale. "
            "J Psychosom Res. 11(2):213–218."
        ),
        "trigger_warning": None,
        "scale_labels": None,
        "scale_values": None,
        "scoring": None,
        "questions": [],
        "options": [
            {"id": "work",         "label": "Work",                    "next": "L2_WORK",    "flag": "domain_work"},
            {"id": "relationship", "label": "Romantic relationship",    "next": "L2_REL",     "flag": "domain_relationship"},
            {"id": "family",       "label": "Family",                  "next": "L2_FAM",     "flag": "domain_family"},
            {"id": "self",         "label": "Myself / my inner world", "next": "L2_SELF",    "flag": "domain_self"},
            {"id": "friends",      "label": "Friends / social",        "next": "L2_FRIENDS", "flag": "domain_friends"},
            {"id": "health",       "label": "Health",                  "next": "L2_HEALTH",  "flag": "domain_health"},
            {"id": "money",        "label": "Money / finances",        "next": "L2_MONEY",   "flag": "domain_money"},
        ],
    },

    # ── Q2a: Work — single-item burnout ──────────────────────────────────────
    {
        "id": "L2_WORK",
        "type": "scale_set",
        "instrument": "Single-item burnout (Dolan 2015)",
        "label": "Thinking about your work right now:",
        "rationale": (
            "A single burnout item correlates r = 0.85 with the full Maslach Burnout "
            "Inventory Emotional Exhaustion subscale. Research shows it captures 88% of "
            "high-burnout cases at a score of 5 or above on a 0–10 scale."
        ),
        "evidence": (
            "Dolan ED et al. (2015). Using a single item to measure burnout in family "
            "physicians: a valid and consistent approach. J Gen Intern Med. 30(5):582–587."
        ),
        "trigger_warning": None,
        "scale_labels": ["0 — Not at all", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10 — Completely"],
        "scale_values": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "scoring": {
            "cutoffs": {
                "0-4":  {"next": "L3_PHQ2"},
                "5-10": {"flag": "burnout_risk", "next": "L3_PHQ2"},
            }
        },
        "questions": [
            {"id": "BURNOUT_1", "text": "I feel burned out from my work."},
        ],
        "options": [],
    },

    # ── Q2b: Relationship — attachment anxiety ────────────────────────────────
    {
        "id": "L2_REL",
        "type": "scale_set",
        "instrument": "ECR-R item AX1 (Fraley 2000)",
        "label": "Thinking about close romantic relationships in general:",
        "rationale": (
            "The abandonment-worry item is the single highest-loading item on the "
            "attachment anxiety subscale of the ECR-R (factor loading λ = 0.89). "
            "It efficiently classifies anxious vs. secure/avoidant attachment."
        ),
        "evidence": (
            "Fraley RC, Waller NG, Brennan KA (2000). An item-response theory analysis "
            "of self-report measures of adult attachment. J Pers Soc Psychol. 78(2):350–365."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Strongly disagree", "2", "3", "4", "5", "6", "7 — Strongly agree"],
        "scale_values": [1, 2, 3, 4, 5, 6, 7],
        "scoring": {
            "cutoffs": {
                "1-4": {"next": "L3_PHQ2"},
                "5-7": {"flag": "anxious_attachment", "next": "L3_PHQ2"},
            }
        },
        "questions": [
            {"id": "ECR_AX1", "text": "I worry about being abandoned by the people I love."},
        ],
        "options": [],
    },

    # ── Q2c: Family — emotional neglect ──────────────────────────────────────
    {
        "id": "L2_FAM",
        "type": "scale_set",
        "instrument": "CTQ-SF item EN3 (Bernstein 2003)",
        "label": "Thinking about your childhood, before age 18:",
        "rationale": (
            "The CTQ-SF Emotional Neglect subscale item EN3 ('I felt loved') has the "
            "highest factor loading (0.87) for identifying emotional neglect in childhood. "
            "A low score on this reverse-scored item flags the emotional neglect construct."
        ),
        "evidence": (
            "Bernstein DP, Stein JA, Newcomb MD et al. (2003). Development and validation "
            "of a brief screening version of the Childhood Trauma Questionnaire. "
            "Child Abuse Negl. 27(2):169–190."
        ),
        "trigger_warning": "This question asks about your childhood. You can skip it if you prefer.",
        "scale_labels": ["1 — Never true", "2 — Rarely true", "3 — Sometimes true", "4 — Often true", "5 — Very often true"],
        "scale_values": [1, 2, 3, 4, 5],
        "scoring": {
            "cutoffs": {
                "1-2": {"flag": "emotional_neglect", "next": "L3_PHQ2"},
                "3-3": {"next": "L3_PHQ2"},
                "4-5": {"next": "L3_PHQ2"},
            }
        },
        "questions": [
            {"id": "CTQ_EN3", "text": "I felt loved.", "reverse": True},
        ],
        "options": [],
    },

    # ── Q2d: Self — self-esteem ───────────────────────────────────────────────
    {
        "id": "L2_SELF",
        "type": "scale_set",
        "instrument": "RSES item 9 (Rosenberg 1965)",
        "label": "How much do you agree with the following?",
        "rationale": (
            "RSES item 9 has the highest item-total correlation (r = 0.82) across "
            "53-nation validation, making it the single best standalone indicator of "
            "global self-esteem deficits."
        ),
        "evidence": (
            "Rosenberg M (1965). Society and the Adolescent Self-Image. Princeton University Press. / "
            "Schmitt DP, Allik J (2005). Simultaneous administration of the RSES in 53 nations. "
            "J Pers Soc Psychol. 89(4):623–642."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Strongly disagree", "2 — Disagree", "3 — Agree", "4 — Strongly agree"],
        "scale_values": [1, 2, 3, 4],
        "scoring": {
            "cutoffs": {
                "1-2": {"next": "L3_PHQ2"},
                "3-4": {"flag": "low_self_esteem", "next": "L3_PHQ2"},
            }
        },
        "questions": [
            {"id": "RSES_9", "text": "All in all, I am inclined to feel that I am a failure."},
        ],
        "options": [],
    },

    # ── Q2e: Friends — loneliness ─────────────────────────────────────────────
    {
        "id": "L2_FRIENDS",
        "type": "scale_set",
        "instrument": "UCLA Single-item loneliness (Hughes 2004)",
        "label": "How much do you agree with the following?",
        "rationale": (
            "The single-item loneliness measure correlates r = 0.82 with the full "
            "UCLA Loneliness Scale-3. It identifies the core loneliness experience "
            "— emotional isolation even in social settings."
        ),
        "evidence": (
            "Hughes ME, Waite LJ, Hawkley LC, Cacioppo JT (2004). A short scale for "
            "measuring loneliness in large surveys. Res Soc Work Pract. 14(4):472–485."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Not at all", "2", "3", "4", "5 — Very much"],
        "scale_values": [1, 2, 3, 4, 5],
        "scoring": {
            "cutoffs": {
                "1-3": {"next": "L3_PHQ2"},
                "4-5": {"flag": "social_isolation", "next": "L3_PHQ2"},
            }
        },
        "questions": [
            {"id": "UCLA_1", "text": "I feel lonely even when I am around other people."},
        ],
        "options": [],
    },

    # ── Q2f: Health — somatic stress ──────────────────────────────────────────
    {
        "id": "L2_HEALTH",
        "type": "scale_set",
        "instrument": "PHQ-15 somatic cluster (Kroenke 2002)",
        "label": "Over the past month:",
        "rationale": (
            "Somatic symptom burden mediates the anxiety-to-physical-illness relationship. "
            "The PHQ-15 somatic cluster identifies whether health stress is primarily "
            "physical or a somatic expression of psychological distress."
        ),
        "evidence": (
            "Kroenke K, Spitzer RL, Williams JBW (2002). The PHQ-15: Validity of a new "
            "measure for evaluating the severity of somatic symptoms. "
            "Arch Intern Med. 162(11):1277–1284."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Not at all", "2", "3", "4", "5 — Nearly every day"],
        "scale_values": [1, 2, 3, 4, 5],
        "scoring": {
            "cutoffs": {
                "1-3": {"next": "L3_PHQ2"},
                "4-5": {"flag": "somatic_stress", "next": "L3_PHQ2"},
            }
        },
        "questions": [
            {"id": "SOMATIC_1", "text": "My stress or worry has been showing up as physical symptoms — such as headaches, stomach problems, muscle tension, or fatigue."},
        ],
        "options": [],
    },

    # ── Q2g: Money — financial shame ──────────────────────────────────────────
    {
        "id": "L2_MONEY",
        "type": "scale_set",
        "instrument": "Financial shame item (Klontz 2011)",
        "label": "How much do you agree with the following?",
        "rationale": (
            "Financial shame (feeling like a failure or feeling ashamed about money) "
            "predicts avoidance, rumination, self-worth conflation with finances, and "
            "routes to the Failure / Defectiveness schema pathway."
        ),
        "evidence": (
            "Klontz B, Britt SL, Mentzer J, Klontz T (2011). Money beliefs and financial "
            "behaviors: Development of the Klontz Money Script Inventory. "
            "J Financ Ther. 2(1):1–21."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Not at all", "2", "3", "4", "5 — Completely"],
        "scale_values": [1, 2, 3, 4, 5],
        "scoring": {
            "cutoffs": {
                "1-3": {"next": "L3_PHQ2"},
                "4-5": {"flag": "financial_shame", "next": "L3_PHQ2"},
            }
        },
        "questions": [
            {"id": "FIN_SHAME_1", "text": "When I think about my financial situation, I feel ashamed or like a failure."},
        ],
        "options": [],
    },

    # ── Q3 + Q4: PHQ-2 — depression screen ───────────────────────────────────
    {
        "id": "L3_PHQ2",
        "type": "scale_set",
        "instrument": "PHQ-2 (Kroenke 2003)",
        "label": "Over the last 2 weeks, how often have you been bothered by the following?",
        "rationale": (
            "PHQ-2 detects major depressive disorder with 83% sensitivity and 92% "
            "specificity at a cutoff score of 3. Two items capture 97% of cases "
            "that the full PHQ-9 would identify at the same threshold."
        ),
        "evidence": (
            "Kroenke K, Spitzer RL, Williams JBW (2003). The Patient Health "
            "Questionnaire-2: Validity of a two-item depression screener. "
            "Med Care. 41(11):1284–1292."
        ),
        "trigger_warning": None,
        "scale_labels": ["0 — Not at all", "1 — Several days", "2 — More than half the days", "3 — Nearly every day"],
        "scale_values": [0, 1, 2, 3],
        "scoring": {
            "cutoffs": {
                "0-2": {"next": "L3_GAD2"},
                "3-6": {"flag": "phq2_elevated", "next": "L3_SAFETY"},
            }
        },
        "questions": [
            {"id": "PHQ_1", "text": "Little interest or pleasure in doing things"},
            {"id": "PHQ_2", "text": "Feeling down, depressed, or hopeless"},
        ],
        "options": [],
    },

    # ── Q* (safety): PHQ-9 item 9 — shown only if PHQ-2 ≥ 3 ─────────────────
    {
        "id": "L3_SAFETY",
        "type": "scale_set",
        "instrument": "PHQ-9 item 9 (Kroenke 2001)",
        "label": "One more question — please answer honestly. Your response is private.",
        "rationale": (
            "PHQ-9 item 9 screens for passive suicidal ideation. Any answer ≥ 1 triggers "
            "immediate display of crisis resources, regardless of total score. This is "
            "standard of care per APA (2022) suicide risk assessment guidelines."
        ),
        "evidence": (
            "Kroenke K, Spitzer RL, Williams JBW (2001). The PHQ-9: Validity of a brief "
            "depression severity measure. J Gen Intern Med. 16(9):606–613. / "
            "American Psychiatric Association (2022). Practice Guidelines for the "
            "Assessment and Treatment of Patients with Suicidal Behaviors."
        ),
        "trigger_warning": "If you are in immediate distress, please contact a crisis line.",
        "scale_labels": ["0 — Not at all", "1 — Several days", "2 — More than half the days", "3 — Nearly every day"],
        "scale_values": [0, 1, 2, 3],
        "scoring": {
            "cutoffs": {
                "0-0": {"next": "L3_GAD2"},
                "1-3": {"flag": "safety_triggered", "next": "L3_GAD2"},
            }
        },
        "questions": [
            {"id": "PHQ_9", "text": "Thoughts that you would be better off dead, or thoughts of hurting yourself in some way.", "safety": True},
        ],
        "options": [],
    },

    # ── Q5 + Q6: GAD-2 — anxiety screen ──────────────────────────────────────
    {
        "id": "L3_GAD2",
        "type": "scale_set",
        "instrument": "GAD-2 (Kroenke 2007)",
        "label": "Over the last 2 weeks, how often have you been bothered by the following?",
        "rationale": (
            "GAD-2 screens for generalised anxiety disorder with 86% sensitivity and 83% "
            "specificity at a cutoff of 3. Together the two items detect 86% of any "
            "anxiety disorder diagnosis."
        ),
        "evidence": (
            "Kroenke K, Spitzer RL, Williams JBW, Monahan PO, Löwe B (2007). Anxiety "
            "disorders in primary care: prevalence, impairment, comorbidity, and detection. "
            "Ann Intern Med. 146(5):317–325."
        ),
        "trigger_warning": None,
        "scale_labels": ["0 — Not at all", "1 — Several days", "2 — More than half the days", "3 — Nearly every day"],
        "scale_values": [0, 1, 2, 3],
        "scoring": {
            "cutoffs": {
                "0-2": {"next": "L4_SHAME"},
                "3-6": {"flag": "anxiety_elevated", "next": "L4_SHAME"},
            }
        },
        "questions": [
            {"id": "GAD_1", "text": "Feeling nervous, anxious, or on edge"},
            {"id": "GAD_2", "text": "Not being able to stop or control worrying"},
        ],
        "options": [],
    },

    # ── Q7: Core shame / defectiveness ───────────────────────────────────────
    {
        "id": "L4_SHAME",
        "type": "scale_set",
        "instrument": "ISS item 2 / YSQ Defectiveness (Cook 1994 · Young 1998)",
        "label": "How often do you experience the following?",
        "rationale": (
            "This item has the highest cross-instrument loading across the Internalized "
            "Shame Scale, YSQ Defectiveness/Shame schema, and RSES negative subscale. "
            "A single-item shame assessment using this item correlates r = 0.88 with the "
            "full ISS shame subscale."
        ),
        "evidence": (
            "Cook DR (1994). Internalized Shame Scale. Alcohol Treat Q. 12(2):197–211. / "
            "Young JE (1998). Young Schema Questionnaire – Short Form. Cognitive Therapy "
            "Center of New York. / Andrews B, Qian M, Valentine JD (2002). Predicting "
            "depressive symptoms with a new measure of shame: The Experience of Shame Scale. "
            "Br J Clin Psychol. 41(4):395–403."
        ),
        "trigger_warning": None,
        "scale_labels": ["0 — Never", "1 — Seldom", "2 — Sometimes", "3 — Often", "4 — Almost always"],
        "scale_values": [0, 1, 2, 3, 4],
        "scoring": {
            "shame_cutoffs": {
                "2-2": "moderate_shame",
                "3-4": "high_shame",
            },
            "flag_routing": {
                "priority": ["burnout_risk", "anxious_attachment", "emotional_neglect", "low_self_esteem", "financial_shame", "high_shame", "social_isolation"],
                "burnout_risk":       "Q8_BURNOUT",
                "anxious_attachment": "Q8_ATTACHMENT",
                "emotional_neglect":  "Q8_NEGLECT",
                "low_self_esteem":    "Q8_SHAME_SCHEMA",
                "financial_shame":    "Q8_SHAME_SCHEMA",
                "high_shame":         "Q8_SHAME_SCHEMA",
                "social_isolation":   "Q8_DEFAULT",
                "default":            "Q8_DEFAULT",
            },
        },
        "questions": [
            {"id": "ISS_2", "text": "I feel as though there is something fundamentally wrong with me as a person."},
        ],
        "options": [],
    },

    # ── Q8 variants — one selected by flag_routing in L4_SHAME ───────────────

    {
        "id": "Q8_BURNOUT",
        "type": "scale_set",
        "instrument": "YSQ-S3 Unrelenting Standards (Young 1998)",
        "label": "How well does the following describe you?",
        "rationale": (
            "Burnout combined with high shame points to the Unrelenting Standards schema "
            "as the likely core driver — a belief that high performance is required for "
            "self-worth. This is the highest-loading single item for this schema."
        ),
        "evidence": (
            "Young JE, Klosko JS, Weishaar ME (2003). Schema Therapy: A Practitioner's Guide. "
            "Guilford. / Rijkeboer MM, van den Bergh H (2006). Multiple group confirmatory "
            "factor analysis of the YSQ in a Dutch clinical versus non-clinical population. "
            "Cogn Ther Res. 30(3):263–278. Item factor loading: 0.82."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Completely untrue", "2", "3", "4", "5", "6 — Describes me perfectly"],
        "scale_values": [1, 2, 3, 4, 5, 6],
        "scoring": {
            "cutoffs": {
                "1-3": {"next": "L5_SELF_COMPASSION"},
                "4-6": {"flag": "unrelenting_standards_schema", "next": "L5_SELF_COMPASSION"},
            }
        },
        "questions": [
            {"id": "US_1", "text": "I must meet all my responsibilities — falling short even slightly is not acceptable."},
        ],
        "options": [],
    },

    {
        "id": "Q8_ATTACHMENT",
        "type": "scale_set",
        "instrument": "ECR-R item AX2 (Fraley 2000)",
        "label": "How well does the following describe you?",
        "rationale": (
            "Anxious attachment combined with shame points to the Abandonment / "
            "Defectiveness schema cluster. AX2 is the second highest-loading attachment "
            "anxiety item and distinguishes preoccupied from fearful attachment."
        ),
        "evidence": (
            "Fraley RC, Waller NG, Brennan KA (2000). J Pers Soc Psychol. 78(2):350–365. "
            "Item factor loading: 0.85 on attachment anxiety subscale."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Strongly disagree", "2", "3", "4", "5", "6", "7 — Strongly agree"],
        "scale_values": [1, 2, 3, 4, 5, 6, 7],
        "scoring": {
            "cutoffs": {
                "1-4": {"next": "L5_SELF_COMPASSION"},
                "5-7": {"flag": "abandonment_schema", "next": "L5_SELF_COMPASSION"},
            }
        },
        "questions": [
            {"id": "ECR_AX2", "text": "My desire to be very close to my partner sometimes scares them away."},
        ],
        "options": [],
    },

    {
        "id": "Q8_NEGLECT",
        "type": "scale_set",
        "instrument": "YSQ-S3 Approval-Seeking (Young 1998)",
        "label": "How well does the following describe you?",
        "rationale": (
            "Emotional neglect in childhood combined with current family stress points to "
            "the Approval-Seeking / Recognition-Seeking schema — where love and acceptance "
            "felt conditional on performance or compliance."
        ),
        "evidence": (
            "Young JE et al. (2003). Schema Therapy. Guilford. / "
            "Parker G, Tupling H, Brown LB (1979). A parental bonding instrument. "
            "Br J Med Psychol. 52(1):1–10. Conditional parental care is the strongest "
            "environmental predictor of this schema."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Completely untrue", "2", "3", "4", "5", "6 — Describes me perfectly"],
        "scale_values": [1, 2, 3, 4, 5, 6],
        "scoring": {
            "cutoffs": {
                "1-3": {"next": "L5_SELF_COMPASSION"},
                "4-6": {"flag": "approval_seeking_schema", "next": "L5_SELF_COMPASSION"},
            }
        },
        "questions": [
            {"id": "AS_1", "text": "I felt I had to be successful or pleasing to be loved — simply being myself was not enough."},
        ],
        "options": [],
    },

    {
        "id": "Q8_SHAME_SCHEMA",
        "type": "scale_set",
        "instrument": "FMPS item CM1 (Frost 1990)",
        "label": "How strongly do you agree with the following?",
        "rationale": (
            "Low self-esteem or high shame combined with perfectionism points to the "
            "Concern over Mistakes dimension — the most psychopathologically relevant "
            "perfectionism subscale. CM1 is the highest-loading item (factor loading 0.81)."
        ),
        "evidence": (
            "Frost RO, Marten P, Lahart C, Rosenblate R (1990). The dimensions of "
            "perfectionism. Cogn Ther Res. 14(5):449–468. / Stoeber J, Otto K (2006). "
            "Positive conceptions of perfectionism. Pers Soc Psychol Rev. 10(4):295–319."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Strongly disagree", "2", "3", "4", "5 — Strongly agree"],
        "scale_values": [1, 2, 3, 4, 5],
        "scoring": {
            "cutoffs": {
                "1-3": {"next": "L5_SELF_COMPASSION"},
                "4-5": {"flag": "maladaptive_perfectionism", "next": "L5_SELF_COMPASSION"},
            }
        },
        "questions": [
            {"id": "CM_1", "text": "If I fail partly, it is as bad as being a complete failure."},
        ],
        "options": [],
    },

    {
        "id": "Q8_DEFAULT",
        "type": "scale_set",
        "instrument": "YSQ-S3 Emotional Inhibition (Young 1998)",
        "label": "How well does the following describe you?",
        "rationale": (
            "When no strong domain-specific schema emerges, Emotional Inhibition is "
            "the most common underlying pattern — suppressing emotions to avoid perceived "
            "rejection or loss of control. It is highly prevalent in working adults."
        ),
        "evidence": (
            "Young JE et al. (2003). Schema Therapy. Guilford. / "
            "Gross JJ (2002). Emotion regulation: Affective, cognitive, and social "
            "consequences. Psychophysiology. 39(3):281–291."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Completely untrue", "2", "3", "4", "5", "6 — Describes me perfectly"],
        "scale_values": [1, 2, 3, 4, 5, 6],
        "scoring": {
            "cutoffs": {
                "1-3": {"next": "L5_SELF_COMPASSION"},
                "4-6": {"flag": "emotional_inhibition_schema", "next": "L5_SELF_COMPASSION"},
            }
        },
        "questions": [
            {"id": "EMIT_1", "text": "I suppress my emotions because expressing them might lead to rejection or make others uncomfortable."},
        ],
        "options": [],
    },

    # ── Q9: Self-compassion ───────────────────────────────────────────────────
    {
        "id": "L5_SELF_COMPASSION",
        "type": "scale_set",
        "instrument": "SCS-SF item SK1 (Neff 2003)",
        "label": "When you are going through something hard:",
        "rationale": (
            "Self-compassion (treating oneself with kindness during difficulty) is the "
            "primary protective factor against depression, anxiety, and burnout. "
            "SCS-SF item SK1 has the highest item-total correlation (r = 0.79) and "
            "is a stronger predictor of psychological health than mindfulness alone."
        ),
        "evidence": (
            "Neff KD (2003). The development and validation of a scale to measure "
            "self-compassion. Self Identity. 2(3):223–250. / Van Dam NT, Sheppard SC, "
            "Forsyth JP, Earleywine M (2011). Self-compassion is a better predictor of "
            "psychological health than mindfulness. Mindfulness. 2(4):288–294."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Almost never", "2", "3", "4", "5 — Almost always"],
        "scale_values": [1, 2, 3, 4, 5],
        "scoring": {
            "cutoffs": {
                "1-2": {"flag": "low_self_compassion",      "next": "L5_EMOTION_REG"},
                "3-3": {"flag": "moderate_self_compassion", "next": "L5_EMOTION_REG"},
                "4-5": {"next": "L5_EMOTION_REG"},
            }
        },
        "questions": [
            {"id": "SCS_SK1", "text": "I try to be understanding and patient with myself when I'm going through something difficult, rather than being self-critical."},
        ],
        "options": [],
    },

    # ── Q10: Emotion regulation ───────────────────────────────────────────────
    {
        "id": "L5_EMOTION_REG",
        "type": "scale_set",
        "instrument": "DERS Strategies item 6 (Gratz & Roemer 2004)",
        "label": "How often does the following apply to you?",
        "rationale": (
            "The Strategies subscale of DERS — specifically the belief that 'nothing will "
            "help when I'm upset' — has the strongest independent prediction of "
            "psychopathology across depression, anxiety, BPD, and PTSD in meta-analysis "
            "(effect sizes d = 0.63–0.89). It measures learned emotional helplessness."
        ),
        "evidence": (
            "Gratz KL, Roemer L (2004). Multidimensional assessment of emotion regulation "
            "and dysregulation. J Psychopathol Behav Assess. 26(1):41–54. / "
            "Aldao A, Nolen-Hoeksema S, Schweizer S (2010). Emotion-regulation strategies "
            "across psychopathology: A meta-analytic review. Clin Psychol Rev. 30(2):217–237."
        ),
        "trigger_warning": None,
        "scale_labels": ["1 — Almost never", "2 — Sometimes", "3 — About half the time", "4 — Most of the time", "5 — Almost always"],
        "scale_values": [1, 2, 3, 4, 5],
        "scoring": {
            "cutoffs": {
                "1-2": {"next": "GENERATE_PROFILE"},
                "3-3": {"flag": "moderate_ER_difficulty", "next": "GENERATE_PROFILE"},
                "4-5": {"flag": "poor_ER_strategies",     "next": "GENERATE_PROFILE"},
            }
        },
        "questions": [
            {"id": "DERS_6", "text": "When I'm upset, I believe there is nothing I can do to make myself feel better."},
        ],
        "options": [],
    },

    # ── Terminal ──────────────────────────────────────────────────────────────
    {
        "id": "GENERATE_PROFILE",
        "type": "terminal",
        "instrument": None,
        "label": "Your psychological stress profile is ready.",
        "rationale": None,
        "evidence": None,
        "trigger_warning": None,
        "scale_labels": None,
        "scale_values": None,
        "scoring": None,
        "questions": [],
        "options": [],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Seed function
# ─────────────────────────────────────────────────────────────────────────────

def seed(reset: bool = False) -> None:
    db = SessionLocal()
    try:
        if reset:
            print("Resetting assessment tables...")
            for tbl in [AssessmentAnswer, AssessmentProfile, AssessmentSession,
                        AssessmentQuestion, AssessmentOption, AssessmentNode]:
                db.query(tbl).delete()
            db.commit()
            print("  Done.")

        inserted = 0
        skipped = 0

        for node_def in NODES:
            if db.get(AssessmentNode, node_def["id"]):
                skipped += 1
                continue

            node = AssessmentNode(
                node_id=node_def["id"],
                node_type=node_def["type"],
                instrument=node_def.get("instrument"),
                label=node_def["label"],
                rationale=node_def.get("rationale"),
                evidence=node_def.get("evidence"),
                trigger_warning=node_def.get("trigger_warning"),
                scale_labels_json=json.dumps(node_def["scale_labels"]) if node_def.get("scale_labels") else None,
                scale_values_json=json.dumps(node_def["scale_values"]) if node_def.get("scale_values") else None,
                scoring_rules_json=json.dumps(node_def["scoring"]) if node_def.get("scoring") else None,
            )
            db.add(node)

            for i, q in enumerate(node_def.get("questions", [])):
                db.add(AssessmentQuestion(
                    node_id=node_def["id"],
                    question_id=q["id"],
                    text=q["text"],
                    subscale=q.get("subscale"),
                    reverse_scored=q.get("reverse", False),
                    safety_item=q.get("safety", False),
                    sort_order=i,
                ))

            for i, o in enumerate(node_def.get("options", [])):
                db.add(AssessmentOption(
                    node_id=node_def["id"],
                    option_id=o["id"],
                    label=o["label"],
                    next_node_id=o.get("next"),
                    flag=o.get("flag"),
                    sort_order=i,
                ))

            inserted += 1

        db.commit()

        total_q = sum(len(n.get("questions", [])) for n in NODES)
        total_o = sum(len(n.get("options", [])) for n in NODES)
        print(f"Inserted {inserted} nodes  |  skipped {skipped} existing")
        print(f"Total stored: {total_q} questions, {total_o} options across {len(NODES)} nodes")
        print("Max questions per session: 11 (10 + 1 safety if PHQ-2 ≥ 3)")

    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed 10-question adaptive assessment")
    parser.add_argument("--reset", action="store_true", help="Delete all assessment data and re-seed")
    args = parser.parse_args()
    seed(reset=args.reset)
