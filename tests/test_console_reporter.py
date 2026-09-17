"""MVP-10B ConsoleReporter presentation tests (Section 19, APPROVED_FOR_MVP_V0.1).

ConsoleReporter is exercised only against manually constructed Requirement,
RequirementQualityProfile, and SpecificationQualityProfile instances; no
extractor, calculator, assessor, aggregator, reader, or CLI involved.
"""

from fractions import Fraction

from requirements_quality_assessment.domain import (
    CharacteristicAssessment, CharacteristicAssessmentState, CharacteristicId,
    Finding, FindingKind, Requirement, RequirementQualityProfile,
    SpecificationCharacteristicAggregate, SpecificationQualityProfile,
)
from requirements_quality_assessment.domain.specification_profile import (
    AGGREGATION_RULE_ID,
)
from requirements_quality_assessment.reporter import ConsoleReporter

_RULE_ID = {
    CharacteristicId.COMPLETENESS: "CALC-C-MVP-001",
    CharacteristicId.VERIFIABILITY: "CALC-V-MVP-001",
    CharacteristicId.UNAMBIGUITY: "CALC-U-MVP-001",
}


def _requirement(req_id="R001", source_line=1, text="The system shall do X."):
    return Requirement(req_id, source_line, text)


def _finding(*, finding_id="F1", requirement_id="R001",
             characteristic_id=CharacteristicId.UNAMBIGUITY,
             kind=FindingKind.SIGNAL, code="VAGUE_TERM_SIGNAL",
             rule_id="FIND-U-VAGUE-001", criterion_id=None,
             evidence_refs=("E001",), explanation="Potential ambiguity indicator."):
    return Finding(finding_id, requirement_id, characteristic_id, kind, code,
                    rule_id, criterion_id, evidence_refs, explanation)


def _computed(characteristic_id, value, findings=(), explanation=None):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.COMPUTED,
        value=value,
        assessment_rule_id=_RULE_ID[characteristic_id],
        findings=findings,
        explanation=explanation or f"{characteristic_id.value} computed",
    )


def _unknown(characteristic_id, explanation="withheld"):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.UNKNOWN,
        value=None,
        assessment_rule_id=None,
        findings=(),
        explanation=explanation,
    )


def _not_applicable(characteristic_id, explanation="not applicable"):
    return CharacteristicAssessment(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.NOT_APPLICABLE,
        value=None,
        assessment_rule_id=None,
        findings=(),
        explanation=explanation,
    )


def _profile(completeness=None, verifiability=None, unambiguity=None):
    return RequirementQualityProfile(
        completeness=completeness or _computed(CharacteristicId.COMPLETENESS, Fraction(1, 1)),
        verifiability=verifiability or _computed(CharacteristicId.VERIFIABILITY, Fraction(1, 1)),
        unambiguity=unambiguity or _computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 1)),
    )


def _aggregate(characteristic_id, state=CharacteristicAssessmentState.COMPUTED,
                value=Fraction(1, 1), computed_count=1, unknown_count=0,
                not_applicable_count=0, total_count=1):
    return SpecificationCharacteristicAggregate(
        characteristic_id=characteristic_id,
        state=state,
        value=value,
        computed_count=computed_count,
        unknown_count=unknown_count,
        not_applicable_count=not_applicable_count,
        total_count=total_count,
        aggregation_rule_id=AGGREGATION_RULE_ID,
    )


def _not_applicable_aggregate(characteristic_id):
    return SpecificationCharacteristicAggregate(
        characteristic_id=characteristic_id,
        state=CharacteristicAssessmentState.NOT_APPLICABLE,
        value=None, computed_count=0, unknown_count=0, not_applicable_count=0,
        total_count=0, aggregation_rule_id=AGGREGATION_RULE_ID,
    )


def _default_specification_profile():
    return SpecificationQualityProfile(
        completeness=_aggregate(CharacteristicId.COMPLETENESS),
        verifiability=_aggregate(CharacteristicId.VERIFIABILITY),
        unambiguity=_aggregate(CharacteristicId.UNAMBIGUITY),
    )


def _empty_specification_profile():
    return SpecificationQualityProfile(
        completeness=_not_applicable_aggregate(CharacteristicId.COMPLETENESS),
        verifiability=_not_applicable_aggregate(CharacteristicId.VERIFIABILITY),
        unambiguity=_not_applicable_aggregate(CharacteristicId.UNAMBIGUITY),
    )


# -- T1: fully computed requirement ----------------------------------------------

def test_fully_computed_requirement_renders_id_text_order_and_no_scalar_score():
    requirement = _requirement(text="The system shall log in a user.")
    profile = _profile()

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    assert "Requirement R001" in output
    assert "Text: The system shall log in a user." in output
    assert output.index("Completeness:") < output.index("Verifiability:") < output.index("Unambiguity:")
    assert output.count("value: 1") == 6  # three per-requirement + three aggregate
    assert "assessment_rule_id: CALC-C-MVP-001" in output
    assert "assessment_rule_id: CALC-V-MVP-001" in output
    assert "assessment_rule_id: CALC-U-MVP-001" in output
    for forbidden in ("score", "overall_score", "file_quality_score"):
        assert forbidden not in output.lower()


# -- T2: exact non-integer Fractions -----------------------------------------------

def test_exact_non_integer_fractions_render_without_decimal_or_percent():
    requirement = _requirement()
    profile = _profile(
        completeness=_computed(CharacteristicId.COMPLETENESS, Fraction(1, 3)),
        verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(1, 2)),
        unambiguity=_computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 2)),
    )
    specification_profile = SpecificationQualityProfile(
        completeness=_aggregate(CharacteristicId.COMPLETENESS, value=Fraction(11, 18)),
        verifiability=_aggregate(CharacteristicId.VERIFIABILITY),
        unambiguity=_aggregate(CharacteristicId.UNAMBIGUITY),
    )

    output = ConsoleReporter().render([(requirement, profile)], specification_profile)

    assert "value: 1/3" in output
    assert "value: 1/2" in output
    assert "value: 11/18" in output
    assert "%" not in output
    assert "0.3" not in output
    assert "0.33" not in output
    assert "0.5" not in output


# -- T3: computed zero vs UNKNOWN --------------------------------------------------

def test_computed_zero_and_unknown_render_distinctly():
    requirement = _requirement()
    profile = _profile(
        verifiability=_computed(CharacteristicId.VERIFIABILITY, Fraction(0, 1)),
        unambiguity=_unknown(CharacteristicId.UNAMBIGUITY),
    )

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    assert "value: 0" in output
    assert "value: UNKNOWN" in output
    assert "state: UNKNOWN" in output
    unambiguity_block = output[output.index("Unambiguity:"):]
    assert "value: 0" not in unambiguity_block


# -- T4: NOT_APPLICABLE -------------------------------------------------------------

def test_not_applicable_renders_literal_token_not_na_or_zero():
    requirement = _requirement()
    profile = _profile(completeness=_not_applicable(CharacteristicId.COMPLETENESS))

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    assert "value: NOT_APPLICABLE" in output
    assert "state: NOT_APPLICABLE" in output
    assert "N/A" not in output
    completeness_block = output[output.index("Completeness:"):output.index("Verifiability:")]
    assert "value: 0" not in completeness_block
    assert "value: None" not in completeness_block


# -- T5: vague-term SIGNAL -----------------------------------------------------------

def test_vague_term_signal_finding_renders_without_defect_language():
    finding = _finding()
    profile = _profile(
        unambiguity=_computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 2), findings=(finding,)),
    )
    requirement = _requirement()

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    assert "kind: SIGNAL" in output
    assert "code: VAGUE_TERM_SIGNAL" in output
    assert "rule_id: FIND-U-VAGUE-001" in output
    assert "evidence_refs: E001" in output
    assert "Potential ambiguity indicator." in output
    assert "QUALITY_PROBLEM" not in output
    assert "defect" not in output.lower()
    assert "confirmed problem" not in output.lower()


# -- T6: criterion_id conditional display --------------------------------------------

def test_criterion_id_line_appears_only_when_present():
    # Both are SIGNAL findings (FIND-U-VAGUE-001 shape); the domain Finding
    # contract permits a non-null criterion_id on any kind. This exercises only
    # the reporter's conditional formatting, not a newly approved production rule.
    with_criterion = _finding(finding_id="F1", criterion_id="CRIT-01")
    without_criterion = _finding(finding_id="F2")
    profile = _profile(
        unambiguity=_computed(
            CharacteristicId.UNAMBIGUITY, Fraction(1, 2),
            findings=(with_criterion, without_criterion),
        )
    )
    requirement = _requirement()

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    assert "criterion_id: CRIT-01" in output
    assert output.count("criterion_id:") == 1


# -- T7: no findings ------------------------------------------------------------------

def test_assessment_without_findings_renders_findings_none():
    requirement = _requirement()
    profile = _profile()

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    assert output.count("findings: none") == 3
    assert "findings:\n" not in output


# -- T8: partial-observability specification aggregate --------------------------------

def test_partial_observability_aggregate_shows_all_four_counts():
    aggregate = _aggregate(
        CharacteristicId.VERIFIABILITY, value=Fraction(2, 3),
        computed_count=2, unknown_count=1, not_applicable_count=0, total_count=3,
    )
    specification_profile = SpecificationQualityProfile(
        completeness=_aggregate(CharacteristicId.COMPLETENESS),
        verifiability=aggregate,
        unambiguity=_aggregate(CharacteristicId.UNAMBIGUITY),
    )

    output = ConsoleReporter().render([], specification_profile)

    verifiability_block = output[output.index("Verifiability:"):]
    assert "state: COMPUTED" in verifiability_block
    assert "value: 2/3" in verifiability_block
    assert "computed_count: 2" in verifiability_block
    assert "unknown_count: 1" in verifiability_block
    assert "not_applicable_count: 0" in verifiability_block
    assert "total_count: 3" in verifiability_block
    assert "aggregation_rule_id: AGG-MVP-001" in verifiability_block


# -- T9: empty specification -----------------------------------------------------------

def test_empty_specification_shows_zero_analyzed_and_not_applicable_aggregates():
    output = ConsoleReporter().render([], _empty_specification_profile())

    assert "Analyzed requirements: 0" in output
    assert output.count("state: NOT_APPLICABLE") == 3
    assert output.count("value: NOT_APPLICABLE") == 3
    assert output.count("computed_count: 0") == 3
    assert output.count("unknown_count: 0") == 3
    assert output.count("not_applicable_count: 0") == 3
    assert output.count("total_count: 0") == 3
    assert "Requirement " not in output
    for forbidden in ("EMPTY", "NO_DATA"):
        assert forbidden not in output


# -- T10: deterministic requirement order ------------------------------------------------

def test_requirement_order_is_preserved_exactly_as_supplied():
    r2 = _requirement(req_id="R002")
    r1 = _requirement(req_id="R001")
    r3 = _requirement(req_id="R003")
    profile = _profile()

    output = ConsoleReporter().render(
        [(r2, profile), (r1, profile), (r3, profile)], _default_specification_profile()
    )

    assert (
        output.index("Requirement R002")
        < output.index("Requirement R001")
        < output.index("Requirement R003")
    )


# -- T11: deterministic characteristic order ----------------------------------------------

def test_characteristic_order_is_fixed_in_both_sections():
    requirement = _requirement()
    profile = _profile()

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    summary_start = output.index("Specification summary")
    requirement_section = output[:summary_start]
    summary_section = output[summary_start:]

    for section in (requirement_section, summary_section):
        assert section.index("Completeness:") < section.index("Verifiability:") < section.index("Unambiguity:")


# -- T12: findings preserve existing order -------------------------------------------------

def test_multiple_findings_preserve_their_supplied_order():
    first = _finding(finding_id="F1", evidence_refs=("E001",), explanation="first finding")
    second = _finding(finding_id="F2", evidence_refs=("E002",), explanation="second finding")
    profile = _profile(
        unambiguity=_computed(CharacteristicId.UNAMBIGUITY, Fraction(1, 2), findings=(first, second)),
    )
    requirement = _requirement()

    output = ConsoleReporter().render([(requirement, profile)], _default_specification_profile())

    assert output.index("first finding") < output.index("second finding")
    assert output.index("E001") < output.index("E002")


# -- T13: iterable/generator input ------------------------------------------------------

def test_generator_input_is_materialized_once_and_produces_correct_count():
    requirements = [_requirement(req_id="R001"), _requirement(req_id="R002")]
    profile = _profile()
    pairs = ((requirement, profile) for requirement in requirements)

    output = ConsoleReporter().render(pairs, _default_specification_profile())

    assert "Analyzed requirements: 2" in output
    assert "Requirement R001" in output
    assert "Requirement R002" in output


# -- T14: deterministic repeated rendering -----------------------------------------------

def test_repeated_rendering_of_the_same_input_is_identical():
    requirement = _requirement()
    profile = _profile()
    specification_profile = _default_specification_profile()
    reporter = ConsoleReporter()

    first = reporter.render([(requirement, profile)], specification_profile)
    second = reporter.render([(requirement, profile)], specification_profile)

    assert first == second


# -- T15: comprehensive golden-output test -----------------------------------------------

def test_golden_output_locks_down_the_canonical_mvp_v0_1_text_format():
    requirement = Requirement("R001", 1, "The system shall authenticate a very fast user.")
    finding = Finding(
        "F-U-1", "R001", CharacteristicId.UNAMBIGUITY, FindingKind.SIGNAL,
        "VAGUE_TERM_SIGNAL", "FIND-U-VAGUE-001", None, ("E001",),
        "Matched vague term 'fast'; potential ambiguity indicator, not a confirmed defect.",
    )
    profile = RequirementQualityProfile(
        completeness=CharacteristicAssessment(
            CharacteristicId.COMPLETENESS, CharacteristicAssessmentState.COMPUTED,
            Fraction(1, 3), "CALC-C-MVP-001", (),
            "Two of three required completeness elements were detected.",
        ),
        verifiability=CharacteristicAssessment(
            CharacteristicId.VERIFIABILITY, CharacteristicAssessmentState.COMPUTED,
            Fraction(0, 1), "CALC-V-MVP-001", (),
            "No accepted verification evidence was found.",
        ),
        unambiguity=CharacteristicAssessment(
            CharacteristicId.UNAMBIGUITY, CharacteristicAssessmentState.COMPUTED,
            Fraction(1, 2), "CALC-U-MVP-001", (finding,),
            "One accepted vague-term signal was found; the result is capped at 1/2.",
        ),
    )
    specification_profile = SpecificationQualityProfile(
        completeness=SpecificationCharacteristicAggregate(
            CharacteristicId.COMPLETENESS, CharacteristicAssessmentState.COMPUTED,
            Fraction(1, 3), 1, 0, 0, 1, AGGREGATION_RULE_ID,
        ),
        verifiability=SpecificationCharacteristicAggregate(
            CharacteristicId.VERIFIABILITY, CharacteristicAssessmentState.COMPUTED,
            Fraction(0, 1), 1, 0, 0, 1, AGGREGATION_RULE_ID,
        ),
        unambiguity=SpecificationCharacteristicAggregate(
            CharacteristicId.UNAMBIGUITY, CharacteristicAssessmentState.UNKNOWN,
            None, 0, 1, 0, 1, AGGREGATION_RULE_ID,
        ),
    )

    output = ConsoleReporter().render([(requirement, profile)], specification_profile)

    expected = "\n".join([
        "Requirement R001",
        "Text: The system shall authenticate a very fast user.",
        "",
        "Completeness:",
        "  state: COMPUTED",
        "  value: 1/3",
        "  assessment_rule_id: CALC-C-MVP-001",
        "  findings: none",
        "  explanation: Two of three required completeness elements were detected.",
        "",
        "Verifiability:",
        "  state: COMPUTED",
        "  value: 0",
        "  assessment_rule_id: CALC-V-MVP-001",
        "  findings: none",
        "  explanation: No accepted verification evidence was found.",
        "",
        "Unambiguity:",
        "  state: COMPUTED",
        "  value: 1/2",
        "  assessment_rule_id: CALC-U-MVP-001",
        "  findings:",
        "    - kind: SIGNAL",
        "      code: VAGUE_TERM_SIGNAL",
        "      rule_id: FIND-U-VAGUE-001",
        "      evidence_refs: E001",
        "      explanation: Matched vague term 'fast'; potential ambiguity indicator, not a confirmed defect.",
        "  explanation: One accepted vague-term signal was found; the result is capped at 1/2.",
        "",
        "Specification summary",
        "Analyzed requirements: 1",
        "",
        "Completeness:",
        "  state: COMPUTED",
        "  value: 1/3",
        "  computed_count: 1",
        "  unknown_count: 0",
        "  not_applicable_count: 0",
        "  total_count: 1",
        "  aggregation_rule_id: AGG-MVP-001",
        "",
        "Verifiability:",
        "  state: COMPUTED",
        "  value: 0",
        "  computed_count: 1",
        "  unknown_count: 0",
        "  not_applicable_count: 0",
        "  total_count: 1",
        "  aggregation_rule_id: AGG-MVP-001",
        "",
        "Unambiguity:",
        "  state: UNKNOWN",
        "  value: UNKNOWN",
        "  computed_count: 0",
        "  unknown_count: 1",
        "  not_applicable_count: 0",
        "  total_count: 1",
        "  aggregation_rule_id: AGG-MVP-001",
    ])

    assert output == expected
