# Architecture

Anomaly AI is a small monorepo for **defensive** ML-assisted detection:

```text
React dashboard (Vite) → FastAPI HTTP API → sklearn inference services → joblib artifacts → reports/metrics
```

## Backend

- **API layer** (`anomaly_ai.api`): routing, validation, error shaping, CORS.
- **Services** (`anomaly_ai.services`): artifact loading, reporting, lightweight prediction history.
- **ML modules**:
  - `anomaly_ai.waf_payload`: TF‑IDF (character n‑grams) + logistic regression; optional rule hints for labeling.
  - `anomaly_ai.network_anomaly`: numeric cleaning + scaling + RandomForest pipeline.

Artifacts are dictionaries saved with `joblib` containing the estimator, feature metadata, label maps, version, timestamps, and evaluation metrics (when trained).

## Frontend

- React + TypeScript + Vite + Tailwind.
- Axios client with `VITE_API_BASE_URL`.
- Pages for dashboard, analyzers, reports, and in-app documentation.

## Deployment

- Local: run backend with uvicorn and frontend with Vite.
- Docker Compose builds both images and exposes ports `8000` and `5173`.

See `DEPLOYMENT.md` for operational detail.
