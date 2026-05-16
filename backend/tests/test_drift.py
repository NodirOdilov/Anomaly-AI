"""Тесты детектора дрейфа."""

from __future__ import annotations

import numpy as np
import pandas as pd

from anomaly_ai.ml.drift import (
    chi_squared_drift,
    detect_drift,
    ks_drift,
    population_stability_index,
)


def test_psi_zero_for_same_distribution() -> None:
    rng = np.random.default_rng(42)
    a = rng.normal(0, 1, size=500)
    b = rng.normal(0, 1, size=500)
    psi = population_stability_index(a, b)
    assert psi < 0.05


def test_psi_large_for_shifted_distribution() -> None:
    rng = np.random.default_rng(42)
    a = rng.normal(0, 1, size=500)
    b = rng.normal(3, 1, size=500)
    psi = population_stability_index(a, b)
    assert psi > 0.5


def test_ks_detects_difference() -> None:
    rng = np.random.default_rng(42)
    a = rng.normal(0, 1, size=300)
    b = rng.normal(2, 1, size=300)
    stat, p = ks_drift(a, b)
    assert stat > 0.5
    assert p < 0.001


def test_chi_squared_distinct_counts() -> None:
    ref = {"a": 100, "b": 100}
    cur = {"a": 50, "b": 150}
    chi2, p = chi_squared_drift(ref, cur)
    assert chi2 > 0
    assert 0 <= p <= 1


def test_detect_drift_dataframe() -> None:
    rng = np.random.default_rng(0)
    ref = pd.DataFrame({"x": rng.normal(0, 1, 200), "y": rng.normal(5, 2, 200)})
    cur = pd.DataFrame({"x": rng.normal(0, 1, 200), "y": rng.normal(8, 2, 200)})
    report = detect_drift(ref, cur)
    assert report.reference_size == 200
    assert report.current_size == 200
    # y сдвинулся → должен иметь больше PSI
    by_feature = {f.feature: f.psi for f in report.features}
    assert by_feature["y"] > by_feature["x"]
