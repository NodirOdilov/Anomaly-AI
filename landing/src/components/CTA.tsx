import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { links } from '../lib/links'
import { fadeUp } from '../lib/motion'

export function CTA() {
  return (
    <section id="cta" className="scroll-mt-28 px-4 pb-28 pt-6 sm:px-6">
      <motion.div
        {...fadeUp}
        className="mx-auto max-w-6xl overflow-hidden rounded-3xl border border-cyan-400/20 bg-gradient-to-r from-cyan-500/15 via-slate-950 to-violet-500/15 p-10 text-center sm:p-14"
      >
        <h2 className="font-display text-3xl font-semibold tracking-tight text-white sm:text-4xl">
          Готовы к эффекту «вау» на своей машине?
        </h2>
        <p className="mx-auto mt-4 max-w-2xl text-base text-slate-300 sm:text-lg">
          Поднимите API, откройте консоль и оцените первый payload за считанные минуты. Подключайте свои данные, когда будете
          готовы — архитектура уже ждёт.
        </p>
        <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <motion.a
            href={links.dashboard}
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.98 }}
            className="inline-flex w-full items-center justify-center rounded-2xl bg-white px-8 py-3.5 text-sm font-semibold text-slate-950 shadow-[0_20px_60px_-20px_rgba(255,255,255,0.35)] sm:w-auto"
          >
            Открыть консоль
          </motion.a>
          <Link
            to="/docs"
            className="inline-flex w-full items-center justify-center rounded-2xl border border-white/15 bg-slate-950/40 px-8 py-3.5 text-sm font-semibold text-white transition hover:border-white/25 sm:w-auto"
          >
            Читать документацию
          </Link>
        </div>
        <p className="mt-6 text-xs text-slate-500">
          Продолжая, вы соглашаетесь использовать стек только в авторизованных защитных сценариях — см. файл SECURITY в
          репозитории.
        </p>
      </motion.div>
    </section>
  )
}
