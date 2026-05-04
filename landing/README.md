# Anomaly AI — marketing landing

Premium, standalone landing page for visitors and stakeholders. Built with **Vite + React + TypeScript + Tailwind v4 + Framer Motion**.

## Develop

```bash
cd landing
npm install
npm run dev
```

Serves on **http://localhost:5174** by default (dashboard stays on 5173).

## Configure CTAs

Copy `.env.example` → `.env` and set:

- `VITE_DASHBOARD_URL` — React console (default `http://localhost:5173`)
- `VITE_API_URL` — FastAPI base (default `http://localhost:8000`)
- `VITE_REPO_URL` — GitHub root for linking `docs/API.md`

## Build

```bash
npm run build
npm run preview
```

Static output is in `dist/` — deploy to any CDN or static host.

## Scientific documentation (in-app)

The marketing site includes a full **Russian-language** technical manual for researchers: open **http://localhost:5174/docs** (or your deployed origin + `/docs`). The CTA button *Read the API docs* routes there.

Configure SPA hosting so all paths fall back to `index.html` (required for direct loads of `/docs/...`).
