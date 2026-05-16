// Компактный переключатель тем для шапки.

import { useTheme, type ThemeMode } from '../../hooks/useTheme'

const options: { value: ThemeMode; label: string }[] = [
  { value: 'light', label: 'Светлая' },
  { value: 'dark', label: 'Тёмная' },
  { value: 'system', label: 'Система' },
]

export function ThemeToggle() {
  const { mode, setMode } = useTheme()
  return (
    <div className="inline-flex items-center gap-1 rounded-lg border border-[var(--aa-border)] bg-[var(--aa-panel)] p-0.5">
      {options.map((opt) => (
        <button
          key={opt.value}
          type="button"
          onClick={() => setMode(opt.value)}
          className={`rounded-md px-2 py-1 text-xs transition ${
            mode === opt.value
              ? 'bg-[var(--aa-accent)] text-slate-900'
              : 'text-[var(--aa-muted)] hover:text-[var(--aa-fg)]'
          }`}
          title={`Тема: ${opt.label}`}
        >
          {opt.label}
        </button>
      ))}
    </div>
  )
}
