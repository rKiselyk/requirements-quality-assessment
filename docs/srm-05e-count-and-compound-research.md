# SRM-05E — Count Roles and Compound Quantitative Constraints Research

**Issue:** #73 (`SRM-05`)  
**Document status:** `RESEARCH_ONLY / PROPOSED_FOR_RESEARCHER_REVIEW`  
**Decision effect:** none; this document records research findings and open
decision gates only  
**Rule-ID effect:** none; no new Rule ID is allocated

## 1. Research objective and scope

This document investigates how one individual requirement can contain several
numeric expressions with different semantic roles. It asks when a number is:

1. the scalar value of a measurable requirement bound;
2. part of the measurement or load context for another bound;
3. a separate partial or independent quantitative constraint; or
4. a qualifier that participates in a compound relationship but cannot yet be
   represented as an independently meaningful target.

The bounded cases are:

- the accepted exact C0 response-time construction with `500` concurrent
  users;
- the constructed C0-like string with `600` concurrent users; and
- the source-attested route-generation requirement containing `95 %`, a
  four-second bound, and a load of up to `300` concurrent requests.

This is not an implementation specification or an approval record. It does not
change [`model-spec.md`](model-spec.md), any SRM-05D artifact, code, tests,
domain models, dependencies, issue state, baseline, tag, or release. Synthetic
strings are used only to expose decision boundaries and are never presented as
dissertation evidence.

The labels used below are:

- `EXISTING_AUTHORITATIVE`: already fixed by `model-spec.md`;
- `SOURCE_ATTESTED`: present verbatim in an inspected repository source;
- `SUPPORTED_INTERPRETATION`: a role directly supported by the source wording
  and current authoritative model, but not a new production allocation;
- `SYNTHETIC`: constructed for research or boundary analysis;
- `PROPOSED_FOR_RESEARCHER_REVIEW`: a candidate decision, not an approval;
- `BLOCKED`: scientific, grammatical, diagnostic, or representation decisions
  are still missing; and
- `DEFERRED`: intentionally outside the candidate under discussion.

## 2. Authoritative baseline

The following statuses are protected and are not changed by this document:

| Item | Current status | Consequence for SRM-05E |
| --- | --- | --- |
| `QUANT-001` / `QUANT-UK-001` | Existing scalar baseline | Preserve comparator, value, unit, Evidence, precedence, diagnostics, and separate-anchor behavior. |
| `QUANT-METRIC-001` | `RESEARCHER_APPROVED / IMPLEMENTED_AND_ACCEPTED` | Preserve the exact response-time metric linkage and the identity of its existing scalar observation. |
| `QUANT-CONTEXT-001` | `RESEARCHER_APPROVED / NOT_IMPLEMENTED` in the authoritative specification | Preserve exact C0 semantics: literal `500`, context-only role, one quantitative observation, and the diagnostic for the embedded number. |
| SRM-05D implementation audit | `READY_FOR_RESEARCHER_ACCEPTANCE` | The audit is not researcher implementation acceptance and does not change the authoritative production status. |
| `COND-UK-001/002` | Existing approved bounded condition rules | Preserve independent condition-family Evidence and processing. |
| `ACCEPT-QUANT-001` | Existing approved scalar-containment composition | Preserve judgeability, result-span containment, clause-level deduplication, Evidence ownership, and diagnostics. |
| `RQD-008` | `PARTIALLY_APPROVED / OPEN` | Variable count roles, broader context grammar, and nested or compound quantitative relationships remain open. |
| SRM-05 issue #73 | `OPEN` | This research does not close it. |

The authoritative representation in §7.15.10 has one optional `metric`, one
optional `context`, scalar components, `unresolved_components`, and a flat
tuple of Evidence references per `QuantitativeConstraintObservation`. It has no
approved parent/child relation, compound-expression identity, population-
qualifier relation, shared-context edge, or logical composition operator.

For C0, the authoritative decision is especially restrictive:

- `при 500 одночасних користувачах` is the measurement/load context of the
  existing response-time observation;
- `500` is not equality, a count unit, an independently judgeable bound, a
  second observation, or a nested quantitative relation;
- the existing `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` diagnostic over `500`
  remains; and
- `600`, variable integer counts, other population nouns, generic `при`
  grammar, and the distinct `при навантаженні до 300 ...` form remain outside
  C0.

## 3. Source inventory and provenance

### 3.1 Authoritative and traceability sources

| Source | Material used | Authority in this document |
| --- | --- | --- |
| [`model-spec.md` §§7.14.6.6–7.14.6.8](model-spec.md) | Scalar anchors, metric/context semantics, exact C0, source cases, diagnostics, and deferred boundaries | Authoritative implementation model |
| [`model-spec.md` §7.15.10](model-spec.md) | Current quantitative component structure and invariants | Authoritative representation |
| [`model-spec.md` §18, `RQD-008`](model-spec.md) | Current partial approval and open research boundary | Authoritative decision status |
| [`srm-05d-quantitative-context-linkage.md`](srm-05d-quantitative-context-linkage.md) | C0 provenance, candidate C1 discussion, count-role alternatives, Evidence risks | Research traceability; not a new authority |
| [`srm-05d-c0-approval-proposal.md`](srm-05d-c0-approval-proposal.md) | Proposal that preceded the exact C0 decision | Historical traceability |
| [`srm-05d-implementation-acceptance-report.md`](srm-05d-implementation-acceptance-report.md) | Technical audit result and protected implementation behavior | Audit evidence only; not researcher acceptance |
| [`reference/2.2_Взаємозвязок_вимог_і_якості.docx`](reference/2.2_Взаємозвязок_вимог_і_якості.docx) | Exact response-time/count example, percent-of-requests example, and performance-evidence table | Original research context |
| [`reference/2.3_Система_метрик.docx`](reference/2.3_Система_метрик.docx) | Methodological distinction among observable quantity, unit, measurement conditions, and admissible bound | Original research context |
| [`reference/Приклад_застосування_моделі.docx`](reference/Приклад_застосування_моделі.docx) | Explicit percentile example and exact route-generation requirement | Original application-example context |

The DOCX sources were inspected through their actual paragraph and table
structures. Repository research documents were used for traceability, but the
exact source claims below were checked against the DOCX text itself.

### 3.2 Exact source wording found

`SOURCE_ATTESTED` — Section 2.2, Table 2.5, row `Семантичний (S)`, contains:

```text
Час відгуку ≤ 2 с при 500 одночасних користувачах
```

The same document's performance row in Table 2.4 lists response time and load
as typical requirement evidence and identifies numeric thresholds, load
conditions, and measurement units as early specification indicators.

`SOURCE_ATTESTED` — Section 2.2, paragraph 3, contains the example:

```text
95 % запитів мають оброблятися не довше ніж за 2 с
```

The paragraph describes this as a performance target. It supplies direct
support for a proportion-of-requests qualifier combined with a duration bound;
it does not call the expression a percentile.

`SOURCE_ATTESTED` — Section 2.3, paragraph 16, states that an especially useful
quality requirement contains an observable quantity, a unit, measurement
conditions, and an admissible limit. This supports preserving those roles
rather than collapsing every number into the same type of observation.

`SOURCE_ATTESTED` — The application example, §8, table headed `Зміна |
Уточнене формулювання`, row `R1 → R1′`, contains:

```text
95-й перцентиль затримки від отримання GPS-події до відображення в UI — не більше 3 с.
```

`SOURCE_ATTESTED` — The same table, row `R2 → R2′`, contains:

```text
Після отримання події про перекриття дороги новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с при навантаженні до 300 одночасних запитів.
```

No inspected source contains the C0-like string with `600`. It is therefore
classified only as:

```text
SYNTHETIC: Час відгуку ≤ 2 с при 600 одночасних користувачах
```

## 4. Numeric-role classification

### 4.1 Role criteria

| Role | Minimum evidence needed | What must not be inferred |
| --- | --- | --- |
| Scalar requirement bound or target | An explicit numeric/value anchor governed by an approved comparator, or an approved value-plus-unit target, associated with an expressed metric or accepted required behavior under a separately approved linkage rule | A metric from the unit alone; equality from a bare cardinal; tolerance, conversion, or an unexpressed denominator |
| Measurement/load context | Wording that states the conditions, population, workload, scenario, or measurement regime under which another explicit target applies, plus a unique approved attachment to that target | Independent pass/fail meaning merely because the context contains a number; nearest-bound attachment; generic `при` semantics |
| Separate partial quantitative constraint | Its own approved scalar anchor and Evidence boundary, with explicit comparator/value or value/unit structure; it may remain partial when metric, count dimension, or inclusivity is unresolved | That the separate observation is independent of every surrounding target; that unresolved `до` is inclusive; that a count noun is an approved unit |
| Independent quantitative constraint | All requirements for a separate partial observation, plus an expressed or approved metric/count dimension, boundary semantics sufficient for its intended use, and a decision that its truth can be evaluated separately from surrounding targets | Independence from mere multiplicity of numbers; a parent/child or logical relation not present in the source or representation |
| Compound qualifier or relationship member | Exact Evidence for each member and an approved relation specifying what qualifies what, cardinality, scope, and ambiguity behavior | Decomposition into unrelated observations when the source expresses one joint target; percentile conversion from a percentage; shared context based on proximity |

These categories are not mutually exclusive at the surface-span level. A phrase
such as `до 300` can be an accepted partial scalar anchor inside a larger load
context. Dual role is permissible only after both roles and their relationship
are explicitly approved; it cannot be inferred merely because the spans
overlap.

### 4.2 Evidence test for choosing a role

A future decision should require all of the following before assigning a role:

1. **Source form:** exact wording and provenance, with synthetic variants
   labelled as such.
2. **Governed quantity:** the text that names or establishes what is measured;
   a unit alone is insufficient.
3. **Operator:** the exact comparator or target construction and its boundary
   semantics. `до` retains `UPPER_BOUND / UNRESOLVED`.
4. **Value representation:** the approved numeric surface and exact parsed
   value, without broadening syntax by analogy.
5. **Dimension or population:** an approved unit, or a preserved count noun and
   population phrase whose role is separately decided.
6. **Attachment:** the exact grammatical/template relation connecting metric,
   result, qualifier, context, and bound. No distance heuristic is allowed.
7. **Cardinality and scope:** whether one qualifier/context governs one bound,
   several bounds, or an entire result clause.
8. **Evidence ownership:** exact original-source spans and owning rule family,
   including any permitted overlap without shared Evidence identity.
9. **Observation identity:** whether the construction enriches an existing
   observation, creates another observation, or requires a relation between
   observations.
10. **Failure behavior:** deterministic negative versus unresolved candidate,
    diagnostic code and span, processing status, and mixed accepted/unresolved
    outcome.
11. **Acceptance interaction:** which scalar Evidence is inside an accepted
    expected result and whether clause-level deduplication applies.
12. **Protected negatives:** technical versions, bare counts, changed nouns,
    unsupported numeric forms, hard boundaries, and competing attachments.

### 4.3 Percentage is not percentile

The sources support two different constructions:

| Form | Directly supported role | Prohibited shortcut |
| --- | --- | --- |
| `95 % запитів` / `для 95 % запитів` | A proportion or population-coverage qualifier over requests. The `%` belongs to the numeric chunk; `запитів` identifies the expressed population in the sentence. | Do not relabel it as `95-й перцентиль`; do not invent a sampling denominator, window, aggregation convention, or distribution statistic. |
| `95-й перцентиль затримки ...` | An ordinal percentile qualifier belonging to the latency metric, explicitly followed by a duration bound. | Do not convert `95-й` into a `PERCENT` quantitative observation or treat it as textually interchangeable with `95 % запитів`. |

The route sentence may operationally resemble a service-level statement, but
the source does not define a statistical transformation between “95 percent of
requests within four seconds” and a percentile-latency metric. Such a
transformation would need rules for the eligible request population,
measurement window, ties, missing/failed requests, and percentile convention.
None is approved.

## 5. Count and load-context cases

### 5.1 Case A — exact C0 with `500`

**Text and provenance:** `SOURCE_ATTESTED`, Section 2.2, Table 2.5.

```text
Час відгуку ≤ 2 с при 500 одночасних користувачах
```

| Required analysis field | Finding |
| --- | --- |
| Metric candidate | `Час відгуку`; existing exact metric component |
| Comparator | `≤` → `LESS_THAN_OR_EQUAL`, `INCLUSIVE` |
| Numeric value | `2` → exact decimal value `2` |
| Unit | `с` → `SECOND` |
| Potential context | `при 500 одночасних користувачах`; existing exact C0 measurement/load context |
| Embedded count | `500`; bare cardinal inside the context, not an equality or independent bound |
| Quantitative relationship | One response-time observation evaluated under the exact concurrent-user context |
| Observation count | Exactly one quantitative observation; no second count observation |
| Existing diagnostic | Preserve `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` over `500`; quantitative processing remains mixed as specified by C0 |
| Acceptance/result effect | No C0-created acceptance criterion or expected result; all existing `ACCEPT-QUANT-001` behavior remains unchanged |
| Known versus unresolved | C0 role is known. General count semantics, alternative values, count unit, and independent/nested interpretations remain unresolved or excluded. |

### 5.2 Case B — synthetic C0-like count `600`

**Text and provenance:** `SYNTHETIC`; not found in the dissertation or
application-example sources.

```text
Час відгуку ≤ 2 с при 600 одночасних користувачах
```

| Required analysis field | Finding under the current baseline |
| --- | --- |
| Metric candidate | The exact existing prefix still supplies `Час відгуку`. |
| Comparator/value/unit | Existing `≤ 2 с` scalar semantics remain unchanged. |
| Potential context | The full suffix is linguistically analogous to C0, but it is outside the exact approved context rule. |
| Embedded count | `600` is a bare count candidate; no equality, lower/upper bound, or count unit is expressed. |
| Quantitative relationship | No approved relationship attaches the suffix to the response-time observation. |
| Observation count | The existing primary response-time observation remains; no count observation and no `QUANT-CONTEXT-001` enrichment may be added. |
| Existing diagnostic | The standalone ASCII count remains governed by existing quantitative diagnostic behavior; no new context-specific diagnostic is authorized. |
| Acceptance/result effect | Unchanged. The suffix cannot independently satisfy `ACCEPT-QUANT-001`. |
| Scientific support | Insufficient for production generalization. A synthetic substitution is a useful negative/boundary case, not source evidence. |

The source corpus does show a different load count, `300`, but in the different
construction `при навантаженні до 300 одночасних запитів`. That second example
does not establish that the literal slot in `при 500 одночасних користувачах`
is freely variable. It changes the marker-headed structure, introduces an
explicit comparator, uses a different population noun, and raises a nested-role
question. C0 numeric syntax must therefore not be generalized by inheritance
from primary scalar anchors.

### 5.3 Case C — source-attested route-generation construction

**Text and provenance:** `SOURCE_ATTESTED`, application example, §8, row
`R2 → R2′`.

```text
Після отримання події про перекриття дороги новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с при навантаженні до 300 одночасних запитів.
```

| Segment | Supported or current role | Unresolved relationship |
| --- | --- | --- |
| `Після отримання події про перекриття дороги` | Governing event/condition for the required route behavior | Whether a future compound structure needs a direct reference to it; no quantitative component is implied |
| `новий маршрут ... має бути сформований` | Existing accepted expected result | The current quantitative representation has no explicit result reference |
| `для 95 % запитів` | Source-supported population/proportion qualifier | Whether it is part of the metric, quantitative context, or a distinct qualifier relation; the denominator scope and measurement window are unstated |
| `95 %` | Existing value-plus-`PERCENT` numeric anchor can be preserved | Its accepted scalar observation does not by itself encode “successful route generation within four seconds” |
| `не більше ніж за 4 с` | Duration bound: `LESS_THAN_OR_EQUAL / INCLUSIVE`, value `4`, unit `SECOND` | The implicit route-generation duration metric is not covered by `QUANT-METRIC-001` |
| `при навантаженні до 300 одночасних запитів` | Source-supported load context candidate and existing condition-family phrase | Exact quantitative-context attachment, cardinality, and dual-role semantics are not approved |
| `до 300` | Existing separate partial anchor: `UPPER_BOUND / UNRESOLVED`, value `300`, no approved count unit | Endpoint inclusion, count dimension, independent judgeability, and relation to the four-second target remain unresolved |
| `одночасних запитів` | Source-attested count/population noun phrase | Not an approved unit ontology entry; no general inflection or noun vocabulary follows |

The source directly supports the following semantic reading: route generation
for a stated proportion of requests is subject to a four-second target under a
stated concurrent-request load. It does not by itself determine how many
domain observations or relation objects must represent that joint meaning.

Under existing independent rules, the requirement can already preserve three
distinct scalar anchors:

1. `95 %` as a value-plus-percent observation;
2. `не більше ніж за 4 с` as an inclusive duration-bound observation; and
3. `до 300` as an upper-directed observation with unresolved inclusivity.

That existing multiplicity does not encode the scientific relationship among
them. In particular, it does not state that `95 %` is the proportion of the
eligible route-generation requests that satisfy the four-second bound while
the `до 300` phrase defines the load under which the measurement is made.

### 5.4 Necessary research cases

These cases are not binding tests for a new rule. They show the positive,
negative, and unresolved distinctions a later proposal would have to close.

| Case | Text or change | Provenance | Required research disposition |
| --- | --- | --- | --- |
| Exact C0 positive | `Час відгуку ≤ 2 с при 500 одночасних користувачах` | `SOURCE_ATTESTED` | Preserve the complete existing C0 contract. |
| Changed C0 count | Replace `500` with `600` | `SYNTHETIC` | Current C0 negative; do not infer a variable slot. |
| Missing population phrase | `Час відгуку ≤ 2 с при 600` | `SYNTHETIC` | A number alone cannot establish a load context. |
| Fractional/grouped/signed count | Use `600,5`, `600.0`, `1 000`, `+600`, or `6e2` | `SYNTHETIC` | Exclude from any bounded count proposal unless separately sourced and approved. |
| Changed count noun or marker | Replace `користувачах` or `при` | `SYNTHETIC` | No synonym, inflection, or generic marker expansion. |
| Exact route compound | Complete `R2 → R2′` sentence | `SOURCE_ATTESTED` | Preserve all three numeric anchors and current result/condition Evidence; relationship remains a research decision. |
| Explicit percentile contrast | `95-й перцентиль ... — не більше 3 с` | `SOURCE_ATTESTED` | Treat as percentile-qualified latency metric, not as the `95 % запитів` form. |
| Percent without expressed population | `95 % має бути сформовано ...` | `SYNTHETIC` | Unresolved or negative for a population relation; do not invent `запитів`. |
| Load phrase alone | `при навантаженні до 300 одночасних запитів` without a uniquely attachable target | Fragment derived from source; complete fragment use is `SYNTHETIC` | Must not attach by proximity or become a standalone acceptance criterion. |
| Hard-boundary split | Put a full stop before the load phrase | `SYNTHETIC` | No cross-boundary quantitative-context or compound attachment. |
| Competing duration bounds | Add another route duration before the load phrase | `SYNTHETIC` | Ambiguous; do not choose the nearest bound without an approved rule. |
| Competing populations | Add a second percent or request group | `SYNTHETIC` | Ambiguous scope/cardinality; no silent distribution. |
| Changed `до` interpretation | Treat `до 300` as `≤ 300` | Inference only | Forbidden until endpoint inclusivity is explicitly decided. |

## 6. Compound quantitative constructions

### 6.1 Relations present in the route source

The exact source supports a semantic structure of at least four kinds:

```text
event condition
  -> required route-generation result
       -> population/proportion qualifier: 95 % of requests
       -> duration target: no more than 4 seconds
       -> load condition: under load up to 300 concurrent requests
```

This diagram is a research interpretation of the source sentence, not an
approved domain graph. It expresses scope that the flat scalar observations do
not currently preserve.

Directly supported relationships are:

- the four-second phrase bounds route-generation time;
- `для 95 % запитів` qualifies the requests for which the route-generation
  target is stated;
- the trailing `при навантаженні ...` phrase states the load condition for the
  route-generation target; and
- `до 300` is upper-directed, while its endpoint inclusivity is not stated.

The following remain unresolved:

- whether the percentage qualifier belongs to the metric, the result, the
  duration bound's context, or a dedicated population relation;
- the exact denominator and observation window for `95 %`;
- whether the four-second requirement should be represented as a percentile,
  proportion-qualified target, or only in its literal source form;
- whether the full load phrase is context only, while `до 300` remains an
  unrelated partial observation, or whether one explicit nested relation is
  required;
- whether `до 300` is independently testable as a workload limit or only sets
  the measurement regime for the primary target;
- whether one load context governs both the `95 %` and four-second anchors or a
  compound parent representing their joint target;
- what happens when one relationship member is unresolved while the other
  anchors are accepted; and
- whether source order plus overlapping Evidence is sufficient or explicit
  relation identity is necessary.

### 6.2 Why separate observations are not a complete decomposition

Three flat observations correctly preserve the explicit numeric anchors, but
they can lose the central statement that the `95 %` proportion is evaluated
against compliance with the four-second route-generation target under the
stated load. Conversely, merging the three numbers into one observation would
exceed the current one-value, one-unit, one-comparator shape and could erase the
independent `до 300` scalar provenance.

A valid future decomposition therefore needs an approved relationship contract,
not merely another regular expression. At minimum that contract must state:

1. which observation or result is primary;
2. the role and scope of the percentage;
3. the role and scope of the load phrase;
4. whether the nested load bound has separate observation identity;
5. cardinality and ordering for all participating members;
6. Evidence references and ownership for every member and relation;
7. unresolved and ambiguity behavior; and
8. the effect, if any, on acceptance composition.

## 7. Evidence and component implications

### 7.1 Exact and possible spans

All offsets below are zero-based Unicode code-point ranges `[start,end)` over
the exact trimmed text shown in each case.

For Case A, existing authoritative spans are:

| Role | Text | Span | Current disposition |
| --- | --- | --- | --- |
| Metric | `Час відгуку` | `[0,11)` | Existing `QUANT-METRIC-001` Evidence |
| Scalar | `≤ 2 с` | `[12,17)` | Existing `QUANT-001` Evidence |
| Quantitative context | `при 500 одночасних користувачах` | `[18,49)` | Existing C0 `QUANT-CONTEXT-001` contract |
| Embedded count candidate | `500` | `[22,25)` | Existing diagnostic span; not accepted Evidence |

Case B has the same character offsets because `600` has the same length, but
the suffix `[18,49)` is not `QUANT-CONTEXT-001` Evidence. The number `[22,25)`
remains a candidate under existing diagnostic behavior. A future rule cannot
turn the whole suffix into accepted context merely by substituting digits.

For Case C, the source sentence has these relevant exact spans:

| Candidate role | Text | Span | Current or possible use |
| --- | --- | --- | --- |
| Event condition | `Після отримання події про перекриття дороги` | `[0,43)` | Existing structural condition candidate; not a quantitative component by itself |
| Expected result / acceptance clause | `новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с` | `[44,116)` | Existing result and clause-level acceptance Evidence |
| Route subject/result core | `новий маршрут` | `[44,57)` | Potential future metric/result basis; no new metric Evidence proposed |
| Proportion phrase | `для 95 % запитів` | `[58,74)` | Possible population-qualifier Evidence; no owning production rule allocated |
| Percent anchor | `95 %` | `[62,66)` | Existing value-plus-unit quantitative Evidence candidate |
| Duration anchor | `не більше ніж за 4 с` | `[96,116)` | Existing `QUANT-UK-001` scalar Evidence |
| Duration value/unit | `4 с` | `[113,116)` | Contained in the duration anchor; no duplicate fallback observation |
| Load context | `при навантаженні до 300 одночасних запитів` | `[117,159)` | Existing condition Evidence candidate and possible future quantitative context |
| Nested count phrase | `до 300 одночасних запитів` | `[134,159)` | Research boundary for a possible nested role; not the current scalar Evidence boundary |
| Existing load scalar | `до 300` | `[134,140)` | Existing `QUANT-UK-001` partial scalar Evidence |
| Count value | `300` | `[137,140)` | Component value within the scalar anchor |
| Count/population noun phrase | `одночасних запитів` | `[141,159)` | Source text to preserve; no approved count unit |
| Sentence terminator | `.` | `[159,160)` | Excluded from the candidate Evidence above |

The full `[134,159)` span must not replace the existing `[134,140)` scalar
Evidence by implication. If a future rule needs the full nested count phrase,
it requires its own Evidence ownership and an explicit decision about whether
the noun phrase is a metric, context content, count dimension, or relation
member.

### 7.2 Observation count and diagnostics

| Case | Existing or protected quantitative count | Diagnostic consequence |
| --- | --- | --- |
| A — exact C0 | One enriched response-time observation | Preserve the existing diagnostic over `500`; do not create count Evidence or a second observation. |
| B — synthetic `600` | One existing response-time observation; no C0 context enrichment and no count observation | Preserve current numeric-candidate behavior. No new “unsupported context” or count-role diagnostic is authorized. |
| C — route source | Existing scalar baseline can preserve separate `95 %`, four-second, and `до 300` anchors | No new compound, percentile, denominator, nesting, or context-ambiguity diagnostic is allocated. `до` remains an accepted partial observation with unresolved inclusivity. |

The absence of a relationship diagnostic does not mean that the compound
semantics are resolved. It means only that no such diagnostic contract exists.
A future proposal must state whether missing relationship resolution makes the
quantitative family `INCOMPLETE`, adds a new annotation without changing
processing, or remains outside production detection.

### 7.3 Current representation sufficiency

| Need | Existing structure sufficient? | Research conclusion |
| --- | --- | --- |
| Exact C0 context on one observation | Yes | Already fixed; no change. |
| Replace literal `500` with another count while keeping context-only semantics | Structurally yes | Scientific grammar and diagnostic policy are not supported merely by structural sufficiency. |
| Attach one exact route load phrase to the four-second observation | Superficially possible through one `context` component | Incomplete if the relationship to the separate `до 300` observation must remain explicit. |
| Represent `95 %` as a qualifier of success against the four-second bound | No approved relation exists | One `context` or `metric` field would require an unapproved semantic choice. |
| Link the `до 300` observation as a nested load member | No | Parent/child or reusable relation identity is absent. |
| Represent two contexts or qualifiers on one primary target | Not unambiguously | The singular `context` field and flat refs do not define role-specific multiplicity. |
| Preserve each numeric anchor independently | Yes | Already possible, but insufficient to encode the joint claim. |

Implementation convenience cannot decide these semantics. If an explicit
relationship is scientifically required, a representation decision must
precede production grammar.

## 8. Acceptance-criterion implications

The existing acceptance contract is scalar-centered and result-contained:

- an accepted quantitative anchor can contribute only when its Evidence lies
  completely inside accepted expected-result Evidence;
- the complete result clause becomes acceptance Evidence;
- several eligible quantitative anchors inside the same result are deduplicated
  to one acceptance observation; and
- a separated load/context quantity does not independently promote the result
  to an acceptance criterion.

Consequences for the investigated cases are:

| Case | Existing acceptance interaction | Required preservation |
| --- | --- | --- |
| A — exact C0 | C0 context enrichment itself creates no expected result or acceptance criterion and changes no judgeability. | Keep scalar-only containment and all current counts unchanged. |
| B — synthetic `600` | No new context rule exists; the primary scalar's existing behavior is unchanged. | The bare count must not become a criterion or make the suffix judgeable. |
| C — route source | The result `[44,116)` is an accepted result and yields one clause-level acceptance observation even though `95 %` and the four-second anchor may be separate quantitative observations. | Keep one acceptance observation; do not create one criterion per number. |
| C — load phrase | `[117,159)` lies outside the accepted result; `до 300` cannot independently satisfy `ACCEPT-QUANT-001`. | Preserve this negative even if a future rule attaches the phrase as context. |

The whole route clause is semantically judgeable as a compound target, but the
current acceptance result does not authorize a new normalized relationship,
denominator, percentile interpretation, or separate acceptance score. Any
future compound representation must either remain transparent to
`ACCEPT-QUANT-001` or receive a separately approved acceptance contract. It
must not alter C/V/U formulas, criterion contribution, or deduplication by
side effect.

## 9. E0/E1/E2 decision matrix

| Option | Supporting evidence | Missing decisions | Required rule or representation | Compatibility implications | Mandatory exclusions | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| **E0 — keep C0 unchanged and defer expansion** | Complete authoritative C0 contract; exact source support; audited implementation is technically ready but not researcher-accepted | No new scientific semantics are needed; only the separate pending implementation-acceptance decision remains | No new rule, representation, or diagnostic | Fully preserves every protected contract | All variable counts, route-context linkage, compound roles, and new diagnostics stay outside production | `READY_FOR_RESEARCHER_APPROVAL` only as a conservative no-expansion disposition |
| **E1 — broaden a bounded count/context construction** | `500` users and `до 300` requests are both source-attested load-related counts; sources support load as measurement context | Which exact construction is broadened; whether a variable count is justified; allowed integer surface; count role; `до` inclusivity; noun vocabulary; attachment/cardinality; observation count; diagnostic policy | A distinct bounded context rule would be required. The C0 Rule ID and meaning must not be broadened silently. Exact route-load enrichment may also require a nested-relation decision. | Must leave C0 matches, Evidence, diagnostic `500`, condition Evidence, scalar observations, acceptance, and downstream behavior unchanged | No generic `при`, no inherited decimal/scientific/grouped counts, no equality, no count ontology, no nearest-bound rule, no changed `до` semantics | `BLOCKED` on current evidence. `600` is synthetic; the `300` case is a different and compound construction. |
| **E2 — represent one bounded compound relationship** | Exact route sentence and the separate exact percent-of-requests source example directly support joint proportion-plus-duration semantics under load; explicit percentile source provides a contrast | Primary identity; percentage role and denominator; metric boundary; load scope; nested `до 300` role; parent/child or relation model; multiplicity; unresolved propagation; Evidence owner; acceptance interaction | A new relation/compound representation or an explicitly justified use of existing components is required before grammar. A future production rule would need a separately approved identity. | Must preserve the three scalar anchors, result/condition Evidence, clause-level acceptance deduplication, unresolved `до`, ordering, and all downstream calculations | No percentage-to-percentile conversion, no inferred denominator/window, no inclusive `до`, no per-number acceptance criteria, no generic compound grammar | `BLOCKED` by semantic and representation gates |

### 9.1 E1 alternatives considered

Two superficially small E1 forms were evaluated:

1. **C0 integer substitution:** replace literal `500` with an ASCII-integer
   slot so that `600` matches. The existing domain could store the resulting
   context, but the only exact same-form source contains `500`. The route source
   cannot justify this substitution because it uses `при навантаженні до`, a
   different noun, and an explicit unresolved comparator. This alternative is
   `BLOCKED`.
2. **Exact route load context:** attach only `[117,159)` to the four-second
   observation. This is source-attested and narrower than generic grammar, but
   it overlaps an existing separate `до 300` observation and occurs alongside
   the `95 %` qualifier. Treating the overlap as context-only, dual-role, or an
   unlinked duplicate is itself the scientific decision. This alternative is
   also `BLOCKED` until that relationship is explicit.

### 9.2 E2 representation alternatives considered

| Alternative | Benefit | Scientific defect if selected now |
| --- | --- | --- |
| Keep three independent observations only | No domain change | Loses the joint success-proportion/duration/load relationship. |
| Put the percentage and load into the duration observation's single `context` | Reuses current fields | Conflates two roles, leaves scope/cardinality undefined, and gives no identity to the nested `до 300` observation. |
| Fold `для 95 % запитів` into the metric text | Could express a qualified metric | Metric boundary and meaning are not approved; it risks treating population scope as part of a generated metric. |
| Add a parent compound observation or explicit relation | Can preserve role and cardinality | No domain contract, relation vocabulary, Evidence ownership, or unresolved propagation is approved. |

No E2 alternative is ready for approval without a preceding representation
decision.

## 10. Smallest candidate next slice

### 10.1 Readiness conclusion

No production expansion beyond C0 is scientifically ready from the available
evidence. The only currently review-ready disposition is **E0**: keep C0 exact
and defer count/context and compound expansion. Selecting E0 would not reject
the source semantics; it would acknowledge that the current production model
cannot yet represent them without additional decisions.

This document does not silently select E0. It reports E0 as the only option not
blocked by missing scientific semantics. The researcher may instead direct
work toward E1 or E2 after resolving the applicable gates.

### 10.2 Smallest defensible next research slice

If further research is requested, the smallest defensible slice is a
**source-exact R2′ relationship decision**, not a detector implementation:

```text
Scope: only the exact source-attested R2′ construction.
Primary target candidate: route-generation duration bound [96,116).
Population qualifier candidate: [58,74), containing [62,66) "95 %".
Load-context candidate: [117,159).
Nested scalar preserved unchanged: [134,140) "до 300".
```

That decision slice would answer only:

1. whether `для 95 % запитів` is a dedicated population qualifier of the
   four-second target;
2. whether the load phrase is context of that same target;
3. whether the existing `до 300` observation is context-only content, a
   separately linked nested member, or an intentionally independent partial
   observation; and
4. whether the current domain is sufficient or one explicit relationship type
   is necessary.

It would keep C0, all scalar grammar, `до` inclusivity, percentile grammar,
acceptance behavior, calculations, Findings, reporter, and aggregation out of
scope. It is the smallest research target because it uses an exact source
sentence and does not pretend that `600` is evidence. It nevertheless remains
`BLOCKED` as an approval candidate until the four questions above receive
explicit answers and a complete Evidence/diagnostic contract is written.

There is therefore no scientifically defensible implementation slice to hand
off from SRM-05E. There is a bounded next **decision problem**, as described
above.

## 11. Explicit exclusions and blockers

### 11.1 Exclusions

Nothing in this document authorizes:

- changing or broadening `QUANT-001`, `QUANT-UK-001`,
  `QUANT-METRIC-001`, or `QUANT-CONTEXT-001`;
- replacing C0's literal `500` with a variable or with `600`;
- treating `500` or `600` as equality, a minimum, a maximum, a count unit, an
  independent constraint, or a second observation;
- generic `при` or load-context grammar;
- generated workload or population vocabulary, morphology, synonyms, or noun
  inflections;
- decimal-comma, decimal-point, grouped, signed, exponent, or written-out
  population counts;
- mapping `95 % запитів` to `95-й перцентиль`, or the reverse;
- inventing the denominator, population window, sample size, failure treatment,
  or percentile algorithm for `95 %`;
- resolving `до` as inclusive or exclusive;
- treating every explicit number as a separate observation;
- merging numeric anchors or introducing parent/child identity without an
  approved relationship;
- parser-distance, token-distance, character-distance, nearest-anchor, or
  cross-hard-boundary attachment;
- new context/count/compound ambiguity diagnostics;
- new metric vocabulary or implicit route-duration metric linkage;
- new expected-result or acceptance grammar;
- changing scalar-only acceptance containment, result-clause deduplication,
  criterion counts, judgeability, or acceptance diagnostics;
- changing Evidence ownership, exact offsets, family separation, or global
  source order;
- changing C/V/U formulas, contributions, applicability, Findings,
  `QUALITY_PROBLEM` behavior, reporter output, or aggregation; or
- allocating a Rule ID, implementation authorization, baseline, tag, release,
  or issue closure.

### 11.2 Blocking decisions

E1 is blocked by:

1. lack of a source-attested `600` or other same-form variable-count example;
2. no approved numeric surface policy for a context cardinal distinct from
   primary scalar syntax;
3. no decision whether a generalized count remains diagnostic-only inside an
   accepted context;
4. no approved general count/population role or noun boundary; and
5. the fact that the only alternative source count uses different, nested
   grammar.

E2 is blocked by:

1. no approved role for the percent phrase relative to the duration bound;
2. no denominator or measurement-window contract;
3. no approved implicit route-duration metric Evidence;
4. no decision on whether the load bound is context, a separate constraint, or
   both;
5. unresolved `до` inclusivity and count dimension;
6. no parent/child, qualifier, or compound relationship representation;
7. no cardinality, ordering, ambiguity, or unresolved-propagation contract; and
8. no decision on whether existing acceptance composition is sufficient for a
   semantically compound target.

## 12. Questions requiring researcher approval

The researcher must explicitly answer the following before any expansion can
be described as approved or implemented.

### 12.1 Count/context questions

1. Should C0 remain permanently exact at `500`, or may a later distinct rule
   abstract the count slot?
2. If abstraction is permitted, what is its scientific basis despite the
   `600` case being synthetic?
3. Which exact integer surfaces are admissible for a population cardinal, and
   are zero and leading zeros determinate negatives, unresolved cases, or
   permitted forms?
4. Does a generalized bare count remain context content only, with no equality,
   count unit, judgeability, or second observation?
5. Does the existing unresolved numeric diagnostic remain for every accepted
   generalized context count, or is a separately approved diagnostic-accounting
   change required?
6. What exact marker, noun phrase, spacing, punctuation, requirement position,
   uniqueness, and hard-boundary restrictions apply?

### 12.2 Percentage and percentile questions

7. Is `для 95 % запитів` a dedicated population qualifier, part of the metric,
   a quantitative context, or another role?
8. What exact request population and measurement window form the denominator,
   if either can be recovered from the requirement text?
9. Must the literal percent-of-requests construction remain distinct from an
   explicit percentile metric in every representation and report?
10. Can the percentage anchor be independently judgeable, or only as part of
    the compound “percentage of requests satisfying the duration bound” claim?

### 12.3 Load and compound-relation questions

11. Does `[117,159)` attach to the duration observation, the expected result, a
    compound parent, or more than one of them?
12. Is `[134,140)` `до 300` only an independently preserved partial anchor, a
    nested member linked to the primary target, or both?
13. Must `[134,159)` receive new Evidence for a count/load role, and if so which
    rule family owns it without replacing existing scalar or condition Evidence?
14. Is a new relation/domain type required, or can existing component fields
    express the exact relationship without conflating roles?
15. What are the cardinality and ambiguity rules when several percentages,
    bounds, contexts, results, or metrics compete?
16. What diagnostic and processing status applies when scalar anchors are
    accepted but their compound relationship cannot be resolved?
17. Must `ACCEPT-QUANT-001` remain completely unchanged, or is a separately
    scoped acceptance decision needed after a compound relation is represented?

### 12.4 Option decision

18. Approve only the conservative E0 disposition, or direct preparation of a
    fully specified E1 or E2 proposal after the relevant questions above are
    answered.

Until those answers exist, E1 and E2 remain `BLOCKED`, E0 is the only
review-ready no-expansion option, `RQD-008` remains
`PARTIALLY_APPROVED / OPEN`, and SRM-05 issue #73 remains `OPEN`.

