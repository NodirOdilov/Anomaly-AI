import type { NetworkCsvResponse } from '../../types/network'
import { StatCard } from '../dashboard/StatCard'

export function NetworkResultSummary({ data }: { data: NetworkCsvResponse }) {
  return (
    <div className="grid gap-4 md:grid-cols-4">
      <StatCard title="Всего потоков" value={String(data.total_flows)} />
      <StatCard title="Benign" value={String(data.benign)} subtitle="Предсказано как BENIGN" />
      <StatCard title="Подозрительные" value={String(data.suspicious)} subtitle="Предсказания не BENIGN" />
      <StatCard title="Топ-метка" value={data.top_prediction} />
    </div>
  )
}
