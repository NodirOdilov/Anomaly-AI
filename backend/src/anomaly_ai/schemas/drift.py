"""Схемы для drift-эндпоинтов."""

from __future__ import annotations

from pydantic import BaseModel


class FeatureDriftItem(BaseModel):
    feature: str
    psi: float
    level: str
    ks_statistic: float | None = None
    ks_p_value: float | None = None
    chi2_statistic: float | None = None
    chi2_p_value: float | None = None


class DriftReportPublic(BaseModel):
    module: str
    overall_psi: float
    level: str
    reference_size: int
    current_size: int
    features: list[FeatureDriftItem]
