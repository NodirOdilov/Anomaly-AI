import type { ModuleMetrics } from '../../types/reports'

export function MetricsTable({ title, m }: { title: string; m: ModuleMetrics }) {
  const rows: Array<[string, string]> = [
    ['Точность (Accuracy)', m.accuracy.toFixed(3)],
    ['Precision', m.precision.toFixed(3)],
    ['Recall', m.recall.toFixed(3)],
    ['F1', m.f1.toFixed(3)],
    ['Доля False Positive', m.false_positive_rate.toFixed(3)],
    ['Доля False Negative', m.false_negative_rate.toFixed(3)],
  ]
  return (
    <div className="overflow-hidden rounded-2xl border border-slate-800">
      <div className="bg-slate-900/70 px-4 py-3 text-sm font-semibold tracking-wide text-slate-100">{title}</div>
      <table className="min-w-full text-sm">
        <tbody>
          {rows.map(([k, v]) => (
            <tr key={k} className="border-t border-slate-800">
              <td className="px-4 py-2.5 leading-relaxed text-slate-400">{k}</td>
              <td className="px-4 py-2.5 font-medium text-slate-100">{v}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {m.notes ? <div className="border-t border-slate-800 px-4 py-3 text-xs leading-relaxed text-slate-400">{m.notes}</div> : null}
    </div>
  )
}
