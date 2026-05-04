export const endpoints = {
  health: '/health',
  info: '/api/v1/info',
  wafPredict: '/api/v1/waf/predict',
  wafBatch: '/api/v1/waf/batch-predict',
  networkPredict: '/api/v1/network/predict',
  networkUpload: '/api/v1/network/upload-csv',
  reportsSummary: '/api/v1/reports/summary',
  modelsStatus: '/api/v1/models/status',
} as const
