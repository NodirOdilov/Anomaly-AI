import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Панель' },
  { to: '/waf', label: 'WAF-анализатор' },
  { to: '/network', label: 'Анализатор сети' },
  { to: '/reports', label: 'Отчёты' },
  { to: '/docs', label: 'Документация' },
] as const

export function Sidebar() {
  return (
    <aside className="hidden w-64 shrink-0 border-r border-slate-800 bg-slate-900/40 lg:w-72 md:block">
      <div className="px-5 py-7">
        <div className="px-2 text-[11px] font-semibold uppercase tracking-[0.16em] text-slate-500">Навигация</div>
        <nav className="mt-4 space-y-1.5">
          {links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.to === '/'}
              className={({ isActive }) =>
                `block rounded-xl px-3.5 py-2.5 text-sm font-medium leading-relaxed ${
                  isActive ? 'bg-slate-800 text-sky-200' : 'text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              {l.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </aside>
  )
}
