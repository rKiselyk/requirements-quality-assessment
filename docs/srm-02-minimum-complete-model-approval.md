# SRM-02 — Minimum Complete Single-Requirement Model Researcher Approval

**Decision status:** `RESEARCHER_APPROVED`  
**Researcher decision date:** 2026-09-23  
**Reviewed starting HEAD:** `895af64d39f0cb0a4f38763013f945f73d71e0a8`  
**Planning context:** SRM-02, existing PR #103  
**Authority:** [`model-spec.md` §2.1](model-spec.md) records the normative
implementation-model decision; this document records the approval package,
milestone interpretation, and ready-to-paste GitHub amendment.

The researcher approves the minimum complete single-requirement assessment
scope proposed by
[`srm-02-minimum-complete-model-audit.md`](srm-02-minimum-complete-model-audit.md).
The audit remains the historical pre-approval analysis and is not rewritten by
this decision.

## 1. Approved first complete model

The first complete single-requirement model is the existing approved bounded:

```text
RequirementQualityProfile(C, V, U)
```

Its independent characteristics are:

- Completeness;
- Verifiability; and
- Unambiguity.

The profile remains multidimensional. This approval adds no scalar
total-quality score and does not authorize a formula that combines C, V, and U.

The dissertation describes nine theoretical individual-requirement
properties. This milestone does not claim automatic evaluation of all nine.
The six properties outside the approved C/V/U profile remain theoretical
context or future scientific work unless each is separately operationalized
and researcher-approved.

The existing specification-level profile remains supported adjacent
functionality. It is not a new characteristic and is not required to establish
that one requirement can be assessed completely under the approved local
profile.

## 2. Complete assessment versus detector coverage

The implemented bounded six-family extraction is sufficient for the first
complete model. Milestone completeness means a complete scientific and
user-facing chain:

```text
Requirement
→ Feature Extraction
→ Characteristic Assessment
→ Quality Profile
→ supported Findings
→ Explainable Report
```

It does not mean exhaustive recognition of every possible Ukrainian
requirement formulation.

The completed model must distinguish:

- completion of an implemented bounded detector from exhaustive linguistic
  coverage;
- an accepted observation from an equivalent unsupported formulation;
- completed absence under implemented rules from universal semantic absence;
- an unresolved candidate from a negative result; and
- a supported `SIGNAL` from a confirmed defect.

Accordingly, `NOT_DETECTED` means that the implemented bounded detector
completed without accepting an observation. It must not be described as proof
that the requirement contains no equivalent semantic construction outside the
implemented grammar.

Known unsupported forms, approved-but-unimplemented detector rules, and the
limitations of maximum-looking characteristic values must be disclosed
honestly in the completed report and validation record. In particular,
`U_i = 1` remains absence of the supported vague-term signal class, not proof
of universal semantic uniqueness.

## 3. Retained applicability decision

The researcher retains the existing `RQD-023` MVP applicability
simplification for the first complete model.

Therefore:

- requirement-type classification is not a milestone prerequisite;
- no new type taxonomy or applicability matrix is required before completion;
- the approved Completeness and Verifiability applicability behavior remains
  unchanged;
- `UNKNOWN` and `NOT_APPLICABLE` remain separate states;
- detection status does not silently determine applicability; and
- no requirement type may be inferred merely for implementation convenience.

SRM-09 type classification is not on the approved first-model critical path.
It may continue as future scientific work without blocking the milestone.

## 4. SIGNAL-only Finding decision

The researcher approves a SIGNAL-only first complete model.

`FIND-U-VAGUE-001` remains:

```text
kind = SIGNAL
code = VAGUE_TERM_SIGNAL
```

This approval does not create or authorize:

- a `QUALITY_PROBLEM` conversion;
- confirmed material ambiguity;
- `U_i = 0`;
- a defect probability or confidence value;
- risk assessment;
- corrective-action generation or optimization; or
- automatic conversion of a low C/V value or completed absence into a
  confirmed defect.

`RQD-016` and the confirmed-material-ambiguity procedure remain open future
research. They do not block the first complete model while excluded under this
approved SIGNAL-only scope.

## 5. Required remaining work

The current calculations and bounded detectors are not reopened. The remaining
work completes traceability from those results to a user-facing explanation.

### 5.1 SRM-10 — minimum scientific trace and explanation contract

SRM-10 must approve the detailed scientific contract for a structured
characteristic-to-source assessment trace. At minimum, the future contract
must be capable of preserving:

- the characteristic state and exact value;
- the assessment Rule ID;
- contributing feature outcomes and accepted observations;
- accepted source Evidence;
- completed absence without invented source spans;
- unresolved diagnostics when they withhold or may alter a result;
- `SIGNAL` Finding provenance; and
- bounded-coverage limitations and non-claims.

This approval intentionally does not select final field names, domain types,
containers, cardinalities, or storage shapes. Those details remain SRM-10
research decisions. SRM-10 must not change C/V/U formulas merely to add the
trace.

### 5.2 SRM-11 — implementation

SRM-11 must implement only the approved SRM-10 trace/explanation contract and
preserve the existing assessment architecture. Calculators must remain
independently testable without an NLP implementation. No scientific decision
may exist only in production code.

### 5.3 SRM-12 — integration and explainable report

SRM-12 must preserve the approved observations, Evidence, absence provenance,
unresolved diagnostics, assessment results, and Findings through the
end-to-end pipeline. The report must render the approved trace so that a user
can resolve an assessment to the requirement source.

The CLI remains orchestration-only. The reporter formats completed structured
results and performs no feature detection, scientific calculation, Finding
classification, or aggregation.

### 5.4 SRM-13 — bounded validation

SRM-13 must approve its reference annotations, methodology, evaluation
measures, and acceptance interpretation before experimental results are
interpreted. Its validation target is the approved bounded assessment and
reporting slice, including feature outcomes, source spans, characteristic
results, uncertainty, Findings, and explanation trace.

The **819 passed** result recorded in the SRM-02 audit is historical regression
verification of that audit state. It is not independent experimental
validation of the completed model. This approval introduces no evaluation
threshold and no new expected reference value.

## 6. Approved but deferred detector extensions

Exact R3 and exact F1-A/M-A retain their existing authoritative status:

```text
RESEARCHER_APPROVED / NOT_IMPLEMENTED / RULE_ID_NOT_ALLOCATED
```

This decision does not revoke, weaken, reinterpret, or supersede their
scientific contracts. It also does not allocate a Rule ID, Evidence ID,
diagnostic ID, type, or field for either rule.

Their implementation is not a prerequisite for the first complete-model
milestone:

- exact R3 creates a bounded relationship record that the current
  characteristic calculators do not consume; and
- exact F1-A adds approved recognition depth to the existing quantitative
  family and existing Verifiability formula, but does not add a missing
  characteristic, calculation, state, Finding kind, or reporting layer.

Unimplemented F1-A must not be presented as supported. Its known exact
coverage boundary must be disclosed. If a future milestone explicitly selects
its two exact envelopes as supported inputs, that future selection may make
implementation necessary for that declared scope; approval status alone does
not make it a prerequisite here.

SRM-03 through SRM-08 remain bounded detector-extension streams. Their open
issue state does not make them unconditional blockers. A detector rule becomes
a first-model dependency only through an explicit later decision selecting it
into the approved first-complete-model slice.

## 7. Excluded work

This approval introduces no:

- new comparator grammar;
- generalized frequency recognition;
- new metric or context grammar;
- generic range recognition;
- vocabulary expansion;
- numeric formula, weight, coefficient, threshold, or rounding rule;
- requirement-type inference;
- confirmed-defect conversion;
- scalar overall requirement or file quality score;
- product-quality prediction;
- risk or defect probability;
- corrective-action model;
- lifecycle reassessment;
- web UI, REST API, or database; or
- production implementation of any kind.

The broader version, local risk, and corrective-action proposals in
[`srm-02-individual-requirement-model.md`](srm-02-individual-requirement-model.md)
remain historical research/planning context. They are not prerequisites for
this approved minimum complete-model milestone.

## 8. Approved milestone dependency path

The critical path is:

```text
SRM-02 scope approval
→ SRM-10 minimum scientific trace/explanation contract
→ SRM-11 implementation
→ SRM-12 end-to-end integration and explainable reporting
→ SRM-13 bounded validation
```

Dependency interpretation:

| Issue stream | First complete-model role |
|---|---|
| SRM-02 | This decision closes the minimum-scope approval gate once recorded and accepted through the repository workflow. |
| SRM-09 | Not a prerequisite while the retained `RQD-023` simplification remains in force. |
| SRM-10 | Owns the detailed structured-trace, explanation, bounded-non-claim, and reference-case science. |
| SRM-11 | Implements the SRM-10-approved contract without changing detector or calculator science. |
| SRM-12 | Integrates the preserved trace and produces the source-resolvable explainable report. |
| SRM-13 | Owns bounded experimental methodology, independently reviewed references, measures, interpretation, and reproducibility. |
| SRM-03–08 | Extension streams; not automatic predecessors of SRM-10–13. |

Future approval of another detector does not reopen this milestone. Reopening
requires a separate explicit decision that selects the new detector into the
first-complete-model slice or changes the accepted milestone claim.

## 9. Ready-to-paste SRM-00 issue #68 amendment

The following amendment is ready to paste into
[SRM-00 #68](https://github.com/rKiselyk/requirements-quality-assessment/issues/68).
It changes only the conflicting completion criterion and adds the minimum
dependency clarification. All other useful completion criteria should remain
unchanged.

### Replace this completion criterion

```text
- All approved detection and assessment rules are implemented.
```

### With this completion criterion

```text
- All scientific, assessment, representation, integration, explanation, and
  validation contracts selected for the explicitly approved first complete
  single-requirement slice are implemented. Approved detector rules whose
  sole purpose is to expand bounded linguistic coverage are not milestone
  prerequisites unless explicitly selected into that slice. Known unsupported
  coverage and approved-but-unimplemented rules are disclosed.
```

### Add this minimum dependency clarification

```text
SRM-03 through SRM-08 are bounded detector-extension streams, not
unconditional prerequisites for milestone completion merely because their
issues remain open. The approved critical path is SRM-02 scope approval →
SRM-10 minimum trace/explanation contract → SRM-11 implementation → SRM-12
end-to-end integration and explainable reporting → SRM-13 bounded validation.
SRM-09 type classification is not a prerequisite while the approved RQD-023
applicability simplification remains in force.
```

Preserve the remaining SRM-00 criteria, including:

- explanation through source Evidence;
- reference and regression tests;
- documented experimental validation; and
- traceability to the dissertation model.

This proposed text does not close an issue, modify the milestone, or alter any
other GitHub content automatically.

## 10. Approval effect and guardrails

This approval records milestone scope; it does not declare the milestone
complete. The remaining blockers are SRM-10, SRM-11, SRM-12, and SRM-13 in the
approved order.

The decision has the following invariants:

- no additional linguistic scope is introduced;
- no R3 or F1-A implementation is authorized or performed;
- no formula, Rule ID, Evidence ID, detector behavior, calculator behavior, or
  aggregation behavior changes;
- historical research and audit documents remain unchanged;
- SRM-10 through SRM-13 retain their assigned responsibilities;
- SRM-09 and SRM-03–08 are not accidental blockers; and
- the completion criterion cannot be reopened merely by approving another
  future detector.

Any later expansion requires a separate researcher decision and must preserve
the same scientific approval, implementation, evidence, uncertainty, and
validation boundaries.
