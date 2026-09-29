# Full Model v0.1 Final Contract Review

**Review ID:** `FULL-MODEL-V0.1-CONTRACT-REVIEW`  
**Review version:** `1`  
**Review date:** `2026-09-29`  
**Scope:** M3-02 through M3-12 bounded vertical slice  
**Status:** `SEMANTICALLY_READY / PARENT_APPROVAL_GATE_PENDING`

## 1. Review question and conclusion

This review asks:

> Is the complete Full Model v0.1 sufficiently specified to implement the
> entire bounded pipeline without downstream issues inventing new scientific
> semantics?

**Answer: YES.**

All blocking or important defects found in the cross-review were correctable
from already approved theory or repository contracts and have been corrected.
No unresolved semantic blocker remains inside the bounded path. The inherited
`FM-D015` researcher-approval requirement remains a process gate before
production implementation; it is not an unresolved scientific meaning.
`RQD-016` also remains open, but the bounded path does not depend on it because
only the separately typed exact QB confirmed problem may enter `D`.

This conclusion applies only to the bounded sequence:

```text
S -> (P, E_stat)
P -> M
S + external product observation -> E_dyn
(M, E_stat, E_dyn) -> X_PE -> M_quality
P -> D -> R_DQ
(D, R_DQ, M_quality as preserved context) -> M_risk
M_risk -> A_corr -> S(v+1) -> ReEval -> M_process
```

The sequence is a dependency graph, not a claim that every node is computed
linearly or that every preceding value is an assessment operand of every later
node.

## 2. Reviewed artifacts

### 2.1 Full Model contracts

| Artifact | Reviewed role |
| --- | --- |
| `docs/full-model-v0.1-contract.md` | parent decisions, pipeline, statuses, provenance, versioning, architecture, and downstream boundaries |
| `docs/full-model-v0.1-metric-profile-contract.md` | lossless `P -> M` adapter and exact metric registry |
| `docs/full-model-v0.1-dynamic-evidence-contract.md` | criterion, observation, conformance, exact Decimal, unit/context, and dynamic provenance |
| `docs/full-model-v0.1-product-quality-feature-contract.md` | bounded `X_PE`, feature roles, applicability, temporal availability, and conflict gate |
| `docs/full-model-v0.1-product-quality-assessment-contract.md` | bounded observed indicator, product-quality claims/non-claims, and absent prediction |
| `docs/full-model-v0.1-defect-quality-risk-contract.md` | confirmed problem eligibility, `D -> R_DQ`, and categorical bounded risk |
| `docs/full-model-v0.1-process-reassessment-contract.md` | corrective action, immutable versions, ReEval, comparison, and `M_process` |

### 2.2 Approved repository and QB inputs

| Artifact | Reviewed role |
| --- | --- |
| `docs/model-spec.md` | authoritative current C/V/U, evidence, assessment, aggregate, identity, and exact `Fraction` semantics |
| `docs/cross-requirement-consistency-decision-package.md` | approved QB-v0.1 scientific decisions, coverage, statuses, and non-claims |
| `docs/cross-requirement-consistency-architecture.md` | QB snapshot, comparison, evidence, provenance, normalization, and aggregation contracts |
| `docs/cross-requirement-consistency-reference-cases.md` | exact supported QB fixtures and expected classifications |
| `docs/srm-05-quantitative-research.md` | quantitative extraction research context |
| `docs/srm-05d-quantitative-context-linkage.md` | accepted context-linkage boundary |
| `docs/srm-05f-quantitative-boundaries-research.md` | comparator, inclusivity, exact bound, and unit research context |

The QB implementation plan was used only to check ownership boundaries. It did
not override the normative decision package, architecture, or model
specification.

Read-only conformance checks also covered the existing typed domain and
boundary implementations in `src/requirements_quality_assessment/domain/`,
the QB records/services in `src/requirements_quality_assessment/cross_analysis/`,
and the exact quantitative bridge in
`src/requirements_quality_assessment/detectors/quantitative.py`. These checks
verified existing type/identifier availability; they did not make production
code normative and no production file was changed.

### 2.3 Dissertation research references

| Reference | Reviewed theory |
| --- | --- |
| Chapter 2.1, `2.1_Властивості_вимог.docx` | requirement-property levels and separation from product quality |
| Chapter 2.2, `2.2_Взаємозвязок_вимог_і_якості.docx` | semantic, risk-mediated, and verification mechanisms; non-universal mapping |
| Chapter 2.3, `2.3_Система_метрик.docx` | metric profiles, applicability/missingness masks, no zero filling, and calibration boundary |
| Chapter 3.1, `3.1_Статичні_методи.docx` | static artifact evidence, provenance, and limits of static conclusions |
| Chapter 3.2, `3.2_Динамічні_методи.docx` | criterion-test/experiment-observation-conformance spine and missing-observation semantics |
| Chapter 3.3, `3.3_Метод_оцінювання.docx` | stage-aware assessment, evidence integration, calibration, and prediction boundary |
| Chapter 4.1, `4.1_Процесна_модель.docx` | lifecycle stages, versioned process state, evidence validity, feedback, and reassessment |
| Chapter 4.2, `4.2_Модель_якості.docx` | `X_j`, `F_theta`, product-quality profile, and experimental parameter boundary |
| Chapter 4.3, `4.3_Модель_ризиків.docx` | problem-quality relation, calibrated risk quantities, action tuple, and closed-loop reevaluation |

The dissertation is research context and traceability, not an executable
specification. No dissertation quantity was made executable unless the parent
or a focused contract already approved its bounded representation.

## 3. Findings

Every finding has one of the required severities. There are no unresolved
`BLOCKING` findings.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| `FMR-001` | `IMPORTANT` | The parent showed the bounded path as a linear chain, omitted `D/R_DQ`, `S(v+1)`, and `M_process`, placed evidence after `M`, and could be read as making product quality the source of risk. | Corrected to an explicit dependency graph and aligned transition table. |
| `FMR-002` | `IMPORTANT` | `ObservationSlotRef` contained `criterion_id`, although a dynamic observation is independent product evidence and the process contract permits exact observation reuse across specification versions. This made immutable reuse impossible when criterion identity changed with artifact version. | Removed criterion identity from the slot. `ConformanceAssessment` remains the sole criterion-to-slot binding. Added acceptance coverage. |
| `FMR-003` | `IMPORTANT` | The dynamic status table allowed upstream `UNKNOWN`, but deterministic precedence omitted it for both criterion and observation. | Added exact `UNKNOWN` propagation and an acceptance case. |
| `FMR-004` | `IMPORTANT` | Feature, quality, problem, relation, and risk results required `process_state_ref`, while `ProcessAssessmentState` required those completed results. Without a creation rule this was circular. | Defined a caller-reserved `ProcessStateRef`, followed by component execution and later immutable state assembly under the same ref. Added acceptance coverage and consumer clauses. |
| `FMR-005` | `IMPORTANT` | The process/reassessment contract lacked its own contract ID/version and parent reference, leaving its rule-version authority and component-version provenance incomplete. | Added normative metadata and parent-gate status. |
| `FMR-006` | `IMPORTANT` | The process contract redefined `RuleRef` and `ContractRef` with shapes incompatible with the dynamic/metric contracts. | Reused canonical `ContractRef(contract_id, version)` and `RuleRef(rule_id, explicit_version, version_authority)`; defined shorthand expansion. |
| `FMR-007` | `IMPORTANT` | The parent used `ProductQualityFeatureProfile`, while the focused contract defines `PerformanceEfficiencyFeatureProfile`; it also blurred stable `SpecificationArtifact` identity with immutable `SpecificationVersion`. | Made the exact concrete feature type and artifact/version distinction normative. |
| `FMR-008` | `IMPORTANT` | `ProcessAssessmentState` promised typed missing/unavailable associations, but optional component refs could be unexplained `None` and the evidence-association type could not describe non-evidence component absence. | Added `ProcessComponentAssociation`, consistency rules for convenience refs, and assembly-failure semantics. |
| `FMR-009` | `IMPORTANT` | Canonical statuses and applicability were reused under local type names without an explicit alias/mapping rule, risking silent enum collapse. | Defined canonical/local label equivalence while preserving source enum types and explicit mappings. |
| `FMR-010` | `IMPORTANT` | Two sentences literally stated “None means ... zero/poor quality,” contrary to their surrounding rules and the no-imputation contract. | Corrected both to “None of these statuses means ...”. No semantic decision was required. |
| `FMR-011` | `MINOR` | `ProductQualityAssessment.value` and `.observed_value` duplicate storage and could drift. | No contract change: the focused contract already requires exact equality or joint absence and explains compatibility ownership. Future validation must enforce the invariant. |
| `FMR-012` | `MINOR` | `status` names both canonical result availability and corrective-action lifecycle state. | No contract change: `CorrectiveActionResolution.status` and `CorrectiveAction.status` are separate records and the process contract explicitly declares them orthogonal. Renaming is optional engineering cleanup, not a semantic blocker. |
| `FMR-013` | `MINOR` | `X_PE` carries contextual C/V/U and QB features that do not affect the bounded product-quality procedure, creating a risk that an implementation treats all seven entries as numeric operands. | No contract change: roles and acceptance invariants already mark only criterion, observation, conformance, and conflict gate as assessment-affecting; C/V/U and QB aggregate values are context/provenance only. |
| `FMR-014` | `BLOCKING` | The authoritative `docs/model-spec.md` still labeled the exact QB `LB-M-C0` bridge and Rule/Evidence IDs unimplemented/unallocated, while the researcher-approved QB reference corpus both promoted an implemented binding end-to-end case and retained stale pre-implementation conclusions. This made the source of the sole exact conflict internally contradictory. | Reconciled the model specification and QB corpus to the already implemented-and-accepted exact bridge, allocated `QUANT-LB-METRIC-001`/`QUANT-LB-CONTEXT-001`, and preserved all wider grammar exclusions. No detector or scientific rule changed. |

## 4. Audit coverage

| Audit concern | Result | Evidence/finding |
| --- | --- | --- |
| 1. Missing transitions | Corrected | `FMR-001`; final process-state assembly is now explicit. |
| 2. Circular logic | Corrected | `FMR-004`; risk eligibility also excludes product-quality context. |
| 3. Duplicated concepts | Controlled | `FMR-007`, `FMR-011`; no competing semantic type remains. |
| 4. Incompatible terminology | Corrected/controlled | `FMR-006`, `FMR-007`, `FMR-009`, `FMR-012`. |
| 5. Inconsistent statuses | Corrected | `FMR-003`, `FMR-009`, `FMR-010`. |
| 6. Broken provenance | Corrected | `FMR-002`, `FMR-005`, `FMR-008`; all branches resolve to source evidence/version records. |
| 7. Versioning gaps | Corrected | canonical contract/rule refs, immutable artifact versions, lineage, parameter refs, collection refs, reserved process refs, and the existing QB lower-bridge rule versions are explicit (`FMR-014`). |
| 8. Applicability gaps | Corrected | canonical three-state applicability remains orthogonal; typed component absence is now explicit. |
| 9. Hidden normalization | None found | QB Unicode/text normalization remains identity-only; no numeric feature normalization is executable. |
| 10. Hidden zero imputation | Corrected wording; none remains | `FMR-010`; exact zero is allowed only as a real computed metric or categorical conformance encoding. |
| 11. Requirement/product-quality conflation | None found | C/V/U and QB metrics remain requirement/specification properties; they are not product-quality values. |
| 12. Observed/predicted conflation | None found | observed single-criterion indicator is explicit; `prediction_value`/`y_hat_PE` is absent. |
| 13. Unsupported causal claims | None found | `R_DQ`, risk, actions, comparisons, and reassessment all carry non-causal limitations. |
| 14. Uncalibrated scientific parameters | None presented as calibrated | all coefficients, weights, probabilities, impacts, reliabilities, uncertainties, and thresholds are absent/deferred. |
| 15. Risk exceeds evidence | None found | only categorical `RISK_IDENTIFIED`; product quality is context and no magnitude is claimed. |
| 16. Automatic correction assumptions | None found | only a proposal is system-generated; revision content and intent are external. |
| 17. Invalid comparisons | None found | subject lineage, metric/result family, scope, scale, semantics, versions, context, stage, and parameter compatibility gate comparison. |
| 18. Dissertation contradictions | None unresolved | bounded omissions are explicit projections, not replacements for the richer theory. |
| 19. Approved repository contradictions | Corrected; none unresolved | `FMR-014`; C/V/U, evidence, `Fraction`, QB `Decimal`, QB statuses, and `RQD-016` retain their approved meaning. |
| 20. Unnecessary complexity | Controlled | `FMR-011`-`FMR-013`; retained structure serves interoperability, provenance, or explicit layer separation. |

## 5. Corrections made

| File | Corrections |
| --- | --- |
| `docs/full-model-v0.1-contract.md` | Replaced the misleading linear path with the full DAG; corrected transition ownership; added `M_process` assembly; clarified risk context; fixed feature and specification terminology; documented status/applicability type relationships; changed provenance from a false chain to a graph; added the reserved-process-ref architecture rule; corrected zero-risk wording. |
| `docs/full-model-v0.1-dynamic-evidence-contract.md` | Made observation slots criterion-independent; located criterion binding exclusively in conformance; added exact upstream `UNKNOWN` propagation and acceptance cases. |
| `docs/full-model-v0.1-product-quality-feature-contract.md` | Declared `process_state_ref` a reserved context identity rather than an assembled-state dependency; corrected no-value wording. |
| `docs/full-model-v0.1-product-quality-assessment-contract.md` | Declared `process_state_ref` a reserved context identity rather than an assembled-state dependency. |
| `docs/full-model-v0.1-defect-quality-risk-contract.md` | Declared every `process_state_ref` a reserved context identity rather than an assembled-state dependency. |
| `docs/full-model-v0.1-process-reassessment-contract.md` | Added contract metadata; reused canonical ref shapes; defined two-phase process-state identity/materialization; distinguished artifact lineage from version snapshot; added typed component associations; strengthened acceptance cases and decisions. |
| `docs/model-spec.md` | Reconciled stale `LB-M-C0` implementation/identifier status with the already promoted, implemented, and accepted QB reference case; retained exact-envelope-only coverage and all wider `RQD-008` limits. |
| `docs/cross-requirement-consistency-reference-cases.md` | Marked the original extractor limitation as historical, made promoted Section 5.1 the current binding end-to-end case, and removed stale statements that the exact bridge remained unimplemented. |

No production code, detector rule, grammar, metric, comparator, unit, context,
formula, threshold, coefficient, or scientific parameter was added.

## 6. Remaining blockers and open decisions

### 6.1 Semantic blockers

**None for the bounded Full Model v0.1 pipeline.**

### 6.2 Process gate

`FM-D015` remains open until a researcher approves the exact parent-contract
commit. It blocks starting production implementation under the existing
delivery policy. It does not leave any bounded record, transition, status,
formula, identity, or claim undefined.

### 6.3 Deliberately open repository decision

`RQD-016` remains open for general conversion of existing findings into
`QUALITY_PROBLEM`. The bounded Full Model path does not close or consume that
decision. It admits only the separately defined, evidence-backed exact QB
`CONFIRMED_CONFLICT` through `D-QB-CONFLICT-001/v1`.

### 6.4 Out-of-scope research

Broader product-quality prediction, quantified risk, action optimization,
checkpoint decisions, general correction operations, additional metrics,
units, contexts, and characteristics require future approved contracts and/or
experimental calibration. Their absence does not block the bounded slice.

## 7. Contradictions found

### 7.1 Corrected internal contradictions

1. The former parent pipeline ordering conflicted with its own detailed
   transition table and with the focused defect/risk contracts (`FMR-001`).
2. Criterion-bound observation slots conflicted with the declared independence
   of observed product evidence and the process contract's exact reuse rule
   (`FMR-002`).
3. The dynamic allowed-state table conflicted with its propagation precedence
   for `UNKNOWN` (`FMR-003`).
4. Component-to-process-state references and process-state-to-component
   references formed an undeclared construction cycle (`FMR-004`).
5. Two no-value sentences contradicted the no-zero-imputation invariants
   (`FMR-010`).
6. The authoritative model specification and two temporal layers inside the
   QB reference corpus disagreed on whether the exact lower-bound bridge and
   identifiers existed (`FMR-014`).

All five are corrected. No researcher judgment was needed because the approved
contracts and dissertation separation rules determine the correction.

### 7.2 External contradictions

No unresolved contradiction was found with `docs/model-spec.md`, QB-v0.1, or
the bounded interpretation of dissertation Chapters 2-4.

QB-v0.1's earlier deferral of remediation lifecycle does not prohibit Full
Model v0.1 from adding a separate external action/version/reassessment layer.
The action never mutates or reinterprets the prior QB snapshot; it creates a
new specification version and obtains a new QB assessment.

## 8. Decision consistency matrix

| Parent decision | Metric | Dynamic | `X_PE` | Quality | Defect/risk | Process | Consistency result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `FM-D001` PE reference characteristic | no contribution invented | response time only | registry fixed to PE | PE scoped result | relation only to PE | PE records associated | Consistent |
| `FM-D002` exact `P_v0.1` set | exact registry | consumes quantitative source directly | only registered contextual entries | C/V/U/QB cannot weight result | only exact QB conflict enters `D` | recomputes same set | Consistent |
| `FM-D003` lossless `P -> M` | exact `Fraction`, source states/provenance | no metric recomputation | values copied by role | no use as predictor | no metric-to-risk shortcut | exact comparison only | Consistent |
| `FM-D004` bounded dynamic evidence | no dynamic metric entry invented | `<=`, `SECOND`, exact context/Decimal | criterion/observation/conformance features | exact categorical encoding | observation not defect evidence | explicit reuse gate | Consistent |
| `FM-D005` observed indicator, no prediction | no product score | categorical conformance only | no assessment | exact `{0,1}` reference indicator | result preserved as context only | comparison keeps bounded scope | Consistent |
| `FM-D006` presence inventory, no numeric reliability | source evidence refs only | source/collection refs | typed availability | categorical coverage record | typed provenance/status | evidence/component associations | Consistent |
| `FM-D007` exact eligible problem | no C/V/U promotion | no conformance promotion | conflict gate only | no defect creation | exact QB confirmed conflict only | action traces same problem | Consistent |
| `FM-D008` non-causal `R_DQ` | N/A | N/A | target key only | no causal effect | bounded relevance only | comparisons prohibit causality | Consistent |
| `FM-D009` categorical risk | N/A | N/A | no risk calculation | no risk calculation | `RISK_IDENTIFIED`, no magnitude | categorical state comparison | Consistent |
| `FM-D010` external correction | N/A | N/A | N/A | N/A | no recommended action field | proposal plus external revision | Consistent |
| `FM-D011` one `tau^T` stage | versioned inputs | collection at reference verification | process ref/stage | scope includes stage | process ref/stage | sole stage fixed | Consistent |
| `FM-D012` compatibility-gated comparison | exact metric identity | exact context/unit/criterion | profile semantics | result kind/scope | categorical states | full compatibility predicate | Consistent |
| `FM-D013` canonical statuses | exact mapping | complete propagation | exact propagation | exact propagation | exact propagation | typed associations | Consistent after `FMR-003`, `FMR-009`, `FMR-010` |
| `FM-D014` calibration boundary | no calibrated values | no statistical inference | no normalized vector | no `F_theta`/`y_hat` | no numeric risk | no threshold/causal delta | Consistent |
| `FM-D015` approval gate | inherited | inherited | inherited | inherited | inherited | inherited | Open process gate; no semantic gap |

## 9. End-to-end traceability matrix

| Stage | Input | Output | Governing contract/rule | Exact evidence/value | Non-claim preserved |
| --- | --- | --- | --- | --- | --- |
| `S -> P, E_stat` | immutable specification version | C/V/U profiles, aggregates, QB assessment, evidence/traces | `docs/model-spec.md`; approved QB contracts | source text/spans, trace states, exact `Fraction`/`Decimal` | no complete language/consistency coverage |
| `P -> M` | completed C/V/U and QB results | `MetricProfile`/`MetricEntry` | Metric Profile contract | exact `Fraction` or typed absence; source refs | no normalization, weighting, scalar quality |
| `S -> criterion` | accepted quantitative source observation | `QuantitativeCriterion` | `DYN-BIND-RT-001/1` | own requirement bound as exact `Decimal` | no invented threshold |
| product source -> observation | controlled fixture record | `DynamicObservation` | Dynamic Evidence source contract | exact `Decimal`, unit, context, product/collection | not telemetry/statistical evidence |
| criterion + observation -> conformance | same metric/unit/context | `ConformanceAssessment` | `DYN-CONFORMANCE-RT-001/1` | categorical exact comparison | missing is not failure; one result is not full PE |
| `M + E -> X_PE` | metric/static/dynamic records | `PerformanceEfficiencyFeatureProfile` | PE feature registry/mapping | typed source refs, roles, statuses, conflict gate | contextual metrics are not predictors |
| `X_PE -> M_quality` | available clear-target conformance profile | `ProductQualityAssessment` | `PE-OBS-CONFORMANCE-001/1` | exact `Fraction(1,1)` or `(0,1)` categorical encoding | not `y_hat_PE`, complete PE, probability, or accuracy |
| `P -> D` | exact QB cross result | confirmed supported problem or typed non-value | `D-QB-CONFLICT-001/1` | participants, bounds, comparison key, QB proof | no `SIGNAL`/score promotion; `RQD-016` open |
| `D -> R_DQ` | eligible exact problem | PE relevance relation | `R_DQ-PE-QB-001/1` | exact problem/key/evidence refs | relevance is not causality/probability |
| `D + R_DQ -> M_risk` | available problem/relation; quality context | bounded risk assessment | `RISK-PE-QB-001/1` | categorical `RISK_IDENTIFIED` | presence is not magnitude, likelihood, impact, or priority |
| `M_risk -> A_corr` | exact risk/problem/relation | proposal resolution/action | `ACTION-RECONCILE-QB-001/1` | target lineages and rationale | candidate is not optimal; no stakeholder-intent choice |
| action + external revision -> `S(v+1)` | proposed action and supplied replacement | application, immutable child, transition | `APPLY-EXTERNAL-REVISION-001/1` | exact parent/child/action/revision/changed subjects | applied does not mean conflict resolved |
| `S(v+1) -> ReEval` | immutable child and versioned context | rebuilt results, reuse decisions, comparisons | `REEVAL-FULL-MODEL-001/1`; `COMPARE-FULL-MODEL-001/1` | exact component/evidence/rule/model/parameter versions | numeric change is not improvement or causal effect |
| completed records -> `M_process` | reserved process ref and typed component records | immutable `ProcessAssessmentState`/transition | `PROCESS-REFERENCE-VERIFICATION-001/1` | typed component/evidence associations and lineage | no process score, checkpoint, release, or full SDLC claim |

## 10. Implementation readiness, M3-02 through M3-12

`READY` below means semantically deterministic for the bounded scope after the
parent approval gate. It does not authorize implementation before `FM-D015` is
satisfied.

| Issue | Readiness | Deterministic input supplied | Remaining boundary |
| --- | --- | --- | --- |
| M3-02 / #139 | `READY` | closed metric registry, scope/subjects, exact values, statuses, ordering, provenance, acceptance cases | adapter only; no recalculation/normalization |
| M3-03 / #140 | `READY` | criterion, independent observation, conformance, Decimal/unit/context/source identity, full propagation | controlled fixture only; no collection infrastructure |
| M3-04 / #141 | `READY` | exact seven-entry `X_PE`, feature roles, target gate, temporal/status/provenance rules | no added feature/metric coverage |
| M3-05 / #142 | `READY` | bounded observed result schema, exact categorical encoding, coverage, calibration status, claims/non-claims | no predicted or complete PE |
| M3-06 / #143 | `READY` | exact confirmed-problem admission and non-causal PE relation | no general defect conversion; `RQD-016` remains open |
| M3-07 / #144 | `READY` | categorical risk result, state precedence, empty parameter set, provenance | no numeric risk quantities |
| M3-08 / #145 | `READY` | action identity, eligibility, proposed/applied split, external-authority boundary | no automatic replacement choice/optimization |
| M3-09 / #146 | `READY` | immutable specification versions, requirement lineage, ReEval, reuse and compatibility rules | replacement-only bounded operation |
| M3-10 / #147 | `READY` | one-stage process state, reserved identity, typed associations, immutable transitions | no checkpoint or complete lifecycle engine |
| M3-11 / #148 | `READY` | all result schemas, exact statuses, explanations, provenance, and mandatory claim boundaries | display/layout is engineering; reporter may not calculate or reinterpret |
| M3-12 / #149 | `READY` | deterministic positive/negative/unavailable dynamic fixtures plus v1 conflict/action/v2 reassessment scenario | integration must use the closed registries and exact fixture identities |

No issue in this range needs to invent a new scientific formula, threshold,
weight, mapping, status, applicability rule, evidence meaning, or causal claim
to implement the bounded path.

## 11. Experimental-calibration work deferred beyond Full Model v0.1

The following work remains explicitly `EXPERIMENTAL_CALIBRATION_REQUIRED`:

- selecting and validating a product-quality function `F_theta_PE`;
- feature selection for prediction and any coefficients, intercepts, weights,
  polarity transformations, normalization, or learned parameters;
- predicted `y_hat_PE`, prediction error, accuracy, confidence intervals, and
  comparison of prediction with observed quality;
- full Performance Efficiency coverage, subcharacteristic aggregation, and
  multi-observation or multi-context aggregation;
- evidence coverage percentages, reliability, repeatability, validity, and
  model uncertainty values;
- statistical sampling, repeated measurements, variability, percentiles,
  tolerances, and performance distributions;
- unit conversion and context-equivalence models;
- defect severity and numeric detection confidence;
- `rho_ij`, `p_ij`, `I_ij`, `kappa_j(C)`, `r_ij`, `Psi_j`, and aggregate
  `Risk_j`;
- risk likelihood, probability, impact, severity, criticality, magnitude,
  priority, ranking, and dependency/causal propagation;
- action cost, expected causal effect, optimization, prioritization, and
  automated stakeholder-intent resolution;
- calibrated evidence/quality/risk checkpoint thresholds and lifecycle
  proceed/hold/release decisions; and
- causal estimates of product-quality or risk change after requirement edits.

None of these quantities has a placeholder zero, one, percentage, default,
synthetic confidence, or provisional numeric estimate in Full Model v0.1.

## 12. Final bounded claims and non-claims

### 12.1 Claims permitted

Full Model v0.1 may claim that:

- the bounded pipeline is deterministic, versioned, explainable, and auditable;
- existing C/V/U and QB results are preserved without semantic change;
- `P -> M` is a lossless adapter over a closed registry;
- one exact response-time observation conforms or does not conform to one
  explicit requirement criterion in the same supported unit/context;
- the exact `{0,1}` result is an observed single-criterion conformance
  indicator only;
- one exact QB direct bound conflict is a confirmed supported specification
  problem within QB-v0.1;
- that problem has a bounded, non-causal relevance relation to Performance
  Efficiency;
- the provisional categorical rule identifies bounded risk presence;
- the system may propose reconciliation while external authority supplies any
  revision content;
- a child specification and all reevaluated results preserve immutable
  lineage, provenance, and semantic versions; and
- before/after records can be compared only when the complete compatibility
  predicate succeeds.

### 12.2 Claims forbidden

Full Model v0.1 must not claim:

- a scalar overall requirement, specification, product, risk, or process
  quality value;
- universal completeness, verifiability, unambiguity, or consistency;
- that C/V/U or QB metrics are product-quality scores or predictors;
- predicted `y_hat_PE` or complete Performance Efficiency;
- that one observation represents the product across time, loads, contexts,
  or Performance Efficiency subcharacteristics;
- that missing observation is failure, success, nonconformance, or zero;
- that `{0,1}` is a calibrated probability, percentage, confidence, accuracy,
  normalized quality level, or ratio scale;
- that the defect-quality relation proves product causality;
- any quantified risk magnitude, likelihood, impact, severity, criticality,
  priority, or aggregate;
- that absence of the bounded problem proves defect-free, safe, or zero risk;
- that a proposed/applied correction is correct, optimal, or stakeholder
  approved merely because it was materialized;
- that a larger metric value is necessarily improvement; or
- that requirement-quality change caused product-quality or risk improvement.

## 13. Final readiness statement

The complete Full Model v0.1 contract set is scientifically and
architecturally sufficient for the entire bounded M3-02 through M3-12 pipeline.
Its transitions, identities, exact numeric representations, applicability,
statuses, provenance, versions, temporal context, comparison rules, and claim
limits are deterministic. Downstream issues do not need to invent new
scientific semantics.

Implementation remains procedurally gated by `FM-D015`. Anything outside the
bounded claims above requires a new reviewed contract, experimental
calibration, or both.
