# Отчёт: WAF payload

> Генерируется пайплайном обучения `waf_payload`. Обновляйте после каждого прогона на авторизованных данных.

| Параметр | Значение |
|----------|----------|
| Команда | `python -m anomaly_ai.waf_payload.train` |
| Конфиг | `configs/waf_payload.yaml` |
| Артефакт | `models/waf_payload_model.joblib` |

## Статус

| Элемент | Состояние |
|---------|-----------|
| Демо-выборка | `data/samples/sample_payloads.json` — проверка конвейера |
| Production-метрики | Заполняются после обучения на вашем корпусе |

---

## Метрики

После обучения зафиксируйте здесь и в поле `metrics` joblib-артефакта:

| Метрика | Значение |
|---------|----------|
| Accuracy | — |
| Precision (macro) | — |
| Recall (macro) | — |
| F1 (macro) | — |
| Дата оценки | — |
| Размер train / val | — |

---

## См. также

- [`../models/README.md`](../models/README.md)
- [`../../docs/MODEL_CARD.md`](../../docs/MODEL_CARD.md)
- [`../../docs/DATASETS.md`](../../docs/DATASETS.md)
