export function pct(n: number, digits = 0): string {
  return `${(n * 100).toFixed(digits)}%`
}

export function clamp01(n: number): number {
  return Math.min(1, Math.max(0, n))
}
