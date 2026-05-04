export type NetworkPredictResponse = {
  prediction: string
  confidence: number
  severity: string
  recommendation: string
  model_version: string
}

export type NetworkRowResult = {
  row: number
  prediction: string
  confidence: number
}

export type NetworkCsvResponse = {
  total_flows: number
  benign: number
  suspicious: number
  top_prediction: string
  results: NetworkRowResult[]
}
