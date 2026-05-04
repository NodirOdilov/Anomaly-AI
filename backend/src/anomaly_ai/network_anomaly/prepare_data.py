from __future__ import annotations

from pathlib import Path

import pandas as pd


def validate_training_csv(path: Path, label_column: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    if label_column not in df.columns:
        raise ValueError(f"Missing label column {label_column!r}")
    return df
