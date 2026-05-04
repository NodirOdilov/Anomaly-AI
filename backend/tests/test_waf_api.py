from __future__ import annotations


def test_waf_predict_json(client) -> None:
    r = client.post("/api/v1/waf/predict", json={"payload": "q=ok"})
    assert r.status_code == 200
    data = r.json()
    assert "is_attack" in data
    assert "attack_type" in data


def test_waf_batch_json(client) -> None:
    r = client.post(
        "/api/v1/waf/batch-predict",
        json={"payloads": ["ok", "id=1' OR '1'='1"]},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert "results" in data


def test_waf_empty_payload_error(client) -> None:
    r = client.post("/api/v1/waf/predict", json={"payload": "   "})
    assert r.status_code == 400
    body = r.json()
    assert body["error"] == "InvalidInput"
