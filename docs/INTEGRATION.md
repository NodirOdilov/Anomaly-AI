# Интеграции: SIEM и Threat Intelligence

## SIEM

Anomaly AI отправляет события в SIEM при детектах с `confidence ≥ SIEM_MIN_CONFIDENCE`
(по умолчанию 0.85). Поддержано два формата:

- **JSON** — для Splunk HEC, ELK, Datadog Logs.
- **CEF** (Common Event Format) — для ArcSight, QRadar.

### Глобальная настройка (через env)

```bash
SIEM_WEBHOOK_URL=https://splunk.example.com/services/collector
SIEM_WEBHOOK_FORMAT=json     # или cef
SIEM_WEBHOOK_TOKEN=<HEC_token>
SIEM_MIN_CONFIDENCE=0.85
```

### Множественные эндпоинты через БД

Админ может добавлять SIEM-эндпоинты через API:

```http
POST /api/v1/integrations/siem
Authorization: Bearer <admin_jwt>

{
  "name": "primary-splunk",
  "url": "https://splunk.example.com/services/collector",
  "format": "json",
  "token": "12345-abcde",
  "min_confidence": 0.9
}
```

Проверить эндпоинт тестовым событием:

```http
POST /api/v1/integrations/siem/{id}/test
```

### Формат JSON-события

```json
{
  "time": "2026-05-16T10:00:00Z",
  "source": "anomaly-ai",
  "sourcetype": "anomaly_ai:waf_payload",
  "event": {
    "module": "waf_payload",
    "severity": "high",
    "summary": "SQL injection detected",
    "details": {
      "confidence": 0.94,
      "attack_type": "sql_injection",
      "payload_preview": "id=1' OR ..."
    }
  }
}
```

### Формат CEF

```
CEF:0|AnomalyAI|AnomalyAI-Detector|2.0|AA-WAF-001|SQL injection detected|8|cs1Label=module cs1=waf_payload confidence=0.94 attack_type=sql_injection
```

Маппинг severity:

| Текст | CEF severity |
|---|---|
| low | 3 |
| medium | 6 |
| high | 8 |
| critical | 10 |

## Threat Intelligence

Локальная база индикаторов (IP, домены, хэши) в таблице `threat_intel_entries`.

### Импорт CSV

```http
POST /api/v1/integrations/threat-intel/import
Authorization: Bearer <admin_jwt>
Content-Type: multipart/form-data

file=@indicators.csv
```

Формат CSV:

```csv
indicator_type,indicator,severity,source,description
ip,192.0.2.1,high,abuse.ch,Known C2 server
domain,evil.example.com,critical,otx,Phishing
hash,abc123...,medium,virustotal,Malware sample
```

### Lookup

```http
POST /api/v1/integrations/threat-intel/lookup

{ "indicator_type": "ip", "indicator": "192.0.2.1" }
```

Ответ:

```json
{
  "indicator": "192.0.2.1",
  "indicator_type": "ip",
  "matched": true,
  "severity": "high",
  "source": "abuse.ch",
  "description": "Known C2 server"
}
```

## Webhook-надёжность

- Retry: до 3 попыток с экспоненциальной задержкой (0.5s → 1s → 2s).
- Timeout: 5 секунд по умолчанию.
- Все попытки логируются в `siem.event_sent` / `siem.send_failed`.
- Field `last_success_at` / `last_error` обновляются в таблице `siem_endpoints`.

## Связано

- [[MONITORING]] — Prometheus метрика alerts_emitted_total
- [[AUTH]] — управление SIEM требует admin роль
