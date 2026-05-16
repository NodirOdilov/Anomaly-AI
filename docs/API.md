# Справочник HTTP API

Базовый URL (локально): `http://localhost:8000`

## `GET /health`

```json
{
  "status": "ok",
  "service": "Anomaly AI",
  "version": "1.0.0",
  "backend": "FastAPI"
}
```

## `GET /api/v1/info`

```json
{
  "name": "Anomaly AI",
  "description": "Machine Learning Based Network Anomaly and Web Attack Detection Platform",
  "modules": ["Network Anomaly Detection", "WAF Payload Attack Detection"],
  "mode": "defensive-security"
}
```

## `POST /api/v1/waf/predict`

Запрос:

```json
{ "payload": "id=1' OR '1'='1" }
```

Ответ (структура):

```json
{
  "payload": "id=1' OR '1'='1",
  "is_attack": true,
  "attack_type": "sql_injection",
  "confidence": 0.94,
  "severity": "high",
  "recommendation": "Block request and log incident",
  "model_version": "1.0.0"
}
```

## `POST /api/v1/waf/batch-predict`

Запрос:

```json
{ "payloads": ["q=books", "id=1' OR '1'='1"] }
```

Ответ содержит `total`, `attacks_detected` и `results[]` с теми же полями, что и одиночный predict (в batch часть опциональных полей может отсутствовать).

## `POST /api/v1/network/predict`

Тело JSON должно включать все числовые признаки, на которых обучена модель. Пример ключей из sample CSV:

`duration`, `tot_fwd_pkts`, `tot_bwd_pkts`, `tot_fwd_len`, `tot_bwd_len`, `fwd_pkt_len_max`, `bwd_pkt_len_max`, `flow_pkts_s`, `flow_byts_s`

Ответ:

```json
{
  "prediction": "UDP_ATTACK",
  "confidence": 0.88,
  "severity": "high",
  "recommendation": "Investigate source IP and traffic pattern",
  "model_version": "1.0.0"
}
```

## `POST /api/v1/network/upload-csv`

`multipart/form-data`, поле `file` (CSV в UTF-8). Возвращает счётчики, `top_prediction` и оценки по строкам.

## `GET /api/v1/reports/summary`

Блоки метрик `network_anomaly` и `waf_payload` (нули/примечания, если метрик артефакта нет).

## `GET /api/v1/models/status`

Статус загрузки, пути и версии каждого артефакта.

## Ошибки

Ошибки валидации и приложения возвращаются в JSON:

```json
{ "error": "InvalidInput", "message": "Payload must not be empty" }
```

Полный перечень v2-эндпоинтов (auth, alerts, drift, integrations): Swagger `http://localhost:8000/api/swagger` и [`AUTH.md`](AUTH.md).
