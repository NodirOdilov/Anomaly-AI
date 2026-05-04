import type { ModuleMetrics } from '../../types/reports'
import { Card } from '../ui/Card'

export function ModelCard({ title, m }: { title: string; m: ModuleMetrics }) {
  return (
    <Card className="p-5">
      <div className="text-base font-semibold text-slate-100">{title}</div>
      <div className="mt-1.5 text-xs leading-relaxed text-slate-400">{m.model}</div>
      <div className="mt-3 text-sm leading-relaxed text-slate-300">
        Назначение: защитный triage и обучение. Не заменяет production-мониторинг, валидацию и экспертную проверку.
      </div>
    </Card>
  )
}
