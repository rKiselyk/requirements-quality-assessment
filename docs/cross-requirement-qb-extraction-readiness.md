# QB-v0.1 quantitative extraction readiness

Research status: `RESEARCH_COMPLETE_READY_FOR_ARCHITECTURE`

Branch: `research/cross-requirement-analysis`

Research date: 2026-09-25

Researcher decision date: 2026-09-25

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
5. Before the final decision in this document, CRA-D067 made any unresolved
   quantitative extraction sufficient to withhold the bounded aggregate. The
   researcher-approved amendment in Section 6 now applies materiality instead.

Therefore the current implementation cannot produce the required combination
of a supported lower bound, complete QB comparison identity, and aggregate
observability from text.

### 2.2 Blocker classification

| Statement | Classification | Basis and consequence |
| --- | --- | --- |
| The supported `не нижче` / `GREATER_THAN_OR_EQUAL` form produces a scalar observation but receives no `Час відгуку` metric link. | `IMPLEMENTATION_LIMITATION` | The lower scalar and exact metric surface are separately approved, but the implemented `QUANT-METRIC-001` contract expressly excludes lexical `QUANT-UK-001` anchors. Changing that boundary requires a new bounded scientific decision before implementation. |
| The same lower-bound observation receives no exact C0 context link. | `IMPLEMENTATION_LIMITATION` | The implemented C0 rule requires an existing symbolic `QUANT-METRIC-001` observation. The suffix is recognized only for that approved construction. A lower-bound C0 composition requires a separate bounded scientific decision. |
| Exact C0 preserves the embedded-`500` diagnostic and leaves quantitative processing `INCOMPLETE`. | `ALREADY_RESEARCHER_APPROVED` | Model-spec Section 7.14.6.8 explicitly freezes the diagnostic, its span and rule, and the incomplete processing state while also establishing that the suffix is context rather than an independent count observation. |
| Original CRA-D067 made unresolved quantitative extraction material to aggregate QB-v0.1 observability even when no unresolved observation pair existed. | `ALREADY_RESEARCHER_APPROVED` | The original strict default was scientifically conservative. On 2026-09-25 it was amended by approved QB-ER-D009 only for unresolved extraction proven non-material under an explicit, versioned, fail-closed QB rule. |

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
observation is researcher-approved only inside the complete `LB-M-C0` envelope.
Standalone lower-bound metric enrichment is not approved.

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

The researcher approved the operational composition on 2026-09-25 with the
narrowing recorded in QB-ER-D002 and QB-ER-D005 below.

### 3.2 Approved closed grammar boundary

The approved bridge has exactly one whole-input envelope. `<value>` and
`<duration-unit>` use only already approved scalar forms:

```text
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
6. exactly one U+0020 followed by the exact C0 suffix
   `при 500 одночасних користувачах`, which ends at trimmed-text end;
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

For the approved example
`Час відгуку не нижче 5 с при 500 одночасних користувачах`, the future
implementation contract must require:

| Role | Exact source text | Span | Ownership |
| --- | --- | --- | --- |
| Metric | `Час відгуку` | `[0,11)` | future bounded enrichment rule; Rule ID and Evidence ID not allocated here |
| Existing scalar | `не нижче 5 с` | `[12,24)` | unchanged `QUANT-UK-001:E001` |
| Context | `при 500 одночасних користувачах` | `[25,56)` | future bounded enrichment rule; Rule ID and Evidence ID not allocated here |
| Preserved diagnostic | `500` | `[29,32)` | unchanged `QUANT-001` diagnostic; not Evidence |

The enriched observation would preserve:

```text
comparator = GREATER_THAN_OR_EQUAL / INCLUSIVE
value = Decimal("5")
unit = SECOND
context = exact C0 context Evidence
unresolved_components = ()
observation count = 1
```

It would add exact-source metric and context Evidence items and make the
top-level evidence-reference tuple the stable source-ordered union of metric,
existing scalar, and context references. Final Rule and Evidence IDs belong to
a later authorized implementation contract and are deliberately not allocated
here.

### 3.4 Excluded and competing cases

The following remain ineligible:

- any metric other than exact `Час відгуку`, including `Час відповіді`;
- changed metric casing, spacing, normalization, morphology, or punctuation;
- a lower duration bound without that exact requirement-start metric;
- the standalone `Час відгуку не нижче <value> <unit>` form without exact C0;
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

The approved bridge changes trace, not the accepted lower scalar or its current local
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
Unambiguity consumes only vague-term occurrences. Thus the approved enrichment
can and must preserve existing `C_i`, `V_i`, and `U_i` while expanding Evidence
and trace. An implementation contract would need regression tests for both the
numeric invariants and the intended trace delta.

## 4. Lower-bound C0 context linkage research

### 4.1 Separate bounded rule requirement

The existing C0 contract cannot silently broaden. It is explicitly defined as
an enrichment of one `QUANT-METRIC-001` symbolic-upper observation. A lower
metric bridge would not make that precondition true and must not reuse the
existing C0 Rule ID with changed semantics.

A separate bounded scientific contract is approved for `LB-M-C0`, composed
with the narrowed lower-bound metric bridge. Its sole positive envelope is:

```text
Час відгуку не нижче <approved-value> <approved-duration-unit>
при 500 одночасних користувачах
```

The line break is editorial. The production text is one line with exact U+0020
separators and no final punctuation.

Mandatory gates are:

1. one observation eligible for the approved combined `LB-M-C0` enrichment;
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
| Metric | `Час відгуку` | `[0,11)` | approved, not-implemented lower-bound bridge |
| Existing scalar | `не нижче 5 с` | `[12,24)` | unchanged `QUANT-UK-001:E001` |
| Context | `при 500 одночасних користувачах` | `[25,56)` | approved, not-implemented lower-bound C0 enrichment |
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
non-match. Because standalone metric enrichment is not approved, non-match
preserves only the existing `QUANT-UK-001` scalar and all other existing
extraction behavior; it creates neither metric/context Evidence nor a
`CONTEXT` diagnostic.

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

Both allowlisted exact C0 scientific contracts prove, for their respective
positive envelopes, that the embedded `500` is:

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

### 5.3 Approved fail-closed materiality allowlist

QB-ER-D009 approves exactly two scientific context contracts for possible
`QB_NON_MATERIAL` classification:

1. the existing exact upper-bound C0 contract represented in production by
   `QUANT-CONTEXT-001`; and
2. the exact lower-bound C0 contract approved by QB-ER-D005, whose production
   implementation, Rule ID, and Evidence IDs remain absent.

No other context contract is allowlisted.

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
the result is `QB_MATERIAL_UNRESOLVED` and aggregate computation fails closed
to `UNKNOWN`.

This is not a generic ignored-diagnostic list. It does not apply to `95`, `600`,
another C0-like phrase, R3's `300`, a missing metric or context, unresolved
inclusivity, or any future diagnostic merely because a developer believes it
is harmless.

### 5.4 Required observability metadata

The existing conceptual
`unresolved_quantitative_extraction_count` must retain its global meaning. It
must not be silently repurposed or reduced. The approved cross-analysis
contract requires separately named conceptual counts, for example:

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

### 6.2 Researcher-approved narrow amendment

On 2026-09-25, QB-ER-D009 amended CRA-D067 as follows:

> `M_cons[QB-v0.1]` is withheld when unresolved quantitative extraction may
> change the QB-v0.1 comparison universe, an observation-pair assessment, or
> membership in `R_conf[QB-v0.1]`. Global extraction incompleteness remains
> preserved and reported. The exact embedded-`500` diagnostic of either
> allowlisted C0 context contract may be classified `QB_NON_MATERIAL` only
> under every gate in Section 5.3, because each accepted C0 contract proves
> that the diagnostic cannot form an independent QB-v0.1 observation. All
> other unresolved quantitative extraction remains
> `QB_MATERIAL_UNRESOLVED` by default.

This is a substantive, researcher-approved amendment, not an editorial
clarification. The original strict rationale remains the fail-closed default.

### 6.3 Consequence analysis

| Concern | Consequence of the approved amendment |
| --- | --- |
| Scientific correctness | Improves correspondence between aggregate withholding and the actual uncertainty capable of changing the bounded operand. It relies on an explicit prior scientific proof, not implementation convenience. |
| False consistency claims | Risk remains bounded by exact gates, fail-closed defaults, coverage-qualified naming, and mandatory audit metadata. `M_cons[QB-v0.1]=1` still cannot mean universal consistency. |
| Frozen local C/V/U | Unchanged. Detector processing remains `INCOMPLETE`; calculators and their inputs are not reinterpreted. |
| Evidence and diagnostics | Preserved exactly. The diagnostic is classified for one downstream purpose, never deleted, converted to Evidence, or relabeled. |
| Audit reporting | Becomes more explicit: both global incompleteness and QB materiality must be visible, together with the proof used for each exception. |
| Accepted reference corpus | The extraction facts remain correct. The amended aggregate science supersedes two expectations: RC-QB-005 is now `COMPUTED / 1`, and RC-QB-011 is now `NOT_APPLICABLE`; missing-identity and unrelated-diagnostic cases remain `UNKNOWN`. The lower-bound conflict pair remains a future post-implementation validation target, not a current end-to-end case. |
| Future detector extensions | Default materiality remains strict. Any rule that makes the C0 count independently observable, changes its role, or changes C0 provenance invalidates the exception until separately reviewed. |

RC-QB-013 through RC-QB-016 and RC-QB-022 through RC-QB-024 do not become
computable merely because this exception exists: their missing identity,
unresolved comparator semantics, competing observations, or unrelated numeric
diagnostics may still change the QB comparison universe or conflict set.

## 7. Option comparison and recommendation

| Option | Scientific effect | Compatibility effect | End-to-end consequence | Disposition |
| --- | --- | --- | --- | --- |
| A — suppress or change the existing `500` diagnostic | Conflates accepted C0 role knowledge with a change to the global scalar-detector contract. It discards an intentionally preserved uncertainty signal instead of classifying its relevance. | Changes detector diagnostics and `INCOMPLETE` processing; may affect traces and future consumers and violates the frozen C0 contract. | Could unblock aggregation, but by paying an unjustified Single Requirement Analysis compatibility cost. | Reject. |
| B — preserve the diagnostic and add QB-specific materiality semantics | Separates global extraction state from whether the unresolved item can change the bounded cross-analysis operand. Uses the explicit C0 non-independent-role proof. | Preserves detector behavior, diagnostics, local calculators, records, and current aggregate profile; adds only future cross-analysis observability metadata and a narrow CRA-D067 amendment. | Enables the exact bounded end-to-end path while remaining fail-closed elsewhere. | Researcher-approved on 2026-09-25. |
| C — keep strict CRA-D067 unchanged | Maximally conservative but ignores the approved proof that exact C0 `500` cannot be an independent QB member. | No contract change. | Exact C0 inputs remain permanently `UNKNOWN`; the accepted QB rule cannot reach a computed end-to-end result through the only approved complete context surface. | Scientifically coherent but reject as the preferred boundary because it blocks a provably observable bounded case. |

Option B is researcher-approved on scientific, not implementation, grounds. It
preserves all evidence and uncertainty at their original layer while allowing
a downstream assessment to distinguish uncertainty relevant to its declared
operand from uncertainty proven irrelevant to that operand.

## 8. Minimum future end-to-end fixture

The following researcher-approved scientific target can become a binding
end-to-end reference case only after a separately authorized
implementation, validation, and audit round.

```text
R001: Час відгуку ≤ 2 с при 500 одночасних користувачах
R002: Час відгуку не нижче 5 с при 500 одночасних користувачах
```

### 8.1 Conditional expected extraction

| Component | R001 | R002 |
| --- | --- | --- |
| Metric | `Час відгуку [0,11)` | `Час відгуку [0,11)` under the approved, not-implemented LB-M-C0 bridge |
| Scalar | `≤ 2 с [12,17)`; `LESS_THAN_OR_EQUAL / INCLUSIVE`; `Decimal("2")`; `SECOND` | `не нижче 5 с [12,24)`; `GREATER_THAN_OR_EQUAL / INCLUSIVE`; `Decimal("5")`; `SECOND` |
| Context | `при 500 одночасних користувачах [18,49)` | `при 500 одночасних користувачах [25,56)` under the approved, not-implemented lower C0 rule |
| Diagnostic | preserved `500 [22,25)` | preserved `500 [29,32)` |
| Quantitative processing | unchanged `INCOMPLETE / DETECTED` | unchanged `INCOMPLETE / DETECTED` |
| QB-material unresolved extraction | none under the approved upper-C0 allowlist entry | none under the approved lower-C0 allowlist entry |

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

Approved post-implementation expected cross result:

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
- a researcher-approved future end-to-end validation target conditional on
  implementation authorization, Rule/Evidence ID allocation, implementation,
  regression verification, technical audit, and reference-corpus amendment.

## 9. Frozen Single Requirement Analysis invariant

The recommended solution must preserve all of the following:

| Frozen element | Required invariant |
| --- | --- |
| `C_i` | No formula, input-family, applicability, state, or value change. |
| `V_i` | Existing accepted lower scalar already establishes the same lower-tier evidence class; enrichment must not add a new class or contribution. |
| `U_i` | No vague-term observation, Finding, or calculation change. |
| Existing quantitative observations | Preserve every observation outside exact `LB-M-C0`; inside it, enrich the existing lower observation rather than duplicate or replace it. Standalone LB-M0 remains outside the bridge. |
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
| QB-ER-D001 | Is the current text-to-computed blocker real? | Current detector; model-spec Sections 7.14.6.6-8; accepted reference corpus; CRA-D067 | Confirm the two missing lower identity links plus the preserved C0 diagnostic and the original strict aggregate gate, which QB-ER-D009 now amends for QB materiality. | None; records observed baseline and the provenance of the approved amendment. | Retain as research premise. | `DIRECTLY_DERIVABLE` |
| QB-ER-D002 | May exact `Час відгуку` enrich the existing exact `не нижче` duration observation? | Separately source-attested metric and comparator; approved scalar forms; linked observation model | Approve only as part of the one closed `LB-M-C0` whole-input envelope in Section 3.2, enriching one existing observation. Standalone LB-M0 is not approved. | Adds metric Evidence/refs only together with the exact context bridge; preserves observation count, scalar, diagnostics, and C/V/U. | Approved with narrowing on 2026-09-25. | `RESEARCHER_APPROVED` |
| QB-ER-D003 | Should the bridge create a new observation? | Existing `QUANT-METRIC-001` enrichment pattern and component-union invariants | No; duplicate scalar observations would misrepresent one expressed bound. | Preserves current observation cardinality and scalar identity. | Require enrichment. | `DIRECTLY_DERIVABLE` |
| QB-ER-D004 | May the lower metric rule infer synonyms, tolerate variant envelopes, use a parser, or infer from units? | Current exact metric contract and explicit deferred boundaries | No; retain every negative boundary in Section 3.4. | Prevents broad RQD-008 expansion. | Reject every such broadening. | `REJECTED` |
| QB-ER-D005 | May exact C0 enrich the newly metric-linked lower observation? | Source-attested C0 role; approved exact C0 semantics; approved narrowed QB-ER-D002 | Approve a separate contract only for exact `LB-M-C0`, with Section 4 provenance and exclusions. | Adds context Evidence/refs; preserves existing C0 rule meaning, scalar, diagnostic, processing, and C/V/U. | Approved on 2026-09-25; implementation and identifiers remain absent. | `RESEARCHER_APPROVED` |
| QB-ER-D006 | May the existing C0 Rule ID silently cover the lower construction? | Immutable Rule ID policy; current C0 contract requires symbolic `QUANT-METRIC-001` | No. A future implementation must allocate new Rule IDs only after authorization. | Protects historical provenance and avoids semantic mutation. | Reject reuse or silent broadening. | `REJECTED` |
| QB-ER-D007 | Should the embedded-`500` diagnostic or `INCOMPLETE` state change? | Researcher-approved C0 contract | No; preserve both exactly. | Fully preserves Single Requirement Analysis extraction semantics. | Retain. | `DIRECTLY_DERIVABLE` |
| QB-ER-D008 | Can exact C0 `500` independently enter QB-v0.1? | Approved C0 statement that it is context, not an independent bound/observation/relation | No, for the exact approved C0 positive and only while that contract/version remains applicable. | Supplies the scientific proof required for a bounded materiality exception. | Use only through the fail-closed gates. | `DIRECTLY_DERIVABLE` |
| QB-ER-D009 | Should CRA-D067 distinguish global extraction incompleteness from QB-material incompleteness? | CRA-D067 rationale; exact C0 non-independent-role proof | Adopt the Section 6.2 amendment and the Section 5.3 allowlist containing exactly the existing upper C0 contract and approved lower C0 contract; preserve separate mandatory audit counts. | Changes only QB aggregate observability; local extraction, diagnostics, C/V/U, AGG-MVP-001, and current profile remain intact. | Approved on 2026-09-25. | `RESEARCHER_APPROVED` |
| QB-ER-D010 | Should C0 `500` be suppressed to enable computation? | Frozen C0 diagnostic and Single Requirement Analysis invariant | No. | Would change accepted extraction state and audit trace. | Reject Option A. | `REJECTED` |
| QB-ER-D011 | Should strict CRA-D067 remain unchanged despite the exact non-materiality proof? | Current approved decision | It remains the default, but should not remain exceptionless for exact C0. | Leaving it unchanged preserves compatibility but permanently blocks the exact C0 end-to-end aggregate. | Reject Option C as preferred solution. | `REJECTED` |
| QB-ER-D012 | Do R3 or F1-A solve the same-metric inclusive upper/lower response-time conflict? | Approved exact R3 and F1-A contracts | No; their grammar, representation, comparator, and identity differ. | None; both remain unimplemented and separate. | Do not use or broaden them here. | `DIRECTLY_DERIVABLE` |
| QB-ER-D013 | Can the Section 8 pair become a binding end-to-end conflict fixture after approval and implementation? | Approved QB identity/predicate/aggregate plus QB-ER-D002, D005, D009 | Yes, conditionally; expected result is conflict, participant set `{R001,R002}`, and `Fraction(0,1)`. | Requires future implementation, audit, and explicit corpus version/amendment; no current case is silently overwritten. | Adopt after all gates pass. | `DIRECTLY_DERIVABLE` |
| QB-ER-D014 | Are arbitrary metric/context linkage, variable populations, unit conversion, ranges, frequency, R3/F1-A implementation, or broader RQD-008 work opened? | Existing deferrals and this round's scope | No. | Keeps the research bridge minimal. | Defer. | `DEFERRED` |

Exactly three genuinely new scientific decisions are researcher-approved:
QB-ER-D002, QB-ER-D005, and QB-ER-D009. All other rows classify existing
authority, derive consequences, reject alternatives, or preserve deferrals.

## 12. Researcher Approval Checklist

- [x] **QB-ER-D002 — exact lower-bound metric enrichment.** Approved with
  narrowing only inside the closed `LB-M-C0` envelope, enriching the existing
  `QUANT-UK-001` `GREATER_THAN_OR_EQUAL / INCLUSIVE` duration observation with
  exact `Час відгуку` Evidence and no duplicate observation. Standalone LB-M0
  remains outside the bridge.
- [x] **QB-ER-D005 — exact lower-bound C0 enrichment.** Approved as a separate
  bounded rule that attaches exact `при 500 одночасних користувачах` Evidence
  to the QB-ER-D002 observation, with all provenance and negative boundaries
  in Section 4 and without changing the existing C0 rule.
- [x] **QB-ER-D009 — QB-specific materiality and CRA-D067 amendment.** Approved
  preservation of global `INCOMPLETE` and the diagnostic, with
  `QB_NON_MATERIAL` available only for the embedded `500` under either of the
  two allowlisted exact C0 contracts and every fail-closed gate in Section 5.3;
  separate global/material audit counts remain mandatory.

Completion of this checklist approves science only. It does not authorize
implementation, tests, Rule ID allocation, architecture, reporter changes,
reference-corpus edits, a merge, baseline, tag, or release.

## 13. End-of-round report

1. **Branch:** `research/cross-requirement-analysis`.
2. **Files finalized:** this readiness record, the Consistency decision
   package, the mixed reference corpus, and the prospective model
   specification; no production source or tests changed.
3. **Exact blocker classification:** two `IMPLEMENTATION_LIMITATION` identity
   gaps plus two `ALREADY_RESEARCHER_APPROVED` strictness conditions: preserved
   C0 diagnostic/`INCOMPLETE` processing and the original strict CRA-D067
   propagation, now amended by QB-ER-D009.
4. **Lower-bound metric linkage:** researcher-approved only inside exact
   `LB-M-C0`; standalone LB-M0 is not approved.
5. **Lower-bound context linkage:** researcher-approved through a separate
   exact lower-C0 contract; production remains `NOT_IMPLEMENTED` with Rule and
   Evidence IDs `NOT_ALLOCATED`.
6. **C0 `500` treatment:** preserve diagnostic and global `INCOMPLETE`; the
   exact, audited `QB_NON_MATERIAL` classification is approved only under the
   two-entry allowlist and Section 5.3 gates.
7. **CRA-D067:** narrowly amended; strict behavior remains the default for
   every other unresolved extraction.
8. **Frozen Single Requirement Analysis:** can remain intact, including current
   local numeric values, diagnostics, records, profile, AGG-MVP-001, and
   reporting meaning.
9. **New researcher decisions approved:** 3 — QB-ER-D002, QB-ER-D005, and
   QB-ER-D009.
10. **Final status:** the first bounded QB-v0.1 scientific slice is complete;
    the next authorized phase is Architecture Contract.

RESEARCH_COMPLETE_READY_FOR_ARCHITECTURE
