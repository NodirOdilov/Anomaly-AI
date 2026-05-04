const raw = (import.meta.env.VITE_FORCE_DEMO_MODE as string | undefined)?.trim().toLowerCase()

// Demo-first UX: enabled by default unless explicitly disabled with VITE_FORCE_DEMO_MODE=false.
export const FORCE_DEMO_MODE = raw !== 'false'

export function demoDelay(minMs = 180, maxMs = 520): Promise<void> {
  const ms = Math.floor(Math.random() * (maxMs - minMs + 1)) + minMs
  return new Promise((resolve) => window.setTimeout(resolve, ms))
}
