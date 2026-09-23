# SRM-05F — Exact Frequency Scientific Approval Proposal

**Issue:** #73 (`SRM-05`)  
**Document status:** `PROPOSED_FOR_RESEARCHER_REVIEW`  
**Proposal scope:** one exact source-backed frequency construction  
**Decision effect:** none; no researcher approval is recorded  
**Implementation effect:** none; production implementation is prohibited in
issue #73  
**Identifier effect:** none; no Rule ID or Evidence ID is allocated

This document prepares one bounded F1 decision for the source construction
`не рідше одного разу на 5 с`. It proposes an exact clause boundary and a
source-level interpretation, and it exposes two scientific approval gates that
must be decided together: whether the governing action phrase is an exact
metric, and whether F1 enters the ordinary quantitative-observation collection
consumed by Verifiability. The proposal does not approve either gate, authorize
implementation, broaden the protected frequency exclusion, or alter any
current production detector, diagnostic, calculator, reporter, or aggregator.

## 1. Source and provenance

### 1.1 Original source

The original application-example DOCX was inspected directly:
[`reference/Приклад_застосування_моделі.docx`](reference/Приклад_застосування_моделі.docx),
§8, Table 7, row `R1 → R1′`.

The exact second-cell text is 206 Unicode code points:

```text
Замість «у реальному часі»: координати активного транспортного засобу повинні оновлюватися не рідше одного разу на 5 с; 95-й перцентиль затримки від отримання GPS-події до відображення в UI — не більше 3 с.
```

All whitespace in this cell is U+0020 SPACE. The editorial prefix ends with
U+003A COLON. The two refined clauses are separated by U+003B SEMICOLON and one
U+0020 SPACE. The second clause contains U+2014 EM DASH and the cell ends with
U+002E FULL STOP.

The table cell decomposes into:

```text
editorial prefix [0,28):
Замість «у реальному часі»: 

refined requirement text [28,206):
координати активного транспортного засобу повинні оновлюватися не рідше одного разу на 5 с; 95-й перцентиль затримки від отримання GPS-події до відображення в UI — не більше 3 с.
```

The refined text without the editorial prefix is 178 code points. It is the
working R1′ requirement view reflected by the authoritative
[`model-spec.md`](model-spec.md) traceability offsets:

```text
координати активного транспортного засобу повинні оновлюватися не рідше одного разу на 5 с; 95-й перцентиль затримки від отримання GPS-події до відображення в UI — не більше 3 с.
```

Within that 178-code-point view:

- the first clause is `[0,90)`;
- the frequency substring is `[63,90)`;
- the semicolon is `[90,91)`;
- the following space is `[91,92)`;
- the percentile metric phrase is `[92,161)`;
- the existing accepted `не більше 3 с` scalar is `[164,177)`; and
- the final period is `[177,178)`.

The original table cell is source evidence. The authoritative implementation
model remains the source of approved production behavior.

### 1.2 Protected current behavior

The first-production scalar baseline currently protects the shape

```text
не рідше одного разу на <approved numeric value> <approved duration unit>
```

before value-plus-unit fallback. For the source `не рідше одного разу на 5 с`,
the nested `5 с` therefore creates no Evidence, observation, or unresolved
numeric-candidate diagnostic. The protected span itself creates no Evidence,
observation, or diagnostic. If no other scalar is present, processing is
`COMPLETE` and the derived outcome is `NOT_DETECTED`. This means that the
first-production baseline accepted no anchor; it does not mean that the source
has no quantitative meaning.

This proposal preserves:

- `QUANT-001` and `QUANT-UK-001` grammar, Evidence, precedence, diagnostics,
  and observation identity;
- `QUANT-METRIC-001` and `QUANT-CONTEXT-001`, including the exact C0 `500`
  diagnostic;
- exact R3 as `RESEARCHER_APPROVED / NOT_IMPLEMENTED /
  RULE_ID_NOT_ALLOCATED`;
- the protected variable-value/unit frequency exclusion outside the exact F1
  positive proposed here;
- `ACCEPT-QUANT-001` and all condition/result behavior;
- current processing-outcome derivation;
- all current C/V/U formulas, Findings, `QUALITY_PROBLEM`, reporter, and
  aggregation rules. Section 7.4 explicitly discloses that ordinary F1
  quantitative evidence can nevertheless change Verifiability outputs under
  those unchanged rules; and
- `RQD-008` and issue #73 as open.

## 2. Exact boundary alternatives

Three boundaries were evaluated. Offsets are zero-based Unicode code-point
ranges `[start,end)`.

### 2.1 Alternative A — frequency substring only

Exact text, 27 code points:

```text
не рідше одного разу на 5 с
```

| Aspect | Assessment |
| --- | --- |
| Scientific meaning | Preserves the recurrence expression but omits what is updated. It cannot by itself distinguish coordinate-update frequency from another behavior using the same words. |
| Evidence boundary | `[0,27)` when supplied alone; `[63,90)` in the refined 178-code-point requirement; `[91,118)` in the original 206-code-point table cell. |
| Semicolon | The semicolon is outside the substring: `[90,91)` in the refined requirement and `[118,119)` in the original cell. |
| Standalone input | A standalone substring would contain the frequency phrase but no expressed update behavior. A positive observation would necessarily have `metric = None`, or would require inference from absent text. |
| Whole source cell | The substring is locally identifiable, but accepting it without the governing clause would ignore the editorial prefix and the behavior it modifies. |
| Existing other observations | The following `не більше 3 с` scalar remains independently accepted at `[164,177)` in the refined requirement or `[192,205)` in the original cell. |
| Positive case | Only the exact 27-code-point substring. |
| Negative boundary | Any attempt to infer `координати ... оновлюватися` as its metric would lack Evidence in the chosen boundary. |

Alternative A is not proposed. It preserves the surface recurrence phrase but
not the source's explicit statement that the frequency applies to coordinate
updates.

### 2.2 Alternative B — refined frequency clause

Exact text, 90 code points:

```text
координати активного транспортного засобу повинні оновлюватися не рідше одного разу на 5 с
```

| Aspect | Assessment |
| --- | --- |
| Scientific meaning | Preserves both the behavior being constrained and the complete recurrence phrase. It states a frequency condition on coordinate updates without importing the later percentile metric. |
| Evidence boundary | `[0,90)` when supplied as a standalone refined requirement or in the 178-code-point refined R1′ view; `[28,118)` as a source slice of the original table cell. |
| Semicolon | The semicolon at refined offset `[90,91)` is a hard boundary and is excluded. The following percentile clause cannot establish, modify, or invalidate the frequency relationship. |
| Standalone input | The exact 90-code-point clause has complete source-level meaning and can be represented without outside text. It is an exact source-derived clause, although the DOCX attests it inside the larger cell rather than as a separate cell. |
| Refined multi-clause input | In the exact 178-code-point refined R1′ requirement, the first clause retains `[0,90)` and the later scalar remains independent across the semicolon. |
| Whole source cell | If the 206-code-point table cell is ingested literally, the clause begins at offset 28 rather than requirement start. The proposed exact F1 rule does not strip the editorial prefix and therefore does not match that input. |
| Existing other observations | In the exact refined R1′ input, `не більше 3 с` remains a distinct `QUANT-UK-001` observation at `[164,177)`. It is not a frequency member or metric. |
| Positive cases | The exact 90-code-point clause as the whole trimmed input; or the exact 178-code-point refined R1′ input containing this first clause and the exact source second clause. |
| Negative boundary | The substring alone, the original cell with the editorial prefix, an arbitrary changed suffix after the semicolon, or any code-point change inside the clause does not satisfy the exact proposed envelope. |

Alternative B is proposed. It is the smallest boundary that preserves the
source's update behavior and frequency expression while respecting the
semicolon as a hard boundary.

### 2.3 Alternative C — entire source table-cell wording

Exact text is the 206-code-point original cell quoted in §1.1.

| Aspect | Assessment |
| --- | --- |
| Scientific meaning | Combines editorial replacement prose, the coordinate-update frequency clause, and a separate percentile-latency clause. The cell describes two refinements, not one quantitative observation. |
| Evidence boundary | `[0,206)` if taken literally. The frequency clause is only the nested slice `[28,118)`. |
| Semicolon | The boundary crosses the semicolon at `[118,119)`, contrary to the current hard-boundary policy for quantitative linkage. |
| Standalone input | Requiring the editorial prefix would make source-table presentation text part of a software requirement. It would reject the refined requirement text already used by the model. |
| Whole source cell | Exact whole-cell equality is possible mechanically, but one Evidence span would conflate provenance prose, frequency, percentile metric, and duration scalar. |
| Existing other observations | The existing `не більше 3 с` observation at `[192,205)` would overlap a whole-cell frequency Evidence item and risk being treated as part of the frequency construction. |
| Positive case | Only the exact table cell, including editorial prefix and later clause. |
| Negative boundary | The actual refined 178-code-point requirement and the standalone 90-code-point clause would fail despite preserving the frequency meaning. |

Alternative C is not proposed. It is source-exact at the artifact-cell level
but not scientifically exact at the individual frequency-requirement level.

### 2.4 Proposed exact input envelope

The proposed boundary is Alternative B with exactly two permitted complete
input envelopes:

1. the exact 90-code-point clause in §2.2 as the complete trimmed
   `Requirement.text`; or
2. the exact 178-code-point refined R1′ text in §1.1, where the same clause is
   `[0,90)`, the semicolon is `[90,91)`, and the exact source percentile clause
   follows.

This is one clause contract with two explicitly bounded source envelopes, not
a clause-search grammar. It does not accept the frequency clause at arbitrary
positions, after arbitrary prefixes, or before arbitrary suffixes. It does not
accept the 206-code-point editorial table cell. A researcher may narrow the
proposal to the 178-code-point envelope only, but no broader clause-local
search is proposed.

## 3. Frequency semantics

### 3.1 Source-level interpretation

The exact proposed interpretation is:

> The coordinate-update behavior is constrained to occur not less frequently
> than the source-stated recurrence `одного разу на 5 с`.

This interpretation preserves distinct roles:

| Source element | Proposed role | Explicit non-meaning |
| --- | --- | --- |
| `координати активного транспортного засобу повинні оновлюватися` | Exact behavior whose update frequency is constrained | Not a generated metric vocabulary or a reusable action-pattern rule. |
| `не рідше` | Comparator label `NOT_LESS_FREQUENT` applied only within this exact construction | Not `LESS_THAN_OR_EQUAL`, `GREATER_THAN_OR_EQUAL`, or an arithmetic operator. |
| `одного разу` | Fixed grammatical material needed to preserve the source recurrence construction | Not parsed as numeric `1`; `разу` is not a count unit. |
| `на` | Fixed relation token connecting the occurrence phrase to the stated interval | Not a division operator. |
| `5` | Exact interval magnitude retained as `Decimal("5")` | Not a frequency value, count, threshold conversion, or generalized numeric slot. |
| `с` | Exact source unit normalized to `SECOND` | Not hertz, reciprocal seconds, or permission to convert units. |

The numeric value `5` and unit `SECOND` describe the interval parameter stated
inside the source recurrence. The comparator remains
`NOT_LESS_FREQUENT` with `inclusivity = None` because the construction expresses
frequency, not an endpoint-inclusion decision. The proposal stores no numeric
frequency and performs no calculation.

The proposal does not convert the source to any of the following:

```text
≤ 5 с
≥ 1
1/5 Hz
```

It also does not assert a general mathematical equivalence between update
frequency and a duration bound. The raw Evidence remains necessary to explain
that `5 SECOND` is the stated recurrence interval rather than the measured
frequency value.

### 3.2 What remains absent

The bounded interpretation supplies no:

- general written-number value for `одного`;
- count component or count-unit ontology;
- rate, reciprocal, hertz value, or compound unit;
- unit conversion;
- tolerance, clock, scheduling, jitter, delay, or missed-update policy;
- sampling or measurement procedure;
- observation window or aggregation rule;
- pass/fail algorithm;
- generated synonym, morphology, or numeric/unit variant; or
- meaning for any non-exact `не рідше` phrase.

These absences do not make the exact frequency meaning unresolved. They delimit
what either proposed F1 record means and what no consumer may infer from it.

### 3.3 Metric-role approval gate

The source and current model establish two facts without resolving the proposed
component assignment:

1. Section 7.14.6.4 names **update frequency** in R1′ as a source-attested
   metric expression; and
2. the current implemented metric contract, `QUANT-METRIC-001`, approves only
   the exact nominal metric `Час відгуку` and explicitly forbids inference of a
   broader noun-phrase or semantic metric grammar.

The current structural implementation also recognizes the complete first
clause `[0,90)` as an `expected_result`. That does not decide whether its
action-only prefix `[0,62)` is additionally an explicit quantitative metric.
Feature overlap is permitted only when each role has its own scientific
justification.

The required researcher choice is:

| Metric-role option | Scientific reading of `[0,62)` | Representation consequence | Boundary |
| --- | --- | --- | --- |
| **M-A — exact bounded metric** | Approve `координати активного транспортного засобу повинні оновлюватися` as the exact object/behavior whose update frequency is constrained. The frequency anchor supplies the measurement dimension; the action phrase supplies what is measured. | The phrase may populate the existing `metric: TextComponent` only in the exact F1 envelopes. | This is a one-source exception. It creates no reusable action-to-metric grammar and does not broaden `QUANT-METRIC-001`. |
| **M-B — separate behavior role** | Treat `[0,62)` only as the required update behavior. The metric is update frequency as expressed by the whole relationship, not by the action phrase alone. | The existing scalar observation shape cannot store this role without mislabeling it as `metric`; a separate role-aware frequency record is required. | The behavior role is exact and source-bound. It creates no actor/action/object model or generic behavior grammar. |
| **M-C — F0 deferral** | Do not decide that the phrase is a metric or introduce a behavior role. | Create no positive F1 representation. | Preserve the current exclusion and all production outputs. |

M-A is scientifically defensible only if the researcher accepts that an
explicitly named update behavior is a sufficient metric component for this
exact frequency construction. Source attestation of update frequency supports
that decision but does not grant it automatically. M-B is scientifically
defensible if the researcher distinguishes the expected behavior from the
measure applied to it. This proposal does not choose between M-A and M-B.

## 4. Representation alternatives

### 4.1 Alternative A — ordinary quantitative observation

This alternative requires metric-role option M-A. If the researcher explicitly
approves `[0,62)` as the bounded metric, the existing
`QuantitativeConstraintObservation` can carry the exact source-level meaning:

```text
feature_id = QUANTITATIVE_CONSTRAINT

metric = TextComponent(
    evidence_refs=(<future exact update-behavior Evidence ref>,)
)

comparator = ComparatorComponent(
    label=NOT_LESS_FREQUENT,
    inclusivity=None,
    evidence_refs=(<future exact frequency-anchor Evidence ref>,)
)

value = NumericValueComponent(
    decimal_value=Decimal("5"),
    evidence_refs=(<future exact frequency-anchor Evidence ref>,)
)

unit = UnitComponent(
    label=SECOND,
    evidence_refs=(<future exact frequency-anchor Evidence ref>,)
)

context = None
unresolved_components = ()

evidence_refs = (
    <future exact update-behavior Evidence ref>,
    <future exact frequency-anchor Evidence ref>,
)
```

The angle-bracketed descriptions are semantic placeholders, not allocated
identifiers. Co-residence in one observation records that the exact update
behavior is governed by the exact frequency construction. The fixed words
`одного разу на` remain in the frequency-anchor Evidence and require no new
component.

This is an **ordinary accepted observation in
`RequirementFeatures.quantitative_constraints`**. Consequently it is eligible
for existing `CALC-V-MVP-001` lower-tier consumption. That consequence is part
of this alternative, not an implementation detail and not avoidable merely by
leaving the calculator formula unchanged. Section 7.4 states the exact current
input consequences. The combination remains valid only under §2.4 and creates
no generic frequency model.

### 4.2 Alternative B — separate non-consumed frequency record

A dedicated exact record would require metric-role option M-B and separately
name:

- exact update-behavior Evidence;
- comparator surface;
- fixed occurrence phrase;
- interval value and unit; and
- their exact relationship.

The record would belong scientifically to feature family
`QUANTITATIVE_CONSTRAINT`, and its two Evidence items would retain that feature
family, but the record must be stored in a separate bounded tuple associated
with the quantitative-family extraction result. It must **not** be inserted
into `RequirementFeatures.quantitative_constraints`, because that existing
collection is consumed by `CALC-V-MVP-001` as accepted lower-tier evidence.

Minimum additional representation requirements are:

1. one exact, role-aware record type with a behavior Evidence reference,
   frequency-anchor Evidence reference, `NOT_LESS_FREQUENT`, interval value
   `Decimal("5")`, and unit `SECOND`;
2. a separate zero-or-one record collection whose non-consumption by current
   calculators and `ACCEPT-QUANT-001` is binding;
3. validation that both Evidence items belong to the same requirement and
   exact envelope and round-trip to `[0,62)` and `[63,90)`;
4. stable source ordering and a processing outcome for the new record without
   changing the existing `quantitative_constraints` outcome; and
5. future domain/type/field names and ownership identifiers, all still
   unallocated.

This adds a bounded representation even though F1 does not join existing scalar
members as R3 does. The extra structure is scientifically justified only if
preserving the behavior/metric distinction and current C/V/U inputs is required.
It is not a generic relationship framework, expression tree, frequency model,
actor/action/object model, or reusable attachment grammar.

### 4.3 Alternative C — explicit deferral

Deferral remains scientifically valid if the researcher rejects both the exact
metric role and the additional separate behavior representation, or does not
approve the downstream consequence of an ordinary observation. The current
exclusion then remains unchanged and no positive F1 record is created.

### 4.4 Coherent approval packages

The proposal defines two coherent F1 packages and one deferral package:

| Package | Metric decision | Representation decision | Existing downstream consumption |
| --- | --- | --- | --- |
| **F1-A** | M-A: `[0,62)` is an exact bounded metric | Alternative A: ordinary `QuantitativeConstraintObservation` | Yes. Existing `CALC-V-MVP-001` consumes it as lower-tier quantitative evidence; `ACCEPT-QUANT-001` does not. |
| **F1-B** | M-B: `[0,62)` is an exact behavior role | Alternative B: separate role-aware frequency record | No. The record is outside `quantitative_constraints` and outside every current calculator and acceptance input. |
| **F0** | M-C: no new role decision | Alternative C: explicit deferral | No change. |

This proposal does not select F1-A or F1-B. A cross-combination is not defined:
placing a behavior role into the existing `metric` field would mislabel it, and
placing an approved metric into a separate non-consumed record would require a
third scientific rationale not prepared here. If neither coherent F1 package
is approved in full, the disposition is F0.

## 5. Protected exclusion compatibility

### 5.1 Coexistence rule

The current protected exclusion remains the default for the full approved
variable-value/unit shape. A future positive exact F1 rule would coexist as
follows:

1. Evaluate the exact F1 input envelopes in §2.4 without changing the current
   scalar candidate-precedence order.
2. If an exact F1 envelope matches, create exactly one record under the
   explicitly selected F1-A or F1-B package and mark its `[63,90)` frequency
   span as positively consumed by F1.
3. The contained `5 с` remains ineligible for `QUANT-001` value-plus-unit
   fallback, exactly as it is under the current exclusion. No duplicate scalar
   observation is created.
4. For every F1 non-match, apply the already approved protected exclusion and
   scalar baseline exactly as they operate now.
5. Do not turn the protected variable-value/unit exclusion into a positive
   recognizer. Forms such as `не рідше одного разу на 6 с` or
   `не рідше одного разу на 5 хв` remain protected exclusions, not F1
   observations.

The positive rule therefore supersedes the exclusion only for the exact source
span in one of the two exact input envelopes. This is the same under F1-A and
F1-B. It does not delete, narrow, or redefine the broader exclusion.

### 5.2 Unchanged scalar precedence

The global scalar order remains:

```text
1. Ukrainian lexical comparator candidate
2. symbolic comparator candidate
3. value + unit fallback
```

F1 is a separate exact gate before fallback eligibility, not a seventh
`QUANT-UK-001` lexical comparator and not a global fourth scalar-precedence
category. It creates no permission to recognize other `не рідше` forms.

In the exact 178-code-point R1′ input, the selected F1 record and the existing
`не більше 3 с` observation are distinct. Under F1-A they are two ordinary
quantitative observations; under F1-B only the later scalar remains in
`quantitative_constraints`. The semicolon prevents role, component, or Evidence
sharing between them.

## 6. Proposed Evidence contract

### 6.1 Evidence items

An exact positive would create exactly two accepted Evidence items in feature
family `QUANTITATIVE_CONSTRAINT`. Their final IDs and producing Rule ID remain
`NOT_ALLOCATED`.

| Role | Exact text | Span in the 90- or 178-code-point proposed input | Feature | Allocation status |
| --- | --- | --- | --- | --- |
| Update behavior (F1-B) or exact bounded metric (F1-A) | `координати активного транспортного засобу повинні оновлюватися` | `[0,62)` | `QUANTITATIVE_CONSTRAINT` | Future Rule ID and Evidence ID `NOT_ALLOCATED` |
| Frequency anchor | `не рідше одного разу на 5 с` | `[63,90)` | `QUANTITATIVE_CONSTRAINT` | Future Rule ID and Evidence ID `NOT_ALLOCATED` |

The U+0020 SPACE at `[62,63)` separates the role spans and is not separately
stored. The exact construction boundary is their enclosing clause `[0,90)`.
The semicolon in the 178-code-point input is outside the Evidence contract.

For provenance only, the analogous slices in the original 206-code-point table
cell are update behavior `[28,90)`, frequency anchor `[91,118)`, and enclosing
clause `[28,118)`. Those offsets do not become accepted F1 Evidence because the
editorial whole-cell input is a deterministic F1 non-match.

### 6.2 Role/component references and source order

Under F1-A, the `metric` component references `[0,62)`, while comparator,
value, and unit reference the complete frequency-anchor Evidence `[63,90)`.
Under F1-B, the separate record's `behavior` role references `[0,62)`, while
its comparator and interval members reference `[63,90)`. No option creates a
component Evidence substring for `5`, `с`, or `одного`; the complete anchor
preserves the exact source roles.

The selected F1 record's top-level Evidence sequence is the same stable,
de-duplicated, source-ordered union in either package:

```text
(
    <future exact update-behavior Evidence ref>,  # [0,62)
    <future exact frequency-anchor Evidence ref>, # [63,90)
)
```

Both Evidence items must:

- belong to the same requirement and the same future exact F1 rule;
- round-trip exactly to their slices of trimmed `Requirement.text`;
- use distinct future identities and rule-local source-order ordinals;
- remain separate from any condition, result, acceptance, or later percentile
  Evidence; and
- participate only in the one selected F1 record. Under F1-A that record is an
  ordinary quantitative observation; under F1-B it is the separate frequency
  record.

### 6.3 Cardinality and coexistence

The proposed cardinality is zero or one F1 record per requirement. An accepted
record has exactly one update-behavior/metric Evidence item and one
frequency-anchor Evidence item.

For the exact 178-code-point refined R1′ input, F1-A ordinary quantitative
observation order is:

1. the F1-A observation, whose earliest Evidence begins at `0`; and
2. the unchanged `QUANT-UK-001` observation for `не більше 3 с` at
   `[164,177)`.

Under F1-B, the separate F1 record is source-ordered before the unchanged
ordinary scalar, but it is not inserted into the ordinary observation tuple.
No Evidence item is shared or merged. The percentile metric candidate at
`[92,161)` remains outside this proposal.

## 7. Status and diagnostic behavior

### 7.1 Exact positive

When either exact input envelope in §2.4 matches and every Evidence invariant
is satisfied, the common proposed outcome is:

- exactly one F1 record under the researcher-selected package;
- exactly two F1 Evidence items;
- no F1-specific diagnostic;
- no nested `5 с` fallback observation;
- no numeric diagnostic for `5`; and
- an exact positive rather than the protected exclusion for `[63,90)`.

Under F1-A, the record is an ordinary quantitative observation, so the
existing quantitative family is `COMPLETE / DETECTED`. Under F1-B, the new
separate record outcome is complete and detected, while the existing
`quantitative_constraints` outcome remains whatever the approved scalar rules
produce. The exact field carrying the F1-B outcome is one of that option's
additional representation requirements.

For the 178-code-point input, the independent `не більше 3 с` observation is
also preserved. Its presence does not change the F1 record count or Evidence.

### 7.2 Deterministic F1 non-match

A deterministic F1 non-match creates:

- no F1 record;
- no F1 Evidence;
- no F1-specific diagnostic; and
- no change to any existing scalar observation, Evidence, diagnostic,
  processing status, or derived outcome.

After a non-match, the existing protected exclusion and scalar rules run
unchanged. Therefore a form can be an F1 non-match while still being
deterministically protected from fallback by the broader existing exclusion.
Conversely, a change that also breaks the protected exclusion is handled only
by the already approved scalar baseline; this proposal does not prescribe a
new fallback or diagnostic result.

### 7.3 Mixed accepted and unresolved outcomes

The two binding positive inputs contain no unresolved numeric candidate. The
proposal nevertheless preserves the existing family-wide outcome table:

| Accepted observations | Existing unresolved candidates | Processing | Derived outcome |
| --- | --- | --- | --- |
| Present | None | `COMPLETE`, no diagnostics | `DETECTED` |
| None | None | `COMPLETE`, no diagnostics | `NOT_DETECTED` |
| None | Present | `INCOMPLETE`, existing diagnostics | `UNRESOLVED` |
| Present | Present | `INCOMPLETE`, existing diagnostics | `DETECTED` |

For F1-A, the table applies directly to the ordinary quantitative family. If an
independently approved detector produces an unresolved candidate in the same
requirement, F1-A neither suppresses nor resolves it. For F1-B, the separate F1
record does not convert, suppress, or resolve an unresolved candidate in the
ordinary quantitative family. No new frequency ambiguity diagnostic,
diagnostic code, or existing-family processing transition is proposed.

### 7.4 Acceptance and downstream approval gate

#### 7.4.1 `ACCEPT-QUANT-001`

Neither F1 package enters the current `ACCEPT-QUANT-001` composition:

- F1-A Evidence would be owned by a future F1 rule, while the authoritative
  acceptance contract admits a quantitative scalar anchor only when its scalar
  Evidence is owned by `QUANT-001` or `QUANT-UK-001`. Metric/context Evidence
  may supplement those anchors, but cannot replace the required scalar owner.
- `NOT_LESS_FREQUENT` with `inclusivity = None` is not one of the comparator
  meanings currently judgeable by `ACCEPT-QUANT-001`. The approved comparator
  path is limited to inclusive `LESS_THAN_OR_EQUAL` or
  `GREATER_THAN_OR_EQUAL`; the comparator-free path requires an existing
  value-plus-unit scalar anchor.
- F1-B is outside the ordinary quantitative-observation collection and is not
  an acceptance input at all.

Therefore F1 creates no acceptance observation, acceptance Evidence, or
acceptance diagnostic. Its Evidence must not reuse a `QUANT-001`,
`QUANT-UK-001`, `RESULT-UK-001`, or `ACCEPT-QUANT-001` identity. The currently
approved result containment, judgeability, Evidence ownership, criterion
deduplication, and mixed acceptance outcome rules remain unchanged. Any future
decision to make frequency judgeable as an acceptance criterion is a separate
scientific change and is not implied by F1-A's Verifiability effect.

#### 7.4.2 `CALC-V-MVP-001` and exact input consequences

`CALC-V-MVP-001` tests whether the ordinary `quantitative_constraints` outcome
contains any accepted observation; it does not filter those observations by
producing Rule ID, comparator, metric type, or scientific subtype. An ordinary
F1-A observation is therefore existing lower-tier Verifiability evidence. An
unchanged formula does **not** imply unchanged output when its accepted input
set changes.

The current implementation produces the following baseline evidence for the
two exact envelopes:

| Exact input | Current relevant evidence | Current `V_i` | F1-A consequence, holding all other detector outcomes fixed | F1-B consequence, holding all other detector outcomes fixed |
| --- | --- | --- | --- | --- |
| Standalone 90-code-point clause | `RESULT-UK-001` expected result `[0,90)`; quantitative, acceptance, and verification-method families complete with no observation | `COMPUTED / 0` | F1-A adds accepted lower-tier quantitative evidence; acceptance remains complete/absent, so `V_i = 1/2`. | Separate record is not consumed; `V_i` remains `0`. |
| Exact 178-code-point refined R1′ | `RESULT-UK-001` expected result `[0,90)`; one `QUANT-UK-001` observation `не більше 3 с` at `[164,177)`; acceptance and verification-method families complete with no observation | `COMPUTED / 1/2` | F1-A adds a second lower-tier observation, but repeated lower-tier evidence does not increase the class; `V_i` remains `1/2`. | Separate record is not consumed; the existing scalar continues to establish `V_i = 1/2`. |

These are exact-input consequences under the currently approved and observed
other detector outcomes, not unconditional scores for every future extraction
state. The authoritative precedence still applies:

- any accepted acceptance criterion yields `V_i = 1`;
- an incomplete acceptance family with no accepted criterion withholds the
  result as `UNKNOWN`, even if lower-tier evidence is present, because the
  candidate could change the class to `1`;
- absent accepted acceptance evidence, one or more accepted lower-tier paths
  yield `1/2`; and
- unresolved lower-tier candidates cannot change `1/2` once F1-A is accepted,
  but can withhold a would-be `0` when no lower-tier path is accepted.

F1-A therefore potentially changes the displayed requirement Verifiability
value and, through `AGG-MVP-001`, the exact `V_file` mean and its displayed
aggregate. For the standalone exact clause under the current evidence state,
the computed contribution changes from `0` to `1/2`; the aggregate denominator
is unchanged because the requirement remains `COMPUTED`, but the aggregate
numerator and mean can change. The exact 178-code-point input already
contributes `1/2`, so F1-A does not change its class under the current evidence
state. F1-B preserves both current values because its record is non-consumed.

Neither package changes the C/V/U formulas. F1-A changes a Verifiability input
and can therefore change Verifiability requirement and specification outputs;
it does not directly change Completeness or Unambiguity inputs. Neither package
creates a Finding or `QUALITY_PROBLEM`. F1-B additionally preserves all current
C/V/U inputs, reporter values, and aggregates by construction.

## 8. Exact positive and negative cases

`SOURCE_ATTESTED` identifies text present verbatim in the original DOCX, either
as the complete table cell or as an exact contiguous slice of that cell.
`SOURCE_DERIVED_EXACT_CLAUSE` identifies the exact first clause extracted from
that source. `SYNTHETIC_TEST_CASE` identifies a constructed boundary case and
is not scientific evidence for expansion.

| Case | Input or change | Classification | Proposed F1 disposition | Existing baseline behavior to preserve |
| --- | --- | --- | --- | --- |
| Standalone exact clause | Exact 90-code-point clause in §2.2 | `SOURCE_DERIVED_EXACT_CLAUSE` | Positive only under an approved package: F1-A creates one ordinary observation; F1-B creates one separate record. Both create the same two Evidence items. | F1 consumes the exact frequency span; no `5 с` fallback or diagnostic. F1-A supplies lower-tier Verifiability evidence; F1-B does not. |
| Exact refined R1′ | Exact 178-code-point text in §1.1 | `SOURCE_ATTESTED` as the exact contiguous DOCX slice `[28,206)`; matches authoritative model offsets | Positive for the first clause only under approved F1-A or F1-B; semicolon excluded. | Preserve separate `не більше 3 с` observation at `[164,177)` and no cross-boundary linkage. Current `V_i = 1/2` remains `1/2` under either package, holding other detector outcomes fixed. |
| Frequency substring alone | `не рідше одного разу на 5 с` | Source substring supplied as standalone boundary case | F1 non-match because update behavior is absent. | Existing protected exclusion yields no observation or diagnostic; absent another candidate, `COMPLETE / NOT_DETECTED`. |
| Original full table cell | Exact 206-code-point cell including `Замість ...:` | `SOURCE_ATTESTED` artifact wording | F1 non-match because the selected clause is not at requirement start and the whole cell is not an approved input envelope. | Preserve protected frequency exclusion and the independent later scalar under existing offsets for that input. |
| Final period after standalone clause | Append `.` to the exact 90-code-point clause | `SYNTHETIC_TEST_CASE` | F1 non-match; punctuation differs. | The protected exclusion can still account for the inner frequency phrase; no positive F1 record. |
| Changed casing or whitespace | Change case or replace a U+0020 space | `SYNTHETIC_TEST_CASE` | F1 non-match because the positive grammar is literal. | The current casefold/Unicode-whitespace-tolerant protected exclusion remains independently applicable when its own contract still matches. |
| Changed interval value | Replace `5` with `6` | `SYNTHETIC_TEST_CASE` | F1 non-match; no variable value slot. | Existing variable-value protected exclusion remains applicable; do not create a positive frequency record. |
| Changed approved duration unit | Replace `с` with `хв`, `секунд`, or `хвилин` | `SYNTHETIC_TEST_CASE`; unit surfaces independently approved elsewhere | F1 non-match; no unit variants. | Existing protected exclusion remains applicable; scalar grammar is not broadened. |
| Unsupported duration unit | Replace `с` with `мс` | `SYNTHETIC_TEST_CASE` | F1 non-match. | Existing exclusion and scalar detector alone determine fallback or unresolved-candidate behavior; F1 adds nothing. |
| Changed fixed phrase | Replace or omit `одного`, `разу`, or `на` | `SYNTHETIC_TEST_CASE` | F1 non-match; no written-number or count grammar. | If the protected exclusion also fails, existing baseline behavior applies without F1 repair. |
| Added material inside clause | Insert an adjective, adverb, punctuation mark, parenthesis, or another numeric candidate | `SYNTHETIC_TEST_CASE` | F1 non-match; exact code-point sequence and cardinality differ. | Preserve all independently accepted observations or diagnostics. |
| Hard boundary inside clause | Insert `.`, `;`, `?`, or `!` before the frequency anchor ends | `SYNTHETIC_TEST_CASE` | F1 non-match; no cross-boundary relationship. | Existing clause and scalar rules run unchanged. |
| Changed following percentile clause | Keep the first 90 code points but alter the suffix after the semicolon | `SYNTHETIC_TEST_CASE` | F1 non-match because only the exact refined R1′ envelope is proposed for the multi-clause form. | Existing frequency exclusion and all scalar behavior for the changed suffix remain unchanged. |
| Additional frequency occurrence | Duplicate the frequency clause or add a competing `не рідше` construction | `SYNTHETIC_TEST_CASE` | F1 non-match; zero-or-one exact cardinality is violated. | Do not select by position, proximity, or order. |
| Arithmetic reinterpretation | Replace the phrase with `≤ 5 с`, `≥ 1`, or `1/5 Hz` | Unsupported inference | F1 non-match and prohibited equivalence. | Independently approved scalar rules may process only their own exact forms; no F1 semantic transfer. |

The negative cases bind only F1 non-match behavior. They do not rewrite the
current protected exclusion or pre-approve tests for an implementation task.

## 9. F0 F1 F2 decision matrix

| Option | Metric-role decision | Representation and Evidence | Acceptance / Verifiability effect | Exclusion and diagnostic effect | Compatibility risk | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| **F0 — retain exclusion and defer positive recognition** | No metric or behavior-role approval. | No new representation or Evidence. | No acceptance or C/V/U input change. | Protected exclusion, no frequency record, and no frequency diagnostic remain unchanged. | Lowest technical risk; preserves deliberate semantic under-coverage. | `READY_FOR_RESEARCHER_REVIEW` as explicit deferral. |
| **F1-A — exact ordinary quantitative observation** | M-A explicitly approves `[0,62)` as a bounded metric for only the exact construction. | One ordinary `QuantitativeConstraintObservation`; exact metric Evidence `[0,62)` and frequency Evidence `[63,90)`; zero or one observation; no IDs allocated. | Does not enter `ACCEPT-QUANT-001`. Does enter `CALC-V-MVP-001`: current standalone class changes `0 → 1/2`; exact refined R1′ remains `1/2`, subject to the authoritative other-detector precedence in §7.4. | Exact positive supersedes exclusion only for its own span. All non-exact forms keep current behavior. No new diagnostic. | Risks mislabeling a behavior as metric and silently changing displayed/aggregated Verifiability if downstream approval is omitted. | `PROPOSED_FOR_RESEARCHER_REVIEW`; requires explicit M-A and downstream approval; not approved or implementable. |
| **F1-B — exact separate frequency record** | M-B keeps `[0,62)` as a behavior role rather than an existing metric component. | One separate role-aware record associated with the quantitative family but outside `quantitative_constraints`; same Evidence offsets; new bounded collection/type required; no IDs allocated. | Does not enter `ACCEPT-QUANT-001` or any current calculator; preserves current C/V/U values and aggregation. | Same exact positive/exclusion coexistence and no-diagnostic policy as F1-A. | Requires additional representation and a binding non-consumption boundary; risks accidental generic relationship design. | `PROPOSED_FOR_RESEARCHER_REVIEW`; requires explicit M-B and representation approval; not approved or implementable. |
| **F2 — family of numeric and duration-unit variants** | Would need a general metric/behavior and frequency-role contract not supplied by the source. | Family grammar, Evidence, ambiguity, cardinality, and representation would be required. | Downstream and acceptance behavior would require a new shared decision rather than inheritance from F1. | Would replace many protected negatives with positives and could change fallback/diagnostic behavior broadly. | High risk of inheriting scalar grammar without scientific support, parsing written counts, or creating an implicit rate ontology. | `NOT_READY`; requires new source evidence and a complete common contract. |

This proposal prepares F1-A and F1-B for an explicit researcher choice but does
not select or approve either. F0 remains the complete conservative alternative.
F2 remains `NOT_READY`.

## 10. Proposed bounded decision

The common scientific core is ready for researcher review, but F1 is not a
single decision until the metric-role and downstream gates are resolved:

1. **Boundary:** approve or revise Alternative B, the exact 90-code-point
   refined frequency clause, and permit only the selected complete input
   envelopes in §2.4.
2. **Frequency semantics:** approve or revise the exact source-level frequency
   condition on coordinate updates, preserving `NOT_LESS_FREQUENT`, value `5`,
   unit `SECOND`, fixed `одного разу на`, and no arithmetic conversion.
3. **Metric/behavior gate:** choose M-A and explicitly approve `[0,62)` as the
   one exact metric, or choose M-B and preserve it as a separate behavior role.
   If neither is approved, select F0.
4. **Representation/downstream gate:** with M-A, choose F1-A and explicitly
   accept ordinary quantitative-family consumption by `CALC-V-MVP-001`; with
   M-B, choose F1-B and explicitly approve the separate non-consumed record and
   its additional domain boundary. No package is selected by this document.
5. **Evidence:** under either F1 package, require exactly two future-owned
   Evidence items at `[0,62)` and `[63,90)` with source-ordered references. Do
   not allocate their IDs or producing Rule ID in this decision.
6. **Cardinality:** allow zero or one exact F1 record per requirement.
7. **Precedence:** let an approved exact positive supersede the protected
   exclusion only for its own frequency span; preserve the full variable-value/
   unit exclusion and global scalar precedence everywhere else.
8. **Status and diagnostics:** an approved exact match creates one selected F1
   record and no F1 diagnostic; deterministic non-match creates none and
   delegates entirely to current baseline behavior. F1-B additionally requires
   an approved separate-outcome storage contract.
9. **Coexistence:** preserve the separate `не більше 3 с` observation in exact
   refined R1′ and forbid cross-semicolon linkage.
10. **Acceptance:** preserve `ACCEPT-QUANT-001` scalar ownership,
    judgeability, Evidence ownership, containment, and deduplication. Neither
    F1 package creates an acceptance observation or diagnostic.
11. **Downstream consequence:** explicitly approve that F1-A can change
    requirement and specification Verifiability outputs as stated in §7.4, or
    explicitly approve F1-B's non-consumption boundary. Do not infer unchanged
    outputs from unchanged formulas.
12. **Lifecycle:** any scientific approval remains documentation-only. Issue
    #73 still cannot implement F1 or allocate final identifiers.

F1-A is defensible only as a deliberate approval of both the exact metric role
and the existing Verifiability consequence. F1-B is defensible only as a
deliberate approval of the behavior-role distinction and the additional bounded
representation. Neither package invents a rate calculation, count ontology,
generic frequency grammar, or new acceptance semantics.

If the researcher does not approve one complete package, the decision falls
back to F0. There is no automatic conversion between F1-A and F1-B and no
implementation-authorized default.

## 11. Explicit blockers and exclusions

### 11.1 Unresolved scientific approval gates

F1 remains unapproved until the researcher explicitly:

1. chooses M-A exact metric or M-B separate behavior role;
2. chooses the matching F1-A ordinary observation or F1-B separate record;
3. for F1-A, accepts the existing `CALC-V-MVP-001` consumption and disclosed
   requirement/specification Verifiability consequences;
4. for F1-B, approves the additional record/collection boundary and binding
   exclusion from current calculators and acceptance composition; and
5. approves the common boundary, semantics, Evidence, exclusion, cardinality,
   status, and no-diagnostic contract.

These are scientific-contract choices. They cannot be delegated to an
implementation issue or inferred from the convenience of existing types.

### 11.2 F1 implementation blockers

Even if the researcher approves the science, implementation remains blocked by
the issue #73 constraint and by the absence of:

1. a separately authorized production implementation issue;
2. a final production Rule ID and Evidence-ID prefix;
3. implementation type and field-name decisions, if any maintenance changes
   are needed;
4. implementation fixtures and technical audit; and
5. explicit researcher acceptance of any later implementation.

These are lifecycle blockers, not permission to revise the scientific
contract during implementation.

### 11.3 Explicit exclusions

Nothing in this proposal authorizes:

- scientific approval by implication;
- production implementation in issue #73;
- a Rule ID, Evidence ID, diagnostic ID, branch, commit, push, or pull request;
- modification of [`model-spec.md`](model-spec.md) or any existing research
  document;
- broadening `QUANT-001`, `QUANT-UK-001`, `QUANT-METRIC-001`, or
  `QUANT-CONTEXT-001`;
- changing the exact C0 `500` diagnostic or C0 processing outcome;
- implementing, renaming, allocating, or broadening exact R3;
- deleting or narrowing the existing protected frequency exclusion;
- turning the exclusion's numeric/unit variables into F1 positive variables;
- adding `не рідше` to `QUANT-UK-001` as a general comparator;
- parsing `одного` as numeric `1` or `разу` as a count unit;
- converting the source to `≤ 5 с`, `≥ 1`, `1/5 Hz`, or another arithmetic
  form;
- unit conversion, compound units, a rate ontology, tolerance, scheduling,
  jitter, missed-update, measurement, or pass/fail rules;
- casefolded, whitespace-tolerant, morphological, synonym, parser, proximity,
  or arbitrary clause-search generalization of the positive rule;
- positive recognition of changed values, duration units, wording,
  punctuation, prefix, suffix, or cardinality;
- linking across the semicolon or treating the percentile clause as a member
  of F1;
- changing condition/result detection, `ACCEPT-QUANT-001`, judgeability,
  criterion count, or deduplication;
- changing any C/V/U formula, Finding or `QUALITY_PROBLEM` rule, reporter
  presentation rule, or aggregation formula. F1-A's disclosed change to an
  accepted Verifiability input and resulting outputs is not a formula change;
- suppressing F1-A from `CALC-V-MVP-001` while still placing it in the ordinary
  `quantitative_constraints` collection;
- allowing F1-B to enter `quantitative_constraints`, `ACCEPT-QUANT-001`, or a
  current characteristic calculator;
- creating a generic frequency model or relationship framework;
- approving F2 without new source evidence and a complete shared contract;
- closing `RQD-008` or issue #73; or
- creating a baseline, tag, or release.

## 12. Researcher approval checklist

Every item remains pending explicit researcher action.

### 12.1 Boundary and source

- [ ] Approve or revise Alternative B as the exact scientific boundary.
- [ ] Confirm the exact 90-code-point clause text and `[0,90)` boundary.
- [ ] Approve both exact input envelopes in §2.4, or narrow the approval to one.
- [ ] Confirm that the 206-code-point editorial table cell is provenance only
  and a deterministic F1 non-match when ingested literally.
- [ ] Confirm that the semicolon is outside F1 Evidence and remains a hard
  boundary.
- [ ] Confirm that arbitrary prefixes, suffixes, and clause positions are not
  approved.

### 12.2 Semantics

- [ ] Approve the exact source-level coordinate-update frequency meaning in
  §3.1.
- [ ] Approve `NOT_LESS_FREQUENT` with `inclusivity = None` for this exact form.
- [ ] Approve value `Decimal("5")` and unit `SECOND` only as the source-stated
  interval parameter.
- [ ] Confirm that `одного разу на` is fixed grammatical material and creates
  no numeric `1`, count component, or count unit.
- [ ] Confirm that no conversion to `≤ 5 с`, `≥ 1`, `1/5 Hz`, rate, or generic
  duration-bound semantics is approved.

### 12.3 Metric role, representation, and Evidence

- [ ] Select exactly one coherent disposition: F1-A/M-A, F1-B/M-B, or F0.
- [ ] If selecting F1-A/M-A, explicitly approve `[0,62)` as the exact bounded
  metric component and confirm that this does not create a reusable
  action-to-metric grammar or broaden `QUANT-METRIC-001`.
- [ ] If selecting F1-B/M-B, explicitly approve `[0,62)` as a separate behavior
  role and approve a bounded record/collection outside
  `quantitative_constraints`.
- [ ] Confirm that no cross-combination or automatic fallback between F1-A and
  F1-B is approved.
- [ ] Approve the exact role Evidence `[0,62)` and frequency-anchor Evidence
  `[63,90)` under the selected F1 package.
- [ ] Approve the selected role/component-reference mapping and the common
  source-ordered Evidence union.
- [ ] Approve zero-or-one F1 record cardinality.
- [ ] Confirm that both Evidence items remain in feature family
  `QUANTITATIVE_CONSTRAINT`, while only F1-A enters the ordinary observation
  collection.
- [ ] Confirm that no final Rule ID, Evidence ID, type name, or field name is
  allocated by scientific approval.
- [ ] Confirm that no generic frequency model, relationship framework, or
  actor/action/object grammar is approved.

### 12.4 Exclusion status and compatibility

- [ ] Approve exact-positive precedence over the protected exclusion only for
  the exact F1 span.
- [ ] Confirm that the current variable-value/unit exclusion remains unchanged
  for every non-exact form.
- [ ] Confirm unchanged global scalar precedence and no nested `5 с` duplicate.
- [ ] Approve no F1 diagnostic for exact match or deterministic non-match.
- [ ] Confirm unchanged mixed accepted/unresolved outcome derivation.
- [ ] Confirm preservation of the separate `не більше 3 с` observation and no
  cross-semicolon linkage.
- [ ] Confirm unchanged C0 and exact R3 contracts.

### 12.5 Acceptance and downstream gate

- [ ] Confirm that neither F1 package enters `ACCEPT-QUANT-001`, creates
  acceptance Evidence/diagnostics, or changes its scalar Evidence-ownership,
  containment, judgeability, criterion-count, or deduplication contract.
- [ ] Confirm that `NOT_LESS_FREQUENT / inclusivity=None` is not independently
  judgeable under the current acceptance contract.
- [ ] If selecting F1-A, explicitly approve ordinary
  `quantitative_constraints` membership and existing `CALC-V-MVP-001`
  consumption.
- [ ] If selecting F1-A, explicitly accept the exact-input consequences:
  current standalone `V_i` changes from `0` to `1/2`, while current refined
  R1′ remains `1/2`, subject to other detector outcomes and the authoritative
  Verifiability precedence.
- [ ] If selecting F1-A, explicitly accept the potential corresponding change
  to displayed requirement Verifiability and `AGG-MVP-001` specification
  aggregation.
- [ ] If selecting F1-B, explicitly approve the binding non-consumption of the
  separate record by every current C/V/U calculator and acceptance rule.
- [ ] Confirm that no C/V/U formula, Finding, `QUALITY_PROBLEM`, reporter
  presentation rule, or aggregation formula is changed.

### 12.6 Option and lifecycle decision

- [ ] Record the selected F0, F1-A, or F1-B disposition explicitly; no selection
  is recorded by this proposal.
- [ ] Confirm F2 remains `NOT_READY` without new source evidence and a complete
  shared scientific contract.
- [ ] Confirm that any scientific approval remains documentation-only and that
  issue #73 authorizes no production implementation or identifier allocation.
- [ ] Confirm `RQD-008` and SRM-05 issue #73 remain open.

Until the researcher explicitly completes both approval gates, F1-A and F1-B
remain `PROPOSED_FOR_RESEARCHER_REVIEW`, the existing protected exclusion
remains the only production behavior for the frequency construction, F2
remains `NOT_READY`, exact R3 remains unimplemented with no Rule ID, and no
production change is authorized.
