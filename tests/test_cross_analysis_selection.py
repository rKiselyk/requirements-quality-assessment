from dataclasses import FrozenInstanceError, fields, replace

import pytest

from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.cross_analysis import (
    CrossCandidateOrderKey,
    CrossObservationPairCandidate,
    CrossRequirementProjector,
    ExhaustivePairSelector,
)
from requirements_quality_assessment.domain import (
    QuantitativeComponentName,
    Requirement,
    UnitLabel,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor


def _record(
    requirement_id: str,
    source_line: int,
    observation_count: int,
    *,
    text: str = "Система працює не більше 2 с",
):
    extraction = BaselineFeatureExtractor().extract(
        Requirement(requirement_id, source_line, text)
    )
    outcome = extraction.features.quantitative_constraints
    if observation_count:
        assert len(outcome.observations) == 1
        source = outcome.observations[0]
        observations = tuple(source for _ in range(observation_count))
    else:
        observations = ()
    object.__setattr__(outcome, "observations", observations)
    return RequirementQualityAssessor().assess_record(extraction)


def _projection(*observation_counts: int):
    records = tuple(
        _record(f"R{index + 1:03d}", index + 1, count)
        for index, count in enumerate(observation_counts)
    )
    return CrossRequirementProjector().project(records)


def _identity(candidate: CrossObservationPairCandidate) -> tuple[str, str, int, int]:
    return (
        candidate.earlier_requirement.requirement_id,
        candidate.later_requirement.requirement_id,
        candidate.left.observation_index,
        candidate.right.observation_index,
    )


@pytest.mark.parametrize(
    ("counts", "expected"),
    [
        ((), 0),
        ((3,), 0),
        ((0, 0, 0), 0),
        ((1, 1), 1),
        ((2, 3), 6),
        ((0, 1, 3, 2), 11),
    ],
    ids=[
        "empty-specification",
        "one-requirement",
        "multiple-zero-observation-requirements",
        "one-by-one",
        "two-by-three",
        "zero-one-many-mixture",
    ],
)
def test_exhaustive_selection_counts(counts, expected: int) -> None:
    projection = _projection(*counts)
    selector = ExhaustivePairSelector()

    candidates = selector.select(projection)

    assert len(candidates) == expected
    assert selector.candidate_count(projection) == expected


def test_multiple_requirement_pairs_follow_exact_deterministic_order() -> None:
    projection = _projection(2, 2, 1)

    candidates = ExhaustivePairSelector().select(projection)

    assert [_identity(candidate) for candidate in candidates] == [
        ("R001", "R002", 0, 0),
        ("R001", "R002", 0, 1),
        ("R001", "R002", 1, 0),
        ("R001", "R002", 1, 1),
        ("R001", "R003", 0, 0),
        ("R001", "R003", 1, 0),
        ("R002", "R003", 0, 0),
        ("R002", "R003", 1, 0),
    ]
    assert [candidate.order_key for candidate in candidates] == sorted(
        candidate.order_key for candidate in candidates
    )


def test_candidate_count_implements_exact_pair_product_formula() -> None:
    counts = (0, 4, 1, 3, 2)
    projection = _projection(*counts)
    oracle = sum(
        left_count * right_count
        for left_index, left_count in enumerate(counts)
        for right_count in counts[left_index + 1 :]
    )
    selector = ExhaustivePairSelector()

    assert selector.candidate_count(projection) == oracle
    assert len(selector.select(projection)) == oracle == 35


def test_no_self_reverse_or_within_requirement_pairs_are_emitted() -> None:
    candidates = ExhaustivePairSelector().select(_projection(3, 2, 2))
    owner_pairs = [
        (candidate.left.requirement_id, candidate.right.requirement_id)
        for candidate in candidates
    ]

    assert all(left != right for left, right in owner_pairs)
    assert all(
        candidate.earlier_requirement.source_order
        < candidate.later_requirement.source_order
        for candidate in candidates
    )
    assert not ({(right, left) for left, right in owner_pairs} & set(owner_pairs))
    assert len({candidate.order_key for candidate in candidates}) == len(candidates)


def test_repeated_selection_is_stable_and_candidates_are_immutable() -> None:
    projection = _projection(2, 3, 1)
    selector = ExhaustivePairSelector()

    first = selector.select(projection)
    second = selector.select(projection)

    assert first == second
    assert first is not second
    with pytest.raises(FrozenInstanceError):
        first[0].left = first[0].right


def test_mismatched_metric_context_and_unit_observations_are_retained() -> None:
    earlier = _record(
        "R001",
        1,
        1,
        text="Час відгуку ≤ 2 с при 500 одночасних користувачах",
    )
    later = _record(
        "R002",
        2,
        1,
        text="Система працює не більше 3 хв",
    )
    projection = CrossRequirementProjector().project((earlier, later))
    left = projection.requirements[0].observations[0]
    right = projection.requirements[1].observations[0]

    candidates = ExhaustivePairSelector().select(projection)

    assert left.metric_evidence_refs and not right.metric_evidence_refs
    assert left.context_evidence_refs and not right.context_evidence_refs
    assert (left.unit, right.unit) == (UnitLabel.SECOND, UnitLabel.MINUTE)
    assert len(candidates) == 1
    assert candidates[0].observation_refs == (left.ref, right.ref)


def test_observations_with_unresolved_components_are_retained() -> None:
    earlier = _record("R001", 1, 1)
    later = _record("R002", 2, 1)
    outcome = later.extraction_result.features.quantitative_constraints
    unresolved = replace(
        outcome.observations[0],
        unresolved_components=(
            QuantitativeComponentName.METRIC,
            QuantitativeComponentName.CONTEXT,
        ),
    )
    object.__setattr__(outcome, "observations", (unresolved,))
    projection = CrossRequirementProjector().project((earlier, later))

    candidates = ExhaustivePairSelector().select(projection)

    assert projection.requirements[1].observations[0].unresolved_components == (
        QuantitativeComponentName.METRIC,
        QuantitativeComponentName.CONTEXT,
    )
    assert len(candidates) == 1


def test_candidate_contains_identity_and_order_data_but_no_scientific_state() -> None:
    projection = _projection(1, 1)
    candidate = ExhaustivePairSelector().select(projection)[0]
    names = {item.name for item in fields(candidate)}

    assert candidate.snapshot_id == projection.snapshot_id
    assert candidate.participants == (
        projection.requirements[0].order_key,
        projection.requirements[1].order_key,
    )
    assert candidate.observation_refs == (
        projection.requirements[0].observations[0].ref,
        projection.requirements[1].observations[0].ref,
    )
    assert names == {
        "snapshot_id",
        "earlier_requirement",
        "later_requirement",
        "left",
        "right",
        "order_key",
    }
    assert not any(
        hasattr(candidate, name)
        for name in (
            "state",
            "disposition",
            "applicability",
            "comparison_key",
            "conflict",
            "materiality",
        )
    )


def test_candidate_rejects_reversed_or_misowned_participants() -> None:
    valid = ExhaustivePairSelector().select(_projection(1, 1))[0]

    with pytest.raises(ValueError, match="source order"):
        CrossObservationPairCandidate(
            snapshot_id=valid.snapshot_id,
            earlier_requirement=valid.later_requirement,
            later_requirement=valid.earlier_requirement,
            left=valid.right,
            right=valid.left,
        )
    with pytest.raises(ValueError, match="left observation"):
        CrossObservationPairCandidate(
            snapshot_id=valid.snapshot_id,
            earlier_requirement=valid.earlier_requirement,
            later_requirement=valid.later_requirement,
            left=valid.right,
            right=valid.right,
        )


def test_candidate_order_key_rejects_same_requirement_id_at_different_orders() -> None:
    valid = ExhaustivePairSelector().select(_projection(1, 1))[0]
    apparent_later = replace(
        valid.later_requirement,
        requirement_id=valid.earlier_requirement.requirement_id,
    )

    with pytest.raises(ValueError, match="distinct requirement IDs"):
        CrossCandidateOrderKey(
            earlier_requirement=valid.earlier_requirement,
            later_requirement=apparent_later,
            left_observation_index=0,
            right_observation_index=0,
        )


def test_candidate_rejects_same_requirement_observations_as_apparent_cross_pair() -> None:
    valid = ExhaustivePairSelector().select(_projection(1, 1))[0]
    requirement_id = valid.earlier_requirement.requirement_id
    apparent_later = replace(
        valid.later_requirement,
        requirement_id=requirement_id,
    )
    apparent_right = replace(valid.right, requirement_id=requirement_id)

    with pytest.raises(ValueError, match="distinct requirement IDs"):
        CrossObservationPairCandidate(
            snapshot_id=valid.snapshot_id,
            earlier_requirement=valid.earlier_requirement,
            later_requirement=apparent_later,
            left=valid.left,
            right=apparent_right,
        )


def test_selector_rejects_cross_snapshot_projection_corruption() -> None:
    projection = _projection(1, 1)
    foreign = _projection(1, 2)
    object.__setattr__(projection.resolver, "snapshot_id", foreign.snapshot_id)

    with pytest.raises(ValueError, match="identities"):
        ExhaustivePairSelector().select(projection)


def test_selector_rejects_snapshot_domain_corruption() -> None:
    projection = _projection(1, 1)
    observation_ref = projection.requirements[0].observations[0].ref
    object.__setattr__(observation_ref, "observation_index", 9)

    with pytest.raises(ValueError, match="observation|identity"):
        ExhaustivePairSelector().select(projection)


def test_selector_rejects_non_projection_input() -> None:
    with pytest.raises(TypeError, match="CrossRequirementProjection"):
        ExhaustivePairSelector().select(())
