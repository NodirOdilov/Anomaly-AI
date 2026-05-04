import { useReports } from '../../hooks/useReports'
import { Card } from '../ui/Card'
import { Loader } from '../ui/Loader'

export function ModuleStatus() {
  const { models, loading, error } = useReports()

  if (loading) return <Loader label="Загрузка статуса моделей…" />
  if (error || !models) return <Card className="p-5 text-sm text-orange-200">Не удалось загрузить статус моделей.</Card>

  return (
    <Card className="p-5">
      <div className="text-base font-semibold text-slate-100">Статус моделей</div>
      <div className="mt-4 grid gap-3.5 md:grid-cols-2">
        <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
          <div className="text-xs font-medium uppercase tracking-wide text-slate-400">WAF payload</div>
          <div className="mt-1.5 text-sm leading-relaxed text-slate-100">
            {models.waf_payload.loaded ? `Загружена · v${models.waf_payload.version}` : 'Не загружена'}
          </div>
        </div>
        <div className="rounded-xl border border-slate-800 bg-slate-950/40 p-4">
          <div className="text-xs font-medium uppercase tracking-wide text-slate-400">Сетевая аномалия</div>
          <div className="mt-1.5 text-sm leading-relaxed text-slate-100">
            {models.network_anomaly.loaded ? `Загружена · v${models.network_anomaly.version}` : 'Не загружена'}
          </div>
        </div>
      </div>
    </Card>
  )
}
