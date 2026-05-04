export type DocsNavItem = { to: string; label: string; end?: boolean }

export const docsNav: DocsNavItem[] = [
  { to: '/docs', label: 'Введение', end: true },
  { to: '/docs/foundations', label: 'Математические основы' },
  { to: '/docs/methodology', label: 'Методология оценки' },
  { to: '/docs/models', label: 'Архитектура моделей' },
  { to: '/docs/datasets', label: 'Данные и протоколы' },
  { to: '/docs/api', label: 'Справочник API' },
  { to: '/docs/artifacts', label: 'Артефакты и версии' },
  { to: '/docs/limitations', label: 'Ограничения и этика' },
  { to: '/docs/references', label: 'Литература' },
]
