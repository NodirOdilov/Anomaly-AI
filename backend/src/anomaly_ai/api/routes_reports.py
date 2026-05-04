from __future__ import annotations

from fastapi import APIRouter

from anomaly_ai.schemas.reports import ReportsSummaryResponse
from anomaly_ai.services.report_service import build_summary

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/summary", response_model=ReportsSummaryResponse, response_model_exclude_none=True)
def reports_summary() -> ReportsSummaryResponse:
    return build_summary()
