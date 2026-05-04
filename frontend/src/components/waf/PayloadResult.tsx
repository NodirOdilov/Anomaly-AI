import type { WafPredictResult } from '../../types/waf'
import { ConfidenceBar } from '../ui/ConfidenceBar'
import { JsonViewer } from '../ui/JsonViewer'
import { AttackTypeBadge } from './AttackTypeBadge'

export function PayloadResult({ result }: { result: WafPredictResult }) {
  return (
    <div className="space-y-5">
      <div className="flex flex-wrap items-center gap-2.5">
        <AttackTypeBadge type={result.attack_type} />
        <span className="text-sm leading-relaxed text-slate-300">Уровень severity: {result.severity}</span>
      </div>
      <ConfidenceBar value={result.confidence} />
      {result.recommendation ? (
        <div className="text-sm leading-relaxed text-slate-200">
          <span className="text-slate-400">Рекомендация: </span>
          {result.recommendation}
        </div>
      ) : null}
      <div>
        <div className="mb-2 text-sm font-semibold tracking-wide text-slate-200">Сырой JSON</div>
        <JsonViewer value={result} />
      </div>
    </div>
  )
}
