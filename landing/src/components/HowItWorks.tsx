import { motion } from 'framer-motion'
import { fadeUp } from '../lib/motion'

const steps = [
  {
    n: '01',
    t: 'Приём данных',
    d: 'Payload’ы через JSON или CSV потоков — UTF-8, проверка схемы и понятные сообщения об ошибках валидации.',
  },
  {
    n: '02',
    t: 'Скоринг',
    d: 'Конвейеры sklearn преобразуют вход так же, как при обучении, и выдают вероятности и метки.',
  },
  {
    n: '03',
    t: 'Объяснение',
    d: 'Уровень серьёзности, рекомендации и метаданные версии модели — для аудируемых процессов.',
  },
  {
    n: '04',
    t: 'Итерации',
    d: 'Переобучение из YAML, обновление артефактов и CI, подтверждающий работоспособность стека.',
  },
] as const

export function HowItWorks() {
  return (
    <section id="how" className="scroll-mt-28 px-4 py-24 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <motion.div {...fadeUp} className="max-w-2xl">
          <h2 className="font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">Как это работает</h2>
          <p className="mt-4 text-base leading-relaxed text-slate-400 sm:text-lg">
            Прямая линия от сырых сигналов к решениям — без театра и без непрозрачных «коробок».
          </p>
        </motion.div>

        <div className="mt-14 grid gap-5 md:grid-cols-2">
          {steps.map((s, i) => (
            <motion.div
              key={s.n}
              initial={fadeUp.initial}
              whileInView={fadeUp.whileInView}
              viewport={fadeUp.viewport}
              transition={{ duration: 0.65, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }}
              className="group relative overflow-hidden rounded-2xl border border-white/[0.07] bg-slate-950/50 p-6 transition hover:border-cyan-400/20"
            >
              <div className="font-display text-3xl font-semibold text-white/10 transition group-hover:text-cyan-300/40">
                {s.n}
              </div>
              <h3 className="font-display mt-2 text-xl font-semibold text-white">{s.t}</h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-400">{s.d}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  )
}
