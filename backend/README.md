# Backend — Anomaly AI

> FastAPI-сервис: health, ML-инференс (WAF + network), отчёты, auth, интеграции.

| Параметр | Значение |
|----------|----------|
| Стек | Python 3.11+, FastAPI, SQLAlchemy 2, scikit-learn |
| Порт (dev) | `8000` |
| API-документация | [`docs/API.md`](../docs/API.md) |
| Репозиторий | [NodirOdilov/Anomaly-AI](https://github.com/NodirOdilov/Anomaly-AI) |

## Содержание

1. [Быстрый старт](#быстрый-старт)
2. [Обучение моделей](#обучение-моделей)
3. [CLI](#cli)
4. [Структура каталога](#структура-каталога)
5. [Качество кода](#качество-кода)

---

## Быстрый старт

```bash
cd backend
pip install -r requirements-dev.txt
```

**PowerShell:**

```powershell
$env:PYTHONPATH = "src"
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**bash:**

```bash
export PYTHONPATH=src
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

| URL | Назначение |
|-----|------------|
| `http://localhost:8000/health` | Healthcheck |
| `http://localhost:8000/api/swagger` | OpenAPI UI |

---

## Обучение моделей

```bash
$env:PYTHONPATH = "src"   # PowerShell

python -m anomaly_ai.waf_payload.train --config configs/waf_payload.yaml
python -m anomaly_ai.network_anomaly.train --config configs/network_anomaly.yaml
```

Артефакты сохраняются в `models/`. Подробнее: [`models/README.md`](models/README.md).

---

## CLI

```bash
python -m anomaly_ai.waf_payload.predict --payload "id=1' OR '1'='1"

python -m anomaly_ai.network_anomaly.predict `
  --model models/network_anomaly_model.joblib `
  --input data/samples/sample_network_flows.csv
```

---

## Структура каталога

| Путь | Назначение |
|------|------------|
| `src/anomaly_ai/` | Исходный код приложения |
| `configs/` | YAML для обучения и runtime |
| `data/` | Образцы и датасеты — [`data/README.md`](data/README.md) |
| `models/` | joblib-артефакты — [`models/README.md`](models/README.md) |
| `migrations/` | Alembic |
| `tests/` | pytest |
| `reports/` | Отчёты после обучения |

---

## Качество кода

```bash
ruff check src tests
ruff format src tests
bandit -c pyproject.toml -r src
pytest --cov=anomaly_ai
```

---

## См. также

- [`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md)
- [`docs/AUTH.md`](../docs/AUTH.md)
- [`../docker-compose.yml`](../docker-compose.yml)
