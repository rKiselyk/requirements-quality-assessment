# SRM-05F — Exact Frequency Scientific Approval Proposal

**Issue:** #73 (`SRM-05`)  
**Document status:** `PROPOSED_FOR_RESEARCHER_REVIEW`  
**Proposal scope:** one exact source-backed frequency construction  
**Decision effect:** none; no researcher approval is recorded  
**Implementation effect:** none; production implementation is prohibited in
issue #73  
**Identifier effect:** none; no Rule ID or Evidence ID is allocated

This document prepares one bounded F1 decision for the source construction
`не рідше одного разу на 5 с`. It proposes an exact clause boundary, a
source-level interpretation, and a representation using the existing
quantitative observation shape. The proposal does not approve the contract,
authorize implementation, broaden the protected frequency exclusion, or alter
any current detector, diagnostic, calculator, reporter, or aggregator.

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
- C/V/U, Findings, `QUALITY_PROBLEM`, reporter, and aggregation; and
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

These absences do not make the exact attachment unresolved. They delimit what
the proposed observation means and what no consumer may infer from it.

## 4. Representation alternatives

### 4.1 Alternative A — one bounded observation using existing components

The existing `QuantitativeConstraintObservation` can represent the proposed
exact source-level meaning if the contract gives `NOT_LESS_FREQUENT` its
bounded role and preserves the complete recurrence phrase as Evidence.

The proposed semantic content is:

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

This alternative does not claim that the observation is a generic frequency
model. The combination is valid only under the exact grammar in §2.4.

### 4.2 Alternative B — dedicated exact relationship record

A dedicated record could separately name:

- update-behavior Evidence;
- comparator surface;
- fixed occurrence phrase;
- interval value and unit; and
- their exact relationship.

This would make every source role explicit, but it would add a second
quantitative representation beside the scalar tuple even though no existing
independent scalar member must be preserved or cross-referenced. Unlike exact
R3, this construction does not join several existing observations. A dedicated
record would therefore add representation complexity without a demonstrated
source need and could invite an unapproved generic frequency framework.

Alternative B is not proposed for this exact F1 slice.

### 4.3 Alternative C — explicit deferral

Deferral remains scientifically valid if the researcher concludes that the
existing component shape cannot safely distinguish the interval parameter from
a frequency value. In that case the current exclusion remains unchanged and no
positive observation is created.

Alternative C is the fallback disposition, not the preferred proposal.

### 4.4 Proposed minimum representation

Alternative A is proposed for researcher review. It is sufficient only because:

1. `NOT_LESS_FREQUENT` already exists as a distinct comparator label with
   `inclusivity = None`;
2. the exact metric Evidence names coordinate updating;
3. the full frequency-anchor Evidence preserves `одного разу на 5 с` rather
   than reducing it to `5 с`;
4. the value/unit pair is explicitly defined as the source interval parameter,
   not a frequency magnitude; and
5. no current consumer receives a new calculation or interpretation.

If any of those five constraints is rejected, Alternative A is not sufficient
and the decision must fall back to explicit deferral rather than silently
creating a relationship model.

## 5. Protected exclusion compatibility

### 5.1 Coexistence rule

The current protected exclusion remains the default for the full approved
variable-value/unit shape. A future positive exact F1 rule would coexist as
follows:

1. Evaluate the exact F1 input envelopes in §2.4 without changing the current
   scalar candidate-precedence order.
2. If an exact F1 envelope matches, create the one proposed observation and
   mark its `[63,90)` frequency span as positively consumed by F1.
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
span in one of the two exact input envelopes. It does not delete, narrow, or
redefine the broader exclusion.

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

In the exact 178-code-point R1′ input, the proposed F1 observation and the
existing `не більше 3 с` observation are distinct. The semicolon prevents
metric, component, or Evidence sharing between them.

## 6. Proposed Evidence contract

### 6.1 Evidence items

An exact positive would create exactly two accepted Evidence items in feature
family `QUANTITATIVE_CONSTRAINT`. Their final IDs and producing Rule ID remain
`NOT_ALLOCATED`.

| Role | Exact text | Span in the 90- or 178-code-point proposed input | Feature | Allocation status |
| --- | --- | --- | --- | --- |
| Update behavior / exact metric | `координати активного транспортного засобу повинні оновлюватися` | `[0,62)` | `QUANTITATIVE_CONSTRAINT` | Future Rule ID and Evidence ID `NOT_ALLOCATED` |
| Frequency anchor | `не рідше одного разу на 5 с` | `[63,90)` | `QUANTITATIVE_CONSTRAINT` | Future Rule ID and Evidence ID `NOT_ALLOCATED` |

The U+0020 SPACE at `[62,63)` separates the role spans and is not separately
stored. The exact construction boundary is their enclosing clause `[0,90)`.
The semicolon in the 178-code-point input is outside the Evidence contract.

For provenance only, the analogous slices in the original 206-code-point table
cell are update behavior `[28,90)`, frequency anchor `[91,118)`, and enclosing
clause `[28,118)`. Those offsets do not become accepted F1 Evidence because the
editorial whole-cell input is a deterministic F1 non-match.

### 6.2 Component references and source order

The metric component references only the update-behavior Evidence. Comparator,
value, and unit reference the one complete frequency-anchor Evidence. No
component references a substring for `5`, `с`, or `одного`; the exact raw
source is preserved by the anchor Evidence.

The observation's top-level Evidence sequence is the stable, de-duplicated,
source-ordered union:

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
- participate only in the one proposed quantitative observation.

### 6.3 Cardinality and coexistence

The proposed cardinality is zero or one F1 observation per requirement. An
accepted observation has exactly one update-behavior Evidence item and one
frequency-anchor Evidence item.

For the exact 178-code-point refined R1′ input, the quantitative observation
order is:

1. the proposed F1 observation, whose earliest Evidence begins at `0`; and
2. the unchanged `QUANT-UK-001` observation for `не більше 3 с` at
   `[164,177)`.

No Evidence item is shared or merged. The percentile metric candidate at
`[92,161)` remains outside this proposal.

## 7. Status and diagnostic behavior

### 7.1 Exact positive

When either exact input envelope in §2.4 matches and every Evidence invariant
is satisfied, the proposed outcome is:

- exactly one F1 quantitative observation;
- exactly two F1 Evidence items;
- no F1-specific diagnostic;
- no nested `5 с` fallback observation;
- no numeric diagnostic for `5`;
- `COMPLETE` quantitative processing; and
- derived outcome `DETECTED`.

For the 178-code-point input, the independent `не більше 3 с` observation is
also preserved. Its presence does not change the F1 observation count or
Evidence.

### 7.2 Deterministic F1 non-match

A deterministic F1 non-match creates:

- no F1 observation;
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

If an independently approved detector produces an unresolved candidate in the
same requirement as a future F1 observation, F1 neither suppresses nor resolves
it. No new frequency ambiguity diagnostic, diagnostic code, or processing
transition is proposed.

## 8. Exact positive and negative cases

`SOURCE_ATTESTED` identifies text present verbatim in the original DOCX, either
as the complete table cell or as an exact contiguous slice of that cell.
`SOURCE_DERIVED_EXACT_CLAUSE` identifies the exact first clause extracted from
that source. `SYNTHETIC_TEST_CASE` identifies a constructed boundary case and
is not scientific evidence for expansion.

| Case | Input or change | Classification | Proposed F1 disposition | Existing baseline behavior to preserve |
| --- | --- | --- | --- | --- |
| Standalone exact clause | Exact 90-code-point clause in §2.2 | `SOURCE_DERIVED_EXACT_CLAUSE` | Positive: one F1 observation and two Evidence items. | F1 consumes the exact frequency span; no `5 с` fallback or diagnostic. |
| Exact refined R1′ | Exact 178-code-point text in §1.1 | `SOURCE_ATTESTED` as the exact contiguous DOCX slice `[28,206)`; matches authoritative model offsets | Positive for first clause; semicolon excluded. | Preserve separate `не більше 3 с` observation at `[164,177)`; no cross-boundary linkage. |
| Frequency substring alone | `не рідше одного разу на 5 с` | Source substring supplied as standalone boundary case | F1 non-match because update behavior is absent. | Existing protected exclusion yields no observation or diagnostic; absent another candidate, `COMPLETE / NOT_DETECTED`. |
| Original full table cell | Exact 206-code-point cell including `Замість ...:` | `SOURCE_ATTESTED` artifact wording | F1 non-match because the selected clause is not at requirement start and the whole cell is not an approved input envelope. | Preserve protected frequency exclusion and the independent later scalar under existing offsets for that input. |
| Final period after standalone clause | Append `.` to the exact 90-code-point clause | `SYNTHETIC_TEST_CASE` | F1 non-match; punctuation differs. | The protected exclusion can still account for the inner frequency phrase; no positive F1 observation. |
| Changed casing or whitespace | Change case or replace a U+0020 space | `SYNTHETIC_TEST_CASE` | F1 non-match because the positive grammar is literal. | The current casefold/Unicode-whitespace-tolerant protected exclusion remains independently applicable when its own contract still matches. |
| Changed interval value | Replace `5` with `6` | `SYNTHETIC_TEST_CASE` | F1 non-match; no variable value slot. | Existing variable-value protected exclusion remains applicable; do not create a positive frequency observation. |
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

| Option | Scientific evidence | Proposed semantics | Representation and Evidence | Exclusion and diagnostic effect | Compatibility risk | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| **F0 — retain exclusion and defer positive recognition** | Fully supported by the current authoritative baseline. The original source remains traceable but unrepresented positively. | No new semantics. `NOT_DETECTED` continues to mean no accepted first-production anchor. | No new representation or Evidence. | Protected exclusion, no frequency observation, and no frequency diagnostic remain unchanged. | Lowest technical risk; preserves deliberate semantic under-coverage. | `READY_FOR_RESEARCHER_REVIEW` as explicit deferral. |
| **F1 — exact source-backed frequency construction** | Exact R1′ source, exact model-spec offsets, existing `NOT_LESS_FREQUENT` label, approved integer `5`, approved `SECOND`, and an already protected complete phrase. | Coordinate updates occur not less frequently than the exact source-stated recurrence. `5 SECOND` is the interval parameter; `одного разу` is fixed text; no rate or inequality conversion. | One existing-shape observation; exact metric Evidence `[0,62)` and frequency Evidence `[63,90)`; zero or one observation; no IDs allocated. | Exact positive supersedes exclusion only for its own span. All non-exact forms keep current exclusion/baseline behavior. No new diagnostic. | Controlled if both exact envelopes, special comparator semantics, and non-consumption by calculators are binding. Main risk is accidental generalization or interpreting `5` as a frequency value. | `PROPOSED_FOR_RESEARCHER_REVIEW`; not approved and not implementable in issue #73. |
| **F2 — family of numeric and duration-unit variants** | The exclusion already recognizes a bounded variable shape, but only `5 с` is original-source-attested in the frequency role. Scalar approval of other numbers/units is not frequency evidence. | Would require shared semantics for every value/unit variant, zero/decimal values, interval versus frequency, and fixed count phrase. | Family grammar, Evidence, ambiguity, cardinality, and possibly a dedicated representation would be required. | Would replace many protected negatives with positives and could change fallback/diagnostic behavior broadly. | High risk of inheriting scalar grammar without scientific support, parsing written counts, or creating an implicit rate ontology. | `NOT_READY`; requires new source evidence and a complete common contract. |

This proposal prepares F1 but does not select or approve it. F0 remains the
complete conservative alternative. F2 remains `NOT_READY`.

## 10. Proposed bounded decision

The following decision package is ready for researcher review:

1. **Boundary:** select Alternative B, the exact 90-code-point refined
   frequency clause. Permit only the two complete input envelopes in §2.4.
2. **Semantics:** interpret the clause as an exact source-level frequency
   condition on coordinate updates. Preserve `NOT_LESS_FREQUENT`, value `5`,
   unit `SECOND`, fixed `одного разу на`, and no arithmetic conversion.
3. **Representation:** select Alternative A, one
   `QuantitativeConstraintObservation` using the existing component shape.
4. **Evidence:** require exactly two new future-owned Evidence items at
   `[0,62)` and `[63,90)` with source-ordered references. Do not allocate their
   IDs or producing Rule ID in this decision.
5. **Cardinality:** allow zero or one exact F1 observation per requirement.
6. **Precedence:** let the exact positive supersede the protected exclusion
   only for its own frequency span; preserve the full variable-value/unit
   exclusion and global scalar precedence everywhere else.
7. **Status:** exact positive is `COMPLETE / DETECTED` with no F1 diagnostic.
   Deterministic non-match adds nothing and delegates entirely to current
   baseline behavior.
8. **Coexistence:** preserve the separate `не більше 3 с` observation in exact
   refined R1′ and forbid cross-semicolon linkage.
9. **Downstream boundary:** create no acceptance, C/V/U, Finding,
   `QUALITY_PROBLEM`, reporter, or aggregation effect.
10. **Lifecycle:** scientific approval, if granted, remains documentation-only.
    Issue #73 still cannot implement the rule or allocate final identifiers.

This package is defensible because it preserves the behavior, recurrence
surface, interval parameter, and hard boundary directly stated by the source
without inventing a rate calculation, count ontology, generic frequency
grammar, or new downstream meaning.

The package must be rejected or revised to F0 if the researcher concludes that
the existing observation fields cannot safely carry an interval parameter
under `NOT_LESS_FREQUENT` without misleading consumers. No automatic fallback
to a dedicated relationship record is authorized.

## 11. Explicit blockers and exclusions

### 11.1 F1 implementation blockers

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

### 11.2 Explicit exclusions

Nothing in this proposal authorizes:

- scientific approval by implication;
- production implementation in issue #73;
- a Rule ID, Evidence ID, diagnostic ID, branch, commit, push, or pull request;
- modification of [`model-spec.md`](model-spec.md) or any existing research
  document;
- broadening `QUANT-001`, `QUANT-UK-001`, `QUANT-METRIC-001`, or
  `QUANT-CONTEXT-001`;
- changing the exact C0 `500` diagnostic or any processing outcome;
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
- changing C/V/U, Findings, `QUALITY_PROBLEM`, reporter, or aggregation;
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

### 12.3 Representation and Evidence

- [ ] Approve Alternative A, one existing-shape quantitative observation, or
  choose F0 deferral if that shape is insufficient.
- [ ] Approve the exact update-behavior Evidence `[0,62)` and frequency-anchor
  Evidence `[63,90)`.
- [ ] Approve the proposed component-reference mapping and source-ordered union.
- [ ] Approve zero-or-one F1 observation cardinality.
- [ ] Confirm that no final Rule ID or Evidence ID is allocated by scientific
  approval.
- [ ] Confirm that no dedicated relationship record or generic frequency model
  is approved.

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
- [ ] Confirm unchanged C0, exact R3, acceptance, C/V/U, Findings,
  `QUALITY_PROBLEM`, reporter, and aggregation.

### 12.5 Option and lifecycle decision

- [ ] Select F0 deferral or approve/revise the exact F1 package; no selection is
  recorded by this proposal.
- [ ] Confirm F2 remains `NOT_READY` without new source evidence and a complete
  shared scientific contract.
- [ ] Confirm that any scientific approval remains documentation-only and that
  issue #73 authorizes no production implementation or identifier allocation.
- [ ] Confirm `RQD-008` and SRM-05 issue #73 remain open.

Until the researcher explicitly completes the decision, F1 remains
`PROPOSED_FOR_RESEARCHER_REVIEW`, the existing protected exclusion remains the
only production behavior for the frequency construction, F2 remains
`NOT_READY`, exact R3 remains unimplemented with no Rule ID, and no production
change is authorized.
