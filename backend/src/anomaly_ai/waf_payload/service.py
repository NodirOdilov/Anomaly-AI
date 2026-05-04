from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.pipeline import Pipeline

from anomaly_ai.common.security import strip_control_chars, truncate_payload
from anomaly_ai.schemas.waf import WafPredictResult
from anomaly_ai.services.prediction_history import prediction_history
from anomaly_ai.waf_payload import rules
from anomaly_ai.waf_payload.features import normalize_payload


def _severity_for(attack_type: str) -> str:
    if attack_type == "benign":
        return "none"
    if attack_type in {"sql_injection", "command_injection"}:
        return "high"
    if attack_type in {"xss", "path_traversal", "generic_injection"}:
        return "medium"
    return "medium"


def _recommendation_for(attack_type: str, is_attack: bool) -> str:
    if not is_attack:
        return "Разрешить с обычным мониторингом"
    if attack_type == "sql_injection":
        return "Заблокировать запрос и зафиксировать инцидент"
    if attack_type == "xss":
        return "Заблокировать или выполнить sanitization ответа; проверить правила WAF"
    if attack_type == "path_traversal":
        return "Отклонить path-параметры; проверить доступ к файлам"
    if attack_type == "command_injection":
        return "Немедленно заблокировать; изолировать источник"
    return "Заблокировать запрос и передать на проверку"


class WafPayloadService:
    def __init__(self, artifact: dict[str, Any]) -> None:
        self._artifact = artifact
        self._pipe: Pipeline = artifact["model"]

    @property
    def version(self) -> str:
        return str(self._artifact.get("version", "1.0.0"))

    def predict(self, raw_payload: str) -> WafPredictResult:
        payload = normalize_payload(strip_control_chars(truncate_payload(raw_payload)))
        if not payload:
            raise ValueError("Payload не должен быть пустым")

        proba = self._pipe.predict_proba([payload])[0]
        classes = list(self._pipe.named_steps["clf"].classes_)
        idx = int(np.argmax(proba))
        confidence = float(proba[idx])
        ml_label = str(classes[idx])

        attack_type = rules.enrich_attack_type_ml_vs_rules(ml_label, confidence, payload)
        is_attack = attack_type != "benign"
        severity = _severity_for(attack_type)
        rec = _recommendation_for(attack_type, is_attack)

        result = WafPredictResult(
            payload=payload,
            is_attack=is_attack,
            attack_type=attack_type,
            confidence=confidence,
            severity=severity,
            recommendation=rec,
            model_version=self.version,
        )
        prediction_history.add("waf", f"{attack_type} ({confidence:.2f}) — {severity}")
        return result

    def predict_batch(self, payloads: list[str]) -> list[WafPredictResult]:
        return [self.predict(p) for p in payloads]
