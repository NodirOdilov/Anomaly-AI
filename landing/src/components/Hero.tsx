import { useState } from 'react'
import { motion, useMotionValue, useSpring, useTransform } from 'framer-motion'
import { links } from '../lib/links'

export function Hero() {
  const [cardActive, setCardActive] = useState(false)
  const pointerX = useMotionValue(0)
  const pointerY = useMotionValue(0)

  const springX = useSpring(pointerX, { stiffness: 340, damping: 22, mass: 0.34 })
  const springY = useSpring(pointerY, { stiffness: 340, damping: 22, mass: 0.34 })

  const rotateY = useTransform(springX, [-88, 88], [-24, 4])
  const rotateX = useTransform(springY, [-46, 46], [12, -4])
  const glowX = useTransform(springX, (v) => v * 0.65)
  const glowY = useTransform(springY, (v) => v * 0.65)

  const handleCardMove: React.MouseEventHandler<HTMLDivElement> = (e) => {
    const rect = e.currentTarget.getBoundingClientRect()
    const nx = ((e.clientX - rect.left) / rect.width - 0.5) * 2
    const ny = ((e.clientY - rect.top) / rect.height - 0.5) * 2
    pointerX.set(nx * 68 - 26)
    pointerY.set(ny * 42)
  }

  const resetCard = () => {
    setCardActive(false)
    pointerX.set(0)
    pointerY.set(0)
  }

  return (
    <section className="relative px-4 pb-24 pt-28 sm:px-6 sm:pb-32 sm:pt-32">
      <div className="mx-auto max-w-6xl">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
          className="inline-flex items-center gap-2 rounded-full border border-cyan-400/20 bg-cyan-400/5 px-3 py-1 text-[11px] font-medium uppercase tracking-[0.22em] text-cyan-200/90"
        >
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-cyan-400 opacity-40" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-cyan-400" />
          </span>
          Силная кибербезопасность · ML-детектирование
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 22 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.75, delay: 0.05, ease: [0.22, 1, 0.36, 1] }}
          className="font-display mt-7 max-w-4xl text-[2.35rem] font-semibold leading-[1.05] tracking-tight text-slate-50 sm:text-5xl lg:text-6xl"
        >
          Увидеть сигнал в шуме.{' '}
          <span className="mt-1 block bg-gradient-to-r from-cyan-300 via-sky-200 to-violet-300 bg-clip-text text-transparent sm:mt-2 sm:whitespace-nowrap">
            Пока это не стало инцидентом.
          </span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 22 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.75, delay: 0.12, ease: [0.22, 1, 0.36, 1] }}
          className="mt-6 max-w-2xl text-base leading-relaxed text-slate-400 sm:text-lg"
        >
          Anomaly AI — современная защитная платформа: классические ML-базовые модели, API, готовый к продакшену подход,
          продуманная консоль аналитика. Классифицируйте подозрительные веб-payload’ы и оценивайте сетевые потоки — с
          артефактами, метриками и честностью по умолчанию.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 22 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.75, delay: 0.18, ease: [0.22, 1, 0.36, 1] }}
          className="mt-10 flex flex-col gap-3 sm:flex-row sm:items-center"
        >
          <motion.a
            href={links.dashboard}
            whileHover={{ scale: 1.02, y: -1 }}
            whileTap={{ scale: 0.98 }}
            className="inline-flex items-center justify-center rounded-2xl bg-gradient-to-r from-cyan-400 to-sky-500 px-7 py-3.5 text-sm font-semibold text-slate-950 shadow-[0_20px_50px_-18px_rgba(34,211,238,0.55)]"
          >
            Открыть консоль
          </motion.a>
          <a
            href="#product"
            className="inline-flex items-center justify-center rounded-2xl border border-white/10 bg-white/[0.03] px-7 py-3.5 text-sm font-semibold text-slate-100 transition hover:border-cyan-400/25 hover:bg-white/[0.06]"
          >
            Узнать о продукте
          </a>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.45, duration: 0.8 }}
          className="mt-16 grid gap-4 sm:grid-cols-3"
        >
          {[
            { k: 'UX для дежурства', v: 'Создано для аналитиков SOC, а не только для слайдов.' },
            { k: 'ML с артефактами', v: 'Модели поставляются с метаданными и воспроизводимостью.' },
            { k: 'Готово к Docker', v: 'Compose для пилотного контура и быстрых инженерных итераций.' },
          ].map((x) => (
            <div
              key={x.k}
              className="shimmer-border relative overflow-hidden rounded-2xl p-5"
            >
              <div className="font-display text-sm font-semibold text-slate-100">{x.k}</div>
              <div className="mt-2 text-sm leading-relaxed text-slate-400">{x.v}</div>
            </div>
          ))}
        </motion.div>
      </div>

      <motion.div
        aria-hidden
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.35, duration: 0.9, ease: [0.22, 1, 0.36, 1] }}
        className="absolute -right-6 top-28 hidden w-[420px] xl:block"
        style={{ perspective: 1200 }}
        onMouseEnter={() => {
          setCardActive(true)
          pointerX.set(-36)
          pointerY.set(0)
        }}
        onMouseMove={handleCardMove}
        onMouseLeave={resetCard}
      >
        <motion.div
          className="pointer-events-none absolute -inset-10 rounded-full bg-cyan-400/20 blur-3xl"
          style={{
            x: glowX,
            y: glowY,
            opacity: cardActive ? 1 : 0.26,
          }}
        />
        <motion.div
          className="transform-gpu rounded-2xl border border-white/10 bg-slate-950/80 p-4 shadow-[0_40px_120px_-40px_rgba(34,211,238,0.35)] ring-1 ring-cyan-400/10 backdrop-blur-md"
          animate={{ scale: cardActive ? 1.1 : 1 }}
          transition={{ type: 'spring', stiffness: 360, damping: 18, mass: 0.3 }}
          style={{ x: springX, y: springY, rotateY, rotateX }}
        >
          <div className="flex items-center justify-between text-[10px] uppercase tracking-widest text-slate-500">
            <span>Оценка в реальном времени</span>
            <span className="text-emerald-400/90">● защищённый режим</span>
          </div>
          <div className="mt-3 space-y-2 rounded-xl bg-slate-900/80 p-3 font-mono text-[11px] leading-relaxed text-slate-300">
            <div>
              <span className="text-violet-300">POST</span> <span className="text-slate-500">/api/v1/waf/predict</span>
            </div>
            <div className="text-slate-500">{'{'} &quot;payload&quot;: &quot;…&quot; {'}'}</div>
            <div className="border-t border-white/5 pt-2 text-cyan-200/90">
              → sql_injection · высокая уверенность · блок + журнал
            </div>
          </div>
        </motion.div>
      </motion.div>
    </section>
  )
}
