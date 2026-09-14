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
| Per-requirement feature/observation registry | Metrics system; researcher-approved Section 7 contract | 2.3 paragraphs 4 and 6-8; Section 7.2 | Six repeatable conceptual feature collections and primary consumers are approved; detector algorithms remain open | Yes | `DEFINED` at registry level; detectors `PARTIALLY_DEFINED` |
| Candidate structural fields `has_actor`, `has_action`, `has_object` | MVP-SPEC issue; researcher-approved Section 7.11 disposition | Candidate list and Section 7.11 | No research definition in supplied references | No; possible optional future observations only | `DEFERRED_FROM_MVP_V0.1` |
| Condition/context, expected result, acceptance criterion, linked quantitative constraint, and explicit verification method | Requirement properties; requirements/product quality; metrics system; static and dynamic methods | 2.1 Table 2.1 and paragraphs 11-12; 2.2 Tables 2.4-2.5; 2.3 Table 2.7 and paragraphs 17-21; 3.1 paragraph 13; 3.2 Table 3.4 | Semantic features, linked quantitative concept, multiplicity, and primary consumers approved; detector/applicability rules absent | Yes | `DEFINED` conceptually; detector rules `MISSING` |
| Vague-term and linguistic-smell evidence | Requirement properties; metrics system; dynamic methods; application example; researcher-approved Section 7.8 | 2.1 paragraph 10; 2.3 paragraphs 12-16; 3.2 paragraph 10; application Sections 2-3, 7-8, and 13 | `uk_vague_terms_v1` and deterministic source-only matching policy approved as a seed lexicon; richer linguistic coverage deferred | Yes | `PARTIALLY_APPROVED` |
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
| `condition_context` | `condition_contexts[]` | An explicit condition, trigger, scenario, execution context, or measurement context under which behavior or a criterion applies | Completeness | OPEN under `RQD-006` |
| `expected_result` | `expected_results[]` | An explicit expected reaction, observable outcome, or required behavior | Completeness | OPEN under `RQD-006` |
| `acceptance_criterion` | `acceptance_criteria[]` | An explicit fulfilment or acceptance condition against which execution or an observation can be judged | Completeness and Verifiability | OPEN under `RQD-006`/`RQD-008` |
| `quantitative_constraint` | `quantitative_constraints[]` | A linked measurable target or bound whose metric, comparator, value, unit, and context remain associated | Verifiability | Linked concept approved; detector OPEN under `RQD-008` |
| `verification_method` | `verification_methods[]` | An explicitly stated reproducible verification method in the requirement text | Verifiability | Semantic feature approved; detector OPEN |
| `vague_term_occurrence` | `vague_term_occurrences[]` | An exact occurrence from approved `uk_vague_terms_v1` | Unambiguity, as `SIGNAL` only | Seed lexicon/matching policy partially approved under `RQD-007` |

The mappings above approve only which characteristic may consume each feature.
They do not define score contributions, double-counting rules, or characteristic
calculations. One source-text span may support more than one observation when
the detector rule justifies each observation and preserves evidence.

### 7.3 Semantic definitions and remaining detector gaps

| Concept | Strongest source-supported definition | Always applicable? | Multiple occurrences? | Can absence currently be detected deterministically? | May one span support another concept? |
| --- | --- | --- | --- | --- | --- |
| Condition/context | Information establishing the condition, trigger, scenario, execution setting, or measurement conditions under which a reaction or bound applies | Not established. Local required elements depend on type/template, while automatic type classification is excluded | The sources do not impose a single-occurrence limit; the proposed representation preserves all detected occurrences | No. No grammar, lexical inventory, or applicability rule is defined | Yes conceptually; a condition may also be part of an acceptance criterion or quantitative context |
| Expected result | The expected reaction, observable outcome, or required behavior to be understood or observed | Not established; the source ties required content to type/template | Yes in the proposed representation, including multi-clause requirements | No deterministic semantic detector or exhaustive absence rule is defined | Yes; an expected result may itself function as an acceptance criterion |
| Acceptance criterion | A fulfilment condition that makes a requirement judgeable; Chapter 3 gives examples including a threshold, expected behavior, admissible range, or condition | Not universally established; Chapter 2 explicitly uses an applicability set | Yes in the proposed representation | No deterministic detector or criterion-sufficiency rule is defined | Yes; it may share a span with an expected result or quantitative constraint |
| Verification method | An explicit reproducible method for establishing fulfilment, including test, analysis, inspection, measurement, or another stated procedure | No. A requirement can be verifiable without literally naming the method, and method need depends on requirement/characteristic type | Yes in the proposed representation | No. The absence of a literal method is not equivalent to non-verifiability | Yes; a procedure reference may also carry acceptance-criterion evidence |

The approved contract permits one source span to support more than one feature
observation when each observation is justified. Evidence references preserve
the common source span without forcing one semantic label onto multi-purpose
text. No dependency grammar, syntactic pattern, parser, regular expression, or
semantic heuristic is approved by this decision.

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
or both; that decomposition remains part of `RQD-008`. No parser or regular
expression, normalized numeric type, unit conversion, or linkage heuristic is
approved here. `RQD-008` remains open.

### 7.7 Proposed stable `rule_id` policy

A `rule_id` identifies the deterministic rule that produced an observation,
evidence item, or downstream finding. Its purposes are reproducibility,
human-readable explanation, unit-test traceability, and comparison across
versioned research changes.

The proposed policy is:

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
examples only. This draft does not create the production rule-ID registry.

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

Case folding or other derived detector forms must preserve a map to the original
source offsets and must not replace original evidence. Exact detector mechanics,
including deterministic handling of nested phrase/token matches, remain open;
no new vocabulary or semantic expansion may be introduced to resolve them.
`RQD-007` is partially approved rather than closed because broader linguistic
coverage remains a future research and validation issue.

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
`RQD-020` remains unresolved. `RQD-016` is partially approved because the core
taxonomy and boundary are approved while exact observation-to-problem
conversion rules remain in the characteristic-calculation gate.

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

The approved portions above close `RQD-005` and `RQD-009` for MVP v0.1 and
partially approve `RQD-007` and `RQD-016`. Implementation remains blocked by:

1. deterministic textual/semantic detectors for `condition_context`,
   `expected_result`, `acceptance_criterion`, and `verification_method`,
   including explicit processing of `NOT_DETECTED` and `UNRESOLVED` (`RQD-006`);
2. deterministic quantitative and criterion detection, component parsing,
   partial-observation handling, and linkage rules (`RQD-008`);
3. exact deterministic mechanics for token/phrase boundaries and nested matches
   in the approved seed lexicon, without expanding its contents (`RQD-007`);
4. criterion-applicability, missing-feature, and absence semantics used by each
   characteristic calculation (`RQD-002`-`RQD-004`, `RQD-010`-`RQD-012`, and
   `RQD-022`);
5. exact observation-to-`QUALITY_PROBLEM` conversion rules and any handling of
   overlapping evidence in characteristic calculations (`RQD-016` and the
   characteristic-calculation gate);
6. the production rule-ID registry and detector descriptions associated with
   approved evidence;
7. the still-unresolved decision on whether any evidence reliability or
   detector-confidence representation belongs in MVP (`RQD-020`). No such value
   is approved by this section.

No decision in this section defines a calculation for `C`, `V`, or `U`, a
coefficient, a weight, a threshold, a score contribution, or a rounding rule.

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

The source-derived seed lexicon and high-level matching policy are approved, but
exact detector mechanics, richer linguistic coverage, context exceptions,
confirmation procedure, applicability rule, and mapping of multiple signals to
the intermediate `a_i,U` value are not defined. The text also does not resolve
whether MVP uses review-confirmed ambiguities or deterministic detector signals
only.

Researcher decisions RQD-004, RQD-007, RQD-008, RQD-010, RQD-012,
and RQD-016 are required.

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
| `RQD-006` | Define detection rules for actor, action, object, condition, scenario, and expected result. | `STILL_BLOCKED_BY_MISSING_RESEARCH_DEFINITION` | Actor/action/object extraction is `DEFERRED_FROM_MVP_V0.1` and cannot affect Completeness, Verifiability, or Unambiguity. Deterministic detection boundaries for condition/context and expected result remain undefined. | OPEN | MVP-04 and consuming calculators |
| `RQD-007` | Approve vague-term vocabulary, languages, matching/normalization rules, exceptions, and versioning. | `PARTIALLY_APPROVED` | Section 7 approves the exact source-derived `uk_vague_terms_v1` seed lexicon and its Ukrainian-only, deterministic, case-insensitive, boundary-aware matching policy. Reduced recall is accepted; exact overlap/normalization mechanics and any broader coverage remain open, and matches are only `SIGNAL`. | OPEN — PARTIALLY APPROVED | MVP-05, MVP-08 |
| `RQD-008` | Define detection and linkage rules for metric, threshold, comparator, unit, context, acceptance criterion, and expected result. | `APPROVED_CONCEPT_DETECTOR_OPEN` | Section 7 approves the linked quantitative-constraint structure, partial observations, and unresolved fields. Component detection, parsing, nesting, linkage mechanics, and overlap disambiguation remain undefined. | OPEN | MVP-04/05, MVP-07 |
| `RQD-009` | Approve the evidence data structure. | `APPROVED_FOR_MVP_V0.1` | Section 7 approves exact source spans, zero-based Unicode code-point offsets with inclusive start/exclusive end, separate repeated occurrences, multiple evidence references per observation, and one span supporting multiple observations. | CLOSED FOR MVP v0.1 | None directly; detector and finding rules remain gated separately |
| `RQD-010` | Define exact formulas, contributions, penalties/rewards, coefficients, and thresholds for the three characteristic scores. | `PARTIALLY_RESOLVED` | Section 2.1 places individual property values `a_ij` in `[0,1]`; Section 2.3 supplies generic and set-level metrics. Neither supplies executable per-requirement formulas for `a_i,C`, `a_i,V`, and intermediate `a_i,U`. | OPEN | MVP-06-08 |
| `RQD-011` | Approve score direction and valid range for each characteristic and property-level aggregate. | `PARTIALLY_RESOLVED` | Chapter 2 supports `[0,1]` and upward compliance orientation for individual properties and their property-level means. It does not approve binary versus graded MVP characteristic assessments. | OPEN | MVP-01, MVP-06-10 |
| `RQD-012` | Define missing, unknown, not-applicable, insufficient-evidence, and optional-feature behavior. | `PARTIALLY_RESOLVED` | Section 7 separates optional detection status (`DETECTED`, `NOT_DETECTED`, `UNRESOLVED`) from criterion applicability (`APPLICABLE`, `NOT_APPLICABLE`, `UNKNOWN`). `NOT_DETECTED` is not a violation, missing observations are not proof, and neither `NOT_APPLICABLE` nor `UNKNOWN` becomes zero. Calculator/aggregation propagation remains open. | OPEN | MVP-01, MVP-06-10 |
| `RQD-013` | Define `RequirementQualityScore = f(Completeness, Verifiability, Unambiguity)`. | `DEFERRED_FROM_MVP_V0.1` | MVP v0.1 preserves `RequirementQualityProfile(C, V, U)` and intentionally has no scalar integrated requirement-quality score. Any future index requires separate researcher approval. | CLOSED FOR MVP v0.1 | None; scalar aggregation excluded |
| `RQD-014` | Define `FileQualityScore = g(Q_1, ..., Q_n)`. | `DEFERRED_FROM_MVP_V0.1` | MVP v0.1 preserves property-level means in `SpecificationQualityProfile(C_file, V_file, U_file)` and intentionally has no scalar integrated file-quality score. Exact missing/`UNKNOWN` propagation remains under RQD-012/RQD-022. | CLOSED FOR MVP v0.1 | None; scalar aggregation excluded |
| `RQD-015` | Approve numeric precision and rounding. | `UNRESOLVED` | Chapter 2 gives no calculation, aggregation, or presentation rounding policy. | OPEN | MVP-06-12 |
| `RQD-016` | Define the problem taxonomy and when an observation becomes a reported problem. | `PARTIALLY_APPROVED` | Section 7 approves `SIGNAL` and `QUALITY_PROBLEM`, the minimal traceable finding schema, and the extractor/downstream-rule boundary. Exact observation-to-finding and signal-to-problem conversion rules remain open; severity, probability, risk, confidence, priority, and corrective action are excluded. | OPEN — PARTIALLY APPROVED | MVP-06-08, MVP-10 |
| `RQD-017` | Provide approved reference requirements with expected features, scores, and explanations. | `ADDITIONAL_CONSTRAINTS` | Chapter 2 provides qualitative cases and working set-level formula examples, but no approved expected per-line MVP feature vectors or scores. Examples must respect applicability and signal/confirmation distinctions. | OPEN | MVP-04-09, MVP-12 |
| `RQD-018` | Define input-language, Unicode/case/punctuation, and multi-sentence or multi-clause behavior. | `APPROVED_FOR_MVP_V0.1` | UTF-8/Unicode input and original punctuation are preserved; linguistic matching may be case-insensitive; Ukrainian is the supported language-dependent profile; one input line remains one requirement even with multiple sentences or clauses. | CLOSED FOR MVP v0.1 | None |
| `RQD-019` | Decide how consistency, traceability, coverage, and other broader properties relate to the three-characteristic MVP. | `APPROVED_FOR_EXCLUSION_FROM_MVP_V0.1` | Per-line Consistency and Traceability, global Completeness, coverage, product-quality prediction, risk, and corrective actions require broader context and remain future extensions. | CLOSED FOR MVP v0.1 | None |
| `RQD-020` | Decide whether evidence coverage/reliability and detector confidence are represented in MVP. | `UNRESOLVED` | Section 2.3 discusses possible reliability constructs but approves no MVP fields, values, scales, or semantics. The approved finding core excludes confidence, severity, probability, risk, priority, and corrective action. | OPEN, CONDITIONALLY BLOCKING | MVP-01, MVP-06-10 if included |
| `RQD-021` | Supply or supersede the Chapter 2/§2.3 definitions referenced by Chapter 4. | `RESOLVED_BY_CHAPTER_2` | Sections 2.1, 2.2, and especially 2.3 are now present and integrated into this specification. Their remaining operational gaps are tracked by the other RQDs. | CLOSED AS RESEARCH INPUT | None directly |
| `RQD-022` | Approve whether and how a score may be withheld when evidence is insufficient. | `PARTIALLY_RESOLVED` | Chapter 2 and Chapter 4 prohibit false precision and distinguish missing from not applicable. Console wording and propagation into requirement and property-level specification profiles remain open. | OPEN | MVP-06-10, MVP-12 |
| `RQD-023` | Define requirement types and the applicability sets/rules used by each candidate feature and characteristic in a text-only per-line MVP. | `APPROVED_MVP_SIMPLIFICATION` | MVP v0.1 performs no automatic requirement-type classification. Requirement type remains unspecified; criterion applicability is `APPLICABLE`, `NOT_APPLICABLE`, or `UNKNOWN`, with neither non-applicable nor unknown treated as zero. Detection status is represented separately. Exact calculator propagation remains under the characteristic-calculation gate. | CLOSED FOR MVP v0.1 | None directly |

### 18.1 RQDs approved or closed for MVP v0.1

- `RQD-001`, `RQD-005`, `RQD-009`, `RQD-018`, `RQD-019`, and `RQD-023` are closed by explicit
  researcher approval for MVP v0.1.
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

1. **Feature-detection and finding-conversion gate:** `RQD-006`, the remaining
   mechanics under `RQD-007`, `RQD-008`, and `RQD-016`. `RQD-005` and
   `RQD-009` are closed.
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

The next recommended approval gate is the **feature-detection and
finding-conversion gate**, followed by the characteristic-calculation gate.
Until the applicable gates are approved and this document's status is changed
from `DRAFT`, unapproved detector rules, characteristic calculators, and
specification aggregation remain blocked.

### 18.5 Downstream GitHub issue impact after contract approval

The descriptions for #2, #4, #5, #6, #9, #11, and #14 were aligned narrowly
with the approved contract. The adjustments record the approved registry,
evidence offsets, detection/applicability separation, linked quantitative
concept, explicit-only verification method, vague-term signal semantics,
finding boundary, actor/action/object deferral, and profile-only MVP scope.

These description updates do not unblock implementation. Issues #5, #6, and #9
remain blocked by open detector and characteristic-calculation decisions; #11
remains downstream of approved assessments; and #14 remains a research issue.
