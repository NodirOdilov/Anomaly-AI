// Хук подписки на WebSocket /api/v1/alerts/ws.
// Реконнект с экспоненциальной задержкой, heartbeat-фильтрация.

import { useEffect, useRef, useState } from 'react'
import { tokenStore } from '../auth/tokenStore'

export interface LiveAlert {
  id?: number
  severity: string
  module: string
  summary: string
  payload?: Record<string, unknown>
  created_at: string
}

const API_BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) ?? ''

function wsUrlFromHttp(baseUrl: string): string {
  if (!baseUrl) {
    // Same-origin: ws(s)://host/api/v1/alerts/ws
    const proto = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    return `${proto}//${window.location.host}/api/v1/alerts/ws`
  }
  const url = new URL(baseUrl)
  url.protocol = url.protocol === 'https:' ? 'wss:' : 'ws:'
  url.pathname = '/api/v1/alerts/ws'
  return url.toString()
}

export function useAlertsStream(): { alerts: LiveAlert[]; connected: boolean } {
  const [alerts, setAlerts] = useState<LiveAlert[]>([])
  const [connected, setConnected] = useState(false)
  const wsRef = useRef<WebSocket | null>(null)
  const reconnectAttempts = useRef(0)

  useEffect(() => {
    let stopped = false

    function connect() {
      if (stopped) return
      const token = tokenStore.getAccess()
      let url = wsUrlFromHttp(API_BASE)
      if (token) {
        url += `?token=${encodeURIComponent(token)}`
      }

      const ws = new WebSocket(url)
      wsRef.current = ws

      ws.onopen = () => {
        setConnected(true)
        reconnectAttempts.current = 0
      }

      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data) as { type?: string } & LiveAlert
          if (data.type === 'ping') return
          setAlerts((prev) => [data, ...prev].slice(0, 100))
        } catch {
          /* пропускаем некорректные сообщения */
        }
      }

      ws.onclose = () => {
        setConnected(false)
        if (stopped) return
        reconnectAttempts.current += 1
        const delay = Math.min(30000, 1000 * 2 ** reconnectAttempts.current)
        setTimeout(connect, delay)
      }

      ws.onerror = () => {
        ws.close()
      }
    }

    connect()
    return () => {
      stopped = true
      wsRef.current?.close()
    }
  }, [])

  return { alerts, connected }
}
