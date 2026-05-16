# Отчёт: сетевые аномалии

> Генерируется пайплайном `network_anomaly`. Нули в API означают отсутствие оценённого артефакта на диске.

| Параметр | Значение |
|----------|----------|
| Команда | `python -m anomaly_ai.network_anomaly.train` |
| Конфиг | `configs/network_anomaly.yaml` |
| Артефакт | `models/network_anomaly_model.joblib` |

## Статус

| Элемент | Состояние |
|---------|-----------|
| Демо-CSV | `data/samples/sample_network_flows.csv` — только smoke-тест |
| Production-метрики | Требуют `train` + `evaluate` на ваших данных |

---

## Метрики

| Метрика | Значение |
|---------|----------|
| Accuracy / F1 | — |
| FPR / FNR | — |
| Confusion matrix | — |
| Дата оценки | — |

Запустите обучение и оценку, затем обновите таблицу и JSON в артефакте.

---

## См. также

- [`../models/README.md`](../models/README.md)
- [`../../docs/DRIFT.md`](../../docs/DRIFT.md)
- [`../../docs/MODEL_CARD.md`](../../docs/MODEL_CARD.md)
