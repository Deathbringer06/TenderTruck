from __future__ import annotations

import logging
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


class NotFoundError(AppError):
    def __init__(
        self,
        message: str = "Resource not found",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__("NOT_FOUND", message, 404, details)


class UnauthorizedError(AppError):
    def __init__(
        self,
        message: str = "Unauthorized",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__("UNAUTHORIZED", message, 401, details)


class ForbiddenError(AppError):
    def __init__(self, message: str = "Forbidden", details: dict[str, Any] | None = None) -> None:
        super().__init__("FORBIDDEN", message, 403, details)


class ValidationError(AppError):
    def __init__(
        self,
        message: str = "VALIDATION_ERROR",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__("VALIDATION_ERROR", message, 422, details)


def _error_response(error: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=error.status_code,
        content={"code": error.code, "message": error.message, "details": error.details},
    )


async def app_error_handler(request: Request, error: AppError) -> JSONResponse:
    return _error_response(error)


async def validation_error_handler(request: Request, error: RequestValidationError) -> JSONResponse:
    details = {"errors": error.errors()}
    return JSONResponse(
        status_code=422,
        content={"code": "VALIDATION_ERROR", "message": "Validation failed", "details": details},
    )


async def unhandled_error_handler(request: Request, error: Exception) -> JSONResponse:
    logging.getLogger(__name__).exception("Unhandled request error", exc_info=error)
    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "Internal server error",
            "details": {},
        },
    )
