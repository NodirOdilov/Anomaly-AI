from __future__ import annotations

import re
from dataclasses import dataclass

from anomaly_ai.common.constants import WAF_ATTACK_TYPES


@dataclass(frozen=True)
class RuleHit:
    attack_type: str
    weight: float


_SQL_HINTS = re.compile(
    r"(\bunion\b|\bselect\b|\bor\b\s+['\"]?\d+['\"]?\s*=\s*['\"]?\d+|--|;\s*drop\b|/\*|\*/|xp_|\bexec\b)",
    re.IGNORECASE,
)
_XSS_HINTS = re.compile(
    r"(<script|javascript:|onerror\s*=|onload\s*=|<iframe|alert\s*\(|document\.cookie)",
    re.IGNORECASE,
)
_PATH_HINTS = re.compile(r"(\.\./|\.\.\\|/etc/passwd|\\\\\.\.\\|%2e%2e%2f)", re.IGNORECASE)
_CMD_HINTS = re.compile(
    r"(;\s*(ls|cat|rm|wget|curl|nc\s|bash|sh|cmd|powershell)|\|\s*sh|`[^`]+`|\$\([^)]+\))",
    re.IGNORECASE,
)


def rule_based_signals(payload: str) -> list[RuleHit]:
    """Return defensive pattern hints; higher weight = stronger hint."""
    hits: list[RuleHit] = []
    if _SQL_HINTS.search(payload):
        hits.append(RuleHit("sql_injection", 0.85))
    if _XSS_HINTS.search(payload):
        hits.append(RuleHit("xss", 0.85))
    if _PATH_HINTS.search(payload):
        hits.append(RuleHit("path_traversal", 0.8))
    if _CMD_HINTS.search(payload):
        hits.append(RuleHit("command_injection", 0.75))
    return hits


def best_rule_attack_type(payload: str) -> str | None:
    hits = rule_based_signals(payload)
    if not hits:
        return None
    hits_sorted = sorted(hits, key=lambda h: h.weight, reverse=True)
    return hits_sorted[0].attack_type


def enrich_attack_type_ml_vs_rules(ml_label: str, confidence: float, payload: str) -> str:
    """
    Prefer ML when confident; otherwise allow high-signal rules to suggest a type.
    Never fabricates offensive capabilities — classification only.
    """
    ml_label_norm = ml_label.strip().lower()
    if ml_label_norm not in WAF_ATTACK_TYPES:
        ml_label_norm = "generic_injection"

    rule_guess = best_rule_attack_type(payload)
    if rule_guess is None:
        return ml_label_norm

    if confidence >= 0.72:
        if ml_label_norm == "benign" and rule_guess:
            return rule_guess
        return ml_label_norm

    if ml_label_norm == "benign" and rule_guess:
        return rule_guess
    return ml_label_norm
