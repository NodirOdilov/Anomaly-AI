# Артефакты моделей (backend/models)

> Сериализованные модели scikit-learn (joblib) и метаданные для инференса и реестра.

| Параметр | Значение |
|----------|----------|
| Формат | `.joblib` (+ опционально JSON метаданные) |
| Реестр API | `POST /api/v1/models` — см. [`docs/API.md`](../../docs/API.md) |
| Карточка модели | [`docs/MODEL_CARD.md`](../../docs/MODEL_CARD.md) |

## Содержание

1. [Файлы по умолчанию](#файлы-по-умолчанию)
2. [Обучение и обновление](#обучение-и-обновление)
3. [Версионирование](#версионирование)
4. [Docker и тома](#docker-и-тома)

---

## Файлы по умолчанию

| Файл | Модуль |
|------|--------|
| `waf_payload_model.joblib` | Классификация вредоносных payload |
| `network_anomaly_model.joblib` | Isolation Forest / сетевые аномалии |

Пути переопределяются через env и `configs/*.yaml`.

---

## Обучение и обновление

```bash
cd backend
$env:PYTHONPATH = "src"

python -m anomaly_ai.waf_payload.train --config configs/waf_payload.yaml
python -m anomaly_ai.network_anomaly.train --config configs/network_anomaly.yaml
```

Отчёты: [`../reports/`](../reports/).

---

## Версионирование

| Механизм | Описание |
|----------|----------|
| Файловая система | Имена с суффиксом версии при ручном деплое |
| API registry | Активная версия на модуль — `GET /api/v1/models/{module}` |
| Drift | Эталонные распределения для PSI — [`docs/DRIFT.md`](../../docs/DRIFT.md) |

---

## Docker и тома

В `docker-compose.yml` каталог `backend/models` монтируется в контейнер API для hot-reload артефактов без пересборки образа.

---

## См. также

- [`../data/README.md`](../data/README.md)
- [`../../docs/DRIFT.md`](../../docs/DRIFT.md)
