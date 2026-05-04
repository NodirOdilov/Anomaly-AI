import type { InputHTMLAttributes } from 'react'

type Props = Omit<InputHTMLAttributes<HTMLInputElement>, 'type'> & { hint?: string }

export function FileUpload({ hint, className = '', ...rest }: Props) {
  return (
    <label className={`block ${className}`}>
      <span className="sr-only">Загрузить файл</span>
      <input
        type="file"
        className="block w-full text-sm leading-relaxed text-slate-200 file:mr-3 file:rounded-xl file:border-0 file:bg-slate-800 file:px-4 file:py-2.5 file:font-medium file:text-slate-100 hover:file:bg-slate-700"
        {...rest}
      />
      {hint ? <div className="mt-2.5 text-xs leading-relaxed text-slate-400">{hint}</div> : null}
    </label>
  )
}
