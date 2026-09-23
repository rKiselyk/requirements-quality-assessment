"""Real-parser acceptance coverage for the approved executable MVP subset."""

from fractions import Fraction

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cli import main
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState, DetectionStatus, FeatureId, FindingKind,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.reader import RequirementReader
from requirements_quality_assessment.reporter import ConsoleReporter


def test_real_parser_acceptance_pipeline_and_repeatability(tmp_path, capsys) -> None:
    # These cases exercise the approved Section 18 examples and detector baselines.
    texts = (
        "Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с.",
        "Система повинна швидко оновити статус.",
        "Система повинна відповісти не більше ніж за 2 с.",
        "Система повинна відповісти до 2 с.",
        "Виконання перевіряється навантажувальним тестом.",
    )
    path = tmp_path / "requirements.txt"
    path.write_text("  " + texts[0] + "  \n\n" + "\n".join(texts[1:]) + "\n", encoding="utf-8")

    requirements = RequirementReader().read(path)
    assert [(r.id, r.source_line, r.text) for r in requirements] == [
        (f"R{i:03d}", line, text)
        for i, (line, text) in enumerate(zip((1, 3, 4, 5, 6), texts), start=1)
    ]

    extractor = BaselineFeatureExtractor()
    assessor = RequirementQualityAssessor()
    results = tuple((r, extractor.extract(r)) for r in requirements)
    records = tuple(assessor.assess_record(result) for _, result in results)
    profiles = tuple(record.quality_profile for record in records)
    specification = SpecificationQualityAggregator().aggregate(profiles)

    families = (
        "condition_contexts", "expected_results", "acceptance_criteria",
        "quantitative_constraints", "verification_methods", "vague_term_occurrences",
    )
    assert len({getattr(results[0][1].features, name).feature_id for name in families}) == 6
    assert {getattr(results[0][1].features, name).feature_id for name in families} == set(FeatureId)
    for requirement, result in results:
        assert result.requirement is requirement
        assert all(
            requirement.text[e.start_offset:e.end_offset] == e.text
            for e in result.evidence
        )

    positive = profiles[0]
    assert (positive.completeness.value, positive.verifiability.value,
            positive.unambiguity.value) == (Fraction(1), Fraction(1), Fraction(1))
    assert [(e.text, e.start_offset, e.end_offset) for e in results[0][1].evidence] == [
        ("Якщо сервіс недоступний", 0, 23),
        ("система повинна відповісти не більше ніж за 2 с", 25, 72),
        ("система повинна відповісти не більше ніж за 2 с", 25, 72),
        ("не більше ніж за 2 с", 52, 72),
    ]

    vague = profiles[1]
    assert (vague.completeness.value, vague.verifiability.value,
            vague.unambiguity.value) == (Fraction(1, 3), Fraction(0), Fraction(1, 2))
    signal = vague.unambiguity.findings[0]
    assert signal.kind is FindingKind.SIGNAL
    assert signal.rule_id == "FIND-U-VAGUE-001"
    source = {e.evidence_id: e for e in results[1][1].evidence}[signal.evidence_refs[0]]
    assert (source.text, source.start_offset, source.end_offset) == ("швидко", 16, 22)

    quantitative = profiles[2]
    assert (quantitative.completeness.value, quantitative.verifiability.value,
            quantitative.unambiguity.value) == (Fraction(2, 3), Fraction(1), Fraction(1))
    assert results[2][1].features.quantitative_constraints.status is DetectionStatus.DETECTED

    unresolved = profiles[3]
    assert results[3][1].features.acceptance_criteria.status is DetectionStatus.UNRESOLVED
    assert unresolved.completeness.state is CharacteristicAssessmentState.UNKNOWN
    assert unresolved.verifiability.state is CharacteristicAssessmentState.UNKNOWN
    assert unresolved.completeness.value is unresolved.verifiability.value is None

    verified = profiles[4]
    assert results[4][1].features.verification_methods.status is DetectionStatus.DETECTED
    assert verified.verifiability.value == Fraction(1, 2)

    assert (specification.completeness.value, specification.verifiability.value,
            specification.unambiguity.value) == (
        Fraction(2, 3), Fraction(5, 8), Fraction(9, 10),
    )
    assert (specification.completeness.computed_count,
            specification.completeness.unknown_count) == (3, 2)
    assert (specification.verifiability.computed_count,
            specification.verifiability.unknown_count) == (4, 1)
    assert specification.unambiguity.computed_count == 5

    report = ConsoleReporter().render(records, specification)
    assert "kind: SIGNAL" in report
    assert "kind: QUALITY_PROBLEM" not in report
    assert "no current QUALITY_PROBLEM" in report
    assert "value: 5/8" in report
    assert "value: UNKNOWN" in report
    assert [report.index(f"Requirement R{i:03d}") for i in range(1, 6)] == sorted(
        report.index(f"Requirement R{i:03d}") for i in range(1, 6)
    )

    assert main([str(path)]) == 0
    first_run = capsys.readouterr()
    assert first_run.err == ""
    assert first_run.out == report + "\n"
    assert main([str(path)]) == 0
    second_run = capsys.readouterr()
    assert second_run == first_run


def test_empty_input_has_not_applicable_aggregates(tmp_path, capsys) -> None:
    path = tmp_path / "empty.txt"
    path.write_text(" \n\t\n", encoding="utf-8")
    assert main([str(path)]) == 0
    output = capsys.readouterr().out
    assert "Analyzed requirements: 0" in output
    assert output.count("  state: NOT_APPLICABLE") == 3
    assert output.count("  value: NOT_APPLICABLE") == 3
    assert output.count("  total_count: 0") == 3
