import type { HTMLAttributes } from 'react'

export function Card({ className = '', ...rest }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={`rounded-2xl border border-slate-800/90 bg-slate-900/60 shadow-[0_10px_30px_-12px_rgba(2,6,23,0.85)] backdrop-blur-[2px] ${className}`}
      {...rest}
    />
  )
}
