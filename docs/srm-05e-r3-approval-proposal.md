# SRM-05E — Bounded R3 Scientific Approval Proposal

**Issue:** #73 (`SRM-05`)  
**Proposal scope:** one exact source-attested R2′ compound quantitative
relationship  
**Final proposal status:** `PROPOSED_FOR_RESEARCHER_APPROVAL`

This document asks the researcher to approve, revise, or reject one bounded R3
contract. It records no scientific approval, implementation authorization,
Rule ID allocation, production change, baseline, tag, release, or issue
closure. Every proposed decision below remains pending until the researcher
explicitly approves it.

## 1. Decision requested from the researcher

The proposed R3 decision is to represent the exact R2′ construction as one
role-aware quantitative relationship:

> The stated proportion of requests satisfies the four-second route-generation
> target under the stated concurrent-request load.

The exact source requirement is:

```text
Після отримання події про перекриття дороги новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с при навантаженні до 300 одночасних запитів.
```

The relationship would reference, without merging or changing, the existing
percent, duration, and load-bound observations. It would add complete Evidence
for the population qualifier and load context. It would not convert the source
into three unrelated pass/fail requirements.

The proposal selects:

1. a dedicated bounded relationship record rather than an extension on the
   duration observation;
2. the nested-role disposition in which `до 300` remains a separate partial
   observation and is also referenced as the load-bound member; and
3. structural disposition B: R3 recognizes only the exact quantitative
   relationship independently of structural-detector success, while preserving
   every current `COND-UK-*`, `RESULT-UK-*`, and acceptance outcome.

## 2. Source basis and protected baseline

### 2.1 Sources

The proposal is based on:

- [`model-spec.md`](model-spec.md) §§7.14.6.6–7.14.6.8, §7.15.10, and
  §18 / `RQD-008`;
- [`srm-05e-count-and-compound-research.md`](srm-05e-count-and-compound-research.md);
- [`srm-05e-r2-relationship-decision.md`](srm-05e-r2-relationship-decision.md);
- [`srm-05d-implementation-acceptance-report.md`](srm-05d-implementation-acceptance-report.md);
- [`reference/Приклад_застосування_моделі.docx`](reference/Приклад_застосування_моделі.docx),
  §8, row `R2 → R2′`; and
- the supporting role distinctions in
  [`reference/2.2_Взаємозвязок_вимог_і_якості.docx`](reference/2.2_Взаємозвязок_вимог_і_якості.docx)
  and [`reference/2.3_Система_метрик.docx`](reference/2.3_Система_метрик.docx).

The exact R2′ wording was reverified against the original application-example
DOCX table, not a paraphrase or synthetic string. The trimmed sentence has 160
Unicode code points. Its whitespace characters are U+0020 SPACE; `95 %` uses
U+0025 PERCENT SIGN; the terminator is U+002E FULL STOP.

### 2.2 Protected statuses

| Item | Current status | Protected consequence |
| --- | --- | --- |
| `QUANT-METRIC-001` | `RESEARCHER_APPROVED / IMPLEMENTED_AND_ACCEPTED` | No grammar, Evidence, observation, or metric change. |
| `QUANT-CONTEXT-001` | `RESEARCHER_APPROVED / IMPLEMENTED_AND_ACCEPTED` | Exact C0, literal `500`, context role, and diagnostic remain unchanged. |
| SRM-05D C0 | `COMPLETED AND RESEARCHER_ACCEPTED` | R3 neither broadens C0 nor reuses its Rule ID. |
| `RQD-008` | `PARTIALLY_APPROVED / OPEN` | R3 would close only the exact relationship slice if separately approved. |
| SRM-05 issue #73 | `OPEN` | This proposal does not close it. |

The proposal also protects all current `QUANT-001`, `QUANT-UK-001`,
`COND-UK-001/002`, `RESULT-UK-001/002`, and `ACCEPT-QUANT-001` contracts.

## 3. Exact proposed R3 source contract

### 3.1 Exact source grammar

R3 is proposed only for this complete trimmed `Requirement.text`:

```text
Після<U+0020>отримання<U+0020>події<U+0020>про<U+0020>перекриття<U+0020>дороги<U+0020>новий<U+0020>маршрут<U+0020>для<U+0020>95<U+0020>%<U+0020>запитів<U+0020>має<U+0020>бути<U+0020>сформований<U+0020>не<U+0020>більше<U+0020>ніж<U+0020>за<U+0020>4<U+0020>с<U+0020>при<U+0020>навантаженні<U+0020>до<U+0020>300<U+0020>одночасних<U+0020>запитів.
```

The line wrapping is editorial only. Every character, casing choice, token,
U+0020 separator, and final U+002E is exact. The proposed contract has no
casefolded, morphology-generated, parser-assisted, punctuation-tolerant, or
whitespace-generalized variant.

Any changed, missing, reordered, inserted, or paraphrased material is a
deterministic R3 non-match. Existing detector-family behavior for that text is
preserved independently.

### 3.2 Required existing scalar members

The exact relationship may exist only when these three already accepted,
source-ordered scalar observations are present and unchanged:

| Role in R3 | Existing Evidence | Span | Required existing semantics |
| --- | --- | --- | --- |
| Percent member | `QUANT-001:E001` — `95 %` | `[62,66)` | value `95`; unit `PERCENT`; comparator, metric, and context absent |
| Primary duration member | `QUANT-UK-001:E001` — `не більше ніж за 4 с` | `[96,116)` | `LESS_THAN_OR_EQUAL / INCLUSIVE`; value `4`; unit `SECOND`; metric and context absent |
| Load-bound member | `QUANT-UK-001:E002` — `до 300` | `[134,140)` | `UPPER_BOUND / UNRESOLVED`; value `300`; unit, metric, and context absent |

R3 does not reparse these anchors. It does not replace their Evidence, mutate
their components, change their tuple positions, or create copies. Existing
observation identity is preserved through the exact scalar Evidence reference
that already belongs to each observation.

## 4. Proposed population role

The complete population qualifier is:

```text
для 95 % запитів
[58,74)
```

Its proposed binding role is:

> The existing percent member `[62,66)` states the proportion of the
> source-named population `запитів` that satisfies the existing primary
> duration member `[96,116)` for the route-generation behavior stated by exact
> R2′.

The complete qualifier and the scalar have distinct purposes:

- `[58,74)` preserves the qualifier construction and source-named population;
- `[62,66)` preserves the already accepted numeric value and `PERCENT` unit;
  and
- `[96,116)` preserves the already accepted duration target against which the
  stated proportion is qualified.

The proposed relationship is descriptive and source-bound. It expressly does
not approve:

- conversion of `95 % запитів` into `95-й перцентиль`;
- a denominator-selection or request-enumeration algorithm;
- a measurement window;
- a sample size;
- failure, retry, cancellation, duplicate, or missing-request treatment;
- a rounding convention, confidence rule, or statistical estimator; or
- independent judgeability of the percent member without the primary duration
  target.

The missing measurement procedure does not erase the explicitly stated
relationship. It does prevent R3 from becoming a new compliance calculation or
statistical rule.

## 5. Proposed load role and nested scalar disposition

The complete load context is:

```text
при навантаженні до 300 одночасних запитів
[117,159)
```

Its proposed binding role is the measurement/load condition under which the
joint proportion-duration target applies. The context is stored once on the
relationship. It is not copied into the percent, duration, and load-bound
observations.

The proposed nested-role disposition is:

```text
separate existing partial observation
    AND
load-bound member referenced by the R3 relationship
```

This is Alternative C from the R2′ research. It is preferred because the source
explicitly places `до 300` inside the load phrase, while the accepted scalar
baseline independently requires `[134,140)` to remain its own observation.

The relationship references `QUANT-UK-001:E002` as its one load-bound member.
That reference records membership and nothing more. It does not:

- convert `UPPER_BOUND` to `LESS_THAN_OR_EQUAL`;
- resolve `UNRESOLVED` inclusivity;
- introduce a count unit for `одночасних запитів`;
- make `до 300` independently judgeable;
- turn the load phrase into a separate acceptance criterion; or
- erase the load scalar by treating the complete phrase as context-only.

No separate Evidence `[134,159)` is proposed. The complete context Evidence
`[117,159)` preserves the population words, while the unchanged inner scalar
Evidence `[134,140)` preserves the bound.

## 6. Preferred minimum representation

### 6.1 Alternatives considered

| Alternative | Benefit | Scientific consequence | Disposition |
| --- | --- | --- | --- |
| **A — dedicated role-aware relationship record** | Represents the source proposition once at the level where population, target, and load meet; preserves all scalar identities. | Requires one bounded future domain addition and a separate relationship collection. | **Preferred.** |
| **B — extension attached to the duration observation** | Smaller apparent change to the existing observation type. | Makes relation-level load scope appear to be duration-only context, couples one scalar observation to two external members, and risks later duplication or mutation. | Not proposed. |

The preferred choice follows source semantics rather than implementation
convenience. R3 is a relationship among existing observations, not an enriched
form of one observation.

### 6.2 Proposed semantic identity

The minimum future addition is one dedicated bounded record whose type itself
means:

```text
exact R2′ proportion-of-requests
satisfying a duration target
under one load context containing one load bound
```

The following name is explanatory only:

```text
ExactR2RelationshipObservation
PROPOSED / NOT ALLOCATED
```

No generic `relationship_kind` vocabulary is required because the dedicated
record has only this one meaning. The proposed type is not a generic
quantitative expression tree, Boolean operator, reusable attachment graph,
general-purpose relationship framework, or count ontology.

The relationship would belong to feature family
`QUANTITATIVE_CONSTRAINT`. To keep calculators and accepted scalar consumers
unchanged, it must be stored in a separate bounded relationship tuple associated
with the quantitative-family extraction result, not inserted into the existing
`quantitative_constraints` observation tuple. The exact field and type names
are implementation details and remain provisional.

### 6.3 Proposed record content

The record requires only these roles:

```text
feature_id
population_qualifier_evidence_ref
percent_member_evidence_ref
primary_duration_member_evidence_ref
load_context_evidence_ref
load_bound_member_evidence_ref
evidence_refs
```

The proposed exact values are:

```text
feature_id = QUANTITATIVE_CONSTRAINT

population_qualifier_evidence_ref =
    <PROPOSED_R3_POPULATION_EVIDENCE_ID>

percent_member_evidence_ref =
    QUANT-001:E001

primary_duration_member_evidence_ref =
    QUANT-UK-001:E001

load_context_evidence_ref =
    <PROPOSED_R3_LOAD_CONTEXT_EVIDENCE_ID>

load_bound_member_evidence_ref =
    QUANT-UK-001:E002
```

Both angle-bracketed identifiers are `PROPOSED / NOT ALLOCATED`. The record
contains no duplicate numeric value, comparator, inclusivity, unit, metric,
source text, or calculated compliance result.

### 6.4 Member identity and cardinality

Member identity is resolved through existing scalar Evidence IDs because the
current domain has no observation ID. For this exact slice, an Evidence member
reference is valid only when it resolves to exactly one existing
`QuantitativeConstraintObservation` in the same requirement and that
observation satisfies the required role contract in §3.2.

The exact cardinalities are:

- zero or one R3 relationship per requirement;
- exactly one population-qualifier Evidence item in an accepted relationship;
- exactly one percent member;
- exactly one primary duration member;
- exactly one load-context Evidence item; and
- exactly one load-bound member.

Zero relationships is the deterministic non-match result. More than one
candidate for any role cannot occur in the exact source grammar and is not
resolved by proximity, source distance, parser dependencies, or selection
order.

A stable observation ID is not required for this exact proposal. Any later
generalization that makes an Evidence reference non-unique would require a
separate domain decision.

### 6.5 Stored and derived semantics

Stored on the relationship:

- the two new role Evidence references;
- the three existing scalar member Evidence references; and
- the stable, de-duplicated, source-ordered Evidence-reference union.

Derived by resolving the member references:

- percent value and `PERCENT` unit;
- duration comparator, inclusivity, value, and `SECOND` unit;
- load-bound comparator, unresolved inclusivity, and value; and
- the fact that the nested scalar remains a separate observation.

The record does not duplicate derived scalar data. Consequently a member's
unresolved semantics stay visible at their authoritative source: the load-bound
observation continues to expose `UPPER_BOUND / UNRESOLVED`. Relationship
presence means the attachment is resolved; it does not mean every member's
internal semantics are resolved.

## 7. Proposed Evidence contract

### 7.1 New relationship Evidence

The proposal adds exactly two Evidence items. Their provisional identifiers and
future owner are explicitly not allocated:

```text
evidence_id = <PROPOSED_R3_POPULATION_EVIDENCE_ID>
              PROPOSED / NOT ALLOCATED
feature_id  = QUANTITATIVE_CONSTRAINT
text        = для 95 % запитів
span        = [58,74)
rule_id     = <FUTURE_R3_RULE_ID>
              PROPOSED / NOT ALLOCATED
```

```text
evidence_id = <PROPOSED_R3_LOAD_CONTEXT_EVIDENCE_ID>
              PROPOSED / NOT ALLOCATED
feature_id  = QUANTITATIVE_CONSTRAINT
text        = при навантаженні до 300 одночасних запитів
span        = [117,159)
rule_id     = <FUTURE_R3_RULE_ID>
              PROPOSED / NOT ALLOCATED
```

The future Rule ID must be selected only after scientific approval. Existing
IDs cannot own these Evidence items because their meanings and Evidence
boundaries are already fixed.

### 7.2 Relationship Evidence-reference order

The relationship's proposed top-level Evidence union is:

```text
(
    <PROPOSED_R3_POPULATION_EVIDENCE_ID>,  # [58,74)
    QUANT-001:E001,                        # [62,66)
    QUANT-UK-001:E001,                     # [96,116)
    <PROPOSED_R3_LOAD_CONTEXT_EVIDENCE_ID>,# [117,159)
    QUANT-UK-001:E002,                     # [134,140)
)
```

The angle-bracketed IDs are `PROPOSED / NOT ALLOCATED`. The tuple is stable,
de-duplicated, and ordered by Evidence `start_offset`, then `end_offset` under
the existing global ordering rule. The containing role spans precede their
contained scalar spans because their start offsets are earlier.

### 7.3 Overlap and family ownership

The following overlaps are required and allowed:

- population Evidence `[58,74)` contains percent scalar Evidence `[62,66)`;
- population and duration Evidence overlap existing result and acceptance
  source spans without reusing their identities;
- load Evidence `[117,159)` contains load scalar Evidence `[134,140)`; and
- load Evidence may share its source span with independently produced
  condition-family Evidence, but must use a distinct identity and owner.

The relationship does not reference `COND-UK-*`, `RESULT-UK-*`, or
`ACCEPT-QUANT-001` Evidence. Structural and acceptance observations do not
reference R3 Evidence. The existing scalar Evidence items are referenced but
never replaced, enlarged, suppressed, or re-owned.

### 7.4 Validation invariants

An accepted relationship must satisfy all of the following:

1. `Requirement.text` equals the exact 160-code-point source in §3.1.
2. The two new Evidence items round-trip exactly to `[58,74)` and `[117,159)`.
3. All five Evidence references exist, belong to the same requirement, and
   have `feature_id = QUANTITATIVE_CONSTRAINT`.
4. Each scalar member reference resolves to exactly one existing observation.
5. Each resolved observation has the exact Evidence, components, and semantics
   stated in §3.2.
6. The three scalar observations retain their existing tuple positions and
   complete component/reference state.
7. The two role Evidence items have distinct IDs owned by the same future R3
   rule and source-ordered rule-local ordinals.
8. The relationship's top-level references equal the exact stable,
   de-duplicated component/member union in §7.2.
9. Exactly one member fills each role, and exactly one relationship exists.
10. No relationship field is treated as a scalar attachment anchor,
    acceptance anchor, score contribution, Finding source, or structural
    observation.

## 8. Mandatory condition-boundary decision gate

The exact source has no comma after the leading `Після ...` phrase. Current
`COND-UK-001` accepts its leading template only when a comma delimits the
condition. The current exact-line condition outcome is therefore
`INCOMPLETE / UNRESOLVED` with the diagnostic candidate `[0,159)`.

R3 must not repair that outcome or treat its own success as proof that the
condition detector recognized `[0,43)`.

### 8.1 Structural dependency alternatives

| Alternative | Scientific meaning and dependency graph | Exact positive behavior | Compatibility and RQD effect | Acceptance and C/V/U effect |
| --- | --- | --- | --- | --- |
| **A — require accepted structural observations** | `COND/RESULT → R3`: R3 exists only after accepted structural condition/result observations delimit the proposition. | Exact R2′ cannot currently produce R3 while the required structural dependency is unresolved. | Does not itself change `COND-UK-001`, but makes R3 implementation blocked. A separate RQD-006 decision and implementation would be required before an R3 positive. | No R3-driven effect. A later structural decision could affect result/acceptance and must be assessed separately. |
| **B — exact R3 independent of structural success** | `three accepted scalars + exact literal source → R3`; structural detectors execute independently in parallel. | R3 relationship and its two Evidence items may exist while current `COND-UK-001` remains `INCOMPLETE / UNRESOLVED`. | Preserves the current condition outcome exactly. Requires no RQD-006 decision because it adds no structural observation, boundary, fallback, or Evidence. | R3 creates no result or criterion and changes no C/V/U input or contribution. Existing structural and acceptance outcomes remain whatever their own rules produce. |
| **C — block R3 pending a separate structural contract** | `new RQD-006 approval and implementation → structural observations → later R3 decision/implementation`. | No R3 relationship until the separate structural lifecycle completes. | Preserves current behavior but defers a source-supported quantitative relationship for a dependency not required to preserve its numeric roles. Requires a separate RQD-006 decision. | None now. Any later result/acceptance effect belongs solely to the separate structural contract. |

### 8.2 Preferred disposition

Alternative B is proposed.

The exact literal source and the three already accepted scalar observations are
sufficient to recognize the bounded quantitative relationship without deciding
where the leading condition ends for the `condition_context` feature family.
R3 neither creates nor consumes structural Evidence. Its recognition therefore
does not assert that `[0,43)` was successfully detected as a condition or that
`[44,116)` was successfully detected as a result.

This separation is scientifically conservative:

- the quantitative relationship is explicit in the exact source;
- the structural boundary remains unresolved under its current rule;
- no parser or boundary fallback is introduced;
- no RQD-006 semantics are invented; and
- a future structural approval may proceed independently without migrating the
  R3 member contract.

Alternative A is scientifically coherent but currently blocks the exact
positive. Alternative C is required only if the researcher decides that every
quantitative relationship must depend on accepted structural observations; the
current model specification does not establish that universal dependency.

## 9. Proposed diagnostics and status behavior

### 9.1 Exact R3 match

An exact match requires the exact source text and all validation invariants in
§7.4.

Proposed result:

- create the two new relationship Evidence items;
- create one R3 relationship record;
- preserve all three scalar observations field-for-field and in place;
- create no new diagnostic;
- preserve existing quantitative `COMPLETE / DETECTED` processing;
- preserve the independent structural outcomes, including the current
  condition diagnostic; and
- retain `UPPER_BOUND / UNRESOLVED` on the load member without propagating it
  into relationship attachment status.

Member-local unresolved inclusivity means only that endpoint inclusion is not
known. It does not make the exact source attachment ambiguous.

### 9.2 Deterministic R3 non-match

Any text that differs from the exact source grammar is a deterministic
non-match, including a paraphrase, punctuation or spacing change, reordered
member, missing token, extra candidate, or different value.

Proposed result:

- no R3 Evidence;
- no R3 relationship record;
- no new relationship diagnostic;
- every existing scalar observation, Evidence item, diagnostic, and processing
  state remains unchanged; and
- no `CONTEXT` entry is added to any observation's `unresolved_components`.

A non-match says only that the exact R3 rule did not apply. It does not say the
changed text lacks quantitative meaning.

### 9.3 Competing or unresolved relationship members

Competing percent, duration, load, or load-bound members cannot occur inside
the exact literal grammar. A changed string containing such competition is a
deterministic R3 non-match under §9.2.

The only member-local unresolved semantic state in the exact positive is the
already accepted inclusivity of `до 300`. It remains local and does not require
a relationship diagnostic.

A future broadened recognizer might identify a relationship candidate while
failing to choose among members. That future case is `BLOCKED`: this proposal
does not allocate a diagnostic code, candidate-span rule, processing-status
change, or ambiguity-resolution policy. No implementation may generalize R3 to
create that state without a separate scientific decision. Existing scalar
outputs would remain unchanged even in that future research case.

## 10. Acceptance and downstream invariants

R3 remains transparent to the approved `ACCEPT-QUANT-001` contract:

- only existing `QUANT-001` and `QUANT-UK-001` scalar Evidence continues to
  drive acceptance containment;
- relationship Evidence and the relationship record are not scalar anchors;
- existing expected-result and acceptance Evidence is preserved wherever the
  current structural rules produce it;
- R3 neither creates missing expected-result/acceptance Evidence nor treats
  itself as a substitute for it;
- one accepted result clause produces at most one acceptance criterion;
- the existing percent and duration anchors inside `[44,116)` remain
  deduplicated to one criterion;
- load Evidence `[117,159)` and load scalar `[134,140)` remain outside scalar
  acceptance containment;
- judgeability and diagnostic behavior remain unchanged; and
- no acceptance criterion is created for each numeric expression.

The separate relationship tuple is not consumed by current characteristic
calculators. R3 therefore changes no:

- Completeness, Verifiability, or Unambiguity formula, contribution,
  applicability, state, or value;
- Finding;
- `QUALITY_PROBLEM` conversion;
- confidence, severity, probability, risk, priority, or corrective action;
- reporter output; or
- requirement- or specification-level aggregation.

Any future downstream use of R3 requires a separate scientific decision.

## 11. Protected C0 and extraction invariants

Any future implementation of an approved R3 contract must preserve:

- exact C0 `QUANT-CONTEXT-001` grammar and literal `500`;
- the one C0 quantitative observation and its metric/scalar/context Evidence;
- the existing `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` diagnostic over C0 `500`;
- independent C0 `COND-UK-001` Evidence;
- all scalar precedence, fallback, Evidence, and diagnostic rules;
- exact-source round trips and zero-based Unicode code-point offsets;
- unique Evidence IDs and non-dangling references;
- feature-family ownership and prohibition of cross-family Evidence identity;
- stable global Evidence order;
- immutable existing observation identities and tuple positions; and
- every acceptance and downstream invariant in §10.

R3 is not a generalization of C0. The two rules have different source forms,
semantics, observation counts, and representation needs.

## 12. Proposed binding cases

The only positive source case is exact R2′. Boundary cases below are synthetic
and serve only to define non-match behavior; they are not scientific evidence
for broader grammar.

| Case | Representative input or condition | Classification | Proposed R3 disposition |
| --- | --- | --- | --- |
| Exact R2′ | Exact 160-code-point sentence in §3.1 | `SOURCE_ATTESTED` | Create one relationship and the two proposed Evidence items; preserve all three scalars and structural outcomes. |
| Missing final period | Exact text without U+002E | `SYNTHETIC_TEST_CASE` | Deterministic non-match. |
| Changed spacing or casing | Any deviation from exact source | `SYNTHETIC_TEST_CASE` | Deterministic non-match; no normalization or tolerance. |
| Percentage rendered as percentile | Replace `95 % запитів` with percentile wording | Source contrast exists, composite string synthetic | Deterministic non-match; no conversion. |
| Missing population phrase | Remove `для` or `запитів` | `SYNTHETIC_TEST_CASE` | Deterministic non-match; do not infer a population. |
| Changed duration | Replace `4 с` or its comparator | `SYNTHETIC_TEST_CASE` | Deterministic non-match; no inheritance from scalar grammar. |
| Changed load value or noun | Replace `300` or `одночасних запитів` | `SYNTHETIC_TEST_CASE` | Deterministic non-match; no variable slot or noun vocabulary. |
| Changed `до` interpretation | Treat `до 300` as `≤ 300` | Unsupported inference | Forbidden; preserve `UPPER_BOUND / UNRESOLVED`. |
| Hard-boundary split | Insert `.`, `;`, `?`, or `!` inside the compound proposition | `SYNTHETIC_TEST_CASE` | Deterministic non-match; no cross-boundary relationship. |
| Additional percent, duration, or load member | Add a competing candidate | `SYNTHETIC_TEST_CASE` | Deterministic non-match; do not select by proximity. |
| Exact C0 | `Час відгуку ≤ 2 с при 500 одночасних користувачах` | `SOURCE_ATTESTED / EXISTING_APPROVED` | Outside R3; preserve complete C0 contract. |
| Synthetic `600` C0-like form | `Час відгуку ≤ 2 с при 600 одночасних користувачах` | `SYNTHETIC_TEST_CASE` | Outside R3 and negative under exact C0. |

## 13. Explicit exclusions

R3 would not approve:

- any source text other than the exact R2′ sentence;
- general percent-of-population, duration, load, or compound grammar;
- a generic relationship framework or expression tree;
- parser-based or proximity-based attachment;
- an implicit route-duration metric or new metric Evidence;
- a count ontology or count unit;
- percentage-to-percentile conversion;
- a denominator, measurement window, sample size, statistical algorithm,
  failure policy, or rounding rule;
- inclusive or exclusive interpretation of `до 300`;
- independent judgeability of the percent or load-bound member;
- scalar observation merge, replacement, enlargement, suppression, or copy;
- new condition, result, or acceptance grammar;
- suppression or reinterpretation of the current condition diagnostic;
- new relationship ambiguity diagnostics for generalized candidates;
- a new acceptance criterion, criterion per numeric expression, or changed
  acceptance containment;
- any C/V/U, Finding, `QUALITY_PROBLEM`, reporter, or aggregation change;
- a final Rule ID; or
- implementation, release, baseline, tag, issue closure, branch, commit, push,
  or pull-request action.

## 14. Researcher approval checklist

Every item is pending explicit researcher decision:

- [ ] Approve or revise the exact 160-code-point R3 source grammar.
- [ ] Approve `[58,74)` as the complete population qualifier and its
  relationship to percent member `[62,66)` and duration member `[96,116)`.
- [ ] Confirm that percentage-to-percentile conversion and all unexpressed
  measurement/statistical semantics remain forbidden.
- [ ] Approve `[117,159)` as one load context over the joint
  proportion-duration relationship.
- [ ] Approve Alternative C for `[134,140)`: preserve the separate observation
  and reference it as the load-bound member.
- [ ] Confirm `UPPER_BOUND / UNRESOLVED`, no count unit, and no independent load
  judgeability.
- [ ] Approve the dedicated bounded relationship record rather than enriching
  the duration observation.
- [ ] Approve a separate quantitative relationship tuple so current scalar
  consumers and calculators remain unchanged.
- [ ] Approve member identity through unique existing scalar Evidence
  references for this exact slice.
- [ ] Approve exactly-one cardinality for all five relationship roles and one
  relationship per requirement.
- [ ] Approve the two new `QUANTITATIVE_CONSTRAINT` Evidence spans and separate
  future ownership without allocating the final Rule ID here.
- [ ] Approve the stable source-ordered relationship Evidence union.
- [ ] Approve structural disposition B: exact R3 recognition independent of
  structural-detector success, with the existing condition outcome unchanged.
- [ ] Confirm that R3 success is not evidence of successful `COND-UK-*` or
  `RESULT-UK-*` detection and requires no RQD-006 change.
- [ ] Approve exact match, deterministic non-match, and member-local
  unresolved-inclusivity behavior in §9.
- [ ] Confirm generalized competing-member diagnostics remain blocked and
  outside this proposal.
- [ ] Approve unchanged `ACCEPT-QUANT-001`, expected-result/acceptance Evidence,
  criterion count, judgeability, and deduplication.
- [ ] Confirm unchanged C/V/U, Findings, `QUALITY_PROBLEM`, reporter, and
  aggregation behavior.
- [ ] Approve a future distinct Rule ID in a separate decision, or direct a
  different lifecycle; no Rule ID is allocated here.

## 15. Final proposal status

The exact bounded R3 contract above is ready for an explicit researcher
decision. It resolves the population role, relation-level load scope, nested
scalar disposition, minimum representation, Evidence ownership, structural
dependency, status behavior, and downstream invariants for only the exact R2′
source.

Nothing in this document records scientific approval or authorizes
implementation. Until explicit researcher approval, no R3 relationship exists
in the authoritative model, `RQD-008` remains `PARTIALLY_APPROVED / OPEN`, and
SRM-05 issue #73 remains `OPEN`.

**Final proposal status: `PROPOSED_FOR_RESEARCHER_APPROVAL`.**
