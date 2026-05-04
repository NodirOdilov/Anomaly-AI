import type { NetworkCsvResponse } from '../../types/network'

export function NetworkPredictionTable({ data }: { data: NetworkCsvResponse }) {
  return (
    <div className="overflow-auto rounded-2xl border border-slate-800">
      <table className="min-w-[560px] text-left text-xs sm:min-w-full sm:text-sm">
        <thead className="bg-slate-900/80 text-xs uppercase tracking-wide text-slate-400">
          <tr>
            <th className="px-4 py-3">Строка</th>
            <th className="px-4 py-3">Предсказание</th>
            <th className="px-4 py-3">Уверенность</th>
          </tr>
        </thead>
        <tbody>
          {data.results.map((r) => (
            <tr key={r.row} className="border-t border-slate-800 hover:bg-slate-900/35">
              <td className="px-4 py-2.5 text-slate-300">{r.row}</td>
              <td className="px-4 py-2.5 font-medium text-slate-100">{r.prediction}</td>
              <td className="px-4 py-2.5 text-slate-300">{(r.confidence * 100).toFixed(0)}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
