"""Orchestration-only CLI entry point: wires the approved pipeline stages together."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .aggregator import SpecificationQualityAggregator
from .assessor import RequirementQualityAssessor
from .extractor import BaselineFeatureExtractor
from .reader import RequirementReader
from .reporter import ConsoleReporter


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

    extractor = BaselineFeatureExtractor()
    assessor = RequirementQualityAssessor()

    requirement_results = tuple(
        assessor.assess_record(extractor.extract(requirement))
        for requirement in requirements
    )

    specification_profile = SpecificationQualityAggregator().aggregate(
        record.quality_profile for record in requirement_results
    )

    print(ConsoleReporter().render(requirement_results, specification_profile))
    return 0
