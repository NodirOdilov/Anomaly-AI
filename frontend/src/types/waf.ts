export type WafPredictRequest = {
  payload: string
}

export type WafPredictResult = {
  payload: string
  is_attack: boolean
  attack_type: string
  confidence: number
  severity: string
  recommendation?: string | null
  model_version?: string | null
}

export type WafBatchResponse = {
  total: number
  attacks_detected: number
  results: WafPredictResult[]
}
