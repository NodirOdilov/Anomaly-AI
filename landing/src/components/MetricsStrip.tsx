import { motion } from 'framer-motion'
import { fadeUp } from '../lib/motion'

const stats = [
  { label: 'Поверхности детектирования', value: '2', hint: 'Сеть и веб-payload’ы' },
  { label: 'Эндпоинты API', value: '8+', hint: 'Health, скоринг, отчёты' },
  { label: 'Режимы развёртывания', value: '3', hint: 'Локально · Docker · CI' },
  { label: 'Философия', value: '1', hint: 'Только защитное применение' },
] as const

export function MetricsStrip() {
  return (
    <section className="border-y border-white/[0.06] bg-slate-950/40 px-4 py-14 sm:px-6">
      <div className="mx-auto grid max-w-6xl gap-10 md:grid-cols-4">
        {stats.map((s, i) => (
          <motion.div
            key={s.label}
            initial={fadeUp.initial}
            whileInView={fadeUp.whileInView}
            viewport={fadeUp.viewport}
            transition={{ duration: 0.65, delay: i * 0.06, ease: [0.22, 1, 0.36, 1] }}
            className="text-center md:text-left"
          >
            <div className="font-display text-4xl font-semibold tracking-tight text-white">{s.value}</div>
            <div className="mt-1 text-xs font-semibold uppercase tracking-[0.2em] text-cyan-200/80">{s.label}</div>
            <div className="mt-2 text-sm text-slate-500">{s.hint}</div>
          </motion.div>
        ))}
      </div>
    </section>
  )
}
