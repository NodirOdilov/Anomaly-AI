import { apiClient } from './client'
import { endpoints } from './endpoints'
import type { WafBatchResponse, WafPredictRequest, WafPredictResult } from '../types/waf'

export async function predictWaf(body: WafPredictRequest): Promise<WafPredictResult> {
  const { data } = await apiClient.post<WafPredictResult>(endpoints.wafPredict, body)
  return data
}

export async function batchPredictWaf(payloads: string[]): Promise<WafBatchResponse> {
  const { data } = await apiClient.post<WafBatchResponse>(endpoints.wafBatch, { payloads })
  return data
}
