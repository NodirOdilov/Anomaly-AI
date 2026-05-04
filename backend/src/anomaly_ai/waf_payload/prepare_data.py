from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def json_payloads_to_dataframe(path: Path) -> pd.DataFrame:
    with path.open("r", encoding="utf-8") as f:
        rows = json.load(f)
    return pd.DataFrame(rows)


def ensure_processed_csv(json_path: Path, out_csv: Path) -> Path:
    df = json_payloads_to_dataframe(json_path)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    return out_csv
