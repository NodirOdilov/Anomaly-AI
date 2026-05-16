// Админ-страница: журнал аудита с пагинацией.

import { useEffect, useState } from 'react'
import { client } from '../api/client'

interface AuditItem {
  id: number
  user_id: number | null
  action: string
  method: string | null
  path: string | null
  status_code: number | null
  ip: string | null
  request_id: string | null
  created_at: string
}

interface AuditPage {
  items: AuditItem[]
  meta: { page: number; page_size: number; total: number; pages: number }
}

export function AdminAuditPage() {
  const [page, setPage] = useState(1)
  const [data, setData] = useState<AuditPage | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    client
      .get<AuditPage>('/api/v1/admin/audit', { params: { page, page_size: 50 } })
      .then(({ data }) => {
        if (!cancelled) setData(data)
      })
      .catch((err) => {
        if (!cancelled) setError(err instanceof Error ? err.message : 'Ошибка загрузки')
      })
    return () => {
      cancelled = true
    }
  }, [page])

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-[var(--aa-fg)]">Журнал аудита</h1>
      {error && <div className="rounded-lg border border-orange-500/40 bg-orange-500/10 p-3 text-sm text-orange-300">{error}</div>}
      <div className="overflow-x-auto rounded-xl border border-[var(--aa-border)]">
        <table className="min-w-full divide-y divide-[var(--aa-border)] text-sm">
          <thead className="bg-[var(--aa-panel)] text-left text-[var(--aa-muted)]">
            <tr>
              <th className="px-3 py-2">ID</th>
              <th className="px-3 py-2">User</th>
              <th className="px-3 py-2">Action</th>
              <th className="px-3 py-2">Status</th>
              <th className="px-3 py-2">IP</th>
              <th className="px-3 py-2">Время</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[var(--aa-border)] text-[var(--aa-fg)]">
            {(data?.items ?? []).map((item) => (
              <tr key={item.id}>
                <td className="px-3 py-2">{item.id}</td>
                <td className="px-3 py-2">{item.user_id ?? '—'}</td>
                <td className="px-3 py-2 font-mono text-xs">{item.action}</td>
                <td className="px-3 py-2">{item.status_code ?? '—'}</td>
                <td className="px-3 py-2 font-mono text-xs">{item.ip ?? '—'}</td>
                <td className="px-3 py-2 text-[var(--aa-muted)]">{new Date(item.created_at).toLocaleString('ru-RU')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {data && (
        <div className="flex items-center justify-between text-sm text-[var(--aa-muted)]">
          <span>
            Страница {data.meta.page} из {data.meta.pages} (всего {data.meta.total})
          </span>
          <div className="space-x-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="rounded-md border border-[var(--aa-border)] px-3 py-1 disabled:opacity-50"
            >
              ←
            </button>
            <button
              onClick={() => setPage((p) => p + 1)}
              disabled={data.meta.pages !== 0 && page >= data.meta.pages}
              className="rounded-md border border-[var(--aa-border)] px-3 py-1 disabled:opacity-50"
            >
              →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
