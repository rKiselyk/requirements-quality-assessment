# Full Model v1.0 theory-to-implementation traceability

Status: `ACCEPTED`

Acceptance marker: `TC06_INTEGRATED_RESEARCH_ACCEPTANCE_ACCEPTED`

Canonical evidence: `CONTROLLED_RESEARCH_REFERENCE_SCENARIO` in
`tests/reference_acceptance_data.py`, executed by
`tests/test_full_model_v1_research_acceptance.py` through the public
`FullModelService` boundary.

This matrix identifies the accepted integrated TC-06 realization over
executable, accepted TC-01 through TC-05 behavior. Historical `V0.1` contract
IDs are retained because they identify versioned components; they are not the
presentation identity of the integrated v1.0 research bundle.

| Dissertation process | Executable implementation | Contract/rule identity | Acceptance evidence |
|---|---|---|---|
| Requirement quality | automatic C/V/U plus TC-01 six-property external composition in `full_quality` | `CALC-C-MVP-001`, `CALC-V-MVP-001`, `CALC-U-MVP-001`; TC-01 typed profile | both R001 and R002 have nine independent property slots in the canonical scenario |
| P / specification consistency | `cross_analysis` and `metrics.MetricProfileBuilder` | `FULL-MODEL-V0.1-CONTRACT / 1`; `SPEC.QB_CONSISTENCY` | v1 conflict and exact `QB=0/1`; v2 exact `QB=1/1` |
| E | `dynamic_evidence` criterion binding, observation resolution, conformance | `FULL-MODEL-V0.1-DYNAMIC-EVIDENCE / 1`; binding/evaluator rules | explicit response-time criterion and `1.8 s` fixture observation produce `CONFORMS` |
| X_PE | `performance_efficiency.PerformanceEfficiencyFeatureProfileBuilder` | `FULL-MODEL-V0.1-PRODUCT-QUALITY-FEATURE / 1` | canonical `feature_profile` and its typed entries |
| M_quality observed | `product_quality.assess_product_quality` | `FULL-MODEL-V0.1-PRODUCT-QUALITY-ASSESSMENT / 1` | distinct observed `ProductQualityAssessment`; v1 unresolved value remains absent |
| Fθ → ŷ | `product_quality_prediction.predict_performance_efficiency` | `FULL-MODEL-V1.0-PE-PRODUCT-QUALITY-PREDICTION / 1`; `F-THETA-PE-001 / 1` | fixture-only predictor and theta produce exact `PredictedPerformanceEfficiency(5/6)` |
| D | `defect_quality.resolve_problem_claim` and `build_defect_population` | accepted problem rule and `FULL-MODEL-V0.1-DEFECT-QUALITY-RISK / 1` | v1 confirmed supported QB problem; bounded v2 supported problem disappears |
| R_DQ | `defect_quality.relate_problem_to_quality` | accepted relation rule | structural Performance Efficiency relation retains `NOT_NUMERIC_RHO` |
| categorical risk | `risk.assess_risk` | accepted risk rule/model | v1 `RISK_IDENTIFIED`; v2 `NOT_APPLICABLE` |
| r_ij | `quantitative_risk.calculate_quantitative_local_risk` | `FULL-MODEL-V0.1-QUANTITATIVE-LOCAL-RISK / 1`; `R-IJ-PE-001 / 1` | explicit `1/2 × 1/4 × 3/4 × 2/3 = 1/16` |
| A_corr | `corrective_action.propose_corrective_action` | accepted corrective-action rule | typed reconciliation proposal for the confirmed problem |
| ReEval | `reassessment.reevaluate` | `FULL-MODEL-V0.1-PROCESS-REASSESSMENT / 1` and accepted reassessment rule | external v2 artifact is reassessed with explicit evidence reuse |
| Compare | `reassessment.compare` | accepted comparison rule | literal `INCREASED` and `STATE_CHANGED` records, with no improvement interpretation |
| checkpoint | `checkpoint.select_metric_result` and `evaluate_checkpoint` | `FULL-MODEL-V1.0-SCALAR-CHECKPOINT / 1`; `CHECKPOINT-SCALAR-PREDICATE-001 / 1` | same external `SPEC.QB_CONSISTENCY >= 1/1` policy gives v1 `NOT_SATISFIED`, v2 `SATISFIED` |
| M_process | `process.assemble_process_state` and `assemble_process_transition` | accepted process rule | linked v1/v2 states and one typed transition |
| public application boundary | `full_model.FullModelService.run` | TC-05 public contract | exactly one call in the canonical acceptance test returns `FullModelResult` |
| USER/AUDIT | `UserFullModelReporter` and `AuditFullModelReporter` | read-only report projections | deterministic v1.0 headings, content assertions, and SHA-256 hashes |

## Explicitly bounded or unimplemented constructs

The canonical scenario does not implement or claim:

- exhaustive prediction across all nine product-quality characteristics;
- aggregate `Q_int`;
- aggregate `Risk_j` or `Ψ_j`;
- defect priority `Π_i`;
- a complete checkpoint set `K_k`;
- full `Decision_j(K_k)`, proceed authorization, or release approval;
- universal predictor or risk calibration, confidence, uncertainty, or validity;
- causal effect, proved correction success, or proved risk reduction;
- exhaustive NLP coverage, automatic rewriting, or production readiness.

