from __future__ import annotations

from pathlib import Path

import pandas as pd

from anomaly_ai.network_anomaly.features import clean_numeric_frame, select_feature_columns


def test_preprocess_sample_csv() -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "data" / "samples" / "sample_network_flows.csv"
    df = pd.read_csv(path)
    feats = select_feature_columns(df, "Label")
    cleaned = clean_numeric_frame(df, feats)
    assert cleaned.shape[0] == len(df)
    assert not cleaned.isna().any().any()
