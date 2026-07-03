import { useState, useEffect, useCallback } from 'react'
import { ArrowLeft, ArrowRight, Check, AlertTriangle, Loader, ChevronDown, ChevronUp } from 'lucide-react'

const fontSans  = "'Geist', ui-sans-serif, system-ui, sans-serif"
const fontSerif = "'Instrument Serif', ui-serif, Georgia, serif"
const BASE      = '/api/consult'

async function apiFetch(path, token, opts = {}) {
  const res = await fetch(BASE + path, {
    ...opts,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}`, ...(opts.headers || {}) },
  })
  const body = await res.json().catch(() => null)
  if (!res.ok) throw new Error(body?.detail || 'Request failed')
  return body
}

/* ── helpers ──────────────────────────────────────────────────── */

function levelLabel(key, val) {
  const maps = {
    depression_level:              { none: 'None', mild: 'Mild', moderate_to_severe: 'Moderate–Severe' },
    anxiety_level:                 { minimal: 'Minimal', mild: 'Mild', moderate_to_severe: 'Moderate–Severe' },
    self_compassion_level:         { low: 'Low', moderate: 'Moderate', high: 'High', not_assessed: '—' },
    emotion_regulation_difficulty: { low: 'Low', moderate: 'Moderate', high: 'High', not_assessed: '—' },
  }
  return maps[key]?.[val] ?? val ?? '—'
}

function schemaLabel(s) {
  const m = {
    unrelenting_standards:     'Unrelenting Standards',
    abandonment:               'Abandonment / Fear of Loss',
    approval_seeking:          'Approval-Seeking',
    maladaptive_perfectionism: 'Perfectionism',
    emotional_inhibition:      'Emotional Inhibition',
  }
  return m[s] ?? s.replace(/_/g, ' ')
}

/* ── Healing methodology data ─────────────────────────────────── */

const HEALING_METHODS = [
  {
    id: 'tipp',
    trigger: (f) => f.includes('poor_ER_strategies') || f.includes('anxiety_elevated') || f.includes('moderate_ER_difficulty'),
    priority: 1,
    icon: '🌊',
    title: 'DBT TIPP — Rapid Distress Relief',
    basis: 'Emotion regulation · DBT (Linehan 2014)',
    tagline: 'When you are overwhelmed and nothing feels like it will help.',
    what: 'TIPP changes your body chemistry quickly — before you can think your way out. Developed in Dialectical Behaviour Therapy, it is the fastest evidence-based route from emotional flood to a regulated state.',
    steps: [
      { label: 'T — Temperature', detail: 'Splash cold water on your face or hold ice for 30 s. Cold triggers the mammalian dive reflex — your heart rate drops within seconds.' },
      { label: 'I — Intense exercise', detail: '20 jumping jacks or 60 s of running in place. Burns off the stress hormones flooding your system right now.' },
      { label: 'P — Paced breathing', detail: 'In for 4 counts, out for 6. The longer exhale activates your parasympathetic system. Do this for 2 minutes.' },
      { label: 'P — Progressive relaxation', detail: 'Tense each muscle group for 5 s, release for 10 s. Start at your feet, work up to your face.' },
    ],
    reference: 'Linehan MM (2014). DBT Skills Training Manual, 2nd ed. Guilford. / Aldao A et al. (2010). Clin Psychol Rev. 30(2):217–237.',
    accent: '#4A7B6F',
  },
  {
    id: 'self_compassion_break',
    trigger: (f, s) => f.includes('low_self_compassion') || f.includes('high_shame') || f.includes('moderate_shame'),
    priority: 1,
    icon: '🤲',
    title: 'Self-Compassion Break',
    basis: 'SCS-SF · Neff 2003',
    tagline: 'A 3-minute practice replacing self-criticism with understanding.',
    what: 'Developed by Kristin Neff and backed by 20+ years of research, the Self-Compassion Break activates the caregiving system — the same you use comforting a friend. Proven to reduce shame, depression, and anxiety in randomised trials.',
    steps: [
      { label: 'Acknowledge', detail: 'Place a hand on your heart. Say: "This is a moment of suffering." Name what you feel — shame, pain, fear. Just acknowledge it without pushing it away.' },
      { label: 'Common humanity', detail: 'Say: "Suffering is part of being human. I am not alone in this." Millions of people have felt exactly this. You are not defective — you are human.' },
      { label: 'Kindness', detail: 'Ask: "What would I say to a close friend feeling this?" Then say that to yourself. Or try: "May I be kind to myself. May I give myself what I need right now."' },
    ],
    reference: 'Neff KD, Germer CK (2013). Pilot study and RCT of the mindful self-compassion program. J Clin Psychol. 69(1):28–44.',
    accent: '#7B6FAF',
  },
  {
    id: 'burnout_recovery',
    trigger: (f) => f.includes('burnout_risk'),
    priority: 1,
    icon: '🔋',
    title: 'Burnout Recovery Protocol',
    basis: 'Burnout · Maslach & Leiter 1997',
    tagline: 'Recovery requires restoration — not just shorter hours.',
    what: 'Burnout depletes three things: energy, engagement, and sense of efficacy. The Maslach model shows that pushing through accelerates collapse; deliberately downregulating is the only way out.',
    steps: [
      { label: 'Map your drain', detail: 'List the 3 things at work that cost the most energy. For each: can you reduce, delegate, or set a boundary? One concrete change beats a week off.' },
      { label: 'Active recovery blocks', detail: 'Block 2 h/day of no-task time — not passive scrolling, but movement, a meal without screens, or time outdoors. Research shows these specifically restore emotional reserves.' },
      { label: 'Reconnect to meaning', detail: 'Write why your work mattered to you originally. What did you hope it would give you? This reconnects the meaning pathway burnout severs, before external conditions change.' },
      { label: 'One temporal boundary', detail: 'Choose one task you will not do after a set time each evening. Even small boundaries signal safety to your nervous system — that recovery is real, not deferred.' },
    ],
    reference: 'Maslach C, Leiter MP (1997). The Truth About Burnout. Jossey-Bass. / Sonnentag S, Fritz C (2007). J Occup Health Psychol. 12(3):204–221.',
    accent: '#C84B31',
  },
  {
    id: 'behavioral_activation',
    trigger: (f) => f.includes('phq2_elevated'),
    priority: 2,
    icon: '⚡',
    title: 'Behavioural Activation',
    basis: 'PHQ-2 elevated · Martell 2001',
    tagline: 'Depression shrinks your world. This gradually re-opens it.',
    what: 'When depressed, the instinct is to wait until you feel better before doing things. Behavioural Activation reverses this: doing comes before feeling. Small scheduled activities restore the positive reinforcement loop that depression breaks.',
    steps: [
      { label: 'List 10 activities', detail: 'Write 10 activities that used to bring pleasure or meaning — no matter how small. Walk to a café, call a friend, cook one meal. Do not filter by whether they feel possible.' },
      { label: 'Rate difficulty', detail: 'Rate each 1–10 for difficulty (10 = hardest). Start with 2–3 rated 2–4. The goal is not to enjoy them immediately — it is to do them and notice what happens after.' },
      { label: 'Schedule as appointments', detail: 'Put them in your calendar. Do them whether or not you feel like it. Track your mood before and after, even on a 1–10 scale.' },
      { label: 'Build momentum', detail: 'Each week, add slightly harder activities. The goal is a gradual reactivation of engagement with life — one action at a time.' },
    ],
    reference: 'Martell CR, Dimidjian S, Herman-Dunn R (2010). Behavioral Activation for Depression. Guilford.',
    accent: '#C84B31',
  },
  {
    id: 'worry_scheduling',
    trigger: (f) => f.includes('anxiety_elevated'),
    priority: 2,
    icon: '🗓',
    title: 'Worry Scheduling',
    basis: 'GAD-2 elevated · Borkovec 1983',
    tagline: 'Contain worry to a fixed window so it stops spreading all day.',
    what: 'Attempting to suppress worry makes it stronger. Worry scheduling gives anxiety a designated container — reducing its intrusion into the rest of your day. Consistently effective in clinical trials for generalised anxiety.',
    steps: [
      { label: 'Choose your 15-minute window', detail: 'Pick one daily slot, not close to bedtime. This is your only permitted worry time. Mark it as a calendar appointment.' },
      { label: 'Postpone during the day', detail: 'When a worry arises outside the window, note it briefly and tell yourself: "I will think about this at [time]." Then return to what you were doing.' },
      { label: 'Use the window fully', detail: 'At the scheduled time, worry deliberately. Write out concerns. For solvable problems: make a small action plan. For unsolvable ones: practise letting the thought pass without engaging.' },
      { label: 'End it cleanly', detail: 'When 15 minutes is up, stop. Worries outside the window get postponed to tomorrow\'s slot. Over time the urge to worry outside it decreases significantly.' },
    ],
    reference: 'Borkovec TD et al. (1983). Stimulus control applications to worry. Behav Res Ther. 21(3):247–251.',
    accent: '#4A7B6F',
  },
  {
    id: 'schema_mode',
    trigger: (f, schemas) => schemas.length > 0,
    priority: 2,
    icon: '🧩',
    title: 'Schema Mode Flash Card',
    basis: 'YSQ-S3 · Young 1998',
    tagline: 'Catch the schema firing — before it runs the show.',
    what: 'Schemas operate like reflexes. The moment you can name what is happening ("this is my Abandonment schema"), you create a pause between trigger and response. Schema flashcards are a standard technique in Schema Therapy for building this pause.',
    steps: [
      { label: 'Name the mode', detail: 'When you have a strong reaction, ask: "Is this proportionate to what actually happened?" If no — a schema may be running. Name it out loud if you can.' },
      { label: 'Speak to the younger self', detail: 'Schemas formed early. Ask: "How old does the part of me that feels [abandoned / like a failure / like I must be perfect] feel right now?" This separates the old wound from the present.' },
      { label: 'Healthy adult response', detail: 'Ask: "What would a calm, caring adult say to a child feeling this?" Then say that to yourself — slowly, without irony. This is the healthy adult mode you are strengthening.' },
      { label: 'Reality test', detail: 'Write three facts about the current situation that do NOT fit the schema\'s story. This corrects a distorted lens with present evidence.' },
    ],
    reference: 'Young JE, Klosko JS, Weishaar ME (2003). Schema Therapy: A Practitioner\'s Guide. Guilford.',
    accent: '#7B6FAF',
  },
  {
    id: 'attachment_journaling',
    trigger: (f, schemas) => f.includes('anxious_attachment') || schemas.includes('abandonment'),
    priority: 2,
    icon: '📎',
    title: 'Attachment Pattern Journaling',
    basis: 'ECR-R · Fraley 2000',
    tagline: 'Understand the pattern so it stops driving from the back seat.',
    what: 'Anxious attachment runs on automatic scripts: scanning for rejection, needing reassurance, escalating when a partner withdraws. Journaling the pattern creates the reflective distance needed to choose differently — the basis of what researchers call "earned security."',
    steps: [
      { label: 'Map the trigger', detail: 'After an anxious episode, write: "What happened? What did I interpret it to mean? What did I do next?" Be factual and specific.' },
      { label: 'Earlier echo', detail: 'Ask: "Does this remind me of anything earlier in my life? What did I learn about closeness from the people who raised me?" Just curiosity — no judgement.' },
      { label: 'What did I actually need?', detail: 'Write: "What did I need in that moment that I didn\'t ask for directly?" Often the answer is simple: reassurance, presence, acknowledgement.' },
      { label: 'Request — not demand', detail: 'Rewrite your response as a direct request: "I felt scared when X happened. I need Y. Can we talk?" Practise saying this without escalation or withdrawal.' },
    ],
    reference: 'Mikulincer M, Shaver PR (2007). Attachment in Adulthood. Guilford. / Siegel DJ (2010). Mindsight. Bantam.',
    accent: '#4A7B6F',
  },
  {
    id: 'shame_resilience',
    trigger: (f) => f.includes('high_shame') || f.includes('moderate_shame'),
    priority: 1,
    icon: '🛡',
    title: 'Shame Resilience Practice',
    basis: 'ISS item 2 · Cook 1994 / Brown 2010',
    tagline: 'Shame grows in silence. The antidote is empathy — starting with yourself.',
    what: 'Brené Brown\'s research across thousands of interviews identified that shame resilience is built through: naming shame, understanding its triggers, practising critical awareness, and sharing vulnerability safely. Shame cannot survive being spoken.',
    steps: [
      { label: 'Name it', detail: 'When shame arises, say: "This is shame. I feel it in my [chest / stomach / face]. I am not this feeling — I am having this feeling." Naming activates the prefrontal cortex and dampens the amygdala response.' },
      { label: 'Identify the trigger', detail: 'Ask: "What story just played? What does this shame say about who I am as a person?" Write it without editing. Then: "Is this a fact, or an old interpretation?"' },
      { label: 'Common humanity', detail: 'Say: "Everyone carries shame. Mine is not a sign I am uniquely broken." Think of someone you deeply respect — they carry shame too. This is what it means to be human.' },
      { label: 'Speak it safely', detail: 'Share the shame with one trusted person, or in writing. You do not need their validation — the act of putting it into words and surviving reduces its power measurably over time.' },
    ],
    reference: 'Brown B (2010). The Gifts of Imperfection. Hazelden. / Brown B (2012). Daring Greatly. Gotham.',
    accent: '#7B6FAF',
  },
]

/* ── HealingCard — expandable methodology card ────────────────── */

function HealingCard({ method }) {
  const [open, setOpen] = useState(false)

  return (
    <div
      style={{
        background: '#FFFFFF',
        border: '1px solid #E0DED6',
        borderRadius: '14px',
        overflow: 'hidden',
        marginBottom: '10px',
        transition: 'box-shadow 0.2s',
      }}
    >
      {/* Header — always visible */}
      <button
        onClick={() => setOpen(v => !v)}
        style={{
          width: '100%',
          padding: '16px 18px',
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '12px',
          textAlign: 'left',
          fontFamily: fontSans,
        }}
      >
        <span style={{ fontSize: '20px', lineHeight: 1, flexShrink: 0, marginTop: '2px' }}>{method.icon}</span>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap', marginBottom: '3px' }}>
            <span style={{ fontSize: '14px', fontWeight: 600, color: '#1B1B19' }}>{method.title}</span>
          </div>
          <span
            style={{
              fontSize: '10px',
              textTransform: 'uppercase',
              letterSpacing: '0.12em',
              color: method.accent,
              fontWeight: 500,
            }}
          >
            {method.basis}
          </span>
          <p style={{ fontSize: '13px', color: '#7A7A72', margin: '5px 0 0', lineHeight: 1.45 }}>
            {method.tagline}
          </p>
        </div>
        <div style={{ flexShrink: 0, marginTop: '2px', color: '#9A9A95' }}>
          {open ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
        </div>
      </button>

      {/* Expanded body */}
      {open && (
        <div style={{ padding: '0 18px 18px', borderTop: '0.5px solid #EAE8E0' }}>
          <p style={{ fontSize: '13px', color: '#3A3A35', lineHeight: 1.65, margin: '14px 0 16px' }}>
            {method.what}
          </p>

          {/* Steps */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '16px' }}>
            {method.steps.map((step, i) => (
              <div
                key={i}
                style={{
                  display: 'flex',
                  gap: '12px',
                  padding: '12px 14px',
                  background: '#F9F8F4',
                  borderRadius: '10px',
                  border: `1px solid ${method.accent}22`,
                }}
              >
                <div
                  style={{
                    width: '22px',
                    height: '22px',
                    borderRadius: '50%',
                    background: method.accent,
                    color: '#fff',
                    fontSize: '11px',
                    fontWeight: 700,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                    marginTop: '1px',
                  }}
                >
                  {i + 1}
                </div>
                <div>
                  <p style={{ fontSize: '12px', fontWeight: 600, color: '#1B1B19', margin: '0 0 3px' }}>{step.label}</p>
                  <p style={{ fontSize: '12px', color: '#7A7A72', margin: 0, lineHeight: 1.55 }}>{step.detail}</p>
                </div>
              </div>
            ))}
          </div>

          {/* Reference */}
          <p style={{ fontSize: '10px', color: '#B0AEA6', lineHeight: 1.5, margin: 0 }}>
            {method.reference}
          </p>
        </div>
      )}
    </div>
  )
}

/* ── HealingSection ───────────────────────────────────────────── */

function HealingSection({ flags, schemas }) {
  const methods = HEALING_METHODS
    .filter(m => m.trigger(flags, schemas))
    .sort((a, b) => a.priority - b.priority)
    .slice(0, 4)

  if (methods.length === 0) return null

  return (
    <div style={{ marginBottom: '14px' }}>
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          marginBottom: '12px',
        }}
      >
        <p style={{
          fontSize: '11px',
          textTransform: 'uppercase',
          letterSpacing: '0.14em',
          color: '#9A9A95',
          margin: 0,
        }}>
          Healing methodologies
        </p>
        <span style={{
          fontSize: '10px',
          background: '#F0F7F5',
          color: '#4A7B6F',
          padding: '2px 7px',
          borderRadius: '4px',
          fontWeight: 500,
        }}>
          {methods.length} matched to your profile
        </span>
      </div>
      {methods.map(m => <HealingCard key={m.id} method={m} />)}
    </div>
  )
}

/* ── sub-components ──────────────────────────────────────────── */

function ProgressBar({ visited, current }) {
  const total = 11
  const done  = visited.length
  const pct   = Math.min(100, Math.round((done / total) * 100))
  return (
    <div style={{ padding: '0 0 20px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
        <span style={{ fontSize: '11px', color: '#9A9A95', textTransform: 'uppercase', letterSpacing: '0.12em' }}>
          Progress
        </span>
        <span style={{ fontSize: '11px', color: '#9A9A95' }}>{pct}%</span>
      </div>
      <div style={{ height: '3px', background: '#EAE8E0', borderRadius: '2px' }}>
        <div
          style={{
            height: '100%', borderRadius: '2px',
            background: '#4A7B6F',
            width: `${pct}%`,
            transition: 'width 0.4s ease',
          }}
        />
      </div>
    </div>
  )
}

function CrisisBox() {
  return (
    <div
      style={{
        marginBottom: '14px',
        padding: '14px 16px',
        background: '#FEF5F2',
        border: '1px solid #F5CFCA',
        borderRadius: '12px',
        display: 'flex',
        gap: '10px',
        alignItems: 'flex-start',
      }}
    >
      <AlertTriangle size={16} color="#C84B31" style={{ marginTop: '2px', flexShrink: 0 }} />
      <div>
        <p style={{ fontSize: '13px', fontWeight: 500, color: '#C84B31', margin: '0 0 4px' }}>
          Support is available
        </p>
        <p style={{ fontSize: '12px', color: '#7A7A72', margin: 0, lineHeight: 1.5 }}>
          Thailand: <strong>1323</strong> (กรมสุขภาพจิต, 24 ชม.) ·{' '}
          International: <a href="https://findahelpline.com" target="_blank" rel="noreferrer" style={{ color: '#C84B31' }}>findahelpline.com</a>
        </p>
      </div>
    </div>
  )
}

/* ── Node renderers ──────────────────────────────────────────── */

function SingleSelect({ node, onSubmit, loading }) {
  const [selected, setSelected] = useState(null)

  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '4px' }}>
        {node.options.map(opt => (
          <button
            key={opt.option_id}
            onClick={() => setSelected(opt.option_id)}
            style={{
              padding: '14px 18px',
              borderRadius: '12px',
              border: selected === opt.option_id ? '1.5px solid #4A7B6F' : '1px solid #E0DED6',
              background: selected === opt.option_id ? '#F0F7F5' : '#FFFFFF',
              color: '#1B1B19',
              fontSize: '14px',
              fontFamily: fontSans,
              cursor: 'pointer',
              textAlign: 'left',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              transition: 'all 0.15s',
            }}
          >
            <span>{opt.label}</span>
            {selected === opt.option_id && <Check size={14} color="#4A7B6F" strokeWidth={2.5} />}
          </button>
        ))}
      </div>

      <button
        disabled={!selected || loading}
        onClick={() => onSubmit({ [selected]: 1 })}
        style={{
          marginTop: '20px',
          width: '100%',
          padding: '13px',
          borderRadius: '999px',
          border: 'none',
          background: selected && !loading ? '#1B1B19' : '#E5E5E0',
          color:      selected && !loading ? '#FAFAF6' : '#9A9A95',
          fontSize: '14px',
          fontWeight: 500,
          fontFamily: fontSans,
          cursor: selected && !loading ? 'pointer' : 'not-allowed',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '6px',
          transition: 'all 0.2s',
        }}
      >
        {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>Continue <ArrowRight size={14} strokeWidth={1.8} /></>}
      </button>
    </div>
  )
}

function ScaleSet({ node, onSubmit, loading }) {
  const [answers, setAnswers] = useState({})

  const scaleLabels = node.scale_labels || []
  const scaleValues = node.scale_values || []
  const allAnswered  = node.questions.every(q => answers[q.question_id] !== undefined)

  const setAnswer = (qid, val) => setAnswers(prev => ({ ...prev, [qid]: val }))

  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', marginTop: '4px' }}>
        {node.questions.map((q, qi) => (
          <div key={q.question_id}>
            {q.safety_item && (
              <div style={{ fontSize: '11px', color: '#C84B31', textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: '6px', fontWeight: 500 }}>
                Sensitive question
              </div>
            )}
            <p style={{ fontSize: '14px', color: '#1B1B19', margin: '0 0 12px', lineHeight: 1.55 }}>
              <span style={{ color: '#C8C6BC', marginRight: '8px', fontSize: '12px' }}>{qi + 1}.</span>
              {q.text}
            </p>
            <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
              {scaleValues.map((val, vi) => {
                const isSelected = answers[q.question_id] === val
                const label      = scaleLabels[vi] || String(val)
                const isShort    = scaleValues.length <= 5
                return (
                  <button
                    key={val}
                    onClick={() => setAnswer(q.question_id, val)}
                    title={label}
                    style={{
                      flex: isShort ? '1 1 0' : undefined,
                      minWidth: isShort ? 0 : '36px',
                      padding: isShort ? '10px 8px' : '8px 12px',
                      borderRadius: '10px',
                      border: isSelected ? '1.5px solid #4A7B6F' : '1px solid #E0DED6',
                      background: isSelected ? '#4A7B6F' : '#FFFFFF',
                      color: isSelected ? '#FFFFFF' : '#7A7A72',
                      fontSize: isShort ? '12px' : '13px',
                      fontFamily: fontSans,
                      cursor: 'pointer',
                      whiteSpace: isShort ? 'normal' : 'nowrap',
                      textAlign: 'center',
                      lineHeight: 1.3,
                      transition: 'all 0.12s',
                    }}
                  >
                    {isShort ? label : val}
                  </button>
                )
              })}
            </div>
            {scaleValues.length > 6 && answers[q.question_id] !== undefined && (
              <p style={{ fontSize: '11px', color: '#4A7B6F', marginTop: '6px', marginBottom: 0 }}>
                Selected: {scaleLabels[scaleValues.indexOf(answers[q.question_id])] || answers[q.question_id]}
              </p>
            )}
          </div>
        ))}
      </div>

      <button
        disabled={!allAnswered || loading}
        onClick={() => onSubmit(answers)}
        style={{
          marginTop: '24px',
          width: '100%',
          padding: '13px',
          borderRadius: '999px',
          border: 'none',
          background: allAnswered && !loading ? '#1B1B19' : '#E5E5E0',
          color:      allAnswered && !loading ? '#FAFAF6' : '#9A9A95',
          fontSize: '14px',
          fontWeight: 500,
          fontFamily: fontSans,
          cursor: allAnswered && !loading ? 'pointer' : 'not-allowed',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '6px',
          transition: 'all 0.2s',
        }}
      >
        {loading
          ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} />
          : <>Continue <ArrowRight size={14} strokeWidth={1.8} /></>}
      </button>
    </div>
  )
}

/* ── Profile result view ─────────────────────────────────────── */

function ProfileResult({ profile: raw, onBack }) {
  // raw = full API response from submit_answers (done=true)
  // raw.profile = profile_data dict from _compute_profile()
  // raw.profile.profile = the nested structured profile fields
  const aiSummary   = raw.ai_summary || null
  const profileData = raw.profile || {}          // profile_data
  const p           = profileData.profile || {}  // profile_data.profile (the nested fields)
  const flags       = profileData.flags  || []
  const schemas     = p.active_schemas   || []

  const Pill = ({ label, value, accent }) => (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '10px 0',
        borderBottom: '0.5px solid #EAE8E0',
      }}
    >
      <span style={{ fontSize: '13px', color: '#7A7A72' }}>{label}</span>
      <span style={{ fontSize: '13px', fontWeight: 500, color: accent || '#1B1B19' }}>{value}</span>
    </div>
  )

  return (
    <div>
      <button
        onClick={onBack}
        style={{
          display: 'flex', alignItems: 'center', gap: '6px',
          fontSize: '13px', color: '#9A9A95',
          background: 'none', border: 'none', cursor: 'pointer',
          fontFamily: fontSans, padding: '0 0 24px',
        }}
      >
        <ArrowLeft size={14} strokeWidth={1.8} /> Back to menu
      </button>

      <div
        style={{
          display: 'inline-block',
          fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.14em',
          color: '#4A7B6F', background: '#F0F7F5',
          padding: '3px 9px', borderRadius: '6px', fontWeight: 500,
          marginBottom: '10px',
        }}
      >
        Assessment complete
      </div>

      <h2
        style={{
          fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400,
          fontSize: '28px', color: '#1B1B19', margin: '0 0 24px',
        }}
      >
        Your stress profile.
      </h2>

      {/* Safety */}
      {(p.safety_flag || flags.includes('safety_triggered')) && <CrisisBox />}

      {/* Mood & Anxiety */}
      <div style={{ background: '#FFFFFF', border: '1px solid #E0DED6', borderRadius: '14px', padding: '18px 20px', marginBottom: '10px' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: '#9A9A95', margin: '0 0 4px' }}>
          Mood &amp; Anxiety
        </p>
        <Pill
          label="Depression screen (PHQ-2)"
          value={levelLabel('depression_level', p.depression_level)}
          accent={p.depression_level === 'moderate_to_severe' ? '#C84B31' : '#1B1B19'}
        />
        <Pill
          label="Anxiety screen (GAD-2)"
          value={levelLabel('anxiety_level', p.anxiety_level)}
          accent={p.anxiety_level === 'moderate_to_severe' ? '#C84B31' : '#1B1B19'}
        />
      </div>

      {/* Inner resources */}
      <div style={{ background: '#FFFFFF', border: '1px solid #E0DED6', borderRadius: '14px', padding: '18px 20px', marginBottom: '10px' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: '#9A9A95', margin: '0 0 4px' }}>
          Inner resources
        </p>
        <Pill
          label="Self-compassion"
          value={levelLabel('self_compassion_level', p.self_compassion_level)}
          accent={p.self_compassion_level === 'low' ? '#C84B31' : undefined}
        />
        <Pill
          label="Emotion regulation"
          value={levelLabel('emotion_regulation_difficulty', p.emotion_regulation_difficulty)}
          accent={p.emotion_regulation_difficulty === 'high' ? '#C84B31' : undefined}
        />
        <Pill
          label="Shame level"
          value={p.shame_level ? p.shame_level.charAt(0).toUpperCase() + p.shame_level.slice(1) : '—'}
          accent={p.shame_level === 'high' ? '#C84B31' : undefined}
        />
      </div>

      {/* Core belief patterns */}
      {schemas.length > 0 && (
        <div style={{ background: '#FFFFFF', border: '1px solid #E0DED6', borderRadius: '14px', padding: '18px 20px', marginBottom: '10px' }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: '#9A9A95', margin: '0 0 12px' }}>
            Core belief patterns
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {schemas.map(sc => (
              <div
                key={sc}
                style={{
                  padding: '9px 12px',
                  background: '#F5F3EB',
                  borderRadius: '9px',
                  fontSize: '13px',
                  color: '#1B1B19',
                  fontWeight: 500,
                }}
              >
                {schemaLabel(sc)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Domain flags */}
      {p.domain_flags && Object.values(p.domain_flags).some(Boolean) && (
        <div style={{ background: '#FFFFFF', border: '1px solid #E0DED6', borderRadius: '14px', padding: '18px 20px', marginBottom: '10px' }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: '#9A9A95', margin: '0 0 12px' }}>
            Flagged areas
          </p>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
            {Object.entries(p.domain_flags).filter(([, v]) => v).map(([k]) => (
              <span
                key={k}
                style={{
                  fontSize: '12px', padding: '4px 10px',
                  background: '#FEF5F2', border: '1px solid #F5CFCA',
                  borderRadius: '999px', color: '#C84B31',
                }}
              >
                {k.replace(/_/g, ' ')}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Referral */}
      {profileData.referral_recommended && (
        <div
          style={{
            padding: '14px 16px',
            background: '#FEF5F2',
            border: '1px solid #F5CFCA',
            borderRadius: '12px',
            marginBottom: '10px',
            fontSize: '13px',
            color: '#7A7A72',
            lineHeight: 1.5,
          }}
        >
          <strong style={{ color: '#C84B31' }}>Professional support recommended.</strong>{' '}
          Your scores suggest speaking with a licensed mental health professional may help.
        </div>
      )}

      {/* Personalised summary */}
      <div style={{ background: '#FFFFFF', border: '1px solid #E0DED6', borderRadius: '14px', padding: '18px 20px', marginBottom: '14px' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: '#9A9A95', margin: '0 0 12px' }}>
          Personalised summary
        </p>
        {aiSummary
          ? <p style={{ fontSize: '14px', color: '#3A3A35', lineHeight: 1.75, margin: 0, whiteSpace: 'pre-wrap' }}>{aiSummary}</p>
          : <p style={{ fontSize: '13px', color: '#9A9A95', margin: 0 }}>Summary not available.</p>
        }
      </div>

      {/* ── Healing methodologies ── */}
      <HealingSection flags={flags} schemas={schemas} />

      <p style={{ fontSize: '11px', color: '#B0AEA6', lineHeight: 1.6, marginBottom: '32px' }}>
        {profileData.disclaimer}
      </p>
    </div>
  )
}

/* ── Main ConsultDashboard ───────────────────────────────────── */

export default function ConsultDashboard({ token, onBack }) {
  const [phase,      setPhase]      = useState('idle')
  const [sessionId,  setSessionId]  = useState(null)
  const [node,       setNode]       = useState(null)
  const [visited,    setVisited]    = useState([])
  const [submitting, setSubmitting] = useState(false)
  const [crisisRes,  setCrisisRes]  = useState(false)
  const [profile,    setProfile]    = useState(null)
  const [error,      setError]      = useState('')

  const startSession = useCallback(async () => {
    setPhase('loading')
    setError('')
    try {
      const data = await apiFetch('/start', token, { method: 'POST' })
      setSessionId(data.session_id)
      setNode(data.node)
      setVisited([])
      setPhase('assessment')
    } catch (e) {
      setError(e.message)
      setPhase('error')
    }
  }, [token])

  useEffect(() => { startSession() }, [startSession])

  const submitAnswer = async (answers) => {
    setSubmitting(true)
    try {
      const data = await apiFetch(`/${sessionId}/answer`, token, {
        method: 'POST',
        body: JSON.stringify({ node_id: node.node_id, answers, text_values: {} }),
      })

      if (data.crisis_resources || data.safety_triggered) setCrisisRes(true)
      setVisited(prev => [...prev, node.node_id])

      if (data.done) {
        setProfile(data)
        setPhase('done')
      } else {
        setNode(data)
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setSubmitting(false)
    }
  }

  const shell = (children) => (
    <div style={{ minHeight: '100vh', background: '#FAFAF6', fontFamily: fontSans, display: 'flex', flexDirection: 'column' }}>
      <style>{`@keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }`}</style>
      <div
        style={{
          display: 'flex', alignItems: 'center', gap: '10px',
          padding: '18px 24px',
          borderBottom: '0.5px solid rgba(0,0,0,0.07)',
          background: '#FFFFFF',
        }}
      >
        <button
          onClick={onBack}
          style={{
            display: 'flex', alignItems: 'center', gap: '6px',
            fontSize: '12px', color: '#9A9A95',
            background: 'none', border: 'none', cursor: 'pointer',
            fontFamily: fontSans, padding: '4px 0',
          }}
        >
          <ArrowLeft size={13} strokeWidth={1.8} />
        </button>
        <div style={{ width: '0.5px', height: '14px', background: '#E0DED6' }} />
        <div style={{ display: 'flex', alignItems: 'center', gap: '7px' }}>
          <span style={{ fontSize: '18px' }}>🧠</span>
          <span style={{ fontSize: '13px', color: '#7A7A72', fontWeight: 500 }}>Consult &amp; Healing</span>
        </div>
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: '32px 24px' }}>
        <div style={{ maxWidth: '560px', margin: '0 auto' }}>
          {children}
        </div>
      </div>
    </div>
  )

  if (phase === 'loading') {
    return shell(
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '80px', gap: '16px' }}>
        <Loader size={20} color="#4A7B6F" style={{ animation: 'spin 1s linear infinite' }} />
        <p style={{ fontSize: '13px', color: '#9A9A95', margin: 0 }}>Setting up your assessment…</p>
      </div>
    )
  }

  if (phase === 'error') {
    return shell(
      <div style={{ paddingTop: '60px', textAlign: 'center' }}>
        <p style={{ color: '#C84B31', fontSize: '14px', marginBottom: '16px' }}>{error}</p>
        <button
          onClick={startSession}
          style={{
            padding: '10px 24px', borderRadius: '999px', border: 'none',
            background: '#1B1B19', color: '#FAFAF6',
            fontSize: '13px', fontFamily: fontSans, cursor: 'pointer',
          }}
        >
          Try again
        </button>
      </div>
    )
  }

  if (phase === 'done' && profile) {
    return shell(<ProfileResult profile={profile} onBack={onBack} />)
  }

  if (phase === 'assessment' && node) {
    if (node.done) {
      return shell(
        <div style={{ paddingTop: '40px', textAlign: 'center' }}>
          <p style={{ fontSize: '15px', color: '#1B1B19' }}>Assessment complete.</p>
        </div>
      )
    }

    return shell(
      <>
        <ProgressBar visited={visited} current={node.node_id} />

        {node.trigger_warning && (
          <div style={{ padding: '10px 14px', background: '#FEF5F2', border: '1px solid #F5CFCA', borderRadius: '10px', fontSize: '12px', color: '#7A7A72', marginBottom: '16px', lineHeight: 1.5 }}>
            {node.trigger_warning}
          </div>
        )}

        {node.instrument && (
          <p style={{ fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.14em', color: '#9A9A95', marginBottom: '8px' }}>
            {node.instrument}
          </p>
        )}

        <h2 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: '22px', color: '#1B1B19', margin: '0 0 6px', lineHeight: 1.35 }}>
          {node.label}
        </h2>

        {node.rationale && (
          <p style={{ fontSize: '12px', color: '#9A9A95', margin: '0 0 20px', lineHeight: 1.55 }}>
            {node.rationale}
          </p>
        )}

        {crisisRes && <CrisisBox />}

        {node.node_type === 'single_select'
          ? <SingleSelect node={node} onSubmit={submitAnswer} loading={submitting} />
          : <ScaleSet     node={node} onSubmit={submitAnswer} loading={submitting} />
        }

        {node.evidence && (
          <p style={{ fontSize: '10px', color: '#C8C6BC', marginTop: '16px', lineHeight: 1.5 }}>
            {node.evidence}
          </p>
        )}
      </>
    )
  }

  return shell(null)
}
