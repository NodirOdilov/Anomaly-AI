from __future__ import annotations

import os
from pathlib import Path

import pytest

BACKEND_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session", autouse=True)
def _backend_cwd_and_models() -> None:
    os.chdir(BACKEND_ROOT)
    if "PYTHONPATH" not in os.environ:
        os.environ["PYTHONPATH"] = str(BACKEND_ROOT / "src")

    from anomaly_ai.api.dependencies import clear_model_caches
    from anomaly_ai.common.config import load_yaml_config
    from anomaly_ai.network_anomaly.train import train_from_config
    from anomaly_ai.waf_payload.train import train_from_config as train_waf

    waf_model = BACKEND_ROOT / "models" / "waf_payload_model.joblib"
    net_model = BACKEND_ROOT / "models" / "network_anomaly_model.joblib"
    if not waf_model.exists():
        train_waf(load_yaml_config("configs/waf_payload.yaml"), root=BACKEND_ROOT)
    if not net_model.exists():
        train_from_config(load_yaml_config("configs/network_anomaly.yaml"), root=BACKEND_ROOT)
    clear_model_caches()


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from anomaly_ai.api.main import app

    return TestClient(app)
