from __future__ import annotations

from pathlib import Path

import pandas as pd

from anomaly_ai.network_anomaly.service import NetworkAnomalyService
from anomaly_ai.services.artifact_loader import load_network_artifact
from anomaly_ai.services.model_registry import default_network_model_path


def test_network_predict_csv() -> None:
    art = load_network_artifact(default_network_model_path())
    svc = NetworkAnomalyService(art)
    root = Path(__file__).resolve().parents[1]
    df = pd.read_csv(root / "data" / "samples" / "sample_network_flows.csv")
    res = svc.predict_csv(df)
    assert res.total_flows == len(df)
    assert res.benign + res.suspicious == res.total_flows
