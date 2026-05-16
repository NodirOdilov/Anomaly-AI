# Anomaly AI — backend

Сервис FastAPI: health, info, скоринг WAF payload, пакетный скоринг сетевых CSV, отчёты и статус моделей.

## Быстрый старт

```bash
cd backend
pip install -r requirements-dev.txt
$env:PYTHONPATH="src"   # PowerShell
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Обучение демо-моделей

```bash
$env:PYTHONPATH="src"
python -m anomaly_ai.waf_payload.train --config configs/waf_payload.yaml
python -m anomaly_ai.network_anomaly.train --config configs/network_anomaly.yaml
```

## Примеры CLI

```bash
python -m anomaly_ai.waf_payload.predict --payload "id=1' OR '1'='1"
python -m anomaly_ai.network_anomaly.predict --model models/network_anomaly_model.joblib --input data/samples/sample_network_flows.csv
```

## Структура

- `src/anomaly_ai/` — код приложения
- `configs/` — YAML для обучения и приложения
- `data/` — образцы и опциональные датасеты
- `models/` — артефакты joblib (генерируются)
- `tests/` — pytest

Документация эндпоинтов: `docs/API.md`.
