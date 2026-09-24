"""Approved concise Ukrainian user-view presentation tests (Section 19.6)."""

from decimal import Decimal
from fractions import Fraction

from requirements_quality_assessment.aggregator import SpecificationQualityAggregator
from requirements_quality_assessment.assessor import RequirementQualityAssessor
from requirements_quality_assessment.domain import (
    CharacteristicAssessmentState,
    CharacteristicId,
    DetectionDiagnostic,
    DetectionProcessingStatus,
    DiagnosticSpan,
    Evidence,
    FeatureDetectionOutcome,
    FeatureId,
    FeatureObservation,
    NumericValueComponent,
    QuantitativeConstraintObservation,
    Requirement,
    RequirementExtractionResult,
    RequirementFeatures,
    SpecificationCharacteristicAggregate,
    SpecificationQualityProfile,
    UnitComponent,
    UnitLabel,
    VagueTermOccurrence,
)
from requirements_quality_assessment.domain.specification_profile import (
    AGGREGATION_RULE_ID,
)
from requirements_quality_assessment.reporter import UserConsoleReporter


R002_TEXT = "Система повинна швидко оновити статус."
R004_TEXT = "Система повинна відповісти до 2 с."
R008_TEXT = "Система повинна швидко зберігати дані та показувати повідомлення."


def _empty(feature_id: FeatureId) -> FeatureDetectionOutcome:
    return FeatureDetectionOutcome(
        feature_id, (), DetectionProcessingStatus.COMPLETE, ()
    )


def _simple(
    feature_id: FeatureId,
    observation_refs: tuple[tuple[str, ...], ...],
) -> FeatureDetectionOutcome:
    return FeatureDetectionOutcome(
        feature_id,
        tuple(FeatureObservation(feature_id, refs) for refs in observation_refs),
        DetectionProcessingStatus.COMPLETE,
        (),
    )


def _evidence(
    requirement: Requirement,
    evidence_id: str,
    feature_id: FeatureId,
    text: str,
    rule_id: str,
    *,
    start: int | None = None,
) -> Evidence:
    offset = requirement.text.index(text) if start is None else start
    return Evidence(
        evidence_id,
        requirement.id,
        feature_id,
        text,
        offset,
        offset + len(text),
        rule_id,
    )


def _vague(
    evidence: Evidence,
) -> FeatureDetectionOutcome[VagueTermOccurrence]:
    return FeatureDetectionOutcome(
        FeatureId.VAGUE_TERM_OCCURRENCE,
        (
            VagueTermOccurrence(
                FeatureId.VAGUE_TERM_OCCURRENCE,
                "uk_vague_terms_v1",
                "швидко",
                (evidence.evidence_id,),
            ),
        ),
        DetectionProcessingStatus.COMPLETE,
        (),
    )


def _quantitative(
    evidence: Evidence,
) -> FeatureDetectionOutcome[QuantitativeConstraintObservation]:
    refs = (evidence.evidence_id,)
    observation = QuantitativeConstraintObservation(
        feature_id=FeatureId.QUANTITATIVE_CONSTRAINT,
        metric=None,
        comparator=None,
        value=NumericValueComponent(Decimal("2"), refs),
        unit=UnitComponent(UnitLabel.SECOND, refs),
        context=None,
        unresolved_components=(),
        evidence_refs=refs,
    )
    return FeatureDetectionOutcome(
        FeatureId.QUANTITATIVE_CONSTRAINT,
        (observation,),
        DetectionProcessingStatus.COMPLETE,
        (),
    )


def _record(
    requirement: Requirement,
    *,
    expected: FeatureDetectionOutcome | None = None,
    acceptance: FeatureDetectionOutcome | None = None,
    quantitative: FeatureDetectionOutcome | None = None,
    method: FeatureDetectionOutcome | None = None,
    vague: FeatureDetectionOutcome | None = None,
    evidence: tuple[Evidence, ...] = (),
):
    result = RequirementExtractionResult(
        requirement,
        RequirementFeatures(
            condition_contexts=_empty(FeatureId.CONDITION_CONTEXT),
            expected_results=expected or _empty(FeatureId.EXPECTED_RESULT),
            acceptance_criteria=acceptance or _empty(FeatureId.ACCEPTANCE_CRITERION),
            quantitative_constraints=quantitative
            or _empty(FeatureId.QUANTITATIVE_CONSTRAINT),
            verification_methods=method or _empty(FeatureId.VERIFICATION_METHOD),
            vague_term_occurrences=vague or _empty(FeatureId.VAGUE_TERM_OCCURRENCE),
        ),
        evidence,
    )
    return RequirementQualityAssessor().assess_record(result)


def _r002_record():
    requirement = Requirement("R002", 2, R002_TEXT)
    expected_evidence = _evidence(
        requirement,
        "RESULT-UK-001:E001",
        FeatureId.EXPECTED_RESULT,
        "Система повинна швидко оновити статус",
        "RESULT-UK-001",
    )
    vague_evidence = _evidence(
        requirement,
        "UK-VAGUE-001:E001",
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "швидко",
        "UK-VAGUE-001",
    )
    expected = _simple(
        FeatureId.EXPECTED_RESULT,
        ((expected_evidence.evidence_id,),),
    )
    return _record(
        requirement,
        expected=expected,
        vague=_vague(vague_evidence),
        evidence=(expected_evidence, vague_evidence),
    )


def _r004_record():
    requirement = Requirement("R004", 4, R004_TEXT)
    expected_evidence = _evidence(
        requirement,
        "RESULT-UK-001:E001",
        FeatureId.EXPECTED_RESULT,
        "Система повинна відповісти до 2 с",
        "RESULT-UK-001",
    )
    quantitative_evidence = _evidence(
        requirement,
        "QUANT-UK-001:E001",
        FeatureId.QUANTITATIVE_CONSTRAINT,
        "до 2 с",
        "QUANT-UK-001",
    )
    expected = _simple(
        FeatureId.EXPECTED_RESULT,
        ((expected_evidence.evidence_id,),),
    )
    start = requirement.text.index("до 2 с")
    diagnostic = DetectionDiagnostic(
        "ACCEPT_UNRESOLVED_CANDIDATE",
        "A contained accepted quantitative candidate is not judgeable.",
        "ACCEPT-QUANT-001",
        DiagnosticSpan("до 2 с", start, start + len("до 2 с")),
    )
    acceptance = FeatureDetectionOutcome(
        FeatureId.ACCEPTANCE_CRITERION,
        (),
        DetectionProcessingStatus.INCOMPLETE,
        (diagnostic,),
    )
    return _record(
        requirement,
        expected=expected,
        acceptance=acceptance,
        quantitative=_quantitative(quantitative_evidence),
        evidence=(expected_evidence, quantitative_evidence),
    )


def _r008_record():
    requirement = Requirement("R008", 8, R008_TEXT)
    anchor = _evidence(
        requirement,
        "RESULT-UK-002:E001",
        FeatureId.EXPECTED_RESULT,
        "Система повинна",
        "RESULT-UK-002",
    )
    first = _evidence(
        requirement,
        "RESULT-UK-002:E002",
        FeatureId.EXPECTED_RESULT,
        "Система повинна швидко зберігати дані",
        "RESULT-UK-002",
    )
    second = _evidence(
        requirement,
        "RESULT-UK-002:E003",
        FeatureId.EXPECTED_RESULT,
        "показувати повідомлення",
        "RESULT-UK-002",
    )
    vague_evidence = _evidence(
        requirement,
        "UK-VAGUE-001:E001",
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "швидко",
        "UK-VAGUE-001",
    )
    expected = _simple(
        FeatureId.EXPECTED_RESULT,
        ((first.evidence_id,), (anchor.evidence_id, second.evidence_id)),
    )
    return _record(
        requirement,
        expected=expected,
        vague=_vague(vague_evidence),
        evidence=(anchor, first, vague_evidence, second),
    )


def _render(record) -> str:
    specification = SpecificationQualityAggregator().aggregate(
        (record.quality_profile,)
    )
    return UserConsoleReporter().render((record,), specification)


def _requirement_block(output: str) -> str:
    return output.removeprefix("Звіт про якість вимог\n\n").split(
        "\n\nПідсумок специфікації", 1
    )[0]


def test_r002_exact_concise_user_view() -> None:
    output = _requirement_block(_render(_r002_record()))

    assert output == "\n".join(
        [
            "Вимога R002",
            f"Текст: {R002_TEXT}",
            "",
            "Повнота: 1/3",
            "Перевірюваність: 0",
            "Однозначність: 1/2",
            "",
            "Чому така оцінка:",
            "  - Повнота: Виявлено: очікуваний результат; за реалізованими правилами не виявлено: умову/контекст і критерій приймання. Кожен із трьох складників враховується один раз.",
            "  - Перевірюваність: Критерій приймання, кількісне обмеження та метод перевірки завершено без прийнятих спостережень. Це завершена відсутність за реалізованими правилами, а не підтверджений дефект.",
            "  - Однозначність: Виявлено 1 підтримуваний SIGNAL, тому значення 1/2; кількість сигналів не накопичує оцінку. SIGNAL є потенційним індикатором, а не підтвердженою неоднозначністю чи дефектом.",
            "",
            "Звернути увагу:",
            "  - SIGNAL: «швидко» — підтримуваний індикатор потенційної неоднозначності, а не підтверджений дефект.",
        ]
    )


def test_r004_exact_unknown_view_keeps_evidence_and_diagnostic_distinct() -> None:
    output = _requirement_block(_render(_r004_record()))

    assert output == "\n".join(
        [
            "Вимога R004",
            f"Текст: {R004_TEXT}",
            "",
            "Повнота: UNKNOWN",
            "Перевірюваність: UNKNOWN",
            "Однозначність: 1",
            "",
            "Чому така оцінка:",
            "  - Повнота: Виявлено: очікуваний результат; за реалізованими правилами не виявлено: умову/контекст; невирішено: критерій приймання. Через невирішений обов'язковий складник результат UNKNOWN.",
            "  - Перевірюваність: Виявлено: кількісне обмеження; за реалізованими правилами не виявлено: метод перевірки; невирішено: критерій приймання. Невирішений істотний кандидат може змінити рівень, тому результат UNKNOWN.",
            "  - Однозначність: Пошук підтримуваного класу SIGNAL завершено без прийнятих входжень, тому значення 1. Це не доводить єдиність тлумачення.",
            "",
            "Звернути увагу:",
            "  - Невирішений кандидат критерію приймання (не прийняте Evidence): «до 2 с». Цей самий фрагмент окремо прийнято як Evidence кількісного обмеження; невирішений кандидат може змінити Повноту й Перевірюваність, тому відповідний результат лишається UNKNOWN.",
        ]
    )
    assert output.count("«до 2 с»") == 1


def test_r008_exact_view_explains_repeated_observations_without_extra_weight() -> None:
    output = _requirement_block(_render(_r008_record()))

    assert output == "\n".join(
        [
            "Вимога R008",
            f"Текст: {R008_TEXT}",
            "",
            "Повнота: 1/3",
            "Перевірюваність: 0",
            "Однозначність: 1/2",
            "",
            "Чому така оцінка:",
            "  - Повнота: Виявлено: два очікувані результати; за реалізованими правилами не виявлено: умову/контекст і критерій приймання. Кожен із трьох складників враховується один раз, тому повторні спостереження одного складника не збільшують оцінку.",
            "  - Перевірюваність: Критерій приймання, кількісне обмеження та метод перевірки завершено без прийнятих спостережень. Це завершена відсутність за реалізованими правилами, а не підтверджений дефект.",
            "  - Однозначність: Виявлено 1 підтримуваний SIGNAL, тому значення 1/2; кількість сигналів не накопичує оцінку. SIGNAL є потенційним індикатором, а не підтвердженою неоднозначністю чи дефектом.",
            "",
            "Звернути увагу:",
            "  - SIGNAL: «швидко» — підтримуваний індикатор потенційної неоднозначності, а не підтверджений дефект.",
            "",
            "Підстава в тексті:",
            "  - Перше прийняте спостереження очікуваного результату: «Система повинна швидко зберігати дані».",
            "  - Друге прийняте спостереження очікуваного результату: «Система повинна» + «показувати повідомлення».",
        ]
    )


def _aggregate(
    characteristic_id: CharacteristicId,
    value: Fraction,
    computed: int,
    unknown: int,
) -> SpecificationCharacteristicAggregate:
    return SpecificationCharacteristicAggregate(
        characteristic_id,
        CharacteristicAssessmentState.COMPUTED,
        value,
        computed,
        unknown,
        0,
        computed + unknown,
        AGGREGATION_RULE_ID,
    )


def test_eight_case_summary_shows_exact_values_and_all_four_counts() -> None:
    records = (_r002_record(),) * 8
    specification = SpecificationQualityProfile(
        completeness=_aggregate(CharacteristicId.COMPLETENESS, Fraction(11, 18), 6, 2),
        verifiability=_aggregate(CharacteristicId.VERIFIABILITY, Fraction(1, 2), 7, 1),
        unambiguity=_aggregate(CharacteristicId.UNAMBIGUITY, Fraction(7, 8), 8, 0),
    )

    output = UserConsoleReporter().render(records, specification)
    summary = output[output.index("Підсумок специфікації"):output.index("Межі звіту")]

    assert "Вимог: 8" in summary
    assert "Повнота: 11/18 (обчислено: 6; UNKNOWN: 2; NOT_APPLICABLE: 0; усього: 8)" in summary
    assert "Перевірюваність: 1/2 (обчислено: 7; UNKNOWN: 1; NOT_APPLICABLE: 0; усього: 8)" in summary
    assert "Однозначність: 7/8 (обчислено: 8; UNKNOWN: 0; NOT_APPLICABLE: 0; усього: 8)" in summary


def test_empty_user_view_has_not_applicable_summary_and_one_disclosure() -> None:
    specification = SpecificationQualityAggregator().aggregate(())

    output = UserConsoleReporter().render((), specification)

    assert output.startswith("Звіт про якість вимог\n\nПідсумок специфікації")
    assert "Вимог: 0" in output
    assert output.count("NOT_APPLICABLE (обчислено: 0; UNKNOWN: 0; NOT_APPLICABLE: 0; усього: 0)") == 3
    assert output.count("Межі звіту") == 1
    disclosures = (
        "Покриття обмежене реалізованими правилами для шести сімейств ознак і C/V/U; це не вичерпний аналіз української мови або змісту вимог.",
        "NOT_DETECTED і завершена відсутність означають лише, що завершені реалізовані правила не прийняли спостереження; це не універсальна семантична відсутність.",
        "Значення C/V, зокрема низькі або нульові, є результатами правил, а не підтвердженими дефектами.",
        "U=1 означає відсутність підтримуваного класу SIGNAL, а не доказ єдиного тлумачення; U=1/2 означає наявність SIGNAL, а не підтверджену неоднозначність; чинне правило U не повертає 0.",
        "FIND-U-VAGUE-001 створює лише SIGNAL; чинна модель не створює QUALITY_PROBLEM, рівень серйозності, упевненість, ризик або коригувальну дію.",
        "R3 і F1-A затверджені дослідником, але не реалізовані й не належать до заявленого покриття виконання.",
        "Це багатовимірний профіль C/V/U, а не скалярна оцінка вимоги чи прогноз якості програмного продукту.",
    )
    for index, disclosure in enumerate(disclosures, 1):
        assert output.count(f"  {index}. {disclosure}") == 1
    assert "Вимога " not in output


def test_user_view_omits_audit_trace_and_is_deterministic() -> None:
    record = _r004_record()
    specification = SpecificationQualityAggregator().aggregate((record.quality_profile,))
    reporter = UserConsoleReporter()

    first = reporter.render((record,), specification)
    second = reporter.render((record,), specification)

    assert first == second
    for forbidden in (
        "FORMAL RESULT",
        "decision_code:",
        "effect_code:",
        "observation_index:",
        "diagnostic_index:",
        "evidence_id:",
        "rule_id:",
        "FeatureObservation(",
        "range: [",
    ):
        assert forbidden not in first


def test_multiple_signals_remain_source_ordered_and_non_cumulative() -> None:
    text = "Система повинна швидко і потім швидко відповісти."
    requirement = Requirement("R009", 9, text)
    first = _evidence(
        requirement,
        "UK-VAGUE-001:E001",
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "швидко",
        "UK-VAGUE-001",
    )
    second = _evidence(
        requirement,
        "UK-VAGUE-001:E002",
        FeatureId.VAGUE_TERM_OCCURRENCE,
        "швидко",
        "UK-VAGUE-001",
        start=text.rindex("швидко"),
    )
    vague = FeatureDetectionOutcome(
        FeatureId.VAGUE_TERM_OCCURRENCE,
        (
            VagueTermOccurrence(
                FeatureId.VAGUE_TERM_OCCURRENCE,
                "uk_vague_terms_v1",
                "швидко",
                (first.evidence_id,),
            ),
            VagueTermOccurrence(
                FeatureId.VAGUE_TERM_OCCURRENCE,
                "uk_vague_terms_v1",
                "швидко",
                (second.evidence_id,),
            ),
        ),
        DetectionProcessingStatus.COMPLETE,
        (),
    )
    output = _render(
        _record(requirement, vague=vague, evidence=(first, second))
    )

    assert "Однозначність: 1/2" in output
    assert "Виявлено 2 підтримуваних SIGNAL" in output
    assert output.count("  - SIGNAL: «швидко»") == 2


def test_material_diagnostic_without_span_is_visible_but_not_evidence() -> None:
    requirement = Requirement("R010", 10, "Виконання перевіряється тестом.")
    diagnostic = DetectionDiagnostic(
        "VERIFY_PARSER_BLOCKED",
        "Parser annotations are unavailable.",
        "VERIFY-UK-001",
        None,
    )
    method = FeatureDetectionOutcome(
        FeatureId.VERIFICATION_METHOD,
        (),
        DetectionProcessingStatus.INCOMPLETE,
        (diagnostic,),
    )

    output = _render(_record(requirement, method=method))

    assert "Перевірюваність: UNKNOWN" in output
    assert (
        "Невирішений кандидат без окремого джерельного фрагмента "
        "(не прийняте Evidence). Він може змінити Перевірюваність"
    ) in output
    assert "Підстава в тексті:" not in output


def test_completed_absence_creates_no_attention_or_source_evidence() -> None:
    requirement = Requirement("R011", 11, "Система працює.")

    output = _render(_record(requirement))

    assert "Повнота: 0" in output
    assert "Перевірюваність: 0" in output
    assert "Однозначність: 1" in output
    assert "Звернути увагу:" not in output
    assert "Підстава в тексті:" not in output
    assert "Прийняте Evidence" not in output


def test_user_view_rejects_legacy_requirement_profile_pairs() -> None:
    record = _r002_record()
    specification = SpecificationQualityAggregator().aggregate((record.quality_profile,))

    try:
        UserConsoleReporter().render(
            ((record.extraction_result.requirement, record.quality_profile),),
            specification,
        )
    except TypeError as exc:
        assert str(exc) == "user view requires RequirementAssessmentRecord inputs"
    else:
        raise AssertionError("legacy audit-only input was accepted by user view")
