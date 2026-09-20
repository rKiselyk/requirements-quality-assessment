# SRM-02 — Full local single-requirement model and traceability

**Status: LOCAL SCIENTIFIC SCOPE APPROVED BY THE RESEARCHER; NEW OPERATIONAL
RULES PENDING RESEARCHER APPROVAL.** This scope decision is not an amendment
to the approved executable rules in [model-spec.md](model-spec.md).
It records the gap between the accepted [MVP v0.1 baseline](mvp-v0.1-baseline.md)
and the researcher-approved local scope of the full single-requirement milestone ([SRM-00, issue #68](https://github.com/rKiselyk/requirements-quality-assessment/issues/68),
[SRM-02, issue #70](https://github.com/rKiselyk/requirements-quality-assessment/issues/70)).
Nothing marked unresolved here authorizes implementation. The researcher must
approve any new scientific rule in `model-spec.md` before production work.

## Sources and boundary of this inventory

`model-spec.md` remains authoritative for **approved MVP v0.1 behavior**;
the dissertation excerpts provide the broader scientific scope, not executable
permission. Relevant sources are [§2.1](reference/2.1_Властивості_вимог.docx)
(Tables 2.1–2.3), [§2.3](reference/2.3_Система_метрик.docx) (Tables 2.7–2.9),
[§3.1](reference/3.1_Статичні_методи.docx) (requirement review and static
evidence), [§3.2](reference/3.2_Динамічні_методи.docx) (criterion-to-test
chain, as a boundary), [§3.3](reference/3.3_Метод_оцінювання.docx)
(explainability and evidence sufficiency), [§4.1](reference/4.1_Процесна_модель.docx)
(versioned state and feedback), [§4.2](reference/4.2_Модель_якості.docx)
(artifact versus product quality), and [§4.3](reference/4.3_Модель_ризиків.docx)
(defect, risk and corrective-action structures). Existing code/tests and the
SRM issue bodies establish *implementation*, not scientific approval.
**Dissertation chapter 1 and complete chapter manuscripts are not in this
working tree.** The available files are excerpts from chapters 2–4, not a
complete dissertation. The inventory is consequently complete for the nine
individual properties explicitly enumerated in the available §2.1 Table 2.1,
not a claim about unseen chapter-1 material. The [example](reference/Приклад_застосування_моделі.docx)
is illustrative, not a source of calibrated constants or binding cases.

The researcher-approved target assessment format is **one Ukrainian-language
sentence representing one requirement**. Multiple clauses in that sentence
remain one requirement.
The frozen MVP reader's unit is one trimmed non-empty UTF-8 **line**, even
when that line contains multiple grammatical sentences; this behavior is not
changed here. Sentence validation is **not** an unconditional prerequisite
for implementing the local model. If a future issue proposes rejecting or
marking a multi-sentence line, that behavior requires its own approved
contract. One line must never be silently split into new requirement objects.
Individual property result `a_ij` is distinct from a
set-level indicator `x_j` and a predicted product characteristic `ŷ_j`.
The approved executable individual profile is exactly `A_i = (C_i, V_i, U_i)`;
it is not a scalar. The full-model inventory below does **not** assert that
all nine dissertation properties must be scored from a text-only line.
Specification coverage, pairwise consistency, structural traceability,
duplicate detection, change metrics across a set, full lifecycle reassessment,
product-quality prediction and product-level risk aggregation are not the
target. **Local** requirement-version reassessment, defect/risk
representation, and corrective-action verification *are* target components
subject to new scientific decisions. Existing property-level `AGG-MVP-001`
remains supported but is not a new local characteristic. The earlier
interpretation that all risk and reassessment were outside this milestone is
superseded by the researcher's scope clarification; it does not silently
approve the Chapter 4 algorithms.

## Individual-property scope

The definitions and possible evidence below are from §2.1 Table 2.1. Table
2.3 provides *illustrative* assessment principles for seven properties; it
does not approve an executable rule for the six non-MVP properties. An
unavailable result must remain unavailable, not zero.

| Individual property | Scientific meaning and source | Inputs / feature or metric / output and MVP relationship |
| --- | --- | --- |
| Completeness `C` | Sufficient information to understand condition, expected reaction and fulfilment criterion (§2.1 Table 2.1, ¶11; Table 2.3). Local, not global coverage. | Existing `condition_context`, `expected_result`, `acceptance_criterion` outcomes and exact Evidence; `CALC-C-MVP-001` yields a stateful exact `Fraction` in `{0,1/3,2/3,1}` or `UNKNOWN` (§8). The three mandatory applicable criteria are an expressly approved MVP simplification, not universal type-dependent semantics. Wider recognition and type-specific criteria need approval. |
| Verifiability `V` | A reproducible way to establish fulfilment (§2.1 Table 2.1, ¶12; §2.3 ¶17–21). | Existing acceptance criterion, linked quantitative constraint, or explicit verification method; `CALC-V-MVP-001` gives alternative tiers `1`, `1/2`, `0`, or `UNKNOWN` (§9). A named method alone does not prove all procedural details. Broader measurement/criterion grammar remains open. Set ratios `M_ver`, `M_ac`, `M_qnt` in §2.3 are not per-line formulas. |
| Unambiguity `U` | One justified interpretation in context (§2.1 Table 2.1, ¶10; Table 2.3). | Existing `uk_vague_terms_v1` occurrence and exact Evidence; `FIND-U-VAGUE-001` yields `SIGNAL`; `CALC-U-MVP-001` yields `1` (no supported signal after complete scanning) or `1/2` (one or more), or `UNKNOWN` (§10). `1` is not proof of universal semantic uniqueness. Confirmed material ambiguity and `0` require a separate rule. |
| Singularity / atomicity `S` | One logically independent need or property (§2.1 Table 2.1, ¶10; Table 2.3). | Potential independent obligations and their relations in multi-clause text; §2.1 illustrates binary and possible intermediate values, but gives no approved segmentation, independence, applicability, adjudication, or calculation. No MVP feature, assessment, or reference case. Reader's one-line unit must not be silently split. |
| Conformance to presentation rules `F` | Consistency with adopted syntax, template, terminology and documentation rules (§2.1 Table 2.1; Table 2.3). | Requires a supplied, versioned project template/style guide/terminology, applicability and rule checks. Table 2.3 sketches a fraction of complied-with rules, not an approved denominator or detector. No MVP assessment; a vague-word signal is not itself a template violation. |
| Correctness `R` | Faithful representation of a real domain need, rule or constraint (§2.1 Table 2.1, ¶13; Table 2.3). | Requires authoritative domain sources, stakeholder confirmation or regulations and a validation procedure. Table 2.3's degree of confirmation is not an approved scale. No text-only MVP rule; fluency is not correctness. |
| Feasibility `E` | Realizability within technical, time, resource and regulatory constraints (§2.1 Table 2.1, ¶13; Table 2.3). | Requires constraints, resource estimates, model/prototype or expert assessment. Table 2.3's degree of confirmation is illustrative; no approved local rule or MVP result. |
| Necessity | Represents an actual need, goal or essential constraint (§2.1 Table 2.1, ¶9). | Requires goal/source links, stakeholder rationale and inclusion decision. No individual numeric principle in Table 2.3, no approved feature/applicability/result; text alone cannot decide necessity. |
| Relevance | Fits project domain, system level and scope without unnecessary implementation prescription (§2.1 Table 2.1, ¶9). | Requires goals, scope and architectural constraints. No individual numeric principle in Table 2.3, no approved feature/applicability/result; text alone cannot decide relevance. |

The additional six remain in the **theoretical** inventory. Their inclusion
as operational local assessments is a separate scientific choice, not a
default nine-calculator plan:

| Property | One-text observation possible? | External evidence / expert confirmation | Executable rule and necessity for target local model |
| --- | --- | --- | --- |
| Singularity | Candidate independent clauses can be signaled; one sentence may contain several obligations without becoming several requirement objects. | Context or expert adjudication may be needed to decide independence. | No approved segmentation/decision/score; inclusion as a local finding or assessment remains pending SRM-03/10. |
| Presentation conformance | A textual template or terminology occurrence could be checked if supplied. | An authoritative project rule set and scope are needed; expert handling of exceptions may be needed. | No approved rule set, denominator or output; inclusion pending SRM-09/10. |
| Correctness | Text alone cannot validate domain truth. | Authoritative domain source or stakeholder confirmation required. | No approved procedure/scale; inclusion pending SRM-10 and external-input decision. |
| Feasibility | Text may state a constraint, but cannot establish realizability. | Technical, resource, time and regulatory evidence plus expert/model validation required. | No approved procedure/scale; inclusion pending SRM-10 and external-input decision. |
| Necessity | Text alone cannot establish an actual need. | Goal/source links, stakeholder rationale and inclusion decision required. | No approved operational assessment; inclusion pending SRM-10. |
| Relevance | Text alone cannot establish project-scope fit. | Goals, scope and architectural context required. | No approved operational assessment; inclusion pending SRM-10. |

None is erased from the theory merely because operationalization is missing.
The dissertation supplies local *concepts* for all nine, but does not establish
that implementing each as a numeric characteristic is necessary to the local
process/defect/action loop. The researcher must decide the minimum supported
local subset and the handling of external and expert inputs before adding
domain fields or calculators.

For the existing C/V/U output, the typed `CharacteristicAssessment` retains
`characteristic_id`, `state`, `value: Fraction | None`, `assessment_rule_id`,
`findings`, and explanation. The `RequirementQualityProfile` retains the three
independent results. `RequirementExtractionResult` retains the unchanged six
`RequirementFeatures` outcomes and accepted source-aligned `Evidence`; detector
diagnostics are not accepted Evidence. `APPLICABLE`, `NOT_APPLICABLE`, and
`UNKNOWN` are criterion-applicability states, distinct from detector
`DETECTED`/`NOT_DETECTED`/`UNRESOLVED` and assessment
`COMPUTED`/`NOT_APPLICABLE`/`UNKNOWN`. The baseline uses exact `Fraction`
arithmetic without rounding. No new output fields or quality criteria are
approved by this inventory.

## Local reconstruction of Chapters 3 and 4

This is a **specialization proposal for one requirement**, not a claim that
an entire chapter is implemented. The Chapter 3 and 4 notation often indexes
product characteristic `q_j` or a set `R_j`; replacing those operands by
`C_i`, `V_i` or `U_i` is **not** licensed by a resemblance in notation.

| Source component | Directly local or locally specializable | Requires a set, product or lifecycle evidence / approval boundary |
| --- | --- | --- |
| §3.1 static requirement analysis and review (¶9–13, 31–34) | Textual/structural observations, applicable criteria, evidence-backed findings, review → correction → recheck are relevant to one `r_i`. MVP implements six narrow detection families and three C/V/U calculations; it does not implement an expert review cycle or confirmed defect rules. | §3.1's `m_k` is a *set-level* indicator, while traceability graph, architecture/code evidence and product `q_j` profile require other artifacts. No local defect may be inferred from a smell or absent observation alone. |
| §3.2 dynamic method (¶4–16, Table 3.4) | Requirement → criterion → verification procedure is useful as a *specification of what would be checked*, not an executed test. MVP detects some textual criteria and named methods. | Test execution, observations, compliance `c_k`, aggregation `v_i` and product-quality validation need a product, test context and a predeclared `Agg_i`. Not part of a text-only local assessment. |
| §3.3 assessment (¶9–19, 30–36) | Source provenance, applicability/missingness, separate explanation and evidence sufficiency guide local result design. MVP preserves exact Evidence, rule IDs and explanations. | `Z_j`, `X_j`, coverage/reliability pair, predictor `Fθ_j`, uncertainty `u_j` and local sensitivity `Δ_kj` are product-characteristic/model constructs; no direct C/V/U or local-risk calculation follows. `RQD-020` remains open for reliability metadata. |
| §4.1 initial state and feedback (¶8–14, 29–33) | One requirement can be assessed at a particular version with source Evidence, changed input, new extraction/assessment, and a before/after record. This is the local process target. | Dissertation `P_j(τ,v)` and update `𝒰_j` concern `q_j`, artifact sets, stages and calibrated predictions. Local state identity, version, evidence invalidation, re-evaluation trigger and comparison semantics require a new contract. Stage checkpoints, `Qmin`/`Cmin`, architecture, code, test and operation remain outside local text reassessment. |
| §4.2 `R → P → M → Q` (¶4–19, 23–31) | `R → P → M` distinguishes requirement properties, observations and indicators; current `RequirementQualityProfile(C,V,U)` is local artifact-quality output. Extend recognition, applicability, uncertainty and provenance only under approved local rules. | `Q`, `G`, `Φ`, `Fθ_j`, `ŷ_j`, `Q_int` and non-compensated product thresholds concern software-product prediction/context. They cannot supply local formulas or a scalar requirement index. External-domain properties need their own input and confirmation contract. |
| §4.3 defect record and correction (¶4–8, 25–31, 35–37) | A potential/confirmed issue can be linked to *one* requirement, its exact Evidence, version and a proposed action; changes can trigger a new local assessment. MVP already has a `Finding` envelope and one vague `SIGNAL`, but neither a confirmed defect instance nor action/version model. | Full tuple `d_i=(type,target,evidence,sev,conf,τ,v)` includes unapproved severity/confidence/stage/version values. Examples in Tables 4.8/4.11 are not deterministic conversion or correction rules. Defect dependencies, traceability and causal claims need external context and confirmation. |
| §4.3 risk and prioritization (¶9–23, 38–47) | A *qualitative, explicitly unresolved* local risk concern may be associated with a confirmed local defect once its representation is approved. No risk value exists in MVP. | `ρ_ij`, `p_ij`, `I_ij`, `κ_j(C)` and `r_ij=ρ_ij·p_ij·I_ij·κ_j(C)` refer to defect-to-**product-`q_j`** consequences. Source states operands require rules, data or calibration; `Ψ_j`, `Π_i`, product risk profile and defect graph are not fixed local algorithms. No numerical risk, priority or automatic action follows. |

For clarity, the five distinct scope dispositions in §§4.1–4.3 are:

| Disposition | §4.1 process | §4.2 quality | §4.3 defect/risk/action |
| --- | --- | --- | --- |
| Directly applicable to one requirement | Initial extraction/assessment with version-specific source provenance as a *principle*; MVP implements the initial run. | Artifact-property assessment with separate C/V/U results, exact Evidence and explanations under the approved MVP rules. | One requirement can be a defect target; an accepted observation can be preserved as `SIGNAL` under the sole approved vague-term rule. |
| Locally specializable only after new approval | Stable local version/state, changed-evidence invalidation, feedback and before/after comparison. | Expanded feature coverage, type applicability, possibly additional individual properties and characteristic-specific uncertainty. | Confirmed defect, local concern, authorized action, verification and reassessment records. |
| Requires multiple requirements/specification data | Specification-wide change/coverage and artifact-impact relations. | `R_j`, set metrics, semantic membership and set-level aggregation; existing `AGG-MVP-001` is supported separately. | Pairwise conflict/duplication, graph dependencies and set-level defect aggregation. |
| Requires product or lifecycle evidence | Architecture/code/test/operation stages, checkpoints and product-stage transitions. | `Q`, `ŷ_j`, calibrated `Fθ_j`, dynamic/static product evidence and product index. | Defect-to-product `q_j` risk links, test/architecture/code actions and observed product effect. |
| Missing formula, calibrated operand or external input | Local state/update/comparison contract; checkpoint thresholds are unset and not imported. | Extra-property rules and external domain authorities; product model parameters are not local formulas. | Confirmation, severity/confidence, `ρ/p/I/κ`, `Ψ`, priority parameters, action-selection and verification rules. |

The target decomposition is:

```text
Requirement (one Ukrainian sentence, clauses retained together)
→ Feature Extraction
→ Characteristic Assessment
→ Finding Interpretation
→ Local Defect/Risk Representation
→ Corrective Action
→ Reassessment
→ Explainable Result
```

It describes dependency and responsibility, **not** an approved executable
algorithm for the latter stages. Each stage must keep its source/version and
Evidence lineage; an unresolved stage cannot silently synthesize the next
stage's output.

| Stage and source | Purpose; required input → target output | Existing MVP; missing decision and dependency | Evidence and reference validation needed |
| --- | --- | --- | --- |
| Requirement (§2.1; §4.1 ¶8–10) | Assess one Ukrainian sentence as one requirement, clauses intact; original text, language, source and proposed version → one stable requirement identity. | `RequirementReader` creates per-file order IDs and source line, not stable cross-version identity. Version mapping needs a local process contract; sentence validation is optional future behavior requiring approval if proposed, not a prerequisite. | Original punctuation/text and source line; one-sentence/multi-clause and cross-version identity cases, plus multi-sentence-line cases if validation is proposed. |
| Feature Extraction (§3.1 ¶9–13; §2.3 ¶3–5) | Requirement and approved linguistic rules → six typed outcomes, diagnostics and exact Evidence, potentially extended only after approval. | `BaselineFeatureExtractor`/detectors implement narrow Ukrainian subsets; `RQD-006`/`008` and SRM-07 extensions gate SRM-04/06/08. | Every accepted span round-trips to the same version's text; repeated, negative and unresolved cases, parser-independent domain values. |
| Characteristic Assessment (§2.1 Table 2.3; §4.2 ¶4–6) | Extraction result and approved applicability/calculation rules → independent stateful C/V/U assessments, any *separately approved* additions. | Three calculators and `RequirementQualityProfile` implemented; full applicability, external inputs, extra properties and uncertainty remain SRM-09/10 decisions before SRM-11. | Contributing features, rule IDs, reasons; binding value, `UNKNOWN`, `NOT_APPLICABLE`, mixed-state and independent-calculator cases. |
| Finding Interpretation (§3.1 ¶10–11, 31; §4.3 ¶2–6) | Observations/assessment, applicable criterion and confirmation evidence → `SIGNAL` or approved `QUALITY_PROBLEM`, with no implicit promotion. | `FIND-U-VAGUE-001` emits `SIGNAL`; `Finding` can *represent* a problem but no conversion is implemented. `RQD-016` gates SRM-10/11. | Exact accepted Evidence refs, or approved absence provenance without fake spans; expert-confirmed/false-positive cases and no-conversion cases. |
| Local Defect/Risk Representation (§4.3 ¶4–19) | Confirmed problem plus version, authority and context → traceable local defect/uncertainty record and, only if approved, local risk description. | No defect/risk object or calculator. Define signal/candidate/confirmed transitions, which tuple fields are applicable, unknown operands and whether qualitative concern is in scope; approval must precede domain/implementation. | Link each defect to finding, requirement version and confirmation; risk operand source and unavailable-value cases; **no** numeric expected results without calibrated rules. |
| Corrective Action (§4.3 ¶25–30; §4.1 ¶29–31) | Confirmed problem, authorized change proposal and verification criterion → action record tied to target/version; user/researcher-approved change, not an invented rewrite. | No action engine. Define action provenance, problem link, expected correction, dependency/cost applicability, authorization and verification status before implementation. | Problem/action/changed-text lineage; positive, rejected, unresolved and nonautomatic-action references. |
| Reassessment (§4.1 ¶8–13, 29–33; §4.3 ¶30–34) | Version `v1`, action/changed Evidence and `v2` → freshly extracted/assessed `v2`, comparison and unresolved-problem status. | CLI can be rerun on text but stores no versioned pair or action relationship. Define identity, event trigger, invalidation, independent recomputation and state comparison; never average old and new scores. | Exact Evidence bound separately to each version; changed/unchanged/unknown and signal-persistence cases; comparison is of local artifact results, not proven product improvement. |
| Explainable Result (§3.3 ¶30–36; §4.2 ¶25–26) | Completed Level-1 state, provenance and uncertainties → Level-2 human-readable account. | `ConsoleReporter` formats MVP profiles, rule IDs, findings and Evidence refs; full-version, defect, risk, action and comparison rendering pending SRM-12. | Rendered explanation must correspond to structured outputs and source version; no new score, confirmation, probability or action invented by reporter. |

### Local process, risk and action contracts still absent

The approved `Requirement` has `id`, `source_line`, `text`; it has no version.
`Evidence` is exact and linked to that ID, but no cross-version carry-forward
or invalidation rule exists. A local `v1 → v2` design needs stable identity,
version provenance, explicit changes in text and/or evidence, re-extraction
of dependent observations, per-version preservation, and comparison of states
and values without interpreting a numeric difference as product improvement.
The requirement may remain one multi-clause sentence across versions; any
new sentence or requirement boundary is a separate scientific/input decision.

The existing `Finding` has `kind`, rule, requirement and Evidence references.
Its `QUALITY_PROBLEM` shape is representable, but no rule produces one.
Chapter 4.3's `d_i` distinguishes a confirmed defect from severity,
confidence, stage and version; the latter are **not** available or approved in
MVP. A local defect record cannot be constructed from a vague term or a low
score alone. `r_ij` is a *source-described* normalized working formula for
possible **product-characteristic** consequences, not an approved numerical
local-requirement risk formula. Its `ρ`, `p`, `I`, `κ` operands, calibration,
missing-value behavior and target `q_j` links are unavailable. The same is
true of `Ψ_j`, priority vector/optimizer and causal graph. The defensible
current representation is the existing evidence-backed `SIGNAL` and
assessment; even a qualitative risk record requires an explicit approved
meaning and source/provenance contract.

Chapter 4.3's action tuple specifies target, change, expected effect,
dependencies, cost and verification, but not an executable rewrite rule.
For a one-requirement adaptation, action provenance and authorization,
problem-to-action linkage, expected correction, verification method, version
change and unresolved status must be defined. `v2` requires a separately
provided or authorized revision; the system must not generate one or claim
the action succeeded solely because an MVP score rose. A genuine later
product effect would require independent product evidence outside this local
milestone.

### Two-level result architecture

**Level 1 — Scientific model result:** immutable/versioned observations,
Evidence, characteristic assessments, Findings and, only after approval,
local defect/risk, action and reassessment records with explicit unknowns.
**Level 2 — User interpretation:** a human-readable rendering of Level 1,
including limits of supported detection and unresolved decisions. The
reporter cannot calculate, confirm a defect, generate a risk probability,
select a corrective action or suppress `UNKNOWN`/`NOT_APPLICABLE`. This
extends the future architecture already recorded in
[mvp-v0.1-baseline.md](mvp-v0.1-baseline.md), without changing the approved
MVP `ConsoleReporter` (§19 of `model-spec.md`).

## Scientific traceability matrix

Each ID is one classified element. `—` means that no approved representation,
component, or binding reference test exists; it is **not** a suggestion to
invent one. Paths are relative to the repository root. A test named here is
an existing reference/regression test, not proof of scientific approval for
a broader rule. `IMPLEMENTED` refers only to the precisely named baseline
behavior. `APPROVED_NOT_IMPLEMENTED` is reserved for a fully approved
executable rule not yet in production; no such additional rule was identified.
**Status is implementation/scientific readiness, not milestone scope**;
the separate scope register after this matrix handles target versus adjacent
behavior. The arrows are traceability links, not a proposed formula.

| ID | Dissertation concept → local scientific component | Required input / feature or metric → scientific rule | Domain representation → existing implementation or missing implementation → reference validation | Source and implementation status |
| --- | --- | --- | --- | --- |
| T01 | Individual artifact and observations → C/V/U | One `r_i`; exact source spans, six independent outcomes; no inference of quality from occurrence | `Requirement`, `Evidence`, `RequirementFeatures`, `RequirementExtractionResult` → `reader.py`, `extractor.py`, `domain/` → `tests/test_reader.py`, `tests/test_extraction_result.py` | §2.1 ¶5–6; §2.3 ¶4–8; model-spec §§6–7.5; **IMPLEMENTED** |
| T02 | Local completeness → C | Condition/context → approved `COND-UK-001` subset | `condition_contexts` outcome → `detectors/condition_context.py` → `tests/test_condition_context_detector.py` | §2.1 Table 2.1; model-spec §§7.2, 7.14.3; **IMPLEMENTED** |
| T03 | Local completeness → C | Expected result → approved normative `RESULT-UK-001` subset | `expected_results` outcome → `detectors/expected_result.py` → `tests/test_expected_result_detector.py` | §2.1 Table 2.1; model-spec §§7.2, 7.14.4; **IMPLEMENTED** |
| T04 | Local completeness and verifiability → C/V | Quantitative acceptance criterion → `ACCEPT-QUANT-001` clause-level judgeability, not general non-numeric acceptance | `acceptance_criteria` outcome → `detectors/acceptance_criterion.py` → `tests/test_acceptance_criterion_detector.py` | §2.1 Table 2.1; §2.3 ¶18–21; model-spec §§7.14.5, 7.15; **IMPLEMENTED** |
| T05 | Local completeness → C | Three mandatory applicable outcomes; `C_i=(c_condition+c_result+c_acceptance)/3`; required unresolved input withholds | `CharacteristicAssessment(Fraction)` → `calculators/completeness.py` → `tests/test_completeness_calculator.py` | §2.1 Table 2.3; *approved MVP operationalization* model-spec §§7.16, 8; **IMPLEMENTED** |
| T06 | Verifiability → V | Linked quantitative target/bound → `QUANT-001`/`QUANT-UK-001` conservative subset; unresolved forms retained | `QuantitativeConstraintObservation`, component Evidence → `detectors/quantitative.py` → `tests/test_quantitative_detector.py` | §2.1 ¶12; §2.3 ¶17–21; model-spec §§7.6, 7.14.6, 7.15; **IMPLEMENTED** |
| T07 | Verifiability → V | Explicit method → three `VERIFY-UK-001` constructions only | `verification_methods` outcome → `detectors/verification_method.py` → `tests/test_verification_method_detector.py` | §2.1 Table 2.1; model-spec §§7.14.7, 7.15; **IMPLEMENTED** |
| T08 | Verifiability → V | Acceptance → `1`; else quantitative/method → `1/2`; else complete absence → `0`; material unresolved → `UNKNOWN` | `CharacteristicAssessment(Fraction)` → `calculators/verifiability.py` → `tests/test_verifiability_calculator.py` | §2.1 Table 2.3; *approved MVP operationalization* model-spec §§7.16, 9; **IMPLEMENTED** |
| T09 | Linguistic smell → U | `UK-VAGUE-001`, exact ten-seed `uk_vague_terms_v1` matching; one accepted occurrence → one `FIND-U-VAGUE-001` `SIGNAL`, never confirmed defect | `VagueTermOccurrence`, `Evidence`, `Finding` → `detectors/vague_terms.py`, `calculators/unambiguity.py` → `tests/test_vague_terms.py`, `tests/test_unambiguity_calculator.py` | §2.1 ¶10; §2.3 ¶12–16; model-spec §§7.8, 7.14.8, 7.16.5; **IMPLEMENTED** |
| T10 | Unambiguity → U | No supported signal → `1`; ≥1 → `1/2`; incomplete scan with none → `UNKNOWN`; no `0` | `CharacteristicAssessment(Fraction)` → `calculators/unambiguity.py` → `tests/test_unambiguity_calculator.py` | §2.1 Table 2.3; *approved MVP operationalization* model-spec §§7.16, 10; **IMPLEMENTED** |
| T11 | Multidimensional individual assessment → C/V/U | Separate rule IDs, Findings, explanations; Cases A–E binding for MVP, no scalar | `RequirementQualityProfile` → `assessor.py`, `domain/profile.py` → `tests/test_requirement_quality_profile.py`, `tests/test_requirement_quality_assessor.py` | §2.1 ¶20–29; model-spec §§7.16.8, 11, 13; **IMPLEMENTED** |
| T12 | Applicability and missingness → C/V/U | Approved MVP simplification and per-rule withholding; `UNKNOWN`/`NOT_APPLICABLE` never zero | `CriterionApplicability`, `FeatureDetectionOutcome`, `CharacteristicAssessment` → `domain/`, calculators → `tests/test_assessment_contracts.py`, calculator tests | §2.3 ¶15–16, 38–41; model-spec §§7.4, 7.16, 8–10, 14; **IMPLEMENTED** |
| T13 | Structural roles → C/V, possible singularity | General attachment, non-modal/coordinated results, non-numeric acceptance and broader method grammar undefined beyond subsets (`RQD-006`) | Existing outcomes accommodate some observations; no approved expanded detector → — | §2.1 Table 2.1; model-spec §§7.14.13, 18 RQD-006; SRM-03/04; **PARTIALLY_DEFINED** |
| T14 | Operationalized bounds → V/C | Complex metric/context linkage, nested/compound constraints, count roles, ranges, written numbers unresolved (`RQD-008`) | Existing typed quantitative parts/diagnostics, no general rule → — | §2.3 ¶17–21; model-spec §§7.14.6, 7.15.10, 18 RQD-008; SRM-05/06; **PARTIALLY_DEFINED** |
| T15 | Linguistic ambiguity → U | Broader vocabulary, lexical/syntactic context and false-positive exceptions not approved; signal ≠ confirmation | Existing occurrence and signal only; no extended detector → — | §2.1 ¶10; model-spec §§7.8, 10; SRM-07/08; **PARTIALLY_DEFINED** |
| T16 | Type-dependent criteria → all proposed characteristics | Full requirement types, per-type applicability, mixed/unknown handling and optional classifier not defined; MVP simplifications stay | Existing applicability enum; no full type model → — | §2.1 Table 2.3; §2.3 ¶4–5, 14–16; model-spec §§7.16.3, 18 RQD-023; SRM-09; **RESEARCH_DECISION_REQUIRED** |
| T17 | Confirmed material ambiguity → U | Confirmation/exception procedure and `U_i=0` mapping absent (`RQD-004`) | Existing `Finding` can express kind, but no conversion or `0` rule → — | §2.1 Table 2.3; model-spec §§7.16.4, 10, 18; SRM-07/10; **RESEARCH_DECISION_REQUIRED** |
| T18 | Confirmed violation → C/V/U and any added property | `QUALITY_PROBLEM` criterion, confirmation, absence semantics and Evidence conditions absent (`RQD-016`) | `FindingKind.QUALITY_PROBLEM` representable, never produced by current calculators → `tests/test_assessment_contracts.py` checks *shape only*, no reference conversion test | §2.1 Table 2.2; §2.3 ¶12–16; model-spec §§7.16.5, 18; SRM-10/11; **RESEARCH_DECISION_REQUIRED** |
| T19 | One logical obligation → singularity | Independence/segmentation, applicability, formula and reference cases absent; Table 2.3 is illustrative | No `CharacteristicId` or detector → — | §2.1 Tables 2.1, 2.3; model-spec §3.1; SRM-03/09/10; **RESEARCH_DECISION_REQUIRED** |
| T20 | Presentation conformance → conformance | Governing template, terminology, applicable rules/denominator and score absent | No `CharacteristicId` or rule registry → — | §2.1 Tables 2.1, 2.3; §2.3 ¶4–5; SRM-09/10; **RESEARCH_DECISION_REQUIRED** |
| T21 | Domain truth → correctness | Authority, validation, applicability and scale absent | No external-source domain result → — | §2.1 Table 2.1, ¶13, Table 2.3; SRM-09/10; **RESEARCH_DECISION_REQUIRED** |
| T22 | Realizability → feasibility | Resource/technical/regulatory context, adjudication and scale absent | No context model or assessment → — | §2.1 Table 2.1, ¶13, Table 2.3; SRM-09/10; **RESEARCH_DECISION_REQUIRED** |
| T23 | Essential need → necessity | Goals, source/rationale linkage, applicability and result rule absent | No external-source domain result → — | §2.1 Table 2.1, ¶9; SRM-09/10; **RESEARCH_DECISION_REQUIRED** |
| T24 | Scope fit → relevance | Project scope/goals, architecture context, applicability and result rule absent | No external-source domain result → — | §2.1 Table 2.1, ¶9; SRM-09/10; **RESEARCH_DECISION_REQUIRED** |
| T25 | Evidence coverage/reliability → possible local result metadata | `RQD-020` unresolved; no approved detector confidence, reliability values or calibration | Current assessment/Finding intentionally omit numeric metadata → — | §2.3 ¶38–41; §3.3 ¶14–19; model-spec §§7.16, 18; SRM-10/13 if included; **RESEARCH_DECISION_REQUIRED** |
| T26 | Binding full-model evaluation → all approved outputs | Reviewed positive/negative, partial and false-positive cases plus predeclared evaluation measures/thresholds absent for extensions | MVP Cases A–E and tests exist; no full-model corpus → — | §2.3 ¶52; model-spec §§7.16.8, 18 RQD-017; SRM-10/13; **PARTIALLY_DEFINED** |
| T27 | Human interpretation of full model → reporting | Full-model explanation/evidence rendering beyond MVP exact-fraction reporter not specified yet; scientific result must remain unchanged | Existing `ConsoleReporter` shows rule IDs, `SIGNAL` and Evidence refs; no full-model rendering → `tests/test_console_reporter.py` covers MVP only | §3.3 ¶30–36; model-spec §§15, 19; SRM-12; **PARTIALLY_DEFINED** |
| T28 | Set-level property indicator → specification summary | `x_j` and `AGG-MVP-001` property mean over computed values, separately counted unknowns | `SpecificationQualityProfile` → `aggregator.py` → `tests/test_specification_quality_aggregator.py` | §2.1 ¶21–25; model-spec §12; existing behavior, **IMPLEMENTED** |
| T29 | Set relationships → consistency, duplicates, coverage, traceability | Pairwise confirmations, expected coverage set, links and lifecycle context require a set/artifacts | No local `CharacteristicId` → — | §2.1 ¶14–16; §2.3 ¶21–30; model-spec §§2, 18 RQD-019; SRM-00 exclusion; **OUT_OF_SCOPE** |
| T30 | Requirement properties → product quality | `R → P → M → Q`, `ŷ_j=Fθ_j(...)`, risk and product index are not `a_ij`; parameters need data | No product predictor → — | §3.3 ¶26–29; §4.2 ¶4–19, 23–31; model-spec §§2, 4.2, 17; SRM-00 exclusion; **OUT_OF_SCOPE** |
| T31 | Scalar requirement quality index | `f(C,V,U,...)` has no approved formula or weights (`RQD-013` deferred); SRM-10 may ask whether needed, not authorize one | `RequirementQualityProfile` has no scalar → `tests/test_requirement_quality_profile.py` asserts absence | §2.3 ¶51–52; model-spec §§1, 11, 18 RQD-013; **OUT_OF_SCOPE** unless separately approved |
| T32 | One-sentence target unit → local requirement | Ukrainian sentence with multiple clauses retained; sentence eligibility/multi-sentence-line behavior has no new approved rule | MVP `Requirement`/reader preserves one line → `tests/test_reader.py`; no sentence-specific target validation → — | §2.1 ¶5–6; model-spec §§2, 6 and RQD-018; researcher clarification; **PARTIALLY_DEFINED** |
| T33 | Initial local assessment → quality profile | Extract and assess one present requirement under approved C/V/U rules; no persistent version state | `RequirementExtractionResult`, `RequirementQualityProfile` → `extractor.py`, `assessor.py`, calculators → `tests/test_mvp_acceptance.py` | §3.1 ¶9–13; §4.1 ¶14; model-spec §§7–11; **IMPLEMENTED** |
| T34 | Versioned local state → process | `P_j(τ,v)` is a product-characteristic state, not a local C/V/U contract; identity, version and scope of local state require approval | `Requirement` has no version; no local state component → — | §4.1 ¶8–10, 32; model-spec §4.2; **RESEARCH_DECISION_REQUIRED** |
| T35 | Changed Evidence → process | `ΔE`, `ΔS`, `𝒰_j` describe broader update; local re-extraction, invalidation and per-version provenance need rules | Existing immutable Evidence is one-result-only; no change tracking → — | §4.1 ¶10–13, 29–33; **RESEARCH_DECISION_REQUIRED** |
| T36 | Comparison of local versions → process | Compare `v1`/`v2` states, contributing evidence and unresolved findings without declaring product improvement | No paired-result model or comparison → — | §4.1 ¶29–33; §4.3 ¶30–34; **RESEARCH_DECISION_REQUIRED** |
| T37 | Defect and potential problem → local defect interpretation | `d_i=(type,target,evidence,sev,conf,τ,v)` is structural theory; signal/confirmed transition and applicable local fields absent | `Finding` can express `SIGNAL`/`QUALITY_PROBLEM`; no confirmed producer, defect object or version → `tests/test_assessment_contracts.py` tests shape only | §3.1 ¶10–11, 31; §4.3 ¶2–8; model-spec §7.16.5 RQD-016; **RESEARCH_DECISION_REQUIRED** |
| T38 | Local risk concern → one requirement | Which confirmed local defect can create which qualitative or uncertain concern, and its input/meaning, is unapproved | No risk representation or calculation; no binding case → — | §4.3 ¶9–16, 38–47; model-spec §4.2 RQD-020; **RESEARCH_DECISION_REQUIRED** |
| T39 | Numeric defect-to-product risk → `q_j` | `r_ij=ρ_ij·p_ij·I_ij·κ_j(C)` requires product-characteristic link and uncalibrated operands; not a local requirement-quality score | No operands, calculator or reference values → — | §4.3 ¶9–19, Table 4.9; **OUT_OF_SCOPE** as executable numeric rule in this local milestone |
| T40 | Corrective action → local changed requirement | `a_corr=(target,change,expected,deps,cost,verify)` is a conceptual tuple; authorization, provenance, local fields and action/problem link undefined | No action record or generator → — | §4.3 ¶25–30, Table 4.11; **RESEARCH_DECISION_REQUIRED** |
| T41 | Verification of correction → local action status | Action's verification criterion, reviewer/authority and unresolved outcome lack an operational procedure | No action-verification component/test → — | §4.3 ¶25–34; §3.1 ¶10; **RESEARCH_DECISION_REQUIRED** |
| T42 | Reassessment → local process | Changed `v2` requires fresh extraction and approved assessment, not arithmetic update; version linkage and trigger undefined | CLI can assess supplied text again, but has no `v1`→`v2` semantics → — | §4.1 ¶11–13, 29–33; §4.3 ¶30–34; **RESEARCH_DECISION_REQUIRED** |
| T43 | Scientific result versus interpretation → explainable result | Level 1 must carry evidence/assessments and future local records; Level 2 only renders | MVP reporter renders C/V/U and Evidence refs; no full local-loop output → `tests/test_console_reporter.py` covers baseline | §3.3 ¶30–36; model-spec §§15, 19; **PARTIALLY_DEFINED** |
| T44 | Full lifecycle process/checkpoints → product `q_j` | `τ_R` through `τ_O`, `K_k`, quality/evidence thresholds and stage prediction need other artifacts and calibration | No such local process implementation → — | §4.1 ¶4–7, 21–28, 35–39; **OUT_OF_SCOPE** |
| T45 | Defect graph, product risk aggregation and priority → `q_j`/set | `Ψ_j`, `Π_i`, `G_D`, `R̂_j` depend on product links, defect dependencies and contextual calibration | No product risk/priority component → — | §4.3 ¶17–23, 35–47; **OUT_OF_SCOPE** |
| T46 | Static requirement-review cycle → local findings/actions | Source describes criteria, independent/group analysis, classification, correction and recheck, not a complete automatic review procedure | Narrow detector pipeline implemented; expert confirmation/action/recheck absent → — | §3.1 ¶9–13, 31–34; **PARTIALLY_DEFINED** |

Implementation-status inventory: **IMPLEMENTED 14;
APPROVED_NOT_IMPLEMENTED 0; PARTIALLY_DEFINED 8;
RESEARCH_DECISION_REQUIRED 18; OUT_OF_SCOPE 6** (46 traced elements).
These are *counts of documentation rows*, never a percentage of scientific
model completeness. A representable `QUALITY_PROBLEM` shape does not mean
confirmed-defect behavior exists. Six non-MVP individual properties remain
theoretical candidates, not six approved calculators.

**Separate milestone-scope register:** T01–T27 and T32–T38, T40–T43, T46
are local baseline or locally specializable questions; only the precise
approved T01–T12 and T33 behavior is already executable. T28 is an
**implemented, supported adjacent** specification summary, not new local
work. T29 concerns set-level relations and is outside this milestone.
T30, T39, T44 and T45 concern product/lifecycle modeling or numeric risk and
are outside the local executable target; their *local analogues* are
separately recorded in T34–T38/T40–T43 and remain pending. T31 is an
excluded scalar index pending a separate inclusion decision. Status
`OUT_OF_SCOPE` never means a dissertation concept is scientifically
irrelevant; status `IMPLEMENTED` never means its entire source chapter is
complete.

## Scientific gaps and downstream dependencies

Each row records what is missing, why the baseline cannot supply it, and the
decision that must precede any extension. Status for all decisions in this
section is **PENDING_RESEARCHER_APPROVAL**.

| Gap / decision | Source defining the problem; why MVP does not close it | Required researcher decision → dependent roadmap issue |
| --- | --- | --- |
| G01 `RQD-006` structural detection | §2.1 Table 2.1; model-spec §§7.14.3–7.14.7 and RQD-006. Four narrow grammars do not establish general attachment, coordinated/non-modal behavior, non-numeric criteria or method sufficiency. | Specify supported grammar, Evidence spans, diagnostics, negative cases and any role features → [SRM-03 #71](https://github.com/rKiselyk/requirements-quality-assessment/issues/71) approval before [SRM-04 #72](https://github.com/rKiselyk/requirements-quality-assessment/issues/72) implementation. |
| G02 `RQD-008` quantitative/criterion semantics | §2.3 ¶17–21; model-spec §§7.14.5–7.14.6, RQD-008. MVP preserves some partial operands; it cannot decide unresolved comparator inclusivity, range, count noun, nested or context attachment by convenience. | Define exact syntax, semantics, unit policy, component links, source Evidence and unresolved cases without invented tolerances → [SRM-05 #73](https://github.com/rKiselyk/requirements-quality-assessment/issues/73) before [SRM-06 #74](https://github.com/rKiselyk/requirements-quality-assessment/issues/74). |
| G03 extended ambiguity (`RQD-007` *closed for the seed only*) | §2.1 ¶10, Table 2.3; model-spec §§7.8, 10. Ten seeded forms detect only supported signals; they do not cover all lexical/syntactic ambiguity or confirm a defect. | Approve versioned additional vocabulary, context exceptions, span and false-positive rules; keep signal distinct from confirmation → [SRM-07 #75](https://github.com/rKiselyk/requirements-quality-assessment/issues/75) before [SRM-08 #76](https://github.com/rKiselyk/requirements-quality-assessment/issues/76). |
| G04 `RQD-023` full applicability | §2.1 Table 2.3; §2.3 ¶4–5, 14–16, 38–39; model-spec §7.16.3. The three mandatory C criteria and universally applicable V are expressly MVP simplifications, not a type taxonomy. | Decide type taxonomy, each characteristic/criterion applicability, mixed/unknown type and whether classification is justified; preserve NA/UNKNOWN → [SRM-09 #77](https://github.com/rKiselyk/requirements-quality-assessment/issues/77), then SRM-10/11. |
| G05 additional text-structural properties | §2.1 Tables 2.1 and 2.3 (singularity, presentation conformance); model-spec §§3.1, 7.11. No approved independent-obligation or governing-template rule and no matching ID/score. | Decide whether each belongs to full local profile; if yes approve necessary source template, feature, applicability, decision procedure/formula, Evidence and cases → SRM-03/04 as needed, SRM-09, [SRM-10 #78](https://github.com/rKiselyk/requirements-quality-assessment/issues/78), then [SRM-11 #79](https://github.com/rKiselyk/requirements-quality-assessment/issues/79). |
| G06 context-dependent individual properties | §2.1 Table 2.1, ¶9, ¶13; Table 2.3 (necessity, relevance, correctness, feasibility); §2.3 ¶4–5. A text-only line lacks goals, authoritative domain facts and feasibility constraints; illustrations do not supply scales. | Decide inclusion versus explicit exclusion for each in this milestone; if included approve external inputs, validation authority, applicability, result states/rules and reference cases → SRM-09/10 before SRM-11. Do not silently widen the file-input contract. |
| G07 `RQD-004` confirmed ambiguity | §2.1 Table 2.3; model-spec §§7.16.4, 10. Automated `1/2` signals never establish material ambiguity or `U_i=0`. | Approve confirmation and context-exception procedure and its assessment mapping, or explicitly exclude it → SRM-07 and SRM-10 before SRM-11. |
| G08 `RQD-016` confirmed Findings | §2.1 Table 2.2; §2.3 ¶12–16, 29–30; model-spec §7.16.5. The domain can represent `QUALITY_PROBLEM`, but production emits only vague `SIGNAL`; absence alone is not a violation. | Define exact applicable violation, processing completeness, confirmation, `criterion_id`, Evidence/absence provenance, explanation and binding cases for each conversion → SRM-10 before SRM-11/12. |
| G09 `RQD-020` reliability metadata | §2.3 ¶38–41; §3.3 ¶14–19; model-spec §§7.16, 18. Numeric confidence/evidence reliability excluded from MVP; no validation or calibration. | Decide whether to keep excluded or add separate metadata with source and validated derivation, never fold it into a score by assumption → SRM-10; validation in SRM-13 if included. |
| G10 `RQD-013` scalar index | §2.3 ¶51; model-spec §§1, 11, 18. C/V/U deliberately separate; no approved integrated rule. | Decide whether full local model even requires an integrated index; if yes separately approve formula, applicability and missingness; otherwise retain profile → SRM-10 before SRM-11/12. No index is proposed here. |
| G11 `RQD-017` expanded reference cases and validation | §2.1 Table 2.3; §2.3 ¶52; model-spec §§7.16.8, 18. Binding A–E cover MVP only; dissertation demonstrations are not independently reviewed labels or accuracy evidence. | Approve feature/assessment/Finding reference cases and predeclare annotation, evaluation measures, thresholds and limitations → SRM-03/05/07/09/10 for rule cases, [SRM-13 #81](https://github.com/rKiselyk/requirements-quality-assessment/issues/81) for independent corpus/validation. |
| G12 full interpretation and exact evidence surface | §3.3 ¶30–36; model-spec §§15, 19. MVP console surfaces Evidence refs and explanations, not full source spans in output; future characteristics and confirmation require a new report contract. | Approve how additional completed results and exact source Evidence are displayed without changing Level 1 or promoting signals → [SRM-12 #80](https://github.com/rKiselyk/requirements-quality-assessment/issues/80), after SRM-10/11. |
| G13 one-sentence target versus line-based MVP (`RQD-018` preserved) | §2.1 ¶5–6; model-spec §§2, 6. The accepted reader treats a whole line as one requirement even with several sentences, whereas the approved target assessment format is one Ukrainian sentence; clauses must stay together. | No sentence-validation feature is required as a prerequisite. If rejection or diagnostics for a multi-sentence line are later proposed, approve their behavior separately without changing the frozen reader or splitting objects. Stable cross-version identity belongs to the local-state contract proposed for SRM-14. |
| G14 local process state and evidence changes | §4.1 ¶8–13, 29–33. `P_j(τ,v)` belongs to product `q_j`; MVP has exact Evidence for one extraction but no requirement version, change event or evidence invalidation. | Define local identity, version, state, change provenance, evidence currency and fresh re-extraction trigger; explicitly separate from lifecycle stages → additional scientific process contract before domain/integration work. |
| G15 local defect/risk representation | §3.1 ¶10–11; §4.3 ¶2–19 and Tables 4.8–4.9. MVP `Finding` represents a `SIGNAL`; it does not produce a confirmed defect, severity/confidence or calibrated risk. Source `r_ij` addresses product `q_j`. | Approve candidate/confirmed transitions, minimal local defect fields, qualitative concern semantics or justified risk operands and unknowns; leave product formula unexecuted → `RQD-016`/`020` and additional risk contract before implementation. |
| G16 local corrective-action record and verification | §4.3 ¶25–34, Table 4.11. Source tuple and examples specify roles but no authorized change generation, linkage or success criterion; MVP has no action state. | Define action authority/provenance, confirmed-problem link, target, expected correction, verification procedure, refusal/unresolved status and reference cases; no invented requirement rewrite → additional action contract and implementation work. |
| G17 local reassessment and comparison | §4.1 ¶11–13, 29–33; §4.3 ¶30–34. Repeated standalone CLI runs are not a versioned action → reassessment sequence, and product `Δŷ_j`/`ΔRisk_j` are not local quality evidence. | Define `v1`/`v2` relationship, independent recomputation, comparison of states/Evidence/Findings, stale and unresolved problems and interpretation limits → additional process/action contract, then integration and SRM-13 cases. |

Dependency order is scientific approval (`SRM-03`, `05`, `07`, `09`, `10`
**plus the proposed SRM-14/16/18 local contracts**)
→ parser-neutral domain representation and evidence contracts
→ feature extraction (`SRM-04`, `06`, `08`)
→ independent characteristic calculation/Finding interpretation (`SRM-11`)
→ approved local state/reassessment, defect/risk and action implementations
  (proposed SRM-15/17/19)
→ full local integration and Level-2 reporting (including those components)
→ independently annotated full local validation (including those components).
The quantitative and structural approval streams can proceed separately,
but no detector approval
licenses a calculator formula. The full type/applicability decision and
characteristic/confirmed-Finding rules gate the corresponding SRM-11 behavior.
SRM-13's methodology and reference labels must be fixed before interpreting
experimental results and must account for the proposed local state, risk and
action components in any claim of *full local* validation. The existing
six-family boundary may be extended only
after the scientific and domain contracts specify any new family; the
present six cannot be silently reinterpreted.

## Proposed roadmap adjustments for researcher review

The existing [SRM-03–SRM-13 roadmap](https://github.com/rKiselyk/requirements-quality-assessment/issues/70)
covers structural approval/implementation (03/04), quantitative approval/
implementation (05/06), linguistic approval/implementation (07/08),
applicability (09), characteristic/Finding rules (10), assessor (11),
reporting/integration (12) and experimental validation (13). Retain those
scopes and dependencies. SRM-10's confirmed-Finding contract can provide a
prerequisite for local defects, but a `Finding` is not by itself the §4.3
defect/risk/action model. SRM-12's current end-to-end reporting scope does not
specify versioned actions or reassessment. SRM-13's present dataset does not
specify before/after correction or risk-operands validation.

The researcher has **proposed** the following additional allocation for the
approved local scope. These labels are **not existing or approved GitHub
issues**; no issue is created or changed by this document.

| Researcher-proposed allocation | Local component | Approval boundary |
| --- | --- | --- |
| SRM-14/15 | Local assessment state, requirement versions, changed Evidence and reassessment | Scientific state/reassessment rules must be approved before implementation; preserve the frozen line-based Reader. Sentence validation is not a prerequisite. |
| SRM-16/17 | Local defect and risk representation | Confirmed-problem and risk semantics require separate approval; `SIGNAL` stays distinct, and no numeric risk follows from an uncalibrated formula. |
| SRM-18/19 | Local corrective actions, verification and their link to reassessment | Action authority, provenance, expected correction and verification need approval; no automatic rewrite or success claim by assumption. |

The precise issue bodies and scientific-versus-implementation split within
each proposed pair await researcher action. Existing SRM-10 Finding rules
are a prerequisite for any confirmed local defect; they are not risk approval.
Full local integration must connect the implemented state/reassessment,
defect/risk and action components while preserving the Level-1/Level-2
boundary. Full local experimental validation must include their Evidence,
version, uncertainty, action and before/after reference cases. The current
SRM-12/13 scopes alone do not establish those future results; the researcher
will reconcile integration and final validation sequencing after the proposed
allocations become actual issues.

This proposed allocation is **not** an assertion that SRM-03–13 already
approve local risk, action or reassessment, and not authorization to
broaden one issue branch or PR silently. Full product/lifecycle stages,
predictors, risk aggregation, prioritization optimization and specification
semantic analysis remain outside the clarified local target.

## Researcher Decisions Required

All entries are **PENDING_RESEARCHER_APPROVAL**. The approved baseline in
the middle column remains in force until a recorded decision supersedes it.

| Decision ID | Scientific context / approved baseline | Missing decision and implementation consequence | Related SRM issue |
| --- | --- | --- | --- |
| `RQD-006` | Local C/V structural observations; narrow `COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, `VERIFY-UK-001` only | General grammar, roles and Evidence/uncertainty rules; expanded detectors blocked | 03 → 04 |
| `RQD-008` | Linked quantitative partial observations and narrow acceptance composition | Complex metric, boundary, unit/context and compound interpretation; extension blocked | 05 → 06 |
| `SRM-07-LING` | `RQD-007` seed closed; `SIGNAL` only | Whether and how to extend vocabulary/syntax, exceptions, confirmation categories and references; new linguistic detector blocked | 07 → 08, 10 |
| `RQD-023` | No type inference; MVP C/V applicability simplifications and explicit UNKNOWN | Full type/criterion matrix or explicit continued exclusion; type-aware calculation blocked | 09 → 10/11 |
| `SRM-02-SCOPE-S` | §2.1 singularity example; no MVP local characteristic | Include or exclude singularity; if included define independence, input, applicability, result and reference cases; new assessment blocked | 03/09/10 → 11 |
| `SRM-02-SCOPE-F` | §2.1 conformance example; no MVP template metric | Include or exclude conformance; if included define authoritative project rules, denominator, applicability and cases; new assessment blocked | 09/10 → 11 |
| `SRM-02-SCOPE-R` | §2.1 correctness example; no domain-validation input | Include or exclude correctness; if included define authority, confirmation and assessment scale; text-only evaluation blocked | 09/10 → 11 |
| `SRM-02-SCOPE-E` | §2.1 feasibility example; no constraint/resource model | Include or exclude feasibility; if included define external evidence and adjudication; text-only evaluation blocked | 09/10 → 11 |
| `SRM-02-SCOPE-N` | §2.1 necessity concept; no numeric example or source linkage | Include or exclude necessity; if included define source/goal proof, applicability and output; text-only evaluation blocked | 09/10 → 11 |
| `SRM-02-SCOPE-REL` | §2.1 relevance concept; no numeric example or scope context | Include or exclude relevance; if included define project scope evidence and output; text-only evaluation blocked | 09/10 → 11 |
| `RQD-004` | `CALC-U-MVP-001` permits `1/2`/`1`; `0` reserved | Confirmation, exceptions and `0` mapping or explicit exclusion; no confirmed U result | 07/10 → 11 |
| `RQD-016` | Finding representation and one vague `SIGNAL` approved | Exact `QUALITY_PROBLEM` conversions, including absence provenance; no production problem findings | 10 → 11/12 |
| `RQD-020` | Confidence/reliability excluded, not resolved scientifically | Keep excluded or approve independent calibrated metadata; no numeric confidence field | 10, 13 if included |
| `RQD-013` | No scalar local score; C/V/U independent | Decide whether full model needs an index; any formula and missingness separately gated | 10 → 11/12 only if approved |
| `RQD-017` / `SRM-13-VALIDATION` | MVP Cases A–E binding; no full-model corpus | Independently reviewed extension cases, annotation and predeclared evaluation/acceptance criteria; no full-model validation claim | 03/05/07/09/10 → 13 |
| `SRM-12-INTERPRETATION` | MVP exact-fraction console with Evidence refs; Level 1 unchanged | Full-result and exact-Evidence presentation contract; no unapproved scientific interpretation in reporter | 12, after 10/11 |
| `SRM-02-SENTENCE` | `RQD-018` MVP line unit remains approved; researcher-approved target format is one Ukrainian sentence, clauses retained | No sentence-validation implementation is required. If a future issue proposes multi-sentence-line diagnostics or rejection, approve that behavior separately without splitting or altering the MVP Reader. | Optional future input contract; not a gate for proposed SRM-14/15 or integration |
| `SRM-02-LOCAL-STATE` | §4.1 version/provenance principle; MVP `Requirement`/Evidence carry no version | Define stable requirement/version identity, local state, changes, evidence validity and unknowns; versioned results blocked | Researcher-proposed SRM-14/15 → full integration/validation |
| `SRM-02-LOCAL-DEFECT-RISK` | `RQD-016` Finding shape and signal-only production; §4.3 tuple/formula concern product `q_j`, uncalibrated operands | Define local confirmed-defect representation and any qualitative concern; decide if/when numerical risk belongs, and independently approve all operands/calibration before calculation; risk output blocked | 10 prerequisite; researcher-proposed SRM-16/17 → full integration/validation |
| `SRM-02-LOCAL-ACTION` | §4.3 action tuple/examples, no executable correction; no MVP action | Define action provenance/authority, problem link, expected correction, verification, unresolved/rejected state and no automatic rewrite; action behavior blocked | Researcher-proposed SRM-18/19 → full integration/validation |
| `SRM-02-LOCAL-REASSESS` | §4.1 feedback principle; rerunning MVP independently creates no paired history | Define change trigger, fresh extraction, evidence invalidation, versioned comparison, problem persistence and limits of improvement claim; reassessment behavior blocked | Researcher-proposed SRM-14/15, with action linkage from SRM-18/19 → full integration/validation |
| `SRM-02-ROADMAP` | SRM-03–13 cover detector, applicability, assessment, integration and validation but do not allocate complete local risk/action/version work | SRM-14/15, 16/17 and 18/19 are proposed allocations, not existing or approved issues; issue bodies and final integration/validation sequencing remain to be reconciled | Researcher-proposed SRM-14–19 |

The researcher-approved **scope** is recorded here; no approval of a new
detector, formula, defect confirmation, risk calculation, action or
reassessment rule is recorded. The earliest blocker for each new behavior is
its relevant scientific decision; approved MVP behavior remains executable
and unchanged.
