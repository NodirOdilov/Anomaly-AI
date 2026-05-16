"""Unsupervised детектор аномалий сетевых потоков (Isolation Forest).

Используется как «второе мнение» к RandomForest. Если оба согласны, что поток
аномальный — повышает severity. Полезен для обнаружения **новых типов атак**,
которые не присутствовали в обучающей выборке RF.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from anomaly_ai.network_anomaly.features import clean_numeric_frame


@dataclass(frozen=True)
class IsolationDecision:
    """Результат проверки одного потока."""

    is_anomaly: bool
    score: float          # чем ниже, тем аномальнее (см. IsolationForest.score_samples)
    normalized: float     # в диапазоне [0, 1], 1 = максимально аномально


def build_pipeline(
    *,
    n_estimators: int = 200,
    contamination: float | str = "auto",
    random_state: int = 42,
) -> Pipeline:
    """Скейлер + IsolationForest."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "iforest",
                IsolationForest(
                    n_estimators=n_estimators,
                    contamination=contamination,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ],
    )


def train(
    frame: pd.DataFrame,
    *,
    features: Iterable[str],
    output_path: str | None = None,
) -> Pipeline:
    """Обучить и (опционально) сохранить артефакт."""
    feature_list = list(features)
    X = clean_numeric_frame(frame[feature_list])
    pipeline = build_pipeline()
    pipeline.fit(X)
    if output_path:
        artifact = {
            "project": "Anomaly AI",
            "model_type": "network_isolation_forest",
            "model": pipeline,
            "features": feature_list,
            "version": "1.0.0",
        }
        joblib.dump(artifact, output_path)
    return pipeline


def predict_decision(
    pipeline: Pipeline,
    features_dict: dict[str, float],
    *,
    feature_order: Iterable[str],
) -> IsolationDecision:
    """Оценить один поток."""
    feature_list = list(feature_order)
    df = pd.DataFrame([features_dict])[feature_list]
    df = clean_numeric_frame(df)
    raw_score = float(pipeline.score_samples(df)[0])
    label = int(pipeline.predict(df)[0])  # -1 = аномалия, 1 = нормально
    is_anomaly = label == -1
    # Нормализация: оценка ~ [-0.5..0.5], 0 = граница. Преобразуем в [0..1].
    normalized = float(np.clip(0.5 - raw_score, 0.0, 1.0))
    return IsolationDecision(is_anomaly=is_anomaly, score=raw_score, normalized=normalized)


__all__ = ["IsolationDecision", "build_pipeline", "predict_decision", "train"]
