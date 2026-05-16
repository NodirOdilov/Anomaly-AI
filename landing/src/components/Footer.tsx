import { Link } from 'react-router-dom'
import { links } from '../lib/links'

export function Footer() {
  return (
    <footer className="border-t border-white/[0.06] px-4 py-14 sm:px-6">
      <div className="mx-auto flex max-w-6xl flex-col gap-10 md:flex-row md:items-start md:gap-12">
        <div className="md:w-[280px] md:shrink-0">
          <div className="font-display text-sm font-semibold text-white">Anomaly AI</div>
          <p className="mt-3 text-[13px] leading-6 text-slate-500">
            Платформа обнаружения сетевых аномалий и веб-атак на базе машинного обучения с фокусом на защитную практику.
          </p>
        </div>
        <div className="grid grid-cols-2 gap-10 sm:grid-cols-3 md:flex-1 md:justify-items-start">
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Продукт</div>
            <ul className="mt-3 space-y-2 text-sm text-slate-400">
              <li>
                <a className="hover:text-cyan-200" href="#modules">
                  Модули
                </a>
              </li>
              <li>
                <a className="hover:text-cyan-200" href={links.dashboard}>
                  Консоль
                </a>
              </li>
              <li>
                <a className="hover:text-cyan-200" href={links.apiHealth}>
                  Статус API
                </a>
              </li>
            </ul>
          </div>
          <div>
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Материалы</div>
            <ul className="mt-3 space-y-2 text-sm text-slate-400">
              <li>
                <Link className="hover:text-cyan-200" to="/docs">
                  Документация
                </Link>
              </li>
              <li>
                <a className="hover:text-cyan-200" href="#trust">
                  Доверие и этика
                </a>
              </li>
            </ul>
          </div>
          <div className="col-span-2 min-w-0 sm:col-span-1">
            <div className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-500">Язык интерфейса</div>
            <p className="mt-3 text-xs leading-relaxed text-slate-500">
              Маркетинговая страница и научно-технический раздел <Link className="text-cyan-400/90 hover:underline" to="/docs">/docs</Link> представлены на русском языке. Унифицированные обозначения API и ML сохраняются в общепринятом латинском написании (REST, JSON, TF‑IDF и т.д.).
            </p>
          </div>
        </div>
      </div>
      <div className="mx-auto mt-12 flex max-w-6xl flex-col items-center gap-2 text-center text-sm text-slate-500">
        <p>© {new Date().getFullYear()} Anomaly AI. Создано для инженеров, аналитиков и исследователей в области защиты.</p>
        <p>
          <a
            className="text-cyan-400/90 transition-colors hover:text-cyan-300 hover:underline"
            href="https://github.com/NodirOdilov/Anomaly-AI"
            target="_blank"
            rel="noopener noreferrer"
          >
            GitHub
          </a>
          {' · '}
          <a
            className="text-cyan-400/90 transition-colors hover:text-cyan-300 hover:underline"
            href="https://github.com/NodirOdilov"
            target="_blank"
            rel="noopener noreferrer"
          >
            Nodir Odilov
          </a>
        </p>
      </div>
    </footer>
  )
}
