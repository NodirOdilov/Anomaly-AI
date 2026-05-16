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
from anomaly_ai.waf_payload.pipeline import build_waf_pipeline
from anomaly_ai.waf_payload.prepare_data import ensure_processed_csv


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
    json_rel = paths.get("train_json", "data/samples/sample_payloads.json")
    csv_rel = paths.get("train_csv", "data/processed/waf_train.csv")
    model_rel = paths.get("model_out", "models/waf_payload_model.joblib")

    json_path = resolve_under_root(json_rel, base)
    csv_path = resolve_under_root(csv_rel, base)
    model_path = resolve_under_root(model_rel, base)

    ensure_processed_csv(json_path, csv_path)
    df = pd.read_csv(csv_path)
    if "payload" not in df.columns or "label" not in df.columns:
        raise ValueError("WAF training data must contain payload and label columns")

    X = df["payload"].astype(str).tolist()
    y = df["label"].astype(str).tolist()

    settings = get_settings()
    train_cfg = cfg.get("train", {})
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=float(train_cfg.get("test_size", 0.25)),
        random_state=int(train_cfg.get("random_state", 42)),
        stratify=y,
    )

    pipeline = build_waf_pipeline(cfg)
    pipeline.fit(X_train, y_train)

    from anomaly_ai.waf_payload.evaluate import evaluate_multiclass

    metrics = evaluate_multiclass(pipeline, X_test, y_test)

    classes = list(pipeline.named_steps["clf"].classes_)
    label_map = {cls: i for i, cls in enumerate(classes)}

    artifact: dict[str, Any] = {
        "project": cfg.get("project", "Anomaly AI"),
        "model": pipeline,
        "preprocessor": None,
        "features": [],
        "labels": label_map,
        "model_type": cfg.get("model_type", "waf_payload_detector"),
        "version": str(cfg.get("version", settings.app_version)),
        "created_at": utc_now_iso(),
        "metrics": {**_default_metrics(), **metrics},
    }

    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact, model_path)
    return model_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Train WAF payload detector")
    parser.add_argument("--config", default="configs/waf_payload.yaml")
    args = parser.parse_args()

    from anomaly_ai.common.config import load_yaml_config

    cfg = load_yaml_config(args.config)
    out = train_from_config(cfg)
    print(f"Saved artifact to {out}")


if __name__ == "__main__":
    main()
