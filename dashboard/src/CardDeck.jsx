import { useState, useEffect, useMemo, useCallback } from 'react'
import { ArrowLeft, ArrowRight, Shuffle, RotateCcw, Languages, BookMarked, Trash2, Check } from 'lucide-react'

/* ------------------------------------------------------------------ */
/*  Fonts + design tokens (shared with the rest of the app)             */
/* ------------------------------------------------------------------ */

const fontSans  = "'Geist', ui-sans-serif, system-ui, sans-serif"
const fontSerif = "'Instrument Serif', ui-serif, Georgia, serif"

// From cards.json style_guide.palette
const PAL = {
  ink:    '#3A3A3A',
  warm:   '#E8A87C',
  cool:   '#7FB5B5',
  paper:  '#FAF7F2',
  bg:     '#FAFAF6',
  muted:  '#9A9A95',
}

/* Per-deck presentation + therapeutic framing (EN/TH) */
const DECKS = {
  tarot: {
    emoji: '🌙',
    accent: '#6B5B95',
    tint: '#F3F1F8',
    border: '#D6CFE8',
    name_en: 'Tarot',
    name_th: 'ทาโรต์',
    use_en: 'Archetypal story-images for looking at your situation from a wider view. Read as mirrors for reflection — not as fixed predictions.',
    use_th: 'ภาพเชิงสัญลักษณ์สำหรับมองสถานการณ์ของคุณจากมุมที่กว้างขึ้น ใช้เป็นกระจกสะท้อนใจ ไม่ใช่คำทำนายที่ตายตัว',
  },
  neuro: {
    emoji: '🌊',
    accent: '#C77B54',
    tint: '#FBF1EA',
    border: '#F0D6C4',
    name_en: 'Neuro / Mind',
    name_th: 'นิวโร / ใจ',
    use_en: 'Projective feeling-images. There is no correct meaning — your own words lead the reading. Good for naming emotion, noticing inner parts, and perception vs. interpretation.',
    use_th: 'ภาพความรู้สึกแบบเปิดกว้าง ไม่มีความหมายที่ถูกต้องตายตัว คำพูดของคุณเองคือสิ่งที่นำทาง เหมาะกับการเรียกชื่ออารมณ์ สังเกตส่วนต่าง ๆ ในใจ และแยกการรับรู้ออกจากการตีความ',
  },
  nature: {
    emoji: '🍃',
    accent: '#4F8C7B',
    tint: '#EFF6F3',
    border: '#C8E2D8',
    name_en: 'Nature',
    name_th: 'ธรรมชาติ',
    use_en: 'Grounding nature images to slow down, breathe, and reconnect with your body and the present moment.',
    use_th: 'ภาพธรรมชาติที่ช่วยให้ช้าลง หายใจ และกลับมาเชื่อมโยงกับร่างกายและปัจจุบันขณะ',
  },
}

/* Spreads available per deck, grounded in how each deck is used in practice */
const SPREADS = {
  tarot: [
    {
      id: 'one', count: 1, projective: false,
      name_en: 'Card of the Moment', name_th: 'ไพ่ประจำช่วงเวลานี้',
      desc_en: 'A single card to reflect on right now.',
      desc_th: 'ไพ่ใบเดียวสำหรับทบทวนช่วงเวลานี้',
      positions: [{ en: 'This moment', th: 'ช่วงเวลานี้' }],
    },
    {
      id: 'three', count: 3, projective: false,
      name_en: 'Past · Present · Future', name_th: 'อดีต · ปัจจุบัน · อนาคต',
      desc_en: 'Three cards tracing where you have been, where you are, and what may be forming.',
      desc_th: 'ไพ่สามใบเชื่อมโยงจุดที่ผ่านมา จุดที่อยู่ และสิ่งที่กำลังก่อตัว',
      positions: [
        { en: 'Past', th: 'อดีต' },
        { en: 'Present', th: 'ปัจจุบัน' },
        { en: 'Future', th: 'อนาคต' },
      ],
    },
  ],
  neuro: [
    {
      id: 'one', count: 1, projective: true,
      name_en: 'What Do You See?', name_th: 'คุณเห็นอะไร',
      desc_en: 'One open image. You say what you see first — your words are the reading.',
      desc_th: 'ภาพเปิดหนึ่งใบ คุณเป็นคนบอกว่าเห็นอะไรก่อน คำพูดของคุณคือการอ่าน',
      positions: [{ en: 'Open image', th: 'ภาพเปิด' }],
    },
    {
      id: 'three', count: 3, projective: true,
      name_en: 'Feeling · Block · Resource', name_th: 'ความรู้สึก · สิ่งที่ติดขัด · แรงที่มี',
      desc_en: 'Three images: a feeling present now, what feels stuck, and a resource that helps.',
      desc_th: 'ภาพสามใบ: ความรู้สึกที่มีตอนนี้ สิ่งที่รู้สึกติดขัด และแรงสนับสนุนที่ช่วยได้',
      positions: [
        { en: 'Feeling', th: 'ความรู้สึก' },
        { en: 'Block', th: 'สิ่งที่ติดขัด' },
        { en: 'Resource', th: 'แรงที่มี' },
      ],
    },
  ],
  nature: [
    {
      id: 'one', count: 1, projective: true,
      name_en: 'Grounding Image', name_th: 'ภาพช่วยตั้งหลัก',
      desc_en: 'One nature image to breathe with and settle.',
      desc_th: 'ภาพธรรมชาติหนึ่งใบสำหรับหายใจไปด้วยและตั้งหลัก',
      positions: [{ en: 'Ground', th: 'ตั้งหลัก' }],
    },
    {
      id: 'three', count: 3, projective: true,
      name_en: 'Notice · Body · Ground', name_th: 'สังเกต · ร่างกาย · ตั้งหลัก',
      desc_en: 'Three gentle images to notice, feel the body, and steady yourself.',
      desc_th: 'ภาพอ่อนโยนสามใบ ชวนสังเกต รับรู้ร่างกาย และตั้งหลักให้มั่นคง',
      positions: [
        { en: 'Notice', th: 'สังเกต' },
        { en: 'Body', th: 'ร่างกาย' },
        { en: 'Ground', th: 'ตั้งหลัก' },
      ],
    },
  ],
}

const FAN_SIZE = 13  // face-down cards presented for picking

/* ------------------------------------------------------------------ */
/*  Small utilities                                                     */
/* ------------------------------------------------------------------ */

function shuffle(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

// deterministic hash from a string → seeds the procedural art
function hashStr(s) {
  let h = 2166136261
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return (h >>> 0)
}

/* ------------------------------------------------------------------ */
/*  Procedural SVG card art (matches style guide: flat, 2–3 colors)     */
/*  cards.json has no image field + only a few PNGs exist, so we draw    */
/*  minimal deck-appropriate art seeded by the card id.                 */
/* ------------------------------------------------------------------ */

function CardArt({ card }) {
  const h = hashStr(card.id)
  const r1 = (h & 0xff) / 255
  const r2 = ((h >> 8) & 0xff) / 255
  const r3 = ((h >> 16) & 0xff) / 255

  if (card.deck === 'tarot') {
    const rays = 8 + Math.floor(r1 * 6)
    const cx = 60, cy = 62, rad = 26
    const spokes = Array.from({ length: rays }, (_, i) => {
      const ang = (i / rays) * Math.PI * 2
      const x1 = cx + Math.cos(ang) * (rad + 6)
      const y1 = cy + Math.sin(ang) * (rad + 6)
      const x2 = cx + Math.cos(ang) * (rad + 14)
      const y2 = cy + Math.sin(ang) * (rad + 14)
      return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={PAL.warm} strokeWidth="2" strokeLinecap="round" />
    })
    return (
      <svg viewBox="0 0 120 130" width="100%" height="100%">
        {spokes}
        <circle cx={cx} cy={cy} r={rad} fill="none" stroke={PAL.ink} strokeWidth="2.2" />
        <path d={`M ${cx - 12} ${cy + 4} q 12 ${8 + r2 * 6} 24 0`} fill="none" stroke={PAL.ink} strokeWidth="2" strokeLinecap="round" />
        <circle cx={cx - 8} cy={cy - 4} r="1.8" fill={PAL.ink} />
        <circle cx={cx + 8} cy={cy - 4} r="1.8" fill={PAL.ink} />
        <path d="M 40 108 L 60 96 L 80 108" fill="none" stroke={PAL.cool} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
      </svg>
    )
  }

  if (card.deck === 'neuro') {
    // organic feeling-blob + scattered dots
    const pts = 6
    const path = Array.from({ length: pts }, (_, i) => {
      const ang = (i / pts) * Math.PI * 2
      const rr = 22 + Math.sin(ang * 2 + r1 * 6) * (7 + r2 * 6)
      const x = 60 + Math.cos(ang) * rr
      const y = 60 + Math.sin(ang) * rr * 0.9
      return `${i === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`
    }).join(' ') + ' Z'
    const dots = Array.from({ length: 5 }, (_, i) => {
      const x = 24 + ((h >> (i * 3)) & 0x3f)
      const y = 30 + ((h >> (i * 4)) & 0x3f)
      return <circle key={i} cx={x % 96 + 12} cy={y % 70 + 22} r={1.6 + (i % 2)} fill={i % 2 ? PAL.warm : PAL.cool} />
    })
    return (
      <svg viewBox="0 0 120 130" width="100%" height="100%">
        <path d={path} fill="none" stroke={r3 > 0.5 ? PAL.warm : PAL.cool} strokeWidth="2.4" strokeLinejoin="round" />
        <path d={path} fill={PAL.ink} opacity="0.05" />
        {dots}
      </svg>
    )
  }

  // nature — layered horizon / hills / water with a small stone or plant
  const wave = (y, amp) =>
    `M 12 ${y} q 18 ${-amp} 36 0 t 36 0 t 36 0`
  return (
    <svg viewBox="0 0 120 130" width="100%" height="100%">
      <circle cx={r1 > 0.5 ? 86 : 34} cy="34" r="12" fill="none" stroke={PAL.warm} strokeWidth="2" />
      <path d={wave(70, 6 + r2 * 4)} fill="none" stroke={PAL.cool} strokeWidth="2.2" strokeLinecap="round" />
      <path d={wave(84, 5 + r3 * 4)} fill="none" stroke={PAL.cool} strokeWidth="1.8" strokeLinecap="round" opacity="0.7" />
      {r3 > 0.4 ? (
        <ellipse cx="60" cy="104" rx="12" ry="6" fill="none" stroke={PAL.ink} strokeWidth="2" />
      ) : (
        <g stroke={PAL.ink} strokeWidth="2" strokeLinecap="round" fill="none">
          <line x1="60" y1="108" x2="60" y2="92" />
          <path d="M 60 98 q -8 -4 -12 -10" />
          <path d="M 60 100 q 8 -4 12 -10" />
        </g>
      )}
    </svg>
  )
}

/* Card face image — uses the real artwork when present, and falls back to
   procedural SVG for cards whose image has not been delivered yet. */
function CardImage({ card }) {
  const [err, setErr] = useState(false)
  if (card.image && !err) {
    return (
      <img
        src={'/' + card.image}
        alt=""
        onError={() => setErr(true)}
        style={{ width: '100%', height: '100%', objectFit: 'cover', display: 'block' }}
      />
    )
  }
  return (
    <div style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '8px 8px 0' }}>
      <CardArt card={card} />
    </div>
  )
}

/* Face-down card back — simple patterned motif per deck accent */
function CardBack({ accent }) {
  return (
    <svg viewBox="0 0 120 180" width="100%" height="100%" preserveAspectRatio="xMidYMid slice">
      <rect x="8" y="8" width="104" height="164" rx="10" fill="none" stroke={accent} strokeWidth="2" opacity="0.55" />
      <rect x="16" y="16" width="88" height="148" rx="7" fill="none" stroke={accent} strokeWidth="1" opacity="0.35" />
      {Array.from({ length: 6 }, (_, i) => (
        <circle key={i} cx="60" cy="90" r={12 + i * 11} fill="none" stroke={accent} strokeWidth="1" opacity={0.28 - i * 0.03} />
      ))}
      <circle cx="60" cy="90" r="5" fill={accent} opacity="0.5" />
    </svg>
  )
}

/* ------------------------------------------------------------------ */
/*  Presentational card component (flips between back and face)         */
/* ------------------------------------------------------------------ */

function DeckCard({ card, name, accent, faceUp, onClick, selected, disabled, label, style }) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        perspective: '900px',
        background: 'none',
        border: 'none',
        padding: 0,
        cursor: disabled ? 'default' : 'pointer',
        outline: 'none',
        ...style,
      }}
    >
      <div
        style={{
          position: 'relative',
          width: '100%',
          aspectRatio: '2 / 3',
          transformStyle: 'preserve-3d',
          transition: 'transform 0.6s cubic-bezier(0.22,1,0.36,1), box-shadow 0.2s',
          transform: `${faceUp ? 'rotateY(180deg)' : 'rotateY(0deg)'}${selected ? ' translateY(-10px)' : ''}`,
          boxShadow: selected
            ? `0 12px 28px -10px ${accent}88`
            : '0 4px 14px -8px rgba(0,0,0,0.25)',
          borderRadius: '12px',
        }}
      >
        {/* Back */}
        <div
          style={{
            position: 'absolute', inset: 0, backfaceVisibility: 'hidden',
            borderRadius: '12px', overflow: 'hidden',
            background: '#fff',
            border: selected ? `2px solid ${accent}` : '1px solid rgba(0,0,0,0.08)',
          }}
        >
          <CardBack accent={accent} />
        </div>

        {/* Face */}
        <div
          style={{
            position: 'absolute', inset: 0, backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)',
            borderRadius: '12px', overflow: 'hidden',
            background: PAL.paper,
            border: `1px solid ${accent}44`,
            display: 'flex', flexDirection: 'column',
          }}
        >
          <div style={{ flex: '1 1 0', minHeight: 0, overflow: 'hidden' }}>
            {card && <CardImage card={card} />}
          </div>
          <div style={{ padding: '4px 6px 8px', textAlign: 'center' }}>
            {label && (
              <div style={{ fontSize: '8px', textTransform: 'uppercase', letterSpacing: '0.12em', color: accent, marginBottom: '1px' }}>
                {label}
              </div>
            )}
            <div style={{ fontFamily: fontSerif, fontStyle: 'italic', fontSize: '12px', color: PAL.ink, lineHeight: 1.15 }}>
              {name ?? card?.name}
            </div>
          </div>
        </div>
      </div>
    </button>
  )
}

/* ------------------------------------------------------------------ */
/*  Main component                                                      */
/* ------------------------------------------------------------------ */

export default function CardDeck({ onBack, token }) {
  const [lang, setLang]       = useState('en')          // 'en' | 'th'
  const [data, setData]       = useState(null)
  const [loadErr, setLoadErr] = useState('')

  // flow: 'deck' → 'spread' → 'draw' → 'reveal'; plus 'history' / 'historyDetail'
  const [step, setStep]       = useState('deck')
  const [deckId, setDeckId]   = useState(null)
  const [spread, setSpread]   = useState(null)

  const [shuffling, setShuffling] = useState(false)
  const [fan, setFan]         = useState([])            // face-down cards to pick from
  const [picked, setPicked]   = useState([])            // indices into `fan`
  const [revealed, setRevealed] = useState(false)

  const [reflection, setReflection] = useState('')
  const [intention, setIntention]   = useState('')
  const [showTheme, setShowTheme]   = useState(false)

  // saving readings + history (Stage 3)
  const [saveState, setSaveState]   = useState('idle')  // idle | saving | saved | error
  const [saveErr, setSaveErr]       = useState('')
  const [history, setHistory]       = useState(null)    // null = not loaded yet
  const [historyErr, setHistoryErr] = useState('')
  const [viewing, setViewing]       = useState(null)    // a reading object for detail view

  const t = useCallback((en, th) => (lang === 'th' ? th : en), [lang])

  /* ---- readings API (uses the bearer token from App) ---- */
  const api = useCallback(async (path, opts = {}) => {
    const headers = { 'Content-Type': 'application/json' }
    if (token) headers['Authorization'] = `Bearer ${token}`
    const res = await fetch('/api/cards' + path, { ...opts, headers })
    if (res.status === 204) return null
    const body = await res.json().catch(() => null)
    if (!res.ok) throw new Error(body?.detail || `Request failed (${res.status})`)
    return body
  }, [token])

  /* Load fonts (idempotent) + card data */
  useEffect(() => {
    const id = 'auth-fonts'
    if (!document.getElementById(id)) {
      const link = document.createElement('link')
      link.id = id
      link.rel = 'stylesheet'
      link.href = 'https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap'
      document.head.appendChild(link)
    }
  }, [])

  useEffect(() => {
    fetch('/cards.json')
      .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json() })
      .then(setData)
      .catch(e => setLoadErr(e.message))
  }, [])

  const deckCards = useMemo(() => {
    if (!data || !deckId) return []
    return data.cards
      .filter(c => c.deck === deckId)
      .map(c => ({ ...c, name: lang === 'th' ? c.name_th : c.name_en }))
  }, [data, deckId, lang])

  const meta = deckId ? DECKS[deckId] : null

  /* ---- flow actions ---- */

  const chooseDeck = (id) => {
    setDeckId(id)
    setSpread(null)
    setStep('spread')
  }

  const chooseSpread = (sp) => {
    setSpread(sp)
    setPicked([])
    setRevealed(false)
    setReflection('')
    setIntention('')
    setShowTheme(false)
    setSaveState('idle')
    setSaveErr('')
    // build a fresh shuffled fan
    const drawn = shuffle(deckCards).slice(0, Math.min(FAN_SIZE, deckCards.length))
    setFan(drawn)
    setStep('draw')
    setShuffling(true)
    setTimeout(() => setShuffling(false), 1100)
  }

  const reshuffle = () => {
    setPicked([])
    setRevealed(false)
    const drawn = shuffle(deckCards).slice(0, Math.min(FAN_SIZE, deckCards.length))
    setFan(drawn)
    setShuffling(true)
    setTimeout(() => setShuffling(false), 1100)
  }

  const togglePick = (idx) => {
    if (revealed || shuffling) return
    setPicked(prev => {
      if (prev.includes(idx)) return prev.filter(i => i !== idx)
      if (prev.length >= spread.count) return prev   // full
      return [...prev, idx]
    })
  }

  const reveal = () => {
    setStep('reveal')
    setRevealed(false)
    // mount face-down, then flip on the next tick so the animation plays
    setTimeout(() => setRevealed(true), 80)
  }

  const restart = () => {
    setStep('deck')
    setDeckId(null)
    setSpread(null)
    setFan([])
    setPicked([])
    setRevealed(false)
    setReflection('')
    setIntention('')
    setShowTheme(false)
    setSaveState('idle')
    setSaveErr('')
  }

  const pickedCards = picked.map(i => fan[i])

  /* ---- saving readings + history ---- */
  const saveReading = async () => {
    setSaveState('saving')
    setSaveErr('')
    try {
      await api('/readings', {
        method: 'POST',
        body: JSON.stringify({
          deck: deckId,
          spread_id: spread.id,
          spread_name: spread.name_en,
          cards: pickedCards.map((c, i) => ({
            card_id: c.id,
            position: spread.positions[i]?.en || null,
          })),
          reflection: reflection.trim() || null,
          intention: intention.trim() || null,
          lang,
        }),
      })
      setSaveState('saved')
      setHistory(null)   // force a refresh next time History opens
    } catch (e) {
      setSaveState('error')
      setSaveErr(e.message)
    }
  }

  const openHistory = async () => {
    setStep('history')
    setViewing(null)
    setHistoryErr('')
    try {
      const rows = await api('/readings')
      setHistory(rows)
    } catch (e) {
      setHistoryErr(e.message)
      setHistory([])
    }
  }

  const deleteReading = async (id) => {
    try {
      await api(`/readings/${id}`, { method: 'DELETE' })
      setHistory(prev => (prev || []).filter(r => r.id !== id))
      setViewing(v => (v && v.id === id ? null : v))
      if (viewing && viewing.id === id) setStep('history')
    } catch (e) {
      setHistoryErr(e.message)
    }
  }

  // resolve a saved card_id back to its display card (name + art)
  const cardById = useCallback((id) => data?.cards.find(c => c.id === id) || null, [data])

  /* ---- shared header ---- */
  const Header = (
    <div style={{
      display: 'flex', alignItems: 'center', justifyContent: 'space-between',
      padding: '16px 20px', borderBottom: '0.5px solid rgba(0,0,0,0.07)', background: '#fff',
      position: 'sticky', top: 0, zIndex: 10,
    }}>
      <button
        onClick={() => {
          if (step === 'deck') onBack()
          else if (step === 'spread') setStep('deck')
          else if (step === 'draw') setStep('spread')
          else if (step === 'history') setStep('deck')
          else if (step === 'historyDetail') setStep('history')
          else setStep('draw')
        }}
        style={{
          display: 'flex', alignItems: 'center', gap: '6px', fontSize: '13px',
          color: '#7A7A72', background: 'none', border: 'none', cursor: 'pointer',
          fontFamily: fontSans, padding: '6px 8px', borderRadius: '8px',
        }}
      >
        <ArrowLeft size={15} strokeWidth={1.8} />
        {step === 'deck' ? t('Home', 'หน้าหลัก') : t('Back', 'ย้อนกลับ')}
      </button>

      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {token && step !== 'history' && step !== 'historyDetail' && (
          <button
            onClick={openHistory}
            title={t('Saved readings', 'บันทึกที่บันทึกไว้')}
            style={{
              display: 'flex', alignItems: 'center', gap: '5px',
              fontSize: '12px', fontWeight: 500, color: '#1B1B19',
              background: '#F0EFE8', border: 'none', cursor: 'pointer',
              fontFamily: fontSans, padding: '6px 10px', borderRadius: '999px',
            }}
          >
            <BookMarked size={13} strokeWidth={1.8} />
            {t('Saved', 'บันทึก')}
          </button>
        )}
        <button
          onClick={() => setLang(lang === 'en' ? 'th' : 'en')}
          style={{
            display: 'flex', alignItems: 'center', gap: '5px',
            fontSize: '12px', fontWeight: 500, color: '#1B1B19',
            background: '#F0EFE8', border: 'none', cursor: 'pointer',
            fontFamily: fontSans, padding: '6px 10px', borderRadius: '999px',
          }}
        >
          <Languages size={13} strokeWidth={1.8} />
          {lang === 'en' ? 'ไทย' : 'EN'}
        </button>
      </div>
    </div>
  )

  const fmtDate = (iso) => {
    if (!iso) return ''
    try {
      return new Date(iso).toLocaleString(lang === 'th' ? 'th-TH' : 'en-US',
        { dateStyle: 'medium', timeStyle: 'short' })
    } catch { return iso }
  }

  const disclaimer = (
    <p style={{ fontSize: '11px', color: PAL.muted, textAlign: 'center', margin: '0 auto', maxWidth: '520px', lineHeight: 1.5 }}>
      {data ? t(data.disclaimer_en, data.disclaimer_th)
            : t('For self-reflection only — not medical or psychological treatment.',
                'เพื่อการทบทวนตนเองเท่านั้น')}
    </p>
  )

  const shell = (children) => (
    <div style={{ minHeight: '100vh', background: PAL.bg, fontFamily: fontSans, display: 'flex', flexDirection: 'column' }}>
      <style>{`
        @keyframes cd-fade { from { opacity:0; transform:translateY(8px) } to { opacity:1; transform:translateY(0) } }
        @keyframes cd-shuffle { 0%{transform:translateX(0) rotate(0)} 25%{transform:translateX(-8px) rotate(-4deg)} 50%{transform:translateX(6px) rotate(3deg)} 75%{transform:translateX(-4px) rotate(-2deg)} 100%{transform:translateX(0) rotate(0)} }
        .cd-fade { animation: cd-fade 0.4s cubic-bezier(0.22,1,0.36,1) both; }
      `}</style>
      {Header}
      <div style={{ flex: 1 }}>{children}</div>
    </div>
  )

  /* ---- loading / error ---- */
  if (loadErr) {
    return shell(
      <div style={{ padding: '60px 24px', textAlign: 'center' }}>
        <p style={{ color: '#C84B31', fontSize: '14px' }}>
          {t('Could not load the card data.', 'ไม่สามารถโหลดข้อมูลไพ่ได้')} ({loadErr})
        </p>
      </div>
    )
  }
  if (!data) {
    return shell(
      <div style={{ padding: '80px 24px', textAlign: 'center' }}>
        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#6B5B95', opacity: 0.6, margin: '0 auto' }} />
      </div>
    )
  }

  /* ============================================================= */
  /*  STEP 1 — choose a deck                                         */
  /* ============================================================= */
  if (step === 'deck') {
    return shell(
      <div className="cd-fade" style={{ maxWidth: '640px', margin: '0 auto', padding: '40px 24px 56px', width: '100%' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: PAL.muted, marginBottom: '8px' }}>
          {t('Step 1 · Choose a deck', 'ขั้นที่ 1 · เลือกสำรับ')}
        </p>
        <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: 'clamp(26px,5vw,36px)', color: '#1B1B19', margin: '0 0 28px', lineHeight: 1.2 }}>
          {t('Which cards feel right today?', 'วันนี้ไพ่แบบไหนที่ใช่สำหรับคุณ')}
        </h1>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '32px' }}>
          {Object.entries(DECKS).map(([id, d]) => {
            const count = data.cards.filter(c => c.deck === id).length
            return (
              <button
                key={id}
                onClick={() => chooseDeck(id)}
                style={{
                  display: 'flex', alignItems: 'center', gap: '18px', width: '100%',
                  background: '#fff', border: `1px solid ${d.border}`, borderRadius: '16px',
                  padding: '20px 22px', cursor: 'pointer', textAlign: 'left', fontFamily: fontSans,
                  boxShadow: '0 1px 3px rgba(0,0,0,0.04)', transition: 'box-shadow 0.2s, transform 0.15s',
                }}
                onMouseEnter={e => { e.currentTarget.style.boxShadow = '0 8px 26px -10px rgba(0,0,0,0.14)'; e.currentTarget.style.transform = 'translateY(-1px)' }}
                onMouseLeave={e => { e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.04)'; e.currentTarget.style.transform = 'translateY(0)' }}
              >
                <div style={{ width: '50px', height: '50px', borderRadius: '14px', background: d.tint, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px', flexShrink: 0 }}>
                  {d.emoji}
                </div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '3px' }}>
                    <span style={{ fontSize: '16px', fontWeight: 500, color: '#1B1B19' }}>{t(d.name_en, d.name_th)}</span>
                    <span style={{ fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.12em', color: d.accent, background: d.tint, padding: '2px 7px', borderRadius: '6px', fontWeight: 500 }}>
                      {count} {t('cards', 'ใบ')}
                    </span>
                  </div>
                  <p style={{ fontSize: '13px', color: '#7A7A72', margin: 0, lineHeight: 1.5 }}>{t(d.use_en, d.use_th)}</p>
                </div>
                <ArrowRight size={16} strokeWidth={1.8} color="#C8C6BC" style={{ flexShrink: 0 }} />
              </button>
            )
          })}
        </div>
        {disclaimer}
      </div>
    )
  }

  /* ============================================================= */
  /*  STEP 2 — choose a spread                                       */
  /* ============================================================= */
  if (step === 'spread') {
    return shell(
      <div className="cd-fade" style={{ maxWidth: '640px', margin: '0 auto', padding: '40px 24px 56px', width: '100%' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: meta.accent, marginBottom: '8px' }}>
          {t('Step 2 · Choose a spread', 'ขั้นที่ 2 · เลือกรูปแบบการวางไพ่')} · {t(meta.name_en, meta.name_th)}
        </p>
        <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: 'clamp(26px,5vw,36px)', color: '#1B1B19', margin: '0 0 8px', lineHeight: 1.2 }}>
          {t('How would you like to read?', 'คุณอยากอ่านไพ่แบบไหน')}
        </h1>

        {deckId === 'neuro' && (
          <div style={{ background: meta.tint, border: `1px solid ${meta.border}`, borderRadius: '12px', padding: '12px 14px', margin: '16px 0 24px', fontSize: '12.5px', color: '#6B4A38', lineHeight: 1.55 }}>
            {t('These images have no fixed meaning. You will be asked what you see first — the cards never recover memories or decide whether something happened.',
               'ภาพเหล่านี้ไม่มีความหมายตายตัว คุณจะได้บอกก่อนว่าเห็นอะไร — ไพ่ไม่ได้ใช้เพื่อรื้อฟื้นความทรงจำหรือชี้ว่าเหตุการณ์เกิดขึ้นจริงหรือไม่')}
          </div>
        )}

        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: deckId === 'neuro' ? 0 : '24px', marginBottom: '32px' }}>
          {SPREADS[deckId].map(sp => (
            <button
              key={sp.id}
              onClick={() => chooseSpread(sp)}
              style={{
                display: 'flex', alignItems: 'center', gap: '16px', width: '100%',
                background: '#fff', border: `1px solid ${meta.border}`, borderRadius: '14px',
                padding: '18px 20px', cursor: 'pointer', textAlign: 'left', fontFamily: fontSans,
                boxShadow: '0 1px 3px rgba(0,0,0,0.04)', transition: 'box-shadow 0.2s, transform 0.15s',
              }}
              onMouseEnter={e => { e.currentTarget.style.boxShadow = '0 8px 26px -10px rgba(0,0,0,0.14)'; e.currentTarget.style.transform = 'translateY(-1px)' }}
              onMouseLeave={e => { e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.04)'; e.currentTarget.style.transform = 'translateY(0)' }}
            >
              <div style={{ display: 'flex', gap: '3px', flexShrink: 0 }}>
                {Array.from({ length: sp.count }).map((_, i) => (
                  <div key={i} style={{ width: '18px', height: '27px', borderRadius: '4px', background: meta.tint, border: `1.5px solid ${meta.accent}` }} />
                ))}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: '15px', fontWeight: 500, color: '#1B1B19', marginBottom: '2px' }}>
                  {t(sp.name_en, sp.name_th)}
                  {sp.projective && (
                    <span style={{ fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.1em', color: meta.accent, marginLeft: '8px' }}>
                      {t('projective', 'เปิดกว้าง')}
                    </span>
                  )}
                </div>
                <p style={{ fontSize: '12.5px', color: '#7A7A72', margin: 0, lineHeight: 1.5 }}>{t(sp.desc_en, sp.desc_th)}</p>
              </div>
              <ArrowRight size={16} strokeWidth={1.8} color="#C8C6BC" style={{ flexShrink: 0 }} />
            </button>
          ))}
        </div>
        {disclaimer}
      </div>
    )
  }

  /* ============================================================= */
  /*  STEP 3 — shuffle + pick face-down cards                       */
  /* ============================================================= */
  if (step === 'draw') {
    const need = spread.count
    const done = picked.length === need

    return shell(
      <div className="cd-fade" style={{ maxWidth: '820px', margin: '0 auto', padding: '32px 20px 56px', width: '100%' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: meta.accent, marginBottom: '6px', textAlign: 'center' }}>
          {t(meta.name_en, meta.name_th)} · {t(spread.name_en, spread.name_th)}
        </p>
        <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: 'clamp(22px,4.5vw,30px)', color: '#1B1B19', margin: '0 0 4px', lineHeight: 1.2, textAlign: 'center' }}>
          {shuffling
            ? t('Shuffling…', 'กำลังสับไพ่…')
            : done
              ? t('Ready when you are.', 'พร้อมแล้วเมื่อคุณพร้อม')
              : t(`Pick ${need} ${need > 1 ? 'cards' : 'card'}`, `เลือกไพ่ ${need} ใบ`)}
        </h1>
        <p style={{ fontSize: '13px', color: '#7A7A72', textAlign: 'center', margin: '0 0 22px' }}>
          {shuffling
            ? t('Take a slow breath.', 'หายใจเข้าช้า ๆ')
            : t(`${picked.length} of ${need} chosen · tap a card to ${picked.length ? 'add or remove' : 'choose'}`,
                `เลือกแล้ว ${picked.length} จาก ${need} ใบ · แตะไพ่เพื่อเลือกหรือยกเลิก`)}
        </p>

        {/* Fan of face-down cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(62px, 1fr))',
          gap: '10px',
          maxWidth: '760px', margin: '0 auto 28px',
        }}>
          {fan.map((card, i) => {
            const sel = picked.includes(i)
            const order = picked.indexOf(i)
            return (
              <div key={card.id} style={{ position: 'relative', animation: shuffling ? `cd-shuffle 0.5s ${i * 0.02}s ease` : 'none' }}>
                <DeckCard
                  card={card}
                  name={lang === 'th' ? card.name_th : card.name_en}
                  accent={meta.accent}
                  faceUp={false}
                  selected={sel}
                  disabled={shuffling}
                  onClick={() => togglePick(i)}
                />
                {sel && (
                  <div style={{
                    position: 'absolute', top: '-6px', right: '-6px',
                    width: '20px', height: '20px', borderRadius: '50%',
                    background: meta.accent, color: '#fff', fontSize: '11px', fontWeight: 600,
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
                  }}>
                    {order + 1}
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Actions */}
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <button
            onClick={reshuffle}
            disabled={shuffling}
            style={{
              display: 'flex', alignItems: 'center', gap: '7px', padding: '11px 18px',
              borderRadius: '999px', border: '1px solid rgba(0,0,0,0.12)', background: '#fff',
              color: '#1B1B19', fontSize: '13px', fontWeight: 500, fontFamily: fontSans,
              cursor: shuffling ? 'default' : 'pointer', opacity: shuffling ? 0.5 : 1,
            }}
          >
            <Shuffle size={14} strokeWidth={1.8} />
            {t('Shuffle again', 'สับไพ่ใหม่')}
          </button>
          <button
            onClick={reveal}
            disabled={!done || shuffling}
            style={{
              display: 'flex', alignItems: 'center', gap: '7px', padding: '11px 22px',
              borderRadius: '999px', border: 'none',
              background: done && !shuffling ? meta.accent : '#E5E5E0',
              color: done && !shuffling ? '#fff' : '#9A9A95',
              fontSize: '13px', fontWeight: 500, fontFamily: fontSans,
              cursor: done && !shuffling ? 'pointer' : 'not-allowed',
              boxShadow: done && !shuffling ? '0 6px 16px -8px rgba(0,0,0,0.3)' : 'none',
            }}
          >
            {t('Reveal', 'เปิดไพ่')}
            <ArrowRight size={14} strokeWidth={1.8} />
          </button>
        </div>
      </div>
    )
  }

  /* ============================================================= */
  /*  HISTORY — list of saved readings                              */
  /* ============================================================= */
  if (step === 'history') {
    return shell(
      <div className="cd-fade" style={{ maxWidth: '640px', margin: '0 auto', padding: '40px 24px 56px', width: '100%' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: PAL.muted, marginBottom: '8px' }}>
          {t('Your saved readings', 'บันทึกการอ่านของคุณ')}
        </p>
        <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: 'clamp(26px,5vw,34px)', color: '#1B1B19', margin: '0 0 28px', lineHeight: 1.2 }}>
          {t('Readings you kept', 'การอ่านที่คุณเก็บไว้')}
        </h1>

        {historyErr && (
          <p style={{ fontSize: '13px', color: '#C84B31', marginBottom: '16px' }}>{historyErr}</p>
        )}

        {history === null ? (
          <div style={{ padding: '40px', textAlign: 'center' }}>
            <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#6B5B95', opacity: 0.6, margin: '0 auto' }} />
          </div>
        ) : history.length === 0 ? (
          <div style={{ background: '#fff', border: '1px dashed rgba(0,0,0,0.14)', borderRadius: '16px', padding: '40px 24px', textAlign: 'center' }}>
            <p style={{ fontSize: '14px', color: '#7A7A72', margin: '0 0 16px' }}>
              {t('No saved readings yet. When a card speaks to you, save it here.', 'ยังไม่มีการอ่านที่บันทึกไว้ เมื่อไพ่ใบใดสื่อถึงคุณ บันทึกไว้ที่นี่ได้')}
            </p>
            <button
              onClick={() => setStep('deck')}
              style={{ padding: '10px 20px', borderRadius: '999px', border: 'none', background: '#6B5B95', color: '#fff', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer' }}
            >
              {t('Draw a card', 'จั่วไพ่')}
            </button>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {history.map(r => {
              const d = DECKS[r.deck] || DECKS.tarot
              return (
                <div key={r.id} style={{ display: 'flex', alignItems: 'stretch', gap: '0', background: '#fff', border: `1px solid ${d.border}`, borderRadius: '14px', overflow: 'hidden' }}>
                  <button
                    onClick={() => { setViewing(r); setStep('historyDetail') }}
                    style={{ flex: 1, minWidth: 0, display: 'flex', alignItems: 'center', gap: '14px', padding: '16px 18px', background: 'none', border: 'none', cursor: 'pointer', textAlign: 'left', fontFamily: fontSans }}
                  >
                    <div style={{ width: '40px', height: '40px', borderRadius: '11px', background: d.tint, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px', flexShrink: 0 }}>
                      {d.emoji}
                    </div>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: '14px', fontWeight: 500, color: '#1B1B19', marginBottom: '2px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {r.cards.map(c => {
                          const card = cardById(c.card_id)
                          return card ? (lang === 'th' ? card.name_th : card.name_en) : c.card_id
                        }).join(' · ')}
                      </div>
                      <div style={{ fontSize: '12px', color: '#9A9A95' }}>
                        {t(d.name_en, d.name_th)} · {fmtDate(r.created_at)}
                      </div>
                    </div>
                  </button>
                  <button
                    onClick={() => deleteReading(r.id)}
                    title={t('Delete', 'ลบ')}
                    style={{ flexShrink: 0, padding: '0 16px', background: 'none', border: 'none', borderLeft: '0.5px solid rgba(0,0,0,0.06)', cursor: 'pointer', color: '#C0BEB5' }}
                    onMouseEnter={e => e.currentTarget.style.color = '#C84B31'}
                    onMouseLeave={e => e.currentTarget.style.color = '#C0BEB5'}
                  >
                    <Trash2 size={16} strokeWidth={1.8} />
                  </button>
                </div>
              )
            })}
          </div>
        )}

        <div style={{ marginTop: '28px' }}>{disclaimer}</div>
      </div>
    )
  }

  /* ============================================================= */
  /*  HISTORY DETAIL — one saved reading                            */
  /* ============================================================= */
  if (step === 'historyDetail' && viewing) {
    const d = DECKS[viewing.deck] || DECKS.tarot
    return shell(
      <div className="cd-fade" style={{ maxWidth: '640px', margin: '0 auto', padding: '32px 24px 56px', width: '100%' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: d.accent, marginBottom: '6px', textAlign: 'center' }}>
          {t(d.name_en, d.name_th)} · {viewing.spread_name} · {fmtDate(viewing.created_at)}
        </p>

        {viewing.intention && (
          <p style={{ fontFamily: fontSerif, fontStyle: 'italic', fontSize: '18px', color: '#1B1B19', textAlign: 'center', margin: '4px 0 22px', lineHeight: 1.3 }}>
            “{viewing.intention}”
          </p>
        )}

        <div style={{ display: 'flex', gap: '14px', justifyContent: 'center', flexWrap: 'wrap', margin: '18px 0 24px' }}>
          {viewing.cards.map((c, i) => {
            const card = cardById(c.card_id)
            return (
              <div key={c.card_id + i} style={{ width: viewing.cards.length === 1 ? '170px' : '130px', maxWidth: '40vw' }}>
                {card && (
                  <DeckCard
                    card={card}
                    name={lang === 'th' ? card.name_th : card.name_en}
                    accent={d.accent}
                    faceUp
                    disabled
                    label={c.position}
                  />
                )}
              </div>
            )
          })}
        </div>

        {viewing.reflection && (
          <div style={{ maxWidth: '520px', margin: '0 auto', background: '#fff', border: `1px solid ${d.border}`, borderRadius: '14px', padding: '16px 18px' }}>
            <div style={{ fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.12em', color: d.accent, marginBottom: '6px' }}>
              {t('What you saw', 'สิ่งที่คุณเห็น')}
            </div>
            <p style={{ fontSize: '14px', color: '#3A3A3A', margin: 0, lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
              {viewing.reflection}
            </p>
          </div>
        )}

        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap', margin: '28px 0 20px' }}>
          <button
            onClick={() => setStep('history')}
            style={{ display: 'flex', alignItems: 'center', gap: '7px', padding: '11px 18px', borderRadius: '999px', border: '1px solid rgba(0,0,0,0.12)', background: '#fff', color: '#1B1B19', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer' }}
          >
            <ArrowLeft size={14} strokeWidth={1.8} />
            {t('All readings', 'การอ่านทั้งหมด')}
          </button>
          <button
            onClick={() => deleteReading(viewing.id)}
            style={{ display: 'flex', alignItems: 'center', gap: '7px', padding: '11px 18px', borderRadius: '999px', border: '1px solid #E8C4BC', background: '#fff', color: '#C84B31', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer' }}
          >
            <Trash2 size={14} strokeWidth={1.8} />
            {t('Delete', 'ลบ')}
          </button>
        </div>

        {disclaimer}
      </div>
    )
  }

  /* ============================================================= */
  /*  STEP 4 — reveal + projective reflection                       */
  /* ============================================================= */
  // Safety net: only the reveal render remains below; anything else routes home.
  if (step !== 'reveal' || !spread) {
    return shell(
      <div className="cd-fade" style={{ padding: '60px 24px', textAlign: 'center' }}>
        <button
          onClick={restart}
          style={{ padding: '11px 22px', borderRadius: '999px', border: 'none', background: '#6B5B95', color: '#fff', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer' }}
        >
          {t('Start a reading', 'เริ่มการอ่าน')}
        </button>
      </div>
    )
  }

  return shell(
    <div className="cd-fade" style={{ maxWidth: '720px', margin: '0 auto', padding: '32px 20px 64px', width: '100%' }}>
      <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: meta.accent, marginBottom: '6px', textAlign: 'center' }}>
        {t(meta.name_en, meta.name_th)} · {t(spread.name_en, spread.name_th)}
      </p>
      <h1 style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, fontSize: 'clamp(24px,4.5vw,32px)', color: '#1B1B19', margin: '0 0 24px', lineHeight: 1.2, textAlign: 'center' }}>
        {spread.projective
          ? t('What do you see?', 'คุณเห็นอะไร')
          : t('Your cards', 'ไพ่ของคุณ')}
      </h1>

      {/* Revealed cards */}
      <div style={{
        display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '28px',
      }}>
        {pickedCards.map((card, i) => (
          <div key={card.id} style={{ width: spread.count === 1 ? '190px' : '150px', maxWidth: '44vw' }}>
            <DeckCard
              card={card}
              name={lang === 'th' ? card.name_th : card.name_en}
              accent={meta.accent}
              faceUp={revealed}
              disabled
              label={t(spread.positions[i]?.en, spread.positions[i]?.th)}
            />
          </div>
        ))}
      </div>

      {/* Projective step — for projective spreads we ask FIRST, before any theme.
          The card's own keywords/theme stay hidden until the user opens them. */}
      <div style={{ maxWidth: '560px', margin: '0 auto' }}>
        {spread.projective ? (
          <>
            <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', marginBottom: '8px' }}>
              {spread.count === 1
                ? t('What do you see in this card? Say whatever comes — there is no wrong answer.',
                     'คุณเห็นอะไรในไพ่ใบนี้ พูดสิ่งที่ผุดขึ้นมาได้เลย ไม่มีคำตอบที่ผิด')
                : t('What do you notice across these cards? Your own words lead the reading.',
                     'คุณสังเกตเห็นอะไรจากไพ่เหล่านี้บ้าง คำพูดของคุณเองคือสิ่งที่นำทาง')}
            </label>
            <textarea
              value={reflection}
              onChange={e => setReflection(e.target.value)}
              rows={4}
              placeholder={t('Type freely…', 'พิมพ์ได้ตามสบาย…')}
              style={{
                width: '100%', padding: '12px 14px', fontSize: '14px', lineHeight: 1.6,
                background: '#fff', border: '1px solid rgba(0,0,0,0.12)', borderRadius: '12px',
                outline: 'none', resize: 'vertical', fontFamily: fontSans, color: '#1B1B19',
                boxSizing: 'border-box',
              }}
            />
            <button
              onClick={() => setShowTheme(v => !v)}
              style={{
                marginTop: '14px', display: 'flex', alignItems: 'center', gap: '6px',
                fontSize: '12.5px', color: meta.accent, background: 'none', border: 'none',
                cursor: 'pointer', fontFamily: fontSans, padding: 0,
              }}
            >
              {showTheme
                ? t('Hide possible themes', 'ซ่อนแนวคิดที่เป็นไปได้')
                : t('Show a possible theme (optional)', 'ดูแนวคิดที่เป็นไปได้ (ถ้าต้องการ)')}
            </button>
          </>
        ) : (
          <label style={{ display: 'block', fontSize: '13px', fontWeight: 500, color: '#1B1B19', marginBottom: '8px' }}>
            {t('What comes up as you look at these cards?', 'เมื่อมองไพ่เหล่านี้ มีอะไรผุดขึ้นในใจบ้าง')}
          </label>
        )}

        {!spread.projective && (
          <textarea
            value={reflection}
            onChange={e => setReflection(e.target.value)}
            rows={4}
            placeholder={t('Type freely…', 'พิมพ์ได้ตามสบาย…')}
            style={{
              width: '100%', padding: '12px 14px', fontSize: '14px', lineHeight: 1.6,
              background: '#fff', border: '1px solid rgba(0,0,0,0.12)', borderRadius: '12px',
              outline: 'none', resize: 'vertical', fontFamily: fontSans, color: '#1B1B19',
              boxSizing: 'border-box',
            }}
          />
        )}

        {/* Theme panel — always available for non-projective, gated for projective */}
        {(!spread.projective || showTheme) && (
          <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {pickedCards.map((card, i) => (
              <div key={card.id} style={{ background: meta.tint, border: `1px solid ${meta.border}`, borderRadius: '12px', padding: '13px 15px' }}>
                <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px', marginBottom: '5px', flexWrap: 'wrap' }}>
                  <span style={{ fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.12em', color: meta.accent }}>
                    {t(spread.positions[i]?.en, spread.positions[i]?.th)}
                  </span>
                  <span style={{ fontFamily: fontSerif, fontStyle: 'italic', fontSize: '16px', color: '#1B1B19' }}>{lang === 'th' ? card.name_th : card.name_en}</span>
                </div>
                {/* Neuro cards carry a written meaning; other decks use keyword chips */}
                {card.meaning_en ? (
                  <p style={{ fontSize: '13px', color: '#5A5A52', margin: '0 0 8px', lineHeight: 1.55 }}>
                    {lang === 'th' ? card.meaning_th : card.meaning_en}
                  </p>
                ) : (
                  <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '6px' }}>
                    {(lang === 'th' ? card.keywords_th : card.keywords_en)?.map((k, ki) => (
                      <span key={ki} style={{ fontSize: '11.5px', color: '#6B5B4A', background: '#fff', border: `1px solid ${meta.border}`, padding: '2px 8px', borderRadius: '999px' }}>
                        {k}
                      </span>
                    ))}
                  </div>
                )}
                <p style={{ fontSize: '13px', color: '#5A5A52', margin: 0, lineHeight: 1.55, fontStyle: 'italic' }}>
                  {lang === 'th' ? card.reflect_prompt_th : card.reflect_prompt_en}
                </p>
                {card.micro_intervention && (
                  <p style={{ fontSize: '12px', color: meta.accent, margin: '8px 0 0', lineHeight: 1.5 }}>
                    <span style={{ fontWeight: 600 }}>{t('A small thing to try', 'สิ่งเล็ก ๆ ที่ลองทำได้')}: </span>
                    {card.micro_intervention}
                  </p>
                )}
                {card.clinical_caution && (
                  <p style={{ fontSize: '11px', color: '#9A6A55', margin: '6px 0 0', lineHeight: 1.5 }}>
                    <span style={{ fontWeight: 600 }}>{t('Gentle note', 'ข้อควรระวังเบา ๆ')}: </span>
                    {card.clinical_caution}
                  </p>
                )}
              </div>
            ))}
            {spread.projective && (
              <p style={{ fontSize: '11px', color: PAL.muted, margin: '2px 0 0', lineHeight: 1.5 }}>
                {t('These are possible themes only — not a fixed meaning. Trust what you saw first.',
                   'สิ่งเหล่านี้เป็นเพียงแนวคิดที่เป็นไปได้ ไม่ใช่ความหมายตายตัว เชื่อในสิ่งที่คุณเห็นเป็นอย่างแรก')}
              </p>
            )}
          </div>
        )}

        {/* Save this reading (Stage 3) — only when signed in */}
        {token && (
          <div style={{ marginTop: '24px', borderTop: '0.5px solid rgba(0,0,0,0.08)', paddingTop: '20px' }}>
            {saveState === 'saved' ? (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', color: meta.accent, fontSize: '13px', fontWeight: 500 }}>
                <Check size={16} strokeWidth={2} />
                {t('Saved to your readings.', 'บันทึกไว้ในบันทึกของคุณแล้ว')}
                <button
                  onClick={openHistory}
                  style={{ background: 'none', border: 'none', color: meta.accent, textDecoration: 'underline', textUnderlineOffset: '2px', cursor: 'pointer', fontFamily: fontSans, fontSize: '13px', padding: 0 }}
                >
                  {t('View', 'ดู')}
                </button>
              </div>
            ) : (
              <>
                <label style={{ display: 'block', fontSize: '12.5px', color: '#7A7A72', marginBottom: '6px' }}>
                  {t('Add a focus for this reading (optional)', 'เพิ่มประเด็นที่โฟกัสสำหรับการอ่านนี้ (ถ้าต้องการ)')}
                </label>
                <input
                  value={intention}
                  onChange={e => setIntention(e.target.value)}
                  placeholder={t('e.g. a decision I am sitting with…', 'เช่น เรื่องที่กำลังตัดสินใจอยู่…')}
                  style={{
                    width: '100%', padding: '10px 14px', fontSize: '14px',
                    background: '#fff', border: '1px solid rgba(0,0,0,0.12)', borderRadius: '10px',
                    outline: 'none', fontFamily: fontSans, color: '#1B1B19', boxSizing: 'border-box', marginBottom: '12px',
                  }}
                />
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '10px', flexWrap: 'wrap' }}>
                  <button
                    onClick={saveReading}
                    disabled={saveState === 'saving'}
                    style={{
                      display: 'flex', alignItems: 'center', gap: '7px', padding: '11px 22px',
                      borderRadius: '999px', border: 'none', background: meta.accent, color: '#fff',
                      fontSize: '13px', fontWeight: 500, fontFamily: fontSans,
                      cursor: saveState === 'saving' ? 'default' : 'pointer', opacity: saveState === 'saving' ? 0.6 : 1,
                      boxShadow: '0 6px 16px -8px rgba(0,0,0,0.3)',
                    }}
                  >
                    <BookMarked size={14} strokeWidth={1.8} />
                    {saveState === 'saving' ? t('Saving…', 'กำลังบันทึก…') : t('Save this reading', 'บันทึกการอ่านนี้')}
                  </button>
                </div>
                {saveState === 'error' && (
                  <p style={{ fontSize: '12px', color: '#C84B31', textAlign: 'center', margin: '10px 0 0' }}>
                    {t('Could not save.', 'บันทึกไม่สำเร็จ')} {saveErr}
                  </p>
                )}
              </>
            )}
          </div>
        )}

        {/* Footer actions */}
        <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap', margin: '28px 0 20px' }}>
          <button
            onClick={() => chooseSpread(spread)}
            style={{
              display: 'flex', alignItems: 'center', gap: '7px', padding: '11px 18px',
              borderRadius: '999px', border: '1px solid rgba(0,0,0,0.12)', background: '#fff',
              color: '#1B1B19', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer',
            }}
          >
            <RotateCcw size={14} strokeWidth={1.8} />
            {t('Draw again', 'จั่วใหม่')}
          </button>
          <button
            onClick={restart}
            style={{
              padding: '11px 20px', borderRadius: '999px', border: 'none', background: meta.accent,
              color: '#fff', fontSize: '13px', fontWeight: 500, fontFamily: fontSans, cursor: 'pointer',
              boxShadow: '0 6px 16px -8px rgba(0,0,0,0.3)',
            }}
          >
            {t('New reading', 'อ่านครั้งใหม่')}
          </button>
        </div>

        {disclaimer}
      </div>
    </div>
  )
}
