import { apiClient } from './client'
import { endpoints } from './endpoints'
import type { NetworkCsvResponse, NetworkPredictResponse } from '../types/network'

export async function predictNetwork(features: Record<string, number>): Promise<NetworkPredictResponse> {
  const { data } = await apiClient.post<NetworkPredictResponse>(endpoints.networkPredict, features)
  return data
}

export async function uploadNetworkCsv(file: File): Promise<NetworkCsvResponse> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await apiClient.post<NetworkCsvResponse>(endpoints.networkUpload, form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}
