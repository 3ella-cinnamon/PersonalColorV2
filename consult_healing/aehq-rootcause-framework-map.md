# AEHQ — Answer-Path Analysis & Root-Cause → Healing-Framework Map
## Companion Report to Design Doc v1.0

**What this report does:** enumerates every path a user's answers can take through the AEHQ, classifies the *root-cause patterns* those answers can reveal, and maps each pattern to healing frameworks with trial-level evidence wherever it exists. Example of the mapping logic (per your spec): *root cause = perfectionism → framework = graded small goals + CBT-for-perfectionism* — fully expanded in Case W1 below.

**Method honesty (the "no guessing" rule applied to itself):**
1. Root-cause classification from questionnaire answers is a **hypothesis, never a diagnosis**. A single answer pattern is probabilistic evidence. The system therefore always runs a **confirmation step** — it proposes the pattern back to the user as a question ("Does this fit: the pressure seems to come from a standard of *perfect or worthless* — is that close?") before serving any framework module. This is collaborative empiricism, the standard epistemic stance of CBT (Beck, 1979).
2. Every framework listed carries its strongest available evidence (meta-analysis > RCT > controlled study) and an honesty tier. Where a popular framework has thin evidence (e.g., imposter-phenomenon interventions), the report says so instead of upgrading it.
3. Frameworks are delivered as **self-help scale techniques** inside the app; the report marks which cases exceed self-help scope and must route to referral.

---

## 1. Complete Path Map

Structurally, every session terminates in exactly one of these paths:

```
PATH A  Crisis exit ............ triage Yes/Not-sure OR keyword hit → resources, no questionnaire
PATH B  Grounding-pause exit ... SUDS ≥8 persists after 2 grounding rounds → pause + support
PATH C  Content paths .......... scenario (6) × track (S/D/R) = 18 base paths
          ± rumination modifier (forces D, caps length)
          ± avoidance modifier (demotes depth, choice format)
PATH E  Closure outcomes ....... delta improved / unchanged / worsened (worsened → grounding + resources)
```

Base terminal-path count: 2 exits + 18 content paths × 3 closure outcomes = **56 structural paths**. Inside Path C, the *content* of answers (Stage 4 appraisal + Stage 5 need items) classifies into the **26 root-cause cases** below (G1–G4, C1–C4, W1–W4, S1–S4, U1–U4, X1–X6). These cases, not the structural paths, are what the healing layer responds to.

**Which answers do the classifying:** primarily the T-items (appraisal: "what does it mean about you") and N-items (unmet need), plus the emotion words chosen in Stage 3b, plus behavioral flags. Each case row below lists its trigger signals explicitly, so the logic is auditable.

---

## 2. Scenario Case Tables

Column key: **Signals** = concrete answer patterns that raise the hypothesis · **Framework** = evidence-based approach the app draws techniques from · **In-app technique** = what the user actually receives · **Tier** = evidence honesty rating (A meta-analysis/RCT · B controlled/mechanistic · C framework/consensus).

### 2.1 Loss / Grief

| Case | Signals in answers | Root-cause hypothesis | Framework(s) | In-app technique | Key evidence | Tier |
|------|--------------------|----------------------|--------------|------------------|--------------|------|
| G1 | Pain comes in waves; still functioning; mixed words (yearning + calm moments) | **Normal oscillating grief** — not a pathology | Dual Process Model of grief; expressive writing | Psychoeducation: healthy grief *oscillates* between loss-focus and restoration-focus — the good days are not betrayal; scheduled writing prompts | Stroebe & Schut (1999), *Death Studies*; Frattaroli (2006) meta-analysis | B / A |
| G2 | "Relief-with-guilt" chosen; "should have" language; self-blame in appraisal item | **Guilt-dominant grief** | Cognitive restructuring + self-compassion | Evidence-audit prompts on the guilt thought; adapted self-compassion break | Beck (1979) cognitive therapy foundations; Neff & Germer (2013) MSC randomized trial, *Journal of Clinical Psychology* | B / A |
| G3 | "Numb / nothing at all"; avoids reminders; short answers on loss items | **Avoidant grief** | Graded approach + behavioral activation + expressive writing (gentle dosing) | One small approach act per week (photo, place, song); BA-style activity scheduling for withdrawn users | Dimidjian et al. (2006), *JCCP*; Ekers et al. (2014) BA meta-analysis, *PLoS ONE* | A |
| G4 | Loss > 12 months ago AND yearning dominant AND daily functioning impaired | **Possible prolonged grief** — exceeds self-help scope | Prolonged/complicated grief therapy (specialist) | **Referral path**: warm explanation that targeted grief therapy has strong trial support, encourage professional contact | Shear et al. (2005) RCT, *JAMA* — complicated-grief treatment outperformed standard IPT | A (for referral rationale) |

### 2.2 Interpersonal Conflict

| Case | Signals | Root-cause hypothesis | Framework(s) | In-app technique | Key evidence | Tier |
|------|---------|----------------------|--------------|------------------|--------------|------|
| C1 | "Unheard / dismissed" chosen; need = "to be heard"; replays trying to explain | **Voice suppressed — assertion deficit** | Assertiveness / communication training | Scripted DEAR-style assertion template; rehearsal prompt for one sentence stating the need without accusation | Speed, Goldstein & Goldfried (2018) evidence review, *Clinical Psychology: Science & Practice* | B |
| C2 | Anger words dominant; appraisal blames other's character; body = hot/tight | **Anger-dominant processing** | CBT anger management + self-distancing | Fly-on-the-wall replay (already in D-track); cognitive reappraisal of the "they did it *to* me" appraisal; time-out rule | Beck & Fernandez (1998) meta-analysis of CBT for anger, *Cognitive Therapy & Research*; Kross et al. (2014) | A / B |
| C3 | R-track answer: "this exact pattern has appeared before" with multiple people | **Recurring relational pattern** | Interpersonal-therapy (IPT) framing | Pattern-mapping worksheet: same feeling, different faces — what's the common trigger and common move; suggest IPT-informed counseling if pattern is long-standing | Cuijpers et al. (2011) IPT meta-analysis, *American Journal of Psychiatry* | A (IPT) / C (self-help transfer) |
| C4 | Fly-on-wall item reveals fear under anger ("afraid of losing them / not mattering") | **Hurt-behind-anger; attachment threat** | Emotion-focused framing + repair behaviors | Name the primary emotion under the secondary anger; one-sentence repair opener drafted (not sent) with user consent | Kross et al. (2014) distancing evidence; Gottman's repair-attempt observational research | B / C |

### 2.3 Work / Study Overwhelm

| Case | Signals | Root-cause hypothesis | Framework(s) | In-app technique | Key evidence | Tier |
|------|---------|----------------------|--------------|------------------|--------------|------|
| **W1** | Fill-in-blank = "…it means I am a failure / not enough"; dread of *evaluation* not volume; all-or-nothing words | **Maladaptive perfectionism** (your worked example) | ① CBT for perfectionism ② Goal-setting theory — *small, specific, proximal goals* ③ Implementation intentions | Shrink the goal: replace "finish the project" with one 25-minute, criterion-defined sub-goal; "good-enough" standard written by the user; if-then plan for the first 2 minutes | ① Egan, Wade & Shafran (2011) review, *Clinical Psychology Review* — perfectionism is transdiagnostic and treatable with CBT; ② Locke & Latham (2002), *American Psychologist* — specific proximal goals outperform vague ones; Bandura & Schunk (1981), *JPSP* — proximal sub-goals build self-efficacy; ③ Gollwitzer (1999) | A / B |
| W2 | Telegraph list is objectively long; bottleneck = "time"; no self-worth appraisal attached | **Structural overload — the pile is real** | Job Demands–Resources model + problem-solving therapy + recovery science | Demand/resource audit (what can be dropped, delegated, renegotiated); PST 4-step on the single clenching item; protected recovery block (psychological detachment) | Bakker & Demerouti (2007), *Journal of Managerial Psychology*; Malouff, Thorsteinsson & Schutte (2007) PST meta-analysis, *Clinical Psychology Review*; Sonnentag & Fritz (2007) recovery experiences, *JOHP* | B / A / B |
| W3 | Bottleneck = "permission to say no"; resentment words; need = "control over my own life" | **Autonomy deficit / boundary collapse** | Assertiveness training + SDT autonomy restoration | One rehearsed no ("I can do A or B by Friday, not both — which?"); track the fear-prediction vs. actual outcome | Speed et al. (2018); Deci & Ryan (2000) | B / A-B |
| W4 | "Depleted + cynical + dread of tomorrow" cluster; low-arousal negative quadrant; weeks-long duration | **Burnout pattern** — partially exceeds self-help scope | Burnout research (exhaustion–cynicism–inefficacy) + BA + recovery; referral if persistent | Honest psychoeducation that burnout is situational, not a character flaw; recovery scheduling; **flag for professional/occupational-health referral if signals persist across ≥3 sessions** | Maslach, Schaufeli & Leiter (2001), *Annual Review of Psychology*; Ekers et al. (2014) | B / A |

### 2.4 Self-Criticism / Shame

| Case | Signals | Root-cause hypothesis | Framework(s) | In-app technique | Key evidence | Tier |
|------|---------|----------------------|--------------|------------------|--------------|------|
| S1 | Critic quote is harsh/contemptuous; "small, exposed, disgusted"; critic's voice "borrowed" from a past figure | **Shame-prone inner critic** | Compassion-Focused Therapy (CFT) + Mindful Self-Compassion (MSC) | Two-chair-style rewrite: critic's sentence re-spoken by an ideal compassionate figure; daily self-compassion micro-practice | Gilbert (2009) CFT, *Advances in Psychiatric Treatment*; Kirby, Tellegen & Steindl (2017) meta-analysis of compassion interventions, *Behavior Therapy*; Neff & Germer (2013) MSC RCT | A |
| S2 | Standard item reveals "perfect or worthless" rule; achievement-contingent self-worth | **Perfectionism-contingent self-worth** | Same stack as W1: CBT-P + small proximal goals + self-defined "good enough" | "Good enough, defined by you, in writing" (already an R-track item) becomes a standing standard; graded sub-goals | Egan, Wade & Shafran (2011); Locke & Latham (2002); Bandura & Schunk (1981) | A / B |
| S3 | "Fraudulent / exposed" chosen; fears being found out despite objective evidence of competence | **Imposter-phenomenon pattern** | Cognitive restructuring + evidence journaling. *Honesty note:* the imposter construct is well documented, but specific intervention trials are scarce — techniques are borrowed from general CBT (Tier B), not imposter-specific RCTs | Weekly "evidence the critic ignored" log (already SELF-S5); attributional retraining (success ← skill, not luck) | Clance & Imes (1978) original construct, *Psychotherapy*; Bravata et al. (2020) systematic review, *Journal of General Internal Medicine* — prevalence well-established, intervention evidence thin | B / C |
| S4 | Standards item answer: standard belongs to someone else ("my father's voice", "society") and user never agreed to it | **Internalized external standards** | ACT values clarification + cognitive defusion | Values sort: which standards survive when *chosen* freely; defusion phrasing ("I'm having the thought that I'm not enough") | Hayes, Luoma, Bond et al. (2006), *Behaviour Research & Therapy*; A-Tjak et al. (2015) ACT meta-analysis, *Psychotherapy and Psychosomatics* | A |

### 2.5 Uncertainty / Future Anxiety

| Case | Signals | Root-cause hypothesis | Framework(s) | In-app technique | Key evidence | Tier |
|------|---------|----------------------|--------------|------------------|--------------|------|
| U1 | Need item = "certainty"; worry spans many domains; "I can't stand not knowing" language | **Intolerance of uncertainty (IU)** | IU-targeted CBT + behavioral experiments | Graduated "uncertainty exposure": deliberately leave one small thing unchecked/undecided, record predicted vs. actual outcome | Dugas & Ladouceur (2000), *Behavior Modification* — IU as the treatment target in GAD; Hebert & Dugas (2019) protocol update, *Cognitive and Behavioral Practice* | B (self-help scale) / A (full protocol) |
| U2 | Worry visits at fixed idle times; user reports worrying "all day"; worry is the *habit*, content rotates | **Worry as uncontrolled process** | Stimulus control / worry postponement + worry-outcome journaling | Scheduled 15-min "worry window"; log each worry's actual outcome — most never materialize, and seeing that base-rate is itself the intervention | Borkovec, Wilkinson, Folensbee & Lerman (1983), *Behaviour Research & Therapy*; LaFreniere & Newman (2020), *Behavior Therapy* — 91% of logged worries did not come true | B |
| U3 | R-track: decisions postponed "until I feel certain"; cost-of-waiting item shows mounting cost | **Decision paralysis** | Problem-solving therapy + ACT committed action | PST 4-step on the smallest postponed decision; "experiment that replaces one assumption with one fact" (already UNC-R2) | Malouff et al. (2007) PST meta-analysis; A-Tjak et al. (2015) | A |
| U4 | Need item = "confidence I could cope"; past-coping recall comes up empty or dismissed | **Low coping self-efficacy** | Self-efficacy building (mastery experiences) | Mastery ladder: recall + log of past coped-with events; one small deliberately-completed challenge per week | Bandura (1997), *Self-Efficacy: The Exercise of Control*; Bandura & Schunk (1981) | B |

### 2.6 Cross-Cutting Cases (any scenario — triggered by flags & patterns, not scenario choice)

| Case | Signals | Root-cause hypothesis | Framework(s) | In-app technique | Key evidence | Tier |
|------|---------|----------------------|--------------|------------------|--------------|------|
| X1 | rumination_flag (repetition, "why/if-only" density, falling concreteness) | **Ruminative processing style** | Rumination-Focused CBT + concreteness training + distancing | Concreteness drill (exact time, place, next physical step); temporal-distance item; session cap | Watkins et al. (2011) RF-CBT RCT, *British Journal of Psychiatry*; Watkins, Baeyens & Read (2009) concreteness training, *Journal of Abnormal Psychology*; Kross et al. (2014) | A / B |
| X2 | LN-quadrant persists ≥3 sessions; "numb, empty, drained"; activity narrowing mentioned | **Withdrawal / anhedonic pattern** | Behavioral Activation | Micro-BA: one values-linked activity scheduled with if-then plan; monitor mood-after vs. mood-before | Jacobson et al. (1996), *JCCP* component analysis; Ekers et al. (2014) meta-analysis; Dimidjian et al. (2006) | A |
| X3 | avoidance_flag recurrent across sessions; skips cluster on emotion items specifically | **Experiential avoidance** | ACT (acceptance + defusion) | Willingness dial: "could you let the feeling be here 10 more seconds?"; choice-format items maintained (never forced exposure) | Hayes et al. (2006); A-Tjak et al. (2015) meta-analysis | A |
| X4 | SUDS ≥8 at *every* session start; body = "buzzing/tight" always | **Chronic hyperarousal** | Slow-breathing training + applied relaxation | Daily 5-min paced-breathing habit (not just in-session); applied-relaxation progression | Zaccaro et al. (2018) systematic review; Öst (1987) applied relaxation, *Behaviour Research & Therapy* | B |
| X5 | "Lonely" chosen repeatedly; need = connection; no named person in "who met this need" item | **Loneliness with negative social expectancies** | Social-cognition-targeted intervention (the component meta-analysis found most effective) | Prediction log for social contact (expected vs. actual reception); one low-stakes contact per week | Masi, Chen, Hawkley & Cacioppo (2011) meta-analysis, *Personality and Social Psychology Review* — targeting maladaptive social cognition beat skills/support/access interventions | A |
| X6 | Any crisis signal; or G4/W4-level impairment persisting despite use | **Beyond self-help scope** | Professional referral — always available, never gated | Warm handoff language; local resources; framing that referral is the *evidence-based* next step, not failure | Non-negotiable design rule (see design doc §9) | — |

---

## 3. Framework Glossary (one-line summaries + primary citation)

| Framework | Core mechanism | Primary evidence |
|-----------|---------------|------------------|
| CBT for perfectionism | Loosen rigid, self-worth-contingent standards via behavioral experiments and cognitive restructuring | Egan, Wade & Shafran (2011), *Clin. Psych. Review* |
| Goal-setting theory (small goals) | Specific + proximal + attainable goals outperform vague ones; sub-goals build efficacy | Locke & Latham (2002); Bandura & Schunk (1981) |
| Implementation intentions | If-then plans automate initiation, roughly doubling follow-through | Gollwitzer (1999); Gollwitzer & Sheeran (2006) meta-analysis, *Advances in Exp. Soc. Psych.* |
| Behavioral Activation (BA) | Re-engagement with reinforcing activity lifts mood; works without cognitive work | Jacobson et al. (1996); Ekers et al. (2014) meta |
| ACT | Acceptance + defusion + values reduce experiential avoidance | Hayes et al. (2006); A-Tjak et al. (2015) meta |
| Compassion-Focused Therapy / MSC | Activate soothing/affiliative system against shame | Gilbert (2009); Kirby et al. (2017) meta; Neff & Germer (2013) RCT |
| Rumination-Focused CBT | Shift abstract-evaluative processing to concrete-experiential | Watkins et al. (2011) RCT |
| Problem-Solving Therapy | Structured define→generate→choose→test loop for actionable stressors | Malouff et al. (2007) meta |
| Assertiveness training | Behavioral rehearsal of direct need-expression | Speed et al. (2018) review |
| IU-targeted CBT | Tolerance of uncertainty built via graduated exposure to not-knowing | Dugas & Ladouceur (2000) |
| Worry postponement / outcome logging | Stimulus control + base-rate correction of feared outcomes | Borkovec et al. (1983); LaFreniere & Newman (2020) |
| Dual Process Model (grief) | Normalizes oscillation between loss- and restoration-orientation | Stroebe & Schut (1999) |
| Applied relaxation / slow breathing | Parasympathetic activation lowers baseline arousal | Öst (1987); Zaccaro et al. (2018) |
| Self-efficacy building | Mastery experiences are the strongest efficacy source | Bandura (1997) |
| Social-cognition loneliness work | Corrects hostile/rejecting expectancy bias | Masi et al. (2011) meta |
| Expressive writing | Structured emotional disclosure improves psych/physical outcomes | Pennebaker & Beall (1986); Frattaroli (2006) meta |

## 4. Delivery Protocol (how a case becomes an intervention)

1. **Detect** — signals accumulate in the session state (per tables above; thresholds auditable).
2. **Confirm** — system reflects the hypothesis as a question; user can reject it, which is logged and down-weights that classifier (collaborative empiricism — Beck, 1979).
3. **Dose small** — one technique, self-help scale, framed as an experiment with a measurable prediction (mirrors behavioral-experiment methodology).
4. **Measure** — technique adherence + next-session SUDS/quadrant feed the measurement plan (design doc §8).
5. **Escalate honestly** — G4, W4-persistent, X6, and any crisis signal route to referral; the app states plainly that stepped-up care is the evidence-based move (stepped-care logic: Bower & Gilbody, 2005, *British Journal of Psychiatry*).

## 5. References (added in this report; design-doc references still apply)

- A-Tjak, J. G., et al. (2015). A meta-analysis of the efficacy of ACT. *Psychotherapy and Psychosomatics, 84*(1).
- Bakker, A. B., & Demerouti, E. (2007). The Job Demands–Resources model. *Journal of Managerial Psychology, 22*(3).
- Bandura, A. (1997). *Self-Efficacy: The Exercise of Control.* Freeman.
- Bandura, A., & Schunk, D. H. (1981). Cultivating competence, self-efficacy, and intrinsic interest through proximal self-motivation. *JPSP, 41*(3).
- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin.
- Beck, R., & Fernandez, E. (1998). Cognitive-behavioral therapy in the treatment of anger: A meta-analysis. *Cognitive Therapy and Research, 22*(1).
- Borkovec, T. D., Wilkinson, L., Folensbee, R., & Lerman, C. (1983). Stimulus control applications to the treatment of worry. *Behaviour Research and Therapy, 21*(3).
- Bower, P., & Gilbody, S. (2005). Stepped care in psychological therapies. *British Journal of Psychiatry, 186*(1).
- Bravata, D. M., et al. (2020). Prevalence, predictors, and treatment of impostor syndrome: A systematic review. *Journal of General Internal Medicine, 35*(4).
- Clance, P. R., & Imes, S. A. (1978). The imposter phenomenon in high achieving women. *Psychotherapy: Theory, Research & Practice, 15*(3).
- Cuijpers, P., et al. (2011). Interpersonal psychotherapy for depression: A meta-analysis. *American Journal of Psychiatry, 168*(6).
- Dimidjian, S., et al. (2006). Randomized trial of behavioral activation, cognitive therapy, and antidepressant medication. *JCCP, 74*(4).
- Dugas, M. J., & Ladouceur, R. (2000). Treatment of GAD: Targeting intolerance of uncertainty. *Behavior Modification, 24*(5).
- Egan, S. J., Wade, T. D., & Shafran, R. (2011). Perfectionism as a transdiagnostic process. *Clinical Psychology Review, 31*(2).
- Ekers, D., et al. (2014). Behavioural activation for depression: An update of meta-analysis. *PLoS ONE, 9*(6).
- Gilbert, P. (2009). Introducing compassion-focused therapy. *Advances in Psychiatric Treatment, 15*(3).
- Gollwitzer, P. M., & Sheeran, P. (2006). Implementation intentions and goal achievement: A meta-analysis. *Advances in Experimental Social Psychology, 38*.
- Hebert, E. A., & Dugas, M. J. (2019). Behavioral experiments for intolerance of uncertainty. *Cognitive and Behavioral Practice, 26*(2).
- Jacobson, N. S., et al. (1996). A component analysis of cognitive-behavioral treatment for depression. *JCCP, 64*(2).
- Kirby, J. N., Tellegen, C. L., & Steindl, S. R. (2017). A meta-analysis of compassion-based interventions. *Behavior Therapy, 48*(6).
- LaFreniere, L. S., & Newman, M. G. (2020). Exposing worry's deceit. *Behavior Therapy, 51*(3).
- Locke, E. A., & Latham, G. P. (2002). Building a practically useful theory of goal setting. *American Psychologist, 57*(9).
- Malouff, J. M., Thorsteinsson, E. B., & Schutte, N. S. (2007). The efficacy of problem solving therapy: A meta-analysis. *Clinical Psychology Review, 27*(1).
- Masi, C. M., Chen, H.-Y., Hawkley, L. C., & Cacioppo, J. T. (2011). A meta-analysis of interventions to reduce loneliness. *Personality and Social Psychology Review, 15*(3).
- Maslach, C., Schaufeli, W. B., & Leiter, M. P. (2001). Job burnout. *Annual Review of Psychology, 52*.
- Neff, K. D., & Germer, C. K. (2013). A pilot study and RCT of the Mindful Self-Compassion program. *Journal of Clinical Psychology, 69*(1).
- Öst, L.-G. (1987). Applied relaxation. *Behaviour Research and Therapy, 25*(5).
- Shear, K., Frank, E., Houck, P. R., & Reynolds, C. F. (2005). Treatment of complicated grief: A randomized controlled trial. *JAMA, 293*(21).
- Sonnentag, S., & Fritz, C. (2007). The Recovery Experience Questionnaire. *Journal of Occupational Health Psychology, 12*(3).
- Speed, B. C., Goldstein, B. L., & Goldfried, M. R. (2018). Assertiveness training: A forgotten evidence-based treatment. *Clinical Psychology: Science and Practice, 25*(1).
- Stroebe, M., & Schut, H. (1999). The dual process model of coping with bereavement. *Death Studies, 23*(3).
- Watkins, E. R., Baeyens, C. B., & Read, R. (2009). Concreteness training reduces dysphoria. *Journal of Abnormal Psychology, 118*(1).
- Watkins, E. R., et al. (2011). Rumination-focused CBT for residual depression: An RCT. *British Journal of Psychiatry, 199*(4).

*Citation note: as before, references are cited from established pre-2026 literature via model knowledge; verify volume/issue details against originals before external publication.*
