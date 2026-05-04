import { useMemo, useState } from 'react'
import { PayloadExamples } from '../components/waf/PayloadExamples'
import { PayloadInput } from '../components/waf/PayloadInput'
import { PayloadResult } from '../components/waf/PayloadResult'
import { Alert } from '../components/ui/Alert'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { Loader } from '../components/ui/Loader'
import { useWafPrediction } from '../hooks/useWafPrediction'
import { isNonEmpty } from '../utils/validators'

export function WafAnalyzerPage() {
  const [payload, setPayload] = useState("id=1' OR '1'='1")
  const { data, loading, error, run } = useWafPrediction()

  const canRun = useMemo(() => isNonEmpty(payload), [payload])

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold leading-tight text-slate-50 sm:text-3xl">WAF-анализатор</h1>
        <p className="max-w-4xl text-sm leading-relaxed text-slate-300">
          Классифицируйте payload для защитного мониторинга. Результат включает предполагаемый тип атаки и confidence score.
        </p>
      </div>

      <Card className="space-y-5 p-4 sm:p-5">
        <PayloadInput value={payload} onChange={setPayload} />
        <div>
          <div className="mb-2 text-sm font-semibold tracking-wide text-slate-200">Примеры</div>
          <PayloadExamples onPick={setPayload} />
        </div>
        <div className="grid gap-2.5 sm:flex sm:flex-wrap sm:gap-3">
          <Button type="button" className="w-full sm:w-auto" disabled={!canRun || loading} onClick={() => void run(payload)}>
            Анализировать
          </Button>
        </div>
        {loading ? <Loader label="Выполняется оценка payload…" /> : null}
        {error ? <Alert variant="error">{error}</Alert> : null}
        {data ? <PayloadResult result={data} /> : null}
      </Card>
    </div>
  )
}
