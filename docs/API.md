# HTTP API

Base URL (local): `http://localhost:8000`

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

Request:

```json
{ "payload": "id=1' OR '1'='1" }
```

Response (shape):

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

Request:

```json
{ "payloads": ["q=books", "id=1' OR '1'='1"] }
```

Response includes `total`, `attacks_detected`, and `results[]` with the same fields as single predict (batch items omit some optional fields).

## `POST /api/v1/network/predict`

JSON body must include all trained feature keys (numeric). Example keys from the sample CSV:

`duration`, `tot_fwd_pkts`, `tot_bwd_pkts`, `tot_fwd_len`, `tot_bwd_len`, `fwd_pkt_len_max`, `bwd_pkt_len_max`, `flow_pkts_s`, `flow_byts_s`

Response:

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

`multipart/form-data` with field `file` (UTF‑8 CSV). Returns counts, `top_prediction`, and per-row scores.

## `GET /api/v1/reports/summary`

Returns `network_anomaly` and `waf_payload` metric blocks (zeros/notes when no artifact metrics exist).

## `GET /api/v1/models/status`

Returns load status, paths, and versions for each artifact.

## Errors

Validation and application errors return JSON:

```json
{ "error": "InvalidInput", "message": "Payload must not be empty" }
```
