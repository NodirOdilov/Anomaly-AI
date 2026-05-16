// Хранилище токенов: localStorage с типизированными ключами и событиями.

const ACCESS_KEY = 'aa.auth.access'
const REFRESH_KEY = 'aa.auth.refresh'
const USER_KEY = 'aa.auth.user'

export interface StoredUser {
  id: number
  email: string
  role: string
  full_name: string | null
}

export const tokenStore = {
  getAccess(): string | null {
    return localStorage.getItem(ACCESS_KEY)
  },
  getRefresh(): string | null {
    return localStorage.getItem(REFRESH_KEY)
  },
  getUser(): StoredUser | null {
    const raw = localStorage.getItem(USER_KEY)
    if (!raw) return null
    try {
      return JSON.parse(raw) as StoredUser
    } catch {
      return null
    }
  },
  setTokens(access: string, refresh?: string | null): void {
    localStorage.setItem(ACCESS_KEY, access)
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh)
    window.dispatchEvent(new CustomEvent('aa-auth-change'))
  },
  setUser(user: StoredUser): void {
    localStorage.setItem(USER_KEY, JSON.stringify(user))
    window.dispatchEvent(new CustomEvent('aa-auth-change'))
  },
  clear(): void {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(USER_KEY)
    window.dispatchEvent(new CustomEvent('aa-auth-change'))
  },
}
