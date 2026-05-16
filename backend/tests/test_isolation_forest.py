"""Тесты Isolation Forest для сетевых потоков."""

from __future__ import annotations

import numpy as np
import pandas as pd

from anomaly_ai.network_anomaly.isolation_forest import predict_decision, train


def test_train_and_predict() -> None:
    rng = np.random.default_rng(0)
    features = ["duration", "bytes", "pkts"]
    normal = pd.DataFrame({
        "duration": rng.normal(10, 1, 200),
        "bytes": rng.normal(500, 50, 200),
        "pkts": rng.normal(20, 3, 200),
    })
    pipeline = train(normal, features=features)
    # Нормальная точка — не аномалия.
    normal_dec = predict_decision(
        pipeline,
        {"duration": 10.2, "bytes": 510, "pkts": 21},
        feature_order=features,
    )
    # Аномальная точка — далеко от нормы.
    anomaly_dec = predict_decision(
        pipeline,
        {"duration": 200.0, "bytes": 99999, "pkts": 5000},
        feature_order=features,
    )
    assert anomaly_dec.normalized > normal_dec.normalized
