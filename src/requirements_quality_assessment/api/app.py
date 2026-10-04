"""FastAPI application exposing the accepted specification assessment path."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from ..cross_analysis.service import assess_specification
from ..domain import Requirement
from .schemas import AnalyzeRequest, AnalyzeResponse, ErrorResponse, HealthResponse
from .serialization import serialize_analysis


app = FastAPI(
    title="Requirements Quality Assessment Research API",
    description=(
        "A thin HTTP adapter over the accepted deterministic requirements-quality "
        "assessment pipeline. The API does not define independent scoring semantics."
    ),
    version="1.0.0",
)


def _error_response(
    status_code: int,
    code: str,
    *,
    details: dict[str, Any],
    path: list[str | int] | None = None,
) -> JSONResponse:
    content = ErrorResponse(
        error={"code": code, "details": details, "path": path}
    ).model_dump(mode="json")
    return JSONResponse(status_code=status_code, content=content)


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    del request
    issues = [
        {
            "path": list(error.get("loc", ())),
            "type": str(error.get("type", "validation_error")),
            "message": str(error.get("msg", "Invalid request data")),
        }
        for error in exc.errors()
    ]
    path = issues[0]["path"] if issues else None
    return _error_response(
        422,
        "MALFORMED_REQUIREMENT_INPUT",
        details={"issues": issues},
        path=path,
    )


@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception) -> JSONResponse:
    del request, exc
    return _error_response(
        500,
        "ANALYSIS_INTERNAL_FAILURE",
        details={"reason": "The analysis could not be completed."},
    )


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Check service health",
    description="Returns service availability without invoking the research model.",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post(
    "/api/v1/analyze",
    response_model=AnalyzeResponse,
    responses={
        422: {"model": ErrorResponse, "description": "Invalid requirement input"},
        500: {"model": ErrorResponse, "description": "Safe internal failure response"},
    },
    summary="Analyze a textual specification",
    description=(
        "Runs the existing accepted extraction, requirement assessment, and "
        "specification aggregation pipeline synchronously."
    ),
)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse | JSONResponse:
    if not request.requirements:
        return _error_response(
            422,
            "EMPTY_SPECIFICATION",
            details={"requirement_count": 0},
            path=["body", "requirements"],
        )

    requirements = tuple(
        Requirement(
            item.id if item.id is not None else f"R{index:03d}",
            index,
            item.text,
        )
        for index, item in enumerate(request.requirements, start=1)
    )
    result = assess_specification(requirements)
    return serialize_analysis(result)
