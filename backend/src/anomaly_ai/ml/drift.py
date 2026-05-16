"""Детектор дрейфа данных.

Поддерживаемые методы:

- **PSI** (Population Stability Index) — для непрерывных и категориальных распределений.
- **KS-тест** (Колмогоров-Смирнов) — для непрерывных.
- **Chi-squared** — для категориальных.

Интерпретация PSI (стандарт индустрии):

- ``PSI < 0.1`` — стабильно.
- ``0.1 ≤ PSI < 0.25`` — небольшой сдвиг (warning).
- ``PSI ≥ 0.25`` — значительный сдвиг (critical).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Iterable, Literal, Sequence

import numpy as np
import pandas as pd
from scipy import stats

from anomaly_ai.common.config import get_settings


DriftLevel = Literal["stable", "warning", "critical"]


@dataclass
class FeatureDriftResult:
    """Результат сравнения одного признака."""

    feature: str
    psi: float
    ks_statistic: float | None = None
    ks_p_value: float | None = None
    chi2_statistic: float | None = None
    chi2_p_value: float | None = None
    level: DriftLevel = "stable"


@dataclass
class DriftReport:
    """Сводный отчёт по всем признакам."""

    overall_psi: float
    level: DriftLevel
    features: list[FeatureDriftResult] = field(default_factory=list)
    reference_size: int = 0
    current_size: int = 0

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "features": [asdict(f) for f in self.features],
        }


# === Базовые статистики ===


def population_stability_index(
    reference: Sequence[float],
    current: Sequence[float],
    bins: int = 10,
) -> float:
    """PSI для двух численных выборок. Безопасен к нулям (eps = 1e-6)."""
    ref = np.asarray(reference, dtype=float)
    cur = np.asarray(current, dtype=float)
    if len(ref) == 0 or len(cur) == 0:
        return 0.0

    # Биннинг по квантилям эталона (устойчиво к скошенным распределениям).
    quantiles = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(quantiles) < 2:
        return 0.0
    quantiles[0] = -np.inf
    quantiles[-1] = np.inf

    ref_hist, _ = np.histogram(ref, bins=quantiles)
    cur_hist, _ = np.histogram(cur, bins=quantiles)
    ref_pct = ref_hist.astype(float) / max(ref_hist.sum(), 1)
    cur_pct = cur_hist.astype(float) / max(cur_hist.sum(), 1)
    eps = 1e-6
    ref_pct = np.where(ref_pct == 0, eps, ref_pct)
    cur_pct = np.where(cur_pct == 0, eps, cur_pct)
    psi = float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))
    return max(psi, 0.0)


def ks_drift(reference: Sequence[float], current: Sequence[float]) -> tuple[float, float]:
    """KS-тест: возвращает (статистика, p-value)."""
    if len(reference) == 0 or len(current) == 0:
        return 0.0, 1.0
    result = stats.ks_2samp(reference, current)
    return float(result.statistic), float(result.pvalue)


def chi_squared_drift(
    reference_counts: dict[str, int],
    current_counts: dict[str, int],
) -> tuple[float, float]:
    """Chi-squared для категориальных распределений."""
    categories = sorted(set(reference_counts) | set(current_counts))
    if not categories:
        return 0.0, 1.0
    observed = np.array([current_counts.get(c, 0) for c in categories], dtype=float)
    expected = np.array([reference_counts.get(c, 0) for c in categories], dtype=float)
    if observed.sum() == 0 or expected.sum() == 0:
        return 0.0, 1.0
    # Нормализуем expected к сумме observed.
    expected = expected / expected.sum() * observed.sum()
    expected = np.where(expected == 0, 1e-6, expected)
    chi2 = float(np.sum((observed - expected) ** 2 / expected))
    df = max(len(categories) - 1, 1)
    p_value = float(1 - stats.chi2.cdf(chi2, df))
    return chi2, p_value


def _level_for(psi: float) -> DriftLevel:
    settings = get_settings()
    if psi >= settings.ml_drift_critical_threshold:
        return "critical"
    if psi >= settings.ml_drift_warning_threshold:
        return "warning"
    return "stable"


# === Высокоуровневое API ===


def detect_drift(
    reference: pd.DataFrame,
    current: pd.DataFrame,
    *,
    numeric_columns: Iterable[str] | None = None,
    categorical_columns: Iterable[str] | None = None,
) -> DriftReport:
    """Главная точка входа: считает PSI/KS/chi² по всем колонкам и агрегирует."""
    numeric_cols = list(numeric_columns) if numeric_columns is not None else list(
        reference.select_dtypes(include=[np.number]).columns,
    )
    cat_cols = list(categorical_columns) if categorical_columns is not None else list(
        reference.select_dtypes(include=["object", "category"]).columns,
    )

    features: list[FeatureDriftResult] = []

    for col in numeric_cols:
        if col not in current.columns:
            continue
        ref_values = reference[col].dropna().to_numpy()
        cur_values = current[col].dropna().to_numpy()
        psi = population_stability_index(ref_values, cur_values)
        ks_stat, ks_p = ks_drift(ref_values, cur_values)
        features.append(
            FeatureDriftResult(
                feature=col,
                psi=psi,
                ks_statistic=ks_stat,
                ks_p_value=ks_p,
                level=_level_for(psi),
            ),
        )

    for col in cat_cols:
        if col not in current.columns:
            continue
        ref_counts = reference[col].value_counts().to_dict()
        cur_counts = current[col].value_counts().to_dict()
        # PSI поверх категориальных: используем доли категорий как «значения».
        ref_pct = np.array(list(ref_counts.values()), dtype=float)
        cur_pct = np.array(list(cur_counts.values()), dtype=float)
        psi = population_stability_index(ref_pct, cur_pct, bins=min(10, len(ref_pct) or 1))
        chi2, chi2_p = chi_squared_drift(ref_counts, cur_counts)
        features.append(
            FeatureDriftResult(
                feature=col,
                psi=psi,
                chi2_statistic=chi2,
                chi2_p_value=chi2_p,
                level=_level_for(psi),
            ),
        )

    overall = float(np.mean([f.psi for f in features])) if features else 0.0
    return DriftReport(
        overall_psi=overall,
        level=_level_for(overall),
        features=features,
        reference_size=len(reference),
        current_size=len(current),
    )


__all__ = [
    "DriftLevel",
    "DriftReport",
    "FeatureDriftResult",
    "chi_squared_drift",
    "detect_drift",
    "ks_drift",
    "population_stability_index",
]
