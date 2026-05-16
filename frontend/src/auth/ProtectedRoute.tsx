// HOC-роут: проверяет аутентификацию и опционально роль.
// Если auth_required=false на бэкенде, пользователь будет анонимным viewer'ом.

import type { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { useAuth } from './AuthContext'

interface Props {
  children: ReactNode
  roles?: string[]
  redirectTo?: string
}

export function ProtectedRoute({ children, roles, redirectTo = '/login' }: Props) {
  const { user, isAuthenticated } = useAuth()
  const location = useLocation()

  if (!isAuthenticated) {
    return <Navigate to={redirectTo} state={{ from: location.pathname }} replace />
  }
  if (roles && roles.length > 0 && user && !roles.includes(user.role)) {
    return <Navigate to="/" replace />
  }
  return <>{children}</>
}
