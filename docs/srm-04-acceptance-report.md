# SRM-04 Final Acceptance Audit

## 1. Audit result

**Final status: `READY_FOR_RESEARCHER_ACCEPTANCE`.**

Every SRM-04 implementation gate defined by
[`model-spec.md` §7.14.16.1–7.14.16.7](model-spec.md) passed this audit. No
blocking implementation defect or unresolved first-slice prerequisite was
found.

This status means that the implemented first slice is ready to be presented to
the researcher. It does **not** claim researcher acceptance, issue closure, a
new frozen baseline, a release, or a release tag.

## 2. Audited baseline and scope

The audited baseline is `main` after merged PR #88, identified by the supplied
verified merge commit:

```text
6c96fca9a2ac4b71c7389d5538806bafb339113b
```

The authoritative implementation contract is `docs/model-spec.md`
§7.14.16.1–7.14.16.7. Scientific traceability and decision boundaries were
checked against `docs/srm-03-structural-rules.md`, especially §§4–7 and
decisions D01, D02, D04, D06, D07, and D08.

The audited production scope is exactly:

- `COND-UK-002`, introduced by PR #86;
- `RESULT-UK-002`, introduced by PR #87;
- `ACCEPT-UK-001`, introduced by PR #88.

The audit was read-only with respect to production code. The only artifact
created by the audit is this report.

## 3. Audit method

The audit combined:

1. Contract-by-contract inspection of the three production detectors and their
   extractor integration.
2. Inspection of the parser-neutral domain and extraction-result invariants.
3. Review of every authorized binding case: P01–P04, P07–P08, and P14–P22.
4. Inspection of precedence, candidate ownership, deterministic ordering,
   mixed uncertainty, and cross-rule composition tests.
5. A read-only production-extractor probe of all non-degraded binding inputs.
6. Direct verification of the installed parser and model versions.
7. Execution of the targeted SRM-04A/B/C tests, the frozen MVP acceptance
   tests, and the complete pytest suite.
8. A source search for unauthorized deferred or blocked rule implementations.

P05–P06 and P09–P13 were kept illustrative only and were not treated as
authorization for implementation or as SRM-04 acceptance cases.

## 4. Shared mechanics and domain-boundary traceability

| Approved contract | Audited implementation | Result |
| --- | --- | --- |
| Original trimmed `Requirement.text` and zero-based Unicode code-point `[start,end)` offsets | All new Evidence is sliced directly from `Requirement.text`; `RequirementExtractionResult` independently checks bounds and exact substring equality. | PASS |
| Evidence excludes surrounding whitespace and sentence-final punctuation | The three detectors trim source intervals before constructing Evidence; binding offsets match the model specification exactly. | PASS |
| Stable rule-local IDs in accepted source order | `COND-UK-002:E001…`, `RESULT-UK-002:E001…`, and `ACCEPT-UK-001:E001…` are allocated independently after deterministic source sorting. | PASS |
| Same-rule duplicate spans collapse; independent occurrences survive | Accepted spans use sets keyed by exact source intervals; multi-segment tests preserve source-distinct occurrences and IDs. | PASS |
| Parser annotations remain internal | Evidence contains only exact source spans, feature family, rule ID, and offsets. No token, dependency edge, or parser object escapes the detector boundary. | PASS |
| No fabricated or concatenated quotation | Multi-fragment observations retain separate `evidence_refs`. In particular, `RESULT-UK-002` does not concatenate its anchor and second predicate Evidence. | PASS |
| Same-family reference integrity | All observations reference Evidence from their own feature family. `RequirementExtractionResult` rejects dangling IDs, duplicate IDs, and family mismatches. | PASS |
| No reusable attachment model or domain change | The bounded relations remain detector-local. The six existing feature families and `FeatureObservation.evidence_refs` are reused unchanged. | PASS |

The six feature families remain exactly:

1. condition/context;
2. expected result;
3. acceptance criterion;
4. quantitative constraint;
5. verification method;
6. vague-term occurrence.

## 5. Rule-by-rule contract traceability

### 5.1 `COND-UK-002`

Audited implementation:
`src/requirements_quality_assessment/detectors/postposed_condition.py`.

| Operative requirement | Audit observation | Result |
| --- | --- | --- |
| Exact source shape `<result>, <якщо-clause>` | Candidate discovery requires a comma followed only by Unicode whitespace and a complete-token `якщо` on the approved NFC/casefold view. | PASS |
| Quoted marker exclusion | Well-formed Ukrainian guillemet intervals are excluded from marker candidates; P02 is a completed negative. | PASS |
| One sentence and semicolon segment | Recognition uses parser sentence annotations plus the existing `RESULT-UK-001` semicolon segmentation. | PASS |
| One simple normative prefix | The prefix requires one approved normative surface, one associated subject, one connected infinitive behavior predicate, no coordination, and no negation. | PASS |
| Exact parser graph | Recognition requires `mark(якщо → finite condition head)`, `advcl(condition head → normative chain head)`, and the connected result chain, all locally headed. | PASS |
| Exact suffix projection | Every suffix token must belong to the condition-head subtree; nonpunctuation descendants outside the suffix reject recognition. The delimiter comma is excluded. | PASS |
| Evidence | One `CONDITION_CONTEXT` Evidence contains only the exact condition suffix and uses `rule_id=COND-UK-002`. | PASS |
| Uncertainty | Closed-graph failures produce `COND_POSTPOSED_YAKSHCHO_UNRESOLVED`; missing/incomplete parser data produces `COND_POSTPOSED_YAKSHCHO_PARSER_BLOCKED`; neither path fabricates Evidence. | PASS |
| Precedence and ownership | The extension dispatches before `COND-UK-001`, owns only its exact marker candidate, and prevents duplicate baseline diagnostics while preserving other markers and segments. | PASS |
| Exact boundary | Leading `якщо`, zero-copula/adjectival, multiple, nested, coordinated, nonmodal, quoted, and no-comma forms are not accepted by this rule. | PASS |

### 5.2 `RESULT-UK-002`

Audited implementation:
`src/requirements_quality_assessment/detectors/coordinated_result.py`.

| Operative requirement | Audit observation | Result |
| --- | --- | --- |
| Exact binary grammar | A candidate requires one approved normative surface, one local subject, exactly two lexical predicates, and exactly one source `і` or `та` coordinator. | PASS |
| Active infinitives | Both predicates must be `VERB` with exact `VerbForm=Inf`; passive morphology is excluded. | PASS |
| Closed dependency graph | The first predicate belongs to the normative component; the second is `conj` headed by the first; the coordinator is `cc` headed by the second. | PASS |
| Exclusions | Negation, alternatives, adversatives, extra coordinators/predicates, conditions, separate subjects, orphaning, punctuation boundaries, and nonlocal heads prevent acceptance. | PASS |
| Source coverage | Tokens must cover the exact segment with whitespace-only gaps; incomplete annotations cannot establish a negative. | PASS |
| Three Evidence items | The detector emits the shared anchor, complete first result, and second predicate phrase as three exact `EXPECTED_RESULT` spans. | PASS |
| Two observations | Observation 1 references `(E002)`; observation 2 references `(E001,E003)`. No concatenated source quotation is created. | PASS |
| Ordering | Evidence is sorted by source span and ID; observations are ordered by predicate-bearing Evidence, first result before second. | PASS |
| Uncertainty | Closed-candidate failures use `RESULT_COORD_UNRESOLVED_CANDIDATE`; parser/annotation blocking uses `RESULT_COORD_PARSER_BLOCKED`; accepted results in other segments survive. | PASS |
| Precedence and fall-through | Apparent coordinated candidates are owned before `RESULT-UK-001`; quoted/noun coordination and alternatives fall through without inventing a coordinated result. | PASS |
| Singularity boundary | The rule emits two expected-result observations but makes no independence or singularity judgment. | PASS |

### 5.3 `ACCEPT-UK-001`

Audited implementation:
`src/requirements_quality_assessment/detectors/acceptance_criterion.py`.

| Operative requirement | Audit observation | Result |
| --- | --- | --- |
| Upstream prerequisites | Only accepted `COND-UK-001` and `RESULT-UK-001` Evidence is eligible; `COND-UK-002` and `RESULT-UK-002` cannot satisfy the rule. | PASS |
| Exact local partition | The condition must begin the same original-text hard segment, followed by its comma and whitespace; the accepted result must occupy the remainder excluding terminal punctuation. | PASS |
| Segment-local dependency accounting | Accepted dependencies and incomplete diagnostics are matched to each candidate's own hard segment. Evidence from another segment cannot satisfy or conceal a blocked local dependency. | PASS |
| Exact predicate/object | Source-aligned tokens and lemmas must be exactly `показати` and `повідомлення`; the object must have `dependency_relation=obj` and point to the predicate. | PASS |
| Exact literal | Original text, not parser punctuation reconstruction, supplies one non-empty, non-nested `«…»` literal immediately after the object, allowing only Unicode whitespace. The closing guillemet is the final non-whitespace result character. | PASS |
| Evidence | Each accepted literal criterion emits independent `ACCEPTANCE_CRITERION` Evidence for the condition and complete result, both with `rule_id=ACCEPT-UK-001`. No upstream cross-family ID is reused. | PASS |
| Determinate negatives | No accepted leading condition, an unquoted output, an empty literal, another quote style, or another verb/object produces no literal criterion and remains complete when dependencies are complete. | PASS |
| Uncertainty | Malformed/nested/multiple guillemets, broken object attachment, invalid source partition, and unavailable required annotations are unresolved rather than confirmed absent. Blocked local dependencies use `ACCEPT_LITERAL_DEPENDENCY_BLOCKED`. | PASS |
| Mixed state | Independently accepted criteria survive unrelated unresolved or dependency-blocked candidates, producing `INCOMPLETE / DETECTED`. | PASS |
| Quantitative interaction | Literal and quantitative rules run independently and merge only on the same complete result span. Both Evidence provenances and diagnostics are retained. | PASS |

## 6. Binding-case matrix

| Case | Required audited outcome | Audit evidence | Result |
| --- | --- | --- | --- |
| P01 | One `COND-UK-002` observation; `E001=[32,57)`; complete/detected | Production probe returned exact text `якщо сервіс не відповідає`, rule/family IDs, span, and no diagnostic. Pinned graph test verifies `nsubj`, `xcomp`, `mark`, `advcl`, and comma projection. | PASS |
| P02 | Quoted `якщо` excluded; complete/not detected for extension | Targeted quoted-marker tests returned no `COND-UK-002` Evidence or diagnostic. | PASS |
| P03 | Three `RESULT-UK-002` Evidence items and two observations | Production probe returned `E001=[0,15)`, `E002=[0,30)`, `E003=[33,53)` with refs `(E002)` and `(E001,E003)`. Pinned graph test verifies both infinitives and `nsubj/xcomp/conj/cc`. | PASS |
| P04 | Quoted coordinator creates no coordinated result; baseline fall-through preserved | Targeted pinned negative/fall-through tests pass with no `RESULT-UK-002` Evidence or diagnostic. | PASS |
| P07 | Two literal-rule Evidence items and one criterion | Production probe returned `E001=[0,23)` and `E002=[25,83)` with refs `(E001,E002)`; oracle `[63,83)`, content `[64,82)`. | PASS |
| P08 | Accepted condition/result but no literal criterion; complete/not detected | Targeted binding-negative test returned no acceptance Evidence or diagnostic. | PASS |
| P14 | Missing coordination annotation is blocked, not absent | Controlled pinned-backend degradation returned `RESULT_COORD_PARSER_BLOCKED`, no Evidence, and incomplete/unresolved over `[0,53)`. | PASS |
| P15 | Missing comma prevents `COND-UK-002`; complete/not detected | Targeted mandatory-comma test returned no extension Evidence or diagnostic. | PASS |
| P16 | Multiple governing results prevent `COND-UK-002`; unresolved `[55,80)` | Production probe returned `COND_POSTPOSED_YAKSHCHO_UNRESOLVED` with the exact suffix and no condition Evidence. | PASS |
| P17 | Negated second result is unresolved `[0,57)` | Production probe returned `RESULT_COORD_UNRESOLVED_CANDIDATE` with exact segment text and no result Evidence. | PASS |
| P18 | Alternative coordinator is not accepted; completed extension fall-through | Targeted pinned negative/fall-through test returned no `RESULT-UK-002` Evidence. | PASS |
| P19 | Empty literal is determinately insufficient; complete/not detected | Targeted binding-negative test returned no acceptance Evidence or diagnostic. | PASS |
| P20 | Nested guillemets are unresolved over result `[27,79)` | Production probe returned `ACCEPT_LITERAL_UNRESOLVED_CANDIDATE`, exact result span, and no acceptance Evidence. | PASS |
| P21 | One merged acceptance observation with three exact refs | Production probe and pinned composition test returned the exact Evidence and ordering documented in §7 below. | PASS |
| P22 | Unconditional exact output produces no `ACCEPT-UK-001` contribution | Targeted binding-negative test returned no literal Evidence or diagnostic. | PASS |

P05–P06 were not promoted from illustrative `RESULT-UK-003` examples.
P09–P10 were not promoted from illustrative `VERIFY-UK-002` examples.
P11–P13 were not promoted from illustrative `ATTACH-UK-001` examples.

## 7. P21 composition verification

Input:

```text
Якщо сервіс не відповідає, система повинна не більше ніж за 2 с показати повідомлення «Сервіс недоступний».
```

Verified upstream Evidence:

- `COND-UK-001=[0,25)`;
- `RESULT-UK-001=[27,106)`;
- `QUANT-UK-001=[43,63)`.

Verified acceptance Evidence:

| Evidence ID | Span | Exact text |
| --- | --- | --- |
| `ACCEPT-UK-001:E001` | `[0,25)` | `Якщо сервіс не відповідає` |
| `ACCEPT-QUANT-001:E001` | `[27,106)` | `система повинна не більше ніж за 2 с показати повідомлення «Сервіс недоступний»` |
| `ACCEPT-UK-001:E002` | `[27,106)` | `система повинна не більше ніж за 2 с показати повідомлення «Сервіс недоступний»` |

Exactly one clause-level acceptance observation was emitted with this exact
reference order:

```text
(
  ACCEPT-UK-001:E001,
  ACCEPT-QUANT-001:E001,
  ACCEPT-UK-001:E002
)
```

The oracle is `[86,106)` `«Сервіс недоступний»`; its content is `[87,105)`
`Сервіс недоступний`. The two rules retain independent rule IDs and scientific
justifications while sharing the complete result span. No duplicate
observation is emitted and the quantitative Evidence is not discarded.

## 8. Evidence invariants

The following Evidence gates passed both inspection and execution:

- every accepted Evidence item round-trips exactly through
  `Requirement.text[start_offset:end_offset]`;
- offsets are zero-based Unicode code-point, start-inclusive/end-exclusive;
- Evidence feature family and rule ID match the producing rule;
- evidence IDs are unique within an extraction result;
- observation references resolve to Evidence in the same family;
- deterministic IDs and ordering are stable across repeated runs;
- overlapping source spans are retained when scientifically justified;
- repeated source-distinct occurrences remain separate;
- no parser token, dependency edge, normalized spelling, fabricated text, or
  concatenated fragment is presented as Evidence;
- independent segments do not exchange condition/result dependencies;
- same-rule duplicate spans collapse without merging distinct occurrences.

The extraction-result constructor enforces the bounds, source-round-trip,
unique-ID, resolved-reference, and same-family invariants independently of the
detectors.

## 9. Uncertainty and interaction invariants

Processing and detection status remain orthogonal:

- `COMPLETE` with no observation yields `NOT_DETECTED`;
- `INCOMPLETE` with no observation yields `UNRESOLVED`;
- `INCOMPLETE` with an independently accepted observation remains `DETECTED`.

The audit verified:

- missing parser annotations take parser-blocked or unresolved paths and are
  never repaired or interpreted as confirmed absence;
- source-known candidate spans are preserved in diagnostics where authorized;
- `COND-UK-002` candidate ownership avoids duplicate `COND-UK-001` diagnostics;
- `RESULT-UK-002` candidate ownership avoids partial `RESULT-UK-001` output
  while preserving unrelated accepted results;
- `ACCEPT-UK-001` and `ACCEPT-QUANT-001` retain independent diagnostics and
  Evidence, merging only observations with the same full result span;
- accepted observations survive unresolved candidates in another segment;
- accepted dependencies in one segment cannot satisfy or conceal a blocked
  dependency in another segment;
- unrelated incomplete analysis does not create a spurious literal dependency
  diagnostic for a locally complete candidate.

## 10. Pinned-backend validation

The installed and executed backend versions were independently read as:

```text
spacy==3.8.16
uk-core-news-sm==3.8.0
```

Mandatory fixtures executed for:

- P01: `nsubj`, `xcomp`, `mark`, `advcl`, exact head identities, comma
  attachment/projection, and missing/changed annotations;
- P03/P14: `nsubj`, `xcomp`, `conj`, `cc`, both `VerbForm=Inf` values, exact
  head identities, missing annotations, and more-than-two-predicate exclusion;
- P07/P21: accepted upstream dependencies, exact source partition, normative
  result chain, `obj(повідомлення → показати)`, original-source guillemet
  boundaries, P21 quantitative/literal composition, degraded annotations, and
  condition/result dependency blocking.

The mandatory fixtures call `pytest.fail()` on missing packages, version
mismatch, parse diagnostics, or absent parsed output. They do not use
`pytest.skip()`. The targeted run reported zero skipped tests, confirming that
the mandatory fixtures actually executed.

## 11. Validation commands and exact results

### Targeted SRM-04A/B/C

```powershell
.\.venv\Scripts\pytest.exe -q tests\test_postposed_condition_detector.py tests\test_coordinated_result_detector.py tests\test_literal_acceptance_criterion_detector.py
```

Result:

```text
203 passed, 0 failed, 0 skipped in 71.51s
```

### Frozen MVP v0.1 acceptance regressions

```powershell
.\.venv\Scripts\pytest.exe -q tests\test_mvp_acceptance.py
```

Result:

```text
2 passed, 0 failed, 0 skipped in 7.49s
```

### Complete repository suite

```powershell
.\.venv\Scripts\pytest.exe -q
```

Result:

```text
757 passed, 0 failed, 0 skipped in 120.77s
```

## 12. MVP v0.1 regression and unauthorized-change audit

No unauthorized SRM-04 change was found in the inspected repository state:

- `FeatureId` still contains exactly the six approved feature families.
- `RequirementFeatures` still contains exactly the six corresponding outcomes.
- `RequirementExtractionResult` and `FeatureObservation.evidence_refs` remain
  the approved domain boundary; no relation or attachment object was added.
- `RequirementReader` still reads UTF-8, trims each physical line, ignores
  blank lines, preserves source line numbers/order, and generates processing-
  order IDs.
- Criterion applicability remains the existing
  `APPLICABLE / NOT_APPLICABLE / UNKNOWN` model.
- Completeness, verifiability, and unambiguity remain governed by
  `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` respectively.
- No SRM-04 detector performs score calculation, applicability calculation,
  `QUALITY_PROBLEM` conversion, aggregation, or presentation.
- `ConsoleReporter` still formats completed assessments and performs no
  detection, scoring, or aggregation.
- No singularity field, observation, calculator, or assessment was found.
- The full 757-test suite, including reader, domain, calculator, assessor,
  aggregation, CLI, and reporter regressions, passed without skips.

## 13. Explicit deferred and out-of-scope inventory

| Item | Required status after SRM-04 | Audit result |
| --- | --- | --- |
| `RESULT-UK-003` | `RESEARCH_BLOCKED` | No implementation found; P05–P06 remain illustrative only. |
| `VERIFY-UK-002` | `DEFERRED` | No implementation found; P09–P10 remain illustrative only. |
| `ATTACH-UK-001` | `DEFERRED` | No implementation or reusable attachment structure found; P11–P13 remain illustrative only. |
| Singularity assessment | `DEFERRED` | No singularity implementation or domain representation found. |
| `RQD-006` | `PARTIALLY_APPROVED / OPEN` | Preserved. Only the three bounded first-slice rules are implemented. |

Also remaining outside SRM-04 are general condition attachment, zero-copula or
multiple/nested/coordinated conditions, broader/nonmodal normative force,
passive/finite or greater-than-binary result coordination, general negation and
implicit subjects, unconditional/postposed/broader nonnumeric acceptance,
general verification grammar, actor/action/object extraction, and claims about
complete requirement fulfilment, usability, procedure adequacy, or domain
correctness.

## 14. Findings and unresolved blockers

### Findings

No blocking or non-blocking implementation defect was found within the
authorized SRM-04 first slice.

The audit specifically found no Evidence corruption, cross-family reference,
cross-segment dependency transfer, duplicate P21 acceptance observation,
silent parser fallback, deferred-rule implementation, domain expansion, or
calculation/presentation change.

### Unresolved blockers

There are no unresolved blockers to researcher review of the SRM-04 first
slice. The open/deferred research items in §13 remain intentionally outside the
implemented scope and do not block this bounded acceptance gate.

## 15. Final gate decision

All authorized contract, binding-case, Evidence, interaction, uncertainty,
pinned-backend, regression, and deferred-boundary gates passed.

**SRM-04 implementation status: `READY_FOR_RESEARCHER_ACCEPTANCE`.**

## 16. Researcher acceptance and closeout

The technical audit status is `READY_FOR_RESEARCHER_ACCEPTANCE` for the
implementation baseline `6c96fca9a2ac4b71c7389d5538806bafb339113b`.
This report was published by PR #89 and merged into `main` at verified merge
commit `62f4f08f97310bd8e0601986e570dd7143176fc1`. Publication of the report is
not an explicit researcher-acceptance decision.

The exact accepted scope is limited to:

- `COND-UK-002`;
- `RESULT-UK-002`;
- `ACCEPT-UK-001`.

The report records 203 targeted tests passed with 0 skipped, 2 MVP acceptance
tests passed with 0 skipped, and 757 full-suite tests passed with 0 skipped.
The pinned backend versions `spacy==3.8.16` and `uk-core-news-sm==3.8.0` were
also verified.

The following boundaries remain explicitly outside this acceptance:

- `RESULT-UK-003`: `RESEARCH_BLOCKED`;
- `VERIFY-UK-002`: `DEFERRED`;
- `ATTACH-UK-001`: `DEFERRED`;
- singularity: `DEFERRED`;
- `RQD-006`: `PARTIALLY_APPROVED / OPEN`.

**Researcher decision: `ACCEPTED`.** This explicit researcher decision is
distinct from the earlier technical audit status
`READY_FOR_RESEARCHER_ACCEPTANCE`; it is not inferred from the technical audit
or from the merge of PR #89.

### Researcher-acceptance statement

The researcher explicitly confirmed the following decision:

> Як дослідник, приймаю реалізацію першого зрізу SRM-04 у складі COND-UK-002,
> RESULT-UK-002 та ACCEPT-UK-001 на підставі
> docs/srm-04-acceptance-report.md. Приймання не поширюється на заблоковані або
> відкладені правила та не означає створення нового baseline чи release.

### Manual closeout references

- Issue #71 (`SRM-03`) is the research-decision and authorization basis for
  the bounded contracts. Its closeout remains a manual step and requires
  confirmation that the issue's own acceptance criteria are satisfied.
- Issue #72 (`SRM-04`) covers only the approved SRM-04 first slice listed
  above. Its closeout remains a manual step; it must not be used to imply
  completion or approval of any deferred, blocked, or open boundary.

Neither issue is claimed closed by this report. No baseline tag or release is
created or authorized here.

