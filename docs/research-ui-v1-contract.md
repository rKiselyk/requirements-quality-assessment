# Research UI v1 application and presentation contract

**Contract ID:** `RESEARCH-UI-V1-CONTRACT`

**Contract version:** `1`

**Milestone:** Research UI v1 (#5)

**Issue:** RUI-01 / #171

**Status:** `FROZEN_FOR_RESEARCH_UI_V1`

## 1. Purpose, authority, and scope

This document is the authoritative application and presentation contract for
Research UI v1. It defines how a future web application may expose the accepted
scientific core without becoming a second scientific implementation.

The approved visual/page baseline is defined by [`research-ui-v1-design-spec.md`](research-ui-v1-design-spec.md), with [`assets/research-ui-v1-design.png`](assets/research-ui-v1-design.png) as its primary visual reference. The design specification and visual reference are subordinate to this contract and may not relax any scientific or lifecycle invariant recorded here.

Scientific rules remain authoritative in [`model-spec.md`](model-spec.md) and
the accepted Full Model contracts. In particular:

- [`full-model-v0.1-contract.md`](full-model-v0.1-contract.md) defines the
  bounded Full Model dependency graph and scientific boundaries;
- [`full-model-v0.1-process-reassessment-contract.md`](full-model-v0.1-process-reassessment-contract.md)
  defines external revision, reassessment, comparison, process, and absence
  semantics;
- [`full-model-v1-theory-traceability.md`](full-model-v1-theory-traceability.md)
  maps accepted theory to implementation; and
- [`full-model-v1-research-acceptance.md`](full-model-v1-research-acceptance.md)
  records the controlled complete reference scenario and its acceptance
  evidence.

This contract does not alter those sources. If this document appears to require
a new formula, coefficient, threshold, detector, vocabulary, applicability
decision, or scientific interpretation, implementation MUST stop and the
scientific contract MUST be amended through the research process first.

Research UI v1 has three layers with deliberately different responsibilities:

| Layer | Responsibility | MUST NOT do |
|---|---|---|
| Scientific/domain | Produce typed extraction, assessment, aggregation, Full Model, reassessment, comparison, and process records under accepted rules. | Depend on HTTP, frontend state, localization, visual components, or presentation convenience. |
| Application/API | Validate an interaction case, invoke the legal accepted boundary for supplied evidence, and project typed records plus explicit section availability into canonical transport data. | Recalculate, reinterpret, complete, normalize, round, localize, or invent scientific results. |
| Frontend/presentation | Collect allowed input, submit it, retain temporary browser workflow state, localize labels, and render canonical data and limitations. | Infer results, manufacture Full Model inputs, translate evidence, equate state with value, or add scientific claims. |

FastAPI, React, persistence, authentication, deployment, and production
infrastructure are outside RUI-01. This document specifies their future
boundary only.

## 2. Primary workflow

The normal Research UI v1 workflow MUST be:

```text
one specification -> Analyze -> one assessment result
```

An ordinary user uploads one UTF-8 textual specification or pastes requirements
manually, selects **Analyze**, and receives one assessment. Input follows the
accepted reader policy: one non-empty physical line is one requirement,
leading/trailing whitespace is trimmed, blank lines are ignored, source line
numbers and input order are preserved, and requirement IDs are generated in
processing order.

The first analysis MUST NOT require a second specification, revision data,
runtime observation values, product or environment identities, predictor
parameters, risk operands, checkpoint thresholds, reassessment provenance, or
other values required only by `FullModelRequest`. There MUST NOT be a
pre-analysis wizard that asks an ordinary user to fabricate such evidence.

## 3. Meaning of “Full Model UI”

Research UI v1 exposes the full *surface* of the accepted research model. It
does not promise that requirement text alone can produce every downstream Full
Model record.

For each section:

- records supported by the supplied specification and evidence MUST be shown
  normally;
- records whose accepted evaluator ran to `UNKNOWN`, `UNRESOLVED`,
  `UNSUPPORTED`, or `NOT_APPLICABLE` MUST retain that exact state and its
  applicability, reason codes, and provenance;
- an optional downstream record that was not and could not legally be
  constructed MUST be represented by the application projection as missing or
  unavailable, not as a fabricated domain record; and
- a missing, unavailable, unknown, unresolved, unsupported, or not-applicable
  result MUST NOT be converted to numeric zero.

`FullModelService.run(FullModelRequest)` is the accepted complete controlled
path. Its request requires explicit external observation, product/environment,
revision, v2, reassessment, process, and related provenance inputs. The
application MUST NOT weaken that service or create placeholder inputs.

For an ordinary initial assessment, the future endpoint MAY orchestrate the
accepted specification-assessment path and then project unavailable downstream
sections. Such a response is a valid Research UI result even though no
`FullModelRequest` existed. The application boundary is composition and
projection, not an alternative Full Model evaluator.

## 4. One-endpoint application boundary

Research UI v1 exposes exactly one analysis endpoint:

```http
POST /api/v1/analyze
```

The endpoint accepts canonical structured request data and returns canonical
structured response data. It MUST NOT return rendered USER report text,
rendered AUDIT report text, HTML, or localized Ukrainian/English prose as the
analysis contract.

### 4.1 Logical `AnalyzeRequest`

The transport schema will be frozen by the API implementation issue, but it
MUST express this logical contract without adding scientific fields:

| Field group | Meaning |
|---|---|
| `case` | Canonical discriminator: `INITIAL`, `CONTROLLED_DEMO`, or `REASSESSMENT`. |
| current specification | For `INITIAL`, uploaded or pasted textual requirements. For `REASSESSMENT`, the explicitly supplied revised specification. Mutually exclusive upload/text encodings MAY exist at the transport boundary. |
| controlled demo identity | For `CONTROLLED_DEMO`, the identifier and version of an approved predefined scenario. No arbitrary client-supplied substitute values. |
| prior context | For `REASSESSMENT`, the complete canonical prior Full Model lifecycle result/context required to validate lineage and construct accepted before/after records without server history. A specification-only `INITIAL` response is insufficient. |
| explicit reassessment context | Only accepted predecessor process state, corrective-action/application, external revision/application lineage, evidence-reuse decisions and identity checks, and other identities required by the existing reassessment contract and actually present in or supplied to the lifecycle workflow. |

Locale is presentation state and SHOULD NOT be part of the scientific analysis
request. Request fields MUST NOT contain invented observations, parameters,
policies, revisions, or provenance merely to satisfy an internal service type.

### 4.2 Case A — initial specification assessment

`INITIAL` is the normal case. The current specification is required and no
previous result is required. The application invokes the accepted
requirement/specification orchestration and returns all supported records.
Downstream sections that require external evidence are projected as unavailable
with stable application reason codes.

An initial response MUST NOT contain reassessment or comparison records. The
corresponding pages MUST NOT appear in first-run navigation.

### 4.3 Case B — controlled demonstration scenario

`CONTROLLED_DEMO` is an explicit opt-in research demonstration. It loads the
accepted, versioned `CONTROLLED_RESEARCH_REFERENCE_SCENARIO`, including its
explicit scientific inputs, and invokes the accepted `FullModelService` path.

The request MUST identify an approved scenario; it MUST NOT permit a purported
demo to replace fixture fields ad hoc. The response MUST label the scenario and
its additional values as predefined demonstration/research-fixture data. They
are not scientific defaults and were not inferred from arbitrary uploaded
requirements.

The controlled scenario may return its accepted revision, reassessment, and
comparison records because a genuine v1/v2 lifecycle is part of that scenario.
This does not change the ordinary initial workflow.

### 4.4 Case C — reassessment

`REASSESSMENT` is an optional formal Full Model lifecycle action. It is legal
only when:

1. the prior canonical result/context contains every prerequisite required by
   the accepted process/reassessment contract, including a predecessor process
   state, accepted corrective-action and action-application context, external
   revision/application lineage, and required evidence-reuse decisions and
   identity checks;
2. the user explicitly chooses an eligible reassessment action;
3. the user explicitly supplies the externally revised specification; and
4. the subsequent analysis is explicitly submitted.

A successful ordinary specification-only `INITIAL` assessment does not produce
those lifecycle prerequisites and MUST NOT by itself enable formal
reassessment. Neither the application nor the browser may fabricate a
predecessor process state, `CorrectiveAction`, `ActionApplication`,
problem/risk/relation record, revision lineage, evidence-reuse identity check,
or any other required lifecycle record.

The backend remains stateless. The request therefore carries the revised
specification together with the complete prior canonical context, artifact and
assessment identities, and explicit revision/evidence-reuse information needed
by the accepted process/reassessment contract. The backend validates this
context, recomputes the revised artifact independently, and constructs only
accepted compatible comparisons. A client-generated summary or displayed
number is not sufficient prior context.

No server-side lookup, hidden history, or inferred revision is permitted. The
system MUST NOT author replacement wording, claim action success, or reuse
evidence without the accepted explicit identity checks.

A future workflow that independently analyzes specification-only v1 and v2 and
then produces a formal comparison, without the current corrective-action and
process prerequisites, requires a separate approved core/application contract
before implementation. Research UI v1 does not authorize that workflow.

## 5. Logical `AnalyzeResponse`

The response is one immutable logical result projection. It SHOULD compose
existing typed records and stable references rather than define parallel
scientific concepts.

At minimum it contains:

| Group | Required content |
|---|---|
| contract identity | API/response contract version, analysis case, and controlled-scenario identity when applicable. |
| input identity | Canonical specification/artifact identity, requirement order, generated IDs, source line numbers, and unchanged trimmed text. |
| section availability | One entry per UI section with `AVAILABLE` or application-level `UNAVAILABLE`, plus a stable reason code. This wrapper describes record presence; it does not replace a domain status. |
| scientific records | Structured requirement, specification, Full Model, process, reassessment, and comparison records actually produced by accepted services. |
| trace | Exact values, states, applicability, canonical enum/code values, rule/model/parameter references, reasons, evidence, offsets, provenance, versions, calibration, and process lineage where present. |
| limitations | Stable canonical limitation codes whose localized explanations are owned by the frontend. |

Exact rational and decimal values MUST use a lossless canonical representation;
the transport implementation MUST NOT introduce floating-point conversion or
rounding. Both a record's status/state and value presence MUST be transported.

### 5.1 Section projections

| UI section | Projection responsibility |
|---|---|
| Overview | Result identity; separate C/V/U summaries; QB when produced; high-level presence/state of product-quality, risk, action, and process records; limitations. No combined score. |
| Requirements | Ordered requirement text and identity; nine-property profile where available; C/V/U values/states; findings, diagnostics, evidence references, exact spans and offsets, rules, and reasons. |
| Specification | Separate C/V/U aggregates with counts; bounded QB records, coverage, findings/relations, evidence, and trace. |
| Product Quality | Dynamic criterion, observation, conformance, `X_PE`, observed bounded result, and predicted result as distinct optional records. |
| Risk | Confirmed-problem population and relations, categorical risk, and quantitative risk as distinct records with provenance and calibration. |
| Corrective Actions | Resolution, proposal/application state, external revision identity, target evidence, and non-causal limitations. |
| Process | Process states, components, evidence associations, transitions, checkpoint records, and lineage. |
| Audit | Recursive canonical identities, exact values, evidence, offsets, reasons, rules, models, parameters, versions, calibration, and provenance. It is not pre-rendered console output. |
| Reassessment | Only an actual accepted second assessment and its v2 records. |
| Comparison | Only model-produced compatible before/after records and exact comparison semantics. |

Every evidence occurrence MUST preserve its evidence identity, requirement
identity, exact source text/span, and zero-based end-exclusive Unicode
code-point offsets as defined by the existing domain contract. Audit projection
MUST retain technical identities; presentation may collapse detail visually but
MUST NOT discard it from the response.

## 6. State and absence semantics

The API and UI MUST preserve two separate dimensions:

1. whether a typed scientific record exists in this analysis; and
2. if it exists, its domain state/status and applicability.

| Representation | Meaning | Presentation rule |
|---|---|---|
| `COMPUTED` | The approved requirement/specification rule produced an exact numeric value. | Show the exact value and `COMPUTED`; do not label it “good.” |
| `UNKNOWN` | The accepted contract cannot determine the result/value from available required inputs. | Show `UNKNOWN`, no fabricated number, and reasons. |
| `NOT_APPLICABLE` | The accepted applicability contract says the result does not apply. | Show `NOT_APPLICABLE`, no numeric zero. |
| missing optional record / section `UNAVAILABLE` | The application did not invoke or could not legally construct that optional downstream record from supplied inputs. | Show an unavailable state and stable reason; do not create a domain object. |
| `UNAVAILABLE` domain status | An accepted Full Model operation represents a required record as unavailable. | Preserve the typed status, applicability, and reasons. |
| `UNRESOLVED` | Identity, provenance, semantics, or another accepted condition remains unresolved. | Preserve the typed status, applicability, and reasons. |
| `UNSUPPORTED` | The requested/source case lies outside an implemented accepted rule. | Preserve the typed status, applicability, and reasons; do not approximate. |

`AVAILABLE` is also a Full Model processing status; it means a typed result is
available, not that its scientific outcome is favorable. Applicability
(`APPLICABLE`, `UNKNOWN`, `NOT_APPLICABLE`) MUST remain distinct from status.

For example, a valid ordinary initial result may contain computed requirement
C/V/U, computed specification aggregates, and computed QB while runtime
observation, observed product quality, prediction, quantitative risk, and
checkpoint records are unavailable. This is a complete response for the
evidence supplied, not a failed or partial calculation.

## 7. Scientific presentation guardrails

Every page and component MUST observe these rules:

- There is no overall scalar requirement-quality or specification-quality
  score.
- `COMPUTED` and `AVAILABLE` do not mean “good,” “passed,” or “safe.”
- Absence of a supported confirmed problem does not prove absence of defects.
- A `SIGNAL` is not automatically a `QUALITY_PROBLEM`.
- Observed product-quality evidence and predicted product quality are distinct
  record types and MUST be labeled separately.
- Categorical risk and quantitative risk are distinct and MUST NOT be merged.
- `INCREASED` and `DECREASED` are numeric comparison directions, not automatic
  “improved” or “worsened” claims.
- A corrective-action proposal, application, later state, or comparison is not
  causal proof that the action succeeded.
- Checkpoint `SATISFIED` means only that the configured predicate was true. It
  is not `RELEASE`, `PROCEED`, approval, or authorization.
- The bounded response-time Performance Efficiency indicator is not a complete
  Performance Efficiency or ISO product-quality assessment.
- Provisional or uncalibrated status MUST remain visible where present.

Color, iconography, ordering, and copy MUST NOT imply a forbidden claim. In
particular, the UI MUST NOT apply generic green/red success/failure semantics
to raw scientific states. Accessible non-color labels are required.

## 8. Localization boundary

Research UI v1 supports Ukrainian (`uk`) as the default locale and English
(`en`). Analysis is presentation-language-neutral. Changing locale MUST NOT
rerun extraction, assessment, aggregation, Full Model services, or comparison.

The frontend localizes navigation, headings, labels, explanatory and limitation
text, validation messages, and messages selected from stable API error codes.

The frontend MUST NOT translate or rewrite:

- user-supplied requirement text;
- exact evidence fragments or source quotations;
- rule IDs, metric IDs, model/parameter IDs, artifact/assessment IDs, or other
  canonical technical identities in audit contexts; or
- canonical enum/code values when they are shown as technical audit data.

Localized display labels MAY accompany canonical codes, but MUST NOT replace
them in the response or audit view.

## 9. Error contract

Errors use stable machine-readable codes, safe structured details, and an
optional field/path. Localized prose is not part of the API contract.

Conceptually:

```text
AnalyzeError {
  code: stable canonical code
  details: safe structured values
  path: optional request-field path
}
```

The v1 error registry is limited to boundary needs:

| Code | When used |
|---|---|
| `EMPTY_SPECIFICATION` | Initial or reassessment input has no non-empty requirements. This web-boundary decision does not change the historical CLI empty-file behavior. |
| `MALFORMED_REQUIREMENT_INPUT` | The transport/input representation cannot be decoded or mapped to the accepted reader contract. |
| `INVALID_REASSESSMENT_CONTEXT` | Prior result, lineage, v2 input, revision, or evidence-reuse context is absent, inconsistent, or invalid. |
| `INVALID_CONTROLLED_DEMO_REQUEST` | Scenario identity/version is absent, unknown, or attempts unsupported overrides. |
| `ANALYSIS_VALIDATION_FAILED` | An accepted application/domain precondition fails; safe reason codes and field context MAY be included. |
| `ANALYSIS_INTERNAL_FAILURE` | An unexpected analysis failure occurred. The response MUST NOT expose a traceback, local path, source code, secret, or raw exception. |

The implementation MAY map these codes to suitable HTTP statuses, but MUST NOT
create a production error taxonomy, correlation platform, or localized backend
message system in Research UI v1.

## 10. State ownership and lifecycle

The backend is stateless. It has no database, persistence, server-side
assessment history, users, accounts, projects, or persistent sessions.

The browser session owns:

- the current specification input;
- the current `AnalyzeResponse`;
- selected navigation state;
- locale preference;
- an eligible prior Full Model lifecycle response while an externally revised
  specification is prepared; and
- optional successful formal reassessment/comparison lifecycle state.

“New specification” clears this temporary workflow state, including retained
v1/v2 context and conditional navigation. Production persistence, sharing,
collaboration, recovery, and accounts are out of scope.

## 11. Navigation and reassessment visibility

After an ordinary first assessment, result navigation contains only:

1. Overview
2. Requirements
3. Specification
4. Product Quality
5. Risk
6. Corrective Actions
7. Process
8. Audit

These sections may be shown according to section availability. `Reassessment`
and `Comparison` MUST NOT appear as ordinary first-run pages, disabled
promises, or empty primary tabs merely because an `INITIAL` result exists. A
formal reassessment action may be offered only when the canonical prior
response/context contains every accepted lifecycle prerequisite. The ordinary
specification-only initial response is not eligible.

`Reassessment` and `Comparison` become result pages only after a valid accepted
subsequent reassessment succeeds and produces the corresponding compatible
before/after records. The frontend MUST NOT calculate a scientific comparison
from two responses independently.

Comparison MUST render model-produced before/after identity, state,
applicability, exact value, comparison kind, reasons, provenance, and
calibration. It MUST NOT infer action effectiveness, causality, improvement,
deterioration, or safety.

The approved controlled demo may expose reassessment/comparison immediately
after its one explicit demo submission because the predefined scenario itself
contains a real accepted two-version lifecycle.

## 12. Component responsibility catalogue

This section freezes responsibilities, not React implementations or visual
design.

### 12.1 Shell components

| Family | Responsibility |
|---|---|
| `AppShell` | Arrange application chrome, input workflow, result navigation, and temporary browser state. |
| `Header` | Show product/research identity and global actions without scientific interpretation. |
| `LanguageToggle` | Switch `uk`/`en` presentation without analysis. |
| `SidebarNavigation` | Show only pages legal for the current lifecycle state. |
| `PageHeader` | Identify the current page, result/artifact context, and applicable limitation copy. |

### 12.2 Generic components

`Button`, `IconButton`, `TextInput`, `TextArea`, `FileDropzone`, `Card`,
`MetricCard`, `StatusBadge`, `Tabs`, `DataTable`, `Accordion`, `Collapsible`,
`Callout`, `Alert`, `LoadingProgress`, `EmptyState`, `UnavailableState`,
`Tooltip`, and `InlineValidation` provide accessible interaction and layout.
They MUST remain semantically neutral: generic names such as `MetricCard` or
`StatusBadge` do not authorize value computation, favorable color mapping, or
collapsing absence states.

### 12.3 Scientific components

| Component | Responsibility |
|---|---|
| `ExactValue` | Render canonical exact values without floating conversion or rounding; pair them with state and units. |
| `RequirementQualityCard` | Render one requirement's structured property profile, C/V/U trace, and limitations; no scalar summary. |
| `SpecificationQualitySummary` | Render separate aggregates, counts, and QB records; no combined score. |
| `EvidenceBadge` | Identify evidence type/identity without replacing the exact span. |
| `EvidenceHighlighter` | Highlight the exact source span using preserved offsets without altering text. |
| `EvidenceDrawer` | Expose full evidence, offsets, provenance, reasons, and source identity. |
| `FindingList` | Keep finding kinds and scopes distinct; never promote `SIGNAL`. |
| `ModelPipeline` | Explain which accepted stages produced records and which lack external input; it does not execute or infer stages. |
| `ProductQualityPanel` | Keep criterion/observation/conformance, `X_PE`, observed result, and prediction distinct. |
| `RiskPanel` | Keep problem relation, categorical risk, and quantitative risk distinct. |
| `CorrectiveActionPanel` | Render proposal/application/revision records and the no-causality limitation. |
| `ProcessTimeline` | Render process/artifact state lineage and transitions, not a workflow engine. |
| `CheckpointPanel` | Render selected result, external policy, predicate, outcome, and no-release limitation. |
| `AuditTree` | Traverse canonical structured data, identities, exact values, evidence, versions, reasons, and provenance. |
| `BeforeAfterComparison` | Render accepted v1/v2 comparison records only; available conditionally after genuine reassessment/demo lifecycle. |

## 13. Traceability matrix

| UI concept | Existing source of truth | Presentation rule |
|---|---|---|
| Requirement C/V/U | `RequirementQualityProfile`, characteristic assessments/traces; `model-spec.md` CALC rules | Show three independent exact results with state, contributing features, rules, and reasons; never combine. |
| Nine-property requirement profile | `FullRequirementQualityProfile` and `full_quality` contract | Show automatic and explicit external properties with their distinct provenance; no missing-as-zero or scalar profile score. |
| Specification aggregates | `SpecificationQualityProfile`, `SpecificationCharacteristicAggregate`, `AGG-MVP-001` | Show C/V/U separately with computed/unknown/not-applicable/total counts. |
| QB | `SpecificationAssessmentResult` and accepted `cross_analysis` QB-v0.1 records | Preserve exact QB value/state, coverage, participants, comparison keys, evidence, and bounded scope. |
| Evidence/findings/diagnostics | `RequirementExtractionResult`, `Evidence`, `Finding`, detector diagnostics, assessment trace | Preserve identity, exact source span, offsets, scope, codes, and provenance; signal is not problem. |
| Dynamic criterion/observation/conformance | `dynamic_evidence` typed results and contract | Show each record and status/applicability separately; never infer an observation from text. |
| `X_PE` | `PerformanceEfficiencyFeatureProfile` | Show feature availability, applicability, temporal context, and source refs; do not call it product quality. |
| Observed product quality | `ProductQualityAssessment` with `OBSERVED_REFERENCE_INDICATOR` | Label as bounded observed result and preserve calibration/coverage; not full PE. |
| Predicted product quality | `PredictedPerformanceEfficiency` and explicit predictor/parameter records | Keep separate from observed result; show predictor, parameters, inputs, provenance, and calibration. |
| Defect/problem relations | `ProblemClaimResolution`, `DefectPopulationSnapshot`, `DefectQualityRelation` | Show supported confirmed scope and relation reasons; absence is not absence of defects and relation is not causal proof. |
| Categorical risk | `BoundedRiskAssessment` | Show classification/status/applicability/calibration; no numeric magnitude inference. |
| Quantitative risk | `QuantitativeLocalRiskAssessment` and explicit operand provenance | Show exact local result and all supplied operands separately from categorical risk; no aggregate/priority claim. |
| Corrective action | `CorrectiveActionResolution`, `CorrectiveAction`, `ActionApplication`, `ExternallySuppliedRevision` | Distinguish proposed/applied/rejected and externally supplied revision; no optimality or effectiveness claim. |
| Process/checkpoint | `ProcessAssessmentState`, `ProcessStateTransition`, `CheckpointEvaluation` | Show state/component/evidence lineage; checkpoint outcome is predicate truth only. |
| Reassessment/comparison | `ReassessmentRun`, `ResultComparison`, accepted process/reassessment contract | Recompute v2 under accepted rules; show only compatibility-gated literal comparisons and preserve calibration/non-claims. |

The UI contract intentionally references, rather than duplicates, scientific
formulas. Any scientific value displayed by the UI MUST be traceable through
these records to its accepted rule in `model-spec.md` or an accepted Full Model
contract.

## 14. Normative invariants

1. The UI is a projection of accepted typed results, never a scientific
   calculator.
2. One ordinary specification is sufficient for an initial analysis.
3. No external scientific input may be synthesized to fill a section.
4. The controlled demo is explicit, versioned fixture data, never defaults.
5. Formal reassessment requires an explicit externally revised specification
   and prior canonical context containing every accepted corrective-action,
   application, process, revision-lineage, and evidence-reuse prerequisite; an
   ordinary initial response is insufficient and the backend stores no history.
6. Missing record, domain status, applicability, and numeric value are distinct.
7. Exact values, evidence text, offsets, identities, reasons, rules, versions,
   provenance, and calibration survive transport and presentation.
8. Language switching changes presentation only.
9. Initial navigation excludes reassessment and comparison.
10. Console reporters remain presentation adapters; their strings are not an
    API schema.
11. The historical CLI and every accepted scientific behavior remain
    unchanged.
12. Specification-only v1/v2 formal comparison without the accepted lifecycle
    prerequisites requires a separate approved contract and is not authorized
    here.

## 15. Deferred implementation work

This contract authorizes no FastAPI endpoint, React/Vite application,
localization framework, upload component, query/session implementation, result
page, or reassessment UI. Those belong to later Research UI issues and MUST
implement this frozen boundary without changing the accepted scientific core.
