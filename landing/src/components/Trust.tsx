import { motion } from 'framer-motion'
import { fadeUp } from '../lib/motion'

export function Trust() {
  return (
    <section id="trust" className="scroll-mt-28 px-4 py-24 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <motion.div
          {...fadeUp}
          className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-slate-900/80 via-slate-950 to-slate-950 p-10 sm:p-14"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(34,211,238,0.12),transparent_45%)]" />
          <div className="relative grid gap-10 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
            <div>
              <h2 className="font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">
                Честный ML — это не обещание, а принцип работы.
              </h2>
              <p className="mt-4 text-base leading-relaxed text-slate-300 sm:text-lg">
                Мы не заявляем 99,9% точности на искусственных примерах. После установки система начинает с прозрачной
                базовой линии и показывает реальные метрики только после обучения на ваших авторизованных данных. Так
                доверие строится на фактах, а не на маркетинговых цифрах.
              </p>
              <div className="mt-8 flex flex-wrap gap-3">
                <span className="rounded-full border border-emerald-400/20 bg-emerald-400/5 px-3 py-1 text-xs font-medium text-emerald-200">
                  Только защитный контур
                </span>
                <span className="rounded-full border border-cyan-400/20 bg-cyan-400/5 px-3 py-1 text-xs font-medium text-cyan-200">
                  Метаданные артефактов
                </span>
                <span className="rounded-full border border-violet-400/20 bg-violet-400/5 px-3 py-1 text-xs font-medium text-violet-200">
                  Тесты и CI
                </span>
              </div>
            </div>
            <div className="rounded-2xl border border-white/10 bg-slate-950/70 p-6 backdrop-blur">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500">Обязательства перед пользователем</div>
              <ul className="mt-4 space-y-4 text-sm text-slate-300">
                <li className="flex gap-3">
                  <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-cyan-400" />
                  Ясные границы: детектирование и триаж — не инструментарий атаки.
                </li>
                <li className="flex gap-3">
                  <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-violet-400" />
                  Документация, которую уважают инженеры: примеры API, данные, развёртывание, дорожная карта.
                </li>
                <li className="flex gap-3">
                  <span className="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-emerald-400" />
                  Интерфейс уровня «дорогого продукта» — потому что первое впечатление влияет на внедрение.
                </li>
              </ul>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
