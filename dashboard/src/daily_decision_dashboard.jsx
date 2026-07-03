import React, { useState, useEffect } from 'react';
import {
  Sparkles, ArrowRight, Copy, Check, X, Clock,
  Wind, Droplets, Footprints, Coffee, Eye, Sun,
  Briefcase, Wallet, Heart, Calendar as CalendarIcon,
  ChevronRight, Activity, User, Zap, LogOut, Brain, Layers,
  AlertTriangle, MessageSquare, Star
} from 'lucide-react';

/* ---------- Backend helpers ---------- */

async function fetchDailyCalc(token, goal, energyLevel, subGoal, lang = 'en') {
  const today = new Date().toISOString().split('T')[0];
  const res = await fetch('/api/daily-calc', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({
      target_date: today,
      goal,
      energy_level: energyLevel,
      hd_aligned: null,
      sub_goal: subGoal || null,
      lang,
    }),
  });
  if (!res.ok) throw new Error('coaching fetch failed');
  return res.json();
}

async function submitFeedback(token, recId, rating) {
  const res = await fetch(`/api/recommendations/${recId}/feedback`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
    },
    body: JSON.stringify({ rating }),
  });
  if (!res.ok) throw new Error('feedback failed');
  return res.json();
}

/* ---------- Curated content ---------- */

const PALETTES = {
  ATTACK: [
    { power: { hex: '#C84B31', name: 'Terracotta' }, support: { hex: '#D4B896', name: 'Wheat' }, neutral: { hex: '#F0EBE3', name: 'Linen' } },
    { power: { hex: '#A03B3B', name: 'Deep Crimson' }, support: { hex: '#E8A33D', name: 'Saffron' }, neutral: { hex: '#EFE9DD', name: 'Bone' } },
    { power: { hex: '#D97757', name: 'Ember' }, support: { hex: '#B8924A', name: 'Burnished' }, neutral: { hex: '#F2EDE3', name: 'Cream' } },
    { power: { hex: '#9C3D2E', name: 'Russet' }, support: { hex: '#D9A441', name: 'Honey' }, neutral: { hex: '#EFE7DA', name: 'Parchment' } },
  ],
  OPTIMIZE: [
    { power: { hex: '#7B8E7F', name: 'Sage' }, support: { hex: '#D4C4A8', name: 'Sand' }, neutral: { hex: '#E8E2D5', name: 'Stone' } },
    { power: { hex: '#5D7E68', name: 'Forest' }, support: { hex: '#9B8F7B', name: 'Mushroom' }, neutral: { hex: '#ECE6D9', name: 'Oat' } },
    { power: { hex: '#8A8B5C', name: 'Olive' }, support: { hex: '#C9B79C', name: 'Driftwood' }, neutral: { hex: '#EBE5D7', name: 'Flax' } },
    { power: { hex: '#6E8569', name: 'Moss' }, support: { hex: '#BFA985', name: 'Camel' }, neutral: { hex: '#EAE3D3', name: 'Wheat' } },
  ],
  RETREAT: [
    { power: { hex: '#6B7B8C', name: 'Slate Blue' }, support: { hex: '#A8B5A8', name: 'Pale Sage' }, neutral: { hex: '#EAEAE6', name: 'Mist' } },
    { power: { hex: '#8A9099', name: 'Dove' }, support: { hex: '#B8BEC4', name: 'Cloud' }, neutral: { hex: '#ECECE8', name: 'Snow' } },
    { power: { hex: '#9888A0', name: 'Soft Mauve' }, support: { hex: '#A8B5BC', name: 'Glacier' }, neutral: { hex: '#EEEAEC', name: 'Fog' } },
    { power: { hex: '#7A8696', name: 'Tide' }, support: { hex: '#B0B5AE', name: 'Lichen' }, neutral: { hex: '#EAEAE5', name: 'Pearl' } },
  ],
};

const TIME_SLOTS = {
  work: {
    ATTACK: [
      { time: '09:00 — 10:30', action: 'Tackle the hardest decision first' },
      { time: '11:00 — 12:00', action: 'High-stakes meetings or pitches' },
      { time: '15:30 — 17:00', action: 'Ship the thing you\'ve been avoiding' },
    ],
    OPTIMIZE: [
      { time: '09:30 — 10:30', action: 'Deep work — single-task only' },
      { time: '13:30 — 14:30', action: 'Review, refine, iterate' },
      { time: '16:00 — 17:00', action: 'Wrap-up & tomorrow\'s plan' },
    ],
    RETREAT: [
      { time: '10:00 — 10:45', action: 'Admin & low-friction tasks only' },
      { time: '14:00 — 15:00', action: 'Read, learn, observe' },
      { time: '16:30 — 17:00', action: 'Light triage — defer big calls' },
    ],
  },
  money: {
    ATTACK: [
      { time: '09:30 — 10:30', action: 'Negotiate, close, ask for the number' },
      { time: '13:00 — 14:00', action: 'Make the investment move' },
      { time: '15:30 — 16:30', action: 'Push outstanding deals forward' },
    ],
    OPTIMIZE: [
      { time: '09:30 — 10:30', action: 'Review positions, rebalance gently' },
      { time: '13:00 — 14:00', action: 'Audit recurring costs' },
      { time: '16:00 — 17:00', action: 'Plan next week\'s moves' },
    ],
    RETREAT: [
      { time: '10:00 — 10:30', action: 'Watch & wait — no new positions' },
      { time: '13:30 — 14:00', action: 'Cancel or pause one expense' },
      { time: '16:00 — 16:30', action: 'Sleep on pending decisions' },
    ],
  },
  relationship: {
    ATTACK: [
      { time: '11:00 — 12:00', action: 'Have the conversation you\'ve postponed' },
      { time: '15:00 — 16:00', action: 'Reach out — initiate without script' },
      { time: '19:00 — 20:00', action: 'Be fully present, phone away' },
    ],
    OPTIMIZE: [
      { time: '12:00 — 13:00', action: 'Lunch with someone who matters' },
      { time: '15:30 — 16:00', action: 'Send the thoughtful message' },
      { time: '19:00 — 20:00', action: 'Share something real, not surface' },
    ],
    RETREAT: [
      { time: '12:30 — 13:00', action: 'Listen more than you speak' },
      { time: '17:00 — 17:30', action: 'Solitude — refill your own cup' },
      { time: '20:00 — 20:30', action: 'Light, easy connection only' },
    ],
  },
};

const SCRIPTS = {
  work: {
    ATTACK: 'Today I move first and decide fast. The expensive cost is hesitation, not error. I commit to one bold move before noon and refuse to renegotiate it with myself for the rest of the day.',
    OPTIMIZE: 'Today I sharpen what already works. I edit before I add. One refinement compounds further than three new starts — I am willing to be quietly excellent today.',
    RETREAT: 'Today I protect my judgment by not using it on big things. I do small work cleanly, observe more than I act, and trust that a calm day now buys me a sharper one tomorrow.',
  },
  money: {
    ATTACK: 'Today money flows toward the person who asks clearly. I name my number without softening it, and I let the silence afterward do the work for me.',
    OPTIMIZE: 'Today I tend to what I already have before I chase what I don\'t. Small leaks sealed quietly outpace one heroic gain. Discipline is the dividend.',
    RETREAT: 'Today I make no irreversible money moves. The market does not need my decision today. Patience is a position — and it is the one I am holding.',
  },
  relationship: {
    ATTACK: 'Today I say the true thing first. The version of me that holds back loses days; the version that speaks plainly gains them. Warm, direct, unhedged.',
    OPTIMIZE: 'Today I show up consistent and unhurried. Connection is built in the small unflashy moments — I aim for one of those, on purpose, with one person.',
    RETREAT: 'Today I conserve. I don\'t explain myself, don\'t over-apologize, don\'t pour out. A short honest "not today" is more loving than a depleted yes.',
  },
};

const TIME_SLOTS_TH = {
  work: {
    ATTACK: [
      { time: '09:00 — 10:30', action: 'จัดการกับการตัดสินใจที่ยากที่สุดก่อนเลย' },
      { time: '11:00 — 12:00', action: 'ประชุมสำคัญหรือนำเสนองานระดับ High-Stakes' },
      { time: '15:30 — 17:00', action: 'ส่งงานที่หลีกเลี่ยงมาตลอดให้สำเร็จ' },
    ],
    OPTIMIZE: [
      { time: '09:30 — 10:30', action: 'Deep work — โฟกัสงานเดียวเท่านั้น' },
      { time: '13:30 — 14:30', action: 'ทบทวน ปรับปรุง และพัฒนาต่อ' },
      { time: '16:00 — 17:00', action: 'สรุปงานและวางแผนพรุ่งนี้' },
    ],
    RETREAT: [
      { time: '10:00 — 10:45', action: 'จัดการงาน Admin และงานที่ไม่กดดัน' },
      { time: '14:00 — 15:00', action: 'อ่าน เรียนรู้ สังเกตการณ์' },
      { time: '16:30 — 17:00', action: 'คัดกรองงานเบาๆ — เลื่อนการตัดสินใจใหญ่ออกไป' },
    ],
  },
  money: {
    ATTACK: [
      { time: '09:30 — 10:30', action: 'เจรจา ปิดดีล ขอตัวเลขที่ต้องการ' },
      { time: '13:00 — 14:00', action: 'ลงมือกับการลงทุนที่วางแผนไว้' },
      { time: '15:30 — 16:30', action: 'ผลักดันดีลที่ค้างอยู่ให้คืบหน้า' },
    ],
    OPTIMIZE: [
      { time: '09:30 — 10:30', action: 'ทบทวน Portfolio และ Rebalance อย่างระมัดระวัง' },
      { time: '13:00 — 14:00', action: 'ตรวจสอบค่าใช้จ่ายประจำ' },
      { time: '16:00 — 17:00', action: 'วางแผน Move ของสัปดาห์หน้า' },
    ],
    RETREAT: [
      { time: '10:00 — 10:30', action: 'แค่สังเกต รอดู — ยังไม่เปิด Position ใหม่' },
      { time: '13:30 — 14:00', action: 'ยกเลิกหรือหยุดค่าใช้จ่ายที่ไม่จำเป็นหนึ่งรายการ' },
      { time: '16:00 — 16:30', action: 'นอนหลับกับการตัดสินใจที่ค้างอยู่' },
    ],
  },
  relationship: {
    ATTACK: [
      { time: '11:00 — 12:00', action: 'พูดคุยเรื่องที่เลื่อนมานานเสียที' },
      { time: '15:00 — 16:00', action: 'ติดต่อก่อน — ริเริ่มโดยไม่ต้องมีสคริปต์' },
      { time: '19:00 — 20:00', action: 'อยู่ตรงนั้นอย่างเต็มที่ วางโทรศัพท์' },
    ],
    OPTIMIZE: [
      { time: '12:00 — 13:00', action: 'ทานข้าวกับคนที่สำคัญ' },
      { time: '15:30 — 16:00', action: 'ส่งข้อความที่เขียนด้วยใจ' },
      { time: '19:00 — 20:00', action: 'แบ่งปันบางอย่างที่จริงใจ ไม่ใช่แค่ผิวเผิน' },
    ],
    RETREAT: [
      { time: '12:30 — 13:00', action: 'ฟังให้มากกว่าพูด' },
      { time: '17:00 — 17:30', action: 'อยู่กับตัวเอง — เติมพลังให้ตัวเอง' },
      { time: '20:00 — 20:30', action: 'การเชื่อมต่อแบบเบาๆ เท่านั้น' },
    ],
  },
};

const SCRIPTS_TH = {
  work: {
    ATTACK: 'วันนี้ฉันลงมือก่อนและตัดสินใจเร็ว ต้นทุนที่แพงที่สุดคือความลังเล ไม่ใช่ความผิดพลาด ฉันจะเลือก Move ที่กล้าหาญหนึ่งอย่างก่อนเที่ยง และจะไม่เจรจาต่อรองกับตัวเองอีกตลอดวัน',
    OPTIMIZE: 'วันนี้ฉันลับคมสิ่งที่ทำงานได้ดีอยู่แล้ว ตัดออกก่อนเพิ่ม การปรับปรุงหนึ่งอย่างให้ดีขึ้นสร้างผลลัพธ์มากกว่าการเริ่มใหม่สามอย่าง ฉันยินดีที่จะเก่งอย่างเงียบๆ วันนี้',
    RETREAT: 'วันนี้ฉันปกป้องวิจารณญาณด้วยการไม่ใช้มันกับเรื่องใหญ่ ทำงานเล็กๆ ให้สะอาด สังเกตให้มากกว่าลงมือ และเชื่อว่าวันที่สงบนี้จะซื้อวันที่คมชัดกว่าไว้ข้างหน้า',
  },
  money: {
    ATTACK: 'วันนี้เงินไหลหาคนที่ขอได้ชัดเจน ฉันบอกตัวเลขที่ต้องการโดยไม่อ่อนลง และปล่อยให้ความเงียบหลังจากนั้นทำงานแทน',
    OPTIMIZE: 'วันนี้ฉันดูแลสิ่งที่มีอยู่ก่อนจะไล่ตามสิ่งที่ยังไม่มี รูรั่วเล็กๆ ที่อุดได้เงียบๆ ชนะได้มากกว่าชัยชนะครั้งใหญ่ครั้งเดียว ระเบียบวินัยคือผลตอบแทน',
    RETREAT: 'วันนี้ฉันไม่ทำ Move ด้านเงินที่ย้อนกลับไม่ได้ ตลาดไม่ต้องการการตัดสินใจของฉันวันนี้ ความอดทนคือ Position — และนั่นคือสิ่งที่ฉันถือไว้',
  },
  relationship: {
    ATTACK: 'วันนี้ฉันพูดความจริงก่อน เวอร์ชันของฉันที่กลั้นไว้สูญเสียเวลา เวอร์ชันที่พูดตรงๆ ได้เวลาคืนมา อบอุ่น ตรงไปตรงมา ไม่อ้อมค้อม',
    OPTIMIZE: 'วันนี้ฉันปรากฏตัวอย่างสม่ำเสมอและไม่รีบร้อน ความสัมพันธ์สร้างขึ้นในช่วงเวลาเล็กๆ ที่ไม่หวือหวา ฉันตั้งใจหาหนึ่งโมเมนต์แบบนั้นกับหนึ่งคน',
    RETREAT: 'วันนี้ฉันอนุรักษ์พลังงาน ไม่อธิบาย ไม่ขอโทษเกินขนาด ไม่เทพลังงานออกไป "ไม่ใช่วันนี้" ที่สั้นและจริงใจ รักมากกว่าคำว่าใช่จากคนที่ล้าแล้ว',
  },
};

const HEALING_ACTIONS = [
  { Icon: Wind, label: 'Box breathing', desc: '4-4-4-4 × 6 rounds' },
  { Icon: Droplets, label: 'Cold splash', desc: '30s on the face' },
  { Icon: Footprints, label: '5-min walk', desc: 'Outside, no phone' },
  { Icon: Coffee, label: 'Tea ritual', desc: 'Make it slowly' },
  { Icon: Eye, label: 'Eye reset', desc: '20ft for 20s' },
  { Icon: Sun, label: 'Sunlight', desc: '2 min, eyes open' },
];

const GOALS = [
  {
    id: 'work', label: 'Work', Icon: Briefcase,
    subs: [
      { id: 'get_buyin',        label: 'Get Buy-in' },
      { id: 'build_trust_work', label: 'Build Trust' },
      { id: 'secure_agreement', label: 'Secure Agreement' },
      { id: 'drive_urgency',    label: 'Drive Urgency' },
      { id: 'win_commitment',   label: 'Win Commitment' },
    ],
  },
  {
    id: 'money', label: 'Money', Icon: Wallet,
    subs: [
      { id: 'close_deal',        label: 'Close the Deal' },
      { id: 'bargain_discount',  label: 'Bargain for Discount' },
      { id: 'handle_objections', label: 'Handle Price Objections' },
      { id: 'increase_value',    label: 'Increase Perceived Value' },
      { id: 'upsell_expand',     label: 'Upsell & Expand' },
    ],
  },
  {
    id: 'relationship', label: 'Relationship', Icon: Heart,
    subs: [
      { id: 'create_attraction',   label: 'Create Attraction' },
      { id: 'build_connection',    label: 'Build Emotional Connection' },
      { id: 'deepen_trust',        label: 'Deepen Trust' },
      { id: 'define_relationship', label: 'Define the Relationship' },
      { id: 'sustain_bond',        label: 'Sustain Long-term Bond' },
    ],
  },
];

/* ---------- Helpers ---------- */

function simpleHash(str) {
  let h = 2166136261;
  for (let i = 0; i < str.length; i++) {
    h ^= str.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return Math.abs(h);
}

function strategyFromScore(score) {
  return score >= 7 ? 'ATTACK' : score >= 4 ? 'OPTIMIZE' : 'RETREAT';
}

function generateInsight(profile, goal, energy) {
  const today = new Date().toDateString();
  const seed = simpleHash(
    `${profile.birthdate}|${profile.time}|${profile.mbti}|${goal}|${today}`
  );
  const goalFactor = (seed % 1000) / 1000;
  const rawScore = energy * 0.62 + goalFactor * 4.2;
  const score = Math.max(0.5, Math.min(10, rawScore));
  const strategy = strategyFromScore(score);
  const palette = PALETTES[strategy][seed % PALETTES[strategy].length];
  const slots = TIME_SLOTS[goal][strategy];
  const script = SCRIPTS[goal][strategy];

  const idxs = [];
  let s = seed;
  while (idxs.length < 3) {
    const i = s % HEALING_ACTIONS.length;
    if (!idxs.includes(i)) idxs.push(i);
    s = Math.floor(s / 7) + 13;
  }
  const actions = idxs.map(i => HEALING_ACTIONS[i]);

  return { score, strategy, palette, slots, script, actions, seed };
}

function energyTint(energy) {
  if (energy <= 3) return '#6B7B8C';
  if (energy <= 6) return '#7B8E7F';
  return '#C84B31';
}

/* ---------- Main component ---------- */

export default function DailyDecisionDashboard({ profile, token, onSaveProfile, onLogout }) {
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [goal, setGoal]         = useState('work');
  const [subGoal, setSubGoal]   = useState('get_buyin');
  const [energy, setEnergy]     = useState(7);
  const [lang, setLang]         = useState('en');
  const [insight, setInsight]   = useState(null);
  const [coachingData, setCoachingData] = useState(null);
  const [coachingLoading, setCoachingLoading] = useState(false);
  const [revealKey, setRevealKey] = useState(0);
  const [copied, setCopied]     = useState(false);
  const [feedbackDone, setFeedbackDone] = useState(false);

  const activeGoalDef = GOALS.find(g => g.id === goal) || GOALS[0];

  const handleSetGoal = (newGoal) => {
    setGoal(newGoal);
    const def = GOALS.find(g => g.id === newGoal);
    const newSubGoal = def ? def.subs[0].id : subGoal;
    if (def) setSubGoal(newSubGoal);

    // Auto-regenerate when goal switches (if a result is already showing)
    if (profile && insight) {
      setInsight(generateInsight(profile, newGoal, energy));
      setCoachingData(null);
      setFeedbackDone(false);
      setRevealKey(k => k + 1);
      if (token) {
        setCoachingLoading(true);
        fetchDailyCalc(token, newGoal, energy, newSubGoal)
          .then(data => setCoachingData(data))
          .catch(() => setCoachingData(null))
          .finally(() => setCoachingLoading(false));
      }
    }
  };

  useEffect(() => {
    const id = 'ddd-fonts';
    if (document.getElementById(id)) return;
    const link = document.createElement('link');
    link.id  = id;
    link.rel = 'stylesheet';
    link.href = 'https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap';
    document.head.appendChild(link);
  }, []);

  const tint = energyTint(energy);

  const handleOnboardingSubmit = async (data) => {
    await onSaveProfile(data);
    setShowOnboarding(false);
  };

  const handleGenerate = async () => {
    if (!profile) { setShowOnboarding(true); return; }
    setCoachingData(null);
    setFeedbackDone(false);
    setInsight(generateInsight(profile, goal, energy));
    setRevealKey(k => k + 1);

    if (token) {
      setCoachingLoading(true);
      try {
        const data = await fetchDailyCalc(token, goal, energy, subGoal, lang);
        setCoachingData(data);
      } catch {
        setCoachingData(null);
      } finally {
        setCoachingLoading(false);
      }
    }
  };

  // Switch language — re-fetch with new lang (cache hit, near-instant)
  const handleLangSwitch = async (newLang) => {
    setLang(newLang);
    if (!coachingData || !token) return;
    setCoachingLoading(true);
    try {
      const data = await fetchDailyCalc(token, goal, energy, subGoal, newLang);
      setCoachingData(data);
    } catch {
      // keep existing data on error
    } finally {
      setCoachingLoading(false);
    }
  };

  const handleFeedback = async (rating) => {
    if (!coachingData?.id || feedbackDone) return;
    try {
      await submitFeedback(token, coachingData.id, rating);
      setFeedbackDone(true);
    } catch {
      // best-effort
    }
  };

  const copyScript = async () => {
    if (!insight) return;
    try {
      await navigator.clipboard.writeText(insight.script);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      // best-effort
    }
  };

  // Use backend bazi_score for strategy when available
  const liveScore = coachingData?.bazi_score != null ? coachingData.bazi_score : insight?.score;
  const liveStrategy = liveScore != null ? strategyFromScore(liveScore) : insight?.strategy;

  const today = new Date().toLocaleDateString(undefined, {
    weekday: 'long', month: 'long', day: 'numeric',
  });

  const fontSans  = "'Geist', ui-sans-serif, system-ui, -apple-system, sans-serif";
  const fontSerif = "'Instrument Serif', ui-serif, Georgia, serif";

  return (
    <div
      className="min-h-screen w-full"
      style={{
        backgroundColor: '#FAFAF6',
        backgroundImage: 'radial-gradient(at 10% 0%, rgba(200,75,49,0.04), transparent 50%), radial-gradient(at 90% 10%, rgba(123,142,127,0.05), transparent 50%)',
        fontFamily: fontSans,
        color: '#1B1B19',
      }}
    >
      <style>{`
        @keyframes ddd-fade-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes ddd-fade { from { opacity: 0; } to { opacity: 1; } }
        @keyframes ddd-scale-in { from { opacity: 0; transform: scale(0.97); } to { opacity: 1; transform: scale(1); } }
        @keyframes ddd-spin { to { transform: rotate(360deg); } }
        .ddd-reveal { animation: ddd-fade-up 0.7s cubic-bezier(0.22, 1, 0.36, 1) both; }
        .ddd-modal-bg { animation: ddd-fade 0.25s ease-out both; }
        .ddd-modal-card { animation: ddd-scale-in 0.35s cubic-bezier(0.22, 1, 0.36, 1) both; }
        .ddd-spinner { animation: ddd-spin 0.8s linear infinite; }
        .ddd-slider { -webkit-appearance: none; appearance: none; width: 100%; height: 4px; border-radius: 999px; background: #E5E5E0; outline: none; transition: background 0.3s; }
        .ddd-slider::-webkit-slider-thumb { -webkit-appearance: none; appearance: none; width: 22px; height: 22px; border-radius: 999px; background: #fff; cursor: pointer; box-shadow: 0 0 0 1.5px var(--tint), 0 1px 3px rgba(0,0,0,0.08); transition: transform 0.15s ease; }
        .ddd-slider::-webkit-slider-thumb:hover { transform: scale(1.1); }
        .ddd-slider::-moz-range-thumb { width: 22px; height: 22px; border-radius: 999px; background: #fff; cursor: pointer; border: none; box-shadow: 0 0 0 1.5px var(--tint), 0 1px 3px rgba(0,0,0,0.08); }
        .ddd-card { background: #FFFFFF; border: 1px solid rgba(0,0,0,0.05); border-radius: 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.02), 0 8px 24px -12px rgba(0,0,0,0.06); }
        .ddd-pill { background: #FFFFFF; border: 1px solid rgba(0,0,0,0.07); border-radius: 999px; transition: all 0.2s ease; }
        .ddd-pill:hover { transform: translateY(-1px); box-shadow: 0 4px 14px rgba(0,0,0,0.06); }
        .ddd-input { background: #FAFAF6; border: 1px solid rgba(0,0,0,0.08); border-radius: 10px; transition: border-color 0.2s, background 0.2s; }
        .ddd-input:focus { outline: none; border-color: rgba(0,0,0,0.25); background: #fff; }
        .ddd-strat-attack { color: #C84B31; }
        .ddd-strat-optimize { color: #5D7E68; }
        .ddd-strat-retreat { color: #6B7B8C; }
        .ddd-star { cursor: pointer; transition: transform 0.1s ease; }
        .ddd-star:hover { transform: scale(1.15); }
      `}</style>

      {/* === Header === */}
      <header
        className="sticky top-0 z-30 backdrop-blur"
        style={{ backgroundColor: 'rgba(250, 250, 246, 0.85)', borderBottom: '1px solid rgba(0,0,0,0.05)' }}
      >
        <div className="max-w-6xl mx-auto px-5 md:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="w-2 h-2 rounded-full transition-colors duration-500" style={{ background: tint }} />
            <span className="text-xs uppercase tracking-[0.18em] text-gray-500">Daily Decision</span>
          </div>
          <div className="hidden md:flex items-center gap-2 text-xs text-gray-500">
            <CalendarIcon size={13} strokeWidth={1.6} />
            <span>{today}</span>
          </div>
          <div className="flex items-center gap-3">
            {profile && (
              <button
                onClick={() => setShowOnboarding(true)}
                className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-900 transition-colors"
                title="Edit profile"
              >
                <User size={13} strokeWidth={1.6} />
                <span className="hidden sm:inline">{profile.mbti}</span>
                {profile.personalColor && (
                  <span
                    className="hidden sm:inline px-1.5 py-0.5 rounded-full text-[10px] font-medium"
                    style={{ background: colorSeasonBg(profile.personalColor), color: colorSeasonFg(profile.personalColor) }}
                  >
                    {profile.personalColor}
                  </span>
                )}
              </button>
            )}
            {/* Language toggle */}
            <div style={{ display: 'flex', background: '#F0EDE6', borderRadius: '20px', padding: '2px', gap: '2px' }}>
              {['en', 'th'].map(l => (
                <button
                  key={l}
                  onClick={() => handleLangSwitch(l)}
                  style={{
                    padding: '3px 10px',
                    borderRadius: '16px',
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '11px',
                    fontWeight: 600,
                    letterSpacing: '0.04em',
                    background: lang === l ? '#1B1B19' : 'transparent',
                    color: lang === l ? '#FAFAF6' : '#9A9A95',
                    transition: 'all 0.15s',
                  }}
                >
                  {l.toUpperCase()}
                </button>
              ))}
            </div>

            {onLogout && (
              <button
                onClick={onLogout}
                className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-900 transition-colors"
                title="Sign out"
              >
                <LogOut size={13} strokeWidth={1.6} />
                <span className="hidden sm:inline">Sign out</span>
              </button>
            )}
          </div>
        </div>

        {/* Input bar */}
        {!showOnboarding && (
          <div className="border-t" style={{ borderColor: 'rgba(0,0,0,0.05)', '--tint': tint }}>
            <div className="max-w-6xl mx-auto px-5 md:px-8 pt-3 pb-2 flex flex-wrap items-center gap-3">
              <span className="text-[11px] uppercase tracking-[0.16em] text-gray-400 shrink-0">Goal</span>
              {GOALS.map(g => {
                const active = goal === g.id;
                return (
                  <button
                    key={g.id}
                    onClick={() => handleSetGoal(g.id)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm transition-all"
                    style={{
                      background: active ? '#1B1B19' : 'transparent',
                      color: active ? '#FAFAF6' : '#1B1B19',
                      border: '1px solid ' + (active ? '#1B1B19' : 'rgba(0,0,0,0.1)'),
                    }}
                  >
                    <g.Icon size={13} strokeWidth={1.7} />
                    {g.label}
                  </button>
                );
              })}
            </div>

            <div className="max-w-6xl mx-auto px-5 md:px-8 pb-2 flex flex-wrap items-center gap-2">
              <span className="text-[11px] uppercase tracking-[0.16em] text-gray-400 shrink-0">Focus</span>
              {activeGoalDef.subs.map(s => {
                const active = subGoal === s.id;
                return (
                  <button
                    key={s.id}
                    onClick={() => setSubGoal(s.id)}
                    className="px-2.5 py-1 rounded-full text-xs transition-all"
                    style={{
                      background: active ? tint + '18' : 'transparent',
                      color: active ? tint : '#9A9A95',
                      border: '1px solid ' + (active ? tint + '50' : 'rgba(0,0,0,0.07)'),
                      fontWeight: active ? 500 : 400,
                    }}
                  >
                    {s.label}
                  </button>
                );
              })}
            </div>

            <div className="max-w-6xl mx-auto px-5 md:px-8 pb-3 flex flex-col md:flex-row md:items-center gap-3 md:gap-6 border-t" style={{ borderColor: 'rgba(0,0,0,0.04)' }}>
              <div className="flex items-center gap-3 flex-1 min-w-0 pt-3">
                <span className="text-[11px] uppercase tracking-[0.16em] text-gray-400 shrink-0">Energy</span>
                <input
                  type="range" min="1" max="10" step="1" value={energy}
                  onChange={e => setEnergy(parseInt(e.target.value))}
                  className="ddd-slider flex-1 min-w-[80px]"
                  style={{
                    '--tint': tint,
                    background: `linear-gradient(to right, ${tint} 0%, ${tint} ${(energy - 1) * 11.11}%, #E5E5E0 ${(energy - 1) * 11.11}%, #E5E5E0 100%)`,
                  }}
                />
                <span className="text-base tabular-nums w-6 text-right" style={{ color: tint, fontWeight: 500 }}>
                  {energy}
                </span>
              </div>
              <button
                onClick={handleGenerate}
                className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-full text-sm font-medium transition-all hover:translate-y-[-1px] active:translate-y-0 md:mt-3"
                style={{
                  background: '#1B1B19',
                  color: '#FAFAF6',
                  boxShadow: '0 1px 2px rgba(0,0,0,0.05), 0 6px 16px -8px rgba(0,0,0,0.2)',
                }}
              >
                {coachingLoading ? (
                  <svg className="ddd-spinner" width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <circle cx="7" cy="7" r="5.5" stroke="rgba(255,255,255,0.3)" strokeWidth="1.5" />
                    <path d="M7 1.5A5.5 5.5 0 0 1 12.5 7" stroke="#FAFAF6" strokeWidth="1.5" strokeLinecap="round" />
                  </svg>
                ) : (
                  <Sparkles size={14} strokeWidth={1.8} />
                )}
                {!profile ? 'Get Started' : insight ? 'Refresh' : 'Generate'}
                {!coachingLoading && <ArrowRight size={14} strokeWidth={1.8} />}
              </button>
            </div>
          </div>
        )}
      </header>

      {/* === Body === */}
      <main className="max-w-6xl mx-auto px-5 md:px-8 py-10 md:py-16">
        {!insight && (
          <EmptyState tint={tint} fontSerif={fontSerif} hasProfile={!!profile} onSetup={() => setShowOnboarding(true)} />
        )}

        {insight && (
          <Dashboard
            key={revealKey}
            insight={insight}
            goal={goal}
            subGoal={subGoal}
            energy={energy}
            tint={tint}
            fontSans={fontSans}
            fontSerif={fontSerif}
            onCopy={copyScript}
            copied={copied}
            coachingData={coachingData}
            coachingLoading={coachingLoading}
            liveStrategy={liveStrategy}
            liveScore={liveScore}
            onFeedback={handleFeedback}
            feedbackDone={feedbackDone}
            profile={profile}
            lang={lang}
          />
        )}
      </main>

      {showOnboarding && (
        <OnboardingModal
          initial={profile}
          onClose={profile ? () => setShowOnboarding(false) : null}
          onSubmit={handleOnboardingSubmit}
          fontSerif={fontSerif}
        />
      )}

      <footer className="max-w-6xl mx-auto px-5 md:px-8 py-10 text-[11px] text-gray-400 tracking-wide">
        Same inputs · same day → same local score. AI coaching varies every generation.
      </footer>
    </div>
  );
}

/* ---------- Color season helpers ---------- */

function colorSeasonBg(season) {
  return { Spring: '#FFF3E0', Summer: '#E8EAF6', Autumn: '#FBE9E7', Winter: '#E3F2FD' }[season] || '#F0F0F0';
}
function colorSeasonFg(season) {
  return { Spring: '#E65100', Summer: '#3949AB', Autumn: '#BF360C', Winter: '#1565C0' }[season] || '#666';
}

/* ---------- Empty state ---------- */

function EmptyState({ tint, fontSerif, hasProfile, onSetup }) {
  return (
    <div className="ddd-reveal py-20 text-center">
      <div
        className="inline-flex items-center justify-center w-12 h-12 rounded-full mb-6 transition-colors duration-500"
        style={{ background: tint + '14', color: tint }}
      >
        <Sparkles size={20} strokeWidth={1.6} />
      </div>
      <h2
        className="text-3xl md:text-4xl mb-3"
        style={{ fontFamily: fontSerif, fontWeight: 400, letterSpacing: '-0.01em' }}
      >
        <span style={{ fontStyle: 'italic' }}>
          {hasProfile ? "Set today's frame." : 'Your daily strategy engine.'}
        </span>
      </h2>
      <p className="text-sm text-gray-500 max-w-md mx-auto">
        {hasProfile
          ? "Pick a goal, gauge your energy, then generate today's strategy."
          : "Pick a goal and energy level, then generate. You'll be asked for a quick profile on your first run."}
      </p>
      {!hasProfile && (
        <button
          onClick={onSetup}
          className="mt-6 inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-sm font-medium transition-all hover:translate-y-[-1px]"
          style={{
            background: '#1B1B19', color: '#FAFAF6',
            boxShadow: '0 1px 2px rgba(0,0,0,0.05), 0 6px 16px -8px rgba(0,0,0,0.2)',
          }}
        >
          <User size={14} strokeWidth={1.7} />
          Set up profile
        </button>
      )}
    </div>
  );
}

/* ---------- Dashboard ---------- */

function Dashboard({
  insight, goal, subGoal, energy, tint, fontSans, fontSerif,
  onCopy, copied, coachingData, coachingLoading, liveStrategy, liveScore,
  onFeedback, feedbackDone, profile, lang,
}) {
  const { score: localScore, strategy: localStrategy, actions, seed } = insight;

  const strategy  = liveStrategy || localStrategy;
  const palette   = PALETTES[strategy][seed % PALETTES[strategy].length];
  // Always derive slots/script from live goal+strategy so switching tabs shows correct content
  const slotsData  = lang === 'th' ? TIME_SLOTS_TH : TIME_SLOTS;
  const scriptsData = lang === 'th' ? SCRIPTS_TH   : SCRIPTS;
  const slots  = slotsData[goal]?.[strategy]  ?? slotsData[goal]?.[localStrategy]  ?? [];
  const script = scriptsData[goal]?.[strategy] ?? scriptsData[goal]?.[localStrategy] ?? '';
  const stratColor =
    strategy === 'ATTACK' ? '#C84B31' :
    strategy === 'OPTIMIZE' ? '#5D7E68' : '#6B7B8C';
  const stratClass =
    strategy === 'ATTACK' ? 'ddd-strat-attack' :
    strategy === 'OPTIMIZE' ? 'ddd-strat-optimize' : 'ddd-strat-retreat';

  const displayScore = liveScore ?? localScore;
  const stagger = (i) => ({ animationDelay: `${i * 90}ms` });

  return (
    <div>
      {/* Score Header */}
      <section className="ddd-reveal" style={stagger(0)}>
        <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-12 md:mb-16">
          <div>
            <div className="text-[11px] uppercase tracking-[0.18em] text-gray-400 mb-3">
              {coachingData?.bazi_score != null ? 'BaZi Action Score' : "Today's Score"}
            </div>
            <div className="leading-none flex items-baseline gap-3" style={{ fontFamily: fontSerif }}>
              <span style={{
                fontSize: 'clamp(96px, 14vw, 168px)',
                fontStyle: 'italic', fontWeight: 400, letterSpacing: '-0.04em', color: '#1B1B19',
              }}>
                {displayScore.toFixed(1)}
              </span>
              <span className="text-2xl md:text-3xl text-gray-300" style={{ fontFamily: fontSerif, fontStyle: 'italic' }}>
                / 10
              </span>
            </div>
          </div>

          <div className="md:text-right">
            <div className="text-[11px] uppercase tracking-[0.18em] text-gray-400 mb-3">Strategy</div>
            <div className="flex md:justify-end items-center gap-3">
              <span className="w-1.5 h-1.5 rounded-full" style={{ background: stratColor }} />
              <span className={'text-2xl md:text-3xl font-medium tracking-[0.06em] ' + stratClass} style={{ fontFamily: fontSans }}>
                {strategy}
              </span>
            </div>
            <p className="text-sm text-gray-500 mt-2 max-w-xs md:ml-auto">
              {strategy === 'ATTACK'  && 'High-conviction day. Move first.'}
              {strategy === 'OPTIMIZE' && 'Steady day. Refine over revolution.'}
              {strategy === 'RETREAT'  && 'Low-friction day. Protect judgment.'}
            </p>
          </div>
        </div>
      </section>

      {/* AI Coaching Section */}
      {(coachingData || coachingLoading) && (
        <section className="ddd-reveal mb-10" style={stagger(1)}>
          <CoachingSection
            data={coachingData}
            loading={coachingLoading}
            goal={goal}
            subGoal={subGoal}
            tint={tint}
            stratColor={stratColor}
            fontSerif={fontSerif}
            onFeedback={onFeedback}
            feedbackDone={feedbackDone}
            profile={profile}
          />
        </section>
      )}

      {/* Color Strategy */}
      <section className="ddd-reveal mb-10" style={stagger(2)}>
        <SectionLabel>Color Strategy</SectionLabel>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 md:gap-4">
          <ColorCard role="Power"     color={palette.power}   />
          <ColorCard role="Supportive" color={palette.support} />
          <ColorCard role="Neutral"   color={palette.neutral}  />
        </div>
      </section>

      {/* Time Slots */}
      <section className="ddd-reveal mb-10" style={stagger(3)}>
        <SectionLabel>
          <span className="flex items-center gap-2">
            <Clock size={12} strokeWidth={1.7} />
            {lang === 'th' ? 'ช่วงเวลาที่เหมาะสมที่สุด' : 'Optimal Time Blocks'}
          </span>
        </SectionLabel>
        <div className="ddd-card overflow-hidden">
          {slots.map((s, i) => (
            <div
              key={i}
              className="flex items-center gap-4 md:gap-8 px-5 md:px-7 py-5"
              style={{ borderTop: i === 0 ? 'none' : '1px solid rgba(0,0,0,0.05)' }}
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="w-1 h-8 rounded-full shrink-0" style={{ background: stratColor, opacity: 0.6 }} />
                <span className="text-sm md:text-base tabular-nums whitespace-nowrap" style={{ color: '#1B1B19', fontWeight: 500 }}>
                  {s.time}
                </span>
              </div>
              <div className="text-sm md:text-base text-gray-600 flex-1">{s.action}</div>
              <ChevronRight size={16} strokeWidth={1.4} className="text-gray-300 shrink-0 hidden md:block" />
            </div>
          ))}
        </div>
      </section>

      {/* Script */}
      <section className="ddd-reveal mb-10" style={stagger(4)}>
        <div className="flex items-end justify-between mb-3">
          <SectionLabel className="mb-0">{lang === 'th' ? 'คำประจำวัน' : 'Daily Auto Script'}</SectionLabel>
          <button onClick={onCopy} className="flex items-center gap-1.5 text-xs text-gray-500 hover:text-gray-900 transition-colors">
            {copied ? <><Check size={13} strokeWidth={1.8} />{lang === 'th' ? 'คัดลอกแล้ว' : 'Copied'}</> : <><Copy size={13} strokeWidth={1.8} />{lang === 'th' ? 'คัดลอก' : 'Copy'}</>}
          </button>
        </div>
        <div
          className="ddd-card relative px-6 md:px-10 py-8 md:py-10"
          style={{ background: `linear-gradient(135deg, ${palette.neutral.hex} 0%, #FFFFFF 100%)` }}
        >
          <span
            className="absolute -top-2 left-6 md:left-10 text-6xl leading-none select-none"
            style={{ fontFamily: fontSerif, color: stratColor, opacity: 0.5 }}
          >
            "
          </span>
          <p
            className="text-lg md:text-xl leading-relaxed pl-2"
            style={{ fontFamily: fontSerif, fontStyle: 'italic', fontWeight: 400, color: '#1B1B19', letterSpacing: '0.005em' }}
          >
            {script}
          </p>
        </div>
      </section>

      {/* Healing Actions */}
      <section className="ddd-reveal" style={stagger(5)}>
        <SectionLabel>
          <span className="flex items-center gap-2">
            <Activity size={12} strokeWidth={1.7} />
            Healing Actions <span className="text-gray-300 font-normal">· under 5 minutes</span>
          </span>
        </SectionLabel>
        <div className="flex flex-wrap gap-2.5">
          {actions.map((a, i) => (
            <button key={i} className="ddd-pill flex items-center gap-2.5 pl-3 pr-4 py-2.5 text-sm">
              <span className="w-7 h-7 rounded-full flex items-center justify-center shrink-0" style={{ background: stratColor + '14', color: stratColor }}>
                <a.Icon size={14} strokeWidth={1.7} />
              </span>
              <span style={{ fontWeight: 500 }}>{a.label}</span>
              <span className="text-gray-400 text-xs hidden sm:inline">{a.desc}</span>
            </button>
          ))}
        </div>
      </section>
    </div>
  );
}

/* ---------- Sub-components ---------- */

function SectionLabel({ children, className = '' }) {
  return (
    <div className={'text-[11px] uppercase tracking-[0.18em] text-gray-400 mb-4 ' + className}>
      {children}
    </div>
  );
}

function ColorCard({ role, color }) {
  return (
    <div className="ddd-card overflow-hidden">
      <div className="h-32 md:h-36 transition-all" style={{ background: color.hex }} />
      <div className="px-5 py-4">
        <div className="text-[10px] uppercase tracking-[0.18em] text-gray-400 mb-1.5">{role}</div>
        <div className="flex items-baseline justify-between gap-3">
          <span className="text-base" style={{ fontWeight: 500 }}>{color.name}</span>
          <span className="text-xs text-gray-400 tabular-nums tracking-wide">{color.hex.toUpperCase()}</span>
        </div>
      </div>
    </div>
  );
}

/* ---------- Coaching Section (replaces PersonalityInsightSection) ---------- */

function CoachingSection({ data, loading, goal, subGoal, tint, stratColor, fontSerif, onFeedback, feedbackDone, profile }) {
  const [copiedIdx, setCopiedIdx] = useState(null);
  const [hoveredStar, setHoveredStar] = useState(0);
  const [selectedStar, setSelectedStar] = useState(0);

  const goalLabel    = { work: 'Work', money: 'Money', relationship: 'Relationship' }[goal] || goal;
  const subGoalLabel = GOALS.find(g => g.id === goal)?.subs.find(s => s.id === subGoal)?.label || '';
  const mbtiType     = profile?.mbti || '';
  const hdType       = profile?.hdType || '';
  const colorSeason  = profile?.personalColor || '';

  const copyText = async (text, idx) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIdx(idx);
      setTimeout(() => setCopiedIdx(null), 1600);
    } catch { /* best-effort */ }
  };

  const handleStar = (n) => {
    if (feedbackDone) return;
    setSelectedStar(n);
    onFeedback(n);
  };

  if (loading && !data) {
    return (
      <div>
        <SectionLabel>
          <span className="flex items-center gap-2">
            <Brain size={12} strokeWidth={1.7} />
            AI Coaching
            <span className="text-gray-300 font-normal">· {goalLabel}{subGoalLabel ? ` / ${subGoalLabel}` : ''}</span>
          </span>
        </SectionLabel>
        <div className="ddd-card px-6 py-10 flex flex-col items-center gap-3 text-center">
          <svg className="ddd-spinner" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <circle cx="10" cy="10" r="8" stroke="rgba(0,0,0,0.1)" strokeWidth="2" />
            <path d="M10 2A8 8 0 0 1 18 10" stroke="#1B1B19" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <p className="text-sm text-gray-500">Generating your coaching…</p>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div>
      <SectionLabel>
        <span className="flex items-center gap-2">
          <Brain size={12} strokeWidth={1.7} />
          AI Coaching
          <span className="text-gray-300 font-normal">· {goalLabel}{subGoalLabel ? ` / ${subGoalLabel}` : ''}</span>
        </span>
      </SectionLabel>

      <div className="flex flex-col gap-3 md:gap-4">

        {/* Profile badges */}
        <div className="flex flex-wrap gap-2">
          {mbtiType && (
            <span className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full" style={{ background: '#7B8E7F14', color: '#5D7E68' }}>
              <Brain size={11} strokeWidth={2} />{mbtiType}
            </span>
          )}
          {hdType && (
            <span className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full" style={{ background: '#9888A014', color: '#9888A0' }}>
              <Layers size={11} strokeWidth={2} />{hdType}
            </span>
          )}
          {colorSeason && (
            <span className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full" style={{ background: colorSeasonBg(colorSeason), color: colorSeasonFg(colorSeason) }}>
              {colorSeason}
            </span>
          )}
        </div>

        {/* Coaching summary */}
        {data.coaching_summary && (
          <div
            className="ddd-card px-5 py-5"
            style={{ background: `linear-gradient(135deg, ${stratColor}08 0%, #FFFFFF 100%)` }}
          >
            <p
              className="text-base md:text-lg leading-relaxed"
              style={{ fontFamily: fontSerif, fontStyle: 'italic', color: '#1B1B19' }}
            >
              {data.coaching_summary}
            </p>
          </div>
        )}

        {/* Behavior + Timing + Communication — 3 cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {data.behavior_recommendation && (
            <CoachingCard
              icon={<Activity size={12} strokeWidth={2} />}
              label="Behavior"
              color="#5D7E68"
              text={data.behavior_recommendation}
            />
          )}
          {data.timing_guidance && (
            <CoachingCard
              icon={<Clock size={12} strokeWidth={2} />}
              label="Timing"
              color="#B8924A"
              text={data.timing_guidance}
            />
          )}
          {data.communication_strategy && (
            <CoachingCard
              icon={<MessageSquare size={12} strokeWidth={2} />}
              label="Communication"
              color="#6B7B8C"
              text={data.communication_strategy}
            />
          )}
        </div>

        {/* Warnings */}
        {data.warnings?.length > 0 && (
          <div className="ddd-card px-5 py-5">
            <div className="flex items-center gap-2 mb-3">
              <span className="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style={{ background: '#C84B3114', color: '#C84B31' }}>
                <AlertTriangle size={12} strokeWidth={2} />
              </span>
              <span className="text-[10px] uppercase tracking-[0.18em] font-semibold" style={{ color: '#C84B31' }}>
                Watch Out For
              </span>
            </div>
            <div className="flex flex-col gap-2">
              {data.warnings.map((w, i) => (
                <div key={i} className="flex items-start gap-2.5">
                  <span className="mt-1.5 w-1.5 h-1.5 rounded-full shrink-0" style={{ background: '#C84B31', opacity: 0.5 }} />
                  <p className="text-sm leading-relaxed text-gray-700">{w}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Sample Sentences */}
        {data.sample_sentences?.length > 0 && (
          <div className="ddd-card px-5 py-5">
            <div className="flex items-center gap-2 mb-4">
              <span className="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style={{ background: `${stratColor}14`, color: stratColor }}>
                <MessageSquare size={12} strokeWidth={2} />
              </span>
              <span className="text-[10px] uppercase tracking-[0.18em] font-semibold" style={{ color: stratColor }}>
                Sample Sentences
              </span>
              <span className="ml-auto text-[10px] text-gray-400">tap to copy</span>
            </div>
            <div className="flex flex-col gap-2">
              {data.sample_sentences.map((sent, i) => {
                const parts = sent.split('::');
                const scenario = parts.length > 1 ? parts[0].trim() : null;
                const sentence = parts.length > 1 ? parts[1].trim() : sent.trim();
                return (
                  <button
                    key={i}
                    onClick={() => copyText(sentence, `s${i}`)}
                    className="group w-full text-left rounded-xl px-4 py-3 transition-all hover:bg-gray-50"
                    style={{ border: '1px solid rgba(0,0,0,0.06)' }}
                  >
                    <div className="flex items-start gap-3">
                      <span className="shrink-0 mt-0.5 text-[10px] font-semibold tabular-nums" style={{ color: stratColor, opacity: 0.6 }}>
                        {String(i + 1).padStart(2, '0')}
                      </span>
                      <div className="flex-1">
                        {scenario && (
                          <p className="text-[10px] uppercase tracking-[0.12em] mb-1" style={{ color: stratColor, opacity: 0.7 }}>
                            {scenario}
                          </p>
                        )}
                        <p className="text-sm leading-relaxed text-gray-800 font-semibold">"{sentence}"</p>
                      </div>
                      <span className="shrink-0 mt-0.5 text-gray-300 group-hover:text-gray-500 transition-colors">
                        {copiedIdx === `s${i}` ? <Check size={13} strokeWidth={2} /> : <Copy size={13} strokeWidth={1.6} />}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Alternative Responses */}
        {data.alternative_responses?.length > 0 && (
          <div className="ddd-card px-5 py-5">
            <div className="flex items-center gap-2 mb-4">
              <span className="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style={{ background: '#9888A014', color: '#9888A0' }}>
                <ArrowRight size={12} strokeWidth={2} />
              </span>
              <span className="text-[10px] uppercase tracking-[0.18em] font-semibold" style={{ color: '#9888A0' }}>
                Alternative Responses
              </span>
            </div>
            <div className="flex flex-col gap-2">
              {data.alternative_responses.map((alt, i) => {
                const parts = alt.split('::');
                const scenario = parts.length > 1 ? parts[0].trim() : null;
                const sentence = parts.length > 1 ? parts[1].trim() : alt.trim();
                return (
                  <button
                    key={i}
                    onClick={() => copyText(sentence, `a${i}`)}
                    className="group w-full text-left rounded-xl px-4 py-3 transition-all hover:bg-gray-50"
                    style={{ border: '1px solid rgba(0,0,0,0.06)' }}
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex-1">
                        {scenario && (
                          <p className="text-[10px] uppercase tracking-[0.12em] mb-1 text-gray-400">
                            {scenario}
                          </p>
                        )}
                        <p className="text-sm leading-relaxed text-gray-700 font-semibold">"{sentence}"</p>
                      </div>
                      <span className="shrink-0 mt-0.5 text-gray-300 group-hover:text-gray-500 transition-colors">
                        {copiedIdx === `a${i}` ? <Check size={13} strokeWidth={2} /> : <Copy size={13} strokeWidth={1.6} />}
                      </span>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Star feedback */}
        <div className="flex items-center gap-4 px-1 py-2">
          <span className="text-[11px] uppercase tracking-[0.16em] text-gray-400">Rate this coaching</span>
          <div className="flex items-center gap-1">
            {[1, 2, 3, 4, 5].map(n => {
              const filled = feedbackDone ? n <= selectedStar : n <= (hoveredStar || selectedStar);
              return (
                <button
                  key={n}
                  className="ddd-star"
                  onMouseEnter={() => !feedbackDone && setHoveredStar(n)}
                  onMouseLeave={() => !feedbackDone && setHoveredStar(0)}
                  onClick={() => handleStar(n)}
                  disabled={feedbackDone}
                  style={{ opacity: feedbackDone && !filled ? 0.3 : 1 }}
                >
                  <Star
                    size={18}
                    strokeWidth={1.5}
                    fill={filled ? stratColor : 'none'}
                    stroke={filled ? stratColor : '#D0D0C8'}
                  />
                </button>
              );
            })}
          </div>
          {feedbackDone && (
            <span className="text-[11px] text-gray-400">
              <Check size={12} strokeWidth={2} className="inline mr-1" />
              Thanks
            </span>
          )}
        </div>

      </div>
    </div>
  );
}

function CoachingCard({ icon, label, color, text }) {
  return (
    <div className="ddd-card px-5 py-5">
      <div className="flex items-center gap-2 mb-3">
        <span className="w-6 h-6 rounded-full flex items-center justify-center shrink-0" style={{ background: color + '14', color }}>
          {icon}
        </span>
        <span className="text-[10px] uppercase tracking-[0.18em] font-semibold" style={{ color }}>
          {label}
        </span>
      </div>
      <p className="text-sm leading-relaxed text-gray-800">{text}</p>
    </div>
  );
}

/* ---------- Onboarding Modal ---------- */

const COLOR_SEASONS = [
  {
    id: 'Spring',
    label: 'Spring',
    energy: 'warm-light',
    desc: 'You radiate warmth and freshness. Your energy is bright, approachable, and naturally inviting.',
  },
  {
    id: 'Summer',
    label: 'Summer',
    energy: 'cool-muted',
    desc: 'You carry cool elegance. Your energy is soft, refined, and thoughtfully restrained.',
  },
  {
    id: 'Autumn',
    label: 'Autumn',
    energy: 'warm-deep',
    desc: 'You carry depth and richness. Your energy is grounded, substantial, and authentic.',
  },
  {
    id: 'Winter',
    label: 'Winter',
    energy: 'cool-clear',
    desc: 'You project precision and authority. Your energy is high-contrast, commanding, and direct.',
  },
];

const HD_TYPES = [
  {
    id: 'Generator',
    label: 'Generator',
    pct: '37%',
    cue: 'You have deep, sustainable energy. You work best responding to life rather than initiating — when you say "mm-hmm" to the right things, you\'re unstoppable.',
  },
  {
    id: 'Manifesting Generator',
    label: 'Manifesting Generator',
    pct: '33%',
    cue: 'You move fast, juggle many things at once, and often skip steps others follow. You respond first, then act — and you need variety to stay alive.',
  },
  {
    id: 'Manifestor',
    label: 'Manifestor',
    pct: '9%',
    cue: 'You initiate naturally and feel frustrated when you need permission. Your impact is biggest when you inform others before you act.',
  },
  {
    id: 'Projector',
    label: 'Projector',
    pct: '20%',
    cue: 'You read people and systems with precision. You\'re here to guide — but only when invited. Without recognition, your gifts go unseen.',
  },
  {
    id: 'Reflector',
    label: 'Reflector',
    pct: '1%',
    cue: 'You mirror the health of the people around you. Deeply influenced by your environment, you need time — ideally a full lunar cycle — before big decisions.',
  },
];

function OnboardingModal({ initial, onClose, onSubmit, fontSerif }) {
  const [birthdate,    setBirthdate]    = useState(initial?.birthdate    || '');
  const [time,         setTime]         = useState(initial?.time         || '');
  const [bloodType,    setBloodType]    = useState(initial?.bloodType    || '');
  const [mbti,         setMbti]         = useState(initial?.mbti         || '');
  const [hdType,       setHdType]       = useState(initial?.hdType       || '');
  const [personalColor, setPersonalColor] = useState(initial?.personalColor || '');
  const [loading,      setLoading]      = useState(false);
  const [error,        setError]        = useState('');

  const isValid = birthdate && time && mbti.length === 4 && hdType && personalColor;

  const submit = async () => {
    if (!isValid || loading) return;
    setError('');
    setLoading(true);
    try {
      await onSubmit({ birthdate, time, bloodType, mbti: mbti.toUpperCase(), hdType, personalColor });
    } catch (e) {
      setError(e.message || 'Failed to save profile');
    } finally {
      setLoading(false);
    }
  };

  const bloodTypes = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'];

  return (
    <div
      className="ddd-modal-bg fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ background: 'rgba(20, 20, 18, 0.45)', backdropFilter: 'blur(6px)' }}
    >
      <div
        className="ddd-modal-card w-full max-w-md relative overflow-y-auto"
        style={{
          background: '#FAFAF6',
          borderRadius: '20px',
          boxShadow: '0 30px 80px -20px rgba(0,0,0,0.25), 0 1px 2px rgba(0,0,0,0.05)',
          maxHeight: '90vh',
        }}
      >
        {onClose && (
          <button
            onClick={onClose}
            className="absolute top-4 right-4 w-8 h-8 rounded-full flex items-center justify-center text-gray-400 hover:bg-gray-100 transition-colors"
          >
            <X size={16} strokeWidth={1.6} />
          </button>
        )}

        <div className="px-7 md:px-9 pt-9 pb-7">
          <div className="flex items-center gap-2 mb-4">
            <Zap size={14} strokeWidth={1.7} className="text-gray-400" />
            <span className="text-[11px] uppercase tracking-[0.18em] text-gray-500">Calibrate</span>
          </div>
          <h1 className="text-3xl md:text-4xl mb-2" style={{ fontFamily: fontSerif, fontWeight: 400, letterSpacing: '-0.01em', color: '#1B1B19' }}>
            <span style={{ fontStyle: 'italic' }}>The basics first.</span>
          </h1>
          <p className="text-sm text-gray-500 mb-7">
            Six inputs. Saved to your account — never enter them again.
          </p>

          <div className="space-y-5">
            <Field label="Birthdate">
              <input
                type="date"
                value={birthdate}
                onChange={e => setBirthdate(e.target.value)}
                className="ddd-input w-full px-3.5 py-2.5 text-sm"
              />
            </Field>

            <Field label="Time of Birth">
              <input
                type="time"
                value={time}
                onChange={e => setTime(e.target.value)}
                className="ddd-input w-full px-3.5 py-2.5 text-sm"
              />
            </Field>

            <Field label="Blood Type (optional)">
              <div className="grid grid-cols-4 gap-1.5">
                {bloodTypes.map(bt => (
                  <button
                    key={bt}
                    onClick={() => setBloodType(bloodType === bt ? '' : bt)}
                    className="py-2 text-sm rounded-md transition-all"
                    style={{
                      background: bloodType === bt ? '#1B1B19' : '#FAFAF6',
                      color: bloodType === bt ? '#FAFAF6' : '#1B1B19',
                      border: '1px solid ' + (bloodType === bt ? '#1B1B19' : 'rgba(0,0,0,0.08)'),
                      fontWeight: 500,
                    }}
                  >
                    {bt}
                  </button>
                ))}
              </div>
            </Field>

            <Field label="MBTI">
              <input
                type="text"
                value={mbti}
                onChange={e => setMbti(e.target.value.toUpperCase().slice(0, 4))}
                placeholder="e.g. INTJ"
                maxLength={4}
                className="ddd-input w-full px-3.5 py-2.5 text-sm uppercase tracking-[0.15em]"
                style={{ fontWeight: 500 }}
              />
            </Field>

            <Field label="Personal Color Season">
              <div className="grid grid-cols-2 gap-2">
                {COLOR_SEASONS.map(cs => {
                  const active = personalColor === cs.id;
                  return (
                    <button
                      key={cs.id}
                      onClick={() => setPersonalColor(cs.id)}
                      className="text-left rounded-xl px-4 py-3 transition-all"
                      style={{
                        background: active ? colorSeasonBg(cs.id) : '#FFFFFF',
                        border: '1px solid ' + (active ? colorSeasonFg(cs.id) + '40' : 'rgba(0,0,0,0.08)'),
                        boxShadow: active ? `0 0 0 1.5px ${colorSeasonFg(cs.id)}30` : '0 1px 2px rgba(0,0,0,0.03)',
                      }}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-semibold" style={{ color: active ? colorSeasonFg(cs.id) : '#1B1B19' }}>
                          {cs.label}
                        </span>
                        <span className="text-[10px] px-1.5 py-0.5 rounded-full" style={{ background: 'rgba(0,0,0,0.05)', color: '#9A9A95' }}>
                          {cs.energy}
                        </span>
                      </div>
                      <p className="text-xs leading-relaxed" style={{ color: active ? colorSeasonFg(cs.id) + 'CC' : '#9A9A95' }}>
                        {cs.desc}
                      </p>
                    </button>
                  );
                })}
              </div>
            </Field>

            <Field label="Human Design Type">
              <div className="flex flex-col gap-2">
                {HD_TYPES.map(ht => {
                  const active = hdType === ht.id;
                  return (
                    <button
                      key={ht.id}
                      onClick={() => setHdType(ht.id)}
                      className="w-full text-left rounded-xl px-4 py-3 transition-all"
                      style={{
                        background: active ? '#1B1B19' : '#FFFFFF',
                        border: '1px solid ' + (active ? '#1B1B19' : 'rgba(0,0,0,0.08)'),
                        boxShadow: active ? 'none' : '0 1px 2px rgba(0,0,0,0.03)',
                      }}
                    >
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm" style={{ fontWeight: 600, color: active ? '#FAFAF6' : '#1B1B19' }}>
                          {ht.label}
                        </span>
                        <span
                          className="text-[10px] tabular-nums px-1.5 py-0.5 rounded-full"
                          style={{
                            background: active ? 'rgba(255,255,255,0.12)' : 'rgba(0,0,0,0.05)',
                            color: active ? 'rgba(255,255,255,0.6)' : '#9A9A95',
                          }}
                        >
                          {ht.pct}
                        </span>
                      </div>
                      <p className="text-xs leading-relaxed" style={{ color: active ? 'rgba(255,255,255,0.65)' : '#9A9A95' }}>
                        {ht.cue}
                      </p>
                    </button>
                  );
                })}
              </div>
            </Field>
          </div>

          {error && <p className="mt-4 text-sm" style={{ color: '#C84B31' }}>{error}</p>}

          <button
            onClick={submit}
            disabled={!isValid || loading}
            className="mt-7 w-full flex items-center justify-center gap-2 py-3 rounded-full text-sm font-medium transition-all"
            style={{
              background: isValid && !loading ? '#1B1B19' : '#E5E5E0',
              color: isValid && !loading ? '#FAFAF6' : '#9A9A95',
              cursor: isValid && !loading ? 'pointer' : 'not-allowed',
              boxShadow: isValid && !loading ? '0 1px 2px rgba(0,0,0,0.05), 0 6px 16px -8px rgba(0,0,0,0.2)' : 'none',
            }}
          >
            {loading ? 'Saving…' : 'Continue'}
            {!loading && <ArrowRight size={14} strokeWidth={1.8} />}
          </button>
        </div>
      </div>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <div>
      <label className="block text-[11px] uppercase tracking-[0.16em] text-gray-500 mb-1.5">
        {label}
      </label>
      {children}
    </div>
  );
}
