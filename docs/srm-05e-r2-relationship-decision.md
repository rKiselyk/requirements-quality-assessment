# SRM-05E — Exact R2′ Relationship Decision Research

**Issue:** #73 (`SRM-05`)  
**Document status:** `RESEARCH_ONLY / PROPOSED_FOR_RESEARCHER_REVIEW`  
**Decision effect:** none; all relationships and representations below are
candidate decisions only  
**Rule-ID effect:** none; no Rule ID is allocated

## 1. Objective and exact scope

This document prepares a decision-ready analysis of the relationships expressed
by the exact source-attested R2′ requirement:

```text
Після отримання події про перекриття дороги новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с при навантаженні до 300 одночасних запитів.
```

The research question is not whether the sentence contains three numeric
anchors. Existing production behavior already preserves `95 %`, `не більше ніж
за 4 с`, and `до 300`. The question is whether the source supports an explicit
relationship contract among those anchors and, if it does, what minimum
representation would preserve that contract without adding statistical,
measurement, acceptance, or scoring semantics.

The scope is only this exact R2′ construction. This document:

- analyzes the proportion-to-duration relationship;
- analyzes the load phrase's scope;
- compares four dispositions for the nested `до 300` observation;
- evaluates the existing `QuantitativeConstraintObservation` representation;
- compares candidate options R0, R1, R2, and R3; and
- identifies the smallest defensible researcher decision.

It does not specify detector code, approve a rule, allocate a Rule ID, change
the model specification, or authorize implementation.

The decision vocabulary used below is:

- `EXISTING_ACCEPTED`: already fixed by `docs/model-spec.md`;
- `SOURCE_ATTESTED`: present in an inspected original DOCX;
- `SOURCE_SUPPORTED`: a semantic relationship stated by the exact source, but
  not an approved production relationship;
- `PROPOSED_FOR_RESEARCHER_REVIEW`: a bounded candidate decision;
- `BLOCKED_FOR_IMPLEMENTATION`: no implementation may proceed before an
  explicit researcher decision and complete representation contract; and
- `EXCLUDED`: outside this task and not inferable from its evidence.

## 2. Source verification

### 2.1 Sources inspected

The following authoritative and original sources were inspected:

| Source | Material verified | Role here |
| --- | --- | --- |
| [`model-spec.md`](model-spec.md), §§7.14.6.6–7.14.6.8 | Scalar anchors, exact metric and C0 context enrichment, Evidence ownership, diagnostic preservation, and deferred grammar | Authoritative implementation model |
| [`model-spec.md`](model-spec.md), §7.15.10 | Current quantitative observation structure and component invariants | Authoritative representation |
| [`model-spec.md`](model-spec.md), §18 / `RQD-008` | Current partial approval and open nested/compound boundary | Authoritative decision status |
| [`srm-05e-count-and-compound-research.md`](srm-05e-count-and-compound-research.md) | Count roles, exact R2′ spans, compound alternatives, and the source-exact next research slice | Research traceability |
| [`srm-05d-implementation-acceptance-report.md`](srm-05d-implementation-acceptance-report.md) | Accepted C0 implementation invariants and exact `500` diagnostic | Implementation acceptance evidence |
| [`reference/Приклад_застосування_моделі.docx`](reference/Приклад_застосування_моделі.docx) | Exact R2′ wording in §8, table `Зміна \| Уточнене формулювання`, row `R2 → R2′`; explicit percentile contrast in row `R1 → R1′` | Original application-example evidence |
| [`reference/2.2_Взаємозвязок_вимог_і_якості.docx`](reference/2.2_Взаємозвязок_вимог_і_якості.docx) | Exact C0 example and the source example `95 % запитів мають оброблятися не довше ніж за 2 с` | Original relationship context |
| [`reference/2.3_Система_метрик.docx`](reference/2.3_Система_метрик.docx) | Observable quantity, unit, measurement conditions, and admissible-limit distinction | Original metrics context |

The original application-example DOCX contains the R2′ sentence exactly as
quoted in §1. It is not a paraphrase or a synthetic reconstruction. The DOCX
table text contains ordinary U+0020 SPACE characters between words, U+0025
PERCENT SIGN in `95 %`, and U+002E FULL STOP as the sentence terminator.

The exact trimmed sentence has 160 Unicode code points. All offsets in this
document are zero-based, start-inclusive, and end-exclusive ranges over those
code points.

### 2.2 What the original sources establish

The sources establish four distinctions relevant to R2′:

1. The application example states one required route-generation proposition
   containing a proportion of requests, a duration limit, and a load
   condition.
2. The separate source example `95 % запитів мають оброблятися не довше ніж
   за 2 с` confirms that a percent-of-requests construction can qualify
   compliance with a duration target. It does not call that construction a
   percentile.
3. The explicit source form `95-й перцентиль затримки ... — не більше 3 с` is
   textually and conceptually distinct. It must remain a negative contrast for
   any R2′ rule.
4. The metrics source distinguishes a measured quantity and admissible limit
   from measurement conditions. This supports preserving the load phrase as a
   condition on evaluation rather than silently turning every number in it into
   an independent criterion.

The sources do not supply a request-enumeration rule, measurement window,
sample-size rule, failure treatment, percentile algorithm, or conversion
between percent-of-requests and percentile latency.

## 3. Existing accepted baseline

The following statuses are authoritative and unchanged:

| Item | Current accepted status | Invariant for this decision |
| --- | --- | --- |
| `QUANT-001` / `QUANT-UK-001` | Existing accepted scalar baseline | Preserve each accepted scalar anchor, its observation identity, components, Evidence, source order, and diagnostic behavior. |
| `QUANT-METRIC-001` | `RESEARCHER_APPROVED / IMPLEMENTED_AND_ACCEPTED` | Preserve its exact `Час відгуку` linkage; do not generalize it into an implicit route-generation metric. |
| `QUANT-CONTEXT-001` | `RESEARCHER_APPROVED / IMPLEMENTED_AND_ACCEPTED` | Preserve exact C0, literal `500`, single enriched observation, context-only role, and the diagnostic over `500`. |
| SRM-05D C0 | `COMPLETED AND RESEARCHER_ACCEPTED` | No R2′ decision may broaden or reinterpret C0. |
| `COND-UK-001/002` | Existing approved bounded condition rules | Preserve their Evidence, ownership, diagnostics, and processing independently of any quantitative relationship. |
| `RESULT-UK-001/002` | Existing approved bounded result rules | Preserve existing result Evidence and do not generate a new result rule from quantitative linkage. |
| `ACCEPT-QUANT-001` | Existing approved composition | Preserve scalar-only containment, one criterion per result clause, judgeability, Evidence ownership, and diagnostics. |
| `RQD-008` | `PARTIALLY_APPROVED / OPEN` | Exact metric/context rules are closed; nested and compound quantitative relationships remain open. |
| SRM-05 issue #73 | `OPEN` | This research does not close the issue. |

For the exact R2′ text, the current quantitative baseline produces three
source-ordered observations and no quantitative diagnostic:

| Order | Existing Evidence | Span | Existing observation semantics |
| --- | --- | --- | --- |
| 1 | `QUANT-001:E001` — `95 %` | `[62,66)` | value `95`; unit `PERCENT`; no comparator, metric, or context |
| 2 | `QUANT-UK-001:E001` — `не більше ніж за 4 с` | `[96,116)` | `LESS_THAN_OR_EQUAL / INCLUSIVE`; value `4`; unit `SECOND`; no metric or context |
| 3 | `QUANT-UK-001:E002` — `до 300` | `[134,140)` | `UPPER_BOUND / UNRESOLVED`; value `300`; no approved unit, metric, or context |

The quantitative family outcome is `COMPLETE / DETECTED`. This is a successful
preservation of three anchors, not a representation of their joint meaning.
None of the three observations currently references either of the others.

The authoritative model also identifies the source-case result and acceptance
span `[44,116)` and the source-attested condition boundaries `[0,43)` and
`[117,159)`. Those structural-family spans have their own rule ownership and
must not be reused as quantitative Evidence identities.

There is a pre-existing boundary that a future implementation proposal must
not silently repair: the executable first-production `COND-UK-001` leading
template requires a comma-delimited leading condition. Applied by itself to the
exact R2′ line, whose leading `Після ...` phrase has no comma, it currently
returns `INCOMPLETE / UNRESOLVED` with candidate `[0,159)`. This does not change
the source-role map in the model specification, but it means a future R2′
relationship implementation must explicitly state whether it depends on
already accepted structural observations or recognizes only the exact
quantitative relationship. This document does not change condition, result, or
acceptance detection to remove that tension.

## 4. Exact R2′ component and Evidence map

### 4.1 Verified source boundaries

| Role | Exact text | Span | Current or candidate disposition |
| --- | --- | --- | --- |
| Event condition | `Після отримання події про перекриття дороги` | `[0,43)` | Existing source-attested condition boundary; not a quantitative component |
| Expected result / acceptance clause | `новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с` | `[44,116)` | Existing model-spec result and clause-level acceptance span |
| Route result core | `новий маршрут` | `[44,57)` | Source text naming the result; no new implicit metric proposed |
| Population/proportion phrase | `для 95 % запитів` | `[58,74)` | Candidate new relationship Evidence; contains the existing percent anchor |
| Existing percent anchor | `95 %` | `[62,66)` | Preserve `QUANT-001:E001` unchanged |
| Existing duration anchor | `не більше ніж за 4 с` | `[96,116)` | Preserve `QUANT-UK-001:E001` unchanged; candidate primary target |
| Duration value and unit | `4 с` | `[113,116)` | Contained in the duration anchor; no duplicate Evidence |
| Load phrase | `при навантаженні до 300 одночасних запитів` | `[117,159)` | Existing condition candidate and candidate quantitative relationship context |
| Nested count phrase | `до 300 одночасних запитів` | `[134,159)` | Source boundary useful for analysis; no new Evidence is required merely to preserve the noun phrase |
| Existing nested scalar | `до 300` | `[134,140)` | Preserve `QUANT-UK-001:E002` unchanged |
| Count value | `300` | `[137,140)` | Existing value component inside `до 300` |
| Count/population phrase | `одночасних запитів` | `[141,159)` | Source text, not an approved unit ontology entry |
| Terminator | `.` | `[159,160)` | Excluded from all candidate Evidence |

The smallest candidate new Evidence boundaries are `[58,74)` for the complete
population qualifier and `[117,159)` for the complete load context. Neither may
replace the existing inner scalar Evidence. A future approved rule would need
its own rule-owned Evidence identities for these spans; this document does not
allocate those identities or a Rule ID.

No new `[44,57)` metric Evidence is scientifically necessary for the bounded
relationship. The source explicitly states required route formation, but the
current quantitative metric component has no approved implicit
route-generation vocabulary. The relationship can remain grounded in the
existing duration anchor and existing result/acceptance containment without
inventing a metric label.

### 4.2 Ownership and overlap contract

The exact construction requires overlap, but not shared Evidence identity.

Allowed overlaps for a future bounded relation are:

- population Evidence `[58,74)` overlapping existing result and acceptance
  Evidence `[44,116)` and containing scalar Evidence `[62,66)`;
- duration scalar Evidence `[96,116)` overlapping result and acceptance
  Evidence `[44,116)`;
- load relationship Evidence `[117,159)` sharing its span with condition-family
  Evidence when that condition observation is accepted, but retaining a
  distinct quantitative owner and Evidence identity; and
- load Evidence `[117,159)` containing existing scalar Evidence `[134,140)`.

The following are forbidden:

- replacing `[62,66)`, `[96,116)`, or `[134,140)` with a larger span;
- merging the three existing observations;
- deleting the independent `до 300` observation after adding context;
- making a quantitative component reference `COND-UK-*`, `RESULT-UK-*`, or
  `ACCEPT-QUANT-001` Evidence;
- making a structural or acceptance observation reference future relationship
  Evidence;
- treating overlap alone as proof of attachment;
- manufacturing Evidence for an inferred denominator, window, percentile,
  metric, or inclusivity decision; or
- changing Evidence order from ascending source order.

### 4.3 Observation identity and source order

The three existing observations remain the same immutable observations in the
same tuple positions. A candidate relationship must reference them rather than
copy, merge, or recreate them. Because the current domain has no observation
identifier, the exact bounded proposal may identify each participating member
through its unique existing scalar Evidence reference, provided the contract
requires exactly one matching observation per member and rejects competition.

Any future relationship-owned Evidence joins the public Evidence collection in
global source order under the existing stable sort. Rule-local Evidence
ordinals would remain local to their future owning rule. This document neither
predicts nor allocates those IDs.

## 5. Proportion-to-duration relationship

### 5.1 Source-supported role

`для 95 % запитів` is a population/proportion qualifier over the source-named
population `запитів`. In the complete required-result clause, it states the
proportion of requests for which route formation must satisfy the four-second
duration bound.

The relationship explicitly expressed by the source is therefore:

```text
stated proportion of requests
    satisfies
route formed no more than four seconds after the stated event
```

This is not three claims. It is one compound success condition in which:

- `95 %` supplies the stated proportion;
- `запитів` supplies the lexical population being qualified;
- `не більше ніж за 4 с` supplies the duration bound; and
- the required route-generation result supplies the behavior whose timely
  completion is judged.

The percentage is not an independent measured percentage with a complete
meaning outside the result clause. The duration bound remains a valid separate
scalar observation, but the `95 %` observation alone does not state what counts
as success.

### 5.2 Explicit exclusions

The source does not authorize any of the following:

- interpreting `95 % запитів` as `95-й перцентиль`;
- converting the clause to a percentile-latency formula;
- choosing an observation window;
- defining which requests enter or leave the denominator;
- deciding how failures, cancellations, retries, duplicates, or missing values
  affect that denominator;
- specifying a sample size, rounding rule, confidence interval, or statistical
  estimator; or
- treating the percentage anchor as independently judgeable without the
  duration success condition.

The relation can be represented descriptively without those decisions. It
cannot be used to calculate compliance or introduce new acceptance
judgeability until a separate measurement contract supplies them.

### 5.3 Candidate contract for R1

A bounded R1 decision could approve only this statement:

> In exact R2′, `[58,74)` is a population/proportion qualifier whose existing
> `[62,66)` percent observation qualifies satisfaction of the existing
> `[96,116)` duration-bound observation for the source-named population
> `запитів`.

That statement is source-supported and does not require a denominator
algorithm. It does require a representation capable of distinguishing the
population qualifier from a metric, context, independent percentage target, or
percentile. Existing fields do not provide that distinction.

## 6. Load-to-duration relationship

### 6.1 Source-supported scope

`при навантаженні до 300 одночасних запитів` is an explicit load condition on
the required route-generation proposition. Its support does not rest on nearest
numeric proximity:

- it is a complete `при навантаженні ...` adjunct in the same hard-bounded
  normative clause;
- the exact sentence contains one required route-generation result and one
  duration target before that adjunct, so there is no competing governing
  target in the source case;
- the source metrics discussion treats measurement conditions separately from
  quantities and admissible limits; and
- the application example presents the phrase as part of the same refined R2′
  requirement, not as a separate requirement.

The strongest source-supported scope is the complete compound success
condition: the route-generation duration target for the stated proportion of
requests is evaluated under the stated load. Consequently the load condition
also qualifies the expected result and the four-second target, but it should be
represented once at the compound relationship level rather than copied onto
several members.

Attaching the load only to the percentage observation is unsupported. Treating
it as an independently judgeable acceptance criterion is also unsupported.

### 6.2 What remains a modeling decision

The source supports semantic scope but does not choose a domain layout. A
researcher must still decide whether a future representation:

1. attaches `[117,159)` directly as `context` of the duration observation;
2. attaches it to an explicit proportion-duration relationship; or
3. records both a primary relation-level context and a derived link to the
   duration member.

Option 2 is the minimum non-duplicating representation for the full R2′
meaning. Option 1 can express an R2-only partial decision, but it cannot by
itself state that the same load governs the proportion-qualified success
condition. Option 3 adds redundant linkage unless a future consumer requires
both views and a consistency rule is approved.

The exact bounded proposal therefore treats `[117,159)` as context of the
compound relation, with the duration bound as that relation's primary target.
This is a candidate modeling decision, not an approval.

## 7. Nested `до 300` relationship

The existing semantics are fixed:

```text
comparator = UPPER_BOUND
inclusivity = UNRESOLVED
value = 300
unit = None
metric = None
context = None
```

The source never authorizes normalization to `≤ 300`. It also does not establish
an approved count unit or an independently judgeable workload criterion.

### 7.1 Alternatives

| Alternative | What the source and baseline support | What would remain a modeling decision | Assessment |
| --- | --- | --- | --- |
| **A — separate partial observation only** | Existing `[134,140)` observation is valid and must remain. | Whether its containment inside the load phrase should be explicitly linked. | Sufficient for R0; incomplete for any explicit load relationship because it loses the stated internal bound. |
| **B — member linked to the primary duration target** | The load phrase containing `до 300` governs the route target. | Whether the scalar is linked directly to duration or through relation-level context; how to preserve separate identity. | Source-supported in direction, but insufficient if it replaces or absorbs the existing observation. |
| **C — separately preserved observation and member of load context** | Both facts are explicit: `до 300` is an accepted upper-directed scalar, and it occurs inside the stated load condition. | The relation-reference mechanism and whether unresolved inclusivity propagates to relationship completeness. | Smallest source-faithful candidate. Preserve the observation; link it as the scalar member of the load context without changing its semantics. |
| **D — unresolved pending further evidence** | Independent judgeability, count dimension, and inclusivity are unresolved. | Whether even lexical containment may be represented. | Necessary for those unresolved semantics, but too conservative about the exact containment relation, which is directly visible in the source. |

Alternative C is the most defensible candidate for researcher review. The
source supports lexical and semantic membership of `до 300` in the load
condition; the current baseline requires separate observation preservation.
The proposed link does not make the scalar inclusive, independently judgeable,
or a count unit.

### 7.2 Unresolved propagation

If Alternative C is approved, `UPPER_BOUND / UNRESOLVED` remains local to the
load-bound member. The relationship may be present and source-resolved while a
member's endpoint inclusivity remains unresolved. The relationship must not be
reported as if the load threshold were `≤ 300`.

This distinction prevents two incorrect outcomes:

- rejecting the entire source relationship merely because `до` inclusivity is
  unresolved; and
- treating successful relationship detection as resolution of `до`.

## 8. Representation alternatives

### 8.1 Sufficiency of existing fields

The current `QuantitativeConstraintObservation` has one optional `metric`, one
optional `context`, one comparator, one value, one unit, unresolved component
names, and a flat Evidence-reference tuple.

| Required R2′ meaning | Existing fields sufficient? | Reason |
| --- | --- | --- |
| Preserve three scalar anchors independently | Yes | Existing observations already do this. |
| Attach the complete load phrase to the duration observation | Superficially yes | The singular `context` can hold `[117,159)`, but cannot identify the separate nested `до 300` observation as a member. |
| State that `95 %` is the proportion of requests satisfying the duration target | No | There is no population/proportion qualifier or typed relation between observations. |
| Preserve `до 300` both separately and as the load-bound member | No | There is no observation-reference or parent/member link. |
| State that one load context governs the joint proportion-duration condition | No | A flat `context` field on one scalar observation does not encode relation-level scope. |
| Preserve the exact result/acceptance interaction without creating new criteria | Yes, if left unchanged | Existing containment and deduplication already do this; the relationship must remain transparent to acceptance. |

Putting both the population qualifier and load phrase into the existing
`context` field would conflate different roles. Folding `для 95 % запитів` into
`metric` would invent a metric boundary. Merging all scalar members would
violate the one-comparator/one-value/one-unit shape and destroy independent
provenance. Existing fields are therefore insufficient for R1 or R3 and only
partially sufficient for R2.

### 8.2 Minimum semantic representation capability

The minimum additional capability is one bounded, role-aware relationship for
the exact source construction. It must be able to reference, without copying or
mutating:

1. one primary existing duration observation, identified by scalar Evidence
   `[96,116)`;
2. one existing percent observation, identified by scalar Evidence `[62,66)`,
   plus complete population-qualifier Evidence `[58,74)`;
3. one complete load-context Evidence span `[117,159)`; and
4. one existing nested load-bound observation, identified by scalar Evidence
   `[134,140)`.

Its fixed semantic roles are:

```text
primary target: duration bound
population qualifier: stated proportion of source-named requests satisfying target
measurement/load context: condition under which the compound target applies
load-bound member: separately preserved UPPER_BOUND / UNRESOLVED observation
```

The relationship must require exactly one member for each role and reject the
bounded rule when members compete. It is not a generic quantitative expression
tree, Boolean algebra, reusable parser attachment engine, or count ontology.
The source justifies these four roles; coding convenience does not.

The exact domain shape remains a researcher modeling decision. Two shapes can
provide the minimum capability:

- a dedicated bounded relationship record that references existing member
  observations through their unique scalar Evidence; or
- an extension attached to the primary duration observation with a dedicated
  population-qualifier component and an explicit reference to the nested
  load-bound observation.

The first shape represents relation-level load scope without duplication and is
the cleaner R3 candidate. The second is smaller structurally but risks making
the load appear to govern only duration and not the compound condition. This
document proposes the required semantic capability, not a production class or
field layout.

### 8.3 Evidence contract for a future bounded relationship

A complete future proposal must fix all of the following before implementation:

- exact source match and hard boundaries;
- future owning Rule ID and rule-local Evidence IDs;
- relationship-owned Evidence `[58,74)` and `[117,159)`;
- references to the three unchanged scalar Evidence items;
- exactly-one cardinality for percent, duration, load phrase, and load scalar;
- stable source ordering and de-duplication;
- separate ownership from condition, result, and acceptance Evidence;
- deterministic rejection of percentile wording, missing population nouns,
  hard-boundary splits, competing members, changed wording, and synthetic
  generalizations; and
- diagnostic behavior for recognized-but-unresolvable relationship candidates.

No additional `[134,159)` Evidence is required for the minimum contract. The
complete load phrase plus the existing inner scalar already preserves the noun
phrase and nesting. A separate nested-count Evidence item would be justified
only if a later decision assigns `одночасних запитів` its own count-dimension
role.

## 9. Acceptance and diagnostic invariants

### 9.1 Expected result and acceptance

The existing result and acceptance relationship remains unchanged:

- result Evidence is `[44,116)` when accepted by the existing result rule;
- the percent and duration scalar Evidence lie inside that result span;
- `ACCEPT-QUANT-001` produces at most one clause-level criterion for that
  result, despite two contained quantitative anchors;
- load Evidence `[117,159)` and scalar `[134,140)` lie outside the result span
  and cannot independently satisfy acceptance containment; and
- no relationship option creates a new acceptance criterion, changes
  judgeability, or alters deduplication.

The proposed relationship is descriptive. It explains why the percentage and
duration anchors form one compound target, but it does not supply the missing
measurement procedure required to compute whether 95 percent was achieved.
Current acceptance behavior must remain exactly as accepted unless a separate
research task changes it.

### 9.2 Diagnostics and unresolved behavior

Under the current exact scalar baseline, R2′ has no quantitative diagnostic:
all three numeric anchors are accepted. A future relationship rule must not
reinterpret that absence as proof that the relationship is already represented.

For the bounded exact-source proposal:

- an exact positive may add the relationship and its Evidence without changing
  any existing scalar, condition, result, or acceptance outcome;
- a deterministic non-match adds no relationship, Evidence, or new diagnostic
  and preserves all existing outputs;
- a recognized exact-form candidate with competing percentage, duration, or
  load members requires a separately approved relationship-ambiguity
  diagnostic before it may produce `INCOMPLETE`; no diagnostic code is
  allocated here;
- unresolved `до` inclusivity stays on the existing load observation and does
  not create a new relationship diagnostic;
- the current exact-line `COND-UK-001` unresolved outcome, where present, must
  not be suppressed by quantitative relationship detection; and
- a relationship implementation must declare whether accepted structural
  dependencies are mandatory. If they are mandatory, current exact-line
  condition/result integration is an implementation blocker to resolve in a
  separate approved contract rather than by fallback.

### 9.3 Protected SRM-05D behavior

Every option preserves:

- exact C0 `QUANT-CONTEXT-001` grammar and literal `500`;
- one C0 quantitative observation;
- `QUANT-METRIC-001:E001`, `QUANT-001:E001`, and
  `QUANT-CONTEXT-001:E001` ownership and order for C0;
- `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` over C0 `[22,25)` `500` with
  `INCOMPLETE / DETECTED`;
- independent `COND-UK-001:E001` over C0 `[18,49)`;
- all `QUANT-001`, `QUANT-UK-001`, `COND-UK-001/002`, and
  `ACCEPT-QUANT-001` behavior;
- existing C/V/U calculations, Findings, reporter, and aggregation; and
- the negative result for `600` and every C0 variant outside the exact approved
  suffix.

## 10. R0/R1/R2/R3 decision matrix

### 10.1 Comparative matrix

| Option | Source support | Semantics requiring approval | Required representation and Evidence | Diagnostic and compatibility implications | Approval blockers | Readiness |
| --- | --- | --- | --- | --- | --- | --- |
| **R0 — preserve independent observations; defer relationships** | Fully supports preservation of all explicit anchors, but not their joint meaning. | No new semantics. Researcher accepts deliberate loss of explicit compound scope for MVP. | No representation change; no new Evidence. | No new diagnostics or compatibility risk. Existing source relationships remain unavailable to consumers. | None for no-expansion; unsuitable if explicit relationship preservation is required. | `DECISION_READY` as a conservative deferral only. |
| **R1 — bounded population/proportion relation to four-second target** | Directly supported by exact R2′ and reinforced by the separate source example `95 % запитів ... не довше ніж за 2 с`. | Approve `[58,74)` as population qualifier; approve the existing percent observation as qualifying satisfaction of `[96,116)`; keep denominator/window/algorithm absent. | Requires one typed population-to-target relation and new Evidence `[58,74)`; existing fields alone are insufficient. | No acceptance or score change. Exact non-match should preserve baseline. A future ambiguity diagnostic is needed only if the rule broadens beyond the unique exact form. | Researcher must approve the qualifier role, exact cardinality, ownership, and representation. R1 alone omits the load scope. | `PROPOSED_FOR_RESEARCHER_REVIEW`; scientifically defensible but partial. |
| **R2 — bounded load context with separate `до 300` observation** | Directly supported by exact `при навантаженні ...`; metrics source supports measurement-condition role. | Approve load scope on the primary target or relation; approve Alternative C for `до 300`; preserve unresolved inclusivity and non-judgeability. | Existing `context` can preserve the full phrase, but an explicit member reference is required to link separate `[134,140)` observation. New Evidence `[117,159)`. | Load remains outside acceptance containment. No suppression of condition Evidence or `до` uncertainty. Competing targets require deterministic negative or a future diagnostic. | Researcher must approve relation-level versus duration-only scope and the nested-member mechanism. R2 alone omits proportion-to-duration meaning. | `PROPOSED_FOR_RESEARCHER_REVIEW`; scientifically defensible but partial. |
| **R3 — exact joint proportion + duration + load relationship** | Best match to the one source proposition: stated proportion satisfies duration target under stated load. | Approve R1 semantics, R2 relation-level scope, Alternative C, exactly-one cardinality, and transparent acceptance behavior. Explicitly leave statistical and `до` semantics unresolved. | One bounded role-aware relationship referencing all three existing observations; new Evidence `[58,74)` and `[117,159)`; no generic tree and no new metric. | Highest representation impact but lowest semantic loss. Must preserve every existing observation, structural outcome, criterion count, diagnostic, and downstream result. No broad grammar follows. | Explicit researcher approval of the semantic roles and minimum relation capability; future Rule ID and full diagnostic contract; resolution of whether implementation depends on currently accepted structural observations. | `PROPOSED_FOR_RESEARCHER_REVIEW`; smallest full-fidelity candidate, still `BLOCKED_FOR_IMPLEMENTATION`. |

### 10.2 Positive and negative reference cases

| Option | Positive reference | Negative or boundary references |
| --- | --- | --- |
| R0 | Exact R2′ retains the three current scalar observations in source order. | Any attempt to infer linkage, merge anchors, or add Evidence is outside R0. |
| R1 | Exact `[58,74)` plus `[96,116)` inside the unique result clause; separate source example `95 % запитів мають оброблятися не довше ніж за 2 с` supports the same role distinction. | Source-attested `95-й перцентиль ...` is not R1; synthetic percent without `запитів`, hard-boundary separation, competing percentages, or competing duration bounds must not attach. |
| R2 | Exact `[117,159)` after the unique R2′ target, containing existing `[134,140)`. | A load fragment without a governing target, a hard-boundary split, competing targets or contexts, changed marker/noun/count, and C0's different `при 500 ...` construction do not establish R2. |
| R3 | Only the complete exact source R2′ sentence supplies all four required roles without competition. | The percentile R1′ source, partial fragments, reordered or paraphrased strings, synthetic `600`, added competing members, or any inferred `≤ 300` semantics are outside R3. |

Synthetic strings in the negative column are boundary-analysis cases only. They
are not source evidence and cannot justify generalization.

### 10.3 Backward-compatibility risk

R0 has no representation risk but permanently withholds explicit source
semantics. R1 adds the smallest new semantic relation but may later require
migration into an R3 parent. R2 can superficially reuse `context`, but doing so
without a nested-member link risks losing `до 300` identity. R3 has the largest
domain impact, yet it avoids later contradiction by representing the source
once at the level where the load actually applies.

The primary R3 risks are accidental broadening and unintended downstream use.
They are controlled only if the future contract is exact-source, requires one
member per role, adds no statistical interpretation, remains transparent to
acceptance and scores, and preserves every existing observation.

## 11. Minimum defensible next decision

The smallest decision that preserves the complete explicit meaning of R2′ is
R3 with a bounded relationship capability, not a detector implementation.
R1 and R2 are scientifically defensible sub-decisions, but either one alone
leaves a different explicit part of the same source proposition unrepresented.

The proposed researcher decision is therefore:

1. **Proportion role:** approve `[58,74)` as a population/proportion qualifier
   whose existing `[62,66)` observation qualifies satisfaction of the existing
   `[96,116)` duration target. Do not approve percentile or measurement
   algorithms.
2. **Load scope:** approve `[117,159)` once as the load context of the compound
   proportion-duration target. Its semantic reach includes the duration target
   and required result; do not duplicate it onto independent members.
3. **Nested scalar:** select Alternative C. Preserve `[134,140)` as its existing
   separate observation and reference it as the load-bound member, without
   changing `UPPER_BOUND / UNRESOLVED`, adding a count unit, or making it
   independently judgeable.
4. **Representation:** approve only the minimum role-aware relationship
   capability described in §8.2. Do not approve a generic expression tree,
   generic load grammar, or an implicit route-duration metric.
5. **Compatibility:** keep result, acceptance, diagnostics, C/V/U, Findings,
   reporter, and aggregation unchanged.

This is a scientifically defensible exact-source contract because every
positive semantic edge is stated by the one source proposition or its
source-supported role distinctions. The contract deliberately stores no
denominator algorithm, measurement window, percentile conversion, or resolved
`до` boundary.

The candidate is `PROPOSED_FOR_RESEARCHER_REVIEW`, not approved. Implementation
remains `BLOCKED_FOR_IMPLEMENTATION` until the researcher explicitly accepts or
rejects the five decisions above, chooses the domain shape, allocates a future
Rule ID in a separate task, supplies the final diagnostic contract, and states
how the relationship composes with existing structural-observation
dependencies.

If the researcher does not want a new relationship representation in MVP
v0.1, R0 is the complete conservative alternative. R0 should be recorded as an
intentional deferral, not as a conclusion that the source lacks a relationship.

## 12. Explicit exclusions

Nothing in this document authorizes:

- changing `docs/model-spec.md` or any existing SRM-05D/SRM-05E document;
- changing or broadening `QUANT-001`, `QUANT-UK-001`,
  `QUANT-METRIC-001`, or `QUANT-CONTEXT-001`;
- allocating a new Rule ID;
- implementing a relationship, component, detector, diagnostic, or domain
  type;
- treating `95 % запитів` as a percentile;
- defining a denominator, measurement window, sample size, percentile method,
  failure treatment, rounding rule, or statistical conversion;
- converting `до 300` to `≤ 300`, resolving its inclusivity, assigning a count
  unit, or making it independently judgeable;
- generating an implicit route-duration metric or metric Evidence;
- using proximity, distance, or parser fallback to choose an attachment;
- generalizing from exact R2′ to paraphrases, other loads, other populations,
  changed word forms, or synthetic `600`;
- creating one acceptance criterion for each number;
- changing result or condition grammar to make the exact line fit a new rule;
- suppressing or replacing any existing diagnostic;
- changing applicability, C/V/U calculations, Findings, `QUALITY_PROBLEM`
  behavior, reporter output, or specification aggregation; or
- creating a baseline, tag, release, issue closure, commit, branch, or pull
  request.

## 13. Questions requiring researcher approval

The following questions are deliberately left for an explicit researcher
decision:

1. Approve R0 deferral, R1, R2, or the bounded R3 candidate?
2. Is `[58,74)` approved as a dedicated population/proportion qualifier of the
   `[96,116)` duration target, distinct from metric and context?
3. Is the percentage member allowed to remain descriptively linked while the
   denominator and measurement window are unspecified?
4. Is `[117,159)` approved as context of the compound proportion-duration
   relationship rather than context only of the duration scalar?
5. Is Alternative C approved for `[134,140)`: separate observation plus linked
   load-bound member?
6. Does unresolved `до` inclusivity remain local to that member while the
   relationship itself can be detected?
7. Should the minimum capability be a dedicated bounded relationship record or
   an extension on the primary duration observation?
8. May exact member identity be represented through each observation's unique
   scalar Evidence reference, or must a separately approved stable observation
   identifier be added?
9. Must a future relationship rule depend on accepted `RESULT-UK-*` and
   `COND-UK-*` observations, or may it recognize the exact quantitative
   relationship while preserving their independent outcomes?
10. If structural dependencies are mandatory, how should the existing exact-line
    `COND-UK-001` unresolved boundary be reconciled without changing this task's
    protected grammar?
11. For a future exact-only rule, is a deterministic non-match sufficient, or
    must a new relationship-ambiguity diagnostic be approved for competing
    members?
12. Confirm that acceptance containment, criterion count, judgeability, scores,
    Findings, reporter, and aggregation remain unchanged.

Until those questions are answered, no R1, R2, or R3 relationship is
`RESEARCHER_APPROVED`, no implementation is authorized, `RQD-008` remains
`PARTIALLY_APPROVED / OPEN`, and SRM-05 issue #73 remains `OPEN`.
