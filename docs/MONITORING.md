# Наблюдаемость и метрики

## Prometheus

Метрики экспонируются на `GET /metrics` (формат Prometheus text-format).
В Docker Compose Prometheus и Grafana поднимаются автоматически:

```bash
docker compose up --build
# Prometheus → http://localhost:9090
# Grafana    → http://localhost:3000  (admin/admin)
```

## Каталог метрик

| Метрика | Тип | Лейблы | Описание |
|---|---|---|---|
| `anomaly_ai_http_requests_total` | Counter | `method, path, status` | Всего HTTP-запросов |
| `anomaly_ai_http_request_duration_seconds` | Histogram | `method, path` | Латентность запросов |
| `anomaly_ai_http_requests_in_progress` | Gauge | `method` | Активные запросы |
| `anomaly_ai_predictions_total` | Counter | `module, prediction, is_attack` | Всего предсказаний |
| `anomaly_ai_prediction_confidence` | Histogram | `module` | Распределение confidence |
| `anomaly_ai_model_drift_score` | Gauge | `module` | Текущий PSI модели |
| `anomaly_ai_model_active_version_info` | Gauge | `module, version` | Активная версия (info) |
| `anomaly_ai_auth_logins_total` | Counter | `result` | Попытки логина |
| `anomaly_ai_alerts_emitted_total` | Counter | `severity, module` | Сгенерированные алерты |

## Health-чеки

- `GET /health` — простой 200 OK (для load balancer).
- `GET /health/live` — liveness (процесс жив).
- `GET /health/ready` — readiness (БД доступна).

## Структурированные логи (structlog)

В production (`APP_ENV=production` или `LOG_JSON=true`) логи пишутся в JSON:

```json
{
  "event": "prediction.completed",
  "level": "info",
  "module": "waf_payload",
  "is_attack": true,
  "request_id": "abc123",
  "timestamp": "2026-05-16T10:00:00Z"
}
```

Каждый запрос получает заголовок `X-Request-ID` (генерируется или приходит от
upstream). Этот ID прокидывается во все логи через `structlog.contextvars`.

## Sentry (опционально)

Установите `SENTRY_DSN` — ошибки будут отправляться в Sentry с
`environment=$APP_ENV` и `traces_sample_rate=0.1`.

## Grafana дашборд

Автоматически провижится из `deploy/grafana/provisioning/dashboards/anomaly-ai.json`.
Содержит панели:

1. Всего предсказаний (stat).
2. Активные HTTP запросы (stat).
3. Алертов сгенерировано (stat).
4. Drift score WAF (gauge).
5. p95 латентность по эндпоинтам (timeseries).
6. Предсказания/мин по модулям (timeseries).

## Примеры PromQL

```promql
# RPS по эндпоинтам:
sum by (path) (rate(anomaly_ai_http_requests_total[5m]))

# p95 латентность /api/v1/waf/predict:
histogram_quantile(0.95,
  sum by (le) (rate(anomaly_ai_http_request_duration_seconds_bucket{path=~".*/waf/predict"}[5m])))

# Доля атак за последний час:
sum(rate(anomaly_ai_predictions_total{is_attack="true"}[1h]))
/
sum(rate(anomaly_ai_predictions_total[1h]))

# Тревога: drift score выше критического порога:
anomaly_ai_model_drift_score > 0.25
```

## Связано

- [[DRIFT]] — детектор дрейфа и интерпретация PSI
- [[INTEGRATION]] — отправка событий в SIEM
