import { useState, useEffect } from 'react'
import { ArrowRight, Zap } from 'lucide-react'
import DailyDecisionDashboard from './daily_decision_dashboard'
import HomeMenu from './HomeMenu'
import ConsultDashboard from './ConsultDashboard'
import CardDeck from './CardDeck'

/* ------------------------------------------------------------------ */
/*  API helpers                                                         */
/* ------------------------------------------------------------------ */

async function apiFetch(path, { token, ...opts } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (token) headers['Authorization'] = `Bearer ${token}`
  Object.assign(headers, opts.headers || {})

  const res = await fetch('/api' + path, { ...opts, headers })
  const body = await res.json().catch(() => null)
  if (!res.ok) throw new Error(body?.detail || 'Request failed')
  return body
}

async function apiLogin(email, password) {
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ username: email, password }),
  })
  const body = await res.json().catch(() => null)
  if (!res.ok) throw new Error(body?.detail || 'Login failed')
  return body
}

/* Profile shape the dashboard uses internally */
function normaliseProfile(apiProfile) {
  if (!apiProfile) return null
  return {
    birthdate:     apiProfile.birthdate,
    time:          apiProfile.birth_time,
    bloodType:     apiProfile.blood_type || '',
    mbti:          apiProfile.mbti,
    hdType:        apiProfile.hd_type || '',
    personalColor: apiProfile.personal_color || '',
  }
}

function denormaliseProfile(p) {
  return {
    birthdate:      p.birthdate,
    time:           p.time,
    mbti:           p.mbti.toUpperCase(),
    blood_type:     p.bloodType || null,
    hd_type:        p.hdType || null,
    personal_color: p.personalColor || null,
  }
}

/* ------------------------------------------------------------------ */
/*  Auth Modal (login ↔ signup)                                        */
/* ------------------------------------------------------------------ */

function AuthModal({ onAuth }) {
  const [mode, setMode]         = useState('login')
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [error, setError]       = useState('')
  const [loading, setLoading]   = useState(false)

  const fontSans  = "'Geist', ui-sans-serif, system-ui, sans-serif"
  const fontSerif = "'Instrument Serif', ui-serif, Georgia, serif"

  useEffect(() => {
    const id = 'auth-fonts'
    if (document.getElementById(id)) return
    const link = document.createElement('link')
    link.id   = id
    link.rel  = 'stylesheet'
    link.href = 'https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap'
    document.head.appendChild(link)
  }, [])

  const submit = async () => {
    if (!email || !password) return
    setError('')
    setLoading(true)
    try {
      let data
      if (mode === 'signup') {
        data = await apiFetch('/auth/signup', {
          method: 'POST',
          body: JSON.stringify({ email, password }),
        })
      } else {
        data = await apiLogin(email, password)
      }
      onAuth(data.access_token, normaliseProfile(data.profile))
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const onKey = (e) => { if (e.key === 'Enter') submit() }

  const inputStyle = {
    width: '100%',
    padding: '10px 14px',
    fontSize: '14px',
    background: '#F4F2EC',
    border: '1px solid rgba(0,0,0,0.08)',
    borderRadius: '10px',
    outline: 'none',
    transition: 'border-color 0.2s, background 0.2s',
    fontFamily: fontSans,
    color: '#1B1B19',
  }

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#FAFAF6',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '1rem',
        fontFamily: fontSans,
      }}
    >
      <style>{`
        @keyframes auth-scale-in { from { opacity:0; transform:scale(0.97) } to { opacity:1; transform:scale(1) } }
        .auth-card { animation: auth-scale-in 0.35s cubic-bezier(0.22,1,0.36,1) both; }
        .auth-input:focus { outline:none; border-color:rgba(0,0,0,0.25) !important; background:#fff !important; }
      `}</style>

      <div
        className="auth-card"
        style={{
          width: '100%',
          maxWidth: '420px',
          background: '#FFFFFF',
          borderRadius: '20px',
          padding: '36px 40px 40px',
          boxShadow: '0 30px 80px -20px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.04)',
        }}
      >
        {/* Logo mark */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '28px' }}>
          <div
            style={{
              width: '8px', height: '8px', borderRadius: '50%',
              background: '#C84B31',
            }}
          />
          <span style={{ fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.18em', color: '#9A9A95' }}>
            Daily Decision
          </span>
        </div>

        {/* Title */}
        <h1
          style={{
            fontFamily: fontSerif,
            fontStyle: 'italic',
            fontWeight: 400,
            fontSize: '32px',
            letterSpacing: '-0.01em',
            color: '#1B1B19',
            margin: '0 0 6px',
          }}
        >
          {mode === 'login' ? 'Welcome back.' : 'Create account.'}
        </h1>
        <p style={{ fontSize: '13px', color: '#9A9A95', margin: '0 0 28px' }}>
          {mode === 'login'
            ? 'Sign in to restore your profile and daily strategy.'
            : 'One account, your profile saved forever.'}
        </p>

        {/* Fields */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.16em', color: '#9A9A95', marginBottom: '6px' }}>
              Email
            </label>
            <input
              className="auth-input"
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              onKeyDown={onKey}
              autoComplete="email"
              placeholder="you@example.com"
              style={inputStyle}
            />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.16em', color: '#9A9A95', marginBottom: '6px' }}>
              Password
            </label>
            <input
              className="auth-input"
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              onKeyDown={onKey}
              autoComplete={mode === 'signup' ? 'new-password' : 'current-password'}
              placeholder={mode === 'signup' ? 'Min. 8 characters' : '••••••••'}
              style={inputStyle}
            />
          </div>
        </div>

        {/* Error */}
        {error && (
          <p style={{ fontSize: '13px', color: '#C84B31', marginTop: '12px', marginBottom: 0 }}>
            {error}
          </p>
        )}

        {/* Submit */}
        <button
          onClick={submit}
          disabled={loading || !email || !password}
          style={{
            marginTop: '20px',
            width: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            padding: '12px',
            borderRadius: '999px',
            border: 'none',
            background: loading || !email || !password ? '#E5E5E0' : '#1B1B19',
            color: loading || !email || !password ? '#9A9A95' : '#FAFAF6',
            fontSize: '14px',
            fontWeight: 500,
            fontFamily: fontSans,
            cursor: loading || !email || !password ? 'not-allowed' : 'pointer',
            transition: 'all 0.2s',
            boxShadow: loading || !email || !password ? 'none' : '0 1px 2px rgba(0,0,0,0.05), 0 6px 16px -8px rgba(0,0,0,0.2)',
          }}
        >
          {loading ? 'Loading…' : mode === 'login' ? 'Sign in' : 'Create account'}
          {!loading && <ArrowRight size={14} strokeWidth={1.8} />}
        </button>

        {/* Toggle */}
        <p style={{ marginTop: '20px', fontSize: '13px', color: '#9A9A95', textAlign: 'center' }}>
          {mode === 'login' ? "Don't have an account? " : 'Already have an account? '}
          <button
            onClick={() => { setMode(mode === 'login' ? 'signup' : 'login'); setError('') }}
            style={{
              background: 'none', border: 'none', padding: 0,
              color: '#1B1B19', fontWeight: 500, cursor: 'pointer',
              fontSize: '13px', fontFamily: fontSans,
              textDecoration: 'underline', textUnderlineOffset: '2px',
            }}
          >
            {mode === 'login' ? 'Sign up' : 'Sign in'}
          </button>
        </p>
      </div>
    </div>
  )
}

/* ------------------------------------------------------------------ */
/*  App — auth shell                                                    */
/* ------------------------------------------------------------------ */

export default function App() {
  const [token,        setToken]       = useState(() => localStorage.getItem('dd_token'))
  const [profile,      setProfile]     = useState(null)
  const [initialising, setInitialising] = useState(true)
  const [section,      setSection]     = useState(null)   // null = home menu | 'daily' | 'consult'

  /* On mount: validate stored token + fetch profile if it exists */
  useEffect(() => {
    if (!token) { setInitialising(false); return }

    apiFetch('/auth/me', { token })
      .then(user => {
        if (!user.has_profile) return null
        return apiFetch('/profile', { token })
      })
      .then(apiProfile => {
        setProfile(normaliseProfile(apiProfile))
      })
      .catch(() => {
        localStorage.removeItem('dd_token')
        setToken(null)
      })
      .finally(() => setInitialising(false))
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  const handleAuth = (newToken, profileFromResponse) => {
    localStorage.setItem('dd_token', newToken)
    setToken(newToken)
    setProfile(profileFromResponse)   // null on signup (no profile yet)
  }

  const handleLogout = () => {
    localStorage.removeItem('dd_token')
    setToken(null)
    setProfile(null)
    setSection(null)
  }

  const handleSaveProfile = async (dashProfile) => {
    const method = profile ? 'PUT' : 'POST'
    const saved = await apiFetch('/profile', {
      method,
      token,
      body: JSON.stringify(denormaliseProfile(dashProfile)),
    })
    setProfile(normaliseProfile(saved))
  }

  if (initialising) {
    return (
      <div style={{ minHeight: '100vh', background: '#FAFAF6', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: '#C84B31', opacity: 0.6 }} />
      </div>
    )
  }

  if (!token) {
    return <AuthModal onAuth={handleAuth} />
  }

  if (section === 'daily') {
    return (
      <DailyDecisionDashboard
        profile={profile}
        token={token}
        onSaveProfile={handleSaveProfile}
        onLogout={() => setSection(null)}
      />
    )
  }

  if (section === 'consult') {
    return (
      <ConsultDashboard
        token={token}
        onBack={() => setSection(null)}
      />
    )
  }

  if (section === 'cards') {
    return (
      <CardDeck
        token={token}
        onBack={() => setSection(null)}
      />
    )
  }

  return (
    <HomeMenu
      onSelect={setSection}
      onLogout={handleLogout}
    />
  )
}
