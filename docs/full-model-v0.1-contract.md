# Full Model v0.1 Contract and Architecture

**Contract ID:** `FULL-MODEL-V0.1-CONTRACT`  
**Contract version:** `1`  
**Milestone:** Milestone 3 - Full Theoretical Model: End-to-End v0.1  
**Issue:** [M3-01 / #138](https://github.com/rKiselyk/requirements-quality-assessment/issues/138)  
**Status:** `NORMATIVE_CANDIDATE / RESEARCHER_APPROVAL_REQUIRED`

This document defines the bounded scientific and software contract for Full
Model v0.1. It freezes the meanings, boundaries, statuses, provenance, and
version rules needed by M3-02 through M3-12. It becomes normative at the exact
commit accepted for issue #138. Until that approval is recorded, downstream
Milestone 3 production implementation remains blocked by the M3-01 approval
gate.

## 1. Purpose and authority

Full Model v0.1 provides one minimal, auditable vertical slice through the
dissertation model:

```text
M = {M_process, M_quality, M_risk}
R -> P -> M -> Q
S -> P -> M -> E -> X_j -> M_quality -> M_risk -> A_corr -> ReEval
```

The first line preserves the dissertation's three-model decomposition. The
second preserves its requirement/property/metric/product-quality path. The
third is the bounded software execution path defined here; it does not collapse
requirement quality into `Q`.

The dissertation documents in `docs/reference/` define the theoretical context.
They are traceability sources, not executable specifications. `docs/model-spec.md`
remains authoritative for every existing requirement representation, detector,
Completeness, Verifiability, Unambiguity, aggregation, evidence, assessment,
and reporting rule. The approved QB-v0.1 documents remain authoritative for
bounded quantitative-bound comparison and aggregation.

This contract is authoritative only for the new Full Model v0.1 boundaries and
the bounded decisions explicitly registered in Section 22. It does not alter an
existing accepted rule. Precedence is:

1. an accepted existing rule in `docs/model-spec.md` or the approved QB-v0.1
   contract for its existing scope;
2. this contract for a new Milestone 3 boundary not already defined there;
3. dissertation reference material as theoretical context;
4. downstream code and tests.

If this contract and an existing accepted rule appear to conflict, implementation
must stop and the conflict must be resolved by a reviewed contract amendment.
Downstream issues must not choose an interpretation locally.

The baseline specification says product-quality prediction, risk, corrective
actions, and lifecycle reassessment are outside the earlier text-only MVP. Full
Model v0.1 is an additive Milestone 3 scope, not a retroactive change to that MVP.
The baseline also leaves `RQD-016` QUALITY_PROBLEM conversion open. This contract
does not close it: its sole confirmed problem source is the already-supported
QB-v0.1 `CONFIRMED_CONFLICT`, never a C/V/U score or `SIGNAL` finding.

## 2. Scope and non-goals

Full Model v0.1 supports one controlled path with:

- the current C/V/U requirement-quality profiles;
- the current C/V/U property-level specification aggregates;
- bounded QB-v0.1 quantitative-bound Consistency where applicable;
- one product-quality characteristic, Performance Efficiency;
- one response-time criterion and one controlled dynamic observation path;
- one confirmed QB conflict to Performance Efficiency relation;
- one categorical, provisional risk-presence rule;
- one traceable corrective-action kind;
- versioned specification reassessment and before/after comparison; and
- one bounded process stage with multiple artifact versions.

The following are non-goals:

- exhaustive detector or Ukrainian grammar coverage;
- additional requirement properties or consistency classes;
- universal or full specification Consistency;
- all nine ISO/IEC 25010 product-quality characteristics;
- a full test, telemetry, architecture, source-code, or traceability platform;
- a complete SDLC or workflow engine;
- an integrated requirement-quality or specification-quality scalar;
- experimentally calibrated prediction, probability, impact, confidence,
  reliability, priority, or optimization;
- universal scientific constants or causal claims;
- product-quality, risk, or action inference from an existing `SIGNAL`; and
- automatic source rewriting or action optimality.

## 3. Terminology and symbol table

| Symbol/term | Dissertation meaning | Full Model v0.1 software meaning |
| --- | --- | --- |
| `S` | Specification `S = (R, Attr, L, H)` | A versioned `SpecificationArtifact`. The bounded projection contains the ordered current `Requirement` values plus artifact identity, version, lineage, and optional links. It does not claim full `Attr`, `L`, or `H` coverage. |
| `R` | Requirements/specification information | The ordered requirements preserved by `RequirementReader`, including stable requirement ID within an artifact version, source line, and trimmed source text. |
| `P` | Requirement/specification properties | Existing structured C/V/U requirement profiles, C/V/U specification aggregates, and separate QB-v0.1 Consistency assessment. |
| `M` | Measurable indicators/metrics | A `MetricProfile` that preserves existing values and states without recalculating them. |
| `E` | Evidence available to the model | Versioned static and dynamic evidence records. |
| `E_stat` | Static evidence | Existing source-aligned `Evidence`, traces, assessments, QB results, and their provenance. |
| `E_dyn` | Dynamic evidence | A bounded `Criterion -> Observation -> Conformance` record collected in a controlled context. |
| `X_j` | Characteristic-specific input features | A typed `ProductQualityFeatureProfile` for exactly one characteristic. It is not a product-quality result. |
| `M_quality` | Product-quality model | A pure evaluator of `X_j` producing a typed, bounded product-quality result. |
| `q_j` | One ISO/IEC 25010 product-quality characteristic | `PERFORMANCE_EFFICIENCY`, the sole v0.1 reference characteristic. |
| `y_hat_j` | Predicted product-quality value | Reserved field for an empirically calibrated prediction. Full Model v0.1 leaves it absent; it must not be synthesized from C/V/U. |
| observed quality value | Post-implementation measurement | The v0.1 exact `{0,1}` reference criterion-conformance indicator, explicitly narrower than full Performance Efficiency. |
| `D` | Defects/problems | Confirmed, evidence-backed artifact problems. In v0.1, only a QB-v0.1 direct quantitative-bound `CONFIRMED_CONFLICT` is eligible. |
| `R_DQ` | Defect-to-quality relation | A typed, reasoned link from the eligible QB problem to `PERFORMANCE_EFFICIENCY`. It is not a probability or causal proof. |
| `M_risk` | Risk model | A pure bounded classifier that can identify a provisional risk presence; it computes no magnitude. |
| `A_corr` | Corrective action | A versioned proposal or application record targeting the conflicting specification artifacts. |
| `ReEval` | Reassessment | Re-running approved components against a new artifact version and comparing compatible results. |
| process state | `P_j(tau,v)` | A `ProcessAssessmentState` associating one stage and artifact version with evidence, assessments, risk, action, and lineage. It is not the requirement-property set `P`. |
| artifact version | Version of a source artifact | Immutable version label within one `artifact_id` lineage. |
| assessment version | Version/identity of an evaluation event | Identifies the execution and its exact inputs; it is separate from artifact version. |
| parameter version | Version of model parameters/rules | Identifies the exact parameter set, including an empty numeric set for parameter-free provisional rules. |

The theoretical `P` (properties) and `P_j(tau,v)` (process state) are distinct.
Software names must not use one unqualified `P` type for both.

## 4. Full pipeline contract

Every transition is pure with respect to its input artifacts: it returns a new
structured result and does not mutate its input.

| Transition | Responsibility and required output | Status/provenance/version rules | Forbidden or unresolved behavior |
| --- | --- | --- | --- |
| `S -> P` | Run the existing extraction, C/V/U calculators, C/V/U aggregator, and QB-v0.1 analysis. Output existing records and `SpecificationAssessment`. | Preserve all current evidence, rules, snapshot identity, values, states, and non-claims. | No changed detector, calculator, aggregation, or QB semantics. |
| `P -> M` | Adapt supported assessments to typed metric entries. | Each entry cites its source assessment/result, rules, evidence, artifact version, and assessment version. | No new calculation, normalization, rounding, weighting, or zero imputation. |
| `S -> E_dyn` | Bind a supported explicit response-time criterion to a controlled observation and evaluate exact conformance. | Preserve criterion, observation, unit, exact context, source, collection version, and rule. | No criterion extraction beyond current supported quantitative observations; no unit conversion; no missing-as-failure. |
| `M + E -> X_j` | Select and package Performance Efficiency features. | Retain feature identity, status, applicability, temporal availability, and every source reference. | No prediction, coefficient, imputation, or global averaging. |
| `X_j -> M_quality` | Produce the bounded observed reference indicator when conformance is available. | Output kind, exact value or absence, explanation, evidence coverage, rule/model/parameter versions, and calibration status. | No static C/V/U-to-product-quality conversion; no full-characteristic or validated-prediction claim. |
| `P -> D` | Admit only eligible confirmed QB conflicts as problems. | Cite the exact cross result, participants, evidence, subtype, and snapshot. | Never promote a `SIGNAL`, low score, completed absence, UNKNOWN, or NOT_APPLICABLE. |
| `D -> R_DQ -> q_j` | Link the exact supported response-time conflict to Performance Efficiency. | Record rule, rationale, applicability, and bounded non-claim. | No universal causal relation or cross-characteristic inference. |
| `D + R_DQ + quality -> M_risk` | Classify `RISK_IDENTIFIED` for the eligible relation. | Quality result may be available or unavailable, but its status is preserved; risk carries provisional calibration status. | No probability, impact, severity, priority, confidence, or scalar risk. |
| `risk/problem -> A_corr` | Associate `RECONCILE_QUANTITATIVE_BOUNDS` with the conflicting requirements. | Distinguish proposed from applied; application needs an explicit, externally supplied revision. | No automatic choice of the authoritative bound and no silent mutation. |
| `S(v1) + applied action -> S(v2)` | Create a new immutable specification version with lineage. | Preserve `S(v1)`, action ID, changed requirement IDs, replacement provenance, and version transition. | No in-place overwrite. |
| `S(v2) -> ReEval` | Re-run the same approved layers and compare compatible outputs. | Record versions of artifact, assessment, evidence, rules, model, and parameters. | No comparison across incompatible meanings and no causal product-improvement claim. |

An unsupported or unavailable transition returns a structured non-value result.
It must not skip a layer, borrow a value from another status, or manufacture a
default.

## 5. P_v0.1 contract

The permitted property inputs are exactly:

1. requirement-level Completeness under `CALC-C-MVP-001`;
2. requirement-level Verifiability under `CALC-V-MVP-001`;
3. requirement-level Unambiguity under `CALC-U-MVP-001`;
4. specification-level C/V/U aggregates under `AGG-MVP-001`; and
5. specification-level `M_cons[QB-v0.1]` and its cross results under the
   approved QB-v0.1 contracts.

Requirement-level and specification-level entries coexist by carrying different
scope and subject identities. A specification mean never replaces its member
assessments. QB Consistency remains beside `SpecificationQualityProfile`; it is
not added as a fourth `CharacteristicId`, folded into C/V/U, or combined into a
scalar.

`M_cons[QB-v0.1]` quantifies confirmed conflict participation only inside the
approved exact quantitative-bound slice. Even a computed value of `1` is not
universal specification consistency. `CONFIRMED_CONFLICT` establishes the
supported logical incompatibility only; this contract separately decides
whether that already-confirmed problem is eligible for its bounded `R_DQ` rule.

## 6. M_v0.1 contract

M3-02 must introduce a conceptual `MetricProfile` containing immutable entries
with at least:

```text
MetricEntry
  metric_id
  scope: REQUIREMENT | SPECIFICATION
  subject_id
  value
  numeric_representation
  result_status
  applicability
  source_assessment_refs
  evidence_refs
  rule_refs
  artifact_id / artifact_version
  assessment_id / assessment_version
  explanation
```

The v0.1 registry is:

| Metric identity | Scope | Value representation | Source |
| --- | --- | --- | --- |
| `RQ.COMPLETENESS` | requirement | exact `Fraction` or absent | existing assessment |
| `RQ.VERIFIABILITY` | requirement | exact `Fraction` or absent | existing assessment |
| `RQ.UNAMBIGUITY` | requirement | exact `Fraction` or absent | existing assessment |
| `SPEC.MEAN_COMPLETENESS` | specification | exact `Fraction` or absent | existing aggregate |
| `SPEC.MEAN_VERIFIABILITY` | specification | exact `Fraction` or absent | existing aggregate |
| `SPEC.MEAN_UNAMBIGUITY` | specification | exact `Fraction` or absent | existing aggregate |
| `SPEC.QB_CONSISTENCY` | specification | exact `Fraction` or absent | `M_cons[QB-v0.1]` |

The adapter preserves the source status. Exact `Fraction` values remain
`Fraction`; quantitative bounds remain exact `Decimal` plus comparator, unit,
and context in evidence/features. Full Model v0.1 defines no common numeric
normalization. `UNKNOWN`, `NOT_APPLICABLE`, `UNRESOLVED`, `UNAVAILABLE`, or
`UNSUPPORTED` always has `value=None` and can never be converted to zero.

## 7. Evidence contract

### 7.1 Static evidence

`E_stat` reuses the existing immutable `Evidence`, extraction results,
requirement assessment trace, QB snapshot, cross-result evidence references,
diagnostics, and contract descriptors. It must resolve every reference back to
the unchanged source requirement text and exact span where such a span exists.
Completed absence remains a trace fact, not fabricated source evidence.

### 7.2 Dynamic evidence

The only v0.1 dynamic family is:

```text
Requirement -> QuantitativeCriterion -> Observation -> Conformance
```

Required fields are:

```text
criterion_id; requirement_id; artifact_id/version; metric_identity;
comparator; exact bound; unit; exact context identity; criterion evidence refs;
observation_id; observed exact value; observed unit/context; source kind;
collection_id/version; collected_at or deterministic fixture sequence;
conformance status; evaluator rule/version; explanation; provenance refs
```

The supported reference criterion is response time with comparator `<=`, unit
`SECOND`, and an exact normalized context already accepted by the quantitative
contract. The supported evaluator compares exact decimal values only when
metric identity, unit, and context match:

```text
observed_value <= criterion_bound -> CONFORMS
observed_value >  criterion_bound -> DOES_NOT_CONFORM
```

This comparison uses the requirement's own bound; it invents no threshold.
Missing observation is `UNAVAILABLE`, unresolved identity is `UNRESOLVED`, an
explicitly irrelevant criterion is `NOT_APPLICABLE`, and an unimplemented
comparator/unit/context conversion is `UNSUPPORTED`. None is negative
conformance. This is a fixture/provider boundary, not a test runner.

## 8. Reference product-quality characteristic

Full Model v0.1 selects **Performance Efficiency**.

The selection is a bounded software decision, not a claim that Performance
Efficiency is universally the most important characteristic. It provides the
clearest auditable path because:

- the dissertation explicitly maps response time, throughput, load, and
  resource constraints to Performance Efficiency;
- the repository already preserves response-time bounds, units, contexts,
  comparison evidence, and confirmed incompatible bounds;
- a response-time observation supplies a minimal dynamic evidence path; and
- exact criterion comparison needs no invented coefficient, natural-language
  heuristic, unit conversion, or quality threshold.

Supported relevant inputs are exact response-time quantitative constraints,
their existing C/V/U and QB assessments, and one controlled response-time
observation in the identical context.

Alternatives considered:

| Characteristic | Reason not selected for v0.1 |
| --- | --- |
| Functional Suitability | Expected-result evidence exists, but a bounded numeric observation and criterion comparison would require a new functional oracle contract. |
| Reliability | Requires duration, failure, recovery, or fault-injection semantics not present in the repository. |
| Security | Requires threat/control semantics and security verification beyond current evidence. |
| Compatibility / Interaction Capability | Requires external-system, user, or environment fixtures and new applicability rules. |
| Maintainability / Flexibility | Depends materially on architecture, code, change, or configuration evidence outside the reference slice. |
| Safety | Requires hazard, severity, and residual-risk semantics that are not calibrated or implemented. |

The v0.1 result covers one response-time criterion. It does not cover the full
Performance Efficiency characteristic or all its subcharacteristics.

## 9. X_j feature contract

`X_PE` is a named feature profile, not an anonymous normalized vector. It must
contain:

| Feature identity | Source | Role |
| --- | --- | --- |
| `PE.CRITERION.RESPONSE_TIME` | supported quantitative requirement evidence | Defines the reference target and context. |
| `PE.REQ.C` / `PE.REQ.V` / `PE.REQ.U` | requirement metric entries | Context and audit provenance only; never product-quality values. |
| `PE.SPEC.QB` | bounded QB metric and relevant cross results | Eligibility/uncertainty gate for the target context. |
| `PE.OBS.RESPONSE_TIME` | dynamic observation | Exact measured value and collection context. |
| `PE.CONFORMANCE.RESPONSE_TIME` | conformance evaluator | Direct input to the reference quality procedure. |

Each feature has identity, status, applicability, typed value, source metric or
evidence references, artifact/evidence version, and rule reference. A feature
unavailable at its process stage stays unavailable. Future-stage evidence must
not be backfilled into an earlier assessment. No missing feature is imputed.

If a QB conflict is on the same exact criterion key, `X_PE` preserves it and
the quality result for that contradictory target is `UNRESOLVED`; the evaluator
must not silently choose one bound. The M3-12 reference scenario may use a
separate unconflicted response-time criterion for its dynamic product-quality
observation while the confirmed conflict drives the risk/action path for the
same characteristic.

## 10. M_quality contract

M3-05 must implement a pure interface:

```text
assess_product_quality(X_PE, ModelVersion, ParameterSetVersion)
  -> ProductQualityAssessment
```

The result contains:

```text
assessment_id; characteristic_id; scope_statement; result_kind;
status; applicability; value; prediction_value; observed_value;
evidence_coverage; reliability; uncertainty; explanation;
feature_refs; evidence_refs; rule/model/parameter versions;
calibration_status; artifact/assessment versions; non_claims
```

The approved reference procedure `PE-OBS-CONFORMANCE-001/v1` is:

- `CONFORMS` -> `result_kind=OBSERVED_REFERENCE_INDICATOR`,
  `observed_value=Fraction(1,1)`;
- `DOES_NOT_CONFORM` -> the same kind with
  `observed_value=Fraction(0,1)`;
- unavailable, unresolved, unsupported, and not-applicable inputs propagate
  their status with no value.

`value` may expose the same exact observed indicator for generic consumers.
`prediction_value` and theoretical `y_hat_j` are always absent in v0.1 because
no calibrated predictive function has been approved. Evidence coverage is a
structured inventory of required/present channels, not an invented percentage.
Numeric evidence reliability and model uncertainty remain absent because the
baseline leaves their rules unresolved. Absence must be reported, not defaulted.

Every available result is labeled
`PROVISIONAL_NOT_CALIBRATED`. The binary value means only whether one observed
response-time measurement conforms to one supported criterion in one declared
context. It is not a probability, confidence, overall Performance Efficiency
score, prediction, or validated estimate.

Requirement quality remains the separate `RequirementQualityProfile` /
`SpecificationQualityProfile`. Predicted product quality remains reserved.
Observed product-quality evidence is the bounded result above. They must be
different types, headings, fields, and report sections.

## 11. Provisional parameter policy

Every parameter set or decision procedure not experimentally calibrated must
carry:

```text
parameter_set_id; version; entries; source_or_rationale;
calibration_status; scope; non_claim; approved_contract_ref
```

Allowed calibration statuses are:

- `EXPERIMENTALLY_CALIBRATED`;
- `PROVISIONAL_NOT_CALIBRATED`; and
- `EXPERIMENTAL_CALIBRATION_REQUIRED`.

No v0.1 result may use the first status. The reference quality and risk rules
use versioned parameter sets with no numeric empirical coefficients. Their
categorical/binary decision rules are still `PROVISIONAL_NOT_CALIBRATED`
because interpreting them at the product-characteristic/risk level has not been
experimentally validated.

Provisional status propagates from any input rule/parameter set to the quality
result, risk result, before/after comparison, user report, and audit report. A
consumer cannot relabel it. A new numeric coefficient, threshold, probability,
impact, weight, or class boundary requires a contract amendment and parameter
record before use.

## 12. Defect/problem contract

Full Model v0.1 distinguishes:

- `SIGNAL`: existing evidence-backed indication requiring no defect claim;
- `CONFIRMED_SUPPORTED_PROBLEM`: a problem conclusively established inside an
  approved bounded rule;
- `UNRESOLVED`: available information cannot confirm or reject the problem;
- `UNSUPPORTED`: the claim lies outside an implemented rule.

The sole `D_v0.1` eligibility rule is
`D-QB-CONFLICT-001/v1`: a QB cross result in state `CONFIRMED_CONFLICT`, class
`LOGICAL_CONFLICT`, subtype
`DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY` becomes a
`CONFIRMED_SUPPORTED_PROBLEM` referring to the specification artifact. The
problem record must retain problem ID, source cross-result ID, participants,
evidence/diagnostic references, snapshot, rule/coverage/non-claim contracts,
artifact and assessment versions, and explanation.

No C/V/U score, aggregate, completed absence, vague-term `SIGNAL`,
`ASSESSMENT_UNRESOLVED`, or `OUTSIDE_V0_1_APPLICABILITY` result is eligible.
This does not approve general `FindingKind.QUALITY_PROBLEM` conversion under
`RQD-016`.

## 13. D -> Q mapping contract

`R_DQ-PE-QB-001/v1` relates the eligible confirmed problem to Performance
Efficiency only when both operands use the exact supported response-time metric
identity and a complete equal unit/context comparison key. The relation stores:

```text
relation_id; problem_id; characteristic_id; relation_status;
rationale; source evidence/result refs; rule/version; artifact/assessment
versions; calibration_status; non_claim
```

The rationale is that incompatible response-time targets create a bounded risk
to specifying and verifying Performance Efficiency. The relation is
characteristic relevance, not probability, impact, causality, or proof that the
implemented product has poor performance. No synonym or wider semantic mapping
is inferred.

## 14. M_risk contract

M3-07 must implement a pure bounded classifier whose input retains the risk
subject, originating problem and requirements, `R_DQ` relation, affected
characteristic, product-quality result (including its status), evidence, and
versions.

The approved rule `RISK-PE-QB-001/v1` is:

```text
eligible CONFIRMED_SUPPORTED_PROBLEM
+ available R_DQ-PE-QB-001 relation
-> risk_classification = RISK_IDENTIFIED
```

The output has no numeric risk value. `likelihood`, `probability`, `impact`,
`severity`, and `priority` are absent. An unresolved problem/relation yields
`UNRESOLVED`; an unsupported relation yields `UNSUPPORTED`; an explicitly
inapplicable subject yields `NOT_APPLICABLE`; unavailable required input yields
`UNAVAILABLE`. None means zero risk.

The result includes status, classification, subject, problem/relation/quality
references, provenance, explanation, rule/model/parameter versions, and
`PROVISIONAL_NOT_CALIBRATED`. This is option A: an explicitly provisional
bounded reference classification. The dissertation product formula
`r_ij = rho_ij * p_ij * I_ij * kappa_j(C)` and aggregate `Psi_j` remain
`EXPERIMENTAL_CALIBRATION_REQUIRED` and are not executable in v0.1.

## 15. Corrective-action contract

`ACTION-RECONCILE-QB-001/v1` associates a `RISK_IDENTIFIED` result and its
problem with action kind `RECONCILE_QUANTITATIVE_BOUNDS`.

An action record includes action ID, target artifact and requirement IDs,
originating problem/relation/risk IDs, rationale, proposed change kind,
explicit replacement payload when supplied, status, provenance, rule/version,
creator/source, and lineage fields.

Statuses distinguish at least `PROPOSED`, `APPLIED`, `REJECTED`, `UNAVAILABLE`,
`UNRESOLVED`, and `NOT_APPLICABLE`. Creating a proposal never edits the source.
Applying it requires an explicit stakeholder- or fixture-supplied revision; the
system must not decide which conflicting bound expresses stakeholder intent.
Application creates `S(v2)` and preserves `S(v1)`. The action is a traceable
candidate, never a universally optimal correction.

## 16. Version and reassessment contract

The bounded transition is:

```text
S(v1) -> applied A_corr -> S(v2) -> ReEval
```

Required identities are:

- stable `artifact_id` and distinct immutable `artifact_version`;
- stable requirement lineage IDs plus version-local requirement IDs/text;
- `assessment_id` and `assessment_version`;
- full-model, rule, detector, aggregation, and coverage versions;
- evidence source/collection versions;
- parameter-set versions; and
- parent version, action ID, changed subjects, and reassessment predecessor.

Before/after comparisons are typed per result and may be `UNCHANGED`,
`INCREASED`, `DECREASED`, `STATE_CHANGED`, or `NOT_COMPARABLE`. These labels
describe structured values only. User wording may use “improved” or “worsened”
only when the property polarity and comparison contract explicitly authorize
that interpretation; product-quality causal improvement is never inferred.

Two assessments are not comparable when characteristic/metric identity,
scope/subject lineage, rule semantics, scale/value kind, required context,
process stage, or interpretation-relevant parameter version differs. A version
change alone is expected and does not make results incomparable. A changed
parameter version is comparable only when its record explicitly declares
semantic compatibility; otherwise `NOT_COMPARABLE`.

Evidence may be reused only when its source artifact/product version, context,
and applicability remain valid and the reuse is recorded. A requirement metric
increase does not prove real-world product-quality improvement. A risk
classification disappearing after conflict removal means only that the bounded
problem is no longer identified under the same rule.

## 17. Minimal M_process contract

Full Model v0.1 uses one bounded process stage,
`REFERENCE_VERIFICATION`, corresponding to dissertation stage `tau^T`, with
multiple specification versions. It is not a complete SDLC model.

`ProcessAssessmentState` is the software projection of `P_j(tau,v)` and must
associate:

```text
process_state_id; stage; artifact_id/version; assessment_id/version;
evidence availability and versions; requirement/specification assessments;
metric profile; X_PE; product-quality assessment; problem/relation; risk;
corrective action; predecessor/successor and reassessment lineage
```

The dynamic fixture is valid only at this stage. The state must preserve absent,
unavailable, unresolved, unsupported, and not-applicable associations. Process
integration invokes components but owns no assessment formula, action selection,
or reporting calculation.

## 18. Status model

Full Model components use this canonical semantic taxonomy while preserving
the exact source enum on imported baseline results:

| Canonical status | Meaning | Numeric value allowed? |
| --- | --- | --- |
| `AVAILABLE` | The declared bounded rule produced a usable value/classification. | Only when the result contract defines one. |
| `UNAVAILABLE` | The input is applicable/supported but not available at this stage/version. | No. |
| `UNKNOWN` | The approved source assessment cannot determine a value from available information. | No. |
| `UNRESOLVED` | Processing or a required scientific/semantic decision cannot determine a justified result. | No. |
| `UNSUPPORTED` | The requested case lies outside the implemented contract. | No. |
| `NOT_APPLICABLE` | An approved applicability rule excludes the case. | No. |

`PROVISIONAL_NOT_CALIBRATED` is an orthogonal calibration status, not a result
status. `APPLICABLE`/`UNKNOWN`/`NOT_APPLICABLE` criterion applicability also
remains orthogonal where the source contract uses it.

Compatibility mappings include:

| Existing state | Canonical interpretation |
| --- | --- |
| `CharacteristicAssessmentState.COMPUTED` | `AVAILABLE` with exact value |
| `CharacteristicAssessmentState.UNKNOWN` | `UNKNOWN` |
| `CharacteristicAssessmentState.NOT_APPLICABLE` | `NOT_APPLICABLE` |
| `DetectionStatus.DETECTED` / `NOT_DETECTED` | Processing observation, not pass/fail or a Full Model result status |
| `DetectionStatus.UNRESOLVED` | `UNRESOLVED` processing input |
| `QbConsistencyState.COMPUTED` | `AVAILABLE` within QB-v0.1 only |
| `QbConsistencyState.UNKNOWN` | `UNKNOWN` |
| `QbConsistencyState.NOT_APPLICABLE` | `NOT_APPLICABLE` |
| `CONFIRMED_CONFLICT` / `COMPATIBLE_WITHIN_RULE` | `AVAILABLE` bounded classifications |
| `ASSESSMENT_UNRESOLVED` | `UNRESOLVED` |
| `OUTSIDE_V0_1_APPLICABILITY` | `NOT_APPLICABLE` within QB-v0.1; no broader-world conclusion |

Downstream code must not collapse statuses for convenience. In particular,
`NOT_DETECTED` is not `NOT_APPLICABLE`, `UNAVAILABLE` is not negative evidence,
and `UNSUPPORTED` is not a pass.

## 19. Provenance contract

The minimum provenance chain is:

```text
Requirement -> Evidence -> Property -> Metric -> Feature
-> Product Quality -> Problem/Relation -> Risk
-> Corrective Action -> Reassessment
```

Every node has a stable ID, artifact/assessment version, producing rule/model
version, and direct parent references. Evidence nodes additionally preserve
source identity/version and exact span or controlled-observation record.
Metric and feature nodes point to their source assessment/evidence rather than
copying an unexplained value. Quality, risk, and action explanations enumerate
their inputs. Reassessment points to both assessment executions and the applied
action. Parameterized nodes cite a parameter-set version and calibration status.

Provenance continuity fails closed: a dangling reference, cross-version source
without an explicit validity link, mismatched snapshot, or incompatible
criterion/observation context makes the affected result `UNRESOLVED` or invalid;
it must not be silently repaired by reporting.

## 20. Component architecture and dependency rules

```text
reader -> extraction -> local calculators -> local profiles/aggregation
                                  \-> QB projection/comparison/aggregation
completed P results -> metric construction
criterion + observation -> dynamic evidence/conformance
metrics + evidence -> characteristic feature mapping
features -> product-quality assessment
confirmed problem -> D/Q relation -> risk classification
risk/problem -> corrective-action association
artifact/action versions -> reassessment/process history
all completed structured results -> user/audit reporting
```

Rules:

- extraction emits observations/evidence and never quality, risk, or actions;
- existing calculators continue to depend only on domain models;
- metric construction adapts completed assessments and never recalculates them;
- dynamic evidence is independent of CLI, files, and reporting;
- feature mapping does not assess product quality;
- quality assessment does not calculate requirement quality or risk;
- defect mapping does not calculate product quality or risk;
- risk does not select or apply corrective actions;
- action application creates artifact versions but does not reassess them;
- process/reassessment orchestrates typed components without absorbing their
  rules; and
- reporters consume completed structured results, never calculate, aggregate,
  infer status, select actions, or mutate state.

Domain contracts may be imported by services; services must not import CLI or
reporters. Reporting may import domain results but no model component may depend
on reporting. Circular dependencies are forbidden.

## 21. Dissertation-to-software traceability matrix

| Construct | Dissertation concept | v0.1 contract | Current foundation | M3 issue | Acceptance evidence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `S` | Versioned specification/artifacts | `SpecificationArtifact` and lineage | `Requirement`, reader order/source line | #146, #147, #149 | v1/v2 fixtures and lineage | `BOUNDED_V0.1_DECISION` |
| `P` | Requirement/specification properties | Existing C/V/U plus separate QB | profiles, aggregates, `SpecificationAssessment` | #139, #149 | unchanged source results | `EXISTING_APPROVED` |
| `M` | Metrics/indicators | exact-value `MetricProfile` adapter | `Fraction` assessments and QB result | #139 | adapter tests and registry | `BOUNDED_V0.1_DECISION` |
| `E_stat` | Static evidence | reuse existing evidence/traces | `Evidence`, assessment trace, QB resolver | #139, #141 | resolvable provenance | `EXISTING_APPROVED` |
| `E_dyn` | Dynamic observations | response-time criterion/observation/conformance | quantitative observation shapes | #140 | positive/negative/state tests | `BOUNDED_V0.1_DECISION` |
| `X_j` | characteristic-specific features | named `X_PE` profile | no current type | #141 | mapping table and fixture | `BOUNDED_V0.1_DECISION` |
| `M_quality` | `F_theta_j(X_j,C)` and result | observed reference indicator; no `y_hat` | theory only | #142 | exact conformance tests | `PROVISIONAL_NOT_CALIBRATED` |
| `D` | evidence-backed artifact defect | confirmed QB conflict only | `CrossRequirementResult` | #143 | eligibility/negative tests | `BOUNDED_V0.1_DECISION` |
| `R_DQ` | defect relevance to characteristic | exact response-time conflict -> PE | theory only | #143 | relation/rationale trace | `BOUNDED_V0.1_DECISION` |
| `M_risk` | local/aggregate risk | categorical `RISK_IDENTIFIED` only | theory formula, no calibrated inputs | #144 | classifier/state tests | `PROVISIONAL_NOT_CALIBRATED` |
| `A_corr` | corrective influence | reconcile-bounds proposal/application | theory action tuple | #145 | no-mutation and lineage tests | `BOUNDED_V0.1_DECISION` |
| `ReEval` | repeat after change | compatible rerun and typed comparison | no current lifecycle type | #146 | v1/v2 comparison | `BOUNDED_V0.1_DECISION` |
| `M_process` | `P_j(tau,v)` | one reference-verification stage | theory only | #147 | process history | `BOUNDED_V0.1_DECISION` |

## 22. Decision register

| ID | Question | Decision and rationale | Scientific status | Issues | Calibrated? | Blocking? |
| --- | --- | --- | --- | --- | --- | --- |
| `FM-D001` | Reference `q_j` | Performance Efficiency; existing response-time bounds plus direct observation form the smallest auditable path. | `BOUNDED_V0.1_DECISION` | #140-#149 | No | No after contract approval |
| `FM-D002` | `P_v0.1` set | Existing C/V/U requirement and aggregate results plus separate bounded QB Consistency only. | `EXISTING_APPROVED` | #139, #141 | N/A | No |
| `FM-D003` | Metric semantics | Lossless adapter; preserve exact `Fraction`, status, scope, provenance; no normalization. | `BOUNDED_V0.1_DECISION` | #139 | N/A | No |
| `FM-D004` | Dynamic evidence | Exact response-time `<=` criterion, same-unit/context observation, deterministic conformance. | `BOUNDED_V0.1_DECISION` | #140, #141 | No empirical parameter | No |
| `FM-D005` | Quality function | Use observed single-criterion `{0,1}` indicator; do not produce `y_hat`. | `PROVISIONAL_NOT_CALIBRATED` | #142 | No | No; broader prediction remains calibration work |
| `FM-D006` | Evidence coverage/reliability | Structured presence inventory only; no invented coverage percentage, reliability, or uncertainty. | `BOUNDED_V0.1_DECISION` plus `EXPERIMENTAL_CALIBRATION_REQUIRED` for numeric forms | #141, #142, #148 | No | Numeric use blocked |
| `FM-D007` | Eligible problem | Only exact QB `CONFIRMED_CONFLICT`; no SIGNAL/score promotion and no closure of RQD-016. | `BOUNDED_V0.1_DECISION` | #143 | N/A | No |
| `FM-D008` | D/Q relation | Exact response-time QB conflict relates to PE as bounded relevance, not causality. | `BOUNDED_V0.1_DECISION` | #143, #144 | No | No |
| `FM-D009` | Risk strategy | Categorical `RISK_IDENTIFIED`; no risk magnitude or formula operands. | `PROVISIONAL_NOT_CALIBRATED` | #144 | No | No; numeric risk blocked |
| `FM-D010` | Corrective action | Propose reconcile-bounds; externally supplied revision required for application. | `BOUNDED_V0.1_DECISION` | #145, #146 | N/A | No |
| `FM-D011` | Process stage | One `REFERENCE_VERIFICATION` / `tau^T` stage with multiple specification versions. | `BOUNDED_V0.1_DECISION` | #147 | N/A | No |
| `FM-D012` | Comparison | Compare only identity/semantics-compatible results; otherwise `NOT_COMPARABLE`. | `BOUNDED_V0.1_DECISION` | #146, #147 | N/A | No |
| `FM-D013` | Status model | Canonical six-state taxonomy with explicit mappings; provisional is orthogonal. | `BOUNDED_V0.1_DECISION` | #139-#149 | N/A | No |
| `FM-D014` | Predictive `F_theta`, coefficients, probabilities, impacts, reliability | Require experimental selection/calibration; absent from v0.1 execution. | `EXPERIMENTAL_CALIBRATION_REQUIRED` | future work, constraints on #142/#144 | No | Blocks those broader numeric claims only |
| `FM-D015` | Contract acceptance | Exact PR commit must receive researcher approval before downstream implementation. | `UNRESOLVED_BLOCKING` until issue #138 approval | #139-#149 | N/A | Yes, process gate only |

No semantic `UNRESOLVED_BLOCKING` decision remains inside the bounded reference
path. `FM-D015` records the required approval gate and is not permission for
downstream issues to begin before approval.

## 23. Claims and non-claims

Full Model v0.1 may claim that:

- one bounded path is deterministic, versioned, explainable, and auditable;
- existing C/V/U and QB results are preserved without semantic change;
- one exact response-time observation conforms or does not conform to one
  exact supported criterion in one declared context;
- one direct QB conflict is a confirmed supported specification problem;
- that problem has a bounded relevance relation to Performance Efficiency;
- the provisional rule identifies a risk presence and a traceable action kind;
- reassessment records structured changes under compatible rules; and
- all provisional and unavailable states remain visible.

It must not claim:

- universal requirement or specification quality;
- complete ambiguity, completeness, verifiability, or consistency detection;
- unqualified specification Consistency;
- that C/V/U or QB values are product-quality scores;
- a full or predicted Performance Efficiency value;
- coverage of all Performance Efficiency subcharacteristics or all nine
  ISO/IEC 25010 characteristics;
- experimentally validated prediction accuracy, weights, thresholds,
  probabilities, impacts, confidence, reliability, or risk magnitude;
- universal defect-to-quality causality;
- that absence of a bounded problem means absence of risk;
- that a corrective action is optimal; or
- that improved requirement metrics or reduced bounded risk prove real-world
  product-quality improvement.

## 24. Downstream acceptance map

| Issue | Must implement from this contract | Must not redefine |
| --- | --- | --- |
| M3-02 / #139 | Sections 5-6, 18-20: metric registry, lossless adapter, exact states/provenance. | P calculations, numeric scales, normalization, status meanings. |
| M3-03 / #140 | Section 7: criterion, observation, conformance, and state propagation. It may consume the supported quantitative criterion directly; it is not blocked on `MetricProfile`. | Test infrastructure, units/conversions, thresholds, missing-as-failure. |
| M3-04 / #141 | Sections 8-9 and 13: PE selection, `X_PE`, mapping table, temporal/status rules. | Characteristic selection, feature meaning, prediction, imputation. |
| M3-05 / #142 | Sections 10-11: observed reference indicator and structured product-quality result. | `y_hat`, weights, confidence/reliability numbers, full-characteristic claim. |
| M3-06 / #143 | Sections 12-13: QB conflict eligibility and exact `R_DQ` relation. | SIGNAL promotion, RQD-016, causal/probability claims. |
| M3-07 / #144 | Sections 11 and 14: provisional categorical risk classifier. | Numeric risk formula, likelihood, impact, severity, priority. |
| M3-08 / #145 | Section 15: proposed/applied action and explicit revision input. | Bound choice, automatic rewriting, optimality, silent mutation. |
| M3-09 / #146 | Section 16: lineage, rerun, compatibility, typed comparison. | Causal improvement semantics or comparison across incompatible contracts. |
| M3-10 / #147 | Section 17 and architecture rules: one-stage process history and associations. | Full SDLC, assessment/action/reporting business logic. |
| M3-11 / #148 | Sections 10-19 and 23: visibly separate structured user/audit views. | Calculation, aggregation, status inference, provisional relabeling. |
| M3-12 / #149 | Entire contract: one controlled end-to-end scenario and exact acceptance evidence. | New breadth, calibration claims, or closure of excluded research. |

M3-12 must demonstrate both paths within the same bounded characteristic: an
unconflicted response-time criterion for dynamic conformance/product-quality
evidence and an exact QB conflict for problem/risk/action/reassessment. This
keeps every transition auditable without choosing a contradictory target.

## Approval record

Approval must record reviewer/researcher identity, date, exact commit SHA,
decision (`APPROVED` or requested amendment), and any surviving blockers in
issue #138 or the pull request. Merge alone must not be interpreted as
experimental calibration. Until that record exists, this document remains a
normative candidate and M3-02 through M3-12 remain blocked by `FM-D015`.
