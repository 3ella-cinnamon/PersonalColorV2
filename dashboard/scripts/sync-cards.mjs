// Syncs card data + deck art from the repo root into the app's public/ folder
// so Vite serves them at /cards.json and /neuro/*. Runs automatically before
// `npm run dev` and `npm run build` (see predev/prebuild in package.json).
//
// Full-resolution masters live in <repoRoot>/Neuro (~2 MB each). We never ship
// those: sharp downscales each to a small WebP (max 520px wide) written into
// public/neuro/, which is what the app actually loads. The public/ copies are
// gitignored and regenerated on every dev run / build.
import { existsSync, mkdirSync, copyFileSync, readdirSync, statSync } from 'node:fs'
import { dirname, join, resolve, parse } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const dashboard = resolve(here, '..')
const repoRoot = resolve(dashboard, '..')
const publicDir = join(dashboard, 'public')

const MAX_WIDTH = 520      // display size is ~200-400px; 520 covers retina
const WEBP_QUALITY = 80

// sharp is optional: if it can't load, fall back to copying masters as-is so a
// build never hard-fails on the image step.
let sharp = null
try { sharp = (await import('sharp')).default }
catch { console.warn('[sync-cards] sharp unavailable — copying images without downscaling') }

function copyIfPresent(from, to) {
  if (!existsSync(from)) { console.warn(`[sync-cards] skip (missing): ${from}`); return false }
  mkdirSync(dirname(to), { recursive: true })
  copyFileSync(from, to)
  return true
}

// true when `out` already exists and is at least as new as `src` (skip rework)
function upToDate(src, out) {
  return existsSync(out) && statSync(out).mtimeMs >= statSync(src).mtimeMs
}

// 1) card data
if (copyIfPresent(join(repoRoot, 'cards.json'), join(publicDir, 'cards.json')))
  console.log('[sync-cards] cards.json → public/cards.json')

// 2) deck art folders (Neuro now; add more as they arrive)
for (const deck of ['Neuro']) {
  const srcDir = join(repoRoot, deck)
  if (!existsSync(srcDir)) { console.warn(`[sync-cards] skip art (missing): ${srcDir}`); continue }
  const destDir = join(publicDir, deck.toLowerCase())
  mkdirSync(destDir, { recursive: true })

  let made = 0, skipped = 0
  for (const f of readdirSync(srcDir)) {
    const src = join(srcDir, f)
    if (!/\.(png|jpe?g|webp)$/i.test(f) || !statSync(src).isFile()) continue

    if (sharp) {
      const out = join(destDir, parse(f).name + '.webp')
      if (upToDate(src, out)) { skipped++; continue }
      await sharp(src).resize({ width: MAX_WIDTH, withoutEnlargement: true })
        .webp({ quality: WEBP_QUALITY }).toFile(out)
      made++
    } else {
      const out = join(destDir, f)
      if (upToDate(src, out)) { skipped++; continue }
      copyFileSync(src, out); made++
    }
  }
  console.log(`[sync-cards] ${deck}/ → public/${deck.toLowerCase()}/ (${made} written, ${skipped} up-to-date)`)
}
