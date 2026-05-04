from __future__ import annotations

from pathlib import Path

import pandas as pd


def test_network_predict_api(client) -> None:
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "samples" / "sample_network_flows.csv")
    row = df.iloc[0].drop(labels=["Label"]).to_dict()
    r = client.post("/api/v1/network/predict", json=row)
    assert r.status_code == 200
    data = r.json()
    assert "prediction" in data
    assert "confidence" in data


def test_network_upload_csv(client) -> None:
    root = Path(__file__).resolve().parents[1]
    path = root / "data" / "samples" / "sample_network_flows.csv"
    files = {"file": ("sample_network_flows.csv", path.read_bytes(), "text/csv")}
    r = client.post("/api/v1/network/upload-csv", files=files)
    assert r.status_code == 200
    data = r.json()
    assert data["total_flows"] > 0


def test_network_upload_bad_csv(client) -> None:
    files = {"file": ("bad.csv", b"not,a,good\ndata", "text/csv")}
    r = client.post("/api/v1/network/upload-csv", files=files)
    assert r.status_code in {400, 422}
