# SRM-05A — Existing Quantitative and Acceptance Contract Audit

**Final status: `DRAFT_FOR_RESEARCHER_REVIEW`.**

## 1. Purpose, scope and baseline

This artifact is the first research inventory for SRM-05. It records the
quantitative and acceptance contracts already approved and implemented,
separates them from source-supported concepts that are not operationalized,
and identifies the decisions still required under `RQD-008` and the related
open part of `RQD-006`.

This is not a production implementation, an approval of new detector behavior,
or a claim that all ten topics of Issue #73 are resolved. It introduces no new
rule ID, formula, threshold, tolerance, unit conversion, measurement semantics,
attachment structure, finding conversion, or C/V/U scoring rule.

The supplied baseline is latest `main` after merged PR #90, merge commit
`5cdf73b0165d98aeeb8197252153da4abd254702`. The audit used the repository
state supplied for this task and did not perform Git or GitHub operations.

The classification labels in §5 describe the readiness of each **whole Issue
#73 topic**, not merely whether one narrow subcase exists:

- `APPROVED_AND_IMPLEMENTED`: the relevant bounded contract is scientifically
  approved and represented in production code with directly relevant tests.
- `APPROVED_NOT_IMPLEMENTED`: an executable scientific contract exists, but the
  audited production code does not implement it.
- `PARTIALLY_SPECIFIED`: approved concepts or bounded subcases exist, but the
  topic still lacks a complete executable scientific contract.
- `RESEARCH_DECISION_REQUIRED`: the sources leave a material semantic,
  syntactic, linkage, or representation choice that implementation must not
  make.
- `DEFERRED`: the authoritative contract explicitly places the topic outside
  the current baseline pending later research.

No topic is classified `APPROVED_NOT_IMPLEMENTED` in this audit. Where an
approved general linkage principle depends on a separately approved grammar,
the topic is `PARTIALLY_SPECIFIED` or `RESEARCH_DECISION_REQUIRED`, not an
implementation backlog.

## 2. Authoritative source inventory

### 2.1 Scientific authority

| Source | Authoritative contribution to this audit | Boundary |
| --- | --- | --- |
| [`model-spec.md` §§7.5–7.7](model-spec.md) | Exact Evidence spans and offsets; linked `QuantitativeConstraintObservation`; partial-component policy; stable rule-ID policy. | The conceptual metric/context fields do not by themselves allocate detector grammar. |
| [`model-spec.md` §7.14.5.1](model-spec.md) | Complete `ACCEPT-QUANT-001` result-containment, judgeability, Evidence, ordering, diagnostics, and mixed-state contract. | It approves no broader quantitative grammar or nonnumeric criterion rule. |
| [`model-spec.md` §§7.14.6.1–7.14.6.6](model-spec.md) | Approved comparator meanings, numeric/unit forms, conservative linkage principles, and the exact `QUANT-001`/`QUANT-UK-001` first-production allocation. | Metric/context examples in §7.14.6.5 are traceability examples; the section expressly says they do not allocate production grammar. |
| [`model-spec.md` §§7.15.7–7.15.10](model-spec.md) | Detection outcome states, diagnostics, degraded processing, and the typed quantitative domain representation. | Unresolved processing is not Evidence, a Finding, applicability, confidence, or a score. |
| [`model-spec.md` §7.14.16.4–.6](model-spec.md) | Complete `ACCEPT-UK-001` contract and binding P07–P08/P19–P22 cases, including P21 composition. | Only the conditioned exact-message subset is approved. |
| [`model-spec.md` §§7.15.12 and 18](model-spec.md) | `RQD-008` status is `PARTIALLY APPROVED / OPEN`; it names the remaining quantitative research boundary. | Calculators may consume existing observations, but do not close detector grammar. |
| [`srm-03-structural-rules.md` §§4.4, 6–10](srm-03-structural-rules.md) | Scientific rationale and bounded approval package for `ACCEPT-UK-001`; local-relation and Evidence decisions; P21 as a composition case. | Complex numeric grammar is assigned to SRM-05/06. P21 does not authorize general acceptance grammar. |
| [`srm-04-acceptance-report.md` §§5.3, 7–9, 13–16](srm-04-acceptance-report.md) | Audit evidence and explicit researcher acceptance of the implemented `ACCEPT-UK-001` first slice, including P21 merging and uncertainty preservation. | Researcher acceptance is restricted to the named SRM-04 first slice and excludes broader nonnumeric acceptance and reusable attachment. |

The dissertation-derived material summarized by these sources supports the
scientific relevance of measurable quantities, bounds, units, measurement
conditions, expected behavior, admissible ranges, conditions, and reproducible
criteria. It does not itself define a complete production grammar, comparator
equivalence table, range syntax, unit ontology, conversion policy, or nested
constraint model. Parser output and current Python behavior are implementation
evidence only and cannot supply those missing decisions.

### 2.2 Implementation evidence inspected

The directly relevant production modules are:

- `src/requirements_quality_assessment/detectors/quantitative.py`;
- `src/requirements_quality_assessment/detectors/acceptance_criterion.py`;
- `src/requirements_quality_assessment/domain/quantitative.py`;
- `src/requirements_quality_assessment/domain/detection.py`.

The directly relevant tests inspected are:

- `tests/test_quantitative_detector.py`;
- `tests/test_acceptance_criterion_detector.py`;
- `tests/test_literal_acceptance_criterion_detector.py`.

These files establish what is implemented and regression-covered. They are not
used as scientific authorization for behavior absent from the documents in
§2.1. No tests were run because this is a documentation-only inventory and the
request expressly excludes the full test suite.

## 3. Existing approved quantitative contracts

### 3.1 Approved and implemented rule IDs

| Rule ID | Approved and implemented scope | Principal source |
| --- | --- | --- |
| `QUANT-001` | Symbolic `≤` plus an approved ASCII numeric value, optionally with an approved unit; or an approved value + unit fallback not consumed by a higher-precedence comparator anchor. | model-spec §§7.14.6.6, 7.15.10 |
| `QUANT-UK-001` | Contiguous Ukrainian comparator/value[/unit] anchors for `не довше ніж`, `не довше`, `не більше ніж`, `не більше`, `не нижче`, and `до`. | model-spec §§7.14.6.1, 7.14.6.6 |
| `RESULT-UK-001` | The only accepted expected-result Evidence eligible to govern `ACCEPT-QUANT-001` and `ACCEPT-UK-001`. | model-spec §§7.14.4.1, 7.14.5.1, 7.14.16.4 |
| `COND-UK-001` | The accepted leading condition required by `ACCEPT-UK-001`; it is not a general quantitative-context relation. | model-spec §§7.14.3.1, 7.14.16.4 |

`QUANT-001` and `QUANT-UK-001` create `quantitative_constraint` observations,
not Findings, quality problems, applicability decisions, or scores.

### 3.2 Linked observation and component semantics

The approved and implemented observation is one linked structure with
`metric`, `comparator`, `value`, `unit`, `context`,
`unresolved_components`, and top-level `evidence_refs`. It does not flatten
these roles into unrelated booleans.

The production domain currently provides:

- comparator labels `LESS_THAN_OR_EQUAL`, `GREATER_THAN_OR_EQUAL`,
  `NOT_LESS_FREQUENT`, and `UPPER_BOUND`;
- boundary states `INCLUSIVE` and `UNRESOLVED`;
- unit labels `SECOND`, `MINUTE`, and `PERCENT`;
- exact `Decimal` values, never binary floating point;
- optional `metric` and `context` text components;
- explicit unresolved-component names `METRIC`, `COMPARATOR`, `VALUE`, `UNIT`,
  and `CONTEXT`.

The domain invariant requires a value and either a comparator or a unit for an
accepted quantitative observation. A populated component cannot also be named
unresolved. Top-level Evidence references are the de-duplicated union of the
populated component references. A missing component not listed in
`unresolved_components` means that the accepted anchor did not explicitly
express it; it is not an assertion that the real-world concept is irrelevant.

The first-production detector populates only comparator, value, and unit. It
leaves `metric` and `context` as `None` without marking them unresolved because
it does not attempt their grammar.

### 3.3 Comparator and boundary contract

The exact current mappings are:

| Surface | Normalized comparator | Inclusivity | Production status |
| --- | --- | --- | --- |
| `≤` | `LESS_THAN_OR_EQUAL` | `INCLUSIVE` | Approved and implemented by `QUANT-001`. |
| `не довше ніж`, `не довше` | `LESS_THAN_OR_EQUAL` | `INCLUSIVE` | Approved and implemented for duration anchors by `QUANT-UK-001`. |
| `не більше ніж`, `не більше` | `LESS_THAN_OR_EQUAL` | `INCLUSIVE` | Approved and implemented by `QUANT-UK-001`. |
| `не нижче` | `GREATER_THAN_OR_EQUAL` | `INCLUSIVE` | Approved and implemented by `QUANT-UK-001`. |
| `до` | `UPPER_BOUND` | `UNRESOLVED` | Approved and implemented as a quantitative observation, but not judgeable acceptance. It must not be converted to `<=`. |
| `не рідше` | `NOT_LESS_FREQUENT` | `None` | Domain meaning is approved, but no production observation rule is allocated. The exact written-count construction is protected from fallback detection. |

No mapping is approved for `<`, `>`, `=`, `≥`, `не менше`, `не пізніше`, or
`щонайменше`. Apparent linguistic or mathematical similarity is not approval
of comparator equivalence.

Comparator text is matched on an offset-preserving NFC plus Unicode-casefold
view, with complete-token boundaries and one-or-more Unicode whitespace between
the fixed words. Original text and original Unicode code-point offsets remain
the Evidence. This normalization is matching behavior only; it does not widen
the vocabulary or semantics.

### 3.4 Numeric values and units

The approved first-production numeric forms are ASCII digit integers and one
decimal comma between digits. Decimal-comma source text is converted exactly to
`Decimal` after the raw span is preserved; there is no rounding.

The approved unit surfaces and labels are:

| Surface | Label | Boundary |
| --- | --- | --- |
| `с`, `секунд` | `SECOND` | No generated inflections or implicit aliases. |
| `хв`, `хвилин` | `MINUTE` | No conversion to seconds. |
| `%` | `PERCENT` | No denominator or population is inferred. |

Percent may be adjacent to the value or follow the source-supported space.
Units are labels for approved source forms, not a unit ontology. No implicit
scaling, alias expansion, compound-unit interpretation, or conversion is
authorized.

Decimal-point measured values, signs, exponents, digit grouping, generic
ranges, dates, symbolic variables, and written-out numbers are outside the
first-production allocation. `TLS 1.3` and `OAuth 2.0` are the approved
technical-version negatives; this does not create a general identifier
ontology.

### 3.5 Candidate precedence, Evidence and diagnostics

The approved and implemented candidate precedence is:

1. Ukrainian lexical comparator candidate;
2. symbolic comparator candidate;
3. value + unit fallback.

A contained fallback does not duplicate a higher-precedence comparator anchor.
Distinct anchors remain separate and source ordered. The exact construction
`не рідше одного разу на <approved number> <approved duration unit>` is
protected from the value + unit fallback. It yields no observation, Evidence,
or diagnostic under the current baseline. This is a deliberate deferral, not a
scientific conclusion that the phrase is non-quantitative and not an
interpretation of `одного` as `1`.

Quantitative Evidence is one contiguous accepted anchor with:

- `feature_id = QUANTITATIVE_CONSTRAINT`;
- `rule_id = QUANT-001` or `QUANT-UK-001`;
- stable source-order IDs such as `QUANT-001:E001` and
  `QUANT-UK-001:E001`;
- exact original source text and zero-based, start-inclusive/end-exclusive
  Unicode code-point offsets.

An approved ASCII numeric candidate that has neither an accepted comparator +
value nor value + unit relation, and is not covered by an approved negative
rule, produces diagnostic `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` under
`QUANT-001`. The candidate span is diagnostic only and creates no Evidence,
observation, Finding, confidence, severity, or score.

## 4. Existing approved acceptance contracts

### 4.1 `ACCEPT-QUANT-001`

`ACCEPT-QUANT-001` is approved and implemented as a narrow composition, not a
standalone numeric matcher:

```text
accepted RESULT-UK-001 result Evidence
+ judgeable accepted QUANT-001 / QUANT-UK-001 observation
+ complete containment of all quantitative Evidence in that result span
```

A contained quantitative observation is judgeable only when it has:

1. `LESS_THAN_OR_EQUAL / INCLUSIVE`; or
2. `GREATER_THAN_OR_EQUAL / INCLUSIVE`; or
3. no comparator and an explicit accepted value plus unit inside the accepted
   normative result.

The third case is an explicit normative target, not an inferred equality or
another inferred comparator. `UPPER_BOUND / UNRESOLVED`, including `до`, and
all other comparator meanings are not judgeable under this rule.

The rule produces at most one criterion per accepted result clause even when
that clause contains several qualifying quantitative anchors. Its Evidence is
the complete accepted `RESULT-UK-001` clause, independently recreated in the
acceptance family with `rule_id = ACCEPT-QUANT-001`; it is not the number or
inner bound alone. Proximity does not create linkage, and quantities outside
the result span cannot qualify it.

The approved diagnostics are:

- `ACCEPT_UNRESOLVED_CANDIDATE` for non-judgeable or unresolved quantitative/
  result linkage within the bounded composition;
- `ACCEPT_DEPENDENCY_BLOCKED` when required expected-result analysis cannot
  execute.

### 4.2 `ACCEPT-UK-001`

`ACCEPT-UK-001` is approved, implemented, audited, and explicitly accepted by
the researcher for only this nonnumeric subset:

- one accepted leading `COND-UK-001` condition;
- its approved comma/whitespace partition;
- one accepted `RESULT-UK-001` result occupying the remainder of the hard
  segment;
- exact predicate/object tokens and lemmas `показати` → `повідомлення`, with
  the approved parser-neutral direct-object relation;
- exactly one final non-empty, non-nested Ukrainian guillemet literal `«…»`
  immediately after the object, apart from Unicode whitespace.

It emits independent acceptance Evidence for the exact condition span and the
complete result span, both with `rule_id = ACCEPT-UK-001`. It does not reuse
upstream cross-family IDs or export a general attachment relationship.

The approved diagnostics are:

- `ACCEPT_LITERAL_UNRESOLVED_CANDIDATE` when the bounded source partition,
  predicate/object attachment, literal pairing/nesting, or result boundary
  cannot be resolved;
- `ACCEPT_LITERAL_DEPENDENCY_BLOCKED` when required condition or result
  analysis is blocked or incomplete.

An unconditional exact message, a postposed condition, another verb/object or
quote style, an empty or unquoted output, and a general nonnumeric state are not
accepted by this rule. This bounded negative result does not prove that such a
requirement lacks an acceptance criterion under a future rule.

### 4.3 Quantitative and literal composition

The two acceptance rules execute independently. Neither supplies the other's
scientific justification. Their observations merge only when they identify the
same complete result span; all rule-specific Evidence and diagnostics remain.

P21 is the approved composition example:

```text
Якщо сервіс не відповідає, система повинна не більше ніж за 2 с показати повідомлення «Сервіс недоступний».
```

It produces one merged clause-level acceptance observation with refs in this
exact order:

```text
ACCEPT-UK-001:E001
ACCEPT-QUANT-001:E001
ACCEPT-UK-001:E002
```

P21 proves only that the independently approved quantitative and literal
justifications may coexist on the same result span without duplicate
observations or lost provenance. It does not authorize broader numeric syntax,
semantic attachment, nonnumeric acceptance grammar, or a reusable relation
engine.

### 4.4 Diagnostic and unresolved-processing behavior

The approved and implemented outcome model separates accepted observations
from processing completeness:

| Observations | Processing | Derived detection status | Meaning |
| --- | --- | --- | --- |
| present | `COMPLETE` | `DETECTED` | Accepted observations only. |
| absent | `COMPLETE` | `NOT_DETECTED` | Every applicable approved check completed and this bounded rule found nothing. |
| absent | `INCOMPLETE` | `UNRESOLVED` | Processing could not resolve a candidate/dependency. |
| present | `INCOMPLETE` | `DETECTED` | Accepted observations and unresolved candidates coexist; neither is discarded. |

Diagnostics are not accepted Evidence and do not create Findings,
`QUALITY_PROBLEM`s, applicability, confidence, severity, or scores. Parser
failure or missing required annotations cannot become `NOT_DETECTED` through a
fallback. Downstream calculators must not convert incomplete processing or an
unresolved candidate to zero except through a separately approved calculator
propagation rule.

## 5. Research-gap matrix for Issue #73

| # | Topic and classification | Current documented/implemented contract | Remaining scientific gap | Sources |
| --- | --- | --- | --- | --- |
| 1 | **Metric identification — `PARTIALLY_SPECIFIED`** | `metric` is an approved linked text component. The sources identify examples such as response time, percentile latency, update frequency, route-generation duration, and monthly availability. The first-production detector deliberately leaves `metric=None` and does not infer latency from a duration. | No approved metric vocabulary, nominal-phrase boundary, metric/qualifier decomposition, implicit-metric rule, multiplicity rule, or production grammar exists. A parser noun phrase alone is not authorization. | model-spec §§7.6, 7.14.6.4–.6, 7.15.10; `RQD-008` |
| 2 | **Threshold and comparator semantics — `PARTIALLY_SPECIFIED`** | The exact mappings in §3.3 are approved and implemented. Only `≤` and the six allocated Ukrainian literals enter the first-production matcher. `не рідше` has an approved domain label but no production rule. | Additional symbols/phrases, equivalence classes, negation, metric-dependent direction, equality/target meaning, and the future `не рідше` semantics require explicit approval. No mapping may be inferred from mathematical or linguistic similarity. | model-spec §§7.14.6.1, 7.14.6.6, 7.15.10; `RQD-008` |
| 3 | **Boundary inclusivity — `PARTIALLY_SPECIFIED`** | `LESS_THAN_OR_EQUAL` and `GREATER_THAN_OR_EQUAL` are inclusive. `до` is preserved as `UPPER_BOUND / UNRESOLVED` and is not judgeable acceptance. The domain enforces these combinations. | Inclusivity for `до` and semantics for any future strict/equality/range/frequency comparator are undecided. No tolerance or measurement uncertainty policy is approved. | model-spec §§7.14.5.1, 7.14.6.1, 7.15.10; `RQD-008` |
| 4 | **Numeric values and units — `PARTIALLY_SPECIFIED`** | ASCII integers, one decimal comma, `%`, `с`, `секунд`, `хв`, and `хвилин` are approved and implemented with exact `Decimal`, raw Evidence, and no conversion. Version identifiers are bounded negatives. | Decimal-point measured values, signs, exponent/grouping, aliases, inflections, compound units, dimensional semantics, denominators/populations, unit attachment beyond one phrase, and any conversion policy are unapproved. | model-spec §§7.14.6.2–.3, 7.14.6.6, 7.15.10; `RQD-008` |
| 5 | **Context-dependent constraints — `RESEARCH_DECISION_REQUIRED`** | Quantitative `context` is an approved linked component distinct from general `condition_context`. Sources establish that load, population, scenario, environment, and measurement window can matter. Containment prevents an already separated context-only quantity from becoming an `ACCEPT-QUANT-001` target. | No production context boundary, attachment grammar, multiplicity/cardinality, context-versus-metric decision, or rule for relating one context to one/several bounds is approved. `для 95 % запитів`, `Місячна`, and load limits can have competing roles. | model-spec §§7.6, 7.14.5.1, 7.14.6.4–.6, 7.15.10; `RQD-008` |
| 6 | **Nested and compound constraints — `RESEARCH_DECISION_REQUIRED`** | Distinct baseline anchors remain separate; no merge occurs without an approved range construction. The model permits a context bound to be both context and a separate observation only under a future approved grammar. | Nested-role identity, parent/child representation, compound logical operators, shared metric/context, cardinality, ordering, Evidence linkage, and ambiguous-role behavior are not decided. No new attachment structure is authorized. | model-spec §§7.6, 7.14.6.4–.6, 7.15.10; `RQD-008` |
| 7 | **Ranges and written-out numbers — `DEFERRED`** | Generic range syntax is expressly outside the baseline. Written `одного разу` is not parsed as `1`; the exact deferred frequency phrase is protected from fallback observation and diagnostic. | A future slice must first approve source-attested syntax, numeric normalization, open/closed endpoints, range component representation, frequency-versus-interval semantics, Evidence, and unresolved cases. | model-spec §§7.14.6.2, 7.14.6.5–.6, 7.15.10; `RQD-008` |
| 8 | **Expected-result/acceptance relationships — `PARTIALLY_SPECIFIED`** | `ACCEPT-QUANT-001` requires accepted `RESULT-UK-001` Evidence and complete containment of approved quantitative Evidence. It deduplicates at result-clause level. `ACCEPT-UK-001` uses its separate exact leading-condition/result partition. Both are implemented. | No general relation covers other result rules, cross-clause attachment, partial overlap, external test artifacts, several results, shared bounds, or general criterion sufficiency. Proximity and parser arcs alone remain insufficient. | model-spec §§7.14.5–.5.1, 7.14.16.4; SRM-03 §§4.4, 6; SRM-04 §§5.3, 7–9; `RQD-006`, `RQD-008` |
| 9 | **Non-numeric acceptance criteria — `PARTIALLY_SPECIFIED`** | `ACCEPT-UK-001` approves and implements only a conditioned exact displayed-message oracle. Empty/unquoted outputs and unconditional exact messages are determinate negatives for that rule; malformed/nested literals are unresolved. | Broader observable states, unconditional/postposed cases, other outputs, enumerations, domain rules, usability, procedure adequacy, and a general nonnumeric judgeability test remain open. An expected result is not universally an acceptance criterion. | model-spec §§7.14.5, 7.14.16.4–.6; SRM-03 §4.4; SRM-04 §§5.3, 13–16; `RQD-006` |
| 10 | **Partial or unresolved observations — `APPROVED_AND_IMPLEMENTED`** | Typed partial quantitative components, `unresolved_components`, four outcome combinations, exact diagnostic spans, dependency-blocked behavior, mixed accepted/unresolved state, and Evidence/diagnostic separation are approved and implemented. | Syntax-specific decisions remain with the affected topics: a future rule must state when a candidate is accepted, determinately excluded, component-unresolved, or family-incomplete. The generic mechanism cannot choose those semantics. | model-spec §§7.6, 7.14.5.1, 7.14.6.6, 7.15.7–.10; relevant detector/domain modules and tests |

## 6. Conflicts or ambiguities requiring decisions

1. **Traceability examples versus production authorization.** Model-spec
   §7.14.6.5 describes fully linked metric/context outputs for source cases, but
   immediately states that those entries do not allocate production grammar.
   They are research targets, not unimplemented rules that engineers may fill
   in.

2. **`до` is detected but not judgeable.** The current detector can preserve
   `до 300` as a quantitative observation while its inclusivity remains
   `UNRESOLVED`. `ACCEPT-QUANT-001` must reject it as a pass/fail anchor and
   preserve an acceptance diagnostic when it occurs inside an eligible result.
   Deciding that `до` means inclusive or exclusive is a researcher decision.

3. **Value + unit is a target only in a bounded normative relationship.** A
   comparator-free `2 с` or `95 %` can make an accepted `RESULT-UK-001` clause
   judgeable under `ACCEPT-QUANT-001`; this does not approve a normalized `=`
   comparator, tolerance, or measurement method.

4. **Percent is structurally incomplete for general semantics.** `%` is an
   approved unit label, but the model explicitly forbids inferring an
   unexpressed denominator. Population/metric attachment and percentile versus
   percentage roles require separate decisions.

5. **Frequency meaning depends on representation.** `NOT_LESS_FREQUENT` exists
   in the domain, while the attested `не рідше одного разу на 5 с` is excluded
   from production because its written count and frequency/interval direction
   are not operationalized. The protected negative behavior must not be read as
   scientific rejection of the constraint.

6. **Context may also be a constraint.** A load bound or population qualifier
   may be context for one target, part of a metric, or its own quantitative
   observation. The current sources do not determine decomposition,
   cardinality, or nested identity.

7. **Narrow local composition is not a general attachment model.** Result-span
   containment and the `ACCEPT-UK-001` source partition are two independent,
   bounded relations. P21 demonstrates their coexistence only. It does not
   approve `ATTACH-UK-001`, cross-clause proximity, nearest-anchor selection, or
   exported parser edges.

8. **`NOT_DETECTED` is rule-relative.** Unsupported/deferred forms can complete
   as not detected under the first-production rule. That status means the
   bounded rule found no approved observation; it is not proof that the text
   contains no quantitative or acceptance meaning.

9. **No quantitative observation implies a quality problem.** The quantitative
   and acceptance detectors create observations and diagnostics only. There is
   no authorization to infer a defect, severity, risk, corrective action, or
   new C/V/U contribution from these detections.

## 7. Candidate reference cases for future research

Every case in this section is **`ILLUSTRATIVE_NOT_APPROVED`**. These are
research prompts, not binding tests and not implementation authorization.

| Label | Candidate text | Intended research question |
| --- | --- | --- |
| `ILLUSTRATIVE_NOT_APPROVED` — positive metric | `Час відгуку системи має бути не більше 2 с.` | Can an explicit nominal metric be attached to one existing comparator/value/unit anchor, and what exact Evidence boundary represents it? |
| `ILLUSTRATIVE_NOT_APPROVED` — negative inferred metric | `Система повинна завершити операцію за 2 с.` | Confirm that a duration target does not justify inventing the metric name `час виконання`, even if the acceptance baseline can judge the explicit target. |
| `ILLUSTRATIVE_NOT_APPROVED` — unresolved metric choice | `Час відповіді та час обробки мають бути не більше 2 с.` | Decide whether the bound governs one metric, both metrics, or remains unresolved; proximity must not choose. |
| `ILLUSTRATIVE_NOT_APPROVED` — positive context | `Час відгуку має бути не більше 2 с при 500 одночасних користувачах.` | Define the exact load-context boundary and its linkage to the primary bound. |
| `ILLUSTRATIVE_NOT_APPROVED` — unresolved nested load bound | `Новий маршрут має бути сформований не більше ніж за 4 с при навантаженні до 300 одночасних запитів.` | Decide whether `до 300` is context only, a nested quantitative observation, or both, and how unresolved inclusivity propagates. |
| `ILLUSTRATIVE_NOT_APPROVED` — compound targets | `Затримка має бути не більше 2 с, а доступність — не нижче 99,9 %.` | Define clause/metric ownership and whether two independent linked observations are sufficient without a compound parent. |
| `ILLUSTRATIVE_NOT_APPROVED` — range positive candidate | `Допустимий час відгуку становить від 1 до 2 с.` | Select source-attested range syntax, endpoint meaning/inclusivity, representation, and unit attachment before any detection is approved. |
| `ILLUSTRATIVE_NOT_APPROVED` — range unresolved | `Час відгуку становить 1–2 с.` | Decide whether dash syntax is a range, identifier, or typography variant and what diagnostic span applies when unresolved. |
| `ILLUSTRATIVE_NOT_APPROVED` — written frequency | `Оновлення має виконуватися не рідше одного разу на 5 с.` | Decide the written count, frequency-versus-interval semantics, operator direction, and whether a specific construction can be approved without general written-number parsing. |
| `ILLUSTRATIVE_NOT_APPROVED` — decimal point | `Час відповіді має бути не більше 1.5 с.` | Decide whether decimal-point measured values are admitted and how they are distinguished from approved version negatives without inventing an ontology. |
| `ILLUSTRATIVE_NOT_APPROVED` — nonnumeric positive candidate | `Після невдалої авторизації система повинна відобразити код помилки E401.` | Determine whether an exact unquoted code can be a reproducible oracle and what explicit condition/result grammar is required. |
| `ILLUSTRATIVE_NOT_APPROVED` — nonnumeric negative | `Система повинна показати зрозуміле повідомлення.` | Preserve the boundary that subjective wording alone is not a reproducible oracle. |
| `ILLUSTRATIVE_NOT_APPROVED` — nonnumeric unresolved | `Система повинна показати один із дозволених статусів.` | Decide whether an external enumeration is required, how its absence is represented, and whether the line alone is judgeable. |
| `ILLUSTRATIVE_NOT_APPROVED` — relationship ambiguity | `При 500 користувачах система формує звіт за 2 с і надсилає його за 5 с.` | Decide whether one context governs both results and how two targets attach without nearest-clause guessing. |

Future research may replace, refine, or reject these cases. If any becomes
binding, its approved expected observations, Evidence, diagnostics, ordering,
and exclusions must be recorded in `model-spec.md` through an explicit
researcher decision.

## 8. Prioritized, bounded SRM-05 research slices

### Slice 1 — comparator and scalar syntax closure

Decide only the remaining scalar surface questions: additional comparator
forms, `до` inclusivity policy, decimal-point measured values if any, and exact
negative/ambiguous boundaries. Keep metrics, context, ranges, written numbers,
and acceptance composition outside this slice.

**Dependency:** none beyond the current `QUANT-001`/`QUANT-UK-001` baseline.

### Slice 2 — explicit metric identification and single-bound linkage

Define one bounded Ukrainian construction for an explicitly written metric and
one scalar bound in the same clause. Specify metric boundaries, essential
qualifiers, Evidence refs, multiplicity, false positives, and unresolved
multi-metric cases. Do not infer metrics from units.

**Dependency:** Slice 1 must first stabilize the scalar anchor vocabulary the
metric rule is allowed to link.

### Slice 3 — context and count/population roles

Define a bounded context construction such as an explicit load phrase and
decide count-noun treatment, context boundaries, attachment cardinality, and
the relationship to general `condition_context`. Explicitly decide when a
context bound is also its own quantitative observation.

**Dependency:** Slice 2 must provide stable target identity; this slice must not
invent a reusable attachment object unless a separate domain gate approves one.

### Slice 4 — nested, compound, and range representation

Choose whether parent/child quantitative identity or an additional relation is
required; then define one source-attested range form and one bounded compound
case. Record endpoint inclusivity, units, Evidence, ordering, and unresolved
roles. Keep unit conversion excluded unless separately approved.

**Dependency:** Slices 1–3 must close scalar, metric, and context semantics. A
domain-representation decision is required before production grammar.

### Slice 5 — written-out frequency construction

Evaluate the exact attested `не рідше одного разу на …` construction separately
from general written-number parsing. Decide count normalization, frequency
versus interval meaning, `NOT_LESS_FREQUENT` semantics, Evidence, and
judgeability. Preserve the current protected exclusion until this slice is
approved and implemented.

**Dependency:** Slice 1 comparator decisions and Slice 4 representation choices
where interval/frequency nesting is relevant.

### Slice 6 — acceptance expansion

Only after the quantitative semantics above are stable, decide which new
quantitative observations are judgeable acceptance anchors and whether
`ACCEPT-QUANT-001` remains unchanged or a new rule ID is required under the
stable-ID policy. Separately research one bounded nonnumeric criterion beyond
`ACCEPT-UK-001`; do not combine general nonnumeric judgeability with numeric
syntax work.

**Dependency:** the applicable quantitative slices and a separate `RQD-006`
decision for any new expected-result, condition, or nonnumeric grammar.

## 9. Explicit researcher decision gates

No future slice may proceed to implementation until the researcher explicitly
approves its applicable gates:

1. **Syntax gate:** exact accepted surface forms, token/character boundaries,
   punctuation and Unicode policy, precedence, protected negatives, and hard
   exclusions.
2. **Semantic gate:** normalized comparator meaning, inclusivity, value
   interpretation, unit label, and any metric/context/range/frequency role.
3. **Linkage gate:** exact relation between metric, bound, unit, context,
   expected result, and acceptance criterion; no proximity fallback.
4. **Representation gate:** whether existing components suffice; if not,
   approve identity, cardinality, nesting, ordering, missing endpoints,
   uncertainty, and Evidence references before changing domain structures.
5. **Evidence gate:** exact accepted spans, component and top-level refs,
   rule-local IDs, overlap behavior, repeat ordering, and source round-trip.
6. **Uncertainty gate:** deterministic negatives versus unresolved candidates,
   diagnostic codes/spans, dependency-blocked behavior, and mixed-state
   preservation.
7. **Acceptance gate:** which quantitative forms are judgeable and why;
   whether a comparator-free target is sufficient; how several anchors dedupe;
   and which result rules may govern composition.
8. **Nonnumeric gate:** exact observable oracle, governing condition/result
   grammar, exclusions, and why the behavior is reproducibly judgeable.
9. **Rule-ID gate:** reuse an existing ID only when semantics and Evidence
   boundaries are unchanged; otherwise approve a new ID explicitly. This audit
   proposes none.
10. **Quality-model gate:** any Finding, `QUALITY_PROBLEM`, applicability, or
    C/V/U effect requires separate approval. Feature detection alone supplies
    no such authorization.

## 10. Final status

The repository has a scientifically approved and implemented first-production
quantitative baseline (`QUANT-001`, `QUANT-UK-001`), quantitative acceptance
composition (`ACCEPT-QUANT-001`), and conditioned exact-message acceptance
composition (`ACCEPT-UK-001`), supported by the existing `RESULT-UK-001` and
`COND-UK-001` contracts. Their Evidence, ordering, containment, diagnostics,
and mixed-state behavior are explicit and implemented.

`RQD-008` remains `PARTIALLY APPROVED / OPEN`. General metric identification,
context and count/population linkage, nested/compound representation, written
numbers, ranges, additional comparator and unit semantics, and expansion of
quantitative judgeability require bounded researcher decisions. The broader
nonnumeric acceptance boundary remains open under `RQD-006`.

No implementation, test, dependency, domain, formula, reporter, or scientific
approval record was changed by this inventory.

**Final status: `DRAFT_FOR_RESEARCHER_REVIEW`.**
