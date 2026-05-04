from __future__ import annotations


class AppError(Exception):
    """Base application error."""

    code = "AppError"

    def __init__(self, message: str, *, code: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        if code:
            self.code = code


class InvalidInputError(AppError):
    code = "InvalidInput"


class ModelNotFoundError(AppError):
    code = "ModelNotFound"


class ModelArtifactError(AppError):
    code = "ModelArtifactError"
