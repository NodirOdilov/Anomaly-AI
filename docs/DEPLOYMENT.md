# Deployment

## Local development

### Backend

```bash
cd backend
python -m venv .venv
# activate venv (OS-specific)
pip install -r requirements-dev.txt
set PYTHONPATH=src   # PowerShell: $env:PYTHONPATH="src"
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Marketing landing

```bash
cd landing
npm install
npm run dev
```

Runs on port **5174** by default. Configure `landing/.env` from `landing/.env.example` for dashboard/API/repo links in CTAs.

### Frontend (analyst console)

```bash
cd frontend
npm install
npm run dev
```

Set `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Docker Compose (demo)

From repository root:

```bash
docker compose up --build
```

- Backend listens on `8000`.
- Frontend dev server listens on `5173`.
- The browser still calls the API at `http://localhost:8000` (host networking from the user’s machine).

## Environment variables

### Backend (`backend/.env.example`)

- `APP_ENV`, `APP_NAME`, `APP_VERSION`
- `MODEL_DIR` (default `models`)
- `DATA_DIR` (default `data`)

### Frontend (`frontend/.env.example`)

- `VITE_API_BASE_URL`

## Vercel (single project)

The repository root includes a Vercel-oriented layout:

- `vercel.json` — `framework: null` (Other preset), `installCommand` (uses **`uv pip install --system`** so dependencies install on Vercel’s PEP 668 / uv-managed Python; plain `pip install` fails), `buildCommand`, SPA rewrites for `/docs/*` and `/console/*`, and Python function duration.
- `api/index.py` — sets `BACKEND_ROOT` to `./backend`, extends `PYTHONPATH`, and exports the FastAPI `app` (required under `api/` so `vercel.json` `functions` glob matches; Vercel CLI 51+ rejects root `server.py` in `functions`).
- Root `requirements.txt` — duplicate of `backend/requirements.txt` (Vercel’s parser does not support `-r` includes from another file).
- `scripts/vercel-build.mjs` — builds `landing/` into `public/` and `frontend/` into `public/console/` (with `VITE_BASE=/console/`). The `public/` folder is build output and may stay gitignored locally; it is generated during Vercel build and then served from the CDN.

**GitHub import:** connect the repo and deploy with defaults. Root directory should stay the repository root; no manual env vars are required for CORS (when `VERCEL` is set, the API uses permissive CORS without cookies, matching the SPA clients).

If the Vercel UI suggests **“Services”** / `experimentalServices`, prefer **Other** (single project) with root **`.`**: this repo relies on **`public/`** for the landing and SPAs on the CDN, and the Python handler (`api/index.py`) only for API paths. Putting FastAPI on `routePrefix: "/"` via `experimentalServices` sends **every** request (including `/`) to Python, which has no `GET /` route, so the site shows `{"detail":"Not Found"}`. Use **`functions`** targeting **`api/index.py`** for `maxDuration`, not root `server.py` (CLI 51+ does not match root files in `functions`).

After deploy:

- Marketing site: `/`
- In-app docs (landing SPA): `/docs/*`
- Analyst console: `/console/*`
- API: `/health`, `/api/v1/*`
- Swagger UI: `/api/swagger` (marketing `/docs` is reserved for the React docs site)

Serverless limits (cold start, duration, bundle size) apply; heavy ML workloads may still be better on Docker or a dedicated API host.

## Notes

- Mount `backend/models` and `backend/data` as volumes when you want persistent artifacts and datasets inside containers.
- For production you would typically serve the Vite `dist/` build behind a reverse proxy, not the dev server.
