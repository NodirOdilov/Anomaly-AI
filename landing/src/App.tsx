import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { DocsLayout } from './docs/DocsLayout'
import { ApiReferencePage } from './docs/pages/ApiReferencePage'
import { ArtifactsPage } from './docs/pages/ArtifactsPage'
import { DatasetsPage } from './docs/pages/DatasetsPage'
import { DocsIndex } from './docs/pages/DocsIndex'
import { FoundationsPage } from './docs/pages/FoundationsPage'
import { LimitationsPage } from './docs/pages/LimitationsPage'
import { MethodologyPage } from './docs/pages/MethodologyPage'
import { ModelsPage } from './docs/pages/ModelsPage'
import { ReferencesPage } from './docs/pages/ReferencesPage'
import LandingPage from './pages/LandingPage'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/docs" element={<DocsLayout />}>
          <Route index element={<DocsIndex />} />
          <Route path="foundations" element={<FoundationsPage />} />
          <Route path="methodology" element={<MethodologyPage />} />
          <Route path="models" element={<ModelsPage />} />
          <Route path="datasets" element={<DatasetsPage />} />
          <Route path="api" element={<ApiReferencePage />} />
          <Route path="artifacts" element={<ArtifactsPage />} />
          <Route path="limitations" element={<LimitationsPage />} />
          <Route path="references" element={<ReferencesPage />} />
          <Route path="*" element={<Navigate to="/docs" replace />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  )
}
