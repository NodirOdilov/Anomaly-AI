export function EmptyState({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-slate-800 bg-slate-950/40 p-10 text-center">
      <div className="text-base font-semibold text-slate-200">{title}</div>
      {subtitle ? <div className="mt-3 text-sm leading-relaxed text-slate-400">{subtitle}</div> : null}
    </div>
  )
}
