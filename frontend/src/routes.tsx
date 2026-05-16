// Дерево маршрутов Anomaly AI v2.
// Публичные: /login. Защищённые: всё остальное (через ProtectedRoute).
// В режиме AUTH_REQUIRED=false на бэкенде ProtectedRoute всё равно пропустит
// (user будет анонимным viewer'ом), потому что fetchMe() вернёт valid user.

import { Route, Routes } from 'react-router-dom'
import { ProtectedRoute } from './auth/ProtectedRoute'
import { AppLayout } from './components/layout/AppLayout'
import { AdminAuditPage } from './pages/AdminAuditPage'
import { AlertsPage } from './pages/AlertsPage'
import { DashboardPage } from './pages/DashboardPage'
import { DocumentationPage } from './pages/DocumentationPage'
import { LoginPage } from './pages/LoginPage'
import { NetworkAnalyzerPage } from './pages/NetworkAnalyzerPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { ReportsPage } from './pages/ReportsPage'
import { WafAnalyzerPage } from './pages/WafAnalyzerPage'

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route element={<AppLayout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/waf" element={<WafAnalyzerPage />} />
        <Route path="/network" element={<NetworkAnalyzerPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/alerts" element={<AlertsPage />} />
        <Route path="/docs" element={<DocumentationPage />} />
        <Route
          path="/admin/audit"
          element={
            <ProtectedRoute roles={['admin', 'analyst']}>
              <AdminAuditPage />
            </ProtectedRoute>
          }
        />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}
