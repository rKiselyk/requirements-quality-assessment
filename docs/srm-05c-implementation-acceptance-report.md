# SRM-05C Implementation Acceptance Audit

## 1. Audit result and status

**Final status: `READY_FOR_RESEARCHER_ACCEPTANCE`.**

The bounded `QUANT-METRIC-001` implementation passed the contract,
integration, boundary, Evidence-integrity, and regression gates defined for
this audit. No blocking or non-blocking implementation defect was found within
the approved slice.

This is a technical-readiness result, not researcher acceptance. Acceptance,
if later granted by the researcher, would cover only the bounded
`QUANT-METRIC-001` implementation.

## 2. Audited baseline and exact scope

The task-supplied audited baseline is branch
`docs/srm-05c-implementation-acceptance`, based on `main` after merged PR #95,
with verified merge commit:

```text
51105862d7871057210359dd0bf57acb69ba9081
```

No Git or GitHub operation was performed. The commit identity above is the
verified identity supplied by the audit task; the audit inspected and executed
the repository contents made available in the working directory.

The technical scope was limited to the `QUANT-METRIC-001` implementation and
its direct integration with the existing quantitative, extraction,
acceptance, and condition-context contracts. The authoritative implementation
contract was `docs/model-spec.md` §7.14.6.7, together with §§7.5–7.7 and
§7.15.10. `docs/srm-05c-metric-linkage.md` was used only for research
provenance. Where lifecycle wording or earlier proposals differ, the approved
contract in `model-spec.md` controls.

The audit was read-only with respect to production code, tests, the model
specification, and prior research artifacts. This report is the only file
created.

## 3. Audit method and inspected files

The audit combined:

1. Line-by-line comparison of the approved grammar, binding examples,
   Evidence rules, partial-observation invariants, and deferred boundaries with
   the production implementation.
2. Inspection of the quantitative detector's existing scalar pipeline and the
   bounded enrichment step.
3. Inspection of the extraction-result registry and public extractor path.
4. Inspection of downstream acceptance and condition-context consumers to
   distinguish metric Evidence from unchanged scalar Evidence.
5. Inspection and execution of the directly relevant detector, composition,
   extraction, and integration tests.
6. A repository search for unauthorized metric inference, diagnostics, domain
   types, parser coupling, findings, scoring, or reporter behavior.
7. One complete pytest run after the targeted checks.

The principal files inspected were:

- `docs/model-spec.md` (§§7.5–7.7, 7.14.5.1, 7.14.6.6–7, 7.15.10, and the
  `RQD-008` boundary);
- `docs/srm-05c-metric-linkage.md`;
- `docs/srm-04-acceptance-report.md` as the structural acceptance-report
  example;
- `src/requirements_quality_assessment/detectors/quantitative.py`;
- `src/requirements_quality_assessment/detectors/acceptance_criterion.py`;
- `src/requirements_quality_assessment/detectors/condition_context.py`;
- `src/requirements_quality_assessment/domain/quantitative.py`;
- `src/requirements_quality_assessment/domain/extraction.py`;
- `src/requirements_quality_assessment/extractor.py`;
- `tests/test_quantitative_metric_detector.py`;
- the existing quantitative, acceptance, P21, condition-context, extraction,
  and extractor test files named in §10.

## 4. Rule-by-rule contract traceability

| Approved contract | Implementation evidence | Audit result |
| --- | --- | --- |
| Exact leading `Час<U+0020>відгуку<U+0020>` template, exact case, offset 0 | `_METRIC_TEXT`, `_METRIC_PREFIX`, and `requirement.text.startswith(_METRIC_PREFIX)` require the exact prefix. The eligible scalar Evidence must start at `len(_METRIC_PREFIX)`, which is offset 12. | PASS |
| Existing symbolic `QUANT-001` `≤` anchor only | `_is_eligible_metric_anchor` requires scalar `rule_id == QUANT-001`, `LESS_THAN_OR_EQUAL`, and `INCLUSIVE`. Lexical `QUANT-UK-001` anchors cannot be eligible. | PASS |
| Existing approved numeric syntax and explicit duration unit only | The enrichment consumes observations produced by the unchanged scalar candidate pipeline. It requires populated value and unit with normalized label `SECOND` or `MINUTE`; the existing surfaces remain exactly `с`, `секунд`, `хв`, and `хвилин`. `%` and unitless anchors are rejected. | PASS |
| One metric and one bound in the same hard-bounded clause | The implementation finds the first `.`, `;`, `?`, or `!`, requires exactly one accepted duration bound and one eligible anchor before it, and requires exactly one exact metric surface in that clause. | PASS |
| Enrich exactly one observation; do not create or merge scalar observations | `dataclasses.replace` updates only the selected existing observation. The observation list length and position are preserved; no second scalar observation or attachment object is created. | PASS |
| Preserve scalar fields, component refs, context, and unresolved components | `replace` supplies only `metric` and the new top-level union. Comparator, value, unit, context, unresolved components, and their Evidence references are inherited unchanged. | PASS |
| Separate Evidence ownership | New metric Evidence uses `QUANT-METRIC-001:E001` and `rule_id = QUANT-METRIC-001`; existing scalar Evidence retains its `QUANT-001` ID, text, offsets, and rule ID. | PASS |
| Stable source-ordered top-level union | The enriched observation uses `(metric_id, *observation.evidence_refs)`. For the approved prefix this is metric `[0,11)` followed by scalar `[12,... )`, with no duplicate. The domain union invariant remains active. | PASS |
| Trailing text cannot establish the link | Eligibility depends only on the exact prefix, existing anchor, and same-clause uniqueness. Trailing `500` is neither metric nor context Evidence and remains subject to the scalar baseline diagnostic. | PASS |
| Negative exclusions do not create metric uncertainty | Every ineligible path returns the original Evidence and observations. No metric diagnostic, `METRIC` unresolved component, or processing-status mutation is introduced. | PASS |

## 5. Binding positive and negative case matrix

### Positive and approved duration-unit surfaces

| Input | Verified behavior | Result |
| --- | --- | --- |
| `Час відгуку ≤ 2 с` | One enriched observation; metric `[0,11)` and unchanged scalar `≤ 2 с` `[12,17)` | PASS |
| `Час відгуку ≤ 3 с` | Same exact metric linked to integer/second scalar value `3` | PASS |
| `Час відгуку ≤ 2,5 с` | Raw decimal comma preserved in Evidence; value remains exact `Decimal("2.5")` | PASS |
| `Час відгуку ≤ 2 хв` | Same exact metric linked to approved minute anchor | PASS |
| `Час відгуку ≤ 2 с при 500 одночасних користувачах` | Prefix link preserved; trailing context not attached; baseline diagnostic for `500` preserved | PASS |
| `Час відгуку ≤ 2 секунд` | Additional approved `SECOND` surface linked without changing scalar Evidence | PASS |
| `Час відгуку ≤ 2 хвилин` | Additional approved `MINUTE` surface linked without changing scalar Evidence | PASS |

### Binding negative boundaries

| Boundary | Executed representative | Verified behavior | Result |
| --- | --- | --- | --- |
| Percent unit | `Час відгуку ≤ 95 %` | Scalar remains; no metric Evidence or attachment | PASS |
| Missing unit | `Час відгуку ≤ 2` | Scalar remains; no metric Evidence or attachment | PASS |
| No exact leading metric | `Затримка ≤ 2 с`, `≤ 2 с` | Scalar remains; no inferred metric | PASS |
| Exact casing/spacing | `час відгуку ≤ 2 с`, `Час  відгуку ≤ 2 с`, tab before `≤` | Scalar remains; no metric attachment | PASS |
| Lexical comparator | `Час відгуку не більше 2 с` | `QUANT-UK-001` owns the scalar; metric remains absent | PASS |
| Multiple metrics | `Час відгуку та Час відгуку ≤ 2 с` | Scalar remains unchanged; neither metric phrase is selected | PASS |
| Multiple symbolic bounds | `Час відгуку ≤ 2 с та ≤ 3 с.` | Two scalar observations remain; neither is enriched | PASS |
| Metric-like phrase in another role | `Час відгуку системи ≤ 2 с` | Scalar remains; proximity does not attach the metric | PASS |
| Hard boundary | `Час відгуку. ≤ 2 с` and the equivalent `;`, `?`, `!` cases | Scalar remains; no cross-boundary linkage or diagnostic | PASS |
| Protected technical versions | `TLS 1.3`, `OAuth 2.0` | No observation, Evidence, or diagnostic | PASS |

The scalar regression tests also reconfirmed the existing ASCII integer,
single-decimal-comma, comparator, duration-unit, percent, fallback, unsupported
numeric-form, and unsupported-unit behavior. `QUANT-METRIC-001` did not extend
those surfaces.

## 6. Competing-bound and trailing-context verification

The mandatory mixed competition input was executed:

```text
Час відгуку ≤ 2 с та не більше 3 с.
```

It produced exactly two unchanged scalar observations and Evidence items in
source order:

1. `QUANT-001:E001` for `≤ 2 с`;
2. `QUANT-UK-001:E001` for `не більше 3 с`.

Both observations retained `metric = None`; no metric Evidence and no new
diagnostic were produced. This confirms that a competing lexical duration
bound prevents attachment without deleting, merging, or modifying either
scalar observation.

For the source-attested trailing case, the detector produced one enriched
observation with top-level references
`(QUANT-METRIC-001:E001, QUANT-001:E001)`. The metric and scalar Evidence texts
were exactly `Час відгуку` and `≤ 2 с`. The existing
`QUANT_UNRESOLVED_NUMERIC_CANDIDATE` diagnostic remained owned by `QUANT-001`
for `500` at `[22,25)`, yielding the existing mixed state
`DETECTED / INCOMPLETE`. No context component or metric ambiguity was invented.

## 7. Evidence and extraction-integrity verification

| Integrity gate | Verification | Result |
| --- | --- | --- |
| Exact source text and Unicode offsets | Metric Evidence is sliced at `[0,11)` and scalar Evidence remains at `[12,end)`. The positive tests assert `Requirement.text[start:end] == Evidence.text` for every item. | PASS |
| Rule-local IDs and ownership | Metric ID is `QUANT-METRIC-001:E001`; scalar ID remains `QUANT-001:E001`. Each item uses `QUANTITATIVE_CONSTRAINT` as its feature family. | PASS |
| Component references | Metric component references only metric Evidence. Comparator, value, and unit continue to reference only scalar Evidence. | PASS |
| Top-level union | The observation references metric then scalar Evidence, exactly once each and in source order. `QuantitativeConstraintObservation` independently enforces a de-duplicated component-ref union. | PASS |
| Extraction-result registry | `RequirementExtractionResult` continues to reject duplicate IDs, wrong requirement IDs, out-of-range or non-round-tripping spans, dangling refs, and family mismatches, including every quantitative component ref. | PASS |
| Public path | `Requirement → BaselineFeatureExtractor.extract → RequirementExtractionResult` resolves both metric and scalar refs to same-family Evidence and preserves their source round trips. | PASS |
| Global Evidence order | The extractor's existing offset-based union places `[0,11)` metric Evidence before `[12,17)` scalar Evidence without rebuilding either observation. | PASS |

No NLP object crosses the feature-extraction boundary, and no domain migration
was introduced.

## 8. Acceptance and condition-context regression verification

`ACCEPT-QUANT-001` explicitly recognizes `QUANT-METRIC-001` only as an allowed
component-Evidence owner. It separately filters `QUANT-001` and
`QUANT-UK-001` Evidence into `scalar_sources`, and only those scalar spans are
used for result containment, diagnostic coverage, and acceptance Evidence.
Judgeability still depends exclusively on the unchanged comparator/value/unit
components. The metric therefore cannot broaden containment, make a bound
judgeable, create an acceptance criterion, or affect clause-level
deduplication.

The dedicated integration test confirmed that enriching the observation does
not change acceptance composition. The existing P21 test also passed with one
merged acceptance observation and its unchanged three-reference ordering:
condition support, `ACCEPT-QUANT-001`, and literal-result support. P21 continues
to use its existing lexical scalar semantics; it gains no metric behavior.

The condition-context detector similarly allows the metric Evidence ID to
resolve the complete quantitative observation but builds attachment anchors
only from scalar `QUANT-001`/`QUANT-UK-001` Evidence. The source-attested
`Час відгуку ≤ 2 с при 500 одночасних користувачах` condition test passed and
continued to emit only `COND-UK-001:E001` for
`при 500 одночасних користувачах`. Metric Evidence did not become condition
Evidence or enlarge the scalar attachment span.

## 9. Uncertainty and deferred-boundary audit

No implementation was found for any behavior deferred by §7.14.6.7:

- no general or inferred metric vocabulary;
- no morphology or arbitrary Ukrainian noun-phrase recognition;
- no parser/dependency-based metric attachment;
- no general metric ambiguity diagnostic or competing-candidate span rule;
- no new `METRIC` unresolved-component trigger;
- no context/load/count/population attachment or nested representation;
- no shared-metric, range, multi-bound, or reusable attachment model;
- no new numeric syntax, unit alias, conversion, or written-out-number rule;
- no new domain type or feature family;
- no C/V/U formula or contribution change;
- no new Finding, `QUALITY_PROBLEM`, applicability, confidence, severity,
  risk, or reporter behavior.

The existing `QuantitativeConstraintObservation` and `TextComponent` types are
sufficient for this exact one-metric/one-bound co-residence. `metric = None`
continues to mean no accepted metric expression unless an independently
approved future rule explicitly introduces unresolved metric semantics.

## 10. Test commands and exact results

The first attempted command used the shell's generic Python name:

```text
python -m pytest -q tests/test_quantitative_metric_detector.py tests/test_quantitative_detector.py tests/test_acceptance_criterion_detector.py tests/test_literal_acceptance_criterion_detector.py tests/test_condition_context_detector.py tests/test_extraction_result.py tests/test_extractor_contract.py tests/test_extractor.py
```

It did not execute pytest because `python` was not present on `PATH`; zero tests
were collected. The repository virtual environment was then used. Its first
restricted-sandbox launch was denied before test collection, so the same
read-only command was run with the required process permission:

```text
.\.venv\Scripts\python.exe -m pytest -q tests/test_quantitative_metric_detector.py tests/test_quantitative_detector.py tests/test_acceptance_criterion_detector.py tests/test_literal_acceptance_criterion_detector.py tests/test_condition_context_detector.py tests/test_extraction_result.py tests/test_extractor_contract.py tests/test_extractor.py
```

Result: **235 passed, 0 failed, 0 skipped** in 30.55 seconds.

After the targeted checks, the complete suite was run exactly once:

```text
.\.venv\Scripts\python.exe -m pytest -q
```

Result: **785 passed, 0 failed, 0 skipped** in 63.54 seconds.

The previously reported `785 passed` value was not copied; it was reproduced
by this audit run. No dependency or environment blocker remained after using
the repository virtual environment.

## 11. Findings and blockers

### Findings

No blocking or non-blocking implementation defect was found in the bounded
`QUANT-METRIC-001` implementation.

The audit specifically found no scalar-Evidence mutation, second scalar
observation, dangling or cross-family reference, offset corruption, metric
inference, ambiguity diagnostic, context attachment, acceptance broadening,
condition-attachment broadening, parser coupling, domain expansion, score
change, Finding, or reporter change attributable to this rule.

### Blockers

There are no unresolved blockers to researcher review of this bounded
implementation. The open/deferred `RQD-008` and SRM-05 items listed in §§9 and
13 are intentionally outside this technical gate and remain open.

## 12. Final technical gate decision

All approved contract, binding-case, competition, trailing-context,
Evidence-integrity, public-integration, acceptance-composition,
condition-context, protected-negative, and regression gates passed.

**SRM-05C bounded implementation status:
`READY_FOR_RESEARCHER_ACCEPTANCE`.**

## 13. Researcher acceptance gate and remaining open SRM-05 / RQD-008 work

Technical readiness is not researcher acceptance. This report does not accept
the implementation on behalf of the researcher and does not close issue #73,
`RQD-008`, or SRM-05.

Any later researcher acceptance would cover only the exact
`QUANT-METRIC-001` implementation audited here: the leading `Час відгуку`
metric linked one-to-one to one already accepted symbolic `QUANT-001` `≤`
duration anchor, with the approved Evidence split and exclusions.

Broader `RQD-008` and SRM-05 work remains open, including complex metric and
context grammar, ambiguity handling, count-noun and nested roles, written-out
numbers, generic ranges, shared or multiple bounds, and future frequency
grammar. No new frozen baseline, tag, release, or release authorization is
created by this report.
