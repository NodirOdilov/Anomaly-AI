// Страница входа в систему.
// Демо-режим: если бэкенд недоступен, кнопка «Войти как demo» использует анонимного viewer.

import { useState, type FormEvent } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

interface LocationState {
  from?: string
}

export function LoginPage() {
  const [email, setEmail] = useState('admin@anomaly.local')
  const [password, setPassword] = useState('ChangeMe!2026')
  const [error, setError] = useState<string | null>(null)
  const { login, loading } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as LocationState | null)?.from ?? '/'

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    try {
      await login(email, password)
      navigate(from, { replace: true })
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Не удалось войти'
      setError(msg)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--aa-bg)] p-4">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md rounded-2xl border border-[var(--aa-border)] bg-[var(--aa-card)] p-8 shadow-2xl"
      >
        <h1 className="text-2xl font-semibold text-[var(--aa-fg)]">Вход в Anomaly AI</h1>
        <p className="mt-1 text-sm text-[var(--aa-muted)]">
          Аутентификация в консоль аналитика
        </p>

        <label className="mt-6 block text-sm text-[var(--aa-fg)]">
          Email
          <input
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="username"
            className="mt-1 w-full rounded-lg border border-[var(--aa-border)] bg-[var(--aa-panel)] px-3 py-2 text-sm text-[var(--aa-fg)] outline-none focus:border-[var(--aa-accent)]"
          />
        </label>

        <label className="mt-4 block text-sm text-[var(--aa-fg)]">
          Пароль
          <input
            type="password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
            className="mt-1 w-full rounded-lg border border-[var(--aa-border)] bg-[var(--aa-panel)] px-3 py-2 text-sm text-[var(--aa-fg)] outline-none focus:border-[var(--aa-accent)]"
          />
        </label>

        {error && (
          <p className="mt-4 rounded-lg border border-orange-500/40 bg-orange-500/10 px-3 py-2 text-sm text-orange-300">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="mt-6 w-full rounded-lg bg-[var(--aa-accent)] px-4 py-2.5 text-sm font-medium text-slate-900 transition hover:brightness-110 disabled:opacity-50"
        >
          {loading ? 'Входим…' : 'Войти'}
        </button>

        <p className="mt-4 text-xs text-[var(--aa-muted)]">
          Дефолтный admin создаётся при первом старте бэкенда из переменных
          <code className="mx-1 rounded bg-[var(--aa-panel)] px-1">BOOTSTRAP_ADMIN_*</code>.
        </p>
      </form>
    </div>
  )
}
