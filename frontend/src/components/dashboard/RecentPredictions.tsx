import { Card } from '../ui/Card'
import { EmptyState } from '../ui/EmptyState'

const recentItems = [
  { module: 'WAF', summary: 'sql_injection (контрольный кейс)' },
  { module: 'Сеть', summary: 'HTTP_ATTACK на примере потока с высокой интенсивностью' },
]

export function RecentPredictions() {
  return (
    <Card className="p-5">
      <div className="text-base font-semibold text-slate-100">Последняя активность</div>
      <div className="mt-4 space-y-2.5">
        {recentItems.length ? (
          recentItems.map((d) => (
            <div key={`${d.module}-${d.summary}`} className="rounded-xl border border-slate-800 bg-slate-950/40 p-3.5">
              <div className="text-xs font-medium uppercase tracking-wide text-slate-400">{d.module}</div>
              <div className="mt-1 text-sm leading-relaxed text-slate-200">{d.summary}</div>
            </div>
          ))
        ) : (
          <EmptyState title="Пока нет недавних предсказаний" subtitle="Запустите анализ, чтобы заполнить эту панель." />
        )}
      </div>
    </Card>
  )
}
