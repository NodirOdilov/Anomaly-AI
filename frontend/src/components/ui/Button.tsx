import type { ButtonHTMLAttributes } from 'react'

type Props = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: 'primary' | 'ghost'
}

export function Button({ variant = 'primary', className = '', ...rest }: Props) {
  const base =
    'inline-flex items-center justify-center rounded-xl px-4 py-2.5 text-sm font-semibold tracking-[0.01em] leading-none transition ' +
    'focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-400 ' +
    'disabled:opacity-50 disabled:pointer-events-none'
  const styles =
    variant === 'primary'
      ? 'bg-sky-500 text-slate-950 hover:bg-sky-400 shadow-[0_8px_20px_-12px_rgba(56,189,248,0.85)]'
      : 'bg-transparent text-slate-200 hover:bg-slate-800 border border-slate-700'
  return <button className={`${base} ${styles} ${className}`} {...rest} />
}
