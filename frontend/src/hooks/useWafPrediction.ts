import { useCallback, useState } from 'react'
import { predictWaf } from '../api/wafApi'
import type { WafPredictResult } from '../types/waf'
import { buildDemoWafResult } from '../utils/demoFallback'
import { demoDelay, FORCE_DEMO_MODE } from '../utils/demoMode'

export function useWafPrediction() {
  const [data, setData] = useState<WafPredictResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const run = useCallback(async (payload: string) => {
    setLoading(true)
    setError(null)
    if (FORCE_DEMO_MODE) {
      await demoDelay()
      setData(buildDemoWafResult(payload))
      setError(null)
      setLoading(false)
      return
    }
    try {
      const res = await predictWaf({ payload })
      setData(res)
    } catch {
      // Demo fallback: do not surface transport/runtime errors in UI.
      setData(buildDemoWafResult(payload))
      setError(null)
    } finally {
      setLoading(false)
    }
  }, [])

  return { data, loading, error, run }
}
