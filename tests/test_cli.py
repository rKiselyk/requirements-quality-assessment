"""Integration tests for the MVP-11 CLI orchestration entry point.

These tests exercise the real production pipeline (reader, extractor,
assessor, aggregator, reporter) end-to-end through ``main`` — no mocking of
domain components. The CLI itself must remain orchestration-only; these
tests guard against it accidentally acquiring scoring/formatting logic of
its own.
"""

from __future__ import annotations

import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys

import pytest

import requirements_quality_assessment.cli as cli_module
from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cli import main
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.reader import RequirementReader
from requirements_quality_assessment.reporter import ConsoleReporter

POSITIVE_REQUIREMENT = (
    "Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с."
)
VAGUE_REQUIREMENT = "Система повинна швидко оновити статус."


def _write(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "requirements.txt"
    path.write_text(text, encoding="utf-8")
    return path


def _parser_dependencies_available() -> bool:
    try:
        if (
            importlib.metadata.version("spacy") != "3.8.16"
            or importlib.metadata.version("uk-core-news-sm") != "3.8.0"
        ):
            return False
    except importlib.metadata.PackageNotFoundError:
        return False
    return True


def test_end_to_end_pipeline_renders_console_report(tmp_path, capsys) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n")

    exit_code = main([str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    assert "Вимога R001" in captured.out
    assert "Підсумок специфікації" in captured.out
    assert "Вимог: 1" in captured.out
    assert "Traceback" not in captured.out


def test_known_positive_requirement_resolves_to_fully_computed_profile(
    tmp_path, capsys
) -> None:
    pytest.importorskip("spacy")
    if not _parser_dependencies_available():
        pytest.skip("Selected spaCy 3.8.16 / uk_core_news_sm 3.8.0 parser is not installed")

    path = _write(tmp_path, f"{POSITIVE_REQUIREMENT}\n")

    exit_code = main([str(path)])

    captured = capsys.readouterr()
    assert exit_code == 0

    requirement_section, _, specification_section = captured.out.partition(
        "Підсумок специфікації"
    )
    for label in ("Повнота", "Перевірюваність", "Однозначність"):
        assert f"{label}: 1" in requirement_section
        assert f"{label}: 1" in specification_section

    assert "PARSER_UNAVAILABLE" not in captured.out


def test_multiple_requirements_preserve_source_order(tmp_path, capsys) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n{POSITIVE_REQUIREMENT}\n")

    main([str(path)])

    captured = capsys.readouterr()
    first = captured.out.index("Вимога R001")
    second = captured.out.index("Вимога R002")
    assert first < second
    assert VAGUE_REQUIREMENT in captured.out[first:second]
    assert POSITIVE_REQUIREMENT in captured.out[second:]


def test_blank_lines_are_ignored_and_ids_stay_contiguous(tmp_path, capsys) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n\n{POSITIVE_REQUIREMENT}\n")

    main([str(path)])

    captured = capsys.readouterr()
    assert "Вимога R001" in captured.out
    assert "Вимога R002" in captured.out
    assert "Вимога R003" not in captured.out


def test_vague_term_signal_is_not_converted_into_a_confirmed_defect(
    tmp_path, capsys
) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n")

    main([str(path)])

    captured = capsys.readouterr()
    assert "SIGNAL: «швидко»" in captured.out
    assert "а не підтверджений дефект" in captured.out
    assert "kind: QUALITY_PROBLEM" not in captured.out


def test_missing_input_file_reports_error_and_nonzero_exit(tmp_path, capsys) -> None:
    missing = tmp_path / "does-not-exist.txt"

    exit_code = main([str(missing)])

    captured = capsys.readouterr()
    assert exit_code != 0
    assert captured.out == ""
    assert str(missing) in captured.err
    assert "Traceback" not in captured.err


def test_invalid_utf8_input_reports_error_and_nonzero_exit(tmp_path, capsys) -> None:
    path = tmp_path / "invalid.txt"
    path.write_bytes(b"\xff\xfe not valid utf-8")

    exit_code = main([str(path)])

    captured = capsys.readouterr()
    assert exit_code != 0
    assert captured.out == ""
    assert captured.err.strip() != ""
    assert "Traceback" not in captured.err


def test_report_output_has_no_scalar_score(tmp_path, capsys) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n")

    main([str(path)])

    captured = capsys.readouterr()
    assert "Повнота:" in captured.out
    assert "Перевірюваність:" in captured.out
    assert "Однозначність:" in captured.out
    assert "RequirementQualityScore" not in captured.out
    assert "FileQualityScore" not in captured.out


def test_module_entry_point_preserves_ukrainian_output_with_legacy_encoding(tmp_path) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n")
    environment = os.environ.copy()
    environment["PYTHONIOENCODING"] = "cp1252"

    completed = subprocess.run(
        [sys.executable, "-m", "requirements_quality_assessment", str(path)],
        capture_output=True,
        encoding="utf-8",
        env=environment,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
    assert VAGUE_REQUIREMENT in completed.stdout
    assert "SIGNAL: «швидко»" in completed.stdout


def test_default_view_equals_explicit_user_view(tmp_path, capsys) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n")

    assert main([str(path)]) == 0
    default = capsys.readouterr()
    assert main(["--view", "user", str(path)]) == 0
    explicit = capsys.readouterr()

    assert explicit == default


def test_explicit_audit_view_matches_existing_console_reporter_exactly(
    tmp_path, capsys
) -> None:
    path = _write(tmp_path, f"{VAGUE_REQUIREMENT}\n")
    requirements = RequirementReader().read(path)
    extractor = BaselineFeatureExtractor()
    assessor = RequirementQualityAssessor()
    records = tuple(
        assessor.assess_record(extractor.extract(requirement))
        for requirement in requirements
    )
    specification = SpecificationQualityAggregator().aggregate(
        record.quality_profile for record in records
    )
    expected = ConsoleReporter().render(records, specification)

    assert main(["--view", "audit", str(path)]) == 0
    captured = capsys.readouterr()

    assert captured.err == ""
    assert captured.out == expected + "\n"


@pytest.mark.parametrize("view", ("user", "audit"))
def test_each_view_receives_one_completed_record_and_one_aggregate(
    monkeypatch, capsys, view
) -> None:
    requirement = object()
    extraction = object()
    profile = object()
    specification = object()

    class Record:
        quality_profile = profile

    record = Record()
    calls = {"read": 0, "extract": 0, "assess": 0, "aggregate": 0, "render": 0}

    class Reader:
        def read(self, path):
            calls["read"] += 1
            assert path == "requirements.txt"
            return (requirement,)

    class Extractor:
        def extract(self, value):
            calls["extract"] += 1
            assert value is requirement
            return extraction

    class Assessor:
        def assess_record(self, value):
            calls["assess"] += 1
            assert value is extraction
            return record

    class Aggregator:
        def aggregate(self, profiles):
            calls["aggregate"] += 1
            assert tuple(profiles) == (profile,)
            return specification

    class UserReporter:
        def render(self, records, supplied_specification):
            assert view == "user"
            calls["render"] += 1
            assert records == (record,)
            assert supplied_specification is specification
            return "user"

    class AuditReporter:
        def render(self, records, supplied_specification):
            assert view == "audit"
            calls["render"] += 1
            assert records == (record,)
            assert supplied_specification is specification
            return "audit"

    monkeypatch.setattr(cli_module, "RequirementReader", Reader)
    monkeypatch.setattr(cli_module, "BaselineFeatureExtractor", Extractor)
    monkeypatch.setattr(cli_module, "RequirementQualityAssessor", Assessor)
    monkeypatch.setattr(cli_module, "SpecificationQualityAggregator", Aggregator)
    monkeypatch.setattr(cli_module, "UserConsoleReporter", UserReporter)
    monkeypatch.setattr(cli_module, "ConsoleReporter", AuditReporter)

    assert main(["--view", view, "requirements.txt"]) == 0
    captured = capsys.readouterr()

    assert captured.out == f"{view}\n"
    assert captured.err == ""
    assert calls == {"read": 1, "extract": 1, "assess": 1, "aggregate": 1, "render": 1}
