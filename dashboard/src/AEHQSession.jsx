/**
 * AEHQSession — one-screen-at-a-time emotional check-in (AEHQ v2.0)
 *
 * Props:
 *   token     — JWT bearer token
 *   onBack    — called when user wants to exit the session
 *   onDone    — called with result payload when session completes
 */

import { useState, useEffect, useCallback } from 'react'
import { ArrowLeft, ArrowRight, Check, Loader, AlertTriangle, Heart } from 'lucide-react'

const fontSans  = "'Geist', ui-sans-serif, system-ui, sans-serif"
const fontSerif = "'Instrument Serif', ui-serif, Georgia, serif"
const BASE      = '/api/aehq'

const ACCENT  = '#4A7B6F'
const RED     = '#C84B31'
const BG      = '#FAFAF6'
const BORDER  = '#E0DED6'
const TEXT    = '#1B1B19'
const MUTED   = '#7A7A72'
const FAINT   = '#9A9A95'

async function api(path, token, opts = {}) {
  const res  = await fetch(BASE + path, {
    ...opts,
    headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}`, ...(opts.headers || {}) },
  })
  const body = await res.json().catch(() => null)
  if (!res.ok) throw new Error(body?.detail || 'Request failed')
  return body
}

/* ── Helpers ────────────────────────────────────────────────── */

function renderMarkdown(text) {
  if (!text) return null
  return text
    .split('\n')
    .map((line, i) => {
      const bold = line.replace(/\*\*(.+?)\*\*/g, (_, m) => `<strong>${m}</strong>`)
      return (
        <span key={i} style={{ display: 'block', minHeight: line.trim() === '' ? '0.8em' : undefined }}
              dangerouslySetInnerHTML={{ __html: bold }} />
      )
    })
}

/* ── Styled button ──────────────────────────────────────────── */

function Btn({ onClick, disabled, primary, danger, children, style = {} }) {
  const bg    = danger ? RED : primary ? TEXT : '#FFFFFF'
  const color = danger || primary ? '#FAFAF6' : TEXT
  const bdr   = danger ? `1.5px solid ${RED}` : primary ? 'none' : `1px solid ${BORDER}`
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        padding: '13px 20px', borderRadius: '999px', border: bdr,
        background: disabled ? '#E5E5E0' : bg,
        color: disabled ? FAINT : color,
        fontSize: '14px', fontWeight: 500, fontFamily: fontSans,
        cursor: disabled ? 'not-allowed' : 'pointer',
        display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '6px',
        transition: 'all 0.15s',
        ...style,
      }}
    >
      {children}
    </button>
  )
}

/* ── Validation copy strip ──────────────────────────────────── */

function ValidationStrip({ text }) {
  if (!text) return null
  return (
    <div style={{
      background: '#F0F7F5', border: `1px solid ${ACCENT}22`,
      borderRadius: '10px', padding: '10px 14px',
      fontSize: '13px', color: ACCENT, lineHeight: 1.5, marginBottom: '20px',
    }}>
      {text}
    </div>
  )
}

/* ── Screen: button choice (safety, options) ────────────────── */

function ButtonChoiceScreen({ screen, onSubmit, loading }) {
  const [selected, setSelected] = useState(null)
  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '4px' }}>
        {(screen.options || []).map(opt => (
          <button
            key={opt.id}
            onClick={() => { setSelected(opt.id); setTimeout(() => onSubmit(opt.id), 80) }}
            style={{
              padding: '14px 18px', borderRadius: '12px',
              border: selected === opt.id ? `1.5px solid ${ACCENT}` : `1px solid ${BORDER}`,
              background: selected === opt.id ? '#F0F7F5' : '#FFFFFF',
              color: TEXT, fontSize: '14px', fontFamily: fontSans,
              cursor: 'pointer', textAlign: 'left',
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              transition: 'all 0.15s',
            }}
          >
            <span>{opt.label}</span>
            {selected === opt.id && <Check size={14} color={ACCENT} strokeWidth={2.5} />}
          </button>
        ))}
      </div>
      {loading && (
        <div style={{ textAlign: 'center', marginTop: '16px' }}>
          <Loader size={16} color={FAINT} style={{ animation: 'spin 1s linear infinite' }} />
        </div>
      )}
    </div>
  )
}

/* ── Screen: slider ─────────────────────────────────────────── */

function SliderScreen({ screen, onSubmit, loading }) {
  const min = screen.slider_min ?? 0
  const max = screen.slider_max ?? 10
  const mid = Math.round((min + max) / 2)
  const [val, setVal] = useState(mid)
  const [touched, setTouched] = useState(false)

  const labels = screen.slider_labels || {}

  return (
    <div>
      {/* Value display */}
      <div style={{
        textAlign: 'center', fontSize: '48px', fontWeight: 700,
        color: TEXT, margin: '8px 0 4px', fontFamily: fontSans,
        opacity: touched ? 1 : 0.35, transition: 'opacity 0.2s',
      }}>
        {val}
      </div>

      {/* Labels row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
        <span style={{ fontSize: '11px', color: FAINT }}>{labels[String(min)] || String(min)}</span>
        <span style={{ fontSize: '11px', color: FAINT }}>{labels[String(max)] || String(max)}</span>
      </div>

      {/* Range input */}
      <input
        type="range" min={min} max={max} step={screen.slider_step ?? 1}
        value={val}
        onChange={e => { setVal(Number(e.target.value)); setTouched(true) }}
        onPointerUp={() => setTouched(true)}
        style={{ width: '100%', accentColor: ACCENT, marginBottom: '4px' }}
      />

      {screen.slider_step === 10 && (
        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
          {[0,10,20,30,40,50,60,70,80,90,100].map(n => (
            <span key={n} style={{ fontSize: '9px', color: BORDER }}>{n}</span>
          ))}
        </div>
      )}

      <div style={{ marginTop: '24px' }}>
        <Btn primary onClick={() => onSubmit(val)} disabled={!touched || loading}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>Continue <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Screen: grounding ──────────────────────────────────────── */

function GroundingScreen({ screen, onSubmit, loading }) {
  const [phase, setPhase] = useState('idle')
  const [count, setCount] = useState(0)
  // one full 4-7-8 breath: in 4s + hold 7s + out 8s = 19s
  const MAX = 19

  useEffect(() => {
    if (phase !== 'running') return
    const t = setInterval(() => {
      setCount(c => {
        if (c + 1 >= MAX) { clearInterval(t); setPhase('done'); return MAX }
        return c + 1
      })
    }, 1000)
    return () => clearInterval(t)
  }, [phase])

  const breatheLabel = () => {
    if (phase === 'idle') return 'Tap to start'
    if (phase === 'done') return 'Done'
    if (count < 4)  return 'Breathe in…'
    if (count < 11) return 'Hold…'
    return 'Breathe out…'
  }

  return (
    <div>
      <div style={{
        width: '160px', height: '160px', borderRadius: '50%',
        margin: '24px auto',
        background: phase === 'running'
          ? `radial-gradient(circle, ${ACCENT}33 0%, ${ACCENT}11 100%)`
          : '#F4F3EF',
        border: `2px solid ${phase === 'done' ? ACCENT : BORDER}`,
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        cursor: phase === 'idle' ? 'pointer' : 'default',
        transition: 'all 0.3s',
      }}
        onClick={() => { if (phase === 'idle') setPhase('running') }}
      >
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: phase === 'done' ? '28px' : '13px', color: TEXT, marginBottom: '4px' }}>
            {phase === 'done' ? '✓' : breatheLabel()}
          </div>
          {phase === 'running' && (
            <div style={{ fontSize: '11px', color: FAINT }}>{MAX - count}s</div>
          )}
        </div>
      </div>

      <p style={{ fontSize: '12px', color: FAINT, textAlign: 'center', marginBottom: '24px' }}>
        {screen.subtext && renderMarkdown(screen.subtext)}
      </p>

      <Btn primary onClick={() => onSubmit('done')} disabled={phase !== 'done' || loading}>
        {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : 'Done — check in again'}
      </Btn>
    </div>
  )
}

/* ── Screen: grid select (situations) ───────────────────────── */

function GridSelectScreen({ screen, onSubmit, loading }) {
  const [selected, setSelected] = useState(null)
  const opts = screen.options || []

  return (
    <div>
      <div style={{
        display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '8px', marginTop: '4px',
      }}>
        {opts.map(opt => (
          <button
            key={opt.id}
            onClick={() => { setSelected(opt.id); setTimeout(() => onSubmit(opt.id), 100) }}
            style={{
              padding: '14px 12px', borderRadius: '12px', cursor: 'pointer',
              border: selected === opt.id ? `1.5px solid ${ACCENT}` : `1px solid ${BORDER}`,
              background: selected === opt.id ? '#F0F7F5' : '#FFFFFF',
              textAlign: 'left', fontFamily: fontSans, transition: 'all 0.12s',
            }}
          >
            <div style={{ fontSize: '20px', marginBottom: '6px' }}>{opt.icon}</div>
            <div style={{ fontSize: '13px', color: TEXT, lineHeight: 1.3, fontWeight: selected === opt.id ? 500 : 400 }}>
              {opt.label}
            </div>
          </button>
        ))}
      </div>
      {loading && (
        <div style={{ textAlign: 'center', marginTop: '16px' }}>
          <Loader size={16} color={FAINT} style={{ animation: 'spin 1s linear infinite' }} />
        </div>
      )}
    </div>
  )
}

/* ── Screen: chip select (body, emotions) ───────────────────── */

function ChipSelectScreen({ screen, onSubmit, loading }) {
  const [selected, setSelected] = useState([])
  const max = screen.max_select || 3
  const opts = screen.options || []

  const toggle = (id) => {
    setSelected(prev => {
      if (prev.includes(id)) return prev.filter(x => x !== id)
      if (prev.length >= max) return prev
      return [...prev, id]
    })
  }

  const canSkip  = screen.skippable !== false
  const hasValue = selected.length > 0

  return (
    <div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '4px' }}>
        {opts.map(opt => {
          const on = selected.includes(opt.id)
          return (
            <button
              key={opt.id}
              onClick={() => toggle(opt.id)}
              style={{
                padding: '9px 14px', borderRadius: '999px', cursor: 'pointer',
                border: on ? `1.5px solid ${ACCENT}` : `1px solid ${BORDER}`,
                background: on ? '#F0F7F5' : '#FFFFFF',
                color: on ? ACCENT : MUTED,
                fontSize: '13px', fontFamily: fontSans, transition: 'all 0.12s',
                fontWeight: on ? 500 : 400,
              }}
            >
              {opt.label}
            </button>
          )
        })}
      </div>
      {max > 1 && (
        <p style={{ fontSize: '11px', color: FAINT, marginTop: '10px' }}>
          {selected.length}/{max} selected
        </p>
      )}
      <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
        {canSkip && !hasValue && (
          <Btn onClick={() => onSubmit([])} disabled={loading} style={{ flex: 1 }}>
            Skip
          </Btn>
        )}
        <Btn primary onClick={() => onSubmit(selected)} disabled={(!hasValue && !canSkip) || loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>Continue <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Screen: single_select question ─────────────────────────── */

function SingleSelectQuestion({ screen, onSubmit, loading }) {
  const [sel, setSel] = useState(null)
  return (
    <div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '4px' }}>
        {(screen.options || []).map(opt => (
          <button
            key={opt.id}
            onClick={() => { setSel(opt.id); setTimeout(() => onSubmit(opt.id), 80) }}
            style={{
              padding: '13px 16px', borderRadius: '12px', cursor: 'pointer',
              border: sel === opt.id ? `1.5px solid ${ACCENT}` : `1px solid ${BORDER}`,
              background: sel === opt.id ? '#F0F7F5' : '#FFFFFF',
              color: TEXT, fontSize: '14px', fontFamily: fontSans, textAlign: 'left',
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              transition: 'all 0.12s',
            }}
          >
            <span>{opt.label}</span>
            {sel === opt.id && <Check size={14} color={ACCENT} strokeWidth={2.5} />}
          </button>
        ))}
      </div>
      {loading && <div style={{ textAlign: 'center', marginTop: '12px' }}><Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /></div>}
    </div>
  )
}

/* ── Screen: open text question ─────────────────────────────── */

function TextQuestion({ screen, onSubmit, loading }) {
  const [text, setText] = useState('')
  const canSkip = screen.skippable

  return (
    <div>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Type here — rough words are fine…"
        rows={4}
        style={{
          width: '100%', padding: '13px 14px', borderRadius: '12px',
          border: `1px solid ${BORDER}`, background: '#FFFFFF',
          fontSize: '14px', fontFamily: fontSans, color: TEXT,
          resize: 'vertical', lineHeight: 1.6, boxSizing: 'border-box',
          outline: 'none',
        }}
      />
      <div style={{ display: 'flex', gap: '10px', marginTop: '12px' }}>
        {canSkip && (
          <Btn onClick={() => onSubmit('__skip__')} disabled={loading} style={{ flex: 1 }}>
            Skip
          </Btn>
        )}
        <Btn primary onClick={() => onSubmit(text || '__skip__')} disabled={loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>Continue <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Screen: display + confirm (self-compassion) ─────────────── */

function DisplayConfirmScreen({ screen, onSubmit, loading }) {
  return (
    <div>
      <div style={{
        background: '#F5F3EB', borderRadius: '16px', padding: '20px 22px',
        marginBottom: '20px', border: `1px solid ${BORDER}`,
      }}>
        <Heart size={18} color={ACCENT} style={{ marginBottom: '12px' }} />
        <p style={{
          fontSize: '15px', color: TEXT, lineHeight: 1.75, margin: 0,
          fontFamily: fontSerif, fontStyle: 'italic',
        }}>
          {screen.question}
        </p>
      </div>
      {screen.subtext && (
        <p style={{ fontSize: '12px', color: FAINT, margin: '0 0 20px', lineHeight: 1.55 }}>
          {screen.subtext}
        </p>
      )}
      <div style={{ display: 'flex', gap: '10px' }}>
        <Btn onClick={() => onSubmit('skip')} disabled={loading} style={{ flex: 1 }}>Skip</Btn>
        <Btn primary onClick={() => onSubmit('ok')} disabled={loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : 'Okay'}
        </Btn>
      </div>
    </div>
  )
}

/* ── Screen: if-then (pre-filled textarea) ──────────────────── */

function IfThenScreen({ screen, onSubmit, loading }) {
  const [text, setText] = useState(screen.prefill || '')

  return (
    <div>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        rows={3}
        style={{
          width: '100%', padding: '13px 14px', borderRadius: '12px',
          border: `1px solid ${BORDER}`, background: '#FFFFFF',
          fontSize: '14px', fontFamily: fontSans, color: TEXT,
          resize: 'vertical', lineHeight: 1.6, boxSizing: 'border-box',
          outline: 'none',
        }}
      />
      <p style={{ fontSize: '11px', color: FAINT, marginTop: '6px', marginBottom: '16px' }}>
        Edit to make it yours — the more concrete, the better.
      </p>
      <div style={{ display: 'flex', gap: '10px' }}>
        <Btn onClick={() => onSubmit('__skip__')} disabled={loading} style={{ flex: 1 }}>Skip</Btn>
        <Btn primary onClick={() => onSubmit(text || '__skip__')} disabled={loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>Save & continue <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Exit screens (crisis / pause) ──────────────────────────── */

function ExitScreen({ screen, type, onBack }) {
  const isCrisis = type === 'crisis_exit'
  return (
    <div style={{ paddingTop: '20px' }}>
      {isCrisis && (
        <div style={{
          display: 'flex', gap: '10px', alignItems: 'flex-start',
          background: '#FEF5F2', border: `1px solid ${RED}33`,
          borderRadius: '14px', padding: '16px 18px', marginBottom: '20px',
        }}>
          <AlertTriangle size={18} color={RED} style={{ flexShrink: 0, marginTop: '2px' }} />
          <p style={{ fontSize: '13px', color: RED, margin: 0, fontWeight: 500 }}>
            Your safety comes first.
          </p>
        </div>
      )}
      <div style={{
        fontSize: '14px', color: TEXT, lineHeight: 1.85,
        whiteSpace: 'pre-wrap', marginBottom: '28px',
      }}>
        {renderMarkdown(screen.question)}
      </div>
      <Btn onClick={onBack}>
        <ArrowLeft size={14} strokeWidth={1.8} /> Back to menu
      </Btn>
    </div>
  )
}

/* ── Result screen ───────────────────────────────────────────── */

function ResultScreen({ payload, onBack }) {
  const { closure_text, result } = payload
  if (!result) return null

  const {
    framework_name, evidence, tier,
    hypothesis, technique,
    ifthen_action, selfcompassion_text,
    situation_label, situation_icon,
    emotion_words, unmet_need,
    suds_start, suds_end, track,
  } = result

  const trackLabel = { D: 'Distanced', S: 'Standard', R: 'Deep' }[track] || track

  const TierBadge = ({ t }) => (
    <span style={{
      fontSize: '10px', padding: '2px 8px', borderRadius: '4px',
      background: t === 'A' ? '#F0F7F5' : '#F5F3EB',
      color:       t === 'A' ? ACCENT      : '#8B7D5A',
      fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.1em',
    }}>
      Evidence tier {t}
    </span>
  )

  return (
    <div>
      <button
        onClick={onBack}
        style={{
          display: 'flex', alignItems: 'center', gap: '6px',
          fontSize: '13px', color: FAINT, background: 'none', border: 'none',
          cursor: 'pointer', fontFamily: fontSans, padding: '0 0 24px',
        }}
      >
        <ArrowLeft size={14} strokeWidth={1.8} /> Back to menu
      </button>

      {/* Completion badge */}
      <div style={{
        display: 'inline-block', fontSize: '10px', textTransform: 'uppercase',
        letterSpacing: '0.14em', color: ACCENT, background: '#F0F7F5',
        padding: '3px 9px', borderRadius: '6px', fontWeight: 500, marginBottom: '10px',
      }}>
        Session complete
      </div>

      {/* Closure text */}
      <h2 style={{
        fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400,
        fontSize: '24px', color: TEXT, margin: '0 0 20px', lineHeight: 1.4,
      }}>
        {closure_text}
      </h2>

      {/* Session snapshot */}
      <div style={{
        background: '#FFFFFF', border: `1px solid ${BORDER}`,
        borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
      }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: '0 0 12px' }}>
          Your check-in
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {situation_label && (
            <Row label="Situation" value={`${situation_icon} ${situation_label}`} />
          )}
          {emotion_words?.length > 0 && (
            <Row label="Emotion words" value={emotion_words.join(' · ')} />
          )}
          {unmet_need && (
            <Row label="What was missing" value={unmet_need} />
          )}
          <Row label="Intensity" value={`Started at ${suds_start} → now at ${suds_end}`} />
          {track && <Row label="Depth" value={trackLabel} />}
        </div>
      </div>

      {/* Hypothesis */}
      <div style={{
        background: '#F5F3EB', borderRadius: '14px',
        padding: '16px 18px', marginBottom: '12px',
        border: `1px solid ${BORDER}`,
      }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: '0 0 10px' }}>
          What the pattern looks like
        </p>
        <p style={{ fontSize: '14px', color: TEXT, lineHeight: 1.75, margin: 0 }}>
          {renderMarkdown(hypothesis)}
        </p>
      </div>

      {/* Technique */}
      <div style={{
        background: '#FFFFFF', border: `1.5px solid ${ACCENT}33`,
        borderRadius: '14px', padding: '18px 20px', marginBottom: '12px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', flexWrap: 'wrap' }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: 0 }}>
            Recommended technique
          </p>
          {tier && <TierBadge t={tier} />}
        </div>
        <p style={{ fontSize: '13px', fontWeight: 600, color: TEXT, margin: '0 0 12px' }}>
          {framework_name}
        </p>
        <div style={{ fontSize: '14px', color: TEXT, lineHeight: 1.85, whiteSpace: 'pre-wrap' }}>
          {renderMarkdown(technique)}
        </div>
        {evidence && (
          <p style={{ fontSize: '10px', color: '#B0AEA6', marginTop: '14px', marginBottom: 0, lineHeight: 1.5 }}>
            {evidence}
          </p>
        )}
      </div>

      {/* If-then */}
      {ifthen_action && (
        <div style={{
          background: '#FFFFFF', border: `1px solid ${BORDER}`,
          borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
        }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: '0 0 10px' }}>
            Your if-then plan
          </p>
          <p style={{ fontSize: '14px', color: TEXT, lineHeight: 1.75, margin: 0, fontStyle: 'italic' }}>
            {ifthen_action}
          </p>
        </div>
      )}

      {/* Self-compassion */}
      {selfcompassion_text && (
        <div style={{
          background: '#F5F3EB', borderRadius: '14px',
          padding: '16px 18px', marginBottom: '20px',
          border: `1px solid ${BORDER}`,
        }}>
          <div style={{ display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
            <Heart size={16} color={ACCENT} style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{
              fontSize: '14px', color: TEXT, lineHeight: 1.7, margin: 0,
              fontFamily: fontSerif, fontStyle: 'italic',
            }}>
              {selfcompassion_text}
            </p>
          </div>
        </div>
      )}

      <p style={{ fontSize: '11px', color: '#B0AEA6', lineHeight: 1.6, marginBottom: '32px' }}>
        This session is a self-reflection tool, not a clinical assessment. If you are experiencing significant
        distress, please speak with a licensed mental health professional.
      </p>
    </div>
  )
}

function Row({ label, value }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', padding: '6px 0', borderBottom: `0.5px solid ${BORDER}` }}>
      <span style={{ fontSize: '12px', color: MUTED }}>{label}</span>
      <span style={{ fontSize: '12px', color: TEXT, fontWeight: 500, textAlign: 'right', maxWidth: '60%' }}>{value}</span>
    </div>
  )
}

/* ── Progress stepper ───────────────────────────────────────── */

const STEP_ORDER = ['SAFETY','SUDS_INIT','GROUNDING','SUDS_RERATE','SITUATION','BODY_LOC','BODY_QUAL','EMOTIONS','QUESTION','UNMET_NEED','COMPASSION','IFTHEN','RERATE']

function ProgressDots({ currentStep }) {
  const idx = STEP_ORDER.indexOf(currentStep)
  const pct = idx < 0 ? 0 : Math.round((idx / (STEP_ORDER.length - 1)) * 100)
  return (
    <div style={{ padding: '0 0 24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
        <span style={{ fontSize: '11px', color: FAINT, textTransform: 'uppercase', letterSpacing: '0.12em' }}>Progress</span>
        <span style={{ fontSize: '11px', color: FAINT }}>{pct}%</span>
      </div>
      <div style={{ height: '3px', background: '#EAE8E0', borderRadius: '2px' }}>
        <div style={{ height: '100%', width: `${pct}%`, background: ACCENT, borderRadius: '2px', transition: 'width 0.4s ease' }} />
      </div>
    </div>
  )
}

/* ── Main component ─────────────────────────────────────────── */

export default function AEHQSession({ token, onBack, onDone }) {
  const [sessionId,  setSessionId]  = useState(null)
  const [screen,     setScreen]     = useState(null)
  const [loading,    setLoading]    = useState(false)
  const [starting,   setStarting]   = useState(true)
  const [error,      setError]      = useState('')
  const [resultPay,  setResultPay]  = useState(null)

  const startSession = useCallback(async () => {
    setStarting(true)
    setError('')
    try {
      const data = await api('/start', token, { method: 'POST' })
      setSessionId(data.session_id)
      setScreen(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setStarting(false)
    }
  }, [token])

  useEffect(() => { startSession() }, [startSession])

  const submitAnswer = async (answer) => {
    if (!sessionId || !screen) return
    setLoading(true)
    try {
      const data = await api(`/${sessionId}/answer`, token, {
        method: 'POST',
        body: JSON.stringify({ step: screen.step, answer }),
      })
      if (data.done) {
        if (data.result) {
          setResultPay(data)
          if (onDone) onDone(data.result)
        } else {
          // crisis or pause exit — still show it
          setScreen(data)
        }
      } else {
        setScreen(data)
      }
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const shell = (children) => (
    <div style={{ minHeight: '100vh', background: BG, fontFamily: fontSans, display: 'flex', flexDirection: 'column' }}>
      <style>{`
        @keyframes spin { from{transform:rotate(0deg)} to{transform:rotate(360deg)} }
        input[type=range]::-webkit-slider-thumb { background: ${ACCENT}; }
        textarea:focus { border-color: ${ACCENT} !important; }
      `}</style>
      <div style={{
        display: 'flex', alignItems: 'center', gap: '10px',
        padding: '18px 24px', borderBottom: '0.5px solid rgba(0,0,0,0.07)',
        background: '#FFFFFF',
      }}>
        <button
          onClick={onBack}
          style={{
            display: 'flex', alignItems: 'center', gap: '6px',
            fontSize: '12px', color: FAINT, background: 'none', border: 'none',
            cursor: 'pointer', fontFamily: fontSans, padding: '4px 0',
          }}
        >
          <ArrowLeft size={13} strokeWidth={1.8} />
        </button>
        <div style={{ width: '0.5px', height: '14px', background: BORDER }} />
        <span style={{ fontSize: '13px', color: MUTED, fontWeight: 500 }}>🌿 Emotional Check-in</span>
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: '32px 24px' }}>
        <div style={{ maxWidth: '560px', margin: '0 auto' }}>
          {children}
        </div>
      </div>
    </div>
  )

  // Loading / starting
  if (starting) {
    return shell(
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '80px', gap: '16px' }}>
        <Loader size={20} color={ACCENT} style={{ animation: 'spin 1s linear infinite' }} />
        <p style={{ fontSize: '13px', color: FAINT, margin: 0 }}>Setting things up…</p>
      </div>
    )
  }

  // Error state
  if (error) {
    return shell(
      <div style={{ paddingTop: '60px', textAlign: 'center' }}>
        <p style={{ color: RED, fontSize: '14px', marginBottom: '16px' }}>{error}</p>
        <Btn primary onClick={startSession}>Try again</Btn>
      </div>
    )
  }

  // Done — show result
  if (resultPay) {
    return shell(<ResultScreen payload={resultPay} onBack={onBack} />)
  }

  // Exit screens (crisis / pause)
  if (screen?.done && !screen.result) {
    return shell(<ExitScreen screen={screen} type={screen.exit_type} onBack={onBack} />)
  }

  if (!screen) return shell(null)

  const step = screen.step
  const isTerminal = screen.done

  if (isTerminal) return shell(<ExitScreen screen={screen} type={screen.exit_type} onBack={onBack} />)

  const renderInput = () => {
    const type = screen.type
    // key resets each input's local state when moving between screens of the
    // same type (e.g. BODY_LOC → BODY_QUAL, or consecutive text questions)
    const k = screen.question_id || screen.step
    if (type === 'button_choice')   return <ButtonChoiceScreen   key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'slider')          return <SliderScreen         key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'grounding')       return <GroundingScreen      key={`${k}-${screen.subtext}`} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'grid_select')     return <GridSelectScreen     key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'chip_select')     return <ChipSelectScreen     key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'display_confirm') return <DisplayConfirmScreen key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'text_prefilled')  return <IfThenScreen         key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'text')            return <TextQuestion         key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    if (type === 'single_select')   return <SingleSelectQuestion key={k} screen={screen} onSubmit={submitAnswer} loading={loading} />
    return null
  }

  return shell(
    <>
      <ProgressDots currentStep={step} />

      <ValidationStrip text={screen.validation_copy} />

      {screen.heading && (
        <p style={{
          fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em',
          color: FAINT, margin: '0 0 8px',
        }}>
          {screen.heading}
        </p>
      )}

      <h2 style={{
        fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400,
        fontSize: '22px', color: TEXT, margin: '0 0 6px', lineHeight: 1.4,
      }}>
        {screen.question}
      </h2>

      {screen.subtext && (
        <p style={{ fontSize: '13px', color: FAINT, margin: '0 0 22px', lineHeight: 1.6 }}>
          {renderMarkdown(screen.subtext)}
        </p>
      )}

      {/* Question counter for root-cause questions */}
      {step === 'QUESTION' && screen.q_total > 1 && (
        <p style={{ fontSize: '11px', color: FAINT, margin: '0 0 14px' }}>
          Question {screen.q_num} of {screen.q_total}
        </p>
      )}

      {renderInput()}
    </>
  )
}
