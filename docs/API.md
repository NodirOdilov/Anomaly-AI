# Справочник HTTP API

> REST API Anomaly AI v2: health, ML-inference, отчёты, auth, drift, интеграции.

| Параметр | Значение |
|----------|----------|
| Базовый URL (локально) | `http://localhost:8000` |
| OpenAPI UI | `/api/swagger` |
| Auth | [`AUTH.md`](AUTH.md) |

## Содержание

1. [Системные эндпоинты](#системные-эндпоинты)
2. [WAF payload](#waf-payload)
3. [Сетевые аномалии](#сетевые-аномалии)
4. [Отчёты и модели](#отчёты-и-модели)
5. [Ошибки](#ошибки)
6. [Расширенный API v2](#расширенный-api-v2)

---

## Системные эндпоинты

### `GET /health`

```json
{
  "status": "ok",
  "service": "Anomaly AI",
  "version": "2.0.0",
  "backend": "FastAPI"
}
```

### `GET /api/v1/info`

```json
{
  "name": "Anomaly AI",
  "description": "Machine Learning Based Network Anomaly and Web Attack Detection Platform",
  "modules": ["Network Anomaly Detection", "WAF Payload Attack Detection"],
  "mode": "defensive-security"
}
```

---

## WAF payload

### `POST /api/v1/waf/predict`

**Запрос:**

```json
{ "payload": "id=1' OR '1'='1" }
```

**Ответ (структура):**

```json
{
  "payload": "id=1' OR '1'='1",
  "is_attack": true,
  "attack_type": "sql_injection",
  "confidence": 0.94,
  "severity": "high",
  "recommendation": "Block request and log incident",
  "model_version": "2.0.0"
}
```

### `POST /api/v1/waf/batch-predict`

**Запрос:**

```json
{ "payloads": ["q=books", "id=1' OR '1'='1"] }
```

**Ответ:** `total`, `attacks_detected`, `results[]` (поля как у одиночного predict; часть опциональных полей может отсутствовать).

---

## Сетевые аномалии

### `POST /api/v1/network/predict`

Тело JSON — все числовые признаки обученной модели. Пример ключей из sample CSV:

`duration`, `tot_fwd_pkts`, `tot_bwd_pkts`, `tot_fwd_len`, `tot_bwd_len`, `fwd_pkt_len_max`, `bwd_pkt_len_max`, `flow_pkts_s`, `flow_byts_s`

**Ответ:**

```json
{
  "prediction": "UDP_ATTACK",
  "confidence": 0.88,
  "severity": "high",
  "recommendation": "Investigate source IP and traffic pattern",
  "model_version": "2.0.0"
}
```

### `POST /api/v1/network/upload-csv`

`multipart/form-data`, поле `file` (CSV UTF-8). Возвращает счётчики, `top_prediction` и оценки по строкам.

---

## Отчёты и модели

| Метод | Путь | Назначение |
|-------|------|------------|
| `GET` | `/api/v1/reports/summary` | Сводка метрик `network_anomaly` и `waf_payload` |
| `GET` | `/api/v1/models/status` | Статус загрузки артефактов |

---

## Ошибки

Ошибки валидации и приложения — JSON:

```json
{ "error": "InvalidInput", "message": "Payload must not be empty" }
```

| Код | Типичная причина |
|-----|------------------|
| 400 | Невалидное тело запроса |
| 401 | Нет или просрочен JWT / API key |
| 403 | Недостаточно прав RBAC |
| 429 | Rate limit |
| 500 | Внутренняя ошибка (см. `X-Request-ID` в логах) |

---

## Расширенный API v2

Полный перечень (auth, users, alerts, drift, integrations, audit):

| Раздел | Документ |
|--------|----------|
| JWT, API keys, RBAC | [`AUTH.md`](AUTH.md) |
| PSI / drift | [`DRIFT.md`](DRIFT.md) |
| SIEM, threat intel | [`INTEGRATION.md`](INTEGRATION.md) |
| Интерактивная схема | `http://localhost:8000/api/swagger` |

---

## См. также

- [`ARCHITECTURE.md`](ARCHITECTURE.md)
- [`DEPLOYMENT.md`](DEPLOYMENT.md)
