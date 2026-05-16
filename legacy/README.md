# Legacy (v1.x)

> Архив первой версии Anomaly AI. **Не** используется в production v2.0.

| Параметр | Значение |
|----------|----------|
| Статус | Только для справки и сравнения |
| Актуальный код | `backend/`, `frontend/`, `landing/` в корне |
| Репозиторий | [NodirOdilov/Anomaly-AI](https://github.com/NodirOdilov/Anomaly-AI) |

## Содержание

1. [Состав каталога](#состав-каталога)
2. [Отличия от v2.0](#отличия-от-v20)
3. [Запуск (исторический)](#запуск-исторический)

---

## Состав каталога

| Путь | Назначение |
|------|------------|
| `backend/` | FastAPI v1, без auth/PostgreSQL |
| `frontend/` | React-консоль v1 |
| `docker-compose.yml` | Минимальный стек v1 |

---

## Отличия от v2.0

| Аспект | v1 (legacy) | v2 (текущий) |
|--------|-------------|--------------|
| База данных | Нет | PostgreSQL + Alembic |
| Аутентификация | Нет | JWT, RBAC, API keys |
| Наблюдаемость | Минимум | Prometheus, Grafana, structlog |
| Интеграции | Нет | SIEM, Alertmanager, drift API |
| CI/CD | Базовый | Lint, security, release workflows |

---

## Запуск (исторический)

```bash
cd legacy
docker compose up --build
```

Для новых разработок используйте корневой [`docker-compose.yml`](../docker-compose.yml) и [`README.md`](../README.md).

---

## См. также

- [`CHANGELOG.md`](../CHANGELOG.md) — миграция на v2.0
- [`docs/ARCHITECTURE.md`](../docs/ARCHITECTURE.md)
