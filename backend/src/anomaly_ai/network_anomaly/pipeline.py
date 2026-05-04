from __future__ import annotations

from typing import Any

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler


def build_network_pipeline(cfg: dict[str, Any]) -> Pipeline:
    train_cfg = cfg.get("train", {})
    n_estimators = int(train_cfg.get("rf_n_estimators", 100))
    clf = RandomForestClassifier(
        n_estimators=n_estimators,
        random_state=int(train_cfg.get("random_state", 42)),
        class_weight="balanced",
        n_jobs=-1,
    )
    return Pipeline(
        steps=[
            ("scaler", MinMaxScaler()),
            ("clf", clf),
        ]
    )
