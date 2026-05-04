import { Card } from '../ui/Card'

export function StatCard({
  title,
  value,
  subtitle,
}: {
  title: string
  value: string
  subtitle?: string
}) {
  return (
    <Card className="p-5">
      <div className="text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-400">{title}</div>
      <div className="mt-2.5 text-2xl font-semibold leading-tight text-slate-50">{value}</div>
      {subtitle ? <div className="mt-2 text-xs leading-relaxed text-slate-400">{subtitle}</div> : null}
    </Card>
  )
}
