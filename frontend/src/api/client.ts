import axios, { type AxiosError } from 'axios'

function apiBaseURL(): string {
  const fromEnv = (import.meta.env.VITE_API_BASE_URL as string | undefined)?.trim()
  if (fromEnv) return fromEnv.replace(/\/$/, '')
  if (import.meta.env.DEV) return 'http://localhost:8000'
  if (typeof window !== 'undefined') return window.location.origin
  return ''
}

const baseURL = apiBaseURL()

export const apiClient = axios.create({
  baseURL,
  timeout: 60_000,
})

apiClient.interceptors.response.use(
  (r) => r,
  (err: AxiosError<{ error?: string; message?: string }>) => {
    const data = err.response?.data
    const message =
      (typeof data?.message === 'string' && data.message) ||
      (typeof data?.error === 'string' && data.error) ||
      err.message ||
      'Запрос завершился ошибкой'
    return Promise.reject(new Error(message))
  },
)
