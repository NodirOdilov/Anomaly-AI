import { NavLink, Outlet } from 'react-router-dom'
import { Footer } from './Footer'
import { Header } from './Header'
import { Sidebar } from './Sidebar'

const mobileLinks = [
  { to: '/', label: 'Главная' },
  { to: '/waf', label: 'WAF' },
  { to: '/network', label: 'Сеть' },
  { to: '/reports', label: 'Отчёты' },
  { to: '/docs', label: 'Документация' },
] as const

export function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex w-full max-w-[1420px]">
        <Sidebar />
        <div className="flex min-h-screen flex-1 flex-col">
          <Header />
          <div className="border-b border-slate-800 px-4 py-3 sm:px-6 md:hidden">
            <div className="flex flex-wrap gap-2">
              {mobileLinks.map((l) => (
                <NavLink
                  key={l.to}
                  to={l.to}
                  end={l.to === '/'}
                  className={({ isActive }) =>
                    `rounded-lg px-3 py-1.5 text-[11px] font-medium ${
                      isActive ? 'bg-slate-800 text-sky-200' : 'text-slate-200 hover:bg-slate-800/60'
                    }`
                  }
                >
                  {l.label}
                </NavLink>
              ))}
            </div>
          </div>
          <main className="flex-1 space-y-6 px-4 py-6 sm:space-y-8 sm:px-6 sm:py-7 lg:px-8 lg:py-8">
            <Outlet />
          </main>
          <Footer />
        </div>
      </div>
    </div>
  )
}
