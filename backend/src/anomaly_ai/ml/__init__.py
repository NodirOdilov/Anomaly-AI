"""Универсальные ML-утилиты Anomaly AI v2.

- :mod:`anomaly_ai.ml.registry` — реестр моделей с версионированием и hot-swap.
- :mod:`anomaly_ai.ml.drift` — детектор дрейфа (PSI, KS, chi-squared).
- :mod:`anomaly_ai.ml.explain` — объяснимость предсказаний (top features).
- :mod:`anomaly_ai.ml.calibration` — калибровка вероятностей.
"""

from anomaly_ai.ml.drift import (
    DriftReport,
    chi_squared_drift,
    detect_drift,
    ks_drift,
    population_stability_index,
)
from anomaly_ai.ml.explain import explain_linear_text, explain_tree_tabular
from anomaly_ai.ml.registry import ModelRegistry, RegistryEntry, get_default_registry

__all__ = [
    "DriftReport",
    "ModelRegistry",
    "RegistryEntry",
    "chi_squared_drift",
    "detect_drift",
    "explain_linear_text",
    "explain_tree_tabular",
    "get_default_registry",
    "ks_drift",
    "population_stability_index",
]
