import { useEffect, useState } from 'react'
import { apiClient } from '../api/client'
import { endpoints } from '../api/endpoints'
import type { HealthResponse } from '../types/common'
import { buildDemoHealth } from '../utils/demoFallback'
import { FORCE_DEMO_MODE } from '../utils/demoMode'

export function useHealth(pollMs = 15_000) {
  const [data, setData] = useState<HealthResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function load() {
      if (FORCE_DEMO_MODE) {
        if (!cancelled) {
          setLoading(true)
          setData(buildDemoHealth())
          setError(null)
          setLoading(false)
        }
        return
      }
      try {
        setLoading(true)
        const { data: d } = await apiClient.get<HealthResponse>(endpoints.health)
        if (!cancelled) {
          setData(d)
          setError(null)
        }
      } catch {
        if (!cancelled) {
          setData(buildDemoHealth())
          setError(null)
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    void load()
    const id = window.setInterval(() => void load(), pollMs)
    return () => {
      cancelled = true
      window.clearInterval(id)
    }
  }, [pollMs])

  return { data, loading, error }
}
