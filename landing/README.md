# Anomaly AI — маркетинговый лендинг

Отдельная премиальная посадочная страница для посетителей и стейкхолдеров. Стек: **Vite + React + TypeScript + Tailwind v4 + Framer Motion**.

## Разработка

```bash
cd landing
npm install
npm run dev
```

По умолчанию: **http://localhost:5174** (консоль аналитика — 5173).

## Настройка CTA

Скопируйте `.env.example` → `.env`:

- `VITE_DASHBOARD_URL` — React-консоль (по умолчанию `http://localhost:5173`)
- `VITE_API_URL` — базовый URL FastAPI (по умолчанию `http://localhost:8000`)
- `VITE_REPO_URL` — корень GitHub (по умолчанию `https://github.com/NodirOdilov/Anomaly-AI`)

## Сборка

```bash
npm run build
npm run preview
```

Статика в `dist/` — деплой на любой CDN или static-хостинг.

## Научная документация (в приложении)

На сайте есть полное **русскоязычное** техническое руководство для исследователей: **http://localhost:5174/docs** (или ваш origin + `/docs`). Кнопка CTA *Документация API* ведёт туда.

Для SPA настройте fallback всех путей на `index.html` (нужно для прямых заходов на `/docs/...`).
