# Anomaly AI — backend

FastAPI service exposing health, info, WAF payload scoring, network CSV scoring, reports, and model status.

## Quick start

```bash
cd backend
pip install -r requirements-dev.txt
$env:PYTHONPATH="src"   # PowerShell
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

## Train demo models

```bash
$env:PYTHONPATH="src"
python -m anomaly_ai.waf_payload.train --config configs/waf_payload.yaml
python -m anomaly_ai.network_anomaly.train --config configs/network_anomaly.yaml
```

## CLI examples

```bash
python -m anomaly_ai.waf_payload.predict --payload "id=1' OR '1'='1"
python -m anomaly_ai.network_anomaly.predict --model models/network_anomaly_model.joblib --input data/samples/sample_network_flows.csv
```

## Layout

- `src/anomaly_ai/` — application code
- `configs/` — YAML training/app configuration
- `data/` — samples and optional datasets
- `models/` — joblib artifacts (generated)
- `tests/` — pytest suite

See repository `docs/API.md` for endpoint documentation.
