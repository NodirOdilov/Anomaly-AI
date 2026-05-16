# Интеграции: SIEM и разведка угроз

> Экспорт событий детекции во внешние системы и локальная база индикаторов компрометации.

| Параметр | Значение |
|----------|----------|
| Порог SIEM | `SIEM_MIN_CONFIDENCE` (по умолчанию 0.85) |
| Форматы | JSON (Splunk HEC, ELK), CEF (ArcSight, QRadar) |
| RBAC | Управление SIEM — роль `admin` |

## Содержание

1. [SIEM](#siem)
2. [Форматы событий](#форматы-событий)
3. [Threat Intelligence](#threat-intelligence)
4. [Надёжность доставки](#надёжность-доставки)

---

## SIEM

События отправляются при детектах с `confidence ≥ SIEM_MIN_CONFIDENCE`.

### Глобальная настройка (env)

```bash
SIEM_WEBHOOK_URL=https://splunk.example.com/services/collector
SIEM_WEBHOOK_FORMAT=json     # или cef
SIEM_WEBHOOK_TOKEN=<HEC_token>
SIEM_MIN_CONFIDENCE=0.85
```

### Эндпоинты через БД

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

Тест:

```http
POST /api/v1/integrations/siem/{id}/test
```

---

## Форматы событий

### JSON

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

### CEF

```
CEF:0|AnomalyAI|AnomalyAI-Detector|2.0|AA-WAF-001|SQL injection detected|8|cs1Label=module cs1=waf_payload confidence=0.94 attack_type=sql_injection
```

| Severity (текст) | CEF severity |
|------------------|--------------|
| low | 3 |
| medium | 6 |
| high | 8 |
| critical | 10 |

---

## Threat Intelligence

Локальная БД индикаторов: IP, домены, хэши (`threat_intel_entries`).

### Импорт CSV

```http
POST /api/v1/integrations/threat-intel/import
Authorization: Bearer <admin_jwt>
Content-Type: multipart/form-data

file=@indicators.csv
```

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

---

## Надёжность доставки

| Параметр | Значение |
|----------|----------|
| Retry | До 3 попыток (0.5s → 1s → 2s) |
| Timeout | 5 с по умолчанию |
| Логи | `siem.event_sent` / `siem.send_failed` |
| Состояние | `last_success_at`, `last_error` в `siem_endpoints` |

---

## См. также

- [`MONITORING.md`](MONITORING.md) — `anomaly_ai_alerts_emitted_total`
- [`AUTH.md`](AUTH.md) — роли и API keys
