import type { ReportsSummaryResponse } from '../../types/reports'
import { Alert } from '../ui/Alert'
import { MetricsTable } from './MetricsTable'
import { ModelCard } from './ModelCard'

export function ReportViewer({ summary }: { summary: ReportsSummaryResponse }) {
  const baselineOnly =
    summary.network_anomaly.accuracy === 0 &&
    summary.network_anomaly.precision === 0 &&
    summary.waf_payload.accuracy === 0 &&
    summary.waf_payload.precision === 0

  return (
    <div className="space-y-5">
      {baselineOnly ? (
        <Alert variant="info">
          Метрики остаются нулевыми/заглушечными, пока вы не обучите модели на своей машине. Это штатный baseline-режим
          до получения обученных артефактов.
        </Alert>
      ) : null}
      <div className="grid gap-5 lg:grid-cols-2">
        <MetricsTable title="Сетевая аномалия" m={summary.network_anomaly} />
        <MetricsTable title="WAF payload" m={summary.waf_payload} />
      </div>
      <div className="grid gap-5 lg:grid-cols-2">
        <ModelCard title="Карточка сетевой модели" m={summary.network_anomaly} />
        <ModelCard title="Карточка WAF-модели" m={summary.waf_payload} />
      </div>
    </div>
  )
}
