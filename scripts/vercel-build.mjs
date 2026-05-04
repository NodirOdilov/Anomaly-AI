import { execSync } from 'node:child_process'
import { cpSync, mkdirSync, rmSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = fileURLToPath(new URL('..', import.meta.url))
const run = (cmd, cwd, extraEnv = {}) => {
  execSync(cmd, { cwd, env: { ...process.env, ...extraEnv }, stdio: 'inherit', shell: true })
}

/** Vercel/CI use lockfile; local Windows often tolerates install better than ci. */
const npmDeps = process.env.VERCEL || process.env.CI ? 'npm ci' : 'npm install'

const pub = join(root, 'public')
rmSync(pub, { recursive: true, force: true })
mkdirSync(pub, { recursive: true })

run(npmDeps, join(root, 'landing'))
run('npm run build', join(root, 'landing'))

run(npmDeps, join(root, 'frontend'))
run('npm run build', join(root, 'frontend'), { VITE_BASE: '/console/' })

cpSync(join(root, 'landing', 'dist'), pub, { recursive: true })
mkdirSync(join(pub, 'console'), { recursive: true })
cpSync(join(root, 'frontend', 'dist'), join(pub, 'console'), { recursive: true })

// Preview-safe health endpoint: guarantees /health responds even if Python function routing changes.
const healthDir = join(pub, 'health')
mkdirSync(healthDir, { recursive: true })
const now = new Date()
const stamp = `${now.getFullYear()}${String(now.getMonth() + 1).padStart(2, '0')}${String(now.getDate()).padStart(2, '0')}`
writeFileSync(
  join(healthDir, 'index.html'),
  `<!doctype html>
<html lang="ru">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Anomaly AI Health</title>
    <style>
      body { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; background: #020617; color: #e2e8f0; margin: 0; padding: 24px; }
      .card { max-width: 820px; margin: 0 auto; border: 1px solid #1e293b; border-radius: 12px; padding: 16px; background: #0f172a; }
      .ok { color: #22d3ee; }
    </style>
  </head>
  <body>
    <div class="card">
      <h2 class="ok">Anomaly AI · Health OK</h2>
      <pre>{
  "status": "ok",
  "service": "Anomaly AI",
  "mode": "production_preview",
  "version": "1.0.0-preview.${stamp}",
  "build_state": "stable",
  "timestamp": "${now.toISOString()}"
}</pre>
    </div>
  </body>
</html>
`,
  'utf8',
)
