import { NavLink, Outlet } from 'react-router-dom'
import { LayoutBg } from '../components/LayoutBg'
import { Nav } from '../components/Nav'
import { docsNav } from './nav'

export function DocsLayout() {
  return (
    <>
      <LayoutBg />
      <Nav variant="docs" />
      <div className="mx-auto flex min-h-screen max-w-7xl gap-0 px-4 pb-24 pt-24 sm:px-6 lg:gap-10">
        <aside className="sticky top-24 hidden h-[calc(100vh-6rem)] w-72 shrink-0 flex-col overflow-y-auto border-r border-white/[0.06] pr-6 lg:flex">
          <div className="text-[10px] font-semibold uppercase tracking-[0.22em] text-slate-500">Научная документация</div>
          <nav className="mt-4 flex flex-col gap-1">
            {docsNav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `rounded-xl px-3 py-2 text-sm transition ${
                    isActive
                      ? 'bg-slate-800/90 font-medium text-cyan-100 ring-1 ring-cyan-400/20'
                      : 'text-slate-400 hover:bg-slate-900/80 hover:text-slate-100'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
          <p className="mt-auto pt-8 text-[11px] leading-relaxed text-slate-600">
            Версия документа: <span className="text-slate-500">1.0.0</span> · синхронизировано с веткой MVP платформы Anomaly AI.
          </p>
        </aside>

        <div className="min-w-0 flex-1 lg:pl-2">
          <div className="mb-8 flex gap-2 overflow-x-auto pb-2 lg:hidden">
            {docsNav.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) =>
                  `shrink-0 rounded-full border px-3 py-1.5 text-xs whitespace-nowrap ${
                    isActive
                      ? 'border-cyan-400/35 bg-cyan-500/10 text-cyan-100'
                      : 'border-white/10 text-slate-400'
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </div>
          <Outlet />
        </div>
      </div>
    </>
  )
}
