# Dual-view CLI presentation contract proposal

- **Status:** `PROPOSED_FOR_RESEARCHER_APPROVAL`
- **Proposal scope:** presentation and CLI selection only
- **Authoritative contract that remains in force unless this proposal is
  approved:** [`model-spec.md` §19](model-spec.md)
- **Scientific input contract:** [`model-spec.md` §7.17](model-spec.md)

## 1. Decision requested

Approve two presentations of the same already-computed
`RequirementAssessmentRecord` and `SpecificationQualityProfile`:

1. `user` — a concise Ukrainian report and the new CLI default; and
2. `audit` — the existing complete formal, trace, Evidence, diagnostic, and
   bounded-coverage report, byte-for-byte unchanged.

The proposed CLI option is exactly:

```text
--view {user,audit}
```

Its default is exactly `user`.

This document proposes an amendment to the approved presentation contract. It
does **not** amend `docs/model-spec.md`, does not claim approval, and does not
authorize implementation. Until a researcher explicitly approves this package
and the decision is recorded in the authoritative model specification, §19
remains the only approved presentation contract and the current
`ConsoleReporter` behavior remains normative.

## 2. Relationship to the approved model

### 2.1 Unchanged scientific boundary

Both views receive the same completed domain values. The pipeline remains:

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

View selection occurs only after assessment and aggregation. Neither renderer
may run a detector, decide applicability, calculate or aggregate a value,
choose a tier, determine diagnostic materiality, create or classify a Finding,
synthesize Evidence, or alter source text. There is one detection path, one
assessment path, one aggregation path, and one Finding path.

The user renderer is a formatting projection over the exact same
`RequirementAssessmentRecord` consumed by the audit renderer. Its Ukrainian
phrases are fixed renderings of existing characteristic IDs, decision codes,
effect codes, states, Findings, Evidence, and diagnostics. They are not a
second scientific interpretation model.

### 2.2 Explicit amendment to §19, not a silent override

If approved, the following interpretation is added to §19:

- the present §19.1–§19.4 contract becomes the normative `audit` view and is
  retained in full;
- the new `user` view is an additional normative projection that may replace
  the detailed formal explanation with the fixed concise Ukrainian templates
  in this proposal;
- the user view may omit raw observation dataclass serialization, tuple
  indexes, raw English `assessment.explanation` and `Finding.explanation`, and
  repeated per-requirement coverage blocks because all remain available in
  `audit`;
- the user view must still expose state, exact value, the applicable rule,
  source text, input disposition, accepted Evidence, unresolved diagnostics,
  completed absence, Findings, and the seven bounded non-claims at the
  granularity specified below; and
- Q1–Q4 and Q6–Q8 retain their scientific meaning. Q5 is extended from one
  canonical detailed layout to two approved layouts over the same record.

The deliberate user-view omissions above are the part of this proposal that
requires researcher approval. They must not be inferred from the existing §19.

## 3. Proposed normative contract

### 3.1 View names and selection

The only accepted view tokens are lowercase `user` and `audit`.

```text
python -m requirements_quality_assessment PATH
    ≡ python -m requirements_quality_assessment --view user PATH

python -m requirements_quality_assessment --view audit PATH
    → existing ConsoleReporter output
```

`argparse` rejects every other view value using its normal invalid-choice
behavior. File-reading errors, UTF-8 handling, stderr text, and exit codes do
not depend on the selected view.

### 3.2 Exact value, state, and ordering rules in both views

Both views must:

- render a computed `Fraction` using its exact reduced string form, such as
  `0`, `1/3`, `1/2`, `11/18`, or `1`;
- render unavailable values using the literal token `UNKNOWN` or
  `NOT_APPLICABLE`; neither may be replaced by `0`, `N/A`, a blank, a decimal,
  or a percentage;
- preserve `Requirement.text` exactly after the reader's approved trimming
  step, including punctuation;
- preserve reader/source requirement order;
- preserve the characteristic order Completeness, Verifiability,
  Unambiguity; the exact user labels are `Повнота`, `Перевірюваність`, and
  `Однозначність`;
- preserve existing Finding/Evidence source order and diagnostic order; and
- place the specification summary after every requirement block, in the same
  C/V/U order.

No view may add a scalar score, combined state, rating, recommendation, risk,
priority, severity, confidence, corrective action, or new scientific rule.

## 4. Exact `user`-view layout

### 4.1 Whole-report grammar

`UserConsoleReporter.render(records, specification_profile)` returns a string
with no trailing newline and this exact section order:

```text
Звіт про якість вимог

<requirement block R001>

<requirement block R002>

...

<specification summary block>

<one bounded-non-claims block>
```

Blocks are separated by one empty line. The CLI's existing `print(...)` adds
the final newline. An empty input contains the title, the specification
summary with three `NOT_APPLICABLE` aggregates and zero counts, and the single
bounded-non-claims block; it contains no requirement block.

### 4.2 Requirement block

Each requirement block has this exact conditional grammar:

```text
Вимога <requirement.id>
Текст: <requirement.text>

Повнота
  Стан: <COMPUTED|UNKNOWN|NOT_APPLICABLE>
  Значення: <exact Fraction|UNKNOWN|NOT_APPLICABLE>
  Правило оцінювання: <assessment_rule_id>              # COMPUTED only
  Керівне правило: <governing_rule_id>                  # otherwise
  Пояснення: <fixed Ukrainian decision template>
  Вхідні дані:
    <input blocks in trace order>
  Знахідки: немає                                       # when empty
  <finding block>                                       # otherwise

Перевірюваність
  ...

Однозначність
  ...
```

The comments above describe conditions and are not output. For a computed
assessment, `Правило оцінювання` renders the authoritative
`assessment_rule_id`; joint record validation guarantees that it equals the
trace's `governing_rule_id`. For `UNKNOWN` or `NOT_APPLICABLE`, no absent
`assessment_rule_id` is invented: `Керівне правило` renders the existing
trace `governing_rule_id`.

### 4.3 Fixed characteristic decision explanations

The user renderer selects exactly one phrase by the already-present
`TraceDecisionCode`:

| Existing decision code | Exact Ukrainian `Пояснення` |
|---|---|
| `C_CRITERION_RATIO_COMPUTED` | `Точне значення Повноти є відношенням кількості виявлених обов'язкових сімейств ознак до трьох; повторні спостереження не додають ваги.` |
| `C_REQUIRED_INPUT_UNRESOLVED` | `Повнота має стан UNKNOWN, тому що принаймні одне обов'язкове сімейство ознак не розв'язане.` |
| `V_FULL_ACCEPTANCE_TIER` | `Прийняте Evidence критерію приймання визначає повний затверджений рівень Перевірюваності.` |
| `V_PARTIAL_LOWER_TIER` | `Критерій приймання завершено відсутністю; прийняте Evidence кількісного обмеження або методу перевірки визначає нижчий затверджений рівень Перевірюваності.` |
| `V_COMPLETED_NO_EVIDENCE_TIER` | `Усі три шляхи Перевірюваності завершено без прийнятого спостереження; отримано затверджений нульовий рівень без створення Evidence відсутності.` |
| `V_MATERIAL_INPUT_UNRESOLVED` | `Перевірюваність має стан UNKNOWN, тому що невирішений істотний кандидат може змінити рівень.` |
| `U_SUPPORTED_SIGNAL_TIER` | `Прийняте входження підтримуваного індикатора дає U=1/2 незалежно від кількості входжень; це SIGNAL, а не підтверджена неоднозначність чи дефект.` |
| `U_COMPLETED_SIGNAL_ABSENCE_TIER` | `Пошук підтримуваного класу сигналів завершено без прийнятого входження; отримано U=1 без створення Evidence відсутності, але не доведено єдиність тлумачення.` |
| `U_MATERIAL_INPUT_UNRESOLVED` | `Однозначність має стан UNKNOWN, тому що невирішена обробка ще може виявити підтримуваний SIGNAL.` |
| `CHARACTERISTIC_NOT_APPLICABLE` | `Назване керівне правило встановило стан NOT_APPLICABLE.` |

These phrases summarize only existing decision codes. They do not translate a
numeric value into a quality judgment.

### 4.4 Input labels and effect explanations

Feature IDs have these fixed user labels:

| Existing `FeatureId` | Exact label |
|---|---|
| `condition_context` | `Умова/контекст` |
| `expected_result` | `Очікуваний результат/реакція` |
| `acceptance_criterion` | `Критерій приймання/виконання` |
| `quantitative_constraint` | `Кількісне обмеження` |
| `verification_method` | `Метод перевірки` |
| `vague_term_occurrence` | `Збіг із підтримуваним словником індикаторів` |

Each `FeatureInputTrace` renders exactly one input block:

```text
    - <fixed feature label>:
      Вплив: <fixed effect phrase>
      <zero or more accepted-Evidence lines>
      <zero or more diagnostic blocks>
      <completed-absence line when and only when applicable>
```

The fixed effect phrases are:

| Existing effect code | Exact Ukrainian phrase |
|---|---|
| `C_PRESENT_1` | `прийняте спостереження; внесок у відношення трьох сімейств дорівнює 1` |
| `C_COMPLETED_ABSENCE_0` | `завершена відсутність; внесок дорівнює 0` |
| `C_REQUIRED_UNRESOLVED` | `невирішений обов'язковий вхід; результат утримано` |
| `V_SELECTS_FULL_TIER` | `прийняте спостереження визначає повний рівень` |
| `V_SELECTS_LOWER_TIER` | `прийняте спостереження визначає нижчий рівень` |
| `V_PRESENT_NONSELECTING` | `прийняте спостереження збережено, але воно не визначає остаточний рівень` |
| `V_COMPLETED_ABSENCE` | `завершена відсутність; прийнятого Evidence для Перевірюваності немає` |
| `V_UNRESOLVED_MATERIAL` | `невирішений істотний кандидат; його розв'язання може змінити рівень` |
| `V_UNRESOLVED_NON_MATERIAL` | `невирішений неістотний для поточного рівня кандидат` |
| `U_SIGNAL_PRESENT` | `прийняте спостереження встановлює підтримуваний рівень SIGNAL` |
| `U_COMPLETED_SIGNAL_ABSENCE` | `завершена відсутність підтримуваного класу SIGNAL` |
| `U_UNRESOLVED_MATERIAL` | `невирішений істотний кандидат; його розв'язання ще може виявити підтримуваний SIGNAL` |

When `V_PRESENT_NONSELECTING` accompanies
`V_MATERIAL_INPUT_UNRESOLVED`, append exactly:

```text
; роль цього Evidence є попередньою, доки невирішений критерій приймання може змінити рівень
```

When `V_UNRESOLVED_NON_MATERIAL` is used, append one of these already-decided
reasons, selected only from the characteristic decision code:

- `V_FULL_ACCEPTANCE_TIER`:
  `; прийнятий критерій приймання вже зафіксував V=1`;
- `V_PARTIAL_LOWER_TIER`:
  `; прийняте Evidence нижчого рівня вже зафіксувало V=1/2`;
- `V_MATERIAL_INPUT_UNRESOLVED`:
  `; цей кандидат не може поліпшити попередній нижчий рівень, але остаточний результат лишається UNKNOWN через невирішений критерій приймання`.

### 4.5 Accepted Evidence, diagnostics, and completed absence

The three concepts must never share a label or be collapsed into one status.

For every Evidence reference of every accepted observation selected by
`observation_indexes`, in observation and reference order, render:

```text
      Прийняте Evidence: <evidence_id> — «<Evidence.text>» [<start_offset>,<end_offset>), правило <Evidence.rule_id>
```

The text and offsets are copied, not normalized or recalculated. This line
means accepted source Evidence. It is never emitted for a diagnostic candidate
or completed absence.

For every diagnostic selected by `diagnostic_indexes`, render:

```text
      Діагностика (не Evidence): <code>; правило <rule_id>
        Кандидат: «<text>» [<start_offset>,<end_offset>)   # span present
        Кандидат: немає                                  # span absent
```

The comments are not output. The user view intentionally omits the current raw
English diagnostic explanation; its materiality is already stated by the
approved effect code and characteristic decision. The audit view retains the
complete diagnostic explanation and exact `DiagnosticSpan` fields.

When and only when the selected outcome is `COMPLETE` and has no accepted
observations, render:

```text
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
```

An input may contain both accepted Evidence and diagnostics. In that mixed
case both are rendered under their distinct labels, and no completed-absence
line is rendered.

### 4.6 Findings

With no Findings, render exactly:

```text
  Знахідки: немає
```

Otherwise render, in existing Finding order:

```text
  Знахідки:
    - Вид: <finding.kind>
      Код: <finding.code>
      Правило: <finding.rule_id>
      Критерій: <finding.criterion_id>                    # non-null only
      Посилання Evidence: <comma-separated evidence_refs|немає>
      Пояснення: <fixed user-facing finding explanation>
      <resolved accepted-Evidence lines>
```

The comment is not output. The only currently approved user-facing Finding
template is:

| Existing Finding contract | Exact Ukrainian explanation |
|---|---|
| `kind=SIGNAL`, `code=VAGUE_TERM_SIGNAL`, `rule_id=FIND-U-VAGUE-001` | `Підтримуваний індикатор потенційної неоднозначності; це SIGNAL, а не підтверджена неоднозначність, дефект, QUALITY_PROBLEM, рівень серйозності, упевненість або ризик.` |

Resolved Finding Evidence uses the same `Прийняте Evidence:` line from §4.5.
`SIGNAL` therefore remains visible as the literal Finding kind and in the
explanation. The renderer may not relabel it as a defect, failure, problem,
risk, warning severity, or recommendation.

### 4.7 Specification summary

The exact summary grammar is:

```text
Підсумок специфікації
Проаналізовано вимог: <number of materialized records>

Повнота
  Стан: <state>
  Значення: <exact Fraction|UNKNOWN|NOT_APPLICABLE>
  Обчислено: <computed_count>
  UNKNOWN: <unknown_count>
  NOT_APPLICABLE: <not_applicable_count>
  Усього: <total_count>
  Правило агрегації: <aggregation_rule_id>

Перевірюваність
  ...

Однозначність
  ...
```

All four counts are unconditional for every characteristic, including an empty
specification and aggregates whose state is `UNKNOWN` or `NOT_APPLICABLE`.
The renderer displays only the supplied aggregate; it does not recompute the
mean or counts.

### 4.8 One report-level bounded-non-claims block

The user view renders this block exactly once, after the specification
summary. It is a faithful concise Ukrainian rendering of all seven canonical
`MVP-V0.1-BOUNDED-CVU-001` disclosures, not a replacement scientific profile:

```text
Межі інтерпретації (MVP-V0.1-BOUNDED-CVU-001)
  1. Покриття обмежене реалізованим обмеженим вилученням шести сімейств ознак і затвердженими правилами C/V/U; це не вичерпний лінгвістичний або семантичний аналіз української мови.
  2. NOT_DETECTED і завершена відсутність означають відсутність прийнятого спостереження за завершеними реалізованими правилами, а не універсальну семантичну відсутність.
  3. Значення C/V, зокрема низькі або нульові, є результатами правил, а не підтвердженими дефектами.
  4. U=1 означає відсутність підтримуваного класу сигналів, а не доказ єдиного тлумачення; U=1/2 означає наявність сигналу, а не підтверджену неоднозначність; чинне правило U не повертає 0.
  5. FIND-U-VAGUE-001 має лише вид SIGNAL; чинна модель не створює QUALITY_PROBLEM, рівень серйозності, упевненість, ризик або коригувальну дію.
  6. R3 і F1-A затверджені дослідником, але не реалізовані й не заявляються як покриття виконання.
  7. Це багатовимірний профіль C/V/U, а не скалярна оцінка вимоги чи прогноз якості програмного продукту.
```

The audit view continues to render the existing canonical disclosures inside
every requirement record exactly as it does now. Moving the user rendering to
one report-level block does not authorize weakening, selecting, or inferring a
different claim.

## 5. DEMONSTRATION — actual known current-main results

**DEMONSTRATION ONLY.** The following values are the actual results from the
eight-requirement run on current `main` including merged PR #107
(`931ef74`). They demonstrate the proposed layout; they do not create new
detector, calculator, aggregation, or validation reference cases.

The eight observed profiles were:

| ID | C | V | U |
|---|---:|---:|---:|
| `R001` | `1` | `1` | `1` |
| `R002` | `1/3` | `0` | `1/2` |
| `R003` | `2/3` | `1` | `1` |
| `R004` | `UNKNOWN` | `UNKNOWN` | `1` |
| `R005` | `UNKNOWN` | `1/2` | `1` |
| `R006` | `1/3` | `0` | `1` |
| `R007` | `1` | `1` | `1` |
| `R008` | `1/3` | `0` | `1/2` |

### 5.1 DEMONSTRATION — R002 user block

```text
Вимога R002
Текст: Система повинна швидко оновити статус.

Повнота
  Стан: COMPUTED
  Значення: 1/3
  Правило оцінювання: CALC-C-MVP-001
  Пояснення: Точне значення Повноти є відношенням кількості виявлених обов'язкових сімейств ознак до трьох; повторні спостереження не додають ваги.
  Вхідні дані:
    - Умова/контекст:
      Вплив: завершена відсутність; внесок дорівнює 0
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
    - Очікуваний результат/реакція:
      Вплив: прийняте спостереження; внесок у відношення трьох сімейств дорівнює 1
      Прийняте Evidence: RESULT-UK-001:E001 — «Система повинна швидко оновити статус» [0,37), правило RESULT-UK-001
    - Критерій приймання/виконання:
      Вплив: завершена відсутність; внесок дорівнює 0
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
  Знахідки: немає

Перевірюваність
  Стан: COMPUTED
  Значення: 0
  Правило оцінювання: CALC-V-MVP-001
  Пояснення: Усі три шляхи Перевірюваності завершено без прийнятого спостереження; отримано затверджений нульовий рівень без створення Evidence відсутності.
  Вхідні дані:
    - Критерій приймання/виконання:
      Вплив: завершена відсутність; прийнятого Evidence для Перевірюваності немає
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
    - Кількісне обмеження:
      Вплив: завершена відсутність; прийнятого Evidence для Перевірюваності немає
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
    - Метод перевірки:
      Вплив: завершена відсутність; прийнятого Evidence для Перевірюваності немає
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
  Знахідки: немає

Однозначність
  Стан: COMPUTED
  Значення: 1/2
  Правило оцінювання: CALC-U-MVP-001
  Пояснення: Прийняте входження підтримуваного індикатора дає U=1/2 незалежно від кількості входжень; це SIGNAL, а не підтверджена неоднозначність чи дефект.
  Вхідні дані:
    - Збіг із підтримуваним словником індикаторів:
      Вплив: прийняте спостереження встановлює підтримуваний рівень SIGNAL
      Прийняте Evidence: UK-VAGUE-001:E001 — «швидко» [16,22), правило UK-VAGUE-001
  Знахідки:
    - Вид: SIGNAL
      Код: VAGUE_TERM_SIGNAL
      Правило: FIND-U-VAGUE-001
      Посилання Evidence: UK-VAGUE-001:E001
      Пояснення: Підтримуваний індикатор потенційної неоднозначності; це SIGNAL, а не підтверджена неоднозначність, дефект, QUALITY_PROBLEM, рівень серйозності, упевненість або ризик.
      Прийняте Evidence: UK-VAGUE-001:E001 — «швидко» [16,22), правило UK-VAGUE-001
```

### 5.2 DEMONSTRATION — R004 user block

This case demonstrates that accepted quantitative Evidence remains visible
while the separate acceptance diagnostic remains explicitly non-Evidence.

```text
Вимога R004
Текст: Система повинна відповісти до 2 с.

Повнота
  Стан: UNKNOWN
  Значення: UNKNOWN
  Керівне правило: CALC-C-MVP-001
  Пояснення: Повнота має стан UNKNOWN, тому що принаймні одне обов'язкове сімейство ознак не розв'язане.
  Вхідні дані:
    - Умова/контекст:
      Вплив: завершена відсутність; внесок дорівнює 0
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
    - Очікуваний результат/реакція:
      Вплив: прийняте спостереження; внесок у відношення трьох сімейств дорівнює 1
      Прийняте Evidence: RESULT-UK-001:E001 — «Система повинна відповісти до 2 с» [0,33), правило RESULT-UK-001
    - Критерій приймання/виконання:
      Вплив: невирішений обов'язковий вхід; результат утримано
      Діагностика (не Evidence): ACCEPT_UNRESOLVED_CANDIDATE; правило ACCEPT-QUANT-001
        Кандидат: «до 2 с» [27,33)
  Знахідки: немає

Перевірюваність
  Стан: UNKNOWN
  Значення: UNKNOWN
  Керівне правило: CALC-V-MVP-001
  Пояснення: Перевірюваність має стан UNKNOWN, тому що невирішений істотний кандидат може змінити рівень.
  Вхідні дані:
    - Критерій приймання/виконання:
      Вплив: невирішений істотний кандидат; його розв'язання може змінити рівень
      Діагностика (не Evidence): ACCEPT_UNRESOLVED_CANDIDATE; правило ACCEPT-QUANT-001
        Кандидат: «до 2 с» [27,33)
    - Кількісне обмеження:
      Вплив: прийняте спостереження збережено, але воно не визначає остаточний рівень; роль цього Evidence є попередньою, доки невирішений критерій приймання може змінити рівень
      Прийняте Evidence: QUANT-UK-001:E001 — «до 2 с» [27,33), правило QUANT-UK-001
    - Метод перевірки:
      Вплив: завершена відсутність; прийнятого Evidence для Перевірюваності немає
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
  Знахідки: немає

Однозначність
  Стан: COMPUTED
  Значення: 1
  Правило оцінювання: CALC-U-MVP-001
  Пояснення: Пошук підтримуваного класу сигналів завершено без прийнятого входження; отримано U=1 без створення Evidence відсутності, але не доведено єдиність тлумачення.
  Вхідні дані:
    - Збіг із підтримуваним словником індикаторів:
      Вплив: завершена відсутність підтримуваного класу SIGNAL
      Завершена відсутність: прийнятого спостереження немає; Evidence відсутності не створено.
  Знахідки: немає
```

### 5.3 DEMONSTRATION — eight-case specification summary

```text
Підсумок специфікації
Проаналізовано вимог: 8

Повнота
  Стан: COMPUTED
  Значення: 11/18
  Обчислено: 6
  UNKNOWN: 2
  NOT_APPLICABLE: 0
  Усього: 8
  Правило агрегації: AGG-MVP-001

Перевірюваність
  Стан: COMPUTED
  Значення: 1/2
  Обчислено: 7
  UNKNOWN: 1
  NOT_APPLICABLE: 0
  Усього: 8
  Правило агрегації: AGG-MVP-001

Однозначність
  Стан: COMPUTED
  Значення: 7/8
  Обчислено: 8
  UNKNOWN: 0
  NOT_APPLICABLE: 0
  Усього: 8
  Правило агрегації: AGG-MVP-001
```

The full user report would append the single §4.8 disclosure block after this
summary. It is omitted from this demonstration snippet only to avoid repeating
the already exact normative text.

## 6. CLI and API compatibility plan

### 6.1 Audit API: exact backward compatibility

`ConsoleReporter.render(requirement_results, specification_profile)` remains
the audit API with:

- the same class name and import path;
- the same signature and accepted record/legacy-tuple inputs;
- the same returned bytes for the same inputs;
- the same formal fields, raw domain rendering, decision/effect trace,
  accepted observations, resolved Evidence, diagnostics, completed-absence
  statements, Findings, human-readable interpretation, per-record seven-item
  coverage disclosure, and specification summary; and
- the same ordering and whitespace.

No existing `ConsoleReporter` call silently changes to user output. The only
default change is at the CLI selection boundary.

### 6.2 New user API

Add a separate public renderer with this proposed API:

```python
class UserConsoleReporter:
    def render(
        self,
        requirement_results: Iterable[RequirementAssessmentRecord],
        specification_profile: SpecificationQualityProfile,
    ) -> str: ...
```

It intentionally requires completed records and has no legacy
`tuple[Requirement, RequirementQualityProfile]` mode because the concise trace,
Evidence/diagnostic distinction, and bounded explanations require §7.17 data.
It does not subclass `ConsoleReporter` and does not call
`ConsoleReporter.render()` and parse its text. Shared pure formatting helpers
may be extracted only when doing so leaves `ConsoleReporter.render()` output
exactly unchanged.

### 6.3 CLI orchestration

The CLI adds one parser argument:

```python
parser.add_argument(
    "--view",
    choices=("user", "audit"),
    default="user",
)
```

After the existing single extraction/assessment pass and single aggregation
pass, orchestration chooses one renderer:

```text
user  → UserConsoleReporter.render(records, specification_profile)
audit → ConsoleReporter.render(records, specification_profile)
```

The records and profile are the same objects whichever view is selected. View
selection may not be passed into the reader, extractor, assessor, calculators,
trace builder, aggregator, or domain models.

The intentional CLI compatibility change is:

- old `python -m requirements_quality_assessment PATH` output becomes the
  Ukrainian user view after approval and implementation;
- old output remains exactly available as
  `python -m requirements_quality_assessment --view audit PATH`; and
- direct callers of `ConsoleReporter.render()` observe no change.

## 7. Test and acceptance matrix for a future implementation

This proposal adds no tests. If approved, a later implementation issue must
cover at least the following matrix.

| Area | Fixture/action | Required acceptance result |
|---|---|---|
| Audit API byte compatibility | Run every existing reporter fixture through `ConsoleReporter.render()` before and after the change | Exact string equality, including whitespace, detailed fields, trace, diagnostic explanations, coverage disclosures, and summary |
| Audit CLI compatibility | Compare the pre-change default CLI output with post-change `--view audit` for the same UTF-8 input | Byte-for-byte stdout equality; same stderr and exit code |
| Audit legacy API | Existing `(Requirement, RequirementQualityProfile)` iterable | Continues to render exactly as before |
| CLI default | Omit `--view` | Output equals explicit `--view user` |
| CLI choices | Use `user`, `audit`, and an invalid token | Both valid tokens select the named view; invalid token is rejected by `argparse` |
| One scientific pass | Spy/count reader, extractor, assessor, trace, and aggregator calls under each view | Same call counts and same record/profile objects; no second detection, assessment, aggregation, or Finding path |
| User R002 SIGNAL | Actual R002 record from §5.1 | Exact user block; `1/3`, `0`, `1/2`; literal `SIGNAL`; exact `швидко` Evidence `[16,22)`; no language that confirms a defect or `QUALITY_PROBLEM` |
| User R004 UNKNOWN | Actual R004 record from §5.2 | C and V each show `Стан: UNKNOWN` and `Значення: UNKNOWN`; no zero substitution; diagnostic is labeled `(не Evidence)`; accepted quantitative Evidence remains separate and provisional |
| User completed absence | Complete empty feature outcome | Exact completed-absence line; no Evidence line synthesized |
| User mixed outcome | One input with accepted observations and diagnostics | Both accepted Evidence and non-Evidence diagnostic render under distinct labels; no completed-absence line |
| User `NOT_APPLICABLE` | Approved empty-specification aggregate now; a requirement record only if a future separately approved governing rule makes that state reachable | Literal `NOT_APPLICABLE` in state and value; never `0` or `N/A`; no non-applicability rule is invented for a test |
| Fractions | Per-requirement and aggregate values including `1/3` and `11/18` | Exact fractions only; no decimal, percentage, or rounding |
| Ordering | Supply records and Findings in approved source order | Requirements, C/V/U, input traces, Findings/Evidence, and summary retain their supplied approved order; no ranking or sorting by value |
| Aggregate visibility | Eight-case profile from §5.3 | Exact `11/18`, `1/2`, `7/8` and all four counts for every characteristic |
| Partial aggregate | `COMPUTED` aggregate with nonzero `unknown_count` and/or `not_applicable_count` | All four counts remain visible beside the exact computed value |
| Empty specification | No records and the approved empty aggregate | Three literal `NOT_APPLICABLE` values; four zero counts for each; no scalar whole-file state |
| Seven non-claims | Any nonempty and empty user report | Exactly one report-level disclosure block containing all seven numbered claims in §4.8; no per-record omission weakens them |
| No prohibited output | Search complete user and audit reports | No scalar score, combined C/V/U result, rating, recommendation, risk, corrective action, invented Finding, or new scientific rule |
| Determinism | Render identical inputs repeatedly | Byte-identical output for each view |

Passing tests show conformance to an approved presentation contract; they do
not constitute researcher approval or scientific validation.

## 8. Researcher approval gate

Implementation is blocked until the researcher explicitly approves or rejects
this package as one decision. Approval must be recorded in
`docs/model-spec.md` as an amendment to §19 and must resolve all of these
points together:

1. `--view {user,audit}` with CLI default `user`;
2. existing `ConsoleReporter.render()` retained unchanged as the audit API;
3. separate `UserConsoleReporter` over completed
   `RequirementAssessmentRecord` values;
4. the exact Ukrainian layout, labels, decision/effect templates, and
   Finding template in §4;
5. exact-Fraction and literal unavailable-state rendering;
6. the explicit accepted Evidence / diagnostic / completed-absence
   distinction;
7. visible `SIGNAL` without confirmed-defect conversion;
8. one report-level user disclosure preserving all seven bounded non-claims;
9. unconditional four-count aggregates and all ordering guarantees; and
10. the audit and CLI compatibility guarantees in §6.

Approval of presentation does not approve production code. A separate scoped
implementation issue and pull request would still be required. Rejection or a
requested change leaves the current §19 and current CLI behavior untouched.

This proposal authorizes no implementation, test modification, commit, push,
pull request, merge, or scientific-model change.
