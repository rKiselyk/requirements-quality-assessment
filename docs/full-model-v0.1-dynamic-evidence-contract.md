# Full Model v0.1 Dynamic Evidence Contract

**Contract ID:** `FULL-MODEL-V0.1-DYNAMIC-EVIDENCE`  
**Contract version:** `1`  
**Milestone issue:** M3-03 / #140  
**Parent contract:** `FULL-MODEL-V0.1-CONTRACT / 1`  
**Related metric contract:** `FULL-MODEL-V0.1-METRIC-PROFILE / 1`  
**Status:** `NORMATIVE_CANDIDATE / PARENT_CONTRACT_APPROVAL_REQUIRED`

## 1. Purpose and authority

This document defines the future Full Model v0.1 dynamic-evidence boundary:

```text
Requirement -> QuantitativeCriterion -> DynamicObservation
            -> ConformanceAssessment
```

It defines domain and service contracts only. It does not implement them.
M3-03 is a deterministic binding and comparison layer over an existing
quantitative requirement observation and an externally supplied controlled
observation. It is not a test runner, telemetry collector, benchmark harness,
measurement platform, statistical procedure, requirement detector, or
product-quality model.

Authority and precedence are:

1. `docs/model-spec.md` for existing quantitative observations, Evidence,
   comparators, exact `Decimal` values, units, and the implemented
   `QUANT-METRIC-001` and `QUANT-CONTEXT-001` contracts;
2. the approved QB-v0.1 contracts for bounded metric/context identity,
   normalization, exact-unit equality, and no-conversion semantics;
3. `docs/full-model-v0.1-contract.md` for the Full Model dynamic-evidence
   scope, canonical statuses, versioning, and downstream boundaries;
4. `docs/full-model-v0.1-metric-profile-contract.md` for shared artifact,
   assessment, rule-reference, and provenance conventions; and
5. this document for the M3-03 representation, binding, and exact conformance
   procedure.

The dissertation files in `docs/reference/` are theoretical and traceability
sources. They do not override an accepted implementation contract. A conflict
with an accepted existing rule must stop implementation and be resolved by a
reviewed amendment.

## 2. Dissertation research basis

### 2.1 Dynamic-evidence model

`docs/reference/3.2_Динамічні_методи.docx` defines dynamic evaluation as
measurable evidence obtained from executable product behavior under stated
conditions. Its general chain is:

```text
r_i -> a_i -> t_k -> o_k -> c_k
```

The source distinguishes:

- `r_i`: the requirement;
- `a_i`: an acceptance or measurable criterion derived from that requirement;
- `t_k`: a test or experimental procedure;
- `o_k`: the observed result; and
- `c_k`: the result of comparing the observation with the criterion.

Table 3.4 further states that the criterion makes the requirement testable,
the observation is primary dynamic evidence, and conformance is the result of
comparing the observation with the criterion. The test or experiment supplies
the procedure, inputs, preconditions, and environment. The observation must
retain its conditions because results from different environments must not be
compared as if they were interchangeable.

The same source establishes four constraints inherited here:

1. the criterion is defined before the observation is evaluated;
2. the criterion comes from the requirement rather than from the observed
   value;
3. absence of dynamic data is not a negative result; and
4. one response-time observation for one scenario is not automatically a full
   assessment of a product-quality characteristic.

The dissertation discusses repeated executions, distributions, coverage,
variability, aggregation, and calibrated normalization as broader work. It
also says that their exact procedure must follow the requirement and be fixed
before result analysis. None of those broader procedures is imported into
Full Model v0.1.

### 2.2 Metric, availability, and quality separation

`docs/reference/2.3_Система_метрик.docx` distinguishes an observed fact, a
measure, and an interpreted indicator. It requires explicit object,
applicability, reproducibility, data source, and semantic context. It also
requires computed, unavailable, and not-applicable states to remain distinct
and forbids replacing unavailable or not-applicable values with zero.

`docs/reference/3.3_Метод_оцінювання.docx` keeps dynamic evidence separate
from the early requirement/static evidence path. Dynamic data is later input
for validation or refinement, and missing dynamic data remains visible through
availability information rather than zero filling.

`docs/reference/4.2_Модель_якості.docx` explicitly separates the quality of a
requirement artifact from the quality of the implemented software product.
It treats product-quality evaluation as a later characteristic-specific
operation over evidence. Therefore a criterion, an observation, and their
conformance result are not themselves a complete product-quality assessment.

### 2.3 Minimum subset adopted for Full Model v0.1

Full Model v0.1 maps only this subset:

```text
existing explicit response-time requirement bound
-> versioned criterion record
-> one externally supplied exact response-time observation
-> categorical exact conformance result
```

The omitted dissertation element `t_k` is represented only by immutable
observation-source, collection, environment, product-version, and sequence
references. M3-03 does not design or execute `t_k`. The broader dynamic
profile components for coverage, repeated observations, variability,
statistics, aggregation, and experimental calibration remain outside M3-03.

This is a bounded operational projection of the dissertation model, not a
claim that the dissertation model contains only one criterion or one
observation.

## 3. Three different scientific objects

The following objects must remain distinct in names, types, identity, values,
statuses, explanations, and reporting.

| Object | Meaning | Subject | What it may claim | What it must not claim |
| --- | --- | --- | --- | --- |
| Requirement criterion | A target explicitly stated by one requirement | versioned requirement artifact | the requirement sets the named bound in the named context | that the product achieved the bound |
| Observed product behavior | A value supplied for one product version under one declared collection and context | versioned executable product | the supplied source recorded the value under the declared conditions | that the requirement conforms or that Performance Efficiency is good |
| Product-quality assessment | A later characteristic-specific interpretation | product-quality characteristic and product version | only what its later model contract authorizes | that it is identical to either the requirement or the raw observation |

`ConformanceAssessment` is the typed relation between the first two objects.
It says whether one observation meets one criterion. It is not the third
object. In particular:

- `CONFORMS` is not a C/V/U score;
- `CONFORMS` is not `M_cons[QB-v0.1]`;
- `CONFORMS` is not a full Performance Efficiency value;
- `DOES_NOT_CONFORM` is not a requirement-quality defect; and
- an unavailable observation is neither `DOES_NOT_CONFORM` nor numeric zero.

M3-04 may package these records as named `X_PE` inputs. M3-05 alone owns the
bounded product-quality result defined by the parent contract.

## 4. Boundary operations

The future conceptual operations are:

```text
bind_quantitative_criterion(
    requirement_source,
    source_observation_ref,
    context,
) -> CriterionBindingResult

resolve_dynamic_observation(
    expected_slot,
    supplied_observation_or_none,
) -> ObservationResolution

assess_conformance(
    criterion_binding,
    observation_resolution,
    context,
) -> ConformanceAssessment
```

Each operation is pure. It must not mutate an input, read a file, invoke a
parser, extract new requirement text, run a product, collect telemetry, perform
a benchmark, format a report, or assess product quality.

`source_observation_ref` is explicit. If a requirement has more than one
quantitative observation, M3-03 does not select one by proximity, value,
position, or perceived meaning.

## 5. Closed v0.1 registry and rule identities

### 5.1 Response-time metric identity

The dynamic metric registry is:

```text
registry_id      = FULL-MODEL-V0.1-DYNAMIC-METRICS
registry_version = 1
```

It contains exactly one entry:

| Ordinal | Metric ID | Meaning | Required source metric identity | Supported criterion unit | Supported criterion comparator |
| ---: | --- | --- | --- | --- | --- |
| 1 | `DYN.RESPONSE_TIME` | elapsed response duration for the exact bounded requirement context | `N("Час відгуку") = "час відгуку"` | `SECOND` | `LESS_THAN_OR_EQUAL / INCLUSIVE` |

`DYN.RESPONSE_TIME` is a measurement identity. It is distinct from:

- `RQ.VERIFIABILITY`, which is a requirement-quality metric;
- `SPEC.QB_CONSISTENCY`, which is bounded specification Consistency;
- `PE.OBS.RESPONSE_TIME`, which is a later M3-04 feature identity; and
- `PERFORMANCE_EFFICIENCY`, which is a product-quality characteristic.

No throughput, percentile, availability, recovery-time, frequency, resource,
or other measurement metric is added by this contract.

### 5.2 Rule identities

The Full Model rules allocated by this contract are:

```text
DYN-CRITERION-RESPONSE-TIME-001 / 1
DYN-CONFORMANCE-RESPONSE-TIME-001 / 1
```

The first binds an existing quantitative source observation to the closed
dynamic metric registry. The second compares one supported criterion and one
supported observation. Neither rule performs requirement extraction.

The registry and rule identities above are independently versioned. The metric
identity names what is measured; the binding and evaluator rules name how
source data is admitted and compared. A rule ID must never be substituted for
the metric ID.

## 6. Supporting identity contracts

The contract reuses the version-qualified concepts established by the parent
and metric-profile contracts and adds only the identities needed by dynamic
evidence:

```text
ArtifactRef(artifact_id, artifact_version)
AssessmentRef(assessment_id, assessment_version, artifact_ref)
RequirementSubjectRef(artifact_ref, requirement_id, source_line)
ContractRef(contract_id, version)
RuleRef(rule_id, explicit_version, version_authority)

ProductRef(product_id, product_version)
EnvironmentRef(environment_id, environment_version)
ObservationCollectionRef(
  collection_id,
  collection_version,
  product_ref,
  environment_ref,
  source_kind,
)
CriterionContextIdentity(normalization_contract_ref, normalized_text)
ObservationSlotRef(collection_ref, fixture_sequence)
CriterionBindingId(
  artifact_ref,
  source_assessment_ref,
  requirement_subject_ref,
  source_snapshot_id,
  source_observation_ref_or_none,
  binding_rule_ref,
)
DynamicEvidenceAssessmentRef(
  assessment_id,
  assessment_version,
  artifact_ref,
  product_ref,
  collection_ref,
)
```

All identifier and version components are non-empty. `fixture_sequence` is a
non-negative integer unique within one collection version. These are immutable
value objects, not display labels.

The source requirement artifact and observed product are different subjects.
`ArtifactRef` never substitutes for `ProductRef`, and a product version is
never inferred from a specification version.

## 7. QuantitativeCriterion

### 7.1 Record shape

`QuantitativeCriterion` is an immutable, source-backed requirement criterion:

```text
QuantitativeCriterion
  criterion_id: CriterionId
  requirement_subject_ref: RequirementSubjectRef
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  source_observation_ref: CrossObservationRef
  metric_ref: DynamicMetricRef
  comparator: ComparatorLabel
  inclusivity: BoundaryInclusivity
  bound: Decimal
  unit: UnitLabel
  context_identity: CriterionContextIdentity
  provenance: CriterionProvenance
  binding_rule_ref: RuleRef
```

The record preserves a requirement-defined target. Its `bound` is not a
measured product value and not an invented Full Model threshold.

The `DynamicMetricRef` is exactly:

```text
(
  FULL-MODEL-V0.1-DYNAMIC-METRICS,
  1,
  DYN.RESPONSE_TIME,
  QB-NORMALIZATION / 1,
  "час відгуку",
)
```

### 7.2 Criterion identity

No hash is required. The exact structured identity is:

```text
CriterionId = (
  artifact_ref,
  source_assessment_ref,
  requirement_subject_ref,
  source_snapshot_id,
  source_observation_ref,
  binding_rule_ref,
)
```

The identity names the source assessment of one observation in one versioned
requirement. The bound, comparator, unit, context, metric, or provenance cannot
change under the same `CriterionId`. A changed requirement artifact or a
genuine reassessment produces a different identity.

`requirement_id` alone is insufficient. Generated IDs such as `R001` are local
to one artifact version and carry no cross-version lineage meaning.

### 7.3 Source binding

The supported reference criterion must come from one existing
`QuantitativeConstraintObservation` and its matching snapshot projection. The
binding rule copies, without reparsing:

- metric identity from the accepted `QUANT-METRIC-001` component Evidence;
- comparator and inclusivity from the accepted scalar observation;
- the exact `Decimal` bound;
- the exact `UnitLabel`;
- context identity from accepted `QUANT-CONTEXT-001` component Evidence; and
- every component and top-level Evidence reference.

The exact supported source requirement is the accepted C0 construction:

```text
Час відгуку ≤ 2 с при 500 одночасних користувачах
```

The value may vary only where the existing `QUANT-METRIC-001` contract already
allows it. This contract does not broaden its grammar. The dynamic binding
still requires the exact implemented C0 context and the other support gates in
this document.

## 8. CriterionBindingResult

Criterion discovery and support are explicit rather than encoded through a
partially populated `QuantitativeCriterion`:

```text
CriterionBindingResult
  binding_id: CriterionBindingId
  status: FullModelStatus
  applicability: Applicability
  criterion: QuantitativeCriterion | None
  source_observation_ref: CrossObservationRef | None
  reasons: tuple[DynamicEvidenceReason, ...]
  provenance: CriterionBindingProvenance
```

Allowed states are:

| Condition | Status | Applicability | Criterion |
| --- | --- | --- | --- |
| Exact supported response-time criterion | `AVAILABLE` | `APPLICABLE` | present |
| Requirement has no applicable response-time criterion after complete source processing, or has a resolved different metric | `NOT_APPLICABLE` | `NOT_APPLICABLE` | absent |
| Source assessment needed for binding has not been produced at the stated stage/version | `UNAVAILABLE` | `UNKNOWN` | absent |
| Metric identity is missing/unresolved | `UNRESOLVED` | `UNKNOWN` | absent |
| Response-time comparator, unit, or context identity is missing/unresolved | `UNRESOLVED` | `APPLICABLE` | absent |
| Response-time criterion is resolved but uses an unsupported comparator, unit, or context | `UNSUPPORTED` | `APPLICABLE` | may be preserved as a fully resolved criterion record, but is not evaluator-ready |

`UNKNOWN` is not produced by the v0.1 binding rule because no approved dynamic
source maps to that meaning. It remains part of the parent taxonomy and must
not be substituted for `UNRESOLVED`, `UNAVAILABLE`, or `NOT_APPLICABLE`.

A missing selected source reference when several quantitative observations
exist is `UNRESOLVED`; M3-03 does not guess which criterion was intended.

`CriterionBindingId` exists in every state, including when no successful
`CriterionId` can be formed. `source_observation_ref_or_none` is the explicit
selected reference when one was supplied and `None` when selection itself is
unresolved or the requirement has no applicable response-time observation.
This gives later unavailable, unresolved, unsupported, and not-applicable
assessments a deterministic source anchor without fabricating a criterion.

## 9. DynamicObservation

### 9.1 Record shape

`DynamicObservation` is immutable primary dynamic evidence about one product
version:

```text
DynamicObservation
  observation_id: DynamicObservationId
  slot_ref: ObservationSlotRef
  product_ref: ProductRef
  metric_ref: DynamicMetricRef
  observed_value: Decimal
  unit: UnitLabel
  context_identity: CriterionContextIdentity
  source_kind: ObservationSourceKind
  collection_ref: ObservationCollectionRef
  fixture_sequence: int
  collected_at: None
  provenance: DynamicObservationProvenance
```

For Full Model v0.1, `ObservationSourceKind` contains exactly:

```text
DETERMINISTIC_FIXTURE
```

This does not claim that the fixture was collected by a real benchmark or
production telemetry system. It provides the controlled provider boundary
required to test the scientific flow without implementing collection
infrastructure.

### 9.2 Observation identity

The exact structured identity is:

```text
DynamicObservationId = (
  collection_ref,
  fixture_sequence,
)
```

`ObservationSlotRef` names a possibly empty position in one versioned
collection. It is deliberately criterion-independent. The criterion-to-slot
binding belongs to `ConformanceAssessment`, whose identity contains both the
criterion binding and the observation slot. This preserves the dissertation's
separation between a requirement criterion and observed product behavior and
allows the same immutable observation to be reconsidered after a specification
revision when the process contract's exact reuse checks succeed.

The slot remains a separate type from `DynamicObservationId` so that an absent
observation can be referenced without fabricating an observation. The
observation's product, metric, value, unit, context, source, environment, or
provenance cannot change under the same ID. Changing any of them requires a new
collection version or collection ID.

### 9.3 Observed value versus criterion bound

`observed_value` is the recorded product behavior. It is not copied from the
criterion and is not derived from any C/V/U or QB value. Constructor or
provider logic must reject a fixture that aliases the criterion object as a
substitute for an independently supplied observation.

The contract does not assert that one fixture value is statistically
representative. It defines only the exact record that the later bounded
reference path consumes.

## 10. ObservationResolution and unavailable observations

Absence is represented without manufacturing a `DynamicObservation`:

```text
ObservationResolution
  slot_ref: ObservationSlotRef
  status: FullModelStatus
  applicability: Applicability
  observation: DynamicObservation | None
  reasons: tuple[DynamicEvidenceReason, ...]
  provenance_refs: tuple[ProvenanceRef, ...]
```

The exact mappings are:

| Condition | Status | Applicability | Observation |
| --- | --- | --- | --- |
| Structurally valid supplied fixture | `AVAILABLE` | `APPLICABLE` | present |
| No observation exists for an applicable supported criterion and declared slot | `UNAVAILABLE` | `APPLICABLE` | absent |
| A candidate record exists but its metric, context, source, collection, product, or slot identity cannot be resolved | `UNRESOLVED` | `UNKNOWN` | absent |
| A resolved source kind or numeric representation lies outside this contract | `UNSUPPORTED` | `APPLICABLE` | absent |
| Criterion binding is `NOT_APPLICABLE` | `NOT_APPLICABLE` | `NOT_APPLICABLE` | absent |

`UNAVAILABLE` means only that an observation was not supplied for the stated
collection and stage. It is not `DOES_NOT_CONFORM`, failure, zero, timeout, or
evidence that the product violated the requirement.

## 11. ConformanceAssessment

### 11.1 Record shape

```text
ConformanceAssessment
  conformance_id: ConformanceAssessmentId
  dynamic_assessment_ref: DynamicEvidenceAssessmentRef
  criterion_binding_id: CriterionBindingId
  criterion_id: CriterionId | None
  observation_slot_ref: ObservationSlotRef | None
  observation_id: DynamicObservationId | None
  status: FullModelStatus
  applicability: Applicability
  outcome: ConformanceOutcome | None
  explanation: str
  reasons: tuple[DynamicEvidenceReason, ...]
  criterion_ref: CriterionRef | None
  observation_ref: DynamicObservationRef | None
  evidence_refs: tuple[EvidenceRef, ...]
  provenance: ConformanceProvenance
  evaluator_rule_ref: RuleRef
```

The closed outcome set is:

```text
CONFORMS
DOES_NOT_CONFORM
```

Both outcomes have `status=AVAILABLE` and `applicability=APPLICABLE`.
Every non-`AVAILABLE` assessment has `outcome=None`. The assessment contains
no numeric conformance value. The later M3-05 product-quality contract owns
any approved mapping from outcome to its bounded exact `{0,1}` indicator.

### 11.2 Conformance identity

```text
ConformanceAssessmentId = (
  dynamic_assessment_ref,
  criterion_binding_id,
  observation_slot_ref_or_none,
  evaluator_rule_ref,
)
```

The slot, rather than a fabricated observation ID, keeps an unavailable result
stable and traceable. When an observation exists, its ID must match the slot.

## 12. Exact comparator semantics

The sole evaluator-ready comparator is:

```text
ComparatorLabel.LESS_THAN_OR_EQUAL
BoundaryInclusivity.INCLUSIVE
```

For a criterion bound `b` and observed value `o`, both exact `Decimal` values:

```text
o <= b  -> CONFORMS
o >  b  -> DOES_NOT_CONFORM
```

Equality conforms. No tolerance, epsilon, uncertainty interval, grace margin,
rounding window, percentile, mean, median, or other statistical rule is
introduced.

Comparator disposition is exact:

| Criterion comparator state | Disposition |
| --- | --- |
| `LESS_THAN_OR_EQUAL / INCLUSIVE` | supported |
| missing comparator or explicitly unresolved comparator component | `UNRESOLVED` |
| `UPPER_BOUND / UNRESOLVED` | `UNRESOLVED`; inclusivity is not guessed |
| `GREATER_THAN_OR_EQUAL / INCLUSIVE` | `UNSUPPORTED` for this Full Model path |
| `NOT_LESS_FREQUENT` | `UNSUPPORTED` |
| a comparator/inclusivity shape invalid under the existing domain contract | invalid input; construction fails |

QB-v0.1 support for an inclusive lower bound does not expand the parent Full
Model dynamic path, which is explicitly fixed to response time `<=`.

## 13. Exact numeric representation

Criterion bounds and observed values are `decimal.Decimal`. They are never
converted through binary floating point, `Fraction`, integer truncation,
percentage, formatted display text, or a normalized `[0,1]` scale.

The exact source criterion `Decimal` object is preserved. The exact supplied
observation `Decimal` object is preserved. Serialization must round-trip the
complete Decimal tuple:

```text
{
  "kind": "DECIMAL",
  "sign": 0 | 1,
  "digits": [digit, ...],
  "exponent": integer
}
```

This preserves representational distinctions such as `Decimal("2")` and
`Decimal("2.00")`. The comparison itself uses exact Decimal numerical ordering,
under which those two values are equal.

Only finite Decimal operands are evaluator-ready. `NaN`, signaling NaN,
positive infinity, and negative infinity are unsupported numeric values. This
is a representability requirement, not an invented response-time threshold.
No minimum value, including an implicit zero lower bound, is introduced by
this contract.

## 14. Unit semantics

The criterion and observation each preserve an existing `UnitLabel`. The sole
evaluator-ready unit is:

```text
UnitLabel.SECOND
```

The evaluator requires exact enum identity:

```text
criterion.unit is SECOND
observation.unit is SECOND
```

No unit conversion is performed. `MINUTE` is not converted to `SECOND`, even
when the numerical conversion might appear obvious. `PERCENT` is not a
duration. Unit aliases, compound units, dimensional analysis, and inferred
units are outside v0.1.

Disposition is:

- missing or unresolved source unit: `UNRESOLVED`;
- resolved criterion unit other than `SECOND`: `UNSUPPORTED`;
- resolved observation unit different from the supported criterion unit:
  conformance `UNSUPPORTED`; and
- an invalid non-`UnitLabel` value: invalid input.

## 15. Context identity

### 15.1 Bounded normalization

Context identity reuses, without extension, the approved QB normalization
contract `QB-NORMALIZATION / 1`:

1. Unicode NFC normalization;
2. Unicode case folding;
3. replacement of every Unicode-whitespace run by one ASCII space; and
4. trimming leading and trailing whitespace.

Every other character, including punctuation, remains significant. There is
no stemming, lemmatization, synonymy, ontology, fuzzy matching, context
overlap, or domain inference.

### 15.2 Supported reference context

The sole supported criterion context is the accepted
`QUANT-CONTEXT-001` C0 source component:

```text
source text:     при 500 одночасних користувачах
normalized text: при 500 одночасних користувачах
```

The `CriterionContextIdentity` is:

```text
(QB-NORMALIZATION / 1, "при 500 одночасних користувачах")
```

The source context must be backed by its own `QUANT-CONTEXT-001` Evidence.
Matching text without the accepted source component and provenance is
insufficient to bind the criterion.

### 15.3 Criterion-observation matching

The observation provider declares a `CriterionContextIdentity`. Evaluation
requires exact identity equality with the criterion. A resolved different
context is `UNSUPPORTED`; the evaluator does not decide whether two contexts
overlap or whether one is stricter. A missing, dangling, or unresolved context
identity is `UNRESOLVED`.

The normalized textual identity is only the requirement-facing measurement
context. `EnvironmentRef` separately records the controlled collection
environment. This contract does not infer that two environment versions are
equivalent, nor does it translate an environment description into a
requirement context.

## 16. Observation source and collection identity

The bounded source is `DETERMINISTIC_FIXTURE`. An observation collection must
name:

- stable `collection_id` and immutable `collection_version`;
- exact `ProductRef`;
- exact `EnvironmentRef`;
- source kind;
- an ordered set of non-negative, collection-local fixture sequences; and
- the source record or fixture provenance for every sequence.

The collection is an external input. M3-03 does not create, run, discover, or
schedule it. For this source kind:

- `fixture_sequence` is required;
- `collected_at` is `None`;
- ordering is ascending `fixture_sequence` within the collection;
- the same sequence cannot identify two observations; and
- changing collection content requires a new collection version.

A later timestamped measurement source requires a new reviewed source-kind
contract. M3-03 must not relabel telemetry, a benchmark, a manual assertion, or
a test-runner result as `DETERMINISTIC_FIXTURE` merely to bypass that gate.

## 17. Evidence and provenance

### 17.1 CriterionProvenance

```text
CriterionProvenance
  requirement_subject_ref
  source_assessment_ref
  source_snapshot_id
  source_observation_ref
  source_processing_status
  source_component_refs
  evidence_refs
  diagnostic_refs
  source_rule_refs
  normalization_contract_ref
  binding_rule_ref
```

It preserves separately the metric, comparator/value/unit, and context
Evidence references. It also preserves the top-level source observation
Evidence order and any source diagnostic references. Evidence is referenced,
not copied or reallocated.

The exact C0 source can be globally `INCOMPLETE / DETECTED` because the embedded
`500` diagnostic remains present. This does not contradict an available
criterion: the accepted `QUANT-CONTEXT-001` contract establishes that the
complete phrase is context while preserving the diagnostic. M3-03 neither
suppresses the diagnostic nor turns it into a second observation.

### 17.2 DynamicObservationProvenance

```text
DynamicObservationProvenance
  product_ref
  source_kind
  collection_ref
  environment_ref
  fixture_sequence
  source_record_ref
  declared_metric_ref
  declared_unit
  declared_context_identity
  numeric_representation
```

The provenance says what the external provider supplied. It does not certify
the provider's empirical validity, repeatability, or statistical
representativeness.

### 17.3 ConformanceProvenance

```text
ConformanceProvenance
  criterion_ref
  observation_ref_or_slot_ref
  direct_criterion_evidence_refs
  dynamic_observation_provenance_ref
  evaluator_rule_ref
  dynamic_contract_ref
  full_model_contract_ref
  exact_operands_or_absence_reason
```

For an available result, `exact_operands_or_absence_reason` preserves the
criterion comparator, inclusivity, bound, unit, and context plus the observed
value, unit, and context. For a non-value result it preserves typed reasons,
not fabricated operands.

Every reference must resolve within the stated artifact, source assessment,
product, collection, and dynamic assessment versions. Dangling or cross-version
references fail closed.

## 18. Availability, applicability, and status semantics

### 18.1 Orthogonal dimensions

The contract uses the parent Full Model statuses:

- `AVAILABLE`;
- `UNAVAILABLE`;
- `UNKNOWN`;
- `UNRESOLVED`;
- `UNSUPPORTED`; and
- `NOT_APPLICABLE`.

Applicability remains orthogonal:

- `APPLICABLE`;
- `UNKNOWN`; and
- `NOT_APPLICABLE`.

`ConformanceOutcome` is a third dimension and is present only for an
`AVAILABLE/APPLICABLE` conformance assessment.

### 18.2 Allowed conformance combinations

| Status | Allowed applicability | Outcome |
| --- | --- | --- |
| `AVAILABLE` | `APPLICABLE` | exactly one of `CONFORMS`, `DOES_NOT_CONFORM` |
| `UNAVAILABLE` | `APPLICABLE` | `None` |
| `UNKNOWN` | `APPLICABLE` or `UNKNOWN` | `None` |
| `UNRESOLVED` | `APPLICABLE` or `UNKNOWN` | `None` |
| `UNSUPPORTED` | `APPLICABLE` or `UNKNOWN` | `None` |
| `NOT_APPLICABLE` | `NOT_APPLICABLE` | `None` |

The v0.1 evaluator does not originate `UNKNOWN`. If a future approved upstream
source supplies `UNKNOWN`, it may be preserved but must not be reinterpreted as
another state.

### 18.3 Deterministic precedence

The evaluator applies this order:

1. reject internally contradictory identities or content as invalid input;
2. propagate criterion `NOT_APPLICABLE`, `UNAVAILABLE`, `UNKNOWN`,
   `UNRESOLVED`, or `UNSUPPORTED` without inspecting an observation value;
3. for an available criterion, propagate observation `UNAVAILABLE`, `UNKNOWN`,
   `UNRESOLVED`, or `UNSUPPORTED`;
4. require equal metric identity, exact `SECOND`, and exact context identity;
5. preserve any resolved but unsupported unit/context case as `UNSUPPORTED`;
6. compare exact finite Decimal operands; and
7. return one available categorical outcome.

This precedence prevents a missing observation from masking an unsupported
criterion and prevents an observed number from bypassing an unresolved
identity.

## 19. Positive and negative conformance

### 19.1 Positive conformance

Positive conformance requires all of the following:

1. criterion binding is `AVAILABLE/APPLICABLE`;
2. observation resolution is `AVAILABLE/APPLICABLE`;
3. both use `DYN.RESPONSE_TIME`;
4. both use exact `UnitLabel.SECOND`;
5. both carry the same supported `CriterionContextIdentity`;
6. both exact Decimal operands are finite;
7. all provenance and version references resolve; and
8. `observed_value <= criterion.bound`.

The result is:

```text
status        = AVAILABLE
applicability = APPLICABLE
outcome       = CONFORMS
```

### 19.2 Negative conformance

Negative conformance requires the same eight gates except that:

```text
observed_value > criterion.bound
```

The result is:

```text
status        = AVAILABLE
applicability = APPLICABLE
outcome       = DOES_NOT_CONFORM
```

Negative conformance is observed failure of this one criterion under this one
declared collection/context. It is not a C/V/U penalty, QB conflict, risk,
corrective action, or full product-quality classification.

## 20. Unavailable, unresolved, and unsupported cases

### 20.1 Unavailable observation

When the criterion is supported but no observation is supplied for the exact
slot:

```text
status        = UNAVAILABLE
applicability = APPLICABLE
outcome       = None
reason        = OBSERVATION_NOT_COLLECTED
```

No observation ID or value is fabricated. The collection, criterion, and slot
remain referenced.

### 20.2 Unresolved identity or context

`UNRESOLVED` applies when a required identity cannot be established, including:

- missing or explicitly unresolved source metric identity;
- missing selected observation reference when several source observations
  exist;
- missing or unresolved source context;
- dangling criterion Evidence;
- missing observation context identity;
- unresolved product, collection, environment, or slot identity; or
- a provenance continuity failure that is not an internally contradictory
  object requiring rejection.

Applicability is `UNKNOWN` when metric or observation association cannot be
established. It is `APPLICABLE` when response-time relevance is known but a
required comparator, unit, or context component remains unresolved.

### 20.3 Unsupported comparator, unit, or context

`UNSUPPORTED` applies only when the relevant component is present and resolved
but lies outside the closed evaluator:

- response-time comparator is resolved but not `LESS_THAN_OR_EQUAL`;
- response-time criterion unit is resolved but not `SECOND`;
- observation unit cannot be matched by exact `SECOND` equality;
- criterion or observation context is resolved but not the supported exact C0
  context;
- criterion and observation contexts are both resolved but unequal; or
- the source or numeric representation is resolved but outside this contract.

`UNSUPPORTED` never means pass. It never invokes conversion, inferred context
overlap, or fallback comparison.

### 20.4 Typed reasons

The minimum closed reason set is:

```text
NO_APPLICABLE_RESPONSE_TIME_CRITERION
SOURCE_ASSESSMENT_UNAVAILABLE
SOURCE_OBSERVATION_SELECTION_UNRESOLVED
METRIC_IDENTITY_UNRESOLVED
COMPARATOR_UNRESOLVED
UNIT_UNRESOLVED
CONTEXT_IDENTITY_UNRESOLVED
PROVENANCE_UNRESOLVED
COMPARATOR_UNSUPPORTED
UNIT_UNSUPPORTED
CONTEXT_UNSUPPORTED
OBSERVATION_NOT_COLLECTED
OBSERVATION_IDENTITY_UNRESOLVED
OBSERVATION_SOURCE_UNRESOLVED
OBSERVATION_NUMERIC_UNSUPPORTED
```

Reasons are explanatory classifications, not severities or scores.

## 21. Version semantics

Every criterion, observation, and conformance assessment preserves all
versions that affect its meaning:

- specification `artifact_id/artifact_version`;
- source `assessment_id/assessment_version`;
- source QB snapshot identity;
- product `product_id/product_version`;
- collection `collection_id/collection_version`;
- environment `environment_id/environment_version`;
- dynamic assessment `assessment_id/assessment_version`;
- Full Model, dynamic registry, and dynamic contract versions;
- binding and evaluator rule versions;
- QB normalization contract version; and
- existing extraction rule authorities and explicit versions where they
  already exist.

`QUANT-001`, `QUANT-METRIC-001`, and `QUANT-CONTEXT-001` retain their existing
stable-rule version authority. This contract must not invent a separate
version string for a source rule whose accepted contract does not define one.

A semantic change to criterion binding or evaluation requires a new rule
version or rule ID and a reviewed dynamic contract version. A changed bound,
context, requirement text, or source assessment requires a new criterion
identity. A changed product, environment, value, context, or collection record
requires a new observation identity. A new evaluation event requires a new
dynamic assessment reference.

Reporter formatting, including display of Decimal values, does not change
scientific identity. Reusing evidence across versions is allowed only under
the parent contract's explicit validity and provenance rules.

## 22. Determinism, ordering, and lossless construction

For identical immutable inputs and versions, all IDs, states, reasons,
outcomes, and ordered references are identical.

Deterministic ordering is:

1. criteria by source requirement order, then source quantitative observation
   index;
2. collections by explicit caller order when more than one collection is
   supplied;
3. observations within one collection by ascending `fixture_sequence`; and
4. conformance assessments by criterion order, then observation slot order.

No sorting by value, conformance outcome, status, requirement text, metric
label, or evidence count is permitted.

Criterion construction is lossless:

- source comparator, inclusivity, Decimal bound, UnitLabel, and component
  Evidence are copied or referenced exactly;
- normalized metric/context identity is derived only with
  `QB-NORMALIZATION / 1`;
- original Evidence text and offsets remain unchanged; and
- diagnostics and source processing status remain visible.

Observation construction is lossless:

- the exact supplied Decimal tuple is preserved;
- the declared UnitLabel and context identity are preserved;
- product, environment, source, collection, and sequence identity are
  preserved; and
- no criterion value is inserted as an observation default.

Conformance construction preserves both exact operands and returns only the
classification authorized by Section 12.

## 23. Invariants and forbidden transformations

The future domain constructors and services must enforce:

1. all successful records are immutable;
2. each identity matches its record content and version references;
3. a criterion resolves to exactly one requirement and one source observation;
4. criterion Evidence resolves to the unchanged source requirement text and
   exact spans;
5. `DYN.RESPONSE_TIME` maps only from the approved bounded metric identity;
6. the evaluator-ready criterion is exact `<=`, `SECOND`, and exact C0 context;
7. every available observation has one product, collection, environment,
   sequence, exact Decimal value, UnitLabel, and context identity;
8. when an observation exists, the conformance assessment's observation slot
   equals `observation.slot_ref`, and the assessment records the criterion
   binding separately;
9. an available conformance result has exactly one outcome;
10. every other conformance status has `outcome=None`;
11. all reference collections are deterministic and source ordered; and
12. source diagnostics and rule provenance are not suppressed.

Forbidden transformations include:

- extracting or reparsing requirement text in M3-03;
- adding a new detector, grammar, metric vocabulary, or context grammar;
- selecting a criterion automatically from competing observations;
- inventing or changing a requirement threshold;
- replacing the requirement bound with an observed value;
- converting `Decimal` through `float` or `Fraction`;
- rounding, quantizing, averaging, normalizing, weighting, or applying a
  tolerance;
- converting units or inferring unit aliases;
- inferring context equivalence or overlap beyond exact normalized identity;
- treating missing observation as `DOES_NOT_CONFORM`, zero, or pass;
- converting `UNRESOLVED`, `UNAVAILABLE`, `UNSUPPORTED`, `UNKNOWN`, or
  `NOT_APPLICABLE` into an outcome;
- converting conformance into C/V/U or QB Consistency;
- assigning a scalar overall requirement-quality value;
- emitting a product-quality score or prediction;
- claiming full Performance Efficiency from one observation;
- suppressing the exact C0 embedded-`500` diagnostic;
- treating fixture data as proof of telemetry or benchmark execution; and
- placing collection, assessment, aggregation, or reporting logic in the
  evaluator.

## 24. Deterministic reference fixtures

These fixtures define future domain/service tests. They do not add extraction
coverage and do not require a test runner.

### 24.1 Shared criterion source

```text
artifact_ref          = (SPEC-DYN-REF, 1)
source_assessment_ref = (ASSESS-DYN-SOURCE, 1, artifact_ref)
requirement           = R001, source line 1
requirement text      = Час відгуку ≤ 2 с при 500 одночасних користувачах
source observation    = quantitative observation index 0
metric                = Час відгуку [0,11), QUANT-METRIC-001:E001
scalar                = ≤ 2 с [12,17), QUANT-001:E001
context               = при 500 одночасних користувачах [18,49),
                        QUANT-CONTEXT-001:E001
preserved diagnostic  = 500 [22,25), QUANT-001,
                        QUANT_UNRESOLVED_NUMERIC_CANDIDATE
comparator            = LESS_THAN_OR_EQUAL / INCLUSIVE
bound                 = Decimal("2")
unit                  = SECOND
context identity      = (QB-NORMALIZATION/1,
                         "при 500 одночасних користувачах")
metric identity       = DYN.RESPONSE_TIME
binding result        = AVAILABLE / APPLICABLE
```

The preserved extraction outcome may remain `INCOMPLETE / DETECTED`. The
criterion is still available because all required criterion components are
accepted and the exact context rule fixes the role of the embedded `500`.

### 24.2 Shared collection

```text
product_ref     = (PRODUCT-DYN-REF, 1)
environment_ref = (ENV-DYN-REF, 1)
collection_ref  = (
  DYN-REF-COLLECTION,
  1,
  product_ref,
  environment_ref,
  DETERMINISTIC_FIXTURE,
)
dynamic assessment = (ASSESS-DYN-CONFORMANCE, 1,
                      artifact_ref, product_ref, collection_ref)
```

### 24.3 Fixture outcomes

| Fixture | Sequence | Observation | Expected result |
| --- | ---: | --- | --- |
| `DYN-RF-001` | 0 | `Decimal("1.5")`, `SECOND`, exact shared context | `AVAILABLE/APPLICABLE/CONFORMS` |
| `DYN-RF-002` | 1 | `Decimal("2.00")`, `SECOND`, exact shared context | `AVAILABLE/APPLICABLE/CONFORMS`; Decimal tuple preserved |
| `DYN-RF-003` | 2 | `Decimal("2.01")`, `SECOND`, exact shared context | `AVAILABLE/APPLICABLE/DOES_NOT_CONFORM` |
| `DYN-RF-004` | 3 | no observation supplied for declared slot | `UNAVAILABLE/APPLICABLE/None` |
| `DYN-RF-005` | 4 | `Decimal("1")`, `MINUTE`, exact shared context | conformance `UNSUPPORTED/APPLICABLE/None`; no conversion |
| `DYN-RF-006` | 5 | `Decimal("1.5")`, `SECOND`, resolved context `під час пікового навантаження` | conformance `UNSUPPORTED/APPLICABLE/None`; no context overlap |
| `DYN-RF-007` | 6 | candidate value/unit present but observation context identity unresolved | `UNRESOLVED/UNKNOWN/None` |
| `DYN-RF-008` | 7 | non-finite Decimal | `UNSUPPORTED/APPLICABLE/None` |

### 24.4 Criterion-state fixtures

| Fixture | Source criterion condition | Expected binding/conformance disposition |
| --- | --- | --- |
| `DYN-RF-009` | response time `UPPER_BOUND / UNRESOLVED` | `UNRESOLVED/APPLICABLE`; no comparison |
| `DYN-RF-010` | response time `GREATER_THAN_OR_EQUAL / INCLUSIVE` | `UNSUPPORTED/APPLICABLE`; no comparison |
| `DYN-RF-011` | response time `<=` in `MINUTE` | `UNSUPPORTED/APPLICABLE`; no conversion |
| `DYN-RF-012` | response time `<= SECOND` with missing context | `UNRESOLVED/APPLICABLE` |
| `DYN-RF-013` | resolved metric other than response time | `NOT_APPLICABLE/NOT_APPLICABLE` |
| `DYN-RF-014` | two candidate source observations with no explicit selected ref | `UNRESOLVED`; no automatic choice |

## 25. Acceptance cases for future M3-03 implementation

| Case | Required assertion |
| --- | --- |
| `DE-AC-001` | The exact C0 source observation binds to one immutable `QuantitativeCriterion`. |
| `DE-AC-002` | Binding copies the exact source `Decimal`, comparator, inclusivity, UnitLabel, and all component Evidence references. |
| `DE-AC-003` | Binding performs no raw-text parsing and accepts an explicitly referenced existing source observation only. |
| `DE-AC-004` | `DYN.RESPONSE_TIME` is distinct from requirement-quality, QB, feature, and product-quality identities. |
| `DE-AC-005` | Criterion identity is deterministic and changes with artifact, source assessment, snapshot, observation, or binding-rule version. |
| `DE-AC-006` | Generated requirement IDs are qualified by artifact version and are not treated as lineage IDs. |
| `DE-AC-007` | Missing metric identity yields `UNRESOLVED/UNKNOWN`, not NOT_APPLICABLE or zero. |
| `DE-AC-008` | A resolved different metric yields `NOT_APPLICABLE/NOT_APPLICABLE`. |
| `DE-AC-009` | `UPPER_BOUND / UNRESOLVED` yields `UNRESOLVED`; inclusivity is not guessed. |
| `DE-AC-010` | Resolved `GREATER_THAN_OR_EQUAL` and `NOT_LESS_FREQUENT` criteria are `UNSUPPORTED` for this path. |
| `DE-AC-011` | Missing criterion unit or context is `UNRESOLVED`. |
| `DE-AC-012` | Resolved non-SECOND criterion unit or non-C0 context is `UNSUPPORTED`. |
| `DE-AC-013` | Multiple source observations without an explicit selected source ref yield `UNRESOLVED`. |
| `DE-AC-014` | The exact C0 embedded-500 diagnostic and global source processing state remain in provenance. |
| `DE-AC-015` | Observation identity is deterministic from collection version and fixture sequence. |
| `DE-AC-016` | A collection version cannot contain duplicate fixture sequences. |
| `DE-AC-017` | A changed observation value, unit, context, product, environment, or source record under the same identity is rejected. |
| `DE-AC-018` | The exact observation Decimal tuple round-trips without float conversion or quantization. |
| `DE-AC-019` | Non-finite Decimal observations are unsupported and never reach the comparator. |
| `DE-AC-020` | Exact metric, SECOND, and context equality are required before comparison. |
| `DE-AC-021` | Observation below the requirement's own bound produces `CONFORMS`. |
| `DE-AC-022` | Observation exactly equal to the bound produces `CONFORMS`. |
| `DE-AC-023` | Observation above the bound produces `DOES_NOT_CONFORM`. |
| `DE-AC-024` | Comparator operands remain Decimal; no Fraction, float, rounding, or tolerance is introduced. |
| `DE-AC-025` | Missing observation produces `UNAVAILABLE/APPLICABLE/None`. |
| `DE-AC-026` | Missing observation never produces `DOES_NOT_CONFORM`, zero, or a synthetic observation ID. |
| `DE-AC-027` | SECOND versus MINUTE produces `UNSUPPORTED` and performs no conversion. |
| `DE-AC-028` | Two resolved unequal contexts produce `UNSUPPORTED` and perform no overlap inference. |
| `DE-AC-029` | Missing or dangling observation context identity produces `UNRESOLVED`. |
| `DE-AC-030` | Criterion `NOT_APPLICABLE` propagates without inspecting an observation value. |
| `DE-AC-031` | Criterion `UNSUPPORTED` takes precedence over an absent observation. |
| `DE-AC-032` | Every available conformance assessment has exactly one categorical outcome and no numeric value. |
| `DE-AC-033` | Every non-available conformance assessment has `outcome=None`. |
| `DE-AC-034` | `CONFORMS` and `DOES_NOT_CONFORM` are both available results and remain distinct from canonical statuses. |
| `DE-AC-035` | Criterion, observation, and conformance provenance resolve across the exact stated artifact, product, collection, and assessment versions. |
| `DE-AC-036` | Dangling or incompatible cross-version provenance fails closed and is not repaired by reporting. |
| `DE-AC-037` | The evaluator is pure and leaves criterion, observation, collection, and source assessment unchanged. |
| `DE-AC-038` | No type or service exposes unit conversion, normalization, weighting, statistics, prediction, or product-quality scoring. |
| `DE-AC-039` | Criteria and assessments retain source order; observations retain collection sequence order. |
| `DE-AC-040` | Identical immutable inputs produce identical structured IDs, reasons, status, applicability, outcome, and ordered provenance. |
| `DE-AC-041` | An observation slot and observation identity are criterion-independent; a conformance assessment, not the observation, binds the criterion to the slot. |
| `DE-AC-042` | An approved upstream `UNKNOWN` criterion or observation propagates as `UNKNOWN` with no outcome and no numeric value. |

Acceptance tests must use manually constructed domain values and existing
quantitative source objects. They must not require CLI orchestration, files,
an NLP parser, a test runner for an external product, telemetry, benchmarking,
or a reporter.

## 26. Scientific assumptions and bounded operational decisions

| ID | Decision | Classification | Blocking? |
| --- | --- | --- | --- |
| `DE-D001` | Adopt only the dissertation's criterion-observation-conformance spine; omit execution infrastructure, coverage, repeated measures, variability, aggregation, and calibration. | `BOUNDED_V0.1_DECISION` | No |
| `DE-D002` | The dynamic registry contains only `DYN.RESPONSE_TIME`. | inherited `FM-D001` and `FM-D004` | No |
| `DE-D003` | Bind response time only from the existing accepted quantitative observation and exact C0 context; do not parse text. | `EXISTING_APPROVED` plus bounded binding | No |
| `DE-D004` | Reuse `QB-NORMALIZATION / 1` for metric/context textual identity only. | `EXISTING_APPROVED` | No |
| `DE-D005` | Evaluator support is exactly `<= / INCLUSIVE`, `SECOND`, and exact C0 context. | inherited `FM-D004` | No |
| `DE-D006` | Criterion and observation operands remain exact finite Decimal; no tolerance or numeric normalization. | `EXISTING_APPROVED` plus representability guard | No |
| `DE-D007` | The only v0.1 source kind is `DETERMINISTIC_FIXTURE`; product, environment, collection version, and sequence make the controlled source explicit. | `BOUNDED_V0.1_DECISION` | No |
| `DE-D008` | Conformance is categorical; numeric `{0,1}` mapping remains owned by the later product-quality contract. | inherited Full Model boundary | No |
| `DE-D009` | Resolved but unequal unit/context is `UNSUPPORTED`; missing/unresolved identity is `UNRESOLVED`; missing observation is `UNAVAILABLE`. | `BOUNDED_V0.1_DECISION` consistent with parent taxonomy | No |
| `DE-D010` | A resolved non-response-time criterion is `NOT_APPLICABLE` to this closed dynamic family. | `BOUNDED_V0.1_DECISION` | No |
| `DE-D011` | The collection environment is provenance, while exact normalized requirement context is the comparison identity. No equivalence is inferred between either representation. | dissertation-derived separation plus bounded identity | No |
| `DE-D012` | M3-03 may consume the supported quantitative criterion directly and does not depend on a completed `MetricProfile`. | inherited parent Section 24 | No |
| `DE-D013` | Parent-contract approval at an exact commit remains required before production M3-03 implementation. | `UNRESOLVED_BLOCKING` process gate inherited as `FM-D015` | Yes |

The finite-Decimal condition does not impose a response-time threshold. It
only excludes Decimal values that have no ordered finite measurement meaning
for the approved comparator.

No additional scientific or semantic decision is blocking inside the bounded
M3-03 path.

## 27. Contradiction review

No contradiction was found among the dissertation dynamic-evidence model, the
parent Full Model contract, the M3-02 metric-profile contract, the quantitative
source model, or QB-v0.1.

Three apparent tensions are scope boundaries rather than contradictions:

1. the dissertation includes a test/experiment `t_k`; M3-03 records its
   versioned source/collection/environment identity but intentionally does not
   implement execution infrastructure;
2. the dissertation allows later normalized or aggregated conformance under a
   predefined metric procedure; M3-03 emits only the categorical direct
   comparison, while the parent assigns the bounded numeric product-quality
   indicator to a later stage; and
3. exact C0 extraction retains an embedded-`500` unresolved diagnostic while
   also accepting the whole phrase as context. The accepted context contract
   explicitly requires both facts, so M3-03 preserves the diagnostic and may
   still bind the resolved criterion.

QB text normalization is used only for bounded identity. It is not numeric
normalization and does not broaden metric or context semantics.

## 28. Implementation readiness for M3-03 and M3-04

Subject to the inherited `FM-D015` approval gate, this contract supplies
sufficient deterministic inputs for later M3-03 implementation. It fixes the
three core records, registry, identities, exact comparator, numeric and unit
semantics, context, source/collection provenance, statuses, precedence,
versioning, fixtures, invariants, and acceptance cases.

It also supplies sufficient deterministic dynamic inputs for the later M3-04
feature-mapping contract:

- `QuantitativeCriterion` can source `PE.CRITERION.RESPONSE_TIME`;
- `DynamicObservation` can source `PE.OBS.RESPONSE_TIME`; and
- `ConformanceAssessment` can source `PE.CONFORMANCE.RESPONSE_TIME`.

M3-04 must preserve these identities, statuses, applicability, temporal
availability, and provenance. It need not infer a threshold, unit conversion,
context relation, or missing value. M3-04 still owns its feature-profile
assembly rules and must not assess product quality.

M3-03 is not implemented by this document.
