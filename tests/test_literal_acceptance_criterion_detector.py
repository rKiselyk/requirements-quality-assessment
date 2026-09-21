"""Binding ACCEPT-UK-001 behavior from model-spec §7.14.16.4-.5."""

from dataclasses import dataclass, replace
from importlib.metadata import PackageNotFoundError, version

import pytest

from requirements_quality_assessment.detectors import (
    AcceptanceCriterionDetector,
    LiteralAcceptanceCriterionDetector,
)
from requirements_quality_assessment.detectors.acceptance_criterion import (
    LITERAL_DEPENDENCY_BLOCKED_CODE,
    LITERAL_RULE_ID,
    LITERAL_UNRESOLVED_CANDIDATE_CODE,
)
from requirements_quality_assessment.domain import (
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DetectionStatus,
    DiagnosticSpan,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    ParserDiagnostic,
    ParserDiagnosticCode,
    ParserOutcome,
    Requirement,
)
from requirements_quality_assessment.extractor import BaselineFeatureExtractor
from requirements_quality_assessment.parsing import SpaCyRequirementParser


P07 = (
    "Якщо сервіс недоступний, система повинна показати повідомлення "
    "«Сервіс недоступний»."
)
P08 = (
    "Якщо сервіс не відповідає, система повинна показати зрозуміле "
    "повідомлення."
)
P19 = "Якщо сервіс не відповідає, система повинна показати повідомлення «»."
P20 = (
    "Якщо сервіс не відповідає, система повинна показати повідомлення "
    "«Помилка «E1»»."
)
P21 = (
    "Якщо сервіс не відповідає, система повинна не більше ніж за 2 с "
    "показати повідомлення «Сервіс недоступний»."
)
P22 = "Система повинна показати повідомлення «Сервіс недоступний»."


@dataclass
class FakeDetector:
    result: tuple[FeatureDetectionOutcome, tuple[Evidence, ...]]

    def detect(self, requirement: Requirement):
        return self.result


@dataclass
class StubParser:
    outcome: ParserOutcome

    def parse(self, requirement: Requirement) -> ParserOutcome:
        return self.outcome


@pytest.fixture(scope="module")
def pinned_parser():
    required = {"spacy": "3.8.16", "uk-core-news-sm": "3.8.0"}
    installed = {}
    for distribution, expected in required.items():
        try:
            installed[distribution] = version(distribution)
        except PackageNotFoundError:
            pytest.fail(
                f"Mandatory pinned backend unavailable: "
                f"{distribution}=={expected}",
                pytrace=False,
            )
    assert installed == required, (
        f"Mandatory pinned backend mismatch: required {required}, "
        f"installed {installed}"
    )
    return SpaCyRequirementParser()


def parse(pinned_parser, requirement):
    outcome = pinned_parser.parse(requirement)
    assert not outcome.diagnostics, (
        f"Mandatory pinned backend failed for {requirement.text!r}: "
        f"{outcome.diagnostics}"
    )
    assert outcome.parsed_requirement is not None
    parsed = outcome.parsed_requirement
    assert (parsed.parser.library_version, parsed.parser.model_version) == (
        "3.8.16",
        "3.8.0",
    )
    return outcome


def extract(text):
    return BaselineFeatureExtractor().extract(Requirement("R072", 12, text))


def acceptance(result):
    evidence = tuple(
        source
        for source in result.evidence
        if source.feature_id is FeatureId.ACCEPTANCE_CRITERION
    )
    return result.features.acceptance_criteria, evidence


def family_result(requirement, feature_id, rule_id, spans, diagnostics=()):
    evidence = tuple(
        Evidence(
            evidence_id=f"{rule_id}:E{ordinal:03d}",
            requirement_id=requirement.id,
            feature_id=feature_id,
            text=requirement.text[start:end],
            start_offset=start,
            end_offset=end,
            rule_id=rule_id,
        )
        for ordinal, (start, end) in enumerate(spans, 1)
    )
    observations = tuple(
        FeatureObservation(feature_id, (source.evidence_id,))
        for source in evidence
    )
    return (
        FeatureDetectionOutcome(
            feature_id=feature_id,
            observations=observations,
            processing_status=(
                DetectionProcessingStatus.INCOMPLETE
                if diagnostics
                else DetectionProcessingStatus.COMPLETE
            ),
            diagnostics=diagnostics,
        ),
        evidence,
    )


def direct_literal(
    requirement,
    parser_outcome,
    *,
    condition_spans=((0, 23),),
    result_spans=((25, 83),),
    condition_rule="COND-UK-001",
    result_rule="RESULT-UK-001",
    condition_diagnostics=(),
    result_diagnostics=(),
):
    condition = family_result(
        requirement,
        FeatureId.CONDITION_CONTEXT,
        condition_rule,
        condition_spans,
        condition_diagnostics,
    )
    expected = family_result(
        requirement,
        FeatureId.EXPECTED_RESULT,
        result_rule,
        result_spans,
        result_diagnostics,
    )
    return LiteralAcceptanceCriterionDetector(
        parser=StubParser(parser_outcome),
        condition_detector=FakeDetector(condition),
        expected_result_detector=FakeDetector(expected),
    ).detect(requirement)


def test_p07_exact_evidence_observation_and_oracle(pinned_parser):
    requirement = Requirement("R072", 12, P07)
    parse(pinned_parser, requirement)
    outcome, evidence = acceptance(extract(P07))
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [
        (source.evidence_id, source.start_offset, source.end_offset, source.text)
        for source in evidence
    ] == [
        (f"{LITERAL_RULE_ID}:E001", 0, 23, "Якщо сервіс недоступний"),
        (
            f"{LITERAL_RULE_ID}:E002",
            25,
            83,
            "система повинна показати повідомлення «Сервіс недоступний»",
        ),
    ]
    assert outcome.observations[0].evidence_refs == (
        f"{LITERAL_RULE_ID}:E001",
        f"{LITERAL_RULE_ID}:E002",
    )
    assert P07[63:83] == "«Сервіс недоступний»"
    assert P07[64:82] == "Сервіс недоступний"


@pytest.mark.parametrize("text", [P08, P19, P22])
def test_binding_completed_negatives(text):
    outcome, evidence = acceptance(extract(text))
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert outcome.observations == outcome.diagnostics == evidence == ()


def test_p20_nested_guillemets_are_unresolved():
    outcome, evidence = acceptance(extract(P20))
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert evidence == outcome.observations == ()
    diagnostic, = outcome.diagnostics
    assert (diagnostic.rule_id, diagnostic.code) == (
        LITERAL_RULE_ID,
        LITERAL_UNRESOLVED_CANDIDATE_CODE,
    )
    assert diagnostic.candidate_span == DiagnosticSpan(P20[27:79], 27, 79)


def test_p21_merges_quantitative_and_literal_justifications(pinned_parser):
    requirement = Requirement("R072", 12, P21)
    parsed = parse(pinned_parser, requirement).parsed_requirement
    tokens = {token.text: token for token in parsed.tokens}
    assert tokens["показати"].dependency_relation == "xcomp"
    assert tokens["показати"].head_token_id == tokens["повинна"].token_id
    assert tokens["повідомлення"].dependency_relation == "obj"
    assert tokens["повідомлення"].head_token_id == tokens["показати"].token_id

    result = extract(P21)
    outcome, evidence = acceptance(result)
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert [
        (source.evidence_id, source.start_offset, source.end_offset)
        for source in evidence
    ] == [
        (f"{LITERAL_RULE_ID}:E001", 0, 25),
        ("ACCEPT-QUANT-001:E001", 27, 106),
        (f"{LITERAL_RULE_ID}:E002", 27, 106),
    ]
    assert [item.evidence_refs for item in outcome.observations] == [
        (
            f"{LITERAL_RULE_ID}:E001",
            "ACCEPT-QUANT-001:E001",
            f"{LITERAL_RULE_ID}:E002",
        )
    ]
    assert P21[86:106] == "«Сервіс недоступний»"
    assert P21[87:105] == "Сервіс недоступний"
    quantitative = result.features.quantitative_constraints
    assert quantitative.status is DetectionStatus.DETECTED
    assert any(source.rule_id == "QUANT-UK-001" for source in result.evidence)


def test_p07_pinned_graph_partition_and_exact_boundaries(pinned_parser):
    requirement = Requirement("R072", 12, P07)
    parsed = parse(pinned_parser, requirement).parsed_requirement
    tokens = {token.text: token for token in parsed.tokens}
    for source, relation, target in [
        ("система", "nsubj", "повинна"),
        ("показати", "xcomp", "повинна"),
        ("повідомлення", "obj", "показати"),
    ]:
        assert tokens[source].dependency_relation == relation
        assert tokens[source].head_token_id == tokens[target].token_id
    assert P07[23:25] == ", "
    assert P07[63] == "«" and P07[82] == "»"


def test_unicode_whitespace_is_allowed_between_object_and_literal():
    text = P07.replace("повідомлення «", "повідомлення\u2003\t«")
    outcome, evidence = acceptance(extract(text))
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert evidence[-1].text == text[25:-1]


@pytest.mark.parametrize(
    ("word", "changes"),
    [
        ("повідомлення", {"dependency_relation": "obl"}),
        ("повідомлення", {"head_token_id": 5}),
        ("повідомлення", {"lemma": None}),
        ("показати", {"lemma": None}),
    ],
)
def test_changed_or_missing_object_annotations_are_unresolved(
    pinned_parser, word, changes
):
    requirement = Requirement("R072", 12, P07)
    parser_outcome = parse(pinned_parser, requirement)
    parsed = parser_outcome.parsed_requirement
    tokens = tuple(
        replace(token, **changes) if token.text == word else token
        for token in parsed.tokens
    )
    outcome, evidence = direct_literal(
        requirement,
        ParserOutcome(replace(parsed, tokens=tokens), ()),
    )
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert evidence == ()
    assert [item.code for item in outcome.diagnostics] == [
        LITERAL_UNRESOLVED_CANDIDATE_CODE
    ]


def test_changed_token_extent_is_not_repaired(pinned_parser):
    requirement = Requirement("R072", 12, P07)
    parser_outcome = parse(pinned_parser, requirement)
    parsed = parser_outcome.parsed_requirement
    tokens = tuple(
        replace(
            token,
            text=P07[51:62],
            start_offset=51,
            lemma="повідомлення",
        )
        if token.text == "повідомлення"
        else token
        for token in parsed.tokens
    )
    outcome, evidence = direct_literal(
        requirement,
        ParserOutcome(replace(parsed, tokens=tokens), ()),
    )
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert evidence == ()


def test_degraded_parser_annotation_is_unresolved_not_absent(pinned_parser):
    requirement = Requirement("R072", 12, P07)
    parsed = parse(pinned_parser, requirement).parsed_requirement
    degraded = ParserOutcome(
        parsed,
        (
            ParserDiagnostic(
                ParserDiagnosticCode.ANNOTATION_INCOMPLETE,
                "fixture annotation missing",
            ),
        ),
    )
    outcome, evidence = direct_literal(requirement, degraded)
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert evidence == ()
    assert outcome.diagnostics[0].code == LITERAL_UNRESOLVED_CANDIDATE_CODE


@pytest.mark.parametrize("blocked_family", ["condition", "result"])
def test_incomplete_condition_or_result_dependency_is_blocked(
    pinned_parser, blocked_family
):
    requirement = Requirement("R072", 12, P07)
    parser_outcome = parse(pinned_parser, requirement)
    diagnostic = DetectionDiagnostic(
        "UPSTREAM_BLOCKED",
        "fixture dependency unavailable",
        "COND-UK-001" if blocked_family == "condition" else "RESULT-UK-001",
    )
    kwargs = {
        "condition_spans": () if blocked_family == "condition" else ((0, 23),),
        "result_spans": () if blocked_family == "result" else ((25, 83),),
        "condition_diagnostics": (diagnostic,)
        if blocked_family == "condition"
        else (),
        "result_diagnostics": (diagnostic,)
        if blocked_family == "result"
        else (),
    }
    outcome, evidence = direct_literal(requirement, parser_outcome, **kwargs)
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert evidence == outcome.observations == ()
    assert [item.code for item in outcome.diagnostics] == [
        LITERAL_DEPENDENCY_BLOCKED_CODE
    ]


def test_invalid_local_source_partition_is_unresolved(pinned_parser):
    requirement = Requirement("R072", 12, P07)
    outcome, evidence = direct_literal(
        requirement,
        parse(pinned_parser, requirement),
        result_spans=((26, 83),),
    )
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert evidence == ()
    assert outcome.diagnostics[0].candidate_span == DiagnosticSpan(P07[26:83], 26, 83)


@pytest.mark.parametrize(
    "text",
    [
        "Якщо сервіс не відповідає, система повинна показати повідомлення "
        "“Сервіс недоступний”.",
        "Якщо сервіс не відповідає, система повинна вивести повідомлення "
        "«Сервіс недоступний».",
        "Якщо сервіс не відповідає, система повинна показати напис "
        "«Сервіс недоступний».",
    ],
)
def test_other_quote_style_or_nonexact_verb_object_is_completed_negative(text):
    outcome, evidence = acceptance(extract(text))
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == outcome.diagnostics == ()


@pytest.mark.parametrize(
    "text",
    [
        "Якщо сервіс не відповідає, система повинна показати повідомлення "
        "«Перше» «Друге».",
        "Якщо сервіс не відповідає, система повинна показати повідомлення "
        "«Помилка» негайно.",
        "Якщо сервіс не відповідає, система повинна показати повідомлення "
        "«Помилка.",
    ],
)
def test_multiple_unclosed_or_trailing_literal_candidate_is_unresolved(text):
    outcome, evidence = acceptance(extract(text))
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert evidence == ()
    assert outcome.diagnostics[-1].code == LITERAL_UNRESOLVED_CANDIDATE_CODE


def test_postposed_condition_is_not_eligible():
    text = (
        "Система повинна показати повідомлення «Сервіс недоступний», "
        "якщо сервіс не відповідає."
    )
    outcome, evidence = acceptance(extract(text))
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == ()


def test_accepted_result_uk_002_is_not_eligible(pinned_parser):
    requirement = Requirement("R072", 12, P07)
    outcome, evidence = direct_literal(
        requirement,
        parse(pinned_parser, requirement),
        result_rule="RESULT-UK-002",
    )
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == ()


def test_multiple_independent_result_spans_are_not_merged():
    clause = P07[:-1]
    text = f"{clause}; {clause}."
    outcome, evidence = acceptance(extract(text))
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert len(outcome.observations) == 2
    assert [source.evidence_id for source in evidence] == [
        f"{LITERAL_RULE_ID}:E001",
        f"{LITERAL_RULE_ID}:E002",
        f"{LITERAL_RULE_ID}:E003",
        f"{LITERAL_RULE_ID}:E004",
    ]
    assert len({source.start_offset for source in evidence}) == 4


def test_accepted_plus_unresolved_candidate_is_mixed_detected():
    text = f"{P07[:-1]}; {P20}"
    outcome, evidence = acceptance(extract(text))
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert len(outcome.observations) == 1
    assert len(evidence) == 2
    assert [item.code for item in outcome.diagnostics] == [
        LITERAL_UNRESOLVED_CANDIDATE_CODE
    ]


def test_evidence_round_trip_same_family_refs_and_determinism():
    first = extract(P21)
    second = extract(P21)
    assert first == second
    outcome, evidence = acceptance(first)
    by_id = {source.evidence_id: source for source in evidence}
    assert len(by_id) == len(evidence)
    for source in evidence:
        assert P21[source.start_offset:source.end_offset] == source.text
        assert source.feature_id is FeatureId.ACCEPTANCE_CRITERION
    for observation in outcome.observations:
        assert all(
            by_id[reference].feature_id is FeatureId.ACCEPTANCE_CRITERION
            for reference in observation.evidence_refs
        )


def test_public_composed_detector_default_executes_p07():
    outcome, evidence = AcceptanceCriterionDetector().detect(
        Requirement("R072", 12, P07)
    )
    assert outcome.status is DetectionStatus.DETECTED
    assert [source.rule_id for source in evidence] == [
        LITERAL_RULE_ID,
        LITERAL_RULE_ID,
    ]
