// Клиент аутентификации Anomaly AI v2.
// Все эндпоинты — под /api/v1/auth/*.

import { client } from './client'

export interface LoginRequest {
  email: string
  password: string
}

export interface TokenPair {
  access_token: string
  refresh_token: string
  token_type: string
  access_expires_in: number
  refresh_expires_in: number
}

export interface AccessTokenResponse {
  access_token: string
  token_type: string
  expires_in: number
}

export interface UserPublic {
  id: number
  email: string
  full_name: string | null
  role: string
  is_active: boolean
  created_at: string
  last_login_at: string | null
}

export interface ApiKeyPublic {
  id: number
  name: string
  prefix: string
  scopes: string
  created_at: string
  expires_at: string | null
  revoked_at: string | null
  last_used_at: string | null
}

export interface ApiKeyCreated extends ApiKeyPublic {
  plain: string
}

// === Запросы ===

export async function login(body: LoginRequest): Promise<TokenPair> {
  const { data } = await client.post<TokenPair>('/api/v1/auth/login', body)
  return data
}

export async function refresh(refresh_token: string): Promise<AccessTokenResponse> {
  const { data } = await client.post<AccessTokenResponse>('/api/v1/auth/refresh', {
    refresh_token,
  })
  return data
}

export async function logout(refresh_token: string): Promise<void> {
  await client.post('/api/v1/auth/logout', { refresh_token })
}

export async function fetchMe(): Promise<UserPublic> {
  const { data } = await client.get<UserPublic>('/api/v1/auth/me')
  return data
}

export async function listApiKeys(): Promise<ApiKeyPublic[]> {
  const { data } = await client.get<ApiKeyPublic[]>('/api/v1/auth/api-keys')
  return data
}

export async function createApiKey(name: string, scopes = 'predict'): Promise<ApiKeyCreated> {
  const { data } = await client.post<ApiKeyCreated>('/api/v1/auth/api-keys', { name, scopes })
  return data
}

export async function revokeApiKey(id: number): Promise<void> {
  await client.delete(`/api/v1/auth/api-keys/${id}`)
}
