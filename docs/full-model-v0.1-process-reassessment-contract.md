# Full Model v0.1 Process and Reassessment Contract

Status: normative design candidate for M3-08 / #145, M3-09 / #146, and
M3-10 / #147. This document defines future contracts only. It does not
implement production code, change existing assessment semantics, or authorize
implementation before the inherited approval gate is satisfied.

## 1. Purpose and authority

This contract closes the bounded Full Model v0.1 loop:

```text
Risk -> A_corr -> S(v2) -> ReEval -> comparison
```

and places that loop in the minimum executable projection of `M_process`.

The normative authority order is:

1. `docs/model-spec.md` for implemented MVP C/V/U behavior;
2. `docs/full-model-v0.1-contract.md` for Full Model v0.1 decisions;
3. `docs/full-model-v0.1-metric-profile-contract.md`,
   `docs/full-model-v0.1-dynamic-evidence-contract.md`,
   `docs/full-model-v0.1-product-quality-feature-contract.md`,
   `docs/full-model-v0.1-product-quality-assessment-contract.md`, and
   `docs/full-model-v0.1-defect-quality-risk-contract.md`;
4. the existing QB-v0.1 contracts, including
   `docs/cross-requirement-consistency-decision-package.md` and
   `docs/cross-requirement-consistency-architecture.md`, for
   quantitative-bound semantics; and
5. dissertation Chapters 4.1 and 4.3 as research context and traceability,
   not as executable specifications.

Where the parent Full Model contract has fixed a decision, this document
refines rather than reopens it. In particular, it inherits:

- `ACTION-RECONCILE-QB-001/v1` and action kind
  `RECONCILE_QUANTITATIVE_BOUNDS`;
- the requirement for a stakeholder- or controlled-fixture-supplied revision;
- immutable `S(v1)` and `S(v2)` artifacts;
- typed, compatibility-gated before/after comparisons;
- the single process stage `REFERENCE_VERIFICATION`, mapped to dissertation
  stage `tau^T`; and
- the approval blocker `FM-D015`.

No part of this contract authorizes a system to determine stakeholder intent,
invent a corrected threshold, edit a source artifact while proposing an
action, or claim that an action is optimal.

## 2. Dissertation research findings and bounded adoption

The research trace used for this contract is:

| Local source | Relevant material | Contract use |
| --- | --- | --- |
| `docs/reference/4.1_Процесна_модель.docx` | paragraphs 1-18, 21-32, and 35-39; Tables 4.1-4.4 | lifecycle stages, versioned assessment state, evidence validity, update/reassessment, feedback, invariants, and `M_process` |
| `docs/reference/4.3_Модель_ризиків.docx` | paragraphs 25-47; Table 4.11 | corrective-action structure, immutable changed artifacts, `ReEval`, before/after boundaries, and non-causal interpretation |

Paragraph numbers refer to the document paragraph order, excluding table cells.

### 2.1 Process model findings from Chapter 4.1

Chapter 4.1 defines a lifecycle-stage set
`T = {tau^R, tau^A, tau^I, tau^T, tau^O}` and states that stages may repeat for
increments rather than imposing a waterfall. Its assessment state
`P_j(tau,v)` binds a quality characteristic to the stage, artifact version,
available features/evidence, current estimate, evidence sufficiency, model
uncertainty, risks, and provenance.

The chapter establishes the following rules used here:

- an assessment has meaning only with its stage, artifact version, available
  evidence, and provenance;
- evidence for one artifact or product version is not automatically valid for
  another;
- an update is a rebuild from the current specification and evidence, not an
  arithmetic average of old and new results;
- more evidence may raise or lower an assessment, or merely change what is
  known;
- at `tau^T`, dynamic evidence supplies observed values and conformance data;
- missing or inapplicable evidence is not zero;
- requirement changes trigger impact analysis and reevaluation of dependent
  metrics and evidence; and
- a positive assessment delta is not proof of improved actual product quality.

Chapter 4.1 also defines checkpoints with evidence, quality, and critical-risk
thresholds. Those thresholds are explicitly left context-dependent and require
calibration. Full Model v0.1 therefore does not execute checkpoint decisions,
does not classify a risk as critical, and does not emit `proceed`.

### 2.2 Corrective-loop findings from Chapter 4.3

Chapter 4.3 represents a corrective action conceptually as:

```text
(target, change, expected effect, dependencies, cost, verification criterion)
```

and gives the loop:

```text
D^v -> Risk^v -> A_corr -> Artifact^(v+1) -> ReEval
    -> Quality^(v+1) -> Risk^(v+1)
```

The chapter does not prescribe one universally correct action per defect. A
conflict may require stakeholder agreement. It also distinguishes predicted
change from demonstrated product improvement and leaves action effect,
prioritization, probabilities, impacts, costs, and aggregate risk for empirical
work.

The minimum adopted subset is therefore:

- a traceable candidate action aimed only at reconciling the confirmed QB
  conflict;
- an externally supplied text revision rather than a system-selected bound;
- an immutable successor specification;
- full reevaluation of approved dependent components;
- a categorical verification of what changed under the same bounded rules;
  and
- no optimality, priority, cost, causal-effect, or product-improvement claim.

### 2.3 Consistency of `REFERENCE_VERIFICATION / tau^T`

The mapping is scientifically consistent for the reference slice because:

1. the dissertation assigns tests, execution logs, measurements, dynamic
   evidence, and conformance evaluation to `tau^T`;
2. its stages may repeat, so v1 and v2 may both be assessed at the same stage;
3. its feedback rule permits a finding at a later stage to revise a requirement
   artifact and then trigger reevaluation; and
4. Full Model v0.1's dynamic fixture is an observed response-time measurement,
   not an early prediction.

`REFERENCE_VERIFICATION` is a software label for a bounded `tau^T` projection.
It does not represent all verification and validation activities, a release
gate, a full test phase, or the complete lifecycle model. The revision changes
a requirements artifact; the process-state label identifies where the bounded
assessment is assembled, not where stakeholder intent was authored.

## 3. Bounded operations and responsibility split

The future design has four pure boundaries plus an orchestration record:

```text
propose_corrective_action(BoundedRiskAssessment, ConfirmedSupportedProblem,
                          DefectQualityRelation, ActionContext)
  -> CorrectiveActionResolution

apply_external_revision(CorrectiveAction, ExternallySuppliedRevision,
                        SpecificationVersion)
  -> ActionApplication

reevaluate(SpecificationVersion, ReassessmentContext)
  -> ReassessmentRun

compare(ComparisonRequest)
  -> ResultComparison

assemble_process_state(ProcessStateAssembly)
  -> ProcessAssessmentState
```

Responsibilities are separated as follows:

- the action proposer links an already identified bounded risk to a candidate
  change kind and never creates replacement text;
- the revision boundary validates and materializes an externally supplied
  replacement without deciding its meaning;
- reevaluation invokes existing approved components against `S(v2)` and owns
  no assessment formula;
- comparison decides semantic comparability and describes structured result
  change without causal interpretation; and
- process-state assembly associates immutable records and owns no calculator,
  risk classifier, action-selection policy, or reporting calculation.

## 4. Closed rule and type registry

The following registry is closed for this contract version:

| Order | Identity | Version | Meaning |
| ---: | --- | ---: | --- |
| 1 | `ACTION-RECONCILE-QB-001` | 1 | Propose the sole bounded corrective-action kind from an eligible risk/problem/relation. |
| 2 | `APPLY-EXTERNAL-REVISION-001` | 1 | Apply explicit replacement text supplied by a stakeholder or controlled fixture. |
| 3 | `REEVAL-FULL-MODEL-001` | 1 | Rebuild the approved Full Model v0.1 path for a successor specification. |
| 4 | `COMPARE-FULL-MODEL-001` | 1 | Compare two semantically compatible result records. |
| 5 | `PROCESS-REFERENCE-VERIFICATION-001` | 1 | Assemble the single-stage process-state projection. |

The sole action kind is:

```text
RECONCILE_QUANTITATIVE_BOUNDS
```

The registry contains no action to select the smaller, larger, stricter,
looser, safer, cheaper, or preferred bound. Adding another action kind or a
policy that chooses replacement content requires a new approved contract.

## 5. Shared identities and ordering

The following references are reused without changing the focused contracts:

```text
ArtifactRef(artifact_id, artifact_version)
AssessmentRef(assessment_id, assessment_version, artifact_ref)
RuleRef(rule_id, rule_version)
ModelRef(model_id, model_version)
ParameterSetRef(parameter_set_id, parameter_set_version)
ProcessStateRef(process_state_id, process_state_version, stage)
```

This contract adds:

```text
ContractRef(contract_id, contract_version)
RequirementLineageId

RequirementSubjectRef(
  artifact_ref,
  requirement_id,
  source_line
)

ActionRef(action_id, action_record_version)
RevisionRef(revision_id, revision_version)
ReassessmentRef(reassessment_id, reassessment_version)
ComparisonRef(comparison_id, comparison_version)
```

For an initial version in this bounded slice, lineage identity is the structured
origin tuple:

```text
RequirementLineageId = (
  artifact_id,
  origin_artifact_version,
  origin_requirement_id,
  origin_source_line
)
```

The tuple is allocated once from the accepted initial artifact and is copied,
not recomputed, for a successor. It therefore remains stable even if a
version-local requirement ID or line reference later differs. No text hash or
semantic similarity algorithm establishes lineage.

All ID and version strings are non-empty. Versions are opaque identities. The
notation `v1`, `v2`, and `v+1` means parent and successor; it does not authorize
integer parsing, automatic increment, lexical ordering, or “latest version”
selection.

Deterministic collections use these orders:

1. requirements and lineage entries: parent artifact source order, then
   version-local `requirement_id` as a tie-breaker;
2. target requirements: the order of their parent subjects;
3. component results: the registries of their owning focused contracts;
4. comparisons: result-kind registry order, metric/characteristic registry
   order, then subject-lineage order; and
5. evidence and provenance references: owning contract order, then complete
   structured identity.

No collection is ordered by bound value, score, status, conformance outcome,
risk classification, or perceived desirability.

## 6. Corrective-action proposal contract

### 6.1 Eligibility

An available proposal is created only when all of the following are true:

1. the `BoundedRiskAssessment` is `AVAILABLE/APPLICABLE` with classification
   `RISK_IDENTIFIED`;
2. its referenced problem is an `AVAILABLE` `ConfirmedSupportedProblem`
   admitted by `D-QB-CONFLICT-001/v1`;
3. its relation is an `AVAILABLE/APPLICABLE`
   `R_DQ-PE-QB-001/v1` relation to Performance Efficiency;
4. all three records refer to the same artifact version, process state,
   comparison key, and provenance chain;
5. the exact two conflict participants and their requirement lineage IDs are
   available; and
6. the target artifact is immutable and addressable by `ArtifactRef`.

Product-quality evidence may be unavailable or unresolved. That does not
invalidate a risk that the risk contract validly identified from the confirmed
problem. Missing product observation is not action failure and is not proof of
poor product behavior.

### 6.2 CorrectiveActionResolution

```text
CorrectiveActionResolution
  resolution_id: CorrectiveActionResolutionId
  status: AVAILABLE | UNAVAILABLE | UNKNOWN | UNRESOLVED |
          UNSUPPORTED | NOT_APPLICABLE
  applicability: APPLICABLE | UNKNOWN | NOT_APPLICABLE
  action_ref: ActionRef | None
  reason_codes: tuple[CorrectiveActionReason, ...]
  source_risk_ref: BoundedRiskAssessmentRef | None
  source_problem_ref: ConfirmedSupportedProblemRef | None
  source_relation_ref: DefectQualityRelationRef | None
  rule_ref: ACTION-RECONCILE-QB-001 / 1
  provenance: CorrectiveActionResolutionProvenance
```

State propagation is:

| Source condition | Resolution |
| --- | --- |
| eligible available risk/problem/relation | `AVAILABLE/APPLICABLE` with a `PROPOSED` action |
| no confirmed supported problem within the bounded rule | `NOT_APPLICABLE/NOT_APPLICABLE`; no action |
| source risk/problem/relation unavailable | `UNAVAILABLE`; no action |
| source assessment unknown | `UNKNOWN`; no action |
| required identity, lineage, or source coherence unresolved | `UNRESOLVED`; no action |
| request lies outside the sole action kind | `UNSUPPORTED`; no action |

No non-available state creates placeholder replacement text or a zero-valued
action.

`CorrectiveActionResolution` is the mandatory top-level action record for every
attempt. When its canonical status is `AVAILABLE`, the referenced
`CorrectiveAction.status` supplies `PROPOSED`, `APPLIED`, or `REJECTED`. When it
is not available, the envelope supplies `UNAVAILABLE`, `UNKNOWN`,
`UNRESOLVED`, `UNSUPPORTED`, or `NOT_APPLICABLE` and has no action payload.
Together, these two orthogonal fields realize the parent contract's required
status distinctions without treating a processing state as an action-lifecycle
state.

### 6.3 CorrectiveAction

```text
CorrectiveAction
  action_id: CorrectiveActionId
  action_record_version: str
  predecessor_action_ref: ActionRef | None
  action_kind: RECONCILE_QUANTITATIVE_BOUNDS
  status: PROPOSED | APPLIED | REJECTED
  rule_ref: ACTION-RECONCILE-QB-001 / 1

  originating_risk_ref: BoundedRiskAssessmentRef
  originating_problem_ref: ConfirmedSupportedProblemRef
  originating_relation_ref: DefectQualityRelationRef

  target_artifact_ref: ArtifactRef
  target_requirements: tuple[ActionTargetRequirement, ActionTargetRequirement]
  comparison_key: QbComparisonKey

  rationale: CorrectiveActionRationale
  proposed_change_kind: REPLACE_REQUIREMENT_TEXT
  expected_bounded_outcome: CorrectiveActionExpectedOutcome
  verification_rule_ref: REEVAL-FULL-MODEL-001 / 1

  external_revision_ref: RevisionRef | None
  application_ref: ActionApplicationRef | None
  rejection_source_ref: ExternalDecisionRef | None

  creator_source: ActionCreatorSource
  provenance: CorrectiveActionProvenance
  non_optimality_claim: CANDIDATE_NOT_OPTIMALITY_CLAIM
```

`ActionTargetRequirement` contains the stable lineage ID and the exact v1
`RequirementSubjectRef`. Its two entries are exactly the ordered QB conflict
participants; the action cannot silently broaden to other requirements.

`CorrectiveActionId` contains a caller-supplied stable action-instance ID plus
the action rule, originating risk ID, originating problem ID, and target
artifact reference. The caller-supplied component permits separate proposals
for the same source state without content-derived or random hidden identity.
The logical origin and target fields are immutable across action-record
versions.

Formally:

```text
CorrectiveActionId = (
  action_instance_id,
  rule_ref,
  originating_risk_id,
  originating_problem_id,
  target_artifact_ref
)
```

### 6.4 Rationale, expected outcome, and non-optimality

The normative rationale is bounded:

```text
The two target requirements contain an exact QB-v0.1 confirmed conflict on
the same complete quantitative comparison key. Stakeholder reconciliation is
requested because the system cannot determine which bound expresses intent.
```

The expected outcome is only that a later rerun may no longer identify that
exact confirmed conflict. It is not a promised outcome and does not mean:

- the externally supplied wording is correct;
- all specification conflicts are removed;
- Performance Efficiency improves;
- a product changes;
- risk magnitude is reduced; or
- the proposal is optimal, preferred, cheapest, or highest priority.

The mandatory `CANDIDATE_NOT_OPTIMALITY_CLAIM` makes those limitations part of
the record rather than optional report prose.

### 6.5 Action lifecycle

Action records are immutable. A status transition creates a new record version:

```text
PROPOSED -> APPLIED
PROPOSED -> REJECTED
```

- `PROPOSED` requires no revision or application reference.
- `APPLIED` requires both an external revision and a successful application
  record that created a distinct child artifact version.
- `REJECTED` requires an explicit external decision source and creates no child
  artifact.
- `APPLIED` and `REJECTED` are terminal within this bounded contract.

The action proposer must not perform the transition to `APPLIED`. Application
is a distinct boundary and requires the record described next.

## 7. Externally supplied revision and action application

### 7.1 ExternallySuppliedRevision

```text
ExternallySuppliedRevision
  revision_id: str
  revision_version: str
  provider_kind: STAKEHOLDER | CONTROLLED_REFERENCE_FIXTURE
  provider_ref: ExternalProviderRef
  action_ref: ActionRef
  parent_artifact_ref: ArtifactRef
  requested_child_artifact_ref: ArtifactRef
  replacements: tuple[RequirementTextReplacement, ...]
  provider_rationale_or_none: str | None
  provenance: ExternalRevisionProvenance
```

```text
RequirementTextReplacement
  lineage_id: RequirementLineageId
  expected_parent_subject_ref: RequirementSubjectRef
  replacement_text: str
```

The replacement tuple is non-empty and is a subset of the action's two target
lineages. Full Model v0.1 permits replacement only: no add, remove, split,
merge, or reorder operation belongs to this action.

Each `replacement_text` must already satisfy the MVP line-input shape: valid
UTF-8, non-empty, no embedded line break, and no leading or trailing whitespace.
Application preserves the supplied text and punctuation exactly; it does not
trim, normalize, paraphrase, choose, or repair it.

The requested child has the same `artifact_id` as its parent and a distinct,
caller-supplied `artifact_version`. The system does not invent the version.
`CONTROLLED_REFERENCE_FIXTURE` is valid only for deterministic tests and the
reference scenario in this contract. A production artifact revision requires
the `STAKEHOLDER` provider kind; a fixture never stands in for stakeholder
authority outside controlled verification.

### 7.2 Application validation

`APPLY-EXTERNAL-REVISION-001/v1` validates only structural authority and
identity:

1. the referenced action is `PROPOSED`;
2. action, revision, and parent artifact references agree exactly;
3. the provider kind is one of the two closed values;
4. every replacement names one exact action target and its expected v1 subject;
5. no target is repeated;
6. no non-target subject is changed;
7. parent and child artifact identities satisfy Section 8; and
8. replacement text satisfies Section 7.1.

Application does not test whether the new wording resolves the conflict. That
is a ReEval result. A structurally valid but ineffective stakeholder-supplied
revision may be `APPLIED` and still produce the same problem and risk afterward.

### 7.3 ActionApplication

```text
ActionApplication
  application_id: ActionApplicationId
  application_version: str
  action_before_ref: ActionRef
  action_after_ref: ActionRef
  revision_ref: RevisionRef
  parent_artifact_ref: ArtifactRef
  child_artifact_ref: ArtifactRef
  changed_subjects: tuple[ChangedRequirementSubject, ...]
  rule_ref: APPLY-EXTERNAL-REVISION-001 / 1
  status: AVAILABLE | UNAVAILABLE | UNRESOLVED | UNSUPPORTED
  reason_codes: tuple[ActionApplicationReason, ...]
  provenance: ActionApplicationProvenance
```

Only an `AVAILABLE` application may reference an `APPLIED` action version and
a materialized child artifact. No failed application partially edits either
artifact.

## 8. Immutable specification versioning and requirement lineage

### 8.1 SpecificationVersion

```text
SpecificationVersion
  artifact_ref: ArtifactRef
  parent_artifact_ref: ArtifactRef | None
  created_by_application_ref: ActionApplicationRef | None
  requirements: tuple[VersionedRequirement, ...]
  changed_subjects: tuple[ChangedRequirementSubject, ...]
  provenance: SpecificationVersionProvenance
```

```text
VersionedRequirement
  lineage_id: RequirementLineageId
  subject_ref: RequirementSubjectRef
  text: str
  predecessor_subject_ref: RequirementSubjectRef | None
```

```text
ChangedRequirementSubject
  lineage_id: RequirementLineageId
  before_subject_ref: RequirementSubjectRef
  after_subject_ref: RequirementSubjectRef
  change_kind: REPLACE_TEXT
```

For an action-produced child:

- `artifact_id` is unchanged;
- `artifact_version` is distinct;
- the parent reference is exact and singular;
- requirement count, source order, and lineage population are unchanged;
- each child requirement has exactly one parent requirement with the same
  lineage ID;
- a changed line uses the exact externally supplied replacement text;
- an unchanged line preserves text exactly;
- version-local requirement IDs and subject references identify the child
  version and are never used as a substitute for lineage; and
- `changed_subjects` is exactly the non-empty replacement set.

The action link belongs to the child and transition record. `S(v1)` is never
modified or backfilled.

### 8.2 ArtifactTransition and immutable history

```text
ArtifactTransition
  transition_id: ArtifactTransitionId
  parent_artifact_ref: ArtifactRef
  child_artifact_ref: ArtifactRef
  action_application_ref: ActionApplicationRef
  revision_ref: RevisionRef
  changed_subjects: tuple[ChangedRequirementSubject, ...]
  provenance: ArtifactTransitionProvenance
```

History is append-only. A child has one parent in this bounded operation. A
parent may have more than one externally authorized child, but each child has a
different artifact version and its own transition/application identity. No
implicit “current,” “latest,” or branch winner is selected.

Requirement lineage asserts subject continuity across artifact versions. It
does not assert semantic equivalence, unchanged intent, or stakeholder approval
of the predecessor. A text replacement keeps lineage because it is the revised
form of that identified requirement; comparison still examines whether the
assessment semantics are compatible.

## 9. ReEval contract

### 9.1 Meaning

`ReEval` is a versioned orchestration record for rebuilding approved results
from `S(v2)`. It is not a formula and never averages, patches, or carries
forward a v1 score.

For the child version it invokes, in dependency order:

1. the existing reader/extraction/C/V/U assessment path;
2. the existing specification aggregation path;
3. QB-v0.1 projection, comparison, materiality, and aggregation;
4. the lossless Metric Profile adapter;
5. dynamic criterion binding and conformance when their inputs are available;
6. `X_PE` construction;
7. bounded product-quality assessment;
8. confirmed-problem construction and the bounded D-to-PE relation;
9. categorical bounded risk assessment; and
10. process-state assembly.

Every component retains its own status precedence and semantics. ReEval cannot
turn unavailable data into failure, zero, pass, or risk absence.

### 9.2 ReassessmentContext and ReassessmentRun

```text
ReassessmentContext
  predecessor_process_state_ref: ProcessStateRef
  action_application_ref: ActionApplicationRef
  parent_artifact_ref: ArtifactRef
  child_artifact_ref: ArtifactRef
  child_assessment_ref: AssessmentRef
  full_model_contract_ref: ContractRef
  component_version_set: ComponentVersionSet
  evidence_reuse_decisions: tuple[EvidenceReuseDecision, ...]
  stage: REFERENCE_VERIFICATION
```

```text
ReassessmentRun
  reassessment_id: str
  reassessment_version: str
  context: ReassessmentContext
  status: AVAILABLE | UNAVAILABLE | UNKNOWN | UNRESOLVED | UNSUPPORTED
  child_process_state_ref: ProcessStateRef | None
  produced_result_refs: tuple[AssessmentResultRef, ...]
  comparison_request_refs: tuple[ComparisonRequestRef, ...]
  reason_codes: tuple[ReassessmentReason, ...]
  rule_ref: REEVAL-FULL-MODEL-001 / 1
  provenance: ReassessmentProvenance
```

`AVAILABLE` means the orchestration completed and preserved all component
states. It does not mean that every component result is available or positive.
A run may validly contain `UNKNOWN`, `UNAVAILABLE`, `UNRESOLVED`,
`UNSUPPORTED`, and `NOT_APPLICABLE` component associations.

### 9.3 Recalculation and evidence reuse

All requirement-derived results are rebuilt for the child artifact. In
particular, changed text never reuses its old extraction evidence, C/V/U
assessment, QB observation, Metric Entry, criterion binding, or problem result.
The bounded reference implementation may rebuild the entire specification even
for unchanged lineages; this is the required deterministic default.

An existing dynamic observation may be reused only when all are exact:

- product identity and product version;
- observation source and collection identity/version;
- observed metric identity and unit;
- normalized context identity;
- applicability;
- process stage; and
- the source contract permits reuse for the successor assessment.

The reuse must be recorded:

```text
EvidenceReuseDecision
  source_evidence_ref
  target_process_state_ref
  decision: REUSE_ALLOWED | REBUILD_OR_RECOLLECT_REQUIRED
  exact_identity_checks
  reason_codes
  provenance
```

Reusing an observation does not reuse conformance, `X_PE`, product-quality,
problem, relation, or risk results. Those records are rebuilt for v2. If the
criterion bound, comparator, unit, metric, or context changed, the old
conformance record cannot be reused. If product/evidence context validity cannot
be proven, the observation is `UNAVAILABLE` for v2 rather than assumed valid.

## 10. Before/after comparison contract

### 10.1 Comparison subjects

A comparison subject is stable across versions by lineage, not by display ID:

| Result family | Stable comparison subject |
| --- | --- |
| requirement C/V/U | requirement lineage ID plus metric ID |
| specification C/V/U | stable artifact ID plus identical ordered requirement-lineage population plus metric ID |
| `M_cons[QB-v0.1]` | stable artifact ID, identical ordered requirement-lineage population, and QB metric ID |
| criterion/conformance | criterion requirement lineage, dynamic metric identity, comparator/unit/context identity, and product/evidence context |
| `X_PE` / product-quality result | selected criterion lineage, characteristic, result kind, product/version, and exact evidence context |
| confirmed problem | ordered participant lineages plus complete QB comparison key and problem rule |
| D-to-PE relation | confirmed-problem comparison subject plus Performance Efficiency identity |
| bounded risk | ordered participant lineages, complete QB comparison key, and Performance Efficiency identity |

The risk subject deliberately does not require the same problem record ID. This
allows an identified v1 risk to be compared with the v2 bounded state in which
the same lineage/key scope contains no confirmed supported problem. The result
is a categorical `STATE_CHANGED`, not a numeric risk decrease.

### 10.2 SemanticCompatibilityDeclaration

Exact version equality is sufficient but not always necessary. A changed rule,
model, or parameter reference is compatible only through an explicit record:

```text
SemanticCompatibilityDeclaration
  declaration_id
  component_kind: RULE | MODEL | PARAMETER_SET
  before_ref
  after_ref
  comparison_scope
  disposition: COMPATIBLE_FOR_COMPARISON | INCOMPATIBLE
  rationale
  authority_ref
  provenance
```

A declaration is scoped; it cannot claim blanket compatibility for unrelated
metrics, subjects, or result kinds. Absence of a required declaration means
`NOT_COMPARABLE`. Version-number similarity or ordering is not evidence of
semantic compatibility.

### 10.3 Necessary and sufficient comparability conditions

Two result records are `COMPARABLE` if and only if all applicable checks pass:

1. both records exist and their structures are valid;
2. they have the same result family and value kind;
3. metric or characteristic identity is equal;
4. the stable comparison subject in Section 10.1 is equal;
5. the child artifact is linked to the parent through the recorded transition;
6. scope and, for specification metrics, ordered lineage population are equal;
7. rule and model semantics are identical or explicitly compatible;
8. parameter-set semantics are identical or explicitly compatible;
9. exact numeric representation and scale are the same where values exist;
10. required evidence context is equal;
11. process stage is exactly `REFERENCE_VERIFICATION` for both; and
12. applicability/status differences can be interpreted under the same source
    contract rather than arising from a change of meaning.

Artifact version and assessment version are expected to differ and do not by
themselves make results incomparable.

The comparison is `NOT_COMPARABLE` if any applicable condition fails. Closed
reason codes are:

```text
RESULT_FAMILY_MISMATCH
VALUE_KIND_OR_SCALE_MISMATCH
METRIC_OR_CHARACTERISTIC_MISMATCH
SUBJECT_LINEAGE_MISSING_OR_MISMATCH
ARTIFACT_ANCESTRY_MISSING_OR_MISMATCH
SCOPE_OR_POPULATION_MISMATCH
RULE_SEMANTICS_INCOMPATIBLE
MODEL_SEMANTICS_INCOMPATIBLE
PARAMETER_SEMANTICS_INCOMPATIBLE
EVIDENCE_CONTEXT_MISMATCH
PROCESS_STAGE_MISMATCH
APPLICABILITY_SEMANTICS_INCOMPATIBLE
```

For dynamic/product-quality results, a changed requirement criterion bound,
comparator, unit, or context changes the evaluated target and therefore yields
`NOT_COMPARABLE`; it is not interpreted as a better or worse result. A changed
observation product/version or collection context likewise yields
`NOT_COMPARABLE` in v0.1.

### 10.4 ResultComparison

```text
ResultComparison
  comparison_id: str
  comparison_version: str
  before_result_ref: AssessmentResultRef
  after_result_ref: AssessmentResultRef
  comparison_subject: ComparisonSubject
  status: AVAILABLE | UNAVAILABLE | UNRESOLVED | UNSUPPORTED
  comparison_kind: UNCHANGED | INCREASED | DECREASED |
                   STATE_CHANGED | NOT_COMPARABLE | None
  before_state_and_value
  after_state_and_value
  reason_codes
  rule_ref: COMPARE-FULL-MODEL-001 / 1
  compatibility_declaration_refs
  parameter_set_refs
  calibration_status_or_none
  explanation
  provenance
  claims
  non_claims
```

If both result records are present, a semantic mismatch produces the available
comparison conclusion `NOT_COMPARABLE`. `UNAVAILABLE` means a required record
does not exist at the comparison event; `UNRESOLVED` means identity or lineage
needed to decide comparability cannot be established; `UNSUPPORTED` means the
result family has no comparison rule in this contract.

### 10.5 Comparison-kind rules

After comparability is established:

- two available exact `Fraction` values are compared as exact rational numbers;
- no float conversion, rounding, tolerance, normalization, weighting, or zero
  imputation is allowed;
- equal exact numeric values yield `UNCHANGED`;
- a mathematically larger exact value yields `INCREASED`;
- a mathematically smaller exact value yields `DECREASED`;
- identical categorical/status/applicability states yield `UNCHANGED`;
- a categorical, status, applicability, presence, or absence transition yields
  `STATE_CHANGED`; and
- categorical risk and problem states have no numeric order.

Exact `Decimal` bounds and observations remain evidence. This contract does not
convert them to `Fraction` or compare raw magnitudes as a proxy for quality. A
bounded product-quality indicator, when comparable, retains the exact
`Fraction(0,1)` or `Fraction(1,1)` representation of its owning contract.

Full Model v0.1 does not authorize the words “improved,” “worsened,” “risk
reduced,” or “product quality increased” for any comparison kind. Reports use
literal phrases such as “the exact metric value increased” or “the bounded
state changed.” This conservative wording applies even when an individual
property has a familiar positive polarity.

### 10.6 Provisional and parameter semantics

If either compared product-quality or risk record is
`PROVISIONAL_NOT_CALIBRATED`, the comparison carries that exact calibration
status. It must not be removed because both sides use the same provisional
rule. A Metric Profile comparison with no parameter set leaves
`calibration_status_or_none` absent rather than inventing a calibrated status.

## 11. Minimal `M_process` projection

### 11.1 Bounded tuple

The Full Model v0.1 projection is:

```text
M_process_v0.1 = (T_0, A_0, E_0, K_0, U_0, C_0)

T_0 = {REFERENCE_VERIFICATION}
A_0 = {immutable specification versions and referenced product/evidence artifacts}
E_0 = {approved static evidence, QB evidence, and bounded dynamic evidence}
K_0 = empty
U_0 = {apply external revision, reevaluate, compare}
C_0 = {approved requirement, QB, response-time, product, and process contexts}
```

`K_0` is empty because v0.1 has no calibrated sufficiency, quality, critical
risk, release, or progression threshold. An action proposal is not a checkpoint
decision and does not imply that a lifecycle transition is blocked or approved.

The projection omits dissertation values that are not executable here:
predicted `y_hat_j`, evidence reliability percentages, model uncertainty,
critical-risk thresholds, action costs, priority, and numeric risk deltas.
Their absence is explicit; none is represented by zero.

### 11.2 ProcessAssessmentState

```text
ProcessAssessmentState
  process_state_id: str
  process_state_version: str
  process_lineage_id: str
  stage: REFERENCE_VERIFICATION

  artifact_ref: ArtifactRef
  artifact_transition_ref_or_none: ArtifactTransitionRef | None
  assessment_ref: AssessmentRef
  full_model_contract_ref: ContractRef
  component_version_set: ComponentVersionSet

  evidence_associations: tuple[ProcessEvidenceAssociation, ...]
  requirement_assessment_refs: tuple[RequirementAssessmentRef, ...]
  specification_assessment_ref: SpecificationAssessmentRef
  metric_profile_ref: MetricProfileRef
  pe_feature_profile_ref: PerformanceEfficiencyFeatureProfileRef | None
  product_quality_assessment_ref: ProductQualityAssessmentRef | None
  defect_population_ref: DefectPopulationRef
  confirmed_problem_refs: tuple[ConfirmedSupportedProblemRef, ...]
  defect_quality_relation_refs: tuple[DefectQualityRelationRef, ...]
  bounded_risk_assessment_refs: tuple[BoundedRiskAssessmentRef, ...]
  corrective_action_refs: tuple[ActionRef, ...]

  predecessor_process_state_ref: ProcessStateRef | None
  reassessment_ref: ReassessmentRef | None
  provenance: ProcessAssessmentStateProvenance
```

Each optional or plural association preserves the owning record's status and
applicability. An absent reference is accompanied in
`evidence_associations` or provenance by a typed reason; absence is not a
negative assessment. There is no scalar process-quality score and no aggregate
pass/fail field.

```text
ProcessEvidenceAssociation
  role: STATIC_REQUIREMENT | QB | DYNAMIC_CRITERION |
        DYNAMIC_OBSERVATION | CONFORMANCE
  evidence_ref: EvidenceRef | None
  status: AVAILABLE | UNAVAILABLE | UNKNOWN | UNRESOLVED |
          UNSUPPORTED | NOT_APPLICABLE
  applicability: APPLICABLE | UNKNOWN | NOT_APPLICABLE
  artifact_or_product_ref
  source_or_collection_ref
  context_ref_or_none
  reuse_decision_ref_or_none
  reason_codes
  provenance
```

This association indexes owning evidence; it does not copy, reinterpret, score,
or combine it.

The state is immutable. Successor association is recorded by a separate
transition so that the predecessor is not edited later:

```text
ProcessStateTransition
  transition_id
  predecessor_process_state_ref
  successor_process_state_ref
  artifact_transition_ref
  action_application_ref
  reassessment_ref
  comparison_refs
  rule_ref: PROCESS-REFERENCE-VERIFICATION-001 / 1
  provenance
```

Thus predecessor and successor are associated in the process history without
mutating either state. A successor state has the same `process_lineage_id`, the
same stage, a child artifact version, a new assessment identity, and an exact
predecessor reference.

### 11.3 ComponentVersionSet

The process state records the exact versions that determine interpretation:

- parent Full Model contract;
- reader/input policy;
- feature extraction and every detector rule;
- C/V/U calculator and aggregation rules;
- QB projection, normalization, coverage, comparison, materiality, and
  aggregation rules;
- Metric Profile registry/adapter;
- dynamic criterion-binding and conformance rules;
- `X_PE` registry/mapping;
- product-quality model/procedure/empty parameter set;
- problem, D-to-PE relation, risk classifier/empty parameter set;
- action, application, reassessment, comparison, and process-state rules; and
- evidence source and collection versions.

No version field may be replaced by the application build version alone.

### 11.4 Provenance minimum

Every new record in this contract has an immutable provenance envelope. At a
minimum, the envelope identifies:

- the record's own versioned identity;
- parent and child artifact/assessment/process-state references as applicable;
- all direct input result and evidence references in deterministic order;
- the governing action, application, reassessment, comparison, and process
  rule references;
- all inherited detector, calculator, aggregation, QB, feature, model, and
  parameter references needed to interpret the record;
- the external provider and revision reference for an application;
- the dynamic source/collection/product/context references for any reused
  observation;
- predecessor record references for action, artifact, assessment, and process
  lineage; and
- typed reason and non-claim codes.

Optional timestamps, actor display names, or report labels may be retained as
metadata, but they are not semantic identity and must not determine ordering or
comparison. A provenance chain must be traversable from comparison to both
results, process states, assessments, artifact versions, action/application,
originating risk/problem/relation, and the evidence that supported them.

## 12. Complete conceptual v1-to-v2 reference scenario

### 12.1 v1 artifact and evidence

```text
artifact              = (SPEC-PROCESS-REF-001, v1)
process stage         = REFERENCE_VERIFICATION

lineage RL-001 / R001 = "Час відгуку ≤ 2 с при 500 одночасних користувачах"
lineage RL-002 / R002 = "Час відгуку не нижче 5 с при 500 одночасних користувачах"

QB key = ("час відгуку",
          "при 500 одночасних користувачах",
          SECOND)
```

QB-v0.1 produces one exact `CONFIRMED_CONFLICT` for the upper bound
`Decimal("2")` and lower bound `Decimal("5")`. Its bounded consistency metric
for the two-requirement reference population is exact `Fraction(0,1)`.

`D-QB-CONFLICT-001/v1` creates the confirmed supported problem,
`R_DQ-PE-QB-001/v1` creates the categorical relation to Performance Efficiency,
and `RISK-PE-QB-001/v1` creates `RISK_IDENTIFIED`. No numeric risk magnitude
exists.

The explicitly selected criterion is RL-001, response time `<= Decimal("2")`
seconds in the same context. A controlled dynamic collection supplies exact
observation `Decimal("1.8")` seconds. Dynamic conformance is `CONFORMS`, but
the `X_PE` target gate is `TARGET_CONFLICT`; therefore the v1 bounded
product-quality result is `UNRESOLVED`, with no numeric indicator. The
observation is not failure and the system chooses neither conflicting bound.

### 12.2 Proposal and external revision

`ACTION-RECONCILE-QB-001/v1` creates action `A-REF-001` in `PROPOSED` state.
Its targets are RL-001 and RL-002, its rationale is the exact confirmed
conflict, and it contains no replacement payload.

A `CONTROLLED_REFERENCE_FIXTURE` then supplies revision `REV-REF-001/v1`:

```text
target lineage RL-002
expected parent subject = (SPEC-PROCESS-REF-001, v1, R002, line 2)
replacement text = "Час відгуку ≤ 5 с при 500 одночасних користувачах"
requested child artifact = (SPEC-PROCESS-REF-001, v2)
```

The fixture, not the system, supplies that wording. The application creates an
`APPLIED` action record version and immutable `S(v2)`. RL-001 is unchanged;
RL-002 retains its lineage but has a v2 subject and new text. `changed_subjects`
contains exactly RL-002. `S(v1)` remains unchanged.

### 12.3 ReEval and v2 state

ReEval rebuilds all requirement-derived components for v2. The response-time
observation may be reused only through an explicit `REUSE_ALLOWED` record
because product/version, collection, unit, context, and stage are unchanged.
The criterion, conformance reference, `X_PE`, product-quality result, problem,
relation, and risk are nevertheless rebuilt.

The two v2 bounds are compatible within QB-v0.1. The bounded consistency metric
is exact `Fraction(1,1)`. No confirmed supported problem exists for the
lineage/key scope, so the bounded risk result is
`NOT_APPLICABLE/NOT_APPLICABLE` with no classification. This means only “no
eligible problem was identified by the bounded rule.”

RL-001 remains the explicitly selected criterion. Its same exact observation
conforms, the target gate is now clear, and the v2 product-quality result is the
bounded observed conformance indicator `Fraction(1,1)`. It still does not
represent complete Performance Efficiency.

C/V/U results are recomputed and associated with the v2 process state. This
scenario intentionally asserts no particular C/V/U change beyond what their
existing contracts deterministically produce; the corrective action and its
acceptance cases do not depend on a new C/V/U interpretation.

### 12.4 Typed comparisons

Given identical approved rule/model/parameter semantics and the recorded
lineage:

| Subject | v1 | v2 | Comparison | Interpretation |
| --- | --- | --- | --- | --- |
| `M_cons[QB-v0.1]` | `Fraction(0,1)` | `Fraction(1,1)` | `INCREASED` | exact bounded-consistency metric increased; not a product-quality claim |
| confirmed problem scope | present | absent within rule | `STATE_CHANGED` | bounded conflict is no longer identified |
| bounded PE risk scope | `RISK_IDENTIFIED` | `NOT_APPLICABLE`, no class | `STATE_CHANGED` | no numeric risk decrease and no “safe” claim |
| bounded product-quality result | `UNRESOLVED`, no value | available `Fraction(1,1)` | `STATE_CHANGED` | the specification gate became resolvable; same observation does not show product improvement |

The product behavior did not change in the fixture: the exact same observation
was reused. The scenario therefore demonstrates especially clearly why a
requirement/specification change and an available v2 conformance result do not
prove causal product-quality improvement.

## 13. Normative invariants and forbidden transformations

### 13.1 Required invariants

1. A proposal never edits a specification.
2. Only an explicit stakeholder- or controlled-fixture-supplied revision can
   create an applied action.
3. The system never selects a replacement threshold or stakeholder intent.
4. Parent and child specifications are immutable and have the same stable
   artifact ID with distinct version IDs.
5. The bounded action preserves requirement count, order, and lineage
   population and changes only named target lineages.
6. Application success means the supplied revision was materialized, not that
   it resolved the conflict.
7. ReEval rebuilds dependent assessments for the child artifact.
8. Requirement-derived evidence from changed text is never reused.
9. Dynamic evidence reuse requires exact validity checks and a reuse record.
10. Every result remains tied to artifact, assessment, rule/model/parameter,
    evidence, process-stage, and provenance versions.
11. Comparability is established before any value relation is calculated.
12. Exact `Fraction` values remain exact; QB and dynamic source decimals remain
    exact `Decimal` evidence.
13. Missing, unavailable, unknown, unresolved, unsupported, and not-applicable
    states are never zero-imputed.
14. `INCREASED` and `DECREASED` are mathematical relations, not improvement or
    deterioration claims.
15. Categorical problem and risk transitions use `STATE_CHANGED`, not numeric
    ordering.
16. A disappearing bounded risk says only that the same rule no longer
    identifies its eligible problem.
17. The process state contains no scalar process, requirement, specification,
    product-quality, or risk aggregate invented by this contract.
18. The single stage remains `REFERENCE_VERIFICATION`; it is not a complete
    SDLC engine.

### 13.2 Forbidden transformations and claims

The future implementation must not:

- generate, rewrite, normalize, rank, or recommend bound values;
- infer that a tighter or looser bound is preferable;
- apply a proposed action without an external revision;
- mutate or overwrite `S(v1)`;
- treat `v+1` as an arithmetic version rule;
- identify cross-version subjects only by version-local requirement ID or line;
- copy v1 assessments into v2 instead of reevaluating;
- reuse evidence merely because its text or numeric value appears equal;
- compare different metrics, subjects, scales, contexts, stages, or semantic
  versions;
- convert exact rational results to float, round them, normalize them, weight
  them, or combine them into an overall score;
- turn `UNKNOWN`, `UNAVAILABLE`, `UNRESOLVED`, `UNSUPPORTED`, or
  `NOT_APPLICABLE` into failure, success, or zero;
- calculate predicted product quality, probability, likelihood, impact,
  severity, criticality, confidence, uncertainty, risk magnitude, aggregate
  risk, priority, cost, or action effect;
- claim that a proposal is optimal or that an applied change is correct;
- claim that a changed requirement metric caused product-quality improvement;
  or
- claim that one response-time observation represents complete Performance
  Efficiency.

## 14. Acceptance cases for future implementations

### 14.1 M3-08 / #145 corrective action

| ID | Acceptance case |
| --- | --- |
| `PR-AC-001` | An eligible exact risk/problem/relation produces one `PROPOSED` `RECONCILE_QUANTITATIVE_BOUNDS` action with both ordered target lineages. |
| `PR-AC-002` | A proposal contains no replacement text and leaves its source artifact byte-for-byte unchanged. |
| `PR-AC-003` | An unavailable product-quality observation does not block a proposal supported by the eligible risk contract. |
| `PR-AC-004` | No confirmed supported problem produces `NOT_APPLICABLE`, not a no-risk or pass claim. |
| `PR-AC-005` | Unresolved source identity produces `UNRESOLVED` and no action. |
| `PR-AC-006` | An unregistered action kind produces `UNSUPPORTED`. |
| `PR-AC-007` | The action preserves risk, problem, relation, artifact, requirement, evidence, rule, and provenance references. |
| `PR-AC-008` | Every action carries the mandatory candidate/non-optimality claim. |
| `PR-AC-009` | Only `PROPOSED -> APPLIED` and `PROPOSED -> REJECTED` are accepted transitions. |
| `PR-AC-010` | A rejected proposal creates no child specification. |

### 14.2 M3-09 / #146 versioning, ReEval, and comparison

| ID | Acceptance case |
| --- | --- |
| `PR-AC-011` | Application without an explicit stakeholder/fixture revision is rejected without mutation. |
| `PR-AC-012` | A revision touching an unrelated lineage, adding/removing a line, or changing order is rejected in v0.1. |
| `PR-AC-013` | Successful application preserves v1 and creates a distinct immutable v2 linked by parent, action, revision, and changed-subject records. |
| `PR-AC-014` | Requirement lineage is stable while v1 and v2 subject references remain version-local. |
| `PR-AC-015` | An applied but still-conflicting revision is recorded as applied; ReEval independently reproduces the conflict/risk. |
| `PR-AC-016` | ReEval rebuilds all requirement-derived results and never copies a changed requirement's prior evidence. |
| `PR-AC-017` | Dynamic observation reuse is allowed only after every exact identity/context check and is recorded. |
| `PR-AC-018` | Same metric, lineage, population, semantics, context, stage, and scale permit comparison despite different artifact/assessment versions. |
| `PR-AC-019` | Different metric, missing lineage, changed population, incompatible semantics, context, stage, or scale yields `NOT_COMPARABLE`. |
| `PR-AC-020` | A changed parameter version without an explicit compatibility declaration yields `NOT_COMPARABLE`. |
| `PR-AC-021` | Exact equal Fractions yield `UNCHANGED`; exact larger/smaller Fractions yield `INCREASED`/`DECREASED` without float conversion. |
| `PR-AC-022` | Available-to-unresolved, risk-identified-to-not-applicable, and problem-present-to-absent transitions yield `STATE_CHANGED`. |
| `PR-AC-023` | A changed criterion bound, comparator, unit, context, product version, or collection context makes product-quality results `NOT_COMPARABLE`. |
| `PR-AC-024` | Provisional calibration status propagates into comparisons of provisional product-quality or risk results. |
| `PR-AC-025` | Comparison explanations never infer optimality, causality, complete PE, or actual product improvement. |

### 14.3 M3-10 / #147 process projection

| ID | Acceptance case |
| --- | --- |
| `PR-AC-026` | Every process state has the sole stage `REFERENCE_VERIFICATION` and an exact artifact/assessment version. |
| `PR-AC-027` | A process state associates evidence, C/V/U/specification assessments, Metric Profile, `X_PE`, product-quality result, problem/relation, risk, action, and lineage without recalculating them. |
| `PR-AC-028` | Non-available and absent associations preserve typed states/reasons and are not zero-filled. |
| `PR-AC-029` | The v2 state has the same process lineage, a new state identity, exact predecessor, child artifact, and reassessment reference. |
| `PR-AC-030` | A separate process transition associates predecessor and successor without mutating v1. |
| `PR-AC-031` | The process model emits no checkpoint threshold, `proceed` decision, critical-risk status, release decision, or scalar process score. |
| `PR-AC-032` | The complete Section 12 fixture produces its exact action, lineage, reassessment, and comparison outcomes. |

## 15. Decisions, assumptions, contradictions, and blockers

### 15.1 Bounded decisions and scientific assumptions

| ID | Decision | Basis | Blocking? |
| --- | --- | --- | --- |
| `PR-D001` | `REFERENCE_VERIFICATION` is the only stage and maps to `tau^T`. | inherited `FM-D011`; Chapter 4.1 places dynamic evidence at `tau^T` and permits iterative stages | No |
| `PR-D002` | `K_0` is empty; no checkpoint decision is executable. | dissertation thresholds are context/calibration dependent; Full Model has no approved values | No |
| `PR-D003` | The only action is a non-optimal reconcile-bounds candidate. | inherited `FM-D010`; Chapter 4.3 rejects a rigid one-defect/one-action rule | No |
| `PR-D004` | Revision content and child version identity are externally supplied. | stakeholder intent cannot be inferred; parent contract requires stakeholder/fixture payload | No |
| `PR-D005` | The bounded action replaces text only and preserves requirement population/order. | minimum deterministic vertical slice; avoids inventing add/remove/split/merge lineage semantics | No |
| `PR-D006` | Applied means materialized, not successful. | action effect is determined only after ReEval and is not guaranteed | No |
| `PR-D007` | All requirement-derived results are rebuilt; exact dynamic observation reuse is separately auditable. | Chapter 4.1 version validity and parent reuse rule | No |
| `PR-D008` | Changed rule/model/parameter versions require explicit scoped semantic compatibility. | inherited `FM-D012`; prevents version-number inference | No |
| `PR-D009` | v0.1 authorizes no improvement/worsening wording, even for numeric increase/decrease. | conservative application of the parent polarity condition | No |
| `PR-D010` | Risk/problem disappearance is a categorical state change over a stable lineage/key scope. | risk contract has no magnitude or ordered no-risk class | No |
| `PR-D011` | Successor association is stored in an immutable transition rather than backfilled into v1 state. | immutable-history requirement | No |
| `PR-D012` | `FM-D015` approval at an exact commit remains required before production implementation. | inherited parent process gate | Yes |

### 15.2 Theoretical quantities deliberately not operationalized

The following remain `EXPERIMENTAL_CALIBRATION_REQUIRED` or outside the
bounded contract: checkpoint sufficiency and quality thresholds; critical-risk
classification; predicted `y_hat_PE`; evidence reliability percentages;
model uncertainty; action cost; expected causal effect; dependency centrality
or spread; probability, likelihood, impact, severity, criticality; numeric or
aggregate risk; prioritization; and causal before/after effect estimates.

### 15.3 Contradiction review

No contradiction was found among the existing Full Model contracts, QB-v0.1,
and the bounded dissertation interpretation.

The following apparent tensions are resolved explicitly rather than silently:

1. Chapter 4.1's full process state contains prediction, sufficiency,
   reliability, and uncertainty; v0.1 is a declared partial projection and does
   not fabricate them.
2. Chapter 4.1's checkpoint logic can initiate corrective action using
   calibrated thresholds or critical risks; this contract creates only a
   traceable candidate from an already identified bounded risk and makes no
   checkpoint or criticality decision.
3. Chapter 4.3 includes cost, expected effect, dependencies, prioritization,
   and numeric risk change; v0.1 preserves the known target/source/verification
   structure while leaving empirical quantities absent.
4. Dissertation notation `v+1` is a successor relation here, not an arithmetic
   versioning algorithm.
5. Chapter 4.3 discusses positive predicted-quality and negative numeric-risk
   deltas; v0.1 has neither calibrated prediction nor risk magnitude, so it uses
   typed exact-value or state comparisons only.
6. A dynamic conformance observation may remain identical while the v2 result
   becomes available because the specification conflict gate changed. That is
   an evidence/assessment-state change, not product improvement.

`RQD-016` remains open exactly as required by the defect/risk contract. This
contract consumes only its separate exact confirmed-supported-problem type and
does not promote existing C/V/U `SIGNAL` findings into defects. `RQD-016` does
not block this exact QB reference loop.

### 15.4 Implementation readiness

Subject to the inherited `FM-D015` approval gate, this contract provides
sufficient deterministic inputs for:

- M3-08: proposal identity, eligibility, statuses, provenance, non-optimality,
  and externally supplied application boundary;
- M3-09: immutable artifact/requirement lineage, ReEval, evidence reuse,
  semantic comparability, typed comparisons, and reference fixtures; and
- M3-10: the one-stage `M_process` projection, `ProcessAssessmentState`, and
  immutable process/reassessment lineage.

No additional scientific or semantic decision blocks the bounded reference
implementation. Work beyond this slice remains blocked on experimental
calibration or a new approved contract, especially lifecycle checkpoints,
prediction, numeric risk, prioritization, action optimization, broader edit
operations, causal effect evaluation, and a complete SDLC process engine.
