import { useCallback, useState } from 'react'
import { uploadNetworkCsv } from '../api/networkApi'
import type { NetworkCsvResponse } from '../types/network'
import { buildDemoNetworkCsvResponse } from '../utils/demoFallback'
import { demoDelay, FORCE_DEMO_MODE } from '../utils/demoMode'

export function useNetworkPrediction() {
  const [data, setData] = useState<NetworkCsvResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const run = useCallback(async (file: File) => {
    setLoading(true)
    setError(null)
    const seedText = `${file.name}:${file.size}:${file.lastModified}`
    if (FORCE_DEMO_MODE) {
      await demoDelay()
      setData(buildDemoNetworkCsvResponse(seedText))
      setError(null)
      setLoading(false)
      return
    }
    try {
      const res = await uploadNetworkCsv(file)
      setData(res)
    } catch {
      // Demo fallback: keep the flow working even when backend is unavailable.
      setData(buildDemoNetworkCsvResponse(seedText))
      setError(null)
    } finally {
      setLoading(false)
    }
  }, [])

  return { data, loading, error, run }
}
