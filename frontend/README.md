# Frontend — Anomaly AI

> Аналитическая консоль: React 19, TypeScript, Vite 8, Tailwind 4.

| Параметр | Значение |
|----------|----------|
| Стек | React, TypeScript, Vite, Tailwind, Axios |
| Порт (dev) | `5173` |
| Backend API | `VITE_API_BASE_URL` (см. `.env`) |
| Репозиторий | [NodirOdilov/Anomaly-AI](https://github.com/NodirOdilov/Anomaly-AI) |

## Содержание

1. [Быстрый старт](#быстрый-старт)
2. [Переменные окружения](#переменные-окружения)
3. [Production-сборка](#production-сборка)
4. [Маршруты приложения](#маршруты-приложения)

---

## Быстрый старт

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Приложение: `http://localhost:5173`

---

## Переменные окружения

Файл `.env` (из `.env.example`):

| Переменная | Назначение | Пример |
|------------|------------|--------|
| `VITE_API_BASE_URL` | Базовый URL FastAPI | `http://localhost:8000` |

---

## Production-сборка

```bash
npm run build
npm run preview
```

Статика в `dist/`. В Docker — nginx-образ из `frontend/Dockerfile`.

---

## Маршруты приложения

| Маршрут | Назначение | Доступ |
|---------|------------|--------|
| `/` | Дашборд | Открытый |
| `/waf` | Анализатор payload | Открытый |
| `/network` | Анализ CSV потоков | Открытый |
| `/reports` | Метрики и графики | Открытый |
| `/alerts` | Поток алертов (WebSocket) | Открытый |
| `/docs` | Встроенная справка | Открытый |
| `/login` | Вход | Публичный |
| `/admin/audit` | Журнал аудита | admin, analyst |

---

## См. также

- [`backend/README.md`](../backend/README.md)
- [`docs/API.md`](../docs/API.md)
- [`docs/AUTH.md`](../docs/AUTH.md)
