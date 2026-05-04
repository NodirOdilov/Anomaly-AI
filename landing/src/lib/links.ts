const dash = import.meta.env.VITE_DASHBOARD_URL as string | undefined
const api = import.meta.env.VITE_API_URL as string | undefined
const repo = import.meta.env.VITE_REPO_URL as string | undefined

/** Встроенная научная документация в приложении лендинга */
export const docsPortalPath = '/docs'

const defaultDashboard = import.meta.env.DEV ? 'http://localhost:5173' : '/console'
const defaultApiOrigin = import.meta.env.DEV ? 'http://localhost:8000' : ''

export const links = {
  dashboard: dash?.trim() || defaultDashboard,
  apiHealth: api
    ? `${api.replace(/\/$/, '')}/health`
    : defaultApiOrigin
      ? `${defaultApiOrigin}/health`
      : '/health',
  /** Markdown в репозитории (если задан VITE_REPO_URL) */
  docsRepo: repo ? `${repo.replace(/\/$/, '')}/blob/main/docs/API.md` : null,
  repo: repo || '#',
}
