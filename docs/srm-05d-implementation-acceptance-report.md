# SRM-05D — `QUANT-CONTEXT-001` Implementation Acceptance Audit

## 1. Audit identity and implementation HEAD

**Audit date:** 2026-09-22  
**Issue:** #73 (`SRM-05`)  
**Existing PR:** #100  
**Task-supplied branch:** `docs/srm-05d-c0-scientific-approval`  
**Task-supplied implementation HEAD:**
`e1fab888e3076ef814cdba4009a59d0a645f710a`  
**Audit purpose:** implementation acceptance readiness

The task prohibited Git and GitHub operations. The implementation HEAD above is
therefore the identity supplied for this audit and was not independently queried
with Git. The working-tree implementation, its directly related tests, and the
complete repository test suite were inspected and executed in place.

This report is not researcher acceptance. It does not change the production
lifecycle status, close SRM-05 or `RQD-008`, create a baseline, tag, or release,
or authorize any scientific expansion.

## 2. Authoritative scientific contract

The authoritative contract is `docs/model-spec.md` §7.14.6.8, read together
with:

- §7.14.6.6 for the unchanged `QUANT-001`/`QUANT-UK-001` scalar baseline and
  diagnostic semantics;
- §7.14.6.7 for the accepted `QUANT-METRIC-001` prefix and competition rules;
- §7.15.10 for quantitative component and Evidence invariants; and
- §18, `RQD-008`, for the current partial-approval/open boundary.

The provenance review also included
`docs/srm-05d-c0-approval-proposal.md`,
`docs/srm-05d-quantitative-context-linkage.md`, and
`docs/srm-05c-implementation-acceptance-report.md`. Those documents were used
for traceability; §7.14.6.8 governed every compliance decision.

The approved slice is only the exact terminal suffix
`при 500 одночасних користувачах` after one accepted
`QUANT-METRIC-001` observation containing its approved symbolic `QUANT-001`
duration anchor. The suffix enriches that observation as measurement/load
context. It is not an independent count constraint, equality assertion,
judgeable bound, second observation, or nested relation.

## 3. Files and behavior audited

Production and integrity paths inspected:

- `src/requirements_quality_assessment/detectors/quantitative.py`;
- `src/requirements_quality_assessment/detectors/condition_context.py`;
- `src/requirements_quality_assessment/detectors/postposed_condition.py`;
- `src/requirements_quality_assessment/detectors/acceptance_criterion.py`;
- `src/requirements_quality_assessment/extractor.py`;
- `src/requirements_quality_assessment/domain/quantitative.py`;
- `src/requirements_quality_assessment/domain/extraction.py`; and
- the unchanged calculator, Finding, reporter, and aggregation paths exercised
  by the full suite.

Direct tests inspected:

- `tests/test_quantitative_context_detector.py`;
- `tests/test_quantitative_metric_detector.py`;
- `tests/test_quantitative_detector.py`;
- `tests/test_condition_context_detector.py`;
- `tests/test_postposed_condition_detector.py`;
- `tests/test_acceptance_criterion_detector.py`;
- `tests/test_extraction_result.py`;
- `tests/test_extractor.py`; and
- downstream calculator, assessor, reporter, and aggregation regressions in the
  complete suite.

The implementation is a small post-metric enrichment in the quantitative
detector. It reuses the existing scalar and metric detectors, creates no parser
dependency or general attachment abstraction, and changes no domain type.

## 4. Exact grammar verification

**Gate result: PASS.**

The implementation declares the exact case-sensitive suffix literal:

```text
при 500 одночасних користувачах
```

`_enrich_response_time_context` runs only after
`_enrich_response_time_metric`. It requires exactly one observation whose
metric component resolves to `QUANT-METRIC-001` Evidence, then requires exactly
one `QUANT-001` scalar Evidence owner in that observation. The preceding metric
rule already restricts that scalar to the approved symbolic `≤` duration anchor
and enforces unique metric/bound competition and hard-clause behavior.

The context rule performs an exact equality check between all text after the
accepted scalar Evidence and:

```text
<U+0020>при<U+0020>500<U+0020>одночасних<U+0020>користувачах
```

This single exact-tail comparison enforces:

- exactly one U+0020 SPACE before the suffix and between suffix tokens;
- exact casing and exact population count `500`;
- immediate adjacency to the scalar anchor;
- suffix termination at the end of trimmed `Requirement.text`;
- rejection of final punctuation, intervening text, alternate counts, markers,
  nouns, or whitespace; and
- no context selection by parser relation or proximity.

There is no parser call or fallback in the quantitative-context path. The rule
does not modify scalar or metric candidate generation. Lexical primary
comparators, competing bounds or metrics, hard-boundary separation, and
unsupported scalar forms cannot establish the prerequisite
`QUANT-METRIC-001` observation or cannot satisfy the exact tail.

## 5. Evidence and domain integrity

**Gate result: PASS.**

For the exact source:

```text
Час відгуку ≤ 2 с при 500 одночасних користувачах
```

the audited output contains exactly one quantitative observation and these
accepted quantitative Evidence items:

| Evidence ID | Exact text | Span `[start,end)` | `feature_id` | `rule_id` |
| --- | --- | --- | --- | --- |
| `QUANT-METRIC-001:E001` | `Час відгуку` | `[0,11)` | `QUANTITATIVE_CONSTRAINT` | `QUANT-METRIC-001` |
| `QUANT-001:E001` | `≤ 2 с` | `[12,17)` | `QUANTITATIVE_CONSTRAINT` | `QUANT-001` |
| `QUANT-CONTEXT-001:E001` | `при 500 одночасних користувачах` | `[18,49)` | `QUANTITATIVE_CONSTRAINT` | `QUANT-CONTEXT-001` |

The context component is exactly:

```text
context = TextComponent(
    evidence_refs=(QUANT-CONTEXT-001:E001,)
)
```

The top-level component union is exactly source ordered:

```text
(
    QUANT-METRIC-001:E001,
    QUANT-001:E001,
    QUANT-CONTEXT-001:E001,
)
```

The implementation uses `dataclasses.replace` to enrich the existing immutable
observation in its existing tuple position. It preserves metric, comparator,
value, unit, scalar references, and `unresolved_components`; it does not append
a count observation or introduce a domain type.

`QuantitativeConstraintObservation` validates that top-level references are a
unique de-duplicated component union. `RequirementExtractionResult` validates
unique Evidence IDs, exact source round trips, in-range offsets, non-dangling
references, and feature-family ownership. The public extraction test constructs
the complete result successfully and verifies those invariants. No duplicate
ID, dangling reference, offset corruption, cross-family reference, or second
quantitative observation was found.

## 6. Diagnostic-500 verification

**Gate result: PASS.**

The exact positive retains exactly the pre-existing diagnostic:

```text
code              = QUANT_UNRESOLVED_NUMERIC_CANDIDATE
rule_id           = QUANT-001
candidate span    = [22,25) "500"
processing status = INCOMPLETE
derived status    = DETECTED
```

Context enrichment occurs without altering the original scalar candidate list.
The existing diagnostic pass therefore continues to identify `500` as an
unresolved numeric candidate. The new accepted Evidence covers the complete
context `[18,49)`; there is no accepted Evidence item for the diagnostic-only
`[22,25)` span.

No diagnostic is suppressed, replaced, or reinterpreted. No ambiguity
diagnostic is added. The preserved diagnostic does not create or imply an
independent count constraint.

## 7. Condition-context compatibility

**Gate result: PASS.**

The exact source still produces independent condition-family Evidence:

```text
evidence_id = COND-UK-001:E001
feature_id  = CONDITION_CONTEXT
text        = при 500 одночасних користувачах
span        = [18,49)
```

The quantitative context item has the same text and span but the distinct ID
`QUANT-CONTEXT-001:E001` and feature owner `QUANTITATIVE_CONSTRAINT`. Neither
observation references the other family's Evidence.

The condition consumer's quantitative component-owner allowlist includes
`QUANT-CONTEXT-001`, so a valid enriched observation is not rejected. Its
`scalar_references` selection remains restricted to `QUANT-001` and
`QUANT-UK-001`; context Evidence cannot become a condition attachment anchor.
The focused and full suites cover `COND-UK-001/002` behavior, including the
same-span exact-source case, without regression.

## 8. Acceptance-criterion compatibility

**Gate result: PASS.**

`ACCEPT-QUANT-001` now recognizes `QUANT-CONTEXT-001` only as an allowed
quantitative component Evidence owner. Its scalar-owner set remains exactly
`QUANT-001` and `QUANT-UK-001`.

Containment is evaluated only over those scalar sources. The dedicated
regression supplies accepted result Evidence ending at offset `17` while the
context begins at offset `18`; the acceptance criterion remains detected. This
demonstrates that context Evidence does not enlarge the scalar containment span
or disqualify an already judgeable scalar.

Judgeability still derives from the unchanged observation comparator, value,
and unit. No criterion count, result-span containment, deduplication, merge
order, or existing diagnostic behavior changed. Focused acceptance regressions
and the complete suite passed.

## 9. Public integration and downstream effects

**Gate result: PASS.**

The public `BaselineFeatureExtractor` result for the exact source contains
globally ordered Evidence IDs:

```text
QUANT-METRIC-001:E001
QUANT-001:E001
COND-UK-001:E001
QUANT-CONTEXT-001:E001
```

The same-span condition and quantitative-context items remain distinct and are
deterministically ordered by the existing extractor ordering rule. The
quantitative family remains `INCOMPLETE / DETECTED`, and all accepted component
references resolve to their own feature family.

No `QUANT-CONTEXT-001` behavior was introduced into calculator, Finding,
`QUALITY_PROBLEM`, reporter, or aggregation code. The same quantitative
observation remains present, so Verifiability evidence class and contribution
are unchanged. Completeness continues to consume the independently preserved
condition result; Unambiguity continues to consume only approved vague-term
signals. The full test suite confirms unchanged C/V/U, Finding, reporter, and
aggregation behavior.

## 10. Positive and negative regression matrix

| Contract case | Audit evidence | Result |
| --- | --- | --- |
| Exact source positive | Exact IDs, spans, components, one observation, diagnostic, and mixed status asserted | PASS |
| Approved ASCII integer primary value | `≤ 3 с` composite test | PASS |
| Approved single-decimal-comma primary value | `≤ 2,5 с` composite test | PASS |
| Approved duration units | `с`, `секунд`, `хв`, and `хвилин` composite tests | PASS |
| Missing `500` | No context Evidence; baseline metric/scalar retained | PASS |
| Changed count `600` | No context Evidence; baseline `600` diagnostic retained | PASS |
| Missing or changed population noun | No context Evidence; baseline output asserted | PASS |
| Changed marker | No context Evidence; baseline output asserted | PASS |
| Changed casing | No context Evidence | PASS |
| Changed spacing | Double-space and TAB boundaries reject C0 | PASS |
| Final punctuation | Final period rejects C0 | PASS |
| Hard-boundary separation | Exact-tail and metric hard-boundary behavior reject attachment | PASS |
| Competing metric | No context Evidence and no metric selection by proximity | PASS |
| Competing symbolic bound | No context Evidence; both baseline scalar observations retained | PASS |
| Competing lexical duration bound | No context Evidence; symbolic and lexical observations retained | PASS |
| Additional context phrase | Terminal-suffix requirement fails; no context selection or merge | PASS |
| Lexical primary comparator | `QUANT-UK-001` baseline retained; no metric prerequisite or context | PASS |
| Unsupported primary numeric form | Decimal-point primary form produces no C0 context | PASS |
| Unsupported population forms | `500,5`, `500.0`, `+500`, `1 000`, and `5e2` produce no context | PASS |
| Different source load grammar | Exact literal/end check cannot accept `при навантаженні до 300 одночасних запитів`; broader/nested role remains deferred | PASS |
| Independent count interpretation | No count observation, comparator, unit, Evidence, or nesting code exists | PASS |
| Protected technical versions | `TLS 1.3` and `OAuth 2.0/OIDC` remain no-observation/no-diagnostic negatives | PASS |

A negative C0 result creates no `QUANT-CONTEXT-001` Evidence and no new
ambiguity diagnostic. Existing baseline observations and diagnostics are left
to their already-approved rules.

## 11. Executed tests and actual results

### Environment

```text
Python 3.14.3
pytest 9.1.1
```

### Dedicated context-rule tests

Command:

```text
.\.venv\Scripts\python.exe -m pytest -q tests\test_quantitative_context_detector.py
```

Actual result:

```text
34 passed in 1.79s
```

Failures: 0. Skips: 0.

### Focused quantitative and integration regressions

Command:

```text
.\.venv\Scripts\python.exe -m pytest -q tests\test_quantitative_detector.py tests\test_quantitative_metric_detector.py tests\test_quantitative_context_detector.py tests\test_condition_context_detector.py tests\test_acceptance_criterion_detector.py tests\test_extraction_result.py tests\test_extractor.py
```

Actual result:

```text
232 passed in 15.16s
```

Failures: 0. Skips: 0.

The complete suite below additionally executed the postposed-condition,
domain-contract, C/V/U calculator, assessor, reporter, and aggregation tests.

### Complete repository suite

Command:

```text
.\.venv\Scripts\python.exe -m pytest -q
```

Actual result:

```text
819 passed in 64.57s (0:01:04)
```

Failures: 0. Skips: 0.

These are results reproduced by this audit, not copied from the earlier
implementation report.

## 12. Findings and blockers

### Findings

No blocking or non-blocking implementation defect was found within the bounded
`QUANT-CONTEXT-001` C0 scope.

The audit found no grammar broadening, parser fallback, alternate population
acceptance, second count observation, scalar or metric Evidence mutation,
diagnostic suppression, ambiguity diagnostic, dangling reference, duplicate
Evidence ID, offset corruption, cross-family reference, condition attachment
broadening, acceptance containment broadening, judgeability change, score
change, Finding, `QUALITY_PROBLEM`, reporter, or aggregation change.

The supplied implementation HEAD was not independently read with Git because
the task expressly prohibited Git operations. This identity constraint did not
prevent source inspection or execution of every required test gate and is not a
contract-compliance blocker.

### Blockers

None.

## 13. Final technical audit decision

All exact-grammar, observation/Evidence, diagnostic, condition, acceptance,
public-integration, downstream-compatibility, focused-test, and full-suite gates
passed with no unaddressed violation.

**Final technical audit decision: `READY_FOR_RESEARCHER_ACCEPTANCE`.**

This status means the bounded implementation is technically ready for a
separate explicit researcher decision. It is not implementation acceptance by
the researcher.

## 14. Remaining scientific and release boundaries

The audit does not approve or implement variable population counts, generic
`при` grammar, broader workload vocabulary, context ambiguity handling,
independent count constraints, nested or shared contexts, multiple-bound
attachment, generic numeric ranges, written-out numbers, new units or unit
conversion, parser-based context linkage, new acceptance criteria, changed C/V/U
formulas or contributions, new Findings or risk inference, or reporter or
aggregation changes.

`RQD-008` remains `PARTIALLY_APPROVED / OPEN`. SRM-05 issue #73 remains `OPEN`.
No new baseline, tag, release, or release authorization is created. The
researcher must separately decide whether to accept the implementation. This
audit does not close the broader scientific work or either tracked open item.
