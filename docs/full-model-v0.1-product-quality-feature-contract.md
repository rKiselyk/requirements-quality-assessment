# Full Model v0.1 Product-Quality Feature Contract

**Contract ID:** `FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE`  
**Contract version:** `1`  
**Target issue:** `M3-04 / #141`  
**Bounded characteristic:** `PERFORMANCE_EFFICIENCY`  
**Status:** `NORMATIVE_CANDIDATE / PARENT_CONTRACT_APPROVAL_REQUIRED`

## 1. Purpose and authority

This document defines the normative, implementation-ready contract for the
Full Model v0.1 Performance Efficiency feature profile:

```text
P / MetricProfile + DynamicEvidence -> X_PE
```

It defines data selection, identity, roles, state propagation, provenance, and
the boundary between assessment inputs and contextual information. It does not
implement M3-04, calculate product quality, add extraction coverage, or define
a predictive model.

Normative precedence is:

1. `docs/full-model-v0.1-contract.md`;
2. this contract for `X_PE`;
3. `docs/full-model-v0.1-metric-profile-contract.md`;
4. `docs/full-model-v0.1-dynamic-evidence-contract.md`;
5. the approved QB-v0.1 contracts and `docs/model-spec.md`; and
6. dissertation material in `docs/reference/` as research rationale rather
   than executable specification.

This contract inherits rather than reopens the parent decisions that Full
Model v0.1:

- selects only Performance Efficiency;
- uses one supported response-time criterion and one observation in the same
  exact unit and context;
- preserves existing C/V/U and QB semantics;
- uses no normalization, weighting, rounding, imputation, or scalar overall
  requirement-quality value; and
- does not calculate predicted product quality.

## 2. Scientific basis and bounded operationalization

### 2.1 Dissertation findings adopted

The feature contract is based on the following distinctions in the dissertation:

- Chapter 2.2 distinguishes requirement-artifact quality from implemented
  product quality. Requirement-property indicators are not themselves product
  characteristic values.
- Chapter 2.2 identifies an explicit quantitative response-time requirement,
  its load condition, and later product measurement as a direct semantic path
  to Performance Efficiency. C/V/U defects instead act through risk and
  verification mechanisms whose strength requires empirical study.
- Chapter 3.2 requires a traceable chain from requirement to criterion,
  observation, and conformance, and preserves execution context.
- Chapter 3.2 distinguishes evidence coverage from conformance and states that
  absent dynamic data is not a negative result.
- Chapter 3.3 requires characteristic-specific feature formation, source
  traceability, applicability and availability masks, deduplication, and no
  zero filling. Feature selection and predictive contribution require later
  experimental work.
- Chapter 4.2 treats feature formation and predictive assessment as separate
  operations. Missing evidence is masked, not replaced by zero, and model
  parameters require calibration.

### 2.2 Bounded operational decisions

Full Model v0.1 adopts only the minimum deterministic subset needed for the
reference path:

```text
one source-backed response-time criterion
+ one exact response-time observation
+ one categorical conformance assessment
+ one target-scoped QB consistency gate
+ the selected requirement's C/V/U entries as context
-> one versioned X_PE feature profile
```

The profile is a named, typed record. It is not the dissertation's future
normalized or experimentally selected numeric vector. The mapping is fixed by
the parent contract and is not evidence that the included features have
predictive power.

## 3. Scope and non-scope

This contract covers only:

- `PERFORMANCE_EFFICIENCY`;
- dynamic metric `DYN.RESPONSE_TIME`;
- comparator `LESS_THAN_OR_EQUAL / INCLUSIVE`;
- unit `SECOND`;
- the exact supported QB-normalized response-time context;
- the selected criterion requirement's C/V/U metric entries;
- target-relevant QB-v0.1 cross results; and
- one `REFERENCE_VERIFICATION` process-state snapshot.

It does not cover:

- throughput, resource utilization, capacity, latency percentiles, averages,
  distributions, availability, reliability, or any other product measure;
- unit conversion, statistical reduction, repeated-measure aggregation, or
  measurement uncertainty;
- selection or training of `F_theta`;
- feature weights, contributions, scaling, normalization, or ranking;
- an early prediction vector or an updated prediction vector;
- full Performance Efficiency coverage; or
- another ISO/IEC 25010 characteristic.

## 4. Feature registry and rule identities

### 4.1 Closed registry

```text
registry_id      = FULL-MODEL-V0.1-PE-FEATURES
registry_version = 1
```

The registry contains exactly seven entries in this order:

| Ordinal | Feature ID | Source | Effect on bounded assessment |
| ---: | --- | --- | --- |
| 1 | `PE.CRITERION.RESPONSE_TIME` | `CriterionBindingResult` and `QuantitativeCriterion` | `REQUIRED_INPUT`: defines the target and context |
| 2 | `PE.REQ.C` | selected requirement's `RQ.COMPLETENESS` `MetricEntry` | `CONTEXT_ONLY` |
| 3 | `PE.REQ.V` | selected requirement's `RQ.VERIFIABILITY` `MetricEntry` | `CONTEXT_ONLY` |
| 4 | `PE.REQ.U` | selected requirement's `RQ.UNAMBIGUITY` `MetricEntry` | `CONTEXT_ONLY` |
| 5 | `PE.SPEC.QB` | target-scoped projection of QB metric provenance and cross results | `ELIGIBILITY_GATE` |
| 6 | `PE.OBS.RESPONSE_TIME` | `ObservationResolution` and `DynamicObservation` | `REQUIRED_INPUT` |
| 7 | `PE.CONFORMANCE.RESPONSE_TIME` | `ConformanceAssessment` | `DIRECT_RESULT_INPUT` |

No implementation may append a feature, omit a slot, change this order, or
replace a missing value with a different metric under registry version `1`.
An unavailable or inapplicable slot remains present with no typed value.

### 4.2 Mapping rule

The sole mapping rule is:

```text
P-M-E-TO-X-PE-001 / 1
```

It performs selection, validation, reference construction, and state
propagation only. It performs no product-quality calculation.

### 4.3 Features deliberately excluded

The following are not `X_PE` features in v0.1:

- `SPEC.MEAN_COMPLETENESS`, `SPEC.MEAN_VERIFIABILITY`, and
  `SPEC.MEAN_UNAMBIGUITY`;
- C/V/U entries for requirements other than the criterion's source
  requirement;
- the numeric value of `SPEC.QB_CONSISTENCY` as an assessment operand;
- unrelated QB cross results;
- raw quantitative bounds as anonymous numeric features;
- diagnostic counts, finding counts, or source-processing completeness as
  numeric predictors; and
- every metric not named in Section 4.1.

The exclusion is scientific, not merely technical: no approved mapping assigns
these values a product-quality contribution. They may remain reachable through
provenance where the source contracts require them.

## 5. Core record contracts

### 5.1 Construction context

```text
PerformanceEfficiencyFeatureConstructionContext
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  metric_profile_ref: MetricProfileRef
  dynamic_assessment_ref: DynamicEvidenceAssessmentRef
  product_ref: ProductRef
  process_state_ref: ProcessStateRef
  full_model_contract_ref: ContractRef
  feature_contract_ref: ContractRef
  feature_registry_ref: ContractRef
  mapping_rule_ref: RuleRef
```

The caller supplies every versioned identity. The mapper must not infer an
artifact, assessment, product, process-state, or rule version from text,
timestamps, file names, object addresses, or ordering.

### 5.2 PerformanceEfficiencyFeatureProfile

```text
PerformanceEfficiencyFeatureProfile
  profile_id: PerformanceEfficiencyFeatureProfileId
  characteristic_id: PERFORMANCE_EFFICIENCY
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  metric_profile_ref: MetricProfileRef
  dynamic_assessment_ref: DynamicEvidenceAssessmentRef
  product_ref: ProductRef
  process_state_ref: ProcessStateRef
  criterion_subject_ref: RequirementSubjectRef | None
  target_key: QbComparisonKey | None
  status: FullModelStatus
  applicability: Applicability
  features: tuple[PerformanceEfficiencyFeature, ...]
  provenance: FeatureProfileProvenance
  registry_ref: ContractRef
  mapping_rule_ref: RuleRef
```

`features` has exactly seven entries in registry order. `status` reports
whether the profile supplies a justified input to the later bounded assessment;
it is not an aggregate of feature values.

### 5.3 PerformanceEfficiencyFeature

```text
PerformanceEfficiencyFeature
  feature_entry_id: PerformanceEfficiencyFeatureEntryId
  feature_id: PerformanceEfficiencyFeatureId
  characteristic_id: PERFORMANCE_EFFICIENCY
  effect: REQUIRED_INPUT | DIRECT_RESULT_INPUT | ELIGIBILITY_GATE | CONTEXT_ONLY
  status: FullModelStatus
  applicability: Applicability
  typed_value: PeFeatureValue | None
  source_refs: tuple[TypedSourceRef, ...]
  evidence_refs: tuple[EvidenceRef, ...]
  provenance_refs: tuple[ProvenanceRef, ...]
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  product_ref: ProductRef | None
  availability_point: AvailabilityPoint
  rule_refs: tuple[RuleRef, ...]
```

The closed `PeFeatureValue` alternatives are:

```text
CriterionFeatureValue(criterion_ref, metric_ref, comparator, inclusivity,
                      exact_decimal_bound, unit, context_identity)
RequirementMetricFeatureValue(metric_entry_ref, exact_fraction_or_none)
QbTargetGateFeatureValue(qb_metric_entry_ref, gate_decision,
                         target_key, ordered_cross_result_refs)
ObservationFeatureValue(observation_ref, metric_ref,
                        exact_decimal_value, unit, context_identity)
ConformanceFeatureValue(conformance_ref, outcome)
```

Decimal and Fraction fields are copied only to make the immutable feature
snapshot self-describing. They must equal their source values exactly. Source
references remain authoritative and must resolve.

## 6. Identity and subject rules

### 6.1 Profile identity

```text
PerformanceEfficiencyFeatureProfileId = (
  artifact_ref,
  source_assessment_ref,
  metric_profile_ref,
  dynamic_assessment_ref,
  product_ref,
  process_state_ref,
  feature_registry_ref,
  mapping_rule_ref,
)
```

No hash is required. A changed source assessment, metric profile, dynamic
assessment, product version, process state, registry, or mapping rule produces
a different profile identity.

### 6.2 Feature entry identity

```text
PerformanceEfficiencyFeatureEntryId = (profile_id, feature_id)
```

Each identity occurs exactly once. A value or status change under the same
profile identity is invalid.

### 6.3 Selected requirement subject

When the criterion is available, `criterion_subject_ref` is exactly the
criterion's `RequirementSubjectRef`:

```text
(artifact_id, artifact_version, requirement_id, source_line)
```

It must equal the subject of the three selected C/V/U metric entries. A bare
generated requirement ID such as `R001` is insufficient and carries no
cross-version lineage meaning.

When criterion binding is not available, the subject is copied from the
binding result if that result identifies one unambiguously; otherwise it is
absent. The mapper must not choose a requirement by text similarity.

### 6.4 Product subject

The criterion and requirement metrics describe a specification artifact. The
observation and conformance describe a `ProductRef`. The profile binds both
subjects without equating them. A product version is never inferred from an
artifact version.

## 7. Exact source selection

### 7.1 Criterion

`PE.CRITERION.RESPONSE_TIME` selects exactly one result produced under
`DYN-CRITERION-RESPONSE-TIME-001 / 1`. An available value must reference:

```text
dynamic metric = DYN.RESPONSE_TIME
source metric  = N("Час відгуку") = "час відгуку"
comparator     = LESS_THAN_OR_EQUAL
inclusivity    = INCLUSIVE
unit           = SECOND
context        = (QB-NORMALIZATION / 1,
                  "при 500 одночасних користувачах")
```

The mapper does not reparse requirement text or reconstruct criterion
components. It copies the criterion's exact Decimal bound and all references.

### 7.2 Requirement C/V/U

For the criterion subject, the mapper selects exactly:

```text
RQ.COMPLETENESS   -> PE.REQ.C
RQ.VERIFIABILITY  -> PE.REQ.V
RQ.UNAMBIGUITY    -> PE.REQ.U
```

The source entries must belong to the named `MetricProfile`, artifact,
assessment, and subject. The exact `Fraction`, status, applicability, numeric
representation, rule references, and provenance are preserved.

These features answer only how the source requirement artifact was assessed.
They do not alter criterion comparison, QB target gating, conformance, or the
later binary observed indicator. In particular:

- `Fraction(0,1)` is not product failure;
- `Fraction(1,1)` is not product conformance;
- `UNKNOWN` does not suppress an otherwise justified dynamic conformance; and
- `NOT_APPLICABLE` is not converted to zero.

If a non-available criterion binding still identifies exactly one requirement
subject, the mapper selects that subject's entries and preserves their states.
If no subject can be justified, the three fixed C/V/U slots are
`UNRESOLVED/UNKNOWN` with no value and a typed
`CRITERION_SUBJECT_UNRESOLVED` reason; those context-only states do not replace
the controlling criterion status. If a subject is justified but the required
entry is absent from an otherwise asserted valid MetricProfile, construction
fails as invalid input rather than manufacturing an absence state.

### 7.3 Observation

`PE.OBS.RESPONSE_TIME` selects the `ObservationResolution` referenced by the
chosen conformance assessment. If available, its observation must use the same
`ProductRef`, `DYN.RESPONSE_TIME`, `SECOND`, and exact context identity as the
criterion. The exact Decimal value is preserved without conversion,
quantization, or rounding.

### 7.4 Conformance

`PE.CONFORMANCE.RESPONSE_TIME` selects exactly one `ConformanceAssessment`
produced under `DYN-CONFORMANCE-RESPONSE-TIME-001 / 1`. Its criterion and
observation references must be those selected by Sections 7.1 and 7.3.

An available feature contains exactly one categorical outcome:

```text
CONFORMS
DOES_NOT_CONFORM
```

The feature layer does not map the outcome to a number. M3-05 owns the parent-
approved `{0,1}` representation.

## 8. Target-scoped QB gate

### 8.1 Purpose

`PE.SPEC.QB` is not a second product-quality score. It is a projection that
answers only whether QB-v0.1 evidence permits this exact response-time target
to be used without silently choosing among contradictory bounds.

Its constrained-subject key is copied from QB-v0.1:

```text
K(q) = (
  N(metric_text(q)),
  N(context_text(q)),
  unit_label(q),
)
```

For the reference criterion:

```text
target_key = (
  "час відгуку",
  "при 500 одночасних користувачах",
  SECOND,
)
```

This remains a bounded textual identity, not a semantic ontology.

### 8.2 Closed gate decisions

```text
TARGET_CLEAR
TARGET_CONFLICT
TARGET_UNRESOLVED
TARGET_NOT_APPLICABLE
```

| Gate decision | Feature status/applicability | Meaning | Assessment effect |
| --- | --- | --- | --- |
| `TARGET_CLEAR` | `AVAILABLE/APPLICABLE` | Target-relevant QB comparisons are complete and no confirmed conflict has the target key | permits evaluation; never changes the conformance value |
| `TARGET_CONFLICT` | `AVAILABLE/APPLICABLE` | At least one `CONFIRMED_CONFLICT` has the exact target key | profile and later result become `UNRESOLVED`; no bound is chosen |
| `TARGET_UNRESOLVED` | `UNRESOLVED/APPLICABLE` or `UNRESOLVED/UNKNOWN` | Required target-related identity/comparison evidence cannot establish whether the chosen target is consistent | profile and later result become `UNRESOLVED` |
| `TARGET_NOT_APPLICABLE` | `NOT_APPLICABLE/NOT_APPLICABLE` | No cross-requirement comparison applies to the selected target and target-local coverage proves that absence | does not block the one-criterion procedure |

The `TARGET_CONFLICT` feature itself is `AVAILABLE`: QB successfully produced
a bounded classification. The profile is nevertheless `UNRESOLVED` because a
single authoritative target cannot be selected.

### 8.3 Projection algorithm

The target gate is formed without reading the aggregate Fraction as follows:

1. validate that `SPEC.QB_CONSISTENCY` and its provenance belong to the same
   artifact, assessment, and snapshot as the selected criterion source;
2. derive `target_key` from the criterion's already accepted metric, context,
   and unit identity; do not normalize again under a different rule;
3. preserve the QB metric entry and its complete provenance as source context;
4. select every `CONFIRMED_CONFLICT` whose complete comparison key equals
   `target_key`, whether or not the chosen criterion is a participant;
5. select every `ASSESSMENT_UNRESOLVED` for which all resolved comparison-key
   components equal the corresponding target-key components and the unresolved
   components could complete to the target key; this includes, but is not
   limited to, pairs involving the chosen criterion source observation;
6. validate target-key coverage: every source observation whose resolved and
   unresolved identity components could form the target key must be represented
   in the QB comparison population, and no materiality/coverage diagnostic may
   leave a potentially target-key comparison unobserved;
7. if Step 4 is non-empty, return `TARGET_CONFLICT`;
8. otherwise, if Step 5 is non-empty or Step 6 cannot be established, return
   `TARGET_UNRESOLVED`;
9. otherwise, if one or more applicable same-key comparisons are all
   `COMPATIBLE_WITHIN_RULE`, return `TARGET_CLEAR`; and
10. otherwise return `TARGET_NOT_APPLICABLE`.

Confirmed conflicts on unrelated complete keys and unresolved comparisons
whose resolved components prove that they cannot have the target key stay in
provenance but do not alter this gate. A global QB aggregate `UNKNOWN` is not
automatically converted into target failure: the projection must apply Steps
4-10. If the source cannot exclude an unresolved comparison or unobserved
candidate from the target key, the decision is `TARGET_UNRESOLVED`.
Conversely, an aggregate Fraction, including `Fraction(1,1)`, never overrides
a target-specific conflict or unresolved comparison.

### 8.4 QB numeric and evidence separation

The feature preserves two distinct numeric domains:

- `MetricEntry.value`, when available, remains exact `Fraction` and describes
  only bounded specification Consistency; and
- quantitative criterion operands remain exact `Decimal` values in QB and
  dynamic evidence.

The mapper must not compare the QB Fraction with the response-time bound, turn
the Decimal bound into a Fraction feature, or use `M_cons[QB-v0.1]` as a
Performance Efficiency value.

## 9. Which features affect assessment

The effect contract is exact:

| Feature | Can determine availability/applicability? | Can change `{0,1}` when conformance is available? | Context/provenance role |
| --- | --- | --- | --- |
| `PE.CRITERION.RESPONSE_TIME` | yes | no; it is already reflected in conformance | target, bound, unit, context |
| `PE.REQ.C` | no | no | requirement-artifact quality context |
| `PE.REQ.V` | no | no | requirement-artifact quality context |
| `PE.REQ.U` | no | no | requirement-artifact quality context |
| `PE.SPEC.QB` | yes, as target gate | no | bounded target-consistency evidence |
| `PE.OBS.RESPONSE_TIME` | yes | no; it is already reflected in conformance | measured product behavior |
| `PE.CONFORMANCE.RESPONSE_TIME` | yes | yes: it is the only direct result input | exact criterion-observation relation |

Only `CONFORMS` versus `DOES_NOT_CONFORM` selects the later binary value. No
C/V/U or QB numeric value changes or weights that mapping.

## 10. Status and applicability propagation

### 10.1 Feature-level mapping

- Criterion, observation, conformance, and C/V/U slots copy their source
  status and applicability exactly.
- `PE.SPEC.QB` uses the target-gate mapping in Section 8.2 while retaining the
  source QB metric status separately in its typed value and provenance.
- If no target key exists, the QB feature copies the controlling criterion
  `NOT_APPLICABLE`, `UNAVAILABLE`, `UNKNOWN`, `UNRESOLVED`, or `UNSUPPORTED`
  state and has no gate value. It does not inspect QB evidence for a different
  target.
- Every non-`AVAILABLE` feature has `typed_value=None`, except that a
  `TARGET_CONFLICT` is an available categorical gate value.
- Every `NOT_APPLICABLE` feature uses applicability `NOT_APPLICABLE`.
- Missing source objects are never represented by zero or empty evidence.

### 10.2 Profile readiness precedence

After structural validation, profile status is determined in this order:

1. criterion `NOT_APPLICABLE` -> `NOT_APPLICABLE/NOT_APPLICABLE`;
2. criterion `UNAVAILABLE`, `UNKNOWN`, `UNRESOLVED`, or `UNSUPPORTED` -> copy
   its status and applicability;
3. QB gate `TARGET_CONFLICT` or `TARGET_UNRESOLVED` ->
   `UNRESOLVED/APPLICABLE`;
4. observation `UNAVAILABLE`, `UNKNOWN`, `UNRESOLVED`, or `UNSUPPORTED` -> copy
   its status and applicability;
5. conformance `NOT_APPLICABLE`, `UNAVAILABLE`, `UNKNOWN`, `UNRESOLVED`, or
   `UNSUPPORTED` -> copy its status and applicability;
6. available conformance with `TARGET_CLEAR` or `TARGET_NOT_APPLICABLE` ->
   `AVAILABLE/APPLICABLE`.

The C/V/U slots do not enter this precedence. Their exact states remain
visible, including `UNKNOWN` and `NOT_APPLICABLE`.

An internally contradictory identity, duplicate slot, dangling reference, or
source/value mismatch is invalid input and fails profile construction. It is
not converted to a scientific status.

### 10.3 Meaning of absence states

- `UNAVAILABLE`: the supported applicable source has not been produced for the
  stated version or collection point.
- `UNKNOWN`: an approved source assessment cannot determine the value from its
  available information.
- `UNRESOLVED`: identity, comparison, or a required semantic/processing
  decision cannot justify a target or result.
- `UNSUPPORTED`: resolved input lies outside this contract, such as another
  comparator, unit, or context.
- `NOT_APPLICABLE`: an approved rule excludes the case.

None means `DOES_NOT_CONFORM`, zero, poor quality, or absence of risk.

## 11. Temporal availability

Full Model v0.1 retains the sole process stage `REFERENCE_VERIFICATION`.
Temporal availability within its evidence chain is recorded by dependency
completion, not by inventing additional lifecycle stages:

```text
SOURCE_ASSESSMENT_AVAILABLE
CRITERION_BINDING_AVAILABLE
DYNAMIC_COLLECTION_AVAILABLE
CONFORMANCE_ASSESSMENT_AVAILABLE
```

| Feature | Earliest availability point |
| --- | --- |
| `PE.REQ.C`, `PE.REQ.V`, `PE.REQ.U`, `PE.SPEC.QB` | `SOURCE_ASSESSMENT_AVAILABLE` |
| `PE.CRITERION.RESPONSE_TIME` | `CRITERION_BINDING_AVAILABLE` |
| `PE.OBS.RESPONSE_TIME` | `DYNAMIC_COLLECTION_AVAILABLE` |
| `PE.CONFORMANCE.RESPONSE_TIME` | `CONFORMANCE_ASSESSMENT_AVAILABLE` |

A profile is an immutable snapshot for one `process_state_ref`. If dynamic
evidence is not yet available, observation and conformance slots are
`UNAVAILABLE` and the profile has no assessment-ready value. Later evidence
creates a new dynamic assessment, process state, and feature profile. It must
not be backfilled into the earlier profile.

## 12. Provenance

### 12.1 Profile provenance

```text
FeatureProfileProvenance
  artifact_ref
  source_assessment_ref
  source_snapshot_id
  metric_profile_ref
  criterion_binding_ref
  observation_resolution_ref
  conformance_assessment_ref
  dynamic_assessment_ref
  product_ref
  environment_ref_or_none
  collection_ref_or_none
  process_state_ref
  ordered_feature_entry_refs
  source_contract_refs
  rule_refs
```

### 12.2 Required chains

The following chains must resolve:

```text
Requirement -> extraction Evidence -> C/V/U assessment -> MetricEntry
            -> PE.REQ.C / PE.REQ.V / PE.REQ.U

Requirement -> quantitative observation -> QuantitativeCriterion
            -> PE.CRITERION.RESPONSE_TIME

Specification -> QB cross result / QB MetricEntry -> PE.SPEC.QB

Product + collection + environment -> DynamicObservation
                                   -> PE.OBS.RESPONSE_TIME

Criterion + observation -> ConformanceAssessment
                        -> PE.CONFORMANCE.RESPONSE_TIME
```

Original evidence text, offsets, diagnostics, exact Decimal tuples, Fraction
numerator/denominator, source explanations, and non-claim descriptors remain
reachable. The mapper does not allocate replacement evidence IDs or copy
source evidence into a new scientific observation.

### 12.3 Explanation boundary

`X_PE` may explain why a feature was selected, unavailable, unresolved,
unsupported, or inapplicable. It must not describe a C/V/U score as causing
product behavior or a QB conflict as proof of poor implemented performance.

## 13. Version semantics

Every profile preserves:

- specification artifact ID/version;
- source assessment ID/version and QB snapshot ID;
- MetricProfile ID, registry version, and adapter rule version;
- dynamic evidence assessment, registry, binding rule, and evaluator rule;
- product, collection, and environment versions;
- Full Model and both focused contract versions;
- `FULL-MODEL-V0.1-PE-FEATURES / 1`; and
- `P-M-E-TO-X-PE-001 / 1`.

Existing stable rule IDs such as `CALC-C-MVP-001` retain the version authority
defined by `docs/model-spec.md`; this contract does not fabricate explicit
version numbers for them. QB contract descriptors retain their own versions.

A semantic change to feature selection, role, target-gate logic, state
precedence, or registry order requires a new mapping-rule and contract/registry
version. A changed source value requires a new source assessment or collection
identity. Reporter formatting does not change scientific identity.

## 14. Conflict and multiplicity handling

The bounded mapper requires one criterion binding and one conformance path.

- Zero applicable criteria -> criterion and profile `NOT_APPLICABLE` when an
  approved binding result establishes that state.
- One applicable supported criterion -> continue.
- More than one candidate criterion with no explicit caller-selected,
  versioned criterion reference -> `UNRESOLVED`; do not select by order, value,
  text length, or favorable outcome.
- A caller may provide an explicit criterion reference only if it is already a
  valid result under the dynamic-evidence contract. The choice is provenance,
  not an assessment by the mapper.
- More than one observation for the selected criterion with no explicit
  observation slot in the conformance reference -> `UNRESOLVED`; do not
  average, take worst/best, or choose latest.
- Any QB `TARGET_CONFLICT` -> profile `UNRESOLVED` even when a dynamic
  conformance outcome exists. The dynamic outcome remains preserved as
  evidence but is not promoted to a product-quality result for a contradictory
  specification target.

## 15. Determinism and ordering

For identical immutable inputs and versions, the profile identity, status,
applicability, feature records, explanations, and ordered references are
identical.

Ordering is:

1. feature entries by the registry order in Section 4.1;
2. feature source references in their source-contract order;
3. QB cross results in source QB cross-result order;
4. evidence and diagnostic references in source order, de-duplicated by first
   occurrence only where the source contract already permits it; and
5. rule/contract references in the dependency order used to produce the
   feature.

No sorting by value, status, conformance outcome, conflict severity, evidence
count, text, or display label is permitted.

## 16. Invariants and forbidden transformations

### 16.1 Required invariants

1. The profile characteristic is exactly `PERFORMANCE_EFFICIENCY`.
2. The profile contains exactly the seven registry slots, once each, in order.
3. All source artifact, assessment, snapshot, subject, product, and dynamic
   references are mutually consistent.
4. Criterion, observation, and conformance form one valid dynamic-evidence
   chain.
5. Available criterion and observation values preserve exact finite Decimal
   tuples and use exact `SECOND` and equal context identity.
6. C/V/U values preserve exact Fraction numerator and denominator.
7. `PE.SPEC.QB` preserves the source QB metric and relevant cross-result
   provenance while applying only the target gate.
8. An available conformance feature contains exactly one categorical outcome.
9. Context-only features never affect profile readiness or product result.
10. Every non-available state has no fabricated numeric value.
11. The profile is immutable and tied to one process-state snapshot.
12. Every explanation is traceable to typed reasons and source references.

### 16.2 Forbidden transformations

An implementation must not:

- normalize, rescale, weight, average, round, rank, or impute features;
- convert Decimal through float or Fraction, or Fraction through float or
  Decimal;
- use the QB aggregate Fraction as a criterion bound or product-quality value;
- use C/V/U as product-quality values or alter conformance from them;
- include specification C/V/U means or unrelated requirement metrics;
- treat a missing observation as `DOES_NOT_CONFORM`;
- treat `NOT_APPLICABLE`, `UNKNOWN`, `UNAVAILABLE`, `UNRESOLVED`, or
  `UNSUPPORTED` as zero;
- choose one side of a same-key QB conflict;
- infer synonyms, context overlap, unit conversion, or criterion identity;
- aggregate multiple observations or criteria;
- claim that `X_PE` is a prediction or full characteristic assessment; or
- mutate an earlier feature profile when later evidence arrives.

## 17. Deterministic reference fixtures

### 17.1 Shared source objects

```text
artifact_ref          = (SPEC-PE-001, 1)
source_assessment_ref = (ASSESS-SPEC-PE-001, 1, artifact_ref)
metric_profile_ref    = (artifact_ref, source_assessment_ref,
                         FULL-MODEL-V0.1-METRICS/1)
product_ref           = (PRODUCT-PE-001, 1)
process_state_ref     = (PROCESS-PE-001, 1, REFERENCE_VERIFICATION)
requirement_subject   = (artifact_ref, R001, source_line=1)
requirement text      = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
criterion bound       = Decimal("2")
criterion unit        = SECOND
target_key            = ("час відгуку",
                         "при 500 одночасних користувачах", SECOND)
```

The requirement's C/V/U entries are whichever exact source states and
Fractions the existing P-to-M adapter produced. Fixtures below do not alter
them.

### 17.2 Feature cases

| Fixture | Variable source facts | Expected profile result |
| --- | --- | --- |
| `PE-X-RF-001` | observation `Decimal("1.8")`; conformance `CONFORMS`; QB target clear | `AVAILABLE/APPLICABLE`; all required dynamic slots available |
| `PE-X-RF-002` | observation `Decimal("2")`; conformance `CONFORMS`; QB target not applicable | `AVAILABLE/APPLICABLE`; equality remains in dynamic evidence |
| `PE-X-RF-003` | observation `Decimal("2.1")`; conformance `DOES_NOT_CONFORM`; QB target clear | `AVAILABLE/APPLICABLE`; negative conformance is still available evidence |
| `PE-X-RF-004` | observation slot exists but no observation was supplied | `UNAVAILABLE/APPLICABLE`; observation and conformance have no values |
| `PE-X-RF-005` | observation unit `MINUTE` | `UNSUPPORTED/APPLICABLE`; no conversion |
| `PE-X-RF-006` | context identity unresolved | `UNRESOLVED`; no inferred context |
| `PE-X-RF-007` | confirmed QB conflict with exact target key | QB feature `TARGET_CONFLICT`; profile `UNRESOLVED`; conformance preserved but not assessment-ready |
| `PE-X-RF-008` | confirmed QB conflict on another complete key | conflict remains provenance only; profile follows selected path |
| `PE-X-RF-009` | unresolved QB pair involving selected criterion and potentially the target key | QB feature and profile `UNRESOLVED` |
| `PE-X-RF-010` | C/V/U states are all `UNKNOWN`; supported conformance is `CONFORMS` | profile remains `AVAILABLE`; the three unknown states remain visible |
| `PE-X-RF-011` | no applicable response-time criterion under binding rule | `NOT_APPLICABLE/NOT_APPLICABLE` |
| `PE-X-RF-012` | two candidate criteria, no explicit criterion reference | `UNRESOLVED`; no automatic selection |

## 18. Acceptance cases for future M3-04 implementation

| ID | Required behavior |
| --- | --- |
| `PE-X-AC-001` | The registry ID/version and seven feature IDs exactly match Section 4.1. |
| `PE-X-AC-002` | Every valid profile contains exactly seven entries in normative order. |
| `PE-X-AC-003` | Profile and feature identities are deterministic structured keys. |
| `PE-X-AC-004` | Only the criterion source requirement's C/V/U entries are selected. |
| `PE-X-AC-005` | Specification C/V/U means and unrelated requirement entries are excluded. |
| `PE-X-AC-006` | C/V/U Fraction values round-trip exactly without float or Decimal conversion. |
| `PE-X-AC-007` | Criterion and observation Decimal tuples round-trip exactly without float or Fraction conversion. |
| `PE-X-AC-008` | C/V/U feature statuses and applicability copy their MetricEntry sources exactly. |
| `PE-X-AC-009` | C/V/U values and statuses cannot alter profile readiness or conformance outcome. |
| `PE-X-AC-010` | Criterion selection uses a dynamic criterion reference and performs no reparsing. |
| `PE-X-AC-011` | Observation selection uses the conformance-linked observation slot/reference. |
| `PE-X-AC-012` | Criterion, observation, and conformance references must form one consistent chain. |
| `PE-X-AC-013` | Exact metric, unit, and context equality are validated. |
| `PE-X-AC-014` | Same-unit exact comparison requires no unit conversion facility. |
| `PE-X-AC-015` | QB target key uses only the approved QB normalization and exact unit label. |
| `PE-X-AC-016` | The QB aggregate Fraction is preserved as provenance and never used as a bound or product value. |
| `PE-X-AC-017` | A same-target confirmed conflict yields `TARGET_CONFLICT` and profile `UNRESOLVED`. |
| `PE-X-AC-018` | A same-target compatible result permits evaluation but adds no numeric contribution. |
| `PE-X-AC-019` | A conflict on a proven different key does not block the selected target and remains traceable. |
| `PE-X-AC-020` | Target-local unresolved evidence yields `TARGET_UNRESOLVED` rather than pass, failure, or zero. |
| `PE-X-AC-021` | Proven absence of an applicable target comparison yields `TARGET_NOT_APPLICABLE` without blocking. |
| `PE-X-AC-022` | Missing observation yields profile `UNAVAILABLE`, not negative conformance. |
| `PE-X-AC-023` | Unsupported comparator, unit, or context propagates `UNSUPPORTED`. |
| `PE-X-AC-024` | Unresolved identity/context propagates `UNRESOLVED`. |
| `PE-X-AC-025` | No applicable criterion propagates `NOT_APPLICABLE`. |
| `PE-X-AC-026` | Available negative conformance keeps profile status `AVAILABLE`. |
| `PE-X-AC-027` | Multiple criteria or observations are never averaged or selected implicitly. |
| `PE-X-AC-028` | Later dynamic evidence creates a new profile and never mutates an earlier snapshot. |
| `PE-X-AC-029` | Feature/evidence/provenance references retain deterministic source order. |
| `PE-X-AC-030` | All relevant artifact, assessment, snapshot, product, collection, environment, registry, contract, and rule versions are retained. |
| `PE-X-AC-031` | Invalid mixed-version or dangling-reference input fails construction rather than becoming a scientific absence state. |
| `PE-X-AC-032` | The implementation contains no normalization, weighting, rounding, ranking, imputation, or product-quality calculation. |
| `PE-X-AC-033` | Tests can construct source domain objects directly without files, CLI, extractor, telemetry, or test-runner infrastructure. |
| `PE-X-AC-034` | Explanations distinguish artifact-quality context, criterion, observed behavior, QB gate, and conformance. |
| `PE-X-AC-035` | No output claims that `X_PE` is predicted or complete Performance Efficiency. |

## 19. Scientific assumptions, contradictions, and blockers

### 19.1 Explicit assumptions

1. The exact response-time metric, C0 context, `SECOND` unit, and inclusive
   upper-bound comparator are already supported by the referenced contracts.
2. An explicit caller-selected criterion/conformance path identifies the one
   bounded subject; selection among multiple candidates is not delegated to
   this mapper.
3. The QB comparison population and provenance are sufficient to determine
   target-local coverage under Section 8.3. If they are not, the gate is
   `TARGET_UNRESOLVED`.
4. C/V/U remain scientifically useful as audit and requirement-risk context,
   but no approved evidence gives them direct product-quality contribution.
5. The profile is constructed only for the parent-defined
   `REFERENCE_VERIFICATION` process stage.

### 19.2 Apparent tensions resolved by this contract

- The dissertation permits future normalized feature formation; the parent
  contract forbids normalization in v0.1. `X_PE` is therefore a typed feature
  profile, not a normalized vector.
- The parent includes C/V/U and QB in `X_PE`; the dissertation warns that
  requirement quality is not product quality. Role typing resolves the issue:
  C/V/U are context only and QB is only a target gate.
- QB has a specification-level Fraction, while dynamic criteria use Decimal.
  They remain separate numeric domains and are never converted or combined.
- A dynamic conformance may exist while the specification has a same-key QB
  conflict. Both facts are preserved; the feature profile is `UNRESOLVED`
  rather than choosing one target.

No contradiction requiring a new scientific formula was found.

### 19.3 Blocking decision

`FM-D015` remains the sole external blocker: the parent Full Model v0.1
contract requires the recorded approval described in its Approval record.
Until that approval exists, this contract remains a normative candidate and
M3-04 implementation remains blocked. This contract does not invent an
approval state.

## 20. M3-04 readiness

Subject to `FM-D015`, this contract supplies sufficient deterministic inputs
for M3-04: a closed feature registry, exact source-selection rules, typed roles,
target-scoped QB gate, identities, temporal/state propagation, provenance,
versioning, conflict behavior, reference fixtures, and acceptance cases.

M3-04 may implement only the construction and validation of `X_PE`. It must not
implement the product-quality indicator, prediction, calibration, test
execution, telemetry, unit conversion, statistics, or any new extraction rule.
