import { useMemo, useState } from 'react'
import { NetworkFileUpload } from '../components/network/NetworkFileUpload'
import { NetworkPredictionTable } from '../components/network/NetworkPredictionTable'
import { NetworkResultSummary } from '../components/network/NetworkResultSummary'
import { Alert } from '../components/ui/Alert'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { EmptyState } from '../components/ui/EmptyState'
import { Loader } from '../components/ui/Loader'
import { useNetworkPrediction } from '../hooks/useNetworkPrediction'
import { isCsvFile } from '../utils/validators'

export function NetworkAnalyzerPage() {
  const [file, setFile] = useState<File | null>(null)
  const { data, loading, error, run } = useNetworkPrediction()

  const canRun = useMemo(() => isCsvFile(file), [file])

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold leading-tight text-slate-50 sm:text-3xl">Анализатор сети</h1>
        <p className="max-w-4xl text-sm leading-relaxed text-slate-300">
          Загрузите CSV с признаками потоков. В примере используются колонки <code className="text-sky-300">duration</code>,{' '}
          <code className="text-sky-300">tot_fwd_pkts</code> и опциональная колонка <code className="text-sky-300">Label</code>.
        </p>
      </div>

      <Card className="space-y-5 p-4 sm:p-5">
        <NetworkFileUpload
          onFile={(f) => {
            setFile(f)
          }}
        />
        <Button type="button" className="w-full sm:w-auto" disabled={!canRun || loading} onClick={() => file && void run(file)}>
          Анализировать CSV
        </Button>
        {loading ? <Loader label="Загрузка и оценка данных…" /> : null}
        {error ? <Alert variant="error">{error}</Alert> : null}
        {data ? (
          <div className="space-y-4">
            <NetworkResultSummary data={data} />
            <NetworkPredictionTable data={data} />
          </div>
        ) : (
          <EmptyState title="Результатов пока нет" subtitle="Выберите CSV и запустите анализ." />
        )}
      </Card>
    </div>
  )
}
