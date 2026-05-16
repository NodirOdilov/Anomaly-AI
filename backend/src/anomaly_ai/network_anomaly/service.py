from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from anomaly_ai.common.constants import NETWORK_LABEL_BENIGN, NETWORK_SUSPICIOUS_LABELS
from anomaly_ai.common.exceptions import InvalidInputError
from anomaly_ai.network_anomaly.features import clean_numeric_frame
from anomaly_ai.schemas.network import NetworkCsvResponse, NetworkPredictResponse, NetworkRowResult
from anomaly_ai.services.prediction_history import prediction_history


def _severity_for_label(label: str) -> str:
    if label == NETWORK_LABEL_BENIGN:
        return "low"
    if label in NETWORK_SUSPICIOUS_LABELS:
        return "high"
    return "medium"


def _recommendation_for_label(label: str) -> str:
    if label == NETWORK_LABEL_BENIGN:
        return "Признаки аномалии по baseline-модели не обнаружены"
    if label == "HTTP_ATTACK":
        return "Проверьте HTTP-нагруженные потоки и логи приложения"
    if label == "UDP_ATTACK":
        return "Проверьте source IP и паттерн трафика"
    return "Проверьте source IP и паттерн трафика"


class NetworkAnomalyService:
    def __init__(self, artifact: dict[str, Any]) -> None:
        self._artifact = artifact
        self._pipe: Pipeline = artifact["model"]
        self._features: list[str] = list(artifact["features"])

    @property
    def version(self) -> str:
        return str(self._artifact.get("version", "1.0.0"))

    def _frame_from_features(self, row: dict[str, Any]) -> pd.DataFrame:
        missing = [c for c in self._features if c not in row]
        if missing:
            raise InvalidInputError(f"Отсутствуют ключи признаков: {missing}")
        data = {c: row[c] for c in self._features}
        df = pd.DataFrame([data])
        return clean_numeric_frame(df, self._features)

    def predict_row(self, features: dict[str, Any]) -> NetworkPredictResponse:
        X = self._frame_from_features(features)
        proba = self._pipe.predict_proba(X)[0]
        classes = list(self._pipe.named_steps["clf"].classes_)
        idx = int(np.argmax(proba))
        label = str(classes[idx])
        confidence = float(proba[idx])
        res = NetworkPredictResponse(
            prediction=label,
            confidence=confidence,
            severity=_severity_for_label(label),
            recommendation=_recommendation_for_label(label),
            model_version=self.version,
        )
        prediction_history.add("network", f"{label} ({confidence:.2f})")
        return res

    def predict_csv(self, df: pd.DataFrame, label_column: str | None = "Label") -> NetworkCsvResponse:
        drop = {label_column} if label_column and label_column in df.columns else set()
        feature_df = df.drop(columns=[c for c in drop if c in df.columns], errors="ignore")
        missing_cols = [c for c in self._features if c not in feature_df.columns]
        if missing_cols:
            raise InvalidInputError(
                f"В CSV отсутствуют обязательные feature columns: {missing_cols}. Ожидается: {self._features}"
            )

        X = clean_numeric_frame(feature_df, self._features)
        preds = self._pipe.predict(X)
        probas = self._pipe.predict_proba(X)
        classes = list(self._pipe.named_steps["clf"].classes_)

        results: list[NetworkRowResult] = []
        counts = Counter()
        for i in range(len(preds)):
            label = str(preds[i])
            counts[label] += 1
            cls_idx = classes.index(label) if label in classes else 0
            confidence = float(probas[i][cls_idx])
            results.append(NetworkRowResult(row=i + 1, prediction=label, confidence=confidence))

        benign = int(counts.get(NETWORK_LABEL_BENIGN, 0))
        suspicious = int(len(results) - benign)
        top_prediction = counts.most_common(1)[0][0] if counts else NETWORK_LABEL_BENIGN

        prediction_history.add("network", f"csv:{len(results)} flows, top={top_prediction}")
        return NetworkCsvResponse(
            total_flows=len(results),
            benign=benign,
            suspicious=suspicious,
            top_prediction=top_prediction,
            results=results,
        )
