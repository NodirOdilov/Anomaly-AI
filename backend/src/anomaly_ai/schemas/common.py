from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    error: str = Field(..., examples=["InvalidInput"])
    message: str
