# Anomaly AI

**Платформа обнаружения сетевых аномалий и веб-атак на основе машинного обучения**

Anomaly AI — это защитно ориентированная (defensive) платформа кибербезопасности, использующая машинное обучение для выявления аномалий сетевого трафика и вредоносных веб-payload’ов: SQL-инъекции, XSS, обходы путей (path traversal), попытки обхода WAF и сходные паттерны. В состав решения входят backend на FastAPI, сервисы ML-инференса, интерфейс командной строки, развёртывание через Docker, интерактивная консоль на React, публичный маркетинговый лендинг и документация для инженеров и аналитиков.

## Обзор

Проект оформлен как **monorepo** уровня портфолио: исходные эксперименты из каталогов `legacy/anom` и `legacy/ngfw` преобразованы в **воспроизводимый** стек — **FastAPI**, артефакты **scikit-learn** (joblib), **React**-консоль, **Docker**, автотесты и структурированная документация.

## Ключевые возможности

- Классификация веб-payload’ов в духе WAF: **TF‑IDF** по символьным **n‑граммам** + **логистическая регрессия**, с осторожными эвристиками (rule hints) только для **классификации**, без исполнения кода.
- Демонстрационная классификация сетевых потоков: предобработка числовых признаков + конвейер **RandomForest**.
- Прозрачные метрики: на «чистой» копии репозитория возможны нули и пояснения до обучения на ваших данных — без искусного завышения точности.
- Точки входа CLI для обучения, оценки и предсказания; набор тестов **pytest**.

## Модули

- **Обнаружение сетевых аномалий** — оценка признаков из CSV; в примерах метки вида `BENIGN`, `HTTP_ATTACK`, `UDP_ATTACK`.
- **Детектирование WAF-payload’ов** — строковые payload’ы и многоклассовые метки; эвристики используются **исключительно в защитных целях**.

## Архитектура

Подробности — в [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

```text
Frontend → HTTP API (FastAPI) → ML-сервисы → артефакты joblib → отчёты и метрики
```

## Технологический стек

- **Backend:** Python 3.11+, FastAPI, Pydantic, scikit-learn, pandas, joblib, Uvicorn, pytest.
- **Frontend (консоль аналитика):** React, TypeScript, Vite, Tailwind CSS, React Router, Axios, Recharts.
- **Landing (маркетинг):** React, TypeScript, Vite, Tailwind CSS, Framer Motion.
- **DevOps:** Docker Compose, GitHub Actions.

## Структура репозитория

```text
backend/   FastAPI, ML, CLI, тесты
frontend/  React-консоль для анализа
landing/   Публичный маркетинговый сайт (Vite + Framer Motion)
docs/      Архитектура, API, датасеты, model card, развёртывание, roadmap
legacy/    Архив ранних прототипов
```

## Быстрый старт

### Backend

```bash
cd backend
pip install -r requirements-dev.txt
# PowerShell: задайте путь к пакету
$env:PYTHONPATH="src"
python -m pytest
uvicorn anomaly_ai.api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (консоль)

```bash
cd frontend
npm install
npm run build
npm run dev
```

Скопируйте `frontend/.env.example` в `frontend/.env` и укажите `VITE_API_BASE_URL` (например, `http://localhost:8000`).

### Маркетинговый лендинг

```bash
cd landing
npm install
npm run dev
```

По умолчанию интерфейс доступен по адресу **http://localhost:5174**. Настройка ссылок для кнопок (консоль, API, репозиторий) — в [`landing/README.md`](landing/README.md) и в `landing/.env.example` (`VITE_DASHBOARD_URL`, `VITE_API_URL`, `VITE_REPO_URL`).

### Docker

```bash
docker compose up --build
```

## Примеры запросов к API

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/info
curl -X POST http://localhost:8000/api/v1/waf/predict -H "Content-Type: application/json" -d "{\"payload\":\"id=1' OR '1'='1\"}"
```

Полное описание методов — в [`docs/API.md`](docs/API.md).

## Примеры CLI

```bash
cd backend
$env:PYTHONPATH="src"
python -m anomaly_ai.waf_payload.train --config configs/waf_payload.yaml
python -m anomaly_ai.network_anomaly.train --config configs/network_anomaly.yaml
python -m anomaly_ai.waf_payload.predict --payload "id=1' OR '1'='1"
python -m anomaly_ai.network_anomaly.predict --model models/network_anomaly_model.joblib --input data/samples/sample_network_flows.csv
```

## Данные

Примеры лежат в `backend/data/samples/`. Они предназначены **только для демонстрации** конвейера обучения и инференса. Описание форматов и ограничений — в [`docs/DATASETS.md`](docs/DATASETS.md).

## Оценка моделей

Скрипты обучения записывают метрики в артефакты. Результаты на малых демо-выборках **нельзя** автоматически переносить на промышленную эксплуатацию. См. [`docs/MODEL_CARD.md`](docs/MODEL_CARD.md).

## Развёртывание

Сценарии локального и контейнерного запуска — в [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md); оркестрация — в корневом `docker-compose.yml`.

### Vercel (монолитный деплой)

В корне репозитория лежат `vercel.json`, `api/index.py` (точка входа FastAPI для рантайма Vercel; каталог `api/` требуется для поля `functions` в `vercel.json`) и скрипт `npm run vercel-build`, который собирает лендинг и консоль в каталог `public/` (консоль доступна по префиксу **`/console`**).

**Импорт из GitHub:** подключите репозиторий и нажмите Deploy. Корень репозитория по умолчанию уже совпадает с корнем monorepo — **отдельно менять Root Directory, Build/Install Command и переменные окружения не требуется** (всё задано в `vercel.json`; CORS на Vercel включается автоматически по переменной `VERCEL`).

После выкладки на одном домене работают:

- **`/`** — маркетинговый лендинг;
- **`/docs/*`** — встроенная документация (SPA);
- **`/console/*`** — консоль аналитика (SPA, `basename` настроен под префикс);
- **`/health`**, **`/api/v1/*`** — FastAPI;
- интерактивная OpenAPI — **`/api/swagger`** (путь **`/docs`** у FastAPI отключён, чтобы не пересекаться с маркетингом).

Учтите лимиты serverless: холодный старт с **scikit-learn** может быть долгим; в `vercel.json` для функции задано **до 60 с** выполнения. Для постоянной высокой нагрузки по-прежнему уместны Docker или отдельный API-хостинг.

## Безопасность и правовые аспекты

Проект рассчитан **исключительно на защитное применение** (образование, исследования, портфолио, анализ данных, на которые у вас есть права). Ознакомьтесь с [`SECURITY.md`](SECURITY.md). **Не используйте** платформу для несанкционированных атак, сканирования или обхода средств защиты.

## Ограничения

- Демонстрационные наборы данных малы и **не отражают** реальное распределение угроз и трафика.
- Без мониторинга дрейфа и регулярной переподготовки модели устаревают; в версии 1.0 нет полноценного production-мониторинга.
- Эвристические подсказки **не заменяют** промышленный WAF, SIEM и политики журналирования.

## Дорожная карта

[`docs/ROADMAP.md`](docs/ROADMAP.md)

## Авторство

Репозиторий ведётся как открытый проект портфолио / учебная работа. При публикации укажите в этом разделе своё имя и контакты при необходимости.
