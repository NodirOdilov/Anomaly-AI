from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(prefix="/info", tags=["info"])


@router.get("")
def info() -> dict[str, str | list[str]]:
    return {
        "name": "Anomaly AI",
        "description": "Платформа обнаружения сетевых аномалий и web-атак на базе Machine Learning",
        "modules": [
            "Обнаружение сетевых аномалий",
            "Обнаружение атак в WAF payload",
        ],
        "mode": "defensive-security",
    }
