# Dual-view CLI presentation contract proposal

- **Status:** `RESEARCHER_APPROVED`
- **Researcher decision date:** 2026-09-23
- **Authoritative amendment:** [`model-spec.md` §19.6](model-spec.md)
- **Delivery:** existing branch `feature/dual-view-presentation` and existing
  PR #108
- **Scientific input contract:** [`model-spec.md` §7.17](model-spec.md)

## 1. Approved decision

The researcher approves two presentations of the same already-computed
`RequirementAssessmentRecord` values and `SpecificationQualityProfile`:

1. `user` — a concise Ukrainian assessment and the new CLI default; and
2. `audit` — the existing complete formal, scientific-trace report.

The proposed CLI interface remains:

```text
--view {user,audit}
```

The default is `user`. Explicit `--view audit` produces the existing output.

The authoritative approval is recorded in `model-spec.md` §19.6. The
researcher directed approval, implementation, tests, and user documentation to
be completed in the same branch and PR #108. This document does not itself
change production behavior; the implementation in that PR does so only within
the approved presentation boundary.

## 2. Scientific and architectural invariants

Both views consume the same completed objects after the single approved
scientific pipeline has finished:

```text
RequirementReader
→ FeatureExtractor
→ RequirementExtractionResult
→ RequirementQualityAssessor
→ RequirementAssessmentRecord
→ SpecificationQualityAggregator
→ SpecificationQualityProfile
→ selected presentation renderer
```

View selection occurs only at the final presentation boundary. There is no
second extraction, assessment, calculation, aggregation, interpretation
engine, Finding classification, or Evidence generation.

Both views preserve:

- exact `Fraction` values;
- literal `UNKNOWN` and `NOT_APPLICABLE` values;
- independent Completeness, Verifiability, and Unambiguity results in C/V/U
  order;
- original requirement text and source order;
- the distinction among accepted Evidence, an unresolved diagnostic
  candidate, and completed absence without Evidence;
- `SIGNAL` as a potential indicator, never a confirmed defect;
- all four aggregate observability counts;
- all seven approved bounded non-claims; and
- no scalar requirement or file score, rating, recommendation, risk,
  corrective action, severity, confidence, or new scientific rule.

The difference is presentation depth. The user view answers “what is the
result and why should I understand it this way?” The audit view exposes the
complete machine-resolvable path that justifies the same result.

## 3. Explicit amendment to the approved §19 contract

The approved §19.6 amendment provides:

- current §19.1–§19.4 and current `ConsoleReporter.render()` become the
  normative `audit` view without any content or byte change;
- a new concise `user` view becomes the CLI default;
- §19 Q1–Q4 and Q6–Q8 keep their approved scientific meaning;
- Q5 is extended from one detailed presentation to two presentations over the
  same completed record; and
- the user view may omit internal trace detail only because the exact same
  detail remains available through `--view audit` and the audit API.

This is a deliberate approved amendment, not an interpretation silently
derived from the previously approved text. The detailed presentation remains
normative as the audit view; §19.6 separately authorizes the concise projection
and its exact omissions.

## 4. Exact `user`-view contract

### 4.1 Conciseness is normative

The user view is not a translated audit report. For each requirement it has:

1. the requirement ID and original Ukrainian text;
2. one compact three-line C/V/U result;
3. exactly three short explanations under `Чому така оцінка`, one per
   characteristic and no more than two sentences each;
4. `Звернути увагу` only when there is a supported `SIGNAL` or a material
   unresolved diagnostic; and
5. `Підстава в тексті` only when additional accepted source fragments
   materially improve understanding and have not already been shown under
   `Звернути увагу`.

The user view must not contain a separate block for every
`FeatureInputTrace`. It must not reproduce the formal result plus a second
interpretation of the same trace.

### 4.2 Whole-report layout

`UserConsoleReporter.render(records, specification_profile)` returns a string
with no trailing newline and this exact order:

```text
Звіт про якість вимог

<requirement block R001>

<requirement block R002>

...

<concise specification summary>

<one report-level bounded disclosure>
```

Blocks are separated by one empty line. The CLI's existing `print(...)` adds
the final newline. For an empty input, no requirement block appears; the
summary and the one bounded disclosure remain.

### 4.3 Always-visible requirement information

Every requirement uses exactly this outer layout:

```text
Вимога <requirement.id>
Текст: <requirement.text>

Повнота: <exact Fraction|UNKNOWN|NOT_APPLICABLE>
Перевірюваність: <exact Fraction|UNKNOWN|NOT_APPLICABLE>
Однозначність: <exact Fraction|UNKNOWN|NOT_APPLICABLE>

Чому така оцінка:
  - Повнота: <one or two short sentences>
  - Перевірюваність: <one or two short sentences>
  - Однозначність: <one or two short sentences>
<optional attention section>
<optional source-basis section>
```

`Requirement.text` is copied exactly after the approved reader trimming step.
A computed value is rendered as its exact reduced fraction. An unavailable
value is the literal token `UNKNOWN` or `NOT_APPLICABLE`, never `0`, `N/A`, a
blank, decimal, or percentage.

Raw assessment state is not printed separately because the literal result
already conveys the user-relevant state. The audit view retains both `state`
and `value` fields.

### 4.4 Exact explanation templates

The renderer fills the templates below only from the already-approved
`CharacteristicTrace`, `FeatureInputTrace`, referenced outcomes, and completed
assessment. It may use existing decision/effect codes to select a template,
but it must not print those codes or reinterpret them.

The fixed Ukrainian feature names used in lists are:

- `умову/контекст`;
- `очікуваний результат`;
- `критерій приймання`;
- `кількісне обмеження`;
- `метод перевірки`; and
- `підтримуваний SIGNAL`.

For a computed Completeness ratio:

```text
Виявлено: <detected C items>; за реалізованими правилами не виявлено: <completed-absent C items>. Кожен із трьох складників враховується один раз<optional repeated-observation suffix>.
```

If no list item exists, render `немає`. When one C family has more than one
accepted observation, append exactly:

```text
, тому повторні спостереження одного складника не збільшують оцінку
```

For `UNKNOWN` Completeness:

```text
Виявлено: <detected C items>; за реалізованими правилами не виявлено: <completed-absent C items>; невирішено: <material unresolved C items>. Через невирішений обов'язковий складник результат UNKNOWN.
```

For full-tier Verifiability:

```text
Виявлено прийнятий критерій приймання, тому застосовано повний затверджений рівень. Інші прийняті або невирішені нижчі шляхи не змінюють цього рівня.
```

The second sentence is omitted when no accepted or unresolved lower-tier input
exists.

For lower-tier Verifiability:

```text
Критерій приймання завершено без прийнятого спостереження; виявлено <accepted quantitative constraint and/or verification method>, тому застосовано нижчий затверджений рівень.
```

For zero-tier Verifiability:

```text
Критерій приймання, кількісне обмеження та метод перевірки завершено без прийнятих спостережень. Це завершена відсутність за реалізованими правилами, а не підтверджений дефект.
```

For `UNKNOWN` Verifiability:

```text
Виявлено: <accepted V inputs>; за реалізованими правилами не виявлено: <completed-absent V inputs>; невирішено: <material unresolved V inputs>. Невирішений істотний кандидат може змінити рівень, тому результат UNKNOWN.
```

For Unambiguity with one or more supported signals:

```text
Виявлено <count> підтримуваний SIGNAL, тому значення 1/2; кількість сигналів не накопичує оцінку. SIGNAL є потенційним індикатором, а не підтвердженою неоднозначністю чи дефектом.
```

Ukrainian number agreement may use `підтримуваних SIGNAL` for counts other
than one; this is language formatting, not a scientific decision.

For completed absence of the supported signal class:

```text
Пошук підтримуваного класу SIGNAL завершено без прийнятих входжень, тому значення 1. Це не доводить єдиність тлумачення.
```

For `UNKNOWN` Unambiguity:

```text
Пошук підтримуваного класу SIGNAL не завершено: невирішена обробка ще може виявити індикатор. Тому результат UNKNOWN.
```

For any future separately approved `NOT_APPLICABLE` characteristic:

```text
Стан NOT_APPLICABLE встановлено чинним керівним правилом; числового значення немає.
```

No current requirement-level C/V/U rule establishes `NOT_APPLICABLE`; the
renderer must not invent such a rule merely to exercise the template.

The phrases `за реалізованими правилами не виявлено` and `завершено без
прийнятих спостережень` are mandatory for completed absence. They must not be
shortened to an unbounded claim such as “the requirement has no criterion.”

### 4.5 Conditional `Звернути увагу`

Render this section only when the completed record contains either:

- a supported Finding with `kind=SIGNAL`; or
- a diagnostic already classified by the approved trace as material to an
  `UNKNOWN` result.

```text
Звернути увагу:
  - <attention item>
```

Each supported vague-term Finding is rendered once, in existing source order:

```text
SIGNAL: «<exact Evidence.text>» — підтримуваний індикатор потенційної неоднозначності, а не підтверджений дефект.
```

Each material diagnostic is rendered once even if the same underlying
diagnostic blocks more than one characteristic. The affected characteristic
names are combined in C/V/U order. With a candidate span:

```text
Невирішений кандидат (не прийняте Evidence): «<exact DiagnosticSpan.text>». Він може змінити <affected characteristics>, тому відповідний результат лишається UNKNOWN.
```

Without a candidate span:

```text
Невирішений кандидат без окремого джерельного фрагмента (не прийняте Evidence). Він може змінити <affected characteristics>, тому відповідний результат лишається UNKNOWN.
```

When the same source range is accepted Evidence for another feature, replace
the first template with this exact distinction:

```text
Невирішений кандидат <diagnostic feature label> (не прийняте Evidence): «<exact DiagnosticSpan.text>». Цей самий фрагмент окремо прийнято як Evidence <accepted feature label>; невирішений кандидат може змінити <affected characteristics>, тому відповідний результат лишається UNKNOWN.
```

This wording preserves both roles without converting the diagnostic candidate
to Evidence. Diagnostic codes, rule IDs, detailed explanations, offsets, and
materiality trace remain in audit mode.

If neither condition applies, the entire `Звернути увагу` heading is omitted;
the user view does not print `немає`.

### 4.6 Conditional `Підстава в тексті`

This optional section shows only accepted Evidence that materially helps a
reader understand the short explanation and is not already shown in
`Звернути увагу`:

```text
Підстава в тексті:
  - <Ukrainian role>: «<exact Evidence.text>»< + «additional exact Evidence.text»>.
```

Rules:

- use accepted Evidence only, never a diagnostic span or completed absence;
- copy complete `Evidence.text` exactly; do not derive a shorter span or create
  a new Evidence object;
- when one observation needs multiple Evidence references, join their exact
  texts with ` + ` in reference order;
- include this section only for accepted V evidence that selects a tier, a C
  family with multiple accepted observations, or accepted Evidence whose
  separate role beside a material diagnostic must be explained;
- preserve source/observation order;
- show each Evidence source range once even if more than one characteristic
  references it;
- do not repeat SIGNAL Evidence already shown under `Звернути увагу`;
- do not create Evidence or a fragment for completed absence; and
- omit the entire section when the original text and short explanations are
  already sufficient.

This is a source-attribution aid, not a complete Evidence registry. Exact
Evidence objects remain available in audit mode.

### 4.7 Information boundary: always, conditional, audit-only

| Information | User visibility | Contract |
|---|---|---|
| Requirement ID and original text | Always | Exact source-order value |
| C/V/U result | Always | Three compact lines; exact fraction or literal unavailable state |
| Why the result has that value/state | Always | Three bullets, each one or two short Ukrainian sentences |
| Supported `SIGNAL` | Conditional | `Звернути увагу`; literal `SIGNAL`, exact source fragment, explicit non-defect wording |
| Material unresolved diagnostic | Conditional | `Звернути увагу`; exact candidate fragment when present and explicit `(не прийняте Evidence)` |
| Accepted source fragment helpful to understanding | Conditional | `Підстава в тексті`; deduplicated and concise |
| Non-material diagnostic | Audit only | It does not require user action to understand the current class |
| Rule IDs and coverage profile ID | Audit only | Retained byte-for-byte in current output |
| `TraceDecisionCode` and `TraceEffectCode` | Audit only | Never dumped in user mode |
| Processing/detection status and applicability fields | Audit only | Never dumped in user mode |
| Observation and diagnostic indexes | Audit only | Never dumped in user mode |
| Raw dataclass serialization | Audit only | Never dumped in user mode |
| Evidence IDs, exact offsets, feature IDs, and detector rule IDs | Audit only | User source fragments remain attributable; complete provenance stays in audit |
| Raw assessment/Finding/diagnostic explanations | Audit only | User mode uses only the fixed concise templates above |
| Full per-input trace blocks | Audit only | No user-mode `FeatureInputTrace` repetition |
| Seven bounded non-claims | Always at report level | Exactly one concise disclosure block in user mode; existing per-record audit disclosures unchanged |

### 4.8 Concise specification summary

The user summary appears once after all requirement blocks:

```text
Підсумок специфікації
Вимог: <record count>
Повнота: <exact Fraction|UNKNOWN|NOT_APPLICABLE> (обчислено: <computed_count>; UNKNOWN: <unknown_count>; NOT_APPLICABLE: <not_applicable_count>; усього: <total_count>)
Перевірюваність: <exact Fraction|UNKNOWN|NOT_APPLICABLE> (обчислено: <computed_count>; UNKNOWN: <unknown_count>; NOT_APPLICABLE: <not_applicable_count>; усього: <total_count>)
Однозначність: <exact Fraction|UNKNOWN|NOT_APPLICABLE> (обчислено: <computed_count>; UNKNOWN: <unknown_count>; NOT_APPLICABLE: <not_applicable_count>; усього: <total_count>)
```

All four counts are unconditional for every characteristic. The renderer
copies the supplied aggregate fields; it does not recalculate them. No overall
file-quality value or state is added. `aggregation_rule_id` remains audit-only.

### 4.9 One report-level bounded disclosure

The user view renders this block exactly once, after the summary. It preserves
all seven canonical `MVP-V0.1-BOUNDED-CVU-001` non-claims:

```text
Межі звіту
  1. Покриття обмежене реалізованими правилами для шести сімейств ознак і C/V/U; це не вичерпний аналіз української мови або змісту вимог.
  2. NOT_DETECTED і завершена відсутність означають лише, що завершені реалізовані правила не прийняли спостереження; це не універсальна семантична відсутність.
  3. Значення C/V, зокрема низькі або нульові, є результатами правил, а не підтвердженими дефектами.
  4. U=1 означає відсутність підтримуваного класу SIGNAL, а не доказ єдиного тлумачення; U=1/2 означає наявність SIGNAL, а не підтверджену неоднозначність; чинне правило U не повертає 0.
  5. FIND-U-VAGUE-001 створює лише SIGNAL; чинна модель не створює QUALITY_PROBLEM, рівень серйозності, упевненість, ризик або коригувальну дію.
  6. R3 і F1-A затверджені дослідником, але не реалізовані й не належать до заявленого покриття виконання.
  7. Це багатовимірний профіль C/V/U, а не скалярна оцінка вимоги чи прогноз якості програмного продукту.
```

The audit view continues to render its existing canonical disclosure block
inside every record. The user renderer may not select, weaken, or strengthen
these seven claims.

## 5. DEMONSTRATION — actual previously observed results

**DEMONSTRATION ONLY.** The following outputs use actual results previously
observed on current `main` including merged PR #107. They demonstrate the
proposed presentation and are not new approved reference annotations,
detector expectations, or validation data.

### 5.1 DEMONSTRATION — R002

The audit record contains the accepted `швидко` Evidence at `[16,22)`. The
offset remains audit-only in the proposed user view.

```text
Вимога R002
Текст: Система повинна швидко оновити статус.

Повнота: 1/3
Перевірюваність: 0
Однозначність: 1/2

Чому така оцінка:
  - Повнота: Виявлено: очікуваний результат; за реалізованими правилами не виявлено: умову/контекст і критерій приймання. Кожен із трьох складників враховується один раз.
  - Перевірюваність: Критерій приймання, кількісне обмеження та метод перевірки завершено без прийнятих спостережень. Це завершена відсутність за реалізованими правилами, а не підтверджений дефект.
  - Однозначність: Виявлено 1 підтримуваний SIGNAL, тому значення 1/2; кількість сигналів не накопичує оцінку. SIGNAL є потенційним індикатором, а не підтвердженою неоднозначністю чи дефектом.

Звернути увагу:
  - SIGNAL: «швидко» — підтримуваний індикатор потенційної неоднозначності, а не підтверджений дефект.
```

No separate source-basis section is needed: the only fragment material to the
user's attention is already shown once under `Звернути увагу`.

### 5.2 DEMONSTRATION — R004

The same exact source fragment has two approved but distinct roles: accepted
quantitative Evidence and a separate unresolved acceptance-criterion
diagnostic candidate. The user output makes that distinction without exposing
their internal IDs or offsets.

```text
Вимога R004
Текст: Система повинна відповісти до 2 с.

Повнота: UNKNOWN
Перевірюваність: UNKNOWN
Однозначність: 1

Чому така оцінка:
  - Повнота: Виявлено: очікуваний результат; за реалізованими правилами не виявлено: умову/контекст; невирішено: критерій приймання. Через невирішений обов'язковий складник результат UNKNOWN.
  - Перевірюваність: Виявлено: кількісне обмеження; за реалізованими правилами не виявлено: метод перевірки; невирішено: критерій приймання. Невирішений істотний кандидат може змінити рівень, тому результат UNKNOWN.
  - Однозначність: Пошук підтримуваного класу SIGNAL завершено без прийнятих входжень, тому значення 1. Це не доводить єдиність тлумачення.

Звернути увагу:
  - Невирішений кандидат критерію приймання (не прийняте Evidence): «до 2 с». Цей самий фрагмент окремо прийнято як Evidence кількісного обмеження; невирішений кандидат може змінити Повноту й Перевірюваність, тому відповідний результат лишається UNKNOWN.
```

The fragment is shown once. It is not duplicated in a source-basis section.

### 5.3 DEMONSTRATION — R008

```text
Вимога R008
Текст: Система повинна швидко зберігати дані та показувати повідомлення.

Повнота: 1/3
Перевірюваність: 0
Однозначність: 1/2

Чому така оцінка:
  - Повнота: Виявлено: два очікувані результати; за реалізованими правилами не виявлено: умову/контекст і критерій приймання. Кожен із трьох складників враховується один раз, тому повторні спостереження одного складника не збільшують оцінку.
  - Перевірюваність: Критерій приймання, кількісне обмеження та метод перевірки завершено без прийнятих спостережень. Це завершена відсутність за реалізованими правилами, а не підтверджений дефект.
  - Однозначність: Виявлено 1 підтримуваний SIGNAL, тому значення 1/2; кількість сигналів не накопичує оцінку. SIGNAL є потенційним індикатором, а не підтвердженою неоднозначністю чи дефектом.

Звернути увагу:
  - SIGNAL: «швидко» — підтримуваний індикатор потенційної неоднозначності, а не підтверджений дефект.

Підстава в тексті:
  - Перше прийняте спостереження очікуваного результату: «Система повинна швидко зберігати дані».
  - Друге прийняте спостереження очікуваного результату: «Система повинна» + «показувати повідомлення».
```

The two observations belong to one Completeness family and therefore do not
increase the value beyond that family's single contribution.

### 5.4 DEMONSTRATION — eight-case specification summary

```text
Підсумок специфікації
Вимог: 8
Повнота: 11/18 (обчислено: 6; UNKNOWN: 2; NOT_APPLICABLE: 0; усього: 8)
Перевірюваність: 1/2 (обчислено: 7; UNKNOWN: 1; NOT_APPLICABLE: 0; усього: 8)
Однозначність: 7/8 (обчислено: 8; UNKNOWN: 0; NOT_APPLICABLE: 0; усього: 8)
```

The complete user report appends the single §4.9 `Межі звіту` block. It is not
repeated in this demonstration snippet.

## 6. Audit view: complete and unchanged

`ConsoleReporter.render(requirement_results, specification_profile)` remains
the audit API with:

- the same class name and import path;
- the same signature and accepted record/legacy-tuple inputs;
- byte-for-byte identical output for identical inputs;
- all existing formal fields and raw domain rendering;
- Rule IDs, assessment state/value, decision/effect codes, applicability,
  processing and detection statuses;
- every accepted observation and observation index;
- exact Evidence IDs, text, offsets, feature IDs, and detector Rule IDs;
- every diagnostic index, code, rule, explanation, and candidate span;
- completed-absence provenance without fabricated Evidence;
- Findings and resolved Finding Evidence;
- the current full human-readable interpretation;
- the current seven-item coverage disclosure in every record; and
- the current specification summary and aggregation Rule IDs.

No existing `ConsoleReporter` caller silently receives user output. The only
default change is at the CLI selection boundary.

## 7. CLI and API compatibility plan

### 7.1 New user API

Add the approved separate renderer in this implementation:

```python
class UserConsoleReporter:
    def render(
        self,
        requirement_results: Iterable[RequirementAssessmentRecord],
        specification_profile: SpecificationQualityProfile,
    ) -> str: ...
```

The user API requires completed §7.17 records. It has no legacy
`tuple[Requirement, RequirementQualityProfile]` mode because concise
explanation, diagnostic materiality, and source attribution require the
approved trace bundle.

The user renderer does not subclass the audit renderer and does not parse audit
text. It formats the same domain objects directly. Pure shared formatting
helpers are allowed only if `ConsoleReporter.render()` remains byte-for-byte
unchanged.

### 7.2 CLI orchestration

The CLI adds:

```python
parser.add_argument(
    "--view",
    choices=("user", "audit"),
    default="user",
)
```

Only after the existing single assessment and aggregation pass:

```text
user  → UserConsoleReporter.render(records, specification_profile)
audit → ConsoleReporter.render(records, specification_profile)
```

The intentional compatibility change is:

- `python -m requirements_quality_assessment PATH` becomes the concise user
  view;
- it equals `python -m requirements_quality_assessment --view user PATH`;
- `python -m requirements_quality_assessment --view audit PATH` is
  byte-for-byte equal to the pre-change CLI output for the same input; and
- direct `ConsoleReporter.render()` callers observe no change.

View selection is never passed into the reader, extractor, assessor,
calculators, trace builder, aggregator, or domain models. File errors, UTF-8
handling, stderr text, and exit codes remain independent of the selected view.

## 8. Implementation test and acceptance matrix

The implementation in the existing branch and PR #108 must cover at least this
matrix.

| Area | Fixture/action | Required result |
|---|---|---|
| Audit API backward compatibility | Render every existing reporter fixture before and after the change | Byte-for-byte equality, including all fields, trace, disclosures, whitespace, and summary |
| Audit CLI backward compatibility | Compare pre-change default output with post-change `--view audit` | Byte-for-byte stdout equality; unchanged stderr and exit code |
| CLI default | Compare omitted `--view` with explicit `--view user` | Byte-for-byte equality |
| Same science | Capture records and aggregate passed to each renderer | Same completed values/objects; one extraction, assessment, trace, Finding, and aggregation path |
| R002 concise user view | Actual R002 record | Exact §5.1 output; compact `1/3`, `0`, `1/2`; one source-attributable `SIGNAL`; no confirmed-defect wording |
| R004 concise user view | Actual R004 record | Exact §5.2 output; literal C/V `UNKNOWN`; accepted quantitative Evidence and non-Evidence diagnostic remain distinct; material blocker explained |
| R008 concise user view | Actual R008 record | Exact §5.3 output; two expected-result observations explained without extra C weight; one `SIGNAL` and no trace dump |
| Exact values | Fractions such as `1/3` and `11/18`; unavailable states | Exact fractions and literal `UNKNOWN`/`NOT_APPLICABLE`; no decimal, percentage, zero substitution, or `N/A` |
| SIGNAL handling | One and multiple supported vague-term Findings | Literal `SIGNAL`, exact source fragment, source order, and explicit potential-indicator/non-defect wording; U count remains non-cumulative |
| Diagnostic handling | Material diagnostic with and without a candidate span | `Звернути увагу` explains every affected `UNKNOWN`; candidate is explicitly not accepted Evidence; technical details remain audit-only |
| Shared span roles | R004 accepted quantitative Evidence plus acceptance diagnostic | One concise item distinguishes both roles; no conversion of diagnostic to Evidence |
| Completed absence | Complete empty outcome | Short bounded explanation only; no fabricated Evidence or source fragment |
| Evidence concision | Evidence reused across characteristics or already shown in attention | Material source fragment appears once unless repetition is essential for clarity |
| Aggregate counts | Eight-case aggregate and partial-observability cases | Independent exact C/V/U values and all four counts on every line |
| Ordering | Multiple requirements, Findings, diagnostics, and source fragments | Requirement/source order, C/V/U order, and existing source order remain deterministic; no value/risk ranking |
| One disclosure | Empty and nonempty user reports | Exactly one report-level block containing all seven bounded non-claims |
| Readability | Inspect complete user output | No raw dataclass representation, observation/diagnostic indexes, Rule IDs, decision/effect-code dumps, processing-status dump, or repeated full trace blocks |
| Audit discoverability | Run the same input with `--view audit` | Every omitted technical detail remains accessible in the unchanged audit output |
| No new science | Dependency/import review plus manually constructed completed records | User renderer depends on completed domain records only and performs no detection, scoring, aggregation, materiality decision, Finding classification, or Evidence generation |
| Determinism | Render identical inputs repeatedly | Byte-identical output per view |

Passing these tests demonstrates implementation conformance to the approved
presentation contract. It does not by itself constitute broader scientific
validation.

## 9. Researcher approval and implementation record

The researcher approved this package as one decision, recorded in
`docs/model-spec.md` §19.6. The approved package resolves together:

1. `--view {user,audit}` with default `user`;
2. the normative conciseness requirement and exact user layout in §4;
3. the always-visible, conditionally visible, and audit-only boundary;
4. the fixed Ukrainian explanation and attention wording;
5. literal unavailable states and exact fractions;
6. source-attributable `SIGNAL` and explicit non-defect language;
7. separate accepted Evidence, diagnostic candidates, and completed absence;
8. the concise four-count specification summary;
9. exactly one user-level disclosure preserving all seven bounded non-claims;
10. unchanged `ConsoleReporter.render()` as the audit API; and
11. byte-for-byte audit compatibility and single-pipeline guarantees.

The researcher additionally directed production implementation, tests, and
README documentation to be completed in the existing
`feature/dual-view-presentation` branch and existing PR #108. No separate
issue, branch, or pull request is required. This approval changes no
scientific rule and does not authorize merging or closing PR #108.
