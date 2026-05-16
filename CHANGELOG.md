# Журнал изменений

Все значимые изменения проекта документируются в этом файле.
Формат: [Keep a Changelog](https://keepachangelog.com/ru/1.1.0/),
версионирование: [SemVer](https://semver.org/lang/ru/).

## [Unreleased]

## [2.0.0] — 2026-05-16

**MEGA-апгрейд: production-grade платформа.**

### Добавлено (бэкенд)

- **Аутентификация и авторизация**:
  - JWT access/refresh токены (Argon2id хэширование паролей).
  - API-ключи `aa_live_*` для машинных интеграций.
  - RBAC: `admin / analyst / viewer`.
  - Эндпоинты: `/api/v1/auth/login`, `/refresh`, `/logout`, `/me`, `/api-keys`.
- **База данных**: SQLAlchemy 2.0 async + Alembic + PostgreSQL/SQLite драйверы.
  Таблицы: `users`, `refresh_tokens`, `api_keys`, `predictions`, `audit_logs`,
  `alerts`, `model_runs`, `siem_endpoints`, `threat_intel_entries`.
- **Наблюдаемость**:
  - Structlog (JSON в prod, ANSI в dev).
  - Request-ID middleware (`X-Request-ID` в логах и ответах).
  - Prometheus `/metrics` (HTTP, predictions, drift, auth, alerts).
  - Health-чеки: `/health`, `/health/live`, `/health/ready`.
  - Sentry интеграция (опционально через `SENTRY_DSN`).
- **Rate limiting** через slowapi (in-memory или Redis).
- **Audit middleware**: каждый запрос → `audit_logs`.
- **ML расширения**:
  - Реестр моделей с версионированием и hot-swap (`/api/v1/ml/registry`).
  - Детектор дрейфа (PSI, KS, Chi²) — `/api/v1/drift/{module}`.
  - Isolation Forest как unsupervised «второе мнение».
  - Объяснимость предсказаний (top n-грамм / feature importances).
  - Калибровка вероятностей (CalibratedClassifierCV).
- **Интеграции**:
  - SIEM dispatcher (Splunk HEC + ArcSight CEF + Bearer-токены).
  - Threat Intelligence: CRUD + CSV-импорт + lookup.
  - Alert Manager: in-memory pub-sub + WebSocket для live-стриминга.
- **Новые роутеры**: `auth`, `users`, `audit`, `alerts` (REST + WS), `drift`,
  `integrations`, `models_registry`.
- **Lifespan**: автоматическая инициализация БД + bootstrap admin.
- Расширенный `Settings`: 30+ параметров, computed-fields, валидаторы.
- 8 новых тестов для auth, drift, registry, isolation_forest, alert_manager, siem.

### Добавлено (фронтенд)

- **AuthContext** + `useAuth` hook + JWT в localStorage.
- **ProtectedRoute** с проверкой ролей.
- Страницы: `/login`, `/alerts` (WebSocket-стрим), `/admin/audit`.
- Хук `useAlertsStream` с авто-реконнектом.
- Хук `useTheme` (light/dark/system) + `ThemeToggle` компонент.
- API-клиент `authApi` (login/refresh/logout/api-keys).
- Axios interceptor для Bearer-токена.

### Добавлено (DevOps)

- **Multi-stage Dockerfile** для backend (~150MB вместо ~600MB).
- **Multi-stage Dockerfile** для frontend (nginx production).
- Non-root user в обоих образах.
- `HEALTHCHECK` в Dockerfile.
- **Docker Compose v2** полный стек: backend + frontend + Postgres 16 + Redis 7
  + Prometheus + Grafana с автопровижингом дашборда.
- Pre-commit hooks: ruff, bandit, gitleaks, prettier, trailing whitespace.
- CI: `backend-ci` (lint + bandit + pytest+coverage + pip-audit),
  `security.yml` (weekly Trivy + dependency-review), `release.yml`
  (GHCR push на тег).

### Добавлено (документация)

- `docs/MEGA_PLAN.md` — master-план эволюции (6 фаз).
- `docs/AUTH.md` — модель безопасности.
- `docs/MONITORING.md` — Prometheus + Grafana + структурированные логи.
- `docs/INTEGRATION.md` — SIEM (JSON/CEF) + Threat Intel.
- `docs/DRIFT.md` — детектор дрейфа (PSI/KS/χ²).
- `CHANGELOG.md` — этот файл.
- `CONTRIBUTING.md` — гайдлайны разработки.

### Изменено

- `Settings`: добавлены 30+ полей, разбиение по группам (DB, JWT, Redis, ML, SIEM).
- `main.py`: middleware-стек (RequestId → Prometheus → CORS → Audit → SlowAPI).
- Версия backend пакета: 1.0.0 → **2.0.0**.

### Совместимость

- Все эндпоинты `/api/v1/*` v1 сохраняют формат запросов/ответов.
- В ответе появляется заголовок `X-Request-ID`.
- В режиме `AUTH_REQUIRED=false` (default в dev) защищённые эндпоинты
  пропускают анонимного `viewer` — для совместимости с демо-режимом фронта.

## [1.0.0] — 2024-XX-XX

- Первая публичная версия: FastAPI + sklearn (TF-IDF+LogReg, MinMaxScaler+RandomForest),
  React 19 console, Vite landing, Docker Compose, Vercel monolit deploy.
