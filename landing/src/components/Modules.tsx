import { motion } from 'framer-motion'
import { fadeUp } from '../lib/motion'

export function Modules() {
  return (
    <section id="modules" className="scroll-mt-28 px-4 py-24 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <motion.div {...fadeUp} className="max-w-2xl">
          <h2 className="font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Два движка. Одна линия повествования.
          </h2>
          <p className="mt-4 text-base leading-relaxed text-slate-400 sm:text-lg">
            Payload’ы и сетевые потоки принципиально различаются — поэтому для них используются разные конвейеры,
            согласованные с «геометрией» данных.
          </p>
        </motion.div>

        <div className="mt-14 grid gap-6 lg:grid-cols-2">
          <motion.div
            {...fadeUp}
            className="relative overflow-hidden rounded-3xl border border-cyan-400/15 bg-gradient-to-br from-cyan-500/10 via-slate-950 to-slate-950 p-8"
          >
            <div className="absolute -right-10 -top-10 h-40 w-40 rounded-full bg-cyan-400/20 blur-3xl" />
            <div className="relative">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200/80">Модуль A</div>
              <h3 className="font-display mt-3 text-2xl font-semibold text-white">Анализ WAF-payload’ов</h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-300">
                Символьные n-граммы улавливают синтаксис атак с большим числом разделителей. Линейная модель сохраняет
                интерпретируемость инференса; консервативные правила снимают неоднозначность в пограничных случаях —{' '}
                <strong>только для классификации</strong>, без исполнения кода.
              </p>
              <ul className="mt-6 space-y-2 text-sm text-slate-400">
                <li className="flex gap-2">
                  <span className="text-cyan-300">↳</span> SQLi · XSS · обход каталога · командные паттерны
                </li>
                <li className="flex gap-2">
                  <span className="text-cyan-300">↳</span> Пакетный скоринг для конвейеров журналов
                </li>
              </ul>
            </div>
          </motion.div>

          <motion.div
            initial={fadeUp.initial}
            whileInView={fadeUp.whileInView}
            viewport={fadeUp.viewport}
            transition={{ duration: 0.65, delay: 0.08, ease: [0.22, 1, 0.36, 1] }}
            className="relative overflow-hidden rounded-3xl border border-violet-400/15 bg-gradient-to-br from-violet-500/10 via-slate-950 to-slate-950 p-8"
          >
            <div className="absolute -left-10 -bottom-10 h-40 w-40 rounded-full bg-violet-400/20 blur-3xl" />
            <div className="relative">
              <div className="text-xs font-semibold uppercase tracking-[0.2em] text-violet-200/80">Модуль B</div>
              <h3 className="font-display mt-3 text-2xl font-semibold text-white">Скоринг сетевых аномалий</h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-300">
                Сначала гигиена чисел: NaN/inf, фиксированный порядок признаков, затем ансамбль деревьев для структурированных
                потоков — всё экспортируется как версионируемый артефакт, как и код.
              </p>
              <ul className="mt-6 space-y-2 text-sm text-slate-400">
                <li className="flex gap-2">
                  <span className="text-violet-300">↳</span> Загрузка CSV для пакетного триажа
                </li>
                <li className="flex gap-2">
                  <span className="text-violet-300">↳</span> JSON-признаки для интеграций
                </li>
              </ul>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
