import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts'
import { ReportViewer } from '../components/reports/ReportViewer'
import { Alert } from '../components/ui/Alert'
import { Loader } from '../components/ui/Loader'
import { useReports } from '../hooks/useReports'

export function ReportsPage() {
  const { summary, loading, error } = useReports()

  if (loading) return <Loader label="Загрузка отчётов…" />
  if (error || !summary) return <Alert variant="error">{error ?? 'Не удалось загрузить данные'}</Alert>

  const chartData = [
    { name: 'Сеть acc', v: summary.network_anomaly.accuracy },
    { name: 'Сеть F1', v: summary.network_anomaly.f1 },
    { name: 'WAF acc', v: summary.waf_payload.accuracy },
    { name: 'WAF F1', v: summary.waf_payload.f1 },
  ]

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold leading-tight text-slate-50 sm:text-3xl">Отчёты</h1>
        <p className="max-w-4xl text-sm leading-relaxed text-slate-300">
          Метрики читаются из обученных артефактов, если они доступны. Нули означают, что оценённой модели на диске пока нет.
        </p>
      </div>

      <Alert variant="info">
        Контрольный baseline: на маленьких выборках метрики могут быть нестабильными или излишне оптимистичными —
        подтверждайте качество на реальных авторизованных данных перед production-использованием.
      </Alert>

      <div className="h-64 rounded-2xl border border-slate-800 bg-slate-900/40 p-3 sm:h-72 sm:p-4">
        <div className="mb-3 text-sm font-semibold tracking-wide text-slate-200">Снимок метрик</div>
        <ResponsiveContainer width="100%" height="85%">
          <BarChart data={chartData}>
            <XAxis dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} />
            <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} domain={[0, 1]} />
            <Tooltip contentStyle={{ background: '#0f172a', border: '1px solid #1e293b' }} />
            <Bar dataKey="v" fill="#38bdf8" radius={[6, 6, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <ReportViewer summary={summary} />
    </div>
  )
}
