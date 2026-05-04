import { motion } from 'framer-motion'
import { fadeUp } from '../lib/motion'

const container = {
  hidden: {},
  visible: {
    transition: { staggerChildren: 0.08, delayChildren: 0.06 },
  },
} as const

const item = {
  hidden: { opacity: 0, y: 22 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.55, ease: [0.22, 1, 0.36, 1] as const } },
} as const

const cards = [
  {
    title: 'Консоль уровня аналитика',
    body: 'Спокойный контрастный дашборд для триажа: WAF-строки, CSV потоков, карточки моделей и честные метрики.',
    span: 'md:col-span-2',
  },
  {
    title: 'Ядро на FastAPI',
    body: 'Типизированные маршруты, предсказуемые ошибки и артефакты, которые можно инспектировать — не «чёрный ящик».',
    span: '',
  },
  {
    title: 'Воспроизводимое обучение',
    body: 'Конфигурации YAML, точки входа CLI и отчёты, отделяющие контрольные baseline-линии от заявлений «как в бою».',
    span: '',
  },
  {
    title: 'Композируемые сервисы',
    body: 'Меняйте датасеты, переобучайте и выкатывайте заново без переписывания контракта API.',
    span: 'md:col-span-2',
  },
  {
    title: 'Позиция по безопасности',
    body: 'Защитная парадигма по замыслу: обучение, триаж в духе SOC и документация уровня портфолио.',
    span: 'md:col-span-3',
  },
] as const

export function Bento() {
  return (
    <section id="product" className="scroll-mt-28 px-4 py-24 sm:px-6">
      <div className="mx-auto max-w-6xl">
        <motion.div {...fadeUp} className="max-w-2xl">
          <h2 className="font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">
            Всё для серьёзного детектирования — без иллюзии «магии».
          </h2>
          <p className="mt-4 text-base leading-relaxed text-slate-400 sm:text-lg">
            Anomaly AI собран как внутренний инструмент: продуманные значения по умолчанию, чёткие границы модулей и
            интерфейс, который уважает дежурного инженера.
          </p>
        </motion.div>

        <motion.div
          className="mt-14 grid gap-4 md:grid-cols-3"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.15 }}
          variants={container}
        >
          {cards.map((c) => (
            <motion.article
              key={c.title}
              variants={item}
              className={`shimmer-border relative rounded-2xl p-6 ${c.span}`}
            >
              <h3 className="font-display text-lg font-semibold text-slate-50">{c.title}</h3>
              <p className="mt-3 text-sm leading-relaxed text-slate-400">{c.body}</p>
            </motion.article>
          ))}
        </motion.div>
      </div>
    </section>
  )
}
