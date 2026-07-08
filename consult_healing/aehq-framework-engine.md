# AEHQ v2.1 — Framework-Selection Logic Engine
## Therapy-Informed Frameworks, Scoring Variables, and Mapping Rules (Product Spec)

**What this module does:** after the AEHQ questionnaire has produced scores and pattern flags, this engine selects **one** framework-informed technique (self-help dose), proposes it to the user as a confirmable hypothesis, and measures the result. It never stacks multiple frameworks in one session, never diagnoses, and never overrides the safety layer.

**Standing rules inherited from v2.0:** safety triage first (crisis → escalation script, session ends); the engine is guided self-reflection, not therapy; every selection decision below cites its evidence and carries an honesty tier (A meta-analysis/RCT · B controlled/mechanistic · C clinical framework — Tier C may only make the system more cautious, never deeper).

---

## 1. Framework Research Table (15 frameworks)

### F1 · CBT (Cognitive Behavioral Therapy)
- **Core idea:** distress follows appraisals, not events; identify and test the thought.
- **Best-fit pattern:** high anxiety/catastrophising; distorted appraisals ("it means I'm a failure"); moderate arousal.
- **Use when:** user can name a specific thought; SUDS ≤ 7; some cognitive distance available.
- **Don't use when:** SUDS ≥ 8 (no bandwidth for restructuring); high shame (disputing shame-thoughts often becomes new ammunition for the critic); numbness.
- **Risk if misused:** turns into arguing with yourself; invalidation ("just think differently").
- **Question style:** "What's the evidence for and against that sentence?" · "What would you tell a friend who believed this?"
- **Key papers:** Beck (1979); Butler et al. (2006) meta-analysis, *Clin. Psych. Review*; Hofmann et al. (2012) review of meta-analyses, *Cognitive Therapy & Research*. **Evidence: A**

### F2 · Behavioural Activation (BA)
- **Core idea:** mood follows behavior; re-engagement with reinforcing activity lifts affect without cognitive work first.
- **Best-fit pattern:** numbness/shutdown, withdrawal, low-arousal negative states, "nothing matters" flatness.
- **Use when:** activity narrowing detected; anhedonic language; works even when insight is low.
- **Don't use when:** the problem is acute conflict or a decision, not withdrawal; as a demand ("just do things") at SUDS ≥ 8.
- **Risk if misused:** becomes productivity pressure; reinforces "I failed at feeling better."
- **Question style:** "What's one 5-minute thing that used to give even 1% of something?" · scheduled micro-action.
- **Key papers:** Jacobson et al. (1996) component analysis, *JCCP*; Dimidjian et al. (2006), *JCCP*; Ekers et al. (2014) meta-analysis, *PLoS ONE*. **Evidence: A**

### F3 · CFT / Self-Compassion (Compassion-Focused Therapy, MSC)
- **Core idea:** shame and self-attack are threat-system responses; deliberately activating the soothing/affiliative system counteracts them.
- **Best-fit pattern:** high shame/self-attack; harsh inner critic; achievement-contingent self-worth.
- **Use when:** shame score high — **always before any cognitive or exposure work**; self-criticism scenario.
- **Don't use when:** user shows strong resistance to compassion ("I don't deserve it" spikes distress — "backdraft"); then dose at psychoeducation level only.
- **Risk if misused:** forced positive self-talk; compassion as another standard to fail at.
- **Question style:** "If your closest friend said those exact words about themselves, what's the first thing you'd feel toward them?"
- **Key papers:** Gilbert (2009), *Adv. Psychiatric Treatment*; Neff (2003); Neff & Germer (2013) RCT; Kirby et al. (2017) meta-analysis, *Behavior Therapy*; Leaviss & Uttley (2015) systematic review, *Psychological Medicine*. **Evidence: A**

### F4 · ACT (Acceptance & Commitment Therapy)
- **Core idea:** struggling against inner experience (experiential avoidance) maintains suffering; acceptance + defusion + values-based action.
- **Best-fit pattern:** avoidance flag; feeling trapped/people-pleasing; fused rules ("a good person never refuses").
- **Use when:** avoidance is the maintaining loop; values conflict detected; chronic "shoulds."
- **Don't use when:** acute crisis; user needs concrete problem-solving for a solvable external problem (acceptance of the solvable is misapplication).
- **Risk if misused:** "acceptance" heard as resignation ("tolerate the intolerable"), especially in genuinely harmful situations.
- **Question style:** "Could you let the feeling be here 10 more seconds?" · "If the fear had no vote, what would you choose?"
- **Key papers:** Hayes et al. (2006), *Behaviour Research & Therapy*; A-Tjak et al. (2015) meta-analysis, *Psychotherapy & Psychosomatics*. **Evidence: A**

### F5 · DBT skills (distress tolerance + emotion regulation)
- **Core idea:** intense emotion needs skills-first regulation (breathe, orient, temperature, paced activity) before any meaning-making.
- **Best-fit pattern:** SUDS 8–10; emotion storms; urge-driven states.
- **Use when:** high arousal gates everything — AEHQ's grounding module is DBT/breathing-informed.
- **Don't use when:** as a substitute for ever processing content (skills forever, reflection never).
- **Risk if misused:** suppression framing ("make it go away") instead of regulation framing ("ride it down").
- **Question style:** instructions, not questions: "In for 4, out for 6, 8 rounds. Then we check the number again."
- **Key papers:** Linehan (1993) skills manual; Linehan et al. (2006) RCT, *Archives of General Psychiatry*. **Evidence: A** (full DBT for BPD); **B/C** for isolated skills transfer to general users — labeled honestly.

### F6 · Emotion-Focused Therapy (EFT)
- **Core idea:** distinguish primary emotion (the first, adaptive signal — often hurt/fear) from secondary emotion (the cover — often anger); access the primary to process it.
- **Best-fit pattern:** anger-hidden-hurt; "furious but wounded underneath"; conflict scenarios.
- **Use when:** anger words + attachment-threat content co-occur; the "one second before the anger" probe lands.
- **Don't use when:** SUDS ≥ 8 (uncovering primary emotion raises intensity first); user hasn't consented to go under the anger.
- **Risk if misused:** stripping someone's armor without their consent; premature vulnerability.
- **Question style:** "What happened one second before the anger arrived?" · "If the anger could say 'It hurt when…', how does the sentence end?"
- **Key papers:** Greenberg (2002) *Emotion-Focused Therapy*, APA; Greenberg & Watson (2006) EFT for depression trials. **Evidence: B/A** (depression trials exist; self-help transfer is B).

### F7 · Schema Therapy (light: pattern-recognition use only)
- **Core idea:** repeated life patterns ("schemas" like abandonment, defectiveness, subjugation) formed early and re-triggered now.
- **Best-fit pattern:** "this exact feeling keeps happening with different people" — recurring relational patterns.
- **Use when:** R-track only; user themselves notices repetition across relationships/situations. In-app scope = *naming the pattern*, nothing more.
- **Don't use when:** anything beyond pattern-naming — schema work proper is long-term, therapist-led. **This is the engine's hardest scope limit.**
- **Risk if misused:** amateur archaeology of childhood; distress without containment.
- **Question style:** "Has this exact feeling appeared before with different people? What's the common shape?" — then, if yes: referral suggestion for pattern work.
- **Key papers:** Young, Klosko & Weishaar (2003) *Schema Therapy*; Giesen-Bloo et al. (2006) RCT, *Archives of General Psychiatry*. **Evidence: A** (therapist-led, BPD); **C** for self-help — hence pattern-naming-only scope.

### F8 · Somatic Grounding
- **Core idea:** regulate through the body — breath, orientation, sensory contact — when words aren't available.
- **Best-fit pattern:** numbness/shutdown; SUDS 8–10; "nowhere—numb" body answers.
- **Use when:** always first for numbness and high arousal; the only track that never requires feelings-talk.
- **Don't use when:** as the *only* intervention forever (regulation without any reflection stalls).
- **Risk if misused:** breath-focus can spike panic in some users — always offer eyes-open, external-anchor alternative.
- **Question style:** micro-instructions: "Hold the warm cup 30 seconds. Just notice warm."
- **Key papers:** Zaccaro et al. (2018) systematic review of slow breathing, *Frontiers in Human Neuroscience* (**B**); Gross (1998, 2015) attentional deployment mechanism (**B**); grounding packaging itself **C** — used only cautiously, consistent with the Tier-C rule.

### F9 · MBCT (Mindfulness-Based Cognitive Therapy)
- **Core idea:** observe thoughts as passing events rather than facts; decenter from rumination loops.
- **Best-fit pattern:** rumination; relapse-prone low mood; "the thoughts run me."
- **Use when:** rumination score high but SUDS ≤ 7; user has some stability.
- **Don't use when:** acute crisis; recent trauma content (unguided mindfulness can intensify intrusions); SUDS ≥ 8.
- **Risk if misused:** meditation as avoidance; distress from unguided long sits.
- **Question style:** "Can you watch the thought go past like a train you don't board — for 30 seconds?"
- **Key papers:** Segal, Williams & Teasdale (2002); Kuyken et al. (2016) individual-patient-data meta-analysis, *JAMA Psychiatry*. **Evidence: A** (relapse prevention); micro-dose transfer **B**.

### F10 · Problem-Solving Therapy (PST)
- **Core idea:** for solvable external stressors: define → generate options → choose → test.
- **Best-fit pattern:** high problem-solving/control score — the stressor is real and actionable (workload, logistics, decisions).
- **Use when:** control-appraisal says "partly in my hands"; work overwhelm with genuine overload.
- **Don't use when:** the problem is grief, shame, or another emotion that cannot be "solved" — solving-mode there becomes avoidance.
- **Risk if misused:** emotional bypass ("let's fix it") when the user needed to be heard first — always validate before solving.
- **Question style:** "What's the smallest version of this problem we could actually act on this week?"
- **Key papers:** D'Zurilla & Nezu problem-solving model; Malouff, Thorsteinsson & Schutte (2007) meta-analysis, *Clin. Psych. Review*; Bell & D'Zurilla (2009) meta-analysis, *Clin. Psych. Review*. **Evidence: A**

### F11 · Behavioural Experiments
- **Core idea:** test a feared prediction against reality with a small, planned action; experience beats argument.
- **Best-fit pattern:** avoidance maintained by untested predictions ("if I say no, they'll leave"); relationship insecurity; people-pleasing.
- **Use when:** a concrete testable prediction exists and the user consents; readiness-for-depth ≥ medium.
- **Don't use when:** the prediction involves genuinely dangerous contexts (abusive relationships, precarious jobs) — reality-testing there is not safe; route to referral instead.
- **Risk if misused:** experiments in unsafe environments; "failed" experiments read as confirmation.
- **Question style:** "What do you predict happens if you ⟨small act⟩? Let's write the prediction down and check it after."
- **Key papers:** Bennett-Levy et al. (2004) *Oxford Guide to Behavioural Experiments*; embedded in CBT trial evidence (Butler et al., 2006). **Evidence: B** (as isolated component) / **A** (within CBT packages).

### F12 · Implementation Intentions
- **Core idea:** if–then plans pre-load the trigger–response link, roughly doubling follow-through.
- **Best-fit pattern:** universal closure tool; any case that ends in a tiny action.
- **Use when:** always at closure; the delivery vehicle for every other framework's micro-action.
- **Don't use when:** as the *whole* intervention for heavy emotional content (an if-then plan is not processing).
- **Risk if misused:** trivializing ("just make a plan") if used alone on grief or shame.
- **Question style:** "If ⟨trigger⟩, then I will ⟨2-minute action⟩."
- **Key papers:** Gollwitzer (1999), *American Psychologist*; Gollwitzer & Sheeran (2006) meta-analysis (k≈94), *Adv. Exp. Social Psych.* **Evidence: A**

### F13 · Narrative Therapy (externalization use only)
- **Core idea:** the person is not the problem; the problem is the problem. Externalizing ("the critic", "the worry") creates working distance.
- **Best-fit pattern:** fused self-descriptions ("I *am* worthless" vs. "the critic *says*…"); already implicitly used across AEHQ item phrasing.
- **Use when:** shame and rumination items — externalized phrasing is the default register.
- **Don't use when:** externalizing responsibility for actions the user actually needs to own (misuse turns it into deflection).
- **Risk if misused:** accountability leakage.
- **Question style:** "When did the critic first get hired? What does it claim its job is?"
- **Key papers:** White & Epston (1990) *Narrative Means to Therapeutic Ends*. **Evidence: C** as standalone (few RCTs — stated honestly); the externalization *mechanic* aligns with defusion evidence (A-Tjak et al., 2015, **A**).

### F14 · Grief Dual-Process + Meaning Reconstruction
- **Core idea:** healthy grief oscillates between loss-orientation and restoration-orientation; longer-term healing involves rebuilding meaning.
- **Best-fit pattern:** grief/meaning-loss score high; loss scenario.
- **Use when:** any grief content — normalization of oscillation is the first intervention; meaning items only on R-track.
- **Don't use when:** prolonged-grief signals (>12 months, yearning-dominant, impaired functioning) → referral, because targeted grief therapy outperforms general approaches.
- **Risk if misused:** pushing "meaning-making" too early reads as "find the silver lining" — a documented way to hurt grievers.
- **Question style:** "The good days are not betrayal — grief is supposed to oscillate. When did you last get a restoration hour?"
- **Key papers:** Stroebe & Schut (1999), *Death Studies*; Neimeyer (2001) *Meaning Reconstruction & the Experience of Loss*, APA; Shear et al. (2005) RCT, *JAMA*. **Evidence: B** (model) / **A** (referral pathway).

### F15 · Attachment-Based Model
- **Core idea:** relationship threat activates the attachment system (protest, clinging, checking); felt security calms it.
- **Best-fit pattern:** relationship-threat score high; reassurance-seeking loops; jealousy/abandonment fear.
- **Use when:** relationship insecurity scenario; reassurance-delay experiments; secure-friend reappraisal items.
- **Don't use when:** actual relationship danger (control, abuse) — insecurity there is signal, not distortion; route to support resources.
- **Risk if misused:** labeling a partner-detection system as pathology when the relationship is genuinely unsafe.
- **Question style:** "The alarm says 'they're leaving.' What's the alarm's actual track record?" · "What would your most secure friend bet is going on?"
- **Key papers:** Hazan & Shaver (1987), *JPSP*; Mikulincer & Shaver (2007) *Attachment in Adulthood*; Joiner & Metalsky (1995), *JPSP* (reassurance-seeking). **Evidence: B**

---

## 2. Scoring Variables — Definitions & Thresholds

All scores 0–10 unless noted. Computed from questionnaire answers (word choices, appraisal items, behavioral flags) — every input is auditable. Thresholds: **Low 0–3 · Med 4–6 · High 7–10.**

| Variable | What it measures | Computed from | High-score signals |
|----------|-----------------|---------------|--------------------|
| `SUDS` | Momentary intensity | Direct 0–10 rating (Wolpe, 1969), re-rated every 3 screens | ≥8 gates everything (DBT/grounding first) |
| `shame_selfattack` | Shame & self-criticism load | Shame-cluster words (ashamed, worthless, exposed, fraudulent, small, disgusted-with-myself) ×2 each; harsh critic quote present +2; self-blame appraisal +2 | Critic quote is contemptuous; worth = performance |
| `rumination` | Repetitive abstract processing | Repetition of same content ≥3 answers +4; "why/if-only/should-have" density (per 100 words) +1 each up to +4; falling concreteness +2 | Loops without new elements |
| `avoidance` | Experiential avoidance | Skips ×2 each; one-word answers after normal-length ones +2; deflection phrases +2 | "idk", "never mind", skip clusters |
| `anxiety_catastrophising` | Future-threat inflation | Anxiety-cluster words +2; worst-case imagery in answers +3; control-appraisal < 20% +2; "all day" worry +3 | Worst frame vivid, likelihood unexamined |
| `anger_hidden_hurt` | Secondary anger over primary hurt | Anger words AND (hurt/betrayed/unappreciated OR attachment content) both present +5; "one second before" item reveals hurt/fear +5 | Fury + wound co-occurring |
| `numbness_shutdown` | Affective shutdown | "Numb/empty/flat/nothing" words +3 each (cap 6); "nowhere—numb" body answer +2; activity narrowing +2 | Volume turned down, not up |
| `problem_control` | Solvability of the stressor | Control-appraisal ≥ 50% +4; stressor is external/logistic +3; user lists actionable items +3 | The pile is real and partly actionable |
| `relationship_threat` | Attachment-system activation | Insecurity words +2 each; checking/reassurance behavior reported +3; abandonment prediction +3 | "They're leaving" alarm active |
| `grief_meaningloss` | Loss & meaning disruption | Loss scenario +3; yearning/hollow words +2 each; "life going forward" appraisal disrupted +3 | Meaning structure broken, not just sad |
| `readiness_depth` | Capacity for deep work *now* | Inverse SUDS (10−SUDS)×0.4 + answer-length engagement ×0.3 + zero flags ×0.3 (0–10 composite) | High = R-track eligible; Low = choice-format, shallow |

Honesty note: these scoring weights are **design hypotheses built on evidenced constructs** (each variable's construct has literature; the exact weights do not). They ship with analytics (§ v2.0 measurement plan) so weights are tuned empirically, not by taste.

---

## 3. IF/THEN Mapping Logic

**Priority stack — evaluated top-down; first match wins the session's single framework slot:**

```
P0  crisis_flag                          → STOP + escalation script (always)
P1  SUDS ≥ 8                             → F5 DBT-informed grounding + F8 somatic; nothing else this session
P2  numbness_shutdown HIGH               → F8 somatic grounding (sensory, zero feelings-demand)
                                            + micro-F2 (BA, 5-minute dose); persistent ≥3 sessions → referral note
P3  shame_selfattack HIGH                → F3 CFT/self-compassion FIRST; F13 externalization phrasing;
                                            HARD RULE: no open free-writing, no thought-disputation (F1 blocked)
P4  anger_hidden_hurt HIGH               → F6 EFT primary/secondary sequence (with consent item first)
P5  grief_meaningloss HIGH               → F14 dual-process normalization; meaning items only if readiness_depth HIGH;
                                            prolonged-grief signals → referral
P6  relationship_threat HIGH             → F15 attachment-informed + reassurance-delay experiment (F11);
                                            safety check first: if control/abuse signals → resources, not experiments
P7  anxiety_catastrophising HIGH         → F1 CBT likelihood-check + worry postponement + F10 PST on controllable %
P8  rumination HIGH                      → self-distancing (Kross) + concrete "what" drill (F9 micro-dose if SUDS ≤ 7)
P9  problem_control HIGH (& emotion moderate) → F10 PST + F2 graded task + F12 if-then
P10 avoidance HIGH (as primary pattern)  → F4 ACT willingness micro-dose; choice-based items; depth −1
DEFAULT                                   → validation + labeling only (that alone is an evidenced intervention — R1)
ALWAYS AT CLOSURE                         → F12 implementation intention (the delivery vehicle, not the therapy)
```

**Conflict-resolution rules:**
1. **One framework per session.** Multiple HIGH scores → highest-priority wins; runner-up is queued and proposed next session ("Last time we worked on X; the answers also pointed at Y — want to look there today?").
2. **Shame trumps technique.** If `shame_selfattack` is HIGH, any other selected framework runs *through* compassionate phrasing (e.g., PST for work overwhelm gets CFT-toned copy).
3. **Confirm before serving.** The engine states its hypothesis as a question ("It sounds like the anger might be guarding something softer — close?"). User rejection down-weights that classifier and falls through to the next rule. (Collaborative empiricism — Beck, 1979.)
4. **Dose small, measure.** Every framework is delivered as one technique + one if–then + next-session re-check; framework switching requires data (score change), not novelty.

---

## 4. Scenario → Framework Mapping (10 AEHQ situations)

| # | Situation | Primary framework | Secondary | Explicitly avoid | Why (evidence anchor) |
|---|-----------|------------------|-----------|------------------|----------------------|
| 1 | Work overwhelm | F10 PST + F2 graded task | F1 CBT (if perfectionism appraisal), F12 | Pure acceptance work while the pile is solvable | Malouff 2007 (A); Ekers 2014 (A); Egan 2011 |
| 2 | Ignored / dismissed | F3 compassion for the sting + Williams-needs mapping | F11 small-voice experiment | Thought-disputation of "I don't matter" while shame HIGH | Williams 2007; Kirby 2017 (A) |
| 3 | Conflict with authority | F1 appraisal-sorting (unfairness vs. danger) + F11 prepared assertion | F10 | EFT uncovering at high SUDS | Edmondson 1999; Speed 2018 |
| 4 | Self-criticism / shame | **F3 CFT — always first** + F13 externalization | F4 values (whose standard?) | F1 disputation; open free-writing at SUDS ≥6 | Gilbert 2009; Kirby 2017 (A); Leaviss & Uttley 2015 |
| 5 | Future anxiety | F1 + worry postponement + F10 on controllable % | F4 (uncertainty willingness), F9 | Reassurance loops; certainty-promising | Borkovec 1983; LaFreniere & Newman 2020; Dugas 2000 |
| 6 | Grief / loss | F14 dual-process normalization | Meaning reconstruction (R-track only); F3 for guilt-grief | Silver-lining prompts; early meaning-pushing | Stroebe & Schut 1999; Neimeyer 2001; Shear 2005 (A, referral) |
| 7 | Anger hiding hurt | F6 EFT primary/secondary (consent-gated) | F3 for the hurt once surfaced; distancing | Anger suppression framing; armor-stripping without consent | Greenberg 2002; Kross 2014 |
| 8 | Emotional numbness | F8 somatic first | F2 micro-BA; granularity recovery items | Any "what do you FEEL" demand; depth of any kind early | Taylor et al. 1997; Ekers 2014 (A) |
| 9 | Relationship insecurity | F15 attachment-informed + reassurance-delay (F11) | F1 base-rate check of the alarm | Experiments if abuse/control signals; partner-blame framing | Mikulincer & Shaver 2007; Joiner & Metalsky 1995 |
| 10 | Trapped / can't say no | F4 ACT values + F11 boundary experiment | F12 two-step no; F3 for guilt | Compliance coaching; experiments in unsafe power contexts | Hayes 2006 (A); Bennett-Levy 2004; Speed 2018 |

---

## 5. Example Case Mapping (end-to-end trace)

**Input:** *"My boss ignored me again. I feel ashamed, angry, and unimportant."*

**Step 1 — Safety & intensity.** Triage: No. SUDS self-rated 6 → Standard track eligible; no P1 gate.

**Step 2 — Signal extraction.**
- Scenario: ignored/dismissed (#2) with authority overlap (#3).
- Emotion words: *ashamed* (+2 shame), *unimportant* (+2 shame — self-worth wording), *angry* (anger cluster).
- "Again" → repetition marker: rumination +2 (watch), possible schema-pattern probe queued for R-track only.
- Anger + status/attachment wound co-occurring → `anger_hidden_hurt` +5 pending the "one-second-before" item.

**Step 3 — Scores (illustrative):** `shame_selfattack` 7 (HIGH) · `anger_hidden_hurt` 6 (MED-HIGH, unconfirmed) · `rumination` 4 (MED) · `relationship_threat` 3 · `SUDS` 6.

**Step 4 — Priority stack runs.** P0 no · P1 no (SUDS 6) · P2 no · **P3 fires: shame HIGH → F3 CFT first.** F1-style disputation of "I don't matter" is explicitly blocked (would feed the critic); free-writing suppressed (SUDS 6 ≥ threshold in shame context).

**Step 5 — Confirm hypothesis.**
> "Two things seem to be happening at once: the sting of being overlooked, and a voice turning the sting into a verdict about you ('unimportant'). Is that close?"
- **Yes →** serve F3 dose: *"If your closest colleague was ignored in that meeting and called themselves unimportant, what's the first thing you'd feel toward them?"* + Williams-needs item (*"What got hit hardest — being seen, being taken seriously, or knowing you matter here?"*).
- **No →** down-weight shame classifier; fall to P4: consent-gated EFT probe (*"What happened one second before the anger arrived?"*).

**Step 6 — Queue, don't stack.** `anger_hidden_hurt` (P4) is queued: next session opens with *"Last time we cared for the sting. The anger might have something to say too — want to look?"*

**Step 7 — Closure.** If–then (F12): *"If the meeting replays in my head tonight, then I write one line: 'Being overlooked stung because mattering matters — that need is legitimate.'"* Re-rate SUDS; delta logged. If "again" repeats across ≥3 sessions with different depth attempts → pattern-naming item (F7-light) + suggestion that recurring workplace dynamics respond well to talking it through with a professional or trusted mentor.

**What the engine deliberately did NOT do:** dispute "I'm unimportant" head-on (shame rule), interpret the boss's motives (unverifiable), stack CFT + EFT + CBT in one session (dose rule), or treat "again" as a schema conclusion (pattern work exceeds self-help scope).

---

## 6. Safety & Ethical Limits

1. **Escalation outranks everything** — crisis signals end the session with the warm handoff script (v2.0 §6); no framework logic runs after a crisis flag.
2. **Scope ceilings are explicit:** Schema Therapy = pattern-naming only; EFT = consent-gated; behavioral experiments = never in unsafe relationships/workplaces (abuse or retaliation signals → resources, not experiments); prolonged grief, persistent numbness, persistent burnout → referral scripts.
3. **No diagnosis, ever.** Scores select question styles; they are never shown as clinical labels. The user sees "it sounds like…" hypotheses they can reject.
4. **Rejection is data.** A rejected hypothesis down-weights the classifier — the system is built to be wrong gracefully.
5. **The weights are hypotheses.** Constructs are evidenced; exact thresholds ship with analytics and get tuned on outcomes (ΔSUDS, skip rates, rejection rates), consistent with measurement-based care (Fortney et al., 2017).
6. **Tier-C rule persists:** consensus-only frameworks may only add caution (gates, referrals), never depth.

## 7. References (added in v2.1; earlier reference lists still apply)

- Bell, A. C., & D'Zurilla, T. J. (2009). Problem-solving therapy for depression: A meta-analysis. *Clinical Psychology Review, 29*(4).
- Butler, A. C., Chapman, J. E., Forman, E. M., & Beck, A. T. (2006). The empirical status of cognitive-behavioral therapy: A review of meta-analyses. *Clinical Psychology Review, 26*(1).
- Giesen-Bloo, J., et al. (2006). Outpatient psychotherapy for borderline personality disorder: RCT of schema-focused therapy vs transference-focused psychotherapy. *Archives of General Psychiatry, 63*(6).
- Greenberg, L. S. (2002). *Emotion-Focused Therapy: Coaching Clients to Work Through Their Feelings.* APA.
- Greenberg, L. S., & Watson, J. C. (2006). *Emotion-Focused Therapy for Depression.* APA.
- Hofmann, S. G., Asnaani, A., Vonk, I. J., Sawyer, A. T., & Fang, A. (2012). The efficacy of CBT: A review of meta-analyses. *Cognitive Therapy and Research, 36*(5).
- Kuyken, W., et al. (2016). Efficacy of MBCT in prevention of depressive relapse: An individual patient data meta-analysis. *JAMA Psychiatry, 73*(6).
- Leaviss, J., & Uttley, L. (2015). Psychotherapeutic benefits of compassion-focused therapy: A systematic review. *Psychological Medicine, 45*(5).
- Linehan, M. M. (1993). *Skills Training Manual for Treating Borderline Personality Disorder.* Guilford.
- Linehan, M. M., et al. (2006). Two-year RCT of DBT vs therapy by experts for suicidal behaviors and BPD. *Archives of General Psychiatry, 63*(7).
- Neimeyer, R. A. (Ed.) (2001). *Meaning Reconstruction and the Experience of Loss.* APA.
- Segal, Z. V., Williams, J. M. G., & Teasdale, J. D. (2002). *Mindfulness-Based Cognitive Therapy for Depression.* Guilford.
- White, M., & Epston, D. (1990). *Narrative Means to Therapeutic Ends.* Norton.
- Young, J. E., Klosko, J. S., & Weishaar, M. E. (2003). *Schema Therapy: A Practitioner's Guide.* Guilford.

(Plus, carried from v2.0: Beck 1979; Jacobson 1996; Dimidjian 2006; Ekers 2014; Gilbert 2009; Neff 2003; Neff & Germer 2013; Kirby 2017; Hayes 2006; A-Tjak 2015; Gollwitzer 1999; Gollwitzer & Sheeran 2006; Stroebe & Schut 1999; Shear 2005; Mikulincer & Shaver 2007; Hazan & Shaver 1987; Joiner & Metalsky 1995; Bennett-Levy 2004; Malouff 2007; Speed 2018; Borkovec 1983; LaFreniere & Newman 2020; Dugas & Ladouceur 2000; Williams 2007; Edmondson 1999; Greenberg references above; Taylor, Bagby & Parker 1997; Kross 2014; Bruehlman-Senecal & Ayduk 2015; Nolen-Hoeksema 2008; Watkins 2009, 2011; Zaccaro 2018; Wolpe 1969; Fortney 2017; Fitzpatrick 2017.)

*Citation note: cited from established pre-2026 literature via model knowledge — verify details against originals before external publication.*
