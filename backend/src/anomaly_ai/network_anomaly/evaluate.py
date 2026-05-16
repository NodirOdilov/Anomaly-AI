from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline

from anomaly_ai.common.constants import NETWORK_LABEL_BENIGN
from anomaly_ai.common.paths import backend_root, resolve_under_root
from anomaly_ai.network_anomaly.features import clean_numeric_frame


def evaluate_multiclass_frame(model: Pipeline, X_test: pd.DataFrame, y_test: pd.Series) -> dict[str, float]:
    y_pred = model.predict(X_test)
    y_true = y_test.astype(str).tolist()
    y_hat = y_pred.astype(str).tolist()
    labels = sorted(set(y_true) | set(y_hat))
    acc = float(accuracy_score(y_true, y_hat))
    prec = float(precision_score(y_true, y_hat, average="weighted", zero_division=0))
    rec = float(recall_score(y_true, y_hat, average="weighted", zero_division=0))
    f1 = float(f1_score(y_true, y_hat, average="weighted", zero_division=0))

    cm = confusion_matrix(y_true, y_hat, labels=labels)
    fpr = 0.0
    fnr = 0.0
    if NETWORK_LABEL_BENIGN in labels:
        bidx = labels.index(NETWORK_LABEL_BENIGN)
        fp = np.sum(cm[:, bidx]) - cm[bidx, bidx]
        fn = np.sum(cm[bidx, :]) - cm[bidx, bidx]
        tn = cm[bidx, bidx]
        tp = np.sum(cm) - (fp + fn + tn)
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
    parser = argparse.ArgumentParser(description="Evaluate network anomaly model")
    parser.add_argument("--model", required=True)
    parser.add_argument("--test", required=True)
    args = parser.parse_args()

    import joblib

    base = backend_root()
    model_path = Path(args.model)
    if not model_path.is_absolute():
        model_path = resolve_under_root(str(model_path), base)
    test_path = Path(args.test)
    if not test_path.is_absolute():
        test_path = resolve_under_root(str(test_path), base)

    artifact: dict[str, Any] = joblib.load(model_path)
    pipe: Pipeline = artifact["model"]
    label_column = "Label"
    df = pd.read_csv(test_path)
    if label_column not in df.columns:
        raise SystemExit("Test CSV must include Label column for evaluation")
    feats = artifact["features"]
    for c in feats:
        if c not in df.columns:
            raise SystemExit(f"Missing feature column {c}")
    X = clean_numeric_frame(df, feats)
    y = df[label_column].astype(str)
    print(evaluate_multiclass_frame(pipe, X, y))


if __name__ == "__main__":
    main()
