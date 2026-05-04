from __future__ import annotations

from anomaly_ai.services.artifact_loader import load_waf_artifact
from anomaly_ai.services.model_registry import default_waf_model_path
from anomaly_ai.waf_payload.service import WafPayloadService


def test_waf_benign_payload() -> None:
    art = load_waf_artifact(default_waf_model_path())
    svc = WafPayloadService(art)
    r = svc.predict("q=books&page=1")
    assert r.is_attack is False
    assert r.attack_type == "benign"


def test_waf_sqli_like_payload() -> None:
    art = load_waf_artifact(default_waf_model_path())
    svc = WafPayloadService(art)
    r = svc.predict("id=1' OR '1'='1")
    assert r.is_attack is True
    assert r.attack_type in {"sql_injection", "generic_injection"}


def test_waf_xss_like_payload() -> None:
    art = load_waf_artifact(default_waf_model_path())
    svc = WafPayloadService(art)
    r = svc.predict("<script>alert(1)</script>")
    assert r.is_attack is True
    assert r.attack_type in {"xss", "generic_injection"}
