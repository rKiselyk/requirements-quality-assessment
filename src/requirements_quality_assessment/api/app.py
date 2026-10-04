"""FastAPI application exposing the accepted specification assessment path."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .schemas import (
    AnalyzeRequest, AnalyzeResponse, ControlledDemoAnalyzeRequest, ErrorResponse,
    HealthResponse, InitialAnalyzeRequest, ReassessmentAnalyzeRequest,
)
from .serialization import (
    serialize_controlled_demo, serialize_initial, serialize_reassessment,
)
from .service import (
    ApiBoundaryError, run_controlled_demo, run_initial, run_reassessment,
)


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
    case = exc.body.get("case") if isinstance(exc.body, dict) else None
    code = (
        "INVALID_CONTROLLED_DEMO_REQUEST"
        if case == "CONTROLLED_DEMO"
        else "INVALID_REASSESSMENT_CONTEXT"
        if case == "REASSESSMENT"
        else "MALFORMED_REQUIREMENT_INPUT"
    )
    return _error_response(
        422,
        code,
        details={"issues": issues},
        path=path,
    )


@app.exception_handler(ApiBoundaryError)
async def api_boundary_error_handler(
    request: Request, exc: ApiBoundaryError
) -> JSONResponse:
    del request
    return _error_response(
        exc.status_code,
        exc.code,
        details=exc.details,
        path=exc.path,
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
    try:
        if isinstance(request, InitialAnalyzeRequest):
            return serialize_initial(run_initial(request))
        if isinstance(request, ControlledDemoAnalyzeRequest):
            result, scenario = run_controlled_demo(request)
            return serialize_controlled_demo(result, scenario)
        if isinstance(request, ReassessmentAnalyzeRequest):
            result, scenario = run_reassessment(request)
            return serialize_reassessment(result, scenario)
    except ApiBoundaryError:
        raise
    except (TypeError, ValueError):
        raise ApiBoundaryError(
            "ANALYSIS_VALIDATION_FAILED",
            {"reason_code": "ACCEPTED_APPLICATION_PRECONDITION_FAILED"},
        ) from None
    raise ApiBoundaryError(
        "ANALYSIS_VALIDATION_FAILED",
        {"reason_code": "UNSUPPORTED_ANALYSIS_CASE"},
    )
