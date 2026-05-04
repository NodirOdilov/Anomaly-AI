from __future__ import annotations

import numpy as np
import pandas as pd


def select_feature_columns(df: pd.DataFrame, label_column: str) -> list[str]:
    cols = [c for c in df.columns if c != label_column]
    return cols


def clean_numeric_frame(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    out = df[feature_cols].copy()
    out = out.replace([np.inf, -np.inf], np.nan)
    out = out.fillna(0.0)
    for c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0.0)
    return out
