# Requirements Quality Assessment Model Specification

**Status: DRAFT — requires researcher approval**

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

The individual textual requirement is the intended MVP unit of analysis, but
this selection is **PROPOSED FOR RESEARCHER APPROVAL**. Chapter 2 supports that
unit as a legitimate level of analysis; it does not by itself approve the exact
MVP reduction or its scoring and aggregation rules.

## 2. Scope of MVP v0.1

MVP v0.1 covers only this flow:

```text
UTF-8 requirements file
        ↓
deterministic textual and structural feature extraction
        ↓
Completeness   Verifiability   Unambiguity
        ↓
Requirement Quality
        ↓
File Quality
        ↓
explainable console output
```

The proposed unit of analysis is one individual textual software requirement,
represented in the input by one non-empty, trimmed line. This unit is
**PROPOSED FOR RESEARCHER APPROVAL** under RQD-001. The reader policy itself is
an approved engineering constraint: it preserves source line number and
processing order and assigns IDs `R001`, `R002`, and so on.

The following are outside MVP v0.1: database storage, REST API, web UI,
authentication, Docker, cloud infrastructure, custom neural-network training,
LLM API integration, risk scoring, defect-probability prediction, corrective
actions, iterative lifecycle reassessment, and advanced semantic consistency
analysis.

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
| Missing/not-applicable evidence is not zero | Requirement properties; metrics system; process and quality models | 2.3, paragraphs 16 and 39-42; 4.1 invariants; 4.2 feature formation | Three states and `NA` invariant defined; exact MVP representation incomplete | Yes | `PARTIALLY_DEFINED` |
| Completeness of an individual requirement | Requirement properties | 2.1 Table 2.1 and paragraphs 11-12; Table 2.3 | Semantic definition and evidence classes available; executable rule absent | Yes | `PARTIALLY_DEFINED` |
| Verifiability of an individual requirement | Requirement properties; metrics system | 2.1 Table 2.1 and paragraph 12; 2.3 paragraphs 17-21 | Semantic definition and evidence classes available; executable rule absent | Yes | `PARTIALLY_DEFINED` |
| Unambiguity of an individual requirement | Requirement properties | 2.1 Table 2.1 and paragraph 10; Table 2.3 | Semantic definition and signal classes available; confirmation rule absent | Yes | `PARTIALLY_DEFINED` |
| Consistency | Requirement properties; metrics system | 2.1 paragraphs 14-15; 2.3 paragraphs 28-30 | Defined primarily for a set of requirements | No, except as boundary context | `OUT_OF_SCOPE_V0.1` |
| Traceability | Requirement properties; requirements/product quality; metrics system | 2.1 paragraph 16; 2.2 paragraphs 23 and 27; 2.3 paragraphs 22-24 | Defined as a structural relationship property | No for text-only MVP | `OUT_OF_SCOPE_V0.1` |
| Individual property result `a_ij` | Requirement properties | 2.1 paragraphs 20-24 and Table 2.3 | Range and examples defined; property-specific rule incomplete | Yes | `PARTIALLY_DEFINED` |
| Specification-level property indicator `x_j = mean_i(a_ij)` | Requirement properties | 2.1 paragraphs 22-24 | Formula explicit for one property; applicability/overall-quality meaning incomplete | Potentially | `PARTIALLY_DEFINED` |
| Per-requirement feature/observation vector | Metrics system | 2.3 paragraphs 4 and 6-8 | `z_i` exists abstractly; concrete fields absent | Yes | `PARTIALLY_DEFINED` |
| Candidate structural fields `has_actor`, `has_action`, `has_object` | MVP-SPEC issue | Candidate list | No research definition in supplied references | Candidate only | `MISSING` |
| Conditions, expected reactions, criteria, metrics, thresholds, and units as signals | Requirement properties; requirements/product quality; metrics system | 2.1 Table 2.1; 2.2 Table 2.4; 2.3 Table 2.7 and paragraphs 17-21 | Semantic roles explicit; detector/linkage rules absent | Candidate | `PARTIALLY_DEFINED` |
| Vague-term and linguistic-smell evidence | Requirement properties; metrics system | 2.1 paragraph 10; 2.3 paragraphs 12-16 | Signal families explicit; vocabulary, matching, and confirmation absent | Candidate | `PARTIALLY_DEFINED` |
| Per-requirement Completeness score | None in supplied references | Not defined | No | Yes | `MISSING` |
| Per-requirement Verifiability score | None in supplied references | Not defined | No | Yes | `MISSING` |
| Per-requirement Unambiguity score | None in supplied references | Not defined | No | Yes | `MISSING` |
| Characteristic score range for MVP | Requirement properties | 2.1 `a_ij ∈ [0,1]` and Table 2.3 | `[0,1]` compliance orientation supported; exact scale rule per property absent | Yes | `PARTIALLY_DEFINED` |
| Requirements metric families and working dictionary | Metrics system | 2.3 Tables 2.7-2.8 | Aggregate formulas explicit; detector operands and applicability incomplete | Partially | `PARTIALLY_DEFINED` |
| Applicability set and empty-denominator `NA` | Metrics system | 2.3 paragraphs 13-16 and 39 | Principle explicit; per-requirement applicability rules absent | Yes | `PARTIALLY_DEFINED` |
| Requirement Quality Score from the three MVP characteristics | None in supplied references | Not defined | No | Yes | `MISSING` |
| File Quality Score from requirement scores | None in supplied references | Not defined | No | Yes | `MISSING` |
| Product-quality predictor `y_hat_j = F_theta_j(X_j, C)` | Quality model | 4.2, general prediction form | Abstract form and `[0,1]` range; model class/parameters unset | No | `OUT_OF_SCOPE_V0.1` |
| Logistic predictive baseline | Quality model and application example | 4.2 baseline; example Section 5 | Formula shown; example coefficients explicitly demonstrational | No | `OUT_OF_SCOPE_V0.1` |
| Context-weighted product-quality index `Q_int` | Quality model and application example | 4.2 aggregation; example Section 6 | General weighted form; weights context-dependent | Not directly | `OUT_OF_SCOPE_V0.1` |
| Non-compensated critical thresholds | Process and quality models | 4.1 checkpoints; 4.2 admissibility | Logical form exists; thresholds unset | Not currently | `OUT_OF_SCOPE_V0.1` |
| Finding/defect evidence | Risk model | 4.3 defect tuple | Conceptual structure exists | Yes for explainability | `PARTIALLY_DEFINED` |
| Local risk `r_ij` and risk aggregation | Risk model | 4.3 local risk and `Psi_j` | Local formula exists; inputs and aggregate operator require calibration | No | `OUT_OF_SCOPE_V0.1` |
| Corrective actions and iterative reassessment | Process and risk models | 4.1 feedback; 4.3 action tuple and loop | Conceptual structure exists | No | `OUT_OF_SCOPE_V0.1` |
| Manually approved reference cases for MVP scores | Requirement properties; metrics system; application example | 2.1 Tables 2.1-2.3; 2.3 Tables 2.7-2.8; example Sections 2-12 | Qualitative and aggregate examples exist; approved per-line expected scores absent | Yes | `PARTIALLY_DEFINED` |

## 4. Terminology and mathematical notation

### 4.1 Concept-definition and approval boundaries

| Concept | Explicitly defined by the dissertation | Derivable without a new scientific assumption | Implementation operationalization requiring researcher approval |
| --- | --- | --- | --- |
| **Requirement Quality** | A multidimensional quality of a requirements information artifact, evaluated through relevant properties at individual-requirement and/or specification level. It is not limited to grammatical correctness. | The MVP characteristics must remain named dimensions of requirement quality rather than be presented as observed or predicted product quality. | Selection of the MVP dimensions as sufficient, one-line unit semantics, and any single overall Requirement Quality Score. |
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

For MVP v0.1, the following symbols are reserved placeholders only:

- `C_i`: Completeness assessment for requirement `i`;
- `V_i`: Verifiability assessment for requirement `i`;
- `U_i`: Unambiguity assessment for requirement `i`;
- `Q_i`: overall Requirement Quality Score for requirement `i`;
- `Q_file`: File Quality Score for the analyzed input.

Their ranges and functions are unresolved. These names must not be confused with
the research document's product-quality set `Q` or contextual product index
`Q_int`.

Chapter 2 supports a `[0,1]` compliance direction for individual property
results `a_ik`, but adopting `C_i`, `V_i`, and `U_i` as exact instances of that
form, including binary versus graded behavior, remains an implementation
operationalization requiring researcher approval.

Status vocabulary in this document:

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
each MVP characteristic, an overall Requirement Quality Score, or a File
Quality Score. In particular, the formula for `x_k` aggregates one property and
must not be silently substituted for `Q_file`.

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
→ RequirementFeatures
→ CompletenessCalculator
→ VerifiabilityCalculator
→ UnambiguityCalculator
→ RequirementQualityAggregator
→ FileQualityAggregator
→ ConsoleReporter
```

The calculators depend only on approved domain data contracts and approved
rules in this specification. They do not depend on a reader, CLI, reporter,
feature-extraction implementation, or NLP library. The feature extractor does
not calculate any quality score. The reporter does not calculate or aggregate.

The broader research lifecycle includes architecture, implementation, testing,
operation, risk, corrective action, and reassessment. MVP boundaries must not
prevent later addition of versioned evidence, but no such subsystem is to be
implemented now.

## 6. Requirement representation

Chapter 2 explicitly supports two units: an individual requirement and a set of
requirements/specification. For MVP v0.1, selecting the individual textual
requirement as the analysis unit is **PROPOSED FOR RESEARCHER APPROVAL**. The
following representation is an approved engineering input contract from the
backlog; it does not by itself approve the scientific scoring unit:

| Field | Type | Meaning | Status |
| --- | --- | --- | --- |
| `id` | string | Automatically assigned processing-order ID such as `R001` | `DEFINED` |
| `source_line` | positive integer | Original one-based source line number | `DEFINED` |
| `text` | string | Non-empty UTF-8 requirement text after trimming leading/trailing whitespace | `DEFINED` |

Blank or whitespace-only lines are ignored. Requirement order matches the order
of non-empty source lines.

Whether one line may contain multiple sentences, which natural languages the
feature rules support, and how applicability is determined from text-only input
remain unresolved in RQD-018 and RQD-023.

## 7. RequirementFeatures

Chapter 2 defines methodological constraints for features and metrics but not a
complete executable feature schema. Every implemented metric must identify its
object and applicability set, use a reproducible algorithm, declare polarity,
record its data source and automation level, and preserve semantic context.

No feature is approved for implementation yet. The table below is a candidate
registry, not an executable schema. It distinguishes source-supported semantic
roles from proposed software fields.

| Identifier | Type | Semantic definition | Extraction evidence | Valid values/range | Source/reference | Consuming characteristics | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `has_actor` | Proposed boolean | Whether an accountable actor is explicitly expressed | Exact text span plus rule ID | Proposed `true/false` | Candidate in MVP-SPEC issue; not defined in supplied theory | Unresolved | `PROPOSED` |
| `has_action` | Proposed boolean | Whether required behavior/action is explicitly expressed | Exact text span plus rule ID | Proposed `true/false` | Candidate in MVP-SPEC issue; not defined in supplied theory | Unresolved | `PROPOSED` |
| `has_object` | Proposed boolean | Whether the action's affected object is explicit | Exact text span plus rule ID | Proposed `true/false` | Candidate in MVP-SPEC issue; not defined in supplied theory | Unresolved | `PROPOSED` |
| `has_condition` | Proposed boolean | Whether an applicable condition, trigger, or scenario is explicit | Exact text span plus rule ID | Proposed `true/false` | 2.1 completeness definition; 2.2 quality-evidence examples; 2.3 metric groups | Likely Completeness; approval required | `PROPOSED` |
| `has_metric` | Proposed boolean | Whether an observable measurable quantity is explicit | Exact quantity/criterion span plus rule ID | Proposed `true/false` | 2.1 verifiability discussion; 2.3 paragraphs 17-21 | Likely Verifiability; approval required | `PROPOSED` |
| `has_threshold` | Proposed boolean | Whether an acceptance boundary or target value is explicit | Exact comparator/value span plus rule ID | Proposed `true/false` | 2.1 Table 2.1; 2.3 paragraphs 17-21 | Likely Verifiability and possibly Unambiguity; approval required | `PROPOSED` |
| `has_unit` | Proposed boolean | Whether a detected numeric measure has an explicit unit | Exact unit span linked to its value | Proposed `true/false` | 2.3 paragraph 17 and Table 2.7 | Likely Verifiability; approval required | `PROPOSED` |
| `has_expected_result` | Proposed boolean | Whether the required expected reaction, observable outcome, or acceptance result is explicit | Exact outcome/criterion span plus rule ID | Proposed `true/false` | 2.1 completeness definition; 2.2 Table 2.4; 2.3 primary-feature definition | Likely Completeness and Verifiability; approval required | `PROPOSED` |
| `vague_terms` | Proposed evidence collection | Occurrences that signal possible multiple interpretations or subjectivity | Matched term, source span, rule/vocabulary version, and confirmation state | Proposed ordered collection; empty when none | 2.1 paragraph 10; 2.3 paragraphs 12-16; application examples | Likely Unambiguity; indicator is not automatically a confirmed defect | `PROPOSED` |

Chapter 2 explicitly supports the relevance of acceptance criteria, numerical
bounds, units, measurement conditions, expected reactions, failure scenarios,
and linguistic-smell signals. It also requires an applicability set and warns
that an automatically detected smell is an indicator rather than proof of a
defect. It does not define universal detectors. In particular, “у реальному
часі”, “швидко”, and “надійно” are examples, not an approved complete
vocabulary.

Any additional feature must either have explicit theoretical support or be
marked `PROPOSED` with a corresponding RQD and researcher approval.

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
of overlap with Verifiability are unresolved. Actor/action/object fields are not
defined by Chapter 2 and remain proposed implementation features.

Researcher decisions RQD-001, RQD-002, RQD-005, RQD-006, RQD-010, RQD-012,
RQD-019, and RQD-023 are required.

### Formula and output range

Chapter 2 places individual property results `a_ij` in `[0,1]` and orients them
toward degree of property compliance. It does not provide the exact rule for
`a_i,C`. Therefore the range/direction is `PARTIALLY_DEFINED`, while the
Completeness formula, criteria, penalties/rewards, and rounding remain
`MISSING`.

### Explanation and evidence requirements

The result must identify each contributing approved feature and preserve the
source evidence for missing or present elements. It must distinguish absence of
evidence from a numeric zero according to the research invariant.

### Reference examples

The initial GPS-provider statement in the application example explicitly says
that failure behavior is not defined; its revised form adds a condition and
observable outcomes. This supports a qualitative test case, not a numeric score.

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
criterion presence, and linkage among quantity/unit/condition/bound is not
defined. The mapping of those observations to `a_i,V` is also not defined.

Researcher decisions RQD-003, RQD-005, RQD-008, RQD-010, RQD-012, and RQD-023
are required.

### Formula and output range

Chapter 2 supports `[0,1]` compliance-oriented individual property results and
explicit set-level ratios, but not an exact per-requirement Verifiability score.
The per-line formula, penalties/rewards, and rounding remain `MISSING`.

### Explanation and evidence requirements

The assessment must point to the observable criterion, metric, threshold, unit,
or expected-result evidence that contributed to the result, or identify the
approved missing element without claiming a stronger semantic conclusion than
the detector supports.

### Reference examples

The application example contrasts “quickly recalculate” with a revised
requirement specifying four seconds under 300 concurrent requests. This supports
qualitative feature/evidence examples only. The example's numeric quality values
are demonstrational and are not expected MVP outputs.

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

The vocabulary, detector rules, context exceptions, confirmation procedure,
applicability rule, and mapping of multiple signals to the intermediate
`a_i,U` value are not defined. The text also does not resolve whether MVP uses
review-confirmed ambiguities or deterministic detector signals only.

Researcher decisions RQD-004, RQD-005, RQD-007, RQD-008, RQD-010, RQD-012,
RQD-016, and RQD-023 are required.

### Formula and output range

Chapter 2 provides direction and boundary examples for `a_i,U` and an aggregate
metric form, but no exact per-line mapping for intermediate values. The score is
therefore `PARTIALLY_DEFINED`; its executable formula and rounding remain
`MISSING`.

### Explanation and evidence requirements

Each ambiguity finding must identify the exact matched text and approved rule or
vocabulary entry. A count without the matched evidence is insufficient.

### Reference examples

The application example supplies useful positive findings for vague phrases and
revised bounded forms. It does not establish that every occurrence is always
ambiguous or provide a complete vocabulary.

## 11. Requirement Quality Score

The required implementation relationship is:

```text
CharacteristicScore(C_i, V_i, U_i)
        ↓
RequirementQualityScore(Q_i)
```

Chapter 2 defines individual property results `a_i,C`, `a_i,V`, and `a_i,U`, but
it deliberately preserves a multidimensional property profile rather than
defining a single quality score for one requirement. Chapter 4's `Q_int` formula
combines context-selected ISO product-quality characteristics, not the three MVP
qualities of one requirement. Reusing either the set-level property mean or
`Q_int` here would be an unsupported scientific adaptation.

The aggregation function, weights or non-compensated rules, missing-score
behavior, output range, and rounding are `MISSING` pending RQD-013.

## 12. File Quality Score

The required implementation relationship is:

```text
RequirementQualityScore(Q_1, ..., Q_n)
        ↓
FileQualityScore(Q_file)
```

Chapter 2 defines `x_k = (1/n) * sum_i(a_ik)` as the set-level indicator for one
specific requirement property. It does not define an overall file-quality value
aggregated from per-requirement `Q_i` values. It also warns against prematurely
reducing the multidimensional metric profile to one integrated requirements-
quality index. The application example scores a specification using
demonstrational property values; it does not aggregate independently calculated
line-level Requirement Quality Scores.

Arithmetic mean, weighted mean, minimum, penalty rules, and empty-file behavior
must not be assumed. They are `MISSING` pending RQD-014.

## 13. Numeric precision and rounding

Chapter 2 establishes `[0,1]` and increasing polarity for several property
metrics and preserves contextual polarity for process measures. It does not
establish an MVP precision or rounding contract. The following are unresolved:

- internal numeric representation;
- output precision;
- intermediate versus final rounding;
- tie-breaking rule;
- representation of unavailable scores.

No implementation may infer these rules from the number of decimal places in
the demonstration document. See RQD-015.

## 14. Missing-data policy

Chapter 2 and Chapter 4 establish these binding principles:

1. distinguish a computed value, an applicable value with missing required
   data, and a value that is not applicable;
2. an empty applicability denominator yields `NA`, not zero;
3. unavailable or not-applicable evidence must not be replaced by numeric zero;
4. critically incomplete evidence must not produce a falsely precise score.

These semantics are explicitly defined, but the concrete domain representation,
console wording, aggregation behavior, and distinction between “missing data”
and “insufficient evidence for a score” remain unresolved. Detector reliability
may be represented by a vector `D`/`Rel`, but Chapter 2 requires it to come from
separate validation rather than unsupported expert assignment. See RQD-012,
RQD-020, and RQD-022.

## 15. Explainability requirements

Every numeric assessment must ultimately be traceable through:

```text
reported value
→ approved model rule
→ contributing feature values
→ evidence or explicit absence condition
→ source requirement ID, line, and text
```

Every detected problem must carry enough evidence for a human-readable reason.
At minimum, the approved domain model will need a stable problem/rule ID, the
affected requirement ID, an explanation, and evidence. Exact span and evidence
structures remain subject to RQD-009 and RQD-016.

Chapter 2 requires the implementation to preserve the distinction among a
primary feature, a measure, and an interpreted indicator. It also requires an
automated linguistic or semantic signal to remain distinguishable from a
confirmed defect. A detector count must not be presented directly as a quality
percentage without an approved interpretation rule.

The reporter receives completed structured results and performs no calculation.

## 16. Reference examples

These examples are traceability candidates. They do not contain approved MVP
scores.

### Example A: vague wording

```text
Requirement:
“Маршрут доставки повинен швидко перераховуватися...”

Supported observation:
the application example identifies “швидко” as lacking a quantitative bound.

Candidate evidence:
vague_terms includes the exact span “швидко”.

Characteristic scores:
UNRESOLVED

Requirement Quality Score:
UNRESOLVED
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

Characteristic scores:
UNRESOLVED

Requirement Quality Score:
UNRESOLVED
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

Characteristic scores:
UNRESOLVED

Requirement Quality Score:
UNRESOLVED
```

Researcher-approved examples must eventually include expected features,
characteristic scores, requirement-quality score, explanations, and boundary
behavior. Demonstration coefficients and scores in the source example must not
be reused as expected values.

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

## 18. Research Decision Status After Chapter 2 Review

Chapter 2 resolves terminology and imposes methodological constraints, but it
does not turn the three MVP characteristics into executable per-line scoring
rules. `RESOLVED_BY_CHAPTER_2` means that the research-input request itself is
closed. `PARTIALLY_RESOLVED` means that Chapter 2 supplies a binding conceptual
definition or part of the contract while an implementation decision remains.
`ADDITIONAL_CONSTRAINTS` means that the decision is still open and Chapter 2
narrows the acceptable answer. `UNRESOLVED` means that Chapter 2 supplies no
answer sufficient for that decision.

No open item in this section may be answered by Codex without researcher
approval.

| ID | Research decision | Chapter 2 assessment | Binding evidence or remaining gap | Current status | Blocked MVP component(s) |
| --- | --- | --- | --- | --- | --- |
| `RQD-001` | Confirm that MVP assesses artifact quality of each individual requirement, not Predicted Product Quality, and define its relation to specification-level quality. | `PARTIALLY_RESOLVED` | Sections 2.1 and 2.2 explicitly distinguish individual-requirement properties, specification-level properties, and product-quality characteristics. For MVP v0.1, the individual textual requirement is the unit of analysis only as **PROPOSED FOR RESEARCHER APPROVAL**. | OPEN | MVP-01, MVP-06-09, MVP-12 |
| `RQD-002` | Approve an operational definition of per-requirement Completeness. | `PARTIALLY_RESOLVED` | Section 2.1 defines local Completeness through sufficient condition, expected reaction, and fulfilment-criterion information, with elements dependent on requirement type/template. It supplies no deterministic detection or scoring rule. | OPEN | MVP-04/05 as applicable, MVP-06 |
| `RQD-003` | Approve an operational definition of per-requirement Verifiability. | `PARTIALLY_RESOLVED` | Sections 2.1 and 2.3 define reproducible verification and relevant evidence, and give set-level ratios. They do not define an `a_i,V` calculation for one line. | OPEN | MVP-04/05 as applicable, MVP-07 |
| `RQD-004` | Approve an operational definition of per-requirement Unambiguity. | `PARTIALLY_RESOLVED` | Section 2.1 defines one justified interpretation and gives boundary meanings for `a_i,U`; Sections 2.1 and 2.3 treat linguistic matches as signals rather than proof. Detector, confirmation, applicability, and intermediate-value rules remain absent. | OPEN | MVP-05, MVP-08 |
| `RQD-005` | Approve the complete MVP `RequirementFeatures` registry, types, valid values, and consuming characteristics. | `ADDITIONAL_CONSTRAINTS` | Section 2.3 requires every metric to identify its object, reproducible algorithm, polarity, data source/automation, and semantic context, and distinguishes feature, measure, and indicator. It does not define the MVP field registry. | OPEN | MVP-01, MVP-03-08 |
| `RQD-006` | Define detection rules for actor, action, object, condition, scenario, and expected result. | `PARTIALLY_RESOLVED` | Section 2.1 supports condition, expected reaction, and fulfilment criterion as Completeness evidence. It neither requires the proposed actor/action/object schema nor supplies syntactic or semantic boundaries. | OPEN | MVP-04 and consuming calculators |
| `RQD-007` | Approve vague-term vocabulary, languages, matching/normalization rules, exceptions, and versioning. | `ADDITIONAL_CONSTRAINTS` | Sections 2.1 and 2.3 identify smell families and require a signal to remain distinct from a confirmed ambiguity. They do not supply a closed vocabulary or executable match rules. | OPEN | MVP-05, MVP-08 |
| `RQD-008` | Define detection and linkage rules for metric, threshold, comparator, unit, context, acceptance criterion, and expected result. | `PARTIALLY_RESOLVED` | Sections 2.1 and 2.3 identify observable quantity, unit, measurement conditions, admissible bound, acceptance criterion, and verification method as relevant evidence when applicable. Exact detection, applicability, and linkage are missing. | OPEN | MVP-04/05, MVP-07 |
| `RQD-009` | Approve the evidence data structure. | `ADDITIONAL_CONSTRAINTS` | Section 2.3 requires reproducibility, source traceability, and separation of observation from interpretation; Chapter 4 requires explanations. Span, ordering, multiplicity, rule-ID, confirmation-state, and absent-evidence representations remain open. | OPEN | MVP-01, MVP-03-10 |
| `RQD-010` | Define exact formulas, contributions, penalties/rewards, coefficients, and thresholds for the three characteristic scores. | `PARTIALLY_RESOLVED` | Section 2.1 places individual property values `a_ij` in `[0,1]`; Section 2.3 supplies generic and set-level metrics. Neither supplies executable per-requirement formulas for `a_i,C`, `a_i,V`, and intermediate `a_i,U`. | OPEN | MVP-06-08 |
| `RQD-011` | Approve score direction and valid range for each characteristic and both aggregate levels. | `PARTIALLY_RESOLVED` | Chapter 2 supports `[0,1]` and upward compliance orientation for individual properties and principal property metrics. It does not approve binary versus graded MVP scores, a Requirement Quality range, or a file aggregate range. | OPEN | MVP-01, MVP-06-10 |
| `RQD-012` | Define missing, unknown, not-applicable, insufficient-evidence, and optional-feature behavior. | `PARTIALLY_RESOLVED` | Section 2.3 binds three states—computed, applicable but missing data, and not applicable—and forbids converting an empty applicability set to zero. Concrete domain states and calculator/aggregation behavior remain open. | OPEN | MVP-01, MVP-06-10 |
| `RQD-013` | Define `RequirementQualityScore = f(Completeness, Verifiability, Unambiguity)`. | `UNRESOLVED` | Chapter 2 intentionally preserves a multidimensional requirements-property profile. Chapter 4's `Q_int` concerns Predicted Product Quality and cannot be reused. | OPEN | MVP-09, MVP-10-12 |
| `RQD-014` | Define `FileQualityScore = g(Q_1, ..., Q_n)`. | `ADDITIONAL_CONSTRAINTS` | Section 2.1 defines a set mean `x_k` for one property, not an aggregate of per-requirement overall scores. Section 2.3 cautions against an unsupported single integrated index. | OPEN | MVP-09, MVP-10-12 |
| `RQD-015` | Approve numeric precision and rounding. | `UNRESOLVED` | Chapter 2 gives no calculation, aggregation, or presentation rounding policy. | OPEN | MVP-06-12 |
| `RQD-016` | Define the problem taxonomy and when an observation becomes a reported problem. | `PARTIALLY_RESOLVED` | Chapter 2 identifies property defect families and distinguishes a raw automated signal from a confirmed defect. MVP problem IDs, conversion rules, severity, and reporter wording remain open. | OPEN | MVP-01, MVP-06-08, MVP-10 |
| `RQD-017` | Provide approved reference requirements with expected features, scores, and explanations. | `ADDITIONAL_CONSTRAINTS` | Chapter 2 provides qualitative cases and working set-level formula examples, but no approved expected per-line MVP feature vectors or scores. Examples must respect applicability and signal/confirmation distinctions. | OPEN | MVP-04-09, MVP-12 |
| `RQD-018` | Define input-language, Unicode/case/punctuation, and multi-sentence or multi-clause behavior. | `UNRESOLVED` | Chapter 2 uses examples and linguistic categories but specifies no implementation language or normalization contract. | OPEN | MVP-03-05, MVP-12 |
| `RQD-019` | Decide how consistency, traceability, coverage, and other broader properties relate to the three-characteristic MVP. | `PARTIALLY_RESOLVED` | Sections 2.1-2.3 define Consistency as conflict-free relations at set level, Traceability as artifact links, and global Completeness as specification coverage. Their theoretical scope is clearer, but inclusion as supporting features or explicit exclusion from MVP still needs approval. | OPEN | MVP-01, MVP-04-08 |
| `RQD-020` | Decide whether evidence coverage/reliability and detector confidence are represented in MVP. | `PARTIALLY_RESOLVED` | Section 2.3 permits an applicability mask `B` and optional reliability vector `D`/`Rel`, but requires empirical validation rather than invented confidence values. MVP inclusion and semantics remain open. | OPEN, CONDITIONALLY BLOCKING | MVP-01, MVP-06-10 if included |
| `RQD-021` | Supply or supersede the Chapter 2/§2.3 definitions referenced by Chapter 4. | `RESOLVED_BY_CHAPTER_2` | Sections 2.1, 2.2, and especially 2.3 are now present and integrated into this specification. Their remaining operational gaps are tracked by the other RQDs. | CLOSED AS RESEARCH INPUT | None directly |
| `RQD-022` | Approve whether and how a score may be withheld when evidence is insufficient. | `PARTIALLY_RESOLVED` | Chapter 2 and Chapter 4 prohibit false precision and distinguish missing from not applicable. Console wording and propagation into requirement/file aggregates remain open. | OPEN | MVP-06-10, MVP-12 |
| `RQD-023` | Define requirement types and the applicability sets/rules used by each candidate feature and characteristic in a text-only per-line MVP. | `UNRESOLVED` | Section 2.3 makes `R_k^app` essential and requires `NA` for an empty applicability set, while Sections 2.1 and 2.3 make several elements type-dependent. The input contract supplies only line text and no approved type classifier or metadata. | OPEN | MVP-01, MVP-04-08, MVP-12 |

### 18.1 RQDs resolved by Chapter 2

- `RQD-021` is closed because the requested Chapter 2 sources are now present
  and traced. This does not close the scientific operationalization decisions
  recorded separately.

### 18.2 RQDs partially resolved by Chapter 2

- `RQD-001`, `RQD-002`, `RQD-003`, `RQD-004`, `RQD-006`, `RQD-008`,
  `RQD-010`, `RQD-011`, `RQD-012`, `RQD-016`, `RQD-019`, `RQD-020`, and
  `RQD-022`.

These items now have binding conceptual definitions or partial semantics, but
still require researcher-approved implementation contracts.

### 18.3 RQDs receiving additional constraints from Chapter 2

- `RQD-005`, `RQD-007`, `RQD-009`, `RQD-014`, and `RQD-017`.

They remain open; Chapter 2 narrows acceptable solutions through applicability,
reproducibility, evidence, confirmation, and multidimensionality constraints.

### 18.4 RQDs still unresolved after Chapter 2

- `RQD-013`, `RQD-015`, `RQD-018`, and `RQD-023`.

All partially resolved and additional-constraint items also remain open for
implementation even though Chapter 2 contributed evidence to them.

### 18.5 New contradictions or design tensions exposed by Chapter 2

1. **Unit of analysis.** Chapter 2 supports individual-requirement assessment
   but also defines essential set-level properties. The MVP choice of one text
   line as one requirement is therefore **PROPOSED FOR RESEARCHER APPROVAL**, not
   a dissertation conclusion.
2. **Multidimensional profile versus mandatory overall scores.** Chapter 2
   preserves a vector of property metrics and warns against premature collapse
   into one index, while the MVP output contract asks for one overall score per
   requirement and one aggregate file score.
3. **Automated signal versus confirmed defect.** A deterministic text detector
   can identify risk signals, while the research definition of Unambiguity uses
   confirmed ambiguity at its boundary values. Treating every match as a defect
   would contradict that distinction.
4. **Applicability versus text-only input.** Chapter 2 requires type- and
   applicability-aware denominators and `NA` behavior, while MVP input contains
   no approved requirement type or metadata.
5. **Local Completeness versus Verifiability overlap.** A fulfilment criterion
   contributes to local Completeness and also provides Verifiability evidence.
   Any shared feature and non-duplication rule requires approval.
6. **Property-specific set means versus File Quality.** The defined `x_k` is a
   mean for one property. It is not the requested aggregate of overall
   per-requirement quality scores and cannot silently replace it.
7. **Set-level properties versus per-line processing.** Consistency,
   Traceability, and global coverage require relationships or expected sets
   that cannot be established from an isolated line alone.

### 18.6 Reduced implementation-blocking RQD list

The remaining decisions can be handled as five approval gates rather than as
an undifferentiated list:

1. **Scope and applicability gate:** `RQD-001`, `RQD-019`, `RQD-023`.
2. **Feature and evidence contract gate:** `RQD-005`-`RQD-009`, `RQD-016`,
   `RQD-018`.
3. **Characteristic-calculation gate:** `RQD-002`-`RQD-004`, `RQD-010`-
   `RQD-012`, `RQD-022`.
4. **Aggregation and numeric-contract gate:** `RQD-013`-`RQD-015`.
5. **Scientific acceptance gate:** `RQD-017`.

`RQD-020` is conditionally blocking only if confidence or evidence-reliability
values are included in MVP v0.1. `RQD-021` is resolved and no longer blocks
implementation.

Until the applicable implementation gates are approved and this document's
status is changed from `DRAFT`, feature rules, characteristic calculators, and
quality aggregators remain blocked.
