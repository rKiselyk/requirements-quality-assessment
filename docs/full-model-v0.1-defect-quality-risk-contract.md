# Full Model v0.1 Defect Quality and Risk Contract

**Contract ID:** `FULL-MODEL-V0.1-DEFECT-QUALITY-RISK`  
**Contract version:** `1`  
**Target issues:** `M3-06 / #143`, `M3-07 / #144`  
**Bounded characteristic:** `PERFORMANCE_EFFICIENCY`  
**Status:** `NORMATIVE_CANDIDATE / PARENT_CONTRACT_APPROVAL_REQUIRED`

## 1. Purpose and authority

This document defines the bounded, deterministic Full Model v0.1 path:

```text
P / Evidence -> D -> R_DQ -> PERFORMANCE_EFFICIENCY -> M_risk
```

It specifies:

- which existing result may become the sole v0.1 defect;
- how that defect is related to Performance Efficiency;
- how the relation is interpreted as categorical risk presence; and
- which richer dissertation risk quantities remain unavailable pending
  experimental calibration.

It does not implement M3-06 or M3-07, change any detector, create a general
problem taxonomy, close `RQD-016`, or calculate a numeric risk.

Normative precedence is:

1. `docs/full-model-v0.1-contract.md`;
2. this contract for M3-06 and M3-07;
3. the other focused Full Model v0.1 contracts;
4. the approved QB-v0.1 decision, architecture, reference-case, and
   implementation contracts;
5. `docs/model-spec.md`; and
6. dissertation Chapters 2-4 in `docs/reference/` as scientific context and
   traceability sources, not executable specifications.

This document inherits the parent decisions `FM-D007`, `FM-D008`, `FM-D009`,
`FM-D013`, `FM-D014`, and `FM-D015`. It does not reopen them.

## 2. Scientific basis

### 2.1 Requirement defects and signals

Dissertation Chapter 2 distinguishes observable textual or structural signs
from established defects. A linguistic smell may be a signal of potential
ambiguity, but context is required before treating it as proof. The existing
repository implements this distinction through detector observations and the
`FindingKind.SIGNAL` contract.

Chapter 2 also recognizes inconsistency as a specification-level property. A
direct contradiction exists when requirements impose mutually incompatible
states or constraints. The approved QB-v0.1 predicate is a particularly narrow
operationalization: two fully identified inclusive quantitative bounds on the
same bounded textual subject have an empty intersection.

### 2.2 Defect-to-quality relation

Dissertation Chapter 2 separates three mechanisms:

- a semantic mechanism, where requirement content defines a quality target;
- a risk-mediated mechanism, where an artifact defect may create risk for one
  or more product-quality characteristics; and
- a verification/traceability mechanism, where artifacts affect the ability
  to demonstrate conformance.

The dissertation explicitly warns that a requirement defect is not a direct
numeric equivalent of product quality and does not prove a product defect or
causal effect. Its relevance and effect depend on the affected characteristic
and context.

### 2.3 Risk model

Dissertation Chapter 4 defines an evidence-backed defect record and a richer
risk model containing, among other quantities:

```text
rho_ij, p_ij, I_ij, kappa_j(C), r_ij, Psi_j, Risk_j, Pi_i
```

It states that a requirement defect is an artifact deficiency that may
increase the risk of failing or incorrectly realizing a quality
characteristic. It is not a guaranteed cause of implemented software failure.
Probability, impact, aggregation, prioritization, uncertainty, and action
effects require data, expert rules, or calibration; absent statistics must not
be replaced by invented precise values.

The bounded v0.1 contract therefore implements only the risk-identification
stage. It does not implement risk analysis, magnitude estimation, evaluation,
aggregation, or prioritization.

## 3. Formal distinctions

The following objects are different types and must never be collapsed:

| Object | Scientific meaning | Current/bounded example | What it does not mean |
| --- | --- | --- | --- |
| Detector observation | Typed primary output that a detector accepted, rejected, or could not resolve, with Evidence and processing state | quantitative observation; vague-term occurrence; `DETECTED`, `NOT_DETECTED`, `UNRESOLVED` | finding, score, defect, or risk |
| `SIGNAL` | Evidence-backed indication requiring interpretation | `FIND-U-VAGUE-001 / VAGUE_TERM_SIGNAL` | confirmed ambiguity, `QUALITY_PROBLEM`, member of `D`, or risk |
| Assessment result | Rule-governed interpretation at its own layer | C/V/U assessment, QB cross result, QB aggregate, conformance, product-quality result | automatic defect or risk merely because its value/state is unfavorable |
| Confirmed supported problem | A problem conclusively established within one approved bounded Full Model rule | exact QB `CONFIRMED_CONFLICT` admitted by `D-QB-CONFLICT-001 / 1` | general `Finding(kind=QUALITY_PROBLEM)`, universal inconsistency, or product failure |
| Defect `D` | The ordered v0.1 population of admitted confirmed supported specification problems | `D_v0.1` contains only eligible QB conflict problem records | detector outputs, signals, scores, unresolved candidates, or product defects |
| Unresolved potential problem | Available information cannot confirm or reject the bounded problem claim | QB `ASSESSMENT_UNRESOLVED` projected as `UNRESOLVED` with no problem record | confirmed conflict, no-problem conclusion, or zero risk |
| Unsupported claim | A requested problem/risk interpretation has no approved rule in this contract | promoting a vague-term signal, C/V/U score, completed absence, or another conflict class into `D` | false claim, not-applicable case, or evidence of safety |

### 3.1 Detector state is not problem state

The existing detection meanings remain binding:

- `DETECTED` means an accepted observation exists;
- `NOT_DETECTED` means the approved detector did not find that observation
  after its declared processing;
- `UNRESOLVED` means the detector could not determine the candidate result.

None automatically supplies applicability, failure, `QUALITY_PROBLEM`, defect,
or risk. Diagnostics remain diagnostics and do not become evidence or problems.

### 3.2 SIGNAL is not D

The only existing finding rule, `FIND-U-VAGUE-001`, emits
`FindingKind.SIGNAL`. Its finding is a potential ambiguity indicator and remains
unchanged. It is never an input to `D-QB-CONFLICT-001 / 1`, `R_DQ-PE-QB-001 / 1`,
or `RISK-PE-QB-001 / 1`.

### 3.3 Assessment result is not defect by polarity

The following cannot enter `D` merely because their value or state might look
unfavorable:

- a C/V/U `Fraction`, including zero;
- a C/V/U or specification aggregate `UNKNOWN`;
- `M_cons[QB-v0.1]`, including `Fraction(0,1)`;
- `DOES_NOT_CONFORM` dynamic evidence;
- an observed product-quality indicator `Fraction(0,1)`;
- a QB `ASSESSMENT_UNRESOLVED`; or
- a QB `OUTSIDE_V0_1_APPLICABILITY`.

Only the source result and rule combination in Section 6 is eligible.

## 4. Bounded scope

This contract covers only:

- specification-level direct quantitative-bound incompatibility already
  established by QB-v0.1;
- the exact response-time Performance Efficiency mapping fixed by the Full
  Model reference slice;
- the `REFERENCE_VERIFICATION` process stage;
- categorical `RISK_IDENTIFIED`; and
- explicit non-available and non-applicable states.

It excludes:

- any new detector or grammar;
- promotion of C/V/U findings or score states;
- general ambiguity, incompleteness, unverifiability, traceability, duplicate,
  feasibility, volatility, or terminology defects;
- product defects and runtime failures;
- indirect, synonym-based, ontology-based, or cross-characteristic mappings;
- numeric defect severity or detection confidence;
- numeric relevance, probability, likelihood, impact, criticality, risk,
  uncertainty, aggregation, priority, or action utility; and
- automatic corrective-action selection or application.

## 5. Closed rule and model identities

The bounded path uses exactly:

```text
problem eligibility rule = D-QB-CONFLICT-001 / 1
relation rule            = R_DQ-PE-QB-001 / 1
risk model               = FULL-MODEL-V0.1-M-RISK-PE-QB / 1
risk classifier rule     = RISK-PE-QB-001 / 1
risk parameter set       = RISK-PE-QB-001-PARAMETERS / 1
```

The problem and relation rules contain no empirical numeric parameters. The
risk parameter set has the record:

```text
ParameterSet
  parameter_set_id: RISK-PE-QB-001-PARAMETERS
  version: 1
  entries: ()
  source_or_rationale: parent Full Model categorical reference rule
  calibration_status: PROVISIONAL_NOT_CALIBRATED
  scope: presence of one bounded PE-related specification risk scenario
  non_claim: no probability, impact, magnitude, severity, or priority
  approved_contract_ref: FULL-MODEL-V0.1-CONTRACT / 1
```

The response-time bounds are source evidence, not parameters. Adding a numeric
entry requires a separately approved contract and parameter-set version.

All `*Ref` types in this document are immutable value references to an existing
record ID plus its explicit version and subject/snapshot qualification where
applicable. In particular:

```text
ProblemClaimResolutionRef(resolution_id)
ConfirmedSupportedProblemRef(problem_id)
DefectPopulationSnapshotRef(population_id)
DefectQualityRelationRef(relation_id)
ProductQualityAssessmentRef(assessment_id,
                            product_quality_assessment_version)
RiskAssessmentEventRef(event_id, event_version, artifact_ref, process_state_ref)
```

A reference must resolve to the exact record whose identity fields it names.
It is not a display label or permission to join records by matching text.

## 6. Problem claim resolution

### 6.1 Pure boundary

```text
resolve_problem_claim(
  source_claim: TypedProblemClaimSource,
  context: DefectConstructionContext,
) -> ProblemClaimResolution
```

The operation performs no detection, extraction, C/V/U calculation, QB
reassessment, product-quality assessment, or risk classification.

### 6.2 DefectConstructionContext

```text
DefectConstructionContext
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  process_state_ref: ProcessStateRef
  full_model_contract_ref: ContractRef
  defect_risk_contract_ref: ContractRef
  problem_rule_ref: D-QB-CONFLICT-001 / 1
```

Every identity and version is supplied explicitly. The resolver must not infer
them from text, file names, timestamps, ordering, or object addresses.

Every `process_state_ref` in this contract is the caller-allocated context
identity reserved before component execution under the process/reassessment
contract. It is not a dependency on an already assembled
`ProcessAssessmentState`; later assembly associates the completed problem,
relation, and risk records with that same identity.

### 6.3 ProblemClaimResolution

```text
ProblemClaimResolution
  resolution_id: ProblemClaimResolutionId
  source_claim_ref: TypedSourceRef
  status: FullModelStatus
  applicability: Applicability
  disposition:
    CONFIRMED_SUPPORTED_PROBLEM |
    NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE |
    None
  problem: ConfirmedSupportedProblem | None
  explanation: str
  reasons: tuple[ProblemResolutionReason, ...]
  evidence_refs: tuple[EvidenceRef, ...]
  provenance_refs: tuple[ProvenanceRef, ...]
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  rule_ref: RuleRef
```

Allowed shapes are:

| Status/applicability | Disposition | Problem |
| --- | --- | --- |
| `AVAILABLE/APPLICABLE` | `CONFIRMED_SUPPORTED_PROBLEM` | exactly one record |
| `AVAILABLE/APPLICABLE` | `NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE` | `None` |
| `UNRESOLVED/APPLICABLE` or `UNRESOLVED/UNKNOWN` | `None` | `None` |
| `UNSUPPORTED/APPLICABLE` or `UNSUPPORTED/UNKNOWN` | `None` | `None` |
| `NOT_APPLICABLE/NOT_APPLICABLE` | `None` | `None` |
| `UNAVAILABLE/APPLICABLE` or `UNAVAILABLE/UNKNOWN` | `None` | `None` |
| `UNKNOWN/APPLICABLE` or `UNKNOWN/UNKNOWN` | `None` | `None` |

`NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE` is not a claim that no defect or
risk exists outside this one rule.

```text
ProblemClaimResolutionId = (
  artifact_ref,
  source_assessment_ref,
  source_snapshot_id,
  source_claim_ref,
  problem_rule_ref,
)
```

The resolution identity exists independently of a positive problem, so every
non-positive state remains stable without a fabricated problem ID.

## 7. Exact D eligibility

### 7.1 Sole positive rule

A source claim enters `D_v0.1` if and only if it is a valid QB-v0.1
`CrossRequirementResult` satisfying all of these conditions:

1. state is `CONFIRMED_CONFLICT`;
2. conflict class is `LOGICAL_CONFLICT`;
3. subtype is `DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY`;
4. the QB comparison key is complete;
5. both requirement participants and both observation references resolve in
   the same immutable QB snapshot;
6. exact Decimal operands, comparator, inclusivity, unit, normalized metric,
   and normalized context satisfy the QB-v0.1 conflict predicate;
7. ordered evidence and required diagnostic references resolve;
8. QB coverage/comparison/non-claim contract descriptors are present; and
9. artifact, assessment, snapshot, and rule versions agree with the
   construction context.

The resolver does not repeat the interval predicate. It validates and consumes
the completed QB assessment result.

The specification-level QB aggregate state or Fraction is not an additional
eligibility operand. A fully proven individual `CONFIRMED_CONFLICT` remains an
eligible problem when the aggregate is `UNKNOWN` because another comparison or
material extraction path is unresolved. The aggregate state, incomplete
population, and unresolved refs remain visible in provenance; the conflict does
not make the overall defect population complete.

### 7.2 Negative and non-positive cases

| Source | Problem resolution |
| --- | --- |
| QB `COMPATIBLE_WITHIN_RULE` | `AVAILABLE/APPLICABLE`, `NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE` |
| QB `ASSESSMENT_UNRESOLVED` | `UNRESOLVED`; no problem |
| QB `OUTSIDE_V0_1_APPLICABILITY` | `NOT_APPLICABLE`; no problem |
| supported source not yet produced for the stated version | `UNAVAILABLE`; no problem |
| future approved source state `UNKNOWN` | preserve `UNKNOWN`; no problem |
| C/V/U score, aggregate, completed absence, detector observation, diagnostic, `SIGNAL`, conformance result, or product-quality result | `UNSUPPORTED`; no problem |
| another conflict class/subtype or a request for a broader semantic defect | `UNSUPPORTED`; no problem |

Malformed identities, impossible source-state fields, foreign evidence,
cross-snapshot composition, or a source result whose content contradicts its ID
are invalid input. They fail construction and are not converted into a
scientific absence state.

## 8. ConfirmedSupportedProblem and D

### 8.1 Record contract

```text
ConfirmedSupportedProblem
  problem_id: ConfirmedSupportedProblemId
  problem_kind: CONFIRMED_SUPPORTED_PROBLEM
  defect_type: SPECIFICATION_INCONSISTENCY
  conflict_class: LOGICAL_CONFLICT
  conflict_subtype: DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY
  target_ref: SpecificationSubjectRef
  participant_refs: tuple[RequirementSubjectRef, RequirementSubjectRef]
  source_cross_result_ref: CrossRequirementResultRef
  source_observation_refs: tuple[CrossObservationRef, CrossObservationRef]
  comparison_key: QbComparisonKey
  operand_refs: tuple[QbBoundOperandRef, QbBoundOperandRef]
  status: AVAILABLE
  applicability: APPLICABLE
  evidence_refs: tuple[CrossEvidenceRef, ...]
  diagnostic_refs: tuple[DiagnosticRef, ...]
  explanation: str
  provenance: ConfirmedProblemProvenance
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  process_state_ref: ProcessStateRef
  rule_ref: D-QB-CONFLICT-001 / 1
  non_claims: tuple[ProblemNonClaim, ...]
```

The record contains no severity, confidence score, probability, likelihood,
impact, criticality, priority, product-quality value, or corrective action.
Categorical confirmation under an exact logical predicate is not numeric
`conf_i = 1` and must not be serialized as such.

### 8.2 Problem identity

```text
ConfirmedSupportedProblemId = (
  artifact_ref,
  source_assessment_ref,
  source_snapshot_id,
  source_cross_result_ref,
  problem_rule_ref,
)
```

The source cross-result ID remains authoritative. A changed artifact,
assessment, snapshot, source result, or rule produces a different problem ID.
No hash is required.

### 8.3 D population

```text
D_v0.1 = tuple[ConfirmedSupportedProblem, ...]
```

Although the dissertation writes `D` as a mathematical set, software uses an
ordered immutable tuple. Problems are ordered by their source QB cross-result
order. Duplicate source cross-result references are invalid. No sorting by
bound, metric text, severity, participant text, or later risk state is allowed.

Only `ProblemClaimResolution` values with the positive disposition contribute
members. An unresolved potential problem, unsupported claim, signal, or
compatible result never creates a placeholder member.

### 8.4 Defect population snapshot

Software must preserve whether the observed `D_v0.1` members form a complete
bounded population:

```text
DefectPopulationSnapshot
  population_id: DefectPopulationId
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  status: FullModelStatus
  applicability: Applicability
  members: tuple[ConfirmedSupportedProblemRef, ...]
  population_complete: bool
  problem_resolution_refs: tuple[ProblemClaimResolutionRef, ...]
  unresolved_resolution_refs: tuple[ProblemClaimResolutionRef, ...]
  source_qb_assessment_ref: QbConsistencyAssessmentRef
  provenance_refs: tuple[ProvenanceRef, ...]
  rule_ref: D-QB-CONFLICT-001 / 1
```

```text
DefectPopulationId = (
  artifact_ref,
  source_assessment_ref,
  source_snapshot_id,
  problem_rule_ref,
)
```

The population decision preserves the source universe:

- complete source comparison/materiality processing -> `AVAILABLE`,
  `population_complete=true`; the member tuple may be empty;
- one or more unresolved cross-result claims -> `UNRESOLVED`,
  `population_complete=false`, while already confirmed members remain;
- source aggregate/materiality `UNKNOWN` without a resolved claim for every
  potentially eligible comparison -> `UNKNOWN`, `population_complete=false`;
- supported source assessment not produced -> `UNAVAILABLE`, incomplete;
- a source universe where QB-v0.1 is explicitly not applicable ->
  `NOT_APPLICABLE/NOT_APPLICABLE`, complete empty members.

An individual confirmed member may feed its relation and risk path even when
the population is incomplete, because its own proof is closed and immutable.
That risk result must retain the incomplete population status and must not
claim that all specification problems have been found.

## 9. RQD-016 boundary

`RQD-016` remains:

```text
FINDING_AND_SIGNAL_CONTRACT_APPROVED /
QUALITY_PROBLEM_CONVERSION_OPEN
```

This contract does not add an existing-model
`Finding(kind=QUALITY_PROBLEM)`. `ConfirmedSupportedProblem` is a distinct Full
Model cross-requirement specification-level type produced from an already completed QB
cross-requirement assessment, not from a detector observation or C/V/U
finding.

Consequently:

- `FIND-U-VAGUE-001` remains `SIGNAL` only;
- no detector observation becomes a `QUALITY_PROBLEM`;
- no C/V/U absence or numeric contribution becomes a problem;
- no criterion ID or rule is allocated for a C/V/U `QUALITY_PROBLEM`;
- the existing `FindingKind` semantics and reporters remain unchanged; and
- future general observation-to-problem conversion still requires a separate
  researcher decision under `RQD-016`.

The bounded QB problem rule does not serve as precedent for another finding
family.

## 10. Scientific review of the sole D decision

The sole-positive-input decision is scientifically consistent with the
dissertation because the QB result establishes all facts needed for the
dissertation's contradiction defect class:

- the problem belongs to a versioned specification artifact;
- two distinct requirement participants are identified;
- both operands and their exact evidence are preserved;
- the constrained subject, context, and unit are identical under the approved
  narrow key;
- the comparator semantics are complete; and
- the admissible sets have an empty intersection under an exact predicate.

This is stronger than a heuristic indication. Calling it a confirmed supported
specification problem does not require a learned threshold, weight, confidence
score, or expert inference.

It is sufficient for the reference vertical slice because a response-time
instance can be mapped by an exact relation to Performance Efficiency and then
to one categorical risk-identification result. It is not sufficient for a
general defect model. `D_v0.1` is intentionally incomplete, and an empty
`D_v0.1` must never be reported as a defect-free specification or zero risk.

## 11. Bounded D to q relation

### 11.1 Pure interface

```text
relate_problem_to_quality(
  problem_resolution: ProblemClaimResolution,
  relation_context: DefectQualityRelationContext,
) -> DefectQualityRelation
```

The operation does not calculate product quality, risk, or another defect. It
does not inspect C/V/U scores or product conformance to decide relevance.

```text
DefectQualityRelationContext
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  process_state_ref: ProcessStateRef
  full_model_contract_ref: ContractRef
  defect_risk_contract_ref: ContractRef
  relation_rule_ref: R_DQ-PE-QB-001 / 1
```

All fields must agree with the problem resolution and, when present, the
confirmed problem.

### 11.2 Exact reference key

The sole available relation requires the same bounded identity used by the
Performance Efficiency reference path:

```text
normalized metric  = "час відгуку"
normalized context = "при 500 одночасних користувачах"
unit               = SECOND
normalization      = QB-NORMALIZATION / 1
characteristic     = PERFORMANCE_EFFICIENCY
```

Both conflict operands must carry this identical complete comparison key. The
mapper must not infer synonyms, translate, convert units, broaden the context,
or infer characteristic relevance from a similar phrase.

### 11.3 Relation meaning

The relation's sole available classification is:

```text
BOUNDED_RISK_RELEVANCE
```

Its rationale is:

> Mutually incompatible response-time targets for the same exact unit and
> context create a bounded risk to selecting, implementing, and verifying an
> authoritative Performance Efficiency target.

The relation asserts characteristic relevance only. It does not assign a
numeric dissertation `rho_ij`, and its presence must not be serialized or
interpreted as `rho_ij = 1`.

## 12. DefectQualityRelation contract

```text
DefectQualityRelation
  relation_id: DefectQualityRelationId
  problem_resolution_ref: ProblemClaimResolutionRef
  problem_ref: ConfirmedSupportedProblemRef | None
  characteristic_id: PERFORMANCE_EFFICIENCY
  relation_kind: BOUNDED_RISK_RELEVANCE | None
  status: FullModelStatus
  applicability: Applicability
  rationale: str
  reasons: tuple[RelationReason, ...]
  source_result_refs: tuple[TypedSourceRef, ...]
  evidence_refs: tuple[CrossEvidenceRef, ...]
  provenance: DefectQualityRelationProvenance
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  process_state_ref: ProcessStateRef
  rule_ref: R_DQ-PE-QB-001 / 1
  calibration_status: PROVISIONAL_NOT_CALIBRATED
  non_claims: tuple[RelationNonClaim, ...]
```

### 12.1 Relation identity

```text
DefectQualityRelationId = (
  problem_resolution_ref,
  problem_ref_or_none,
  PERFORMANCE_EFFICIENCY,
  relation_rule_ref,
)
```

The identity includes the resolution reference so a non-available or
non-applicable result remains stable without fabricating a problem ID.

### 12.2 Status and applicability

| Input condition | Relation status/applicability | Relation kind |
| --- | --- | --- |
| available confirmed problem with the exact Section 11.2 key | `AVAILABLE/APPLICABLE` | `BOUNDED_RISK_RELEVANCE` |
| available `NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE` | `NOT_APPLICABLE/NOT_APPLICABLE` | `None` |
| confirmed QB problem with a resolved different metric | `NOT_APPLICABLE/NOT_APPLICABLE` | `None` |
| confirmed problem using exact response-time metric but another unit or context | `UNSUPPORTED/APPLICABLE` | `None` |
| unresolved potential problem or unresolved required identity/provenance | `UNRESOLVED/APPLICABLE` or `UNRESOLVED/UNKNOWN` | `None` |
| unsupported problem claim | `UNSUPPORTED` with source applicability preserved | `None` |
| unavailable problem input | `UNAVAILABLE` with source applicability preserved | `None` |
| future approved `UNKNOWN` input | `UNKNOWN` with source applicability preserved | `None` |

A confirmed problem's comparison key is complete by QB invariant. A missing key
on such a record is invalid input, not relation `UNRESOLVED`.

### 12.3 Evidence and provenance

An available relation preserves, by reference:

- the problem and source cross-result;
- both requirement subjects and observation operands;
- both exact Decimal bounds, comparators, inclusivity, unit, normalized metric,
  and normalized context;
- all ordered cross-evidence and relevant diagnostic references;
- QB coverage, normalization, comparison, and non-claim contracts;
- artifact, assessment, snapshot, process, problem-rule, and relation-rule
  versions; and
- the exact structured rationale and non-causal limitations.

It creates no replacement evidence and no product observation.

## 13. Non-causal interpretation

`R_DQ-PE-QB-001 / 1` does not claim that the confirmed conflict:

- caused slow response time;
- caused any implemented product defect;
- caused an observed nonconformance;
- has a known probability or impact;
- necessarily affects every implementation;
- is the only Performance Efficiency risk; or
- proves low Performance Efficiency.

The mapping is a bounded, rule-backed relevance statement between a
specification inconsistency and the ability to specify and verify one
Performance Efficiency target. It is compatible with the dissertation's
risk-mediated mechanism and its explicit warning that causality requires
empirical validation.

## 14. Scientific review of RISK_IDENTIFIED

The categorical strategy is valid only when interpreted as risk
identification, not risk quantification.

The exact conflict supplies an established artifact deficiency. The available
`R_DQ` relation supplies a characteristic-specific risk scenario. Together
they justify recording that a bounded risk is present for management and
traceability. They do not provide the operands required by the dissertation's
local risk equation.

The v0.1 classification therefore means:

> A confirmed contradiction in the exact Performance Efficiency response-time
> target creates an identified risk that specification, implementation, or
> verification may proceed against no single justified target.

It does not mean that an adverse product outcome is probable, severe, critical,
high priority, or of any particular magnitude. The term `IDENTIFIED` names the
existence of the bounded scenario, not the result of risk analysis or
evaluation.

## 15. Bounded risk input contract

```text
BoundedRiskAssessmentInput
  input_id: BoundedRiskAssessmentInputId
  subject: SpecificationRiskSubject
  problem_resolution_ref: ProblemClaimResolutionRef
  problem_ref: ConfirmedSupportedProblemRef | None
  defect_population_ref: DefectPopulationSnapshotRef
  defect_population_status: FullModelStatus
  relation_ref: DefectQualityRelationRef
  characteristic_id: PERFORMANCE_EFFICIENCY
  product_quality_context: ProductQualityContext
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  process_state_ref: ProcessStateRef
  evidence_refs: tuple[EvidenceRef, ...]
  provenance_refs: tuple[ProvenanceRef, ...]
```

```text
SpecificationRiskSubject
  artifact_ref: ArtifactRef
  participant_refs: tuple[RequirementSubjectRef, RequirementSubjectRef] | ()
  affected_characteristic_id: PERFORMANCE_EFFICIENCY
```

```text
ProductQualityContext
  assessment_ref: ProductQualityAssessmentRef
  status: FullModelStatus
  applicability: Applicability
  result_kind: OBSERVED_REFERENCE_INDICATOR
  scope_ref: ProductQualityScopeRef
  product_ref: ProductRef
```

```text
BoundedRiskAssessmentInputId = (
  subject,
  problem_resolution_ref,
  defect_population_ref,
  relation_ref,
  product_quality_context.assessment_ref,
  process_state_ref,
)
```

The complete product-quality result, including its status and non-claims,
remains reachable through `assessment_ref`. It is context/provenance only for
`RISK-PE-QB-001 / 1`:

- `CONFORMS` does not clear the specification risk;
- `DOES_NOT_CONFORM` does not increase or quantify it; and
- `UNAVAILABLE`, `UNKNOWN`, `UNRESOLVED`, `UNSUPPORTED`, or
  `NOT_APPLICABLE` product-quality status does not change the categorical rule.

A valid `ProductQualityContext` is structurally required by the parent Full
Model input shape. The referenced assessment may have any valid status. A
missing, dangling, or cross-version assessment reference is invalid input, not
permission to omit the context or invent a scientific result.

For the parent rule that an unavailable required input yields `UNAVAILABLE`,
the required decision inputs are the problem resolution/problem and relation.
A present, valid product-quality assessment whose own scientific status is
`UNAVAILABLE` is not a missing decision input; it is an explicitly unavailable
context result and remains visible as such.

## 16. Bounded risk result contract

```text
BoundedRiskAssessment
  risk_assessment_id: BoundedRiskAssessmentId
  assessment_event_ref: RiskAssessmentEventRef
  subject: SpecificationRiskSubject
  characteristic_id: PERFORMANCE_EFFICIENCY
  status: FullModelStatus
  applicability: Applicability
  classification: RISK_IDENTIFIED | None
  risk_statement: str
  explanation: str
  problem_resolution_ref: ProblemClaimResolutionRef
  problem_ref: ConfirmedSupportedProblemRef | None
  defect_population_ref: DefectPopulationSnapshotRef
  defect_population_status: FullModelStatus
  relation_ref: DefectQualityRelationRef
  product_quality_context: ProductQualityContext
  evidence_refs: tuple[EvidenceRef, ...]
  provenance: BoundedRiskProvenance
  model_ref: FULL-MODEL-V0.1-M-RISK-PE-QB / 1
  rule_ref: RISK-PE-QB-001 / 1
  parameter_set_ref: RISK-PE-QB-001-PARAMETERS / 1
  calibration_status: PROVISIONAL_NOT_CALIBRATED
  artifact_ref: ArtifactRef
  source_assessment_ref: AssessmentRef
  source_snapshot_id: AssessmentSnapshotId
  process_state_ref: ProcessStateRef
  non_claims: tuple[RiskNonClaim, ...]
```

There is no numeric `value` field. The schema has no probability, likelihood,
impact, severity, criticality, weight, threshold, aggregate risk, confidence,
uncertainty, priority, rank, or recommended action field.

### 16.1 Risk identity

```text
BoundedRiskAssessmentId = (
  assessment_event_ref,
  subject,
  problem_resolution_ref,
  defect_population_ref,
  relation_ref,
  product_quality_context.assessment_ref,
  model_ref,
  rule_ref,
  parameter_set_ref,
)
```

`RiskAssessmentEventRef` is a caller-supplied versioned evaluation-event
identity, not the output ID. This keeps the result identity non-circular.

### 16.2 Sole positive rule

```text
problem resolution = AVAILABLE / CONFIRMED_SUPPORTED_PROBLEM
+ problem status    = AVAILABLE
+ relation status   = AVAILABLE
+ relation kind     = BOUNDED_RISK_RELEVANCE
-> risk status      = AVAILABLE
-> applicability    = APPLICABLE
-> classification   = RISK_IDENTIFIED
```

No numeric calculation occurs.

## 17. Risk state propagation

After structural validation, the classifier applies this order:

1. problem resolution `NOT_APPLICABLE` or
   `NO_CONFIRMED_SUPPORTED_PROBLEM_WITHIN_RULE` ->
   `NOT_APPLICABLE/NOT_APPLICABLE`, no classification;
2. problem resolution `UNAVAILABLE`, `UNKNOWN`, `UNRESOLVED`, or `UNSUPPORTED`
   -> copy its status/applicability, no classification;
3. missing positive problem despite a positive disposition -> invalid input;
4. relation `NOT_APPLICABLE`, `UNAVAILABLE`, `UNKNOWN`, `UNRESOLVED`, or
   `UNSUPPORTED` -> copy its status/applicability, no classification;
5. available problem and available bounded relation ->
   `AVAILABLE/APPLICABLE/RISK_IDENTIFIED`.

No status maps to numeric zero. In particular:

- no eligible problem is not proof of no risk;
- `UNRESOLVED` is not low risk;
- `UNSUPPORTED` is not safe;
- `NOT_APPLICABLE` is not zero risk outside the bounded rule;
- `UNAVAILABLE` is not negative evidence; and
- `RISK_IDENTIFIED` is not a magnitude.

The product-quality context does not participate in the decision precedence,
but its exact status is preserved in the result and explanation.

The defect-population status likewise does not invalidate an individually
confirmed problem. It is preserved to disclose whether other potential
problems remain unresolved; it cannot change or scale `RISK_IDENTIFIED` for the
closed member proof.

## 18. Theoretical quantities requiring calibration

The following dissertation quantities are not executable Full Model v0.1
fields or calculations:

| Theoretical quantity | Meaning | v0.1 disposition |
| --- | --- | --- |
| `sev_i` | local severity of the requirement defect | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `conf_i` | confidence/reliability of defect detection | `EXPERIMENTAL_CALIBRATION_REQUIRED`; categorical logical confirmation is not a numeric substitute |
| `rho_ij` | degree of defect relevance to characteristic | `EXPERIMENTAL_CALIBRATION_REQUIRED`; the categorical relation is not `rho_ij=1` |
| `p_ij` | probability of an adverse consequence | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `I_ij` | potential impact magnitude | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `kappa_j(C)` | contextual criticality | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `r_ij` | local risk magnitude | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `Psi_j` | local-risk aggregation operator | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `Risk_j` | aggregate characteristic risk | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `G_D` / `Dep_j` | defect dependency/causal structure used for aggregation | `EXPERIMENTAL_CALIBRATION_REQUIRED` for causal or aggregation use |
| `Pi_i` components | risk, confidence, business priority, centrality, spread, cost, stage | `EXPERIMENTAL_CALIBRATION_REQUIRED` for prioritization; no v0.1 vector |
| `Priority_theta(Pi_i)` | scalar or ordered priority | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| `TopD_j` | highest-contributing defects | `EXPERIMENTAL_CALIBRATION_REQUIRED`; no contribution values exist |
| `Unc_j` | risk-model uncertainty | `EXPERIMENTAL_CALIBRATION_REQUIRED` |
| corrective-action effect | expected or realized risk reduction | `EXPERIMENTAL_CALIBRATION_REQUIRED` and outside M3-07 |

The product formula:

```text
r_ij = rho_ij * p_ij * I_ij * kappa_j(C)
```

and aggregate:

```text
Risk_j = Psi_j({r_ij}, Dep_j)
```

remain theoretical only. No operand is defaulted to `0`, `1`, or an expert
guess. No partial multiplication is performed.

## 19. Provenance

### 19.1 Problem provenance

```text
ConfirmedProblemProvenance
  source_cross_result_ref
  source_snapshot_id
  participant_refs
  source_observation_refs
  comparison_key
  exact_operand_refs
  ordered_cross_evidence_refs
  diagnostic_refs
  normalization_contract_ref
  coverage_profile_ref
  comparison_rule_ref
  conflict_classification_ref
  source_non_claim_refs
  problem_rule_ref
```

### 19.2 Relation provenance

```text
DefectQualityRelationProvenance
  problem_resolution_ref
  problem_ref_or_none
  source_cross_result_ref
  comparison_key_or_none
  characteristic_id
  relation_rule_ref
  rationale_code
  evidence_refs
  source_contract_refs
```

### 19.3 Risk provenance

```text
BoundedRiskProvenance
  problem_resolution_ref
  problem_ref_or_none
  defect_population_ref
  defect_population_status
  relation_ref
  product_quality_context
  source_cross_result_ref_or_none
  participant_refs
  ordered_evidence_refs
  source_assessment_refs
  artifact_ref
  source_snapshot_id
  process_state_ref
  full_model_contract_ref
  defect_risk_contract_ref
  model_ref
  rule_ref
  parameter_set_ref
```

The minimum resolvable path is:

```text
Requirement pair
-> quantitative observations and Evidence
-> QB CrossRequirementResult
-> ConfirmedSupportedProblem in D_v0.1
-> DefectQualityRelation to PERFORMANCE_EFFICIENCY
-> BoundedRiskAssessment
```

The product-quality assessment is an adjacent context reference, not an input
to the conflict proof or categorical risk decision.

Provenance continuity fails closed. Dangling evidence, foreign participants,
snapshot mismatch, cross-version composition without an explicit validity
link, or inconsistent source identities are invalid or `UNRESOLVED` according
to the parent provenance contract; reporting must not repair them.

## 20. Version semantics

Every problem, relation, and risk result preserves all meaning-bearing
versions:

- specification artifact and source assessment;
- QB snapshot, coverage, normalization, materiality, comparison, aggregation,
  and non-claim contracts;
- source quantitative observation and Evidence rule authorities;
- Full Model and this focused contract;
- problem, relation, risk model, classifier, and empty parameter set;
- process state;
- product-quality assessment/model/rule/parameter references used as context;
  and
- risk assessment event.

Existing stable rule IDs retain the version authority defined by their source
contracts. This contract does not invent an explicit version for a stable rule
that has none.

A semantic change to eligibility, the exact D/Q key, relation meaning, risk
classification, state propagation, or non-claims requires a new rule and/or
contract version. A changed source result, artifact, assessment, snapshot,
process state, or evaluation event requires new output identities. Reporter
formatting does not change scientific identity.

## 21. Determinism and ordering

For identical immutable inputs and versions, all identities, statuses,
applicability values, classifications, reasons, explanations, provenance, and
ordered references are identical.

Ordering is:

1. problem resolutions by QB source cross-result order;
2. `D_v0.1` members by the same source order, filtered without re-sorting;
3. relation results by corresponding problem-resolution order;
4. risk results by relation order, or by explicit risk-input order when a
   single relation is evaluated independently;
5. participants in canonical QB earlier/later requirement order;
6. evidence, diagnostics, and source results in source order; and
7. non-claims in the order defined in Sections 22.2-22.4.

No sorting by bound, classification, state, metric text, risk presence,
evidence count, or product-quality result is permitted.

## 22. Explanations claims and non-claims

### 22.1 Explanation requirements

A positive problem explanation states:

- the exact two requirement participants and observations;
- the exact comparison key and Decimal bounds;
- why the QB admissible-set intersection is empty;
- the bounded problem class/subtype; and
- that this is a specification problem, not a product defect.

An available relation explanation states the exact Performance Efficiency key,
the risk-mediated/verification rationale, and its non-causal limit.

An available risk explanation states the risk scenario, the positive problem
and relation refs, the product-quality context and status, the empty parameter
set, provisional calibration status, and that no magnitude was computed.

Every non-available result identifies its controlling typed reason and source
reference. Explanations are deterministic renderings of structured facts; prose
does not override data.

### 22.2 Problem non-claims

```text
NC-D-001  NOT_GENERAL_SPECIFICATION_CONSISTENCY
NC-D-002  NOT_PRODUCT_DEFECT
NC-D-003  NOT_CV_OR_U_SIGNAL_PROMOTION
NC-D-004  NOT_RQD_016_CLOSURE
NC-D-005  NO_SEVERITY_OR_CONFIDENCE_SCORE
NC-D-006  NO_CAUSAL_CLAIM
```

### 22.3 Relation non-claims

```text
NC-RDQ-001  NOT_NUMERIC_RHO
NC-RDQ-002  NOT_CAUSALITY
NC-RDQ-003  NOT_PROBABILITY_OR_IMPACT
NC-RDQ-004  NOT_PROOF_OF_POOR_PRODUCT_PERFORMANCE
NC-RDQ-005  NOT_MAPPING_BEYOND_EXACT_RESPONSE_TIME_KEY
```

### 22.4 Risk non-claims

```text
NC-RISK-001  IDENTIFIED_PRESENCE_NOT_MAGNITUDE
NC-RISK-002  NO_PROBABILITY_OR_LIKELIHOOD
NC-RISK-003  NO_IMPACT_SEVERITY_OR_CRITICALITY
NC-RISK-004  NO_WEIGHT_THRESHOLD_OR_AGGREGATE_RISK
NC-RISK-005  NO_PRIORITY_OR_RANK
NC-RISK-006  NOT_PRODUCT_FAILURE_OR_QUALITY_SCORE
NC-RISK-007  NO_CAUSAL_CLAIM
NC-RISK-008  ABSENCE_OF_BOUNDED_RISK_NOT_ABSENCE_OF_RISK
NC-RISK-009  PROVISIONAL_NOT_CALIBRATED
```

The central interpretation is mandatory:

```text
identified bounded risk presence != quantified risk magnitude
```

## 23. Invariants and forbidden transformations

### 23.1 Required invariants

1. Only the exact Section 7.1 source state/class/subtype creates a problem.
2. Every problem is specification-scoped and source-cross-result-backed.
3. Every `D_v0.1` member is an available confirmed supported problem.
4. No unresolved, unsupported, unavailable, unknown, not-applicable, compatible,
   signal, or score input creates a `D` member.
5. `RQD-016` remains open and no existing `Finding(kind=QUALITY_PROBLEM)` is
   created.
6. An available relation has the exact Section 11.2 key and characteristic.
7. The relation is categorical and has no numeric relevance value.
8. An available risk result has exactly `RISK_IDENTIFIED` and no numeric value.
9. A non-available risk result has no classification.
10. The risk parameter set is empty and calibration status is
    `PROVISIONAL_NOT_CALIBRATED`.
11. Product-quality context is preserved but cannot create, clear, or scale the
    risk classification.
12. Every evidence and provenance reference resolves within compatible
    artifact, assessment, snapshot, and process versions.
13. Theoretical/calibration-required quantities remain absent.
14. Every output carries its mandatory non-claims.

### 23.2 Forbidden transformations

An implementation must not:

- turn a detector observation, diagnostic, signal, C/V/U value, completed
  absence, aggregate, conformance, or product-quality result into `D`;
- instantiate existing `FindingKind.QUALITY_PROBLEM`;
- use `M_cons[QB-v0.1]` as a defect, defect count, risk value, or weight;
- convert `ASSESSMENT_UNRESOLVED` into a conflict or no-conflict conclusion;
- treat `OUTSIDE_V0_1_APPLICABILITY` as compatibility;
- infer metric synonyms, context overlap, unit conversion, or wider quality
  relevance;
- assign relation presence the numeric value `rho_ij=1`;
- calculate probability, likelihood, impact, severity, criticality, confidence,
  uncertainty, magnitude, aggregate, rank, or priority;
- default a missing theoretical operand to zero or one;
- multiply a partial subset of the dissertation risk formula;
- use product conformance to erase or scale the specification risk;
- claim that `RISK_IDENTIFIED` means high, severe, probable, or prioritized;
- claim that no bounded result means no risk; or
- select or apply a corrective action.

## 24. Deterministic reference fixtures

### 24.1 Shared response-time conflict

```text
artifact_ref          = (SPEC-RISK-001, 1)
source_assessment_ref = (ASSESS-SPEC-RISK-001, 1, artifact_ref)
snapshot_id           = SNAP-RISK-001
process_state_ref     = (PROCESS-RISK-001, 1, REFERENCE_VERIFICATION)

R001: "Час відгуку ≤ 2 с при 500 одночасних користувачах"
R002: "Час відгуку не нижче 5 с при 500 одночасних користувачах"

comparison key = (
  "час відгуку",
  "при 500 одночасних користувачах",
  SECOND,
)

R001 admissible set = (-infinity, Decimal("2")]
R002 admissible set = [Decimal("5"), +infinity)
intersection        = empty
```

The fixture assumes both operands were validly produced by existing approved
QB source contracts. It is not new extraction coverage.

### 24.2 Problem relation and risk cases

| Case | Source fact | Problem result | Relation result | Risk result |
| --- | --- | --- | --- | --- |
| `DQR-RF-001` | shared exact conflict | available confirmed supported problem; one `D` member | available bounded relevance to PE | `AVAILABLE/APPLICABLE/RISK_IDENTIFIED` |
| `DQR-RF-002` | same key, upper `2`, lower `2` | compatible; no problem | `NOT_APPLICABLE` | `NOT_APPLICABLE`; no classification |
| `DQR-RF-003` | same key, upper `2`, lower `1` | compatible; no problem | `NOT_APPLICABLE` | `NOT_APPLICABLE` |
| `DQR-RF-004` | exact confirmed conflict on a resolved different metric | confirmed supported problem; member of `D` | `NOT_APPLICABLE` to PE mapping | `NOT_APPLICABLE` |
| `DQR-RF-005` | exact response-time conflict but different supported QB context from the fixed reference context | confirmed supported problem | `UNSUPPORTED` by this PE relation | `UNSUPPORTED` |
| `DQR-RF-006` | QB `ASSESSMENT_UNRESOLVED` | unresolved potential problem; no `D` member | `UNRESOLVED` | `UNRESOLVED` |
| `DQR-RF-007` | QB `OUTSIDE_V0_1_APPLICABILITY` | `NOT_APPLICABLE`; no `D` member | `NOT_APPLICABLE` | `NOT_APPLICABLE` |
| `DQR-RF-008` | `FIND-U-VAGUE-001` signal submitted as defect claim | `UNSUPPORTED`; signal unchanged; no `D` member | `UNSUPPORTED` | `UNSUPPORTED` |
| `DQR-RF-009` | C/V/U value zero submitted as defect claim | `UNSUPPORTED`; no problem | `UNSUPPORTED` | `UNSUPPORTED` |
| `DQR-RF-010` | shared exact conflict plus conforming separate PE product-quality result | same as case 001 | same as case 001 | `RISK_IDENTIFIED`; conformance does not clear it |
| `DQR-RF-011` | shared exact conflict plus unavailable PE product-quality result record | same as case 001 | same as case 001 | `RISK_IDENTIFIED`; unavailable quality status is preserved context |
| `DQR-RF-012` | shared exact conflict with dangling evidence or cross-snapshot participant | invalid input | no fabricated relation | no fabricated risk |

In every positive risk case:

```text
numeric risk value = absent
parameter entries  = ()
calibration status = PROVISIONAL_NOT_CALIBRATED
```

## 25. Acceptance cases for future implementation

### 25.1 M3-06 problem acceptance

| ID | Required behavior |
| --- | --- |
| `DQR-AC-001` | Only a valid QB `CONFIRMED_CONFLICT` with the exact class/subtype enters `D_v0.1`. |
| `DQR-AC-002` | The resolver consumes a completed QB result and does not repeat extraction or the conflict predicate. |
| `DQR-AC-003` | `COMPATIBLE_WITHIN_RULE` yields the bounded no-problem disposition and no `D` member. |
| `DQR-AC-004` | `ASSESSMENT_UNRESOLVED` yields `UNRESOLVED` and no problem. |
| `DQR-AC-005` | `OUTSIDE_V0_1_APPLICABILITY` yields `NOT_APPLICABLE` and no problem. |
| `DQR-AC-006` | A detector observation or diagnostic submitted as a problem is `UNSUPPORTED`. |
| `DQR-AC-007` | A `SIGNAL` submitted as a problem is `UNSUPPORTED` and remains unchanged. |
| `DQR-AC-008` | C/V/U values, aggregates, completed absences, conformance, and product-quality values cannot create problems. |
| `DQR-AC-009` | No existing `Finding(kind=QUALITY_PROBLEM)` is created. |
| `DQR-AC-010` | `RQD-016` remains explicitly open in result non-claims and documentation. |
| `DQR-AC-011` | Problem identity is deterministic from source and rule identities. |
| `DQR-AC-012` | Problem records preserve exact participants, operands, Decimal values, evidence, diagnostics, snapshot, and contract versions. |
| `DQR-AC-013` | Problem records contain no numeric severity, confidence, risk, or priority. |
| `DQR-AC-014` | `D_v0.1` preserves QB source order and contains no placeholders or duplicates. |
| `DQR-AC-015` | Invalid source-state combinations, foreign evidence, or cross-snapshot composition fail validation. |
| `DQR-AC-016` | A confirmed conflict remains an eligible individual problem when the QB aggregate is `UNKNOWN` for an unrelated unresolved comparison. |
| `DQR-AC-017` | The defect population snapshot preserves incomplete/unknown status and confirmed members simultaneously. |

### 25.2 M3-06 relation acceptance

| ID | Required behavior |
| --- | --- |
| `DQR-AC-018` | Only the exact reference response-time metric/context/unit key produces the available PE relation. |
| `DQR-AC-019` | A resolved different metric produces `NOT_APPLICABLE`, not a PE relation. |
| `DQR-AC-020` | The exact response-time metric with an unsupported context/unit produces `UNSUPPORTED` and no inferred conversion. |
| `DQR-AC-021` | An unresolved potential problem propagates `UNRESOLVED`. |
| `DQR-AC-022` | The available relation kind is exactly `BOUNDED_RISK_RELEVANCE`. |
| `DQR-AC-023` | Relation presence is never represented as numeric `rho_ij`. |
| `DQR-AC-024` | Relation rationale is characteristic-specific, evidence-backed, and explicitly non-causal. |
| `DQR-AC-025` | Relation identity and provenance are deterministic and version-complete. |
| `DQR-AC-026` | Product-quality values and C/V/U do not affect relation applicability or status. |
| `DQR-AC-027` | No synonym, ontology, unit conversion, or broader context mapping is performed. |

### 25.3 M3-07 risk acceptance

| ID | Required behavior |
| --- | --- |
| `DQR-AC-028` | Available confirmed problem plus available PE relation yields exactly `RISK_IDENTIFIED`. |
| `DQR-AC-029` | The risk result has no numeric value field. |
| `DQR-AC-030` | The risk schema contains no probability, likelihood, impact, severity, criticality, confidence, uncertainty, aggregate, rank, or priority value. |
| `DQR-AC-031` | The risk parameter set is explicit, versioned, and empty. |
| `DQR-AC-032` | Calibration status is exactly `PROVISIONAL_NOT_CALIBRATED`. |
| `DQR-AC-033` | Non-available problem/relation states propagate exactly without zero imputation. |
| `DQR-AC-034` | No eligible problem yields `NOT_APPLICABLE`, not `NO_RISK`. |
| `DQR-AC-035` | Product-quality context and its exact status are preserved in input, output, provenance, and explanation. |
| `DQR-AC-036` | A conforming product-quality result cannot clear the bounded specification risk. |
| `DQR-AC-037` | A nonconforming result cannot increase or quantify the risk. |
| `DQR-AC-038` | An unavailable/unknown/unresolved product-quality status cannot alter the categorical rule. |
| `DQR-AC-039` | Every positive result explains identified presence versus unquantified magnitude. |
| `DQR-AC-040` | Every risk result carries all mandatory non-claims in order. |
| `DQR-AC-041` | All quantities listed in Section 18 remain absent and marked calibration-required at contract level. |
| `DQR-AC-042` | Identical immutable inputs and versions produce field-equivalent results in deterministic order. |
| `DQR-AC-043` | Later artifact/assessment/process versions create new immutable results rather than mutating earlier results. |
| `DQR-AC-044` | Tests can construct domain inputs directly without files, CLI, extractor, reporter, test runner, telemetry, or benchmarking infrastructure. |
| `DQR-AC-045` | The risk component does not select or apply a corrective action. |

## 26. Assumptions contradictions blockers and readiness

### 26.1 Explicit bounded assumptions

1. QB-v0.1 `CONFIRMED_CONFLICT` is a validated exact logical result with
   complete participants, key, operands, evidence, and provenance.
2. The Full Model problem type is separate from the existing
   `FindingKind.QUALITY_PROBLEM`, preserving `RQD-016`.
3. The exact response-time reference key is sufficient for the one selected
   Performance Efficiency relation and no broader semantic map is needed.
4. Risk identification may record a well-formed risk scenario without
   quantifying its probability or consequence.
5. The product-quality assessment is required context but is independent of
   the specification-conflict risk-presence rule.

### 26.2 Contradiction review

The dissertation says risk should not be determined only from defect presence,
while the parent proposes a categorical rule. There is no contradiction once
the rule is interpreted narrowly: it requires both a confirmed defect and a
characteristic-specific relation, and it performs only risk identification.
It does not instantiate the dissertation's quantitative risk equation or claim
that a product consequence will occur.

The dissertation's defect tuple includes severity and detection confidence.
Their omission from the v0.1 problem record is deliberate and visible because
neither has an approved source or scale. Categorical logical confirmation is
not substituted for numeric confidence.

The existing `RQD-016` gate covers observation-to-`FindingKind.QUALITY_PROBLEM`
conversion. The separate QB cross-requirement specification-level problem type follows the parent
Full Model decision without changing that finding contract. No contradiction
requires closing `RQD-016`.

No unresolved scientific contradiction was found inside the bounded slice.

### 26.3 Blocking decisions

`FM-D015` remains the process blocker: the parent Full Model v0.1 contract must
receive the recorded researcher approval required by its Approval record before
M3-06 or M3-07 implementation.

`RQD-016` remains open for every general or C/V/U observation-to-
`QUALITY_PROBLEM` conversion. It does not block the separate, parent-approved
QB cross-requirement specification-level problem type, but it blocks using that type as authority to
promote other signals or observations.

Numeric risk analysis, aggregation, uncertainty, and prioritization remain
`EXPERIMENTAL_CALIBRATION_REQUIRED`. They do not block the categorical
reference result.

### 26.4 Implementation readiness

Subject to `FM-D015`, this contract is sufficient for the bounded M3-06 and
M3-07 implementations. It fixes object distinctions, exact eligibility,
problem and `D` identity, `R_DQ` applicability and non-causal semantics,
categorical risk input/output, state propagation, provenance, versioning,
empty parameters, calibration status, explanations, fixtures, non-claims, and
acceptance invariants.

M3-06 may implement only the exact QB problem projection and exact PE relation.
M3-07 may implement only `RISK_IDENTIFIED` presence and state propagation.
Everything resembling quantified risk magnitude must wait for experimental
calibration and a separately approved contract.
