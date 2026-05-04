import { apiClient } from './client'
import { endpoints } from './endpoints'
import type { ModelsStatusResponse, ReportsSummaryResponse } from '../types/reports'

export async function fetchReportsSummary(): Promise<ReportsSummaryResponse> {
  const { data } = await apiClient.get<ReportsSummaryResponse>(endpoints.reportsSummary)
  return data
}

export async function fetchModelsStatus(): Promise<ModelsStatusResponse> {
  const { data } = await apiClient.get<ModelsStatusResponse>(endpoints.modelsStatus)
  return data
}
