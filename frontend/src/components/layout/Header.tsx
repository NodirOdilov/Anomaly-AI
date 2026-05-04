import { useHealth } from '../../hooks/useHealth'
import { FORCE_DEMO_MODE } from '../../utils/demoMode'
import { PROJECT_NAME } from '../../utils/constants'
import { Badge } from '../ui/Badge'

export function Header() {
  const { data, error } = useHealth()
  const ok = Boolean(data && !error)

  return (
    <header className="border-b border-slate-800 bg-slate-900/30 px-4 py-4 sm:px-6 sm:py-5 lg:px-8">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="text-lg font-semibold leading-tight text-slate-50 sm:text-xl">{PROJECT_NAME}</div>
          <div className="max-w-2xl text-[11px] leading-relaxed text-slate-400 sm:text-xs">
            Обнаружение сетевых аномалий и web-атак на базе Machine Learning
          </div>
        </div>
        <div className="flex w-full flex-wrap items-center gap-2 sm:w-auto sm:justify-end sm:gap-2.5">
          {FORCE_DEMO_MODE ? <Badge tone="info">PRODUCTION PREVIEW</Badge> : null}
          <span className="text-xs text-slate-400">Бэкенд</span>
          <Badge tone={ok ? 'good' : 'bad'}>{ok ? `OK · v${data?.version}` : 'Оффлайн / Ошибка'}</Badge>
        </div>
      </div>
    </header>
  )
}
