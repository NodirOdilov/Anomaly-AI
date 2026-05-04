from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from anomaly_ai.common.config import get_settings
from anomaly_ai.common.paths import backend_root, resolve_under_root
from anomaly_ai.common.utils import utc_now_iso
from anomaly_ai.network_anomaly.features import clean_numeric_frame, select_feature_columns
from anomaly_ai.network_anomaly.pipeline import build_network_pipeline
from anomaly_ai.network_anomaly.prepare_data import validate_training_csv


def _default_metrics() -> dict[str, float]:
    return {
        "accuracy": 0.0,
        "precision": 0.0,
        "recall": 0.0,
        "f1": 0.0,
        "false_positive_rate": 0.0,
        "false_negative_rate": 0.0,
    }


def train_from_config(cfg: dict[str, Any], root: Path | None = None) -> Path:
    base = root or backend_root()
    paths = cfg.get("paths", {})
    train_rel = paths.get("train_csv", "data/samples/sample_network_flows.csv")
    model_rel = paths.get("model_out", "models/network_anomaly_model.joblib")

    train_path = resolve_under_root(train_rel, base)
    model_path = resolve_under_root(model_rel, base)

    train_cfg = cfg.get("train", {})
    label_column = str(train_cfg.get("label_column", "Label"))
    df = validate_training_csv(train_path, label_column)

    drop_cols = [c for c in train_cfg.get("drop_columns", []) if c in df.columns]
    if drop_cols:
        df = df.drop(columns=drop_cols)

    feature_cols = select_feature_columns(df, label_column)
    if not feature_cols:
        raise ValueError("No feature columns found for network training")

    X = clean_numeric_frame(df, feature_cols)
    y = df[label_column].astype(str)

    settings = get_settings()
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=float(train_cfg.get("test_size", 0.25)),
        random_state=int(train_cfg.get("random_state", 42)),
        stratify=y,
    )

    pipeline = build_network_pipeline(cfg)
    pipeline.fit(X_train, y_train)

    from anomaly_ai.network_anomaly.evaluate import evaluate_multiclass_frame  # noqa: PLC0415

    metrics = evaluate_multiclass_frame(pipeline, X_test, y_test)

    classes = list(pipeline.named_steps["clf"].classes_)
    label_map = {cls: i for i, cls in enumerate(classes)}

    artifact: dict[str, Any] = {
        "project": cfg.get("project", "Anomaly AI"),
        "model": pipeline,
        "preprocessor": pipeline.named_steps["scaler"],
        "features": feature_cols,
        "labels": label_map,
        "model_type": cfg.get("model_type", "network_anomaly_detector"),
        "version": str(cfg.get("version", settings.app_version)),
        "created_at": utc_now_iso(),
        "metrics": {**_default_metrics(), **metrics},
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, model_path)
    return model_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Train network anomaly detector")
    parser.add_argument("--config", default="configs/network_anomaly.yaml")
    args = parser.parse_args()

    from anomaly_ai.common.config import load_yaml_config  # noqa: PLC0415

    cfg = load_yaml_config(args.config)
    out = train_from_config(cfg)
    print(f"Saved artifact to {out}")


if __name__ == "__main__":
    main()
