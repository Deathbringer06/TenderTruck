from __future__ import annotations

from contextvars import ContextVar
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.api_v1 import router as api_v1_router
from src.app.config.settings import settings
from src.app.core.exceptions import (
    AppError,
    app_error_handler,
    unhandled_error_handler,
    validation_error_handler,
)
from src.app.lib.logging import setup_logging

setup_logging()

trace_id_context: ContextVar[str | None] = ContextVar("trace_id", default=None)

app = FastAPI(title="TenderTruck API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, unhandled_error_handler)


@app.middleware("http")
async def add_trace_id(request: Request, call_next):  # type: ignore[no-untyped-def]
    trace_id = request.headers.get("X-Trace-Id") or str(uuid4())
    token = trace_id_context.set(trace_id)
    try:
        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        return response
    finally:
        trace_id_context.reset(token)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}


app.include_router(api_v1_router)
