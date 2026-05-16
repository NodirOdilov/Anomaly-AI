# Landing — Anomaly AI

> Маркетинговый сайт и встроенная техническая документация (`/docs`).

| Параметр | Значение |
|----------|----------|
| Стек | Vite, React, TypeScript, Tailwind 4, Framer Motion |
| Порт (dev) | `5174` |
| Репозиторий | [NodirOdilov/Anomaly-AI](https://github.com/NodirOdilov/Anomaly-AI) |

## Содержание

1. [Разработка](#разработка)
2. [Переменные окружения](#переменные-окружения)
3. [Сборка и деплой](#сборка-и-деплой)
4. [Документация в приложении](#документация-в-приложении)

---

## Разработка

```bash
cd landing
npm install
cp .env.example .env
npm run dev
```

| Сервис | URL (локально) |
|--------|----------------|
| Landing | `http://localhost:5174` |
| Консоль | `http://localhost:5173` |
| API | `http://localhost:8000` |

---

## Переменные окружения

Скопируйте `.env.example` в `.env`:

| Переменная | Назначение | По умолчанию |
|------------|------------|--------------|
| `VITE_DASHBOARD_URL` | Ссылка на консоль | `http://localhost:5173` |
| `VITE_API_URL` | FastAPI | `http://localhost:8000` |
| `VITE_REPO_URL` | GitHub (CTA, docs) | `https://github.com/NodirOdilov/Anomaly-AI` |

---

## Сборка и деплой

```bash
npm run build
npm run preview
```

Выход: `dist/` — любой static-хостинг или CDN.

Для SPA настройте fallback всех путей на `index.html` (нужно для `/docs/...`).

---

## Документация в приложении

| Раздел | URL |
|--------|-----|
| Техническое руководство (RU) | `http://localhost:5174/docs` |
| API в репозитории | `docs/API.md` на GitHub |

Кнопка CTA «Документация» ведёт на `/docs`.

---

## См. также

- [`frontend/README.md`](../frontend/README.md)
- [`docs/DEPLOYMENT.md`](../docs/DEPLOYMENT.md)
