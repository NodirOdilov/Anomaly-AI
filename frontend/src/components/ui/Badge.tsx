import type { HTMLAttributes } from 'react'

type Tone = 'neutral' | 'good' | 'bad' | 'info'

const tones: Record<Tone, string> = {
  neutral: 'bg-slate-800 text-slate-200 border-slate-700',
  good: 'bg-emerald-950 text-emerald-200 border-emerald-800',
  bad: 'bg-orange-950 text-orange-200 border-orange-800',
  info: 'bg-sky-950 text-sky-200 border-sky-800',
}

export function Badge({
  tone = 'neutral',
  className = '',
  ...rest
}: HTMLAttributes<HTMLSpanElement> & { tone?: Tone }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-1 text-[11px] font-semibold tracking-[0.06em] ${tones[tone]} ${className}`}
      {...rest}
    />
  )
}
