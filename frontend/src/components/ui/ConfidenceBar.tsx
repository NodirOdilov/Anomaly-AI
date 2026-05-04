import { clamp01 } from '../../utils/formatters'

export function ConfidenceBar({ value }: { value: number }) {
  const v = clamp01(value)
  return (
    <div className="w-full">
      <div className="h-2 w-full rounded-full bg-slate-800">
        <div
          className="h-2 rounded-full bg-gradient-to-r from-sky-500 to-emerald-400"
          style={{ width: `${Math.round(v * 100)}%` }}
        />
      </div>
      <div className="mt-1 text-xs text-slate-400">Уверенность: {(v * 100).toFixed(0)}%</div>
    </div>
  )
}
