export type ModuleMetrics = {
  model: string
  accuracy: number
  precision: number
  recall: number
  f1: number
  false_positive_rate: number
  false_negative_rate: number
  notes?: string | null
}

export type ReportsSummaryResponse = {
  network_anomaly: ModuleMetrics
  waf_payload: ModuleMetrics
}

export type ModelStatusItem = {
  loaded: boolean
  version?: string | null
  model_type?: string | null
  path?: string | null
  message?: string | null
}

export type ModelsStatusResponse = {
  network_anomaly: ModelStatusItem
  waf_payload: ModelStatusItem
}
