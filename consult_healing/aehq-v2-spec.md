# AEHQ v2.0 — Adaptive Emotional Self-Reflection Questionnaire
## Consolidated, Research-Backed Specification (10 Situations)

**Goal:** help an emotionally overwhelmed person (1) name the feeling, (2) understand the trigger, (3) identify the unmet need, (4) choose one small next action.

**Positioning (shown to users, plainly):** This is guided self-reflection — not therapy, not diagnosis, not a replacement for professional care. Safety triage runs first in every session; a path to human support is one tap away at all times.

**Tone rules (enforced across all items):** warm, simple, non-clinical. One question per screen. No "why" questions — only *what / where / when / which / how much* (rumination research, §1). Every open question carries an implicit permission to answer imperfectly ("rough words are fine", "a guess counts").

---

## 1. Research Foundation Table

| # | Research area | Core finding | How AEHQ uses it | Key sources | Tier |
|---|--------------|--------------|------------------|-------------|------|
| R1 | **Affect labeling** | Putting feelings into words dampens amygdala response and subjective distress | Naming the emotion is the central mechanic of every session | Lieberman et al. (2007); Kircanski et al. (2012); Torre & Lieberman (2018) | B/A |
| R2 | **Emotion granularity** | Fine-grained emotion differentiation predicts better regulation and coping | Two-step ladder: quadrant → situation-specific word list; distinct-word count tracked as a skill metric | Barrett et al. (2001); Kashdan, Barrett & McKnight (2015) | B |
| R3 | **Self-distancing** | Third-person / observer / temporal distance reduces distress at low cognitive cost, especially for intense material | Dedicated D-phrasings; mandatory at SUDS 8–10 and under rumination | Kross et al. (2014); Bruehlman-Senecal & Ayduk (2015) | B |
| R4 | **Rumination** | Abstract "why"-processing prolongs distress; concrete "what"-processing helps | "Why" banned; concreteness prompts; rumination detector switches track | Nolen-Hoeksema et al. (2008); Watkins et al. (2009, 2011) | A/B |
| R5 | **Expressive writing** | Structured emotional disclosure yields measurable benefits | One short free-write near the end of standard/deep tracks — never first, never at high intensity | Pennebaker & Beall (1986); Frattaroli (2006) meta-analysis | A |
| R6 | **Self-compassion** | Compassion-based practice reliably reduces shame and self-criticism | Tailored compassion line in every situation's closure; CFT-style reframes for shame | Neff (2003); Neff & Germer (2013) RCT; Kirby et al. (2017) meta-analysis | A |
| R7 | **Validation** | Perceived validation is a precondition for productive disclosure | Micro-copy after heavy answers; "never over-claim empathy" rule | Rogers (1957); Linehan (1997) | C/B |
| R8 | **Appraisal theory** | Emotion follows the *meaning* assigned to events | Every situation has a T-item ("what did it seem to mean") — the root-cause detector | Lazarus & Folkman (1984) | B |
| R9 | **ACT** | Acceptance, defusion, and values-based action reduce experiential avoidance | Willingness prompts for avoiders; values link in the action step | Hayes et al. (2006); A-Tjak et al. (2015) meta-analysis | A |
| R10 | **Implementation intentions** | If–then plans roughly double follow-through vs. vague intentions | Closure always ends in one tiny if–then action | Gollwitzer (1999); Gollwitzer & Sheeran (2006) meta-analysis | A |
| R11 | **Digital mental-health agents** | Structured conversational self-help delivered by software can reduce symptoms short-term | Interaction pattern: short turns, one question/screen, empathic micro-copy, human escalation | Fitzpatrick et al. (2017) RCT | A (short-term, young adults) |

Tier code: **A** meta-analysis/RCT · **B** controlled or mechanistic studies · **C** clinical framework — used only to make the system *more cautious*, never deeper.

---

## 2. Adaptive Flow

```
Screen 1   SAFETY TRIAGE ──── crisis signal ──→ SAFETY SCRIPT (§6), session ends
Screen 2   SUDS 0–10
              ├─ 8–10 → GROUNDING module → re-rate
              │          ├─ still ≥8 (×2) → pause script (§6), no content questions
              │          └─ drops → DISTANCED-ONLY track (D): self-distancing items,
              │                     no deepening, no free-writing
              ├─ 4–7  → STANDARD track (S): guided reflection, full spine
              └─ 0–3  → REFLECTIVE-DEEP track (R): meaning, pattern, values items
Screen 3   Situation selection (10 options + "something else")
Screen 4   Body sensation locator
Screen 5   Emotion words (quadrant → situation list, pick ≤3)
Screen 6-8 Root-cause items (track-matched, from situation bank §4)
Screen 9   Unmet-need item
Screen 10  Self-compassion line (optional, skippable without penalty)
Screen 11  Tiny if–then action
Screen 12  Re-rate SUDS + closure
```

Spot re-rate every 3 screens; every free-text answer passes the crisis keyword monitor.

## 3. IF/THEN Branching Rules

| # | IF | THEN | Basis |
|---|----|------|-------|
| B1 | Crisis / self-harm signal (triage answer or keyword hit, any screen) | Stop questionnaire; safety script; human resources; no resume this session | Safety, non-negotiable |
| B2 | SUDS 8–10 | Grounding before any content; then D-track only (distancing items, no deepening) | R3; window-of-tolerance (Siegel 1999, Tier C, conservative use) |
| B3 | SUDS still ≥8 after 2 grounding rounds | Pause script; recommend human contact today | Same as B2 |
| B4 | Rumination detected (same content ≥3 answers · "why/if-only/should-have" density · falling concreteness) | Switch to self-distancing items; inject temporal-distance question; cap at 2 more screens | R3/R4 |
| B5 | Avoidance detected (≥2 skips · repeated one-word answers · "idk/never mind") | Convert open items to choice format; drop depth one level; normalizing micro-copy; never confront | R9 (experiential avoidance); R7 |
| B6 | SUDS rises ≥2 mid-session | One breathing round; re-evaluate track | R3 mechanism; Zaccaro et al. (2018) |
| B7 | SUDS 0–3 at start | R-track (deep) permitted | R2/R5 |
| B8 | Closure SUDS higher than start | Grounding round + support resources before ending; log for review | Measurement-based care (Fortney et al., 2017) |
| B9 | Numbness situation OR "nowhere-numb" body answer at SUDS ≥6 | Sensory grounding first; shallow items only; persistent numbness across ≥3 sessions → gentle referral suggestion | Conservative; see situation 8 notes |
| B10 | Triage skipped or "Not sure" | Treat as crisis path (conservative) | Safety |

---

## 4. Question Banks by Situation

### 4.0 Shared Core (identical for all 10 situations — annotated once)

**Safety question [every session, screen 1]**
> "Before we start: right now, are you having thoughts of hurting yourself, or feeling that life isn't worth living?" *(No / Yes / Not sure)*
- Purpose: triage before any emotional deepening. · Basis: standard clinical risk-screening practice; conservative routing (B1/B10). · When: always first. · Softer wording: none — softening a safety question reduces its function; warmth goes into the *response* script (§6), not the question.

**Intensity question [screen 2]**
> "0 to 10 — how big is the feeling right now? 0 = calm, 10 = the most overwhelmed you've ever been."
- Purpose: track gating (SUDS). · Basis: Wolpe (1969); adaptive gating per Gibbons et al. (2012). · When: always; re-rated mid-session and at close. · Softer: "No wrong number — first instinct is fine."

**Body sensation question [screen 4]**
> "Where does it sit in your body?" *(chest / throat / stomach / shoulders–jaw / head / everywhere / nowhere—numb)* then "What's it like?" *(tight / heavy / hot / buzzing / hollow / frozen)*
- Purpose: interoceptive anchor; feeds emotion identification. · Basis: Craig (2009); Farb et al. (2015). · When: all tracks; for numbness answers see B9. · Softer: "If nothing shows up, 'nowhere' is a real answer too."

**Closure / re-rate [final screen]**
> "Same 0–10 — where is it now?" then: improved → "You arrived at ⟨x⟩ and you're leaving at ⟨y⟩ — you did that with words." · unchanged → "Naming things doesn't always feel better right away. The research says the naming still counts." · worse → grounding + §6 support script.
- Purpose: outcome measurement + honest closure. · Basis: R1 (labeling effect), Fortney et al. (2017). · When: always last.

**Structure of each situation bank below:** emotion words → root-cause items (tagged [S] standard / [D] distanced / [R] deep) → unmet-need item → self-compassion line → tiny if–then → softer wordings. Root-cause items are the appraisal probes (R8); each is annotated compactly as *(Purpose · Basis · When)*.

### 4.1 Work Overwhelm

**Emotion words:** overwhelmed · dread · pressured · depleted · trapped · inadequate · resentful · foggy
**Root-cause items:**
1. [S] "What's actually on the pile? Telegraph style — no sentences." *(Concrete inventory breaks the undifferentiated 'everything' · R4 concreteness · SUDS 4–7)*
2. [S] "Finish honestly: 'If I don't get this done, it means I am ___.'" *(Appraisal probe — separates real overload from perfectionism · R8; Egan et al. 2011 · S/R only, never at high intensity)*
3. [D] "If {name} were your employee, what would a decent manager take off their plate first?" *(Distanced perspective unlocks solutions self-blame hides · R3 · D-track)*
4. [R] "Is this a season with an end date, or a structure with no exit? Evidence for each?" *(Deep appraisal audit · R8 · SUDS 0–3)*
**Unmet need:** "What's most missing: rest · control over your time · feeling capable · permission to say no?" *(SDT — Deci & Ryan 2000)*
**Self-compassion:** "You're not behind on being a person. Try: 'This is a lot. Anyone carrying it would feel it.'" *(R6)*
**Tiny if–then:** "If I sit down tomorrow, then I do only the first 25 minutes of ⟨smallest item⟩." *(R10; proximal sub-goals — Bandura & Schunk 1981)*
**Softer wordings:** item 2 → "Some people find a sentence hiding under the pressure, like 'it means I'm failing.' Is there one under yours? Rough guess is fine."

### 4.2 Feeling Ignored or Dismissed

**Emotion words:** invisible · unimportant · hurt · embarrassed · deflated · quietly angry · lonely · resigned
**Root-cause items:**
1. [S] "What happened, camera-view only — who said or didn't say what?" *(Separates event from interpretation · R4/R8 · S)*
2. [S] "Which landed harder: what they did, or what it seemed to *say about your place* with them?" *(Ostracism threatens belonging, esteem, control, and mattering — the probe finds which one · Williams 2007, Annual Review of Psychology · S/R)*
3. [D] "A kind observer watches that moment. What do they see {name} needing that nobody noticed?" *(R3 · D)*
4. [R] "When you're *not* being ignored — who notices you, and what do they notice?" *(Counter-evidence recall; belonging repair · Williams 2007 · R)*
**Unmet need:** "What's most missing: being seen · being taken seriously · belonging · knowing you matter?" *(Direct Williams needs mapping)*
**Self-compassion:** "Being overlooked hurts because mattering matters. Try: 'My need to be seen is not too much.'" *(R6)*
**Tiny if–then:** "If I feel invisible in a group this week, then I will say one sentence out loud within the first ten minutes." *(R10; behavioral experiment — Bennett-Levy et al. 2004)*
**Softer:** item 2 → "No need to be exact — did it sting more in the moment, or in what it hinted about where you stand?"

### 4.3 Conflict with Authority (boss, parent, teacher, official)

**Emotion words:** powerless · unfairly treated · intimidated · angry · humiliated · anxious · defiant · torn
**Root-cause items:**
1. [S] "What exactly did they say or decide, and at which word did your body react?" *(Concrete anchor · R4; Craig 2009 · S)*
2. [S] "Which is louder: the unfairness of it, or the danger of pushing back?" *(Separates injustice appraisal from fear appraisal — different needs, different actions · R8; Edmondson 1999 on psychological safety · S/R)*
3. [D] "If a colleague {name} respects were treated this way, what would {name} say was unfair about it?" *(Distancing legitimizes the grievance without escalation · R3 · D)*
4. [R] "What have you already swallowed with this person? How much of today's weight is today's, and how much is the pile?" *(Accumulated suppression audit · Morrison 2014 on voice and silence · R)*
**Unmet need:** "What's most missing: fairness · respect · safety to speak · room to decide for yourself?"
**Self-compassion:** "Feeling small in front of power is a human reflex, not weakness. Try: 'My read on unfairness deserves a hearing — at least from me.'" *(R6)*
**Tiny if–then:** "If I decide to raise it, then I will write one factual sentence — what happened + what I'm asking for — before the meeting." *(R10; assertion structure — Speed et al. 2018)*
**Softer:** item 4 → "No need to count everything — is this the first time, or does it rhyme with other times?"

### 4.4 Self-Criticism / Shame

Special rule: **no free-writing at SUDS ≥6** (shame spirals in unstructured text — conservative application of R4); D-track is default at SUDS ≥6 (B-rules).
**Emotion words:** ashamed · small · exposed · worthless · fraudulent · disgusted with myself · tired of myself
**Root-cause items:**
1. [S] "What are the critic's exact words? Quote it." *(Externalizes the voice; labeling · R1 · S, SUDS <6)*
2. [S] "Whose voice does the critic borrow? Does the accent belong to someone from your past?" *(Source attribution loosens fusion · R8; Gilbert 2009 · S/R)*
3. [D] "If your closest friend said those exact words about themselves, what's the first thing you'd feel toward them?" *(Classic self-compassion induction · Neff 2003; Kirby et al. 2017 · D — the workhorse item for this situation)*
4. [R] "What is the critic trying to protect you from? It usually has a job." *(Functional analysis of self-criticism · Gilbert 2009 · R)*
**Unmet need:** "What's most missing: acceptance as-is · a standard you actually chose · rest from self-watching · proof that counts?"
**Self-compassion:** "Try, in your own words: 'This is a moment of struggle. Struggle is human. May I be on my own side today.'" *(Neff & Germer 2013 — adapted self-compassion break)*
**Tiny if–then:** "If the critic starts tonight, then I will write down one thing from the last 7 days it is conveniently ignoring." *(R10; evidence log)*
**Softer:** item 1 → "Only if you're willing — what's one line the critic says? You can paraphrase."

### 4.5 Future Anxiety

**Emotion words:** dread · restless · frozen · scattered · powerless · on-edge · braced
**Root-cause items:**
1. [S] "Name the unknown in one line: 'I don't know whether ___.'" *(Labels the feared object · R1 · S)*
2. [S] "What's the worst frame of the movie your mind plays — one line only? Naming it usually shrinks it." *(Feared-image labeling; exposure-adjacent · Kircanski et al. 2012 · S, skippable)*
3. [S] "Roughly what % of this is inside your control?" *(Control appraisal splits problem-solving from tolerance-building · R8; Lazarus & Folkman 1984 · S/R)*
4. [D] "Picture {name} five years from now, on the other side, having coped. What does that {name} know?" *(Temporal distancing · Bruehlman-Senecal & Ayduk 2015 · D)*
5. [R] "What decision are you postponing until you feel certain — and what is the waiting costing?" *(IU pattern probe · Dugas & Ladouceur 2000 · R)*
**Unmet need:** "What's most missing: certainty (rarely available) · confidence you could cope either way · a plan for the controllable part · company in the waiting?"
**Self-compassion:** "A mind that scans the future is trying to keep you safe. Try: 'I can be scared and still choose my next step.'" *(R6/R9)*
**Tiny if–then:** "If the worry starts tonight, then I write it in the worry list and close the notebook — it gets its 15 minutes tomorrow at ⟨time⟩." *(Worry postponement — Borkovec et al. 1983; outcome logging — LaFreniere & Newman 2020)*
**Softer:** item 2 → "Only a rough sketch — no need to look at it long."

### 4.6 Grief / Loss

**Emotion words:** yearning · hollow · heavy · guilty · relieved-then-guilty · disbelief · tender
**Root-cause items:**
1. [S] "What did you lose? One plain sentence." *(Naming the loss object · R1 · S)*
2. [S] "When does it hit hardest — a time, a place, a habit that's now broken?" *(Concrete trigger map · R4 · S)*
3. [S] "Is there a feeling you think you're not *allowed* to have here — relief, anger, nothing at all? All of those are documented, normal grief." *(Mixed-emotion permission · Kashdan et al. 2015; Stroebe & Schut 1999 · S/R)*
4. [D] "Watching {name} from across the room this week — what are they carrying?" *(R3 · D)*
5. [R] "What did they/it make possible in your life? Which doors are truly closed, and which are only closed for now?" *(Restoration-orientation probe · Stroebe & Schut 1999 · R)*
**Unmet need:** "What's most missing: permission to grieve at your own pace · someone to remember with · rest · a way to honor them?"
**Self-compassion:** "Grief is love with nowhere to go yet. Try: 'I'm allowed to take this at my speed — including the okay days.'" *(R6; dual-process normalization)*
**Tiny if–then:** "If Sunday evening comes (the hard slot), then I will light a candle / play their song / write them three lines." *(R10; approach at 10% dose)*
**Referral trigger:** loss >12 months + yearning dominant + daily functioning impaired → gentle referral script (§6) — targeted grief therapy has strong RCT support (Shear et al., 2005, JAMA).
**Softer:** item 3 → "Some feelings in grief feel forbidden. If one of yours does, you can name it here — nobody grades this."

### 4.7 Anger Hiding Hurt

**Emotion words:** furious · betrayed · unappreciated · bitter · protective · and-underneath: hurt · wounded · scared of not mattering
**Root-cause items:**
1. [S] "Replay the moment. What happened *one second before* the anger arrived?" *(Anger is often secondary; the second-before probe finds the primary emotion · Greenberg 2002, emotion-focused therapy · S)*
2. [D] "A fly on the wall watches the scene. What does it see {name} feeling first — before the anger armor goes on?" *(R3; Greenberg 2002 · D — default at high intensity)*
3. [S] "If the anger could only speak one sentence that starts with 'It hurt when…', what would it say?" *(Primary-emotion labeling · R1; Greenberg 2002 · S, skippable)*
4. [R] "What does the anger protect? What would be at risk if you showed the hurt instead?" *(Functional analysis · Greenberg 2002; R8 · R)*
**Unmet need:** "What's most missing: acknowledgment of the hurt · an apology · mattering to them · safety to be soft?"
**Self-compassion:** "Anger that guards a wound is loyalty to yourself. Try: 'The hurt under this is allowed to exist.'" *(R6)*
**Tiny if–then:** "If I'm still hot in an hour, then I write the 'It hurt when…' sentence somewhere private before deciding anything." *(R10; delay + labeling — Beck & Fernandez 1998 on CBT anger management)*
**Softer:** item 3 → "Only if it's true for you — some anger is just anger, and that's a full answer too."

### 4.8 Emotional Numbness

Special handling (B9): sensory grounding first; items stay shallow; **never pathologize the numbness**; persistent numbness ≥3 sessions → gentle referral note.
**Emotion words:** numb · empty · flat · distant · foggy · disconnected · "nothing — and that's my answer"
**Root-cause items:**
1. [S] "On the outside of the numbness — is there 1% of anything? Heaviness, static, tiredness? 0% is also a real answer." *(Low-threshold interoception; avoids demand to feel · Craig 2009; alexithymia research — Taylor, Bagby & Parker 1997 · S)*
2. [S] "When did the volume go down — after one event, or slowly over weeks?" *(Onset map distinguishes protective shutdown from gradual depletion · R8 · S)*
3. [D] "If a documentary narrator described {name}'s last two weeks, what would the narrator say {name} has been through?" *(Distanced narration bypasses the 'I feel nothing' block · R3 · D)*
4. [R] "What did you used to feel *most* — which feeling went quiet first?" *(Granularity recovery probe · R2 · R)*
**Unmet need:** "What's most missing: rest · safety to feel again slowly · connection · time without demands?"
**Self-compassion:** "Numbness is often the mind's circuit-breaker, not a defect. Try: 'Something in me decided to protect me. I can thank it and still want the feeling back.'" *(R6; conservative framing)*
**Tiny if–then:** "If I make tea tomorrow, then I hold the cup for 30 seconds and just notice warm." *(Micro-BA + interoception — Ekers et al. 2014; Farb et al. 2015)*
**Softer:** all items in this bank already run at the softest register; the rule here is *never demand feeling*.

### 4.9 Relationship Insecurity

**Emotion words:** anxious · unwanted · jealous · on-edge · unsure of my place · clingy-then-ashamed · braced for the ending
**Root-cause items:**
1. [S] "What was the trigger — a message, a silence, a tone? Camera-view only." *(Separates signal from story · R4/R8 · S)*
2. [S] "What did the silence/tone seem to *mean*? Finish: 'It felt like it meant ___.'" *(Appraisal probe — attachment-threat meaning · R8; Mikulincer & Shaver 2007 · S)*
3. [D] "If {name}'s most secure friend read this situation, what would they bet is actually going on?" *(Distanced re-appraisal; security priming direction · R3; Mikulincer & Shaver 2007 · D)*
4. [R] "When the fear says 'they're leaving' — how often has that alarm been right before? What's its actual track record?" *(Base-rate audit of the alarm · Bennett-Levy et al. 2004 behavioral-experiment logic · R)*
5. [R] "What do you do when the fear spikes — check, ask again, go quiet? What does that move cost?" *(Reassurance-seeking loop probe · Joiner & Metalsky 1995 · R)*
**Unmet need:** "What's most missing: reassurance you can trust · consistency · knowing where you stand · your own ground to stand on?"
**Self-compassion:** "Wanting to feel secure with someone is wiring, not weakness. Try: 'My need for steadiness is legitimate — and I can give myself the first 10% of it.'" *(R6)*
**Tiny if–then:** "If the urge to check/re-ask hits, then I wait 20 minutes and write the fear down first — then decide." *(R10; interrupts the reassurance loop)*
**Softer:** item 5 → "No judgment on the move — everyone has one. What's yours?"

### 4.10 Feeling Trapped / Unable to Say No

**Emotion words:** trapped · suffocated · resentful · obligated · guilty-in-advance · invisible · exhausted
**Root-cause items:**
1. [S] "What did you say yes to that your body said no to? Name the most recent one." *(Concrete instance beats the global 'I can never say no' · R4 · S)*
2. [S] "Finish: 'If I say no, then ___.'" *(The feared consequence is the root — rejection, conflict, guilt, being seen as selfish · R8 · S/R)*
3. [D] "If {name} watched a friend carry this exact obligation load, what would {name} tell them they're allowed to put down?" *(R3 · D)*
4. [R] "Whose rule is 'a good person doesn't refuse'? Did you ever actually sign it?" *(Internalized-standard audit · R8; ACT values — Hayes et al. 2006 · R)*
**Unmet need:** "What's most missing: permission (yours) · room to choose · rest · a relationship that survives a no?"
**Self-compassion:** "A no to them is often a yes to you — that's not selfish, it's a boundary. Try: 'My limits are information, not betrayal.'" *(R6)*
**Tiny if–then:** "If a request lands this week, then my first sentence is 'Let me check and come back to you' — the no gets to be a two-step." *(R10; graded assertion — Speed et al. 2018; prediction-testing — Bennett-Levy et al. 2004)*
**Softer:** item 2 → "First guess is enough — what's the scary ending after the no?"

---

## 5. Validation Copy (inserted between screens; R7)

Rotated, matched to answer weight, always reflecting the user's own words where possible:
- "That makes sense, given what you just described."
- "You put that into words — that's harder than it looks."
- "⟨their word⟩ is a heavy one. Take your time."
- "Rough words are fine. There's no grading here."
- "Noticing it's in your ⟨body place⟩ is information, not weakness."
- After a skip: "Skipping is allowed. The next one is lighter."

Hard rules: never praise the *content* of self-critical statements; never claim "I understand exactly how you feel"; never rush ("whenever you're ready" over "quickly rate…"); validate the person's response as understandable, per Linehan's validation levels — not necessarily the appraisal as accurate.

## 6. Safety Scripts (verbatim, warm, non-clinical)

**Crisis script (B1):**
> "Thank you for telling me — that took courage. What you're carrying right now is bigger than a questionnaire, and you deserve real support from a person today. Please reach out now to a crisis line in your country or someone you trust — and if you're in immediate danger, contact emergency services. This app will still be here later. Right now, a human is the right next step."
(Design note: no interrogation, no delay, resources shown as tappable list configured per region.)

**Grounding-pause script (B3):**
> "Your feelings are working hard right now, and that's not a failure — it's a signal. Questions can wait. It makes sense to be with a person for this part: someone you trust, or a professional. Would you like the support options?"

**Referral script (persistent patterns — e.g., prolonged grief, ongoing numbness, burnout ≥3 sessions):**
> "You've shown up here ⟨n⟩ times with this, and it's still heavy — that's important information, not a failure of yours or the app's. This looks like the kind of thing that responds well to working with a professional; research specifically supports it for what you're describing. Want help finding options?"

**Distress-increase script (B8):**
> "The number went up while we talked. Sometimes naming things stirs them before it settles them — that's documented and normal. Let's do one minute of slow breathing together before you go, and here are the support options, just in case."

## 7. Ethical Limitations (stated honestly, shown in-app)

1. **Not therapy, not diagnosis.** The system labels, reflects, and suggests micro-actions; it never names conditions, and validated instruments (if a user opts in) are shown as trends without diagnostic labels.
2. **Assembly is a hypothesis.** Each component (labeling, distancing, if–then plans…) has trial or mechanistic support; this exact assembled flow has not itself been trialed. Within-session SUDS deltas and skip analytics exist to test it, not decorate it.
3. **Tier-C caution rule.** Clinical frameworks without trial evidence (window of tolerance, grounding packaging) are used only to make the system more cautious, never to justify deeper probing.
4. **Digital-agent evidence limits.** Fitzpatrick et al. (2017) shows short-term effects in young adults; generalization is not assumed.
5. **Data minimalism.** Emotional disclosures are highly sensitive; store state variables, not raw text, unless the user explicitly opts into a journal; deletion must be one tap.
6. **Escalation is structural.** Crisis routing, pause scripts, and referral triggers are not removable by configuration.
7. **Cultural adaptation required.** Emotion vocabularies and compassion phrasings need cultural adaptation (e.g., Thai emotion lexicon differs in granularity structure), not literal translation.

## 8. References

Core mechanisms: Lieberman et al. (2007) *Psych. Science*; Kircanski, Lieberman & Craske (2012) *Psych. Science*; Torre & Lieberman (2018) *Emotion Review*; Barrett, Gross, Christensen & Benvenuto (2001) *Cognition & Emotion*; Kashdan, Barrett & McKnight (2015) *Current Directions*; Kross et al. (2014) *JPSP*; Bruehlman-Senecal & Ayduk (2015) *JPSP*; Nolen-Hoeksema, Wisco & Lyubomirsky (2008) *Perspectives on Psych. Science*; Watkins, Baeyens & Read (2009) *J. Abnormal Psych.*; Watkins et al. (2011) *British J. Psychiatry*; Pennebaker & Beall (1986) *J. Abnormal Psych.*; Frattaroli (2006) *Psych. Bulletin*; Neff (2003) *Self and Identity*; Neff & Germer (2013) *J. Clinical Psych.*; Kirby, Tellegen & Steindl (2017) *Behavior Therapy*; Rogers (1957) *J. Consulting Psych.*; Linehan (1997) in *Empathy Reconsidered*; Lazarus & Folkman (1984) *Stress, Appraisal, and Coping*; Hayes et al. (2006) *Behaviour Research & Therapy*; A-Tjak et al. (2015) *Psychotherapy & Psychosomatics*; Gollwitzer (1999) *American Psychologist*; Gollwitzer & Sheeran (2006) *Adv. Exp. Social Psych.*; Fitzpatrick, Darcy & Vierhile (2017) *JMIR Mental Health*.

Situation-specific: Williams (2007) *Annual Review of Psychology* (ostracism); Edmondson (1999) *Administrative Science Quarterly* (psychological safety); Morrison (2014) *Annual Review of Organizational Psych.* (voice & silence); Greenberg (2002) *Emotion-Focused Therapy*, APA (primary vs. secondary emotion); Taylor, Bagby & Parker (1997) *Disorders of Affect Regulation* (alexithymia); Mikulincer & Shaver (2007) *Attachment in Adulthood* (attachment insecurity); Hazan & Shaver (1987) *JPSP*; Joiner & Metalsky (1995) *JPSP* (reassurance seeking); Stroebe & Schut (1999) *Death Studies*; Shear et al. (2005) *JAMA*; Egan, Wade & Shafran (2011) *Clin. Psych. Review*; Bandura & Schunk (1981) *JPSP*; Locke & Latham (2002) *American Psychologist*; Speed, Goldstein & Goldfried (2018) *Clin. Psych.: Science & Practice*; Beck & Fernandez (1998) *Cognitive Therapy & Research*; Dugas & Ladouceur (2000) *Behavior Modification*; Borkovec et al. (1983) *Behaviour Research & Therapy*; LaFreniere & Newman (2020) *Behavior Therapy*; Ekers et al. (2014) *PLoS ONE*; Deci & Ryan (2000) *Psychological Inquiry*; Bennett-Levy et al. (2004) *Oxford Guide to Behavioural Experiments*; Craig (2009) *Nature Reviews Neuroscience*; Farb et al. (2015) *Frontiers in Psychology*; Zaccaro et al. (2018) *Frontiers in Human Neuroscience*; Wolpe (1969); Gibbons et al. (2012) *Archives of General Psychiatry*; Fortney et al. (2017) *Psychiatric Services*; Siegel (1999) *The Developing Mind*.

*Citation note: cited from established pre-2026 literature via model knowledge — verify volume/page details against originals before external publication.*
