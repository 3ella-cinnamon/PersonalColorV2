import { LogOut, ArrowRight } from 'lucide-react'

const fontSans  = "'Geist', ui-sans-serif, system-ui, sans-serif"
const fontSerif = "'Instrument Serif', ui-serif, Georgia, serif"

const SECTIONS = [
  {
    id: 'daily',
    emoji: '⚡',
    title: 'Daily Strategy',
    sub:   'Coaching engine',
    desc:  'Get today\'s personalised behavior plan, timing guidance, and communication strategy based on your MBTI, Human Design, and BaZi.',
    accent: '#C84B31',
    bg:     '#FEF5F2',
    border: '#F5CFCA',
  },
  {
    id: 'consult',
    emoji: '🧠',
    title: 'Consult & Healing',
    sub:   'Psychological assessment',
    desc:  '10 research-validated questions to map your stress patterns, core beliefs, and emotional regulation — with a full profile at the end.',
    accent: '#4A7B6F',
    bg:     '#F0F7F5',
    border: '#B8D9D2',
  },
  {
    id: 'cards',
    emoji: '🃏',
    title: 'Card Deck',
    sub:   'Projective reflection',
    desc:  'Draw from Tarot, Neuro, or Nature decks. Shuffle, pick your cards, and let the images open a gentle, self-guided reflection.',
    accent: '#6B5B95',
    bg:     '#F3F1F8',
    border: '#D6CFE8',
  },
]

export default function HomeMenu({ onSelect, onLogout }) {
  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#FAFAF6',
        fontFamily: fontSans,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '20px 28px',
          borderBottom: '0.5px solid rgba(0,0,0,0.07)',
          background: '#FFFFFF',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <div style={{ width: '7px', height: '7px', borderRadius: '50%', background: '#C84B31' }} />
          <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: '#9A9A95' }}>
            Boong
          </span>
        </div>
        <button
          onClick={onLogout}
          style={{
            display: 'flex', alignItems: 'center', gap: '6px',
            fontSize: '12px', color: '#9A9A95',
            background: 'none', border: 'none', cursor: 'pointer',
            fontFamily: fontSans, padding: '6px 10px',
            borderRadius: '8px', transition: 'background 0.15s',
          }}
          onMouseEnter={e => e.currentTarget.style.background = '#F0EFE8'}
          onMouseLeave={e => e.currentTarget.style.background = 'none'}
        >
          <LogOut size={13} strokeWidth={1.8} />
          Sign out
        </button>
      </div>

      {/* Hero */}
      <div style={{ padding: '52px 28px 36px', maxWidth: '680px', margin: '0 auto', width: '100%' }}>
        <p style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: '#9A9A95', marginBottom: '10px' }}>
          Where would you like to go?
        </p>
        <h1
          style={{
            fontFamily: fontSerif,
            fontStyle: 'italic',
            fontWeight: 400,
            fontSize: 'clamp(28px, 5vw, 40px)',
            color: '#1B1B19',
            letterSpacing: '-0.01em',
            margin: 0,
            lineHeight: 1.2,
          }}
        >
          Your personal engine.
        </h1>
      </div>

      {/* Cards */}
      <div
        style={{
          padding: '0 28px 52px',
          maxWidth: '680px',
          margin: '0 auto',
          width: '100%',
          display: 'flex',
          flexDirection: 'column',
          gap: '14px',
        }}
      >
        {SECTIONS.map(s => (
          <button
            key={s.id}
            onClick={() => onSelect(s.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '20px',
              width: '100%',
              background: '#FFFFFF',
              border: `1px solid ${s.border}`,
              borderRadius: '16px',
              padding: '22px 24px',
              cursor: 'pointer',
              textAlign: 'left',
              transition: 'box-shadow 0.2s, transform 0.15s',
              fontFamily: fontSans,
              boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
            }}
            onMouseEnter={e => {
              e.currentTarget.style.boxShadow = '0 6px 24px -8px rgba(0,0,0,0.12)'
              e.currentTarget.style.transform = 'translateY(-1px)'
            }}
            onMouseLeave={e => {
              e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.04)'
              e.currentTarget.style.transform = 'translateY(0)'
            }}
          >
            {/* Icon */}
            <div
              style={{
                width: '52px', height: '52px', borderRadius: '14px',
                background: s.bg,
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '24px', flexShrink: 0,
              }}
            >
              {s.emoji}
            </div>

            {/* Text */}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '3px' }}>
                <span style={{ fontSize: '16px', fontWeight: 500, color: '#1B1B19' }}>
                  {s.title}
                </span>
                <span
                  style={{
                    fontSize: '10px', textTransform: 'uppercase', letterSpacing: '0.14em',
                    color: s.accent, background: s.bg,
                    padding: '2px 7px', borderRadius: '6px', fontWeight: 500,
                  }}
                >
                  {s.sub}
                </span>
              </div>
              <p style={{ fontSize: '13px', color: '#7A7A72', margin: 0, lineHeight: 1.5 }}>
                {s.desc}
              </p>
            </div>

            {/* Arrow */}
            <ArrowRight size={16} strokeWidth={1.8} color="#C8C6BC" style={{ flexShrink: 0 }} />
          </button>
        ))}
      </div>
    </div>
  )
}
