import { useEffect, useState } from 'react'
import { fetchModelsStatus, fetchReportsSummary } from '../api/reportsApi'
import type { ModelsStatusResponse, ReportsSummaryResponse } from '../types/reports'
import { buildDemoModelsStatus, buildDemoReportsSummary } from '../utils/demoFallback'
import { FORCE_DEMO_MODE } from '../utils/demoMode'

export function useReports() {
  const [summary, setSummary] = useState<ReportsSummaryResponse | null>(null)
  const [models, setModels] = useState<ModelsStatusResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      setError(null)
      if (FORCE_DEMO_MODE) {
        if (!cancelled) {
          setSummary(buildDemoReportsSummary())
          setModels(buildDemoModelsStatus())
          setError(null)
          setLoading(false)
        }
        return
      }
      try {
        const [s, m] = await Promise.all([fetchReportsSummary(), fetchModelsStatus()])
        if (!cancelled) {
          setSummary(s)
          setModels(m)
          setError(null)
        }
      } catch {
        if (!cancelled) {
          setSummary(buildDemoReportsSummary())
          setModels(buildDemoModelsStatus())
          setError(null)
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    void load()
    return () => {
      cancelled = true
    }
  }, [])

  return { summary, models, loading, error }
}
