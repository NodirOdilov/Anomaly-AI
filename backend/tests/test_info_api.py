from __future__ import annotations


def test_info_project_name(client) -> None:
    r = client.get("/api/v1/info")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Anomaly AI"
    assert "modules" in data
