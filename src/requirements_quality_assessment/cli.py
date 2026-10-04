"""Orchestration-only CLI entry point: wires the approved pipeline stages together."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .assessor import RequirementQualityAssessor
from .cross_analysis.service import SpecificationAssessmentService
from .extractor import BaselineFeatureExtractor
from .full_model import FullModelService
from .full_model.config import load_full_model_request
from .full_model_reporter import AuditFullModelReporter, UserFullModelReporter
from .reader import RequirementReader
from .reporter import ConsoleReporter, UserConsoleReporter


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m requirements_quality_assessment",
        description=(
            "Assess requirement quality for a UTF-8 file containing one "
            "requirement per non-empty line."
        ),
    )
    parser.add_argument(
        "path",
        help="Path to a UTF-8 requirements text file.",
    )
    parser.add_argument(
        "--view",
        choices=("user", "audit"),
        default="user",
        help="Presentation view: concise Ukrainian user report (default) or full audit trace.",
    )
    parser.add_argument(
        "--mode",
        choices=("specification", "full-model"),
        default="specification",
        help="Assessment mode: historical specification mode (default) or explicit full-model orchestration.",
    )
    parser.add_argument(
        "--config",
        help="UTF-8 JSON request configuration; required with --mode full-model.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _parse_args(argv)

    try:
        requirements = RequirementReader().read(args.path)
    except FileNotFoundError:
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 1
    except UnicodeDecodeError as exc:
        print(f"error: {args.path} is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    except OSError as exc:
        print(f"error: cannot read {args.path}: {exc}", file=sys.stderr)
        return 1

    if args.mode == "full-model":
        if not args.config:
            print("error: --config is required with --mode full-model", file=sys.stderr)
            return 2
        try:
            request = load_full_model_request(args.config, requirements)
            result = FullModelService().run(request)
        except (OSError, UnicodeDecodeError, ValueError, TypeError, KeyError) as exc:
            print(f"error: invalid full-model config: {exc}", file=sys.stderr)
            return 2
        reporter = UserFullModelReporter() if args.view == "user" else AuditFullModelReporter()
        print(reporter.render(result.report_bundle))
        return 0

    if args.config:
        print("error: --config is only valid with --mode full-model", file=sys.stderr)
        return 2

    extractor = BaselineFeatureExtractor()
    assessor = RequirementQualityAssessor()

    requirement_results = tuple(
        assessor.assess_record(extractor.extract(requirement))
        for requirement in requirements
    )

    assessment_result = SpecificationAssessmentService().assess(requirement_results)

    reporter = UserConsoleReporter() if args.view == "user" else ConsoleReporter()
    print(reporter.render_assessment(assessment_result))
    return 0
