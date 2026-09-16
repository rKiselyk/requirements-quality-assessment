"""Approved VERIFY-UK-001 first-production behavior."""

from dataclasses import dataclass

import pytest

from requirements_quality_assessment.detectors import (
    VerificationMethodBaselineDetector,
)
from requirements_quality_assessment.detectors.verification_method import (
    PARSER_BLOCKED_CODE,
    RULE_ID,
    UNRESOLVED_CANDIDATE_CODE,
)
from requirements_quality_assessment.domain import (
    DetectionProcessingStatus,
    DetectionStatus,
    FeatureId,
    FeatureObservation,
    MorphFeature,
    ParsedRequirement,
    ParserDiagnostic,
    ParserDiagnosticCode,
    ParserMetadata,
    ParserOutcome,
    Requirement,
    SentenceAnnotation,
    TokenAnnotation,
)
from requirements_quality_assessment.parsing import SpaCyRequirementParser


@dataclass(frozen=True)
class _TokenSpec:
    surface: str
    lemma: str | None = None
    relation: str | None = None
    morphology: tuple[MorphFeature, ...] = ()
    head: int | None = None
    sentence_id: int = 0
    upos: str | None = "NOUN"


class _FakeParser:
    def __init__(self, outcome: ParserOutcome):
        self.outcome = outcome
        self.calls = 0

    def parse(self, requirement: Requirement) -> ParserOutcome:
        self.calls += 1
        return self.outcome


def _instrumental() -> tuple[MorphFeature, ...]:
    return (MorphFeature("Case", ("Ins",)),)


def _parsed(
    requirement: Requirement,
    specs: tuple[_TokenSpec, ...] = (),
    sentence_ranges: tuple[tuple[int, int], ...] | None = None,
) -> ParsedRequirement:
    if sentence_ranges is None:
        sentence_ranges = ((0, len(requirement.text)),)
    sentences = tuple(
        SentenceAnnotation(sentence_id, start, end)
        for sentence_id, (start, end) in enumerate(sentence_ranges)
    )
    cursors = {
        sentence_id: start
        for sentence_id, (start, _) in enumerate(sentence_ranges)
    }
    tokens = []
    for token_id, spec in enumerate(specs):
        start = requirement.text.index(spec.surface, cursors[spec.sentence_id])
        end = start + len(spec.surface)
        cursors[spec.sentence_id] = end
        tokens.append(
            TokenAnnotation(
                token_id=token_id,
                sentence_id=spec.sentence_id,
                text=spec.surface,
                start_offset=start,
                end_offset=end,
                lemma=spec.lemma,
                upos=spec.upos,
                morphology=spec.morphology,
                head_token_id=spec.head,
                dependency_relation=spec.relation,
            )
        )
    return ParsedRequirement(
        requirement_id=requirement.id,
        text=requirement.text,
        sentences=sentences,
        tokens=tuple(tokens),
        parser=ParserMetadata("fake", "1", "fake-uk", "1", "uk"),
    )


def _scan(
    text: str,
    specs: tuple[_TokenSpec, ...] = (),
    *,
    sentence_ranges: tuple[tuple[int, int], ...] | None = None,
):
    requirement = Requirement("R049", 49, text)
    parsed = _parsed(requirement, specs, sentence_ranges)
    parser = _FakeParser(ParserOutcome(parsed, ()))
    detector = VerificationMethodBaselineDetector(parser=parser)
    outcome, evidence = detector.detect(requirement)

    assert parser.calls == 1
    assert outcome.feature_id is FeatureId.VERIFICATION_METHOD
    assert all(isinstance(item, FeatureObservation) for item in outcome.observations)
    assert len(outcome.observations) == len(evidence)
    assert [item.start_offset for item in evidence] == sorted(
        item.start_offset for item in evidence
    )
    for observation, source in zip(outcome.observations, evidence):
        assert observation.evidence_refs == (source.evidence_id,)
        assert source.requirement_id == requirement.id
        assert source.feature_id is FeatureId.VERIFICATION_METHOD
        assert source.rule_id == RULE_ID
        assert text[source.start_offset : source.end_offset] == source.text
    for diagnostic in outcome.diagnostics:
        assert diagnostic.rule_id == RULE_ID
        if diagnostic.candidate_span is not None:
            span = diagnostic.candidate_span
            assert text[span.start_offset : span.end_offset] == span.text
    return requirement, parsed, outcome, evidence


def _a_specs(
    predicate: str = "перевіряється",
    *,
    relation: str = "obl",
    morphology: tuple[MorphFeature, ...] | None = None,
) -> tuple[_TokenSpec, ...]:
    if morphology is None:
        morphology = _instrumental()
    return (
        _TokenSpec(predicate, lemma="перевірятися", upos="VERB"),
        _TokenSpec(
            "тестом",
            lemma="тест",
            relation=relation,
            morphology=morphology,
            head=0,
        ),
    )


def test_default_parser_is_spacy_requirement_parser():
    detector = VerificationMethodBaselineDetector()
    assert isinstance(detector._parser, SpaCyRequirementParser)


def test_injected_parser_is_used_and_called_exactly_once():
    requirement = Requirement("R049", 1, "Немає методу.")
    parser = _FakeParser(ParserOutcome(_parsed(requirement), ()))
    detector = VerificationMethodBaselineDetector(parser=parser)

    outcome, evidence = detector.detect(requirement)

    assert detector._parser is parser
    assert parser.calls == 1
    assert outcome.status is DetectionStatus.NOT_DETECTED
    assert evidence == ()


@pytest.mark.parametrize("code", list(ParserDiagnosticCode))
def test_each_parser_blocking_code_maps_to_exact_blocked_outcome(code):
    requirement = Requirement("R049", 1, "Перевірка: тест.")
    parsed = None
    if code is ParserDiagnosticCode.ANNOTATION_INCOMPLETE:
        parsed = _parsed(requirement)
    parser = _FakeParser(
        ParserOutcome(parsed, (ParserDiagnostic(code, "provider detail"),))
    )

    outcome, evidence = VerificationMethodBaselineDetector(parser=parser).detect(
        requirement
    )

    assert parser.calls == 1
    assert outcome.observations == ()
    assert evidence == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert len(outcome.diagnostics) == 1
    assert outcome.diagnostics[0].code == PARSER_BLOCKED_CODE
    assert outcome.diagnostics[0].rule_id == RULE_ID
    assert outcome.diagnostics[0].candidate_span is None
    assert "provider detail" not in outcome.diagnostics[0].explanation


@pytest.mark.parametrize("predicate", ["перевіряється", "перевіряються"])
def test_construction_a_exact_predicates_and_evidence_boundary(predicate):
    text = f"Виконання {predicate} навантажувальним тестом."
    _, _, outcome, evidence = _scan(text, _a_specs(predicate))

    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [item.text for item in evidence] == ["навантажувальним тестом"]


@pytest.mark.parametrize("relation", ["obl", "obl:agent", "obl:means"])
def test_construction_a_accepts_exact_obl_and_obl_subtypes(relation):
    text = "Виконання перевіряється навантажувальним тестом."
    _, _, outcome, evidence = _scan(text, _a_specs(relation=relation))
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["навантажувальним тестом"]


@pytest.mark.parametrize(
    ("relation", "morphology"),
    [
        ("obj", _instrumental()),
        ("obl", (MorphFeature("Case", ("Acc",)),)),
        ("obl", ()),
    ],
)
def test_construction_a_wrong_role_is_unresolved_with_exact_member_span(
    relation, morphology
):
    text = "Виконання перевіряється навантажувальним тестом."
    _, _, outcome, evidence = _scan(
        text, _a_specs(relation=relation, morphology=morphology)
    )
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert [item.code for item in outcome.diagnostics] == [
        UNRESOLVED_CANDIDATE_CODE
    ]
    assert outcome.diagnostics[0].candidate_span.text == "навантажувальним тестом"


def test_construction_a_oblique_instrument_must_depend_on_governing_predicate():
    text = "Виконання перевіряється тестом."
    specs = (
        _TokenSpec("Виконання", lemma="виконання"),
        _TokenSpec("перевіряється", lemma="перевірятися", upos="VERB"),
        _TokenSpec(
            "тестом",
            lemma="тест",
            relation="obl",
            morphology=_instrumental(),
            head=0,
        ),
    )

    _, _, outcome, evidence = _scan(text, specs)

    assert evidence == ()
    assert outcome.observations == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.code for item in outcome.diagnostics] == [
        UNRESOLVED_CANDIDATE_CODE
    ]
    assert outcome.diagnostics[0].candidate_span.text == "тестом"


def test_construction_a_does_not_include_neighboring_behavior_in_evidence():
    text = "Виконання перевіряється система реєструє тестом."
    specs = (
        _TokenSpec("перевіряється", lemma="перевірятися", upos="VERB"),
        _TokenSpec("система", lemma="система", relation="nsubj", head=2),
        _TokenSpec("реєструє", lemma="реєструвати", upos="VERB"),
        _TokenSpec(
            "тестом",
            lemma="тест",
            relation="obl",
            morphology=_instrumental(),
            head=0,
        ),
    )

    _, _, outcome, evidence = _scan(text, specs)

    assert evidence == ()
    assert outcome.observations == ()
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.code for item in outcome.diagnostics] == [
        UNRESOLVED_CANDIDATE_CODE
    ]
    assert outcome.diagnostics[0].candidate_span.text == "система реєструє тестом"


@pytest.mark.parametrize(
    ("label", "delimiter", "method", "specs"),
    [
        (
            "Перевірка",
            ":",
            "навантажувальний тест",
            (_TokenSpec("тест", lemma="тест"),),
        ),
        (
            "Перевірка",
            "—",
            "негативні security tests",
            (),
        ),
        (
            "Метод перевірки",
            ":",
            "інспекція журналу",
            (_TokenSpec("інспекція", lemma="інспекція"),),
        ),
        (
            "Процедура перевірки",
            "-",
            "acceptance test",
            (),
        ),
    ],
)
def test_construction_b_exact_labels_delimiters_and_evidence_exclusion(
    label, delimiter, method, specs
):
    text = f"{label} {delimiter} {method}."
    _, _, outcome, evidence = _scan(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.diagnostics == ()
    assert [item.text for item in evidence] == [method]


def test_construction_b_supports_clean_hyphen_without_surrounding_space():
    text = "Процедура перевірки-security tests."
    _, _, outcome, evidence = _scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["security tests"]


def test_construction_c_exact_casefold_surface():
    text = "ВИЗНАЧЕНО негативні security tests."
    _, _, outcome, evidence = _scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["негативні security tests"]


def test_r3_full_source_exact_round_trip_and_calculated_extent():
    text = (
        "Дані передаються через TLS 1.3; доступ до API — за OAuth 2.0/OIDC; "
        "критичні операції журналюються; дані клієнтів логічно ізолюються між "
        "tenant-ами; визначено негативні security tests."
    )
    _, _, outcome, evidence = _scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [(item.text, item.start_offset, item.end_offset) for item in evidence] == [
        ("негативні security tests", 158, 182)
    ]
    assert text[158:182] == evidence[0].text


@pytest.mark.parametrize(
    "surface",
    ["визначений", "визначена", "визначені", "визначати", "встановлено", "описано", "задано", "передбачено"],
)
def test_construction_c_rejects_other_declaration_surfaces(surface):
    _, _, outcome, evidence = _scan(f"{surface} негативні security tests.")
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].candidate_span.text == "негативні security tests"


@pytest.mark.parametrize(
    ("text", "candidate"),
    [
        ("визначено посилання на acceptance test.", "acceptance test"),
        ("визначено документ для NFR test.", "NFR test"),
    ],
)
def test_construction_c_requires_immediate_attachment(text, candidate):
    _, _, outcome, evidence = _scan(text)
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.candidate_span.text for item in outcome.diagnostics] == [candidate]


@pytest.mark.parametrize("coordinator", ["та", "і"])
def test_construction_a_approved_coordination(coordinator):
    text = (
        f"Виконання перевіряється навантажувальним тестом {coordinator} "
        "інспекцією журналу."
    )
    specs = (
        _TokenSpec("перевіряється", lemma="перевірятися", upos="VERB"),
        _TokenSpec(
            "тестом", lemma="тест", relation="obl", morphology=_instrumental(), head=0
        ),
        _TokenSpec(coordinator, lemma=coordinator, relation="cc", head=3),
        _TokenSpec(
            "інспекцією",
            lemma="інспекція",
            relation="conj",
            morphology=_instrumental(),
            head=1,
        ),
    )
    _, _, outcome, evidence = _scan(text, specs)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [
        "навантажувальним тестом",
        "інспекцією журналу",
    ]
    assert [item.evidence_id for item in evidence] == [
        f"{RULE_ID}:E001",
        f"{RULE_ID}:E002",
    ]


def test_ambiguous_method_list_is_unresolved_not_partially_accepted():
    text = "Перевірка: тест та журнал."
    specs = (
        _TokenSpec("тест", lemma="тест"),
        _TokenSpec("та", lemma="та"),
    )
    _, _, outcome, evidence = _scan(text, specs)
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].candidate_span.text == "тест та журнал"


def test_semicolon_is_hard_boundary_and_second_candidate_is_independent():
    text = "Виконання перевіряється тестом; аналіз журналу виконує система."
    specs = (
        _TokenSpec("перевіряється", lemma="перевірятися", upos="VERB"),
        _TokenSpec(
            "тестом", lemma="тест", relation="obl", morphology=_instrumental(), head=0
        ),
        _TokenSpec("аналіз", lemma="аналіз"),
    )
    _, _, outcome, evidence = _scan(text, specs)
    assert [item.text for item in evidence] == ["тестом"]
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "аналіз журналу виконує система"
    ]


def test_system_behavior_analysis_is_unresolved_with_exact_binding_span():
    text = "Система виконує аналіз журналу."
    _, _, outcome, evidence = _scan(
        text, (_TokenSpec("аналіз", lemma="аналіз"),)
    )
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert outcome.diagnostics[0].candidate_span.text == "аналіз журналу"


def test_apparent_testability_is_complete_not_detected():
    text = (
        "Маршрут доставки повинен швидко перераховуватися у разі зміни "
        "дорожньої ситуації."
    )
    _, _, outcome, evidence = _scan(text)
    assert evidence == ()
    assert outcome.observations == ()
    assert outcome.diagnostics == ()
    assert outcome.processing_status is DetectionProcessingStatus.COMPLETE
    assert outcome.status is DetectionStatus.NOT_DETECTED


@pytest.mark.parametrize("candidate", ["acceptance test", "NFR test", "security tests"])
def test_isolated_named_method_candidates_are_unresolved(candidate):
    _, _, outcome, evidence = _scan(f"Посилання: {candidate}.")
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert outcome.diagnostics[0].candidate_span.text == candidate


def test_protected_sla_candidate_has_exact_unresolved_extent():
    text = (
        "Місячна доступність сервісу — не нижче 99,9 %; визначено допустимі "
        "виключення та спосіб розрахунку SLA."
    )
    _, _, outcome, evidence = _scan(text)
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    span = outcome.diagnostics[0].candidate_span
    assert (span.text, span.start_offset, span.end_offset) == (
        "спосіб розрахунку SLA",
        81,
        102,
    )


def test_quantitative_acceptance_does_not_infer_verification_method():
    _, _, outcome, evidence = _scan(
        "Система повинна відповісти не більше ніж за 2 с."
    )
    assert evidence == ()
    assert outcome.diagnostics == ()
    assert outcome.status is DetectionStatus.NOT_DETECTED


def test_accepted_plus_separate_unresolved_candidate_preserves_mixed_state():
    text = "Перевірка: security tests; Посилання на acceptance test."
    _, _, outcome, evidence = _scan(text)
    assert [item.text for item in evidence] == ["security tests"]
    assert outcome.status is DetectionStatus.DETECTED
    assert outcome.processing_status is DetectionProcessingStatus.INCOMPLETE
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "acceptance test"
    ]


def test_repeated_identical_accepted_methods_remain_distinct_and_source_ordered():
    text = "Перевірка: security tests; Перевірка: security tests."
    _, _, outcome, evidence = _scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == ["security tests", "security tests"]
    assert [item.evidence_id for item in evidence] == [
        f"{RULE_ID}:E001",
        f"{RULE_ID}:E002",
    ]
    assert evidence[0].start_offset < evidence[1].start_offset


def test_repeated_unresolved_candidates_and_diagnostics_remain_source_distinct():
    text = "acceptance test; acceptance test."
    _, _, outcome, evidence = _scan(text)
    assert evidence == ()
    assert outcome.status is DetectionStatus.UNRESOLVED
    assert [item.candidate_span.text for item in outcome.diagnostics] == [
        "acceptance test",
        "acceptance test",
    ]
    assert (
        outcome.diagnostics[0].candidate_span.start_offset
        < outcome.diagnostics[1].candidate_span.start_offset
    )


def test_nfc_comparison_preserves_decomposed_source_text():
    decomposed = "тестови\u0438\u0306 оракул"
    text = f"Перевірка: {decomposed}."
    _, _, outcome, evidence = _scan(text)
    assert outcome.status is DetectionStatus.DETECTED
    assert evidence[0].text == decomposed
    assert evidence[0].text == text[evidence[0].start_offset : evidence[0].end_offset]


def test_requirement_and_parser_outcome_are_not_mutated():
    text = "Виконання перевіряється навантажувальним тестом."
    requirement = Requirement("R049", 49, text)
    parsed = _parsed(requirement, _a_specs())
    parser_outcome = ParserOutcome(parsed, ())
    parser = _FakeParser(parser_outcome)

    VerificationMethodBaselineDetector(parser=parser).detect(requirement)

    assert requirement == Requirement("R049", 49, text)
    assert parser.outcome is parser_outcome
    assert parser.outcome == ParserOutcome(parsed, ())


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "Виконання перевіряється навантажувальним тестом.",
            "навантажувальним тестом",
        ),
        ("визначено негативні security tests.", "негативні security tests"),
        (
            "Дані передаються через TLS 1.3; доступ до API — за OAuth 2.0/OIDC; "
            "критичні операції журналюються; дані клієнтів логічно ізолюються "
            "між tenant-ами; визначено негативні security tests.",
            "негативні security tests",
        ),
    ],
)
def test_real_pinned_parser_smoke_binding_cases(text, expected):
    requirement = Requirement("R049", 49, text)
    outcome, evidence = VerificationMethodBaselineDetector().detect(requirement)
    assert outcome.status is DetectionStatus.DETECTED
    assert [item.text for item in evidence] == [expected]
