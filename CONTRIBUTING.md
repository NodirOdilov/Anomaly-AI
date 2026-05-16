# Гайдлайны разработки

Спасибо за интерес к Anomaly AI. Этот документ описывает рабочий процесс
для контрибьюторов.

**Репозиторий:** [github.com/NodirOdilov/Anomaly-AI](https://github.com/NodirOdilov/Anomaly-AI)  
**Автор:** [Nodir Odilov](https://github.com/NodirOdilov)

## Архитектурные принципы

1. **Только защита.** Мы строим инструменты обнаружения, а не эксплуатации.
   Любые правила и эвристики должны быть классификаторами, а не генераторами.
2. **Честные метрики.** Никаких подкрашенных цифр. Если на демо-данных
   точность 70% — пишем 70%.
3. **Тесты не опциональны.** Каждая публичная функция должна иметь хотя бы
   smoke-тест. Целевое покрытие: ≥ 80%.
4. **Без хайпа.** Не добавляйте глубокое обучение ради красивого слова, если
   sklearn-конвейер решает задачу.

## Локальное окружение

### Бэкенд

```bash
cd backend
python -m venv .venv
source .venv/bin/activate            # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt

# Применить миграции:
alembic upgrade head

# Запустить:
$env:PYTHONPATH="src"
uvicorn anomaly_ai.api.main:app --reload
```

### Фронтенд

```bash
cd frontend
npm install
cp .env.example .env  # отредактируйте VITE_API_BASE_URL
npm run dev
```

### Лендинг

```bash
cd landing
npm install
npm run dev
```

### Полный стек

```bash
docker compose up --build
# backend  → http://localhost:8000
# frontend → http://localhost:5173
# grafana  → http://localhost:3000
```

## Стиль кода

### Python

- **Ruff** — линтер и форматтер. Конфиг в `backend/pyproject.toml`.
- **Mypy** — типизация. Не обязательна везде, но публичные функции должны
  быть типизированы.
- **Bandit** — security-сканер. Не игнорировать предупреждения без причины.

```bash
cd backend
ruff check src tests --fix
ruff format src tests
mypy src
bandit -c pyproject.toml -r src
```

### TypeScript

- **ESLint** + **prettier**.
- Строгий режим TypeScript.

```bash
cd frontend
npm run lint
```

### Хуки pre-commit

```bash
pip install pre-commit
pre-commit install
```

Перед коммитом запускаются: ruff, ruff-format, bandit, gitleaks, prettier.

## Запросы на слияние (Pull Request)

1. Форк репозитория.
2. Создайте ветку: `git checkout -b feature/<short-name>`.
3. Коммиты в формате **Conventional Commits**:
   - `feat: добавлен webhook для Datadog`
   - `fix(auth): исправлена валидация refresh-токена`
   - `docs: обновлена INTEGRATION.md`
   - `test: покрыт drift детектор chi-squared`
4. Убедитесь что:
   - Тесты проходят: `pytest`
   - Линтеры чистые: `ruff check src tests`
   - Нет утечек секретов: `gitleaks detect`
5. Откройте PR с описанием **что** и **зачем**, ссылка на issue если есть.

## Тесты

### Бэкенд

```bash
cd backend
$env:PYTHONPATH="src"
pytest                                    # все тесты
pytest -k auth                            # только auth-тесты
pytest --cov=anomaly_ai --cov-report=term # с покрытием
pytest -m "not slow"                      # пропустить медленные
```

Маркеры:

- `@pytest.mark.integration` — требует Postgres/Redis.
- `@pytest.mark.slow` — обучает модели на полных данных.

### Фронтенд

```bash
cd frontend
npm test
```

## Безопасность

Если вы нашли уязвимость:

- **Не** открывайте публичный issue.
- Свяжитесь с мейнтейнером через email или приватный security-канал
  (см. `SECURITY.md`).

## Лицензия

Проект под MIT (см. `LICENSE`). Внося контрибьюшен, вы соглашаетесь
выпускать его на тех же условиях.
