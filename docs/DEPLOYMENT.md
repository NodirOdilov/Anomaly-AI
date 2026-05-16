# Развёртывание

> Сценарии запуска: локальная разработка, Docker Compose, Vercel (демо), production-заметки.

| Параметр | Значение |
|----------|----------|
| Compose | корневой `docker-compose.yml` |
| Backend env | `backend/.env.example` |
| Репозиторий | [NodirOdilov/Anomaly-AI](https://github.com/NodirOdilov/Anomaly-AI) |

## Содержание

1. [Локальная разработка](#локальная-разработка)
2. [Docker Compose](#docker-compose)
3. [Переменные окружения](#переменные-окружения)
4. [Vercel (один проект)](#vercel-один-проект)
5. [Production-заметки](#production-заметки)

---

## Локальная разработка

### Бэкенд

```bash
cd backend
python -m venv .venv
# активировать venv
pip install -r requirements-dev.txt
```

**PowerShell:** `$env:PYTHONPATH = "src"`  
**bash:** `export PYTHONPATH=src`

```bash
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

| Сервис | URL |
|--------|-----|
| API | `http://localhost:8000` |
| Swagger | `http://localhost:8000/api/swagger` |

### Landing

```bash
cd landing
npm install
cp .env.example .env
npm run dev
```

Порт по умолчанию: **5174**. CTA-ссылки — из `landing/.env`.

### Frontend (консоль)

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

`frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Порт: **5173**.

---

## Docker Compose

Из корня репозитория:

```bash
docker compose up --build
```

| Сервис | Порт (хост) |
|--------|-------------|
| API | 8000 |
| Frontend dev | 5173 |
| Postgres | 5432 |
| Redis | 6379 |
| Prometheus | 9090 |
| Grafana | 3000 |

Браузер обращается к API по `http://localhost:8000`.

---

## Переменные окружения

### Бэкенд (`backend/.env.example`)

| Группа | Ключи (примеры) |
|--------|-----------------|
| Приложение | `APP_ENV`, `APP_NAME`, `APP_VERSION` |
| Пути | `MODEL_DIR`, `DATA_DIR` |
| БД | `DATABASE_URL` |
| Auth | `AUTH_REQUIRED`, `JWT_SECRET`, `BOOTSTRAP_ADMIN_*` |
| SIEM | `SIEM_WEBHOOK_*` |
| Наблюдаемость | `LOG_JSON`, `SENTRY_DSN` |

Полный список — в файле `.env.example`.

### Frontend

| Переменная | Назначение |
|------------|------------|
| `VITE_API_BASE_URL` | URL FastAPI |

---

## Vercel (один проект)

| Файл | Назначение |
|------|------------|
| `vercel.json` | build, rewrites `/docs/*`, `/console/*`, Python function |
| `api/index.py` | Экспорт FastAPI (`BACKEND_ROOT=./backend`) |
| `requirements.txt` | Зависимости backend (корень, для парсера Vercel) |
| `scripts/vercel-build.mjs` | Сборка landing → `public/`, frontend → `public/console/` |

**Импорт:** root = `.`, framework **Other** (не experimentalServices для всего трафика — иначе `GET /` уйдёт в Python без маршрута).

После деплоя:

| Путь | Назначение |
|------|------------|
| `/` | Landing |
| `/docs/*` | Встроенная документация (SPA) |
| `/console/*` | Аналитическая консоль |
| `/health`, `/api/v1/*` | API |
| `/api/swagger` | OpenAPI (не путать с `/docs` SPA) |

Ограничения serverless: cold start, duration, размер бандла. Тяжёлый ML — Docker или выделенный API-хост.

---

## Production-заметки

| Тема | Рекомендация |
|------|--------------|
| Статика | Собранный Vite `dist/` за reverse proxy, не dev-сервер |
| Модели и данные | Volume на `backend/models`, `backend/data` |
| Секреты | `JWT_SECRET`, пароли БД — только через secret manager |
| Auth | `AUTH_REQUIRED=true` |
| Мониторинг | [`MONITORING.md`](MONITORING.md) |

---

## См. также

- [`AUTH.md`](AUTH.md)
- [`../docker-compose.yml`](../docker-compose.yml)
- [`../backend/README.md`](../backend/README.md)
