import { useState, useEffect, useMemo, useCallback, useRef } from 'react'
import { ArrowLeft, ArrowRight, Shuffle, Check, LifeBuoy, Wind } from 'lucide-react'

/* ------------------------------------------------------------------ */
/*  Guided Neuro session — the full 11-stage flow from Session_Logic    */
/*  (stages 0-10). Rule-based, no AI. Neuro deck only for this POC.      */
/* ------------------------------------------------------------------ */

const fontSans  = "'Geist', 'Noto Sans Thai', ui-sans-serif, system-ui, sans-serif"
const fontSerif = "'Instrument Serif', 'Noto Serif Thai', ui-serif, Georgia, serif"

const PAL = {
  ink: '#3A3A3A', paper: '#FAF7F2', bg: '#FAFAF6', muted: '#9A9A95',
  accent: '#C77B54', tint: '#FBF1EA', border: '#F0D6C4',
}

const CONSENT_VERSION = 'cards-guided-1'

/* Crisis-language routing (Session_Logic stage 1 safety gate).
   Deliberately broad and low-precision — a false positive just offers help. */
const CRISIS_TERMS = [
  'kill myself', 'suicide', 'suicidal', 'end my life', 'want to die', 'wanna die',
  'hurt myself', 'harm myself', 'self-harm', 'self harm', 'cut myself',
  'no reason to live', 'better off dead', "don't want to live", 'dont want to live',
  'ฆ่าตัวตาย', 'อยากตาย', 'ทำร้ายตัวเอง', 'ไม่อยากมีชีวิต', 'จบชีวิต', 'ไม่อยากอยู่',
]
const looksLikeCrisis = (txt) => {
  const s = (txt || '').toLowerCase()
  return CRISIS_TERMS.some(k => s.includes(k))
}

const INTENTION_TAGS = [
  { en: 'A feeling I want to understand', th: 'อารมณ์ที่อยากเข้าใจ' },
  { en: 'A decision I am sitting with',   th: 'เรื่องที่กำลังตัดสินใจ' },
  { en: 'A relationship',                 th: 'ความสัมพันธ์' },
  { en: 'Something at work',              th: 'เรื่องงาน' },
  { en: 'Just checking in with myself',   th: 'แค่สำรวจใจตัวเอง' },
]

const NS_CUES = [
  { id: 'breath', en: 'Slow breathing — longer out-breath', th: 'หายใจช้า ๆ ให้ลมหายใจออกยาวขึ้น',
    body_en: 'Breathe in for 4, out for 6. Three gentle rounds. No breath-holding.',
    body_th: 'หายใจเข้านับ 4 หายใจออกนับ 6 สัก 3 รอบเบา ๆ ไม่ต้องกลั้นหายใจ' },
  { id: 'orient', en: 'Orient — five things you can see', th: 'มองรอบตัว — ห้าสิ่งที่มองเห็น',
    body_en: 'Name five things you can see, four you can hear, three you can touch.',
    body_th: 'บอกชื่อห้าสิ่งที่เห็น สี่เสียงที่ได้ยิน สามสิ่งที่สัมผัสได้' },
  { id: 'space', en: 'Just take a little space', th: 'ขอพื้นที่ให้ตัวเองสักหน่อย',
    body_en: 'Rest your eyes for a moment. There is no rush.', th_body: '',
    body_th: 'พักสายตาสักครู่ ไม่ต้องรีบ' },
]

const STAGE_META = [
  { key: 'consent',    en: 'Consent',        th: 'ความยินยอม' },
  { key: 'arrival',    en: 'Arrival',        th: 'ตั้งหลัก' },
  { key: 'intention',  en: 'Intention',      th: 'ตั้งใจ' },
  { key: 'draw',       en: 'Draw',           th: 'จั่วไพ่' },
  { key: 'observe',    en: 'Observe',        th: 'สังเกต' },
  { key: 'meaning',    en: 'Meaning',        th: 'ความหมาย' },
  { key: 'support',    en: 'Steady',         th: 'ปรับสมดุล' },
  { key: 'reframe',    en: 'Choice',         th: 'ทางเลือก' },
  { key: 'action',     en: 'Small step',     th: 'ก้าวเล็ก ๆ' },
  { key: 'integrate',  en: 'Carry forward',  th: 'เก็บกลับไป' },
  { key: 'feedback',   en: 'Feedback',       th: 'สะท้อนกลับ' },
]

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

/* ---- small presentational card (image with graceful fallback) ---- */
function CardMini({ card, lang, size = 150 }) {
  const [err, setErr] = useState(false)
  const name = lang === 'th' ? card.name_th : card.name_en
  return (
    <div style={{ width: size, maxWidth: '46vw' }}>
      <div style={{
        aspectRatio: '2 / 3', borderRadius: '12px', overflow: 'hidden',
        background: PAL.paper, border: `1px solid ${PAL.border}`,
        boxShadow: '0 6px 18px -10px rgba(0,0,0,0.3)',
        display: 'flex', flexDirection: 'column',
      }}>
        <div style={{ flex: 1, minHeight: 0, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          {card.image && !err ? (
            <img src={'/' + card.image} alt="" onError={() => setErr(true)}
              style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }} />
          ) : (
            <span style={{ fontSize: '30px' }}>🌫️</span>
          )}
        </div>
        <div style={{ padding: '6px 6px 9px', textAlign: 'center', fontFamily: fontSerif, fontStyle: 'italic', fontSize: '13px', color: PAL.ink }}>
          {name}
        </div>
      </div>
    </div>
  )
}

/* ---- reusable inputs ---- */
function Slider({ value, onChange, min = 0, max = 10, labelLeft, labelRight }) {
  return (
    <div>
      <input
        type="range" min={min} max={max} value={value ?? min}
        onChange={e => onChange(Number(e.target.value))}
        style={{ width: '100%', accentColor: PAL.accent }}
      />
      <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: PAL.muted, marginTop: '2px' }}>
        <span>{labelLeft}</span>
        <span style={{ fontWeight: 600, color: PAL.accent, fontSize: '14px' }}>{value ?? min}</span>
        <span>{labelRight}</span>
      </div>
    </div>
  )
}

function Field({ label, value, onChange, placeholder, rows = 3 }) {
  return (
    <div style={{ marginBottom: '16px' }}>
      {label && <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', marginBottom: '7px', lineHeight: 1.45 }}>{label}</label>}
      <textarea
        value={value} onChange={e => onChange(e.target.value)} rows={rows} placeholder={placeholder}
        style={{
          width: '100%', padding: '11px 13px', fontSize: '14px', lineHeight: 1.6,
          background: '#fff', border: '1px solid rgba(0,0,0,0.12)', borderRadius: '11px',
          outline: 'none', resize: 'vertical', fontFamily: fontSans, color: '#1B1B19', boxSizing: 'border-box',
        }}
      />
    </div>
  )
}

/* Module-level so their identity is stable across renders (otherwise the
   textareas inside would remount and lose focus on every keystroke). */
function PrimaryBtn({ onClick, disabled, children }) {
  return (
    <button onClick={onClick} disabled={disabled}
      style={{
        display: 'flex', alignItems: 'center', gap: '7px', padding: '12px 24px', borderRadius: '999px', border: 'none',
        background: disabled ? '#E5E5E0' : PAL.accent, color: disabled ? '#9A9A95' : '#fff',
        fontSize: '14px', fontWeight: 500, fontFamily: fontSans, cursor: disabled ? 'not-allowed' : 'pointer',
        boxShadow: disabled ? 'none' : '0 6px 16px -8px rgba(0,0,0,0.3)',
      }}>
      {children}<ArrowRight size={15} strokeWidth={1.8} />
    </button>
  )
}

function StageBody({ t, title, subtitle, children, onNext, nextLabel, nextDisabled }) {
  return (
    <div className="gs-fade" style={{ maxWidth: '560px', margin: '0 auto', padding: '28px 24px 56px', width: '100%' }}>
      <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: 'clamp(23px,4.6vw,30px)', color: '#1B1B19', margin: '0 0 8px', lineHeight: 1.35 }}>{title}</h1>
      {subtitle && <p style={{ fontSize: '13.5px', color: '#7A7A72', margin: '0 0 22px', lineHeight: 1.55 }}>{subtitle}</p>}
      {children}
      {onNext && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '24px' }}>
          <PrimaryBtn onClick={onNext} disabled={nextDisabled}>{nextLabel || t('Continue', 'ต่อไป')}</PrimaryBtn>
        </div>
      )}
    </div>
  )
}

/* ================================================================== */

export default function GuidedSession({ onBack, token }) {
  const [lang, setLang] = useState('en')
  const t = useCallback((en, th) => (lang === 'th' ? th : en), [lang])

  const [data, setData]     = useState(null)
  const [loadErr, setLoadErr] = useState('')
  const [manifest, setManifest] = useState(null)   // Set of delivered N-XX basenames
  const [thStrings, setThStrings] = useState({})   // Thai copy for English-only card content
  const [stage, setStage]   = useState(0)          // index into STAGE_META
  const [crisis, setCrisis] = useState(false)      // safety override screen

  // collected session data
  const [consent, setConsent]           = useState(false)
  const [trainingOptIn, setTrainingOptIn] = useState(false)
  const [activationBefore, setActBefore] = useState(3)
  const [bodyState, setBodyState]       = useState('')
  const [arrivalPhase, setArrivalPhase] = useState('assess')  // assess | grounding
  const [intention, setIntention]       = useState('')
  const [intentionTag, setIntentionTag] = useState(null)
  const [drawn, setDrawn]               = useState(null)
  const [fan, setFan]                   = useState([])
  const [redraws, setRedraws]           = useState(0)
  const [notice, setNotice]             = useState('')
  const [feeling, setFeeling]           = useState('')
  const [association, setAssociation]   = useState('')
  const [userMeaning, setUserMeaning]   = useState('')
  const [hypoFit, setHypoFit]           = useState({})        // {idx: 'fits'|'partly'|'no'}
  const [nsCue, setNsCue]               = useState(null)
  const [activationMid, setActMid]      = useState(3)
  const [need, setNeed]                 = useState('')
  const [value, setValue]               = useState('')
  const [choicePoint, setChoicePoint]   = useState('')
  const [microAction, setMicroAction]   = useState('')
  const [confidence, setConfidence]     = useState(6)
  const [summary, setSummary]           = useState('')
  const [anchor, setAnchor]             = useState('')
  const [activationAfter, setActAfter]  = useState(3)
  const [helpfulness, setHelpfulness]   = useState(7)
  const [resonance, setResonance]       = useState(7)
  const [safetyRating, setSafetyRating] = useState(8)
  const [consentToStore, setConsentToStore] = useState(false)

  const [saveState, setSaveState] = useState('idle')
  const [saveErr, setSaveErr]     = useState('')
  const safetyEventRef = useRef(null)   // records if a crisis gate fired

  /* fonts + data */
  useEffect(() => {
    const id = 'auth-fonts'
    if (!document.getElementById(id)) {
      const link = document.createElement('link')
      link.id = id; link.rel = 'stylesheet'
      link.href = 'https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&family=Noto+Sans+Thai:wght@300;400;500;600;700&family=Noto+Serif+Thai:wght@400;500;600&display=swap'
      document.head.appendChild(link)
    }
  }, [])
  useEffect(() => {
    fetch('/cards.json')
      .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json() })
      .then(setData).catch(e => setLoadErr(e.message))
    fetch('/neuro/manifest.json')
      .then(r => (r.ok ? r.json() : []))
      .then(list => setManifest(new Set(list)))
      .catch(() => setManifest(new Set()))
    fetch('/api/cards/i18n/th')
      .then(r => (r.ok ? r.json() : { strings: {} }))
      .then(b => setThStrings(b.strings || {}))
      .catch(() => setThStrings({}))
  }, [])

  // English -> Thai lookup (micro_intervention etc.) with fallback to English.
  const th = useCallback((en) => (en ? (thStrings[en] || en) : en), [thStrings])

  // Only Neuro cards whose art is actually in the folder (manifest).
  const neuroCards = useMemo(() => {
    if (!data || !manifest) return []
    return data.cards.filter(c => {
      if (c.deck !== 'neuro') return false
      const base = (c.image || '').split('/').pop().replace(/\.\w+$/, '')
      return manifest.has(base)
    })
  }, [data, manifest])

  /* tentative hypotheses for the meaning stage — built from the drawn card,
     never asserted as fact (Session_Logic stage 5). */
  const hypotheses = useMemo(() => {
    if (!drawn) return []
    const out = []
    if (drawn.archetype) out.push(t(`this touches on ${drawn.archetype.toLowerCase()}`, `เรื่องนี้เกี่ยวข้องกับ${drawn.archetype}`))
    if (drawn.meaning_en) out.push(lang === 'th' ? drawn.meaning_th : drawn.meaning_en)
    if (drawn.reflect_prompt_en) out.push(lang === 'th' ? drawn.reflect_prompt_th : drawn.reflect_prompt_en)
    return out.slice(0, 3)
  }, [drawn, lang, t])

  const guard = useCallback((...texts) => {
    if (texts.some(looksLikeCrisis)) {
      safetyEventRef.current = { risk_type: 'reality-testing-or-self-harm-language', action_taken: 'crisis_info', at: new Date().toISOString() }
      setCrisis(true)
      return true
    }
    return false
  }, [])

  const buildFan = useCallback(() => {
    setFan(shuffle(neuroCards).slice(0, Math.min(9, neuroCards.length)))
  }, [neuroCards])

  const next = () => setStage(s => Math.min(STAGE_META.length - 1, s + 1))
  const prev = () => {
    if (stage === 0) onBack()
    else setStage(s => s - 1)
  }

  // Use the free-text intention, or fall back to the chosen chip's label.
  const effectiveIntention = () =>
    intention.trim() || (intentionTag != null ? t(INTENTION_TAGS[intentionTag].en, INTENTION_TAGS[intentionTag].th) : null)

  const sessionPayload = () => ({
    consent_version: CONSENT_VERSION,
    consent, training_opt_in: trainingOptIn,
    activation_before: activationBefore, body_state: bodyState || null,
    intention: effectiveIntention(), intention_tag: intentionTag,
    selected_card_id: drawn?.id || null, redraws,
    observations: { notice: notice || null, feeling: feeling || null, association: association || null },
    user_meaning: userMeaning || null,
    hypotheses, hypothesis_fit: hypoFit,
    ns_cue: nsCue, activation_mid: activationMid,
    need: need || null, value: value || null, choice_point: choicePoint || null,
    micro_action: microAction || null, confidence_0_10: confidence,
    session_summary: summary || null, anchor: anchor || null,
    activation_after: activationAfter,
    feedback: { helpfulness, resonance, safety_rating: safetyRating, consent_to_store: consentToStore },
    safety_event: safetyEventRef.current,
    lang,
  })

  const finish = async () => {
    setSaveState('saving'); setSaveErr('')
    try {
      const headers = { 'Content-Type': 'application/json' }
      if (token) headers['Authorization'] = `Bearer ${token}`
      const res = await fetch('/api/cards/readings', {
        method: 'POST', headers,
        body: JSON.stringify({
          deck: 'neuro', spread_id: 'guided', spread_name: t('Guided session', 'เซสชันแบบมีไกด์'),
          cards: drawn ? [{ card_id: drawn.id, position: t('Guided', 'มีไกด์') }] : [],
          reflection: userMeaning || notice || null,
          intention: effectiveIntention(),
          activation_before: activationBefore,
          lang, mode: 'guided', session: sessionPayload(),
        }),
      })
      if (!res.ok) {
        const b = await res.json().catch(() => null)
        throw new Error(b?.detail || `Save failed (${res.status})`)
      }
      setSaveState('saved')
    } catch (e) { setSaveState('error'); setSaveErr(e.message) }
  }

  /* ---------- chrome ---------- */
  const header = (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '16px 20px', borderBottom: '0.5px solid rgba(0,0,0,0.07)', background: '#fff',
      position: 'sticky', top: 0, zIndex: 10,
    }}>
      <button onClick={crisis ? () => setCrisis(false) : prev}
        style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px', color: '#7A7A72', background: 'none', border: 'none', cursor: 'pointer', fontFamily: fontSans, padding: '6px 8px', borderRadius: '8px' }}>
        <ArrowLeft size={15} strokeWidth={1.8} />
        {stage === 0 && !crisis ? t('Exit', 'ออก') : t('Back', 'ย้อนกลับ')}
      </button>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.16em', color: PAL.muted }}>
          {t('Guided session', 'เซสชันแบบมีไกด์')}
        </span>
        <button onClick={() => setLang(lang === 'en' ? 'th' : 'en')}
          style={{ fontSize: '12px', fontWeight: 500, color: '#1B1B19', background: '#F0EFE8', border: 'none', cursor: 'pointer', fontFamily: fontSans, padding: '6px 10px', borderRadius: '999px' }}>
          {lang === 'en' ? 'ไทย' : 'EN'}
        </button>
      </div>
    </div>
  )

  const progress = !crisis && (
    <div style={{ maxWidth: '620px', margin: '0 auto', padding: '18px 24px 0', width: '100%' }}>
      <div style={{ display: 'flex', gap: '4px' }}>
        {STAGE_META.map((s, i) => (
          <div key={s.key} style={{ flex: 1, height: '4px', borderRadius: '2px', background: i <= stage ? PAL.accent : '#EAE7DF', transition: 'background 0.3s' }} />
        ))}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '8px' }}>
        <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.14em', color: PAL.accent }}>
          {t(STAGE_META[stage].en, STAGE_META[stage].th)}
        </span>
        <span style={{ fontSize: '11px', color: PAL.muted }}>{stage + 1} / {STAGE_META.length}</span>
      </div>
    </div>
  )

  const shell = (children) => (
    <div lang={lang} style={{ minHeight: '100vh', background: PAL.bg, fontFamily: fontSans, display: 'flex', flexDirection: 'column' }}>
      <style>{`
        @keyframes gs-fade { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:translateY(0) } }
        .gs-fade { animation: gs-fade 0.35s cubic-bezier(0.22,1,0.36,1) both; }
        /* Thai tone marks/vowels stack on the base consonant — extra letter-spacing
           (used for uppercase EN eyebrow labels) visually separates them. */
        [lang="th"], [lang="th"] * { letter-spacing: normal !important; }
      `}</style>
      {header}{progress}
      <div style={{ flex: 1 }}>{children}</div>
    </div>
  )


  const disclaimer = (
    <p style={{ fontSize: '11px', color: PAL.muted, textAlign: 'center', margin: '0 auto', maxWidth: '480px', lineHeight: 1.5, paddingTop: '24px' }}>
      {data ? t(data.disclaimer_en, data.disclaimer_th) : t('For self-reflection only — not medical or psychological treatment.', 'เพื่อการทบทวนตนเองเท่านั้น')}
    </p>
  )

  /* ---------- states: loading / error / crisis ---------- */
  if (loadErr) return shell(<div style={{ padding: '60px 24px', textAlign: 'center', color: '#C84B31' }}>{loadErr}</div>)
  if (!data || !manifest) return shell(<div style={{ padding: '80px', textAlign: 'center' }}><div style={{ width: '8px', height: '8px', borderRadius: '50%', background: PAL.accent, opacity: 0.6, margin: '0 auto' }} /></div>)

  if (crisis) {
    return shell(
      <div className="gs-fade" style={{ maxWidth: '540px', margin: '0 auto', padding: '32px 24px 56px', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '14px', color: PAL.accent }}>
          <LifeBuoy size={22} strokeWidth={1.8} />
          <span style={{ fontSize: '12px', textTransform: 'uppercase', letterSpacing: '0.14em' }}>{t('You are not alone', 'คุณไม่ได้อยู่คนเดียว')}</span>
        </div>
        <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: '28px', color: '#1B1B19', margin: '0 0 14px', lineHeight: 1.35 }}>
          {t('It sounds like this is really heavy right now.', 'ดูเหมือนตอนนี้มันหนักมากจริง ๆ')}
        </h1>
        <p style={{ fontSize: '14px', color: '#5A5A52', lineHeight: 1.65, margin: '0 0 18px' }}>
          {t('This tool is for gentle reflection and cannot help in a crisis. Please reach a real person who can — you deserve support right now.',
             'เครื่องมือนี้ไว้สำหรับทบทวนใจเบา ๆ และช่วยในภาวะวิกฤตไม่ได้ กรุณาติดต่อคนจริง ๆ ที่ช่วยได้ คุณสมควรได้รับการดูแลในตอนนี้')}
        </p>
        <div style={{ background: '#fff', border: `1px solid ${PAL.border}`, borderRadius: '14px', padding: '16px 18px', marginBottom: '20px' }}>
          {[
            { label: t('Thailand · Mental Health Hotline', 'ประเทศไทย · สายด่วนสุขภาพจิต'), val: '1323', note: t('24 hours, free', 'ตลอด 24 ชม. ฟรี') },
            { label: t('Samaritans Thailand', 'สมาริตันส์ ไทยแลนด์'), val: '02-113-6789', note: '' },
            { label: t('Emergency (medical)', 'ฉุกเฉิน (การแพทย์)'), val: '1669', note: '' },
          ].map((r, i) => (
            <div key={i} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', padding: '8px 0', borderBottom: i < 2 ? '0.5px solid rgba(0,0,0,0.06)' : 'none' }}>
              <div>
                <div style={{ fontSize: '13px', color: '#1B1B19', fontWeight: 500 }}>{r.label}</div>
                {r.note && <div style={{ fontSize: '11px', color: PAL.muted }}>{r.note}</div>}
              </div>
              <a href={`tel:${r.val.replace(/[^0-9]/g, '')}`} style={{ fontSize: '16px', fontWeight: 600, color: PAL.accent, textDecoration: 'none' }}>{r.val}</a>
            </div>
          ))}
        </div>
        <p style={{ fontSize: '12px', color: PAL.muted, lineHeight: 1.55, marginBottom: '22px' }}>
          {t('If you are in immediate danger, contact your local emergency number right away.',
             'หากคุณกำลังตกอยู่ในอันตรายเฉพาะหน้า โปรดโทรหาเบอร์ฉุกเฉินในพื้นที่ทันที')}
        </p>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button onClick={() => setCrisis(false)}
            style={{ padding: '11px 20px', borderRadius: '999px', border: '1px solid rgba(0,0,0,0.14)', background: '#fff', color: '#1B1B19', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer' }}>
            {t("I'm safe — go back", 'ฉันปลอดภัย — กลับไป')}
          </button>
          <button onClick={onBack}
            style={{ padding: '11px 20px', borderRadius: '999px', border: 'none', background: PAL.accent, color: '#fff', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer' }}>
            {t('Close session', 'ปิดเซสชัน')}
          </button>
        </div>
      </div>
    )
  }

  const key = STAGE_META[stage].key

  /* ================= STAGE 0 — Consent & Scope ================= */
  if (key === 'consent') {
    return shell(
      <StageBody t={t}
        title={t('Before we begin', 'ก่อนเริ่มต้น')}
        subtitle={t('This is a reflective tool — not fortune-telling, diagnosis, or a replacement for care. You lead; you can pause or stop anytime.',
                    'นี่คือเครื่องมือทบทวนใจ ไม่ใช่การทำนาย การวินิจฉัย หรือการทดแทนการดูแลรักษา คุณเป็นผู้นำ และหยุดพักหรือยุติเมื่อไหร่ก็ได้')}
        onNext={next} nextDisabled={!consent} nextLabel={t('I understand — begin', 'เข้าใจแล้ว — เริ่ม')}
      >
        <label style={{ display: 'flex', gap: '10px', alignItems: 'flex-start', background: '#fff', border: `1px solid ${consent ? PAL.accent : 'rgba(0,0,0,0.12)'}`, borderRadius: '12px', padding: '14px', cursor: 'pointer', marginBottom: '12px' }}>
          <input type="checkbox" checked={consent} onChange={e => setConsent(e.target.checked)} style={{ marginTop: '2px', accentColor: PAL.accent }} />
          <span style={{ fontSize: '13.5px', color: '#3A3A3A', lineHeight: 1.5 }}>
            {t('I understand this is for self-reflection only, and I am choosing to continue.',
               'ฉันเข้าใจว่านี่เป็นการทบทวนตนเองเท่านั้น และฉันเลือกที่จะทำต่อ')}
          </span>
        </label>
        <label style={{ display: 'flex', gap: '10px', alignItems: 'flex-start', padding: '4px 14px', cursor: 'pointer' }}>
          <input type="checkbox" checked={trainingOptIn} onChange={e => setTrainingOptIn(e.target.checked)} style={{ marginTop: '2px', accentColor: PAL.accent }} />
          <span style={{ fontSize: '12.5px', color: '#7A7A72', lineHeight: 1.5 }}>
            {t('Optional: allow my anonymised answers to help improve this tool.',
               'ไม่บังคับ: อนุญาตให้นำคำตอบแบบไม่ระบุตัวตนไปช่วยพัฒนาเครื่องมือนี้')}
          </span>
        </label>
        {disclaimer}
      </StageBody>
    )
  }

  /* ================= STAGE 1 — Arrival & Regulation ================= */
  if (key === 'arrival') {
    if (arrivalPhase === 'grounding') {
      return shell(
        <StageBody t={t}
          title={t('Let’s steady first', 'ตั้งหลักก่อนสักนิด')}
          subtitle={t('Your activation is high. Before any images, a few slow breaths can help. No rush.',
                      'ระดับความตื่นตัวของคุณค่อนข้างสูง ก่อนจะดูภาพใด ๆ ลองหายใจช้า ๆ สักครู่ ไม่ต้องรีบ')}
          onNext={() => { setArrivalPhase('assess'); next() }}
          nextLabel={t('I feel a little steadier', 'รู้สึกนิ่งขึ้นนิดนึง')}
        >
          <div style={{ background: PAL.tint, border: `1px solid ${PAL.border}`, borderRadius: '14px', padding: '20px', display: 'flex', gap: '12px', alignItems: 'flex-start' }}>
            <Wind size={22} strokeWidth={1.8} color={PAL.accent} style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{ fontSize: '14px', color: '#5A5A52', lineHeight: 1.65, margin: 0 }}>
              {t('Breathe in for 4, out for 6. Let the out-breath be longer than the in-breath. Three gentle rounds, at your own pace.',
                 'หายใจเข้านับ 4 ออกนับ 6 ให้ลมหายใจออกยาวกว่าหายใจเข้า สัก 3 รอบเบา ๆ ตามจังหวะของคุณเอง')}
            </p>
          </div>
        </StageBody>
      )
    }
    const highRisk = () => {
      if (guard(bodyState)) return
      if (activationBefore >= 7) { setArrivalPhase('grounding'); return }
      next()
    }
    return shell(
      <StageBody t={t}
        title={t('How are you arriving?', 'ตอนนี้คุณเป็นอย่างไรบ้าง')}
        subtitle={t('Before any images, notice where you are right now. There are no wrong answers.',
                    'ก่อนจะดูภาพใด ๆ ลองสังเกตว่าตอนนี้คุณอยู่ตรงไหน ไม่มีคำตอบที่ผิด')}
        onNext={highRisk}
      >
        <div style={{ marginBottom: '22px' }}>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', marginBottom: '12px' }}>
            {t('How activated or stirred-up do you feel?', 'ตอนนี้รู้สึกตื่นตัวหรือปั่นป่วนแค่ไหน')}
          </label>
          <Slider value={activationBefore} onChange={setActBefore} labelLeft={t('calm', 'สงบ')} labelRight={t('very stirred', 'ปั่นป่วนมาก')} />
        </div>
        <Field
          label={t('What is happening in your body right now?', 'ตอนนี้ร่างกายคุณรู้สึกอย่างไรบ้าง')}
          value={bodyState} onChange={setBodyState}
          placeholder={t('e.g. tight chest, restless, tired…', 'เช่น แน่นหน้าอก กระสับกระส่าย เหนื่อย…')} rows={2}
        />
      </StageBody>
    )
  }

  /* ================= STAGE 2 — Intention ================= */
  if (key === 'intention') {
    return shell(
      <StageBody t={t}
        title={t('What would feel useful today?', 'วันนี้อยากได้อะไรจากการอ่านนี้')}
        subtitle={t('Pick what fits, or write your own. One focus is enough.', 'เลือกที่ตรงกับใจ หรือเขียนเอง โฟกัสเรื่องเดียวก็พอ')}
        onNext={() => { if (!guard(intention)) next() }}
      >
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '18px' }}>
          {INTENTION_TAGS.map((tag, i) => {
            const sel = intentionTag === i
            return (
              <button key={i} onClick={() => setIntentionTag(sel ? null : i)}
                style={{
                  fontSize: '13px', padding: '8px 14px', borderRadius: '999px', cursor: 'pointer', fontFamily: fontSans,
                  background: sel ? PAL.accent : '#fff', color: sel ? '#fff' : '#3A3A3A',
                  border: `1px solid ${sel ? PAL.accent : 'rgba(0,0,0,0.14)'}`,
                }}>
                {t(tag.en, tag.th)}
              </button>
            )
          })}
        </div>
        <Field label={t('Or in your own words (optional)', 'หรือเขียนด้วยคำของคุณเอง (ถ้าต้องการ)')}
          value={intention} onChange={setIntention} placeholder={t('What’s on your mind…', 'มีอะไรอยู่ในใจ…')} rows={2} />
      </StageBody>
    )
  }

  /* ================= STAGE 3 — Card Selection ================= */
  if (key === 'draw') {
    if (!drawn) {
      if (fan.length === 0) buildFan()
      return shell(
        <StageBody t={t}
          title={t('Choose the image with energy for you', 'เลือกภาพที่มีพลังดึงดูดคุณ')}
          subtitle={t('Not the “correct” card — the one your eye goes to. Tap to turn it over.',
                      'ไม่ใช่ไพ่ที่ “ถูกต้อง” แต่เป็นใบที่สายตาคุณมองไป แตะเพื่อพลิกดู')}
        >
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(64px, 1fr))', gap: '10px' }}>
            {fan.map((c) => (
              <button key={c.id} onClick={() => setDrawn(c)}
                style={{ aspectRatio: '2/3', borderRadius: '10px', border: `1px solid ${PAL.border}`, background: '#fff', cursor: 'pointer', padding: 0, overflow: 'hidden' }}>
                <svg viewBox="0 0 60 90" width="100%" height="100%">
                  <rect x="4" y="4" width="52" height="82" rx="6" fill="none" stroke={PAL.accent} strokeWidth="1.5" opacity="0.5" />
                  <circle cx="30" cy="45" r="12" fill="none" stroke={PAL.accent} strokeWidth="1" opacity="0.4" />
                  <circle cx="30" cy="45" r="3" fill={PAL.accent} opacity="0.5" />
                </svg>
              </button>
            ))}
          </div>
        </StageBody>
      )
    }
    return shell(
      <StageBody t={t}
        title={t('Your card', 'ไพ่ของคุณ')}
        subtitle={t('Sit with it a moment before we look together.', 'อยู่กับมันสักครู่ก่อนที่เราจะดูไปด้วยกัน')}
        onNext={next}
      >
        <div style={{ display: 'flex', justifyContent: 'center', margin: '4px 0 20px' }}>
          <CardMini card={drawn} lang={lang} size={190} />
        </div>
        {redraws < 1 && (
          <div style={{ textAlign: 'center' }}>
            <button onClick={() => { setDrawn(null); setRedraws(r => r + 1); buildFan() }}
              style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '12.5px', color: PAL.accent, background: 'none', border: 'none', cursor: 'pointer', fontFamily: fontSans }}>
              <Shuffle size={13} strokeWidth={1.8} />
              {t('Draw once more instead', 'จั่วใหม่อีกครั้ง')}
            </button>
          </div>
        )}
      </StageBody>
    )
  }

  /* ================= STAGE 4 — Observe Before Interpret ================= */
  if (key === 'observe') {
    return shell(
      <StageBody t={t}
        title={t('What do you notice?', 'คุณสังเกตเห็นอะไร')}
        subtitle={t('Start with what you actually see — before any story. Then feeling, then anything it brings up.',
                    'เริ่มจากสิ่งที่คุณเห็นจริง ๆ ก่อนจะมีเรื่องราว จากนั้นค่อยเป็นความรู้สึก แล้วก็สิ่งที่มันชวนให้นึกถึง')}
        onNext={() => { if (!guard(notice, feeling, association)) next() }}
      >
        <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '18px' }}>
          <CardMini card={drawn} lang={lang} size={130} />
        </div>
        <Field label={t('What do you notice first? (just what you see)', 'สิ่งแรกที่สังเกตเห็นคืออะไร (แค่สิ่งที่เห็น)')}
          value={notice} onChange={setNotice} placeholder={t('shapes, colours, a figure…', 'รูปทรง สี ภาพ…')} rows={2} />
        <Field label={t('What feeling shows up as you look?', 'เมื่อมองแล้วมีความรู้สึกอะไรเกิดขึ้น')}
          value={feeling} onChange={setFeeling} placeholder={t('name the feeling…', 'เรียกชื่อความรู้สึก…')} rows={2} />
        <Field label={t('Anything it reminds you of? (optional)', 'มันชวนให้นึกถึงอะไรไหม (ถ้ามี)')}
          value={association} onChange={setAssociation} placeholder={t('a situation, a person, a memory…', 'สถานการณ์ คน หรือความทรงจำ…')} rows={2} />
      </StageBody>
    )
  }

  /* ================= STAGE 5 — Meaning Co-creation ================= */
  if (key === 'meaning') {
    return shell(
      <StageBody t={t}
        title={t('Making meaning — together', 'สร้างความหมายไปด้วยกัน')}
        subtitle={t('Here are a few gentle possibilities. You decide what fits — your sense is the one that counts.',
                    'นี่คือความเป็นไปได้เบา ๆ ไม่กี่ข้อ คุณเป็นคนตัดสินว่าอะไรใช่ ความรู้สึกของคุณคือสิ่งที่สำคัญที่สุด')}
        onNext={next}
      >
        {notice && (
          <div style={{ background: PAL.tint, border: `1px solid ${PAL.border}`, borderRadius: '12px', padding: '12px 14px', marginBottom: '16px' }}>
            <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.1em', color: PAL.accent }}>{t('You said', 'คุณบอกว่า')}</span>
            <p style={{ fontSize: '13.5px', color: '#3A3A3A', margin: '4px 0 0', lineHeight: 1.55, fontStyle: 'italic' }}>“{notice}{feeling ? ` … ${feeling}` : ''}”</p>
          </div>
        )}
        <p style={{ fontSize: '12.5px', color: '#7A7A72', margin: '0 0 10px' }}>{t('Could this be touching on…', 'สิ่งนี้อาจกำลังพูดถึง…')}</p>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '18px' }}>
          {hypotheses.map((h, i) => (
            <div key={i} style={{ background: '#fff', border: `1px solid ${PAL.border}`, borderRadius: '12px', padding: '12px 14px' }}>
              <p style={{ fontSize: '13.5px', color: '#3A3A3A', margin: '0 0 8px', lineHeight: 1.5 }}>{h}</p>
              <div style={{ display: 'flex', gap: '6px' }}>
                {[['fits', t('fits', 'ใช่เลย')], ['partly', t('partly', 'บางส่วน')], ['no', t("doesn’t fit", 'ไม่ใช่')]].map(([v, lbl]) => {
                  const sel = hypoFit[i] === v
                  return (
                    <button key={v} onClick={() => setHypoFit(p => ({ ...p, [i]: sel ? undefined : v }))}
                      style={{ fontSize: '12px', padding: '5px 12px', borderRadius: '999px', cursor: 'pointer', fontFamily: fontSans,
                        background: sel ? PAL.accent : '#FAF7F2', color: sel ? '#fff' : '#7A7A72', border: `1px solid ${sel ? PAL.accent : 'rgba(0,0,0,0.1)'}` }}>
                      {lbl}
                    </button>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
        <Field label={t('In your own words, what does it mean for you?', 'ในความรู้สึกคุณ มันมีความหมายว่าอย่างไร')}
          value={userMeaning} onChange={setUserMeaning} placeholder={t('there is no wrong answer…', 'ไม่มีคำตอบที่ผิด…')} rows={3} />
      </StageBody>
    )
  }

  /* ================= STAGE 6 — Nervous-System Support ================= */
  if (key === 'support') {
    const cue = NS_CUES.find(c => c.id === nsCue)
    return shell(
      <StageBody t={t}
        title={t('How is your body now?', 'ตอนนี้ร่างกายคุณเป็นอย่างไร')}
        subtitle={t('If anything stirred up, here’s a small way to steady. Pick one, or continue.',
                    'ถ้ามีอะไรปั่นป่วนขึ้นมา นี่คือวิธีเล็ก ๆ ในการตั้งหลัก เลือกสักอย่าง หรือไปต่อก็ได้')}
        onNext={next}
      >
        <div style={{ marginBottom: '20px' }}>
          <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', marginBottom: '12px' }}>
            {t('Activation right now', 'ความตื่นตัวตอนนี้')}
          </label>
          <Slider value={activationMid} onChange={setActMid} labelLeft={t('calm', 'สงบ')} labelRight={t('very stirred', 'ปั่นป่วนมาก')} />
        </div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', marginBottom: cue ? '16px' : 0 }}>
          {NS_CUES.map(c => {
            const sel = nsCue === c.id
            return (
              <button key={c.id} onClick={() => setNsCue(sel ? null : c.id)}
                style={{ textAlign: 'left', padding: '12px 14px', borderRadius: '12px', cursor: 'pointer', fontFamily: fontSans, fontSize: '13.5px',
                  background: sel ? PAL.tint : '#fff', color: '#3A3A3A', border: `1px solid ${sel ? PAL.accent : 'rgba(0,0,0,0.12)'}` }}>
                {t(c.en, c.th)}
              </button>
            )
          })}
        </div>
        {cue && (
          <div style={{ background: PAL.tint, border: `1px solid ${PAL.border}`, borderRadius: '12px', padding: '14px 16px', display: 'flex', gap: '10px', alignItems: 'flex-start' }}>
            <Wind size={18} strokeWidth={1.8} color={PAL.accent} style={{ flexShrink: 0, marginTop: '2px' }} />
            <p style={{ fontSize: '13.5px', color: '#5A5A52', margin: 0, lineHeight: 1.6 }}>{t(cue.body_en, cue.body_th)}</p>
          </div>
        )}
      </StageBody>
    )
  }

  /* ================= STAGE 7 — Reframe & Choice ================= */
  if (key === 'reframe') {
    return shell(
      <StageBody t={t}
        title={t('What choice becomes visible?', 'ทางเลือกอะไรที่เริ่มมองเห็น')}
        subtitle={t('Not a prediction — just what feels a little clearer now.', 'ไม่ใช่คำทำนาย แค่สิ่งที่รู้สึกชัดขึ้นอีกนิดในตอนนี้')}
        onNext={() => { if (!guard(need, value, choicePoint)) next() }}
      >
        <Field label={t('What do you need right now?', 'ตอนนี้คุณต้องการอะไร')}
          value={need} onChange={setNeed} placeholder={t('rest, honesty, space, connection…', 'พักผ่อน ความจริงใจ พื้นที่ การเชื่อมโยง…')} rows={2} />
        <Field label={t('What matters to you here? (a value)', 'อะไรคือสิ่งที่สำคัญกับคุณตรงนี้ (คุณค่า)')}
          value={value} onChange={setValue} placeholder={t('e.g. kindness, courage, steadiness…', 'เช่น ความเมตตา ความกล้า ความมั่นคง…')} rows={2} />
        <Field label={t('Where is the choice point?', 'จุดที่ต้องเลือกอยู่ตรงไหน')}
          value={choicePoint} onChange={setChoicePoint} placeholder={t('the small fork in front of you…', 'ทางแยกเล็ก ๆ ที่อยู่ตรงหน้า…')} rows={2} />
      </StageBody>
    )
  }

  /* ================= STAGE 8 — Micro-action ================= */
  if (key === 'action') {
    const lowConf = confidence < 6
    return shell(
      <StageBody t={t}
        title={t('One small, respectful step', 'ก้าวเล็ก ๆ ที่อ่อนโยนต่อตัวเอง')}
        subtitle={t('Something you could do in 10 minutes or less. Smaller is better.', 'สิ่งที่ทำได้ใน 10 นาทีหรือน้อยกว่า ยิ่งเล็กยิ่งดี')}
        onNext={next}
      >
        {drawn?.micro_intervention && !microAction && (() => {
          const suggestion = lang === 'th' ? th(drawn.micro_intervention) : drawn.micro_intervention
          return (
            <button onClick={() => setMicroAction(suggestion)}
              style={{ display: 'block', width: '100%', textAlign: 'left', background: PAL.tint, border: `1px dashed ${PAL.border}`, borderRadius: '10px', padding: '10px 13px', marginBottom: '12px', cursor: 'pointer', fontFamily: fontSans, fontSize: '12.5px', color: '#7A5A48' }}>
              💡 {t('Try this from the card', 'ลองใช้ข้อเสนอจากไพ่')}: {suggestion}
            </button>
          )
        })()}
        <Field label={t('My small step', 'ก้าวเล็ก ๆ ของฉัน')}
          value={microAction} onChange={setMicroAction} placeholder={t('I will…', 'ฉันจะ…')} rows={2} />
        <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', margin: '4px 0 12px' }}>
          {t('How confident are you that you’ll do it?', 'มั่นใจแค่ไหนว่าจะได้ทำจริง')}
        </label>
        <Slider value={confidence} onChange={setConfidence} labelLeft={t('unsure', 'ไม่แน่ใจ')} labelRight={t('very sure', 'มั่นใจมาก')} />
        {lowConf && microAction && (
          <p style={{ fontSize: '12.5px', color: PAL.accent, margin: '12px 0 0', lineHeight: 1.5 }}>
            {t('That’s okay — could you shrink it so it feels almost easy?', 'ไม่เป็นไร ลองย่อให้เล็กลงจนรู้สึกว่าเกือบง่ายได้ไหม')}
          </p>
        )}
      </StageBody>
    )
  }

  /* ================= STAGE 9 — Integration ================= */
  if (key === 'integrate') {
    return shell(
      <StageBody t={t}
        title={t('What will you carry forward?', 'คุณจะเก็บอะไรกลับไป')}
        subtitle={t('And what can stay here, set down for now?', 'และอะไรที่วางไว้ตรงนี้ก่อนได้')}
        onNext={next}
      >
        <Field label={t('In a sentence, what stood out today?', 'สรุปสั้น ๆ วันนี้มีอะไรที่โดดเด่นในใจ')}
          value={summary} onChange={setSummary} placeholder={t('the thread that mattered…', 'ประเด็นที่สำคัญ…')} rows={2} />
        <Field label={t('An anchor word or phrase to keep', 'คำหรือวลีที่อยากยึดไว้')}
          value={anchor} onChange={setAnchor} placeholder={t('e.g. “it will pass”, “steady”…', 'เช่น “เดี๋ยวมันก็ผ่าน”, “มั่นคง”…')} rows={1} />
        <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', margin: '10px 0 12px' }}>
          {t('How activated do you feel now?', 'ตอนนี้รู้สึกตื่นตัวแค่ไหน')}
        </label>
        <Slider value={activationAfter} onChange={setActAfter} labelLeft={t('calm', 'สงบ')} labelRight={t('very stirred', 'ปั่นป่วนมาก')} />
        {activationAfter > activationBefore && (
          <p style={{ fontSize: '12px', color: PAL.accent, margin: '10px 0 0', lineHeight: 1.5 }}>
            {t('If you feel more stirred than when you started, it’s worth pausing with a few slow breaths before you go.',
               'ถ้ารู้สึกปั่นป่วนกว่าตอนเริ่ม ลองหยุดหายใจช้า ๆ สักครู่ก่อนไปต่อ')}
          </p>
        )}
      </StageBody>
    )
  }

  /* ================= STAGE 10 — Feedback + Save ================= */
  if (key === 'feedback') {
    if (saveState === 'saved') {
      return shell(
        <div className="gs-fade" style={{ maxWidth: '480px', margin: '0 auto', padding: '60px 24px', width: '100%', textAlign: 'center' }}>
          <div style={{ width: '52px', height: '52px', borderRadius: '50%', background: PAL.tint, display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 18px' }}>
            <Check size={26} strokeWidth={2} color={PAL.accent} />
          </div>
          <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: '28px', color: '#1B1B19', margin: '0 0 10px' }}>
            {t('Session saved.', 'บันทึกเซสชันแล้ว')}
          </h1>
          <p style={{ fontSize: '14px', color: '#7A7A72', lineHeight: 1.6, margin: '0 0 26px' }}>
            {anchor ? t(`Carry this with you: “${anchor}”.`, `เก็บสิ่งนี้ไว้กับคุณ: “${anchor}”`) : t('Be gentle with yourself today.', 'วันนี้ขอให้อ่อนโยนกับตัวเอง')}
          </p>
          <button onClick={onBack}
            style={{ padding: '12px 24px', borderRadius: '999px', border: 'none', background: PAL.accent, color: '#fff', fontSize: '14px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer' }}>
            {t('Done', 'เสร็จสิ้น')}
          </button>
        </div>
      )
    }
    return shell(
      <StageBody t={t}
        title={t('One last thing', 'อีกสิ่งสุดท้าย')}
        subtitle={t('This helps the tool serve you better. Then we’ll save your session.', 'สิ่งนี้ช่วยให้เครื่องมือดูแลคุณได้ดีขึ้น จากนั้นเราจะบันทึกเซสชันของคุณ')}
      >
        {[
          [t('Was this helpful?', 'สิ่งนี้ช่วยได้ไหม'), helpfulness, setHelpfulness],
          [t('Did it resonate?', 'มันตรงกับใจไหม'), resonance, setResonance],
          [t('Did you feel safe?', 'คุณรู้สึกปลอดภัยไหม'), safetyRating, setSafetyRating],
        ].map(([lbl, val, set], i) => (
          <div key={i} style={{ marginBottom: '18px' }}>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', marginBottom: '10px' }}>{lbl}</label>
            <Slider value={val} onChange={set} labelLeft={t('not really', 'ไม่เท่าไร')} labelRight={t('very much', 'มากเลย')} />
          </div>
        ))}
        <label style={{ display: 'flex', gap: '10px', alignItems: 'flex-start', padding: '10px 0', cursor: 'pointer', marginBottom: '8px' }}>
          <input type="checkbox" checked={consentToStore} onChange={e => setConsentToStore(e.target.checked)} style={{ marginTop: '2px', accentColor: PAL.accent }} />
          <span style={{ fontSize: '12.5px', color: '#7A7A72', lineHeight: 1.5 }}>
            {t('Save this full session to my history (otherwise only a short summary is kept).',
               'บันทึกเซสชันเต็มไว้ในประวัติของฉัน (ถ้าไม่เลือก จะเก็บเพียงสรุปสั้น ๆ)')}
          </span>
        </label>
        {saveState === 'error' && <p style={{ fontSize: '12px', color: '#C84B31', margin: '0 0 12px' }}>{t('Could not save.', 'บันทึกไม่สำเร็จ')} {saveErr}</p>}
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button onClick={finish} disabled={saveState === 'saving'}
            style={{ display: 'flex', alignItems: 'center', gap: '7px', padding: '12px 26px', borderRadius: '999px', border: 'none',
              background: PAL.accent, color: '#fff', fontSize: '14px', fontWeight: 500, fontFamily: fontSans,
              cursor: saveState === 'saving' ? 'default' : 'pointer', opacity: saveState === 'saving' ? 0.6 : 1, boxShadow: '0 6px 16px -8px rgba(0,0,0,0.3)' }}>
            <Check size={15} strokeWidth={2} />
            {saveState === 'saving' ? t('Saving…', 'กำลังบันทึก…') : t('Finish & save', 'จบและบันทึก')}
          </button>
        </div>
      </StageBody>
    )
  }

  return shell(<div style={{ padding: '60px', textAlign: 'center' }} />)
}
