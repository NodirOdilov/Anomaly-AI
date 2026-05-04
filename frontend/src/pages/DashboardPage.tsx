import { Link } from 'react-router-dom'
import { ModuleStatus } from '../components/dashboard/ModuleStatus'
import { RecentPredictions } from '../components/dashboard/RecentPredictions'
import { StatCard } from '../components/dashboard/StatCard'
import { ThreatSummary } from '../components/dashboard/ThreatSummary'
import { Button } from '../components/ui/Button'
import { Card } from '../components/ui/Card'
import { PROJECT_BLURB, PROJECT_NAME } from '../utils/constants'

export function DashboardPage() {
  return (
    <div className="space-y-6 sm:space-y-8">
      <div className="space-y-2">
        <h1 className="text-2xl font-semibold leading-tight text-slate-50 sm:text-3xl">{PROJECT_NAME}</h1>
        <p className="max-w-4xl text-sm leading-relaxed text-slate-300">{PROJECT_BLURB}</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard title="Обнаружение WAF payload" value="Активный модуль" subtitle="TF‑IDF + baseline на logistic regression" />
        <StatCard title="Обнаружение сетевых аномалий" value="Активный модуль" subtitle="Pipeline на RandomForest + scaling" />
        <StatCard title="Модели" value="Панель статуса" subtitle="Текущая загрузка и версия" />
        <StatCard title="Отчёты" value="Метрики и карточки" subtitle="Прозрачная baseline-маркировка и контроль качества" />
      </div>

      <div className="grid gap-2.5 sm:flex sm:flex-wrap sm:gap-3">
        <Link to="/waf" className="w-full sm:w-auto">
          <Button type="button" className="w-full sm:w-auto">
            Анализировать payload
          </Button>
        </Link>
        <Link to="/network" className="w-full sm:w-auto">
          <Button type="button" className="w-full sm:w-auto">
            Анализировать сетевой CSV
          </Button>
        </Link>
        <Link to="/reports" className="w-full sm:w-auto">
          <Button type="button" variant="ghost" className="w-full sm:w-auto">
            Открыть отчёты
          </Button>
        </Link>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <ThreatSummary />
        <RecentPredictions />
      </div>

      <ModuleStatus />

      <Card className="p-4 text-sm leading-relaxed text-slate-300 sm:p-5">
        Anomaly AI — защитная платформа кибербезопасности, использующая Machine Learning для обнаружения аномалий сетевого
        трафика и вредоносных web-payload, включая SQL injection, XSS, path traversal и попытки обхода WAF. В систему
        входят FastAPI backend, ML-сервисы детектирования, CLI-инструменты, деплой через Docker и React-панель для
        интерактивного анализа.
      </Card>
    </div>
  )
}
