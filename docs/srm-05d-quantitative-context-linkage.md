# SRM-05D — Bounded Quantitative Context Linkage Research

**Issue:** #73  
**Research slice:** source-attested quantitative context linkage after the
accepted `QUANT-METRIC-001` prefix  
**Document status:** `DRAFT_FOR_RESEARCHER_REVIEW`

This document is a scientific decision package, not an implementation or an
approval record. The audited sources support treating the exact postposed
phrase `при 500 одночасних користувачах` as the measurement/load context of the
existing response-time observation. They do not support treating `500` as an
independent judgeable count constraint, and they do not allocate production
grammar for either role.

The smallest candidate recommended for researcher review attaches only the
exact source phrase to an already accepted `QUANT-METRIC-001` observation. It
uses a separate quantitative-family Evidence item for the context, preserves
the independent `COND-UK-001` Evidence over the same source span, and preserves
the existing `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` diagnostic for `500`. No Rule
ID is allocated here.

## 1. Purpose and audited baseline

`EXISTING_APPROVED` — The task-supplied protected baseline is `main` after
merged PR #97, verified merge commit
`8a559cbe3546b86ccaf1a76f030c5ab568b59fc9`. The repository was already on
`research/srm-05d-quantitative-context-linkage` at that commit with a clean
working tree before this document was created.

`EXISTING_APPROVED` — `QUANT-METRIC-001` is
`RESEARCHER_APPROVED` and `IMPLEMENTED_AND_ACCEPTED`. Its exact grammar,
Evidence split, scalar component references, deterministic exclusions,
diagnostic preservation, and downstream behavior are protected. This package
does not revise them.

`EXISTING_APPROVED` — `QUANT-001`, `QUANT-UK-001`, `COND-UK-001/002`,
`RESULT-UK-001/002`, `ACCEPT-QUANT-001`, and `ACCEPT-UK-001` remain unchanged.
`RQD-008` remains `PARTIALLY_APPROVED / OPEN`, and SRM-05 issue #73 remains
open.

This document uses the following decision labels:

- `EXISTING_APPROVED`: already authoritative in `model-spec.md`.
- `SOURCE_ATTESTED_NOT_ALLOCATED`: present in the original research material,
  but not allocated as production grammar.
- `PROPOSED_RESEARCH_DECISION`: a bounded candidate requiring explicit
  researcher approval.
- `DEFERRED`: intentionally outside the smallest candidate.
- `UNSUPPORTED_BY_AVAILABLE_SOURCES`: not justified by the audited research
  material.

No production code, tests, domain models, dependencies, formulas, reporter,
prior research artifact, model specification, or GitHub issue is changed by
this package. No pytest, Git mutation, or GitHub operation was performed.

## 2. Source provenance and scientific support

### 2.1 Audited authoritative material

| Source | Evidence used in this package | Classification |
| --- | --- | --- |
| [`model-spec.md` §§7.5–7.7](model-spec.md) | Exact-source Evidence, family ownership, linked partial observation, and stable Rule-ID policy. | `EXISTING_APPROVED` |
| [`model-spec.md` §§7.14.5–7.14.6.7](model-spec.md) | Acceptance containment, quantitative context semantics, conservative linkage, scalar allocation, and protected `QUANT-METRIC-001`. | `EXISTING_APPROVED` |
| [`model-spec.md` §7.15.10](model-spec.md) | `TextComponent`, `context`, unresolved components, and component-union invariants. | `EXISTING_APPROVED` |
| [`model-spec.md` §18, especially `RQD-008`](model-spec.md) | Keeps context/count/nested grammar open after acceptance of the exact metric link. | `EXISTING_APPROVED` |
| [`srm-05-quantitative-research.md`](srm-05-quantitative-research.md) | Identifies context/count/population roles as Slice 3 and separates them from metric linkage and scalar syntax. | `EXISTING_APPROVED` research boundary |
| [`srm-05b-scalar-decisions.md`](srm-05b-scalar-decisions.md) | Freezes existing scalar syntax and rejects unsupported scalar generalization. | `EXISTING_APPROVED` research boundary |
| [`srm-05c-metric-linkage.md`](srm-05c-metric-linkage.md) | Defines the research provenance and exclusions for the exact metric prefix. | `EXISTING_APPROVED` research provenance |
| [`srm-05c-implementation-acceptance-report.md`](srm-05c-implementation-acceptance-report.md) | Confirms accepted production behavior: metric plus scalar refs, no context attachment, and preserved diagnostic for `500`. | `EXISTING_APPROVED` implementation acceptance |
| [`reference/2.2_Взаємозвязок_вимог_і_якості.docx`](reference/2.2_Взаємозвязок_вимог_і_якості.docx) | Directly attests the complete response-time/load example and identifies response time, load, numeric thresholds, load conditions, and units as performance evidence. | `SOURCE_ATTESTED_NOT_ALLOCATED` |
| [`reference/Приклад_застосування_моделі.docx`](reference/Приклад_застосування_моделі.docx) | Attests `при навантаженні до 300 одночасних запитів`, plus the protected scalar and technical-version examples. | `SOURCE_ATTESTED_NOT_ALLOCATED` |
| Relevant domain, detector, extractor, calculator, and test files | Establish current implemented invariants and regression risks; implementation behavior is not scientific authorization. | `EXISTING_APPROVED` as implementation confirmation only |

### 2.2 Original dissertation evidence

`SOURCE_ATTESTED_NOT_ALLOCATED` — The original Section 2.2 source contains the
exact example:

```text
Час відгуку ≤ 2 с при 500 одночасних користувачах
```

The example appears in a semantic-mechanism table and maps the complete
requirement to performance. In the same source, the performance row lists
response time and load among typical requirement evidence and describes early
specification indicators as requirements containing numeric thresholds, load
conditions, and measurement units. The surrounding prose also states that a
requirement containing a numeric threshold, conditions, and a verification
method creates an observable target.

`SOURCE_ATTESTED_NOT_ALLOCATED` — The application example contains:

```text
Після отримання події про перекриття дороги новий маршрут для 95 % запитів
має бути сформований не більше ніж за 4 с при навантаженні до 300 одночасних
запитів.
```

This second source corroborates that a postposed load phrase can qualify a
performance target. It does not justify substituting `запитів` for
`користувачах`, dropping `навантаженні до`, or generalizing either construction
into a Ukrainian context grammar. The application document explicitly marks
its company, requirements, values, model coefficients, risks, and test results
as conditional demonstration material, not calibrated experimental results.

`SOURCE_ATTESTED_NOT_ALLOCATED` — The two original DOCX files were inspected
directly through their native paragraph and table structures, including the
complete relevant rows. The task environment's bundled document runtime did
not include LibreOffice, so a separate visual page render could not be
reproduced. This limits independent pagination/layout verification, not access
to the exact table text used here. No model-generated requirement is treated as
dissertation evidence.

### 2.3 What the sources do and do not establish

The sources establish that:

1. `Час відгуку` is the measured performance quantity;
2. `≤ 2 с` is its scalar response-time bound;
3. `при 500 одночасних користувачах` states the concurrent-user load under
   which that bound is to be observed; and
4. the whole construction belongs to performance semantics.

The sources do not establish:

- a general grammar for phrases headed by `при`;
- a general population or workload noun vocabulary;
- equality semantics for bare counts;
- a `USER` unit or count-dimension ontology;
- decimal-comma population counts;
- whether every context count must also be a separate quantitative
  observation;
- a parent/child identity between a primary target and a nested count; or
- a rule that any nearby count is context for the nearest bound.

## 3. Existing approved contracts and boundaries

| Area | Protected contract | Consequence for SRM-05D |
| --- | --- | --- |
| Metric and scalar | `QUANT-METRIC-001` enriches exactly one existing symbolic `QUANT-001` duration observation. | SRM-05D may only enrich that same observation; it must not reparse or duplicate it. |
| Scalar Evidence | Metric `[0,11)` belongs to `QUANT-METRIC-001`; scalar `[12,17)` belongs to `QUANT-001`. | Both spans, IDs, rules, and component refs remain unchanged. |
| Trailing phrase | Existing production does not interpret or attach it. | Context linkage needs a separate approval and Evidence owner. |
| Diagnostic `500` | `500` at `[22,25)` is `QUANT_UNRESOLVED_NUMERIC_CANDIDATE`, owned by `QUANT-001`. | It cannot disappear merely because a context component is added. |
| Quantitative context | `context: TextComponent | None` is approved as part of one linked observation. | The exact context-only proposal needs no new domain field. |
| General condition/context | `COND-UK-001` already accepts the full phrase `[18,49)`. | Quantitative context must coexist with, not replace or borrow identity from, this family. |
| Evidence integrity | Every ref resolves within one result and matches the referencing feature family. Shared source spans are permitted. | A quantitative component cannot reference a `CONDITION_CONTEXT` Evidence item. |
| Acceptance | Judgeability uses the scalar comparator/value/unit and accepted result containment. Metric enrichment changes neither. | Context enrichment must likewise leave judgeability and scalar containment unchanged. |
| Findings and scores | Quantitative and condition detection alone creates observations/Evidence, not Findings or `QUALITY_PROBLEM`s. | SRM-05D proposes no quality inference or formula change. |

## 4. Meaning of the source-attested context

### 4.1 Distinct possible roles

| Possible role | Interpretation of `при 500 одночасних користувачах` | Finding |
| --- | --- | --- |
| Measurement/execution context | The response-time bound is evaluated while the stated concurrent-user condition holds. | `SOURCE_ATTESTED_NOT_ALLOCATED`; directly supported by the complete requirement and the source's load-condition discussion. |
| Population or workload qualifier | `500 одночасних користувачах` characterizes the workload/population for the response-time measurement. | `SOURCE_ATTESTED_NOT_ALLOCATED`; supported as the internal semantic content of the context phrase. |
| Count-bearing phrase | The phrase contains the explicit ASCII count `500`. | `SOURCE_ATTESTED_NOT_ALLOCATED`; surface fact only. It does not settle normalized count semantics. |
| Separate quantitative constraint | The text independently requires a count equal to, at least, or at most 500 users. | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; no comparator or approved unit states any such independent bound. |
| Nested quantitative role | The same source span is both context of response time and a distinct quantitative observation linked to it. | `DEFERRED`; model-spec permits this only under a separately approved grammar and representation decision. |

### 4.2 Decision among interpretations A–D

`SOURCE_ATTESTED_NOT_ALLOCATED` — Interpretation **A** is the smallest
source-supported reading: an explicit postposed measurement/load context is
attached to the existing response-time bound. The concurrent-user phrase is a
population/workload qualifier inside that context.

`UNSUPPORTED_BY_AVAILABLE_SOURCES` — Interpretation **B**, an independent
count-valued quantitative observation, is not established. The source does not
say `= 500`, `не більше 500`, `не менше 500`, or provide an approved count unit.
Inferring equality from a bare cardinal would introduce new comparator and
measurement semantics.

`DEFERRED` — Interpretation **C**, both context and an independent observation,
requires all decisions needed by B plus explicit nested identity and
traceability. The sources make it scientifically plausible in general but do
not close those decisions for this phrase.

`PROPOSED_RESEARCH_DECISION` — Interpretation **D** applies to production
status, not to the most defensible semantic reading: A is source-attested, but
the detector contract remains an unresolved research candidate until the
researcher allocates exact grammar, Evidence ownership, diagnostic treatment,
and integration behavior.

The phrase must therefore not be described merely as “a number after the
bound.” Its defensible role is the condition under which the response-time
observation is measured; its embedded count remains separately unresolved by
the protected scalar detector.

## 5. Smallest candidate context grammar

### 5.1 Candidate C0 — exact source phrase

`PROPOSED_RESEARCH_DECISION` — The smallest reviewable candidate is:

```text
<one already-accepted QUANT-METRIC-001 observation>
<U+0020>при<U+0020>500<U+0020>одночасних<U+0020>користувачах
<requirement-end>
```

The line wrapping is editorial. The candidate is one contiguous source
construction. The quantitative context span begins immediately after the one
U+0020 SPACE following the accepted scalar anchor. For the source example it is
exactly `[18,49)`.

All of these restrictions are part of C0:

1. The prefix must already satisfy the complete `QUANT-METRIC-001` contract.
   SRM-05D does not recognize the metric, comparator, value, or duration unit
   independently.
2. Exactly one U+0020 SPACE separates the existing scalar anchor from `при`.
3. The marker and population phrase are exactly lowercase
   `при 500 одночасних користувачах`, with one U+0020 SPACE between tokens.
4. The context is postposed, in the same hard-bounded segment, and at the end of
   the trimmed requirement. No intervening comma, parenthesis, conjunction, or
   arbitrary material is admitted.
5. The candidate has exactly one eligible metric, scalar anchor, and context
   phrase. It does not choose among competitors by proximity.
6. Full stop, semicolon, question mark, and exclamation mark cannot be crossed.
   C0 initially requires requirement end because that is the exact attested
   source. A punctuation-terminated variant would be a separate bounded
   approval, although its Evidence should exclude the terminator if approved.
7. Text inside the context does not alter the scalar Evidence boundary and does
   not become a second scalar anchor.
8. Failure to match this exact candidate is a deterministic non-match for the
   proposed rule, not automatically an unresolved quantitative context.

This is an exact postposed source template, not a general `при` rule, not a
nearest-phrase rule, and not parser-driven context attachment.

### 5.2 Primary bound generalization

`EXISTING_APPROVED` — `QUANT-METRIC-001` already generalizes its source seed
over the approved primary scalar values and duration-unit surfaces: ASCII
integer or single decimal comma, and `с`, `секунд`, `хв`, or `хвилин`. SRM-05D
can depend on any already accepted `QUANT-METRIC-001` observation without
inventing scalar semantics.

`PROPOSED_RESEARCH_DECISION` — Applying exact C0 context text after those
already approved metric/scalar variants is scientifically bounded, but the
combined strings are synthetic regression cases rather than dissertation
quotes. The researcher must explicitly approve that compositional reuse.

### 5.3 Population-count generalization

`SOURCE_ATTESTED_NOT_ALLOCATED` — Only count `500` is attested with the exact
marker and noun phrase in C0.

`PROPOSED_RESEARCH_DECISION` — If reuse across population sizes is required, a
larger candidate C1 could replace only `500` with one approved ASCII-integer
surface while keeping `при`, `одночасних користувачах`, spacing, position, and
all other C0 restrictions exact. That abstraction is plausible but is not
authorized merely because integers are accepted in scalar anchors.

`UNSUPPORTED_BY_AVAILABLE_SOURCES` — Reusing the entire existing “approved
numeric form” set would admit decimal-comma user counts. The audited sources do
not justify fractional concurrent-user cardinality. C1 must therefore not
inherit decimal-comma syntax automatically.

`DEFERRED` — Different markers, population nouns, number morphology, count
units, load introductions, optional words, punctuation, case variation,
Unicode-whitespace variation, and parser attachment remain outside C0 and C1.

## 6. Exact Evidence and component alternatives

### 6.1 Verified source offsets

The exact requirement has 49 Unicode code points. Direct slicing verifies:

| Role | Exact text | Span `[start,end)` | Current/proposed owner |
| --- | --- | --- | --- |
| Metric | `Час відгуку` | `[0,11)` | `QUANT-METRIC-001` — unchanged |
| Scalar | `≤ 2 с` | `[12,17)` | `QUANT-001` — unchanged |
| Candidate quantitative context | `при 500 одночасних користувачах` | `[18,49)` | future separately approved quantitative-context rule; no ID allocated here |
| Embedded unresolved numeric candidate | `500` | `[22,25)` | `QUANT-001` diagnostic — unchanged under the recommended treatment |

Every accepted Evidence item must preserve the exact substring and offsets of
the trimmed original requirement.

### 6.2 Evidence ownership alternatives

| Alternative | Integrity assessment | Decision |
| --- | --- | --- |
| Reuse `COND-UK-001:E001` inside `QuantitativeConstraintObservation.context` | Invalid. That Evidence has `feature_id = CONDITION_CONTEXT`, while every quantitative component ref must resolve to `QUANTITATIVE_CONSTRAINT`. It would violate `RequirementExtractionResult` family ownership. | Rejected. |
| Create separate quantitative-context Evidence for the same `[18,49)` span | Valid. Shared spans are permitted, IDs remain unique, and each family owns its own semantic observation. | `PROPOSED_RESEARCH_DECISION`; recommended. |
| Enlarge scalar Evidence to include the context | Invalid for this slice. It changes protected `QUANT-001` Evidence, scalar component refs, and `QUANT-METRIC-001` behavior. | Rejected. |
| Reuse `QUANT-METRIC-001` as the context owner | Incompatible with its immutable approved meaning and Evidence boundary. Context recognition is a material semantic change. | Rejected. |
| Add a relation/attachment domain object | Unnecessary for one context component on one existing observation. | `DEFERRED` unless nested or shared-role research proves it necessary. |

Shared source span does not mean shared Evidence identity. Under the recommended
alternative, `COND-UK-001:E001` and a future quantitative-context Evidence item
have identical text and offsets but different IDs, feature families, and rule
provenance.

### 6.3 Proposed quantitative observation

Using documentation placeholders only, the C0 result would be:

```text
metric.evidence_refs     = (QUANT-METRIC-001:E001,)
comparator.evidence_refs = (QUANT-001:E001,)
value.evidence_refs      = (QUANT-001:E001,)
unit.evidence_refs       = (QUANT-001:E001,)
context.evidence_refs    = (<QUANTITATIVE_CONTEXT_EVIDENCE_ID>,)
unresolved_components    = ()

evidence_refs = (
    QUANT-METRIC-001:E001,
    QUANT-001:E001,
    <QUANTITATIVE_CONTEXT_EVIDENCE_ID>,
)
```

`PROPOSED_RESEARCH_DECISION` — The top-level references are the de-duplicated
component union in source order: metric, scalar, context. The proposed context
Evidence has `feature_id = QUANTITATIVE_CONSTRAINT`, exact span `[18,49)`, and
a future researcher-approved rule identity. The placeholder above is not an ID
allocation.

`EXISTING_APPROVED` — The scalar comparator remains
`LESS_THAN_OR_EQUAL / INCLUSIVE`, value remains `Decimal("2")`, unit remains
`SECOND`, and all their refs remain `QUANT-001:E001`.

## 7. `COND-UK` and quantitative-context coexistence

`EXISTING_APPROVED` — For the exact source, `COND-UK-001` independently emits:

```text
Evidence ID: COND-UK-001:E001
feature_id: CONDITION_CONTEXT
text: при 500 одночасних користувачах
span: [18,49)
processing: COMPLETE
derived status: DETECTED
```

`PROPOSED_RESEARCH_DECISION` — C0 must preserve that result exactly and add a
separate quantitative-family Evidence item over the same span. The two
observations answer different questions:

- `COND-UK-001`: does the requirement express a general condition/context?
- quantitative context: under which workload/population does this particular
  linked response-time observation apply?

Neither family should consume, replace, or deduplicate the other's Evidence.
Global `RequirementExtractionResult.evidence` may contain both same-span items
because identity and family differ. The quantitative observation may reference
only its quantitative-family item.

`PROPOSED_RESEARCH_DECISION` — Existing implementation has a compatibility
risk that must be handled in any later implementation: the condition detector
currently validates complete quantitative observations against an allowlist of
`QUANT-001`, `QUANT-UK-001`, and `QUANT-METRIC-001` Evidence owners before it
extracts scalar attachment spans. A future context Evidence owner would make
the enriched observation fail that allowlist unless compatibility is updated.
The required scientific outcome is no change to `COND-UK-001/002`: recognize
the new quantitative Evidence owner as an allowed component while continuing
to use only unchanged scalar Evidence as the attachment anchor.

This compatibility work is not permission to broaden `COND-UK-001`, export a
cross-family reference, or add a reusable attachment model.

## 8. The `500` diagnostic decision

### 8.1 Decision alternatives

| Option | Quantitative observation and Evidence | Family processing/status | Diagnostic ownership | Scientific consequence |
| --- | --- | --- | --- | --- |
| **A. Preserve the diagnostic** | Add accepted context `TextComponent` and context Evidence; do not add a second observation. | `INCOMPLETE`; derived `DETECTED` because the primary observation remains present. | Existing `QUANT-001` diagnostic over `[22,25)` remains. | Context role is accepted while the embedded count's independent quantitative role remains unresolved. No judgeability is added. |
| **B. Resolve the numeric candidate as accepted context content** | Same context component; no separate count observation. | `COMPLETE / DETECTED` if no other diagnostic exists. | The `QUANT-001` diagnostic would be explicitly suppressed or removed under a new approved accounting rule. | Could mean only that `500` is deterministically accounted for inside context; it must not imply equality or an independently judgeable count. Requires a separate scientific change to diagnostic behavior. |
| **C. Create a separate quantitative observation** | Primary observation gains context; a second observation represents a count bound. | Depends on the new count contract; potentially `COMPLETE / DETECTED`. | Existing diagnostic would be replaced only after the second observation is validly accepted. | Current domain cannot accept value-only `500`; comparator, count unit, nesting, and linkage would have to be approved. Not ready. |
| **D. Introduce a different unresolved state** | Primary context may be accepted while a new context/count-specific diagnostic records unresolved nested role. | `INCOMPLETE / DETECTED`. | A new future rule would own a new diagnostic; the old diagnostic could change only by explicit decision. | More expressive but unnecessary for C0 and requires code, span, cardinality, and propagation decisions. |

### 8.2 Recommended treatment

`PROPOSED_RESEARCH_DECISION` — Choose **A** for the first bounded context slice.
Preserve exactly:

```text
code = QUANT_UNRESOLVED_NUMERIC_CANDIDATE
rule_id = QUANT-001
candidate span = [22,25) "500"
processing_status = INCOMPLETE
derived status = DETECTED
```

The accepted quantitative context Evidence is the complete `[18,49)` phrase;
the diagnostic span remains diagnostic only and does not enter component refs
or `RequirementExtractionResult.evidence`. One source region can support an
accepted context role while the narrower numeric candidate retains an
unresolved independent role. This is not contradictory: C0 links text as
context but does not normalize the embedded count as a comparator/value/unit
constraint.

`EXISTING_APPROVED` — The existing accepted metric and scalar Evidence and
components remain unchanged. `500` still creates no accepted Evidence or
independent observation. No diagnostic is silently deleted or suppressed.

`DEFERRED` — Option B may be reviewed later as a separate scientific gate if
the researcher decides that an accepted context deterministically accounts for
its embedded count. Such approval must state explicitly that diagnostic
suppression does not make the count an acceptance criterion. Options C and D
belong to nested/count-role research.

## 9. Positive, negative, unresolved, and deferred case matrix

Every classification in this matrix is provisional. “Future disposition”
means the result expected **if C0 and its stated exclusions are approved**; it
is not a binding test or implementation authorization.

| Case | Candidate text or interpretation | Evidence status | Future disposition under C0 | Reason |
| --- | --- | --- | --- | --- |
| Exact source-attested positive | `Час відгуку ≤ 2 с при 500 одночасних користувачах` | `SOURCE_ATTESTED` | Binding positive | Exact accepted prefix plus exact C0 suffix; context `[18,49)`. |
| Alternative approved response-time value | `Час відгуку ≤ 3 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding positive | Prefix variation is already approved by `QUANT-METRIC-001`; context remains exact. |
| Alternative approved duration unit | `Час відгуку ≤ 2 хв при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding positive | Minute prefix is existing approved behavior; context remains exact. |
| Decimal comma in primary response time | `Час відгуку ≤ 2,5 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding positive | Existing approved scalar semantics apply only to the primary bound. |
| Missing population count | `Час відгуку ≤ 2 с при одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding negative | Does not match exact C0; no quantitative context Evidence. |
| Missing population noun | `Час відгуку ≤ 2 с при 500` | `SYNTHETIC_TEST_CASE` | Binding negative | Count alone does not establish the attested workload phrase. |
| Altered population noun | `Час відгуку ≤ 2 с при 500 одночасних клієнтах` | `SYNTHETIC_TEST_CASE` | Binding negative | No vocabulary or synonym expansion is approved. |
| Different context marker | `Час відгуку ≤ 2 с за 500 одночасних користувачів` | `SYNTHETIC_TEST_CASE` | Binding negative | Only exact postposed `при` is considered. |
| Source-attested different load grammar | `... при навантаженні до 300 одночасних запитів` | `SOURCE_ATTESTED` | Deferred | It has a different marker-headed structure, comparator, noun, and possible nested role. |
| Hard-boundary separation | `Час відгуку ≤ 2 с. при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding negative | Context cannot cross `.`, `;`, `?`, or `!`. |
| A second metric | `Час відгуку та Час обробки ≤ 2 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding negative | Protected metric contract is inapplicable; no proximity selection. |
| A second competing bound | `Час відгуку ≤ 2 с та ≤ 3 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding negative | `QUANT-METRIC-001` itself refuses a competing scalar bound. |
| More than one plausible context phrase | `Час відгуку ≤ 2 с при 500 одночасних користувачах при піковому навантаженні` | `SYNTHETIC_TEST_CASE` | Binding negative for C0; broader case deferred | Exact suffix/end boundary fails; C0 does not choose or merge contexts. |
| Context belongs to a different result | `Час відгуку ≤ 2 с, а звіт формується при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding negative | Adjacency/proximity cannot override result ownership; broader result attachment is deferred. |
| Lexical comparator instead of exact metric template | `Час відгуку не більше 2 с при 500 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding negative | `QUANT-METRIC-001` does not link lexical `QUANT-UK-001` anchors. |
| Alternative population count | `Час відгуку ≤ 2 с при 600 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Binding negative under C0; candidate C1 deferred | Only exact `500` is source-attested in this syntax. |
| Decimal-comma population count | `Час відгуку ≤ 2 с при 500,5 одночасних користувачах` | `UNSUPPORTED_BY_AVAILABLE_SOURCES` | Binding negative | Existing decimal-comma measurement syntax does not justify fractional user cardinality. |
| Other unsupported population numeric forms | `+500`, `1 000`, `5e2`, or `500.0` in the C0 count position | `UNSUPPORTED_BY_AVAILABLE_SOURCES` | Binding negative | No sign, grouping, exponent, or decimal-point count grammar is approved. |
| Count interpreted as a separate bound | Treat source `500` as `= 500 users` | `UNSUPPORTED_BY_AVAILABLE_SOURCES` | Deferred | Equality, count unit, separate Evidence, and nested linkage are absent. |
| Protected technical versions | `TLS 1.3`; `OAuth 2.0/OIDC` | `SOURCE_ATTESTED` | Binding negative | Existing technical-version protection remains authoritative; no context rule may turn them into counts or bounds. |

`EXISTING_APPROVED` — The approved `QUANT-METRIC-001` positive variations and
the protected technical-version behavior remain binding independently of C0.
The composite context strings marked `SYNTHETIC_TEST_CASE` are not dissertation
evidence.

## 10. Interactions and regression risks

| Contract or consumer | Required outcome | Risk or approval gate |
| --- | --- | --- |
| `COND-UK-001/002` | Exact existing observations, Evidence, diagnostics, and processing remain unchanged. | Future quantitative Evidence owner must be compatibility-allowlisted without changing scalar attachment or condition grammar. |
| Quantitative observation count | Remain exactly one primary response-time observation for C0. | A second count observation is forbidden without separate count/nested approval. |
| `QUANT-METRIC-001` | Preserve metric component, Evidence, scalar attachment, exclusions, and identity. | Context enrichment must occur after and depend on the accepted metric observation; it cannot alter that rule. |
| `ACCEPT-QUANT-001` | Judgeability, result-span containment, criterion count, Evidence, and diagnostics remain unchanged. | Its component-owner allowlist must eventually accept the new quantitative-context Evidence owner while continuing to use only scalar Evidence for containment and judgeability. This requires an explicit compatibility decision. |
| `RESULT-UK-001/002` and `ACCEPT-UK-001` | No grammar, attachment, Evidence, or merge-order change. | Context linkage cannot become a result or literal-acceptance relation. |
| Quantitative diagnostics | Preserve the `500` diagnostic and mixed `INCOMPLETE / DETECTED` state under C0. | Suppression or replacement is a separate scientific decision. |
| Public `FeatureExtractor` | Continue assembling family outcomes and globally source-ordering Evidence without business-logic changes. | The quantitative detector may return one extra same-family Evidence item; the result registry will validate it. Same-span `COND` and quantitative items must retain distinct IDs. |
| Completeness | No change. It consumes general condition, expected-result, and acceptance families, not quantitative context. | Losing the existing `COND-UK-001` result through an allowlist regression could change Completeness and is unacceptable. |
| Verifiability | No change. The same quantitative observation remains present, so the lower-tier evidence class is unchanged; preserving the diagnostic does not remove that observation. | A context implementation must not create an acceptance criterion or an extra additive contribution. |
| Unambiguity | No change. Only approved vague-term signals are consumed. | No context/count ambiguity finding is authorized. |
| Findings and `QUALITY_PROBLEM` | No new Finding or problem conversion. | Detection and diagnostic data remain explanation/provenance only. |
| Reporter and aggregation | No presentation, formula, precision, or aggregation change. | Any new reporting of raw context components would be a separate presentation task, not part of scientific linkage. |

The acceptance allowlist is a material integration point. It currently permits
`QUANT-001`, `QUANT-UK-001`, and `QUANT-METRIC-001` as component Evidence
owners, then deliberately uses only scalar sources for containment. A future
context owner must be added only as an allowed component source. If all
top-level refs were instead required to lie inside result Evidence, the
postposed condition could wrongly disqualify the already judgeable scalar
result and change `ACCEPT-QUANT-001`. That change is not authorized.

## 11. Existing-domain sufficiency

| Need | Existing type/invariant | Assessment |
| --- | --- | --- |
| Attach one exact context phrase to one existing observation | `context: TextComponent | None` | Sufficient. |
| Preserve exact context source | `TextComponent.evidence_refs` plus `Evidence` | Sufficient. |
| Keep metric, scalar, and context refs linked and ordered | Top-level de-duplicated component union | Sufficient. |
| Coexist with same-span `COND-UK-001` | Distinct Evidence IDs and feature-family validation | Sufficient; shared span, separate identity. |
| Preserve unresolved embedded count | Family diagnostic outside accepted Evidence | Sufficient. |
| Represent a value-only independent count observation | Observation invariant requires comparator + value or value + unit | Insufficient without inventing comparator/unit semantics or changing the invariant. |
| Link a separate count observation back to its parent context | No parent/child or reusable attachment identity | Insufficient for a general nested model. |
| Represent several contexts or shared contexts | One `TextComponent` can hold several refs but has no explicit cardinality/attachment graph | Not established for broader grammar; deferred. |

`PROPOSED_RESEARCH_DECISION` — The existing domain is sufficient for C0 only:
one accepted context `TextComponent` on the existing response-time observation,
plus the preserved `500` diagnostic. No domain migration, new feature family,
unit label, comparator label, count component, or attachment class is needed.

`DEFERRED` — Existing types are not sufficient to claim that `500` is also an
independent quantitative observation or to preserve an explicit nested
relationship between two observations. Those roles must not be forced into
`TextComponent` merely because it can reference text.

## 12. Required researcher approval gates

No implementation may begin until the researcher records all applicable
decisions in the authoritative model specification:

1. **Semantic-role gate:** approve context interpretation A and explicitly
   defer or reject independent count/nested interpretations B and C for C0.
2. **Exact grammar gate:** approve or revise the exact postposed C0 suffix,
   including casing, U+0020 spacing, position, requirement-end restriction,
   punctuation, and hard boundaries.
3. **Primary-prefix gate:** confirm that any already accepted
   `QUANT-METRIC-001` value/duration variant may compose with the exact suffix,
   while no scalar syntax is extended.
4. **Population-count gate:** choose exact `500` for C0 or separately approve
   ASCII-integer C1. Decimal comma and other numeric forms must not be inherited
   silently.
5. **Evidence-ownership gate:** approve a separate quantitative-family Evidence
   item over `[18,49)`, independent of same-span `COND-UK-001` Evidence.
6. **Component-ref gate:** approve `context = TextComponent(...)` and the
   metric/scalar/context source-ordered top-level union.
7. **Diagnostic gate:** approve option A, or explicitly approve another option
   with its processing status, diagnostic owner/code/span, accepted Evidence,
   and judgeability consequences.
8. **Coexistence gate:** confirm that `COND-UK-001/002` results remain unchanged
   and shared spans do not imply shared IDs.
9. **Acceptance-compatibility gate:** permit the future context Evidence owner
   as a quantitative component source while preserving scalar-only
   containment, judgeability, and criterion deduplication.
10. **Domain gate:** confirm existing-domain sufficiency for context-only C0 and
    keep independent/nested count representation deferred.
11. **Multiplicity and uncertainty gate:** approve deterministic negatives for
    altered syntax and decide whether any recognized competing context produces
    an unresolved diagnostic in a later, broader rule. C0 itself proposes no
    new diagnostic.
12. **Rule-ID gate:** allocate a new production rule identity only after the
    semantics and Evidence boundary are approved. This package allocates none.
13. **Quality-model gate:** explicitly preserve no change to C/V/U,
    applicability, Findings, `QUALITY_PROBLEM`, confidence, severity, risk,
    aggregation, or reporting.
14. **Implementation gate:** authorize production code and binding tests in a
    separate task after the preceding scientific decisions are recorded.

## 13. Smallest candidate for later model-spec approval

`PROPOSED_RESEARCH_DECISION` — The smallest candidate is C0:

```text
Prerequisite:
  exactly one already accepted QUANT-METRIC-001 observation

Exact suffix:
  <U+0020>при<U+0020>500<U+0020>одночасних<U+0020>користувачах
  at trimmed requirement end and inside the same hard-bounded segment

Meaning:
  measurement/load context of the existing response-time observation

Evidence:
  one new quantitative-family item for the exact context span
  (future Rule ID; none allocated here)

Observation:
  populate context TextComponent on the existing observation
  preserve metric, comparator, value, unit, scalar refs, and observation count

Coexistence:
  preserve independent same-span COND-UK-001 Evidence and observation

Diagnostic:
  preserve QUANT_UNRESOLVED_NUMERIC_CANDIDATE for 500 at [22,25)
  preserve INCOMPLETE / DETECTED quantitative family state

Exclusions:
  no alternate count, marker, noun, spacing, punctuation variant, lexical
  comparator, second metric, second bound, multiple context, cross-boundary
  attachment, independent count observation, nested role, or parser fallback
```

This candidate is deliberately narrower than
`при <approved numeric form> одночасних користувачах`. The source supports the
exact count `500`; it does not support inheriting decimal-comma syntax for user
cardinality. If the researcher requires a reusable population value, C1 should
be a separate explicit decision limited to ASCII integers.

The candidate does not allocate a Rule ID, binding test, or implementation. It
does not claim that the context phrase is already approved merely because the
domain has a `context` field or `COND-UK-001` detects the same text.

## 14. Open blockers and final research status

The blockers to implementation are:

1. Context interpretation A is source-attested but not researcher-approved as
   production grammar.
2. C0's exact position, whitespace, end boundary, and punctuation behavior are
   not approved.
3. The scope of population-count generalization is undecided; existing scalar
   numeric syntax cannot settle count semantics.
4. A future quantitative-context Rule ID and Evidence identity are not
   allocated.
5. The researcher has not approved preserving `500` as an unresolved numeric
   candidate inside accepted context Evidence.
6. Condition and acceptance component-owner compatibility must be approved and
   later implemented without altering their current semantics.
7. Independent count and nested dual-role representation remain unsupported or
   deferred.
8. No implementation or binding-test task has been authorized.

`SOURCE_ATTESTED_NOT_ALLOCATED` — The available sources do support one bounded
candidate: the exact postposed phrase as the measurement/load context of the
accepted response-time observation. Therefore the package does not conclude
`NO_EXTENSION_READY`.

`PROPOSED_RESEARCH_DECISION` — C0 is scientifically plausible and narrow enough
for researcher review. It remains non-binding until the applicable gates in
§12 are recorded in `model-spec.md`.

**Final status: `DRAFT_FOR_RESEARCHER_REVIEW`.**
