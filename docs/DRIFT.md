# Детектор дрейфа моделей

> Раннее обнаружение деградации ML-моделей: PSI, KS, Chi-squared и интеграция с Prometheus.

| Параметр | Значение |
|----------|----------|
| API | `POST /api/v1/drift/{module}` |
| Модули | `network_anomaly`, `waf_payload` |
| Метрика | `anomaly_ai_model_drift_score` |

## Содержание

1. [Зачем](#зачем)
2. [Методы](#методы)
3. [API](#api)
4. [Prometheus и алерты](#prometheus-и-алерты)
5. [Действия при срабатывании](#действия-при-срабатывании)
6. [Программное использование](#программное-использование)

---

## Зачем

ML-модели в продакшене **деградируют**, когда:

| Причина | Пример |
|---------|--------|
| Сдвиг данных | Атакующие меняют технику |
| Новые payload | Классы вне обучающей выборки |
| Рост трафика | Меняется сетевой профиль |

Дрейф нужно поймать **до** падения качества предсказаний.

---

## Методы

### PSI (Population Stability Index)

Биннинг по квантилям эталона + сумма `(p_i - q_i) * log(p_i / q_i)`. Безопасен к нулям (`eps=1e-6`).

| PSI | Уровень |
|-----|---------|
| < 0.10 | `stable` |
| 0.10 – 0.25 | `warning` |
| ≥ 0.25 | `critical` |

```bash
ML_DRIFT_WARNING_THRESHOLD=0.10
ML_DRIFT_CRITICAL_THRESHOLD=0.25
```

### KS (Колмогоров–Смирнов)

Для непрерывных признаков: статистика и p-value гипотезы «одно распределение».

### Chi-squared

Для категориальных признаков: наблюдаемые vs ожидаемые частоты.

---

## API

```http
POST /api/v1/drift/{module}
Authorization: Bearer <analyst_jwt>
Content-Type: multipart/form-data

current_csv=@recent_data.csv
```

`module` ∈ `{network_anomaly, waf_payload}`.

**Пример ответа:**

```json
{
  "module": "network_anomaly",
  "overall_psi": 0.18,
  "level": "warning",
  "reference_size": 16,
  "current_size": 1000,
  "features": [
    {
      "feature": "duration",
      "psi": 0.05,
      "level": "stable",
      "ks_statistic": 0.07,
      "ks_p_value": 0.31
    },
    {
      "feature": "flow_pkts_s",
      "psi": 0.42,
      "level": "critical",
      "ks_statistic": 0.55,
      "ks_p_value": 0.0001
    }
  ]
}
```

**curl:**

```bash
curl -X POST \
  -H "Authorization: Bearer $JWT" \
  -F "current_csv=@last_week_flows.csv" \
  http://localhost:8000/api/v1/drift/network_anomaly
```

---

## Prometheus и алерты

Каждый `POST /drift/{module}` обновляет gauge `anomaly_ai_model_drift_score{module=...}`.

```yaml
groups:
  - name: anomaly-ai
    rules:
      - alert: ModelDriftCritical
        expr: anomaly_ai_model_drift_score >= 0.25
        for: 10m
        labels: { severity: critical }
        annotations:
          summary: "Critical drift in {{ $labels.module }}"
```

---

## Действия при срабатывании

| Уровень | Действие |
|---------|----------|
| **Warning** | Накопить выборку за неделю, разобрать признаки с высоким PSI |
| **Critical** | Переобучение в течение 24–48 ч; новые данные — дополнение к эталону |

---

## Программное использование

```python
from anomaly_ai.ml.drift import detect_drift
import pandas as pd

ref = pd.read_csv("baseline.csv")
cur = pd.read_csv("recent.csv")
report = detect_drift(ref, cur)
print(report.overall_psi, report.level)
for f in report.features:
    print(f"{f.feature}: PSI={f.psi:.3f} → {f.level}")
```

---

## См. также

- [`MODEL_CARD.md`](MODEL_CARD.md)
- [`MONITORING.md`](MONITORING.md)
