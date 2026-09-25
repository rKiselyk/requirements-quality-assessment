# Cross-Requirement Consistency QB-v0.1 Architecture Contract

- **Branch:** `research/cross-requirement-analysis`
- **Round:** architecture only
- **Architecture status:** researcher-approved; implementation planning is next
- **Researcher approval date:** 2026-09-25
- **Scientific baseline:** frozen on 2026-09-25
- **Implementation effect:** none; this document creates no production contract,
  Rule ID, Evidence ID, code, test, migration, or reporter wording

## 1. Purpose, authority, and frozen invariants

This document proposes the complete software architecture needed to implement
the first bounded Cross-Requirement Consistency slice, `QB-v0.1`. It consumes
the approved science without reopening it. Authority is applied in this order:

1. `docs/model-spec.md`;
2. `docs/cross-requirement-consistency-decision-package.md`;
3. `docs/cross-requirement-consistency-reference-cases.md`;
4. `docs/cross-requirement-qb-extraction-readiness.md`;
5. `docs/cross-requirement-analysis-research.md`;
6. accepted production domain contracts and pipeline; and
7. existing tests.

The following invariants are frozen:

- `RequirementAssessmentRecord` remains the authoritative joined output of
  Single Requirement Analysis.
- `RequirementExtractionResult` and all existing feature-family processing,
  observation, diagnostic, and Evidence semantics remain unchanged.
- `RequirementQualityProfile(C_i,V_i,U_i)` remains unchanged.
- `SpecificationQualityProfile(C_file,V_file,U_file)` remains unchanged and is
  not reinterpreted as a complete assessment of all specification properties.
- `AGG-MVP-001` remains unchanged and does not govern Consistency.
- Existing Evidence ownership, local Evidence ID uniqueness, exact-source span,
  accepted-reference, and source-order invariants remain unchanged.
- Existing diagnostics and quantitative `COMPLETE`/`INCOMPLETE` meaning remain
  unchanged.
- Cross-analysis is downstream and must not mutate extraction results, local
  traces, local findings, or local C/V/U values.
- Full unqualified `M_cons` remains non-executable.
- Only coverage-qualified `M_cons[QB-v0.1]` is in scope.
- No severity, probability, risk, priority, corrective action, product-quality
  inference, generic semantic equivalence, unit conversion, or overall scalar
  specification score enters this architecture.

## 2. Target processing architecture

The target flow is:

```text
Specification input
-> RequirementReader                                      (existing)
-> feature extraction + Single Requirement Analysis      (existing)
-> immutable RequirementAssessmentRecord[]                (existing boundary)
-> SpecificationQualityAggregator                         (existing, independent)
-> CrossRequirementProjector                              (new)
-> QbMaterialityClassifier                                (new)
-> ExhaustiveCrossPairSelector                            (new)
-> QbObservationPairAssessor                              (new)
-> ordered CrossRequirementResult[]                       (new)
-> QbConsistencyAggregator                               (new)
-> QbConsistencyAssessment                               (new)
-> SpecificationAssessment                               (new composition boundary)
-> composed technical/user reporting                     (new additive section)
```

The local aggregate may be calculated before or after cross-analysis because
neither consumes the other. The recommended orchestration calculates it first,
then cross-analysis, and composes both only after both results exist. A failure
or scientific `UNKNOWN` in cross-analysis cannot change construction of any
`RequirementAssessmentRecord` or the local aggregate.

Responsibilities stay separate:

| Stage | Sole responsibility | Must not do |
| --- | --- | --- |
| Projector | Validate records against one snapshot and expose the minimum immutable QB view | Compare observations, classify diagnostics, aggregate, or format |
| Materiality classifier | Classify quantitative diagnostics under the exact two-entry C0 allowlist and emit audit records | Change detector state or suppress diagnostics |
| Pair selector | Enumerate the declared cross-requirement observation-pair universe in deterministic order | Decide scientific state or prune without equivalence proof |
| Pair assessor | Apply identity, applicability, comparator, and conflict rules to one pair | Read global specification state or aggregate results |
| Consistency aggregator | Build observed `R_conf[QB-v0.1]`, observability metadata, state, and exact value | Reassess pairs or use `AGG-MVP-001` |
| Specification composer | Place the unchanged local profile beside the separate Consistency assessment | Combine them into one scalar or reinterpret either |
| Reporters | Render supplied immutable results and provenance | Calculate, classify, repair, or aggregate |

## 3. `CrossRequirementProjection` contract

### 3.1 Purpose and ownership strategy

The projection is an anti-corruption boundary. Cross-analysis receives a
validated immutable view instead of navigating arbitrary fields of
`RequirementAssessmentRecord`. The projector is the only cross-analysis
component allowed to read the record structure directly.

The projector constructs stable frozen domain views:

- copy immutable scalar/enum/`Decimal` values and tuples required by QB;
- represent observations and Evidence by stable qualified references;
- retain read-only references to the already-frozen `Requirement`, `Evidence`,
  and diagnostic values only inside a snapshot-scoped resolver;
- never copy or embed the local C/V/U profile in the scientific QB projection;
  and
- never retain mutable collection or object-memory identity as a domain key.

This balances snapshot validation with non-duplication. The projected values
are sufficient for deterministic calculation; the resolver supplies exact
source material for validation and reporting.

### 3.2 Minimum projected field classification

| Information | Classification | Projection placement and reason |
| --- | --- | --- |
| `requirement_id` | `REQUIRED_FOR_SCIENCE` | Participant identity and both bounded formula operands |
| input/source order | `REQUIRED_FOR_SCIENCE` | Canonical pair, result, `R_conf`, and report ordering |
| `source_line` | `REQUIRED_FOR_VALIDATION` | Confirms reader order and gives stable source traceability |
| exact requirement text access | `REQUIRED_FOR_VALIDATION` | Snapshot digest and Evidence/diagnostic span round-trip; exposed through resolver, not duplicated in every result |
| quantitative observation source-order index | `REQUIRED_FOR_SCIENCE` | Stable observation identity within the owning record |
| metric/context component refs and exact source surfaces | `REQUIRED_FOR_SCIENCE` | Bounded normalization and key construction |
| comparator label and inclusivity | `REQUIRED_FOR_SCIENCE` | Applicability and admissible-bound semantics |
| exact `Decimal` value and unit label | `REQUIRED_FOR_SCIENCE` | Exact predicate and key identity |
| quantitative `unresolved_components` | `REQUIRED_FOR_SCIENCE` | Typed unresolved disposition |
| observation Evidence refs | `REQUIRED_FOR_VALIDATION` | Ownership and complete explanation provenance |
| quantitative processing status | `REQUIRED_FOR_SCIENCE` | Global unresolved observability is preserved |
| quantitative diagnostics, source index, code, source Rule ID, and candidate span | `REQUIRED_FOR_SCIENCE` | CRA-D067 materiality classification and audit |
| snapshot-scoped Evidence lookup | `REQUIRED_FOR_VALIDATION` | Qualified lookup, exact-source, family, and observation-use checks |
| materiality contract/version descriptors | `REQUIRED_FOR_VALIDATION` | Fail-closed two-entry C0 allowlist validation |
| local `RequirementQualityProfile` | `REQUIRED_FOR_REPORTING` | Optional report context only; carried beside the projection in the report bundle, never read by QB calculation |
| local `RequirementAssessmentTrace` | `NOT_REQUIRED` | It explains C/V/U, not QB identity or conflict mathematics |
| actor/action/object or generic semantic roles | `NOT_REQUIRED` | No approved QB science uses them |
| severity, risk, confidence score, priority, corrective action | `NOT_REQUIRED` | Explicitly outside the scientific contract |

### 3.3 Projection validation

Construction fails if record IDs are duplicated, source order is not strict,
an observation reference is out of range, a component reference is dangling,
Evidence ownership is foreign, an Evidence span does not round-trip, a
diagnostic span does not round-trip, or the records do not share the declared
snapshot. These are invalid internal/domain invariants, not scientific
`ASSESSMENT_UNRESOLVED` results.

## 4. Stable quantitative-observation identity

The approved architecture view is conceptually:

```text
CrossObservationRef(
    requirement_id,
    feature_id = QUANTITATIVE_CONSTRAINT,
    observation_index
)
```

`observation_index` is the zero-based position in the immutable quantitative
observation tuple for that requirement and therefore represents approved
source order. The enclosing result and resolver carry `snapshot_id`; it is not
necessary to duplicate it inside every reference value.

Validation requires that the requirement exists in the snapshot, the feature
family is quantitative, the index is in range, and resolution returns exactly
one observation owned by that requirement. An object address, Python `id()`,
unqualified tuple index, or Evidence ID alone is never an observation identity.

## 5. `CrossEvidenceRef` and provenance resolution

The architecture preserves the approved compound reference exactly:

```text
CrossEvidenceRef(requirement_id, evidence_id)
```

Evidence IDs remain local to one `RequirementExtractionResult`. A
snapshot-scoped `CrossEvidenceResolver` owns lookup and validation. For each
reference it must establish:

1. the owner is a result participant;
2. the Evidence exists exactly once in that owner's extraction result;
3. `Evidence.requirement_id` equals the qualified owner;
4. its span and text round-trip against the owner's exact requirement text;
5. its feature family is appropriate;
6. the referenced observation/component legitimately uses it; and
7. result-level Evidence contains the required support from both participants.

Cross-results store qualified refs only. They do not duplicate `Evidence` and
do not rewrite existing IDs. The resolver may return the original frozen
`Evidence` value to a reporter. Invalid, foreign, dangling, or detached refs
raise domain validation errors during construction; they never degrade to a
human-only explanation or scientific `UNKNOWN`.

## 6. Assessment snapshot identity

### 6.1 Contract

`AssessmentSnapshot` is one immutable QB execution boundary, not a history or
lifecycle system. It contains:

- an opaque `snapshot_id`;
- the ordered projected requirements;
- a frozen provenance resolver/catalog;
- a contract manifest for projection, normalization, comparison, materiality,
  aggregation, and coverage-profile versions; and
- the exact QB-relevant count/order manifest used to validate all derived
  objects.

The snapshot identity is a deterministic, canonical, content-derived identity
over only the QB-relevant source state and QB contract manifest. Conceptually:

```text
QB snapshot identity =
    canonical(QB-relevant source state + QB contract manifest)
```

The semantic input is limited to:

1. ordered requirement identity;
2. exact requirement source text needed for provenance;
3. requirement/source order;
4. QB-relevant quantitative observations;
5. QB-relevant Evidence and exact spans;
6. quantitative diagnostics relevant to materiality;
7. QB-relevant processing and provenance facts; and
8. approved projection, materiality, comparison, aggregation, and coverage
   contract versions.

`RequirementQualityProfile`, local C/V/U states and values,
`RequirementAssessmentTrace`, local explanation text, reporter representation,
and unrelated local assessment metadata are explicitly excluded. A change to
one of those excluded values cannot change QB snapshot or cross-result
identity.

It excludes file path, wall-clock time, process identity, Python object
identity, runtime UUID, and report formatting. SHA-256 remains an acceptable
recommended implementation mechanism, but this architecture does not freeze a
JSON shape, whitespace policy, enum encoding, byte format, or other canonical
serialization mechanics. Implementation must document, version, and
regression-test one deterministic canonical encoding. The lower bridge's
future production Rule/Evidence identifiers enter the manifest only after
separately allocated during implementation.

### 6.2 Snapshot invariants

Every projection, materiality audit record, cross-result, `R_conf` view,
Consistency assessment, and broader `SpecificationAssessment` must carry or be
validated against the same snapshot ID. Cross-snapshot composition is an
internal error. A stable result identity derives from the QB snapshot identity,
canonical observation refs, governing QB rule/contract version, and result
state/identity data. It contains no randomness, timestamps, local C/V/U,
local trace, or reporting data. The exact canonical encoding remains the same
versioned implementation concern described above.

The implementation phase must separately allocate production identifiers and
versions for the QB pair comparison/confirmation rule, QB Consistency
aggregation rule, and QB materiality rule, in addition to the two future
lower-bridge Rule/Evidence families. Their fields are required below, but this
architecture document allocates none of those identifiers.

`SpecificationAssessment` may compose the unchanged local profile with the QB
assessment without importing the profile into QB identity. The orchestration
layer must build both from the same ordered requirement source set and retain
that source-set association through composition. A future identity for the
complete composed assessment would be a separate architecture/implementation
concern and cannot redefine QB snapshot identity.

## 7. Cross-result domain contract

The approved frozen result value, named conceptually
`CrossRequirementResult`, contains:

| Field group | Required content |
| --- | --- |
| Identity | stable `result_id`, `snapshot_id`, deterministic ordering key |
| Participants | canonical earlier/later requirement IDs; two distinct owners |
| Inputs | ordered left/right `CrossObservationRef`; projected comparator, inclusivity, exact `Decimal` value, unit, and available normalized identity components |
| Scientific scope | coverage profile ID/version; future-allocated comparison/confirmation Rule ID and version; quantitative-bound relation under test |
| Disposition | exactly one of `CONFIRMED_CONFLICT`, `COMPATIBLE_WITHIN_RULE`, `ASSESSMENT_UNRESOLVED`, `OUTSIDE_V0_1_APPLICABILITY` |
| Identity result | resolved comparison key only when complete; otherwise the resolved/missing component facts used by the decision |
| Provenance | ordered `CrossEvidenceRef` tuple; diagnostic refs where reasons depend on diagnostics |
| Conflict classification | logical-conflict class and direct quantitative-bound incompatibility subtype only for `CONFIRMED_CONFLICT` |
| Reasons | typed unresolved reasons or typed outside-applicability reasons according to state |
| Explanation data | structured operands, normalization outputs, predicate outcome, and bounded non-claim keys; rendered prose is not stored as authority |

The result never contains severity, probability, risk, priority, confidence
score, corrective action, defect prediction, product-quality inference, or an
overall quality score.

## 8. State-specific construction invariants

All results require two distinct canonically ordered requirement participants,
two valid observation refs from those owners, one snapshot, deterministic
Evidence ordering, and one coverage/comparison contract.

### 8.1 `CONFIRMED_CONFLICT`

It requires:

- complete metric, context, unit, comparator, inclusivity, and value inputs;
- equal normalized metric and context plus exact equal unit labels;
- supported inclusive `LESS_THAN_OR_EQUAL`/`GREATER_THAN_OR_EQUAL` inputs;
- an empty intersection under the approved half-line predicate;
- Evidence from both observations and both requirements;
- logical-conflict class plus approved direct quantitative-bound subtype; and
- no unresolved or outside-applicability reasons.

### 8.2 `COMPATIBLE_WITHIN_RULE`

It requires the same complete supported comparison gates, but the admissible
sets have a non-empty intersection. It has no conflict class/subtype and no
unresolved/outside reasons. Its explanation must say bounded joint
satisfiability only; it must not claim universal absence of conflict.

### 8.3 `ASSESSMENT_UNRESOLVED`

It requires at least one typed unresolved reason and provenance pointing to
the missing/unresolved component or diagnostic facts. It has no complete
comparison key, no conflict classification, and cannot enter
`R_conf[QB-v0.1]`. It withholds the aggregate even when other results are
confirmed.

### 8.4 `OUTSIDE_V0_1_APPLICABILITY`

It requires at least one resolved typed applicability boundary: unsupported
`NOT_LESS_FREQUENT`, resolved metric mismatch, resolved context mismatch, or
resolved unit mismatch. It is not compatible, does not enter `R_conf`, and
does not itself make the bounded set incomplete. The approved decision order
allows a resolved mismatch to establish this state even when another identity
component is missing.

## 9. Typed reason-code architecture

Human prose is derived from typed reasons and structured operands. The minimum
QB-v0.1 reason vocabulary is:

| Reason family | Conceptual reason code | Use |
| --- | --- | --- |
| unresolved | `MISSING_METRIC` | metric component absent and no resolved mismatch already excludes the pair |
| unresolved | `UNRESOLVED_METRIC` | metric explicitly unresolved |
| unresolved | `MISSING_CONTEXT` | context absent |
| unresolved | `UNRESOLVED_CONTEXT` | context explicitly unresolved |
| unresolved | `MISSING_UNIT` | unit absent |
| unresolved | `MISSING_VALUE` | exact value absent |
| unresolved | `MISSING_COMPARATOR` | comparator absent |
| unresolved | `UNRESOLVED_INCLUSIVITY` | comparator cannot supply approved inclusive semantics, including `UPPER_BOUND` |
| unresolved | `MATERIAL_UNRESOLVED_EXTRACTION` | snapshot has a material quantitative diagnostic capable of changing the QB operand; aggregate-level reason, not fabricated pair evidence |
| outside | `METRIC_MISMATCH` | both resolved normalized metrics differ |
| outside | `CONTEXT_MISMATCH` | both resolved normalized contexts differ |
| outside | `UNIT_MISMATCH` | both resolved unit labels differ; no conversion |
| outside | `COMPARATOR_OUTSIDE_PROFILE` | `NOT_LESS_FREQUENT` or another explicitly resolved comparator outside QB-v0.1 |

No generic NLP-error hierarchy is introduced. Multiple reasons are retained in
the approved deterministic component order, but the state follows the
scientific precedence in the decision package.

## 10. QB materiality classifier and audit

### 10.1 Dedicated downstream component

`QbMaterialityClassifier` consumes the immutable projection, provenance
resolver, and an explicit closed allowlist of exactly two versioned contract
descriptors:

1. existing exact upper C0 represented by `QUANT-CONTEXT-001`; and
2. future exact lower C0 represented by the separately allocated rule from the
   approved `LB-M-C0` implementation.

The allowlist is code-owned and versioned with the QB contract. It is not a
user configuration, generic ignored-diagnostic list, wildcard registry, or
text-only exception.

### 10.2 Input and fail-closed validation

For every quantitative diagnostic, the classifier receives a stable
`CrossDiagnosticRef(requirement_id, quantitative_feature_id,
diagnostic_index)`, the diagnostic, owning observation candidates, exact
Evidence, requirement text, and contract manifest. `QB_NON_MATERIAL` is
possible only if all eight approved gates pass:

1. exact diagnostic code;
2. exact source Rule ID;
3. exact ASCII text `500`;
4. exact span containment in accepted context Evidence;
5. same QB-eligible observation ownership;
6. exact allowlisted contract/version guarantee;
7. no other material unresolved candidate/component or competing observation;
8. complete Evidence, diagnostic, span, and ownership integrity.

Any missing descriptor, unallocated lower rule, failed lookup, version
mismatch, malformed span, extra candidate, or failed gate yields
`QB_MATERIAL_UNRESOLVED`. The classifier never edits diagnostics or changes
the quantitative processing state.

Classification is two-pass: first validate each diagnostic and its potential
owner/contract; then evaluate requirement/snapshot-wide competition and other
unresolved candidates before finalizing gate 7. This prevents an early
non-material disposition from hiding a later material candidate.

### 10.3 Output and counts

One immutable `QbMaterialityAuditRecord` is emitted per quantitative
diagnostic. It carries snapshot and diagnostic refs, disposition
`QB_NON_MATERIAL` or `QB_MATERIAL_UNRESOLVED`, matched allowlist entry when
applicable, the future-allocated materiality Rule ID/version, all gate
outcomes, and supporting qualified Evidence refs.

The Consistency observability contract separately reports:

- global unresolved quantitative extraction count from the unchanged
  quantitative outcomes/diagnostics;
- QB-material unresolved diagnostic count from material audit dispositions;
- QB-non-material preserved diagnostic count from non-material dispositions.

Unresolved observation components are additionally represented by pair-result
reasons; materiality classification does not erase or replace them.

## 11. Exact `LB-M-C0` extraction-bridge architecture

Three options were considered:

| Option | Design | Assessment |
| --- | --- | --- |
| A | One rule enriches metric and context together | Simple atomicity, but collapses the separately approved QB-ER-D002 and QB-ER-D005 provenance and prevents independent Rule/Evidence ownership |
| B | Two bounded enrichment rules, coordinated atomically for the same existing scalar | Preserves separate scientific ownership and future IDs while preventing partial enrichment |
| C | Generic grammar/plugin producing arbitrary metric/context links | Rejected; exceeds the exact approved envelope and frozen extraction boundary |

The recommendation is **Option B with an atomic envelope coordinator**:

- an exact lower-metric enrichment rule and a distinct exact lower-C0 context
  enrichment rule each have future separately allocated Rule/Evidence IDs;
- a narrow coordinator first validates the entire `LB-M-C0` whole-input
  envelope and identifies exactly one existing `QUANT-UK-001` scalar;
- both component contributions are constructed against that same observation;
- the assembler applies both or neither, so no standalone `LB-M0` metric
  enrichment and no partial lower context enrichment can escape;
- the scalar observation object is enriched in place conceptually during
  extraction assembly; no duplicate observation is created;
- the existing scalar Evidence, comparator, inclusivity, `Decimal`, unit,
  diagnostic, processing state, and source ordering are preserved;
- `QUANT-CONTEXT-001`, R3, and F1-A are untouched; and
- local C/V/U states, numeric values, findings, and calculation semantics
  remain unchanged; only the approved metric/context Evidence graph is added.

The coordinator is an implementation mechanism, not a third scientific rule.
No production Rule ID or Evidence ID is allocated by this document.

## 12. Candidate-pair selection

### 12.1 Baseline exhaustive evaluator

Materialize requirements in reader order. Enumerate every unordered distinct
requirement pair once, earlier first. Within it, enumerate the Cartesian
product of left and right quantitative observation tuples in observation
source order. Emit one candidate for every product member. Preserve separate
material unresolved diagnostics even when no observation exists.

This directly implements the conceptual universe and naturally emits resolved
unequal-key `OUTSIDE_V0_1_APPLICABILITY` results.

### 12.2 Indexed selection option

An index could group complete resolved keys and accelerate equal-key
comparisons. By itself that is not equivalent: it would omit required
outside-applicability results, unresolved comparisons, and coverage counts.
An equivalent index would need additional buckets and a deterministic merge
covering every omitted/mismatched/unresolved class, which is more complex than
the current scientific slice.

### 12.3 Recommendation

Implement exhaustive selection first. Indexed selection is deferred until
measured need exists and an equivalence suite proves identical ordered
cross-results, reasons, provenance, counts, `R_conf`, state, and value. No
numeric performance threshold is invented here.

## 13. Pure QB observation-pair assessment

`QbObservationPairAssessor` is deterministic and side-effect free. Its only
inputs are two projected observations, their validated resolver, the snapshot
and comparison contract, and their canonical refs. It cannot read aggregate
counts, other pairs, local C/V/U, or reporter state.

Its internal responsibility chain remains explicit:

1. `QbApplicabilityEvaluator` applies the approved precedence: comparator
   outside-profile; resolved metric/context/unit inequality; missing or
   unresolved inputs; unsupported/unresolved inclusivity.
2. `QbComparisonKeyBuilder` applies only NFC, case folding, Unicode-whitespace
   collapse, and trim to metric/context, plus exact unit equality.
3. `QbSupportedBoundValidator` admits only resolved inclusive upper/lower
   comparators with exact `Decimal` values.
4. `QbConflictPredicate` evaluates the two supported bounds.
5. `CrossResultFactory` validates state invariants, provenance, reason order,
   and stable identity.

Candidate generation, scientific assessment, result construction validation,
and aggregation are separate callable boundaries even if the first
implementation keeps them in one package.

## 14. Minimal admissible-set representation

A general interval algebra is unnecessary. The pair rule needs only an
immutable conceptual bound:

```text
SupportedInclusiveBound(direction = UPPER | LOWER, value = Decimal)
```

The direct predicate is:

- two upper bounds: compatible;
- two lower bounds: compatible;
- lower `l` and upper `u`: conflict exactly when `l > u`;
- `l == u`: compatible at the shared inclusive endpoint.

This is scientifically equivalent to intersecting `(-infinity,u]` and
`[l,+infinity)` while remaining smaller and easier to explain. Structured
explanation data retains direction, exact values, chosen lower/upper operands,
and predicate result. No infinity values, open intervals, ranges, conversion,
or tolerance objects are introduced.

## 15. `R_conf[QB-v0.1]` construction

`QbConflictSetBuilder` consumes only validated ordered cross-results. It adds
both participant requirement IDs from each `CONFIRMED_CONFLICT` to a set and
emits a tuple sorted by snapshot source order. Duplicate participation is
collapsed; result count never substitutes for requirement count.

Validation rejects unknown participants, snapshot mismatches, duplicate result
IDs, noncanonical participant order, or attempts to add participants from any
other state.

The observed tuple remains available when the aggregate is `UNKNOWN`, but
`rconf_complete` is false if any pair result is `ASSESSMENT_UNRESOLVED` or any
QB-material unresolved extraction could change the comparison universe. Such
a partial observed set is audit evidence only and is never used as a numeric
`M_cons[QB-v0.1]` numerator. `OUTSIDE_V0_1_APPLICABILITY` does not by itself
make the set incomplete.

## 16. QB Consistency assessment contract

### 16.1 Options

| Option | Consequence |
| --- | --- |
| A — reuse `CharacteristicAssessment` | Rejected. Its characteristic IDs, findings, local calculator rules, and state semantics are C/V/U-specific and do not carry cross-result coverage or `R_conf`. |
| B — introduce a separate `QbConsistencyAssessment` | Recommended. It preserves exact QB state, operand, coverage, provenance, and non-claims without coupling local and set-level calculations. |
| C — first factor a shared generic state/value envelope | Deferred. It would refactor frozen local contracts before behavioral acceptance and still would not remove QB-specific fields. |

### 16.2 Approved fields

The separate immutable assessment contains:

- `snapshot_id`;
- state `COMPUTED`, `UNKNOWN`, or `NOT_APPLICABLE`;
- exact `Fraction | None`;
- ordered observed `R_conf[QB-v0.1]` participant IDs;
- `rconf_complete`;
- the complete approved observability metadata set;
- coverage profile ID/version and future-allocated aggregation Rule ID/version;
- ordered refs to relevant cross-results and materiality audit records;
- typed aggregate reasons;
- structured explanation operands; and
- the complete bounded non-claim set/version.

The observability value contains at least all counts approved in the decision
package: requirements, requirements with observations, requirements in
applicable comparisons, requirement pairs, observation pairs, applicable,
conflict, compatible, unresolved, outside, global unresolved extraction,
QB-material unresolved, QB-non-material diagnostics, observed `R_conf` size,
and completeness.

Construction validates at least:

```text
total_requirement_pair_count = N_R * (N_R - 1) / 2
total_observation_pair_count = N_C + N_W + N_U + N_O
applicable_comparison_count = N_C + N_W
observed_rconf_count = len(ordered_unique_rconf_participants)
global_unresolved_count = QB_material_count + QB_non_material_count
```

The last equality applies to the classified quantitative diagnostic universe;
unresolved observation components remain pair-result reasons and are not
double-counted as diagnostics.

### 16.3 State decision order and validation

Aggregation applies this order:

1. fewer than two requirements -> `NOT_APPLICABLE`; no cross-requirement pair
   can exist, while any global diagnostics remain visible in metadata;
2. otherwise any QB-material unresolved extraction or any
   `ASSESSMENT_UNRESOLVED` pair -> `UNKNOWN`;
3. otherwise zero applicable comparisons -> `NOT_APPLICABLE`; and
4. otherwise -> `COMPUTED`.

- `COMPUTED` requires at least two requirements, at least one applicable
  comparison, zero unresolved pair results, zero QB-material unresolved
  extraction, complete `R_conf`, and
  `value = Fraction(N_R - N_Rconf, N_R)`.
- `UNKNOWN` requires `value is None`, incomplete `R_conf`, and at least one
  unresolved pair or QB-material unresolved extraction. Confirmed results and
  the partial observed set remain linked for audit.
- `NOT_APPLICABLE` requires `value is None`, complete empty `R_conf`, zero
  applicable comparisons, and either fewer than two requirements or a
  completed universe containing no material uncertainty that could make a
  comparison applicable.
- Every state validates the metadata equations and result counts. Global
  `INCOMPLETE` alone does not force `UNKNOWN` when all its diagnostics are
  validly `QB_NON_MATERIAL`.

## 17. Broader `SpecificationAssessment` boundary

The approved long-term boundary is a composition, never an inheritance or
numeric merge:

```text
SpecificationAssessment(
    snapshot_id,
    quality_profile: SpecificationQualityProfile,
    qb_consistency: QbConsistencyAssessment
)
```

Future set-level properties may be added only through separately approved
contracts. There is no overall `value` field and no generic list whose items
can silently change meaning.

Two implementation timings were considered:

| Timing | Assessment |
| --- | --- |
| Return Consistency separately through the first complete release | Minimizes one type initially but leaves reporter/orchestration without the approved composition boundary and invites ad hoc pairing. |
| Build layers separately, then add the thin container before reporter integration in the first end-to-end slice | Recommended. It preserves independent development while ensuring the delivered pipeline expresses approved Option B. |

Therefore early domain/pair/aggregate slices return their own values, but the
first integrated end-to-end QB release introduces the thin container. The
existing `SpecificationQualityProfile` class is embedded unchanged.

## 18. Safe integration point and orchestration

The only safe insertion point is after the complete ordered tuple of
`RequirementAssessmentRecord` values exists. Recommended orchestration is:

```text
requirements = reader.read(...)
records = tuple(assessor.assess_record(extractor.extract(r)) for r in requirements)
quality_profile = existing_aggregator.aggregate(record.quality_profile for record in records)

snapshot = cross_projector.project(records, approved_contract_manifest)
materiality = qb_materiality.classify(snapshot)
candidates = exhaustive_selector.select(snapshot)
cross_results = pair_service.assess(candidates, snapshot)
consistency = qb_consistency_aggregator.aggregate(snapshot, materiality, cross_results)
specification_assessment = compose(snapshot, quality_profile, consistency)

report_bundle = bundle(records, specification_assessment, cross_results, materiality)
reporter.render(report_bundle)
```

The CLI continues to contain orchestration only. The lower extraction bridge
is implemented behind the existing quantitative extraction boundary; it does
not invoke cross-analysis. Cross-analysis does not invoke local calculators or
the existing specification aggregator.

## 19. Reporter architecture

Reporting remains a consumer. The approved immutable `AssessmentReportBundle`
contains:

- ordered existing `RequirementAssessmentRecord` values;
- the broader `SpecificationAssessment`;
- ordered cross-results;
- materiality audit refs/records appropriate to the selected view; and
- resolvers needed to render exact source Evidence.

An additive composed reporter delegates the existing individual requirement
and C/V/U sections to their current rendering behavior, then appends a separate
Cross-Requirement Consistency section. Existing reporter calculations do not
change.

The future technical/audit view consumes full result, Evidence, diagnostic,
reason, count, contract-version, and materiality-audit data. The user view
consumes the same authoritative bundle but selects concise interpretation. The
architecture requires, without fixing prose templates:

- a confirmed conflict shows source Evidence from both requirements;
- `UNKNOWN` identifies each material unresolved reason and why the exact value
  was withheld;
- `NOT_APPLICABLE` is visibly different from computed `Fraction(1,1)`;
- computed `Fraction(1,1)` carries the bounded non-claim;
- compatible results are never called universally conflict-free; and
- global incomplete extraction remains visible when diagnostics are
  QB-non-material.

## 20. Performance boundary

Let `N` be requirement count and `O_i` the quantitative observation count for
requirement `i`. Exhaustive candidate count and pair-rule time are:

```text
sum over 1 <= i < j <= N of (O_i * O_j)
```

With a uniform upper observation count `O`, this is `O(N^2 * O^2)` time.
Projection, provenance indexing, and materiality classification are linear in
records plus projected observations, Evidence, and diagnostics. Stored result
space is proportional to the exhaustive candidate count because the approved
report/coverage contract retains all four dispositions.

No unsupported scale threshold is defined. Instrument candidate count and
elapsed stages first. An index becomes eligible for a later architecture
change only when measured repository use demonstrates a need and equivalence
tests compare exhaustive and indexed evaluators for exact ordered results,
reasons, Evidence refs, coverage counts, materiality, `R_conf`, aggregate
state, and exact value.

## 21. Error handling boundary

| Condition | Architectural treatment |
| --- | --- |
| Missing/unresolved scientifically required observation input | `ASSESSMENT_UNRESOLVED` with typed reason and provenance |
| Resolved valid input outside the bounded profile | `OUTSIDE_V0_1_APPLICABILITY` with typed boundary reason |
| Material unresolved quantitative diagnostic | Aggregate `UNKNOWN`; preserve audit and existing detector state |
| Invalid/foreign Evidence or observation ref | Fail construction/validation; domain invariant error |
| Cross-snapshot object composition | Fail fast; domain invariant error |
| Malformed projection, impossible state/field combination, bad metadata equation | Fail fast; domain invariant error |
| Valid but unsupported comparator | Approved outside or unresolved state according to the scientific decision order |
| Exhaustive selector omits/duplicates a conceptual pair | Programmer/invariant error, never scientific `UNKNOWN` |
| Unexpected enum/control branch or impossible predicate state | Programmer error; fail fast |

Domain corruption is never converted to scientific uncertainty. Orchestration
may catch validation/programmer failures only to return an application error;
it must not emit a fabricated Consistency assessment.

## 22. Approved future module boundaries

The responsibility separation below is approved. Exact filenames remain
implementation choices and no modules are created in this round:

```text
requirements_quality_assessment/
  cross_analysis/
    domain.py             # refs, snapshot, result, reasons, assessment values
    projection.py         # record -> immutable QB projection and resolver
    materiality.py        # exact fail-closed C0 diagnostic classification
    selection.py          # exhaustive pair enumeration
    comparison.py         # applicability, key, bound, predicate, result factory
    aggregation.py        # R_conf and QbConsistencyAssessment
    specification.py      # thin local-profile + consistency composition
    service.py            # thin sequencing of the above components
  cross_reporter.py       # additive report composition/sections
```

The exact filenames remain implementation choices. The responsibility split is
normative: no monolithic `cross_analyzer.py` may combine projection,
materiality, comparison, aggregation, and reporting.

The future `LB-M-C0` bridge belongs with quantitative extraction/detector
implementation behind `FeatureExtractor`, not inside `cross_analysis`.

## 23. Dependency direction

Allowed dependency direction is:

```text
existing core/extraction/assessment domain  <- cross projection/domain/rules
existing SpecificationQualityProfile        <- SpecificationAssessment composition

cross domain <- projection, materiality, selection, comparison, aggregation
cross results + existing local outputs <- reporting/orchestration
```

More explicitly:

- existing Single Requirement domain, detectors, calculators, assessor,
  traces, and aggregator have no dependency on cross-analysis;
- the lower bridge may change only the quantitative extraction implementation
  and accepted Evidence graph under its own contract;
- cross-analysis may import stable existing domain value types but not concrete
  detector implementations, calculators, CLI, or reporters;
- pair rules depend only on cross-domain values and exact standard-library
  arithmetic;
- aggregation depends on result/materiality contracts, not extraction
  implementations;
- reporting and orchestration may depend on both sides; and
- circular imports or callback dependencies from Single Requirement Analysis
  into cross-analysis are prohibited.

## 24. Future test architecture

No tests are created in this round. Future layers are:

| Test layer | Required coverage |
| --- | --- |
| Domain validation | snapshots, qualified refs, result state matrices, assessment state/value/count equations, stable ordering/IDs |
| Pair-rule unit | normalization, mismatch precedence, supported comparators, exact Decimal bound predicate, four result states |
| Materiality unit | all eight gates, both exact allowlist entries, every named negative, fail-closed errors, preserved global state |
| Consistency aggregation | set-union uniqueness, partial `R_conf`, `COMPUTED`/`UNKNOWN`/`NOT_APPLICABLE`, exact Fraction, observability equations |
| Projection | accepted record views, Evidence ownership, diagnostic/source round-trip, foreign/dangling/cross-snapshot failures |
| Frozen-local regression | unchanged C/V/U profiles, traces, diagnostics, `AGG-MVP-001`, and existing reports before/after the bridge |
| End-to-end | reader through composed report for implemented extractor paths |
| Reference-corpus conformance | exact fixtures, states, results, order, counts, Evidence, `R_conf`, and values |

Binding corpus mapping:

| Cases | Primary future level |
| --- | --- |
| RC-QB-001 | pair-rule conflict + domain aggregation conformance |
| RC-QB-002 | canonical participant/result ordering + pair rule |
| RC-QB-003 | exhaustive selection + repeated-participant set union |
| RC-QB-004 | mixed-bound non-empty-intersection pair rule |
| RC-QB-005 | current-extractor end-to-end + upper-C0 materiality + computed aggregate |
| RC-QB-006 | same-direction lower-bound pair rule |
| RC-QB-007 | inclusive shared-endpoint pair rule |
| RC-QB-008 | bounded text-normalization and key identity |
| RC-QB-009 | resolved metric-mismatch outside-applicability reason |
| RC-QB-010 | resolved context-mismatch outside-applicability reason |
| RC-QB-011 | current-extractor end-to-end + unit mismatch + upper-C0 materiality + NA aggregate |
| RC-QB-012 | domain unit-mismatch and no-applicable aggregate |
| RC-QB-013 | current-extractor end-to-end missing-metric unresolved path |
| RC-QB-014 | current-extractor end-to-end missing-context unresolved path |
| RC-QB-015 | domain explicit unresolved-component reasons |
| RC-QB-016 | current-extractor end-to-end unresolved inclusivity path |
| RC-QB-017 | comparator-outside-profile reason |
| RC-QB-018 | current-extractor exhaustive multi-observation order/counts |
| RC-QB-019 | domain all-compatible multi-requirement aggregation |
| RC-QB-020 | domain one-conflict multi-requirement aggregate and Fraction |
| RC-QB-021 | domain denominator includes isolated non-quantitative requirement |
| RC-QB-022 | domain confirmed conflict + partial `R_conf` + UNKNOWN |
| RC-QB-023 | domain compatible result + unresolved comparisons + UNKNOWN |
| RC-QB-024 | current-extractor material diagnostic with no observation/result |
| RC-QB-025 | end-to-end empty specification |
| RC-QB-026 | end-to-end single requirement |
| RC-QB-027 | end-to-end completed universe with no applicable comparison |

All 27 binding cases must also run through one corpus-level conformance harness
at their declared boundary. The approved upper-2/lower-5 `LB-M-C0` pair remains
a non-binding future target now and becomes an end-to-end acceptance case only
after bridge implementation, identifier allocation, audit, and explicit corpus
status update.

## 25. Minimal implementation sequence after approval

Each slice remains separately reviewable and follows issue -> implementation
-> tests -> local review -> commit -> push -> pull request -> merge:

1. prepare the implementation plan/issues and create the separate
   implementation branch; allocate future production identifiers only in the
   subsequently authorized extraction/rule issues;
2. add cross-domain primitives, snapshot, ref/resolver, and validation tests;
3. implement the two-rule atomic `LB-M-C0` bridge with frozen-local regression;
4. add projection and provenance validation;
5. add the fail-closed materiality classifier and audit contract;
6. add exhaustive selection and the pure pair-rule chain;
7. add `R_conf` construction, observability, and Consistency aggregation;
8. add the thin `SpecificationAssessment` and orchestration integration;
9. add composed technical/user report sections;
10. run all binding reference cases and promote the approved future conflict
    target only after its implementation gates pass; and
11. consider refactoring or indexing only after the first behaviorally frozen
    end-to-end slice.

Steps may be divided into smaller one-issue pull requests, but unrelated
layers must not be combined merely to reduce PR count.

## 26. Refactoring boundary

Before the first accepted QB-v0.1 end-to-end slice, do not refactor:

- `RequirementAssessmentRecord`, `RequirementExtractionResult`, Evidence, or
  the six feature-family contracts;
- local C/V/U calculators, profiles, trace contracts, or assessor;
- `SpecificationQualityProfile` or `SpecificationQualityAggregator`;
- existing reporter section behavior;
- detector registries into a generic rule engine;
- local Evidence IDs into global IDs; or
- current ordering helpers merely for hypothetical reuse.

Implementation should be additive. After acceptance, possible separately
justified refactors include shared state/value utilities, versioned rule
registries, ordering helpers, Evidence-reference helpers, and candidate
indexes. None is a prerequisite for correctness.

## 27. Architecture decision register

| Architecture ID | Question | Options | Recommended decision | Rationale | Scientific dependency | Compatibility impact | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CRA-A001 | Where does cross-analysis enter? | Before local assessment; during calculators; after all records | After the immutable ordered `RequirementAssessmentRecord[]` boundary | Prevents cross effects on local calculation and uses the accepted joined record | CRA-D051-D054; frozen pipeline | Additive downstream stage only | `DERIVED_FROM_APPROVED_SCIENCE` |
| CRA-A002 | How should projection isolate record internals? | Pass records everywhere; immutable stable views + scoped resolver; deep-copy every object | Immutable stable views plus snapshot-scoped resolver | Minimal coupling with exact provenance and no memory identity | CRA-D043, D046, D048-D050 | New cross-only values; existing records unchanged | `RESEARCHER_APPROVED` |
| CRA-A003 | What identifies an observation? | Object identity; global new ID; owner + feature + source-order index | `(requirement_id, quantitative feature, observation_index)` within one snapshot | Direct concrete realization of approved identity | CRA-D046, D060-D061 | No existing observation mutation | `DERIVED_FROM_APPROVED_SCIENCE` |
| CRA-A004 | How is Evidence carried? | Duplicate Evidence; globally rewrite IDs; qualified refs resolved against owner | Store `(requirement_id,evidence_id)` refs and validate through resolver | Preserves local IDs and five provenance invariants | CRA-D048-D050, D062 | Existing Evidence unchanged | `DERIVED_FROM_APPROVED_SCIENCE` |
| CRA-A005 | How is one reproducible assessment snapshot identified? | Runtime UUID; path/time key; deterministic canonical QB content/contract identity | Canonical identity over only the Section 6 QB-relevant source state and QB contract manifest; SHA-256 is recommended but exact encoding is a documented, versioned, regression-tested implementation decision | Stable across identical QB inputs/contracts, changes with QB-relevant inputs/contracts, and avoids churn from unrelated local C/V/U or trace changes | CRA-D014, D043, D045; researcher amendment dated 2026-09-25 | New cross-only identity; local-profile identity remains separate | `RESEARCHER_APPROVED` |
| CRA-A006 | What is the cross-result representation? | Loose dictionaries; one frozen validated discriminated value; separate unrelated classes per state | One frozen discriminated result with state-specific constructor validation | Common provenance/order with impossible state combinations rejected | CRA-D011-D013, D043-D047, D056-D058 | New domain type only | `RESEARCHER_APPROVED` |
| CRA-A007 | How are scientific reasons represented? | Prose only; general NLP taxonomy; minimal typed QB enums + structured operands | Minimal typed unresolved/outside enums defined in Section 9 | Stable tests and explanations without scope expansion | CRA-D013, D034, D056-D058 | New cross-only vocabulary | `RESEARCHER_APPROVED` |
| CRA-A008 | How is CRA-D067 implemented? | Modify detector; ignore configured codes; downstream fail-closed classifier with audit | Dedicated downstream classifier with exactly two versioned allowlist descriptors and per-diagnostic audit | Preserves global state while proving QB-only non-materiality | CRA-D067; QB-ER-D009 | No diagnostic or C/V/U mutation | `DERIVED_FROM_APPROVED_SCIENCE` |
| CRA-A009 | How is `LB-M-C0` implemented? | One combined rule; two independent rules; two rules atomically coordinated; generic grammar | Two separately owned bounded rules behind one whole-envelope coordinator; apply both or neither | Preserves QB-ER-D002/D005 separation and prohibits standalone/partial enrichment | QB-ER-D002, D005; model-spec 7.14.6.11 | Additive extraction change; future IDs required, none allocated here | `RESEARCHER_APPROVED` |
| CRA-A010 | Which pair-selection architecture ships first? | Equal-key index; exhaustive universe; hybrid index | Exhaustive ordered requirement/observation Cartesian evaluation | Direct equivalence to science and preserves outside/unresolved coverage | CRA-D005-D009, D057, D060-D061 | Simpler first implementation; possible later performance cost | `RESEARCHER_APPROVED` |
| CRA-A011 | How is supported-set mathematics represented? | General interval algebra; explicit half-line objects; minimal direction/value bound and direct predicate | Minimal inclusive direction/value bound with mixed-direction `lower > upper` predicate | Exactly equivalent for the two approved forms and easiest to explain | CRA-D033-D040 | New pure cross rule; no generic math layer | `RESEARCHER_APPROVED` |
| CRA-A012 | How is `R_conf[QB-v0.1]` built? | Count results; append participants; separate set-union builder | Separate validated set-union builder, emitted in source order | Counts requirements once and preserves partial observed membership | CRA-D015-D017, D021, D028 | New aggregation stage only | `DERIVED_FROM_APPROVED_SCIENCE` |
| CRA-A013 | Should Consistency reuse `CharacteristicAssessment`? | Reuse; separate assessment; refactor a generic envelope first | Separate `QbConsistencyAssessment` | Avoids coupling set-level observability and `R_conf` to local characteristic semantics | CRA-D023-D028, D052-D054, D066-D067 | Existing assessment/profile types unchanged | `RESEARCHER_APPROVED` |
| CRA-A014 | When should `SpecificationAssessment` be introduced? | Never; only after a later release; thin container before first QB reporter integration | Build layers independently, then add the thin container in the first integrated slice | Implements approved Option B without blocking isolated component work | CRA-D054-D055 | New composition; existing profile embedded unchanged | `RESEARCHER_APPROVED` |
| CRA-A015 | How should reporting integrate? | Rewrite existing reporters; calculate inside reporter; compose existing local sections with a new cross section from one report bundle | Additive composed reporter/bundle | Preserves existing meanings and keeps reporting calculation-free | CRA-D043, D051-D055, D064-D065 | Existing output remains a delegated section; new section additive | `RESEARCHER_APPROVED` |
| CRA-A016 | Should an indexed selector be designed now? | Implement now; define numeric threshold; defer pending evidence and equivalence proof | Defer | No approved threshold and exhaustive behavior is the oracle | CRA-D009 | No current optimization dependency | `DEFERRED` |
| CRA-A017 | Should a generic interval/semantic engine be introduced? | Generalize now; bounded direct implementation | Reject generalization for QB-v0.1 | It would add unsupported semantics and speculative refactoring | CRA-D003, D029-D038, D064 | Keeps scope additive and deterministic | `REJECTED` |
| CRA-A018 | Should all responsibilities live in one analyzer module? | Monolith; responsibility-separated package | Reject monolith; use Section 22 boundaries | Independent validation/testing and dependency direction are required | CRA-D010, D027, D043, D051-D052 | More small modules; no circular dependency | `RESEARCHER_APPROVED` |

## 28. Architecture Approval Checklist

The researcher approved all eleven architecture decisions, grouped into ten
review items, on 2026-09-25. Scientifically forced decisions remain classified
`DERIVED_FROM_APPROVED_SCIENCE`; deferred/rejected decisions remain unchanged.

- [x] **CRA-A002 — projection boundary:** immutable stable QB views plus a
  snapshot-scoped provenance resolver.
- [x] **CRA-A005 — snapshot identity:** deterministic canonical QB-relevant
  content/contract identity, with unrelated local C/V/U and trace state
  excluded and exact encoding left to a documented, versioned, regression-tested
  implementation decision.
- [x] **CRA-A006 and CRA-A007 — result/reason representation:** one validated
  discriminated cross-result and the minimal typed QB reason set.
- [x] **CRA-A009 — extraction bridge:** two separately owned metric and context
  rules applied atomically under the exact whole-envelope coordinator.
- [x] **CRA-A010 — pair selection:** exhaustive evaluation as the first
  implementation and behavioral-equivalence oracle; no initial index.
- [x] **CRA-A011 — bound representation:** minimal inclusive direction/value
  representation and direct exact-`Decimal` predicate.
- [x] **CRA-A013 — Consistency representation:** separate immutable
  `QbConsistencyAssessment`, with no local assessment reuse/refactoring.
- [x] **CRA-A014 — specification composition timing:** thin non-scalar
  `SpecificationAssessment` in the first integrated reporting slice.
- [x] **CRA-A015 — reporting boundary:** additive report composition from one
  immutable bundle while preserving existing local-section meaning.
- [x] **CRA-A018 — module separation:** responsibility-separated
  cross-analysis modules; no monolithic analyzer.

All eleven decisions above are `RESEARCHER_APPROVED`. This closes QB-v0.1
architecture design and authorizes implementation planning, not production
implementation on the current research branch.

## 29. Architecture contradiction audit

### 29.1 All 41 approved original QB decisions

| Approved decision group | Architecture evidence | Audit result |
| --- | --- | --- |
| CRA-D001, D005-D007 — scope/universe | Sections 2, 12, and 13 use unordered distinct requirement pairs and every cross-observation product | Conforms |
| CRA-D011-D013 — four states and deterministic confirmation | Sections 7-9 define the four states, state validation, and no candidate-as-fact path | Conforms |
| CRA-D019-D021 — single/no-observation/partial set | Sections 15-16 preserve NA and partial observed `R_conf` without a numeric value | Conforms |
| CRA-D023-D026, D066-D067 — exact bounded aggregate and observability | Sections 10 and 16 use exact Fraction, strict material UNKNOWN, exact C0 exception, full metadata, and coverage-qualified name | Conforms |
| CRA-D029 — normalization | Section 13 permits only NFC, case folding, whitespace collapse, and trim | Conforms |
| CRA-D030, D032, D036 — metric/context/key identity | Sections 3, 8, and 13 require resolved normalized metric/context and exact unit | Conforms |
| CRA-D033-D035 — unit/comparator/value | Sections 9, 13, and 14 prohibit conversion and use only supported inclusive comparators with exact Decimal | Conforms |
| CRA-D037-D038, D041 — admissible sets/conflict/examples | Section 14 implements the exact half-line predicate; Section 24 maps all binding examples to conformance tests | Conforms |
| CRA-D043, D044, D046 — result contract | Sections 4 and 7 preserve stable IDs, participants, refs, relation, rules, Evidence, reasons, coverage, and order | Conforms |
| CRA-D048, D050 — Evidence | Section 5 implements qualified refs and fail-fast five-plus validation | Conforms |
| CRA-D051-D052 — local boundary | Sections 1, 2, 18, and 23 make cross-analysis downstream and separate | Conforms |
| CRA-D054 — broader specification boundary | Section 17 implements Option B composition without changing the local profile | Conforms |
| CRA-D056-D058 — unknown/outside boundary | Sections 8-9 preserve unresolved versus resolved mismatch and never call outside compatible | Conforms |
| CRA-D060-D062 — deterministic order | Sections 3-7, 12, and 15 preserve source, observation, result, and Evidence order | Conforms |
| CRA-D064 — non-claims | Sections 7, 16, and 19 make bounded non-claims mandatory report data | Conforms |

### 29.2 QB extraction-readiness decisions

| Decision | Architecture evidence | Audit result |
| --- | --- | --- |
| QB-ER-D002 | Section 11 permits metric enrichment only in exact `LB-M-C0`, enriches the existing scalar, and rejects standalone `LB-M0` | Conforms |
| QB-ER-D005 | Section 11 separates lower-C0 ownership, preserves existing `QUANT-CONTEXT-001`, and defers actual IDs | Conforms |
| QB-ER-D009 | Section 10 preserves global state and uses exactly the two approved C0 contracts with all fail-closed gates | Conforms |

### 29.3 Binding corpus and frozen local boundary

- Section 24 maps every RC-QB-001 through RC-QB-027 to a future test boundary;
  the ten current end-to-end cases remain end-to-end and the seventeen domain
  cases remain binding at domain-contract level.
- The future upper-2/lower-5 pair is not promoted before the bridge exists.
- No architecture stage writes to a `RequirementAssessmentRecord`, local
  profile, trace, extraction outcome, diagnostic, `SpecificationQualityProfile`,
  or `AGG-MVP-001` result.
- The approved bridge changes only exact metric/context linkage and Evidence
  under the extraction boundary while preserving local numeric behavior.

The audit found no conflict among the frozen scientific contracts, the 27-case
corpus, and the approved additive architecture. All scientific obligations can
be implemented without changing Single Requirement Analysis.

`NO_SCIENTIFIC_CONTRADICTION_FOUND`

## 30. Readiness conclusion

The QB-v0.1 scientific research and architecture research/design phases are
closed. The next phase is implementation planning followed by creation of the
separate implementation branch. Production implementation, test creation,
identifier allocation, refactoring, and implementation-branch creation were
not performed in this architecture-approval round.

ARCHITECTURE_APPROVED_READY_FOR_IMPLEMENTATION
