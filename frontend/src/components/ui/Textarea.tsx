import type { TextareaHTMLAttributes } from 'react'

export function Textarea({ className = '', ...rest }: TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return (
    <textarea
      className={`w-full min-h-44 rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm leading-relaxed text-slate-100 placeholder:text-slate-500 focus:border-sky-500 focus:outline-none ${className}`}
      {...rest}
    />
  )
}
