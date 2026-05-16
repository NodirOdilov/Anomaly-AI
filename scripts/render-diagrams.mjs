#!/usr/bin/env node
/**
 * Render all Mermaid diagrams under docs/diagrams/*.mmd to SVG (+ PNG overview/full).
 * Usage: node scripts/render-diagrams.mjs
 */
import { execSync } from 'node:child_process'
import { readdirSync } from 'node:fs'
import { join, basename } from 'node:path'

const root = join(import.meta.dirname, '..')
const diagramsDir = join(root, 'docs', 'diagrams')
const config = join(diagramsDir, 'mermaid-config.json')
const bg = '#0d1117'
const mmdc = 'npx -y @mermaid-js/mermaid-cli@11.4.0'

const files = readdirSync(diagramsDir).filter((f) => f.endsWith('.mmd'))

for (const file of files) {
  const name = basename(file, '.mmd')
  const input = join(diagramsDir, file)
  const svg = join(diagramsDir, `${name}.svg`)
  const base = `${mmdc} -c "${config}" -i "${input}" -o "${svg}" -b "${bg}"`
  console.log(`→ ${name}.svg`)
  execSync(base, { stdio: 'inherit', cwd: root })

  if (name.startsWith('architecture-')) {
    const png = join(diagramsDir, `${name}.png`)
    const w = name === 'architecture-overview' ? 1400 : 1200
    console.log(`→ ${name}.png`)
    execSync(`${base.replace(svg, png)} -w ${w} -s 2`, { stdio: 'inherit', cwd: root })
  }
}

console.log('Done. Diagrams in docs/diagrams/')
