# SRM-02 — Minimum Complete Single-Requirement Model Audit

**Audit basis:** repository state after merged PR #102, 2026-09-23  
**Scope:** research and planning only; no production, test, model-spec, Git, or
GitHub change is authorized by this document  
**Conclusion:** the first complete model does **not** require broader linguistic
coverage. The existing bounded C/V/U model is scientifically and
computationally sufficient at its declared depth. The remaining milestone work
is to close the user-facing assessment contract: preserve a structured trace
from every characteristic result to its contributing feature outcomes and
source Evidence, render that trace and the bounded-coverage limitations, make
an explicit first-model Finding decision, and validate the resulting
end-to-end claim. Exact R3 and F1-A are approved extensions, but approval alone
does not make them prerequisites.

This audit supersedes neither [`model-spec.md`](model-spec.md) nor any GitHub
issue. It does not change the broader inventory in
[`srm-02-individual-requirement-model.md`](srm-02-individual-requirement-model.md).
Where that older inventory proposes versioned reassessment, local risk, and
corrective-action work, those proposals are not prerequisites for the minimum
complete assessment defined here.

Audited planning sources were GitHub milestone #1 (currently titled `Full
Single Requirement Model v1.0`, with 13 open and 1 closed issue at audit time),
[SRM-00 #68](https://github.com/rKiselyk/requirements-quality-assessment/issues/68),
[SRM-02 #70](https://github.com/rKiselyk/requirements-quality-assessment/issues/70),
and SRM-03 through SRM-13 (#71–#81). Repository sources included the
authoritative model specification, current domain/extraction/calculation/
assessment/reporting code and tests, SRM-03–05 research and acceptance records,
and the supplied dissertation excerpts in `docs/reference/`, especially §§2.1,
2.3, 3.1, 3.2, and 3.3. Sections 4.1–4.3 were checked to prevent product,
lifecycle, risk, and corrective-action concepts from being imported into the
minimum local assessment.

## 1. Target user-facing result

The minimum complete result for one supported Ukrainian software requirement
is an honest, deterministic assessment of the approved multidimensional
profile:

```text
Requirement identity and unchanged source text
→ bounded feature observations and processing status
→ independent Completeness, Verifiability, and Unambiguity assessments
→ RequirementQualityProfile(C, V, U)
→ supported Findings
→ human-readable explanation with resolvable source Evidence
```

The report must let a user answer all of the following without inspecting
Python objects or source code:

1. What requirement was assessed?
2. Was each characteristic `COMPUTED`, `UNKNOWN`, or `NOT_APPLICABLE`?
3. If computed, what exact value and assessment Rule ID produced it?
4. Which feature-family outcomes contributed to that value or tier?
5. Which exact source spans support positive observations?
6. Which required observation was absent after completed processing, without
   fabricating Evidence for that absence?
7. Which unresolved detector input withheld or could have changed a result?
8. Which Findings are mere `SIGNAL`s and which, if any, are approved
   `QUALITY_PROBLEM`s?
9. What does the bounded implementation not claim to detect?

The result remains `A_i = (C_i, V_i, U_i)`. It is not a scalar requirement
score, a product-quality prediction, a risk score, or a corrective-action
recommendation. The existing specification-level profile may remain available,
but it is adjacent functionality and is not necessary to assess one
requirement.

The phrase **complete model** therefore means complete scientific-to-user
traceability for the approved bounded C/V/U slice. It does not mean exhaustive
recognition of every Ukrainian formulation.

## 2. Current end-to-end capabilities

The production pipeline is already executable:

```text
UTF-8 text file
→ RequirementReader
→ BaselineFeatureExtractor
→ RequirementExtractionResult
→ CompletenessCalculator / VerifiabilityCalculator / UnambiguityCalculator
→ RequirementQualityAssessor
→ RequirementQualityProfile
→ SpecificationQualityAggregator
→ ConsoleReporter
```

Current capabilities established by source inspection and the existing suite:

- `RequirementReader` preserves trimmed text, punctuation, source line, input
  order, and generated IDs.
- The pinned spaCy adapter stays behind a parser-neutral boundary and preserves
  exact Unicode code-point offsets or reports parser/annotation failure.
- Six typed feature families preserve repeated observations, diagnostics, and
  accepted Evidence.
- `RequirementExtractionResult` rejects out-of-range or non-round-tripping
  spans, duplicate Evidence IDs, dangling references, and cross-family
  references.
- Implemented bounded detector Rule IDs are:
  `COND-UK-001`, `COND-UK-002`, `RESULT-UK-001`, `RESULT-UK-002`,
  `ACCEPT-QUANT-001`, `ACCEPT-UK-001`, `QUANT-001`, `QUANT-UK-001`,
  `QUANT-METRIC-001`, `QUANT-CONTEXT-001`, `VERIFY-UK-001`, and
  `UK-VAGUE-001`.
- `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` implement the
  approved exact `Fraction` calculations and characteristic-specific
  uncertainty propagation.
- `FIND-U-VAGUE-001` creates one evidence-backed Unambiguity `SIGNAL` per
  accepted vague-term occurrence. No production rule creates a
  `QUALITY_PROBLEM`.
- `RequirementQualityAssessor` assembles, but does not reinterpret, the three
  independent assessments.
- `ConsoleReporter` shows requirement ID and text, characteristic state/value,
  assessment Rule ID, Finding fields, and explanation. It does not calculate
  or aggregate.
- `AGG-MVP-001` and the specification profile correctly preserve
  `UNKNOWN`/`NOT_APPLICABLE` counts and exact means. This is already sufficient
  adjacent functionality, not a missing single-requirement component.
- The complete existing test suite passes: **819 passed in 100.81 seconds** on
  this audit environment.

The current CLI nevertheless drops the `RequirementExtractionResult` after
assessment and passes only `(Requirement, RequirementQualityProfile)` to the
reporter. Consequently, a displayed Finding Evidence ID cannot be resolved in
the console, positive C/V contributions have no displayed Evidence references,
and the user cannot inspect accepted feature observations or detector
diagnostics except where calculator prose happens to summarize them. The
scientific trace exists internally, but the user-facing chain is incomplete.

## 3. Scientific-model completeness matrix

Classification:

- **A — REQUIRED FOR FIRST COMPLETE MODEL:** missing science,
  representation, integration, explanation, or validation without which the
  bounded result cannot be claimed honestly.
- **B — ALREADY SUFFICIENT AT MVP DEPTH:** current bounded behavior is enough
  for the first complete model.
- **C — APPROVED FUTURE EXPANSION:** approved science that increases detection
  depth but is not necessary for the first complete model.
- **D — DEFERRED RESEARCH:** unapproved or out-of-scope work that must not be
  inferred into the milestone.

| Component | Scientific source | Current approved contract | Current implementation / Rule IDs | Evidence and uncertainty behavior | Minimum remaining work and classification |
|---|---|---|---|---|---|
| Unit of assessment and input | Dissertation §2.1 ¶¶2–6; model-spec §§1–2, 6; `RQD-018` | One non-empty trimmed UTF-8 line is one `Requirement`; Ukrainian is the supported language-dependent profile; punctuation, line, and order are preserved | `RequirementReader`, `Requirement`; implemented | Source text is the canonical coordinate system; malformed file and UTF-8 failures are explicit | None for the first model. One-line input is sufficient even if linguistic sentence validation remains absent. **B** |
| Parser-neutral annotation | Dissertation §3.1; model-spec §7.15 | spaCy 3.8.16 / `uk_core_news_sm` 3.8.0 is a replaceable engineering backend, not scientific authority | `SpaCyRequirementParser`; implemented | Parser failure or incomplete annotation propagates to detector diagnostics; no spaCy object escapes | None beyond documenting the pinned-backend limitation. **B** |
| Feature/Evidence boundary | Dissertation §2.3 metric passport and provenance rules; §3.1 structured findings; model-spec §§7.1–7.7 | Six typed outcomes plus immutable accepted Evidence; detection is separate from applicability and assessment | `RequirementFeatures`, `FeatureDetectionOutcome`, `RequirementExtractionResult`; implemented | Exact source spans, stable IDs, repeated occurrences, separate diagnostics, strict reference validation | Sufficient internally. The report still needs access to this registry. Internal contract **B**; user-facing preservation is covered by the **A** trace/report rows below. |
| Condition/context | §2.1 Table 2.1 (Completeness); model-spec §§7.14.3, 7.14.16 | Bounded leading/postposed condition subsets only | `COND-UK-001`, `COND-UK-002`; implemented and SRM-04-audited | Accepted exact spans; unsupported candidates may be `UNRESOLVED`; no absence Finding | Current bounded grammar is sufficient. Further attachment and grammar are detection-depth expansion. **B** |
| Expected result/reaction | §2.1 Table 2.1; model-spec §§7.14.4, 7.14.16 | Simple normative-modal and exact binary coordinated-result subsets | `RESULT-UK-001`, `RESULT-UK-002`; implemented and SRM-04-audited | Exact source Evidence; incomplete/ambiguous candidates remain diagnostics; two coordinated observations do not imply non-singularity | Current bounded grammar is sufficient. **B** |
| Acceptance criterion | §2.1 Table 2.1; §2.3 Verifiability discussion; model-spec §§7.14.5, 7.14.16 | Quantitative judgeable composition plus exact conditioned guillemet-output slice | `ACCEPT-QUANT-001`, `ACCEPT-UK-001`; implemented and SRM-04-audited | Evidence from independent rules is retained and deterministically merged; blocked dependencies remain unresolved | Current bounded grammar is sufficient. Broader nonnumeric criteria are future research. **B** |
| Quantitative scalar, metric, and context observations | §2.1 Verifiability; §2.3 ¶¶17–21 and Tables 2.7–2.8; model-spec §7.14.6 | Conservative partial scalar observations plus exact metric and C0 context links | `QUANT-001`, `QUANT-UK-001`, `QUANT-METRIC-001`, `QUANT-CONTEXT-001`; implemented and accepted | Partial components and unresolved roles are preserved; no unit conversion or invented inclusivity | Sufficient for a bounded first model. **B** |
| Exact R3 relationship | Same quantitative sources; model-spec §7.14.6.9 | Exact 160-code-point relationship; separate dedicated record; no calculator, Finding, report, or aggregate consumer | `RESEARCHER_APPROVED / NOT_IMPLEMENTED / RULE_ID_NOT_ALLOCATED` | Would add two Evidence items and a non-consumed relationship record; preserves scalar uncertainty | It cannot change the current C/V/U result by contract. It is not a completeness blocker. **C** |
| Exact F1-A/M-A frequency observation | Same quantitative sources; model-spec §§7.14.6.10 and 9 | Exact recognition for two complete-input envelopes as an ordinary quantitative observation consumed by existing `CALC-V-MVP-001` | `RESEARCHER_APPROVED / NOT_IMPLEMENTED / RULE_ID_NOT_ALLOCATED` | Exact metric/anchor Evidence; no acceptance Finding; can change standalone exact-case V from `0` to `1/2` | This increases supported linguistic coverage but introduces no new characteristic, formula, state, Finding semantics, or reporting structure. Defer it only if the report explicitly discloses bounded coverage and never presents `NOT_DETECTED` as universal absence. **C**, not automatically **A**. |
| Explicit verification method | §2.1 Table 2.1; §2.3 ¶¶17–21; model-spec §7.14.7 | Three narrow explicit-method constructions | `VERIFY-UK-001`; implemented | Exact Evidence or unresolved candidate; a named method is only lower-tier evidence | Current bounded rule is sufficient. **B** |
| Vague-term signal | §2.1 ¶49 and Table 2.3; requirements-smell discussion; model-spec §§7.8, 7.14.8, 10 | Exact `uk_vague_terms_v1` seed matching; signal, not confirmed ambiguity | `UK-VAGUE-001`; implemented | One exact Evidence occurrence per signal; complete no-match or explicit unresolved processing | Seed coverage is sufficient for the first bounded model. Vocabulary/syntax expansion is not required. **B** |
| Completeness assessment | §2.1 Table 2.1 and Table 2.3; model-spec §8 | Mandatory MVP condition/result/acceptance ratio; values `{0,1/3,2/3,1}` | `CALC-C-MVP-001`; implemented | Any required incomplete family yields `UNKNOWN`; absence contributes zero without fake Evidence or Finding | Formula, state, and explanation are sufficient. Structured contributor-to-Evidence trace is still missing from the user result. Calculation **B**; trace **A**. |
| Verifiability assessment | §2.1 Table 2.1; §2.3; model-spec §9 | Acceptance → `1`; else quantitative/method → `1/2`; else completed absence → `0`; material-dependency uncertainty | `CALC-V-MVP-001`; implemented | Unresolved input withholds only if it can change the tier; no absence Finding | Formula is sufficient. The report must disclose bounded detector coverage and selected evidence path. Calculation **B**; trace/limitation **A**. |
| Unambiguity assessment | §2.1 ¶49 and Table 2.3; model-spec §10 | No supported signal → `1`; one or more → `1/2`; `0` reserved for future confirmed ambiguity | `CALC-U-MVP-001`, `FIND-U-VAGUE-001`; implemented | Accepted signals compute `1/2` even with additional unresolved candidates; no signal plus incomplete scan yields `UNKNOWN` | Automated scale is sufficient if the report states that `1` means no supported signal, not proven semantic uniqueness. Confirmed ambiguity is not needed unless explicitly selected. **B** with one **A** scope confirmation. |
| Applicability and unavailable states | §2.3 ¶¶130–133; model-spec §§7.4, 7.16.3, 14; `RQD-023` | No type inference; C criteria and V characteristic use explicit MVP applicability simplifications; U signal is not an applicability criterion | Domain enums and calculator propagation implemented | `UNKNOWN`, `NOT_APPLICABLE`, detector `UNRESOLVED`, and completed absence remain distinct | Sufficient if the first model retains the approved simplification. Full type taxonomy is not inherently required. **B**, conditional on explicit milestone retention. |
| Requirement quality profile | §2.1 multidimensional artifact quality; model-spec §§1, 11 | Exactly three independent assessments; no scalar | `RequirementQualityProfile`, `RequirementQualityAssessor`; implemented | Each assessment retains state, value, Rule ID, Findings, and prose explanation | Profile shape and orchestration are sufficient. **B** |
| Finding semantics | §2.1 Table 2.2 and ¶49; §2.3 confirmed-indicator distinction; §3.1 structured findings; model-spec §§7.10, 7.16.5, 15 | `SIGNAL` and `QUALITY_PROBLEM` are distinct; only vague-term signal conversion is allocated; all problem conversions remain open | `Finding` contract and `FIND-U-VAGUE-001` implemented; no production `QUALITY_PROBLEM` | Signals require Evidence; future absence problems may use empty refs only with approved criterion/rule provenance; unresolved input cannot create a problem | First-model acceptance must explicitly choose either signal-only Findings or a separately approved minimum problem set. The minimum path is signal-only with no defect claim. The decision is **A**; new problem rules are **D** until approved. |
| Structured assessment trace | §2.3 reproducible metric/indicator contract; §3.1 provenance; §3.3 ¶¶33 and 78; model-spec §15 | Every numeric assessment must trace to its CALC rule, detector outcomes/observations, Evidence where applicable, and requirement | Internal objects collectively contain the data, but `CharacteristicAssessment` has no structured contribution/path references; calculators emit prose only | Positive Evidence exists; completed absence has no span; diagnostics explain withholding | Approve and implement a minimal structured trace for contribution, absence, and unresolved-path provenance, without changing any formula. **A** |
| Explainable report | §3.3 requires source-linked explanations; model-spec §§15 and 19; SRM-12 | Reporter formats completed results and must not calculate | `ConsoleReporter` implemented, but receives no extraction result; Finding refs are unresolved in output; C/V supporting spans are not shown | Literal states and Finding kinds are visible, but exact Evidence text/offsets and detector coverage limits are not | Carry the trace/Evidence registry through integration and render resolvable spans, absence provenance, uncertainty reasons, and bounded-coverage limits. **A** |
| End-to-end integration | Model-spec §5; required architecture; SRM-12 | Preserve extraction → calculation → profile → Finding → report separation | CLI is orchestration-only and works for a one-line file | Extraction is currently discarded before reporting | Integrate the approved trace/report contract without moving science into CLI or reporter. **A** |
| Scientific/reference validation | §2.3 ¶132; §3.1 ¶124; §3.3 reproducibility; model-spec `RQD-017`; SRM-13 | Binding MVP cases and deterministic tests exist; experimental claims require independently reviewed data and predeclared measures | 819 automated tests pass; detector acceptance audits exist; no independent end-to-end reference corpus/annotation study for the milestone claim | Tests verify implementation conformance, not empirical coverage or independent annotation agreement | Validate the bounded model and its explanation trace. Do not make detector expansion a prerequisite for validation. **A** |
| Specification aggregation | §2.1 property-level mean; model-spec §§12–14 | Independent exact means with observability counts | `AGG-MVP-001`; implemented | Unknown and not-applicable values are excluded and counted | Already sufficient but not required for one-requirement completeness. **B / adjacent** |
| Scalar score, product quality, risk, action, lifecycle reassessment | Dissertation §§3.3, 4.1–4.3 concern broader stages/product models; model-spec §§2, 17 and `RQD-013/014/019` | Explicitly absent from MVP; no approved local formula/contract makes them part of `A_i` | Not implemented | Inputs, calibration, authority, and uncertainty rules are absent | Do not add them to the first complete model. **D** |

### Characteristic-scope finding

Dissertation §2.1 enumerates nine individual-requirement properties:
necessity, relevance, unambiguity, completeness, singularity, feasibility,
verifiability, correctness, and presentation-rule conformance. The supplied
sources also explain why necessity, relevance, feasibility, and correctness
cannot be established reliably from text alone, while singularity and
presentation conformance need operational rules or an external rule set.

The authoritative implementation model has already selected the executable
per-requirement result `A_i = (C_i, V_i, U_i)`. Therefore the six other
properties are not silently missing fields from the current profile. They are
theoretical or future context-dependent properties. Making them first-model
requirements would expand the input contract and require new science; it is
not a consequence of the word “complete.” The milestone must say that its
first complete result is the approved bounded C/V/U profile, or explicitly
reopen this decision.

## 4. Essential missing components

### 4.1 Explicit minimum-slice acceptance contract

The milestone needs an approved statement that completeness is judged at the
model/integration level, not by exhaustively implementing every approved or
future detector. It must identify:

- C/V/U as the first complete profile;
- the retained no-type-inference applicability simplification;
- bounded Ukrainian detector coverage as a disclosed limitation;
- no scalar, product-quality, risk, corrective-action, or lifecycle result;
- whether signal-only Findings are acceptable for this milestone; and
- which exact reference cases define the accepted slice.

Without this statement, “full” can be read as either model completeness or
unbounded linguistic coverage, and SRM-03–08 remain accidental moving gates.

### 4.2 Structured characteristic-to-source trace

The implementation currently proves traceability only by joining several
objects mentally or in tests. The minimum trace must preserve, for each
characteristic result:

- assessment Rule ID and state/value;
- contributing feature family or selected Verifiability path;
- the accepted observation references and Evidence IDs used by the result;
- completed-absence provenance for criteria/evidence paths that contribute an
  absence result, without invented spans;
- unresolved detector family and diagnostic reason when a value is withheld;
- Finding IDs linked to the same requirement and Evidence registry; and
- explicit scope language where a maximum-looking value is only absence of a
  supported signal.

This is a representation and explainability contract, not a new metric,
formula, weight, threshold, detector, or `QUALITY_PROBLEM` rule.

### 4.3 Resolvable evidence in the report

The pipeline must retain the extraction result or an approved equivalent trace
through reporting. For every displayed Evidence reference, the user must see
at least its exact source text, `[start,end)` offsets, feature family, and
detector Rule ID. The reporter may format these completed domain values but
must not rediscover which evidence contributed or implement characteristic
logic.

Completed absence must be reported as completed processing plus no accepted
observation under the named rule/family. It must not receive a fabricated
source span. An unresolved candidate must remain visibly unresolved.

### 4.4 First-model Finding disposition

The current assessment can be complete as a profile without claiming to
diagnose confirmed defects. The narrowest scientifically safe decision is:

- keep `FIND-U-VAGUE-001` as a `SIGNAL`;
- keep low C/V values and absence reasons in the assessment trace;
- do not create `QUALITY_PROBLEM` findings;
- keep `U_i = 0` unreachable; and
- state this limitation in the report and release claim.

This disposition requires explicit researcher/milestone acceptance because
SRM-10 currently asks for full `QUALITY_PROBLEM` and confirmed-ambiguity rules.
If the researcher instead requires confirmed problems in the first model,
`RQD-016` and the confirmation procedure become scientific blockers before
SRM-11. This audit does not propose those rules.

### 4.5 Bounded end-to-end validation

SRM-13 must validate the model actually claimed, not postpone validation until
all possible detector grammars exist. The minimum validation package needs:

- a documented Ukrainian reference set spanning each implemented detector
  rule, each C/V/U state/value class, mixed accepted-plus-unresolved outcomes,
  signal Findings, exact Evidence spans, and important negative cases;
- independent review of reference annotations;
- predeclared evaluation measures and acceptance interpretation;
- comparison of feature outcomes, spans, assessments, Findings, and report
  trace against the references;
- determinism and reproducibility evidence; and
- explicit error and supported-coverage limitations.

No evaluation threshold or expected value is invented here. Those decisions
belong to the approved SRM-13 methodology.

## 5. Existing MVP components sufficient at bounded detection depth

The following work should not be reopened merely to complete the first model:

- input identity, UTF-8 handling, and source preservation;
- parser-neutral annotations and degraded-operation behavior;
- six-family `RequirementFeatures` and `RequirementExtractionResult`;
- exact Evidence offsets, reference integrity, and repeated observations;
- the implemented bounded structural rules, including the accepted SRM-04
  first slice;
- the implemented scalar, metric-link, and C0 quantitative rules;
- `VERIFY-UK-001` and `uk_vague_terms_v1`;
- `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001`;
- exact `Fraction` representation and no-rounding presentation;
- current detector-to-assessment uncertainty propagation;
- `RequirementQualityProfile(C,V,U)` and no scalar score;
- the signal/confirmed-problem distinction and implemented vague signal;
- `AGG-MVP-001`, although aggregation is not required for one requirement;
  and
- the architecture boundaries among extraction, calculators, assessor, CLI,
  and reporter.

Bounded sufficiency does not convert a supported no-match into proof that no
other linguistic expression could carry the same meaning. The final report
and release documentation must make that limitation explicit.

## 6. Approved but deferrable extensions

### Exact R3

R3 is scientifically approved but has no allocated Rule ID, production type,
or implementation. Its contract explicitly says that calculators ignore the
future relationship and that it changes no characteristic, Finding, report
row, or aggregate. It is therefore pure detection/representation depth for the
current assessment model and is not a first-complete-model prerequisite.

### Exact F1-A

F1-A is scientifically approved and, if implemented, is consumed by the
unchanged Verifiability formula. It can change the 90-code-point exact input
from `V_i = 0` to `V_i = 1/2`; the 178-code-point input remains `1/2` because
another lower-tier scalar is already present.

That material output effect does not add a missing model component. It adds
one exact recognized formulation to an already complete feature family and
formula. F1-A may therefore be deferred if all of these conditions hold:

1. the first-model supported-depth contract does not promise this envelope;
2. the report explains that completed detection means completed execution of
   the implemented bounded rules, not exhaustive semantic absence;
3. validation reports the known coverage limit; and
4. the milestone criterion no longer equates every approved detector with a
   completion prerequisite.

If the milestone instead declares the two F1-A envelopes supported inputs,
F1-A becomes a blocker for that declared coverage. The deciding fact is the
accepted support claim, not approval status alone.

### Other SRM-03–08 work

The implemented SRM-03/04 bounded structural slice and implemented SRM-05C/D
quantitative slices are already sufficient. Remaining structural,
quantitative, and linguistic work is extension work:

- approved exact slices may be scheduled later as **C**;
- unapproved generalized grammar, vocabularies, ranges, written numbers,
  count roles, nested relations, attachment, or ambiguity detection remain
  **D** until separately approved; and
- none becomes a prerequisite merely because the parent issue remains open.

Confirmed material ambiguity, `QUALITY_PROBLEM` conversion, type taxonomy,
and the six additional dissertation properties are not “approved detector
backlog.” They are unresolved scientific choices. They remain deferred unless
the researcher selects them for the first-model claim.

## 7. Actual blocking dependencies

| Issue | Dependency for the first complete model | Blocking status |
|---|---|---|
| [SRM-02 #70](https://github.com/rKiselyk/requirements-quality-assessment/issues/70) | Establish this minimum scope, classifications, and researcher decisions | **Blocking now**: the milestone claim cannot be evaluated consistently until the minimum slice is accepted |
| [SRM-09 #77](https://github.com/rKiselyk/requirements-quality-assessment/issues/77) | Decide whether the existing `RQD-023` simplification remains the first-model applicability contract | **Conditional**: non-blocking if the simplification is explicitly retained; blocking only if type-aware applicability is selected |
| [SRM-10 #78](https://github.com/rKiselyk/requirements-quality-assessment/issues/78) | Approve the minimum structured assessment trace, bounded-result wording, Finding disposition, and binding explanation cases | **Blocking** for scientific/explanation completeness; it need not add formulas or problem rules if signal-only scope is approved |
| [SRM-11 #79](https://github.com/rKiselyk/requirements-quality-assessment/issues/79) | Implement only the SRM-10-approved trace/assessor changes, if any | **Blocking after SRM-10**; existing calculator formulas remain unchanged |
| [SRM-12 #80](https://github.com/rKiselyk/requirements-quality-assessment/issues/80) | Preserve extraction/trace data through the CLI and render source-resolvable Evidence, absence, uncertainty, Findings, and limits | **Blocking after SRM-11** for the promised user-facing result |
| [SRM-13 #81](https://github.com/rKiselyk/requirements-quality-assessment/issues/81) | Predeclare and execute independent bounded-model validation | **Blocking after integration** for milestone validation/release claims |
| SRM-03–08 | Add structural, quantitative, and ambiguity detection depth | **Not automatic blockers**. A rule blocks only if explicitly selected into the accepted first-model coverage. Exact R3/F1-A are not selected by this audit. |

The logical critical path is:

```text
SRM-02 scope approval
→ SRM-10 minimum trace/Finding/explanation contract
→ SRM-11 trace-preserving assessment implementation
→ SRM-12 evidence-resolving integration and report
→ SRM-13 bounded end-to-end validation
```

SRM-09 is a decision branch before SRM-10, not necessarily a taxonomy
implementation project. SRM-03–08 can proceed independently as later coverage
iterations.

## 8. Proposed minimal milestone path

1. **Accept the first-model claim.** Record that the milestone targets a
   complete, explainable C/V/U assessment at explicit bounded detector depth.
   Retain no scalar score and exclude product quality, risk, corrective action,
   and lifecycle reassessment.
2. **Retain or reject the MVP applicability simplification.** The minimal path
   retains it and closes SRM-09 for this milestone without introducing a type
   classifier or type matrix.
3. **Complete only the missing scientific output contract in SRM-10.** Approve
   contribution/absence/unresolved trace semantics, evidence presentation
   requirements, bounded-coverage wording, signal-only Finding scope, and
   binding explanation cases. Do not change C/V/U formulas.
4. **Implement trace preservation in SRM-11.** Calculators remain independent
   of NLP. Any new trace representation is domain data, derived alongside the
   assessment by approved rules. No scientific decision may live only in code.
5. **Integrate and report in SRM-12.** Retain the extraction result or approved
   equivalent through orchestration. Render exact Evidence text/offsets,
   feature and rule provenance, absence and unresolved reasons, and supported
   limits. The reporter remains formatting-only.
6. **Validate in SRM-13.** Freeze methodology and annotations before
   interpreting results. Validate the bounded slice and document its error
   modes. Existing unit/reference tests remain regression evidence but do not
   replace independent experimental validation.
7. **Close the milestone without forcing coverage work.** Leave exact R3,
   F1-A, broader SRM-03–08 grammar, confirmed ambiguity, problem conversion,
   and type-aware applicability in their correctly classified future streams
   unless the researcher explicitly adds one to the accepted slice.

This path changes no mathematical result. It completes the chain from approved
science to an evidence-resolvable user result.

## 9. Needed GitHub scope correction

SRM-00 currently requires:

> All approved detection and assessment rules are implemented.

That sentence conflicts with the agreed goal of completing the assessment
model before expanding detector coverage. It makes every approved detector,
including an exact non-consumed R3 representation and exact F1-A coverage,
an automatic milestone gate even when the characteristic model, uncertainty,
Findings, and user report are otherwise complete. It also creates an unstable
acceptance criterion: approving another bounded detector would reopen the
milestone.

Proposed narrow replacement for researcher review:

> All scientific, assessment, representation, integration, explanation, and
> validation contracts selected for the approved minimum complete
> single-requirement slice are implemented. Approved detector rules whose sole
> purpose is to expand bounded linguistic coverage are not milestone
> prerequisites unless explicitly selected into that slice; unimplemented
> approved rules and supported-coverage limitations are disclosed.

No other SRM-00 scope change is required by this audit. In particular, the
criteria for source Evidence, regression tests, experimental validation, and
dissertation traceability should remain.

For dependency clarity, SRM-00 should also treat SRM-03–08 as extension streams
rather than unconditional predecessors of SRM-10–13. This audit does not
modify the issue or milestone.

## 10. Questions requiring explicit researcher approval

1. Is the first complete model formally the bounded three-characteristic
   `RequirementQualityProfile(C,V,U)`, with the other six §2.1 properties
   outside this milestone unless separately operationalized?
2. May the existing `RQD-023` applicability simplification remain the complete
   first-model contract, allowing SRM-09 type taxonomy/classification to be
   deferred?
3. Is a signal-only first model acceptable: `FIND-U-VAGUE-001` remains a
   `SIGNAL`, `QUALITY_PROBLEM` production remains empty, and confirmed
   ambiguity / `U_i = 0` remains deferred?
4. What exact structured contribution/absence/unresolved fields must be
   preserved so every characteristic result can be traced to detector outcomes
   and Evidence without parsing prose?
5. Must the canonical report display every contributing Evidence span or only
   the evidence selected by the approved assessment trace? How should repeated
   observations be grouped without implying additional score weight?
6. Is the proposed SRM-00 acceptance-criterion replacement approved, including
   explicit deferral of exact R3 and F1-A from the first complete slice?
7. What annotation procedure, evaluation measures, and acceptance
   interpretation will govern SRM-13? These must be approved before results are
   interpreted; this audit proposes no thresholds.
8. Should the older broad SRM-02 roadmap proposals for versioned reassessment,
   local risk, and corrective actions be explicitly marked outside the
   minimum-complete milestone so they cannot become accidental SRM-12/13
   dependencies?

Until these decisions are recorded, the existing implementation remains a
valid and well-tested bounded MVP. It should not be described as an exhaustive
linguistic analyzer or as a confirmed-defect, risk, or corrective-action
system.
