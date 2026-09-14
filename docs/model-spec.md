# Requirements Quality Assessment Model Specification

**Status: DRAFT — approved scope decisions incorporated; operational rules remain**

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
| Missing/not-applicable evidence is not zero | Requirement properties; metrics system; process and quality models; approved RQD-023 | 2.3, paragraphs 16 and 39-42; 4.1 invariants; 4.2 feature formation | Applicability states `APPLICABLE`, `NOT_APPLICABLE`, and `UNKNOWN` are approved; exact calculator propagation remains incomplete | Yes | `PARTIALLY_DEFINED` |
| Completeness of an individual requirement | Requirement properties | 2.1 Table 2.1 and paragraphs 11-12; Table 2.3 | Semantic definition and evidence classes available; executable rule absent | Yes | `PARTIALLY_DEFINED` |
| Verifiability of an individual requirement | Requirement properties; metrics system | 2.1 Table 2.1 and paragraph 12; 2.3 paragraphs 17-21 | Semantic definition and evidence classes available; executable rule absent | Yes | `PARTIALLY_DEFINED` |
| Unambiguity of an individual requirement | Requirement properties | 2.1 Table 2.1 and paragraph 10; Table 2.3 | Semantic definition and signal classes available; confirmation rule absent | Yes | `PARTIALLY_DEFINED` |
| Consistency | Requirement properties; metrics system | 2.1 paragraphs 14-15; 2.3 paragraphs 28-30 | Defined primarily for a set of requirements | No, except as boundary context | `OUT_OF_SCOPE_V0.1` |
| Traceability | Requirement properties; requirements/product quality; metrics system | 2.1 paragraph 16; 2.2 paragraphs 23 and 27; 2.3 paragraphs 22-24 | Defined as a structural relationship property | No for text-only MVP | `OUT_OF_SCOPE_V0.1` |
| Individual property result `a_ij` | Requirement properties | 2.1 paragraphs 20-24 and Table 2.3 | Range and examples defined; property-specific rule incomplete | Yes | `PARTIALLY_DEFINED` |
| Specification-level property indicator `x_j = mean_i(a_ij)` | Requirement properties; approved aggregation correction | 2.1 paragraphs 22-24 | Property-level mean is approved for computed/applicable values; exact missing/`UNKNOWN` propagation remains incomplete | Yes | `PARTIALLY_DEFINED` |
| Per-requirement feature/observation registry | Metrics system; researcher-approved Section 7 contract | 2.3 paragraphs 4 and 6-8; Sections 7.2 and 7.14 | Six repeatable conceptual feature collections, primary consumers, and approved detector baselines are defined; concrete parser/domain operationalization remains open | Yes | `DEFINED` at registry level; detectors `PARTIALLY_DEFINED` |
| Candidate structural fields `has_actor`, `has_action`, `has_object` | MVP-SPEC issue; researcher-approved Section 7.11 disposition | Candidate list and Section 7.11 | No research definition in supplied references | No; possible optional future observations only | `DEFERRED_FROM_MVP_V0.1` |
| Condition/context, expected result, acceptance criterion, linked quantitative constraint, and explicit verification method | Requirement properties; requirements/product quality; metrics system; static and dynamic methods; researcher-approved Section 7.14 | 2.1 Table 2.1 and paragraphs 11-12; 2.2 Tables 2.4-2.5; 2.3 Table 2.7 and paragraphs 17-21; 3.1 paragraph 13; 3.2 Table 3.4; Section 7.14 | Semantic features, conservative detector strategies, partial observations, and primary consumers approved; concrete parser/template rules and complex metric/context grammar remain open | Yes | `PARTIALLY_APPROVED` |
| Vague-term and linguistic-smell evidence | Requirement properties; metrics system; dynamic methods; application example; researcher-approved Sections 7.8 and 7.14 | 2.1 paragraph 10; 2.3 paragraphs 12-16; 3.2 paragraph 10; application Sections 2-3, 7-8, and 13 | `uk_vague_terms_v1` and exact MVP seed-matching mechanics approved; richer linguistic coverage deferred without keeping `RQD-007` open | Yes | `APPROVED_FOR_MVP_V0.1` |
| Per-requirement Completeness score | None in supplied references | Not defined | No | Yes | `MISSING` |
| Per-requirement Verifiability score | None in supplied references | Not defined | No | Yes | `MISSING` |
| Per-requirement Unambiguity score | None in supplied references | Not defined | No | Yes | `MISSING` |
| Characteristic score range for MVP | Requirement properties | 2.1 `a_ij ∈ [0,1]` and Table 2.3 | `[0,1]` compliance orientation supported; exact scale rule per property absent | Yes | `PARTIALLY_DEFINED` |
| Requirements metric families and working dictionary | Metrics system | 2.3 Tables 2.7-2.8 | Aggregate formulas explicit; detector operands and applicability incomplete | Partially | `PARTIALLY_DEFINED` |
| Applicability set and empty-denominator `NA` | Metrics system | 2.3 paragraphs 13-16 and 39 | Principle explicit; per-requirement applicability rules absent | Yes | `PARTIALLY_DEFINED` |
| Scalar Requirement Quality Score from the three MVP characteristics | None in supplied references; approved RQD-013 disposition | Not defined and intentionally deferred | No | No | `OUT_OF_SCOPE_V0.1` |
| Scalar File Quality Score from requirement scores | None in supplied references; approved RQD-014 disposition | Not defined and intentionally deferred | No | No | `OUT_OF_SCOPE_V0.1` |
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
→ RequirementFeatures
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
policy, and core finding taxonomy. Deterministic structural/semantic detectors,
quantitative parsing/linkage algorithms, and observation-to-quality-problem
conversion rules remain open. The overall model specification therefore remains
`DRAFT`, and feature extraction is not yet approved for implementation.

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
RequirementFeatures / FeatureObservation + Evidence
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

### 7.1 Separation of contract concepts

| Concept | Meaning in this draft | May be produced by `FeatureExtractor`? | Scientific interpretation? | Status |
| --- | --- | --- | --- | --- |
| Raw text | The trimmed original requirement text, with original punctuation preserved | Input only | None | `DEFINED` by the approved input contract |
| `Evidence` | An exact source-text span explaining why a detector produced an observation | Yes | None by itself | `APPROVED_FOR_MVP_V0.1` |
| `FeatureObservation` | An explicit detected observation with linked evidence; optional detection processing state is separate from criterion applicability | Yes | It states detection only, not quality | Conceptual contract `APPROVED_FOR_MVP_V0.1`; detector algorithms open |
| `Finding` | A downstream interpretation of observations under an approved model rule | No | Either a `SIGNAL` or an established `QUALITY_PROBLEM` | Core taxonomy `PARTIALLY_APPROVED`; conversion rules open |
| `CharacteristicAssessment` | A later result for Completeness, Verifiability, or Unambiguity | No | Determined only by an approved characteristic rule | Outside this approval gate; calculation remains unresolved |

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
| `condition_context` | `condition_contexts[]` | An explicit condition, trigger, scenario, execution context, or measurement context under which behavior or a criterion applies | Completeness | Source-attested marker strategy and conservative boundaries approved; ambiguous attachment remains `UNRESOLVED` under open `RQD-006` |
| `expected_result` | `expected_results[]` | An explicit expected reaction, observable outcome, or required behavior | Completeness | `PARSER_ASSISTANCE_REQUIRED` strategy approved; concrete parser operationalization remains open under `RQD-006` |
| `acceptance_criterion` | `acceptance_criteria[]` | An explicit fulfilment or acceptance condition against which execution or an observation can be judged | Completeness and Verifiability | Narrow quantitative baseline and parser-assisted non-numeric strategy approved; concrete grammar remains open under `RQD-006`/`RQD-008` |
| `quantitative_constraint` | `quantitative_constraints[]` | A linked measurable target or bound whose metric, comparator, value, unit, and context remain associated | Verifiability | Partial observations and conservative linkage approved; complex grammar remains open under `RQD-008` |
| `verification_method` | `verification_methods[]` | An explicitly stated reproducible verification method in the requirement text | Verifiability | Explicit-only strategy approved; concrete grammar/template operationalization remains open |
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
| Acceptance criterion | A fulfilment condition that makes a requirement judgeable; Chapter 3 gives examples including a threshold, expected behavior, admissible range, or condition | Not universally established; Chapter 2 explicitly uses an applicability set | Yes in the approved representation | A narrow quantitative baseline is approved; non-numeric parser grammar and criterion sufficiency remain open | Yes; it may share a span with an expected result or quantitative constraint |
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
criterion applicability, and any required absence semantics. Those rules remain
unapproved under the characteristic-calculation gate.

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
metric:      unresolved
comparator:  <=
value:       2
unit:        seconds
context:     unresolved
```

For the source example “Час відгуку ≤ 2 с при 500 одночасних користувачах”,
the response-time metric, `≤` comparator, value `2`, unit `с`, and load context
must remain associated. Likewise, the worked revision linking a four-second
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

Shapes such as `UK-VAGUE-001`, `QUANT-COMP-001`, and `COND-001` are conceptual
examples only. Semantic versions belong in registry metadata. This approval does
not create the production rule-ID registry.

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
categories do not constitute a production vocabulary or detector.

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
scientific rule is approved. No method-name vocabulary or procedure-sufficiency
detector is approved by this decision.

### 7.10 Partially approved finding taxonomy

```text
FindingKind:
    SIGNAL
    QUALITY_PROBLEM

Finding:
    code
    characteristic
    kind
    explanation
    evidence_refs[]
    rule_id
```

This core taxonomy and conceptual structure are approved for MVP v0.1:

- `code` is a stable machine-readable finding category, distinct from the
  detector's `rule_id`;
- `characteristic` identifies Completeness, Verifiability, or Unambiguity;
- `kind` preserves whether the result is an automated indicator requiring
  interpretation/model logic (`SIGNAL`) or a violation established by an
  approved characteristic rule (`QUALITY_PROBLEM`);
- `explanation` states what the approved rule concluded without overstating the
  evidence;
- `evidence_refs` supports direct explanation against original text;
- `rule_id` identifies the approved interpretation rule that created the
  finding.

The `FeatureExtractor` emits observations and evidence, not confirmed quality
defects. A downstream approved characteristic/model rule may transform
observations into findings. Every vague-term occurrence produces only an
ambiguity-related `SIGNAL`. It may never become `QUALITY_PROBLEM` from the match
alone. A `QUALITY_PROBLEM` requires an approved characteristic rule that
establishes the violation.

Severity, probability, risk, numeric confidence, calibrated certainty, and
evidence-reliability values are deliberately absent. Chapter 4 places some of
these concepts in a broader defect/risk tuple, but they are outside MVP v0.1.
`RQD-020` remains unresolved. Under `RQD-016`, the extractor-side contract is
approved for MVP v0.1: each accepted vague-term occurrence produces one
Unambiguity `SIGNAL`, while the other five feature families produce observations
and evidence only. Exact observation-to-`QUALITY_PROBLEM` conversion rules remain
open in the characteristic-calculation gate.

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
v0.1 and approve the extractor-side portion of `RQD-016`. Implementation remains
blocked by:

1. concrete, replaceable parser/template operationalization for the approved
   `condition_context`, `expected_result`, `acceptance_criterion`, and
   `verification_method` strategies (`RQD-006`);
2. complex quantitative grammar, ambiguous metric/context attachment, nested
   constraint representation, and deliberately deferred numeric/range forms
   beyond the approved baseline (`RQD-008`);
3. criterion-applicability, missing-feature, and absence semantics used by each
   characteristic calculation (`RQD-002`-`RQD-004`, `RQD-010`-`RQD-012`, and
   `RQD-022`);
4. exact observation-to-`QUALITY_PROBLEM` conversion rules and any handling of
   overlapping evidence in characteristic calculations (`RQD-016` and the
   characteristic-calculation gate);
5. the production rule-ID registry and detector descriptions associated with
   approved evidence;
6. the still-unresolved decision on whether any evidence reliability or
   detector-confidence representation belongs in MVP (`RQD-020`). No such value
   is approved by this section.

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
behind the `FeatureExtractor` boundary. No NLP library is selected.

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
boundary. `за умови` does not occur in the supplied corpus. They are therefore
not `SOURCE-ATTESTED`
requirement-example markers. Adding either to an executable marker inventory
would be a **PROPOSED IMPLEMENTATION EXTENSION** requiring separate approval.

The approved detector strategy accepts a condition only when a source-attested marker
heads a non-empty phrase or clause and that phrase/clause explicitly modifies a
required behavior, expected result, acceptance criterion, or quantitative
bound. For a leading `якщо` clause, the evidence begins at `якщо` and ends
immediately before the delimiting comma. For a postposed `у разі`, `під час`,
`після`, or `при` phrase, evidence begins at the marker and ends at the phrase
boundary, excluding following punctuation. A bare marker, an incomplete
complement, or a marker whose attachment cannot be determined is not `DETECTED`.
If a candidate exists but attachment or boundary is not deterministic, the
result is `UNRESOLVED`.

Coordinated conditions that have independent heads become separate observations.
A shared condition is not duplicated merely because it governs several results;
its one evidence item may be referenced by those results or constraints. A
nested condition with its own trigger is retained as a separate observation.

| Case | Source status and input | Approved detector output | Evidence span(s) | Approved rule family |
| --- | --- | --- | --- | --- |
| Positive | SOURCE-ATTESTED — Application example, Section 2, Table 1, R2: `Маршрут доставки повинен швидко перераховуватися у разі зміни дорожньої ситуації.` | `DETECTED`; one condition | `[49,80)` `у разі зміни дорожньої ситуації` | `COND-UK` |
| Negative | SOURCE-ATTESTED — Application example, Section 2, Table 1, R3: `Персональні та комерційні дані повинні бути надійно захищені.` | `NOT_DETECTED` | none | `COND-UK` |
| Unresolved | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система повідомляє про помилку при перевірці.` | `UNRESOLVED`; `при перевірці` may be temporal context or verification-method context | no accepted evidence; candidate `[31,44)` is diagnostic only | `COND-UK` |
| Repeated | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Якщо сервіс недоступний, система зберігає запит; якщо зв’язок відновлено, система надсилає запит.` | `DETECTED`; two ordered conditions | `[0,23)` `Якщо сервіс недоступний`; `[49,72)` `якщо зв’язок відновлено` | `COND-UK` |
| Punctuation | SOURCE-ATTESTED — Application example, Section 2, Table 1, R4: `Система повинна залишатися доступною під час пікового навантаження.` | `DETECTED`; final full stop excluded | `[37,66)` `під час пікового навантаження` | `COND-UK` |
| Interaction | SOURCE-ATTESTED — Application example, Section 8, Table 7, `R2 → R2′` | `DETECTED`; load phrase is a condition and may also be quantitative context | `[117,159)` `при навантаженні до 300 одночасних запитів` | `COND-UK`, `QUANT` |

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

The approved lexical baseline therefore leaves `metric` unresolved unless an
explicit nominal metric phrase is attached unambiguously to the bound. Parser
assistance may extract the governing noun phrase and essential complements. It
must not infer a metric such as latency merely because a duration occurs.

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
4. Link a metric only when one governing metric phrase has an explicit template
   or grammatical relation to the bound in the same clause. If zero such phrases
   exist, leave `metric` unresolved. If more than one is compatible and grammar
   does not decide, leave it unresolved rather than selecting the nearest.
5. Link context only when a marker-headed phrase/clause modifies the same metric,
   result, or bound. A unique grammatical attachment may cross a comma inside
   the same sentence; it may not cross a hard boundary. Ambiguous context remains
   unresolved.
6. Do not merge distinct numeric anchors except through an approved range
   construction. No generic range construction is approved. Each bound
   therefore remains independently traceable.
7. A context bound may be represented both as the `context` of the primary
   target and as its own partial quantitative observation only when both roles
   are explicit under an approved grammar/template rule. Until that concrete
   nested-context rule is approved, preserve the context evidence and leave the
   separate-observation decision unresolved.
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
| Repeated | SOURCE-ATTESTED — Application example, Section 8, Table 7, R1′ | `DETECTED`; frequency candidate and latency constraint remain separate | `[63,90)` `не рідше одного разу на 5 с` with written count unresolved; metric `[92,161)` and bound `[164,177)` `не більше 3 с` | `QUANT` |
| Punctuation/decimal | SOURCE-ATTESTED — Application example, Section 8, Table 7, R4′: `Місячна доступність сервісу — не нижче 99,9 %; ...` | `DETECTED`; comma belongs to decimal and semicolon ends the constraint | metric `[0,27)`; bound `[30,45)` with comparator `GREATER_THAN_OR_EQUAL`, raw value `99,9`, unit `PERCENT` | `QUANT` |
| Nested interaction | SOURCE-ATTESTED — Application example, Section 8, Table 7, R2′ | `DETECTED`; primary four-second route bound with linked load context; separate nested load observation remains unresolved | primary bound `[96,116)`; context `[117,159)`; nested candidate `[134,159)` with comparator `UPPER_BOUND` and inclusivity `UNRESOLVED` | `QUANT`, `COND-UK` |

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

The approved explicit-only strategy accepts a method only when a complete phrase explicitly
names a verification procedure and grammatical/template context establishes
that it is the means for establishing requirement fulfilment. Evidence includes
the method head and its essential qualifiers; when needed to establish role, it
also includes the governing phrase such as “перевіряється ... тестом.” A method
word used as system behavior (`аналізує журнал`), an artifact/link target, a
future promise to define a method, or a statement that a requirement seems
testable must not count.

A named procedure or test category is accepted only when an approved grammatical
or template construction establishes its verification role. A name by itself is
not evidence that the method is reproducible, and apparent testability never
implies `verification_method`.

Multiple coordinated method phrases are separate observations. A shared
governing verification predicate may be referenced by each. If the phrase names
a possible method but its role or reproducibility cannot be established, the
outcome is `UNRESOLVED`. No method is inferred from a quantitative constraint.

| Case | Source status and input | Approved detector output | Evidence span(s) | Approved rule family |
| --- | --- | --- | --- | --- |
| Positive | SOURCE-ATTESTED — Application example, Section 8, Table 7, R3′ | `DETECTED`; explicit named test category | `[158,182)` `негативні security tests` | `VERIFY-UK` |
| Negative | SOURCE-ATTESTED — Application example, Section 2, Table 1, R2: `Маршрут доставки повинен швидко перераховуватися у разі зміни дорожньої ситуації.` | `NOT_DETECTED`; apparent testability does not state a method | none | `VERIFY-UK` |
| Unresolved | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Система виконує аналіз журналу.` | `UNRESOLVED`; `аналіз` may be system behavior rather than a verification procedure | no accepted evidence | `VERIFY-UK` |
| Repeated | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Виконання перевіряється навантажувальним тестом та інспекцією журналу.` | `DETECTED`; two named methods | `[24,47)` `навантажувальним тестом`; `[51,69)` `інспекцією журналу` | `VERIFY-UK` |
| Punctuation/boundary | SYNTHETIC TEST CASE — NOT DISSERTATION EVIDENCE: `Виконання перевіряється тестом; аналіз журналу виконує система.` | `DETECTED` only for the first clause; semicolon prevents the second system behavior from attaching to the verification predicate | `[24,30)` `тестом` | `VERIFY-UK` |
| Interaction | SOURCE-ATTESTED — Application example, Section 8, Table 7, R4′ | `UNRESOLVED` for `спосіб розрахунку SLA`; the line says a method is defined but does not state it | no accepted method evidence; quantitative availability criterion remains separate | `VERIFY-UK`, `QUANT` |

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
        ↓ FIND-U-VAGUE family rule
one Finding:
    code = VAGUE_TERM_SIGNAL
    characteristic = Unambiguity
    kind = SIGNAL
    explanation = identifies the exact approved seed literal and states that
                  it is a potential ambiguity indicator, not a confirmed defect
    evidence_refs = exactly the occurrence evidence reference(s)
    rule_id = the approved FIND-U-VAGUE rule identifier
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
QUANT-NNN
QUANT-UK-NNN
VERIFY-UK-NNN
UK-VAGUE-NNN
FIND-U-VAGUE-NNN
```

`UK` denotes the Ukrainian language profile. Language-independent symbolic or
unit rules use `QUANT-NNN`; Ukrainian lexical comparators use `QUANT-UK-NNN`.
`NNN` is a zero-padded stable rule number and does not imply priority. Semantic
versions belong to rule-registry metadata rather than to the stable identifier.
The examples above define families only; they do not create dozens of production
IDs. Each eventual registry entry must state the immutable detector description,
feature ID, language/profile, evidence boundary, source/approval reference,
status, and superseding rule if any. Evidence uses the detector rule ID; a
finding uses the interpretation/conversion rule ID that created the finding.

#### 7.14.12 Readiness of the targeted RQDs

Researcher approval closes the MVP seed-matching decision and partially approves
the parser-assisted and quantitative families without inventing their remaining
operational rules.

| RQD | Readiness | Reason |
| --- | --- | --- |
| `RQD-006` | `PARTIALLY_APPROVED / OPEN` | Source-attested condition markers, conservative phrase/clause boundaries, parser-optional condition attachment, and parser-required expected-result semantics are approved. No arbitrary verb rule is allowed. Concrete parser/template operationalization remains open; actor/action/object remain deferred. |
| `RQD-007` | `APPROVED_FOR_MVP_V0.1 / CLOSED` | NFC plus Unicode `casefold()`, Unicode-aware token boundaries, Unicode-whitespace phrase separators, repeated ordering, and `LEFTMOST_LONGEST_NON_OVERLAPPING` are approved without changing the ten-entry seed. Broader vocabulary coverage is future work and does not keep this MVP decision open. |
| `RQD-008` | `PARTIALLY_APPROVED / OPEN` | The narrow quantitative acceptance baseline, partial observations, approved comparator/numeric/unit forms, and conservative linkage without arbitrary distance thresholds are approved. Written-out numbers and generic ranges are outside the baseline; complex metric/context grammar and nested representation remain open. |
| `RQD-016` | `EXTRACTOR_SIDE_APPROVED_FOR_MVP_V0.1 / OPEN` | One accepted vague-term occurrence produces one Unambiguity `SIGNAL`; the other five families produce observations/evidence only. Any `QUALITY_PROBLEM` conversion and characteristic scoring remain open in the later calculation gate. |

`RQD-005`, `RQD-007`, and `RQD-009` are closed for MVP v0.1. `RQD-020` remains
unresolved; this approval adds no confidence, reliability, severity,
probability, risk, priority, or corrective-action field.

#### 7.14.13 Remaining researcher decisions

1. Define the concrete replaceable parser/template operationalization for
   condition attachment, expected-result clauses, non-numeric acceptance
   criteria, and explicitly named verification procedures (`RQD-006`). No NLP
   library is selected by this contract.
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

#### 7.14.14 Downstream GitHub issue alignment

The approval is reflected narrowly in issue descriptions #4, #5, #6, #9, and
#14. Issues #7 and #8 are intentionally unchanged. No implementation issue is
unblocked by detector approval alone.

| Issue | Approved narrow alignment |
| --- | --- |
| #4 MVP-03 | Record approved `DetectionStatus` semantics and the replaceable parser-information boundary while deferring the concrete mixed-state domain representation; keep observations/evidence only and no findings |
| #5 MVP-04 | Record approved condition/result/criterion/quantitative strategies, evidence boundaries, partial-observation behavior, and reference cases; keep concrete parser operationalization and actor/action/object deferred |
| #6 MVP-05 | Record approved Unicode, token/phrase boundary, overlap, ordering, comparator, numeric, unit, linkage, and verification-method mechanics allocated to textual extraction |
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
  `RQD-008` remain partially approved/open; the extractor-side portion of
  `RQD-016` is approved while its calculation-side conversion remains open; and
  `RQD-020` remains unresolved.

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
defined by Chapter 2 and are `DEFERRED_FROM_MVP_V0.1` as possible optional
future structural observations; they cannot affect Completeness in v0.1.

Researcher decisions RQD-002, RQD-006, RQD-010, and RQD-012 are
required.

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

Researcher decisions RQD-003, RQD-008, RQD-010, and RQD-012 are
required.

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

The source-derived seed lexicon and exact deterministic matching mechanics are
approved for MVP v0.1. Richer linguistic coverage, context exceptions,
confirmation procedure, applicability rule, and mapping of multiple signals to
the intermediate `a_i,U` value are not defined. The text also does not resolve
whether MVP uses review-confirmed ambiguities or deterministic detector signals
only.

Researcher decisions RQD-004, RQD-008, RQD-010, RQD-012, and the
characteristic-calculation portion of RQD-016 are required. `RQD-007` is closed
for the MVP v0.1 seed matcher.

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

## 11. Requirement Quality Profile

The approved implementation relationship is:

```text
CharacteristicAssessments(C_i, V_i, U_i)
        ↓
RequirementQualityProfile(A_i)
```

Chapter 2 defines individual property results `a_i,C`, `a_i,V`, and `a_i,U`, but
it deliberately preserves a multidimensional property profile. Therefore the
primary result is `A_i = (C_i, V_i, U_i)`. No function combines these values,
and no scalar `RequirementQualityScore` is required in MVP v0.1. Chapter 4's
`Q_int` formula combines context-selected ISO product-quality characteristics,
not the three MVP properties of one requirement, and must not be reused here.
RQD-013's original scalar-score request is intentionally deferred from MVP
v0.1.

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
aggregates:

```text
C_file = mean(C_i for applicable/computed C_i)
V_file = mean(V_i for applicable/computed V_i)
U_file = mean(U_i for applicable/computed U_i)
```

No scalar `FileQualityScore` combines these values. RQD-014's original scalar-
score request is intentionally deferred from MVP v0.1. Exact missing/`UNKNOWN`
propagation, empty-set behavior beyond the approved `NA` principle, numeric
precision, and rounding remain unresolved under RQD-012, RQD-015, and RQD-022.

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

Feature detection and assessment applicability are separate. A detector may use
`DETECTED`, `NOT_DETECTED`, or `UNRESOLVED` as processing states, while
characteristic/model criteria use the approved applicability states
`APPLICABLE`, `NOT_APPLICABLE`, and `UNKNOWN`. `NOT_DETECTED` and a missing
feature observation are not quality violations. `NOT_APPLICABLE` and `UNKNOWN`
are distinct and neither is numeric zero. An `APPLICABLE` criterion's
computed-versus-missing assessment state is a separate concern.

These semantics are explicitly defined, but concrete characteristic-state
representation, console wording, aggregation behavior, and the distinction
between “missing data” and “insufficient evidence for a score” remain
unresolved. No detector-confidence or evidence-reliability value is approved
for MVP v0.1; `RQD-020` remains unresolved. See RQD-012, RQD-020, and RQD-022.

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
Section 7 approves separate evidence and observation contracts and partially
approves the core finding taxonomy with stable rule traceability. Exact
observation-to-`QUALITY_PROBLEM` conversion remains unapproved under RQD-016 and
the characteristic-calculation gate.

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

Requirement Quality Profile:
(C, V, U) values UNRESOLVED
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

Requirement Quality Profile:
(C, V, U) values UNRESOLVED
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

Requirement Quality Profile:
(C, V, U) values UNRESOLVED
```

Researcher-approved examples must eventually include expected features,
characteristic assessments, requirement-quality profiles, explanations, and
boundary behavior. Demonstration coefficients and scores in the source example
must not be reused as expected values.

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
| `RQD-002` | Approve an operational definition of per-requirement Completeness. | `PARTIALLY_RESOLVED` | Section 2.1 defines local Completeness through sufficient condition, expected reaction, and fulfilment-criterion information, with elements dependent on requirement type/template. It supplies no deterministic detection or scoring rule. | OPEN | MVP-04/05 as applicable, MVP-06 |
| `RQD-003` | Approve an operational definition of per-requirement Verifiability. | `PARTIALLY_RESOLVED` | Sections 2.1 and 2.3 define reproducible verification and relevant evidence, and give set-level ratios. They do not define an `a_i,V` calculation for one line. | OPEN | MVP-04/05 as applicable, MVP-07 |
| `RQD-004` | Approve an operational definition of per-requirement Unambiguity. | `PARTIALLY_RESOLVED` | Section 2.1 defines one justified interpretation and gives boundary meanings for `a_i,U`; Sections 2.1 and 2.3 treat linguistic matches as signals rather than proof. Detector, confirmation, applicability, and intermediate-value rules remain absent. | OPEN | MVP-05, MVP-08 |
| `RQD-005` | Approve the complete MVP `RequirementFeatures` registry, types, valid values, and consuming characteristics. | `APPROVED_FOR_MVP_V0.1` | Section 7 defines the six repeatable feature arrays, their singular `feature_id` values, and their primary characteristic consumers. The mapping is traceability only and authorizes no score contribution or double-counting rule. | CLOSED FOR MVP v0.1 | None directly; detector and calculation rules remain gated separately |
| `RQD-006` | Define detection rules for actor, action, object, condition, scenario, and expected result. | `PARTIALLY_APPROVED` | Section 7.14 approves source-attested condition markers, conservative evidence boundaries, parser-optional condition attachment, parser-required expected-result semantics, and the prohibition on an arbitrary-verb fallback. Concrete replaceable parser/template operationalization remains open. Actor/action/object remain `DEFERRED_FROM_MVP_V0.1`. | OPEN — PARTIALLY APPROVED | MVP-04 and consuming calculators |
| `RQD-007` | Approve vague-term vocabulary, languages, matching/normalization rules, exceptions, and versioning. | `APPROVED_FOR_MVP_V0.1` | The ten-entry `uk_vague_terms_v1` remains unchanged. Section 7.14 approves NFC plus Unicode `casefold()`, Unicode-aware token boundaries, one-or-more-Unicode-whitespace phrase separators, repeated ordering, and `LEFTMOST_LONGEST_NON_OVERLAPPING`. Each selected occurrence produces one Unambiguity `SIGNAL`; broader vocabulary coverage is future work. | CLOSED FOR MVP v0.1 | None for the seed matcher; Unambiguity calculation remains gated separately |
| `RQD-008` | Define detection and linkage rules for metric, threshold, comparator, unit, context, acceptance criterion, and expected result. | `PARTIALLY_APPROVED` | Section 7.14 approves the narrow quantitative acceptance baseline, partial observations, source-attested comparator/numeric/unit forms plus operational `секунд`, and conservative linkage without arbitrary distance thresholds. `до` is `UPPER_BOUND` with inclusivity `UNRESOLVED`; written-out numbers and generic ranges are outside the baseline. Complex metric/context grammar and nested representation remain open. | OPEN — PARTIALLY APPROVED | MVP-04/05, MVP-07 |
| `RQD-009` | Approve the evidence data structure. | `APPROVED_FOR_MVP_V0.1` | Section 7 approves exact source spans, zero-based Unicode code-point offsets with inclusive start/exclusive end, separate repeated occurrences, multiple evidence references per observation, and one span supporting multiple observations. | CLOSED FOR MVP v0.1 | None directly; detector and finding rules remain gated separately |
| `RQD-010` | Define exact formulas, contributions, penalties/rewards, coefficients, and thresholds for the three characteristic scores. | `PARTIALLY_RESOLVED` | Section 2.1 places individual property values `a_ij` in `[0,1]`; Section 2.3 supplies generic and set-level metrics. Neither supplies executable per-requirement formulas for `a_i,C`, `a_i,V`, and intermediate `a_i,U`. | OPEN | MVP-06-08 |
| `RQD-011` | Approve score direction and valid range for each characteristic and property-level aggregate. | `PARTIALLY_RESOLVED` | Chapter 2 supports `[0,1]` and upward compliance orientation for individual properties and their property-level means. It does not approve binary versus graded MVP characteristic assessments. | OPEN | MVP-01, MVP-06-10 |
| `RQD-012` | Define missing, unknown, not-applicable, insufficient-evidence, and optional-feature behavior. | `PARTIALLY_RESOLVED` | Section 7 separates optional detection status (`DETECTED`, `NOT_DETECTED`, `UNRESOLVED`) from criterion applicability (`APPLICABLE`, `NOT_APPLICABLE`, `UNKNOWN`). `NOT_DETECTED` is not a violation, missing observations are not proof, and neither `NOT_APPLICABLE` nor `UNKNOWN` becomes zero. Calculator/aggregation propagation remains open. | OPEN | MVP-01, MVP-06-10 |
| `RQD-013` | Define `RequirementQualityScore = f(Completeness, Verifiability, Unambiguity)`. | `DEFERRED_FROM_MVP_V0.1` | MVP v0.1 preserves `RequirementQualityProfile(C, V, U)` and intentionally has no scalar integrated requirement-quality score. Any future index requires separate researcher approval. | CLOSED FOR MVP v0.1 | None; scalar aggregation excluded |
| `RQD-014` | Define `FileQualityScore = g(Q_1, ..., Q_n)`. | `DEFERRED_FROM_MVP_V0.1` | MVP v0.1 preserves property-level means in `SpecificationQualityProfile(C_file, V_file, U_file)` and intentionally has no scalar integrated file-quality score. Exact missing/`UNKNOWN` propagation remains under RQD-012/RQD-022. | CLOSED FOR MVP v0.1 | None; scalar aggregation excluded |
| `RQD-015` | Approve numeric precision and rounding. | `UNRESOLVED` | Chapter 2 gives no calculation, aggregation, or presentation rounding policy. | OPEN | MVP-06-12 |
| `RQD-016` | Define the problem taxonomy and when an observation becomes a reported problem. | `EXTRACTOR_SIDE_APPROVED_FOR_MVP_V0.1` | Section 7.14 approves one accepted `vague_term_occurrence` to one traceable Unambiguity `SIGNAL` and no finding from the other five feature families at extraction time. Any `QUALITY_PROBLEM` conversion and characteristic calculation remain open; severity, probability, risk, confidence, priority, and corrective action remain excluded. | OPEN — PARTIALLY APPROVED | MVP-06-08, MVP-10 |
| `RQD-017` | Provide approved reference requirements with expected features, scores, and explanations. | `ADDITIONAL_CONSTRAINTS` | Chapter 2 provides qualitative cases and working set-level formula examples, but no approved expected per-line MVP feature vectors or scores. Examples must respect applicability and signal/confirmation distinctions. | OPEN | MVP-04-09, MVP-12 |
| `RQD-018` | Define input-language, Unicode/case/punctuation, and multi-sentence or multi-clause behavior. | `APPROVED_FOR_MVP_V0.1` | UTF-8/Unicode input and original punctuation are preserved; linguistic matching may be case-insensitive; Ukrainian is the supported language-dependent profile; one input line remains one requirement even with multiple sentences or clauses. | CLOSED FOR MVP v0.1 | None |
| `RQD-019` | Decide how consistency, traceability, coverage, and other broader properties relate to the three-characteristic MVP. | `APPROVED_FOR_EXCLUSION_FROM_MVP_V0.1` | Per-line Consistency and Traceability, global Completeness, coverage, product-quality prediction, risk, and corrective actions require broader context and remain future extensions. | CLOSED FOR MVP v0.1 | None |
| `RQD-020` | Decide whether evidence coverage/reliability and detector confidence are represented in MVP. | `UNRESOLVED` | Section 2.3 discusses possible reliability constructs but approves no MVP fields, values, scales, or semantics. The approved finding core excludes confidence, severity, probability, risk, priority, and corrective action. | OPEN, CONDITIONALLY BLOCKING | MVP-01, MVP-06-10 if included |
| `RQD-021` | Supply or supersede the Chapter 2/§2.3 definitions referenced by Chapter 4. | `RESOLVED_BY_CHAPTER_2` | Sections 2.1, 2.2, and especially 2.3 are now present and integrated into this specification. Their remaining operational gaps are tracked by the other RQDs. | CLOSED AS RESEARCH INPUT | None directly |
| `RQD-022` | Approve whether and how a score may be withheld when evidence is insufficient. | `PARTIALLY_RESOLVED` | Chapter 2 and Chapter 4 prohibit false precision and distinguish missing from not applicable. Console wording and propagation into requirement and property-level specification profiles remain open. | OPEN | MVP-06-10, MVP-12 |
| `RQD-023` | Define requirement types and the applicability sets/rules used by each candidate feature and characteristic in a text-only per-line MVP. | `APPROVED_MVP_SIMPLIFICATION` | MVP v0.1 performs no automatic requirement-type classification. Requirement type remains unspecified; criterion applicability is `APPLICABLE`, `NOT_APPLICABLE`, or `UNKNOWN`, with neither non-applicable nor unknown treated as zero. Detection status is represented separately. Exact calculator propagation remains under the characteristic-calculation gate. | CLOSED FOR MVP v0.1 | None directly |

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
  scalar `FileQualityScore`.

Any future scalar index requires a separate researcher-approved scientific
decision.

### 18.3 Remaining implementation-blocking RQDs

The remaining decisions are grouped into four approval gates:

1. **Remaining feature-operationalization and finding-conversion gate:** Section
   7.14 records approved detector strategies and baselines. `RQD-006` remains
   open for concrete parser/template operationalization; `RQD-008` remains open
   for complex metric/context grammar and representation; and `RQD-016` remains
   open only beyond its approved extractor-side contract. `RQD-007` is closed
   for the MVP seed matcher.
2. **Characteristic-calculation gate:** `RQD-002`-`RQD-004`, `RQD-010`-
   `RQD-012`, and `RQD-022`.
3. **Property aggregation and numeric-contract gate:** the still-open
   propagation aspects of `RQD-012` and `RQD-022`, plus `RQD-015`.
4. **Scientific acceptance gate:** `RQD-017`.

`RQD-020` is conditionally blocking only if confidence or evidence-reliability
values are included in MVP v0.1. It is not permission to invent such values.

### 18.4 Remaining design tensions

1. **Automated signal versus confirmed defect.** A deterministic text detector
   can identify risk signals, while the research definition of Unambiguity uses
   confirmed ambiguity at its boundary values. Treating every match as a defect
   would contradict that distinction.
2. **Applicability without type classification.** Requirement type remains
   unspecified. Feature and criterion contracts must preserve `UNKNOWN` rather
   than infer a type or violation, and calculators still need approved
   propagation rules.
3. **Local Completeness versus Verifiability overlap.** A fulfilment criterion
   contributes to local Completeness and also provides Verifiability evidence.
   Any shared feature and non-duplication rule requires approval.

The next recommended research work is the concrete parser/data-contract portion
of the remaining feature-operationalization gate, followed by the
characteristic-calculation gate. Until the applicable gates are approved and
this document's status is changed from `DRAFT`, unapproved detector rules,
characteristic calculators, and specification aggregation remain blocked.

### 18.5 Downstream GitHub issue impact after detector-contract approval

Issue descriptions #4, #5, #6, #9, and #14 are aligned narrowly with the
approved detector contract. #4 records approved status semantics and the
replaceable parser boundary without freezing a mixed-state domain shape; #5 and
#6 record the approved detector allocation, evidence, Unicode, boundary,
linkage, and reference-case mechanics; #9 records only the approved
one-occurrence-to-one-`SIGNAL` rule; and #14 records the approvals and RQD
statuses. Issues #7 and #8 are intentionally unchanged and remain blocked by
their characteristic-calculation gates.

No implementation issue is unblocked by this documentation approval, and no
issue may infer a `QUALITY_PROBLEM` or characteristic score from detector rules.
