/**
 * AEHQSession — one-screen-at-a-time emotional check-in (AEHQ v2.0)
 *
 * Props:
 *   token     — JWT bearer token
 *   onBack    — called when user wants to exit the session
 *   onDone    — called with result payload when session completes
 */

import { useState, useEffect, useCallback, createContext, useContext } from 'react'
import { ArrowLeft, ArrowRight, Check, Loader, AlertTriangle, Heart, Shield, LifeBuoy, CalendarClock } from 'lucide-react'

const fontSans  = "'Geist', ui-sans-serif, system-ui, sans-serif"
const fontSerif = "'Instrument Serif', ui-serif, Georgia, serif"
const BASE      = '/api/aehq'

/* ── i18n: fixed UI chrome (content comes translated from the API) ──── */
const LangCtx = createContext('th')

const UI = {
  en: {
    header: 'Emotional Check-in', setup: 'Setting things up…', tryAgain: 'Try again',
    back: 'Back to menu', progress: 'Progress',
    cont: 'Continue', skip: 'Skip', okay: 'Okay', saveCont: 'Save & continue',
    doneCheck: 'Done — check in again', tapStart: 'Tap to start', doneWord: 'Done',
    selected: 'selected', qCounter: (a, b) => `Question ${a} of ${b}`,
    typeHere: 'Type here — rough words are fine…',
    editYours: 'Edit to make it yours — the more concrete, the better.',
    safetyFirst: 'Your safety comes first.',
    complete: 'Session complete', yourCheckin: 'Your check-in',
    patternLooks: 'What the pattern looks like', recommendedTech: 'Recommended technique',
    yourIfThen: 'Your if-then plan', checkBack: 'If you want to check back in',
    optional: 'Entirely optional — this session stands on its own.',
    talkHelp: 'Talking to someone might help', lowMoodTitle: 'Worth taking seriously',
    chasingTitle: 'A pattern worth catching early', tier: (t) => `Evidence tier ${t}`,
    blTitle: 'The belief underneath', blBelief: (n) => `You believe this ${n}% right now`,
    blNote: 'Worth noticing — beliefs feel like facts, but this is a snapshot you can revisit.',
    criticTitle: "The critic's job", criticProtects: 'What it says it protects you from',
    hatedTitle: 'Please be gentle with yourself here',
    journeyTitle: 'Your journey so far',
    journeyMoved: (b, from, to) => <>Last time you believed <em>“{b}”</em> <strong>{from}%</strong>. Today: <strong>{to}%</strong>.</>,
    journeyLoosened: (n) => `That's ${n} points looser — visible change, not imagination.`,
    journeySame: 'Holding steady — some beliefs take many small visits to shift.',
    journeyRose: 'It feels stronger today — hard days happen; the practice still holds.',
    goalMoveTitle: 'Toward what you came for', goalMoveVal: (n) => `${n}/10 closer`,
    rGoal: 'Why you came', rSituation: 'Situation', rThought: 'The thought', rEmotion: 'Emotion words', rMissing: 'What was missing',
    rIntensity: 'Intensity', rDepth: 'Depth', started: (a, b) => `Started at ${a} → now at ${b}`,
    trackD: 'Distanced', trackS: 'Standard', trackR: 'Deep',
    goodMoment: (n) => <>A good moment for that is in about <strong>{n}</strong>.</>,
    days: (n) => `${n} days`, months: (n) => `${n} month${n >= 2 ? 's' : ''}`,
    ifthenHours: (h) => <> Your if-then plan is worth checking in the next <strong>{h} hours</strong>.</>,
    disclaimer: 'This session is a self-reflection tool, not a clinical assessment. If you are experiencing significant distress, please speak with a licensed mental health professional.',
  },
  th: {
    header: 'เช็คอินใจ', setup: 'กำลังเตรียมให้คุณ…', tryAgain: 'ลองอีกครั้ง',
    back: 'กลับเมนู', progress: 'ความคืบหน้า',
    cont: 'ต่อไป', skip: 'ข้าม', okay: 'โอเค', saveCont: 'บันทึกแล้วไปต่อ',
    doneCheck: 'เสร็จแล้ว — เช็คอีกครั้ง', tapStart: 'แตะเพื่อเริ่ม', doneWord: 'เสร็จ',
    selected: 'เลือกแล้ว', qCounter: (a, b) => `ข้อ ${a} จาก ${b}`,
    typeHere: 'พิมพ์ตรงนี้ — คำห้วน ๆ ก็ได้…',
    editYours: 'แก้ให้เป็นของคุณ — ยิ่งเป็นรูปธรรมยิ่งดี',
    safetyFirst: 'ความปลอดภัยของคุณมาก่อน',
    complete: 'เซสชันเสร็จสมบูรณ์', yourCheckin: 'สรุปการเช็คอินของคุณ',
    patternLooks: 'แพทเทิร์นนี้เป็นแบบไหน', recommendedTech: 'เทคนิคที่แนะนำ',
    yourIfThen: 'แผน ถ้า…ฉันจะ… ของคุณ', checkBack: 'ถ้าอยากกลับมาเช็คอีกครั้ง',
    optional: 'ไม่บังคับเลย — เซสชันนี้สมบูรณ์ในตัวเอง',
    talkHelp: 'การได้คุยกับใครสักคนอาจช่วยได้', lowMoodTitle: 'เรื่องที่ควรใส่ใจ',
    chasingTitle: 'แพทเทิร์นที่จับได้เร็วยิ่งดี', tier: (t) => `หลักฐานระดับ ${t}`,
    blTitle: 'ความเชื่อที่อยู่ข้างใต้', blBelief: (n) => `ตอนนี้คุณเชื่อประโยคนี้ ${n}%`,
    blNote: 'ลองสังเกตดู — ความเชื่อรู้สึกเหมือนความจริง แต่นี่คือภาพช็อตหนึ่งที่กลับมาดูใหม่ได้',
    criticTitle: 'หน้าที่ของเสียงตำหนิ', criticProtects: 'สิ่งที่มันบอกว่ากำลังปกป้องคุณจาก',
    hatedTitle: 'ขออ่อนโยนกับตัวเองตรงนี้หน่อยนะ',
    journeyTitle: 'เส้นทางของคุณที่ผ่านมา',
    journeyMoved: (b, from, to) => <>ครั้งก่อนคุณเชื่อ <em>“{b}”</em> <strong>{from}%</strong> วันนี้: <strong>{to}%</strong></>,
    journeyLoosened: (n) => `คลายลง ${n} จุด — การเปลี่ยนแปลงที่เห็นได้จริง ไม่ใช่จินตนาการ`,
    journeySame: 'ยังทรงตัวอยู่ — บางความเชื่อต้องใช้การแวะเยือนเล็ก ๆ หลายครั้งกว่าจะขยับ',
    journeyRose: 'วันนี้มันรู้สึกแรงขึ้น — วันแย่ ๆ มีได้ การฝึกยังอยู่กับคุณ',
    goalMoveTitle: 'ใกล้สิ่งที่คุณตั้งใจมา', goalMoveVal: (n) => `ใกล้ขึ้น ${n}/10`,
    rGoal: 'ที่มาที่ทำให้เปิด', rSituation: 'เรื่องที่เข้ามา', rThought: 'ความคิด', rEmotion: 'คำความรู้สึก', rMissing: 'สิ่งที่ขาดหาย',
    rIntensity: 'ความหนักใจ', rDepth: 'ระดับความลึก', started: (a, b) => `เริ่มที่ ${a} → ตอนนี้ ${b}`,
    trackD: 'ผ่อน', trackS: 'มาตรฐาน', trackR: 'ลึก',
    goodMoment: (n) => <>ช่วงที่เหมาะคืออีกประมาณ <strong>{n}</strong></>,
    days: (n) => `${n} วัน`, months: (n) => `${n} เดือน`,
    ifthenHours: (h) => <> แผน ถ้า…ฉันจะ… ของคุณ ควรเช็คภายใน <strong>{h} ชั่วโมง</strong>ข้างหน้า</>,
    disclaimer: 'เซสชันนี้เป็นเครื่องมือสะท้อนใจ ไม่ใช่การประเมินทางคลินิก หากคุณกำลังเผชิญความทุกข์อย่างมาก โปรดปรึกษาผู้เชี่ยวชาญด้านสุขภาพจิต',
  },
}

function useT() {
  const lang = useContext(LangCtx)
  return UI[lang] || UI.en
}

/* Localize a screen payload: swap fields for their _th variants when Thai. */
function localizeScreen(s, lang) {
  if (!s || lang !== 'th') return s
  const pick = (k) => s[k + '_th'] || s[k]
  const out = {
    ...s,
    question: pick('question'), subtext: pick('subtext'),
    heading: pick('heading'), validation_copy: pick('validation_copy'),
    prefill: pick('prefill'), body: pick('body'), optin_label: pick('optin_label'),
    backdraft_note: pick('backdraft_note'),
  }
  if (s.options) out.options = s.options.map((o) => ({ ...o, label: o.label_th || o.label }))
  if (s.slider_labels_th) out.slider_labels = s.slider_labels_th
  return out
}

/* Localize a completed-result payload (nested `result`). */
function localizeResult(payload, lang) {
  if (!payload || lang !== 'th') return payload
  const r = payload.result || {}
  const p = (k) => r[k + '_th'] || r[k]
  const fu = r.followup
  return {
    ...payload,
    closure_text: payload.closure_text_th || payload.closure_text,
    result: {
      ...r,
      framework_name: p('framework_name'), hypothesis: p('hypothesis'),
      technique: p('technique'), ifthen_action: p('ifthen_action'),
      selfcompassion_text: p('selfcompassion_text'), situation_label: p('situation_label'),
      unmet_need: p('unmet_need'), emotion_words: r.emotion_words_th || r.emotion_words,
      trauma_ack: p('trauma_ack'), referral: p('referral'),
      low_mood_note: p('low_mood_note'), chasing_note: p('chasing_note'),
      critic_reframe: p('critic_reframe'), hated_self_note: p('hated_self_note'),
      followup: fu ? { ...fu, checkin: fu.checkin_th || fu.checkin } : fu,
    },
  }
}

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

/* ── Screen: consent gate (PDPA) ────────────────────────────── */

function ConsentScreen({ screen, onSubmit, loading }) {
  const [training, setTraining] = useState(false)
  return (
    <div>
      <div style={{
        background: '#FFFFFF', border: `1px solid ${BORDER}`, borderRadius: '14px',
        padding: '18px 20px', marginBottom: '16px',
        fontSize: '14px', color: TEXT, lineHeight: 1.85, whiteSpace: 'pre-wrap',
      }}>
        {renderMarkdown(screen.body)}
      </div>

      {/* the one separate, optional, default-off opt-in */}
      <label style={{
        display: 'flex', gap: '10px', alignItems: 'flex-start', cursor: 'pointer',
        background: training ? '#F0F7F5' : '#FFFFFF',
        border: `1px solid ${training ? ACCENT : BORDER}`, borderRadius: '12px',
        padding: '13px 15px', marginBottom: '18px', transition: 'all 0.15s',
      }}>
        <input
          type="checkbox" checked={training}
          onChange={e => setTraining(e.target.checked)}
          style={{ marginTop: '2px', width: '16px', height: '16px', accentColor: ACCENT, flexShrink: 0 }}
        />
        <span style={{ fontSize: '13px', color: MUTED, lineHeight: 1.5 }}>{screen.optin_label}</span>
      </label>

      <Btn primary onClick={() => onSubmit({ agreed: true, training })} disabled={loading}>
        {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>{screen.options?.[0]?.label} <ArrowRight size={14} strokeWidth={1.8} /></>}
      </Btn>
    </div>
  )
}

/* ── Screen: slider ─────────────────────────────────────────── */

function SliderScreen({ screen, onSubmit, loading }) {
  const tr = useT()
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
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>{tr.cont} <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Screen: grounding ──────────────────────────────────────── */

function GroundingScreen({ screen, onSubmit, loading }) {
  const tr = useT()
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
    if (phase === 'idle') return tr.tapStart
    if (phase === 'done') return tr.doneWord
    if (count < 4)  return tr === UI.th ? 'หายใจเข้า…' : 'Breathe in…'
    if (count < 11) return tr === UI.th ? 'กลั้นไว้…'   : 'Hold…'
    return tr === UI.th ? 'หายใจออก…' : 'Breathe out…'
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
        {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : tr.doneCheck}
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
  const tr = useT()
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
          {selected.length}/{max} {tr.selected}
        </p>
      )}
      <div style={{ display: 'flex', gap: '10px', marginTop: '20px' }}>
        {canSkip && !hasValue && (
          <Btn onClick={() => onSubmit([])} disabled={loading} style={{ flex: 1 }}>
            {tr.skip}
          </Btn>
        )}
        <Btn primary onClick={() => onSubmit(selected)} disabled={(!hasValue && !canSkip) || loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>{tr.cont} <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Screen: body map (tap where you feel it) ───────────────── */

function BodyMapScreen({ screen, onSubmit, loading }) {
  const tr = useT()
  const [selected, setSelected] = useState([])
  const max = screen.max_select || 3
  const opts = screen.options || []
  const zones = opts.filter(o => o.zone)
  const extras = opts.filter(o => !o.zone)
  const byZone = Object.fromEntries(zones.map(z => [z.zone, z]))

  const toggle = (id) => setSelected(prev =>
    prev.includes(id) ? prev.filter(x => x !== id) : (prev.length >= max ? prev : [...prev, id]))
  const on = (id) => selected.includes(id)
  const canSkip = screen.skippable !== false
  const hasValue = selected.length > 0

  const STATIC = '#EDE9DF', STATIC_L = '#DDD7C8'
  const zFill = (z) => { const o = byZone[z]; return o && on(o.id) ? ACCENT : STATIC }
  const zStroke = (z) => { const o = byZone[z]; return o && on(o.id) ? ACCENT : STATIC_L }
  const tap = (z) => { const o = byZone[z]; if (o) toggle(o.id) }

  const Z = ({ z, children }) => (
    <g onClick={() => tap(z)} style={{ cursor: byZone[z] ? 'pointer' : 'default' }}>{children}</g>
  )

  const selectedLabels = selected
    .map(id => opts.find(o => o.id === id)?.label).filter(Boolean)

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '4px' }}>
        <svg viewBox="0 0 200 360" width="180" height="324" role="img" aria-label="Body map">
          {/* static silhouette — arms, hips, legs */}
          <rect x="40" y="98" width="15" height="104" rx="7.5" fill={STATIC} stroke={STATIC_L} />
          <rect x="145" y="98" width="15" height="104" rx="7.5" fill={STATIC} stroke={STATIC_L} />
          <rect x="66" y="222" width="68" height="20" rx="9" fill={STATIC} stroke={STATIC_L} />
          <rect x="72" y="240" width="24" height="104" rx="10" fill={STATIC} stroke={STATIC_L} />
          <rect x="104" y="240" width="24" height="104" rx="10" fill={STATIC} stroke={STATIC_L} />
          {/* interactive zones */}
          <Z z="head"><circle cx="100" cy="40" r="25" fill={zFill('head')} stroke={zStroke('head')} strokeWidth="1.5" /></Z>
          <Z z="throat"><rect x="86" y="63" width="28" height="17" rx="7" fill={zFill('throat')} stroke={zStroke('throat')} strokeWidth="1.5" /></Z>
          <Z z="shoulders"><rect x="50" y="83" width="100" height="22" rx="11" fill={zFill('shoulders')} stroke={zStroke('shoulders')} strokeWidth="1.5" /></Z>
          <Z z="chest"><rect x="60" y="107" width="80" height="56" rx="18" fill={zFill('chest')} stroke={zStroke('chest')} strokeWidth="1.5" /></Z>
          <Z z="stomach"><rect x="64" y="165" width="72" height="56" rx="20" fill={zFill('stomach')} stroke={zStroke('stomach')} strokeWidth="1.5" /></Z>
        </svg>
      </div>

      {/* selected-zone confirmation chips */}
      {selectedLabels.length > 0 && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', justifyContent: 'center', marginTop: '4px' }}>
          {selectedLabels.map((lbl, i) => (
            <span key={i} style={{ fontSize: '12px', color: ACCENT, background: '#F0F7F5', border: `1px solid ${ACCENT}44`, borderRadius: '999px', padding: '4px 12px' }}>{lbl}</span>
          ))}
        </div>
      )}

      {/* the non-body options as buttons */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', justifyContent: 'center', marginTop: '14px' }}>
        {extras.map(opt => {
          const isOn = on(opt.id)
          return (
            <button key={opt.id} onClick={() => toggle(opt.id)} style={{
              padding: '9px 14px', borderRadius: '999px', cursor: 'pointer',
              border: isOn ? `1.5px solid ${ACCENT}` : `1px solid ${BORDER}`,
              background: isOn ? '#F0F7F5' : '#FFFFFF', color: isOn ? ACCENT : MUTED,
              fontSize: '13px', fontFamily: fontSans, fontWeight: isOn ? 500 : 400,
            }}>{opt.label}</button>
          )
        })}
      </div>

      <p style={{ fontSize: '11px', color: FAINT, marginTop: '12px', textAlign: 'center' }}>{selected.length}/{max}</p>

      <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
        {canSkip && !hasValue && (
          <Btn onClick={() => onSubmit([])} disabled={loading} style={{ flex: 1 }}>{tr.skip}</Btn>
        )}
        <Btn primary onClick={() => onSubmit(selected)} disabled={(!hasValue && !canSkip) || loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>{tr.cont} <ArrowRight size={14} strokeWidth={1.8} /></>}
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
  const tr = useT()
  const [text, setText] = useState('')
  const canSkip = screen.skippable

  return (
    <div>
      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder={tr.typeHere}
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
            {tr.skip}
          </Btn>
        )}
        <Btn primary onClick={() => onSubmit(text || '__skip__')} disabled={loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>{tr.cont} <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Screen: display + confirm (self-compassion) ─────────────── */

function DisplayConfirmScreen({ screen, onSubmit, loading }) {
  const tr = useT()
  const isTH = tr === UI.th
  const opts = screen.options || []
  const pause = opts.find(o => o.id === 'pause')
  const okLabel = opts.find(o => o.id === 'ok')?.label || tr.okay
  const skipLabel = opts.find(o => o.id === 'skip')?.label || tr.skip
  return (
    <div>
      <div style={{
        background: '#F5F3EB', borderRadius: '16px', padding: '20px 22px',
        marginBottom: '16px', border: `1px solid ${BORDER}`,
      }}>
        <Heart size={18} color={ACCENT} style={{ marginBottom: '12px' }} />
        <div style={{
          fontSize: '15px', color: TEXT, lineHeight: 1.75,
          fontFamily: isTH ? fontSans : fontSerif, fontStyle: isTH ? 'normal' : 'italic',
          whiteSpace: 'pre-wrap',
        }}>
          {renderMarkdown(screen.question)}
        </div>
      </div>
      {screen.subtext && (
        <p style={{ fontSize: '12px', color: FAINT, margin: '0 0 16px', lineHeight: 1.55 }}>
          {screen.subtext}
        </p>
      )}
      {/* Backdraft psychoeducation — pain surge is normal, pause is available */}
      {screen.backdraft_note && (
        <div style={{
          background: '#FFFDF7', border: '1px solid #E4D9B8', borderRadius: '12px',
          padding: '13px 15px', marginBottom: '18px', display: 'flex', gap: '10px', alignItems: 'flex-start',
        }}>
          <Shield size={15} color="#8B7D5A" style={{ flexShrink: 0, marginTop: '2px' }} />
          <div style={{ fontSize: '13px', color: TEXT, lineHeight: 1.65 }}>
            {renderMarkdown(screen.backdraft_note)}
          </div>
        </div>
      )}
      <div style={{ display: 'flex', gap: '10px' }}>
        <Btn onClick={() => onSubmit('skip')} disabled={loading} style={{ flex: 1 }}>{skipLabel}</Btn>
        <Btn primary onClick={() => onSubmit('ok')} disabled={loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : okLabel}
        </Btn>
      </div>
      {pause && (
        <Btn onClick={() => onSubmit('pause')} disabled={loading} style={{ width: '100%', marginTop: '10px', color: MUTED }}>
          {pause.label}
        </Btn>
      )}
    </div>
  )
}

/* ── Screen: if-then (pre-filled textarea) ──────────────────── */

function IfThenScreen({ screen, onSubmit, loading }) {
  const tr = useT()
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
        {tr.editYours}
      </p>
      <div style={{ display: 'flex', gap: '10px' }}>
        <Btn onClick={() => onSubmit('__skip__')} disabled={loading} style={{ flex: 1 }}>{tr.skip}</Btn>
        <Btn primary onClick={() => onSubmit(text || '__skip__')} disabled={loading} style={{ flex: 2 }}>
          {loading ? <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} /> : <>{tr.saveCont} <ArrowRight size={14} strokeWidth={1.8} /></>}
        </Btn>
      </div>
    </div>
  )
}

/* ── Exit screens (crisis / pause) ──────────────────────────── */

function ExitScreen({ screen, type, onBack }) {
  const tr = useT()
  const isCrisis = type === 'crisis_exit'
  const body = screen.question_th && tr === UI.th ? screen.question_th : screen.question
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
            {tr.safetyFirst}
          </p>
        </div>
      )}
      <div style={{
        fontSize: '14px', color: TEXT, lineHeight: 1.85,
        whiteSpace: 'pre-wrap', marginBottom: '28px',
      }}>
        {renderMarkdown(body)}
      </div>
      <Btn onClick={onBack}>
        <ArrowLeft size={14} strokeWidth={1.8} /> {tr.back}
      </Btn>
    </div>
  )
}

/* ── Result screen ───────────────────────────────────────────── */

function ResultScreen({ payload, onBack }) {
  const tr = useT()
  const { closure_text, result } = payload
  if (!result) return null

  const {
    framework_name, evidence, tier,
    hypothesis, technique,
    ifthen_action, selfcompassion_text,
    situation_label, situation_icon,
    emotion_words, unmet_need,
    suds_start, suds_end, track,
    trauma_ack, referral, followup,
    low_mood_note, chasing_note,
    goal_text,
    bottom_line_text, bottom_line_belief,
    thought_text,
    critic_reframe, critic_protects_text, hated_self_note,
    goal_attainment, belief_trajectory,
  } = result

  const trackLabel = { D: tr.trackD, S: tr.trackS, R: tr.trackR }[track] || track

  const TierBadge = ({ t }) => (
    <span style={{
      fontSize: '10px', padding: '2px 8px', borderRadius: '4px',
      background: t === 'A' ? '#F0F7F5' : '#F5F3EB',
      color:       t === 'A' ? ACCENT      : '#8B7D5A',
      fontWeight: 500, textTransform: 'uppercase', letterSpacing: '0.1em',
    }}>
      {tr.tier(t)}
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
        <ArrowLeft size={14} strokeWidth={1.8} /> {tr.back}
      </button>

      {/* Completion badge */}
      <div style={{
        display: 'inline-block', fontSize: '10px', textTransform: 'uppercase',
        letterSpacing: '0.14em', color: ACCENT, background: '#F0F7F5',
        padding: '3px 9px', borderRadius: '6px', fontWeight: 500, marginBottom: '10px',
      }}>
        {tr.complete}
      </div>

      {/* Closure text */}
      <h2 style={{
        fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400,
        fontSize: '24px', color: TEXT, margin: '0 0 20px', lineHeight: 1.4,
      }}>
        {closure_text}
      </h2>

      {/* Journey — belief trajectory vs prior sessions (S11 "visible change") */}
      {belief_trajectory && (
        <div style={{
          background: '#F0F7F5', border: `1px solid ${ACCENT}44`,
          borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
        }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: ACCENT, margin: '0 0 10px' }}>
            {tr.journeyTitle}
          </p>
          <p style={{ fontSize: '14px', color: TEXT, lineHeight: 1.7, margin: '0 0 8px' }}>
            {tr.journeyMoved(belief_trajectory.belief, belief_trajectory.prior_belief, belief_trajectory.current_belief)}
          </p>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', margin: '8px 0' }}>
            <span style={{ fontSize: '12px', color: FAINT, minWidth: '30px' }}>{belief_trajectory.prior_belief}%</span>
            <div style={{ flex: 1, height: '6px', background: '#DDE8E3', borderRadius: '3px', position: 'relative' }}>
              <div style={{ position: 'absolute', top: '-3px', left: `${belief_trajectory.prior_belief}%`, width: '2px', height: '12px', background: '#B9C9C2' }} />
              <div style={{ position: 'absolute', top: '-3px', left: `${belief_trajectory.current_belief}%`, width: '3px', height: '12px', background: ACCENT, borderRadius: '2px' }} />
            </div>
            <span style={{ fontSize: '12px', color: ACCENT, fontWeight: 600, minWidth: '30px' }}>{belief_trajectory.current_belief}%</span>
          </div>
          <p style={{ fontSize: '12px', color: MUTED, margin: '6px 0 0', lineHeight: 1.55 }}>
            {belief_trajectory.delta < 0 ? tr.journeyLoosened(Math.abs(belief_trajectory.delta))
              : belief_trajectory.delta === 0 ? tr.journeySame : tr.journeyRose}
          </p>
        </div>
      )}

      {/* Session snapshot */}
      <div style={{
        background: '#FFFFFF', border: `1px solid ${BORDER}`,
        borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
      }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: '0 0 12px' }}>
          {tr.yourCheckin}
        </p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {goal_text && (
            <Row label={tr.rGoal} value={`“${goal_text}”`} />
          )}
          {situation_label && (
            <Row label={tr.rSituation} value={`${situation_icon} ${situation_label}`} />
          )}
          {thought_text && (
            <Row label={tr.rThought} value={`“${thought_text}”`} />
          )}
          {emotion_words?.length > 0 && (
            <Row label={tr.rEmotion} value={emotion_words.join(' · ')} />
          )}
          {unmet_need && (
            <Row label={tr.rMissing} value={unmet_need} />
          )}
          <Row label={tr.rIntensity} value={tr.started(suds_start, suds_end)} />
          {typeof goal_attainment === 'number' && (
            <Row label={tr.goalMoveTitle} value={tr.goalMoveVal(goal_attainment)} />
          )}
          {track && <Row label={tr.rDepth} value={trackLabel} />}
        </div>
      </div>

      {/* Hypothesis */}
      <div style={{
        background: '#F5F3EB', borderRadius: '14px',
        padding: '16px 18px', marginBottom: '12px',
        border: `1px solid ${BORDER}`,
      }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: '0 0 10px' }}>
          {tr.patternLooks}
        </p>
        <p style={{ fontSize: '14px', color: TEXT, lineHeight: 1.75, margin: 0 }}>
          {renderMarkdown(hypothesis)}
        </p>
      </div>

      {/* Bottom Line (S2 formulation) — the core belief + belief-strength % */}
      {bottom_line_text && (
        <div style={{
          background: '#FFFFFF', border: `1px solid ${BORDER}`,
          borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
        }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: '0 0 10px' }}>
            {tr.blTitle}
          </p>
          <p style={{ fontSize: '16px', color: TEXT, lineHeight: 1.5, margin: '0 0 12px', fontFamily: fontSerif, fontStyle: 'italic' }}>
            “{bottom_line_text}”
          </p>
          {typeof bottom_line_belief === 'number' && (
            <>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '6px' }}>
                <div style={{ flex: 1, height: '6px', background: '#EAE8E0', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${bottom_line_belief}%`, background: ACCENT, borderRadius: '3px' }} />
                </div>
                <span style={{ fontSize: '13px', fontWeight: 600, color: ACCENT, minWidth: '36px', textAlign: 'right' }}>
                  {bottom_line_belief}%
                </span>
              </div>
              <p style={{ fontSize: '12px', color: MUTED, margin: '0 0 4px' }}>{tr.blBelief(bottom_line_belief)}</p>
            </>
          )}
          <p style={{ fontSize: '11px', color: '#B0AEA6', margin: '6px 0 0', lineHeight: 1.5 }}>{tr.blNote}</p>
        </div>
      )}

      {/* Inner critic (S5) — protective-intention card */}
      {critic_reframe && (
        <div style={{
          background: '#F5F3EB', border: `1px solid ${BORDER}`,
          borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
        }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: '0 0 10px' }}>
            {tr.criticTitle}
          </p>
          <div style={{ fontSize: '14px', color: TEXT, lineHeight: 1.75 }}>
            {renderMarkdown(critic_reframe)}
          </div>
          {critic_protects_text && (
            <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: `0.5px solid ${BORDER}` }}>
              <p style={{ fontSize: '11px', color: FAINT, margin: '0 0 4px' }}>{tr.criticProtects}</p>
              <p style={{ fontSize: '13px', color: MUTED, margin: 0, fontStyle: 'italic' }}>“{critic_protects_text}”</p>
            </div>
          )}
        </div>
      )}

      {/* Hated-self escalation — warm referral (the unguided-tool supervision flag) */}
      {hated_self_note && (
        <div style={{
          background: '#FEF5F2', border: `1px solid ${RED}33`,
          borderRadius: '14px', padding: '18px 20px', marginBottom: '12px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
            <Heart size={15} color={RED} />
            <p style={{ fontSize: '13px', fontWeight: 600, color: RED, margin: 0 }}>{tr.hatedTitle}</p>
          </div>
          <div style={{ fontSize: '14px', color: TEXT, lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>
            {renderMarkdown(hated_self_note)}
          </div>
        </div>
      )}

      {/* Trauma-safe acknowledgment — explains why we steady rather than go deeper.
          Never probes, never names a diagnosis. */}
      {trauma_ack && (
        <div style={{
          background: '#FFFDF7', border: `1px solid #E4D9B8`,
          borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
          display: 'flex', gap: '10px', alignItems: 'flex-start',
        }}>
          <Shield size={16} color="#8B7D5A" style={{ flexShrink: 0, marginTop: '2px' }} />
          <p style={{ fontSize: '14px', color: TEXT, lineHeight: 1.7, margin: 0 }}>
            {trauma_ack}
          </p>
        </div>
      )}

      {/* Low-mood pattern note — supportive signal, never a diagnosis label */}
      {low_mood_note && (
        <div style={{
          background: '#F0F7F5', border: `1px solid ${ACCENT}44`,
          borderRadius: '14px', padding: '18px 20px', marginBottom: '12px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
            <Heart size={15} color={ACCENT} />
            <p style={{ fontSize: '13px', fontWeight: 600, color: ACCENT, margin: 0 }}>
              {tr.lowMoodTitle}
            </p>
          </div>
          <div style={{ fontSize: '14px', color: TEXT, lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>
            {renderMarkdown(low_mood_note)}
          </div>
        </div>
      )}

      {/* Chasing pattern note — urge support, never a verdict */}
      {chasing_note && (
        <div style={{
          background: '#FFFAF0', border: '1px solid #E4C989',
          borderRadius: '14px', padding: '18px 20px', marginBottom: '12px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
            <Shield size={15} color="#A5812E" />
            <p style={{ fontSize: '13px', fontWeight: 600, color: '#A5812E', margin: 0 }}>
              {tr.chasingTitle}
            </p>
          </div>
          <div style={{ fontSize: '14px', color: TEXT, lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>
            {renderMarkdown(chasing_note)}
          </div>
        </div>
      )}

      {/* Technique */}
      <div style={{
        background: '#FFFFFF', border: `1.5px solid ${ACCENT}33`,
        borderRadius: '14px', padding: '18px 20px', marginBottom: '12px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', flexWrap: 'wrap' }}>
          <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: 0 }}>
            {tr.recommendedTech}
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
            {tr.yourIfThen}
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

      {/* Follow-up — opt-in. Sessions are self-contained; this just plants a marker. */}
      {followup && (
        <div style={{
          background: '#FFFFFF', border: `1px solid ${BORDER}`,
          borderRadius: '14px', padding: '16px 18px', marginBottom: '12px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px' }}>
            <CalendarClock size={14} color={FAINT} />
            <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: FAINT, margin: 0 }}>
              {tr.checkBack}
            </p>
          </div>
          <p style={{ fontSize: '14px', color: TEXT, lineHeight: 1.7, margin: '0 0 10px', fontStyle: 'italic' }}>
            “{followup.checkin}”
          </p>
          <p style={{ fontSize: '12px', color: MUTED, margin: 0, lineHeight: 1.6 }}>
            {tr.goodMoment(followup.interval_days >= 30
              ? tr.months(Math.round(followup.interval_days / 30))
              : tr.days(followup.interval_days))}
            {ifthen_action && followup.action_check_hours && tr.ifthenHours(followup.action_check_hours)}
          </p>
          <p style={{ fontSize: '11px', color: '#B0AEA6', margin: '10px 0 0', lineHeight: 1.5 }}>
            {tr.optional}
          </p>
        </div>
      )}

      {/* Warm referral — choice-preserving, never forced disclosure */}
      {referral && (
        <div style={{
          background: '#FEF5F2', border: `1px solid ${RED}33`,
          borderRadius: '14px', padding: '18px 20px', marginBottom: '20px',
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px' }}>
            <LifeBuoy size={16} color={RED} />
            <p style={{ fontSize: '13px', fontWeight: 600, color: RED, margin: 0 }}>
              {tr.talkHelp}
            </p>
          </div>
          <div style={{ fontSize: '14px', color: TEXT, lineHeight: 1.8, whiteSpace: 'pre-wrap' }}>
            {renderMarkdown(referral)}
          </div>
        </div>
      )}

      <p style={{ fontSize: '11px', color: '#B0AEA6', lineHeight: 1.6, marginBottom: '32px' }}>
        {tr.disclaimer}
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

const STEP_ORDER = ['CONSENT','SAFETY','SUDS_INIT','GROUNDING','SUDS_RERATE','SITUATION','GOAL','BODY_LOC','BODY_QUAL','EMOTIONS','QUESTION','BELIEF','MOOD1','MOOD2','UNMET_NEED','FOC','COMPASSION','SOOTHE','IFTHEN','GOAL_ATTAIN','RERATE']

function ProgressDots({ currentStep }) {
  const tr = useT()
  const idx = STEP_ORDER.indexOf(currentStep)
  const pct = idx < 0 ? 0 : Math.round((idx / (STEP_ORDER.length - 1)) * 100)
  return (
    <div style={{ padding: '0 0 24px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
        <span style={{ fontSize: '11px', color: FAINT, textTransform: 'uppercase', letterSpacing: '0.12em' }}>{tr.progress}</span>
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
  const [lang,       setLang]       = useState(() => localStorage.getItem('aehq_lang') || 'th')
  const t = UI[lang] || UI.en
  const setLangPersist = (l) => { setLang(l); try { localStorage.setItem('aehq_lang', l) } catch {} }

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
        body: JSON.stringify({ step: screen.step, answer, lang }),
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

  const LangToggle = () => (
    <div style={{ marginLeft: 'auto', display: 'flex', gap: '2px', background: '#F0EFE9', borderRadius: '999px', padding: '2px' }}>
      {['th', 'en'].map(l => (
        <button
          key={l}
          onClick={() => setLangPersist(l)}
          aria-pressed={lang === l}
          style={{
            fontSize: '11px', fontWeight: 600, letterSpacing: '0.04em',
            padding: '4px 12px', borderRadius: '999px', border: 'none', cursor: 'pointer',
            fontFamily: fontSans,
            background: lang === l ? '#FFFFFF' : 'transparent',
            color: lang === l ? ACCENT : FAINT,
            boxShadow: lang === l ? '0 1px 2px rgba(0,0,0,0.08)' : 'none',
            transition: 'all 0.15s',
          }}
        >
          {l === 'th' ? 'ไทย' : 'EN'}
        </button>
      ))}
    </div>
  )

  const shell = (children) => (
    <LangCtx.Provider value={lang}>
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
        <span style={{ fontSize: '13px', color: MUTED, fontWeight: 500 }}>🌿 {t.header}</span>
        <LangToggle />
      </div>
      <div style={{ flex: 1, overflowY: 'auto', padding: '32px 24px' }}>
        <div style={{ maxWidth: '560px', margin: '0 auto' }}>
          {children}
        </div>
      </div>
    </div>
    </LangCtx.Provider>
  )

  // Loading / starting
  if (starting) {
    return shell(
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '80px', gap: '16px' }}>
        <Loader size={20} color={ACCENT} style={{ animation: 'spin 1s linear infinite' }} />
        <p style={{ fontSize: '13px', color: FAINT, margin: 0 }}>{t.setup}</p>
      </div>
    )
  }

  // Error state
  if (error) {
    return shell(
      <div style={{ paddingTop: '60px', textAlign: 'center' }}>
        <p style={{ color: RED, fontSize: '14px', marginBottom: '16px' }}>{error}</p>
        <Btn primary onClick={startSession}>{t.tryAgain}</Btn>
      </div>
    )
  }

  // Done — show result (localized)
  if (resultPay) {
    return shell(<ResultScreen payload={localizeResult(resultPay, lang)} onBack={onBack} />)
  }

  // Exit screens (crisis / pause)
  if (screen?.done && !screen.result) {
    return shell(<ExitScreen screen={screen} type={screen.exit_type} onBack={onBack} />)
  }

  if (!screen) return shell(null)

  const S = localizeScreen(screen, lang)   // localized copy of the current screen
  const step = screen.step
  const isTerminal = screen.done

  if (isTerminal) return shell(<ExitScreen screen={screen} type={screen.exit_type} onBack={onBack} />)

  const renderInput = () => {
    const type = S.type
    // key resets each input's local state when moving between screens of the
    // same type (e.g. BODY_LOC → BODY_QUAL, or consecutive text questions)
    const k = S.question_id || S.step
    if (type === 'consent')         return <ConsentScreen        key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'button_choice')   return <ButtonChoiceScreen   key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'slider')          return <SliderScreen         key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'grounding')       return <GroundingScreen      key={`${k}-${S.subtext}`} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'grid_select')     return <GridSelectScreen     key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'body_map')        return <BodyMapScreen        key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'chip_select')     return <ChipSelectScreen     key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'display_confirm') return <DisplayConfirmScreen key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'text_prefilled')  return <IfThenScreen         key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'text')            return <TextQuestion         key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    if (type === 'single_select')   return <SingleSelectQuestion key={k} screen={S} onSubmit={submitAnswer} loading={loading} />
    return null
  }

  return shell(
    <>
      <ProgressDots currentStep={step} />

      <ValidationStrip text={S.validation_copy} />

      {S.heading && (
        <p style={{
          fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em',
          color: FAINT, margin: '0 0 8px',
        }}>
          {S.heading}
        </p>
      )}

      <h2 style={{
        fontFamily: lang === 'th' ? fontSans : fontSerif,
        fontStyle: lang === 'th' ? 'normal' : 'italic',
        fontWeight: lang === 'th' ? 500 : 400,
        fontSize: lang === 'th' ? '20px' : '22px', color: TEXT, margin: '0 0 6px', lineHeight: 1.5,
      }}>
        {S.question}
      </h2>

      {S.subtext && (
        <p style={{ fontSize: '13px', color: FAINT, margin: '0 0 22px', lineHeight: 1.6 }}>
          {renderMarkdown(S.subtext)}
        </p>
      )}

      {/* Question counter for root-cause questions */}
      {step === 'QUESTION' && S.q_total > 1 && (
        <p style={{ fontSize: '11px', color: FAINT, margin: '0 0 14px' }}>
          {t.qCounter(S.q_num, S.q_total)}
        </p>
      )}

      {renderInput()}
    </>
  )
}
