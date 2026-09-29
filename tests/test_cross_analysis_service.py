"""IMP-09 composition and application-orchestration integration tests."""

from dataclasses import FrozenInstanceError, fields, replace
from fractions import Fraction
from pathlib import Path

import pytest

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    CrossRequirementProjector,
    CrossResultState,
    QbConsistencyState,
    SpecificationAssessment,
    SpecificationAssessmentResult,
    SpecificationAssessmentService,
)
from requirements_quality_assessment.domain import (
    Requirement,
    RequirementAssessmentRecord,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor


UPPER_TWO = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
UPPER_FIVE = "Час відгуку ≤ 5 с при 500 одночасних користувачах"
LOWER_FIVE = "Час відгуку не нижче 5 с при 500 одночасних користувачах"


def _record(requirement_id: str, source_line: int, text: str):
    extraction = BaselineFeatureExtractor().extract(
        Requirement(requirement_id, source_line, text)
    )
    return RequirementQualityAssessor().assess_record(extraction)


def _records(*texts: str) -> tuple[RequirementAssessmentRecord, ...]:
    return tuple(
        _record(f"R{index:03d}", index, text)
        for index, text in enumerate(texts, start=1)
    )


def _direct_local_profile(records: tuple[RequirementAssessmentRecord, ...]):
    return SpecificationQualityAggregator().aggregate(
        tuple(record.quality_profile for record in records)
    )


def test_specification_assessment_valid_construction_and_exact_fields() -> None:
    result = SpecificationAssessmentService().assess(_records(UPPER_TWO))
    assessment = result.specification_assessment

    assert [item.name for item in fields(SpecificationAssessment)] == [
        "snapshot_id",
        "quality_profile",
        "qb_consistency",
    ]
    assert assessment.snapshot_id == result.projection.snapshot_id
    assert assessment.quality_profile is result.specification_assessment.quality_profile
    assert assessment.qb_consistency.state is QbConsistencyState.NOT_APPLICABLE
    for forbidden in (
        "value",
        "overall_score",
        "quality_score",
        "mean",
        "combined_score",
    ):
        assert not hasattr(assessment, forbidden)


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"snapshot_id": "snapshot"}, "AssessmentSnapshotId"),
        ({"quality_profile": object()}, "SpecificationQualityProfile"),
        ({"qb_consistency": object()}, "QbConsistencyAssessment"),
    ],
)
def test_specification_assessment_rejects_invalid_field_types(
    changes: dict[str, object], message: str
) -> None:
    assessment = SpecificationAssessmentService().assess(
        _records(UPPER_TWO)
    ).specification_assessment

    with pytest.raises(TypeError, match=message):
        replace(assessment, **changes)


def test_specification_assessment_rejects_snapshot_and_population_mismatch() -> None:
    one = SpecificationAssessmentService().assess(_records(UPPER_TWO))
    two = SpecificationAssessmentService().assess(_records(UPPER_TWO, UPPER_FIVE))

    with pytest.raises(ValueError, match="cross snapshots"):
        SpecificationAssessment(
            snapshot_id=one.snapshot_id,
            quality_profile=one.specification_assessment.quality_profile,
            qb_consistency=two.specification_assessment.qb_consistency,
        )

    with pytest.raises(ValueError, match="same source population"):
        SpecificationAssessment(
            snapshot_id=two.snapshot_id,
            quality_profile=one.specification_assessment.quality_profile,
            qb_consistency=two.specification_assessment.qb_consistency,
        )


def test_empty_and_single_requirement_runs_are_not_applicable() -> None:
    empty = SpecificationAssessmentService().assess(())
    single = SpecificationAssessmentService().assess(_records(UPPER_TWO))

    assert (
        empty.specification_assessment.qb_consistency.state
        is QbConsistencyState.NOT_APPLICABLE
    )
    assert empty.cross_results == ()
    assert empty.specification_assessment.quality_profile == _direct_local_profile(())
    assert (
        single.specification_assessment.qb_consistency.state
        is QbConsistencyState.NOT_APPLICABLE
    )
    assert single.cross_results == ()
    assert single.specification_assessment.quality_profile == _direct_local_profile(
        single.records
    )


def test_multi_requirement_compatible_and_conflict_runs() -> None:
    compatible_records = _records(UPPER_TWO, UPPER_FIVE)
    conflict_records = _records(UPPER_TWO, LOWER_FIVE)

    compatible = SpecificationAssessmentService().assess(compatible_records)
    conflict = SpecificationAssessmentService().assess(conflict_records)

    assert (
        compatible.specification_assessment.qb_consistency.state
        is QbConsistencyState.COMPUTED
    )
    assert compatible.specification_assessment.qb_consistency.value == Fraction(1, 1)
    assert [item.state for item in compatible.cross_results] == [
        CrossResultState.COMPATIBLE_WITHIN_RULE
    ]
    assert (
        conflict.specification_assessment.qb_consistency.state
        is QbConsistencyState.COMPUTED
    )
    assert conflict.specification_assessment.qb_consistency.value == Fraction(0, 1)
    assert conflict.specification_assessment.qb_consistency.rconf_participant_ids == (
        "R001",
        "R002",
    )
    assert [item.state for item in conflict.cross_results] == [
        CrossResultState.CONFIRMED_CONFLICT
    ]
    assert compatible.specification_assessment.quality_profile == _direct_local_profile(
        compatible_records
    )
    assert conflict.specification_assessment.quality_profile == _direct_local_profile(
        conflict_records
    )


def test_unknown_and_no_applicable_qb_do_not_change_local_profile() -> None:
    unknown_records = _records(
        "Система працює не більше 2 с",
        "Система працює не нижче 5 с",
    )
    not_applicable_records = _records(
        "Система має обробляти запити.",
        "Система має журналювати події.",
    )

    unknown = SpecificationAssessmentService().assess(unknown_records)
    not_applicable = SpecificationAssessmentService().assess(not_applicable_records)

    assert (
        unknown.specification_assessment.qb_consistency.state
        is QbConsistencyState.UNKNOWN
    )
    assert [item.state for item in unknown.cross_results] == [
        CrossResultState.ASSESSMENT_UNRESOLVED
    ]
    assert unknown.specification_assessment.quality_profile == _direct_local_profile(
        unknown_records
    )
    assert (
        not_applicable.specification_assessment.qb_consistency.state
        is QbConsistencyState.NOT_APPLICABLE
    )
    assert not_applicable.specification_assessment.quality_profile == _direct_local_profile(
        not_applicable_records
    )


def test_changed_local_aggregate_does_not_change_qb_result() -> None:
    records = _records(UPPER_TWO, LOWER_FIVE)
    baseline = SpecificationAssessmentService().assess(records)
    changed_profile = replace(
        baseline.specification_assessment.quality_profile,
        completeness=replace(
            baseline.specification_assessment.quality_profile.completeness,
            value=Fraction(0, 1),
        ),
    )

    class FixedLocalAggregator:
        def aggregate(self, profiles):
            tuple(profiles)
            return changed_profile

    changed = SpecificationAssessmentService(
        quality_aggregator=FixedLocalAggregator()
    ).assess(records)

    assert changed.specification_assessment.quality_profile == changed_profile
    assert (
        changed.specification_assessment.qb_consistency
        == baseline.specification_assessment.qb_consistency
    )
    assert changed.cross_results == baseline.cross_results
    assert changed.materiality == baseline.materiality
    assert changed.snapshot_id == baseline.snapshot_id


class _CallSpy:
    def __init__(self, delegate, method_name: str, event: str, events: list[str]):
        self.delegate = delegate
        self.method_name = method_name
        self.event = event
        self.events = events
        self.calls = []

    def __getattr__(self, name: str):
        if name != self.method_name:
            return getattr(self.delegate, name)

        def call(*args, **kwargs):
            self.events.append(self.event)
            self.calls.append((args, kwargs))
            return getattr(self.delegate, self.method_name)(*args, **kwargs)

        return call


def test_service_sequences_each_component_once_after_complete_records_exist() -> None:
    from requirements_quality_assessment.cross_analysis import (
        ExhaustivePairSelector,
        QbConsistencyAggregator,
        QbMaterialityClassifier,
        QbObservationPairAssessor,
    )

    records = _records(UPPER_TWO, LOWER_FIVE)
    events: list[str] = []
    local = _CallSpy(SpecificationQualityAggregator(), "aggregate", "local", events)
    projector = _CallSpy(CrossRequirementProjector(), "project", "project", events)
    materiality = _CallSpy(QbMaterialityClassifier(), "classify", "materiality", events)
    selector = _CallSpy(ExhaustivePairSelector(), "select", "select", events)
    assessor = _CallSpy(QbObservationPairAssessor(), "assess", "assess", events)
    aggregator = _CallSpy(QbConsistencyAggregator(), "aggregate", "aggregate", events)

    SpecificationAssessmentService(
        quality_aggregator=local,
        projector=projector,
        materiality_classifier=materiality,
        pair_selector=selector,
        pair_assessor=assessor,
        consistency_aggregator=aggregator,
    ).assess(records)

    assert events == ["local", "project", "materiality", "select", "assess", "aggregate"]
    assert [
        len(spy.calls)
        for spy in (local, projector, materiality, selector, aggregator)
    ] == [1, 1, 1, 1, 1]
    assert len(assessor.calls) == 1
    assert projector.calls[0][0][0] is records
    assert all(isinstance(item, RequirementAssessmentRecord) for item in records)


def test_pair_assessor_processes_complete_selected_universe_once() -> None:
    from requirements_quality_assessment.cross_analysis import QbObservationPairAssessor

    records = _records(
        "Система працює не більше 2 с та не нижче 3 с",
        "Система працює не більше 4 с та не нижче 5 с",
    )
    calls = []

    class PairSpy:
        def __init__(self):
            self.delegate = QbObservationPairAssessor()

        def assess(self, candidate, projection):
            calls.append(candidate)
            return self.delegate.assess(candidate, projection)

    result = SpecificationAssessmentService(pair_assessor=PairSpy()).assess(records)

    assert len(calls) == 4
    assert len({item.order_key for item in calls}) == 4
    assert [item.order_key for item in calls] == sorted(
        item.order_key for item in calls
    )
    assert tuple(item.observation_refs for item in result.cross_results) == tuple(
        (item.left, item.right) for item in calls
    )


def test_service_uses_accepted_conflict_set_builder_once(monkeypatch) -> None:
    import requirements_quality_assessment.cross_analysis.aggregation as aggregation

    real_builder = aggregation.QbConflictSetBuilder
    calls = []

    class BuilderSpy:
        def build(self, snapshot, results, materiality):
            calls.append((snapshot, results, materiality))
            return real_builder().build(snapshot, results, materiality)

    monkeypatch.setattr(aggregation, "QbConflictSetBuilder", BuilderSpy)

    result = SpecificationAssessmentService().assess(_records(UPPER_TWO, LOWER_FIVE))

    assert len(calls) == 1
    assert result.specification_assessment.qb_consistency.rconf_participant_ids == (
        "R001",
        "R002",
    )


def test_result_preserves_materiality_audits_resolver_and_snapshot_association() -> None:
    result = SpecificationAssessmentService().assess(_records(UPPER_TWO, LOWER_FIVE))

    assert result.materiality.audit_records
    assert result.resolver is result.projection.resolver
    assert all(item.snapshot_id == result.snapshot_id for item in result.cross_results)
    assert result.materiality.snapshot_id == result.snapshot_id
    assert tuple(item.result_id for item in result.cross_results) == (
        result.specification_assessment.qb_consistency.cross_result_ids
    )
    assert tuple(item.diagnostic_ref for item in result.materiality.audit_records) == (
        result.specification_assessment.qb_consistency.materiality_diagnostic_refs
    )


def test_result_rejects_foreign_cross_and_materiality_artifacts() -> None:
    first = SpecificationAssessmentService().assess(_records(UPPER_TWO, LOWER_FIVE))
    second = SpecificationAssessmentService().assess(_records(UPPER_FIVE, LOWER_FIVE))

    with pytest.raises(ValueError, match="cross results and projection"):
        replace(first, cross_results=second.cross_results)
    with pytest.raises(ValueError, match="materiality result and projection"):
        replace(first, materiality=second.materiality)


@pytest.mark.parametrize(
    "records",
    [
        [_record("R001", 1, UPPER_TWO)],
        (_record("R001", 1, UPPER_TWO), _record("R001", 2, UPPER_FIVE)),
        (_record("R001", 2, UPPER_TWO), _record("R002", 1, UPPER_FIVE)),
    ],
)
def test_invalid_record_collection_fails_fast(records) -> None:
    with pytest.raises((TypeError, ValueError)):
        SpecificationAssessmentService().assess(records)


def test_projection_failure_is_not_converted_to_unknown() -> None:
    class FailingProjector:
        def project(self, records):
            raise ValueError("projection integrity failure")

    with pytest.raises(ValueError, match="projection integrity failure"):
        SpecificationAssessmentService(projector=FailingProjector()).assess(
            _records(UPPER_TWO)
        )


def test_service_does_not_mutate_local_inputs_or_outputs() -> None:
    records = _records(UPPER_TWO, LOWER_FIVE)
    before = repr(records)

    result = SpecificationAssessmentService().assess(records)

    assert repr(records) == before
    assert result.records is records
    with pytest.raises(FrozenInstanceError):
        result.cross_results = ()
    with pytest.raises(FrozenInstanceError):
        result.specification_assessment.quality_profile = object()


def test_repeated_execution_is_deterministic() -> None:
    records = _records(UPPER_TWO, LOWER_FIVE)

    first = SpecificationAssessmentService().assess(records)
    second = SpecificationAssessmentService().assess(records)

    assert first.snapshot_id == second.snapshot_id
    assert first.specification_assessment == second.specification_assessment
    assert first.cross_results == second.cross_results
    assert first.materiality == second.materiality


def test_single_requirement_modules_do_not_import_cross_analysis() -> None:
    package_root = Path(__file__).parents[1] / "src" / "requirements_quality_assessment"
    forbidden = []
    for path in package_root.rglob("*.py"):
        if "cross_analysis" in path.parts:
            continue
        if "metrics" in path.parts:
            # M3-02 is an approved downstream composition boundary over the
            # completed local and QB assessments. It must not move this
            # dependency into any single-requirement module.
            continue
        if "performance_efficiency" in path.parts:
            # M3-04 is the approved downstream M + E_stat + E_dyn composition
            # boundary. Its target-scoped QB gate consumes completed cross
            # results without moving cross analysis into upstream modules.
            continue
        if path.name in {"cli.py", "cross_reporter.py", "reporter.py"}:
            # IMP-10 reporting/orchestration is the approved downstream
            # composition boundary and may consume both local and cross results.
            continue
        text = path.read_text(encoding="utf-8")
        if "cross_analysis" in text:
            forbidden.append(path.relative_to(package_root).as_posix())

    assert forbidden == []


def test_application_result_is_immutable_and_has_expected_boundary_type() -> None:
    result = SpecificationAssessmentService().assess(())

    assert type(result) is SpecificationAssessmentResult
    assert [item.name for item in fields(SpecificationAssessmentResult)] == [
        "records",
        "specification_assessment",
        "projection",
        "cross_results",
        "materiality",
    ]
    assert not hasattr(result, "overall_score")
