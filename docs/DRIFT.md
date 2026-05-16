# Детектор дрейфа моделей

## Зачем

ML-модели в продакшене **деградируют** со временем, потому что:

- Распределение входных данных меняется (атакующие меняют технику).
- Появляются новые типы payload, которых не было в обучении.
- Сетевой профиль трафика дрейфует с ростом бизнеса.

Дрейф нужно **поймать заранее** — до того, как качество предсказаний упадёт.

## Методы

### PSI (Population Stability Index)

Стандартная индустриальная метрика. Биннинг по квантилям эталона + сумма
`(p_i - q_i) * log(p_i / q_i)`. Безопасен к нулям (eps=1e-6).

| PSI | Интерпретация |
|---|---|
| < 0.10 | Стабильно (`stable`) |
| 0.10 – 0.25 | Небольшой сдвиг (`warning`) |
| ≥ 0.25 | Значительный сдвиг (`critical`) |

Пороги настраиваются:

```bash
ML_DRIFT_WARNING_THRESHOLD=0.10
ML_DRIFT_CRITICAL_THRESHOLD=0.25
```

### KS (Колмогоров-Смирнов)

Для непрерывных распределений. Проверяет гипотезу
«две выборки из одного распределения». Возвращает статистику и p-value.

### Chi-squared

Для категориальных распределений. Сравнивает наблюдаемые vs ожидаемые частоты.

## API

```http
POST /api/v1/drift/{module}
Authorization: Bearer <analyst_jwt>
Content-Type: multipart/form-data

current_csv=@recent_data.csv
```

`module` ∈ `{network_anomaly, waf_payload}`.

Ответ:

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

## Bash-пример

```bash
curl -X POST \
  -H "Authorization: Bearer $JWT" \
  -F "current_csv=@last_week_flows.csv" \
  http://localhost:8000/api/v1/drift/network_anomaly
```

## Prometheus

Каждый POST к `/drift/{module}` обновляет gauge
`anomaly_ai_model_drift_score{module=...}`. В Grafana настроен порог
жёлтый/красный по уровням warning/critical.

Пример алертинга:

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

## Что делать при срабатывании

1. **Warning**: накопить выборку за неделю, проанализировать какие признаки
   дрейфуют, обсудить с командой.
2. **Critical**: запланировать переобучение модели в течение 24-48 часов.
   Использовать новые данные как добавку к эталонной выборке.

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

## Связано

- [[MODEL_CARD]] — метрики качества модели
- [[MONITORING]] — Grafana дашборд с drift gauge
