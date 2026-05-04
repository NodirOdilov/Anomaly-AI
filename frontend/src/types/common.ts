export type HealthResponse = {
  status: string
  service: string
  version: string
  backend: string
}

export type InfoResponse = {
  name: string
  description: string
  modules: string[]
  mode: string
}
