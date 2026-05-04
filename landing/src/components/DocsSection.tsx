import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { fadeUp } from '../lib/motion'

export function DocsSection() {
  return (
    <section id="documentation" className="scroll-mt-28 px-4 py-16 sm:px-6">
      <motion.div {...fadeUp} className="mx-auto max-w-6xl">
        <div className="rounded-3xl border border-white/10 bg-slate-950/60 p-8 sm:p-10">
          <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between lg:gap-10">
            <div className="max-w-2xl min-w-0">
              <h2 className="font-display text-2xl font-semibold text-white sm:text-3xl">
                Документация поставляется вместе с продуктом
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-slate-400 sm:text-base">
                Архитектура, ожидания к данным, карточки моделей и примеры HTTP — рядом с кодом, потому что зрелые команды
                не прячут руководство.
              </p>
            </div>
            <div className="flex w-full min-w-0 max-w-lg flex-col gap-3 lg:shrink-0 lg:items-stretch">
              <Link
                to="/docs"
                className="inline-flex items-center justify-center rounded-2xl bg-white px-6 py-3 text-center text-sm font-semibold text-slate-950"
              >
                Открыть документацию
              </Link>
              <p className="rounded-2xl border border-white/10 bg-slate-950/40 px-4 py-3 text-left text-xs leading-relaxed text-slate-400">
                <span className="font-semibold text-slate-300">Совет:</span> полный научно-технический комплект доступен по
                маршруту <code className="mx-0.5 rounded bg-slate-900 px-1.5 py-0.5 font-mono text-[11px] text-cyan-200/95">/docs</code>.
                Дополнительно в <code className="mx-0.5 rounded bg-slate-900 px-1.5 py-0.5 font-mono text-[11px] text-cyan-200/95">landing/.env</code> можно задать{' '}
                <code className="break-all rounded bg-slate-900 px-1.5 py-0.5 font-mono text-[11px] text-cyan-200">VITE_REPO_URL</code> для ссылки на исходники на GitHub.
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </section>
  )
}
