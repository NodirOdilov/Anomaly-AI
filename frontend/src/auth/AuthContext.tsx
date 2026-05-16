// React Context для аутентификации: хранит текущего пользователя, login/logout.
// Автоматически прикрепляет Bearer-токен ко всем axios-запросам через interceptor.

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import { client } from '../api/client'
import { fetchMe, login as loginRequest, logout as logoutRequest } from '../api/authApi'
import { tokenStore, type StoredUser } from './tokenStore'

interface AuthContextValue {
  user: StoredUser | null
  loading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

// === Axios interceptor для Bearer-токена ===

let interceptorId: number | null = null

function ensureInterceptor() {
  if (interceptorId !== null) return
  interceptorId = client.interceptors.request.use((config) => {
    const token = tokenStore.getAccess()
    if (token) {
      config.headers = config.headers ?? {}
      ;(config.headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
    }
    return config
  })
}

ensureInterceptor()

// === Provider ===

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<StoredUser | null>(() => tokenStore.getUser())
  const [loading, setLoading] = useState<boolean>(false)

  const refreshUser = useCallback(async () => {
    try {
      const me = await fetchMe()
      const stored: StoredUser = {
        id: me.id,
        email: me.email,
        role: me.role,
        full_name: me.full_name,
      }
      tokenStore.setUser(stored)
      setUser(stored)
    } catch {
      // Не залогинены или dev-mode без auth — оставляем user=null.
    }
  }, [])

  const login = useCallback(
    async (email: string, password: string) => {
      setLoading(true)
      try {
        const pair = await loginRequest({ email, password })
        tokenStore.setTokens(pair.access_token, pair.refresh_token)
        await refreshUser()
      } finally {
        setLoading(false)
      }
    },
    [refreshUser],
  )

  const logout = useCallback(async () => {
    const refresh = tokenStore.getRefresh()
    if (refresh) {
      try {
        await logoutRequest(refresh)
      } catch {
        /* игнорируем — мы всё равно очистим локальные токены */
      }
    }
    tokenStore.clear()
    setUser(null)
  }, [])

  useEffect(() => {
    const handler = () => setUser(tokenStore.getUser())
    window.addEventListener('aa-auth-change', handler)
    return () => window.removeEventListener('aa-auth-change', handler)
  }, [])

  const value = useMemo<AuthContextValue>(
    () => ({
      user,
      loading,
      isAuthenticated: user !== null,
      login,
      logout,
      refreshUser,
    }),
    [user, loading, login, logout, refreshUser],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth должен использоваться внутри <AuthProvider>')
  return ctx
}
