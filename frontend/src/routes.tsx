import { Route, Routes } from 'react-router-dom'
import { AppLayout } from './components/layout/AppLayout'
import { DashboardPage } from './pages/DashboardPage'
import { DocumentationPage } from './pages/DocumentationPage'
import { NetworkAnalyzerPage } from './pages/NetworkAnalyzerPage'
import { NotFoundPage } from './pages/NotFoundPage'
import { ReportsPage } from './pages/ReportsPage'
import { WafAnalyzerPage } from './pages/WafAnalyzerPage'

export function AppRoutes() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/waf" element={<WafAnalyzerPage />} />
        <Route path="/network" element={<NetworkAnalyzerPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/docs" element={<DocumentationPage />} />
      </Route>
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}
