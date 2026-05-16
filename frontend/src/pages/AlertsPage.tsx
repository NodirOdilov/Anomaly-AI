// Страница live-алертов: WebSocket-поток + статус подключения.

import { useAlertsStream } from '../hooks/useAlertsStream'

const SEVERITY_COLORS: Record<string, string> = {
  critical: 'bg-red-500/15 text-red-300 border-red-500/40',
  high: 'bg-orange-500/15 text-orange-300 border-orange-500/40',
  medium: 'bg-amber-500/15 text-amber-300 border-amber-500/40',
  low: 'bg-sky-500/15 text-sky-300 border-sky-500/40',
}

export function AlertsPage() {
  const { alerts, connected } = useAlertsStream()
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-[var(--aa-fg)]">Живые алерты</h1>
        <span
          className={`inline-flex items-center gap-2 rounded-full border px-3 py-1 text-xs ${
            connected
              ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300'
              : 'border-slate-500/40 bg-slate-500/10 text-slate-300'
          }`}
        >
          <span className={`h-2 w-2 rounded-full ${connected ? 'bg-emerald-400' : 'bg-slate-400'}`} />
          {connected ? 'Подключено' : 'Переподключение…'}
        </span>
      </div>

      {alerts.length === 0 ? (
        <div className="rounded-xl border border-dashed border-[var(--aa-border)] p-8 text-center text-sm text-[var(--aa-muted)]">
          Ожидание событий. Новые алерты появятся здесь автоматически.
        </div>
      ) : (
        <ul className="space-y-2">
          {alerts.map((alert, i) => (
            <li
              key={`${alert.created_at}-${i}`}
              className={`rounded-lg border p-3 text-sm ${
                SEVERITY_COLORS[alert.severity] ?? 'border-[var(--aa-border)] bg-[var(--aa-panel)]'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-medium uppercase tracking-wide">{alert.severity}</span>
                <span className="text-xs opacity-60">{new Date(alert.created_at).toLocaleString('ru-RU')}</span>
              </div>
              <div className="mt-1 text-[var(--aa-fg)]">{alert.summary}</div>
              <div className="mt-1 text-xs opacity-70">Модуль: {alert.module}</div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
