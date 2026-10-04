"""Case dispatch for the frozen Research UI v1 application boundary."""

from __future__ import annotations

from typing import Any

from ..cross_analysis.service import assess_specification
from ..domain import Requirement
from ..full_model import FullModelService
from ..full_model.controlled_scenario import (
    ControlledResearchReferenceScenario,
    load_controlled_research_reference_scenario,
)
from ..full_model.domain import FullModelResult
from .schemas import (
    ControlledDemoAnalyzeRequest,
    InitialAnalyzeRequest,
    ReassessmentAnalyzeRequest,
    RequirementInput,
)
from .serialization import build_reassessment_context


class ApiBoundaryError(Exception):
    def __init__(
        self,
        code: str,
        details: dict[str, Any],
        path: list[str | int] | None = None,
        status_code: int = 422,
    ) -> None:
        super().__init__(code)
        self.code = code
        self.details = details
        self.path = path
        self.status_code = status_code


def _requirements(items: list[RequirementInput]) -> tuple[Requirement, ...]:
    if not items:
        raise ApiBoundaryError(
            "EMPTY_SPECIFICATION",
            {"requirement_count": 0},
            ["body", "requirements"],
        )
    return tuple(
        Requirement(f"R{index:03d}", item.source_line, item.text)
        for index, item in enumerate(items, start=1)
    )


def run_initial(request: InitialAnalyzeRequest):
    return assess_specification(_requirements(request.requirements))


def run_controlled_demo(
    request: ControlledDemoAnalyzeRequest,
) -> tuple[FullModelResult, ControlledResearchReferenceScenario]:
    try:
        scenario = load_controlled_research_reference_scenario(
            request.scenario.id,
            request.scenario.version,
        )
    except (TypeError, ValueError) as exc:
        del exc
        raise ApiBoundaryError(
            "INVALID_CONTROLLED_DEMO_REQUEST",
            {
                "scenario_id": request.scenario.id,
                "scenario_version": request.scenario.version,
            },
            ["body", "scenario"],
        ) from None
    return FullModelService().run(scenario.request), scenario


def run_reassessment(
    request: ReassessmentAnalyzeRequest,
) -> tuple[FullModelResult, ControlledResearchReferenceScenario]:
    revised_requirements = _requirements(request.requirements)
    try:
        scenario = load_controlled_research_reference_scenario(
            request.prior_context.scenario.id,
            request.prior_context.scenario.version,
        )
    except (TypeError, ValueError):
        raise ApiBoundaryError(
            "INVALID_REASSESSMENT_CONTEXT",
            {"reason_code": "UNKNOWN_PRIOR_SCENARIO"},
            ["body", "prior_context", "scenario"],
        ) from None

    result = FullModelService().run(scenario.request)
    expected_context = build_reassessment_context(result, scenario)
    if request.prior_context.model_dump(mode="json") != expected_context.model_dump(
        mode="json"
    ):
        raise ApiBoundaryError(
            "INVALID_REASSESSMENT_CONTEXT",
            {"reason_code": "PRIOR_LIFECYCLE_CONTEXT_MISMATCH"},
            ["body", "prior_context"],
        )

    expected_requirements = result.revised_specification.requirements
    if tuple(
        (item.id, item.source_line, item.text) for item in revised_requirements
    ) != tuple(
        (
            item.subject_ref.requirement_id,
            item.subject_ref.source_line,
            item.text,
        )
        for item in expected_requirements
    ):
        raise ApiBoundaryError(
            "INVALID_REASSESSMENT_CONTEXT",
            {"reason_code": "REVISED_SPECIFICATION_MISMATCH"},
            ["body", "requirements"],
        )
    return result, scenario


__all__ = [
    "ApiBoundaryError",
    "run_controlled_demo",
    "run_initial",
    "run_reassessment",
]
