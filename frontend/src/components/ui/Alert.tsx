import type { HTMLAttributes } from 'react'

type Variant = 'info' | 'error' | 'success'

const map: Record<Variant, string> = {
  info: 'border-sky-800 bg-sky-950/40 text-sky-100',
  error: 'border-orange-800 bg-orange-950/30 text-orange-100',
  success: 'border-emerald-800 bg-emerald-950/30 text-emerald-100',
}

export function Alert({
  variant = 'info',
  className = '',
  ...rest
}: HTMLAttributes<HTMLDivElement> & { variant?: Variant }) {
  return (
    <div className={`rounded-xl border px-4 py-3 text-sm leading-relaxed ${map[variant]} ${className}`} {...rest} />
  )
}
