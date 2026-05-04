from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline

from anomaly_ai.common.paths import backend_root, resolve_under_root


def evaluate_multiclass(model: Pipeline, X_test: list[str], y_test: list[str]) -> dict[str, float]:
    y_pred = model.predict(X_test)
    labels = sorted(set(y_test) | set(y_pred))
    acc = float(accuracy_score(y_test, y_pred))
    prec = float(precision_score(y_test, y_pred, average="weighted", zero_division=0))
    rec = float(recall_score(y_test, y_pred, average="weighted", zero_division=0))
    f1 = float(f1_score(y_test, y_pred, average="weighted", zero_division=0))

    cm = confusion_matrix(y_test, y_pred, labels=labels)
    # Approximate binary "attack" as not benign for FPR/FNR if benign exists
    fpr = 0.0
    fnr = 0.0
    if "benign" in labels:
        benign_idx = labels.index("benign")
        tp = np.sum(cm) - (np.sum(cm[benign_idx, :]) + np.sum(cm[:, benign_idx]) - cm[benign_idx, benign_idx])
        fp = np.sum(cm[:, benign_idx]) - cm[benign_idx, benign_idx]
        fn = np.sum(cm[benign_idx, :]) - cm[benign_idx, benign_idx]
        tn = cm[benign_idx, benign_idx]
        denom_fp = fp + tn
        denom_fn = fn + tp
        fpr = float(fp / denom_fp) if denom_fp else 0.0
        fnr = float(fn / denom_fn) if denom_fn else 0.0

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "false_positive_rate": fpr,
        "false_negative_rate": fnr,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate WAF model")
    parser.add_argument("--model", required=True)
    parser.add_argument("--test", required=True, help="CSV with payload,label")
    args = parser.parse_args()

    import joblib  # noqa: PLC0415
    import pandas as pd  # noqa: PLC0415

    base = backend_root()
    model_path = Path(args.model)
    if not model_path.is_absolute():
        model_path = resolve_under_root(str(model_path), base)
    test_path = Path(args.test)
    if not test_path.is_absolute():
        test_path = resolve_under_root(str(test_path), base)

    artifact: dict[str, Any] = joblib.load(model_path)
    pipe: Pipeline = artifact["model"]
    df = pd.read_csv(test_path)
    metrics = evaluate_multiclass(pipe, df["payload"].astype(str).tolist(), df["label"].astype(str).tolist())
    print(metrics)


if __name__ == "__main__":
    main()
