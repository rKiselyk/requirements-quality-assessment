from dataclasses import replace
from fractions import Fraction

import pytest

from requirements_quality_assessment.corrective_action import RequirementLineageId
from requirements_quality_assessment.dynamic_evidence import Applicability, FullModelStatus
from requirements_quality_assessment.metrics import (
    FULL_MODEL_CONTRACT_REF,
    RuleRef,
    RuleVersionAuthority,
)
from requirements_quality_assessment.performance_efficiency import ProcessStage
from requirements_quality_assessment.product_quality import CalibrationStatus
from requirements_quality_assessment.reassessment import (
    AssessmentResultRef,
    ComparableResult,
    ComparisonKind,
    ComparisonReason,
    ComparisonRequest,
    ComparisonResultFamily,
    ComparisonSubject,
    ComparisonValueKind,
    SemanticCompatibilityDeclaration,
    CompatibilityComponentKind,
    CompatibilityDisposition,
    compare,
)

from test_versioned_reassessment import _application_bundle


RULE = RuleRef(
    "METRIC-RULE",
    "1",
    RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
)


def _lineages(parent):
    return tuple(item.lineage_id for item in parent.requirements)


def _subject(parent, family=ComparisonResultFamily.SPECIFICATION_METRIC, **changes):
    values = dict(
        result_family=family,
        metric_or_characteristic_id="SPEC_QB_CONSISTENCY",
        stable_subject_identity=(parent.artifact_ref.artifact_id, "SPEC_QB_CONSISTENCY"),
        ordered_lineage_population=_lineages(parent),
        scope_identity=("SPECIFICATION",),
        evidence_context=(),
    )
    values.update(changes)
    return ComparisonSubject(**values)


def _comparable(
    artifact_ref,
    subject,
    *,
    value=Fraction(0, 1),
    status=FullModelStatus.AVAILABLE,
    applicability=Applicability.APPLICABLE,
    value_kind=ComparisonValueKind.EXACT_FRACTION,
    categorical_state=None,
    rules=(RULE,),
    parameters=(),
    calibration=None,
):
    return ComparableResult(
        AssessmentResultRef("TEST-RESULT", (artifact_ref, subject), artifact_ref),
        subject,
        value_kind,
        status,
        applicability,
        value if status is FullModelStatus.AVAILABLE and value_kind is ComparisonValueKind.EXACT_FRACTION else None,
        categorical_state,
        "EXACT_FRACTION" if value_kind is ComparisonValueKind.EXACT_FRACTION else None,
        ProcessStage.REFERENCE_VERIFICATION,
        rules,
        (),
        parameters,
        FULL_MODEL_CONTRACT_REF,
        calibration,
    )


@pytest.mark.parametrize(
    ("before_value", "after_value", "expected"),
    [
        (Fraction(1, 3), Fraction(1, 3), ComparisonKind.UNCHANGED),
        (Fraction(0, 1), Fraction(1, 1), ComparisonKind.INCREASED),
        (Fraction(2, 3), Fraction(1, 3), ComparisonKind.DECREASED),
    ],
)
def test_exact_compatible_fraction_comparisons(before_value, after_value, expected):
    _, parent, _, application = _application_bundle()
    subject = _subject(parent)
    result = compare(
        ComparisonRequest(
            "COMPARE-REF",
            "1",
            _comparable(parent.artifact_ref, subject, value=before_value),
            _comparable(application.child_artifact_ref, subject, value=after_value),
            application.transition,
        )
    )

    assert result.status is FullModelStatus.AVAILABLE
    assert result.comparison_kind is expected
    assert isinstance(result.before_state_and_value.exact_value, Fraction)
    assert isinstance(result.after_state_and_value.exact_value, Fraction)
    assert "improved" not in result.explanation.lower()
    assert "worsened" not in result.explanation.lower()


def test_categorical_problem_and_risk_changes_have_no_numeric_order() -> None:
    _, parent, _, application = _application_bundle()
    risk_subject = _subject(
        parent,
        family=ComparisonResultFamily.BOUNDED_RISK,
        metric_or_characteristic_id="PERFORMANCE_EFFICIENCY",
        stable_subject_identity=(*_lineages(parent), "QB-KEY", "PERFORMANCE_EFFICIENCY"),
    )
    before = _comparable(
        parent.artifact_ref,
        risk_subject,
        value_kind=ComparisonValueKind.CATEGORICAL_STATE,
        categorical_state="RISK_IDENTIFIED",
        calibration=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
    )
    after = _comparable(
        application.child_artifact_ref,
        risk_subject,
        status=FullModelStatus.NOT_APPLICABLE,
        applicability=Applicability.NOT_APPLICABLE,
        value_kind=ComparisonValueKind.CATEGORICAL_STATE,
        categorical_state=None,
        calibration=CalibrationStatus.PROVISIONAL_NOT_CALIBRATED,
    )

    result = compare(
        ComparisonRequest("RISK-COMPARE", "1", before, after, application.transition)
    )

    assert result.comparison_kind is ComparisonKind.STATE_CHANGED
    assert result.reason_codes == (ComparisonReason.STRUCTURED_STATE_CHANGED,)
    assert result.before_state_and_value.exact_value is None
    assert result.after_state_and_value.exact_value is None
    assert result.calibration_status_or_none is CalibrationStatus.PROVISIONAL_NOT_CALIBRATED


def test_semantic_rule_mismatch_is_available_not_comparable() -> None:
    _, parent, _, application = _application_bundle()
    subject = _subject(parent)
    changed_rule = RuleRef(
        "METRIC-RULE",
        "2",
        RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
    )
    result = compare(
        ComparisonRequest(
            "RULE-MISMATCH",
            "1",
            _comparable(parent.artifact_ref, subject),
            _comparable(application.child_artifact_ref, subject, rules=(changed_rule,)),
            application.transition,
        )
    )

    assert result.status is FullModelStatus.AVAILABLE
    assert result.comparison_kind is ComparisonKind.NOT_COMPARABLE
    assert ComparisonReason.RULE_SEMANTICS_INCOMPATIBLE in result.reason_codes


def test_scoped_compatibility_declaration_allows_changed_version() -> None:
    _, parent, _, application = _application_bundle()
    subject = _subject(parent)
    changed_rule = RuleRef(
        "METRIC-RULE",
        "2",
        RuleVersionAuthority.EXPLICIT_CONTRACT_VERSION,
    )
    declaration = SemanticCompatibilityDeclaration(
        "DECL-1",
        CompatibilityComponentKind.RULE,
        RULE,
        changed_rule,
        subject,
        CompatibilityDisposition.COMPATIBLE_FOR_COMPARISON,
        "Approved scope-preserving comparison compatibility",
        FULL_MODEL_CONTRACT_REF,
        (),
    )
    result = compare(
        ComparisonRequest(
            "RULE-COMPATIBLE",
            "1",
            _comparable(parent.artifact_ref, subject, value=Fraction(1, 3)),
            _comparable(
                application.child_artifact_ref,
                subject,
                value=Fraction(2, 3),
                rules=(changed_rule,),
            ),
            application.transition,
            (declaration,),
        )
    )

    assert result.comparison_kind is ComparisonKind.INCREASED
    assert result.compatibility_declaration_refs == ("DECL-1",)


def test_parameter_change_without_declaration_is_not_comparable() -> None:
    _, parent, _, application = _application_bundle()
    subject = _subject(parent)
    result = compare(
        ComparisonRequest(
            "PARAM-MISMATCH",
            "1",
            _comparable(parent.artifact_ref, subject, parameters=(("PARAM", "1"),)),
            _comparable(
                application.child_artifact_ref,
                subject,
                parameters=(("PARAM", "2"),),
            ),
            application.transition,
        )
    )

    assert result.comparison_kind is ComparisonKind.NOT_COMPARABLE
    assert ComparisonReason.PARAMETER_SEMANTICS_INCOMPATIBLE in result.reason_codes


def test_changed_context_and_population_are_not_comparable() -> None:
    _, parent, _, application = _application_bundle()
    before_subject = _subject(parent, evidence_context=("collection", "1"))
    after_subject = _subject(
        parent,
        ordered_lineage_population=(_lineages(parent)[0],),
        evidence_context=("collection", "2"),
    )
    result = compare(
        ComparisonRequest(
            "CONTEXT-MISMATCH",
            "1",
            _comparable(parent.artifact_ref, before_subject),
            _comparable(application.child_artifact_ref, after_subject),
            application.transition,
        )
    )

    assert result.comparison_kind is ComparisonKind.NOT_COMPARABLE
    assert ComparisonReason.SCOPE_OR_POPULATION_MISMATCH in result.reason_codes
    assert ComparisonReason.EVIDENCE_CONTEXT_MISMATCH in result.reason_codes


def test_missing_result_and_missing_identity_preserve_canonical_states() -> None:
    _, parent, _, application = _application_bundle()
    subject = _subject(parent)
    available = _comparable(parent.artifact_ref, subject)

    missing_result = compare(
        ComparisonRequest("MISSING", "1", available, None, application.transition)
    )
    assert missing_result.status is FullModelStatus.UNAVAILABLE
    assert missing_result.comparison_kind is None

    missing_identity = compare(
        ComparisonRequest(
            "UNRESOLVED",
            "1",
            replace(available, subject=None),
            _comparable(application.child_artifact_ref, subject),
            application.transition,
        )
    )
    assert missing_identity.status is FullModelStatus.UNRESOLVED
    assert missing_identity.comparison_kind is None


def test_comparison_emits_change_only_and_no_forbidden_interpretation() -> None:
    _, parent, _, application = _application_bundle()
    subject = _subject(parent)
    result = compare(
        ComparisonRequest(
            "WORDS",
            "1",
            _comparable(parent.artifact_ref, subject, value=Fraction(0, 1)),
            _comparable(application.child_artifact_ref, subject, value=Fraction(1, 1)),
            application.transition,
        )
    )
    emitted = " ".join(
        (
            result.explanation,
            *(item.value for item in result.claims),
            *(item.value for item in result.non_claims),
        )
    ).lower()

    assert result.comparison_kind is ComparisonKind.INCREASED
    for forbidden in (
        "improved",
        "worsened",
        "risk reduced",
        "product quality improved",
        "action successful",
        "stakeholder intent correctness",
    ):
        assert forbidden not in emitted
