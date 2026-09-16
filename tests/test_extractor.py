"""Six-family production extractor orchestration and integration behavior."""

from dataclasses import dataclass, field
from decimal import Decimal
import subprocess
import sys
import textwrap
from typing import Any

import pytest

from requirements_quality_assessment.domain import (
    BoundaryInclusivity,
    ComparatorComponent,
    ComparatorLabel,
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DetectionStatus,
    DiagnosticSpan,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    NumericValueComponent,
    QuantitativeConstraintObservation,
    Requirement,
    TextComponent,
    UnitComponent,
    UnitLabel,
    VagueTermOccurrence,
)
from requirements_quality_assessment.extractor import (
    BaselineFeatureExtractor,
    FeatureExtractor,
)


@dataclass
class _FakeDetector:
    name: str
    outcome: FeatureDetectionOutcome[Any]
    evidence: tuple[Evidence, ...] = ()
    call_log: list[str] | None = None
    call_count: int = 0
    received_requirements: list[Requirement] = field(default_factory=list)

    def detect(
        self, requirement: Requirement
    ) -> tuple[FeatureDetectionOutcome[Any], tuple[Evidence, ...]]:
        self.call_count += 1
        self.received_requirements.append(requirement)
        if self.call_log is not None:
            self.call_log.append(self.name)
        return self.outcome, self.evidence


def _outcome(
    feature_id: FeatureId,
    observations: tuple[Any, ...] = (),
    diagnostics: tuple[DetectionDiagnostic, ...] = (),
) -> FeatureDetectionOutcome[Any]:
    return FeatureDetectionOutcome(
        feature_id=feature_id,
        observations=observations,
        processing_status=(
            DetectionProcessingStatus.INCOMPLETE
            if diagnostics
            else DetectionProcessingStatus.COMPLETE
        ),
        diagnostics=diagnostics,
    )


def _empty_fakes(
    *, call_log: list[str] | None = None
) -> dict[str, _FakeDetector]:
    return {
        "condition": _FakeDetector(
            "condition_context", _outcome(FeatureId.CONDITION_CONTEXT), call_log=call_log
        ),
        "expected": _FakeDetector(
            "expected_result", _outcome(FeatureId.EXPECTED_RESULT), call_log=call_log
        ),
        "acceptance": _FakeDetector(
            "acceptance_criterion",
            _outcome(FeatureId.ACCEPTANCE_CRITERION),
            call_log=call_log,
        ),
        "quantitative": _FakeDetector(
            "quantitative_constraint",
            _outcome(FeatureId.QUANTITATIVE_CONSTRAINT),
            call_log=call_log,
        ),
        "verification": _FakeDetector(
            "verification_method",
            _outcome(FeatureId.VERIFICATION_METHOD),
            call_log=call_log,
        ),
        "vague": _FakeDetector(
            "vague_term_occurrence",
            _outcome(FeatureId.VAGUE_TERM_OCCURRENCE),
            call_log=call_log,
        ),
    }


def _extractor(fakes: dict[str, _FakeDetector]) -> BaselineFeatureExtractor:
    return BaselineFeatureExtractor(
        condition_context_detector=fakes["condition"],
        expected_result_detector=fakes["expected"],
        acceptance_criterion_detector=fakes["acceptance"],
        quantitative_detector=fakes["quantitative"],
        verification_method_detector=fakes["verification"],
        vague_term_detector=fakes["vague"],
    )


def _source(
    requirement: Requirement,
    evidence_id: str,
    feature_id: FeatureId,
    start: int,
    end: int,
    rule_id: str,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        requirement_id=requirement.id,
        feature_id=feature_id,
        text=requirement.text[start:end],
        start_offset=start,
        end_offset=end,
        rule_id=rule_id,
    )


def _simple_result(
    requirement: Requirement,
    feature_id: FeatureId,
    evidence_id: str,
    start: int,
    end: int,
) -> tuple[FeatureDetectionOutcome[FeatureObservation], tuple[Evidence, ...]]:
    source = _source(
        requirement, evidence_id, feature_id, start, end, f"RULE-{feature_id.value}"
    )
    observation = FeatureObservation(feature_id, (evidence_id,))
    return _outcome(feature_id, (observation,)), (source,)


def _quantitative_observation(
    refs: tuple[str, ...],
    *,
    metric: TextComponent | None = None,
    comparator: ComparatorComponent | None = None,
    value: NumericValueComponent | None = None,
    unit: UnitComponent | None = None,
    context: TextComponent | None = None,
) -> QuantitativeConstraintObservation:
    return QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=metric,
        comparator=comparator,
        value=value,
        unit=unit,
        context=context,
        unresolved_components=(),
        evidence_refs=refs,
    )


def _as_protocol(extractor: FeatureExtractor) -> FeatureExtractor:
    return extractor


def _run_real_integration(source: str) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys\nsys.path.insert(0, 'src')\n" + textwrap.dedent(source),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_all_empty_preserves_protocol_requirement_and_top_level_call_contract() -> None:
    requirement = Requirement("R001", 1, "Система формує звіт.")
    call_log: list[str] = []
    fakes = _empty_fakes(call_log=call_log)
    extractor = _as_protocol(_extractor(fakes))

    result = extractor.extract(requirement)

    assert result.requirement is requirement
    assert result.evidence == ()
    assert call_log == [
        "condition_context",
        "expected_result",
        "acceptance_criterion",
        "quantitative_constraint",
        "verification_method",
        "vague_term_occurrence",
    ]
    for fake in fakes.values():
        assert fake.call_count == 1
        assert fake.received_requirements == [requirement]
        assert fake.received_requirements[0] is requirement
    outcomes = (
        result.features.condition_contexts,
        result.features.expected_results,
        result.features.acceptance_criteria,
        result.features.quantitative_constraints,
        result.features.verification_methods,
        result.features.vague_term_occurrences,
    )
    assert all(item.status is DetectionStatus.NOT_DETECTED for item in outcomes)
    assert outcomes == tuple(fake.outcome for fake in fakes.values())


def test_one_populated_family_is_mapped_without_rebuilding_objects() -> None:
    requirement = Requirement("R002", 2, "Система швидко оновлює статус.")
    fakes = _empty_fakes()
    start = requirement.text.index("швидко")
    source = _source(
        requirement,
        "UK-VAGUE-001:E001",
        FeatureId.VAGUE_TERM_OCCURRENCE,
        start,
        start + len("швидко"),
        "UK-VAGUE-001",
    )
    observation = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "uk_vague_terms_v1",
        "швидко",
        (source.evidence_id,),
    )
    vague_outcome = _outcome(FeatureId.VAGUE_TERM_OCCURRENCE, (observation,))
    fakes["vague"] = _FakeDetector("vague_term_occurrence", vague_outcome, (source,))

    result = _extractor(fakes).extract(requirement)

    assert result.features.vague_term_occurrences is vague_outcome
    assert result.features.vague_term_occurrences.observations[0] is observation
    assert result.evidence == (source,)
    assert result.evidence[0] is source
    assert result.features.condition_contexts is fakes["condition"].outcome
    assert result.features.expected_results is fakes["expected"].outcome
    assert result.features.acceptance_criteria is fakes["acceptance"].outcome
    assert result.features.quantitative_constraints is fakes["quantitative"].outcome
    assert result.features.verification_methods is fakes["verification"].outcome


def test_all_six_families_survive_simultaneously_with_typed_quantitative_data() -> None:
    requirement = Requirement(
        "R003", 3, "умова результат критерій 2 с перевірка швидко"
    )
    fakes = _empty_fakes()
    simple_specs = (
        ("condition", FeatureId.CONDITION_CONTEXT, "умова", "C:E1"),
        ("expected", FeatureId.EXPECTED_RESULT, "результат", "R:E1"),
        ("acceptance", FeatureId.ACCEPTANCE_CRITERION, "критерій", "A:E1"),
        ("verification", FeatureId.VERIFICATION_METHOD, "перевірка", "V:E1"),
    )
    expected_objects: dict[str, Any] = {}
    for key, feature_id, text, evidence_id in simple_specs:
        start = requirement.text.index(text)
        outcome, evidence = _simple_result(
            requirement, feature_id, evidence_id, start, start + len(text)
        )
        expected_objects[key] = outcome
        fakes[key] = _FakeDetector(key, outcome, evidence)

    value_start = requirement.text.index("2")
    unit_start = requirement.text.index("с", value_start)
    value_source = _source(
        requirement,
        "Q:VALUE",
        FeatureId.QUANTITATIVE_CONSTRAINT,
        value_start,
        value_start + 1,
        "QUANT-001",
    )
    unit_source = _source(
        requirement,
        "Q:UNIT",
        FeatureId.QUANTITATIVE_CONSTRAINT,
        unit_start,
        unit_start + 1,
        "QUANT-001",
    )
    quantitative = _quantitative_observation(
        (value_source.evidence_id, unit_source.evidence_id),
        value=NumericValueComponent(Decimal("2"), (value_source.evidence_id,)),
        unit=UnitComponent(UnitLabel.SECOND, (unit_source.evidence_id,)),
    )
    quantitative_outcome = _outcome(
        FeatureId.QUANTITATIVE_CONSTRAINT, (quantitative,)
    )
    fakes["quantitative"] = _FakeDetector(
        "quantitative", quantitative_outcome, (value_source, unit_source)
    )

    vague_start = requirement.text.index("швидко")
    vague_source = _source(
        requirement,
        "VG:E1",
        FeatureId.VAGUE_TERM_OCCURRENCE,
        vague_start,
        vague_start + len("швидко"),
        "UK-VAGUE-001",
    )
    vague = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "uk_vague_terms_v1",
        "швидко",
        (vague_source.evidence_id,),
    )
    vague_outcome = _outcome(FeatureId.VAGUE_TERM_OCCURRENCE, (vague,))
    fakes["vague"] = _FakeDetector("vague", vague_outcome, (vague_source,))

    result = _extractor(fakes).extract(requirement)

    assert result.features.condition_contexts is expected_objects["condition"]
    assert result.features.expected_results is expected_objects["expected"]
    assert result.features.acceptance_criteria is expected_objects["acceptance"]
    assert result.features.quantitative_constraints is quantitative_outcome
    assert result.features.quantitative_constraints.observations[0] is quantitative
    assert result.features.verification_methods is expected_objects["verification"]
    assert result.features.vague_term_occurrences is vague_outcome
    assert len(result.evidence) == 7


def test_mixed_family_statuses_remain_independent_and_identical() -> None:
    requirement = Requirement("R004", 4, "умова результат")
    fakes = _empty_fakes()
    condition_outcome, condition_evidence = _simple_result(
        requirement, FeatureId.CONDITION_CONTEXT, "C:E1", 0, len("умова")
    )
    diagnostic = DetectionDiagnostic(
        "UNRESOLVED", "candidate is unresolved", "RULE"
    )
    expected_outcome = _outcome(
        FeatureId.EXPECTED_RESULT, diagnostics=(diagnostic,)
    )
    result_start = requirement.text.index("результат")
    acceptance_outcome, acceptance_evidence = _simple_result(
        requirement,
        FeatureId.ACCEPTANCE_CRITERION,
        "A:E1",
        result_start,
        result_start + len("результат"),
    )
    acceptance_outcome = FeatureDetectionOutcome(
        feature_id=FeatureId.ACCEPTANCE_CRITERION,
        observations=acceptance_outcome.observations,
        processing_status=DetectionProcessingStatus.INCOMPLETE,
        diagnostics=(diagnostic,),
    )
    fakes["condition"] = _FakeDetector(
        "condition", condition_outcome, condition_evidence
    )
    fakes["expected"] = _FakeDetector("expected", expected_outcome)
    fakes["acceptance"] = _FakeDetector(
        "acceptance", acceptance_outcome, acceptance_evidence
    )

    result = _extractor(fakes).extract(requirement)

    assert result.features.condition_contexts is condition_outcome
    assert result.features.condition_contexts.status is DetectionStatus.DETECTED
    assert result.features.expected_results is expected_outcome
    assert result.features.expected_results.status is DetectionStatus.UNRESOLVED
    assert result.features.acceptance_criteria is acceptance_outcome
    assert result.features.acceptance_criteria.status is DetectionStatus.DETECTED
    assert result.features.quantitative_constraints.status is DetectionStatus.NOT_DETECTED
    assert result.features.verification_methods.status is DetectionStatus.NOT_DETECTED
    assert result.features.vague_term_occurrences.status is DetectionStatus.NOT_DETECTED


def test_global_evidence_order_uses_source_family_then_local_tie_breaks() -> None:
    requirement = Requirement("R005", 5, "x" * 70)
    fakes = _empty_fakes()
    specs = (
        ("condition", FeatureId.CONDITION_CONTEXT, 30, 40, "C:E1"),
        ("expected", FeatureId.EXPECTED_RESULT, 0, 20, "R:E1"),
        ("acceptance", FeatureId.ACCEPTANCE_CRITERION, 0, 20, "A:E1"),
        ("verification", FeatureId.VERIFICATION_METHOD, 50, 60, "V:E1"),
    )
    for key, family, start, end, evidence_id in specs:
        outcome, evidence = _simple_result(
            requirement, family, evidence_id, start, end
        )
        fakes[key] = _FakeDetector(key, outcome, evidence)

    quantitative_source = _source(
        requirement, "Q:E1", FeatureId.QUANTITATIVE_CONSTRAINT, 10, 15, "Q"
    )
    quantitative = _quantitative_observation(
        (quantitative_source.evidence_id,),
        value=NumericValueComponent(Decimal("1"), (quantitative_source.evidence_id,)),
        unit=UnitComponent(UnitLabel.SECOND, (quantitative_source.evidence_id,)),
    )
    fakes["quantitative"] = _FakeDetector(
        "quantitative",
        _outcome(FeatureId.QUANTITATIVE_CONSTRAINT, (quantitative,)),
        (quantitative_source,),
    )
    vague_source = _source(
        requirement, "VG:E1", FeatureId.VAGUE_TERM_OCCURRENCE, 25, 30, "VG"
    )
    vague = VagueTermOccurrence(
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "uk_vague_terms_v1",
        "швидко",
        (vague_source.evidence_id,),
    )
    fakes["vague"] = _FakeDetector(
        "vague",
        _outcome(FeatureId.VAGUE_TERM_OCCURRENCE, (vague,)),
        (vague_source,),
    )

    result = _extractor(fakes).extract(requirement)

    assert [item.evidence_id for item in result.evidence] == [
        "R:E1",
        "A:E1",
        "Q:E1",
        "VG:E1",
        "C:E1",
        "V:E1",
    ]


def test_same_span_cross_family_evidence_is_not_deduplicated() -> None:
    requirement = Requirement("R006", 6, "Система формує звіт.")
    fakes = _empty_fakes()
    end = len(requirement.text)
    expected_outcome, expected_evidence = _simple_result(
        requirement, FeatureId.EXPECTED_RESULT, "RESULT-UK-001:E001", 0, end
    )
    acceptance_outcome, acceptance_evidence = _simple_result(
        requirement,
        FeatureId.ACCEPTANCE_CRITERION,
        "ACCEPT-QUANT-001:E001",
        0,
        end,
    )
    fakes["expected"] = _FakeDetector(
        "expected", expected_outcome, expected_evidence
    )
    fakes["acceptance"] = _FakeDetector(
        "acceptance", acceptance_outcome, acceptance_evidence
    )

    result = _extractor(fakes).extract(requirement)

    assert result.evidence == (expected_evidence[0], acceptance_evidence[0])
    assert result.evidence[0].text == result.evidence[1].text
    assert result.evidence[0].evidence_id != result.evidence[1].evidence_id


def test_repeated_source_text_at_different_offsets_remains_distinct() -> None:
    requirement = Requirement("R007", 7, "тест і тест")
    fakes = _empty_fakes()
    first = _source(
        requirement, "V:E1", FeatureId.VERIFICATION_METHOD, 0, 4, "V"
    )
    second = _source(
        requirement, "V:E2", FeatureId.VERIFICATION_METHOD, 7, 11, "V"
    )
    observations = tuple(
        FeatureObservation(FeatureId.VERIFICATION_METHOD, (item.evidence_id,))
        for item in (first, second)
    )
    fakes["verification"] = _FakeDetector(
        "verification",
        _outcome(FeatureId.VERIFICATION_METHOD, observations),
        (second, first),
    )

    result = _extractor(fakes).extract(requirement)

    assert result.evidence == (first, second)
    assert result.evidence[0].text == result.evidence[1].text == "тест"


def test_duplicate_evidence_id_surfaces_domain_invariant_failure() -> None:
    requirement = Requirement("R008", 8, "alpha beta")
    fakes = _empty_fakes()
    fakes["condition"].evidence = (
        _source(requirement, "DUPLICATE", FeatureId.CONDITION_CONTEXT, 0, 5, "C"),
    )
    fakes["expected"].evidence = (
        _source(requirement, "DUPLICATE", FeatureId.EXPECTED_RESULT, 6, 10, "R"),
    )

    with pytest.raises(ValueError, match="duplicate evidence_id"):
        _extractor(fakes).extract(requirement)


def test_dangling_ref_surfaces_domain_invariant_failure() -> None:
    requirement = Requirement("R009", 9, "результат")
    fakes = _empty_fakes()
    observation = FeatureObservation(FeatureId.EXPECTED_RESULT, ("MISSING:E001",))
    fakes["expected"].outcome = _outcome(
        FeatureId.EXPECTED_RESULT, (observation,)
    )

    with pytest.raises(ValueError, match="dangling accepted evidence_ref"):
        _extractor(fakes).extract(requirement)


def test_wrong_requirement_id_surfaces_domain_invariant_failure() -> None:
    requirement = Requirement("R010", 10, "evidence")
    fakes = _empty_fakes()
    fakes["condition"].evidence = (
        Evidence(
            "C:E1",
            "OTHER",
            FeatureId.CONDITION_CONTEXT,
            "evidence",
            0,
            8,
            "C",
        ),
    )

    with pytest.raises(ValueError, match="requirement_id"):
        _extractor(fakes).extract(requirement)


def test_source_round_trip_failure_surfaces_domain_invariant_failure() -> None:
    requirement = Requirement("R011", 11, "alpha beta")
    fakes = _empty_fakes()
    fakes["condition"].evidence = (
        Evidence(
            "C:E1",
            requirement.id,
            FeatureId.CONDITION_CONTEXT,
            "xxxxx",
            0,
            5,
            "C",
        ),
    )

    with pytest.raises(ValueError, match="round-trip"):
        _extractor(fakes).extract(requirement)


def test_wrong_family_evidence_surfaces_domain_invariant_failure() -> None:
    requirement = Requirement("R012", 12, "result")
    fakes = _empty_fakes()
    source = _source(
        requirement, "E1", FeatureId.CONDITION_CONTEXT, 0, 6, "C"
    )
    observation = FeatureObservation(FeatureId.EXPECTED_RESULT, (source.evidence_id,))
    fakes["expected"] = _FakeDetector(
        "expected", _outcome(FeatureId.EXPECTED_RESULT, (observation,)), (source,)
    )

    with pytest.raises(ValueError, match="expected_result feature family"):
        _extractor(fakes).extract(requirement)


def test_diagnostics_remain_family_local_and_never_become_evidence() -> None:
    requirement = Requirement("R013", 13, "candidate")
    fakes = _empty_fakes()
    diagnostic = DetectionDiagnostic(
        code="RESULT_UNRESOLVED_CANDIDATE",
        explanation="candidate is unresolved",
        rule_id="RESULT-UK-001",
        candidate_span=DiagnosticSpan("candidate", 0, 9),
    )
    expected = _outcome(FeatureId.EXPECTED_RESULT, diagnostics=(diagnostic,))
    fakes["expected"] = _FakeDetector("expected", expected)

    result = _extractor(fakes).extract(requirement)

    assert result.features.expected_results is expected
    assert result.features.expected_results.diagnostics == (diagnostic,)
    assert result.evidence == ()


def test_quantitative_component_refs_are_preserved_and_resolved() -> None:
    requirement = Requirement("R014", 14, "не більше 2 с")
    comparator = _source(
        requirement, "Q:C", FeatureId.QUANTITATIVE_CONSTRAINT, 0, 9, "Q"
    )
    value = _source(
        requirement, "Q:V", FeatureId.QUANTITATIVE_CONSTRAINT, 10, 11, "Q"
    )
    unit = _source(
        requirement, "Q:U", FeatureId.QUANTITATIVE_CONSTRAINT, 12, 13, "Q"
    )
    observation = _quantitative_observation(
        (comparator.evidence_id, value.evidence_id, unit.evidence_id),
        comparator=ComparatorComponent(
            ComparatorLabel.LESS_THAN_OR_EQUAL,
            BoundaryInclusivity.INCLUSIVE,
            (comparator.evidence_id,),
        ),
        value=NumericValueComponent(Decimal("2"), (value.evidence_id,)),
        unit=UnitComponent(UnitLabel.SECOND, (unit.evidence_id,)),
    )
    fakes = _empty_fakes()
    fakes["quantitative"] = _FakeDetector(
        "quantitative",
        _outcome(FeatureId.QUANTITATIVE_CONSTRAINT, (observation,)),
        (unit, comparator, value),
    )

    result = _extractor(fakes).extract(requirement)

    assert result.features.quantitative_constraints.observations[0] is observation
    assert result.evidence == (comparator, value, unit)
    evidence_by_id = {item.evidence_id: item for item in result.evidence}
    assert set(observation.evidence_refs) == set(evidence_by_id)

    fakes["quantitative"].evidence = (comparator, value)
    with pytest.raises(ValueError, match="dangling accepted evidence_ref"):
        _extractor(fakes).extract(requirement)


def test_unexpected_detector_exception_is_not_converted_to_an_outcome() -> None:
    class _BrokenDetector:
        def detect(self, requirement: Requirement) -> Any:
            raise RuntimeError("detector failed")

    fakes = _empty_fakes()
    fakes["condition"] = _BrokenDetector()  # type: ignore[assignment]

    with pytest.raises(RuntimeError, match="detector failed"):
        _extractor(fakes).extract(Requirement("R015", 15, "text"))


def test_default_graph_smoke_returns_all_six_families() -> None:
    _run_real_integration(
        """
        from requirements_quality_assessment.domain import FeatureId, Requirement
        from requirements_quality_assessment.extractor import BaselineFeatureExtractor

        result = BaselineFeatureExtractor().extract(
            Requirement("R016", 16, "Система повинна швидко оновити статус.")
        )
        assert result.requirement.id == "R016"
        assert result.features.condition_contexts.feature_id is FeatureId.CONDITION_CONTEXT
        assert result.features.expected_results.feature_id is FeatureId.EXPECTED_RESULT
        assert result.features.acceptance_criteria.feature_id is FeatureId.ACCEPTANCE_CRITERION
        assert result.features.quantitative_constraints.feature_id is FeatureId.QUANTITATIVE_CONSTRAINT
        assert result.features.verification_methods.feature_id is FeatureId.VERIFICATION_METHOD
        assert result.features.vague_term_occurrences.feature_id is FeatureId.VAGUE_TERM_OCCURRENCE
        """
    )


def test_real_quantitative_acceptance_integration() -> None:
    _run_real_integration(
        """
        from requirements_quality_assessment.domain import DetectionStatus, Requirement
        from requirements_quality_assessment.extractor import BaselineFeatureExtractor

        requirement = Requirement(
            "R017", 17, "Система повинна відповісти не більше ніж за 2 с."
        )
        result = BaselineFeatureExtractor().extract(requirement)
        assert result.features.expected_results.status is DetectionStatus.DETECTED
        assert result.features.quantitative_constraints.status is DetectionStatus.DETECTED
        assert result.features.acceptance_criteria.status is DetectionStatus.DETECTED
        assert result.features.verification_methods.status is DetectionStatus.NOT_DETECTED
        evidence_by_id = {item.evidence_id: item for item in result.evidence}
        outcomes = (
            result.features.condition_contexts,
            result.features.expected_results,
            result.features.acceptance_criteria,
            result.features.verification_methods,
            result.features.vague_term_occurrences,
        )
        refs = [
            ref
            for outcome in outcomes
            for observation in outcome.observations
            for ref in observation.evidence_refs
        ]
        for observation in result.features.quantitative_constraints.observations:
            refs.extend(observation.evidence_refs)
            for component in (
                observation.metric, observation.comparator, observation.value,
                observation.unit, observation.context,
            ):
                if component is not None:
                    refs.extend(component.evidence_refs)
        assert all(ref in evidence_by_id for ref in refs)
        """
    )


def test_real_explicit_verification_integration() -> None:
    _run_real_integration(
        """
        from requirements_quality_assessment.domain import DetectionStatus, Requirement
        from requirements_quality_assessment.extractor import BaselineFeatureExtractor

        requirement = Requirement(
            "R018", 18, "Виконання перевіряється навантажувальним тестом."
        )
        result = BaselineFeatureExtractor().extract(requirement)
        assert result.features.verification_methods.status is DetectionStatus.DETECTED
        refs = result.features.verification_methods.observations[0].evidence_refs
        evidence_by_id = {item.evidence_id: item for item in result.evidence}
        assert [evidence_by_id[ref].text for ref in refs] == [
            "навантажувальним тестом"
        ]
        """
    )


def test_real_vague_term_integration_preserves_exact_source() -> None:
    _run_real_integration(
        """
        from requirements_quality_assessment.domain import DetectionStatus, Requirement
        from requirements_quality_assessment.extractor import BaselineFeatureExtractor

        requirement = Requirement(
            "R019", 19, "Система повинна швидко оновити статус."
        )
        result = BaselineFeatureExtractor().extract(requirement)
        outcome = result.features.vague_term_occurrences
        assert outcome.status is DetectionStatus.DETECTED
        source = next(
            item
            for item in result.evidence
            if item.evidence_id == outcome.observations[0].evidence_refs[0]
        )
        assert source.text == "швидко"
        assert requirement.text[source.start_offset : source.end_offset] == source.text
        """
    )


def test_full_r3_prime_verification_integration() -> None:
    _run_real_integration(
        """
        from requirements_quality_assessment.domain import DetectionStatus, Requirement
        from requirements_quality_assessment.extractor import BaselineFeatureExtractor

        requirement = Requirement(
            "R020",
            20,
            "Дані передаються через TLS 1.3; доступ до API — за OAuth 2.0/OIDC; "
            "критичні операції журналюються; дані клієнтів логічно ізолюються між "
            "tenant-ами; визначено негативні security tests.",
        )
        result = BaselineFeatureExtractor().extract(requirement)
        outcome = result.features.verification_methods
        assert outcome.status is DetectionStatus.DETECTED
        evidence_by_id = {item.evidence_id: item for item in result.evidence}
        sources = [
            evidence_by_id[ref]
            for observation in outcome.observations
            for ref in observation.evidence_refs
        ]
        assert [(item.text, item.start_offset, item.end_offset) for item in sources] == [
            ("негативні security tests", 158, 182)
        ]
        """
    )
