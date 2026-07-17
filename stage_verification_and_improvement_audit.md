# Stage-by-Stage Verification & Improvement Audit
## Companion to: Therapist Session Workflow Design (v1)

**Purpose:** For each session stage, verify what your existing project already covers, identify gaps, and apply targeted improvements.
**How to use:** For every stage, mark each Verify item as ✅ Present / 🟡 Partial / ❌ Missing in your project. Any 🟡/❌ maps to the listed Improve action. Items marked ⚠ are non-negotiable (safety/validity) — treat any ❌ there as a blocker.

**Legend of check types:** [C] content exists · [L] logic/branching exists · [M] measurement exists · [S] safety mechanism exists · [D] data captured for §7 storage/LLM plan

---

## S1 — Alliance, Intake & Informed Consent

**Verify in existing project:**
1. ⚠ [S] PHQ-9 item-9 (or equivalent) hard-interrupt exists and cannot be skipped or continued past.
2. ⚠ [C] Informed-consent content covers: confidentiality limits, data use, and a *separate* opt-in for LLM/training use (PDPA-compliant).
3. [M] Baseline battery present: RSES + SCS(-SF) + PHQ-9/GAD-7 + trauma screen — and Thai versions are the *validated* ones, not in-house translations.
4. [L] Trauma-screen answers actually set flags (`TRAUMA_COMPLEX`, `TRAUMA_HX`) that later stages read.
5. [C] Client goal captured in client's own words (free text), stored bilingually if entered in Thai.

**Improve:**
- If your intake is one long form, split it: rapport questions first, scales second (form-first intakes depress alliance and honesty).
- Add a "what brings you here in one sentence" field — it becomes the S12 outcome anchor and a high-value training label.
- If Thai scale versions are unverified → swap to Wongpakaran RSES-TH and Lotrakul PHQ-9-TH; log scale version IDs per record.

---

## S2 — Formulation & Psychoeducation

**Verify:**
1. [C] A visual/co-built formulation artifact exists (Bottom Line → Rules for Living → triggers → confirming behaviors) — not just therapist notes.
2. [C] Three-circles (threat/drive/soothing) psychoeducation exists in both languages, culturally reviewed.
3. [D] The elicited Bottom Line is stored as a structured field (it's referenced again in S5, S11, and follow-up).

**Improve:**
- If formulation lives only in free-text notes → convert to a structured template so S11's "New Bottom Line" can be diffed against it (powerful progress artifact + clean training pair).
- Add a belief-strength rating (0–100%) on the Bottom Line at S2; re-rate at S5, S11 — cheap, sensitive progress metric your project likely lacks.

---

## S3–S4 — Self-Awareness

**Verify:**
1. [C] Thought-record tool exists and is usable on mobile in < 60 seconds (adherence dies otherwise).
2. [C] Emotion-vocabulary support exists in Thai (Thai emotion lexicon differs; direct EN translation reads clinical/stiff).
3. [L] Top-3 trigger contexts are captured as structured tags, not prose — later branches and analytics need them.
4. [D] Each thought record stores {trigger tag, thought, emotion, intensity pre/post} — this is your richest LLM-training signal.

**Improve:**
- Replace 7-column CBT thought records with a 3-field quick capture (situation → critic said → I felt), expanding only in-session.
- Add a body-map input (tap where you feel it) — improves interoception work and engagement, especially for clients who can't verbalize emotion.

---

## S5 — Inner Critic

**Verify:**
1. [L] Branch C exists: the critic's *function* (driver / social-threat / internalized attacker) is asked and routes differently.
2. ⚠ [L] "Hated-self" pattern (FSCRS or the "I deserve it" answer) raises a supervision flag — verify the flag actually reaches a human.
3. [C] Two-chair / externalization protocol has a written script with therapist guidance, both languages.

**Improve:**
- If your project treats all self-criticism identically → this is likely its biggest clinical gap; implement Branch C before anything else.
- Add a "critic's protective intention" summary card the client keeps — reduces internal-war framing and improves S6 uptake.

---

## S6–S7 — Self-Compassion & Self-Love

**Verify:**
1. ⚠ [M] Fears of Compassion is measured (scale or the Q7 probe) *before* compassion practices start.
2. [L] Branch D routing exists: high fear-of-compassion → others-first → receiving → self-directed sequencing.
3. ⚠ [C] Backdraft psychoeducation exists (grief/pain surge is normal, slow down, not failure) with a visible "pause" pathway.
4. [C] Audio-guided soothing-breathing and compassionate-imagery exercises exist in Thai voice (not subtitled English).
5. [C] Optional (opt-in) metta-framed variant exists; default variant is secular.

**Improve:**
- If practices are text-only → add audio; compassion practices transfer poorly as reading material.
- Add post-practice 2-tap feedback (soothing 0–10 / any distress Y-N) → feeds Branch D pacing automatically and creates outcome-labeled training data.

---

## S8–S9 — Inner-Child / Rescripting (Gated)

**Verify:**
1. ⚠ [L] The entry gate (Branch E) is enforced in software/workflow, not just documented: safe-place demonstrated, SUD ≤ 6, no active risk flags, clinician sign-off when `TRAUMA_COMPLEX`.
2. ⚠ [S] In-session SUD checks (~every 5 min) with the abort path (SUD > 8 or dissociation → grounding → no re-entry that session).
3. ⚠ [C] Rescripting scripts contain zero suggestive memory content (false-memory safeguard) — audit every prompt line.
4. [L] "Child part refuses help" branch exists (IFS unblending path), not just the happy path.
5. [D] Session log stores SUD trajectory + completion status — required for the gate's re-check logic and safety auditing.

**Improve:**
- If your project has inner-child content without the gate → highest-priority fix; gate first, content second.
- Add the post-rescripting consolidation homework (letter from adult self to child self) with private-by-default storage.
- Add a pre-session grounding warm-up (2 min) as a fixed prefix to every S8–S9 session.

---

## S10 — Inner Power & Potential

**Verify:**
1. [C] Strengths inventory exists (VIA or structured strengths-spotting) — Thai VIA translation availability confirmed.
2. [C] Values clarification exercise exists and outputs a ranked/structured values list.
3. [L] Behavioral experiments are generated *from the client's Rules for Living captured in S2* — verify the linkage exists; generic experiment lists don't work.
4. [D] Experiment records store {rule targeted, prediction, outcome, learning} — classic CBT data structure and a gold training format.

**Improve:**
- If experiments aren't linked to S2 rules → add the linkage; it converts "positive activities" into belief-disconfirming evidence.
- Add a prediction-vs-outcome delta display to the client ("you predicted 90% rejection; actual: accepted") — one of the most persuasive UI moments in CBT tools.

---

## S11 — Integration & New Self-Narrative

**Verify:**
1. [C] New Bottom Line is drafted and stored beside the old one with belief % ratings for both.
2. [C] Evidence-log tool exists and persists *after* the therapy arc (client-owned).
3. [D] Old→new belief pair + evidence entries are stored bilingually with alignment IDs (§7 model).

**Improve:**
- Add a narrative re-authoring exercise ("the story I used to tell / the story I'm building") — strong closure artifact and rich, consented training text.
- Show the S2→S11 measure trajectory to the client in-session; visible change consolidates identity shift.

---

## S12 — Relapse Prevention & Closure

**Verify:**
1. [C] Blueprint template exists (learned / warning signs / tools / plan) as a living, editable, bilingual document.
2. [L] Booster schedule (2w / 1m / 3m / 6m) is automated with the re-entry rule (≥ 2 warning signs or RSES drop ≥ 5 → offer booster).
3. [M] Closure criteria (Branch H) are checked, and the extension path (2–4 targeted sessions) exists rather than a hard stop.

**Improve:**
- If follow-ups are manual → automate pulses; manual follow-up is where most products silently fail.
- Add goal-attainment scaling against the S1 one-sentence goal as a closure ritual.

---

## Cross-Stage Verification (applies to your whole project)

1. ⚠ Every stage reads/writes the same flag set (risk, trauma, FOC, gate status) — check for stages that were built as silos.
2. ⚠ Safety interrupts override *every* branch at *every* stage, including S10–S12.
3. [M] ORS/SRS (or equivalent session feedback) runs every session, with an alliance-drop alert to the therapist.
4. [D] Every content item shown to a client logs its `content_id + version + language` — without this, your future LLM training set is unusable.
5. Clinician sign-off metadata exists per content item (§6) — if your existing content predates review, mark all of it "pending validation."

---

## Next step for a real gap analysis
Upload your existing project materials (flow diagrams, question banks, app screens, session scripts, DB notes — any format). I'll map each element to the stages above, mark ✅/🟡/❌ per item for you, and produce a prioritized improvement backlog (safety blockers first).
