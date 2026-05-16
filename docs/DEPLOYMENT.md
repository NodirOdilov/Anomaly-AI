# Развёртывание

## Локальная разработка

### Бэкенд

```bash
cd backend
python -m venv .venv
# активировать venv (зависит от ОС)
pip install -r requirements-dev.txt
set PYTHONPATH=src   # PowerShell: $env:PYTHONPATH="src"
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Маркетинговый лендинг

```bash
cd landing
npm install
npm run dev
```

По умолчанию порт **5174**. Настройте `landing/.env` из `landing/.env.example` для ссылок на консоль/API/репозиторий в CTA.

### Фронтенд (аналитическая консоль)

```bash
cd frontend
npm install
npm run dev
```

Файл `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Docker Compose (демо)

Из корня репозитория:

```bash
docker compose up --build
```

- Backend слушает `8000`.
- Dev-сервер frontend — `5173`.
- Браузер по-прежнему обращается к API по `http://localhost:8000` (сеть хоста).

## Переменные окружения

### Бэкенд (`backend/.env.example`)

- `APP_ENV`, `APP_NAME`, `APP_VERSION`
- `MODEL_DIR` (по умолчанию `models`)
- `DATA_DIR` (по умолчанию `data`)

### Фронтенд (`frontend/.env.example`)

- `VITE_API_BASE_URL`

## Vercel (один проект)

В корне репозитория подготовлена конфигурация для Vercel:

- `vercel.json` — `framework: null` (пресет Other), `installCommand` (использует **`uv pip install --system`**, т. к. на Vercel PEP 668 / uv-managed Python обычный `pip install` может падать), `buildCommand`, SPA-rewrite для `/docs/*` и `/console/*`, длительность Python-функции.
- `api/index.py` — задаёт `BACKEND_ROOT` в `./backend`, расширяет `PYTHONPATH`, экспортирует FastAPI `app` (нужен в `api/`, чтобы glob `functions` в `vercel.json` совпадал; Vercel CLI 51+ не принимает корневой `server.py` в `functions`).
- Корневой `requirements.txt` — копия `backend/requirements.txt` (парсер Vercel не поддерживает `-r` из другого файла).
- `scripts/vercel-build.mjs` — собирает `landing/` в `public/` и `frontend/` в `public/console/` (`VITE_BASE=/console/`). Папка `public/` — артефакт сборки, может быть в `.gitignore` локально; на Vercel генерируется при build и отдаётся с CDN.

**Импорт с GitHub:** подключите репозиторий и деплойте с настройками по умолчанию. Root directory — корень репозитория; для CORS отдельные env не нужны (при `VERCEL` API использует открытый CORS без cookies, как SPA-клиенты).

Если UI Vercel предлагает **«Services»** / `experimentalServices`, предпочтите **Other** (один проект) с корнем **`.`**: репозиторий опирается на **`public/`** для лендинга и SPA на CDN, а Python-обработчик (`api/index.py`) — только для путей API. FastAPI с `routePrefix: "/"` через `experimentalServices` отправляет **все** запросы (включая `/`) в Python, где нет маршрута `GET /`, и сайт отвечает `{"detail":"Not Found"}`. Для `maxDuration` используйте **`functions`** с **`api/index.py`**, не корневой `server.py`.

После деплоя:

- Маркетинг: `/`
- Встроенная документация (landing SPA): `/docs/*`
- Аналитическая консоль: `/console/*`
- API: `/health`, `/api/v1/*`
- Swagger UI: `/api/swagger` (маркетинговый путь `/docs` зарезервирован под React-документацию)

Действуют лимиты serverless (cold start, duration, размер бандла); тяжёлый ML лучше на Docker или выделенном API-хосте.

## Замечания

- Смонтируйте `backend/models` и `backend/data` как volumes, если нужны постоянные артефакты и датасеты в контейнерах.
- В production обычно отдают собранный Vite `dist/` за reverse proxy, а не dev-сервер.
