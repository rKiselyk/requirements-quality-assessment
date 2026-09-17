# Requirements Quality Assessment Model Specification

**Status: DRAFT — characteristic result and finding contracts incorporated;
executable per-requirement Completeness, Verifiability, and Unambiguity
calculation rules (`CALC-C-MVP-001`, `CALC-V-MVP-001`, `CALC-U-MVP-001`) are
now incorporated; the internal production numeric representation for
per-requirement and specification-level aggregate characteristic scores is
now approved as Python standard-library `fractions.Fraction` (Section 13);
specification-level aggregation semantics (`AGG-MVP-001`, Section 12) are now
`APPROVED_FOR_MVP_V0.1`; `QUALITY_PROBLEM` conversion and downstream
presentation/rounding semantics remain open**

This document is the prospective authoritative implementation specification for
MVP v0.1. It formalizes only what can be traced to the supplied research
references or to an explicit approved MVP constraint. Anything marked
`PARTIALLY_DEFINED`, `AMBIGUOUS`, `MISSING`, or `PROPOSED` is not approved for
implementation. Codex must not resolve such items by assumption.

## 1. Purpose

The purpose of this specification is to define the contract between the
dissertation model and its software implementation. Once approved, it will
govern feature extraction, characteristic calculations, aggregation,
explainability, and reference tests for MVP v0.1.

The supplied research describes both the quality of requirements as information
artifacts and a broader system that predicts software-product quality from
requirements and other lifecycle evidence. Chapter 2 explicitly separates the
individual-requirement level from the specification level and separates both
from product quality. MVP v0.1 is narrower than the full research system: it is
intended to evaluate three properties of an individual textual requirement and
then produce requirement-level and file-level summaries.

The researcher-approved MVP unit of analysis is one individual textual software
requirement, `r_i`. For MVP input, one non-empty input line is one requirement.
MVP v0.1 evaluates Requirement Quality as the quality of that requirement
information artifact. It does not predict software-product quality.

The primary per-requirement result is the multidimensional profile
`A_i = (C_i, V_i, U_i)`. MVP v0.1 does not require a scalar integrated
Requirement Quality score. A future integrated index would require a separate
researcher-approved scientific decision.

## 2. Scope of MVP v0.1

MVP v0.1 covers only this flow:

```text
UTF-8 requirements file
        ↓
deterministic textual and structural feature extraction
        ↓
Completeness   Verifiability   Unambiguity
        ↓
RequirementQualityProfile (C, V, U)
        ↓
property-level specification aggregation
        ↓
SpecificationQualityProfile (mean C, mean V, mean U)
        ↓
explainable console output
```

The unit of analysis is one individual textual software requirement, represented
in the input by one non-empty, trimmed line. The reader preserves source line
number and processing order and assigns IDs `R001`, `R002`, and so on.

The following are outside MVP v0.1: per-line Consistency or Traceability,
specification/global Completeness, requirements coverage, product-quality
prediction, risk, corrective actions, database storage, REST API, web UI,
authentication, Docker, cloud infrastructure, custom neural-network training,
LLM API integration, defect-probability prediction, iterative lifecycle
reassessment, and advanced semantic consistency analysis. These broader
properties require a requirement set, artifact relationships, lifecycle
evidence, or other context and remain future extensions.

## 3. Source and traceability policy

The source hierarchy is:

```text
Research references in docs/reference/
        ↓ formalization and researcher approval
docs/model-spec.md
        ↓ implementation
source code
        ↓ verification
tests
```

The files in `docs/reference/` provide theory and traceability. They are not
executable specifications. Demonstration values are not model constants.

Primary sources analyzed:

- [Requirement properties](reference/2.1_Властивості_вимог.docx), Section 2.1;
- [Requirements and product quality](reference/2.2_Взаємозвязок_вимог_і_якості.docx), Section 2.2;
- [Requirements metrics system](reference/2.3_Система_метрик.docx), Section 2.3;
- [Static methods](reference/3.1_Статичні_методи.docx), Section 3.1;
- [Dynamic methods](reference/3.2_Динамічні_методи.docx), Section 3.2;
- [Assessment method](reference/3.3_Метод_оцінювання.docx), Section 3.3;
- [Process model](reference/4.1_Процесна_модель.docx), Section 4.1;
- [Quality model](reference/4.2_Модель_якості.docx), Section 4.2;
- [Risk model](reference/4.3_Модель_ризиків.docx), Section 4.3;
- [Chapter 4 conclusions](reference/Висновки_до_розділу_4.docx);
- [Application example](reference/Приклад_застосування_моделі.docx).

No separate terminology or notation reference was present. Sections 2.1-2.3
now provide the previously missing definitions of requirement properties,
quality/product-quality separation, metric classes, applicability, polarity,
and missing-value semantics. They do not define a complete executable MVP
feature registry or calculator rules.

### 3.1 Decision classification policy

This draft separates three levels of knowledge:

1. **Explicitly defined by the dissertation**: a definition, formula, invariant,
   or distinction appears directly in a research reference.
2. **Derivable without a new scientific assumption**: a software-facing
   consequence follows directly from an explicit definition, without choosing
   a new formula, threshold, vocabulary, weight, or interpretation.
3. **Implementation operationalization requiring researcher approval**: a
   deterministic detector, applicability rule, feature schema, score mapping,
   threshold, aggregation rule, or other choice is not uniquely fixed by the
   references.

An explicit research formula may still be non-executable when its operands,
applicability set, or confirmation procedure are not operationally defined.

### 3.2 Research traceability table

| Model concept | Source document | Source section | Formal definition available? | Required for MVP? | Implementation status |
| --- | --- | --- | --- | --- | --- |
| Research-to-implementation hierarchy | `docs/reference/README.md` | Rules 1-5 | Yes | Yes | `DEFINED` |
| Requirement quality as a multidimensional property of an information artifact | Requirement properties | 2.1, paragraphs 2-6 | Yes conceptually | Yes | `DEFINED` |
| Individual-requirement and specification-level assessment are distinct | Requirement properties | 2.1, paragraphs 5 and 11-16 | Yes | Yes | `DEFINED` |
| Requirement Quality and Predicted Product Quality are distinct | Requirement properties; requirements/product quality | 2.1, paragraph 30; 2.2, paragraphs 2-5 | Yes | Yes | `DEFINED` |
| Primary feature, measure, and indicator are distinct concepts | Metrics system | 2.3, paragraph 4 | Yes | Yes | `DEFINED` |
| A requirements metric must define object/applicability, reproducible algorithm, polarity, source, automation, and semantic context | Metrics system | 2.3, paragraph 5 | Yes as methodological constraints | Yes | `DEFINED` |
| Lifecycle stage set `T = {requirements, architecture, implementation, test, operation}` | Process model | 4.1, Eq. `T` and Table 4.1 | Yes | No | `OUT_OF_SCOPE_V0.1` |
| Versioned assessment state `P_j(stage, version)` | Process model | 4.1, state tuple | Yes at conceptual level | No | `OUT_OF_SCOPE_V0.1` |
| Reassessment after changed evidence or specification | Process model | 4.1, update operator and feedback loop | Conceptual operator only | No | `OUT_OF_SCOPE_V0.1` |
| Evidence coverage and reliability are distinct from score | Process and quality models | 4.1 Tables 4.2-4.4; 4.2 result tuple | Conceptually yes; numeric rules absent | Potentially | `PARTIALLY_DEFINED` |
| Missing/not-applicable evidence is not zero | Requirement properties; metrics system; process and quality models; approved RQD-023 | 2.3, paragraphs 16 and 39-42; 4.1 invariants; 4.2 feature formation; Section 7.16 | Criterion applicability and characteristic assessment states are approved; required detector `UNRESOLVED` propagates to assessment `UNKNOWN` with no value; specification-level aggregation propagation is now approved under `AGG-MVP-001` (Section 12) | Yes | `APPROVED_FOR_MVP_V0.1` |
| Completeness of an individual requirement | Requirement properties | 2.1 Table 2.1 and paragraphs 11-12; Table 2.3; Section 7.16 | Semantic definition, evidence classes, and non-numeric result envelope available; `CALC-C-MVP-001` now supplies an executable three-criterion MVP formula (Section 8) | Yes | `APPROVED_FOR_MVP_V0.1` |
| Verifiability of an individual requirement | Requirement properties; metrics system | 2.1 Table 2.1 and paragraph 12; 2.3 paragraphs 17-21; Section 7.16 | Semantic definition, evidence classes, and non-numeric result envelope available; `CALC-V-MVP-001` now supplies an executable alternative-evidence-path MVP formula (Section 9) | Yes | `APPROVED_FOR_MVP_V0.1` |
| Unambiguity of an individual requirement | Requirement properties | 2.1 Table 2.1 and paragraph 10; Table 2.3; Section 7.16 | Semantic definition, source-derived signals, and signal finding rule available; `CALC-U-MVP-001` now supplies an executable signal-presence MVP formula (Section 10); confirmed-material-ambiguity (`0`) remains a future separate decision | Yes | `APPROVED_FOR_MVP_V0.1` |
| Consistency | Requirement properties; metrics system | 2.1 paragraphs 14-15; 2.3 paragraphs 28-30 | Defined primarily for a set of requirements | No, except as boundary context | `OUT_OF_SCOPE_V0.1` |
| Traceability | Requirement properties; requirements/product quality; metrics system | 2.1 paragraph 16; 2.2 paragraphs 23 and 27; 2.3 paragraphs 22-24 | Defined as a structural relationship property | No for text-only MVP | `OUT_OF_SCOPE_V0.1` |
| Individual property result `a_ij` | Requirement properties | 2.1 paragraphs 20-24 and Table 2.3 | Range and examples defined; per-requirement property-specific derivation is now approved for MVP v0.1 by `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10). This is an MVP v0.1 operationalization, not a closure of broader future research into `a_ij` beyond the approved scope (e.g. confirmed-material-ambiguity `0`, specification-level aggregation) | Yes | `APPROVED_FOR_MVP_V0.1` (per-requirement scope) |
| Stateful `CharacteristicAssessment` envelope | Requirement properties; metrics system; assessment method; researcher-approved Section 7.16 | 2.1 paragraphs 18-26; 2.3 paragraphs 37-40; 3.3 paragraphs 9-19 and 29-35 | Characteristic identity, computed/not-applicable/unknown state, nullable value, rule provenance, findings, and explanation are approved; per-requirement numeric derivation is now approved via `CALC-C/V/U-MVP-001`; specification-level aggregation derivation is now likewise approved via `AGG-MVP-001` (Section 12) | Yes | `APPROVED_DATA_CONTRACT / PER-REQUIREMENT_AND_AGGREGATE_CALCULATION_APPROVED` |
| Specification-level property indicator `x_j = mean_i(a_ij)` | Requirement properties; approved aggregation correction | 2.1 paragraphs 22-24 | Property-level mean is approved for computed/applicable values; exact missing/`UNKNOWN` propagation is now closed under `AGG-MVP-001` (Section 12): `UNKNOWN` values are excluded from the mean and tracked as `unknown_count`, never treated as zero | Yes | `APPROVED_FOR_MVP_V0.1` |
| Per-requirement feature/observation registry | Metrics system; researcher-approved Section 7 contract | 2.3 paragraphs 4 and 6-8; Sections 7.2, 7.14, and 7.15 | Six repeatable feature families and their typed detection wrappers are approved; `COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, `VERIFY-UK-001`, and the quantitative/vague lexical baselines are allocated, while remaining parser/template grammar stays open | Yes | `DEFINED` at registry/data level; detectors `PARTIALLY_DEFINED` |
| Candidate structural fields `has_actor`, `has_action`, `has_object` | MVP-SPEC issue; researcher-approved Section 7.11 disposition | Candidate list and Section 7.11 | No research definition in supplied references | No; possible optional future observations only | `DEFERRED_FROM_MVP_V0.1` |
| Condition/context, expected result, acceptance criterion, linked quantitative constraint, and explicit verification method | Requirement properties; requirements/product quality; metrics system; static and dynamic methods; researcher-approved Sections 7.14-7.15 | 2.1 Table 2.1 and paragraphs 11-12; 2.2 Tables 2.4-2.5; 2.3 Table 2.7 and paragraphs 17-21; 3.1 paragraph 13; 3.2 Table 3.4; Sections 7.14-7.15 | Semantic features, conservative strategies, backend and data shape approved; `COND-UK-001` supplies a narrow condition/context baseline, `RESULT-UK-001` a narrow normative-modal expected-result baseline, `ACCEPT-QUANT-001` a clause-level quantitative acceptance baseline, and `VERIFY-UK-001` the three explicitly governed verification-method constructions, while general parser/template rules, non-numeric acceptance grammar, and complex metric/context grammar remain open | Yes | `PARTIALLY_APPROVED` |
| Vague-term and linguistic-smell evidence | Requirement properties; metrics system; dynamic methods; application example; researcher-approved Sections 7.8 and 7.14 | 2.1 paragraph 10; 2.3 paragraphs 12-16; 3.2 paragraph 10; application Sections 2-3, 7-8, and 13 | `uk_vague_terms_v1` and exact MVP seed-matching mechanics approved; richer linguistic coverage deferred without keeping `RQD-007` open | Yes | `APPROVED_FOR_MVP_V0.1` |
| Per-requirement Completeness score | Requirement properties supplies only the generic property range | 2.1 `a_ij ∈ [0,1]`; Section 7.16.7 | `CALC-C-MVP-001` approves `C_i = (c_condition + c_result + c_acceptance) / 3` over the three MVP-mandatory criteria, exact value set `{0, 1/3, 2/3, 1}` | Yes | `APPROVED_FOR_MVP_V0.1` |
| Per-requirement Verifiability score | Requirement properties and metrics system supply evidence classes and set-level ratios only | 2.1 Table 2.3; 2.3 paragraphs 17-20; Section 7.16.7 | `CALC-V-MVP-001` approves an alternative-evidence-path mapping (acceptance criterion → `1`; quantitative or verification method only → `1/2`; none after complete processing → `0`), exact value set `{0, 1/2, 1}` | Yes | `APPROVED_FOR_MVP_V0.1` |
| Per-requirement Unambiguity score | Requirement properties supplies boundary meanings and an unspecified intermediate state | 2.1 Table 2.3; Section 7.16.7 | `CALC-U-MVP-001` approves signal-presence mapping (no supported signal → `1`; one or more → `1/2`); `0` remains reserved for a future separately-approved confirmed-ambiguity rule | Yes | `APPROVED_FOR_MVP_V0.1` (automated scale only; `0` still `OPEN`) |
| Characteristic score range for MVP | Requirement properties | 2.1 `a_ij ∈ [0,1]` and Table 2.3 | `[0,1]` compliance orientation supported; each characteristic's exact permitted value set is closed for MVP v0.1 (Completeness `{0,1/3,2/3,1}`; Verifiability `{0,1/2,1}`; Unambiguity `{1/2,1}` automated, `0` reserved). Specification-level range is now likewise closed as a direct mathematical consequence of `AGG-MVP-001` (Section 12): whenever a numeric aggregate exists, `C_file, V_file ∈ [0,1]` and `U_file ∈ [1/2,1]` under the current automated MVP rules, same upward compliance orientation | Yes | `APPROVED_FOR_MVP_V0.1` (per-requirement and specification-level aggregate range) |
| Requirements metric families and working dictionary | Metrics system | 2.3 Tables 2.7-2.8 | Aggregate formulas explicit; detector operands and applicability incomplete | Partially | `PARTIALLY_DEFINED` |
| Applicability set and empty-denominator `NA` | Metrics system | 2.3 paragraphs 13-16 and 39 | Principle explicit; per-requirement applicability rules absent | Yes | `PARTIALLY_DEFINED` |
| Scalar Requirement Quality Score from the three MVP characteristics | None in supplied references; approved RQD-013 disposition | Not defined and intentionally deferred | No | No | `OUT_OF_SCOPE_V0.1` |
| Scalar File Quality Score from requirement scores | None in supplied references; approved RQD-014 disposition | Not defined and intentionally deferred | No | No | `OUT_OF_SCOPE_V0.1` |
| Product-quality predictor `y_hat_j = F_theta_j(X_j, C)` | Quality model | 4.2, general prediction form | Abstract form and `[0,1]` range; model class/parameters unset | No | `OUT_OF_SCOPE_V0.1` |
| Logistic predictive baseline | Quality model and application example | 4.2 baseline; example Section 5 | Formula shown; example coefficients explicitly demonstrational | No | `OUT_OF_SCOPE_V0.1` |
| Context-weighted product-quality index `Q_int` | Quality model and application example | 4.2 aggregation; example Section 6 | General weighted form; weights context-dependent | Not directly | `OUT_OF_SCOPE_V0.1` |
| Non-compensated critical thresholds | Process and quality models | 4.1 checkpoints; 4.2 admissibility | Logical form exists; thresholds unset | Not currently | `OUT_OF_SCOPE_V0.1` |
| Finding/defect evidence | Requirement properties; metrics system; static methods; risk model; Section 7.16 | 2.1 paragraph 10; 2.3 paragraphs 12-16 and 30; 3.1 paragraphs 10 and 29-31; 4.3 defect tuple | Minimal MVP Finding contract, vague-term signal conversion, and absence provenance are approved; quality-problem conversions absent | Yes for explainability | `APPROVED DATA CONTRACT / QUALITY_PROBLEM RULES BLOCKED` |
| Local risk `r_ij` and risk aggregation | Risk model | 4.3 local risk and `Psi_j` | Local formula exists; inputs and aggregate operator require calibration | No | `OUT_OF_SCOPE_V0.1` |
| Corrective actions and iterative reassessment | Process and risk models | 4.1 feedback; 4.3 action tuple and loop | Conceptual structure exists | No | `OUT_OF_SCOPE_V0.1` |
| Manually approved reference cases for MVP scores | Requirement properties; metrics system; application example | 2.1 Tables 2.1-2.3; 2.3 Tables 2.7-2.8; example Sections 2-12 | Qualitative and aggregate examples exist; approved per-line expected scores absent | Yes | `PARTIALLY_DEFINED` |

## 4. Terminology and mathematical notation

### 4.1 Concept-definition and approval boundaries

| Concept | Explicitly defined by the dissertation | Derivable without a new scientific assumption | Implementation operationalization requiring researcher approval |
| --- | --- | --- | --- |
| **Requirement Quality** | A multidimensional quality of a requirements information artifact, evaluated through relevant properties at individual-requirement and/or specification level. It is not limited to grammatical correctness. | The approved MVP profile is `A_i = (C_i, V_i, U_i)` for one textual requirement represented by one non-empty input line. It must not be presented as observed or predicted product quality. | Any future scalar integrated Requirement Quality index. |
| **Completeness** | At individual level, sufficient information to understand the condition, expected reaction, and fulfilment criterion; at specification level, coverage of required functions, quality characteristics, interfaces, constraints, and significant scenarios. | Local completeness does not establish global coverage. Only elements applicable to the requirement type/template can be required locally. | Required element sets by type, element detectors, overlap with Verifiability, and mapping to `a_i,C`. |
| **Unambiguity** | Wording allows one justified interpretation in its context. Absence of ambiguous terms and stable reviewer interpretation are evidence; linguistic smells are possible automated signals. | A detected smell cannot be reported as a confirmed ambiguity without an approved confirmation rule. | Vocabulary, context exceptions, confirmation procedure, applicability, and mapping of signals to `a_i,U`. |
| **Verifiability** | A reproducible way exists to establish fulfilment. Evidence may include an acceptance criterion, threshold, test oracle, or analysis/inspection method. | For applicable quality requirements, quantity, unit, measurement conditions, and admissible boundary are distinct relevant observations; not every quality requirement must be numeric. | Requirement-type/applicability rules, evidence detection and linkage, and mapping to `a_i,V`. |
| **Consistency** | A set-level property concerning absence of logical, terminological, or resource conflicts among requirements. | It cannot be established from one isolated requirement line without information about other requirements or shared terms/resources. | Conflict definitions, comparison scope, confirmation, and any relation to the three MVP characteristics. |
| **Traceability** | A structural property expressed through links among sources, goals, requirements, and later lifecycle artifacts. | A text-only input with no links cannot establish research traceability merely from wording. | Link model, required directions and coverage, data source, and any MVP inclusion. |
| **Measurable requirement properties** | Individual property assessments are represented by `a_ik ∈ [0,1]`; a set-level indicator for one property may be `x_k = (1/n) * sum_i(a_ik)`. Section 2.3 distinguishes primary features, measures, and interpreted indicators. | An implemented property metric needs observable inputs, an applicability set, reproducible computation, declared polarity, provenance, and semantic context. | The concrete observations, binary/graded scale, applicability rules, detector behavior, and property-specific calculation. |
| **Requirements evaluation criteria** | Table 2.1 supplies evidence classes for properties; Section 2.3 requires metric validity, repeatability, data availability, non-redundancy, and variability to be considered when selecting a metric system. | Source evidence classes constrain what an approved criterion may represent, but do not by themselves constitute deterministic acceptance tests. | Exact criteria, thresholds, vocabularies, evidence sufficiency, expected outputs, and validation protocol for MVP. |

The following distinctions come from the research sources:

- `R = {r_i}` is a set of requirements or specification elements.
- `P = {p_k}` is a set of requirement-quality properties, including
  completeness, unambiguity, consistency, verifiability, and traceability.
- `a_ik` is the assessment of property `p_k` for individual requirement `r_i`.
  Chapter 2 places it in `[0,1]`; it may be binary in a simple case or
  intermediate when a property has multiple criteria or an expert scale.
- `x_k = (1/n) * sum_i(a_ik)` is the Chapter 2 aggregate for one property over
  a requirements set. It is not an overall File Quality Score.
- `z_i` is an abstract set of observations for one requirement. It may include
  text, type, acceptance criteria, numeric constraints, sources, links, and
  change information; Chapter 2 does not define its concrete schema.
- `M = {m_l}` is a set of measurable metrics or indicators.
- A **primary feature** is a directly observable fact; a **measure** quantifies
  a collection of facts; an **indicator** interprets a measure relative to an
  evaluation objective.
- `R_k_app` is the applicability set for a rule or metric. An empty applicable
  denominator produces `NA`, not zero.
- `Q = {q_j}` is the ISO/IEC 25010 product-quality space. It is not the same as
  requirement quality.
- `X_j` is a characteristic-specific feature vector used by the broader product
  quality model.
- `y_hat_j` is a predicted product-quality characteristic value in the broader
  model.
- `C_data_j = (c_cov_j, c_rel_j)` represents evidence coverage and reliability.
- `Expl_j` is an explanation traceable to source requirements and evidence.

For MVP v0.1, the following profile symbols are approved:

- `C_i`: Completeness assessment for requirement `i`;
- `V_i`: Verifiability assessment for requirement `i`;
- `U_i`: Unambiguity assessment for requirement `i`;
- `A_i = (C_i, V_i, U_i)`: `RequirementQualityProfile` for requirement `i`;
- `C_file`: mean of applicable/computed `C_i` values;
- `V_file`: mean of applicable/computed `V_i` values;
- `U_file`: mean of applicable/computed `U_i` values;
- `(C_file, V_file, U_file)`: `SpecificationQualityProfile` for the analyzed
  input.

Exact per-characteristic calculation rules and missing/`UNKNOWN` propagation
remain unresolved. The profiles must not be confused with the research
document's product-quality set `Q` or contextual product index `Q_int`.

Chapter 2 supports a `[0,1]` compliance direction for individual property
results `a_ik`, but adopting `C_i`, `V_i`, and `U_i` as exact instances of that
form, including binary versus graded behavior, remains an implementation
operationalization requiring researcher approval.

Status vocabulary in this document:

- `APPROVED`: the stated executable contract is authorized for its declared
  MVP scope;
- `PARTIALLY_APPROVED`: an explicitly identified subset is executable while
  the remaining scientific rule is still open;
- `OPEN`: a researcher decision is still required before the affected rule can
  be made executable;
- `BLOCKED`: implementation of the affected component must not proceed because
  a required scientific decision is open;
- `DEFINED`: sufficiently specified for implementation;
- `PARTIALLY_DEFINED`: supported conceptually, but missing implementation detail;
- `AMBIGUOUS`: multiple interpretations remain possible;
- `MISSING`: required information is absent;
- `OUT_OF_SCOPE_V0.1`: relevant to the broader model but excluded from this MVP;
- `PROPOSED`: an implementation candidate awaiting researcher approval.

### 4.2 Equations and formal structures found in the references

The following are research traceability records, not automatically approved MVP
formulas:

```text
Requirement properties and metrics
a_ik ∈ [0,1]
x_k = (1/n) * sum_i(a_ik)
d_k = 1 - x_k
X_R = (x_1, ..., x_m)
G = [g_ij], g_ij ∈ {0,1}
R_j = {r_i ∈ R | g_ij = 1}
x_kj = sum_i(a_ik * g_ij) / sum_i(g_ij), when sum_i(g_ij) > 0
m_k = 1 - N_k_viol / N_k_app
M_ver = |R_ver| / |R_V|
M_ac = |R_ac| / |R_V|
M_qnt = |R_Q_qnt| / |R_Q|
M_up,j = N_up,j / |R_j|
M_down,j = N_down,j / |R_j_d|
M_covQ = |Q_cov ∩ Q*| / |Q*|
M_cons = 1 - |R_conf| / |R|
M_unique = 1 - |R_dup| / |R|
B = (b_1, ..., b_p), b_k ∈ {0,1}
D = (d_1, ..., d_p), 0 ≤ d_k ≤ 1

Process model
T = {tau_R, tau_A, tau_I, tau_T, tau_O}
P_j(tau, v) = (X_j, y_hat_j, C_data_j, u_j, Risk_j, Prov_j)
P_j(tau_next, v') = U_j(P_j(tau, v), delta_E_j, delta_S, C)
K_k = (tau_k, ReqArt_k, Cmin_k, Qmin_k, CritRisk_k)
Decision_j(K_k) ∈ {evidence_required, corrective_action, proceed}
M_process = (T, A, E, K, U, C)

Quality model
R → P → M → Q
X_j(tau, v) = Phi_j(Z_j, E_static_j, E_dynamic_j, C, B_j)
y_hat_j(tau, v) = F_theta_j(X_j(tau, v), C), y_hat_j ∈ [0,1]
y_hat_j = sigma(beta_0j + sum_k beta_kj x_kj)  [candidate baseline only]
Y_hat = (y_hat_1, ..., y_hat_9)
Q_hat_j = (y_hat_j, C_data_j, u_j, Expl_j)
Q_int(C) = sum alpha_j(C) * y_hat_j, sum alpha_j(C) = 1
M_quality = (Q, G, Phi, F, Theta, C, Agg, D)

Risk model
d_i = (type_i, target_i, evidence_i, sev_i, conf_i, tau_i, v_i)
R_DQ = [rho_ij], rho_ij ∈ [0,1]
r_ij = rho_ij * p_ij * I_ij * kappa_j(C), r_ij ∈ [0,1]
Risk_j = Psi_j({r_ij}, Dep_j)
Pi_i = (max_j r_ij, conf_i, bp_i, cent_i, spread_i, cost_i, tau_i)
a_corr_k = (target_k, change_k, expected_k, deps_k, cost_k, verify_k)
G_D = (D, E_D)
M_risk = (D, R_DQ, Psi, Pi, A_corr, G_D, ReEval, C)
```

Chapter 2 defines the formulas above primarily for properties and metrics over
sets of requirements. Their use does not determine a per-line scoring rule for
each MVP characteristic. The approved aggregation correction uses `x_k` only
for the corresponding property in `SpecificationQualityProfile`; it does not
combine Completeness, Verifiability, and Unambiguity into an overall scalar.

The application example also demonstrates logistic prediction, contextual
weighted aggregation, critical thresholds, and risk calculations. Its document
explicitly labels all metric values, coefficients, risk parameters, and results
as conditional demonstration data. They must not be copied into MVP rules.

## 5. Processing pipeline

The MVP runtime pipeline is:

```text
Text file
→ RequirementReader
→ Requirement
→ FeatureExtractor
→ RequirementExtractionResult (requirement, features, evidence)
→ RequirementFeatures (result.features)
→ CompletenessCalculator
→ VerifiabilityCalculator
→ UnambiguityCalculator
→ RequirementQualityProfile
→ SpecificationQualityAggregator
→ SpecificationQualityProfile
→ ConsoleReporter
```

The calculators depend only on approved domain data contracts and approved
rules in this specification. They do not depend on a reader, CLI, reporter,
feature-extraction implementation, or NLP library. The feature extractor does
not calculate quality assessments. The reporter does not calculate or
aggregate.

The broader research lifecycle includes architecture, implementation, testing,
operation, risk, corrective action, and reassessment. MVP boundaries must not
prevent later addition of versioned evidence, but no such subsystem is to be
implemented now.

## 6. Requirement representation

Chapter 2 explicitly supports two units: an individual requirement and a set of
requirements/specification. For MVP v0.1, the individual textual requirement is
the researcher-approved analysis unit. The following representation is the
approved input contract:

| Field | Type | Meaning | Status |
| --- | --- | --- | --- |
| `id` | string | Automatically assigned processing-order ID such as `R001` | `DEFINED` |
| `source_line` | positive integer | Original one-based source line number | `DEFINED` |
| `text` | string | Non-empty UTF-8 requirement text after trimming leading/trailing whitespace | `DEFINED` |

Blank or whitespace-only lines are ignored. Requirement order matches the order
of non-empty source lines. The reader is Unicode-capable and decodes UTF-8.
Original text is preserved after leading/trailing whitespace is trimmed;
punctuation is not destroyed. One input line remains one `Requirement` even
when it contains multiple grammatical sentences or clauses.

Ukrainian is the officially supported natural language for language-dependent
feature detection in MVP v0.1. Dictionary and linguistic matching may be
case-insensitive. Language-independent detection may operate on approved
constructs such as numbers, percentages, comparison operators, measurable
values, and supported units. No English linguistic profile is approved in this
task. Future language profiles must be replaceable or additive without changing
quality calculators. Evidence always points back to the original text.

## 7. Feature & Evidence Contract — PARTIALLY APPROVED FOR MVP v0.1

The researcher has approved the conceptual feature registry, primary consumer
mappings, evidence contract, linked quantitative-constraint concept, explicit
verification-method meaning, source-derived Ukrainian seed lexicon and matching
policy, and core finding taxonomy. Narrow production contracts are allocated
for condition/context, expected result, quantitative constraint, quantitative
acceptance criterion, verification method, and vague-term occurrence; broader structural/semantic
grammar and observation-to-quality-problem conversion rules remain open. The
overall model specification therefore remains `DRAFT`.

Chapter 2 defines methodological constraints for features and metrics but not a
complete executable feature schema. It requires a reproducible algorithm, a
defined object and applicability set, known polarity, recorded data source and
automation level, and preserved semantic context. It also distinguishes a
primary observation from a measure and an interpreted indicator. Those
distinctions produce the following required boundary:

```text
trimmed original Requirement text
        ↓
FeatureExtractor
        ↓
RequirementExtractionResult
    ├── requirement: Requirement
    ├── features: RequirementFeatures
    └── evidence: tuple[Evidence, ...]
        ↓ approved characteristic/model rule
Finding
        ↓ approved characteristic calculation
CharacteristicAssessment
```

The `FeatureExtractor` detects observations and their evidence only. It does
not calculate Completeness, Verifiability, or Unambiguity; it does not emit a
`RequirementQualityProfile`; and it does not declare a scientific quality
problem merely because a text signal matched. Both `SIGNAL` and
`QUALITY_PROBLEM` findings belong after an approved calculator/model rule has
interpreted an observation.

The public boundary is `Requirement -> FeatureExtractor ->
RequirementExtractionResult`. The immutable result carries the exact input
`Requirement`, the unchanged six-family `RequirementFeatures`, and accepted
`Evidence`. The wrapper makes accepted observation `evidence_refs` resolvable
without adding Evidence to or contaminating the six-family feature registry.
Calculators remain independent of the extractor and use only structured domain
features/assessment inputs authorized by their own contracts; the result wrapper
contains no quality calculation.

### 7.1 Separation of contract concepts

| Concept | Meaning in this draft | May be produced by `FeatureExtractor`? | Scientific interpretation? | Status |
| --- | --- | --- | --- | --- |
| Raw text | The trimmed original requirement text, with original punctuation preserved | Input only | None | `DEFINED` by the approved input contract |
| `Evidence` | An exact source-text span explaining why a detector produced an observation | Yes | None by itself | `APPROVED_FOR_MVP_V0.1` |
| `FeatureObservation` | An explicit detected observation with linked evidence; optional detection processing state is separate from criterion applicability | Yes | It states detection only, not quality | Conceptual contract `APPROVED_FOR_MVP_V0.1`; detector algorithms open |
| `Finding` | A downstream interpretation of observations under an approved model rule | No | Either a `SIGNAL` or an established `QUALITY_PROBLEM` | Minimal data contract and vague-term `SIGNAL` conversion `APPROVED_FOR_MVP_V0.1`; all `QUALITY_PROBLEM` conversions remain blocked |
| `CharacteristicAssessment` | A stateful result envelope for Completeness, Verifiability, or Unambiguity | No | Preserves a computed value or explicitly withholds it without converting missing, unresolved, or non-applicable information to zero | Minimal envelope `APPROVED_FOR_MVP_V0.1` in Section 7.16; per-requirement numeric calculation is now `APPROVED_FOR_MVP_V0.1` via `CALC-C/V/U-MVP-001` (Sections 8-10); specification-level aggregation is now `APPROVED_FOR_MVP_V0.1` via `AGG-MVP-001` (Section 12); `QUALITY_PROBLEM` conversion remains open |

An observation such as “the text contains the exact phrase `швидко`” is not
equivalent to “the requirement is ambiguous.” The first is reproducible lexical
evidence. The second requires an approved interpretation or confirmation rule
that the supplied references do not yet provide.

### 7.2 Approved MVP feature registry and consumer mappings

The following conceptual registry and singular feature identifiers are
`APPROVED_FOR_MVP_V0.1`:

```text
RequirementFeatures:
    condition_contexts[]
    expected_results[]
    acceptance_criteria[]
    quantitative_constraints[]
    verification_methods[]
    vague_term_occurrences[]
```

Multiple observations of the same feature are allowed. The absence of an
observation is not automatically a quality violation.

| Approved `feature_id` | Approved collection | Semantic definition | Approved primary consumer(s) | Detector status |
| --- | --- | --- | --- | --- |
| `condition_context` | `condition_contexts[]` | An explicit condition, trigger, scenario, execution context, or measurement context under which behavior or a criterion applies | Completeness | `COND-UK-001` is allocated for the deterministic first-production leading/postposed subset in Section 7.14.3; general parser-assisted attachment remains open under `RQD-006` |
| `expected_result` | `expected_results[]` | An explicit expected reaction, observable outcome, or required behavior | Completeness | `RESULT-UK-001` is allocated for the narrow parser-assisted normative-modal first-production subset in Section 7.14.4.1; broader expected-result grammar remains open under `RQD-006` |
| `acceptance_criterion` | `acceptance_criteria[]` | An explicit fulfilment or acceptance condition against which execution or an observation can be judged | Completeness and Verifiability | `ACCEPT-QUANT-001` is allocated for the first-production clause-level composition of accepted `RESULT-UK-001` and contained judgeable `QUANT-001`/`QUANT-UK-001` observations in Section 7.14.5.1; non-numeric acceptance grammar and complex quantitative roles remain open under `RQD-006`/`RQD-008` |
| `quantitative_constraint` | `quantitative_constraints[]` | A linked measurable target or bound whose metric, comparator, value, unit, and context remain associated | Verifiability | Partial observations and conservative linkage approved; complex grammar remains open under `RQD-008` |
| `verification_method` | `verification_methods[]` | An explicitly stated reproducible verification method in the requirement text | Verifiability | `VERIFY-UK-001` is allocated for the parser-required first-production governing-predicate, explicit-label, and exact declared-test constructions in Section 7.14.7.1; broader verification-method grammar remains open under `RQD-006` |
| `vague_term_occurrence` | `vague_term_occurrences[]` | An exact occurrence from approved `uk_vague_terms_v1` | Unambiguity, as `SIGNAL` only | Seed lexicon and deterministic matching mechanics approved; `RQD-007` closed for MVP v0.1 |

The mappings above approve only which characteristic may consume each feature.
They do not define score contributions, double-counting rules, or characteristic
calculations. One source-text span may support more than one observation when
the detector rule justifies each observation and preserves evidence.

### 7.3 Semantic definitions and remaining detector gaps

| Concept | Strongest source-supported definition | Always applicable? | Multiple occurrences? | Can absence currently be detected deterministically? | May one span support another concept? |
| --- | --- | --- | --- | --- | --- |
| Condition/context | Information establishing the condition, trigger, scenario, execution setting, or measurement conditions under which a reaction or bound applies | Not established. Local required elements depend on type/template, while automatic type classification is excluded | The sources do not impose a single-occurrence limit; the approved representation preserves all detected occurrences | Only explicit source-attested candidates; no universal absence/applicability rule is approved | Yes; a condition may also be part of an acceptance criterion or quantitative context |
| Expected result | The expected reaction, observable outcome, or required behavior to be understood or observed | Not established; the source ties required content to type/template | Yes in the approved representation, including multi-clause requirements | Parser assistance is required; concrete operationalization and an exhaustive absence rule remain open | Yes; an expected result may itself function as an acceptance criterion |
| Acceptance criterion | A fulfilment condition that makes a requirement judgeable; Chapter 3 gives examples including a threshold, expected behavior, admissible range, or condition | Not universally established; Chapter 2 explicitly uses an applicability set | Yes in the approved representation | `ACCEPT-QUANT-001` defines the narrow quantitative clause-level baseline; non-numeric parser grammar and broader criterion sufficiency remain open | Yes; it may share a span with an expected result or quantitative constraint |
| Verification method | An explicit reproducible method for establishing fulfilment, including test, analysis, inspection, measurement, or another stated procedure | No. A requirement can be verifiable without literally naming the method, and method need depends on requirement/characteristic type | Yes in the approved representation | Explicit-only strategy is approved; concrete grammar/template and absence semantics remain open | Yes; a procedure reference may also carry acceptance-criterion evidence |

The approved contract permits one source span to support more than one feature
observation when each observation is justified. Evidence references preserve
the common source span without forcing one semantic label onto multi-purpose
text. Section 7.14 approves parser assistance conceptually but selects no NLP
library and defines no concrete dependency grammar, syntactic pattern, parser,
or production regular expression.

### 7.4 Detection and criterion applicability are separate

The extractor reports explicit observations and evidence. The approved
conceptual observation shape is:

```text
FeatureObservation:
    feature_id
    evidence_refs[]
```

When a detector needs an explicit processing state, it uses this conceptual
state set:

```text
DetectionStatus:
    DETECTED
    NOT_DETECTED
    UNRESOLVED
```

`DETECTED` means the detector produced an explicit observation supported by
evidence. `NOT_DETECTED` means only that the detector did not find an
observation according to its approved rule. `UNRESOLVED` means the detector
could not determine the result. Neither `NOT_DETECTED` nor an empty feature
collection is automatically a quality violation.

Characteristic/model criteria separately use the already approved states:

```text
CriterionApplicability:
    APPLICABLE
    NOT_APPLICABLE
    UNKNOWN
```

`APPLICABLE` means the assessment criterion applies to the requirement;
`NOT_APPLICABLE` means an approved criterion rule establishes that it does not;
and `UNKNOWN` means available information cannot establish applicability.
These states primarily describe assessment criteria, not the mere existence of
a raw text occurrence.

The binding invariants remain:

```text
NOT_APPLICABLE != 0
UNKNOWN != 0
missing FeatureObservation != failed applicable criterion
NOT_DETECTED != QUALITY_PROBLEM
```

A downstream characteristic rule must explicitly combine detection evidence,
criterion applicability, and any required absence semantics. `CALC-C-MVP-001`,
`CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10) are now the approved
rules that do so for per-requirement Completeness, Verifiability, and the
automated Unambiguity scale; converting an observation into a
`QUALITY_PROBLEM` finding remains unapproved (RQD-016).

### 7.5 Approved evidence contract

```text
Evidence:
    evidence_id
    requirement_id
    feature_id
    text
    start_offset
    end_offset
    rule_id
```

| Field | Purpose | Approved constraint |
| --- | --- | --- |
| `evidence_id` | Stable reference from observations and later findings | Unique within one requirement assessment |
| `requirement_id` | Anchors the evidence to its source requirement | Must identify the requirement whose trimmed original text supplies the span |
| `feature_id` | Identifies the observation concept for which the span was captured | Must name an approved registry entry |
| `text` | Preserves the exact source characters that caused the observation | Must equal the corresponding substring of trimmed original `Requirement.text`; never replace with normalized text |
| `start_offset` | Locates the first source character | Zero-based Unicode code-point offset, inclusive |
| `end_offset` | Locates the position immediately after the source span | Zero-based Unicode code-point offset, exclusive |
| `rule_id` | Identifies the deterministic rule that produced the evidence | Must trace the evidence to the applicable approved detector rule |

The approved offset invariant is:

```text
Requirement.text[start_offset:end_offset] == Evidence.text
```

Offsets refer to the trimmed original requirement text, not a normalized copy.
Punctuation remains in `Requirement.text` and is included in `Evidence.text`
only when it falls inside the detected span. Repeated occurrences remain
separate evidence items with separate `evidence_id` values, even when their text
is identical. One feature observation may reference multiple evidence items,
and one source span may support multiple justified observations. Any ordering or
overlap resolution beyond preserving each repeated occurrence belongs to the
relevant detector contract.

An absent or `NOT_DETECTED` observation has no source span to quote. A later
finding based on approved absence semantics must preserve the requirement and
detector/model rule; it must not fabricate an `Evidence` span.

Normalized detector text must never replace original evidence text. If a
detector later uses normalized forms internally, they are derived detector data,
not source evidence, and the approved offsets still address the trimmed original
text. `RQD-009` is closed for MVP v0.1 by this contract.

#### 7.5.1 Approved extraction-result integrity (Issue #25)

```python
@dataclass(frozen=True, slots=True)
class RequirementExtractionResult:
    requirement: Requirement
    features: RequirementFeatures
    evidence: tuple[Evidence, ...]
```

Construction requires the three declared domain types, with `evidence` an
immutable tuple containing only `Evidence`. For every evidence item,
`evidence.requirement_id == result.requirement.id`. Before substring equality,
its offsets must satisfy
`0 <= evidence.start_offset <= evidence.end_offset <= len(result.requirement.text)`.
The exact trimmed-source round-trip then holds:

```python
result.requirement.text[evidence.start_offset:evidence.end_offset] == evidence.text
```

Every `evidence_id` is unique within one result. Every accepted `evidence_ref`
in all six family outcomes resolves to exactly one evidence item in that same
result, whose `Evidence.feature_id` matches the referencing observation's
approved `FeatureId` family. This covers simple `FeatureObservation`,
`VagueTermOccurrence`, and both the top-level and every populated component's
references in
`QuantitativeConstraintObservation`. Its existing component-union invariant
remains unchanged. Diagnostics and `DiagnosticSpan` are not accepted Evidence
and do not need to resolve against this registry. Repeated identical literals
at distinct offsets remain distinct evidence items with distinct IDs.

### 7.6 Approved linked quantitative-constraint concept

Independent booleans such as `has_metric`, `has_threshold`, and `has_unit` are
insufficient because they lose which quantity, bound, unit, and context belong
together. The following conceptual linkage model is
`APPROVED_FOR_MVP_V0.1`:

```text
QuantitativeConstraintObservation:
    metric
    comparator
    value
    unit
    context
    evidence_refs[]
```

The fields form one linked observation, and `evidence_refs[]` preserves the
original source spans supporting it. Partial observations are allowed: a
detector may identify some components while leaving others unresolved.

| Component | Approved semantic role | Detector decision still missing |
| --- | --- | --- |
| `metric` | Chapter 2 names an observable/measurable quantity; Chapter 3 names the object of measurement | Representation, vocabulary, semantic boundary, and detector |
| `comparator` | Admissible boundary, threshold, target, upper/lower bound, and examples using `≤`, “не більше”, and “не нижче” support the concept | Allowed comparator forms, equivalence/normalization, and parser |
| `value` | Numeric thresholds, target values, percentages, durations, counts, and ranges are explicit examples | Raw versus parsed type, decimal convention, ranges, percentiles, and multiple values |
| `unit` | Unit of measurement is explicitly required for operationalized quantitative requirements when applicable | Supported unit registry, aliases, normalization, and attachment rule |
| `context` | Measurement conditions, load profile, scenario, environment, and qualifying population are explicitly relevant | Context boundary, multiplicity, nesting, and linkage to one or several constraints |

Approved partial-observation example:

```text
source:      "не більше 2 секунд"
metric:      None (not expressed in the first-production anchor)
comparator:  <=
value:       2
unit:        seconds
context:     None (not expressed in the first-production anchor)
```

This baseline example does not name `METRIC` or `CONTEXT` in
`unresolved_components`. An explicitly expressed candidate whose role cannot
be resolved instead uses `None` with the corresponding unresolved entry, as
specified in Section 7.15.10.

For the source example “Час відгуку ≤ 2 с при 500 одночасних користувачах”,
the response-time metric, `≤` comparator, value `2`, unit `с`, and load context
must remain associated if a separately approved metric/context grammar later
extracts those roles. The first-production baseline accepts only the explicit
`≤ 2 с` anchor. Likewise, the worked revision linking a four-second
route-generation bound to 95 percent of requests under up to 300 concurrent
requests must not become unrelated true/false flags. This approval does not decide
whether a percentile qualifier or load limit is a nested constraint, context,
or both; that decomposition remains part of `RQD-008`. Section 7.14 approves a
conservative linkage baseline without arbitrary distance thresholds. No concrete
parser or regular expression, final normalized numeric type, unit conversion, or
nested-context representation is approved. `RQD-008` remains open.

### 7.7 Approved stable `rule_id` policy

A `rule_id` identifies the deterministic rule that produced an observation,
evidence item, or downstream finding. Its purposes are reproducibility,
human-readable explanation, unit-test traceability, and comparison across
versioned research changes.

The approved policy is:

1. use a machine-readable, ASCII, case-stable identifier;
2. keep an identifier's semantic meaning immutable after publication;
3. issue a new identifier when detector semantics, applicability, or evidence
   boundaries change materially; do not silently reuse an old identifier;
4. retain deprecated identifiers in the rule registry for historical results;
5. associate every identifier with the approving model-spec version, detector
   description, input language/profile when relevant, and expected evidence;
6. reference the same identifier from evidence, observations, findings, and
   tests when they exercise the same rule;
7. identify a vocabulary and its version separately from the generic matching
   algorithm so either can change without obscuring provenance.

`UK-VAGUE-001` is allocated as the production detection rule ID for the exact
Section 7.14.8 `uk_vague_terms_v1` matcher. This allocation changes none of
its matching semantics and implies no finding, confirmed ambiguity, score, or
penalty. `QUANT-001` and `QUANT-UK-001` are allocated only for the narrow
first-production quantitative lexical baseline in Section 7.14.6.6, by
researcher-approved Issue #29. `COND-UK-001` is allocated only for the narrow
first-production condition/context baseline in Section 7.14.3, by
researcher-approved Issue #35. `RESULT-UK-001` is allocated only for the
narrow parser-assisted normative-modal expected-result subset in Section
7.14.4.1, by researcher-approved Issue #39. `ACCEPT-QUANT-001` is allocated
only for the clause-level quantitative acceptance composition in Section
7.14.5.1, by researcher-approved Issue #43. `VERIFY-UK-001` is allocated only
for the three parser/template verification-role constructions in Section
7.14.7.1, including the Issue #47 researcher decision resolving the exact R3′
source declaration. `FIND-U-VAGUE-001` is allocated only for the one accepted
vague-term occurrence to one Unambiguity `SIGNAL` conversion finalized in
Sections 7.14.10 and 7.16.5; it never creates a confirmed ambiguity, score, or
penalty. Shapes such as `QUANT-COMP-001`
and `COND-001` remain conceptual examples only. Semantic versions belong in
registry metadata. No speculative production rule-ID registry is created by
these allocations.

### 7.8 Approved source-derived Ukrainian vague-term seed lexicon

The following inventory contains only literal Ukrainian surface forms present
in the supplied references. It is approved as `uk_vague_terms_v1` with the
scientific status `SOURCE-DERIVED MVP SEED LEXICON`. Approval does not mean that
every occurrence is ambiguous or that the list is a complete Ukrainian
ambiguity vocabulary.

| Approved literal | Source and location | Surrounding research meaning | Source treatment | Language | MVP status |
| --- | --- | --- | --- | --- | --- |
| `в реальному часі` | Application example, Section 2, Table 1, R1; Section 13 discussion | Update timing can be interpreted as different intervals without a bound | Confirmed defect in the demonstrational example; illustrative wording | Ukrainian | Approved exact phrase |
| `у реальному часі` | Application example, Sections 2-3 discussion; Section 7, Table 6, `d1`; Section 8, Table 7, `R1 → R1′` | The phrase lacks a numeric limit and is replaced by bounded update and latency criteria | Confirmed ambiguity/defect in the demonstrational example and revised anti-pattern | Ukrainian | Approved exact phrase |
| `реальний час` | Application example, Section 3, Table 2, Unambiguity row | Listed among terms that have no quantitative limits | Anti-pattern/example term | Ukrainian | Approved literal surface form |
| `швидко` | Requirement properties, Section 2.1, paragraph 12; Application example, Section 2, Table 1, R2 and Section 3 | States intent but supplies no reproducible or quantitative criterion | Linguistic/operationalization signal; demonstrational undefined concept | Ukrainian | Approved exact token |
| `швидкою` | Dynamic methods, Section 3.2, paragraph 10 | Example wording whose lack of operationalization limits construction of a correct test | Illustrative anti-pattern | Ukrainian | Approved exact token |
| `зручною` | Dynamic methods, Section 3.2, paragraph 10 | Example wording whose lack of operationalization limits construction of a correct test | Illustrative anti-pattern | Ukrainian | Approved exact token |
| `надійною` | Dynamic methods, Section 3.2, paragraph 10 | Example wording whose lack of operationalization limits construction of a correct test | Illustrative anti-pattern | Ukrainian | Approved exact token |
| `надійно` | Application example, Section 2, Table 1, R3 and Section 3 | Listed as an undefined concept without a quantitative or verifiable criterion | Confirmed defect in the demonstrational example; illustrative wording | Ukrainian | Approved exact token |
| `надійний захист` | Application example, Section 3, Table 2, security-specificity row | Protection is asserted without technical and verifiable criteria | Anti-pattern/example phrase | Ukrainian | Approved exact phrase; no automatic morphological relation to `надійно` |
| `надійно захищені` | Application example, Section 7, Table 6, `d3` | Protection wording is treated as a defect when criteria are absent | Confirmed defect in the demonstrational risk example | Ukrainian | Approved exact phrase |

Section 2.1, paragraph 10 supplies families rather than literal vocabulary:
subjective formulations, vague adjectives/adverbs, weak modal constructions,
pronoun references, and other language patterns. Those families are evidence
that automated signals may be useful, but they are not executable Ukrainian
entries. No literal terms were added from general knowledge. The remaining
reference documents add no further explicit Ukrainian vague-term examples.

This source-derived inventory is intentionally a narrow MVP seed and is not
claimed to be a complete or generally sufficient Ukrainian ambiguity
vocabulary. Reduced recall is accepted in MVP v0.1 in exchange for
reproducibility and source traceability. No synonyms, lemmas, missing grammatical
variants, or semantically similar terms may be generated automatically.

Approved matching policy for MVP v0.1:

- language: Ukrainian;
- deterministic, case-insensitive matching;
- token boundaries for single-token entries and phrase boundaries for
  multi-token entries;
- preservation of every occurrence as a separate evidence item;
- stable vocabulary identifier `uk_vague_terms_v1`;
- no semantic expansion, automatic synonym expansion, embedding similarity, or
  LLM-based matching.

Every lexicon match produces only an ambiguity-related `SIGNAL`. A match alone
must never be reported as a confirmed ambiguity or `QUALITY_PROBLEM`. In
particular, expressions related to `реальний час` may be valid when adequately
defined by context or measurable bounds; their automatic occurrence remains a
signal only.

The exact seed-matching mechanics are approved in Section 7.14.8: the derived
view uses NFC plus Unicode `casefold()`, single tokens use Unicode-aware word
boundaries, phrase tokens may be separated by one or more Unicode whitespace
characters, and overlap resolution is
`LEFTMOST_LONGEST_NON_OVERLAPPING`. Every selected occurrence retains exact
original evidence and offsets. No new vocabulary or semantic expansion may be
introduced. `RQD-007` is closed for the MVP v0.1 seed matcher; broader linguistic
coverage is future research and does not keep the MVP decision open.

### 7.9 Explicit verification-method evidence

`verification_method` is approved as a feature representing only an explicitly
stated reproducible verification method in requirement text. Possible semantic
categories include test, measurement, inspection, and analysis. These
categories do not by themselves constitute accepted production evidence.
Section 7.14.7.1 allocates only the narrow source-derived candidate vocabulary
and role constructions of `VERIFY-UK-001`; vocabulary presence alone remains
insufficient.

The references do not require every verifiable requirement to contain a literal
method name. Therefore the extractor may produce only:

```text
explicit verification-method evidence
```

It must not produce:

```text
inferred verifiability
```

from text alone or merely because a requirement seems testable. A later
Verifiability calculator may use explicit method evidence together with
acceptance criteria and linked quantitative constraints, but only after its
scientific rule is approved. `VERIFY-UK-001` does not determine method
sufficiency, procedure quality, applicability, or a Verifiability score.

### 7.10 Finding taxonomy and boundary

`FindingKind = SIGNAL | QUALITY_PROBLEM` and the distinction between those
values are approved for MVP v0.1. Section 7.16.5 is the authoritative minimal
`Finding` data contract, including finding identity, requirement provenance,
characteristic identity, optional criterion provenance, evidence references,
rule traceability, and explanation.

The `FeatureExtractor` emits observations, accepted Evidence, and diagnostics;
it does not emit findings or confirmed quality defects. A downstream approved
characteristic/model rule may transform an accepted observation into a
finding. `FIND-U-VAGUE-001` is the only allocated MVP conversion rule: every
accepted vague-term occurrence produces one Unambiguity `SIGNAL`. A match may
never become `QUALITY_PROBLEM` from the match alone. No Completeness,
Verifiability, or Unambiguity `QUALITY_PROBLEM` conversion rule is currently
approved.

Severity, probability, risk, numeric confidence, calibrated certainty, and
evidence-reliability values are deliberately absent from both `Finding` and
`CharacteristicAssessment`. Chapter 4 places some of these concepts in a
broader defect/risk tuple, but they are outside the MVP v0.1 characteristic
contract. `RQD-020` remains `OPEN / UNRESOLVED — NON-BLOCKING WHILE EXCLUDED`:
the absence of these fields from the current contract does not resolve whether
they belong in MVP. If their inclusion is later proposed, `RQD-020` becomes
blocking and requires a separate scientific contract. `RQD-016` remains open
only for future `QUALITY_PROBLEM` conversion rules; the finding representation
and vague-term signal conversion are approved.

### 7.11 Actor, action, and object disposition

| Earlier candidate | Research finding | MVP v0.1 disposition | Traceability disposition |
| --- | --- | --- | --- |
| `has_actor` | No supplied reference defines explicit actor presence as a required feature of Completeness, Verifiability, or Unambiguity | `DEFERRED_FROM_MVP_V0.1`; may become an optional future structural observation | Retained here and in the research traceability table as an earlier MVP-SPEC candidate |
| `has_action` | Required/expected behavior is discussed, but the references do not define a general grammatical “action” field or detector | `DEFERRED_FROM_MVP_V0.1`; may become an optional future structural observation. Source-supported `expected_result` remains separate | Retained here and in the research traceability table |
| `has_object` | No supplied reference defines an affected grammatical object as an MVP quality feature | `DEFERRED_FROM_MVP_V0.1`; may become an optional future structural observation | Retained here and in the research traceability table |

These fields are not part of the approved MVP feature registry and are not erased
from decision history. A later issue may reconsider them for template checking
or structural analysis only after supplying a research definition and approved
contract. They must not affect Completeness, Verifiability, or Unambiguity in
MVP v0.1.

### 7.12 Research-source traceability for this contract

| Source | Contract evidence extracted |
| --- | --- |
| Requirement properties, Section 2.1, Table 2.1 and paragraphs 10-12; Table 2.3 | Local Completeness roles; reproducible Verifiability evidence; quantitative indicator/condition/bound; signal-versus-confirmed-ambiguity distinction; `швидко` example |
| Requirements and product quality, Section 2.2, Table 2.4; Table 2.5 | Expected results and criteria; linked response-time, unit, and load-context example; preservation of semantic context |
| Metrics system, Section 2.3, paragraphs 4-21 and 39-42; Tables 2.7-2.9 | Observation/measure/indicator separation; applicability; criteria, thresholds, units, conditions; explicit verification procedure; missing-value and optional reliability boundaries |
| Static methods, Section 3.1, paragraphs 10-13 and 32-34 | Structured findings, rule/source/evidence traceability, operationalization components, and separation of findings from numeric indicators |
| Dynamic methods, Section 3.2, paragraphs 5-10 and Table 3.4 | Requirement-to-criterion-to-procedure-to-observation chain; criterion forms; reproducible method meaning; `швидкою`, `зручною`, and `надійною` examples |
| Assessment method, Section 3.3, canonicalization and interpretation discussion | Feature provenance, non-duplication, applicability metadata, and explanation traceability |
| Risk model, Section 4.3, defect tuple | Evidence and rule traceability context; severity/confidence explicitly reserved for the broader risk model |
| Application example, Sections 2-3, 7-8, and 13 | Exact vague-word occurrences; original and revised requirements; linked quantitative examples; demonstrational signal/problem cases |

### 7.13 Remaining research decisions

The approved portions above close `RQD-005`, `RQD-007`, and `RQD-009` for MVP
v0.1 and approve the detector-to-signal portion of `RQD-016`; Section 7.16
later finalizes the Finding representation and exact signal rule. Sections 8-10
later close the per-requirement calculation portions of `RQD-002`-`RQD-004`,
`RQD-010`-`RQD-012`, and `RQD-022` via `CALC-C-MVP-001`, `CALC-V-MVP-001`, and
`CALC-U-MVP-001`. Broader detector/runtime coverage remains blocked; the
internal production numeric representation (item 7 below) and
specification-level aggregation (item 3 below) are now resolved. Isolated
implementation and testing of
`CompletenessCalculator`,
`VerifiabilityCalculator`, and `UnambiguityCalculator` against manually
constructed `RequirementExtractionResult` inputs is not blocked by items 1-2:

1. richer detector coverage — parser/template operationalization beyond the
   approved `COND-UK-001` condition subset, `RESULT-UK-001` expected-result
   subset, and quantitative `ACCEPT-QUANT-001` composition and beyond the
   three `VERIFY-UK-001` verification-role constructions, including general
   condition attachment, broader expected-result grammar, non-numeric
   `acceptance_criterion`, and broader `verification_method` strategies
   (`RQD-006`). This is future detector-expansion work; it does not block
   isolated `CALC-C/V/U-MVP-001` implementation or testing, which consumes
   whatever `RequirementExtractionResult` a test or the current extractor
   already supplies;
2. richer detector coverage — complex quantitative grammar, ambiguous
   metric/context attachment, nested constraint representation, and
   deliberately deferred numeric/range forms beyond the approved baseline
   (`RQD-008`). Same non-blocking relationship to isolated `CALC-V-MVP-001`
   implementation/testing as item 1;
3. **RESOLVED.** specification-level aggregation propagation for
   missing/`UNKNOWN` per-requirement values, empty computed denominators, and
   final aggregation semantics (the remaining, specification-level portions
   of `RQD-012` and `RQD-022`). Section 12's `AGG-MVP-001` now closes this:
   the mean is computed from `COMPUTED` values only, `UNKNOWN` values are
   excluded and tracked as `unknown_count` (never zero), and an empty
   `COMPUTED` denominator yields aggregate state `UNKNOWN` (if the
   applicability set is non-empty) or `NOT_APPLICABLE`/NA (if it is empty).
   The per-requirement criterion-applicability, missing-feature, and absence
   semantics used by each characteristic calculation were already resolved
   by `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections
   8-10);
4. exact observation-to-`QUALITY_PROBLEM` conversion rules and any handling of
   overlapping evidence in characteristic calculations (`RQD-016` only; the
   per-requirement characteristic-calculation gate itself is now closed for
   MVP v0.1);
5. production rule-ID allocations and detector descriptions for rules other
   than the allocated `COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`,
   `VERIFY-UK-001`, `QUANT-001`, `QUANT-UK-001`, and `UK-VAGUE-001`
   baselines;
6. the then-unresolved decision on whether any evidence reliability or
   detector-confidence representation belongs in MVP (`RQD-020`). Section 7.16
   later excludes both from the current MVP v0.1 characteristic contract while
   leaving the research decision open and non-blocking while they remain
   excluded;
7. **RESOLVED.** the internal production numeric representation for
   `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` output values (the
   remaining implementation portion of `RQD-015`, Section 13). Exact
   mathematical calculation semantics were already approved; Section 13 now
   additionally approves Python standard-library `fractions.Fraction` as the
   concrete representation for production values such as `1/3` and `2/3`, so
   this item no longer gates concrete production implementation of
   MVP-06/07/08.

No decision in this section defines a calculation for `C`, `V`, or `U`, a
coefficient, a weight, a threshold, a score contribution, or a rounding rule.

### 7.14 Deterministic Feature Detection Contract — PARTIALLY APPROVED

This section records the researcher-approved MVP v0.1 detector rules for the six
feature families and identifies the remaining operational decisions. Approval
does not authorize implementation while the affected issue remains blocked, and
it does not change the approved registry or evidence contract in Sections 7.2
and 7.5. The overall model specification remains `DRAFT`.

The contract prefers explicit, local evidence and reproducibility over recall.
It does not use domain common sense to supply missing meaning. It requires no
LLM API, embedding, generative inference, or custom trained classifier. Parser
assistance, where identified, means only a replaceable source of tokenization,
lemma, part of speech, morphology, dependency relation, and clause boundaries
behind the `FeatureExtractor` boundary. This Section 7.14 did not select an NLP
library; the later Section 7.15 approves a replaceable engineering backend
without defining executable detector grammar.

#### 7.14.1 Corpus review and source classification

All supplied research references were reviewed for semantic definitions and
literal detector examples. A literal is `SOURCE-ATTESTED` only when it occurs in
the supplied corpus. Occurrence in explanatory prose or a mathematical formula
does not by itself establish that the literal is suitable as a requirement-text
detector. Use of a source-attested literal is executable only where this section
explicitly approves its detector role.

| Source reviewed | Detector-relevant contribution | Literal-detector consequence |
| --- | --- | --- |
| Requirement properties, Section 2.1, paragraphs 10-12 and Tables 2.1/2.3 | Condition, expected reaction, fulfilment criterion, reproducible verification, quantitative indicator/condition/bound, and signal-versus-defect semantics | Supports the six feature meanings, but supplies no complete detector grammar; `швидко` is the only new literal already captured by the approved seed lexicon |
| Requirements and product quality, Section 2.2, paragraph 4, paragraph 25, Tables 2.4/2.5 | Expected results, criteria, observable targets, response-time bound, and load context | Supplies the linked example `Час відгуку ≤ 2 с при 500 одночасних користувачах` and the duration construction `не довше ніж за 2 с` |
| Metrics system, Section 2.3, paragraphs 4-21 and 39-42, Tables 2.7-2.9 | Primary-observation boundary, applicability, criteria, quantities, units, conditions, reproducible procedures, and missing states | Supports deterministic lexical baselines and unresolved states; it does not supply an exhaustive lexicon or parser |
| Static methods, Section 3.1, paragraphs 10-13 and 32-34 | Operationalization components and traceable rule/evidence records | Supports preserving object of measurement, conditions, unit, target/bound, criterion, rule, and provenance |
| Dynamic methods, Section 3.2, paragraphs 3-10 and 20-23, Tables 3.4/3.5 | Requirement-to-criterion-to-procedure-to-observation chain; threshold, expected behavior, admissible range, condition; named verification procedures | Supplies semantic and vocabulary candidates, not production lexical rules |
| Assessment method, Section 3.3, paragraphs 10-11 and 46 | Canonicalization, provenance, deduplication, and detector version traceability | Supports stable rule provenance and avoiding duplicate interpreted inputs; it supplies no detector literal |
| Process model, Section 4.1 | Lifecycle conditions, checkpoints, evidence availability, and missing-data invariants | No additional requirement-text detector literal is adopted from this source |
| Quality model, Section 4.2 | Characteristic-specific context, evidence profiles, and later prediction | No additional requirement-text detector literal is adopted from this source |
| Risk model, Section 4.3 | Traceable defect/finding context and later risk interpretation | Supports the finding boundary; no detector literal, risk value, or severity field is adopted |
| Chapter 4 conclusions | Summary of the three broader models | No additional detector mechanic or literal is adopted |
| Application example, Sections 2-3, 7-8, and 13, especially Tables 1, 2, 6, and 7 | Original and revised Ukrainian requirements with conditions, results, numeric bounds, units, contexts, verification references, and vague-term occurrences | Primary source for the source-attested Ukrainian requirement-text forms below; all example scores, weights, thresholds, and risk values remain demonstrational and excluded |

The following feasibility classification is approved:

| Feature family | Approved class | Smallest useful deterministic baseline | Linguistic information needed beyond the baseline |
| --- | --- | --- | --- |
| `condition_context` | `PARSER_ASSISTANCE_OPTIONAL` | Source-attested marker plus a conservatively delimited phrase/clause | Clause boundary and dependency attachment for nested, coordinated, or ambiguous contexts |
| `expected_result` | `PARSER_ASSISTANCE_REQUIRED` | No scientifically defensible lexical-only baseline equates a word or arbitrary verb with a result | Tokenization, lemma, part of speech, morphology, dependency relation, coordination, negation, and clause boundary |
| `acceptance_criterion` | `PARSER_ASSISTANCE_OPTIONAL` | An explicit linked quantitative bound can form a narrow baseline | Predicate/argument and clause attachment for non-numeric expected behaviors and conditions |
| `quantitative_constraint` | `PARSER_ASSISTANCE_OPTIONAL` | Comparator/value/unit chunks and partial observations | Dependency or template relation for metric, population, measurement context, and nested constraints |
| `verification_method` | `PARSER_ASSISTANCE_OPTIONAL` | Explicit method-naming constructions and named procedure phrases | Morphology and dependency role to distinguish a verification procedure from system behavior or discussion about testing |
| `vague_term_occurrence` | `LEXICAL_BASELINE_FEASIBLE` | Exact approved seed matching with deterministic Unicode, boundary, overlap, and ordering mechanics | None for the approved seed baseline |

The family-level `PARSER_ASSISTANCE_OPTIONAL` classification remains unchanged.
The narrower first-production `VERIFY-UK-001` rule is nevertheless
`PARSER_REQUIRED`, as specified in Section 7.14.7.1, because candidate method
vocabulary alone cannot distinguish verification procedure from behavior,
discussion, artifact/reference use, or a promise to define a method later.

#### 7.14.2 General approved detector mechanics

The following mechanics are approved for MVP v0.1:

1. Each detector operates on one trimmed original `Requirement.text`. It may
   use a derived matching view, but evidence always addresses original Unicode
   code-point offsets.
2. An evidence span is the smallest contiguous original substring that contains
   the explicit text needed to justify that observation. Leading/trailing
   whitespace and sentence-final punctuation are excluded. Punctuation inside
   a semantic construction is included only when required by that construction.
3. A comma may delimit a leading or trailing condition, but a comma between
   digits in a decimal value does not delimit a clause. Full stop, semicolon,
   question mark, and exclamation mark are hard candidate boundaries after
   protected numeric/version tokens have been recognized. A colon or dash is
   not automatically a boundary; its grammatical role must be established.
4. Every distinct accepted occurrence produces a separate observation and
   separate evidence, ordered by ascending `start_offset`. Repeated identical
   text is not collapsed.
5. Non-overlapping observations from one family are retained. One source span
   may support different feature families. Same-family nested candidates use
   the feature-specific policy below; semantic nesting is not erased merely to
   make spans non-overlapping.
6. A marker, number, unit, verb, or method word alone does not establish a
   semantic observation unless its rule explicitly permits a partial
   observation. Ambiguous attachment produces `UNRESOLVED`, not a guessed link.
7. No detector crosses from one requirement line to another. No domain fact,
   requirement type, missing argument, implicit unit, implicit verification
   method, or implicit expected behavior is supplied from common sense.

#### 7.14.3 `condition_context`

**Source-attested requirement/example markers.** These literals occur in a
requirement or requirement-like example in the supplied sources. Their use as
detector markers is approved subject to the conservative attachment and boundary
rules below.

| Literal | Semantic role in the source | Traceability | Approved evidence end | Main false-positive risk |
| --- | --- | --- | --- | --- |
| `у разі` | Event/failure condition | Application example, Section 2, Table 1, R2 and R5 | End of the marker-headed phrase, before sentence punctuation | A noun phrase may describe a topic rather than condition required behavior |
| `під час` | Temporal/load execution context | Application example, Section 2, Table 1, R4 | End of the marker-headed phrase | General temporal narrative not modifying a required result or criterion |
| `якщо` | Clause-level trigger/failure condition | Application example, Section 8, Table 7, `R5 → R5′` | End of the subordinate clause; exclude its delimiting comma | Conditional language in a definition or formula rather than the requirement behavior |
| `після` | Event/temporal trigger | Application example, Section 8, Table 7, `R2 → R2′` and `R5 → R5′` | End of the marker-headed phrase or clause | Narrative sequence, lifecycle timing, or a result phrase not functioning as a condition |
| `при` | Load/measurement context | Requirements and product quality, Section 2.2, Table 2.5, semantic example; Application example, Section 8, Table 7, `R2 → R2′` | End of the attached phrase | Highly polysemous preposition; corpus prose also uses it in non-requirement senses |

`коли` occurs in explanatory prose, for example Requirement properties,
Section 2.1, paragraphs 5 and 15, and Metrics system, Section 2.3, paragraph 17,
but not in an explicit supplied requirement example that establishes a detector
boundary. `за умови` does not occur in the supplied corpus. Neither is approved
for the first-production inventory. No synonym, generated form, morphological
variant, or semantic equivalent may be added.

##### 7.14.3.1 First-production allocation (Issue #35)

`COND-UK-001` is the only production rule allocated by this contract. Its
marker inventory is exactly:

```text
якщо
у разі
під час
після
при
```

The detector matches markers on an offset-preserving derived view produced by
NFC normalization followed by Unicode `casefold()`. Original
`Requirement.text` remains unchanged and authoritative. Derived-view matches
must be mapped back to zero-based Unicode code-point offsets in that original
trimmed text; transformed-view indices must not be used directly as source
offsets. Evidence and diagnostic spans preserve the exact original substring.

For multi-token markers `у разі` and `під час`, each canonical space may match
one or more Unicode whitespace characters. This is formatting tolerance only:
punctuation, reordered or inserted words, lemmatization, generated morphology,
and semantic expansion are not permitted. Marker tokens use the complete-token
outer lexical boundaries already approved in Section 7.14.6.1: a Unicode
Letter, Mark, Number, Connector_Punctuation, or one of `'`, `’`, `ʼ`, and `-`
is a word constituent. In particular, `при` cannot match inside a longer joined
word. The vague-term `LEFTMOST_LONGEST_NON_OVERLAPPING` policy is not
transferred to condition candidates; this family uses only the structural
templates below.

Full stop, semicolon, question mark, and exclamation mark are hard condition
candidate boundaries after protected numeric tokens have been recognized. A
candidate cannot cross one of these boundaries. Sentence-final punctuation is
excluded from Evidence. A decimal comma inside an approved numeric expression
is not a clause delimiter. Colon and dash do not independently authorize a
condition boundary.

The first-production subset establishes attachment only through one of these
two anchors in the governing non-condition portion of the same hard segment:

1. a complete lexical token whose value on the same NFC-then-Unicode-
   `casefold()` view is exactly `повинен`, `повинна`, `повинні`, `має`, or
   `мають`; or
2. an already accepted `QUANT-001` or `QUANT-UK-001` observation in that
   governing portion.

The five normative surfaces are attachment anchors only. Their use here does
not create an `expected_result` observation and does not approve general
expected-result grammar. The future detector must reuse
`QuantitativeBaselineDetector` for the quantitative anchor and must not
duplicate its grammar. Only an accepted quantitative observation establishes
the anchor; an unresolved numeric candidate or diagnostic does not. A
quantitative anchor is not copied into condition Evidence and does not alter the
quantitative observation.

**Leading template.** The approved form is:

```text
<marker> <non-empty condition>, <governing behavior>
```

Ignoring only leading whitespace, the marker begins the current hard segment.
Evidence starts at the marker and ends at the character immediately before the
delimiting comma. The governing remainder after the comma must contain one of
the approved attachment anchors. `якщо` is accepted only in this
comma-delimited leading template for first production. No arbitrary clause
interpretation is authorized. For example:

```text
Якщо сервіс недоступний, система повинна зберегти запит.
```

produces Evidence `Якщо сервіс недоступний`.

**Postposed template.** Only `у разі`, `під час`, `після`, and `при` may begin
a first-production postposed candidate. Evidence starts at the marker and
extends to the current hard-boundary end, excluding sentence-final punctuation.
The governing prefix before the marker must contain one of the approved
attachment anchors. Postposed `якщо` is not accepted. If comma or coordination
makes the candidate boundary ambiguous, the candidate remains unresolved; the
detector must not guess its phrase boundary.

Each accepted candidate creates exactly one Evidence item and one observation:

```python
FeatureObservation(
    feature_id=FeatureId.CONDITION_CONTEXT,
    evidence_refs=(evidence_id,),
)
```

Evidence has `feature_id = CONDITION_CONTEXT` and
`rule_id = COND-UK-001`. Accepted Evidence IDs are
`COND-UK-001:E001`, `COND-UK-001:E002`, and so on. Their ordinals are assigned
independently of other rule families by ascending accepted source occurrence
within one requirement assessment. Accepted observations are returned by
ascending Evidence `start_offset`; repeated identical text at distinct offsets
remains separate. Diagnostics are also source ordered.

`COND_UNRESOLVED_CANDIDATE` is the allocated diagnostic code for an approved
marker-headed, non-empty apparent phrase or clause whose attachment or
first-production boundary cannot be decided. Its `rule_id` is `COND-UK-001`.
The diagnostic is not Evidence and creates no `FeatureObservation`. A bare
marker without a non-empty complement is deterministically rejected and creates
no Evidence. A requirement with no approved marker candidate completes with no
observation, Evidence, or diagnostic.

The family outcome semantics are:

| Accepted observations | Unresolved candidates | Processing | Derived status |
| --- | --- | --- | --- |
| present | none | `COMPLETE`, no diagnostics | `DETECTED` |
| none | none | `COMPLETE`, no diagnostics | `NOT_DETECTED` |
| none | present | `INCOMPLETE`, diagnostics present | `UNRESOLVED` |
| present | present | `INCOMPLETE`, diagnostics present | `DETECTED` |

The following cases are binding for this allocation:

| Case | Input | First-production result |
| --- | --- | --- |
| Source-attested postposed condition | `Маршрут доставки повинен швидко перераховуватися у разі зміни дорожньої ситуації.` | One observation with Evidence `у разі зміни дорожньої ситуації` |
| Source-attested postposed context | `Система повинна залишатися доступною під час пікового навантаження.` | One observation with Evidence `під час пікового навантаження` |
| Quantitative attachment | `Час відгуку ≤ 2 с при 500 одночасних користувачах` | The postposed candidate `при 500 одночасних користувачах` may attach through the accepted `QUANT-001` observation in the governing prefix; no metric or quantitative-context field is inferred |
| Unresolved attachment | `Система повідомляє про помилку при перевірці.` | No observation or Evidence; one `COND_UNRESOLVED_CANDIDATE` diagnostic with candidate span `[31,44)` `при перевірці`, `processing_status = INCOMPLETE`, and derived status `UNRESOLVED`; no verification-method or temporal-context meaning is inferred |

The source-attested `при навантаженні до 300 одночасних запитів` form may
likewise produce one condition Evidence span beginning at `при` when its
governing prefix has an accepted anchor. The nested `до 300` candidate remains
independently governed by the quantitative contract; this rule does not infer
or populate the `metric` or `context` field of a
`QuantitativeConstraintObservation`.

This allocation approves no general subordinate-clause or dependency-based
attachment, no coordinated-condition grammar beyond a separately
deterministic candidate, and no general modal or expected-result grammar.
`RQD-006` therefore remains `PARTIALLY APPROVED / OPEN` for general
parser-assisted condition attachment, expected-result grammar, broader
subordinate-clause attachment, non-numeric acceptance grammar, and
verification-method grammar beyond `VERIFY-UK-001`.

#### 7.14.4 `expected_result`

The sources express expected results through required behavior, observable
outcomes, and reactions after a condition. Source-attested constructions include
the Ukrainian modal forms `повинен`, `повинна`, and `повинні` in the Application
example, Section 2, Table 1, R1-R4; `має`/`мають` in Requirements and product
quality, Section 2.2, paragraph 4, and the Application example, Section 8,
Table 7, `R2 → R2′`; and coordinated result clauses such as `події зберігаються`,
`UI показує`, `виконується повторна спроба`, and `формують alert` in the
Application example, Section 8, Table 7, `R5 → R5′`.

Those words are evidence of how the sources express behavior; they are not an
exhaustive verb or modal lexicon. The approved strategy classifies this family
as `PARSER_ASSISTANCE_REQUIRED` and requires a parser-assisted clause rule that
establishes all of the following:

- the clause asserts required behavior or an observable result, rather than
  merely mentioning, describing, negating the definition of, or discussing it;
- the predicate and its essential arguments/complements form an explicit result;
- coordination and negation scopes are resolved; and
- an initial or final condition can be separated without removing text essential
  to the result.

Evidence is the complete minimal result clause, including its subject when the
subject is expressed locally, modal/normative construction, predicate, essential
object/complement, and any bound that is part of the required result. A separable
condition is excluded and preserved as `condition_context`. An arbitrary verb,
the noun phrase `очікуваний результат`, or an assertion that behavior is “not
defined” must not count. When the parser cannot determine clause or attachment
scope, the detector returns `UNRESOLVED`; it does not fall back to “contains a
verb.”

Each independent coordinated result clause is a separate observation, even when
several share one condition. A result span may also support an
`acceptance_criterion` and a `quantitative_constraint`.

| Case | Source status and input | Approved detector output | Evidence span(s) | Approved rule family |
| --- | --- | --- | --- | --- |
| Positive | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R2 → R2′` | `DETECTED`; required route result | `[44,116)` `новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с` | `RESULT-UK` |
| Negative | SOURCE-ATTESTED — Application example, Section 2, Table 1, R6: `У двох частинах документа задано різний час завершення неактивної сесії: 15 і 30 хвилин.` | `NOT_DETECTED`; this reports a conflict, not a required system result | none | `RESULT-UK` |
| Unresolved | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система контролює обробку запитів.` | `UNRESOLVED`; an indicative verb alone does not establish normative/expected-result force | no accepted evidence | `RESULT-UK` |
| Repeated | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R5 → R5′` | `DETECTED`; four result clauses under two temporal conditions | `[39,65)` `події зберігаються у черзі`; `[67,93)` `UI показує статус degraded`; `[95,132)` `виконується повторна спроба з backoff`; `[145,159)` `формують alert` | `RESULT-UK` |
| Punctuation | Same source case | The comma separates the leading condition; the semicolon separates the final temporal condition/result pair; neither punctuation enters result evidence | same four spans | `RESULT-UK` |
| Interaction | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R2 → R2′` | One result span may also support an acceptance criterion; its inner bound supports a quantitative observation | result `[44,116)`; bound `[96,116)` | `RESULT-UK`, `ACCEPT-UK`, `QUANT` |

The table above remains a family-level semantic reference. In particular, the
source-attested `R5 → R5′` clauses demonstrate the broader meaning of
`expected_result`; they are not all executable coverage of the first-production
rule below. Their inherited normative force and coordinated scopes remain open
under `RQD-006`.

##### 7.14.4.1 First-production parser-assisted allocation (Issue #39)

`RESULT-UK-001` is the only expected-result production rule allocated by this
contract. It produces `expected_result` observations and accepted Evidence; it
creates no Finding, applicability decision, characteristic assessment, or
score. Its accepted Evidence IDs are `RESULT-UK-001:E001`,
`RESULT-UK-001:E002`, and so on, assigned in accepted source order within one
requirement assessment. Accepted observations are ordered by ascending Evidence
`start_offset`; repeated source-distinct accepted clauses remain separate.
Diagnostics are ordered by their affected source span when a span exists, with
parser-blocked diagnostics that have no source span ordered after source-bound
diagnostics.

The first-production normative-force inventory is exactly:

```text
повинен
повинна
повинні
має
мають
```

The forms are matched as complete source tokens on an offset-preserving derived
view produced by NFC normalization followed by Unicode `casefold()`. Original
`Requirement.text` remains unchanged and authoritative. The complete-token
word-constituent policy is the policy already approved in Section 7.14.6.1.
No generated morphology, synonym, semantic equivalent, or additional normative
surface is authorized. This inventory is a conservative first-production
subset, not an exhaustive Ukrainian normative lexicon.

`RESULT-UK-001` is parser-required. Detector logic consumes only the approved
parser-neutral `SentenceAnnotation` and `TokenAnnotation` values, including
`text`, `lemma`, `upos`, `morphology`, `head_token_id`, and
`dependency_relation`. No spaCy-native document, token, span, tag, or other
provider object enters the detector contract. This allocation does not change
the selected parser backend or version contract in Section 7.15.

Parser sentence annotations are the primary sentence boundary. Within one
parser sentence, semicolon (`;`) is a first-production result hard boundary.
Colon and dash do not independently create a result boundary. The detector must
not split raw source independently on every full stop; parser sentence
boundaries preserve technical forms such as `TLS 1.3` and `OAuth 2.0`.
Terminal sentence punctuation is excluded from result Evidence.

For each parser sentence / semicolon result segment, a candidate is accepted
only when all of the following hold:

1. any accepted leading or postposed edge condition is deterministically
   separated and removed by reusing `ConditionContextBaselineDetector` and its
   `COND-UK-001` result; this rule does not duplicate condition grammar;
2. the remaining candidate is non-empty and contains exactly one approved
   normative anchor;
3. parser annotations establish an explicit local grammatical subject and a
   parser-connected lexical predicate chain associated with that anchor;
4. an explicit lexical behavior predicate is present;
5. neither coordination nor negation requires unresolved scope
   interpretation; and
6. the complete minimal governing result clause maps to one exact contiguous
   span of original `Requirement.text`.

No arbitrary token-distance or character-distance threshold between subject,
normative anchor, and predicate is permitted.

The local-subject requirement is satisfied only by parser dependency relation
`nsubj` or a subtype `nsubj:*` associated with the normative/predicate clause.
An omitted subject or actor is not inferred from surrounding document context.
This grammatical acceptance condition does not reintroduce the deferred
`actor` feature.

The normative anchor must participate in a parser-connected predicate chain
that reaches an explicit lexical behavior predicate. The first-production rule
may use only `xcomp`, `ccomp`, `aux`, and `cop` relations to connect the
normative construction to that predicate, and only where those relations
actually occur in the parser-neutral representation. The chain must reach a
token with `upos = VERB`, or a token represented as a participial verbal form
by the approved parser-neutral morphology. An `AUX` token alone is insufficient,
and a following noun phrase does not become a result merely because it follows
a normative anchor. The rule must not require one provider-specific dependency
tree shape.

The following passive construction is a binding first-production target:

```text
новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с
```

A parser-neutral chain equivalent to `має -> бути -> сформований` is accepted
when it satisfies the subject and predicate requirements above. Result Evidence
is the entire clause exactly as shown. The inner quantitative bound remains
independently governed by `QuantitativeBaselineDetector`; cross-family Evidence
overlap is allowed, but quantitative Evidence is not copied into or used to
mutate the expected-result observation. No new metric or context interpretation
is introduced.

For accepted results, Evidence is the complete minimal governing result clause
after deterministic accepted edge-condition removal. It includes the locally
expressed subject, normative construction, predicate, essential complements,
and any source-attested quantitative bound belonging to the required result.
It excludes a separable leading or postposed condition, terminal sentence
punctuation, and any neighboring hard segment. Evidence offsets are zero-based
Unicode code-point offsets into original trimmed `Requirement.text`, start
inclusive and end exclusive, and must satisfy the Section 7.5 round-trip
invariant.

The simple binding case `Система повинна сформувати звіт.` produces Evidence
`Система повинна сформувати звіт`, with `processing_status = COMPLETE` and
derived status `DETECTED`.

Condition separation is binding in these cases:

| Input | Independent condition Evidence | `RESULT-UK-001` Evidence |
| --- | --- | --- |
| `Якщо сервіс недоступний, система повинна зберегти запит.` | `Якщо сервіс недоступний` | `система повинна зберегти запит` |
| `Система повинна залишатися доступною під час пікового навантаження.` | `під час пікового навантаження` | `Система повинна залишатися доступною` |

An accepted edge condition may be removed only when its source relationship is
structurally deterministic. If condition detection for the same structural
candidate is `INCOMPLETE` and its unresolved boundary or attachment affects the
result candidate, the result remains unresolved; the detector must not guess
across `COND_UNRESOLVED_CANDIDATE`.

Each accepted result creates exactly one observation:

```python
FeatureObservation(
    feature_id=FeatureId.EXPECTED_RESULT,
    evidence_refs=(evidence_id,),
)
```

The corresponding Evidence has `feature_id = EXPECTED_RESULT` and
`rule_id = RESULT-UK-001`. Parser tags, dependency details, confidence, and
duplicated source text are not added to `FeatureObservation`.

Exactly two diagnostics are allocated for this production rule:

| Diagnostic code | Binding use |
| --- | --- |
| `RESULT_UNRESOLVED_CANDIDATE` | A source candidate exists, but the narrow grammar cannot establish normative force, result scope, condition separation, coordination scope, or negation scope. |
| `RESULT_PARSER_BLOCKED` | Parser-required analysis cannot complete because of `PARSER_UNAVAILABLE`, `PARSER_PROCESSING_FAILED`, `ANNOTATION_INCOMPLETE`, or `OFFSET_INVARIANT_FAILED`. |

Both diagnostics use `rule_id = RESULT-UK-001`. Neither diagnostic is Evidence,
and neither creates a `FeatureObservation`. A diagnostic candidate span is
present only when an exact affected original-source span can still be
established. The parser reason may be preserved in the human-readable
explanation.

The synthetic binding case `Система контролює обробку запитів.` is not
sufficient for `DETECTED`. When parser annotations establish an apparent
local-subject lexical behavior candidate but no first-production normative
anchor, the outcome has no observation or Evidence and contains
`RESULT_UNRESOLVED_CANDIDATE`; processing is `INCOMPLETE` and derived status is
`UNRESOLVED`. There is no arbitrary-verb fallback.

The source-attested descriptive statement
`У двох частинах документа задано різний час завершення неактивної сесії: 15 і
30 хвилин.` is not an accepted expected result. A reported conflict must not be
reinterpreted as required system behavior. When the narrow rule establishes no
apparent local-subject behavior candidate, all approved checks may complete as
`NOT_DETECTED`.

General coordinated and non-modal result grammar is outside `RESULT-UK-001`.
A candidate with independently headed predicates or parser `conj` structure
whose scopes would need to be separated is unresolved rather than guessed.
The source-attested `R5 → R5′` clauses remain family-level semantic reference
cases, while their inherited normative force and coordinated scopes remain
open under `RQD-006`; they are not erased or falsely claimed as executable
first-production coverage. A segment containing multiple approved normative
anchors is likewise unresolved unless hard segmentation has already established
independent result segments.

General negation-scope interpretation is also outside first production. A
parser-visible negation whose scope must be interpreted produces
`RESULT_UNRESOLVED_CANDIDATE`. Negation is neither removed nor inverted, and
negative behavior is not reinterpreted as positive behavior.

For any of `PARSER_UNAVAILABLE`, `PARSER_PROCESSING_FAILED`,
`ANNOTATION_INCOMPLETE`, or `OFFSET_INVARIANT_FAILED`, this parser-required
family returns exactly:

```text
observations = ()
evidence = ()
processing_status = INCOMPLETE
diagnostic = RESULT_PARSER_BLOCKED
```

With no accepted observation, derived status is `UNRESOLVED`. Parser failure is
never mapped to `NOT_DETECTED` or `NOT_APPLICABLE`. This is the family-specific
binding application of Section 7.15.8.

The family outcome semantics are:

| Accepted observations | Unresolved or blocked candidate | Processing | Derived status |
| --- | --- | --- | --- |
| present | none | `COMPLETE` | `DETECTED` |
| none | none; all approved checks completed | `COMPLETE` | `NOT_DETECTED` |
| none | present | `INCOMPLETE` | `UNRESOLVED` |
| present | present elsewhere | `INCOMPLETE` | `DETECTED` |

This allocation resolves only the deterministic normative-modal
first-production subset. `RQD-006` remains `PARTIALLY APPROVED / OPEN` for
general expected-result grammar, non-modal or inherited normative force,
coordinated results, general negation, implicit subjects, general condition
attachment beyond `COND-UK-001`, non-numeric acceptance grammar, and
verification-method grammar beyond `VERIFY-UK-001`.

#### 7.14.5 `acceptance_criterion`

Dynamic methods, Section 3.2, Table 3.4 defines a criterion through a threshold,
expected behavior, admissible range, or condition. Requirement properties,
Section 2.1, Table 2.1 treats a criterion, threshold, test oracle, analysis, or
inspection method as possible Verifiability evidence. Metrics system,
Section 2.3, paragraphs 18-21 distinguishes an explicit acceptance criterion
from a reproducible verification procedure and from a quantitative quality
criterion.

The approved narrow baseline accepts a quantitative expression as an
`acceptance_criterion` only when it is linked to explicit required/expected
behavior and supplies an admissible bound or target against which the behavior
can be judged. A version, identifier, date, observed value, load description, or
other number is not automatically a criterion. A quantitative context such as
`при навантаженні до 300 одночасних запитів` is not automatically a pass/fail
criterion for the result it qualifies.

For non-numeric criteria, parser assistance must establish a complete observable
behavior under an explicit condition such that fulfilment can be judged. This
supports source cases such as the failure reactions in the Application example,
Section 8, Table 7, `R5 → R5′`, but does not assume that every expected result is
sufficiently precise to be an acceptance criterion.

Evidence for a quantitative criterion is the minimal full clause containing the
judged subject/behavior and bound, not the number alone. Evidence for a
non-numeric criterion is the complete observable behavior clause plus a
reference to any separately captured governing condition. One span may validly
support `expected_result`, `acceptance_criterion`, and
`quantitative_constraint`, because the sources give overlapping semantic roles;
this permission does not imply universal equivalence.

| Relationship | Approved conclusion |
| --- | --- |
| Quantitative bound → acceptance criterion | Sometimes. Only an attached target/admissible bound for required behavior qualifies. |
| Quantitative expression → acceptance criterion | Not universally. Versions, identifiers, observed counts, and context-only quantities do not qualify. |
| Expected result → acceptance criterion | Not universally. The result must be observable and sufficiently explicit to judge fulfilment. |
| Acceptance criterion → quantitative constraint | Not universally. Section 3.2 Table 3.4 explicitly permits expected behavior or a condition without a numeric bound. |

| Case | Source status and input | Approved detector output | Evidence span(s) | Approved rule family |
| --- | --- | --- | --- | --- |
| Positive | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R2 → R2′` | `DETECTED`; route-generation bound is judgeable | `[44,116)` `новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с` | `ACCEPT-UK` |
| Negative | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R7 → R7′`: `Для кожної критичної API-вимоги створити traceability link до acceptance test, NFR test та відповідного релізного критерію.` | `NOT_DETECTED`; it requests links but supplies no acceptance content | none | `ACCEPT-UK` |
| Unresolved | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система забезпечує належний результат обробки.` | `UNRESOLVED`; neither an observable boundary nor a reproducibly judgeable behavior is explicit | no accepted evidence | `ACCEPT-UK` |
| Repeated | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R5 → R5′` | `DETECTED` for each parser-confirmed observable failure reaction; each remains independently judgeable | result spans `[39,65)`, `[67,93)`, `[95,132)`, and `[145,159)`, with governing conditions `[0,37)` or `[134,144)` as applicable | `ACCEPT-UK` |
| Punctuation | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R1 → R1′` | `DETECTED`; semicolon separates two candidate criteria rather than merging them | `[0,90)` update-frequency clause; `[92,177)` percentile-latency clause | `ACCEPT-UK` |
| Interaction | Same `R2 → R2′` source case | Result and acceptance evidence may share `[44,116)`; quantitative evidence uses the inner bound and linked metric/context evidence | `[44,116)`, including `[96,116)` | `RESULT-UK`, `ACCEPT-UK`, `QUANT` |

##### 7.14.5.1 First-production quantitative allocation (Issue #43)

`ACCEPT-QUANT-001` is the only acceptance-criterion production rule allocated
by this contract. It is a narrow clause-level composition of already accepted
upstream results:

```text
accepted RESULT-UK-001 expected-result Evidence
+
judgeable accepted QUANT-001 / QUANT-UK-001 quantitative observation
+
complete source-span containment
```

The future detector must reuse `ExpectedResultBaselineDetector` and
`QuantitativeBaselineDetector`. It must not duplicate or reinterpret
`RESULT-UK-001`, `QUANT-001`, `QUANT-UK-001`, or the transitively reused
`COND-UK-001` condition separation. It introduces no parser grammar, no direct
spaCy-native dependency, and no independent parser workaround. Parser-native
objects remain behind the existing expected-result dependency.

Only accepted `expected_result` Evidence with
`rule_id = RESULT-UK-001` may establish the required/expected-behavior side of
this rule. An unresolved expected-result candidate, descriptive sentence,
arbitrary verb clause, or quantitative expression without such an accepted
governing result is not a behavior anchor.

Only accepted quantitative observations whose complete referenced Evidence is
produced by `QUANT-001` or `QUANT-UK-001` may establish a first-production
quantitative criterion. Every Evidence item referenced by that quantitative
observation must lie completely inside one accepted `RESULT-UK-001` Evidence
span:

```text
result.start_offset <= quantitative.start_offset
and quantitative.end_offset <= result.end_offset
```

for every referenced quantitative Evidence item. Quantitative Evidence outside
the result span is not linked to that result, and proximity alone never creates
linkage. The rule does not copy or mutate an upstream observation and does not
infer a missing metric, context, denominator, or measurement procedure.

A linked accepted quantitative observation is judgeable for this allocation
when either:

1. it has `LESS_THAN_OR_EQUAL / INCLUSIVE` or
   `GREATER_THAN_OR_EQUAL / INCLUSIVE`; or
2. it has no comparator and explicitly contains an accepted value plus unit,
   such as `2 с` or `95 %`, inside the accepted required-result Evidence.

The second form is an explicit target because the accepted normative result
states the value and unit as required behavior. It does not authorize an
inferred comparator or any other missing semantic component. No other current
comparator meaning is judgeable under `ACCEPT-QUANT-001`.

In particular, Ukrainian `до` remains exactly:

```text
UPPER_BOUND / UNRESOLVED
```

It is not sufficiently exact for an accepted first-production pass/fail
criterion and must never be reinterpreted as `<=`. Therefore:

```text
Система повинна відповісти до 2 с.
```

may contain an accepted quantitative observation, but it creates no acceptance
observation or Evidence. It produces `ACCEPT_UNRESOLVED_CANDIDATE`, with
`processing_status = INCOMPLETE` and derived status `UNRESOLVED`.

For each accepted `RESULT-UK-001` Evidence span, apply this clause-level
algorithm:

1. collect accepted quantitative observations whose complete referenced
   Evidence lies inside that result span;
2. classify every linked observation as either a judgeable first-production
   anchor or an unresolved/non-judgeable first-production anchor;
3. consider source-bound `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` diagnostics whose
   complete candidate span lies inside the result span and whose role cannot be
   deterministically excluded;
4. if at least one judgeable anchor exists, accept the complete result clause as
   exactly one `acceptance_criterion` observation;
5. preserve `ACCEPT_UNRESOLVED_CANDIDATE` diagnostics for linked unresolved or
   non-judgeable quantitative candidates even when another anchor establishes
   the criterion; and
6. ignore quantitative Evidence and candidate spans outside the result span for
   that result.

This is clause-level acceptance detection, not one acceptance observation per
numeric expression. One accepted expected-result clause produces at most one
`ACCEPT-QUANT-001` observation. Repeated source-distinct accepted result clauses
remain distinct criteria.

Acceptance Evidence is exactly the complete accepted `RESULT-UK-001` clause
that contains the qualifying quantitative bound or target. It is not merely
`2`, `2 с`, `95 %`, or `≤ 2 с` when the governing result clause is larger.
The acceptance family creates independent Evidence with:

```text
feature_id = ACCEPTANCE_CRITERION
rule_id = ACCEPT-QUANT-001
evidence_id = ACCEPT-QUANT-001:E001, ACCEPT-QUANT-001:E002, ...
```

The acceptance Evidence source span may intentionally equal the source span of
the governing `RESULT-UK-001` Evidence. This cross-family overlap is valid, but
the result or quantitative Evidence ID is never reused. Each accepted criterion
creates the existing stable simple observation only:

```python
FeatureObservation(
    feature_id=FeatureId.ACCEPTANCE_CRITERION,
    evidence_refs=(evidence_id,),
)
```

No `result_reference`, `quantitative_reference`, confidence, score, severity,
or new observation type is added. Linkage remains traceable through source
offsets and the independent family Evidence.

Exactly two diagnostics are allocated for this rule:

| Diagnostic code | Binding use |
| --- | --- |
| `ACCEPT_UNRESOLVED_CANDIDATE` | A plausible quantitative acceptance candidate exists, but the approved composition cannot establish a uniquely judgeable criterion or linkage. |
| `ACCEPT_DEPENDENCY_BLOCKED` | The required expected-result dependency cannot execute, including `RESULT_PARSER_BLOCKED`. |

Both diagnostics use `rule_id = ACCEPT-QUANT-001`. They are not accepted
Evidence, create no `FeatureObservation`, Finding, applicability value, or
score, and do not enter `RequirementExtractionResult.evidence`. A source-bound
unresolved quantitative diagnostic preserves its upstream candidate span; an
accepted but non-judgeable quantitative anchor preserves its complete
quantitative Evidence span as the acceptance diagnostic candidate span. The
unresolved-result case below instead uses the complete unresolved result
candidate span. Diagnostics are source ordered; a dependency-blocked diagnostic
without a source span follows source-bound diagnostics.

The following cases are binding:

| Case | Input and upstream condition | `ACCEPT-QUANT-001` result |
| --- | --- | --- |
| Resolved comparator | `Система повинна відповісти не більше ніж за 2 с.` with accepted `RESULT-UK-001` and contained `QUANT-UK-001` Evidence | One acceptance observation with Evidence `Система повинна відповісти не більше ніж за 2 с`; `COMPLETE / DETECTED` |
| Explicit value + unit target | `Система повинна завершити операцію за 2 с.` with accepted `2 с` from `QUANT-001` inside accepted result Evidence | One acceptance observation with Evidence `Система повинна завершити операцію за 2 с`; no comparator is required |
| Clause-level deduplication | `новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с` | Exactly one acceptance observation and the complete clause as Evidence, even though `95 %` and `не більше ніж за 4 с` may be separate accepted quantitative observations |
| Separated condition quantity | `Система повинна відповісти не більше ніж за 2 с при 500 одночасних користувачах.` when `COND-UK-001` and `RESULT-UK-001` separate `при 500 одночасних користувачах` | Only quantitative Evidence completely inside result Evidence may qualify; the condition-only quantity cannot independently qualify the result, and the condition remains separately traceable |
| Load-context negative | `Система повинна залишатися доступною при навантаженні до 300 одночасних запитів.` when the `при ...` phrase is separated as `condition_context` | `до 300` lies outside result Evidence and cannot satisfy this rule; the load description is not promoted to a pass/fail criterion |
| Technical-version negative | Inputs containing `TLS 1.3` or `OAuth 2.0` | The existing quantitative negative behavior remains authoritative; neither identifier becomes a quantitative acceptance target and no version grammar is added |
| Quantitative fragment only | `Профіль 95 %.` | No acceptance observation: a quantitative expression without accepted `RESULT-UK-001` required behavior is insufficient |
| Accepted result without candidate | An accepted `RESULT-UK-001` clause containing no accepted or unresolved quantitative candidate | `COMPLETE / NOT_DETECTED`; this means only that this narrow quantitative rule did not detect a criterion |

When `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` lies inside accepted
`RESULT-UK-001` Evidence and its role cannot be deterministically excluded, the
acceptance outcome contains `ACCEPT_UNRESOLVED_CANDIDATE`. If a separate
judgeable linked anchor in the same or another accepted result clause already
establishes an acceptance criterion, the accepted observation and Evidence are
retained and the family outcome is `INCOMPLETE / DETECTED`; the unresolved
candidate is not discarded.

When a `RESULT_UNRESOLVED_CANDIDATE` span contains or overlaps either accepted
quantitative Evidence or a `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` span,
acceptance linkage cannot be established. Produce
`ACCEPT_UNRESOLVED_CANDIDATE` using the unresolved result candidate span. Do not
promote the quantitative expression to acceptance Evidence without an accepted
required-behavior clause. An unresolved result candidate with no overlapping
or contained quantitative candidate does not by itself become a candidate for
this narrow quantitative rule.

If `ExpectedResultBaselineDetector` returns `RESULT_PARSER_BLOCKED`, the
required-behavior dependency is globally blocked. The acceptance family returns
exactly:

```text
observations = ()
evidence = ()
processing_status = INCOMPLETE
diagnostic = ACCEPT_DEPENDENCY_BLOCKED
derived status = UNRESOLVED
```

It does not run an independent parser workaround. The family outcome semantics
are:

| Condition | Processing and derived status |
| --- | --- |
| accepted criterion and no unresolved dependency/candidate | `COMPLETE / DETECTED` |
| no candidate under this approved quantitative baseline | `COMPLETE / NOT_DETECTED` |
| unresolved quantitative/result linkage and no accepted criterion | `INCOMPLETE / UNRESOLVED` |
| accepted criterion plus an unresolved candidate elsewhere | `INCOMPLETE / DETECTED` |
| globally blocked required-result dependency | `INCOMPLETE / UNRESOLVED` |

Accepted criteria are ordered by the `start_offset` of their complete
result-clause Evidence. `ACCEPT-QUANT-001` Evidence IDs follow that accepted
source order. Diagnostics are source ordered. No non-numeric acceptance rule,
new expected-result grammar, condition grammar, quantitative grammar,
comparator meaning, verification-method rule, requirement-type inference,
Finding, characteristic calculation, applicability rule, score, or full
`FeatureExtractor` is approved by this allocation.

`RQD-006` remains `PARTIALLY APPROVED / OPEN` for general expected-result and
condition attachment, non-numeric acceptance grammar, and verification-method
grammar beyond `VERIFY-UK-001`. `RQD-008` remains `PARTIALLY APPROVED / OPEN` for complex
metric/context grammar, count-noun and nested quantitative roles, written-out
numbers, generic ranges, and other deferred quantitative forms.

#### 7.14.6 `quantitative_constraint`

This contract preserves the approved linked shape and partial-observation
policy. It does not create independent `has_metric`, `has_threshold`, or
`has_unit` booleans.

##### 7.14.6.1 Comparator forms

The following are source-attested in quantitative requirement or
requirement-like examples. The normalized meanings below are approved only for
the stated forms and qualifications.

| Source surface form | Approved normalized meaning | Traceability | Status/qualification |
| --- | --- | --- | --- |
| `≤` | `LESS_THAN_OR_EQUAL` | Requirements and product quality, Section 2.2, Table 2.5, semantic example | `SOURCE-ATTESTED`; approved mapping |
| `не довше ніж` | `LESS_THAN_OR_EQUAL` for duration | Requirements and product quality, Section 2.2, paragraph 4 | `SOURCE-ATTESTED`; approved mapping |
| `не довше` | `LESS_THAN_OR_EQUAL` for duration | Dynamic methods, Section 3.2, paragraph 21 | `SOURCE-ATTESTED`; approved mapping |
| `не більше` | `LESS_THAN_OR_EQUAL` | Application example, Section 8, Table 7, `R1 → R1′` | `SOURCE-ATTESTED`; approved mapping |
| `не більше ніж` | `LESS_THAN_OR_EQUAL` | Application example, Section 8, Table 7, `R2 → R2′` | `SOURCE-ATTESTED`; approved mapping |
| `не нижче` | `GREATER_THAN_OR_EQUAL` | Application example, Section 8, Table 7, `R4 → R4′` | `SOURCE-ATTESTED`; approved mapping |
| `не рідше` | `NOT_LESS_FREQUENT`; numeric direction depends on whether the metric is frequency or interval | Application example, Section 8, Table 7, `R1 → R1′` | `SOURCE-ATTESTED`; the written-out count and normalized numeric operator remain unresolved |
| `до` | comparator `UPPER_BOUND`; inclusivity `UNRESOLVED` | Application example, Section 8, Table 7, `R2 → R2′` | `SOURCE-ATTESTED`; preserve surface/value and do not map to `LESS_THAN_OR_EQUAL`; unresolved inclusivity is not a scoring state |

The literals `<`, `>`, `=`, and `≥` occur elsewhere in the corpus in formulas,
state transitions, or model checkpoints, but not as supplied natural-language
requirement comparator examples for this contract. `не менше` and `не пізніше`
do not occur in the supplied corpus. `щонайменше` occurs in explanatory prose,
not as an example requirement bound. Treating any of these forms as a production
constraint comparator is a **PROPOSED IMPLEMENTATION EXTENSION**, not
source-derived detector evidence. No mapping is approved here.

Comparator evidence begins at the first comparator symbol/word and continues
through any fixed grammatical material that belongs to the attested construction
(`ніж`, or duration-introducing `за`) and the linked numeric/unit phrase. A
negation or comparative word separated from a compatible value is not accepted.

For `QUANT-UK-001`, match only the six allocated Ukrainian comparator literals
on an offset-preserving derived view: normalize to NFC, then apply Unicode
`casefold()` to both source and literals. Original `Requirement.text` is never
changed. Map derived-view matches back to zero-based Unicode code-point offsets
in the trimmed original text; transformed-view indices must never be used
directly as Evidence offsets. Evidence text is always the exact original
`Requirement.text[start_offset:end_offset]`, preserving source case,
normalization form, whitespace, and punctuation inside the accepted anchor.

Canonical spaces between tokens of a multi-token comparator may match one or
more Unicode whitespace characters. This is formatting tolerance only:
punctuation cannot replace the separator, and lexical tokens cannot be
inserted, omitted, reordered, inflected, or semantically expanded. Match
comparator words as complete lexical tokens. At outer boundaries, a Unicode
Letter, Mark, Number, Connector_Punctuation, or one of `'`, `’`, `ʼ`, `-` is a
word constituent. In particular, `до` cannot match inside a longer joined
word. This matching policy does not add comparator vocabulary or transfer the
vague-term matcher's overlap policy to quantitative detection.

##### 7.14.6.2 Numeric forms

| Form | Source-attested example and traceability | Approved MVP treatment |
| --- | --- | --- |
| Integer | `2`, `500` in Requirements and product quality, Section 2.2, Table 2.5; `3`, `4`, `300`, `15`, `2` in Application example, Section 8, Table 7 | Accept ASCII digit integers in a linked quantitative candidate |
| Decimal comma | `99,9 %` in Application example, Section 8, Table 7, `R4 → R4′` | Accept one comma between digits as a decimal separator; preserve raw text; parsed value is decimal `99.9` without rounding |
| Decimal point | `TLS 1.3` and `OAuth 2.0` in Application example, Section 8, Table 7, `R3 → R3′` | Source-attested as version identifiers, not measured values; do not treat as a quantitative constraint without an independently established metric/comparator relation |
| Percentage | `95 %` in Requirements and product quality, Section 2.2, paragraph 4; `95 %` and `99,9 %` in Application example, Section 8, Table 7 | Accept the number plus percent sign as one value/unit chunk whether separated by the source-attested single space; do not infer a denominator not expressed by the clause |
| Count/population | `500 одночасних користувачах` in Section 2.2 Table 2.5; `300 одночасних запитів` in Application example Table 7 | Preserve the count and population phrase; decide through linkage whether it is metric, constraint, or context |
| Duration | `2 с` in Section 2.2 paragraph 4/Table 2.5; `3 с`, `4 с`, `15 с`, `2 хв`, and `15 хв` in Application example Table 7 | Accept only source-supported unit forms; no conversion between seconds and minutes |
| Ordinal/percentile | `95-й перцентиль` in Application example, Section 8, Table 7, `R1 → R1′` | Preserve as metric qualifier; do not convert it to a percentage observation |
| Written-out number | `одного разу` in the same `R1 → R1′` example | `OUT_OF_MVP_V0.1_BASELINE`; do not parse it as numeric `1`; an implementation may preserve an unresolved candidate without accepting a quantitative observation |
| Range | “допустимий діапазон” is a semantic category in Dynamic methods, Section 3.2, Table 3.4, but no literal requirement range syntax is supplied | Generic range syntax is deferred; only a separately approved source-attested construction may enter the MVP baseline |

Signs, exponent notation, digit grouping, ordinals other than the attested
percentile construction, dates, and symbolic variables are not approved numeric
forms. A numeric token in a version, identifier, formula, or document reference
must not count merely because it contains digits.

##### 7.14.6.3 Unit forms

| Surface form | Approved normalized label | Traceability | Limitation |
| --- | --- | --- | --- |
| `с` | `SECOND` | Requirements and product quality, Section 2.2, paragraph 4/Table 2.5; Application example, Section 8, Table 7, R1′/R2′ | No implicit plural or conversion rule is needed for the abbreviation |
| `хв` | `MINUTE` | Application example, Section 8, Table 7, R5′/R6′ | No conversion to seconds |
| `хвилин` | `MINUTE` | Application example, Section 2, Table 1, R6 | Inflected forms not present in the sources are not generated |
| `секунд` | `SECOND` | Section 7.6 authoritative model-spec operational example | Researcher-approved operational form; not `SOURCE-ATTESTED` in the supplied corpus; no automatic inflection expansion |
| `%` | `PERCENT` | Requirements and product quality, Section 2.2, paragraph 4; Application example, Section 8, Table 7 | A percent is not complete without its associated population/metric semantics |

`користувачах`, `запитів`, and `разу` are source-attested count/population nouns,
not entries in a general unit ontology. They may be preserved inside metric or
context evidence. A future unit registry, SI/IT ontology, aliases, compound
units, and unit conversion are outside this contract.

The `секунд` entry is approved because Section 7.6 is an authoritative
model-spec operational example. That approval does not relabel the form as
`SOURCE-ATTESTED` corpus evidence and does not authorize an ontology, generated
aliases, inflection rules, or unit conversions.

##### 7.14.6.4 Metric and context

Source-attested metric expressions include `Час відгуку` (Requirements and
product quality, Section 2.2, Table 2.5), a percentage of processed requests
(Section 2.2, paragraph 4), `95-й перцентиль затримки від отримання GPS-події до
відображення в UI` and update frequency (Application example, Section 8,
Table 7, R1′), implicit route-generation duration (R2′), and `Місячна доступність
сервісу` (R4′). They demonstrate metric roles but do not define an exhaustive
metric vocabulary.

The first-production lexical baseline in Section 7.14.6.6 does not infer or
attach a metric: `metric = None` without an `unresolved_components` entry when
no metric candidate is expressed as part of the accepted anchor. A separately
approved grammar may later attach an explicit nominal metric phrase
unambiguously to the bound. Parser assistance may then extract the governing
noun phrase and essential complements. It must not infer a metric such as
latency merely because a duration occurs.

Source-attested quantitative contexts include `при 500 одночасних
користувачах` in Section 2.2 Table 2.5 and `при навантаженні до 300 одночасних
запитів` in the Application example Table 7 R2′. A population qualifier such as
`для 95 % запитів`, a temporal measurement window such as `Місячна`, and a load
bound may be part of the metric, context, or a nested constraint. When the role
is not unique, the component remains unresolved.

`condition_context` and quantitative `context` are not duplicate semantics.
The former is a general feature observation consumed by Completeness; the latter
is the condition retained inside one linked quantitative observation. The same
source evidence may support both. If a context contains its own measurable
bound, it may also form a separate quantitative observation, provided each role
is explicit and traceable.

##### 7.14.6.5 Approved linkage algorithm

The following conservative linkage algorithm is approved for the baseline:

1. Build an offset-preserving matching view and identify protected numeric
   chunks before punctuation segmentation. A decimal comma between digits is
   part of the number; a period inside a recognized version candidate does not
   make that version a quantitative value.
2. Segment the requirement into parser-provided clauses when available. In the
   lexical baseline, full stop, semicolon, question mark, and exclamation mark
   are hard boundaries. Comma is a soft boundary and cannot by itself authorize
   cross-clause linkage.
3. Create one candidate around each explicit numeric/value chunk. Attach a
   comparator only through a source-approved contiguous construction that
   governs that value. Attach a unit only when it is in the same numeric phrase.
   No arbitrary token-distance or character-distance threshold is used.
4. Link a metric only under a separately approved template or grammatical rule
   relating one governing metric phrase to the bound in the same clause. If an
   expressed candidate cannot be resolved, name `METRIC` in
   `unresolved_components`; do not select the nearest among compatible phrases.
   The first-production anchor alone does not attempt this linkage.
5. Link context only under a separately approved rule when a marker-headed
   phrase/clause modifies the same metric, result, or bound. A unique
   grammatical attachment may cross a comma inside the same sentence; it may
   not cross a hard boundary. Ambiguous context remains unresolved. The
   first-production anchor alone does not attempt this linkage.
6. Do not merge distinct numeric anchors except through an approved range
   construction. No generic range construction is approved. Each bound
   therefore remains independently traceable.
7. A context bound may be represented both as the `context` of the primary
   target and as its own partial quantitative observation only when both roles
   are explicit under an approved grammar/template rule. Until that concrete
   nested-context rule is approved, leave that nested-role decision unresolved;
   the first-production subset creates only its separately accepted anchors,
   not speculative metric/context Evidence.
8. A candidate with an explicit comparator/value or value/unit relation becomes
   a partial `QuantitativeConstraintObservation` even when metric or context is
   unresolved. If digits may instead be a version, identifier, date, or label and
   the rule cannot decide, no observation is created and the detector outcome is
   `UNRESOLVED`.
9. Order observations by the first referenced `start_offset`; order each
   observation's evidence references by `(start_offset, end_offset, evidence_id)`.

| Case | Source status and input | Approved detector output | Evidence span(s) and linked fields | Approved rule family |
| --- | --- | --- | --- | --- |
| Positive | SOURCE-ATTESTED — Requirements and product quality, Section 2.2, Table 2.5: `Час відгуку ≤ 2 с при 500 одночасних користувачах` | `DETECTED`; one primary constraint | metric `[0,11)`; bound `[12,17)` with comparator `LESS_THAN_OR_EQUAL`, value `2`, unit `SECOND`; context `[18,49)` | `QUANT` |
| Negative | SOURCE-ATTESTED — Application example, Section 8, Table 7, R3′: `Дані передаються через TLS 1.3; доступ до API — за OAuth 2.0/OIDC; ...` | `NOT_DETECTED` for `1.3` and `2.0`; they are version identifiers without a bound relation | none for those numbers | `QUANT` |
| Unresolved | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система використовує профіль 95.` | `UNRESOLVED`; `95` may be a label or quantity and has no explicit metric/comparator/unit relation | no accepted evidence | `QUANT` |
| Repeated | SOURCE-ATTESTED — Application example, Section 8, Table 7, R1′ | `DETECTED` for the `не більше 3 с` bound; the distinct `не рідше одного разу на 5 с` frequency construction awaits separately approved production grammar | First-production accepted bound `[164,177)` `не більше 3 с`; `[63,90)` frequency construction and metric `[92,161)` remain research linkage candidates, not first-production Evidence | `QUANT` |
| Punctuation/decimal | SOURCE-ATTESTED — Application example, Section 8, Table 7, R4′: `Місячна доступність сервісу — не нижче 99,9 %; ...` | `DETECTED`; comma belongs to decimal and semicolon ends the constraint | metric `[0,27)`; bound `[30,45)` with comparator `GREATER_THAN_OR_EQUAL`, raw value `99,9`, unit `PERCENT` | `QUANT` |
| Nested interaction | SOURCE-ATTESTED — Application example, Section 8, Table 7, R2′ | `DETECTED`; primary four-second route bound with linked load context; separate nested load observation remains unresolved | primary bound `[96,116)`; context `[117,159)`; nested candidate `[134,159)` with comparator `UPPER_BOUND` and inclusivity `UNRESOLVED` | `QUANT`, `COND-UK` |

The metric/context and nested-role entries in this research traceability table
do not allocate production grammar. In particular, the frequency candidate
`не рідше одного разу на 5 с` is not an accepted `QUANT-UK-001` anchor:
its written-out count is outside the first-production numeric baseline.

##### 7.14.6.6 First-production quantitative lexical allocation (Issue #29)

Only the following production IDs are allocated for this narrow baseline.
Both produce `quantitative_constraint` observations and accepted Evidence;
neither creates findings or characteristic scores.

| Rule ID | Profile and accepted anchor | Evidence boundary | Approval and status |
| --- | --- | --- | --- |
| `QUANT-001` | Language-independent symbolic `≤` linked to an approved ASCII numeric value; or an approved value + unit fallback not consumed by a higher-precedence accepted comparator anchor | One contiguous explicit comparator/value/unit or value/unit construction, excluding outside whitespace and sentence-final punctuation | Issue #29; allocated for first production |
| `QUANT-UK-001` | Ukrainian `не довше ніж`, `не довше`, `не більше ніж`, `не більше`, `не нижче`, or `до`, linked through the approved contiguous construction to an approved ASCII numeric value and, where present, an approved unit | One contiguous explicit comparator/value/unit construction, including fixed grammatical material such as duration-introducing `за` when required | Issue #29; allocated for first production |

The numeric forms remain ASCII digit integers and a single decimal comma
between digits. The only unit surfaces are `с`, `хв`, `хвилин`, `секунд`, and
`%`, with labels `SECOND`, `MINUTE`, and `PERCENT` as in Section 7.14.6.3.
No decimal-point measured values, scientific notation, grouping, new aliases,
conversion, generic ranges, or written-out-number parsing are allocated.
`QUANT-001` does not accept `<`, `>`, `=`, or `≥` as comparator forms.

For `QUANT-001`, `≤` maps to `LESS_THAN_OR_EQUAL` with `INCLUSIVE`
inclusivity. For `QUANT-UK-001`, `не довше ніж`, `не довше`, `не більше ніж`, and
`не більше` map to `LESS_THAN_OR_EQUAL` with `INCLUSIVE` inclusivity;
`не нижче` maps to `GREATER_THAN_OR_EQUAL` with `INCLUSIVE` inclusivity;
`до` maps to `UPPER_BOUND` with `UNRESOLVED` inclusivity. The domain label
`NOT_LESS_FREQUENT` remains approved, but `не рідше` is deliberately not
allocated to this first production subset. Its supplied construction
`не рідше одного разу на 5 с` depends on written-out-number semantics
deferred here. A future separately approved rule may operationalize that
specific construction without general written-number parsing.

Baseline candidate precedence is exactly:

```text
1. Ukrainian lexical comparator candidate
2. symbolic comparator candidate
3. value + unit fallback
```

Before accepting step 3, protect exactly the deferred frequency construction
`не рідше одного разу на <approved numeric value> <approved duration unit>`.
Its fixed ordered lexical tokens are `не`, `рідше`, `одного`, `разу`, `на`;
the numeric value uses only the ASCII-integer or single-decimal-comma baseline
in Section 7.14.6.2, and the duration unit surface is only `с`, `секунд`,
`хв`, or `хвилин`. Match the fixed Ukrainian tokens on the same
offset-preserving NFC-then-Unicode-`casefold()` view, with complete lexical
token boundaries and one or more Unicode whitespace characters between the
fixed tokens, value, and unit. No punctuation or arbitrary material may be
inserted into this construction. This is a protected exclusion, not a fourth
production observation rule or a general suppression of other `не рідше`
phrases.

A `QUANT-001` value + unit fallback wholly contained in that protected source
span is ineligible at step 3. For `не рідше одного разу на 5 с`, the nested
`5 с` creates no Evidence or observation. Its numeric candidate creates no
`QUANT_UNRESOLVED_NUMERIC_CANDIDATE` diagnostic either: it is deterministically
accounted for by the protected deferred construction. The protected span
itself creates no Evidence, observation, or diagnostic. With no other baseline
candidate, the outcome has empty observations, Evidence, and diagnostics,
`COMPLETE` processing, and derived `NOT_DETECTED`: this means no accepted
first-production anchor, not that the deferred source phrase is semantically
non-quantitative. The exclusion neither constructs `NOT_LESS_FREQUENT` nor
parses `одного` as numeric `1`; it calculates no frequency or interval meaning.
It requires no new Evidence rule ID. The only accepted production IDs remain
`QUANT-001` and `QUANT-UK-001`.

An approved value + unit fallback may be accepted when it is not consumed by a
higher-precedence accepted comparator anchor. A fallback wholly contained by
such an accepted anchor does not create a duplicate observation: `не більше 3 с`
yields one `не більше 3 с` observation, not another for `3 с`.
Distinct anchors elsewhere in the same requirement remain separate, ordered
by their earliest referenced Evidence `start_offset`; this precedence does
not authorize arbitrary cross-observation merging.

One contiguous accepted anchor Evidence may be referenced by all populated
baseline components explicitly contained in it (`comparator`, `value`,
`unit`). No speculative component-specific duplicate Evidence is required.
Its exact source spelling and zero-based Unicode code-point offsets must
round-trip to the trimmed original requirement text. Accepted Evidence IDs
use source-order ordinals per rule within one requirement assessment:

```text
QUANT-001:E001, QUANT-001:E002, ...
QUANT-UK-001:E001, QUANT-UK-001:E002, ...
```

The distinct rule prefixes preserve ID uniqueness within one
`RequirementExtractionResult`. A baseline anchor populates only the explicit
comparator/value/unit components it contains: `metric = None` and
`context = None`, without automatically naming `METRIC` or `CONTEXT` in
`unresolved_components`. `None` plus an unresolved entry denotes an
explicitly expressed candidate whose role could not be resolved; `None`
without such an entry denotes absence/unexpressed content. Metric/context
grammar, count-noun roles, and nested context/constraint representation
remain open under `RQD-008`.

`QUANT_UNRESOLVED_NUMERIC_CANDIDATE` is the allocated detector diagnostic
code for an approved ASCII numeric candidate that forms neither an accepted
comparator + value nor value + unit anchor and cannot deterministically be
excluded by an already-approved negative rule. In the existing model-spec
example `Система використовує профіль 95.`, its diagnostic candidate span is
exactly `95`, and its `rule_id` is `QUANT-001`. The span is diagnostic only:
no accepted Evidence,
observation, Finding, confidence, or severity is created for this candidate.
The recognized technical-version cases `TLS 1.3` and `OAuth 2.0` remain
`NOT_DETECTED` for those numeric strings, without this diagnostic; this
negative case is not a general identifier ontology.

The approved outcome semantics apply to this family without a stored
`DetectionStatus`:

| Accepted observations | Unresolved candidates | Processing | Derived status |
| --- | --- | --- | --- |
| present | none | `COMPLETE`, no diagnostics | `DETECTED` |
| none | none | `COMPLETE`, no diagnostics | `NOT_DETECTED` |
| none | present | `INCOMPLETE`, diagnostics present | `UNRESOLVED` |
| present | present | `INCOMPLETE`, diagnostics present | `DETECTED` |

This allocation does not close `RQD-008`: complex metric/context grammar,
count-noun roles, nested constraint/context representation, written-out
numbers, generic ranges, and future `не рідше` production grammar remain
`PARTIALLY APPROVED / OPEN`.

#### 7.14.7 `verification_method`

The semantic contract remains “an explicitly stated reproducible verification
method in the requirement text.” Source-derived candidate vocabulary includes:

| Source-derived term/category | Traceability | Approved interpretation limit |
| --- | --- | --- |
| `тестовий оракул`, `метод аналізу`, `інспекції` | Requirement properties, Section 2.1, Table 2.1, Verifiability row | Evidence categories, not sufficient as isolated words |
| `процедура перевірки` / `відтворювана процедура перевірки` | Requirement properties, Section 2.1, paragraph 12; Metrics system, Section 2.3, paragraph 21/Table 2.8 | Must name or state the procedure in the requirement; a claim that one exists elsewhere is insufficient |
| `тест` / `тестовий випадок`, `експеримент` / `експериментальна процедура` | Dynamic methods, Section 3.2, paragraphs 5-7 and Table 3.4 | Must function as the means of verification, not as an object discussed by the system |
| Functional/scenario, performance/load/stress, integration/interoperability, recovery, security, usability, and configuration/platform test categories | Dynamic methods, Section 3.2, Table 3.5 | Source-derived candidate method names; English fragments are retained only when explicitly present in the Ukrainian sources |
| `негативні security tests` | Application example, Section 8, Table 7, R3′ | Explicit named procedure category; does not by itself prove test sufficiency |
| `acceptance test`, `NFR test` | Application example, Section 8, Table 7, R7′ | A link request is not the verification procedure content and must not become method evidence by name alone |
| `спосіб розрахунку SLA` | Application example, Section 8, Table 7, R4′ | Names a method category but does not state the calculation; reproducibility from this line is unresolved |

The approved explicit-only strategy accepts a method only when a complete phrase
explicitly names a verification procedure and one of the approved grammatical
or template constructions establishes its verification role. A method word used
as system behavior, an artifact/link target, a future promise to define a
method, or a statement that a requirement seems testable must not count. A name
by itself is not evidence that the method is reproducible, and apparent
testability never implies `verification_method`.

##### 7.14.7.1 First-production parser/template allocation (Issue #47)

`VERIFY-UK-001` is the only verification-method production rule allocated by
this contract. It produces `FeatureId.VERIFICATION_METHOD` observations and
accepted Evidence only. It creates no Finding, applicability decision,
characteristic assessment, method-sufficiency judgment, or score.

Exactly two detector diagnostics are allocated:

| Diagnostic code | Binding use |
| --- | --- |
| `VERIFY_UNRESOLVED_CANDIDATE` | A source phrase names or plausibly describes a verification method, but the approved first-production rule cannot establish its verification role, method boundary, coordination scope, or reproducibility status. |
| `VERIFY_PARSER_BLOCKED` | Parser-required role analysis cannot execute safely. |

Both diagnostics use `rule_id = VERIFY-UK-001`. A diagnostic is neither
Evidence nor a `FeatureObservation`. An unresolved method candidate creates no
accepted Evidence and no observation; an exact candidate span is preserved in
the diagnostic when its source boundary is known.

Although the broader family remains `PARSER_ASSISTANCE_OPTIONAL`, this
first-production rule is `PARSER_REQUIRED`. Method vocabulary alone cannot
distinguish a verification procedure from system behavior, discussion about
testing, references to test artifacts, or promises to define a method later.
The detector may consume only the existing parser-neutral structures
`SentenceAnnotation` and `TokenAnnotation`, using these fields:

```text
text
lemma
upos
morphology
head_token_id
dependency_relation
sentence_id
start_offset
end_offset
```

No spaCy-native object enters detector logic. No domain field or parser
contract is added by this allocation. Original `Requirement.text` remains the
authoritative source.

For approved lexical and template anchors, comparison uses a derived view
formed by NFC normalization followed by Unicode `casefold()`. Evidence offsets
remain zero-based Unicode code-point offsets into the original trimmed source.
NFKC, NFKD, synonym generation, embedding similarity, LLM classification,
semantic expansion, and automatic translation are not authorized.

The approved Ukrainian candidate method-head lemmas are exactly:

```text
тест
інспекція
аналіз
експеримент
```

The parser lemma may recognize inflected Ukrainian source surfaces. No complete
hand-generated morphology list is authorized. The explicit source-derived
candidate phrases retained by this allocation are exactly:

```text
тестовий оракул
метод аналізу
процедура перевірки
відтворювана процедура перевірки
тестовий випадок
експериментальна процедура
```

The source-attested English fragments retained are exactly:

```text
test
tests
security test
security tests
acceptance test
NFR test
негативні security tests
```

No additional English method category or automatic translation is authorized.
All of these are candidate evidence only. In particular, the presence of any
of the following is insufficient by itself:

```text
аналіз
тест
інспекція
експеримент
acceptance test
NFR test
security tests
```

The binding invariant is:

```text
named method candidate
!=
accepted verification_method
```

unless one of constructions A, B, or C below establishes the verification role.

**Construction A — governing verification predicate.** The approved predicate
surfaces are exactly:

```text
перевіряється
перевіряються
```

No additional verification verb is authorized. Within one parser sentence and
semicolon hard segment, a method phrase is accepted under construction A only
when one applicable approved predicate is present, the candidate belongs to
that governing construction, parser-neutral grammar establishes its
means/instrument role, the phrase is source-contiguous, it contains an approved
method head, and any coordination can be deterministically separated.

For an uncoordinated Ukrainian method phrase, or the governing head of an
approved coordinated method list under construction A, the conservative
instrumental relation is:

```text
dependency_relation = obl
or dependency_relation = obl:*
and morphology includes Case = Ins
```

This is only a grammatical detector rule. It introduces no semantic-role
labelling, actor/action/object feature, or new method ontology. A parse that
does not establish the approved relation deterministically produces
`VERIFY_UNRESOLVED_CANDIDATE`; the detector does not add another dependency
relation merely to fit provider output. A later coordinated member is admitted
only through the exact `та`/`і` method-list rule below and an instrumental
`Case = Ins` method head. No separate dependency relation is allocated or
required for that member; if the approved surface, morphology, and list
boundary do not establish it deterministically, the list is unresolved.

The binding input:

```text
Виконання перевіряється навантажувальним тестом.
```

is `DETECTED` with Evidence exactly:

```text
навантажувальним тестом
```

The governing verification predicate is not part of Evidence when the named
method phrase is independently source-contiguous.

**Construction B — explicit verification label.** The approved template is:

```text
<label> <delimiter> <named method phrase>
```

Approved labels are exactly:

```text
перевірка
метод перевірки
процедура перевірки
```

Approved delimiters are exactly:

```text
:
—
-
```

A method phrase following the label may be accepted only when it remains in the
same parser sentence and semicolon hard segment, contains an approved candidate
method head or complete approved phrase, and has a deterministic source
boundary. For example:

```text
Перевірка: навантажувальний тест.
Перевірка — негативні security tests.
Метод перевірки: інспекція журналу.
```

Evidence excludes the label, delimiter, and terminal punctuation.

**Construction C — exact declaration of a named test method.** The approved
template is exactly:

```text
визначено <named test-method phrase>
```

The only governing surface is `визначено`. No other form, generated morphology,
or synonym is authorized. Construction C is restricted to the already-approved
test family:

```text
тест
test
tests
```

and source-approved test phrases or categories built around those fragments.
It does not authorize arbitrary `аналіз`, `інспекція`, `експеримент`, `метод`,
`процедура`, or `розрахунок` after `визначено`.

After normalized matching of `визначено`, the named test-method phrase must
begin immediately, ignoring only Unicode whitespace. It must remain inside the
same parser sentence and semicolon hard segment. The template cannot skip an
intervening noun, artifact head, or reference phrase. Therefore constructions
equivalent to these do not qualify through construction C:

```text
визначено посилання на acceptance test
визначено документ для NFR test
```

Construction C uses parser-neutral sentence/segment information and
deterministic phrase delimitation. It allocates no dependency relation and no
provider-specific tree shape. An independent predicate, unresolved
coordination, or ambiguous method boundary produces
`VERIFY_UNRESOLVED_CANDIDATE` rather than guessed acceptance. Construction C
adds no coordination grammar.

The complete source-attested R3′ requirement from Application example,
Section 8, Table 7 is:

```text
Дані передаються через TLS 1.3; доступ до API — за OAuth 2.0/OIDC; критичні операції журналюються; дані клієнтів логічно ізолюються між tenant-ами; визначено негативні security tests.
```

Its relevant declaration clause is:

```text
визначено негативні security tests.
```

It is executable under `VERIFY-UK-001` construction C and is `DETECTED`.
Accepted Evidence is exactly `[158,182)`:

```text
негативні security tests
```

The governing `визначено` and terminal full stop are excluded.

Accepted method Evidence under all three constructions is the minimal complete
source-contiguous named method phrase. It includes, as applicable, the method
head, adjectival/category qualifier, and essential local complement identifying
the named procedure. Binding Evidence examples are:

```text
навантажувальним тестом
інспекцією журналу
негативні security tests
```

Evidence excludes the governing verification predicate, explicit verification
label, label delimiter, coordinator, neighboring behavior, unrelated next
clause, semicolon, and sentence-terminal punctuation. Every item must satisfy:

```python
evidence.text == requirement.text[
    evidence.start_offset:evidence.end_offset
]
```

The only first-production method-list coordinators are `та` and `і`. One
approved governing predicate or explicit label may govern several
deterministically separable method phrases, and each phrase creates a separate
observation. Construction C may use no coordination interpretation beyond this
already-approved deterministic method-list rule. A phrase list whose boundary
cannot be separated deterministically produces
`VERIFY_UNRESOLVED_CANDIDATE`; coordinators do not enter Evidence.

The binding coordinated input:

```text
Виконання перевіряється навантажувальним тестом та інспекцією журналу.
```

produces two observations with source-ordered Evidence:

```text
навантажувальним тестом
інспекцією журналу
```

Parser sentence boundaries are primary. Within one parser sentence, semicolon
(`;`) is a hard verification-role boundary: a governing predicate, label, or
declaration cannot attach across it. Colon and dash are not general
segmentation rules; they have special meaning only in construction B. The
detector does not raw-split source on every full stop independently of parser
sentence boundaries.

The binding boundary input:

```text
Виконання перевіряється тестом; аналіз журналу виконує система.
```

is `DETECTED` only for Evidence `тестом`. The second clause does not inherit
`перевіряється`.

The system-behavior case:

```text
Система виконує аналіз журналу.
```

has candidate span `аналіз журналу` but no approved verification-role
construction. Its binding result is:

```text
observations = ()
evidence = ()
diagnostic = VERIFY_UNRESOLVED_CANDIDATE
processing_status = INCOMPLETE
derived status = UNRESOLVED
```

System behavior is not reinterpreted as verification because `аналіз` is a
candidate method word.

The source-attested apparent-testability case:

```text
Маршрут доставки повинен швидко перераховуватися у разі зміни дорожньої ситуації.
```

has no named method candidate and produces empty observations, Evidence, and
diagnostics with `COMPLETE / NOT_DETECTED`. No method is inferred from apparent
testability.

A named method without constructions A, B, or C is unresolved rather than
accepted. This includes isolated `acceptance test`, `NFR test`, and
`security tests` mentions. A reference to a test artifact, link, ticket, or a
request to add, provide, or link a test does not itself state a reproducible
verification method. General artifact/link parsing is not allocated. In
particular, the source-derived `acceptance test` and `NFR test` remain
non-accepted when they function only as references or artifacts, and
construction C applies only to the immediate exact declaration template.

The complete source-attested R4′ context from Application example, Section 8,
Table 7 is:

```text
Місячна доступність сервісу — не нижче 99,9 %; визначено допустимі виключення та спосіб розрахунку SLA.
```

The exact candidate `спосіб розрахунку SLA` at `[81,102)` remains protected and
unresolved because the actual calculation procedure is not stated. It creates
no observation or accepted Evidence and produces
`VERIFY_UNRESOLVED_CANDIDATE`, `processing_status = INCOMPLETE`, and derived
status `UNRESOLVED`; its exact source span is preserved in the diagnostic.
Construction C does not apply even to a form containing
`визначено спосіб розрахунку SLA`, because that phrase is not an approved named
test/test-category phrase. `розрахунок` is not added as a method head and no SLA
calculation procedure is inferred.

No verification method may be inferred from `RESULT-UK-001`, `QUANT-001`,
`QUANT-UK-001`, or `ACCEPT-QUANT-001`. For example:

```text
Система повинна відповісти не більше ніж за 2 с.
```

may have detected `expected_result`, `quantitative_constraint`, and
`acceptance_criterion` observations while `verification_method` remains
`NOT_DETECTED`, unless an approved method is separately stated. A future
verification detector must not depend on `QuantitativeBaselineDetector` or
`AcceptanceCriterionBaselineDetector` for method inference.

Each accepted method creates only the existing observation shape:

```python
FeatureObservation(
    feature_id=FeatureId.VERIFICATION_METHOD,
    evidence_refs=(evidence_id,),
)
```

No `method_type`, confidence, severity, score, probability, parser tags,
reproducibility score, or procedure-quality field is added. Evidence IDs are:

```text
VERIFY-UK-001:E001
VERIFY-UK-001:E002
...
```

assigned in accepted source order within one requirement. Repeated identical
method phrases at different source offsets remain separate Evidence items.
Accepted observations and Evidence are ordered by ascending Evidence
`start_offset`; diagnostics with candidate spans are source ordered. A
parser-blocked diagnostic without a source span follows source-bound
diagnostics if both can coexist.

For any parser blocking diagnostic:

```text
PARSER_UNAVAILABLE
PARSER_PROCESSING_FAILED
ANNOTATION_INCOMPLETE
OFFSET_INVARIANT_FAILED
```

the verification result is exactly:

```text
observations = ()
evidence = ()
processing_status = INCOMPLETE
diagnostic = VERIFY_PARSER_BLOCKED
derived status = UNRESOLVED
```

Parser failure never becomes `NOT_DETECTED` or `NOT_APPLICABLE`, and raw
provider errors do not become Evidence.

The family outcome semantics are:

| Condition | Processing and derived status |
| --- | --- |
| accepted method(s), no diagnostics | `COMPLETE / DETECTED` |
| no accepted method and no method candidate | `COMPLETE / NOT_DETECTED` |
| method candidate with unresolved role, boundary, coordination, or reproducibility | `INCOMPLETE / UNRESOLVED` |
| accepted method(s) plus an unresolved candidate elsewhere | `INCOMPLETE / DETECTED` |
| parser blocked | `INCOMPLETE / UNRESOLVED` |

This allocation preserves the Section 7.14.10 and `RQD-016` boundary:
verification-method detection produces observations, accepted Evidence, and
diagnostics only. It produces no Finding, `QUALITY_PROBLEM`, Verifiability
score, or other characteristic calculation.

`RQD-006` remains `PARTIALLY APPROVED / OPEN`. `VERIFY-UK-001` resolves only:

```text
Construction A: перевіряється / перевіряються + instrumental method
Construction B: explicit verification label + delimiter + named method
Construction C: визначено + immediately following named test-method phrase
```

Still open are broader expected-result grammar, general condition attachment,
non-numeric acceptance grammar, general declaration predicates, general
verification predicates and labels, arbitrary method noun phrases, broader
coordination, general artifact/reference interpretation, imperative
verification instructions, implicit procedures, semantic inference of
reproducibility, and richer procedure-content grammar. This allocation does not
close general verification-method grammar.

This contract does not approve or implement
`VerificationMethodBaselineDetector`, characteristic calculation,
Verifiability scoring, method sufficiency scoring, method taxonomy output,
testability inference, method inference from quantitative constraints or
acceptance criteria, new English method vocabulary, general artifact/link
resolution, requirement-type inference, Finding conversion, applicability,
`C`/`V`/`U` calculations, `FeatureExtractor` orchestration, or CLI/PoC work.

#### 7.14.8 Exact `uk_vague_terms_v1` matching mechanics

The ten approved literals in Section 7.8 remain unchanged. The following exact
mechanics are approved for MVP v0.1.

**Case handling.** Use Unicode `casefold()` rather than locale-sensitive case
conversion or ASCII lowering. It provides a defined Unicode caseless operation
and keeps the mechanism replaceable across language profiles. Both the
requirement matching view and the approved lexicon are transformed identically.
Because case folding can change code-point count for some Unicode characters,
the matching view must retain a provenance map to original offsets. This is an
implementation mechanic, not a change to `Evidence.text`.

**Unicode normalization.** Normalize only the derived matching view and lexicon
to NFC before case folding. NFC is approved because canonically equivalent
Ukrainian text, especially a decomposed base letter plus combining mark, should
not fail matching solely because of encoding composition. Compatibility
normalization (`NFKC`/`NFKD`) is not approved because it may collapse
typographically or semantically distinct source characters. Each transformed
code-point interval retains the minimal covering original interval. A candidate
is accepted only when transforming that exact original slice reproduces the
matched lexicon entry. Original evidence and offsets are never normalized.

**Token boundaries.** For a single-token entry, both sides must be start/end of
text or a non-word boundary. A word constituent is a Unicode letter, combining
mark, or number, plus connector punctuation and the apostrophe/hyphen characters
that may join Ukrainian word forms (`'`, `’`, `ʼ`, `-`). Quotes, parentheses,
commas, semicolons, colons, sentence punctuation, and whitespace are boundaries.
This prevents `швидко` from matching inside a longer or hyphen-joined word while
allowing quoted or punctuated occurrences.

**Phrase boundaries.** A multi-token literal must match the same ordered token
sequence in the case-folded NFC view and satisfy the same outer word-boundary
rule. Between phrase tokens, one or more Unicode whitespace characters match the
single separator stored in `uk_vague_terms_v1`. This is formatting tolerance
only: it does not add tokens, alter token order, lemmatize, or generate inflected
or semantically related forms. Evidence preserves the exact complete substring,
including its original whitespace and offsets.

**Overlap alternatives.** Under exact literal matching, the prompt's conceptual
example `у реальному часі`/`реальний час` is not a character-span overlap:
`реальному часі` and `реальний час` are different surface forms. Treating them
as overlapping would require forbidden morphological expansion. The actual seed
overlap is `надійно` at the start of `надійно захищені`.

| Policy | Consequence for evidence and signals | Assessment |
| --- | --- | --- |
| `ALL_MATCHES` | Keeps both the phrase and nested token, producing two evidence items and two signals for one textual construction | Maximizes traceability but predictably double-counts the actual nested seed case |
| `LONGEST_MATCH_ONLY` | Keeps the longest candidate among overlaps, but without a left-to-right rule can be underspecified for crossing or repeated candidates | Avoids the known nested duplicate but is not a complete selection algorithm |
| `LEFTMOST_LONGEST_NON_OVERLAPPING` | At the earliest start, selects the longest span; ties use stable vocabulary order; discards candidates overlapping the selected span; resumes at its end | Approved deterministic MVP policy; preserves one signal for one surface construction while keeping repeated non-overlapping occurrences |

The approved policy is `LEFTMOST_LONGEST_NON_OVERLAPPING`.
Candidate enumeration and output ordering are:

1. enumerate every exact boundary-valid candidate;
2. sort by ascending original `start_offset`, descending original span length,
   then stable `uk_vague_terms_v1` order;
3. select the first candidate, discard only candidates whose spans overlap it,
   and continue with the earliest remaining candidate; and
4. emit selected observations in ascending `start_offset` order, with separate
   evidence IDs for repeated occurrences.

The production detection rule ID for this exact matcher is `UK-VAGUE-001`.
Its accepted evidence IDs use `UK-VAGUE-001:E001`, `UK-VAGUE-001:E002`, and so
on in selected occurrence order after the policy above. The ordinal is an
engineering/provenance identifier unique within one requirement assessment;
repeated identical literals at different offsets receive separate IDs. Future
detector rules use their own production rule-ID prefix. This contract does not
implement matching or assign quality meaning to a match.

| Case | Source status and input | Approved detector output | Evidence span(s) | Approved rule family |
| --- | --- | --- | --- | --- |
| Positive/case | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система повинна ШВИДКО сформувати звіт.` | `DETECTED`; case-folded match, original uppercase evidence preserved | `[16,22)` `ШВИДКО` | `UK-VAGUE` |
| Negative boundary | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система працює надшвидко.` | `NOT_DETECTED`; approved token is embedded in a longer word | none | `UK-VAGUE` |
| Unresolved | Valid Unicode input and a functioning deterministic matcher make this detector total | Not meaningful for ordinary matching; `UNRESOLVED` is reserved for inability to construct/map the matching view, not for absence of a lexicon hit | none | `UK-VAGUE` |
| Repeated | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Швидко сформувати звіт і швидко надіслати його.` | `DETECTED`; two observations | `[0,6)` `Швидко`; `[25,31)` `швидко` | `UK-VAGUE` |
| Punctuation | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система повинна працювати «швидко», надійно.` | `DETECTED`; quotes/comma/full stop are outside the evidence | `[27,33)` `швидко`; `[36,43)` `надійно` | `UK-VAGUE` |
| Actual overlap | SOURCE-ATTESTED wording — Application example, Section 2, Table 1, R3: `Персональні та комерційні дані повинні бути надійно захищені.` | `DETECTED`; approved policy keeps the longer phrase and suppresses nested token candidate | `[44,60)` `надійно захищені`; nested `[44,51)` is not emitted | `UK-VAGUE` |

#### 7.14.9 Detection status semantics

The approved semantics refine, but do not replace, Section 7.4:

- `DETECTED`: at least one approved detector rule produced an explicit
  observation with evidence. A partial quantitative observation is `DETECTED`
  even when one or more component fields are unresolved.
- `NOT_DETECTED`: the detector completed all applicable deterministic checks on
  the valid requirement text, produced no observation, and encountered no
  candidate whose semantic status could not be decided.
- `UNRESOLVED`: no observation was accepted and at least one candidate could not
  be deterministically classified or bounded with the approved information, or
  required parser/matching processing was unavailable. It is not a low
  confidence value and does not equal zero.

The semantics permit a family to contain accepted observations while another
candidate remains unresolved. The final Python/domain representation for this
mixed state, including any diagnostic shape, is deferred to the MVP-01 data
contract. No confidence value is approved here.

An accepted observation semantically implies `DETECTED`. For total lexical
detectors such as the approved `UK-VAGUE` baseline,
`DETECTED`/`NOT_DETECTED` is derivable from the collection. This section does not
freeze an observation-level status field, a family-level wrapper, or any other
Python/domain shape. The MVP-01 data contract must choose a representation that
can preserve empty `NOT_DETECTED`, empty `UNRESOLVED`, and mixed
accepted-plus-unresolved outcomes without introducing confidence.

`NOT_DETECTED` does not mean a quality defect. `UNRESOLVED` does not mean zero,
`NOT_APPLICABLE`, or `UNKNOWN` applicability. Criterion applicability remains a
separate downstream concept.

#### 7.14.10 Finding-conversion boundary

The following one-observation-to-one-signal rule is approved for MVP v0.1:

```text
one accepted vague_term_occurrence
        ↓ FIND-U-VAGUE-001
one Finding:
    finding_id = unique within the requirement assessment
    requirement_id = enclosing requirement ID
    code = VAGUE_TERM_SIGNAL
    characteristic_id = UNAMBIGUITY
    kind = SIGNAL
    criterion_id = None
    explanation = identifies the exact approved seed literal and states that
                  it is a potential ambiguity indicator, not a confirmed defect
    evidence_refs = exactly the occurrence evidence reference(s)
    rule_id = FIND-U-VAGUE-001
```

Repeated accepted occurrences therefore create repeated independently traceable
signals. The approved longest-overlap policy prevents a nested token and phrase
from producing two signals for the same selected surface construction. No
signal is automatically converted to `QUALITY_PROBLEM`.

For `condition_context`, `expected_result`, `acceptance_criterion`,
`quantitative_constraint`, and `verification_method`, feature detection alone
produces observations and evidence only. It produces no finding. A later
characteristic rule may interpret presence, absence, applicability, sufficiency,
or interaction, but that rule belongs to the characteristic-calculation gate.
This boundary is consistent with Requirement properties, Section 2.1,
paragraph 10; Metrics system, Section 2.3, paragraphs 12-16 and 30; Static
methods, Section 3.1, paragraphs 32-34; and the approved distinction in Section
7.10: automatic observations are not automatically confirmed defects.

#### 7.14.11 Approved rule-ID convention

Rule IDs encode the feature/rule family and a stable sequence number.
They should encode language only for language-dependent lexical or grammatical
rules. They should not encode a mutable semantic version: material semantic,
applicability, or evidence-boundary changes receive a new sequence number, while
the rule registry records the approving model-spec revision.

Approved family shapes are:

```text
COND-UK-NNN
RESULT-UK-NNN
ACCEPT-UK-NNN
ACCEPT-QUANT-NNN
QUANT-NNN
QUANT-UK-NNN
VERIFY-UK-NNN
UK-VAGUE-NNN
FIND-U-VAGUE-NNN
```

`UK` denotes the Ukrainian language profile. Language-independent symbolic or
unit rules use `QUANT-NNN`; Ukrainian lexical comparators use `QUANT-UK-NNN`.
`ACCEPT-QUANT-NNN` denotes an acceptance rule whose distinguishing contract is
composition with approved quantitative observations; it does not create a new
quantitative language profile.
`NNN` is a zero-padded stable rule number and does not imply priority. Semantic
versions belong to rule-registry metadata rather than to the stable identifier.
The examples above define families only; they do not create dozens of production
IDs. Each eventual registry entry must state the immutable detector description,
feature ID, language/profile, evidence boundary, source/approval reference,
status, and superseding rule if any. Evidence uses the detector rule ID; a
finding uses the interpretation/conversion rule ID that created the finding.
`UK-VAGUE-001` remains the production allocation for the already-approved exact
Section 7.14.8 matcher. `QUANT-001` and `QUANT-UK-001` are the only quantitative
production allocations, with the immutable first-production meanings,
source-aligned evidence boundaries, profiles, and Issue #29 approval recorded
in Section 7.14.6.6. `COND-UK-001` is the only condition/context production
allocation, with the immutable first-production templates, attachment anchors,
evidence boundaries, and Issue #35 approval recorded in Section 7.14.3.1.
`RESULT-UK-001` is the only expected-result production allocation, with its
immutable normative inventory, parser-assisted subject/predicate contract,
condition separation, evidence boundary, diagnostics, and Issue #39 approval
recorded in Section 7.14.4.1. `ACCEPT-QUANT-001` is the only
acceptance-criterion production allocation, with its accepted result anchor,
quantitative containment, judgeability, clause-level deduplication, degraded
outcomes, and Issue #43 approval recorded in Section 7.14.5.1. In particular,
`ACCEPT-UK-NNN` remains an unallocated family shape for a future separately
approved non-numeric or other Ukrainian grammatical rule. `VERIFY-UK-001` is
the only verification-method production allocation, with its three approved
role constructions, candidate inventory, Evidence boundary, diagnostics, and
Issue #47 approval recorded in Section 7.14.7.1. `FIND-U-VAGUE-001` is the
only finding-conversion allocation, with the immutable one-accepted-occurrence
to one Unambiguity `SIGNAL` meaning finalized in Sections 7.14.10 and 7.16.5.
The remaining family shapes remain unallocated.

#### 7.14.12 Readiness of the targeted RQDs

Researcher approval closes the MVP seed-matching decision and partially approves
the parser-assisted and quantitative families without inventing their remaining
operational rules.

| RQD | Readiness | Reason |
| --- | --- | --- |
| `RQD-006` | `PARTIALLY_APPROVED / OPEN` | `COND-UK-001` approves the exact five-marker first-production condition subset. `RESULT-UK-001` approves the exact five-surface parser-assisted normative-modal expected-result subset, its explicit local subject and lexical predicate chain, edge-condition separation, evidence boundary, diagnostics, and outcome semantics. `ACCEPT-QUANT-001` reuses those accepted result clauses as its only required-behavior anchors and adds no parser grammar. `VERIFY-UK-001` approves exactly construction A (`перевіряється`/`перевіряються` plus an instrumental method), construction B (an approved verification label, delimiter, and named method), and construction C (`визначено` plus an immediately following named test-method phrase). General condition attachment, broader/non-modal or inherited normative force, coordinated results, general negation, implicit subjects, non-numeric acceptance grammar, general declaration/verification predicates and labels, arbitrary method noun phrases, broader method coordination, artifact/reference interpretation, imperative or implicit procedures, semantic reproducibility inference, and richer procedure-content grammar remain open; no arbitrary verb rule is allowed and actor/action/object remain deferred. |
| `RQD-007` | `APPROVED_FOR_MVP_V0.1 / CLOSED` | NFC plus Unicode `casefold()`, Unicode-aware token boundaries, Unicode-whitespace phrase separators, repeated ordering, and `LEFTMOST_LONGEST_NON_OVERLAPPING` are approved without changing the ten-entry seed. Broader vocabulary coverage is future work and does not keep this MVP decision open. |
| `RQD-008` | `PARTIALLY_APPROVED / OPEN` | The `QUANT-001`/`QUANT-UK-001` partial observations and `ACCEPT-QUANT-001` clause-level containment composition are approved without arbitrary distance thresholds. Only resolved inclusive lower/upper comparator bounds and explicit value + unit targets are judgeable for this acceptance baseline; `до` remains non-judgeable `UPPER_BOUND / UNRESOLVED`. Written-out numbers and generic ranges are outside the baseline; complex metric/context grammar, count-noun roles, and nested representation remain open. |
| `RQD-016` | `FINDING_AND_SIGNAL_CONTRACT_APPROVED / QUALITY_PROBLEM_CONVERSION_OPEN` | One accepted vague-term occurrence produces one Unambiguity `SIGNAL`; Section 7.16 finalizes the minimal Finding representation and allocates `FIND-U-VAGUE-001`. The other five families produce observations/evidence only. Every `QUALITY_PROBLEM` conversion remains open. |

`RQD-005`, `RQD-007`, and `RQD-009` are closed for MVP v0.1. Section 7.16
later keeps `RQD-020` open and non-blocking while confidence and evidence
reliability remain excluded; this approval adds no confidence, reliability,
severity, probability, risk, priority, or corrective-action field.

The later Section 7.15 approval resolves the backend and domain-representation
parts of these open items. The `COND-UK-001`, `RESULT-UK-001`,
`ACCEPT-QUANT-001`, and `VERIFY-UK-001` allocations resolve only their
first-production subsets; they do not close broader `RQD-006` grammar or
`RQD-008` complex grammar.

#### 7.14.13 Remaining researcher decisions

1. Define parser/template operationalization beyond the `COND-UK-001`
   condition subset, `RESULT-UK-001` normative-modal result subset,
   `ACCEPT-QUANT-001` quantitative composition, and `VERIFY-UK-001` three-role
   verification subset: general condition attachment, broader/non-modal or
   inherited expected-result force, coordinated results, general negation,
   implicit subjects, non-numeric acceptance criteria, general declaration and
   verification predicates/labels, arbitrary method noun phrases, broader
   method coordination, artifact/reference interpretation, imperative or
   implicit procedures, semantic reproducibility inference, and richer
   procedure-content grammar (`RQD-006`).
2. Define any approved complex metric/context grammar, count-noun roles, and
   nested load-context representation (`RQD-008`). Ambiguous linkage remains
   `UNRESOLVED`; no arbitrary distance threshold may be introduced.
3. Decide any future expansion for written-out numbers or generic range syntax.
   Both are outside the MVP v0.1 baseline unless a separately approved,
   source-attested construction is added.
4. Define the final MVP-01 Python/domain representation for
   `DetectionStatus`, including mixed accepted-plus-unresolved candidates. The
   semantics are approved, but no wrapper or confidence field is frozen here.
5. Define characteristic-calculation rules, including any conversion from a
   `SIGNAL` or another observation to `QUALITY_PROBLEM`. Detection alone may not
   perform that conversion.

This list records what Section 7.14 left open at that gate. Section 7.15 later
resolves the backend and detector-side data-representation portions of items 1
and 4. Issues #35, #39, #43, and #47 later resolve only the `COND-UK-001`,
`RESULT-UK-001`, `ACCEPT-QUANT-001`, and `VERIFY-UK-001` first-production
subsets of item 1, not its remaining general grammar or the other research
decisions.

#### 7.14.14 Downstream GitHub issue alignment

This detector-contract approval was reflected narrowly in issue descriptions
#4, #5, #6, #9, and #14. Section 7.15 subsequently approves the parser/data
boundary and aligns #2, #4, #5, #6, and #14. Issues #7 and #8 are intentionally
unchanged. No calculator issue is
unblocked by detector approval alone.

| Issue | Approved narrow alignment |
| --- | --- |
| #4 MVP-03 | Record approved `DetectionStatus` semantics and the replaceable parser-information boundary while deferring the concrete mixed-state domain representation; keep observations/evidence only and no findings |
| #5 MVP-04 | Record approved condition/result/criterion/quantitative/verification strategies, evidence boundaries, partial-observation behavior, and reference cases; `COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, and `VERIFY-UK-001` supply only their first-production subsets, while general parser operationalization and actor/action/object remain deferred |
| #6 MVP-05 | Record approved Unicode, token/phrase boundary, overlap, ordering, comparator, numeric, unit, linkage, and verification-method mechanics allocated to textual extraction, including the clause-level `ACCEPT-QUANT-001` composition |
| #7 MVP-06 | No detector-only edit is required unless its input list is clarified after approval; it remains blocked by the Completeness calculation gate |
| #8 MVP-07 | No detector-only edit is required unless its approved input observations are enumerated; it remains blocked by the Verifiability calculation gate |
| #9 MVP-08 | Add only the approved one-occurrence-to-one-`SIGNAL` conversion and overlap consequence; keep all Unambiguity scoring and `QUALITY_PROBLEM` conversion blocked |
| #14 MVP-SPEC | Record the researcher's approvals and resulting RQD statuses; keep the overall specification `DRAFT` until all required gates are approved |

#### 7.14.15 Guardrails preserved by this approval

- No application code, production regular expression, parser, test under `src/`,
  runtime dependency, or NLP-library choice is introduced.
- No `C`, `V`, or `U` calculation, score contribution, coefficient, weight,
  threshold, scale choice, or rounding rule is introduced.
- The `uk_vague_terms_v1` inventory remains exactly the ten literals approved in
  Section 7.8.
- `QUALITY_PROBLEM` is never inferred directly from lexical matching.
- `has_actor`, `has_action`, and `has_object` remain deferred from MVP v0.1.
- `RQD-005`, `RQD-007`, and `RQD-009` are closed for MVP v0.1; `RQD-006` and
  `RQD-008` remain partially approved/open; `RQD-016` is approved for its
  Finding and signal contract while every
  `QUALITY_PROBLEM` conversion remains open; and Section 7.16 later leaves
  `RQD-020` open and non-blocking while confidence and evidence reliability
  remain excluded.

### 7.15 Parser & Domain Operationalization Contract — APPROVED FOR MVP v0.1

Researcher approval on 2026-09-15 makes the parser-backend and domain
representation decisions in this section binding for MVP v0.1, with the
ParserOutcome and `RQD-006` corrections below. This section does not itself
approve concrete executable parser/template detector grammar; the later Issue
#35 approval in Section 7.14.3.1 and Issue #39 approval in Section 7.14.4.1
allocate only the narrow `COND-UK-001` and `RESULT-UK-001` subsets. Issue #43
in Section 7.14.5.1 allocates the compositional `ACCEPT-QUANT-001` subset
without adding parser grammar. Issue #47 in Section 7.14.7.1 allocates the
parser-required `VERIFY-UK-001` constructions without changing the neutral
parser contract. None of these approvals authorizes application
implementation in its contract-only research pass or changes the overall
specification from `DRAFT`. They
introduce no characteristic formula, score, weight, threshold, rounding rule,
new quality criterion, automatic requirement-type classifier, or confidence
value.

This approval resolves two representation gates left by Section 7.14:

1. select a versioned Ukrainian parser package that remains replaceable behind
   a parser-neutral adapter; and
2. define the minimum typed observation/outcome structures needed by MVP-01 so
   `DETECTED`, `NOT_DETECTED`, `UNRESOLVED`, partial quantitative observations,
   and mixed accepted-plus-unresolved results remain explicit.

The selected parser is replaceable engineering infrastructure of feature
extraction, not part of the scientific model. Parser output is fallible
linguistic annotation input. A dependency arc,
lemma, POS tag, or sentence boundary is never by itself a feature observation,
finding, applicability decision, or quality result.

#### 7.15.1 Evaluation scope and evidence classification

The candidate review used official project and model documentation current on
2026-09-15:

- [spaCy Ukrainian pipelines](https://spacy.io/models/uk),
  [spaCy token API](https://spacy.io/api/token), and the official
  [`uk_core_news_sm` 3.8.0 metadata](https://raw.githubusercontent.com/explosion/spacy-models/master/meta/uk_core_news_sm-3.8.0.json);
- the official [spaCy 3.8.16 release](https://github.com/explosion/spaCy/releases/tag/v3.8.16);
- [Stanza pipeline documentation](https://stanfordnlp.github.io/stanza/pipeline.html),
  [data-object and offset documentation](https://stanfordnlp.github.io/stanza/data_objects.html),
  [model download/offline documentation](https://stanfordnlp.github.io/stanza/download_models.html),
  and the official
  [1.14.0 resource manifest](https://raw.githubusercontent.com/stanfordnlp/stanza-resources/main/resources_1.14.0.json);
- the official [Stanza 1.14.0 release](https://github.com/stanfordnlp/stanza/releases/tag/v1.14.0)
  and [Stanza language-pack licensing note](https://stanfordnlp.github.io/stanza/performance.html);
- the upstream
  [UD Ukrainian-IU README](https://raw.githubusercontent.com/UniversalDependencies/UD_Ukrainian-IU/master/README.md)
  and [license](https://raw.githubusercontent.com/UniversalDependencies/UD_Ukrainian-IU/master/LICENSE.txt)
  for training-corpus scope and licensing context.

The dissertation examples reviewed for this gate were the source-attested
requirements and revisions already transcribed in Section 7.14.1, especially
`R1'`-`R5'` and the negative case `R6`. They are research traceability examples,
not a gold parser corpus. Two additional strings were used only to probe an
apostrophe, coordination, and an ordinary finite verb. They are labelled
`SYNTHETIC TECHNICAL CASE — NOT DISSERTATION EVIDENCE` and carry no scientific
authority.

No labelled requirements-domain Ukrainian parser benchmark was found in the
repository or created by this evaluation. Consequently, the candidate
comparison supports an engineering selection only. It does not establish
parser accuracy, detector recall, detector precision, or scientific validity.

#### 7.15.2 Minimum annotation capability

An MVP parser backend must expose all of the following through the neutral
contract:

| Capability | Required use |
| --- | --- |
| deterministic tokenization with source offsets | construct exact source-span evidence without replacing `Requirement.text` |
| sentence boundaries | bound sentence-local dependency identifiers and provide a conservative structural scope |
| lemma | support only rules whose approved definition explicitly calls for a lemma; it does not expand `uk_vague_terms_v1` |
| Universal POS (`UPOS`) | distinguish approved grammatical candidates without library-specific tag objects |
| morphology | preserve UD-style key/value features needed by an approved rule |
| dependency head and relation | support conservative clause and attachment checks required by Section 7.14 |

Named entities, vectors/embeddings, sentiment, parser probabilities, beam
scores, model tensors, and library-native document/token objects are excluded
from the MVP boundary. Clause observations remain detector decisions; the
parser contract does not assert a universal clause segmentation.

#### 7.15.3 Candidate comparison

The minimum credible candidates are the current official Ukrainian pipelines
from spaCy and Stanza. No third candidate was added because no additional
library was needed to exercise the required annotation contract, and adding an
unverified option would not improve this gate.

| Dimension | spaCy `uk_core_news_sm` 3.8.0 | Stanza 1.14.0 Ukrainian `iu` package |
| --- | --- | --- |
| Ukrainian tokenization | Yes | Yes, with `tokenize` and `mwt` processors |
| sentence boundaries | Yes (`parser`/`senter`) | Yes (`tokenize`) |
| lemma | Yes (`lemmatizer`) | Yes (`lemma`, default `iu_nocharlm`) |
| UPOS and morphology | Yes (`morphologizer`; `Token.pos_` and `Token.morph`) | Yes (`pos`, default `iu_charlm`; `Word.upos` and `Word.feats`) |
| dependencies | Yes (`parser`; head and dependency relation) | Yes (`depparse`, default `iu_charlm`; head and relation) |
| source offsets | `Token.idx` plus token length; adapter conversion is straightforward | documented `start_char`/`end_char`; adapter must map syntactic words conservatively |
| CPU/offline operation | official metadata says CPU-optimized; installed Python package loads without network access | supports `use_gpu=False` and offline loading after an explicit model download |
| version identity | model is a normal versioned Python package compatible with spaCy `>=3.8.0,<3.9.0` | library and resource manifest are versioned; individual processor artifacts have manifest identities/checksums |
| reproducible acquisition | exact model wheel and SHA-256 are published in official metadata | resource manifest supplies package choices and MD5 values; deployment must freeze the complete processor set and resource manifest |
| published model size | 14 MB package metadata, with no word vectors | no single comparable package-size claim; default `iu` resolves several processor, pretrain, and character-language-model files |
| observed local model footprint | 43,136,050 bytes in the isolated Windows environment | 333,363,122 bytes for the downloaded resource directory in the same environment |
| observed one-process load | 0.707 s in one isolated run | 2.671 s in the same isolated run |
| integration surface | spaCy plus model package and the model's declared Ukrainian morphology dependencies | Stanza plus PyTorch and a separately managed model directory |
| software license | [MIT](https://raw.githubusercontent.com/explosion/spaCy/master/LICENSE) | [Apache-2.0](https://raw.githubusercontent.com/stanfordnlp/stanza/main/LICENSE) |
| model/data licensing signal | selected model metadata declares MIT and names the MIT-licensed `Ukr-Synth` source; transitive dependency notices still require release review | Stanza describes language-pack licensing only to the extent Stanford owns rights; upstream UD Ukrainian-IU declares CC BY-NC-SA 4.0, so distribution/commercial use requires project/legal review |
| training-domain signal | official model page labels the pipeline as news written text; metadata identifies `Ukr-Synth`; neither is a requirements corpus | UD Ukrainian-IU reports mixed web/news/legal/fiction and other genres; it is not a requirements corpus |
| current maintenance signal | official spaCy releases and 3.8-compatible Ukrainian model metadata were current when reviewed | Stanza 1.14.0 and resource manifest 1.14.0 were current when reviewed |

The local footprint and timing observations are `INDICATIVE ONLY — NOT A
BENCHMARK`. They are single-machine engineering observations with no warm-up,
statistical analysis, service-level threshold, or quality interpretation.

#### 7.15.4 Narrow empirical spike

An isolated temporary environment evaluated spaCy 3.8.16 with
`uk_core_news_sm` 3.8.0 and Stanza 1.14.0 with resource manifest 1.14.0 and the
default Ukrainian `iu` syntax processors. Both were forced to CPU operation and
offline inference after explicit installation/download. No package, model,
lockfile, source file, or test was added to the repository.

Observed behavior on six source-attested examples and two clearly labelled
synthetic technical cases:

- both candidates returned exact source-offset round trips for every emitted
  token in all eight strings;
- both preserved Ukrainian apostrophe text and produced UPOS, morphology,
  lemmas, sentence boundaries, heads, and dependency relations;
- both kept every tested semicolon-coordinated requirement on one sentence,
  demonstrating that detector clause logic cannot be delegated to sentence
  segmentation alone;
- spaCy kept decimal-comma `99,9` as one token, while Stanza emitted `99`, `,`,
  and `9`; therefore the approved quantitative lexical baseline must operate on
  source spans and may not assume that a numeric value is one parser token;
- spaCy kept `1.3` and `2.0` intact but split `tenant-ами`; Stanza split version
  numbers around the period but kept `tenant-ами`; therefore technical-token
  shapes must not become undocumented semantic rules;
- dependency attachments differed in coordinated examples even where surface
  tokens matched. The accepted/unresolved outcome contract is therefore
  required; a backend parse must not be treated as unquestionable truth.

Across the eight strings, the single-run average processing observations were
approximately 6.2 ms for spaCy and 124.3 ms for Stanza. These values are recorded
only to confirm practical local CPU execution and relative integration cost in
that environment. They are not acceptance thresholds, performance promises, or
scientific comparison results.

#### 7.15.5 Engineering recommendation

**SELECTED ENGINEERING BACKEND FOR MVP v0.1:** `spacy==3.8.16` with the official
`uk_core_news_sm` 3.8.0 package, loaded with `ner` disabled and the tokenizer,
morphologizer, parser/sentence-boundary support, attribute ruler, and lemmatizer
retained.

This recommendation is based on the following bounded engineering reasons:

1. it supplies every minimum annotation and exact source offset required by the
   neutral contract;
2. the selected package is CPU-oriented, has no vectors, and had a materially
   smaller observed model footprint and integration stack in the narrow spike;
3. the library/model compatibility range, package version, checksum, source,
   and model license are explicit in official metadata; and
4. the empirical cases exposed no offset failure that would prevent exact
   Evidence construction.

The selection is subject to validation on the approved reference cases and
does **not** claim superior linguistic accuracy. Both
candidates have a domain mismatch, and neither was evaluated against a labelled
Ukrainian requirements corpus. Stanza remains a viable replacement if later
validation or deployment constraints favour it, provided an adapter satisfies
the same invariants and its model/data licensing is approved.
No spaCy `Doc`, `Token`, `Span`, or other native object may cross the NLP adapter
boundary into domain models or calculators.

Approval here does not add a runtime dependency or authorize a parser adapter
implementation outside its allocated implementation issue. When an issue
authorizes integration, reproducibility must
freeze the exact spaCy and model package versions and verify the official model
wheel SHA-256. Processing must never download a model implicitly. A missing or
incompatible model is a structured parser failure, not a reason to switch model
versions silently.

#### 7.15.6 Parser-neutral contract

The approved contract below is conceptual and language/library neutral. Names show the
minimum typed fields; they do not prescribe a particular Python framework.

```text
ParserMetadata
  provider_id: str
  library_version: str
  model_package: str
  model_version: str
  language: str

MorphFeature
  name: str
  values: tuple[str, ...]

SentenceAnnotation
  sentence_id: int
  start_offset: int
  end_offset: int

TokenAnnotation
  token_id: int
  sentence_id: int
  text: str
  start_offset: int
  end_offset: int
  lemma: str | None
  upos: str | None
  morphology: tuple[MorphFeature, ...]
  head_token_id: int | None
  dependency_relation: str | None

ParsedRequirement
  requirement_id: str
  text: str
  sentences: tuple[SentenceAnnotation, ...]
  tokens: tuple[TokenAnnotation, ...]
  parser: ParserMetadata

ParserDiagnostic
  code: ParserDiagnosticCode
  explanation: str

ParserOutcome
  parsed_requirement: ParsedRequirement | None
  diagnostics: tuple[ParserDiagnostic, ...]
```

`ParserDiagnosticCode` has the approved minimum infrastructure values
`PARSER_UNAVAILABLE`, `PARSER_PROCESSING_FAILED`,
`ANNOTATION_INCOMPLETE`, and `OFFSET_INVARIANT_FAILED`. These values describe
processing, not requirement quality. They carry no severity, probability,
confidence, numeric reliability, or score. Their code-to-outcome rules are:

| Code | `parsed_requirement` | Meaning |
| --- | --- | --- |
| `PARSER_UNAVAILABLE` | `None` | Required parser/model cannot be loaded |
| `PARSER_PROCESSING_FAILED` | `None` | Processing cannot return a valid result |
| `OFFSET_INVARIANT_FAILED` | `None` | Source-span invariant cannot be satisfied |
| `ANNOTATION_INCOMPLETE` | may be present | Source-aligned annotations may be retained, but a required annotation is missing; consuming detectors become `INCOMPLETE` |

The first three conditions prevent delivery of a parsed result. They are
defined through this code-to-outcome rule, not an untyped diagnostic-severity
or runtime `fatal` property. `ANNOTATION_INCOMPLETE` does not erase otherwise
valid parsed annotations. If it coexists with a result, each detector that
requires the missing annotation records a `DetectionDiagnostic` and sets
`processing_status = INCOMPLETE`; unrelated complete checks may continue.

The following invariants are mandatory:

1. `ParsedRequirement.requirement_id` equals the input `Requirement.id`, and
   `ParsedRequirement.text` is value-identical to the already-trimmed
   `Requirement.text`. The parser may not normalize, rewrite, or become the
   source of record for requirement text.
2. All sentence and token offsets use the Section 7.2 convention: zero-based
   Unicode code-point indices, start inclusive and end exclusive, against that
   exact `Requirement.text`.
3. Every emitted token satisfies
   `Requirement.text[start_offset:end_offset] == text`. Provider-native byte or
   UTF-16 offsets must be converted and validated by the adapter.
4. Token IDs are zero-based, unique, and in source order within one requirement.
   Sentence IDs are zero-based and in source order.
5. A non-root `head_token_id` refers to a token in the same sentence. A root has
   `head_token_id = None`; provider-native root indices never cross the boundary.
6. `upos` and `dependency_relation` use UD-compatible string labels.
   Morphological features are immutable tuples sorted by feature name and value
   for deterministic equality/serialization. Provider-native objects and XPOS
   tagsets do not cross the boundary.
7. Empty or missing annotations required by an approved detector produce an
   `ANNOTATION_INCOMPLETE` diagnostic and an incomplete consuming detector
   outcome. A source-aligned `ParsedRequirement` may still be present. The
   missing annotation is not guessed from another field.
8. If a backend multi-word-token analysis cannot be mapped to exact source
   spans satisfying invariant 3, the adapter returns
   `OFFSET_INVARIANT_FAILED`; it must not fabricate offsets or evidence.
9. A fully annotated parse has `parsed_requirement` present and no diagnostic.
   An annotation-incomplete parse may have it present with
   `ANNOTATION_INCOMPLETE`. Each of the three result-preventing codes above
   requires `parsed_requirement = None`. An absent result has at least one
   diagnostic; it never silently becomes a complete scan.
10. Parser annotations do not contain `Evidence`, observations, findings,
    applicability, or quality values. Only approved detectors may convert
    source-aligned annotations into feature observations and exact Evidence.

The parser adapter stays entirely inside the feature-extraction boundary. It
accepts one domain `Requirement` and returns `ParserOutcome`. The public
`FeatureExtractor` contract is `Requirement -> RequirementExtractionResult`;
calculators never import the adapter, spaCy, Stanza, or parser-neutral annotation
types.

#### 7.15.7 Detection-outcome representation

Two representation strategies were considered:

| Strategy | Benefit | Defect |
| --- | --- | --- |
| store one mutable/explicit `DetectionStatus` next to observations | superficially direct | permits contradictions such as `NOT_DETECTED` with observations and cannot alone express accepted observations plus unresolved candidates |
| store observations, processing completeness, and structured diagnostics; derive `DetectionStatus` | represents all four required cases and prevents divergent stored state | callers must use one specified derivation rule |

**Approved strategy:** derive `DetectionStatus` from an immutable generic
outcome wrapper:

```text
DetectionProcessingStatus = COMPLETE | INCOMPLETE

DetectionDiagnostic
  code: str
  explanation: str
  rule_id: str
  candidate_span: DiagnosticSpan | None

DiagnosticSpan
  text: str
  start_offset: int
  end_offset: int

FeatureDetectionOutcome[T]
  feature_id: FeatureId
  observations: tuple[T, ...]
  processing_status: DetectionProcessingStatus
  diagnostics: tuple[DetectionDiagnostic, ...]
```

The derived status is exactly:

```text
if observations is not empty:
    DetectionStatus = DETECTED
else if processing_status == COMPLETE:
    DetectionStatus = NOT_DETECTED
else:
    DetectionStatus = UNRESOLVED
```

`processing_status = INCOMPLETE` requires at least one diagnostic;
`processing_status = COMPLETE` has none. Diagnostics
record why processing was incomplete; they are not accepted Evidence and do not
create a finding. A diagnostic candidate span follows the same Unicode offset
convention and must round-trip to its exact text. Diagnostic codes must be
stable and rule-specific when implemented; this draft does not invent dozens of
production codes. `DiagnosticSpan` is distinct from scientific `Evidence`:
an unresolved candidate that did not become an accepted observation does not
enter the accepted Evidence collection merely for diagnostic convenience.
`DetectionDiagnostic` is neither a Finding nor `QUALITY_PROBLEM`, quality
evidence, confidence, severity, or a score input by itself.

This single structure represents the required cases without null overloading:

| Case | `observations` | processing | derived status | diagnostics |
| --- | --- | --- | --- | --- |
| A — accepted detections only | non-empty | `COMPLETE` | `DETECTED` | empty |
| B — no accepted detection after complete processing | empty | `COMPLETE` | `NOT_DETECTED` | empty |
| C — unresolved only | empty | `INCOMPLETE` | `UNRESOLVED` | non-empty |
| D — accepted observations plus unresolved candidates | non-empty | `INCOMPLETE` | `DETECTED` | non-empty; mixed state remains visible |

The approved `RequirementFeatures` shape contains exactly six typed
`FeatureDetectionOutcome` fields,
one per approved feature family. The existing notation `condition_contexts[]`,
`expected_results[]`, `acceptance_criteria[]`,
`quantitative_constraints[]`, `verification_methods[]`, and
`vague_term_occurrences[]` refers to each corresponding wrapper's
`observations` tuple. This adds processing metadata, not a seventh feature
family. Every collection is immutable and ordered by its earliest referenced
Evidence offset, with the already-approved family-specific tie rules applied.

`DetectionStatus` remains entirely separate from
`CriterionApplicability = APPLICABLE | NOT_APPLICABLE | UNKNOWN`. Neither enum
may be converted into the other. In particular, parser failure is not
`NOT_APPLICABLE`, and `UNKNOWN` applicability is not an unresolved detector
candidate.

#### 7.15.8 Parser failure and degraded operation

Parser availability is not allowed to turn missing analysis into false
certainty:

- detector families or subrules that do not consume parser output continue
  deterministically from the exact source text;
- a parser-required family returns `INCOMPLETE` with a diagnostic when parsing
  is unavailable, fails, violates offsets, or omits a required annotation;
- a parser-optional family may preserve accepted lexical observations and also
  return `INCOMPLETE` diagnostics for candidates whose approved attachment check
  could not be completed;
- `NOT_DETECTED` is permitted only when every applicable approved check for that
  family completed and produced no observation;
- downstream calculators and aggregators must not convert parser diagnostics,
  `UNRESOLVED`, missing observations, or incomplete processing into zero or a
  `QUALITY_PROBLEM`. Section 7.16 later resolves the required-input
  characteristic case as assessment `UNKNOWN` with no value; specification-
  level aggregation propagation is now approved under `AGG-MVP-001`
  (`RQD-012`, `RQD-022`, Section 12); general insufficient-evidence beyond
  the approved per-characteristic and aggregation rules remains open.

The minimum diagnostic explains the affected feature family, stable detector
rule, machine-readable reason code, human-readable reason, and exact candidate
span when one exists. Raw exceptions, model tensors, and stack traces remain in
technical logging and do not enter the domain outcome.

#### 7.15.9 Stable observation shapes

The four simple span-based families use the approved minimal core:

```text
FeatureObservation
  feature_id: FeatureId
  evidence_refs: tuple[str, ...]
```

This type is sufficient for `condition_context`, `expected_result`,
`acceptance_criterion`, and `verification_method` because their approved MVP
meaning is carried by the feature ID, detector rule, and exact referenced
Evidence. It must not grow parser tags, confidence, or duplicated source text.

Vague-term occurrences use the approved small typed specialization:

```text
VagueTermOccurrence
  feature_id: VAGUE_TERM_OCCURRENCE
  vocabulary_id: str
  matched_literal: str
  evidence_refs: tuple[str, ...]
```

For MVP v0.1, `vocabulary_id` is `uk_vague_terms_v1` and `matched_literal` is
one of its ten exact canonical entries. The referenced Evidence, not
`matched_literal`, preserves the original case, whitespace, punctuation, and
offsets. The matcher remains exactly as approved in Section 7.14.8; parser
lemmas do not expand it and `RQD-007` remains closed.

#### 7.15.10 Quantitative-constraint representation

The approved linked quantitative observation remains partial and evidence-first:

```text
QuantitativeComponentName =
  METRIC | COMPARATOR | VALUE | UNIT | CONTEXT

ComparatorLabel =
  LESS_THAN_OR_EQUAL | GREATER_THAN_OR_EQUAL |
  NOT_LESS_FREQUENT | UPPER_BOUND

BoundaryInclusivity = INCLUSIVE | UNRESOLVED

UnitLabel = SECOND | MINUTE | PERCENT

TextComponent
  evidence_refs: tuple[str, ...]

ComparatorComponent
  label: ComparatorLabel
  inclusivity: BoundaryInclusivity | None
  evidence_refs: tuple[str, ...]

NumericValueComponent
  decimal_value: Decimal
  evidence_refs: tuple[str, ...]

UnitComponent
  label: UnitLabel
  evidence_refs: tuple[str, ...]

QuantitativeConstraintObservation
  feature_id: QUANTITATIVE_CONSTRAINT
  metric: TextComponent | None
  comparator: ComparatorComponent | None
  value: NumericValueComponent | None
  unit: UnitComponent | None
  context: TextComponent | None
  unresolved_components: tuple[QuantitativeComponentName, ...]
  evidence_refs: tuple[str, ...]
```

Component rules are:

1. Every populated component references the exact Evidence that justified it.
   The top-level `evidence_refs` is the stable, de-duplicated, source-ordered
   union of all accepted component evidence. Original spellings such as `с`,
   `хв`, `секунд`, `%`, or `99,9` live only in Evidence; normalized labels and
   `Decimal` values never replace raw text.
2. Decimal-comma text is parsed deterministically to `Decimal` only after its
   exact raw span is preserved. Binary floating point, unit conversion,
   implicit scaling, and rounding are prohibited.
3. `LESS_THAN_OR_EQUAL` and `GREATER_THAN_OR_EQUAL` carry
   `inclusivity = INCLUSIVE`. Approved Ukrainian `до` carries
   `label = UPPER_BOUND` and `inclusivity = UNRESOLVED`; it is never normalized
   to `LESS_THAN_OR_EQUAL`. `NOT_LESS_FREQUENT` has
   `inclusivity = None` because the approved form expresses frequency rather
   than a boundary-inclusion decision.
4. `SECOND`, `MINUTE`, and `PERCENT` are labels for the approved source forms,
   not a unit ontology. No conversion relation is implied.
5. A component that could not be resolved is `None` and is named in
   `unresolved_components`. A `None` component not named there was not
   explicitly expressed in the accepted partial observation. A populated
   component cannot also be listed as unresolved.
6. The observation is valid when at least the approved anchor components are
   linked under Section 7.14.6. It need not contain all five components. The
   first-production baseline in Section 7.14.6.6 does not infer `metric` or
   `context`: each is `None` and is not automatically listed in
   `unresolved_components` merely because it was not part of the accepted
   comparator/value/unit anchor. One contiguous anchor Evidence may support
   every populated baseline component it explicitly contains, without
   component-specific duplicate Evidence.
7. Written-out numbers, generic ranges, complex count-noun role inference,
   inferred metrics, and nested load-context structures remain outside this
   representation gate. They remain open/deferred under `RQD-008` rather than
   being guessed.

#### 7.15.11 Reproducibility, licensing, and distribution policy

When an allocated implementation issue later authorizes parser integration,
it must follow this approved policy:

1. pin `spacy==3.8.16` and `uk_core_news_sm==3.8.0` in the implementation
   dependency mechanism authorized by its issue;
2. verify the official model wheel SHA-256
   `d20adb50b42c0dcfdedf4994dabcb96789a64983a9ab560d0c6c38a59e8efb58`
   during controlled acquisition and record the model identity in
   `ParserMetadata`;
3. install models as explicit deployment artifacts; do not auto-download,
   auto-upgrade, or silently fall back during requirement processing;
4. keep the binary model and download cache out of the source repository unless
   a separately reviewed distribution decision explicitly vendors them;
5. include the spaCy/model/transitive dependency license notices required by
   the chosen distribution mode and perform a release-time dependency-license
   inventory. This technical review is not legal advice;
6. treat any future model or parser upgrade as a controlled change requiring
   the same source-span validation cases, rule-registry compatibility review,
   and explicit approval when observed detector behavior changes; and
7. permit a replacement backend only through the adapter contract and the same
   invariants. Calculators and domain quality profiles must remain unchanged.

The non-selected Stanza option must not be adopted merely by changing a package
name. Its frozen processor/resource set, artifact checksums, PyTorch footprint,
offline packaging, and the upstream Ukrainian model/data licensing implications
must first be approved for the target distribution context.

#### 7.15.12 RQD status after this approval

The researcher approves the following narrow subdecisions. None closes an
overall RQD whose remaining research rules are still open:

| RQD | Status after approval | Approved portion and remaining boundary |
| --- | --- | --- |
| `RQD-006` | `PARTIALLY_APPROVED / OPEN` | Backend and parser-neutral operationalization are approved. Issue #35 allocates the deterministic `COND-UK-001` condition subset, Issue #39 allocates the deterministic `RESULT-UK-001` normative-modal expected-result subset, Issue #43 composes accepted result clauses into `ACCEPT-QUANT-001` without new parser grammar, and Issue #47 allocates exactly the three `VERIFY-UK-001` constructions: A (`перевіряється`/`перевіряються` plus instrumental method), B (approved verification label, delimiter, and named method), and C (`визначено` plus an immediately following named test-method phrase). General condition attachment, broader/non-modal or inherited normative force, coordinated results, general negation, implicit subjects, non-numeric acceptance criteria, general declaration/verification predicates and labels, arbitrary method noun phrases, broader method coordination, artifact/reference interpretation, imperative or implicit procedures, semantic reproducibility inference, and richer procedure-content grammar remain open. Selecting spaCy does not define those remaining scientific detector rules; actor/action/object remain deferred and no “any verb” fallback is allowed. |
| `RQD-008` | `PARTIALLY APPROVED / OPEN` | Quantitative data representation, conservative baseline, Issue #29 first-production provenance/precedence/diagnostic contract, Issue #32 matching-view and protected deferred-frequency exclusion, and Issue #43 result-span containment and judgeability for `ACCEPT-QUANT-001` are approved. Complex metric/context grammar, count-noun roles, nested-context representation, written-out numbers, generic ranges, and future accepted `не рідше` production grammar remain open/deferred. |
| `RQD-012` | `PARTIALLY_APPROVED` at the time of this decision; detector-side representation and required-input characteristic propagation resolved here, specification-level aggregation propagation later `APPROVED_FOR_MVP_V0.1` via `AGG-MVP-001` (Section 12) | The four detection cases and mixed state have stable data representation. Section 7.16 later requires assessment `UNKNOWN` with no value when a required input is unresolved and preserves accepted data in mixed outcomes. General insufficient-evidence and characteristic applicability beyond the approved per-characteristic and aggregation rules remain open. |
| `RQD-020` | `OPEN / UNRESOLVED — NON-BLOCKING WHILE EXCLUDED` | No confidence or evidence-reliability value or field is approved for the current MVP characteristic or Finding contract. Exclusion does not resolve whether such metadata belongs in MVP; proposing inclusion makes this decision blocking and requires a separate scientific contract. |

#### 7.15.13 Downstream issue impact and approved narrow alignment

The researcher authorizes narrow alignment of the five named GitHub issues.
Their implementation scope remains limited as follows:

| Issue | Impact | Proposed description/acceptance update |
| --- | --- | --- |
| #2 MVP-01 | the approved immutable domain/data-contract subset is safe to start after this PR is merged | implement six typed outcome wrappers, parser-neutral data/result structures, typed observations and invariants; retain calculation and propagation blockers |
| #4 MVP-03 | record the selected default behind a parser-neutral, replaceable boundary | use `Requirement -> RequirementExtractionResult` with unchanged `result.features`; no spaCy object crosses the adapter; record result-preventing versus annotation-incomplete behavior; adapter implementation requires allocation by its issue |
| #5 MVP-04 | structural extraction still has an open general grammar gate | Issues #35, #39, #43, and #47 allocate only `COND-UK-001`, `RESULT-UK-001`, compositional `ACCEPT-QUANT-001`, and the three `VERIFY-UK-001` constructions; general condition/result/method and non-numeric criterion grammar plus complex `RQD-008` grammar remain open, while actor/action/object stay deferred |
| #6 MVP-05 | textual extraction still has an open grammar gate | keep source-span quantitative baseline independent of parser token boundaries and vague-term matching unchanged; Issues #43 and #47 authorize only the contracts for future `ACCEPT-QUANT-001` composition and `VERIFY-UK-001` verification-role detection, while broader grammar and new vocabulary remain unauthorized |
| #14 MVP-SPEC | remain open with overall `DRAFT` status | record this section's approval and only the affected RQD/traceability updates; characteristic formulas, propagation, and rounding remain unresolved |

After this PR is merged, MVP-01 may implement only the approved immutable
domain/data contracts. This approval does not authorize characteristic
calculators, C/V/U formulas, aggregation, a parser adapter outside its allocated
implementation issue, complex detector grammar, or `QUALITY_PROBLEM`
conversion. MVP-04 and MVP-05 are not fully unblocked.

#### 7.15.14 Decision record and guardrails

**Evaluation owner:** Codex technical evaluation.

**Researcher decision, 2026-09-15:** approve (a) `spacy==3.8.16` and
`uk_core_news_sm==3.8.0` as `SELECTED ENGINEERING BACKEND FOR MVP v0.1`, (b)
the parser-neutral contract with the code-to-outcome correction in Section
7.15.6, (c) the derived immutable detection-outcome wrapper and separate
DiagnosticSpan, and (d) the minimal typed observation and quantitative shapes.
`RQD-006` stays `PARTIALLY APPROVED / OPEN` for executable scientific grammar
beyond the allocated `COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, and
`VERIFY-UK-001` subsets;
the overall model specification stays `DRAFT`.

Guardrails preserved:

- the six approved feature families and all Section 7.14 detection semantics
  remain unchanged;
- raw trimmed text, punctuation, exact Evidence, and Unicode code-point offsets
  remain authoritative;
- `uk_vague_terms_v1` remains unchanged and `RQD-007` remains closed;
- no parser output directly creates a finding, `QUALITY_PROBLEM`,
  applicability value, score, penalty, or reward;
- no arbitrary proximity threshold, new comparator, new unit alias, inferred
  metric, written-number rule, or range grammar is introduced;
- `has_actor`, `has_action`, and `has_object` remain deferred from MVP v0.1;
- `DetectionStatus` remains separate from `CriterionApplicability`;
- no confidence, reliability, severity, probability, risk, priority, or
  corrective-action field is added; and
- no application code, test, package declaration, or runtime dependency is
  changed by this research gate.

### 7.16 Requirement Characteristic Assessment Contract — PARTIALLY APPROVED FOR MVP v0.1

This section is the authoritative scientific contract for the boundary after
feature extraction and before specification-level aggregation. It approves the
smallest result and provenance structures that can be executed without
inventing a characteristic formula. It does **not** approve production
calculator code or a numeric calculation for Completeness, Verifiability, or
Unambiguity.

The layer receives an immutable `RequirementExtractionResult` as domain data:

```text
RequirementExtractionResult
    ├── requirement
    ├── features: six FeatureDetectionOutcome values
    └── evidence: accepted Evidence registry
        ↓
CompletenessCalculator
VerifiabilityCalculator
UnambiguityCalculator
        ↓
CharacteristicAssessment(COMPLETENESS)
CharacteristicAssessment(VERIFIABILITY)
CharacteristicAssessment(UNAMBIGUITY)
        ↓
RequirementQualityProfile(C, V, U)
```

This input choice does not couple a calculator to `FeatureExtractor`: the
result, requirement, features, Evidence, observations, outcomes, and
diagnostics are domain values and can be constructed directly in calculator
tests. A calculator must not import a concrete extractor, parser, NLP library,
reader, CLI, reporter, or file-I/O component.

The decision status at this gate is:

| Decision | Status | Consequence |
| --- | --- | --- |
| Exactly three MVP characteristic identifiers | `APPROVED` | Only `COMPLETENESS`, `VERIFIABILITY`, and `UNAMBIGUITY` may occur in a requirement-level MVP profile. |
| Minimal `CharacteristicAssessment` envelope and state/value invariants | `APPROVED` | A value can be withheld explicitly without substituting zero. |
| `CriterionApplicability` state meanings and conservative default | `APPROVED` | Applicability is never inferred from detection; without an approved rule it is `UNKNOWN`. |
| Minimal `Finding` contract and `SIGNAL`/`QUALITY_PROBLEM` distinction | `APPROVED` | Findings remain downstream interpretations and retain requirement/rule/evidence provenance. |
| One vague-term occurrence to one Unambiguity signal | `APPROVED` | `FIND-U-VAGUE-001` may execute without asserting ambiguity or a score. |
| Absence-finding provenance and required-input `UNRESOLVED` propagation | `APPROVED` | No fake Evidence span and no numeric substitution are permitted. |
| Per-criterion applicability allocations for the current Completeness and Verifiability candidates | `RESOLVED FOR CALCULATION PURPOSES` | For Completeness, `CALC-C-MVP-001` approves an explicit MVP simplification: condition/context, expected result, and acceptance criterion are each `APPLICABLE` for every supported input requirement. For Verifiability, its three evidence families are approved as alternative, non-mandatory evidence paths rather than individually mandatory criteria, so no per-family mandatory-applicability rule was needed; the Verifiability characteristic itself is applicable to every supported requirement. |
| Completeness numeric rule | `APPROVED_FOR_MVP_V0.1` | `CALC-C-MVP-001` produces `C_i` in `{0, 1/3, 2/3, 1}` (Section 8). |
| Verifiability numeric rule | `APPROVED_FOR_MVP_V0.1` | `CALC-V-MVP-001` produces `V_i` in `{0, 1/2, 1}` (Section 9). |
| Unambiguity confirmation and numeric rule | `PARTIALLY APPROVED_FOR_MVP_V0.1` | `CALC-U-MVP-001` produces the automated `U_i` in `{1/2, 1}` (Section 10). Confirmed material ambiguity and `U_i = 0` remain `BLOCKED — FUTURE RESEARCHER DECISION`. |
| Specification aggregation with `UNKNOWN`/missing values | `APPROVED_FOR_MVP_V0.1` (downstream of this contract) | This contract did not finalize file-level aggregation itself; `AGG-MVP-001` (Section 12) has since done so: `UNKNOWN` values are excluded from the mean and tracked separately, never treated as zero. |

#### 7.16.1 Characteristic identifiers

The executable identifier set is exactly:

```text
CharacteristicId:
    COMPLETENESS
    VERIFIABILITY
    UNAMBIGUITY
```

The identifiers name requirement-quality properties of the information
artifact. They do not name ISO product-quality characteristics. Consistency,
Traceability, Maintainability, specification coverage, and all product-quality
characteristics remain outside the per-requirement MVP profile.

#### 7.16.2 Minimal characteristic result

The approved conceptual representation is:

```text
CharacteristicAssessmentState:
    COMPUTED
    NOT_APPLICABLE
    UNKNOWN

CharacteristicAssessment:
    characteristic_id: CharacteristicId
    state: CharacteristicAssessmentState
    value: Fraction | None
    assessment_rule_id: str | None
    findings: tuple[Finding, ...]
    explanation: str
```

`value: Fraction | None` is the approved MVP v0.1 implementation-facing
representation of the abstract `a_ij ∈ [0,1]` range from Section 2.1, using
Python standard-library `fractions.Fraction` (Section 13). This is the only
representation decision this contract makes; it introduces no new wrapper
type, alias, or serialization contract.

| Field | Scientific meaning | Allowed values | Required? | Derivation source |
| --- | --- | --- | --- | --- |
| `characteristic_id` | Identifies which independent requirement property is being assessed | Exactly the three values in Section 7.16.1 | Yes | Requirement properties, Section 2.1; approved MVP profile `A_i = (C_i, V_i, U_i)` |
| `state` | Distinguishes an actually calculated value from non-applicability and scientifically unavailable assessment | `COMPUTED`, `NOT_APPLICABLE`, `UNKNOWN` | Yes | Metrics system, Section 2.3, paragraphs 16 and 39-42; the prohibition on zero substitution; approved applicability/missing distinction |
| `value` | The individual property assessment when, and only when, an approved property rule computed it | `Fraction` in `[0,1]` or `None` | Yes as a field; nullable by state | Requirement properties, Section 2.1, `a_ij ∈ [0,1]`; Section 13 now approves `fractions.Fraction` as the concrete MVP v0.1 numeric type for this per-requirement value |
| `assessment_rule_id` | Identifies the approved characteristic rule that derived a computed value or established characteristic-level non-applicability | Stable approved rule ID or `None` | Yes as a field; nullable by state | Explainability and reproducibility requirements in Sections 2.3, 3.1, and 3.3; Section 7.7 stable rule policy |
| `findings` | Preserves downstream rule interpretations that are relevant to this characteristic without conflating them with its numeric value | Immutable ordered tuple of valid `Finding` values for the same requirement and characteristic | Yes; may be empty | Signal/confirmed-defect distinction in Sections 2.1 and 2.3; structured finding requirement in Section 3.1 |
| `explanation` | States why the state/value is justified or withheld, without presenting a detector state as a quality conclusion | Non-empty human-readable text traceable to the governing rule or unresolved decision/input | Yes | Research explainability and provenance requirements in Sections 3.1 and 3.3 |

The state/value invariants are:

```text
state == COMPUTED
    => value is present
    => Fraction(0, 1) <= value <= Fraction(1, 1)
    => assessment_rule_id is present and approved

state == NOT_APPLICABLE
    => value is None
    => an approved characteristic-level applicability rule established
       non-applicability
    => no QUALITY_PROBLEM may be asserted for that characteristic

state == UNKNOWN
    => value is None
    => no numeric zero, pass, or failure is implied
```

These are distinct typed state spaces even where labels resemble one another:

```text
CharacteristicAssessmentState.UNKNOWN
    != CriterionApplicability.UNKNOWN
    != DetectionStatus.UNRESOLVED
```

The first withholds a characteristic result, the second says criterion
applicability cannot be established, and the third says detector processing
could not decide an observation candidate.

`CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10) now
allow each characteristic to reach `COMPUTED` under the stated conditions of
its own rule. No current rule establishes characteristic-level
`NOT_APPLICABLE` for any of the three. `UNKNOWN` remains the correct result
precisely when the governing rule's own required-input or material-dependency
propagation says so — a required input still `UNRESOLVED`, or, for
Verifiability, an unresolved candidate that could still change the numeric
class — not as a universal default. Findings and positive observations remain
preserved separately regardless of the resulting state.

`findings` may be non-empty while `state = UNKNOWN`. In particular, a vague-
term `SIGNAL` is a traceable warning and does not make Unambiguity computed.
The envelope does not include criterion results, confidence, severity,
probability, risk, priority, corrective actions, evidence reliability, or a
scalar aggregate. Criterion-result representation remains open until the
criteria and their applicability rules are approved; it is not added merely
for implementation convenience.

No detector-confidence, numeric-confidence, or evidence-reliability field or
value is approved for the current MVP v0.1 `CharacteristicAssessment` or
`Finding` contract. This exclusion does not resolve `RQD-020`; it remains
`OPEN / UNRESOLVED — NON-BLOCKING WHILE EXCLUDED`. If inclusion of any such
metadata is later proposed, `RQD-020` becomes blocking and requires a separate
scientific contract.

#### 7.16.3 Applicability contract

The existing state set remains unchanged:

```text
CriterionApplicability:
    APPLICABLE
    NOT_APPLICABLE
    UNKNOWN
```

The executable allocation rule is conservative:

1. `APPLICABLE` requires an approved criterion-specific rule whose observable
   premises are satisfied by the available domain data.
2. `NOT_APPLICABLE` requires an approved criterion-specific rule whose
   observable premises establish exclusion.
3. Otherwise the result is `UNKNOWN`.
4. `DETECTED`, `NOT_DETECTED`, `UNRESOLVED`, a non-empty observation tuple, and
   an empty observation tuple never convert automatically to an applicability
   value.
5. No requirement type, functional/non-functional class, template, domain
   role, or implicit context may be inferred to decide applicability.

Applied to the current candidate elements, this yields:

| Characteristic | Candidate element or criterion | Current applicability conclusion | Reason |
| --- | --- | --- | --- |
| Completeness | condition/context | `APPLICABLE` (MVP simplification) | `CALC-C-MVP-001` approves an explicit MVP v0.1 simplification: this criterion is mandatory and `APPLICABLE` for every supported input requirement. This is an MVP operationalization, not a universal claim that every requirement in every context must contain a condition/context element. |
| Completeness | expected reaction/result | `APPLICABLE` (MVP simplification) | Same `CALC-C-MVP-001` MVP simplification as above. |
| Completeness | fulfilment/acceptance criterion | `APPLICABLE` (MVP simplification) | Same `CALC-C-MVP-001` MVP simplification as above. |
| Verifiability | acceptance criterion, quantitative constraint, explicit verification method | Not individually mandatory criteria | `CALC-V-MVP-001` treats these three evidence families as alternative, non-mandatory evidence paths, not as three independently mandatory scoring criteria. None requires its own per-family `CriterionApplicability` allocation; a detected observation from any path is positive evidence for the corresponding tier, and a completed absence of all three contributes to a `0` result only through the calculation rule itself, never through a per-family `NOT_APPLICABLE`/`UNKNOWN` applicability judgment. |
| Verifiability | Verifiability (characteristic-level) | `APPLICABLE` | `CALC-V-MVP-001` establishes that Verifiability itself is applicable to every supported MVP requirement; sufficiency is then determined by which alternative evidence path, if any, is satisfied. |
| Unambiguity | vague-term occurrence | Not an applicability criterion | `UK-VAGUE-001` is a total signal detector for supported input when processing succeeds; a match or non-match does not establish property applicability or quality. |
| Unambiguity | confirmed ambiguity | `UNKNOWN` | The confirmation procedure and context exceptions are not defined; this criterion remains reserved for a future `U_i = 0` rule and is untouched by `CALC-U-MVP-001`. |

Consequently, the three current Completeness candidate elements are now
mandatory and `APPLICABLE` under the `CALC-C-MVP-001` MVP simplification, and
the Verifiability characteristic is applicable to every supported requirement
under `CALC-V-MVP-001`, even though none of its three evidence families is
individually mandatory. No candidate currently has an approved
`NOT_APPLICABLE` rule. A detected element remains valid positive evidence in
all cases; it is not erased because a sibling element or evidence family
contributed differently to the calculation.

#### 7.16.4 Characteristic-specific executable status

**Completeness — `APPROVED_FOR_MVP_V0.1` for calculation.** `CALC-C-MVP-001`
converts the condition/context, expected-result, and acceptance-criterion
outcomes into a criterion ratio `C_i = (c_condition + c_result +
c_acceptance) / 3`, where each criterion contributes `1` for `DETECTED` and
`0` for `NOT_DETECTED` under the explicit MVP simplification that all three
are mandatory and `APPLICABLE`. Any of the three required inputs being
`UNRESOLVED` withholds the result (`state = UNKNOWN`, `value = None`);
`NOT_DETECTED` alone is not a Completeness problem and does not create a
`QUALITY_PROBLEM`. No Completeness `QUALITY_PROBLEM` rule is approved.

**Verifiability — `APPROVED_FOR_MVP_V0.1` for calculation.** `CALC-V-MVP-001`
treats acceptance criteria, linked quantitative constraints, and explicit
verification methods as alternative (not additive or equally weighted)
evidence paths: an accepted acceptance criterion alone yields `V_i = 1`; absent
that, an accepted quantitative constraint or explicit verification method
yields `V_i = 1/2`; absent all three after complete relevant detector
processing, `V_i = 0`. An unresolved candidate withholds the result only when
resolving it could still change the numeric class (Section 9's worked
examples). No Verifiability `QUALITY_PROBLEM` rule is approved.

**Unambiguity — `APPROVED_FOR_MVP_V0.1` for the automated MVP scale;
confirmed-ambiguity calculation remains `BLOCKED`.** `CALC-U-MVP-001` converts
accepted `vague_term_occurrence` observations, via the existing one-for-one
`FIND-U-VAGUE-001` `SIGNAL` conversion, into `U_i = 1` when complete scanning
finds no accepted supported signal and `U_i = 1/2` when at least one exists;
additional signals do not further reduce the value. `U_i = 0` is reserved for
a future, separately approved confirmed-material-ambiguity rule and is never
produced by `CALC-U-MVP-001`. No supplied rule confirms ambiguity from an
occurrence alone, and `U_i = 1` represents absence of the supported signal
class, not universal semantic proof of a unique interpretation. No Unambiguity
`QUALITY_PROBLEM` rule is approved.

#### 7.16.5 Finalized minimal Finding contract

The approved representation is:

```text
FindingKind:
    SIGNAL
    QUALITY_PROBLEM

Finding:
    finding_id: str
    requirement_id: str
    characteristic_id: CharacteristicId
    kind: FindingKind
    code: str
    rule_id: str
    criterion_id: str | None
    evidence_refs: tuple[str, ...]
    explanation: str
```

| Field | Scientific meaning | Allowed values | Required? | Derivation source |
| --- | --- | --- | --- | --- |
| `finding_id` | Distinguishes repeated, independently traceable interpretations within one requirement assessment | Stable machine-readable identifier unique within the requirement assessment | Yes | Repeated-occurrence preservation and structured finding traceability in Sections 2.3 and 3.1 |
| `requirement_id` | Anchors the interpretation to the assessed information artifact even when no source span exists | ID of the enclosing `RequirementExtractionResult.requirement` | Yes | Requirement-level unit of analysis and absence provenance requirement |
| `characteristic_id` | Identifies the affected independent MVP property | Exactly the three values in Section 7.16.1 | Yes | Approved multidimensional profile |
| `kind` | Separates an indicator that needs interpretation from a violation established by an approved rule | `SIGNAL` or `QUALITY_PROBLEM` | Yes | Requirement properties paragraph 10; Metrics system paragraphs 12-16 and 30 |
| `code` | Names the stable finding category independently of detector implementation | Approved machine-readable category | Yes | Structured defect/finding classification and reproducibility |
| `rule_id` | Identifies the downstream interpretation rule that created the finding | Approved stable finding-rule ID | Yes | Sections 3.1 and 3.3 provenance; Section 7.7 |
| `criterion_id` | Identifies the applicable assessment criterion whose violation was established, especially when the finding is based on absence | Approved criterion ID or `None` when the rule is not a criterion violation | Yes as a field; conditionally non-null | Applicability and absence explainability; no criterion IDs are allocated by this contract |
| `evidence_refs` | Links evidence-based findings to immutable accepted detector Evidence without copying or replacing it | Ordered tuple of IDs resolving in the same extraction result; may be empty only under the absence rule below | Yes | Approved Evidence contract and exact-span explainability |
| `explanation` | States exactly what the rule established and its limit | Non-empty text; must not overstate a signal as a problem | Yes | Explainability requirements |

All referenced Evidence remains unchanged in the extraction result. A finding
never edits, replaces, normalizes, or reclassifies accepted Evidence. Evidence
references must resolve within the same `RequirementExtractionResult`, and the
finding's `requirement_id` must match that result's requirement.

The only allocated finding rule is:

```text
rule_id = FIND-U-VAGUE-001
code = VAGUE_TERM_SIGNAL
characteristic_id = UNAMBIGUITY
kind = SIGNAL
criterion_id = None
evidence_refs = exactly the accepted occurrence evidence reference(s)
```

It produces one finding per accepted `vague_term_occurrence`. Its explanation
names the matched approved seed literal and states that the occurrence is a
potential ambiguity indicator, not a confirmed defect. Repeated occurrences
produce separate findings, ordered by the accepted occurrence Evidence
`start_offset` under the existing matcher order. No other feature family
produces a current finding. Any future ordering across multiple finding rules
must be stated by the rule contract rather than inferred here.

**Absence-based provenance.** A future absence-based `QUALITY_PROBLEM` may be
created only when an approved rule establishes all of the following:

```text
criterion applicability == APPLICABLE
required detector processing completed
required observation == NOT_DETECTED
approved absence semantics say that this is a violation
```

Such a finding has `evidence_refs = ()`; it must not fabricate text, offsets,
or Evidence. It instead requires `requirement_id`, `characteristic_id`, the
approved characteristic `rule_id`, a non-null approved `criterion_id`, and an
explanation of the applicable required absence. `UNRESOLVED`, incomplete
processing, or `UNKNOWN` applicability can never create an absence-based
`QUALITY_PROBLEM`. No such absence-conversion rule or criterion ID is currently
approved.

#### 7.16.6 Detection-state propagation and mixed outcomes

The characteristic layer preserves the distinction between detector processing
and assessment interpretation:

| Detector input | What may be concluded | What may not be concluded |
| --- | --- | --- |
| `DETECTED` with complete processing | The accepted observations and Evidence exist and may be consumed by an approved rule | Automatic pass, score contribution, applicability, or `QUALITY_PROBLEM` |
| `NOT_DETECTED` with complete processing | The approved detector found no observation | Failed criterion, numeric zero, non-applicability, or confirmed problem without an approved applicable absence rule |
| `UNRESOLVED` | The detector could not determine the candidate result | False, absent, zero, failed, passed, or `NOT_APPLICABLE` |
| mixed accepted observations plus incomplete processing | Accepted observations and their Evidence remain valid; unresolved candidates and diagnostics remain visible | Erasing accepted observations, treating the family as wholly absent, or ignoring a required unresolved input |

When an approved characteristic rule identifies a detector input as required
and that input is `UNRESOLVED`, or an unresolved candidate remains material to
the rule, the characteristic result is:

```text
state = UNKNOWN
value = None
no absence-based QUALITY_PROBLEM from that input
```

The characteristic explanation must identify the affected required input and
its incomplete processing reason. Detector diagnostics remain diagnostics;
they do not become Evidence or findings merely to explain withholding.

In a mixed family outcome, accepted observations, accepted Evidence, and any
valid findings derived from them are retained. If the unresolved part is a
required input for the attempted characteristic rule, the assessment remains
`UNKNOWN`. Only a future approved rule that explicitly proves its result is
independent of the unresolved candidate could compute despite that candidate.
No current characteristic rule has that permission.

The following mixed-state consequences are binding:

- `expected_result = DETECTED`, `acceptance_criterion = DETECTED`, and
  `condition_context = UNRESOLVED` preserve the first two accepted observation
  families and their Evidence. The condition is neither absent nor failed.
  Under `CALC-C-MVP-001`, `condition_context` is one of the three required
  inputs, so its `UNRESOLVED` state withholds the result: Completeness remains
  `UNKNOWN` with no value.
- `acceptance_criterion = DETECTED`, a quantitative family with accepted
  observation(s) plus incomplete processing, and
  `verification_method = NOT_DETECTED` preserve the acceptance and accepted
  quantitative evidence. Under `CALC-V-MVP-001`, an accepted acceptance
  criterion alone is already sufficient for full Verifiability: `V_i = 1` is
  computed, and neither the unresolved quantitative candidate nor the
  `NOT_DETECTED` method can change that conclusion, because lower-tier
  evidence paths cannot improve a result beyond `1` (Section 9, Example V1).

#### 7.16.7 Numeric decisions

The source range `a_ik ∈ [0,1]` is an invariant for a future computed
individual property value; it is not itself a formula. This gate is now
resolved for per-requirement MVP v0.1 calculation:

| Characteristic | Approved rule | Formula | Exact value set | Current numeric status |
| --- | --- | --- | --- | --- |
| Completeness | `CALC-C-MVP-001` | `C_i = (c_condition + c_result + c_acceptance) / 3`, each criterion `1` if `DETECTED` else `0` under the MVP three-mandatory-criteria simplification | `{0, 1/3, 2/3, 1}` | `APPROVED_FOR_MVP_V0.1` |
| Verifiability | `CALC-V-MVP-001` | Alternative evidence paths: accepted acceptance criterion → `1`; else accepted quantitative constraint or verification method → `1/2`; else, after complete relevant processing, `0` | `{0, 1/2, 1}` | `APPROVED_FOR_MVP_V0.1` |
| Unambiguity | `CALC-U-MVP-001` | No accepted supported vague-term signal after complete scanning → `1`; one or more accepted signals → `1/2`; `0` reserved for a future confirmed-material-ambiguity rule | `{1/2, 1}` automated; `0` reserved | `APPROVED_FOR_MVP_V0.1` (automated scale); `0` `OPEN` |

`CALC-C-MVP-001` uses an unweighted criterion ratio; `CALC-V-MVP-001`
explicitly rejects equal weighting or an additive `(A + Q + M) / 3` formula in
favor of alternative sufficient-evidence tiers; `CALC-U-MVP-001` treats signal
count as explainability information only, not a cumulative penalty. All three
formulas use exact mathematical values (`1/3`, `2/3`, `1/2`); no calculator-
level rounding is introduced (Section 13). This closes the exact
calculation-semantics portion of `RQD-015`, and Section 13 additionally
approves Python standard-library `fractions.Fraction` as the internal
production representation for these values, so concrete MVP-06/07/08
implementation is no longer gated on representation. Specification-level
aggregation propagation and sufficiency semantics (`RQD-012`, `RQD-022`) are
now likewise `APPROVED_FOR_MVP_V0.1` via `AGG-MVP-001` (Sections 12-14);
only presentation precision and display-rounding policy remain open under
`RQD-015`.

#### 7.16.8 Binding characteristic-layer cases

These cases bind the strongest current conclusion against executable extractor
output, now including the approved `CALC-C-MVP-001`, `CALC-V-MVP-001`, and
`CALC-U-MVP-001` numeric results. `UNKNOWN` below is a characteristic
assessment state, not detector `UNRESOLVED` and not
`CriterionApplicability.UNKNOWN`, even when either may be the reason for
withholding. The underlying detector facts established by each case are
unchanged from the prior draft; only the resulting characteristic
state/value has been updated to reflect the newly approved calculation rules.

**Case A**

```text
У разі перевищення навантаження, система повинна відповісти не більше ніж за 2 с.
```

- Completeness has accepted condition/context, expected-result, and
  acceptance-criterion observations (`DETECTED`, `DETECTED`, `DETECTED`). Under
  `CALC-C-MVP-001`, `c_condition = c_result = c_acceptance = 1`, so
  `state = COMPUTED`, `value = 1`, `assessment_rule_id = CALC-C-MVP-001`. It
  emits no Completeness `QUALITY_PROBLEM`.
- Verifiability has an accepted acceptance-criterion observation. Under
  `CALC-V-MVP-001`, an accepted acceptance criterion alone is sufficient for
  full Verifiability regardless of the accepted quantitative-constraint
  evidence or the `NOT_DETECTED` verification method: `state = COMPUTED`,
  `value = 1`, `assessment_rule_id = CALC-V-MVP-001`, with no Verifiability
  `QUALITY_PROBLEM`.
- Unambiguity has no vague-term signal under the seed matcher, and scanning is
  complete. Under `CALC-U-MVP-001`, this yields `state = COMPUTED`,
  `value = 1`, `assessment_rule_id = CALC-U-MVP-001`, with no finding. This
  represents absence of the supported signal class, not universal semantic
  proof of a unique interpretation.

**Case B**

```text
Система повинна швидко оновити статус.
```

- The accepted expected result is the only accepted Completeness observation
  (`c_result = 1`); condition/context and acceptance criterion are
  `NOT_DETECTED` (`c_condition = c_acceptance = 0`), with complete processing
  for all three. Under `CALC-C-MVP-001`: `state = COMPUTED`, `value = 1/3`,
  `assessment_rule_id = CALC-C-MVP-001`.
- No acceptance criterion, quantitative constraint, or explicit verification
  method is accepted, and all relevant detector processing is complete. Under
  `CALC-V-MVP-001`: `state = COMPUTED`, `value = 0`,
  `assessment_rule_id = CALC-V-MVP-001`. Absence alone does not create a
  Verifiability `QUALITY_PROBLEM`.
- The accepted `швидко` occurrence creates exactly one `VAGUE_TERM_SIGNAL`
  under `FIND-U-VAGUE-001`. It is not a confirmed ambiguity or
  `QUALITY_PROBLEM`; under `CALC-U-MVP-001` one accepted supported signal
  yields `state = COMPUTED`, `value = 1/2`,
  `assessment_rule_id = CALC-U-MVP-001`, with the finding preserved.

**Case C**

```text
Перевірка: навантажувальний тест.
```

`VERIFY-UK-001` establishes explicit verification-method Evidence for the
named method phrase. It does not establish that the method is sufficient,
complete, linked to an acceptance criterion, or reproducible in all necessary
details, and it does not create a quality problem.
- No acceptance criterion is accepted; the accepted verification-method
  observation is the named lower-tier evidence path, with no material
  unresolved candidate that could raise it. Under `CALC-V-MVP-001`:
  `state = COMPUTED`, `value = 1/2`, `assessment_rule_id = CALC-V-MVP-001`.
  This named method is partial Verifiability evidence; it does not establish
  full Verifiability.
- Completeness has no accepted condition/context, expected-result, or
  acceptance-criterion observation, with complete processing for all three.
  Under `CALC-C-MVP-001`: `state = COMPUTED`, `value = 0`,
  `assessment_rule_id = CALC-C-MVP-001`.
- Unambiguity has no vague-term signal under the seed matcher, with complete
  scanning. Under `CALC-U-MVP-001`: `state = COMPUTED`, `value = 1`,
  `assessment_rule_id = CALC-U-MVP-001`.

**Case D**

```text
Система виконує аналіз журналу.
```

The verification-method family contains `VERIFY_UNRESOLVED_CANDIDATE`, no
accepted method observation, and incomplete processing. The diagnostic is not
Evidence, a signal, or a quality problem.
- No acceptance criterion and no quantitative constraint are accepted, and the
  verification-method candidate remains materially unresolved: resolving it
  could still turn the tier-two path from absent to present, which would
  change the numeric class from `0` to `1/2`. Under `CALC-V-MVP-001`'s
  material-dependency rule, this withholds the result: `state = UNKNOWN`,
  `value = None`. The candidate is treated as neither a present nor an absent
  method.
- Completeness has no accepted condition/context, expected-result, or
  acceptance-criterion observation, with complete processing for all three
  required inputs. Under `CALC-C-MVP-001`: `state = COMPUTED`, `value = 0`,
  `assessment_rule_id = CALC-C-MVP-001`.
- Unambiguity has no vague-term signal under the seed matcher, with complete
  scanning. Under `CALC-U-MVP-001`: `state = COMPUTED`, `value = 1`,
  `assessment_rule_id = CALC-U-MVP-001`.

Accepted observations from other feature families, if any, remain intact.

**Case E**

For a requirement where every relevant approved detector for Completeness and
Verifiability has completed, and all candidate observations are `NOT_DETECTED`
with no unresolved candidate:

- Completeness: `c_condition = c_result = c_acceptance = 0`. Under
  `CALC-C-MVP-001`: `state = COMPUTED`, `value = 0`,
  `assessment_rule_id = CALC-C-MVP-001`.
- Verifiability: no accepted acceptance criterion, quantitative constraint, or
  verification method, with complete processing. Under `CALC-V-MVP-001`:
  `state = COMPUTED`, `value = 0`, `assessment_rule_id = CALC-V-MVP-001`.
- Unambiguity: no vague-term signal under the seed matcher, with complete
  scanning. Under `CALC-U-MVP-001`: `state = COMPUTED`, `value = 1`,
  `assessment_rule_id = CALC-U-MVP-001`.

This conclusion is no longer inferred from `NOT_DETECTED` alone: it follows
because the researcher-approved `CALC-C-MVP-001` and `CALC-V-MVP-001` rules
explicitly define how a completed, fully-`NOT_DETECTED` outcome enters the
calculators. `NOT_DETECTED` remains a detector result, not automatically a
quality violation, and neither result above creates a `QUALITY_PROBLEM`
finding.

#### 7.16.9 Researcher decisions still required

The per-requirement Completeness, Verifiability, and Unambiguity formula
decisions previously tracked here are now resolved by `CALC-C-MVP-001`,
`CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10). The internal
production numeric representation row is now also resolved: Section 13
approves Python standard-library `fractions.Fraction` as the internal
production representation for computed characteristic values. Specification-
level aggregation (the row below) is now likewise resolved by `AGG-MVP-001`
(Section 12). The remaining row concerns only downstream presentation and
the future confirmed-material-ambiguity rule.

| Exact model-spec location | Research-source evidence | Scientifically plausible options | Implementation consequence | Smallest researcher decision required |
| --- | --- | --- | --- | --- |
| Section 10 and this Section 7.16.4 | Requirement properties, Table 2.3, reserves `0` for confirmed material ambiguity, distinct from the automated MVP signal-presence scale approved by `CALC-U-MVP-001` | manual/expert confirmation; deterministic context-exception rule; researcher-defined confirmation procedure | Determines whether a Unambiguity `QUALITY_PROBLEM` and `U_i = 0` can ever be produced | Approve a confirmation procedure and its mapping to `U_i = 0`, or explicitly leave `0` permanently unreachable for MVP |
| Section 13 — **RESOLVED** | `CALC-C/V/U-MVP-001` approve exact mathematical semantics (`1/3`, `2/3`, `1/2`) and no calculator-level intermediate rounding; Section 13 now additionally approves `fractions.Fraction` as the internal production representation, for both per-requirement values and the `AGG-MVP-001` aggregate, leaving only presentation-precision/rounding open | internal representation: `fractions.Fraction` (approved, per-requirement and aggregate); presentation: fixed precision; rule-specific precision; tie-breaking convention — still open | The concrete numeric type for `CompletenessCalculator`/`VerifiabilityCalculator`/`UnambiguityCalculator`/aggregator code (`Fraction`) is now recorded; console/reporting display precision remains a separate, still-open decision | Internal representation approved under `RQD-015` (this task); presentation/rounding and tie-breaking remain to be approved separately by the reporter task |
| Sections 12 and 14 — **RESOLVED** | Requirement properties supports property means; Metrics system requires `NA` for an empty applicability set and separates missing from non-applicable | `AGG-MVP-001` (Section 12) approved: exclude `UNKNOWN` values from the mean and report coverage as `unknown_count`; aggregate state `UNKNOWN` when the applicability set is non-empty but nothing is `COMPUTED`; aggregate state `NOT_APPLICABLE`/NA when the applicability set is empty | Determines `C_file`, `V_file`, and `U_file` behavior | None; property-level aggregation propagation and empty/partially-known denominator semantics are approved for MVP v0.1 |

`CompletenessCalculator`, `VerifiabilityCalculator`, and
`UnambiguityCalculator` are no longer blocked by open scientific formulas or
by an unselected internal representation: `CALC-C-MVP-001`, `CALC-V-MVP-001`,
and `CALC-U-MVP-001` authorize their calculation logic in principle, and
Section 13 now records `fractions.Fraction` as the concrete production
representation of `1/3` and `2/3`, so MVP-06, MVP-07, and MVP-08 are no
longer blocked on either ground. A concrete implementation must construct and
propagate `Fraction` values exactly (for example `Fraction(1, 3)`,
`Fraction(2, 3)`, `Fraction(1, 2)`), never via an intermediate `float` or
approximate `Decimal` conversion. Numeric `SpecificationQualityAggregator`
implementation, presentation/aggregate rounding, and any confirmed-ambiguity
`QUALITY_PROBLEM` rule remain separately blocked.

## 8. Completeness

### Explicitly defined by the dissertation

Section 2.1 defines local completeness as sufficient information to understand
the condition, expected reaction, and criterion of fulfilment. Table 2.1 names
required template components and defined conditions, values, and bounds as
possible evidence. Table 2.3 represents individual completeness as `a_i,C`, the
degree to which content elements required by the requirement type or template
are present.

The dissertation also explicitly distinguishes local completeness from global
specification completeness. Locally complete statements do not prove that the
specification covers every required function, quality characteristic,
interface, constraint, or significant scenario.

### Derivable without a new scientific assumption

- Condition, expected-reaction, and fulfilment-criterion evidence are relevant
  to local completeness.
- Specification coverage must not be inferred solely from per-line local
  completeness.
- A missing element may only count against a requirement when the element is
  applicable to that requirement type or template.

### Operationalization requiring researcher approval

The required elements by requirement type, the applicability rule, the mapping
from detected elements to `a_i,C`, binary versus graded behavior, and treatment
of overlap with Verifiability were previously unresolved. Actor/action/object
fields are not defined by Chapter 2 and are `DEFERRED_FROM_MVP_V0.1` as
possible optional future structural observations; they cannot affect
Completeness in v0.1.

`CALC-C-MVP-001` (researcher decision 1) resolves this for MVP v0.1 with an
explicit, narrow operationalization: local per-requirement Completeness is
measured using exactly three criteria — condition/context, expected
result/reaction, and acceptance/fulfilment criterion — and, for this specific
MVP scope, **all three are mandatory and `APPLICABLE` for every supported input
requirement**. This is an explicit MVP simplification. It is not a universal
theoretical claim that every software requirement in every context must always
contain these exact three elements, and it does not introduce automatic
requirement-type inference: MVP v0.1 still performs no requirement-type
classification. Section 7.16.3 records this simplification as an
applicability allocation, replacing the previous conservative `UNKNOWN`
default for these three candidate elements specifically. Detected
condition/context, expected-result, and acceptance-criterion observations
remain positive evidence exactly as before; only their entry into the
calculation formula is new. No Completeness `QUALITY_PROBLEM` rule is
approved by this decision.

Researcher decision RQD-002 is now `APPROVED_FOR_MVP_V0.1` (Section 18).
RQD-010 is closed for the per-requirement Completeness formula by
`CALC-C-MVP-001` itself (Section 18) and is not a remaining blocker here.
RQD-006 (broader detector grammar) remains separately open; the
specification-level portion of RQD-012 (aggregation) is now
`APPROVED_FOR_MVP_V0.1` via `AGG-MVP-001` (Section 12). Neither blocks, nor
blocked, per-requirement Completeness calculation.

### Formula and output range

Chapter 2 places individual property results `a_ij` in `[0,1]` and orients them
toward degree of property compliance; it does not itself supply the exact rule
for `a_i,C`. `CALC-C-MVP-001` supplies that rule for MVP v0.1:

```text
c_condition, c_result, c_acceptance ∈ {0, 1}

DETECTED     -> 1
NOT_DETECTED -> 0

C_i = (c_condition + c_result + c_acceptance) / 3
```

Multiple accepted observations within the same criterion family still
contribute at most `1`; repeated observations do not increase the score. The
exact allowed numeric values are `0`, `1/3`, `2/3`, and `1`, computed with
exact mathematical values (Section 13) rather than decimal rounding.

All three inputs are required by `CALC-C-MVP-001`. If any of the three
required detector inputs is `UNRESOLVED`, the other criteria cannot compensate
for it:

```text
state = UNKNOWN
value = None
```

Already-accepted observations and their Evidence are preserved unchanged in
this case. When the formula computes, the result carries
`assessment_rule_id = CALC-C-MVP-001`. This task does not approve any
Completeness `QUALITY_PROBLEM` finding; a low numeric Completeness value is
not automatically equivalent to a Finding. The executable status is now
`APPROVED_FOR_MVP_V0.1`; the current Completeness assessment reaches
`state = COMPUTED` whenever all three required inputs have completed
processing, and `state = UNKNOWN` with `value = None` only when a required
input remains `UNRESOLVED`.

### Explanation and evidence requirements

The assessment preserves every contributing approved observation and its
Evidence, and it now also cites `assessment_rule_id = CALC-C-MVP-001` when
`state = COMPUTED`. A later absence-based `QUALITY_PROBLEM` finding would still
have to follow Section 7.16.5 and use requirement/rule/criterion provenance
without a fabricated span, but no such finding is approved by this decision.
A criterion contributing `0` to `C_i` because its observation was
`NOT_DETECTED` does not itself require or fabricate Evidence for the absence.

### Reference examples

The initial GPS-provider statement in the application example explicitly says
that failure behavior is not defined; its revised form adds a condition and
observable outcomes. This remains a qualitative traceability example; its
exact `C_i` value is not re-derived outside the binding Section 7.16.8 cases
(see Section 16).

## 9. Verifiability

### Explicitly defined by the dissertation

Section 2.1 defines Verifiability as existence of a reproducible way to
establish whether a requirement is fulfilled. Possible evidence includes an
acceptance criterion, threshold, test oracle, or specified analysis/inspection
method. It further states that a measurable quality requirement may need an
indicator, measurement conditions, and an admissible boundary.

Section 2.3 distinguishes general Verifiability from operationalization of
quality requirements and defines aggregate research metrics `M_ver`, `M_ac`,
and `M_qnt`. These are set-level ratios over applicable requirements; they are
not per-line calculator formulas.

### Derivable without a new scientific assumption

- An explicit reproducible verification procedure is direct evidence for
  Verifiability.
- An acceptance criterion is a separate observable fact from the existence of a
  verification procedure.
- For applicable quality requirements, observable quantity, unit, measurement
  conditions, and admissible bound are relevant operationalization evidence.
- Not every quality requirement must be numeric; the verification method
  depends on requirement and characteristic type.

### Operationalization requiring researcher approval

The rule for determining applicability, requirement type, procedure presence,
criterion presence, and linkage among quantity/unit/condition/bound was
previously undefined, as was the mapping of those observations to `a_i,V`.

`CALC-V-MVP-001` (researcher decision 2) resolves this for MVP v0.1. It uses
the already-approved evidence families — acceptance criterion, quantitative
constraint, and explicit verification method — but treats them as **alternative
evidence paths, not three mandatory criteria**. The formula is deliberately
not an equally weighted `(A + Q + M) / 3`: an accepted acceptance-criterion
observation under the current approved extraction contract is, by itself,
sufficient for the MVP full-verifiability class, because the approved detector
contract establishes a judgeable acceptance composition. Verifiability itself
is applicable to every supported MVP requirement (Section 7.16.3); its three
evidence families no longer each need their own mandatory-criterion
applicability decision, because none of them is individually mandatory.

Researcher decision RQD-003 is now `APPROVED_FOR_MVP_V0.1` (Section 18).
`RQD-008` remains relevant to broader quantitative-constraint grammar,
which remains open; `RQD-012`'s specification-level aggregation portion is
now `APPROVED_FOR_MVP_V0.1` via `AGG-MVP-001` (Section 12). Neither blocks
per-requirement Verifiability calculation.

### Formula and output range

Chapter 2 supports `[0,1]` compliance-oriented individual property results and
explicit set-level ratios; `CALC-V-MVP-001` now supplies the exact
per-requirement mapping for MVP v0.1:

**Full Verifiability.** If there is an accepted `acceptance_criterion`
observation:

```text
V_i = 1
```

**Partial Verifiability.** If there is no accepted acceptance criterion, but at
least one accepted quantitative constraint or accepted explicit verification
method exists:

```text
V_i = 1/2
```

Repeated observations do not increase this value.

**No detected operationalization evidence.** If all detector processing that
remains relevant to `CALC-V-MVP-001` has completed and no accepted acceptance
criterion, quantitative constraint, or verification method exists:

```text
V_i = 0
```

**Material-dependency unresolved propagation.** `CALC-V-MVP-001` does not use
blanket unresolved propagation. An unresolved input withholds the result
(`state = UNKNOWN`, `value = None`) only when resolving it could still change
the numeric class:

- an accepted acceptance criterion already exists, with lower-tier candidates
  unresolved → `V_i = 1` still computes, because lower-tier inputs cannot
  improve beyond `1` (Example V1);
- no accepted acceptance criterion, no accepted lower-tier evidence, and a
  quantitative or verification-method candidate is unresolved → `state =
  UNKNOWN`, because resolving it could change `0` to `1/2` (Example V2);
- no accepted acceptance criterion, an accepted quantitative constraint
  exists, and the verification method is unresolved → `V_i = 1/2` still
  computes, because the unresolved verification-method candidate cannot
  change the numeric class (Example V3);
- an accepted lower-tier path gives a provisional `1/2`, but the
  acceptance-criterion family contains a material unresolved candidate that
  could still become an accepted acceptance criterion → `state = UNKNOWN`,
  because the unresolved acceptance candidate could change `1/2` to `1`
  (Example V4).

The exact allowed numeric values are `0`, `1/2`, and `1`, using exact
mathematical values rather than decimal rounding (Section 13). When the
formula computes, the result carries `assessment_rule_id = CALC-V-MVP-001`.
This task does not approve any Verifiability `QUALITY_PROBLEM` finding. The
executable status is now `APPROVED_FOR_MVP_V0.1`.

### Explanation and evidence requirements

The assessment preserves observable criterion, metric, threshold, unit,
expected-result, and method evidence that is present, and now also cites
`assessment_rule_id = CALC-V-MVP-001` when `state = COMPUTED`. A `V_i = 0`
result contributed by completed absence does not itself require or fabricate
Evidence, and it is not automatically a `QUALITY_PROBLEM`; any future
absence-based finding would still require a separately approved rule under
Section 7.16.5. It must not claim a stronger conclusion than the detector
supports.

### Reference examples

The application example contrasts “quickly recalculate” with a revised
requirement specifying four seconds under 300 concurrent requests. This remains
a qualitative feature/evidence example; its exact `V_i` value is not
re-derived outside the binding Section 7.16.8 cases (see Section 16). The
example's numeric quality values are demonstrational and are not expected MVP
outputs.

## 10. Unambiguity

### Explicitly defined by the dissertation

Section 2.1 defines Unambiguity as allowing one justified interpretation in the
given context. Possible evidence includes absence of ambiguous terms, expert
agreement, and stable interpretation by different reviewers. It identifies
subjective wording, vague adjectives/adverbs, weak modal constructions, and
pronoun references as possible automated signals.

Table 2.3 describes `a_i,U`: `1` when no confirmed ambiguities exist, an
intermediate value when risk signals exist, and `0` when a material ambiguity is
confirmed. Section 2.3 gives the set-level metric `M_amb = 1 - N_amb/N_app` for
requirements without confirmed ambiguity indicators.

### Derivable without a new scientific assumption

- An automated linguistic match is a risk indicator, not proof of ambiguity.
- Confirmation state must remain distinct from raw detector output.
- Only applicable requirements belong in the metric denominator.

### Operationalization requiring researcher approval

The source-derived seed lexicon and exact deterministic matching mechanics are
approved for MVP v0.1. Richer linguistic coverage, context exceptions, and a
confirmed-material-ambiguity procedure remain undefined and are explicitly
deferred to future research. `CALC-U-MVP-001` (researcher decision 3) now
resolves the mapping of the automated MVP signal to a numeric `a_i,U` for MVP
v0.1, using the currently approved vague-term detector and `FIND-U-VAGUE-001`.
The Finding remains `kind = SIGNAL`; it must never become `QUALITY_PROBLEM`
merely from a match.

The one-occurrence-to-one-signal rule `FIND-U-VAGUE-001` is executable and
produces only `VAGUE_TERM_SIGNAL`. No occurrence is a confirmed ambiguity, and
`CALC-U-MVP-001` never produces `U_i = 0`; that value is reserved for a future,
separately approved confirmed-material-ambiguity rule. No Unambiguity
`QUALITY_PROBLEM` rule is approved by this decision.

Researcher decision RQD-004 is now `APPROVED_FOR_MVP_V0.1` for the automated
signal-presence scale (Section 18); the confirmed-ambiguity portion remains
`OPEN`. `CALC-U-MVP-001` depends only on the approved vague-term seed matcher
and `FIND-U-VAGUE-001`, not on quantitative-constraint or linkage grammar, so
`RQD-008` is not a dependency of the Unambiguity calculator. The
specification-level aggregation portion of `RQD-012` is now
`APPROVED_FOR_MVP_V0.1` via `AGG-MVP-001` (Section 12); the
characteristic-calculation portion of `RQD-016` remains relevant to future
`QUALITY_PROBLEM`/confirmed-ambiguity conversions. Neither blocks the
per-requirement automated Unambiguity calculation.
`RQD-007` remains closed for the MVP v0.1 seed matcher.

### Formula and output range

Chapter 2 provides direction and boundary examples for `a_i,U`: `1` when no
confirmed ambiguity exists, an intermediate value for risk signals, and `0`
when a material ambiguity is confirmed. `CALC-U-MVP-001` supplies the
executable MVP v0.1 mapping between the approved automated signal and the
first two of those:

**No supported vague-term signal.** If vague-term processing completes
successfully and no accepted supported vague-term occurrence exists:

```text
U_i = 1
```

This means no ambiguity-risk signal from the approved MVP vague-term detector
was found. It must not be described as universal proof that the requirement
has exactly one semantically valid interpretation in every possible context.

**One or more supported signals.** If at least one accepted supported
vague-term occurrence exists:

```text
U_i = 1/2
```

Signal count is explainability information, not a cumulative numeric penalty:
one signal, two signals, or `n` signals all yield `1/2`. Each individual
Finding and its Evidence are preserved regardless of count.

**Confirmed material ambiguity.** `U_i = 0` is reserved for a future,
separately approved confirmed-material-ambiguity rule. The current automated
MVP rule, `CALC-U-MVP-001`, must never produce `0`.

**Unresolved behavior.** If no accepted vague-term signal exists and
unresolved processing could still contain a supported vague-term signal:

```text
state = UNKNOWN
value = None
```

If at least one valid vague-term signal already exists, `U_i = 1/2` computes
even if additional candidates are unresolved, because additional signals do
not further reduce the score and the current automated rule cannot produce
`0`.

The exact allowed numeric values from `CALC-U-MVP-001` are `1/2` and `1`,
using exact mathematical values rather than decimal rounding (Section 13).
When the formula computes, the result carries
`assessment_rule_id = CALC-U-MVP-001`. The executable status for the
automated scale is now `APPROVED_FOR_MVP_V0.1`; confirmed-ambiguity
calculation remains `NO EXECUTABLE SCORE — FUTURE RESEARCH DECISION`.

### Explanation and evidence requirements

Each signal identifies the exact matched Evidence, vocabulary entry, and
`FIND-U-VAGUE-001` interpretation rule, and the resulting `state = COMPUTED`
assessment now also cites `assessment_rule_id = CALC-U-MVP-001`. A count
without the matched Evidence is insufficient. A `U_i = 1` result from a
complete scan with no signal requires no fabricated Evidence for the absence.
A future confirmed ambiguity must use a separately approved `QUALITY_PROBLEM`
rule and is not created by this decision.

### Reference examples

The application example supplies useful positive findings for vague phrases and
revised bounded forms. It does not establish that every occurrence is always
ambiguous or provide a complete vocabulary. Its exact `U_i` values for these
illustrative fragments are not re-derived outside the binding Section 7.16.8
cases (see Section 16).

## 11. Requirement Quality Profile

The approved implementation relationship is:

```text
CharacteristicAssessments(C_i, V_i, U_i)
        ↓
RequirementQualityProfile(A_i)
```

Chapter 2 defines individual property results `a_i,C`, `a_i,V`, and `a_i,U`, but
it deliberately preserves a multidimensional property profile. Therefore the
primary result is `A_i = (C_i, V_i, U_i)`, where each component is the
corresponding Section 7.16 `CharacteristicAssessment`, not an assumed number.
Each component may now reach `state = COMPUTED` with a value in `[0,1]` under
its approved rule (`CALC-C-MVP-001`, `CALC-V-MVP-001`, or `CALC-U-MVP-001`,
Sections 8-10), or remain `state = UNKNOWN` with `value = None` exactly when
that rule's own required-input or material-dependency propagation says so.
No function combines these components, and no scalar `RequirementQualityScore`
is required in MVP v0.1. Chapter 4's `Q_int` formula combines context-selected
ISO product-quality characteristics, not the three MVP properties of one
requirement, and must not be reused here. RQD-013's original scalar-score
request remains intentionally deferred from MVP v0.1.

## 12. Specification Quality Profile

The approved implementation relationship is:

```text
RequirementQualityProfile(A_1, ..., A_n)
        ↓
property-level specification aggregation
        ↓
SpecificationQualityProfile(C_file, V_file, U_file)
```

Chapter 2 defines `x_k = (1/n) * sum_i(a_ik)` as the set-level indicator for one
specific requirement property. MVP v0.1 therefore preserves three separate
aggregates, one per characteristic, with no scalar combination across them:

```text
C_file = mean(...)
V_file = mean(...)
U_file = mean(...)
```

No scalar `FileQualityScore` combines these values. RQD-014's original scalar-
score request is intentionally deferred from MVP v0.1 (Section 18.2). Per-
requirement `C_i`, `V_i`, and `U_i` are now executable under Sections 8-10, so
this gate is no longer blocked merely by the absence of a per-requirement
numeric rule. This section's aggregation rule — `AGG-MVP-001` — is now
researcher-approved for MVP v0.1 (Section 18): it fixes *which*
per-requirement values populate each `mean(...)` above, and what aggregate
outcome results when the computed subset is empty or partial. `AGG-MVP-001`
is one shared, characteristic-agnostic rule applied identically to compute
`C_file`, `V_file`, and `U_file`. This section now authorizes calculation of
`C_file`, `V_file`, and `U_file` under that rule; only the eventual
`SpecificationQualityAggregator`/`SpecificationQualityProfile`
implementation, and presentation/display rounding, remain outstanding.

### Explicitly defined by the dissertation

- `2.3_Система_метрик.docx` (¶43-44) states the aggregation-denominator
  convention directly: "if the applicability set forming the denominator is
  empty, the result is recorded as NA (not applicable) and is not equated to
  zero," and that this convention "extends to verifiability, traceability,
  coverage and other normalized-fraction metrics" — i.e. it is general, not
  characteristic-specific. Applied here: if every requirement is
  `NOT_APPLICABLE` for a given property, or the requirement collection itself
  is empty, the aggregate's semantic result is NA / not applicable, and the
  numeric value is absent (never zero).
- `2.1_Властивості_вимог.docx` (¶92) states the aggregation *formula* itself:
  `x_k = (1/n) * sum_i(a_ik)`, a plain, unweighted arithmetic mean over a
  property (already transcribed at Section 4.2, line 197). This fixes the
  shape of the calculation once its inputs are fixed; it does not say which
  `a_ik` values belong in that sum when some are `UNKNOWN` rather than
  `NOT_APPLICABLE` or computed.
- `2.3_Система_метрик.docx` (¶132) restates the three-state distinctness
  principle this contract must respect: "at least three states [must] be
  distinguished: the indicator is computed; the indicator is applicable but
  the necessary data is missing; the indicator does not apply... Substituting
  zero for the second or third case mixes different semantic situations." No
  reference document extends this sentence to state, verbatim, what an
  aggregate built from a *mix* of these states should look like, or what
  state the aggregate itself should carry when nothing was computed. The
  "Operationalization requiring researcher approval" subsection below
  records the researcher-approved MVP v0.1 resolution of that gap; it is a
  documented operationalization of this principle, not a claim that the
  dissertation states the aggregate-level rule verbatim.
- Chapter 4 (§4.1, §4.2) reaffirms "absent/inapplicable evidence is not
  equated to a zero value" and that no default scalar integral index exists
  (`Q_int` is a separate, optional, explicitly demonstrational construct,
  already excluded from MVP v0.1 by RQD-013/RQD-014, Section 18.2).

### Derivable without a new scientific assumption

- *Given* a fixed set of `Fraction` values to average, the mean must be
  computed with exact `fractions.Fraction` arithmetic — sum of `Fraction`s
  divided by an integer count, with no intermediate rounding. This is a
  mechanical consequence of two already-approved facts: the mean formula
  itself (`2.1`, ¶92, above) and Section 13's exact-arithmetic principle for
  `CharacteristicAssessment.value`. It introduces no new scientific claim and
  is independent of which items are selected into that set. `AGG-MVP-001`
  below now fixes that selection, so this consequence applies unconditionally
  to `C_file`, `V_file`, and `U_file`; it still approves no display or
  percentage rounding (Section 13).
- `NOT_APPLICABLE` requirements are outside a property's applicability set by
  definition — that is what `NOT_APPLICABLE` means (Section 7.16.3) — so a
  `NOT_APPLICABLE` item never contributes to, and is never "excluded from," a
  mean's numerator or denominator in the sense of a policy choice about
  missing data; it was never in scope for that mean. This is definitional,
  not an aggregation-policy decision.
- **Specification-level numeric range.** Given `AGG-MVP-001`'s approved
  inclusion rule (mean over `COMPUTED` values only, below), the
  specification-level numeric range follows mechanically from the
  already-approved per-requirement ranges: the mean of values drawn from a
  bounded interval is itself within that interval. Under the current MVP
  v0.1 automated per-requirement value sets — Completeness `{0,1/3,2/3,1} ⊂
  [0,1]`, Verifiability `{0,1/2,1} ⊂ [0,1]`, Unambiguity automated
  `{1/2,1} ⊂ [1/2,1]` (Sections 8-10) — whenever a numeric aggregate exists
  (`state == COMPUTED`):

  ```text
  C_file ∈ [0, 1]
  V_file ∈ [0, 1]
  U_file ∈ [1/2, 1]
  ```

  Compliance orientation is preserved: higher value = greater conformance to
  the corresponding property, matching the per-requirement orientation
  (Chapter 2; Section 7.16). `U_file = 0` remains impossible under the
  current automated MVP because the per-requirement `U_i = 0`
  confirmed-material-ambiguity rule is still deferred (Section 7.16.4,
  RQD-004); if that per-requirement rule is later approved, `U_file`'s lower
  bound would need to be re-derived, not assumed to remain `1/2`. `UNKNOWN`
  and `NOT_APPLICABLE` aggregates carry `value = None` and are therefore not
  numeric points on these scales — they are excluded from these range
  statements entirely, consistent with Section 14's "missing/inapplicable is
  not zero" principle. This introduces no new scientific claim: it is a
  direct mathematical consequence of already-approved facts (RQD-011).

### Operationalization requiring researcher approval

Two questions are not settled verbatim by the sources above and could not be
answered by assumption. Both concern only requirements whose per-requirement
characteristic state is `UNKNOWN` (applicable, but the calculator withheld a
value) — not `NOT_APPLICABLE`, which is already resolved above. The
researcher has now approved a candidate for each, recorded here as
`AGG-MVP-001` and `APPROVED_FOR_MVP_V0.1` (Section 18, RQD-012/RQD-022).

**Q1 — a property's requirement set contains both `COMPUTED` and `UNKNOWN`
items.** Considered candidates were:

- **A.** any `UNKNOWN` item withholds the *entire* aggregate: the aggregate's
  semantic outcome becomes "unresolved," regardless of how many `COMPUTED`
  items exist alongside it.
- **B.** the mean is computed from the `COMPUTED` items only; the count of
  `UNKNOWN` items is preserved and reported alongside the aggregate rather
  than folded into it.
- **C.** any other source-supported rule — none was found in the reference
  material.

**Approved: candidate B.** The aggregate mean is computed from `COMPUTED`
values only; `UNKNOWN` values enter neither the numerator nor the
denominator and must never become numeric zero; the count of `UNKNOWN`
items is preserved separately as `unknown_count` (see the representation
contract below). The aggregate numeric result therefore exists even when
observability is partial, as long as at least one `COMPUTED` value is
present. This operationalizes `2.3_Система_метрик.docx` ¶132's "observability
mask" recommendation: missingness/observability is tracked separately
(`unknown_count`) rather than converted into the numeric metric itself. This
is a researcher-approved MVP v0.1 operationalization of that principle, not
a claim that the dissertation states this exact rule.

**Q2 — a property's requirement set contains one or more `UNKNOWN` items and
zero `COMPUTED` items** (the applicability set — `COMPUTED` ∪ `UNKNOWN` — is
non-empty, but nothing was resolved). No new state is invented (Section 4.1
fixes the status vocabulary; `CharacteristicAssessmentState` is likewise
closed to `COMPUTED`/`NOT_APPLICABLE`/`UNKNOWN`, Section 7.16.2); the only two
candidates were the existing per-requirement states:

- **A.** aggregate state = `UNKNOWN`, value = `None` — preserves the
  distinction between "applicable but unresolved" and "not applicable."
- **B.** aggregate state = `NOT_APPLICABLE`, value = `None` — collapses that
  distinction.

**Approved: candidate A.** When there are zero `COMPUTED` values but one or
more `UNKNOWN` values, the aggregate state is `UNKNOWN` and its value is
`None`; this case must not be mapped to `NOT_APPLICABLE`. Collapsing to
`NOT_APPLICABLE` (candidate B) would conflate exactly the two states that
§2.3 ¶132 says must not be conflated. This applies only when the
applicability set is genuinely non-empty (at least one `UNKNOWN`); if the
applicability set is genuinely empty — every value is `NOT_APPLICABLE`, or
the requirement collection is empty — the semantic result remains
`NOT_APPLICABLE` / NA with value `None`, per "Explicitly defined by the
dissertation" above.

`RQD-012` and `RQD-022`'s specification-aggregation portions are closed for
MVP v0.1 by these two approvals (Section 18). Only presentation/display
rounding (Section 13) and the actual `SpecificationQualityAggregator`/
`SpecificationQualityProfile` implementation remain outstanding.

### Decision matrix

`AGG-MVP-001` (`APPROVED_FOR_MVP_V0.1`) resolves all eight required cases.
The matrix still separates the **semantic outcome** from the **representation
state**, since the two are conceptually distinct (Section 7.16.2 draws the
same distinction for per-requirement assessments), but both columns are now
approved, not proposed. One shared matrix covers Completeness, Verifiability,
and Unambiguity: the rule is characteristic-agnostic and does not differ
between them.

| Case | Status | Semantic outcome | Numeric value | Representation state |
| --- | --- | --- | --- | --- |
| All `COMPUTED` | Approved | A numeric aggregate is available | Exact arithmetic mean of all included values | `COMPUTED` |
| `COMPUTED` + `UNKNOWN` | Approved (Q1 = B) | The mean is computed from the `COMPUTED` items; `UNKNOWN` items are excluded from numerator/denominator and tracked separately, never treated as zero | Exact mean of the `COMPUTED` items only; `unknown_count` records the excluded items | `COMPUTED` |
| `COMPUTED` + `NOT_APPLICABLE` | Approved | A numeric aggregate is available over the applicable subset; `NOT_APPLICABLE` items are outside the applicability set by definition | Exact arithmetic mean of the `COMPUTED` (applicable) values | `COMPUTED` |
| `COMPUTED` + `UNKNOWN` + `NOT_APPLICABLE` | Approved (Q1 = B) | Same as `COMPUTED` + `UNKNOWN`; `NOT_APPLICABLE` items are additionally outside the applicability set | Exact mean of the `COMPUTED` items only; `unknown_count` and `not_applicable_count` both recorded | `COMPUTED` |
| All `UNKNOWN` | Approved (Q2 = A) | The applicability set is non-empty but nothing is resolved; this must not be conflated with "not applicable" | Absent | `UNKNOWN` |
| All `NOT_APPLICABLE` | Approved | The applicability set is empty; semantic result = NA / not applicable | Absent | `NOT_APPLICABLE` |
| `UNKNOWN` + `NOT_APPLICABLE`, no `COMPUTED` | Approved (Q2 = A) | Same as "all `UNKNOWN`": the applicability set is non-empty because the `UNKNOWN` items are in it | Absent | `UNKNOWN` |
| Empty requirement collection | Approved | The applicability set is vacuously empty; semantic result = NA / not applicable | Absent | `NOT_APPLICABLE` |

### Reference examples

All examples use only the already-approved per-requirement value sets
(Completeness `{0,1/3,2/3,1}`, Verifiability `{0,1/2,1}`, Unambiguity
`{1/2,1}`) plus the two non-numeric per-requirement states `UNKNOWN` and
`NOT_APPLICABLE`. No new per-requirement value is introduced.

**Example 1 — partially known set (Verifiability-shaped values).** Five
requirements' `V_i`: `1`, `1/2`, `UNKNOWN`, `0`, `NOT_APPLICABLE`.

- Semantic outcome: a numeric aggregate is available from the three
  `COMPUTED` items; the `UNKNOWN` and `NOT_APPLICABLE` requirements sit
  outside the numerator/denominator for different reasons — one because the
  source data withholds computation (`AGG-MVP-001`, Q1 = B); one because the
  property never applied to it.
- Approved result: `(1 + 1/2 + 0) / 3 = (3/2) / 3 = 1/2` exactly, computed as
  `Fraction`, no rounding; `computed_count = 3`, `unknown_count = 1`,
  `not_applicable_count = 1`, `total_count = 5`; representation state
  `COMPUTED`.
- For contrast only (not the approved rule): candidate A for Q1 — any
  `UNKNOWN` withholds the whole aggregate — would have withheld this result
  even though three of five requirements were computed. This was considered
  and rejected in favor of B.

**Example 2 — no `COMPUTED` denominator, applicability set non-empty
(Completeness-shaped values).** Three requirements' `C_i`: `UNKNOWN`,
`UNKNOWN`, `NOT_APPLICABLE`.

- The applicability set (`COMPUTED` ∪ `UNKNOWN`) has two members; it is not
  empty, so the empty-applicability-set NA rule does not apply here.
- Approved result (`AGG-MVP-001`, Q2 = A): aggregate state `UNKNOWN`, value
  `None`; `computed_count = 0`, `unknown_count = 2`,
  `not_applicable_count = 1`, `total_count = 3`.
- For contrast only (not the approved rule): candidate B for Q2 — collapsing
  to `NOT_APPLICABLE` — was considered and rejected because it would conflate
  "applicable but unresolved" with "not applicable."

**Example 3 — empty applicability set (Unambiguity-shaped values).** Three
requirements' `U_i`: `NOT_APPLICABLE`, `NOT_APPLICABLE`, `NOT_APPLICABLE`.

- The applicability set is empty. Approved result: semantic outcome NA / not
  applicable, aggregate state `NOT_APPLICABLE`, value `None`;
  `computed_count = 0`, `unknown_count = 0`, `not_applicable_count = 3`,
  `total_count = 3`. This is the directly evidence-supported case (§2.3
  ¶43-44).

**Example 4 — exact arithmetic, no rounding.** A characteristic-agnostic
illustration of the arithmetic itself, decoupled from any one characteristic's
approved discrete scale: given three `COMPUTED` values `1`, `1/2`, and `1/3`:

```text
mean(1, 1/2, 1/3)
  = (Fraction(1,1) + Fraction(1,2) + Fraction(1,3)) / 3
  = Fraction(11,6) / 3
  = Fraction(11,18)
```

`11/18` is exact and is not rounded to `0.61`, `0.611`, or any other decimal
form; any such rounding is a presentation-layer decision and remains outside
this contract's scope (Section 13).

### `SpecificationQualityProfile` representation contract — `APPROVED_FOR_MVP_V0.1`

A bare `Fraction | None` per property cannot represent this section's
decision matrix: it cannot distinguish an aggregate reading as `UNKNOWN` from
one reading as `NOT_APPLICABLE` (both would be `None`), which is the same
problem `CharacteristicAssessment.state` already solves once at the
per-requirement level (Section 7.16.2). Given the approved `AGG-MVP-001`
outcomes above, each of `C_file`, `V_file`, and `U_file` therefore needs a
stateful aggregate result — not a bare `Fraction`, not a scalar, and not a
reuse of `CharacteristicAssessment` itself (that type's per-item
`findings`/`explanation` fields describe a single rule-based evidence
assessment over one requirement, not a computed-over-many aggregate).

The researcher-approved minimum shape, not yet implemented by this
documentation-only decision:

```text
characteristic_id: CharacteristicId  (COMPLETENESS, VERIFIABILITY, or
       UNAMBIGUITY — identifies which property this aggregate is for)
state: one of COMPUTED, NOT_APPLICABLE, UNKNOWN  (reuses the existing
       CharacteristicAssessmentState vocabulary)
value: Fraction | None  (present iff state == COMPUTED, mirroring the same
       invariant as CharacteristicAssessment)
computed_count: int
unknown_count: int
not_applicable_count: int
total_count: int  (== computed_count + unknown_count + not_applicable_count)
aggregation_rule_id: str  ("AGG-MVP-001" for MVP v0.1 — stable provenance,
       mirroring CharacteristicAssessment.assessment_rule_id, so every
       specification-level numeric result remains traceable to its approved
       rule, Section 15)
```

No aggregate `findings` field is approved: `AGG-MVP-001` is a uniform
arithmetic rule applied to already-computed per-requirement values, not a
new evidence-gathering rule, so it produces no findings of its own.
`SpecificationQualityProfile(C_file, V_file, U_file)` holds exactly three
such aggregates, one per characteristic — mirroring
`RequirementQualityProfile`'s three-field, no-scalar shape one level up. This
preserves the already-approved invariant that there is no `FileQualityScore`,
no `RequirementQualityScore` reuse, no weights, and no combined/weighted
C/V/U scoring in MVP v0.1 (RQD-013, RQD-014, Section 18.2). This section
approves the contract but does not implement it: `SpecificationQualityAggregator`
and `SpecificationQualityProfile` remain unimplemented Python; a future
implementation task builds them exactly to this shape.

## 13. Numeric precision and rounding

Chapter 2 establishes `[0,1]` and increasing polarity for several property
metrics and preserves contextual polarity for process measures. It does not
establish a full MVP precision or rounding contract. `CALC-C-MVP-001`,
`CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10) approve the
calculation-semantics portion of this contract. This section additionally
approves the internal production numeric representation for computed
characteristic values, and now also the specification-level aggregate
computation itself; only presentation/display rounding remains open.
`RQD-015`'s status is therefore
`INTERNAL_EXACT_REPRESENTATION_APPROVED (PER-REQUIREMENT AND AGGREGATE) / PRESENTATION_ROUNDING_OPEN`,
not fully closed. Section 12's `AGG-MVP-001` fixes the specification-level
inclusion set (Q1/Q2, `RQD-012`/`RQD-022`), so the aggregate-arithmetic
exactness recorded below is no longer conditional on an open question — only
presentation/display rounding is:

**Approved now — exact calculation semantics:**

- calculator formulas use exact mathematical values (`1/3`, `2/3`, `1/2`, not
  `0.33`/`0.67` or any other decimal approximation);
- no intermediate rounding is part of any characteristic formula;
- the only exact per-characteristic value sets are `{0, 1/3, 2/3, 1}` for
  Completeness, `{0, 1/2, 1}` for Verifiability, and `{1/2, 1}` (`0` reserved)
  for Unambiguity.

**Approved now — internal production numeric representation:**

- Python standard-library `fractions.Fraction` is the approved internal
  production representation for computed `CharacteristicAssessment.value`
  (Completeness, Verifiability, and Unambiguity per-requirement scores) for
  MVP v0.1 (Section 7.16.2: `value: Fraction | None`). No third-party
  dependency is required;
- scores must be constructed from exact integer numerator/denominator pairs,
  for example `Fraction(1, 3)`, `Fraction(2, 3)`, and `Fraction(1, 2)`; for
  Completeness, an implementation may equivalently construct
  `Fraction(detected_criterion_count, 3)`, where `detected_criterion_count`
  is the approved integer count from `CALC-C-MVP-001`;
- a score must never be constructed by first producing a floating-point
  approximation (for example `Fraction(0.3333333333333333)` is not an
  approved construction) or by encoding an approximate decimal string (for
  example `Decimal("0.33")` or `Decimal("0.333333")` is not an approved
  characteristic-score value);
- calculator and domain-layer arithmetic must preserve `Fraction` throughout,
  with no intermediate rounding and no implicit conversion to `float`,
  approximate `Decimal`, or a formatted decimal string as part of
  calculation; comparison against the score interval is exact rational
  comparison against `Fraction(0, 1)` and `Fraction(1, 1)` (Section 7.16.2).

**Rationale for `fractions.Fraction`:** the already-approved formulas require
exact rational values including `1/3`, `2/3`, and `1/2`. Binary floating-point
cannot guarantee an exact representation of a value such as `1/3`. A finite
base-10 decimal representation likewise cannot represent `1/3` exactly, so
using `Decimal` for these scores would require a precision/rounding decision
that is intentionally excluded from calculator semantics (no calculator-level
intermediate rounding is permitted). Python's standard-library
`fractions.Fraction` represents the required rational values exactly and
deterministically without introducing a new dependency. This is a
researcher-approved MVP v0.1 implementation operationalization of the
already-approved mathematical semantics, not a new scientific theorem.

**Domain separation — `Decimal` and `Fraction` are distinct and must not be
coupled:**

- `Decimal` remains the approved representation for extracted quantitative
  *measurement* values parsed from requirement text
  (`NumericValueComponent.decimal_value`, Section 7.15.10). This contract is
  unchanged by this decision;
- `Fraction` is approved only for exact, dimensionless
  quality-*characteristic* values (`CharacteristicAssessment.value`);
- a characteristic score must not be represented as `Decimal`, and an
  extracted measurement value must not be represented as `Fraction`; the two
  numeric domains have different semantic roles and must remain distinct.

**Float policy:** `float` is not an approved internal characteristic-score
representation for MVP v0.1. No calculator or domain model may convert an
exact characteristic score to `float` as part of calculation or propagation.

**Approved now — specification-level aggregate arithmetic exactness:**

- under `AGG-MVP-001` (Section 12), the specification-level mean for
  `C_file`, `V_file`, and `U_file` must use the same exact
  `fractions.Fraction` arithmetic already approved above for per-requirement
  values: sum of `Fraction`s divided by an integer count, with no
  intermediate rounding. This is a mechanical consequence of the
  already-approved exactness principle and the already-sourced mean formula
  (Section 12, "Derivable without a new scientific assumption"); it
  introduces no new scientific claim;
- this closes the aggregate-computation-exactness portion of `RQD-015`. It
  does not approve any display, percentage, or decimal-place rounding for
  presentation, which remains open below.

**Still open — presentation rounding (`RQD-015`):**

- console/reporting output precision, including whether a computed `Fraction`
  such as `1/3` (per-requirement) or `11/18` (aggregate) is displayed as a
  fraction, `0.33`/`0.61`, `0.333`/`0.611`, a percentage, or otherwise — a
  future presentation/reporter-layer decision, not made here;
- intermediate-versus-final rounding for display purposes only (the
  underlying calculation is already exact and unrounded, per above);
- tie-breaking rule for display;
- representation of unavailable (`UNKNOWN`/`NOT_APPLICABLE`) scores in
  presentation;
- specification aggregate output/display representation (Section 12).

No implementation may infer presentation rules from the number of decimal
places in the demonstration document. Specification-level aggregate
presentation precision remains open pending the reporter task. Approving
`fractions.Fraction` as the exact internal representation, for both
per-requirement values and the `AGG-MVP-001` aggregate, is the closed
calculation/representation layer; only its display remains open.

## 14. Missing-data policy

Chapter 2 and Chapter 4 establish these binding principles:

1. distinguish a computed value, an applicable value with missing required
   data, and a value that is not applicable;
2. an empty applicability denominator yields `NA`, not zero;
3. unavailable or not-applicable evidence must not be replaced by numeric zero;
4. critically incomplete evidence must not produce a falsely precise score.

Feature detection and assessment applicability are separate. A detector may use
`DETECTED`, `NOT_DETECTED`, or `UNRESOLVED` as processing states, while
characteristic/model criteria use the approved applicability states
`APPLICABLE`, `NOT_APPLICABLE`, and `UNKNOWN`. `NOT_DETECTED` and a missing
feature observation are not quality violations. `NOT_APPLICABLE` and `UNKNOWN`
are distinct and neither is numeric zero. An `APPLICABLE` criterion's
computed-versus-missing assessment state is a separate concern.

Section 7.16 now defines the minimal characteristic state representation:
`COMPUTED`, `NOT_APPLICABLE`, or `UNKNOWN`. `NOT_APPLICABLE` and `UNKNOWN`
require `value = None`; `COMPUTED` requires an approved rule and a value in
`[0,1]`. Mixed accepted-plus-incomplete outcomes retain accepted observations
and findings while withholding a value when the unresolved part is required.

`CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10) now
approve the following property-specific calculator-level propagation rules,
which must not be conflated with one another:

- **Completeness** uses all-three-required propagation: condition/context,
  expected result, and acceptance criterion are each mandatory under the MVP
  simplification, so any one of them being `UNRESOLVED` propagates the whole
  assessment to `UNKNOWN`, never to zero, pass, failure, or non-applicability.
  The other two criteria cannot compensate for the missing one.
- **Verifiability** uses material-dependency propagation: an unresolved
  candidate withholds the result only when resolving it could still change
  the numeric class (Section 9's worked examples V1-V4). An unresolved
  lower-tier candidate below an already-accepted acceptance criterion, or an
  unresolved lower-tier candidate below an already-accepted lower-tier path,
  does not withhold the result.
- **Unambiguity** uses signal-presence capping: once at least one accepted
  supported vague-term signal exists, the result computes to `1/2` regardless
  of any other unresolved candidate, because additional signals cannot lower
  the score and the current automated rule can never produce `0`. Only the
  absence of any accepted signal combined with a materially unresolved
  candidate withholds the result.

Console wording and general insufficient-evidence rules beyond these
property-specific cases remain unresolved. Property-level aggregation
behavior is resolved: Section 12's `AGG-MVP-001` (`APPROVED_FOR_MVP_V0.1`)
answers the two questions this section previously left open — Q1 (mixed
`COMPUTED`+`UNKNOWN`: excluded-and-tracked, candidate B) and Q2 (zero
`COMPUTED` with `UNKNOWN` present: aggregate state `UNKNOWN`, candidate A).
Detector confidence and evidence reliability are excluded from the current
MVP v0.1 characteristic contract. `RQD-020` remains open and non-blocking
while they remain excluded; proposing inclusion makes it blocking and
requires a separate scientific contract.

This decision approves: the calculator-level propagation portion of
`RQD-012` (the three property-specific rules above); the per-characteristic
withholding portion of `RQD-022`; and, for `RQD-015`, the exact mathematical
calculation semantics, the absence of calculator-level intermediate
rounding, and the internal production numeric representation
(`fractions.Fraction`), all recorded in Section 13. The `Fraction | None`
propagation described above is unaffected by this section's `UNKNOWN`/value
rules. The specification-level aggregation portions of `RQD-012` and
`RQD-022` are now closed for MVP v0.1: the empty-applicability-set NA rule
and `AGG-MVP-001`'s Q1/Q2 resolution (Section 12, "Operationalization
requiring researcher approval") are both `APPROVED_FOR_MVP_V0.1`. Only the
presentation/display-rounding portion of `RQD-015` remains open, unchanged
(Section 13); the aggregate-computation-exactness portion of `RQD-015` is
likewise now closed (Section 13).

## 15. Explainability requirements

Every numeric assessment must ultimately be traceable through:

```text
reported characteristic value
→ CALC-C/V/U-MVP-001 rule
→ contributing detector outcomes / observations
→ Evidence where applicable
→ requirement ID / source text
```

Every detected problem must carry enough evidence for a human-readable reason.
Section 7 approves separate evidence and observation contracts and the minimal
finding contract with stable requirement, rule, criterion, and Evidence
provenance. Evidence-based findings reference accepted Evidence without
changing it. Absence-based findings use requirement/rule/criterion provenance
and an empty evidence-reference tuple; they never fabricate a source span. A
criterion or evidence path that contributes a `0` to `C_i` or `V_i` because its
observation was `NOT_DETECTED`, or a complete scan that yields `U_i = 1`
because no signal was found, is an absence-based numeric contribution: it
requires no fabricated Evidence, and it must not itself be reported as a
`QUALITY_PROBLEM` finding merely because it contributed zero (or the maximum
Unambiguity value) to the calculation. Numeric score and Finding remain
separate model constructs. `FIND-U-VAGUE-001` is the only allocated finding
rule and produces a `SIGNAL`. All observation-to-`QUALITY_PROBLEM` conversions
remain unapproved under RQD-016; that gate is unrelated to, and unaffected by,
the newly approved numeric `CALC-C/V/U-MVP-001` calculation rules.

Chapter 2 requires the implementation to preserve the distinction among a
primary feature, a measure, and an interpreted indicator. It also requires an
automated linguistic or semantic signal to remain distinguishable from a
confirmed defect. A detector count must not be presented directly as a quality
percentage without an approved interpretation rule.

The reporter receives completed structured results and performs no calculation.

## 16. Reference examples

These examples are traceability candidates, drawn from truncated or
demonstrational source fragments. They do not contain approved MVP scores.
Section 7.16.8 contains the binding, numerically resolved characteristic-layer
cases for the current contract (Cases A-E); the values below are not
re-derived to that same binding standard, because these fragments' full
detector outcomes for every candidate feature were never established as
binding facts the way Cases A-E were. Per-requirement C/V/U are executable
under Sections 8-10; where a value below is not stated, it is because
re-deriving it here would require inventing detector outcomes beyond what
this specification has established, not because the calculation itself
remains blocked.

### Example A: vague wording

```text
Requirement:
“Маршрут доставки повинен швидко перераховуватися...”

Supported observation:
the application example identifies “швидко” as lacking a quantitative bound.

Candidate evidence:
vague_terms includes the exact span “швидко”.

Characteristic assessment:
Unambiguity: one accepted occurrence of “швидко” under `FIND-U-VAGUE-001` is
sufficient, by itself, for `CALC-U-MVP-001` to compute `U_i = 1/2`
(`assessment_rule_id = CALC-U-MVP-001`), regardless of how the elided
remainder of the sentence reads; no confirmed ambiguity or `QUALITY_PROBLEM`.
Completeness and Verifiability are not re-derived here: this fragment is
truncated (“...”) and its condition/result/acceptance/verification-method
detector outcomes are not established facts in this specification, unlike the
complete sentences in Section 7.16.8.

Requirement Quality Profile:
(C, V) not re-derived for this fragment; U = 1/2 per CALC-U-MVP-001
```

### Example B: measurable revised wording

```text
Requirement:
“...новий маршрут для 95 % запитів має бути сформований не більше ніж
за 4 с при навантаженні до 300 одночасних запитів.”

Supported observation:
the revision supplies quantitative bounds, units, load context, and an
observable result.

Candidate extracted features:
subject to approved definitions in Section 7.

Characteristic assessments:
C, V, and U are now executable in principle under Sections 8-10 once their
detector outcomes are known. This fragment is truncated (“...”) and is not one
of the binding Section 7.16.8 cases, so its exact detector outcomes for every
Completeness/Verifiability/Unambiguity input are not re-verified here; no
value is invented for it. See Section 7.16.8 for the binding numeric
reference cases.

Requirement Quality Profile:
(C, V, U) not re-derived for this fragment
```

### Example C: missing failure behavior

```text
Requirement:
“Поведінка системи у разі недоступності зовнішнього GPS-провайдера не
визначена.”

Supported observation:
the application example treats the absent failure response as incomplete.

Candidate evidence:
missing expected behavior for the stated failure condition.

Characteristic assessments:
the source example is qualitative evidence that an applicable missing-result
rule may be useful. Per-requirement C, V, and U are executable under Sections
8-10, but this requirement's exact detector outcomes (which of
condition/context, expected result, acceptance criterion, quantitative
constraint, verification method, and vague-term signal are DETECTED versus
NOT_DETECTED here) were never established as a binding fact in this
specification, unlike Cases A-E in Section 7.16.8. No value is invented for
it here; the current detector/applicability contract still cannot create an
absence-based `QUALITY_PROBLEM` regardless of the numeric outcome.

Requirement Quality Profile:
(C, V, U) not re-derived for this fragment
```

Researcher-approved examples must eventually include expected features,
characteristic assessments, requirement-quality profiles, explanations, and
boundary behavior, verified against the actual detector implementation.
Demonstration coefficients and scores in the source example must not be reused
as expected values.

## 17. Future extensions

The architecture should permit, but MVP v0.1 must not implement:

- cross-requirement consistency analysis;
- semantic NLP and replaceable learned extractors;
- traceability graphs and specification structure;
- ISO product-quality prediction;
- evidence coverage, reliability, and model uncertainty profiles;
- defect probability and risk models;
- risk aggregation and prioritization;
- corrective actions;
- versioned iterative reassessment;
- architecture, code, test, and operational evidence;
- API, UI, database, authentication, Docker, or cloud infrastructure.

Future findings may need the broader defect tuple described by the risk model,
including target, evidence, severity, confidence, stage, and version. MVP must
not conflate a detected quality problem with a calibrated risk probability, and
it need not implement those future fields now.

## 18. Current Research Decision Status

Chapter 2 resolves terminology and imposes methodological constraints, but it
does not turn the three MVP characteristics into executable per-line scoring
rules. Researcher approvals recorded below supersede earlier proposed or open
statuses for their MVP scope. `DEFERRED_FROM_MVP_V0.1` means the requested
scientific construct is intentionally not an implementation requirement for
this release.

No open item in this section may be answered by Codex without researcher
approval.

| ID | Research decision | Assessment or approved decision | Binding evidence or remaining gap | Current status | Blocked MVP component(s) |
| --- | --- | --- | --- | --- | --- |
| `RQD-001` | Confirm that MVP assesses artifact quality of each individual requirement, not Predicted Product Quality, and define its relation to specification-level quality. | `APPROVED_FOR_MVP_V0.1` | One non-empty input line is one `r_i`; Requirement Quality is artifact quality, its primary result is `A_i = (C_i, V_i, U_i)`, and it is strictly separate from Predicted Product Quality. | CLOSED FOR MVP v0.1 | None |
| `RQD-002` | Approve an operational definition of per-requirement Completeness. | `APPROVED_FOR_MVP_V0.1` | `CALC-C-MVP-001` (Section 8) approves the three-mandatory-criterion MVP simplification, the `(c_condition + c_result + c_acceptance) / 3` formula, and all-three-required unresolved propagation. Absence-based `QUALITY_PROBLEM` conversion remains separately gated under RQD-016. | CLOSED FOR MVP v0.1 — MVP-06 NO LONGER SCIENTIFICALLY BLOCKED BY THE COMPLETENESS FORMULA | None for the formula itself; `QUALITY_PROBLEM` conversion remains under RQD-016 |
| `RQD-003` | Approve an operational definition of per-requirement Verifiability. | `APPROVED_FOR_MVP_V0.1` | `CALC-V-MVP-001` (Section 9) approves the alternative-evidence-path formula (acceptance criterion → `1`; quantitative/method only → `1/2`; none after complete processing → `0`) and its material-dependency unresolved propagation. Absence-based `QUALITY_PROBLEM` conversion remains separately gated under RQD-016. | CLOSED FOR MVP v0.1 — MVP-07 NO LONGER SCIENTIFICALLY BLOCKED BY THE VERIFIABILITY FORMULA | None for the formula itself; `QUALITY_PROBLEM` conversion remains under RQD-016 |
| `RQD-004` | Approve an operational definition of per-requirement Unambiguity. | `AUTOMATED_SCALE_APPROVED_FOR_MVP_V0.1 / CONFIRMED_AMBIGUITY_OPEN` | `CALC-U-MVP-001` (Section 10) approves the executable automated MVP scale: no accepted supported signal after complete scanning → `1`; one or more → `1/2`. `0` remains reserved for a future, separately approved confirmed-material-ambiguity rule and is never produced by `CALC-U-MVP-001`. `FIND-U-VAGUE-001` remains a signal-only rule. | CLOSED FOR MVP v0.1 AUTOMATED SCALE — MVP-08 NO LONGER SCIENTIFICALLY BLOCKED BY THE UNAMBIGUITY NUMERIC RULE; confirmed-ambiguity `0` rule remains OPEN | Confirmed-ambiguity rule and any `QUALITY_PROBLEM` conversion remain under RQD-016 and future research |
| `RQD-005` | Approve the complete MVP `RequirementFeatures` registry, types, valid values, and consuming characteristics. | `APPROVED_FOR_MVP_V0.1` | Section 7 defines the six repeatable feature arrays, their singular `feature_id` values, and their primary characteristic consumers. The mapping is traceability only and authorizes no score contribution or double-counting rule by itself; score contribution for the mapped features is separately authorized by `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10). | CLOSED FOR MVP v0.1 | None directly; broader detector grammar remains gated under RQD-006/RQD-008 |
| `RQD-006` | Define detection rules for actor, action, object, condition, scenario, expected result, acceptance criterion, and verification method. | `PARTIALLY_APPROVED` | Section 7.14 allocates `COND-UK-001` for the exact five-marker first-production condition/context subset, `RESULT-UK-001` for the exact five-surface parser-assisted normative-modal expected-result subset, `ACCEPT-QUANT-001` for clause-level quantitative acceptance composition using only accepted result clauses, and `VERIFY-UK-001` for exactly construction A (`перевіряється`/`перевіряються` plus instrumental method), construction B (approved verification label, delimiter, and named method), and construction C (`визначено` plus an immediately following named test-method phrase). Section 7.15 approves the spaCy backend and neutral data/processing boundary. General expected-result grammar, non-modal/inherited normative force, coordinated results, general negation, implicit subjects, general condition attachment beyond `COND-UK-001`, non-numeric acceptance grammar, general declaration/verification predicates and labels, arbitrary method noun phrases, broader method coordination, artifact/reference interpretation, imperative or implicit procedures, semantic reproducibility inference, and richer procedure-content grammar remain open. Actor/action/object remain `DEFERRED_FROM_MVP_V0.1`. | PARTIALLY APPROVED / OPEN | MVP-04/05 detector coverage beyond the allocated first-production subsets. This does not block `CompletenessCalculator`, `VerifiabilityCalculator`, or `UnambiguityCalculator`: they consume `RequirementExtractionResult` domain data under `CALC-C/V/U-MVP-001` and can be implemented and tested against manually constructed extraction results independently of remaining detector grammar. |
| `RQD-007` | Approve vague-term vocabulary, languages, matching/normalization rules, exceptions, and versioning. | `APPROVED_FOR_MVP_V0.1` | The ten-entry `uk_vague_terms_v1` remains unchanged. Section 7.14 approves NFC plus Unicode `casefold()`, Unicode-aware token boundaries, one-or-more-Unicode-whitespace phrase separators, repeated ordering, and `LEFTMOST_LONGEST_NON_OVERLAPPING`. Each selected occurrence produces one Unambiguity `SIGNAL`; broader vocabulary coverage is future work. | CLOSED FOR MVP v0.1 | None for the seed matcher; the automated Unambiguity calculation itself is approved by `CALC-U-MVP-001` (Section 10) |
| `RQD-008` | Define detection and linkage rules for metric, threshold, comparator, unit, context, acceptance criterion, and expected result. | `PARTIALLY_APPROVED` | Sections 7.14.5.1, 7.14.6.6, and 7.15 approve the narrow conservative quantitative baseline, its `QUANT-001`/`QUANT-UK-001` first-production allocation, candidate precedence, diagnostic code, typed partial data representation, and the `ACCEPT-QUANT-001` result-span containment, clause-level deduplication, and judgeability contract. Issue #32 additionally approves the offset-preserving NFC/casefold comparator view and protected deferred-frequency exclusion without accepting `не рідше`. `до` remains `UPPER_BOUND` with inclusivity `UNRESOLVED` and is not a judgeable acceptance bound. Complex metric/context grammar, count-noun and nested quantitative roles, written-out numbers, generic ranges, and future accepted `не рідше` production grammar remain open/deferred. | PARTIALLY APPROVED / OPEN | MVP-04/05 detector coverage beyond the approved baseline. This does not block `VerifiabilityCalculator` (MVP-07) implementation or testing: `CALC-V-MVP-001` consumes whatever quantitative-constraint observations the extraction result already carries, and the calculator can be exercised against manually constructed inputs independently of remaining detector grammar. |
| `RQD-009` | Approve the evidence data structure. | `APPROVED_FOR_MVP_V0.1` | Section 7 approves exact source spans, zero-based Unicode code-point offsets with inclusive start/exclusive end, separate repeated occurrences, multiple evidence references per observation, and one span supporting multiple observations. | CLOSED FOR MVP v0.1 | None directly; detector and finding rules remain gated separately |
| `RQD-010` | Define exact formulas, contributions, penalties/rewards, coefficients, and thresholds for the three characteristic scores. | `PER-REQUIREMENT_MVP_FORMULAS_APPROVED / FUTURE_REFINEMENT_OPEN` | `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10) approve the per-requirement MVP v0.1 formulas, contributions, and unresolved-propagation rules for all three characteristics. This approval is scoped to MVP v0.1: it does not permanently close all future characteristic-formula research, including a future confirmed-material-ambiguity `0` rule or later Completeness/Verifiability refinements. | CLOSED FOR MVP v0.1 PER-REQUIREMENT FORMULAS | None for the approved MVP formulas; future refinements require separate researcher approval |
| `RQD-011` | Approve score direction and valid range for each characteristic and property-level aggregate. | `PER-REQUIREMENT_SCALE_CLOSED_FOR_MVP_V0.1 / SPECIFICATION_SCALE_CLOSED_FOR_MVP_V0.1` | Chapter 2 and Section 7.16 support `[0,1]` and upward compliance orientation. For MVP v0.1, the per-requirement scale/range is closed with the property-specific permitted value sets defined by each calculation rule: Completeness `{0,1/3,2/3,1}`, Verifiability `{0,1/2,1}`, Unambiguity `{1/2,1}` automated with `0` reserved. Section 12 ("Derivable without a new scientific assumption") now additionally closes the specification-level scale as a direct mathematical consequence of `AGG-MVP-001`: whenever a numeric aggregate exists, `C_file ∈ [0,1]`, `V_file ∈ [0,1]`, `U_file ∈ [1/2,1]` (the automated-MVP lower bound; `U_file = 0` remains impossible while the per-requirement `U_i = 0` rule is deferred under RQD-004), with the same upward compliance orientation as the per-requirement scales. `UNKNOWN`/`NOT_APPLICABLE` aggregates have `value = None` and are not numeric points on these scales. | CLOSED FOR MVP v0.1 — PER-REQUIREMENT AND SPECIFICATION-LEVEL SCALE BOTH CLOSED | None; specification-level aggregation (MVP-09/10) is no longer blocked by an open scale question |
| `RQD-012` | Define missing, unknown, not-applicable, insufficient-evidence, and optional-feature behavior. | `CALCULATOR-LEVEL_PROPAGATION_APPROVED / AGGREGATION_PROPAGATION_APPROVED_FOR_MVP_V0.1` | Sections 7.15-7.16 and 8-10 approve immutable detector outcomes, separate applicability, characteristic states, and the three property-specific calculator-level propagation rules (Completeness all-three-required, Verifiability material-dependency, Unambiguity signal-presence capping). Section 12's `AGG-MVP-001` now additionally approves the empty-applicability-set NA rule (direct match to `2.3_Система_метрик.docx` ¶43-44) and the researcher-approved resolution of the two remaining aggregation questions: Q1 (mixed `COMPUTED`+`UNKNOWN` — candidate B: mean of `COMPUTED` only, `UNKNOWN` excluded and tracked as `unknown_count`, never zero) and Q2 (zero `COMPUTED` with `UNKNOWN` present — candidate A: aggregate state `UNKNOWN`, value `None`, not `NOT_APPLICABLE`). | CALCULATOR-LEVEL PORTION AND SPECIFICATION-LEVEL AGGREGATION PROPAGATION (Q1/Q2, `AGG-MVP-001`, SECTION 12) BOTH CLOSED FOR MVP v0.1 | None for the aggregation rule itself; the `SpecificationQualityAggregator`/`SpecificationQualityProfile` implementation remains a separate, not-yet-started task |
| `RQD-013` | Define `RequirementQualityScore = f(Completeness, Verifiability, Unambiguity)`. | `DEFERRED_FROM_MVP_V0.1` | MVP v0.1 preserves `RequirementQualityProfile(C, V, U)` and intentionally has no scalar integrated requirement-quality score. Any future index requires separate researcher approval. | CLOSED FOR MVP v0.1 | None; scalar aggregation excluded |
| `RQD-014` | Define `FileQualityScore = g(Q_1, ..., Q_n)`. | `DEFERRED_FROM_MVP_V0.1` | MVP v0.1 preserves property-level means in `SpecificationQualityProfile(C_file, V_file, U_file)` and intentionally has no scalar integrated file-quality score. Exact missing/`UNKNOWN` propagation is now approved under `AGG-MVP-001` (RQD-012/RQD-022, Section 12); this row remains closed on the separate scalar-exclusion question, unaffected by that approval. | CLOSED FOR MVP v0.1 | None; scalar aggregation excluded |
| `RQD-015` | Approve numeric precision and rounding. | `INTERNAL_EXACT_REPRESENTATION_APPROVED (PER-REQUIREMENT AND AGGREGATE) / PRESENTATION_ROUNDING_OPEN` | `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Section 13) approve exact mathematical calculator formula semantics (`1/3`, `2/3`, `1/2`) with no calculator-level intermediate rounding. Section 13 now additionally approves Python standard-library `fractions.Fraction` as the internal production representation for per-requirement `CharacteristicAssessment.value` (`value: Fraction | None`, Section 7.16.2), distinct from the unchanged `Decimal` representation used for extracted quantitative measurement values, **and** for the `AGG-MVP-001` specification-level aggregate (Section 12): the aggregate mean over `COMPUTED` values is computed with the same exact, unrounded `Fraction` arithmetic, now that `AGG-MVP-001` fixes which values are included. No reporter/display presentation-precision or rounding policy is selected; that remains open. | CALCULATION-SEMANTICS, INTERNAL-REPRESENTATION, AND AGGREGATE-COMPUTATION-EXACTNESS PORTIONS ALL CLOSED FOR MVP v0.1; PRESENTATION/DISPLAY-ROUNDING PORTION REMAINS OPEN | MVP-06/07/08 are no longer blocked by numeric representation; MVP-09/10 specification aggregation is no longer blocked by numeric representation or inclusion-set semantics; MVP-11/12 reporter presentation remains blocked by the presentation/rounding portion of `RQD-015` only |
| `RQD-016` | Define the problem taxonomy and when an observation becomes a reported problem. | `FINDING_AND_SIGNAL_CONTRACT_APPROVED / QUALITY_PROBLEM_CONVERSION_OPEN` | Section 7.16.5 finalizes the minimal Finding representation, absence provenance, and `FIND-U-VAGUE-001`. The other five feature families produce no finding, and no `QUALITY_PROBLEM` rule is approved. Severity, probability, risk, confidence, priority, and corrective action are excluded. **This task approves no new `QUALITY_PROBLEM` rule**; this row remains open specifically, and only, for future `QUALITY_PROBLEM` conversion rules. | OPEN ONLY FOR `QUALITY_PROBLEM` RULES | MVP-06-08, MVP-10 |
| `RQD-017` | Provide approved reference requirements with expected features, scores, and explanations. | `BINDING_NUMERIC_CASES_APPROVED_FOR_MVP_V0.1` | Section 7.16.8 approves Cases A-E as binding numeric reference cases: A=(C=1,V=1,U=1), B=(C=1/3,V=0,U=1/2), C=(C=0,V=1/2,U=1), D=(C=0,V=UNKNOWN,U=1), E=(C=0,V=0,U=1), each with `assessment_rule_id` traceability. Downstream specification-level aggregation acceptance is not solved by this approval. | CLOSED FOR MVP v0.1 PER-REQUIREMENT NUMERIC REFERENCE CASES; AGGREGATION-LEVEL REFERENCE CASES REMAIN OPEN | Specification-level aggregation (MVP-09/10, MVP-12) |
| `RQD-018` | Define input-language, Unicode/case/punctuation, and multi-sentence or multi-clause behavior. | `APPROVED_FOR_MVP_V0.1` | UTF-8/Unicode input and original punctuation are preserved; linguistic matching may be case-insensitive; Ukrainian is the supported language-dependent profile; one input line remains one requirement even with multiple sentences or clauses. | CLOSED FOR MVP v0.1 | None |
| `RQD-019` | Decide how consistency, traceability, coverage, and other broader properties relate to the three-characteristic MVP. | `APPROVED_FOR_EXCLUSION_FROM_MVP_V0.1` | Per-line Consistency and Traceability, global Completeness, coverage, product-quality prediction, risk, and corrective actions require broader context and remain future extensions. | CLOSED FOR MVP v0.1 | None |
| `RQD-020` | Decide whether evidence coverage/reliability and detector confidence are represented in MVP. | `UNRESOLVED` | No confidence or evidence-reliability representation is approved in the current MVP v0.1 `CharacteristicAssessment` or `Finding` contracts. Whether such metadata belongs in MVP remains a researcher decision. | OPEN / UNRESOLVED — NON-BLOCKING WHILE EXCLUDED | Not blocking while these values remain excluded; blocking if inclusion is proposed, which requires a separate scientific contract. |
| `RQD-021` | Supply or supersede the Chapter 2/§2.3 definitions referenced by Chapter 4. | `RESOLVED_BY_CHAPTER_2` | Sections 2.1, 2.2, and especially 2.3 are now present and integrated into this specification. Their remaining operational gaps are tracked by the other RQDs. | CLOSED AS RESEARCH INPUT | None directly |
| `RQD-022` | Approve whether and how a score may be withheld when evidence is insufficient. | `PER-CHARACTERISTIC_WITHHOLDING_APPROVED / AGGREGATION_SUFFICIENCY_APPROVED_FOR_MVP_V0.1` | Section 7.16 and the three CALC rules (Sections 8-10) approve the exact per-characteristic withholding behavior needed by `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001`: `UNKNOWN` with `value = None` when a required detector input is unresolved (Completeness), when a material-dependency candidate could still change the numeric class (Verifiability), or when no signal exists and unresolved processing could still surface one (Unambiguity). Section 12's `AGG-MVP-001` additionally approves the empty-applicability-set NA rule and the Q1/Q2 resolution (mixed `COMPUTED`+`UNKNOWN` → excluded-and-tracked; zero `COMPUTED` with `UNKNOWN` present → aggregate `UNKNOWN`). Downstream aggregation sufficiency semantics (how withheld per-requirement values affect `C_file`/`V_file`/`U_file`) are now defined; console wording for presentation remains a separate, open reporter decision (Section 13). | PER-CHARACTERISTIC PORTION AND DOWNSTREAM AGGREGATION SUFFICIENCY (Q1/Q2, `AGG-MVP-001`, SECTION 12) BOTH CLOSED FOR MVP v0.1 | None for the aggregation-sufficiency rule itself; the `SpecificationQualityAggregator`/`SpecificationQualityProfile` implementation remains a separate, not-yet-started task |
| `RQD-023` | Define requirement types and the applicability sets/rules used by each candidate feature and characteristic in a text-only per-line MVP. | `APPROVED_MVP_SIMPLIFICATION` | MVP v0.1 performs no automatic requirement-type classification. Section 7.16.3 makes the conservative rule executable: only an approved observable criterion rule can yield `APPLICABLE` or `NOT_APPLICABLE`; otherwise applicability is `UNKNOWN`. `CALC-C-MVP-001` now supplies such a rule for the three Completeness candidates, as an explicit MVP simplification rather than automatic type inference; `CALC-V-MVP-001` makes Verifiability itself applicable to every supported requirement without needing a per-family mandatory-applicability rule for its three alternative evidence paths. | CLOSED FOR MVP v0.1 | None directly; per-requirement calculation rules are recorded under RQD-002/RQD-003 |

### 18.1 RQDs approved or closed for MVP v0.1

- `RQD-001`, `RQD-005`, `RQD-007`, `RQD-009`, `RQD-018`, `RQD-019`, and
  `RQD-023` are closed by explicit researcher approval for MVP v0.1.
- `RQD-021` remains closed because the requested Chapter 2 sources are present
  and traced.

### 18.2 Scalar-score RQDs deferred from MVP v0.1

- `RQD-013` is closed for MVP v0.1 by retaining
  `RequirementQualityProfile(C, V, U)` instead of inventing a scalar
  `RequirementQualityScore`.
- `RQD-014` is closed for MVP v0.1 by retaining property-level means in
  `SpecificationQualityProfile(C_file, V_file, U_file)` instead of inventing a
  scalar `FileQualityScore`. Section 12's approved `SpecificationQualityProfile`
  representation contract (`characteristic_id`, `state`, `value`,
  `computed_count`, `unknown_count`, `not_applicable_count`, `total_count`,
  `aggregation_rule_id`) carries no aggregate `findings`, weights, or
  combined C/V/U scoring, consistent with this deferral.

Any future scalar index requires a separate researcher-approved scientific
decision.

### 18.3 Remaining implementation-blocking RQDs

The remaining decisions are grouped into four approval gates:

1. **Remaining feature-operationalization and quality-problem gate:** Section
   7.14 records approved detector strategies and baselines. Section 7.15
   approves the backend and domain representation, while `RQD-006` remains
   open for parser/template grammar beyond the `COND-UK-001`,
   `RESULT-UK-001`, `ACCEPT-QUANT-001`, and `VERIFY-UK-001`
   first-production subsets and
   `RQD-008` remains open for complex metric/context grammar and nested
   representation. Section 7.16 finalizes the Finding contract and
   `FIND-U-VAGUE-001`; `RQD-016` remains open only for `QUALITY_PROBLEM`
   conversions. `RQD-007` is closed for the MVP seed matcher.
2. **Characteristic-calculation gate — CLOSED FOR MVP v0.1 PER-REQUIREMENT
   SCOPE:** `RQD-002`-`RQD-004` and the per-requirement portions of
   `RQD-010`-`RQD-012` and `RQD-022` are now approved. `CALC-C-MVP-001`,
   `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10) authorize the
   calculation logic for `C_i`, `V_i`, and the automated `U_i` in principle, so
   MVP-06, MVP-07, and MVP-08 are no longer blocked by open scientific
   formulas. This gate is now closed for both the calculation semantics and
   the internal production numeric representation: Section 13 approves
   `fractions.Fraction` as the concrete representation for `1/3` and `2/3`, so
   no separate implementer choice remains. Only the confirmed-material-
   ambiguity `U_i = 0` rule and any `QUALITY_PROBLEM` conversion (RQD-016)
   remain scientifically open within this gate.
3. **Property aggregation and numeric-contract gate — CLOSED FOR MVP v0.1
   AGGREGATION SEMANTICS; PRESENTATION PORTION STILL OPEN:** the
   empty-applicability-set NA sub-case, and the two previously-named open
   questions, of `RQD-012` and `RQD-022` are now closed by `AGG-MVP-001`
   (Section 12, `APPROVED_FOR_MVP_V0.1`): Q1 (mixed `COMPUTED`+`UNKNOWN` →
   mean of `COMPUTED` only, `UNKNOWN` excluded and tracked, never zero) and
   Q2 (zero `COMPUTED` with `UNKNOWN` present → aggregate state `UNKNOWN`,
   not `NOT_APPLICABLE`). Per-requirement calculation *semantics*, the
   internal production numeric representation, and now the specification-
   level aggregate arithmetic itself are all approved (exact mathematical
   values, no intermediate rounding, `fractions.Fraction`; Sections 12-13).
   Only the presentation/display-rounding portion of `RQD-015` remains open
   within this gate — it concerns reporter/console output only, not the
   aggregation algorithm, which is no longer blocking. `SpecificationQualityAggregator`
   and `SpecificationQualityProfile` may now be implemented against the
   approved `AGG-MVP-001` rule and representation contract (Section 12); this
   documentation-only decision does not itself implement them.
4. **Scientific acceptance gate:** the per-requirement portion of `RQD-017`
   is approved (Cases A-E are binding numeric reference cases).
   Specification-level numeric reference cases are illustrated in Section 12's
   worked examples but are not yet separately declared binding under
   `RQD-017`; that remains a distinct, not-yet-addressed decision, independent
   of gate 3 above (which is now closed).

`RQD-020` remains `OPEN / UNRESOLVED — NON-BLOCKING WHILE EXCLUDED`. It is not
part of the current implementation-blocking gates because confidence and
evidence-reliability values remain outside the approved contracts. If inclusion
is proposed, the decision becomes blocking and requires a separate scientific
contract.

### 18.4 Remaining design tensions

1. **Automated signal versus confirmed defect.** A deterministic text detector
   can identify risk signals, while the research definition of Unambiguity uses
   confirmed ambiguity at its boundary values. Treating every match as a defect
   would contradict that distinction.
2. **Applicability without type classification.** Requirement type remains
   unspecified, and MVP v0.1 still performs no automatic requirement-type
   inference. Feature and criterion contracts preserve `UNKNOWN` by default.
   `CALC-C-MVP-001` resolves this for Completeness by an explicit, narrow MVP
   simplification (all three criteria mandatory and `APPLICABLE`, not a
   universal claim), and `CALC-V-MVP-001` resolves it for Verifiability by
   making the characteristic itself applicable to every supported requirement
   while treating its three evidence families as non-mandatory alternatives
   rather than criteria each needing their own applicability rule.
3. **Local Completeness versus Verifiability overlap — resolved for the
   approved MVP formulas.** An accepted `acceptance_criterion` observation may
   be consumed once by `CALC-C-MVP-001` within Completeness and, independently,
   once by `CALC-V-MVP-001` as a Verifiability evidence path. `C_i` and `V_i`
   are independent components of the profile `A_i = (C_i, V_i, U_i)`; MVP v0.1
   has no scalar C/V aggregation, so consuming the same accepted observation
   in both characteristics is not cross-characteristic numeric double-counting.
   Within a single characteristic, repeated observations of the same criterion
   family still contribute at most once (Sections 8-9): `CALC-C-MVP-001`'s
   `c_acceptance` and `CALC-V-MVP-001`'s acceptance-criterion tier do not
   increase from multiple accepted observations in the same family.

Now that the per-requirement characteristic-calculation gate is closed,
including the internal production numeric representation (`fractions.Fraction`,
Section 13), the recommended sequence is:

1. implement and test `CompletenessCalculator`, `VerifiabilityCalculator`, and
   `UnambiguityCalculator` against manually constructed and currently
   extracted `RequirementExtractionResult` inputs, per `CALC-C-MVP-001`,
   `CALC-V-MVP-001`, and `CALC-U-MVP-001` (Sections 8-10), using
   `fractions.Fraction` for `CharacteristicAssessment.value` as approved in
   Section 13 — this is no longer blocked by an unselected numeric
   representation;
2. implement `SpecificationQualityAggregator` and `SpecificationQualityProfile`
   against the now-approved `AGG-MVP-001` rule and representation contract
   (Section 12, RQD-012/RQD-022 closed); only the presentation/display-
   rounding portion of `RQD-015` (gate 3 above) remains for the later
   reporter task and does not block this implementation;
3. broader detector grammar — parser/template operationalization beyond the
   `COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, and `VERIFY-UK-001`
   first-production subsets under `RQD-006`, and complex metric/context
   grammar under `RQD-008` — can evolve independently of steps 1-2, as future
   detector-coverage work, unless a later feature specifically requires it.
   It is not a prerequisite for calculator implementation.

The Section 7.15 domain/data-contract subset of MVP-01 may start only after
PR #19 is merged. Until the other applicable gates are approved, unapproved
detector rules and specification aggregation remain blocked; the overall
document stays `DRAFT` pending the remaining gates.

### 18.5 Downstream GitHub issue impact after characteristic-contract approval

The prior detector issues remain governed by Sections 7.14-7.15. The
characteristic implementation issues for Completeness, Verifiability, and
Unambiguity (MVP-06, MVP-07, MVP-08) are no longer blocked by open scientific
formulas: RQD-002-RQD-004 and the per-requirement portions of RQD-010-RQD-012
are approved via `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001`
(Sections 8-10), so implementation of their calculation logic is authorized in
principle. A future implementation issue may implement the Section 7.16
identifiers, assessment envelope, Finding representation, `FIND-U-VAGUE-001`
conversion, and the three numeric `CompletenessCalculator`,
`VerifiabilityCalculator`, and `UnambiguityCalculator` rules exactly as
specified in Sections 8-10 and 7.16.7-7.16.8. `RQD-015` has now selected and
recorded the internal production numeric representation in Section 13:
Python standard-library `fractions.Fraction`, used exactly as
`CharacteristicAssessment.value: Fraction | None` (Section 7.16.2). The
implementation issue does not select or re-derive that representation itself
— it must follow the recorded decision (`Fraction`) rather than inferring or
choosing a different type (`float`, `Decimal`, or otherwise) on its own. It
may still **not** implement a `QUALITY_PROBLEM` conversion (RQD-016 remains
open for that only), a confirmed-material-ambiguity `U_i = 0` rule, or
specification-level aggregation (`SpecificationQualityAggregator`,
`C_file`/`V_file`/`U_file`).

No issue may infer a `QUALITY_PROBLEM` or characteristic score beyond the
approved `CALC-C/V/U-MVP-001` formulas from detector or parser rules.
Specification aggregation is no longer scientifically blocked: the
specification-level missing/`UNKNOWN` propagation (Sections 12-14,
`AGG-MVP-001`) is now `APPROVED_FOR_MVP_V0.1`. A future implementation issue
may implement `SpecificationQualityAggregator` and `SpecificationQualityProfile`
exactly to the Section 12 representation contract; it must still not select
or invent a presentation/display-rounding policy, which remains open and is
reserved for the reporter task.
