# Наблюдаемость и метрики

> Prometheus, Grafana, structlog и health-чеки для эксплуатации Anomaly AI в production.

| Параметр | Значение |
|----------|----------|
| Метрики | `GET /metrics` |
| Дашборд | `deploy/grafana/provisioning/dashboards/anomaly-ai.json` |
| Drift | [`DRIFT.md`](DRIFT.md) |

## Содержание

1. [Prometheus](#prometheus)
2. [Каталог метрик](#каталог-метрик)
3. [Health-чеки](#health-чеки)
4. [Структурированные логи](#структурированные-логи)
5. [Sentry](#sentry-опционально)
6. [Grafana](#grafana-дашборд)
7. [Примеры PromQL](#примеры-promql)

---

## Prometheus

Метрики экспонируются на `GET /metrics` (формат Prometheus text-format).

Docker Compose поднимает Prometheus и Grafana:

```bash
docker compose up --build
```

| Сервис | URL |
|--------|-----|
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` (admin/admin) |

---

## Каталог метрик

| Метрика | Тип | Лейблы | Описание |
|---------|-----|--------|----------|
| `anomaly_ai_http_requests_total` | Counter | `method, path, status` | Всего HTTP-запросов |
| `anomaly_ai_http_request_duration_seconds` | Histogram | `method, path` | Латентность запросов |
| `anomaly_ai_http_requests_in_progress` | Gauge | `method` | Активные запросы |
| `anomaly_ai_predictions_total` | Counter | `module, prediction, is_attack` | Всего предсказаний |
| `anomaly_ai_prediction_confidence` | Histogram | `module` | Распределение confidence |
| `anomaly_ai_model_drift_score` | Gauge | `module` | Текущий PSI модели |
| `anomaly_ai_model_active_version_info` | Gauge | `module, version` | Активная версия (info) |
| `anomaly_ai_auth_logins_total` | Counter | `result` | Попытки логина |
| `anomaly_ai_alerts_emitted_total` | Counter | `severity, module` | Сгенерированные алерты |

---

## Health-чеки

| Эндпоинт | Назначение |
|----------|------------|
| `GET /health` | Простой 200 OK (load balancer) |
| `GET /health/live` | Liveness |
| `GET /health/ready` | Readiness (доступность БД) |

---

## Структурированные логи

В production (`APP_ENV=production` или `LOG_JSON=true`) логи — JSON:

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

Каждый запрос получает `X-Request-ID` (генерируется или от upstream). ID прокидывается через `structlog.contextvars`.

---

## Sentry (опционально)

`SENTRY_DSN` — отправка ошибок с `environment=$APP_ENV`, `traces_sample_rate=0.1`.

---

## Grafana дашборд

Провижинг: `deploy/grafana/provisioning/dashboards/anomaly-ai.json`.

| Панель | Тип |
|--------|-----|
| Всего предсказаний | stat |
| Активные HTTP | stat |
| Алертов сгенерировано | stat |
| Drift score WAF | gauge |
| p95 латентность | timeseries |
| Предсказания/мин | timeseries |

---

## Примеры PromQL

```promql
# RPS по эндпоинтам:
sum by (path) (rate(anomaly_ai_http_requests_total[5m]))

# p95 /api/v1/waf/predict:
histogram_quantile(0.95,
  sum by (le) (rate(anomaly_ai_http_request_duration_seconds_bucket{path=~".*/waf/predict"}[5m])))

# Доля атак за час:
sum(rate(anomaly_ai_predictions_total{is_attack="true"}[1h]))
/
sum(rate(anomaly_ai_predictions_total[1h]))

# Drift выше критического порога:
anomaly_ai_model_drift_score > 0.25
```

---

## См. также

- [`DRIFT.md`](DRIFT.md) — PSI и алерты по дрейфу
- [`INTEGRATION.md`](INTEGRATION.md) — SIEM и события
- [`DEPLOYMENT.md`](DEPLOYMENT.md) — развёртывание стека
