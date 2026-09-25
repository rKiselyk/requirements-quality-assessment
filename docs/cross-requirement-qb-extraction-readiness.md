# QB-v0.1 quantitative extraction readiness

Research status: proposal pending researcher decision

Branch: `research/cross-requirement-analysis`

Research date: 2026-09-25

Accepted input status: `RESEARCHER_APPROVED / MIXED END_TO_END +
DOMAIN_CONTRACT CORPUS / END_TO_END_COMPOSITION_GAP_OPEN`

## 1. Purpose and authority boundary

This document answers one narrow question:

> What is the minimum scientifically defensible extraction bridge required to
> make the already-approved QB-v0.1 direct quantitative-bound conflict rule
> executable from text through a computed `M_cons[QB-v0.1]`, without changing
> the frozen Single Requirement Analysis semantics?

The accepted scientific inputs are:

- `docs/cross-requirement-analysis-research.md`;
- `docs/cross-requirement-consistency-decision-package.md`;
- `docs/cross-requirement-consistency-reference-cases.md`; and
- the authoritative implementation model in `docs/model-spec.md`.

Current production code and focused quantitative tests were inspected only to
verify the implemented baseline. No production code, detector, calculator,
test, reporter, pipeline, domain type, Rule ID, or Evidence ID was added or
changed in this round.

This is not a general reopening of `RQD-008`. It does not approve arbitrary
metrics or contexts, synonyms, unit conversion, parser linkage, general ranges,
frequency grammar, R3, F1-A, or semantic NLP. The 27 accepted reference cases
remain binding at their stated end-to-end or domain-contract boundaries.

## 2. Exact blocker confirmation

### 2.1 Verified current behavior

For the intended positive pair, the current quantitative detector produces the
following relevant records.

| Requirement | Current scalar result | Current identity enrichment | Diagnostic and processing |
| --- | --- | --- | --- |
| `R001`: `Час відгуку ≤ 2 с при 500 одночасних користувачах` | `QUANT-001:E001 = ≤ 2 с [12,17)`; `LESS_THAN_OR_EQUAL / INCLUSIVE`; `Decimal("2")`; `SECOND` | metric `QUANT-METRIC-001:E001 = Час відгуку [0,11)`; context `QUANT-CONTEXT-001:E001 = при 500 одночасних користувачах [18,49)` | `QUANT_UNRESOLVED_NUMERIC_CANDIDATE = 500 [22,25)`; `INCOMPLETE / DETECTED` |
| `R002`: `Час відгуку не нижче 5 с при 500 одночасних користувачах` | `QUANT-UK-001:E001 = не нижче 5 с [12,24)`; `GREATER_THAN_OR_EQUAL / INCLUSIVE`; `Decimal("5")`; `SECOND` | metric absent; context absent | `QUANT_UNRESOLVED_NUMERIC_CANDIDATE = 500 [29,32)`; `INCOMPLETE / DETECTED` |

The code path explains the result without an inferred semantic assumption:

1. `QUANT-UK-001` accepts `не нижче 5 с` as a lower-bound scalar.
2. The `QUANT-METRIC-001` eligibility check accepts only a symbolic
   `QUANT-001` `LESS_THAN_OR_EQUAL / INCLUSIVE` duration anchor.
3. `QUANT-CONTEXT-001` requires an already enriched
   `QUANT-METRIC-001` observation containing a symbolic `QUANT-001` anchor.
4. The general numeric diagnostic pass still sees the embedded `500`, because
   C0 deliberately does not turn it into accepted scalar Evidence or suppress
   it.
5. CRA-D067 currently makes any unresolved quantitative extraction sufficient
   to withhold the bounded aggregate.

Therefore the current implementation cannot produce the required combination
of a supported lower bound, complete QB comparison identity, and aggregate
observability from text.

### 2.2 Blocker classification

| Statement | Classification | Basis and consequence |
| --- | --- | --- |
| The supported `не нижче` / `GREATER_THAN_OR_EQUAL` form produces a scalar observation but receives no `Час відгуку` metric link. | `IMPLEMENTATION_LIMITATION` | The lower scalar and exact metric surface are separately approved, but the implemented `QUANT-METRIC-001` contract expressly excludes lexical `QUANT-UK-001` anchors. Changing that boundary requires a new bounded scientific decision before implementation. |
| The same lower-bound observation receives no exact C0 context link. | `IMPLEMENTATION_LIMITATION` | The implemented C0 rule requires an existing symbolic `QUANT-METRIC-001` observation. The suffix is recognized only for that approved construction. A lower-bound C0 composition requires a separate bounded scientific decision. |
| Exact C0 preserves the embedded-`500` diagnostic and leaves quantitative processing `INCOMPLETE`. | `ALREADY_RESEARCHER_APPROVED` | Model-spec Section 7.14.6.8 explicitly freezes the diagnostic, its span and rule, and the incomplete processing state while also establishing that the suffix is context rather than an independent count observation. |
| CRA-D067 makes unresolved quantitative extraction material to aggregate QB-v0.1 observability even when no unresolved observation pair exists. | `ALREADY_RESEARCHER_APPROVED` | The decision package requires aggregate `UNKNOWN` for any unresolved quantitative extraction because an unextracted observation could change the comparison universe or `R_conf[QB-v0.1]`. A narrower materiality test would amend, not reinterpret, that decision. |

The source/model distinction is important. The dissertation sources directly
attest the response-time metric surface and C0 suffix in the symbolic-upper
construction, and directly attest `не нижче` as a lower-bound comparator in a
different requirement. They do not directly attest the exact composite lower
response-time sentence proposed here. The missing bridge is therefore neither
a new mathematical rule nor a direct quotation of one source example. It is a
bounded composition of already supported facts requiring researcher
operationalization.

## 3. Lower-bound metric linkage research

### 3.1 Scientific feasibility

Attaching the exact existing metric surface to the already accepted lower-bound
observation is scientifically defensible, but it is not already approved.

The supporting facts are already established:

- `Час відгуку` is a source-attested quantitative metric;
- `не нижче` is a source-attested comparator mapped to
  `GREATER_THAN_OR_EQUAL / INCLUSIVE`;
- ASCII integer and single-decimal-comma values are approved;
- the duration surfaces `с`, `секунд`, `хв`, and `хвилин` already have approved
  `SECOND` or `MINUTE` labels;
- the domain model explicitly supports enriching an existing partial
  observation; and
- the approved linkage algorithm permits metric attachment only under a
  separately approved bounded template relating one governing metric to one
  bound.

What is new is the operational claim that these parts form one linked
observation in the exact lower-bound envelope below. That claim needs explicit
researcher approval.

### 3.2 Proposed closed grammar boundary

The minimum proposal has two accepted whole-input envelopes, where `<value>`
and `<duration-unit>` use only already approved scalar forms:

```text
LB-M0:
<Requirement.text start>Час<U+0020>відгуку<U+0020>не<U+0020>нижче
<U+0020><approved-value><U+0020><approved-duration-unit><Requirement.text end>

LB-M-C0:
<Requirement.text start>Час<U+0020>відгуку<U+0020>не<U+0020>нижче
<U+0020><approved-value><U+0020><approved-duration-unit>
<U+0020>при<U+0020>500<U+0020>одночасних<U+0020>користувачах
<Requirement.text end>
```

Line wrapping above is editorial only. Every displayed separator is exactly one
U+0020 SPACE. The exact mandatory boundary is:

1. metric text exactly `Час відгуку`, with that casing, at offset `0`;
2. exact lower comparator surface `не нижче`, with one U+0020 between its
   words;
3. one already accepted `QUANT-UK-001` anchor whose existing scalar semantics
   are `GREATER_THAN_OR_EQUAL / INCLUSIVE`;
4. an approved ASCII integer or single-decimal-comma value;
5. exactly one explicit approved duration surface: `с`, `секунд`, `хв`, or
   `хвилин`;
6. either trimmed-text end immediately after the duration unit, or the one
   exact C0 suffix in `LB-M-C0`;
7. exactly one metric occurrence and one eligible scalar bound in the whole
   input; and
8. no competing metric, bound, context, punctuation, conjunction,
   parenthesis, or arbitrary intervening/trailing material.

This full-envelope rule is intentionally narrower than the existing general
`QUANT-UK-001` lexical tolerance and narrower than a parser or proximity rule.
It does not inherit case-folding or variable Unicode whitespace for the metric
or composite envelope merely because the scalar detector can recognize some
such scalar variants internally.

### 3.3 Required disposition and Evidence

The bridge must enrich the one existing `QUANT-UK-001` observation. It must not
create a second quantitative observation, copy the scalar components, or
change comparator/value/unit semantics.

For the bare example `Час відгуку не нижче 5 с`, the future scientific
contract would require:

| Role | Exact source text | Span | Ownership |
| --- | --- | --- | --- |
| Metric | `Час відгуку` | `[0,11)` | new bounded metric-enrichment rule; Rule ID not allocated here |
| Existing scalar | `не нижче 5 с` | `[12,24)` | unchanged `QUANT-UK-001:E001` |

The enriched observation would preserve:

```text
comparator = GREATER_THAN_OR_EQUAL / INCLUSIVE
value = Decimal("5")
unit = SECOND
context = None
unresolved_components = ()
observation count = 1
```

It would add one exact-source metric Evidence item and make the top-level
evidence-reference tuple the stable source-ordered union of metric and existing
scalar references. Final Rule and Evidence IDs belong to a later authorized
implementation contract and are deliberately not proposed here.

### 3.4 Excluded and competing cases

The following remain ineligible:

- any metric other than exact `Час відгуку`, including `Час відповіді`;
- changed metric casing, spacing, normalization, morphology, or punctuation;
- a lower duration bound without that exact requirement-start metric;
- a metric inferred only from `SECOND` or `MINUTE`;
- another lexical comparator such as `не більше`, `не довше`, or `до`;
- symbolic `≥`, which is not an approved scalar comparator form;
- percent, missing-unit, decimal-point, signed, grouped, exponent, written
  number, range, or new-unit forms;
- two metric occurrences, two bounds, or any competing attachment candidate;
- a hard boundary between metric and bound;
- added prose, conjunctions, parentheses, clauses, or trailing punctuation;
- a parser relation, nearest-noun selection, or semantic synonym inference;
  and
- redistribution of one metric over multiple observations.

Non-match is deterministic absence of this enrichment only. It must not delete
the existing scalar observation, create a new ambiguity diagnostic, or add
`METRIC` to `unresolved_components` without a separately approved ambiguity
rule.

### 3.5 Compatibility consequences

The proposal changes trace, not the accepted lower scalar or its current local
numeric contribution:

- it adds exact metric Evidence and an evidence reference;
- it changes the lower observation from `metric=None` to a resolved metric;
- it preserves the existing scalar Evidence ID and all scalar components;
- it preserves the observation count and source order;
- it does not create an acceptance criterion or Finding; and
- it does not alter the quantitative diagnostic or processing state.

Current `CALC-V-MVP-001` already receives an accepted quantitative observation
from `QUANT-UK-001`; metric enrichment cannot raise the lower-tier class.
Completeness does not consume the quantitative metric component, and
Unambiguity consumes only vague-term occurrences. Thus the proposed enrichment
can and must preserve existing `C_i`, `V_i`, and `U_i` while expanding Evidence
and trace. An implementation contract would need regression tests for both the
numeric invariants and the intended trace delta.

## 4. Lower-bound C0 context linkage research

### 4.1 Separate bounded rule requirement

The existing C0 contract cannot silently broaden. It is explicitly defined as
an enrichment of one `QUANT-METRIC-001` symbolic-upper observation. A lower
metric bridge would not make that precondition true and must not reuse the
existing C0 Rule ID with changed semantics.

A separate bounded scientific rule is feasible for `LB-M-C0`, conditional on
approval of the lower-bound metric bridge. Its sole positive envelope is:

```text
Час відгуку не нижче <approved-value> <approved-duration-unit>
при 500 одночасних користувачах
```

The line break is editorial. The production text is one line with exact U+0020
separators and no final punctuation.

Mandatory gates are:

1. one observation already enriched by the proposed lower-bound metric rule;
2. the exact `GREATER_THAN_OR_EQUAL / INCLUSIVE` `QUANT-UK-001` scalar;
3. exactly one U+0020 after the duration unit;
4. exact suffix `при 500 одночасних користувачах` ending at trimmed-text end;
5. the same single metric/bound/context hard-bounded segment;
6. no competing metric, bound, context, or intervening material; and
7. no generic `при` grammar, parser fallback, population variation, or context
   inference.

For `Час відгуку не нижче 5 с при 500 одночасних користувачах`, the required
provenance is:

| Role | Exact source text | Span | Ownership |
| --- | --- | --- | --- |
| Metric | `Час відгуку` | `[0,11)` | proposed lower-bound metric rule |
| Existing scalar | `не нижче 5 с` | `[12,24)` | unchanged `QUANT-UK-001:E001` |
| Context | `при 500 одночасних користувачах` | `[25,56)` | separate proposed lower-bound C0 rule |
| Preserved diagnostic candidate | `500` | `[29,32)` | unchanged diagnostic under `QUANT-001`; not Evidence |

The context rule must enrich the same observation; observation count remains
one. Its top-level references are the stable source-ordered union of metric,
scalar, and context Evidence. The quantitative context reference must resolve
to Evidence owned by the new bounded context rule. A same-span
`COND-UK-001` item remains distinct condition-family Evidence and cannot be
substituted. Cross-requirement use later qualifies every reference by its
owning requirement ID under CRA-D048.

Changed `500`, changed marker/casing/spacing/population text, extra context,
punctuation after the suffix, hard-boundary separation, or any competition is a
non-match. Non-match preserves the metric-enriched lower observation and all
existing extraction behavior; it does not invent a `CONTEXT` diagnostic.

## 5. C0 embedded-`500` materiality

### 5.1 Two different completeness questions

The existing evidence supports a distinction between:

1. **quantitative extraction globally incomplete**: the public quantitative
   detector outcome is `INCOMPLETE` because the preserved `500` diagnostic is
   present; and
2. **QB-v0.1 material extraction incomplete**: unresolved extraction exists
   that could change the QB comparison universe, a comparison state, or
   membership in `R_conf[QB-v0.1]`.

The first state belongs to the frozen Single Requirement Analysis extraction
contract. The second is a coverage/observability predicate for one explicitly
bounded cross-requirement analysis. They must not be represented by rewriting
the first state.

### 5.2 Why a narrow exception is scientifically defensible

The accepted C0 scientific contract already proves, for its exact positive,
that the embedded `500` is:

- measurement/load context of the response-time bound;
- not an independent count constraint;
- not an equality assertion;
- not an independently judgeable bound;
- not a second quantitative observation; and
- not a nested quantitative relation.

That proof is stronger than mere implementation silence. It establishes that
this one diagnostic cannot create an additional QB-v0.1 comparison member
under the same approved coverage profile. Preserving the diagnostic remains
necessary for the global detector contract, but treating it as material to the
QB numerator is no longer scientifically necessary once the cross layer can
verify the exact approved C0 provenance.

### 5.3 Proposed fail-closed materiality exception

The exception must apply only when every condition below is true:

1. the diagnostic code is exactly
   `QUANT_UNRESOLVED_NUMERIC_CANDIDATE`;
2. its diagnostic `rule_id` is exactly `QUANT-001`;
3. its candidate text is exactly ASCII `500`;
4. its source span is exactly the embedded numeric span within an accepted
   exact C0 context Evidence item;
5. that C0 item enriches the same single QB-eligible response-time observation;
6. the C0 rule version explicitly carries the approved non-independent-role
   guarantee listed in Section 5.2;
7. the requirement has no other unresolved quantitative diagnostic,
   unresolved quantitative component, unlinked quantitative candidate, or
   competing quantitative observation whose resolution could affect QB-v0.1;
   and
8. all referenced Evidence and diagnostic spans pass their existing ownership
   and exact-source invariants.

If any gate is absent, ambiguous, invalid, or changed by a future rule version,
the diagnostic remains QB-material and aggregate computation fails closed to
`UNKNOWN`.

This is not a generic ignored-diagnostic list. It does not apply to `95`, `600`,
another C0-like phrase, R3's `300`, a missing metric or context, unresolved
inclusivity, or any future diagnostic merely because a developer believes it
is harmless.

### 5.4 Required observability metadata

The existing conceptual
`unresolved_quantitative_extraction_count` must retain its global meaning. It
must not be silently repurposed or reduced. The proposed cross-analysis profile
needs a separately named conceptual count, for example:

```text
global_unresolved_quantitative_extraction_count
qb_material_unresolved_quantitative_extraction_count
qb_non_material_preserved_diagnostic_count
```

These are scientific roles, not approved Python field names. Audit output must
identify every non-material classification with requirement, diagnostic code,
span, governing C0 Evidence, C0 contract version, and the QB materiality rule
version.

For the minimum future conflict pair, the expected distinction is:

```text
global unresolved quantitative extraction count = 2
QB-v0.1 material unresolved quantitative extraction count = 0
preserved QB-non-material C0 diagnostic count = 2
```

Both detector outcomes remain `INCOMPLETE`. The aggregate becomes observable
only because the two diagnostics are proven not to change this bounded
comparison universe.

## 6. CRA-D067 review

### 6.1 Current decision

CRA-D067 is scientifically conservative and correct without a proof of
diagnostic non-materiality: an unextracted observation may introduce an
applicable comparison and add requirements to `R_conf[QB-v0.1]`. It must remain
the default.

Keeping it literally unchanged, however, makes the only approved exact C0
surface permanently incapable of producing a computed QB-v0.1 aggregate while
its deliberately preserved diagnostic exists. That consequence is stronger
than the rationale requires in the one case where another approved rule proves
that the diagnostic cannot be an independent QB observation.

### 6.2 Proposed narrow amendment

CRA-D067 should receive a researcher-approved, coverage-specific amendment:

> `M_cons[QB-v0.1]` is withheld when unresolved quantitative extraction may
> change the QB-v0.1 comparison universe, an observation-pair assessment, or
> membership in `R_conf[QB-v0.1]`. Global extraction incompleteness remains
> preserved and reported. The exact embedded-`500` diagnostic of an accepted
> C0 context may be classified as non-material to QB-v0.1 only under every
> gate in Section 5.3, because the accepted C0 contract proves that it cannot
> form an independent QB-v0.1 observation. All other unresolved quantitative
> extraction remains material by default.

This is a substantive amendment, not an editorial clarification, and is
therefore `RESEARCHER_APPROVAL_PROPOSED`.

### 6.3 Consequence analysis

| Concern | Consequence of the proposed amendment |
| --- | --- |
| Scientific correctness | Improves correspondence between aggregate withholding and the actual uncertainty capable of changing the bounded operand. It relies on an explicit prior scientific proof, not implementation convenience. |
| False consistency claims | Risk remains bounded by exact gates, fail-closed defaults, coverage-qualified naming, and mandatory audit metadata. `M_cons[QB-v0.1]=1` still cannot mean universal consistency. |
| Frozen local C/V/U | Unchanged. Detector processing remains `INCOMPLETE`; calculators and their inputs are not reinterpreted. |
| Evidence and diagnostics | Preserved exactly. The diagnostic is classified for one downstream purpose, never deleted, converted to Evidence, or relabeled. |
| Audit reporting | Becomes more explicit: both global incompleteness and QB materiality must be visible, together with the proof used for each exception. |
| Accepted reference corpus | The corpus is not factually wrong under current CRA-D067 and is not modified now. After approval, cases whose only uncertainty is exact C0 `500` require an explicit superseding expectation/version: RC-QB-005 would become `COMPUTED / 1`; RC-QB-011 would become `NOT_APPLICABLE`, while missing-identity and unrelated-diagnostic cases remain `UNKNOWN`. A new end-to-end conflict case would then be eligible. |
| Future detector extensions | Default materiality remains strict. Any rule that makes the C0 count independently observable, changes its role, or changes C0 provenance invalidates the exception until separately reviewed. |

RC-QB-013 through RC-QB-016 and RC-QB-022 through RC-QB-024 do not become
computable merely because this exception exists: their missing identity,
unresolved comparator semantics, competing observations, or unrelated numeric
diagnostics may still change the QB comparison universe or conflict set.

## 7. Option comparison and recommendation

| Option | Scientific effect | Compatibility effect | End-to-end consequence | Disposition |
| --- | --- | --- | --- | --- |
| A — suppress or change the existing `500` diagnostic | Conflates accepted C0 role knowledge with a change to the global scalar-detector contract. It discards an intentionally preserved uncertainty signal instead of classifying its relevance. | Changes detector diagnostics and `INCOMPLETE` processing; may affect traces and future consumers and violates the frozen C0 contract. | Could unblock aggregation, but by paying an unjustified Single Requirement Analysis compatibility cost. | Reject. |
| B — preserve the diagnostic and add QB-specific materiality semantics | Separates global extraction state from whether the unresolved item can change the bounded cross-analysis operand. Uses the explicit C0 non-independent-role proof. | Preserves detector behavior, diagnostics, local calculators, records, and current aggregate profile; adds only future cross-analysis observability metadata and a narrow CRA-D067 amendment. | Enables the exact bounded end-to-end path while remaining fail-closed elsewhere. | Recommend for researcher approval. |
| C — keep strict CRA-D067 unchanged | Maximally conservative but ignores the approved proof that exact C0 `500` cannot be an independent QB member. | No contract change. | Exact C0 inputs remain permanently `UNKNOWN`; the accepted QB rule cannot reach a computed end-to-end result through the only approved complete context surface. | Scientifically coherent but reject as the preferred boundary because it blocks a provably observable bounded case. |

Option B is recommended on scientific, not implementation, grounds. It
preserves all evidence and uncertainty at their original layer while allowing
a downstream assessment to distinguish uncertainty relevant to its declared
operand from uncertainty proven irrelevant to that operand.

## 8. Minimum future end-to-end fixture

The following pair can become a binding end-to-end reference case only after
researcher approval of the three decisions in Section 12 and a separately
authorized implementation/audit round.

```text
R001: Час відгуку ≤ 2 с при 500 одночасних користувачах
R002: Час відгуку не нижче 5 с при 500 одночасних користувачах
```

### 8.1 Conditional expected extraction

| Component | R001 | R002 |
| --- | --- | --- |
| Metric | `Час відгуку [0,11)` | `Час відгуку [0,11)` under the proposed lower metric rule |
| Scalar | `≤ 2 с [12,17)`; `LESS_THAN_OR_EQUAL / INCLUSIVE`; `Decimal("2")`; `SECOND` | `не нижче 5 с [12,24)`; `GREATER_THAN_OR_EQUAL / INCLUSIVE`; `Decimal("5")`; `SECOND` |
| Context | `при 500 одночасних користувачах [18,49)` | `при 500 одночасних користувачах [25,56)` under the proposed lower C0 rule |
| Diagnostic | preserved `500 [22,25)` | preserved `500 [29,32)` |
| Quantitative processing | unchanged `INCOMPLETE / DETECTED` | unchanged `INCOMPLETE / DETECTED` |
| QB-material unresolved extraction | none, conditionally under the exact exception | none, conditionally under the exact exception |

The normalized key on both sides is:

```text
(
    N("Час відгуку") = "час відгуку",
    N("при 500 одночасних користувачах") =
        "при 500 одночасних користувачах",
    UnitLabel.SECOND,
)
```

The approved admissible sets would be:

```text
A(R001) = {x in Decimal | x <= Decimal("2")}
A(R002) = {x in Decimal | x >= Decimal("5")}
A(R001) intersection A(R002) = empty set
```

Conditional expected cross result:

```text
state = CONFIRMED_CONFLICT
subtype = DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
participants = (R001, R002)
R_conf[QB-v0.1] = {R001, R002}
R_conf_complete = true
M_cons[QB-v0.1] = 1 - 2/2 = Fraction(0, 1)
aggregate state = COMPUTED
```

Every cross Evidence reference remains participant-qualified. The conflict
explanation must cite both metrics, both scalar anchors, and both contexts. The
two preserved diagnostics and their non-materiality proofs remain in aggregate
audit metadata. The result remains coverage-qualified and makes no claim about
terminological, resource, other logical, duplicate, or semantic conflicts.

### 8.2 Current status of the fixture

The pair is not a binding end-to-end fixture today. It remains:

- binding at the domain-contract boundary through existing reference cases;
- a verified negative/rejected current-extractor fixture for the missing lower
  identity bridge; and
- a candidate future end-to-end fixture conditional on researcher approval,
  implementation authorization, Rule/Evidence ID allocation, implementation,
  regression verification, technical audit, and reference-corpus amendment.

## 9. Frozen Single Requirement Analysis invariant

The recommended solution must preserve all of the following:

| Frozen element | Required invariant |
| --- | --- |
| `C_i` | No formula, input-family, applicability, state, or value change. |
| `V_i` | Existing accepted lower scalar already establishes the same lower-tier evidence class; enrichment must not add a new class or contribution. |
| `U_i` | No vague-term observation, Finding, or calculation change. |
| Existing quantitative observations | Preserve every observation outside the two exact envelopes; inside them, enrich the existing lower observation rather than duplicate or replace it. |
| Diagnostics and processing | Preserve the embedded-`500` diagnostic and `INCOMPLETE` quantitative processing exactly. |
| Findings | No new Finding, `QUALITY_PROBLEM`, confidence, severity, risk, or correction. |
| `RequirementAssessmentRecord` | Preserve envelope meaning and local assessment semantics; only accepted extraction Evidence/refs may be enriched by a future authorized rule. |
| `SpecificationQualityProfile` | Remains exactly the current C/V/U aggregate profile. Consistency stays a separate future set-level assessment. |
| `AGG-MVP-001` | No formula, mixed-state, denominator, or presentation change. |
| User/audit reporting | Preserve the meaning of global `INCOMPLETE`; disclose new Evidence and both global and QB-material unresolved counts rather than hiding the diagnostic. |

Read-only exploratory execution of the current full extraction/calculation path
for the proposed pair produced the same local values on both requirements:

```text
C_i = Fraction(1,3)
V_i = Fraction(1,2)
U_i = Fraction(1,1)
```

Those exact current values are regression anchors for the future fixture, not
new calculation decisions. An option that changes them has a major
compatibility cost and is outside the recommended solution.

## 10. Relationship to R3 and F1-A

Neither already approved but unimplemented contract solves this blocker.

### 10.1 Exact R3

R3 recognizes one different 160-code-point requirement and produces a separate
relationship record connecting a percentage member, an existing upper duration
bound, an exact load context, and an unresolved `до 300` load-bound member. It
preserves its scalar observations and does not enrich the response-time lower
bound proposed here. Its duration observation also lacks the exact QB metric
identity required for this pair. Implementing R3 would not create
`Час відгуку`, `GREATER_THAN_OR_EQUAL`, or the exact C0 lower-bound link.

### 10.2 Exact F1-A

F1-A recognizes exact `не рідше одного разу на 5 с` frequency semantics as an
ordinary observation. Its comparator is `NOT_LESS_FREQUENT`, which CRA-D034
places outside QB-v0.1. It neither creates the required response-time lower
bound nor supplies the exact C0 link. Its approved local Verifiability
consequence on one fixture is unrelated to the proposed pair.

Therefore R3 and F1-A remain separately approved, unimplemented work. They must
not be implemented, broadened, or used as surrogate authority in this round.

## 11. Decision table

| Decision ID | Question | Existing authority | Proposed decision | Compatibility impact | Recommendation | Status |
| --- | --- | --- | --- | --- | --- | --- |
| QB-ER-D001 | Is the current text-to-computed blocker real? | Current detector; model-spec Sections 7.14.6.6-8; accepted reference corpus; CRA-D067 | Confirm the two missing lower identity links plus the preserved C0 diagnostic and strict aggregate gate. | None; records observed baseline. | Retain as research premise. | `DIRECTLY_DERIVABLE` |
| QB-ER-D002 | May exact `Час відгуку` enrich the existing exact `не нижче` duration observation? | Separately source-attested metric and comparator; approved scalar forms; linked observation model | Approve only the two closed whole-input envelopes in Section 3.2, enriching one existing observation. | Adds metric Evidence/refs; preserves observation count, scalar, diagnostics, and C/V/U. | Approve. | `RESEARCHER_APPROVAL_PROPOSED` |
| QB-ER-D003 | Should the bridge create a new observation? | Existing `QUANT-METRIC-001` enrichment pattern and component-union invariants | No; duplicate scalar observations would misrepresent one expressed bound. | Preserves current observation cardinality and scalar identity. | Require enrichment. | `DIRECTLY_DERIVABLE` |
| QB-ER-D004 | May the lower metric rule infer synonyms, tolerate variant envelopes, use a parser, or infer from units? | Current exact metric contract and explicit deferred boundaries | No; retain every negative boundary in Section 3.4. | Prevents broad RQD-008 expansion. | Reject every such broadening. | `REJECTED` |
| QB-ER-D005 | May exact C0 enrich the newly metric-linked lower observation? | Source-attested C0 role; approved exact C0 semantics; proposed QB-ER-D002 | Approve a separate rule only for exact `LB-M-C0`, with Section 4 provenance and exclusions. | Adds context Evidence/refs; preserves existing C0 rule meaning, scalar, diagnostic, processing, and C/V/U. | Approve conditionally with QB-ER-D002. | `RESEARCHER_APPROVAL_PROPOSED` |
| QB-ER-D006 | May the existing C0 Rule ID silently cover the lower construction? | Immutable Rule ID policy; current C0 contract requires symbolic `QUANT-METRIC-001` | No. A future implementation must allocate new Rule IDs only after authorization. | Protects historical provenance and avoids semantic mutation. | Reject reuse or silent broadening. | `REJECTED` |
| QB-ER-D007 | Should the embedded-`500` diagnostic or `INCOMPLETE` state change? | Researcher-approved C0 contract | No; preserve both exactly. | Fully preserves Single Requirement Analysis extraction semantics. | Retain. | `DIRECTLY_DERIVABLE` |
| QB-ER-D008 | Can exact C0 `500` independently enter QB-v0.1? | Approved C0 statement that it is context, not an independent bound/observation/relation | No, for the exact approved C0 positive and only while that contract/version remains applicable. | Supplies the scientific proof required for a bounded materiality exception. | Use only through the fail-closed gates. | `DIRECTLY_DERIVABLE` |
| QB-ER-D009 | Should CRA-D067 distinguish global extraction incompleteness from QB-material incompleteness? | CRA-D067 rationale; exact C0 non-independent-role proof | Adopt the Section 6.2 amendment and Section 5.3 sole exception; preserve separate mandatory audit counts. | Changes only future QB aggregate observability; local extraction, diagnostics, C/V/U, AGG-MVP-001, and current profile remain intact. | Approve. | `RESEARCHER_APPROVAL_PROPOSED` |
| QB-ER-D010 | Should C0 `500` be suppressed to enable computation? | Frozen C0 diagnostic and Single Requirement Analysis invariant | No. | Would change accepted extraction state and audit trace. | Reject Option A. | `REJECTED` |
| QB-ER-D011 | Should strict CRA-D067 remain unchanged despite the exact non-materiality proof? | Current approved decision | It remains the default, but should not remain exceptionless for exact C0. | Leaving it unchanged preserves compatibility but permanently blocks the exact C0 end-to-end aggregate. | Reject Option C as preferred solution. | `REJECTED` |
| QB-ER-D012 | Do R3 or F1-A solve the same-metric inclusive upper/lower response-time conflict? | Approved exact R3 and F1-A contracts | No; their grammar, representation, comparator, and identity differ. | None; both remain unimplemented and separate. | Do not use or broaden them here. | `DIRECTLY_DERIVABLE` |
| QB-ER-D013 | Can the Section 8 pair become a binding end-to-end conflict fixture after approval and implementation? | Approved QB identity/predicate/aggregate plus QB-ER-D002, D005, D009 | Yes, conditionally; expected result is conflict, participant set `{R001,R002}`, and `Fraction(0,1)`. | Requires future implementation, audit, and explicit corpus version/amendment; no current case is silently overwritten. | Adopt after all gates pass. | `DIRECTLY_DERIVABLE` |
| QB-ER-D014 | Are arbitrary metric/context linkage, variable populations, unit conversion, ranges, frequency, R3/F1-A implementation, or broader RQD-008 work opened? | Existing deferrals and this round's scope | No. | Keeps the research bridge minimal. | Defer. | `DEFERRED` |

Exactly three genuinely new scientific approvals are requested:
QB-ER-D002, QB-ER-D005, and QB-ER-D009. All other rows classify existing
authority, derive consequences, reject alternatives, or preserve deferrals.

## 12. Researcher Approval Checklist

- [ ] **QB-ER-D002 — exact lower-bound metric enrichment.** Approve only the
  closed `LB-M0` and `LB-M-C0` envelopes, enriching the existing
  `QUANT-UK-001` `GREATER_THAN_OR_EQUAL / INCLUSIVE` duration observation with
  exact `Час відгуку` Evidence and no duplicate observation.
- [ ] **QB-ER-D005 — exact lower-bound C0 enrichment.** Approve a separate
  bounded rule that attaches exact `при 500 одночасних користувачах` Evidence
  to the QB-ER-D002 observation, with all provenance and negative boundaries
  in Section 4 and without changing the existing C0 rule.
- [ ] **QB-ER-D009 — QB-specific materiality and CRA-D067 amendment.** Preserve
  global `INCOMPLETE` and the diagnostic, but classify only the exact proven C0
  embedded-`500` diagnostic as non-material to QB-v0.1 under every fail-closed
  gate in Section 5.3; require separate global/material audit counts.

Approval of this checklist would approve science only. It would not authorize
implementation, tests, Rule ID allocation, architecture, reporter changes,
reference-corpus edits, a merge, baseline, tag, or release.

## 13. End-of-round report

1. **Branch:** `research/cross-requirement-analysis`.
2. **File created:** `docs/cross-requirement-qb-extraction-readiness.md`.
3. **Exact blocker classification:** two `IMPLEMENTATION_LIMITATION` identity
   gaps plus two `ALREADY_RESEARCHER_APPROVED` strictness conditions: preserved
   C0 diagnostic/`INCOMPLETE` processing and current CRA-D067 propagation.
4. **Lower-bound metric linkage:** scientifically feasible as a bounded
   composition requiring researcher operationalization; not directly supported
   as the exact composite sentence.
5. **Lower-bound context linkage:** scientifically feasible only through a
   separate exact lower-C0 rule conditional on the metric bridge.
6. **C0 `500` treatment:** preserve diagnostic and global `INCOMPLETE`; propose
   exact, audited QB-non-material classification only under Section 5.3.
7. **CRA-D067:** requires a narrow researcher-approved amendment; strict
   behavior remains the default for every other unresolved extraction.
8. **Frozen Single Requirement Analysis:** can remain intact, including current
   local numeric values, diagnostics, records, profile, AGG-MVP-001, and
   reporting meaning.
9. **New researcher decisions required:** 3.
10. **Reason for readiness:** the gap can be closed with two exact enrichment
    rules and one coverage-specific materiality amendment, without reopening
    broad quantitative grammar or changing local quality science.

READY_FOR_RESEARCHER_DECISION
