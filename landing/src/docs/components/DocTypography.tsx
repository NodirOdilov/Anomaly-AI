import type { ReactNode } from 'react'

export function DocH1({ children }: { children: ReactNode }) {
  return <h1 className="font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">{children}</h1>
}

export function DocLead({ children }: { children: ReactNode }) {
  return <p className="mt-4 text-base leading-relaxed text-slate-400 sm:text-lg">{children}</p>
}

export function DocH2({ id, children }: { id?: string; children: ReactNode }) {
  return (
    <h2
      id={id}
      className="scroll-mt-28 font-display mt-14 text-xl font-semibold tracking-tight text-white first:mt-0 sm:text-2xl"
    >
      {children}
    </h2>
  )
}

export function DocH3({ children }: { children: ReactNode }) {
  return <h3 className="mt-8 text-base font-semibold text-slate-100 sm:text-lg">{children}</h3>
}

export function DocP({ children }: { children: ReactNode }) {
  return <p className="mt-4 text-sm leading-relaxed text-slate-300 sm:text-base">{children}</p>
}

export function DocUl({ children }: { children: ReactNode }) {
  return <ul className="mt-4 list-inside list-disc space-y-2 text-sm leading-relaxed text-slate-300 sm:text-base">{children}</ul>
}

export function DocOl({ children }: { children: ReactNode }) {
  return (
    <ol className="mt-4 list-inside list-decimal space-y-2 text-sm leading-relaxed text-slate-300 sm:text-base">{children}</ol>
  )
}

export function DocLi({ children }: { children: ReactNode }) {
  return <li className="marker:text-cyan-500/80">{children}</li>
}

export function DocCode({ children }: { children: ReactNode }) {
  return (
    <code className="rounded bg-slate-900 px-1.5 py-0.5 font-mono text-[0.85em] text-cyan-200/90">{children}</code>
  )
}

export function DocPre({ children }: { children: ReactNode }) {
  return (
    <pre className="mt-4 overflow-x-auto rounded-2xl border border-white/10 bg-slate-950/80 p-4 text-xs leading-relaxed text-slate-200 sm:text-sm">
      {children}
    </pre>
  )
}

export function DocCallout({ title, children }: { title: string; children: ReactNode }) {
  return (
    <aside className="mt-6 rounded-2xl border border-cyan-400/20 bg-cyan-500/5 p-5">
      <div className="text-xs font-semibold uppercase tracking-[0.16em] text-cyan-200/90">{title}</div>
      <div className="mt-2 text-sm leading-relaxed text-slate-300">{children}</div>
    </aside>
  )
}

export function DocMath({ children }: { children: ReactNode }) {
  return (
    <div className="mt-4 rounded-2xl border border-white/10 bg-slate-900/50 px-4 py-3 font-mono text-sm text-slate-200">
      {children}
    </div>
  )
}
