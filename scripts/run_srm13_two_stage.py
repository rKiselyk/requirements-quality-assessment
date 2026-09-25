"""Run the bounded SRM-13 authored verification and real-source demonstration."""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import platform
import subprocess
import sys
from decimal import Decimal
from enum import Enum
from fractions import Fraction
from pathlib import Path
from typing import Any

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.domain import CharacteristicId, FeatureId, Requirement
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.reporter import ConsoleReporter, UserConsoleReporter


FEATURE_ATTRIBUTES = {
    "condition_context": "condition_contexts",
    "expected_result": "expected_results",
    "acceptance_criterion": "acceptance_criteria",
    "quantitative_constraint": "quantitative_constraints",
    "verification_method": "verification_methods",
    "vague_term_occurrence": "vague_term_occurrences",
}
CHARACTERISTICS = {
    "C": CharacteristicId.COMPLETENESS,
    "V": CharacteristicId.VERIFIABILITY,
    "U": CharacteristicId.UNAMBIGUITY,
}


def jsonable(value: Any) -> Any:
    if dataclasses.is_dataclass(value):
        return {
            field.name: jsonable(getattr(value, field.name))
            for field in dataclasses.fields(value)
        }
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Fraction):
        return f"{value.numerator}/{value.denominator}"
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (tuple, list)):
        return [jsonable(item) for item in value]
    if isinstance(value, dict):
        return {str(key): jsonable(item) for key, item in value.items()}
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            rows.append(row)
    ids = [row.get("id") for row in rows]
    if any(not isinstance(case_id, str) or not case_id for case_id in ids):
        raise ValueError(f"{path}: every case requires a non-empty string id")
    if len(ids) != len(set(ids)):
        raise ValueError(f"{path}: case ids must be unique")
    return rows


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], text=True, encoding="utf-8"
    ).strip()


def package_versions() -> dict[str, str]:
    import spacy

    model = spacy.load("uk_core_news_sm")
    return {
        "python": platform.python_version(),
        "spacy": spacy.__version__,
        "uk_core_news_sm": str(model.meta.get("version")),
        "operating_system": platform.platform(),
    }


def assess_cases(cases: list[dict[str, Any]]):
    extractor = BaselineFeatureExtractor()
    assessor = RequirementQualityAssessor()
    records = []
    for source_line, case in enumerate(cases, 1):
        requirement = Requirement(case["id"], source_line, case["text"])
        records.append(assessor.assess_record(extractor.extract(requirement)))
    return tuple(records)


def feature_summary(record) -> dict[str, Any]:
    evidence_by_feature: dict[str, list[dict[str, Any]]] = {
        feature: [] for feature in FEATURE_ATTRIBUTES
    }
    for evidence in record.extraction_result.evidence:
        evidence_by_feature[evidence.feature_id.value].append(
            {
                "evidence_id": evidence.evidence_id,
                "rule_id": evidence.rule_id,
                "text": evidence.text,
                "start_offset": evidence.start_offset,
                "end_offset": evidence.end_offset,
            }
        )

    summary = {}
    for feature, attribute in FEATURE_ATTRIBUTES.items():
        outcome = getattr(record.extraction_result.features, attribute)
        summary[feature] = {
            "status": outcome.status.value,
            "processing_status": outcome.processing_status.value,
            "observation_count": len(outcome.observations),
            "evidence": evidence_by_feature[feature],
            "diagnostics": [
                {
                    "code": diagnostic.code,
                    "rule_id": diagnostic.rule_id,
                    "candidate_text": (
                        diagnostic.candidate_span.text
                        if diagnostic.candidate_span is not None
                        else None
                    ),
                    "start_offset": (
                        diagnostic.candidate_span.start_offset
                        if diagnostic.candidate_span is not None
                        else None
                    ),
                    "end_offset": (
                        diagnostic.candidate_span.end_offset
                        if diagnostic.candidate_span is not None
                        else None
                    ),
                }
                for diagnostic in outcome.diagnostics
            ],
        }
    return summary


def assessment_summary(record) -> dict[str, Any]:
    profile = record.quality_profile
    by_id = {
        CharacteristicId.COMPLETENESS: profile.completeness,
        CharacteristicId.VERIFIABILITY: profile.verifiability,
        CharacteristicId.UNAMBIGUITY: profile.unambiguity,
    }
    traces = {item.characteristic_id: item for item in record.trace.characteristics}
    result = {}
    for short_name, characteristic_id in CHARACTERISTICS.items():
        assessment = by_id[characteristic_id]
        trace = traces[characteristic_id]
        result[short_name] = {
            "state": assessment.state.value,
            "value": jsonable(assessment.value),
            "assessment_rule_id": assessment.assessment_rule_id,
            "decision_code": trace.decision_code.value,
            "effects": {
                input_trace.feature_id.value: input_trace.effect_code.value
                for input_trace in trace.inputs
            },
        }
    return result


def finding_summary(record) -> list[dict[str, Any]]:
    evidence_by_id = {
        item.evidence_id: item for item in record.extraction_result.evidence
    }
    findings = []
    for assessment in (
        record.quality_profile.completeness,
        record.quality_profile.verifiability,
        record.quality_profile.unambiguity,
    ):
        for finding in assessment.findings:
            findings.append(
                {
                    "characteristic": finding.characteristic_id.value,
                    "kind": finding.kind.value,
                    "code": finding.code,
                    "rule_id": finding.rule_id,
                    "evidence_texts": [
                        evidence_by_id[reference].text
                        for reference in finding.evidence_refs
                    ],
                }
            )
    return findings


def actual_summary(record) -> dict[str, Any]:
    return {
        "features": feature_summary(record),
        "assessments": assessment_summary(record),
        "findings": finding_summary(record),
    }


def add_discrepancy(
    discrepancies: list[dict[str, Any]], path: str, expected: Any, actual: Any
) -> None:
    if expected != actual:
        discrepancies.append({"path": path, "expected": expected, "actual": actual})


def compare_authored(case: dict[str, Any], actual: dict[str, Any]) -> dict[str, Any]:
    expected = case["expected"]
    discrepancies: list[dict[str, Any]] = []
    component_discrepancies: dict[str, list[dict[str, Any]]] = {
        "Evidence/features": [],
        "states_values": [],
        "Trace": [],
        "Findings": [],
    }

    absent = {
        "status": "NOT_DETECTED",
        "processing_status": "COMPLETE",
        "observation_count": 0,
        "evidence_texts": [],
        "diagnostics": [],
    }
    feature_expectations = {
        feature: absent for feature in expected.get("absent_features", [])
    }
    feature_expectations.update(expected.get("features", {}))
    for feature, assertion in feature_expectations.items():
        observed = actual["features"][feature]
        projections = {
            "status": observed["status"],
            "processing_status": observed["processing_status"],
            "observation_count": observed["observation_count"],
            "evidence_texts": [item["text"] for item in observed["evidence"]],
            "diagnostics": [
                {"code": item["code"], "candidate_text": item["candidate_text"]}
                for item in observed["diagnostics"]
            ],
        }
        for key, expected_value in assertion.items():
            add_discrepancy(
                component_discrepancies["Evidence/features"],
                f"features.{feature}.{key}",
                expected_value,
                projections[key],
            )

    characteristic_status = {}
    for short_name in CHARACTERISTICS:
        expected_assessment = expected["assessments"][short_name]
        observed = actual["assessments"][short_name]
        local: list[dict[str, Any]] = []
        for key in ("state", "value"):
            add_discrepancy(
                local,
                f"assessments.{short_name}.{key}",
                expected_assessment[key],
                observed[key],
            )
        add_discrepancy(
            local,
            f"trace.{short_name}.decision_code",
            expected["trace_decisions"][short_name],
            observed["decision_code"],
        )
        characteristic_status[short_name] = "PASS" if not local else "FAIL"
        component_discrepancies["states_values"].extend(
            item for item in local if item["path"].startswith("assessments")
        )
        component_discrepancies["Trace"].extend(
            item for item in local if item["path"].startswith("trace")
        )

    add_discrepancy(
        component_discrepancies["Findings"],
        "findings",
        expected.get("findings", []),
        actual["findings"],
    )
    for items in component_discrepancies.values():
        discrepancies.extend(items)

    requested = case.get("comparison_status")
    if requested == "NOT_ASSESSABLE":
        status = "NOT_ASSESSABLE"
    else:
        status = "PASS" if not discrepancies else "FAIL"
    return {
        "status": status,
        "characteristics": characteristic_status,
        "components": {
            name: "PASS" if not items else "FAIL"
            for name, items in component_discrepancies.items()
        },
        "discrepancies": discrepancies,
    }


def aggregate_authored(comparisons: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = {status: 0 for status in ("PASS", "FAIL", "NOT_ASSESSABLE")}
    characteristics = {
        name: {status: 0 for status in ("PASS", "FAIL", "NOT_ASSESSABLE")}
        for name in CHARACTERISTICS
    }
    components: dict[str, dict[str, int]] = {}
    for comparison in comparisons:
        statuses[comparison["status"]] += 1
        for name, status in comparison["characteristics"].items():
            characteristics[name][status] += 1
        for name, status in comparison["components"].items():
            components.setdefault(name, {"PASS": 0, "FAIL": 0})[status] += 1
    return {
        "cases": len(comparisons),
        "case_status": statuses,
        "characteristics": characteristics,
        "components": components,
    }


def aggregate_real(records) -> dict[str, Any]:
    assessments = {name: {} for name in CHARACTERISTICS}
    finding_count = 0
    diagnostic_cases = 0
    for record in records:
        summary = actual_summary(record)
        if any(item["diagnostics"] for item in summary["features"].values()):
            diagnostic_cases += 1
        finding_count += len(summary["findings"])
        for name, observed in summary["assessments"].items():
            key = f"{observed['state']}:{observed['value']}"
            assessments[name][key] = assessments[name].get(key, 0) + 1
    return {
        "cases": len(records),
        "assessment_distributions": assessments,
        "signal_findings": finding_count,
        "cases_with_diagnostics": diagnostic_cases,
    }


def render_reports(records, output_dir: Path, prefix: str) -> None:
    specification = SpecificationQualityAggregator().aggregate(
        record.quality_profile for record in records
    )
    (output_dir / f"{prefix}-user-report.txt").write_text(
        UserConsoleReporter().render(records, specification) + "\n", encoding="utf-8"
    )
    (output_dir / f"{prefix}-audit-report.txt").write_text(
        ConsoleReporter().render(records, specification) + "\n", encoding="utf-8"
    )


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("docs/srm-13-two-stage-results"),
    )
    args = parser.parse_args()
    data_dir = args.data_dir
    authored_path = data_dir / "authored-requirements.jsonl"
    real_path = data_dir / "real-requirements.jsonl"

    authored_cases = load_jsonl(authored_path)
    real_cases = load_jsonl(real_path)
    authored_records = assess_cases(authored_cases)
    real_records = assess_cases(real_cases)

    authored_rows = []
    comparisons = []
    for case, record in zip(authored_cases, authored_records, strict=True):
        summary = actual_summary(record)
        comparison = compare_authored(case, summary)
        comparisons.append(comparison)
        authored_rows.append(
            {
                **case,
                "actual": summary,
                "comparison": comparison,
                "full_record": jsonable(record),
            }
        )

    real_rows = []
    for case, record in zip(real_cases, real_records, strict=True):
        real_rows.append(
            {
                **case,
                "actual": actual_summary(record),
                "full_record": jsonable(record),
            }
        )

    write_jsonl(data_dir / "authored-results.jsonl", authored_rows)
    write_jsonl(data_dir / "real-results.jsonl", real_rows)
    (data_dir / "authored-input.txt").write_text(
        "\n".join(case["text"] for case in authored_cases) + "\n", encoding="utf-8"
    )
    (data_dir / "real-input.txt").write_text(
        "\n".join(case["text"] for case in real_cases) + "\n", encoding="utf-8"
    )
    render_reports(authored_records, data_dir, "authored")
    render_reports(real_records, data_dir, "real")

    summary = {
        "study": "SRM-13 bounded two-stage verification and demonstration",
        "implementation_commit": git(
            "log", "-1", "--format=%H", "--", "src", "pyproject.toml"
        ),
        "environment": package_versions(),
        "datasets": {
            "authored": {"path": str(authored_path), "sha256": sha256(authored_path)},
            "real": {"path": str(real_path), "sha256": sha256(real_path)},
        },
        "stage_1": aggregate_authored(comparisons),
        "stage_2": aggregate_real(real_records),
    }
    (data_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
