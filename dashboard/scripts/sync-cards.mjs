// Syncs card data + deck art from the repo root into the app's public/ folder
// so Vite serves them at /cards.json and /neuro/*. Runs automatically before
// `npm run dev` and `npm run build` (see predev/prebuild in package.json).
import { existsSync, mkdirSync, copyFileSync, readdirSync, statSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const dashboard = resolve(here, '..')
const repoRoot = resolve(dashboard, '..')
const publicDir = join(dashboard, 'public')

function copyIfPresent(from, to) {
  if (!existsSync(from)) { console.warn(`[sync-cards] skip (missing): ${from}`); return false }
  mkdirSync(dirname(to), { recursive: true })
  copyFileSync(from, to)
  return true
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
  let n = 0
  for (const f of readdirSync(srcDir)) {
    if (!/\.(png|jpe?g|webp|svg)$/i.test(f)) continue
    if (!statSync(join(srcDir, f)).isFile()) continue
    copyFileSync(join(srcDir, f), join(destDir, f))
    n++
  }
  console.log(`[sync-cards] ${deck}/ → public/${deck.toLowerCase()}/ (${n} images)`)
}
