export function isNonEmpty(s: string): boolean {
  return s.trim().length > 0
}

export function isCsvFile(f: File | null): boolean {
  if (!f) return false
  return f.name.toLowerCase().endsWith('.csv')
}
