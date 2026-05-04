import { motion, useScroll, useTransform } from 'framer-motion'
import { useRef } from 'react'
import { Link, NavLink } from 'react-router-dom'
import { links } from '../lib/links'

const landingItems = [
  { href: '#product', label: 'Продукт' },
  { href: '#modules', label: 'Модули' },
  { href: '#how', label: 'Как это работает' },
  { href: '#trust', label: 'Доверие' },
] as const

export function Nav({ variant = 'landing' }: { variant?: 'landing' | 'docs' }) {
  const ref = useRef<HTMLElement>(null)
  const { scrollY } = useScroll()
  const headerBg = useTransform(scrollY, [0, 100], ['rgba(2, 6, 23, 0.45)', 'rgba(2, 6, 23, 0.82)'])

  return (
    <motion.header
      ref={ref}
      style={{ backgroundColor: headerBg }}
      className="fixed top-0 z-50 w-full border-b border-white/[0.06] backdrop-blur-xl"
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-4 py-3 sm:px-6">
        <Link to="/" className="group flex items-center gap-2">
          <span className="relative flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-cyan-400/20 to-violet-500/20 ring-1 ring-white/10 transition group-hover:scale-[1.04]">
            <svg viewBox="0 0 36 36" className="h-6 w-6" aria-hidden="true">
              <defs>
                <linearGradient id="aa-icon-stroke" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#67e8f9" />
                  <stop offset="100%" stopColor="#a78bfa" />
                </linearGradient>
                <radialGradient id="aa-icon-core" cx="50%" cy="42%" r="68%">
                  <stop offset="0%" stopColor="#0e7490" stopOpacity="0.45" />
                  <stop offset="100%" stopColor="#020617" stopOpacity="0.05" />
                </radialGradient>
              </defs>
              <path
                d="M18 3.8 28.8 8v8.1c0 7.3-4.4 12.9-10.8 16.1C11.6 29 7.2 23.4 7.2 16.1V8z"
                fill="url(#aa-icon-core)"
                stroke="url(#aa-icon-stroke)"
                strokeWidth="1.35"
                strokeLinejoin="round"
              />
              <path
                d="M12.4 22.7 18 11l5.6 11.7M14.8 18.1h6.4"
                fill="none"
                stroke="url(#aa-icon-stroke)"
                strokeWidth="1.6"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              <circle cx="27.2" cy="9.1" r="1.4" fill="#22d3ee" fillOpacity="0.9" />
            </svg>
          </span>
          <span className="font-display text-sm font-semibold tracking-tight text-slate-100">
            Anomaly AI<span className="text-slate-500">.</span>
          </span>
        </Link>
        <nav className="hidden items-center gap-6 md:flex">
          {variant === 'landing'
            ? landingItems.map((i) => (
                <a
                  key={i.href}
                  href={i.href}
                  className="text-xs font-medium uppercase tracking-[0.18em] text-slate-400 transition hover:text-cyan-200"
                >
                  {i.label}
                </a>
              ))
            : null}
          <NavLink
            to="/docs"
            className={({ isActive }) =>
              `text-xs font-medium uppercase tracking-[0.18em] transition ${
                isActive ? 'text-cyan-200' : 'text-slate-400 hover:text-cyan-200'
              }`
            }
          >
            Документация
          </NavLink>
        </nav>
        <div className="flex items-center gap-2">
          <a
            href={links.apiHealth}
            target="_blank"
            rel="noreferrer"
            className="hidden rounded-full border border-white/10 bg-white/[0.03] px-3 py-1.5 text-xs font-medium text-slate-200 transition hover:border-cyan-400/30 hover:text-white sm:inline-flex"
          >
            Статус API
          </a>
          <motion.a
            href={links.dashboard}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="inline-flex items-center rounded-full bg-gradient-to-r from-cyan-400 to-sky-500 px-4 py-2 text-xs font-semibold text-slate-950 shadow-[0_0_24px_-4px_rgba(34,211,238,0.65)]"
          >
            Открыть консоль
          </motion.a>
        </div>
      </div>
    </motion.header>
  )
}
