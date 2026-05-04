from __future__ import annotations

from pathlib import Path

import pytest

from anomaly_ai.services.artifact_loader import ModelNotFoundError, load_waf_artifact


def test_missing_model_graceful() -> None:
    with pytest.raises(ModelNotFoundError):
        load_waf_artifact(Path("/nonexistent/waf_payload_model.joblib"))
