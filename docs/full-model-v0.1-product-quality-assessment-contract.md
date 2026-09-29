# Full Model v0.1 Product-Quality Assessment Contract

**Contract ID:** `FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT`  
**Contract version:** `1`  
**Target issue:** `M3-05 / #142`  
**Bounded characteristic:** `PERFORMANCE_EFFICIENCY`  
**Status:** `NORMATIVE_CANDIDATE / PARENT_CONTRACT_APPROVAL_REQUIRED`

## 1. Purpose and authority

This document defines the normative contract for the bounded Full Model v0.1
product-quality assessment step:

```text
X_PE + ModelVersion + ParameterSetVersion
-> ProductQualityAssessment
```

It completes the contract research for:

```text
P / M + E -> X_PE -> M_quality
```

It does not implement M3-05 and does not define a predictive function,
experimental calibration, a full Performance Efficiency measure, or a general
ISO/IEC 25010 assessment method.

Normative precedence is:

1. `docs/full-model-v0.1-contract.md`;
2. this contract for `M_quality`'s bounded Performance Efficiency result;
3. `docs/full-model-v0.1-product-quality-feature-contract.md`;
4. `docs/full-model-v0.1-dynamic-evidence-contract.md`;
5. `docs/full-model-v0.1-metric-profile-contract.md`;
6. existing QB-v0.1 contracts and `docs/model-spec.md`; and
7. dissertation material in `docs/reference/` as scientific rationale rather
   than executable specification.

Where the parent contract has fixed a decision, this document specializes it
without reopening it.

## 2. Scientific review of the bounded result

### 2.1 Dissertation constraints

The dissertation establishes all of the following:

- Requirement quality describes an information artifact; product quality
  describes an implemented product and its behavior.
- A requirement may define an observable response-time target, but achievement
  can be confirmed only through product observation.
- For a binary-verifiable criterion, Chapter 3.2 permits
  `c_k in {0,1}`, where `1` means that the criterion is met and `0` that it is
  not met.
- A continuous `[0,1]` transformation is permissible only when its function is
  predefined in a metric passport or acceptance criterion. No universal
  transformation is supplied.
- Test coverage and criterion conformance are separate. Full coverage does not
  itself mean good product quality.
- One response-time observation for one scenario cannot automatically become
  a complete actual value `y_PE`; a separate transparent and predeclared
  aggregation procedure would be required.
- Predicted product quality `y_hat_PE` requires a selected function `F_theta`,
  data-defined or otherwise justified parameters, calibration, validation,
  and evidence-sufficiency rules.
- Missing observations are availability information, not negative evidence.

### 2.2 Decision on the proposed `{0,1}` indicator

The parent decision is scientifically supportable with a narrower
interpretation than a product-characteristic score:

```text
CONFORMS          -> Fraction(1, 1)
DOES_NOT_CONFORM  -> Fraction(0, 1)
```

This is accepted only as an exact encoding of the dissertation's binary
criterion-conformance variable `c_k`. It is named
`OBSERVED_REFERENCE_INDICATOR` and means:

> the observed conformance state of one response-time criterion for one
> product version in one declared collection, environment, and context.

It is not:

- `y_hat_PE`;
- actual complete `y_PE`;
- a normalized Performance Efficiency level;
- a probability, confidence, reliability, accuracy, or uncertainty value;
- a percentage of Performance Efficiency achieved;
- an aggregation of Performance Efficiency subcharacteristics; or
- evidence that the requirement target is valid for stakeholder need.

The categorical `ConformanceOutcome` remains the primary scientific fact. The
Fraction is a lossless conventional encoding of that two-state fact for the
parent-approved reference procedure. It does not introduce a distance scale:
arithmetic on indicators from multiple criteria or observations is not
authorized.

### 2.3 Why no alternative representation replaces it

A categorical-only output would also be scientifically defensible and is
already preserved by `ConformanceAssessment`. The parent contract, however,
explicitly approves the exact Fraction representation for M3-05. Retaining
both the categorical source and exact encoding preserves the source semantics
without inventing a continuous transformation. No dissertation requirement
forces replacement of the bounded binary encoding.

## 3. Three distinct concepts

### 3.1 Requirement Quality

Requirement Quality is represented by existing
`RequirementQualityProfile`, `SpecificationQualityProfile`, and the lossless
`MetricProfile` projection of C/V/U and QB-v0.1 Consistency.

Its subject is a requirement or specification artifact. It says nothing by
itself about observed product behavior. Those profiles remain unchanged.

### 3.2 Predicted Product Quality

Predicted Product Quality is the future characteristic-specific estimate
usually denoted `y_hat_j`, and here `y_hat_PE`. It would require:

```text
y_hat_PE = F_theta_PE(X_PE, context)
```

No function class, selected features, coefficients, weights, normalization,
training data, target definition, calibration procedure, validation result, or
prediction-uncertainty rule has been approved. Therefore Full Model v0.1 does
not calculate `y_hat_PE`.

For every result under this contract:

```text
prediction_value = None
```

Absence is normative, not an implementation gap to fill with the observed
indicator.

### 3.3 Observed product-quality evidence / bounded conformance

The v0.1 output is a typed interpretation of one observed conformance event.
Its subject is a versioned product, its scope is one criterion and context, and
its evidence is the exact criterion-observation-conformance chain.

It is placed in the product-quality assessment layer because it is
characteristic-specific observed evidence for Performance Efficiency. Its
`result_kind` and scope prevent it from being presented as the characteristic
in full.

## 4. Bounded assessment registry

### 4.1 Characteristic

```text
characteristic_id = PERFORMANCE_EFFICIENCY
```

No other product-quality characteristic is supported.

### 4.2 Model, procedure, and parameter identities

```text
model_id                 = FULL-MODEL-V0.1-M-QUALITY-PE
model_version            = 1
assessment_procedure_id  = PE-OBS-CONFORMANCE-001
procedure_version        = 1
parameter_set_id         = PE-OBS-CONFORMANCE-001-PARAMETERS
parameter_set_version    = 1
```

`PE-OBS-CONFORMANCE-001 / 1` is the procedure already fixed by the parent
contract. The model ID identifies the bounded M_quality component that hosts
that procedure; it does not imply a fitted prediction model.

### 4.3 Result kind

The closed v0.1 result-kind registry contains exactly:

```text
OBSERVED_REFERENCE_INDICATOR
```

No `PREDICTION`, `ESTIMATED_PERFORMANCE_EFFICIENCY`,
`ACTUAL_PERFORMANCE_EFFICIENCY`, `QUALITY_SCORE`, or generic `PASS_RATE` result
kind is supported.

## 5. Pure assessment interface

```text
assess_product_quality(
  feature_profile: PerformanceEfficiencyFeatureProfile,
  model_ref: ModelRef,
  parameter_set_ref: ParameterSetRef,
  assessment_context: ProductQualityAssessmentContext,
) -> ProductQualityAssessment
```

The function is pure: it performs no I/O, test execution, telemetry
collection, requirement extraction, feature calculation, unit conversion,
statistical analysis, training, calibration, or reporting.

It validates and interprets an already constructed `X_PE`. It must not inspect
raw requirement text to repair a feature profile.

## 6. Supporting context and parameter records

### 6.1 ProductQualityAssessmentContext

```text
ProductQualityAssessmentContext
  assessment_event_ref: ProductQualityAssessmentEventRef
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  feature_profile_ref: PerformanceEfficiencyFeatureProfileRef
  product_ref: ProductRef
  process_state_ref: ProcessStateRef
  full_model_contract_ref: ContractRef
  assessment_contract_ref: ContractRef
```

All identity and version fields are supplied explicitly and must agree with the
feature profile. No version is inferred.

`process_state_ref` is the caller-allocated context identity reserved before
component execution under the process/reassessment contract. It does not
reference an already assembled state as an input dependency; later assembly
associates this completed assessment with that same identity.

### 6.2 ParameterSet

```text
ParameterSet
  parameter_set_id: PE-OBS-CONFORMANCE-001-PARAMETERS
  version: 1
  entries: ()
  source_or_rationale: parent contract Section 10 binary procedure
  calibration_status: PROVISIONAL_NOT_CALIBRATED
  scope: one response-time criterion conformance encoding
  non_claim: no empirical coefficient or predictive calibration
  approved_contract_ref: FULL-MODEL-V0.1-CONTRACT / 1
```

The empty tuple is mandatory. The procedure has no coefficient, weight,
threshold beyond the requirement's own bound, tolerance, confidence, or
reliability parameter. Adding an entry is a semantic change requiring a new
approved contract and parameter-set version.

The requirement's response-time bound is criterion evidence, not a model
parameter.

## 7. ProductQualityAssessment schema

```text
ProductQualityAssessment
  assessment_id: ProductQualityAssessmentId
  assessment_event_ref: ProductQualityAssessmentEventRef
  characteristic_id: PERFORMANCE_EFFICIENCY
  product_ref: ProductRef
  artifact_ref: ArtifactRef
  feature_profile_ref: PerformanceEfficiencyFeatureProfileRef
  scope: ProductQualityScope
  scope_statement: str
  result_kind: OBSERVED_REFERENCE_INDICATOR
  status: FullModelStatus
  applicability: Applicability
  source_conformance_outcome: ConformanceOutcome | None
  value: Fraction | None
  prediction_value: None
  observed_value: Fraction | None
  numeric_representation: EXACT_FRACTION | NONE
  evidence_coverage: BoundedEvidenceCoverage
  reliability: None
  uncertainty: None
  explanation: str
  feature_refs: tuple[PerformanceEfficiencyFeatureEntryRef, ...]
  evidence_refs: tuple[EvidenceRef, ...]
  provenance: ProductQualityAssessmentProvenance
  model_ref: ModelRef
  procedure_rule_ref: RuleRef
  parameter_set_ref: ParameterSetRef
  calibration_status: PROVISIONAL_NOT_CALIBRATED
  artifact_version: str
  source_assessment_version: str
  product_version: str
  product_quality_assessment_version: str
  non_claims: tuple[ProductQualityNonClaim, ...]
```

The apparently redundant `value` and `observed_value` fields preserve the
generic result shape fixed by the parent contract:

- `observed_value` is the canonical typed observed indicator;
- `value` exposes that same exact indicator to generic result consumers; and
- for this sole result kind, both have the same exact numerator and denominator
  or both are `None`.

`prediction_value` is statically absent. It must not alias either field.

## 8. Scope contract

### 8.1 Structured scope

```text
ProductQualityScope
  scope_kind: SINGLE_CRITERION_SINGLE_OBSERVATION
  characteristic_id: PERFORMANCE_EFFICIENCY
  dynamic_metric_ref: DYN.RESPONSE_TIME
  criterion_ref: QuantitativeCriterionRef | None
  requirement_subject_ref: RequirementSubjectRef | None
  observation_ref: DynamicObservationRef | None
  conformance_ref: ConformanceAssessmentRef | None
  product_ref: ProductRef
  environment_ref: EnvironmentRef | None
  collection_ref: ObservationCollectionRef | None
  context_identity: CriterionContextIdentity | None
  unit: SECOND | None
  process_stage: REFERENCE_VERIFICATION
  full_characteristic_coverage: NOT_ESTABLISHED
```

### 8.2 Required scope statement

For an available result, `scope_statement` must communicate all of these facts:

```text
Observed conformance of one response-time criterion for the named product
version in the named collection/environment and exact criterion context. This
is not complete Performance Efficiency and is not a prediction.
```

Identifiers may be interpolated, but none of the four semantic clauses may be
omitted. A non-available result must additionally state the controlling status
and reason.

A reporter may make the wording more readable but must not shorten it to
"Performance Efficiency = 1", "PE passed", or an equivalent full-
characteristic claim.

## 9. Exact result procedure

After validating the feature profile and version references:

```text
if X_PE.status != AVAILABLE:
    propagate X_PE.status and applicability
    source_conformance_outcome = None
    value = None
    observed_value = None
    numeric_representation = NONE

if X_PE.status == AVAILABLE and
   PE.CONFORMANCE.RESPONSE_TIME.outcome == CONFORMS:
    status = AVAILABLE
    applicability = APPLICABLE
    source_conformance_outcome = CONFORMS
    observed_value = Fraction(1, 1)
    value = Fraction(1, 1)
    numeric_representation = EXACT_FRACTION

if X_PE.status == AVAILABLE and
   PE.CONFORMANCE.RESPONSE_TIME.outcome == DOES_NOT_CONFORM:
    status = AVAILABLE
    applicability = APPLICABLE
    source_conformance_outcome = DOES_NOT_CONFORM
    observed_value = Fraction(0, 1)
    value = Fraction(0, 1)
    numeric_representation = EXACT_FRACTION
```

No other branch may produce a numeric value. The evaluator does not recompute
the Decimal comparison and does not inspect the observed distance from the
bound. It trusts the validated conformance feature and retains the exact source
operands in provenance.

The mapping is not normalization: it encodes two categorical outcomes fixed
by the criterion procedure. It cannot be interpolated, averaged, or interpreted
as a ratio scale under this contract.

## 10. Status and applicability

### 10.1 Allowed result shapes

| Status | Applicability | Outcome | Value fields |
| --- | --- | --- | --- |
| `AVAILABLE` | `APPLICABLE` | exactly one categorical outcome | exact `Fraction(1,1)` or `Fraction(0,1)` as defined in Section 9 |
| `UNAVAILABLE` | `APPLICABLE` | `None` | both `None` |
| `UNKNOWN` | `APPLICABLE` or `UNKNOWN` | `None` | both `None` |
| `UNRESOLVED` | `APPLICABLE` or `UNKNOWN` | `None` | both `None` |
| `UNSUPPORTED` | `APPLICABLE` or `UNKNOWN` | `None` | both `None` |
| `NOT_APPLICABLE` | `NOT_APPLICABLE` | `None` | both `None` |

`prediction_value`, `reliability`, and `uncertainty` are always `None`,
including for an available result.

### 10.2 Propagation

The assessment copies the validated feature profile's status and applicability
when they are non-available. It does not re-run profile precedence.

Consequences include:

- missing supported observation -> `UNAVAILABLE`, not zero and not failure;
- unresolved target identity or same-key QB conflict -> `UNRESOLVED`;
- unsupported comparator, unit, or context -> `UNSUPPORTED`;
- no applicable criterion -> `NOT_APPLICABLE`;
- an upstream `UNKNOWN` -> `UNKNOWN`; and
- `DOES_NOT_CONFORM` -> `AVAILABLE` with exact zero, not an absence status.

An internally invalid profile, inconsistent version set, missing mandatory
slot, or impossible status/value combination fails construction. Invalid data
is not converted into a scientific result state.

## 11. Evidence coverage

### 11.1 Structured inventory

```text
BoundedEvidenceCoverage
  coverage_kind: BOUNDED_REQUIRED_CHANNEL_INVENTORY
  procedure_scope: SINGLE_RESPONSE_TIME_CRITERION
  items: tuple[EvidenceCoverageItem, ...]
  bounded_procedure_state:
    COMPLETE | UNAVAILABLE | UNKNOWN | UNRESOLVED | UNSUPPORTED | NOT_APPLICABLE
  full_performance_efficiency_coverage: NOT_ESTABLISHED
  numeric_coverage: None
```

```text
EvidenceCoverageItem
  channel_id:
    RESPONSE_TIME_CRITERION |
    TARGET_QB_GATE |
    RESPONSE_TIME_OBSERVATION |
    RESPONSE_TIME_CONFORMANCE |
    REQUIREMENT_C_CONTEXT |
    REQUIREMENT_V_CONTEXT |
    REQUIREMENT_U_CONTEXT
  role: REQUIRED | GATE | CONTEXT_ONLY
  feature_ref: PerformanceEfficiencyFeatureEntryRef
  status: FullModelStatus
  applicability: Applicability
  source_refs: tuple[TypedSourceRef, ...]
```

Items are ordered as:

1. criterion;
2. QB target gate;
3. observation;
4. conformance;
5. C context;
6. V context; and
7. U context.

This order is an evidence inventory and does not change `X_PE` feature order.

### 11.2 Procedure-state semantics

- `COMPLETE`: criterion, observation, and conformance are available and the QB
  gate is `TARGET_CLEAR` or `TARGET_NOT_APPLICABLE`.
- `UNAVAILABLE`: the profile status is `UNAVAILABLE`.
- `UNKNOWN`: the profile status is `UNKNOWN`.
- `UNRESOLVED`: the profile status is `UNRESOLVED`, including a QB target
  conflict or unresolved target gate.
- `UNSUPPORTED`: the profile status is `UNSUPPORTED`.
- `NOT_APPLICABLE`: the criterion is `NOT_APPLICABLE`.

The state describes only input completeness for this bounded procedure. It is
not a percentage or claim about Performance Efficiency coverage. C/V/U context
items cannot prevent `COMPLETE` because they are not required assessment
channels.

No ratio such as `4/7`, percentage, evidence-reliability number, confidence, or
uncertainty number is calculated. The dissertation's future coverage and
reliability formulas require an approved applicable feature set and source-
reliability rules that Full Model v0.1 does not possess.

## 12. Calibration, reliability, and uncertainty

Every result carries:

```text
calibration_status = PROVISIONAL_NOT_CALIBRATED
```

This status is orthogonal to result status. An available `Fraction(1,1)` is
still provisional at the product-characteristic interpretation layer.

The following fields are absent by rule:

```text
reliability = None
uncertainty = None
```

The explanation and non-claims must state that these values are not
established. An implementation must not substitute `0`, `1`, the evidence
inventory state, detector completeness, QB Consistency, or source-processing
status.

`EXPERIMENTALLY_CALIBRATED` is forbidden for v0.1. The future predictive
extension is labeled `EXPERIMENTAL_CALIBRATION_REQUIRED`, but that label does
not replace this procedure's mandatory `PROVISIONAL_NOT_CALIBRATED` status.

## 13. Explanation contract

Every explanation is non-empty, deterministic for the same immutable inputs,
and covers:

1. the result kind and exact scope;
2. the source conformance outcome, or the controlling non-available state;
3. the response-time criterion ID, bound, comparator, unit, and context when
   available;
4. the observation ID, exact Decimal value, product, collection, and
   environment when available;
5. the target QB gate decision;
6. the exact Fraction mapping when available;
7. that C/V/U are requirement-artifact context only;
8. that prediction, reliability, and uncertainty are absent; and
9. that the result does not represent complete Performance Efficiency.

An explanation must not say or imply that:

- C/V/U caused the observed response time;
- QB Consistency measured the product;
- an unavailable observation failed;
- a conforming result validates the correctness of the requirement target; or
- a nonconforming result supplies a calibrated magnitude of poor quality.

## 14. Provenance

```text
ProductQualityAssessmentProvenance
  feature_profile_ref
  ordered_feature_refs
  criterion_ref_or_none
  requirement_subject_ref_or_none
  metric_profile_ref
  qb_metric_entry_ref
  ordered_qb_cross_result_refs
  observation_ref_or_none
  conformance_ref_or_none
  product_ref
  environment_ref_or_none
  collection_ref_or_none
  process_state_ref
  source_evidence_refs
  source_diagnostic_refs
  source_assessment_refs
  contract_refs
  rule_refs
  model_ref
  parameter_set_ref
```

The minimum resolvable chain is:

```text
Requirement
-> quantitative source Evidence
-> QuantitativeCriterion
-> DynamicObservation
-> ConformanceAssessment
-> X_PE
-> ProductQualityAssessment
```

C/V/U and QB provenance attach to `X_PE` without being rewritten as product
observations. Exact Decimal criterion/observation operands and exact Fraction
indicator numerator/denominator remain in their respective domains.

No evidence object is duplicated or assigned a replacement evidence ID.

## 15. Identity and versioning

### 15.1 Assessment identity

```text
ProductQualityAssessmentId = (
  assessment_event_ref,
  feature_profile_ref,
  characteristic_id,
  result_kind,
  model_ref,
  procedure_rule_ref,
  parameter_set_ref,
)
```

`ProductQualityAssessmentEventRef` contains a caller-supplied event ID/version
and its product/artifact association. It is not the output ID and therefore
does not make the identity circular. No hash is required.

### 15.2 Required versions

Every result retains:

- artifact and source-assessment versions;
- QB snapshot and contract versions;
- MetricProfile, metric registry, and P-to-M adapter versions;
- criterion-binding, dynamic registry, collection, environment, observation,
  dynamic-assessment, and conformance-evaluator versions;
- `X_PE` profile, registry, mapping-rule, and contract versions;
- product and process-state versions;
- `FULL-MODEL-V0.1-M-QUALITY-PE / 1`;
- `PE-OBS-CONFORMANCE-001 / 1`;
- `PE-OBS-CONFORMANCE-001-PARAMETERS / 1`; and
- this assessment contract and parent Full Model versions.

A semantic change to mapping, status propagation, scope, evidence coverage, or
interpretation requires a new procedure/model/contract version as applicable.
A changed input assessment or product observation requires new source and
output identities. Formatting changes do not change scientific identity.

### 15.3 Reassessment

Later evidence or a changed product/specification version produces a new
`ProductQualityAssessment`. It does not mutate or backfill an earlier result.
Cross-version comparison is owned by the later reassessment contract and must
respect semantic compatibility. A change from `UNAVAILABLE` to `AVAILABLE`
means evidence became available; it does not by itself prove product
improvement.

## 16. Determinism and ordering

For identical immutable inputs and version references, the assessment ID,
status, applicability, values, evidence coverage, explanation, provenance, and
non-claims are identical.

Ordering is:

1. feature references in `X_PE` registry order;
2. evidence-coverage items in Section 11.1 order;
3. QB cross results in source order;
4. source evidence and diagnostics in source order, with first-occurrence
   de-duplication only where already approved; and
5. non-claims in the mandatory order in Section 17.2.

No sorting by result value, conformance polarity, C/V/U values, status,
evidence count, or text is permitted.

## 17. Claims and non-claims

### 17.1 Authorized claims

An available result may claim only:

1. the named response-time criterion was evaluated against the named exact
   observation;
2. the observation was collected for the named product version under the
   named collection/environment and exact context;
3. the source conformance outcome is `CONFORMS` or `DOES_NOT_CONFORM` under the
   exact inclusive `<=` rule; and
4. the observed reference indicator is the exact binary encoding defined by
   Section 9.

A non-available result may claim only its status, applicable scope, and typed
reason with provenance.

### 17.2 Mandatory non-claims

Every result contains these non-claim identities in order:

```text
NC-PE-001  NOT_COMPLETE_PERFORMANCE_EFFICIENCY
NC-PE-002  NOT_PREDICTED_PRODUCT_QUALITY
NC-PE-003  NOT_ACTUAL_AGGREGATED_Y_PE
NC-PE-004  NOT_PROBABILITY_CONFIDENCE_RELIABILITY_OR_ACCURACY
NC-PE-005  NO_MODEL_UNCERTAINTY_ESTIMATE
NC-PE-006  NO_CAUSAL_CLAIM_FROM_REQUIREMENT_QUALITY
NC-PE-007  NO_VALIDATION_OF_REQUIREMENT_TARGET_OR_STAKEHOLDER_NEED
NC-PE-008  NO_OTHER_PE_METRICS_OR_CONTEXTS_ASSESSED
NC-PE-009  NO_SCALAR_OVERALL_PRODUCT_OR_REQUIREMENT_QUALITY
```

For a non-available result, the same non-claims remain present. Missing
evidence does not weaken the need for scope control.

## 18. Invariants and forbidden transformations

### 18.1 Required invariants

1. `characteristic_id` is exactly `PERFORMANCE_EFFICIENCY`.
2. `result_kind` is exactly `OBSERVED_REFERENCE_INDICATOR`.
3. `prediction_value`, `reliability`, and `uncertainty` are always `None`.
4. `calibration_status` is always `PROVISIONAL_NOT_CALIBRATED`.
5. The parameter set contains no entries.
6. An available result has exactly one conformance outcome and the matching
   exact Fraction mapping.
7. `value == observed_value` for every available result.
8. A non-available result has no outcome and no numeric value.
9. `Fraction(0,1)` appears only for observed `DOES_NOT_CONFORM`, never for
   missing, unknown, unresolved, unsupported, or inapplicable evidence.
10. Evidence coverage is a structured inventory with no numeric percentage.
11. `full_performance_efficiency_coverage` is always `NOT_ESTABLISHED`.
12. Scope and provenance resolve to the same criterion, observation,
    conformance, product, and feature profile.
13. Exact source Decimal operands and the exact result Fraction remain
    separately traceable.
14. Every result carries all mandatory non-claims.

### 18.2 Forbidden transformations and interpretations

An implementation must not:

- calculate or populate `y_hat_PE` or complete `y_PE`;
- call the observed indicator a Performance Efficiency score, level, grade,
  probability, pass rate, confidence, or accuracy;
- treat one observation as full characteristic coverage;
- normalize response time, distance to bound, C/V/U, or QB Consistency;
- weight or aggregate any feature;
- average binary indicators across criteria, observations, products, or
  versions;
- recompute conformance from raw Decimal operands in M3-05;
- invent a threshold other than the requirement's criterion;
- round, quantize, or convert through binary float;
- substitute zero for absent evidence;
- infer reliability or uncertainty from detector/coverage states;
- suppress a same-target QB conflict;
- treat positive conformance as validation of the requirement's correctness;
- treat negative conformance as a calibrated measure of characteristic
  magnitude; or
- overwrite an earlier assessment when new evidence arrives.

## 19. Deterministic reference cases

All cases use the exact source criterion:

```text
requirement = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
bound       = Decimal("2")
unit        = SECOND
context     = (QB-NORMALIZATION / 1,
               "при 500 одночасних користувачах")
product     = (PRODUCT-PE-001, 1)
result kind = OBSERVED_REFERENCE_INDICATOR
calibration = PROVISIONAL_NOT_CALIBRATED
```

### 19.1 Available cases

| Case | Observation/conformance | Expected result |
| --- | --- | --- |
| `PE-Q-RF-001` | `Decimal("1.8")`, `CONFORMS` | `AVAILABLE/APPLICABLE`; `value=observed_value=Fraction(1,1)`; prediction/reliability/uncertainty absent |
| `PE-Q-RF-002` | `Decimal("2")`, `CONFORMS` | same exact `Fraction(1,1)`; equality is already justified by dynamic evaluator |
| `PE-Q-RF-003` | `Decimal("2.1")`, `DOES_NOT_CONFORM` | `AVAILABLE/APPLICABLE`; `value=observed_value=Fraction(0,1)` |
| `PE-Q-RF-004` | `CONFORMS`, source C/V/U all `UNKNOWN` | same as `PE-Q-RF-001`; context states preserved and do not alter value |
| `PE-Q-RF-005` | `CONFORMS`, QB gate `TARGET_NOT_APPLICABLE` | same as `PE-Q-RF-001`; absence of a cross comparison is not a penalty |

For every available case:

```text
full_performance_efficiency_coverage = NOT_ESTABLISHED
prediction_value = None
reliability = None
uncertainty = None
```

### 19.2 Non-available cases

| Case | Controlling input | Expected result |
| --- | --- | --- |
| `PE-Q-RF-006` | observation not supplied | `UNAVAILABLE/APPLICABLE`; no outcome/value |
| `PE-Q-RF-007` | criterion identity unresolved | `UNRESOLVED`; no outcome/value |
| `PE-Q-RF-008` | observation unit `MINUTE` | `UNSUPPORTED`; no conversion and no value |
| `PE-Q-RF-009` | no applicable response-time criterion | `NOT_APPLICABLE/NOT_APPLICABLE`; no value |
| `PE-Q-RF-010` | target-key QB `CONFIRMED_CONFLICT` even though one conformance result exists | `UNRESOLVED/APPLICABLE`; dynamic evidence retained in provenance; no product-quality value |
| `PE-Q-RF-011` | upstream approved state `UNKNOWN` | `UNKNOWN`; no value and no zero |

### 19.3 Scope rendering example

An acceptable available statement is:

```text
Observed reference indicator 1/1: observation OBS-001 conforms to response-time
criterion CRIT-001 for PRODUCT-PE-001 version 1 in collection COLL-001 version
1, environment ENV-001 version 1, and context "при 500 одночасних
користувачах". This covers one criterion and observation; it is not complete
Performance Efficiency and is not a prediction.
```

The `1/1` rendering is presentation only. The domain value remains exact
`Fraction(1,1)`.

## 20. Acceptance cases for future M3-05 implementation

| ID | Required behavior |
| --- | --- |
| `PE-Q-AC-001` | The pure interface accepts only a validated `PerformanceEfficiencyFeatureProfile` and explicit version contexts. |
| `PE-Q-AC-002` | Only `PERFORMANCE_EFFICIENCY` is accepted. |
| `PE-Q-AC-003` | Only `OBSERVED_REFERENCE_INDICATOR` is emitted. |
| `PE-Q-AC-004` | `CONFORMS` maps exactly to `Fraction(1,1)`. |
| `PE-Q-AC-005` | `DOES_NOT_CONFORM` maps exactly to `Fraction(0,1)`. |
| `PE-Q-AC-006` | Available `value` and `observed_value` are exactly equal. |
| `PE-Q-AC-007` | No non-available state carries an outcome or numeric value. |
| `PE-Q-AC-008` | Missing observation propagates `UNAVAILABLE` and never becomes zero or nonconformance. |
| `PE-Q-AC-009` | Criterion/QB identity conflict propagates `UNRESOLVED` and never chooses a bound. |
| `PE-Q-AC-010` | Unsupported comparator/unit/context propagates `UNSUPPORTED`. |
| `PE-Q-AC-011` | No applicable criterion propagates `NOT_APPLICABLE`. |
| `PE-Q-AC-012` | Upstream `UNKNOWN` remains `UNKNOWN`. |
| `PE-Q-AC-013` | Negative conformance remains `AVAILABLE`; zero is an observed category encoding, not missing data. |
| `PE-Q-AC-014` | The evaluator does not recalculate conformance or inspect raw requirement text. |
| `PE-Q-AC-015` | `prediction_value` is always absent and no `y_hat_PE` field is populated elsewhere. |
| `PE-Q-AC-016` | Reliability and uncertainty are always absent with explicit explanatory reasons. |
| `PE-Q-AC-017` | Calibration status is always `PROVISIONAL_NOT_CALIBRATED`. |
| `PE-Q-AC-018` | The parameter set version is explicit and its entries are empty. |
| `PE-Q-AC-019` | The result preserves all artifact, assessment, feature, product, collection, environment, model, rule, parameter, and contract versions. |
| `PE-Q-AC-020` | Evidence coverage is a seven-item structured inventory in normative order. |
| `PE-Q-AC-021` | No evidence coverage percentage, ratio, reliability, or confidence is computed. |
| `PE-Q-AC-022` | `full_performance_efficiency_coverage` is always `NOT_ESTABLISHED`. |
| `PE-Q-AC-023` | C/V/U are visible only through context/provenance and cannot change status/value. |
| `PE-Q-AC-024` | The QB aggregate Fraction cannot change or weight the result. |
| `PE-Q-AC-025` | The exact criterion and observation Decimal operands remain provenance and are not converted to result Fraction. |
| `PE-Q-AC-026` | The scope statement names one criterion/context/product/collection and both central non-claims. |
| `PE-Q-AC-027` | Every result includes all nine mandatory non-claim identities in order. |
| `PE-Q-AC-028` | Explanations distinguish requirement quality, observed behavior, and product-quality interpretation. |
| `PE-Q-AC-029` | No output labels the result as complete or predicted Performance Efficiency. |
| `PE-Q-AC-030` | No normalization, weighting, rounding, imputation, threshold invention, or aggregation occurs. |
| `PE-Q-AC-031` | Multiple criteria/observations cannot be averaged into one result. |
| `PE-Q-AC-032` | A later observation or changed version creates a new immutable assessment. |
| `PE-Q-AC-033` | Mixed-version, dangling-reference, duplicate-slot, or impossible source/value input fails validation rather than producing an absence state. |
| `PE-Q-AC-034` | Identical immutable inputs and versions produce field-equivalent canonical result data in deterministic order. |
| `PE-Q-AC-035` | Unit tests can construct domain inputs directly without files, CLI, extractor, test runner, telemetry, or benchmarking infrastructure. |

## 21. Experimental-calibration boundary

### 21.1 M3-05 may implement now

Subject to the parent approval blocker, M3-05 may implement only:

- validation of the `X_PE` contract;
- the pure `PE-OBS-CONFORMANCE-001 / 1` mapping from categorical outcome to
  exact Fraction `1/1` or `0/1`;
- non-available state propagation;
- the structured single-procedure evidence inventory;
- explicit absent prediction/reliability/uncertainty fields;
- immutable identity, scope, explanation, provenance, version, calibration,
  claim, and non-claim records; and
- deterministic reference tests for Sections 19-20.

This is an observed single-criterion conformance indicator hosted by
`M_quality`; it is not a predictive model.

### 21.2 Must wait for experimental calibration and separate approval

The following remain absent until an experimental protocol and reviewed
contracts define them:

- `F_theta_PE` and any model class;
- selected predictive features and feature contributions;
- coefficients, weights, thresholds, intercepts, or learned parameters;
- normalization or direction harmonization;
- an experimentally defined actual target `y_PE`;
- aggregation across response-time scenarios or other Performance Efficiency
  measures/subcharacteristics;
- numeric evidence coverage and source reliability;
- model uncertainty, confidence, prediction interval, and accuracy;
- validation error, calibration quality, generalization, and cross-project
  stability;
- comparison of `y_hat_PE` with `y_PE`; and
- any overall product-quality scalar.

These are `EXPERIMENTAL_CALIBRATION_REQUIRED`, not defaults for M3-05.

## 22. Assumptions, contradictions, blockers, and readiness

### 22.1 Explicit scientific assumptions

1. The categorical conformance supplied by M3-03 is valid under its exact
   comparator, unit, context, identity, and provenance gates.
2. Encoding that category as exact Fraction zero/one preserves the binary
   meaning but creates no continuous magnitude.
3. The target-scoped QB gate in `X_PE` is authoritative for whether a single
   criterion may be interpreted without selecting among contradictory targets.
4. One conformance event is useful observed evidence for Performance
   Efficiency but insufficient for full characteristic measurement.
5. No rule in the current repository establishes numeric evidence reliability,
   uncertainty, or predictive calibration for this slice.

### 22.2 Contradiction review

The apparent tension between the parent `{0,1}` decision and the dissertation's
warning against treating one observation as complete `y_PE` is resolved by
result typing and scope: the value is `c_k`, an observed reference indicator,
not `y_PE` or `y_hat_PE`.

The dissertation discusses future normalization, feature selection, coverage
ratios, reliability, and `F_theta`; the parent contract explicitly excludes
those from v0.1 without calibration. Omitting them is consistent with the
dissertation's requirement that such rules be predeclared and experimentally
justified.

No scientific contradiction requiring replacement of the bounded indicator
was found.

### 22.3 Blocking decision

`FM-D015` remains the sole external blocker: the parent Full Model v0.1
contract requires its recorded approval. Until that approval exists, this
contract remains a normative candidate and M3-05 implementation remains
blocked. No calibration blocker prevents implementing the narrowly scoped
indicator because it makes no calibrated or predictive claim; calibration
does block every extension listed in Section 21.2.

### 22.4 Implementation readiness

Subject to `FM-D015`, the M3-05 contract is sufficient for the bounded
implementation. It fixes the output schema, exact result kind and mapping,
status/applicability behavior, structured evidence coverage, empty parameter
set, provisional calibration label, explanation/provenance/version rules,
claims/non-claims, deterministic fixtures, and acceptance invariants.

The implementation boundary is explicit: M3-05 can produce one scoped observed
conformance indicator now; predicted or complete Performance Efficiency must
wait for experimental target definition, calibration, and validation.
