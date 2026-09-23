# SRM-13 — Experimental Validation Protocol Proposal

**Decision status:** `PROPOSED_FOR_RESEARCHER_REVIEW`  
**Issue:** `#81 — SRM-13`  
**Scope:** independent validation of the completed bounded, single-requirement
Ukrainian `RequirementQualityProfile(C, V, U)` model approved by SRM-02.  
**Experiment status:** not started; this document defines the protocol only.

## 1. Decision requested

Approve a pre-registered protocol for constructing an independently annotated
evaluation corpus and comparing the frozen system under test with that
reference. Approval of this protocol would authorize the later experiment; it
would not approve a corpus, create reference annotations, establish expected
C/V/U values, set acceptance thresholds, or claim that independent review has
already occurred.

The protocol preserves the approved pipeline and scientific boundaries:

```text
UTF-8 Ukrainian requirement line
→ bounded six-family feature extraction
→ RequirementExtractionResult and exact Evidence
→ independent C, V, and U assessments
→ RequirementAssessmentTrace and SIGNAL Findings
→ bounded-coverage disclosures
```

It does not redesign a detector, calculation, applicability rule, trace rule,
Finding rule, or reporter. The experiment must validate the implementation
against the contracts in `docs/model-spec.md`; it must not use evaluation data
to redefine those contracts during the same experimental run.

## 2. Validation scope and non-claims

### 2.1 Unit of analysis

The evaluation unit is one non-empty, trimmed Ukrainian requirement line under
the MVP v0.1 input policy. One line remains one requirement even when it
contains multiple clauses or sentences. The corpus must preserve source text,
punctuation, Unicode code points, source provenance, source line identity, and
input order.

The assessed result is the multidimensional requirement-level profile:

```text
A_i = (C_i, V_i, U_i)
```

The three characteristics are evaluated and reported independently. They must
not be combined into a scalar score for validation or acceptance.

### 2.2 Claims that the experiment can test

Subject to the approved corpus and sampling frame, the experiment can test
these precise implementation claims:

1. For each approved feature family, the frozen implementation produces the
   observations, processing state, diagnostics, and accepted Evidence required
   by the bounded detector contracts.
2. Every accepted Evidence span is source-exact and linked to the correct
   requirement, feature family, observation, component, and Rule ID.
3. Completed absence, accepted observation, and unresolved processing remain
   distinct; a diagnostic candidate span is not converted into Evidence.
4. `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` produce the
   correct characteristic state and exact `Fraction` value from the approved
   feature outcomes, including the approved materiality rules for `UNKNOWN`.
5. The assessment trace uses the correct governing rule, decision code, input
   effect code, observation/diagnostic references, Finding references, and
   bounded-coverage profile.
6. Each supported vague-term occurrence produces exactly one correctly linked
   `FIND-U-VAGUE-001` `SIGNAL`, and no current output is presented as a
   `QUALITY_PROBLEM`.
7. Repeated execution of the frozen implementation in the frozen environment
   is deterministic for the evaluated inputs.
8. The observed performance and coverage limitations within the approved
   sampling frame can be described separately for supported bounded
   constructions and unsupported formulations.

### 2.3 Claims that the experiment cannot establish

The experiment cannot establish any of the following:

- exhaustive recognition of Ukrainian linguistic or semantic formulations;
- universal absence of a semantic feature from `NOT_DETECTED` or a completed
  empty outcome;
- unique interpretation from `U=1`, confirmed ambiguity from `U=1/2`, or a
  valid `U=0` rule;
- a confirmed defect, severity, confidence, risk, priority, corrective action,
  or `QUALITY_PROBLEM` from a C/V/U value or completed absence;
- validity of R3 or F1-A as runtime coverage while they remain unimplemented;
- a scalar requirement-quality score, whole-file quality score, or prediction
  of software-product quality;
- specification-level coverage, consistency, traceability, or the other six
  theoretical individual-requirement properties;
- population-wide accuracy outside the approved sampling frame, source
  domains, construction strata, and corpus composition; or
- construct validity of the broader theoretical concepts beyond the approved
  bounded operationalization.

## 3. Research questions

The later experimental report must answer the following questions separately.
It must not collapse them into one accuracy number.

| ID | Research question | Primary comparison unit |
| --- | --- | --- |
| `RQ-SRM13-1` | How accurately does the system identify approved observations in each of the six bounded feature families? | Reference observation versus system observation, per family |
| `RQ-SRM13-2` | How accurately does the system localize and link exact accepted Evidence? | Exact source span and graph link |
| `RQ-SRM13-3` | How accurately does the system distinguish completed processing, completed absence, accepted observations, incomplete processing, diagnostics, and downstream `UNKNOWN`? | Categorical processing/state result and diagnostic provenance |
| `RQ-SRM13-4` | How often does each C, V, and U assessment match the independently derived state and exact value under the approved rules? | Per-characteristic state and exact `Fraction` |
| `RQ-SRM13-5` | How faithfully does the trace explain the authoritative assessment and resolve to observations, diagnostics, Evidence, and Findings? | Decision/effect code and referential-integrity path |
| `RQ-SRM13-6` | How accurately and faithfully are supported vague-term `SIGNAL` Findings produced? | Exact Finding event and one-to-one occurrence provenance |
| `RQ-SRM13-7` | Which supported and unsupported construction strata account for observed errors and coverage limitations? | Pre-registered stratum and limitation category |
| `RQ-SRM13-8` | Is output reproducible under repeated execution of the frozen artifact and environment? | Canonical per-case record and run hash |

## 4. Evaluation-set separation

Three classes of cases have different purposes and must remain separate.

### 4.1 Approved binding reference cases

The five characteristic-layer cases in `docs/model-spec.md` §7.16.8 and the
seven trace cases in §7.17.8 are binding scientific conformance cases. They may
be run as a pre-experiment readiness check, but they are already known to the
model and implementation process. They are not independent observations and
must not be included in experimental performance measures.

### 4.2 Regression and acceptance-test cases

Existing test fixtures verify engineering behavior, invariants, previously
approved examples, and regressions. This includes cases in detector,
calculator, assessment-trace, reporter, CLI, and end-to-end acceptance tests.
Whether a fixture is copied from a binding case or is merely synthetic, it is
development-visible and must not be counted as independent evaluation data.

Regression results may be reported as a separate implementation-readiness
statement only. Their pass/fail counts must never be pooled with evaluation
metrics.

### 4.3 Independently annotated evaluation cases

Only the frozen, independently sourced and annotated holdout defined by this
protocol is the evaluation set. It must have no exact duplicate or
meaning-preserving near-duplicate of a binding case, test fixture, model-spec
example, detector example, documentation example, or annotation-training case.

The experimental report must publish three separate inventories:

```text
binding_reference_case_ids
development_and_regression_case_ids
independent_evaluation_case_ids
```

No case may contribute to more than one reported class. A detected overlap
must be resolved before unblinding by removing the evaluation candidate or by
classifying it as development-only; it must not be silently retained.

## 5. Corpus sampling and inclusion protocol

### 5.1 Sampling frame

Before collection, the researcher must approve and freeze:

- source domains and source types;
- access, licensing, confidentiality, and redistribution conditions;
- time window, organization/project boundaries, and sampling method;
- corpus size and per-stratum composition;
- the policy for naturally occurring versus researcher-authored cases;
- duplicate and near-duplicate criteria;
- the annotation-development/pilot/evaluation split; and
- whether any source is excluded because it was visible during development.

The sampling frame must be reported exactly. Convenience sampling may be used
only if approved and disclosed; it cannot support claims about a broader
population that was not sampled.

### 5.2 Inclusion rules

A candidate evaluation case is eligible only when all of these conditions are
met:

1. It is Ukrainian text intended or presented as a software requirement,
   constraint, acceptance statement, or explicit verification statement under
   the researcher-approved source taxonomy.
2. It can be represented as one non-empty UTF-8 line without rewriting its
   wording or punctuation.
3. Its original wording and provenance can be retained for audit, subject to
   the approved confidentiality policy.
4. It was not used to design, approve, implement, debug, or regression-test the
   model, and it is not a prohibited duplicate or near-duplicate.
5. Its inclusion stratum can be assigned without consulting the system output.
6. It can be annotated using the versioned codebook, including a coverage
   limitation record when its semantics exceed the bounded rules.

Exclusions and their reasons must be logged before system-output unblinding.
The protocol must not silently discard difficult, unsupported, or
`UNKNOWN`-producing cases after seeing their results.

### 5.3 Bounded Ukrainian construction strata

MVP v0.1 does not classify requirement types automatically. Therefore the
following are corpus-analysis strata, not new model types, applicability
rules, or score inputs:

| Stratum | In-scope bounded content to sample | Boundary to preserve |
| --- | --- | --- |
| Condition/context | Approved leading and bounded postposed condition/context constructions | Broader attachment and grammar remain unsupported |
| Expected result | Approved simple normative-modal result and bounded two-active-infinitive coordination | Broader result grammar and semantic role resolution remain unsupported |
| Acceptance criterion | Approved quantitative criterion and bounded exact-message construction | Broader nonnumeric acceptance grammar and sufficiency judgment remain unsupported |
| Quantitative constraint | Approved partial linked metric/comparator/value/unit/context forms | Complex grammar and unimplemented R3/F1-A runtime coverage remain unsupported |
| Verification method | Approved explicit governing-predicate, label, and declared-test constructions | Broader verification-method grammar and method sufficiency remain unsupported |
| Vague-term signal | Exact `uk_vague_terms_v1` occurrences under approved matching mechanics | Broader ambiguity vocabulary, context exceptions, and confirmation remain unsupported |
| Completed absence | Requirements for which relevant bounded rules complete with no accepted observation | Absence is bounded-rule absence, not universal semantic absence |
| Mixed and repeated observations | Multiple clauses, repeated observations, overlapping Evidence, and approved same-family/cross-family mixed states | Repetition must not add unapproved weight; one span may support multiple justified observations |
| Unresolved processing | Cases that exercise approved incomplete-processing and diagnostic behavior | Candidate spans remain non-Evidence; `UNKNOWN` is not zero |

The researcher must approve the final stratum definitions, source taxonomy,
and composition. If a functional/non-functional or other requirement-type
taxonomy is desired for descriptive analysis, it must be declared as
annotation-only metadata and must not alter the current `RQD-023`
applicability simplification or any expected C/V/U result.

### 5.4 Unsupported-coverage sample

The corpus must include a separately identified coverage-challenge stratum of
genuine Ukrainian requirements that are relevant to one or more semantic
feature families but fall outside an implemented bounded detector rule. Its
purpose is to characterize non-coverage, not to redefine the supported rule.

For these cases, annotators record both:

- whether an observation is expected under the exact approved bounded rule;
  and
- a separate `coverage_limitation` describing a semantically relevant
  formulation that the bounded rule does not claim to recognize.

An unsupported semantic candidate must not be inserted into the reference
`observations` expected from the bounded implementation. Conversely, labeling
it only as `NOT_DETECTED` without a limitation record would conceal the known
coverage boundary. Results for supported-contract cases and coverage-challenge
cases must be reported separately before any combined descriptive summary.

## 6. Independent annotation procedure

### 6.1 Roles and independence

The proposed process uses independent primary annotation followed by explicit
adjudication. The researcher must approve the number, qualifications, language
competence, domain competence, training, compensation/conflict policy, and
adjudicator role before annotation begins.

Primary annotators must:

- receive the frozen source text, provenance allowed by policy, annotation
  codebook, approved model rules, and annotation tool instructions;
- not receive the frozen system's output, test expectations, or another
  annotator's labels before submitting their own labels;
- annotate independently in a randomized case order identified by opaque case
  IDs; and
- declare prior exposure to any candidate case or development artifact.

Anyone who implemented or debugged the evaluated detector or rule may advise
on the codebook but must not be treated as an independent primary annotator for
that rule unless the researcher explicitly approves and discloses the
conflict.

### 6.2 Codebook preparation and pilot

Before evaluation annotation, create and version a codebook that restates only
the approved bounded contracts and gives annotation mechanics for offsets,
links, diagnostics, states, trace codes, Findings, and limitation tags. It must
not add synonyms, grammar, thresholds, or semantic assumptions.

A separate pilot/training set may be used to refine instructions and the
annotation tool. Pilot cases and their variants become development-visible and
are permanently excluded from evaluation. Codebook changes after the pilot
must create a new version and trigger re-annotation of any affected
evaluation labels before the reference is frozen.

### 6.3 Annotation passes

Each primary annotator completes the following passes without viewing system
output:

1. **Eligibility and metadata:** confirm inclusion, language, source metadata,
   and pre-registered corpus stratum.
2. **Coverage classification:** mark each relevant family as supported by an
   exact bounded rule, unsupported/coverage-challenge, or not implicated; give
   the applicable Rule ID or limitation code and rationale.
3. **Feature outcomes:** annotate processing status, every accepted observation,
   every exact Evidence span/link, quantitative components, and every approved
   diagnostic/candidate span where applicable.
4. **Assessment derivation:** apply the approved C/V/U rules to the annotated
   outcomes, recording state, exact rational value or `None`, governing Rule
   ID, and explanation. No subjective holistic quality rating is substituted
   for the approved calculation.
5. **Trace and Finding derivation:** record decision/effect codes, local
   observation/diagnostic references, Finding references, and one-to-one vague
   occurrence → `SIGNAL` provenance.
6. **Self-check:** validate offset round-trips, reference integrity, state/value
   invariants, allowed value sets, and the absence of fabricated Evidence.

To reduce propagation mistakes, the annotation tool should derive or validate
mechanically determined fields only after the human feature labels are saved.
Any such reference derivation/validation implementation must be independent
of the production implementation, reviewed, versioned, and tested against the
binding cases; it must not call production detectors or calculators to create
the reference.

### 6.4 Review and disagreement resolution

The annotation system must preserve each primary annotation unchanged. It
then computes disagreements by output type: coverage class, processing state,
observation identity, exact span/link, diagnostic, assessment state/value,
trace code/reference, and Finding.

Annotators may review each other's rationales only after both independent
submissions are locked. The adjudicator resolves disagreements by citing the
approved Rule ID and codebook version. The adjudicated reference must retain:

- both original annotations;
- the machine-generated disagreement record;
- the adjudicated value;
- adjudicator identity and timestamp;
- rationale and cited rule/section; and
- whether the resolution exposed a codebook defect, source defect, or genuine
  rule ambiguity.

If the approved model does not determine the answer, the case must not be
forced into a label. It is recorded as a protocol/model-specification issue and
handled under the researcher-approved exclusion or unresolved-case policy.
The policy must be frozen before unblinding, and all such cases must remain in
the corpus accounting.

### 6.5 Reference freeze and provenance

The reference release must have an immutable version and cryptographic hashes
for the corpus, codebook, raw annotations, adjudications, and final reference.
Every record must identify source provenance, corpus version, annotation-tool
version, codebook version, annotator/adjudicator pseudonymous IDs, timestamps,
and amendment history.

No annotation is final merely because annotators agree. Structural validation
must also confirm exact source round-trips and internal reference integrity.

## 7. Proposed reference schema

The storage format is a researcher decision. JSON Lines or another
machine-readable format is suitable only if it preserves the following logical
schema exactly. Names below define protocol fields, not proposed production
domain changes.

### 7.1 Dataset and case records

```text
ValidationDataset
  protocol_version
  corpus_version
  codebook_version
  annotation_schema_version
  sampling_frame_id
  source_inventory_hash
  case_ids[]

ValidationCase
  case_id
  source_record_id
  source_provenance
  source_hash
  language
  original_text
  normalized_input_text          # trimmed input only; no linguistic rewrite
  source_line_metadata
  sampling_strata[]
  evaluation_partition
  inclusion_decision
  exclusion_reason | null
  prior_exposure_declarations[]
  feature_outcomes[]
  evidence_registry[]
  characteristic_assessments[]
  characteristic_traces[]
  findings[]
  coverage_limitations[]
  annotation_provenance
```

`original_text` and `normalized_input_text` must make any reader trimming
explicit. All span offsets below are zero-based, end-exclusive Unicode
code-point offsets into `normalized_input_text`, matching the production
Evidence contract.

### 7.2 Feature outcomes, observations, Evidence, and diagnostics

```text
ReferenceFeatureOutcome
  feature_id                    # one of the six approved FeatureId values
  bounded_rule_ids[]
  coverage_class                # SUPPORTED_BOUNDED | COVERAGE_CHALLENGE |
                                # NOT_IMPLICATED
  processing_status             # COMPLETE | INCOMPLETE
  derived_detection_status      # DETECTED | NOT_DETECTED | UNRESOLVED
  observations[]
  diagnostics[]

ReferenceObservation
  annotation_observation_id     # reference-only stable ID
  feature_id
  observation_type              # simple | quantitative | vague_term
  evidence_refs[]
  quantitative_components | null
  vague_vocabulary_id | null
  vague_matched_literal | null
  annotator_rationale

ReferenceEvidence
  evidence_id
  requirement_case_id
  feature_id
  text
  start_offset
  end_offset
  rule_id

ReferenceDiagnostic
  annotation_diagnostic_id
  code
  explanation
  rule_id
  candidate_span | null         # text/start/end; explicitly not Evidence
```

For a quantitative observation, `quantitative_components` records the approved
`metric`, `comparator`, `value`, `unit`, and `context` components, including
component Evidence references, approved labels, decimal value, comparator
inclusivity, and `unresolved_components`. The top-level Evidence reference set
must equal the de-duplicated union of populated component references.

Every accepted reference Evidence entry must satisfy:

```text
normalized_input_text[start_offset:end_offset] == text
```

Evidence equality for evaluation uses feature family, exact offsets, text, and
Rule ID. Reference-only IDs are join keys and are not compared literally with
runtime-generated IDs.

### 7.3 C/V/U assessment and processing/`UNKNOWN`

```text
ReferenceCharacteristicAssessment
  characteristic_id             # COMPLETENESS | VERIFIABILITY | UNAMBIGUITY
  state                         # COMPUTED | NOT_APPLICABLE | UNKNOWN
  value_numerator | null
  value_denominator | null
  assessment_rule_id | null
  governing_rule_id
  finding_refs[]
  explanation
  derivation_provenance
```

The schema preserves these distinctions:

```text
DetectionProcessingStatus.INCOMPLETE
  != DetectionStatus.UNRESOLVED
  != CharacteristicAssessmentState.UNKNOWN
  != CriterionApplicability.UNKNOWN
  != NOT_APPLICABLE
  != numeric zero
```

The reference must use exact rational numerator/denominator pairs and the
approved value sets. No decimal conversion, tolerance, rounding, or inferred
value is permitted. Under current C/V/U rules, characteristic-level
`NOT_APPLICABLE` is representable but unreachable for a non-empty supported
requirement; annotators must not invent a rule to produce it.

### 7.4 Trace decisions

```text
ReferenceCharacteristicTrace
  characteristic_id
  governing_rule_id
  decision_code
  inputs[]
  finding_refs[]
  coverage_profile_id           # MVP-V0.1-BOUNDED-CVU-001

ReferenceFeatureInputTrace
  feature_id
  applicability | null
  observation_refs[]            # converted to local tuple indexes for comparison
  diagnostic_refs[]             # converted to local tuple indexes for comparison
  effect_code
```

Decision codes are restricted to the approved `TraceDecisionCode` set, and
effect codes to the approved `TraceEffectCode` set. C has exactly the three
condition/result/acceptance inputs, V the three
acceptance/quantitative/method inputs, and U the vague-term input. Observation
and diagnostic ordering must be frozen so the reference can be compared with
the production trace's local zero-based tuple indexes.

### 7.5 `SIGNAL` Findings

```text
ReferenceFinding
  finding_id
  requirement_case_id
  characteristic_id             # UNAMBIGUITY
  kind                          # SIGNAL
  code                          # VAGUE_TERM_SIGNAL
  rule_id                       # FIND-U-VAGUE-001
  criterion_id                  # null
  evidence_refs[]
  source_occurrence_ref
  explanation
```

Each supported vague occurrence maps to exactly one Finding in source order.
The reference schema must reject `QUALITY_PROBLEM`, severity, confidence,
risk, priority, or corrective-action annotations in the current scope.

### 7.6 Coverage limitations

```text
CoverageLimitation
  limitation_id
  feature_family | null
  limitation_category
  source_span | null
  semantic_description
  relevant_approved_boundary
  expected_bounded_behavior
  researcher_disposition
```

The initial limitation vocabulary may contain only categories directly
traceable to approved non-claims, such as broader grammar/attachment,
unimplemented R3/F1-A, vocabulary/context beyond `uk_vague_terms_v1`,
confirmed ambiguity, requirement-type/applicability inference, cross-
requirement properties, or product-quality claims. The final controlled
vocabulary requires researcher approval; annotators must not create new
quality criteria through free-form limitation tags.

## 8. Measures by output type

All measures must be pre-registered before the frozen system output is opened.
Counts and denominators accompany every rate. Results are reported per feature
family, per characteristic, per approved corpus stratum, and separately for
supported-contract versus coverage-challenge cases wherever the denominator is
non-empty.

No numeric C/V/U distance may compensate for or be presented as an
Evidence-span match. No aggregate measure may hide a state mismatch,
unsupported case, or invalid provenance path.

### 8.1 Corpus and annotation measures

Report:

- candidate, included, excluded, pilot, development, and evaluation counts;
- source and stratum composition;
- duplicate/near-duplicate removals and reasons;
- per-field pre-adjudication agreement and disagreement counts;
- adjudication counts and reasons; and
- reference amendments, exclusions after annotation, and unresolved cases.

Agreement measures must match the data type: categorical agreement/confusion
for states and codes, exact set agreement for observations/links, and exact
boundary agreement for spans. Any chance-corrected agreement statistic and
its interpretation require researcher approval because sparse labels and class
imbalance can make a single statistic misleading.

### 8.2 Observation detection

For each feature family, match a system observation to a reference observation
only when its approved typed content and complete Evidence-link set match. Use
one-to-one matching; an item cannot satisfy multiple references.

Report true-positive, false-positive, and false-negative counts and the
resulting precision, recall, and F1 separately per family. Micro and macro
summaries may be reported only in addition to, not instead of, family-level
results. Exact per-case set match and observation-count error are also
reported. The matching algorithm and treatment of multi-span or overlapping
observations must be frozen before unblinding.

### 8.3 Exact Evidence spans and links

The primary Evidence measure is exact match of feature family, start offset,
end offset, text, Rule ID, and required observation/component link. Report
exact-span/link precision, recall, F1, and whole-case exact graph match.

For diagnosis only, report start-boundary error, end-boundary error, and a
pre-approved character-overlap measure. Partial overlap is never promoted to
an exact match and cannot erase a wrong feature link, Rule ID, or observation
association. Evidence IDs themselves are not compared because they are
run-local identifiers.

### 8.4 Processing, diagnostics, and `UNKNOWN`

Report categorical confusion matrices and exact agreement for:

- `processing_status` per family;
- derived `DetectionStatus` per family;
- diagnostic presence, code, Rule ID, and exact candidate span;
- characteristic state separately for C, V, and U; and
- the material/non-material effect of unresolved inputs in V.

Report precision and recall for the `INCOMPLETE`/`UNRESOLVED`/characteristic
`UNKNOWN` classes when their denominators are non-empty. These are different
targets and must not be pooled. Also report invalid substitutions such as an
`UNKNOWN` reference emitted as zero, or a diagnostic candidate emitted as
Evidence, as explicit contract-violation counts.

### 8.5 C/V/U assessments

For each characteristic independently, report:

1. exact state agreement;
2. exact `Fraction` agreement among cases where both reference and system are
   `COMPUTED`;
3. exact joint state-and-value agreement, treating any state mismatch as a
   mismatch rather than coercing missing values to zero;
4. a confusion matrix over the approved exact values plus `UNKNOWN` and
   `NOT_APPLICABLE`; and
5. whole-profile exact match, requiring all three independent components to
   match, reported only as an additional measure.

An absolute numeric difference may be reported as a secondary diagnostic only
when both sides are `COMPUTED`, and only per characteristic. It is not a
substitute for exact-value accuracy, cannot cross an `UNKNOWN` boundary, and
must never be combined across C/V/U into a scalar quality or loss score.

### 8.6 Trace fidelity

For each characteristic, report exact agreement for governing Rule ID,
decision code, ordered input families, applicability, effect code, complete
observation references, complete diagnostic references, Finding references,
and coverage profile ID.

Additionally report counts for each graph-integrity invariant:

- every index resolves exactly once and is in range;
- every accepted observation and diagnostic consulted by a rule is referenced;
- every Evidence reference resolves and round-trips to source;
- completed absence has no fabricated Evidence;
- candidate diagnostic spans remain non-Evidence;
- the trace state/value branch agrees with the authoritative assessment; and
- Findings resolve one-to-one to the approved vague occurrences.

Report full-trace exact match per characteristic and per requirement only after
the component measures. A structurally valid but wrong decision code and a
correct decision with a broken Evidence path remain separately visible.

### 8.7 `SIGNAL` Findings

Match Findings one-to-one on characteristic, kind, code, Rule ID,
`criterion_id`, exact Evidence-link set, and source occurrence. Report event-
level precision, recall, F1, exact per-case Finding-set match, ordering errors,
and one-to-one provenance violations. Separately count any prohibited
`QUALITY_PROBLEM` or defect-like classification.

### 8.8 Coverage and non-claim compliance

Report the number and proportion of cases and feature-family opportunities in
each approved coverage-limitation category. For coverage-challenge cases,
report bounded-contract behavior and broader semantic limitation side by side;
do not call bounded non-recognition a false negative unless the exact approved
rule required recognition.

Report whether every evaluated record/report carries the canonical
`MVP-V0.1-BOUNDED-CVU-001` disclosure and whether output wording violates any
of its seven non-claims. Coverage statistics describe the corpus and current
boundary; they do not establish exhaustive coverage.

### 8.9 Reproducibility

Canonicalize and hash each structured per-case result. Report exact equality
and field-level differences across repeated runs. The number of repetitions,
machines/environments, and whether cross-environment equality is required are
researcher decisions. No random seed is a substitute for recording the full
environment and input hashes.

## 9. Experimental execution procedure

The later experiment proceeds only after all decision gates in §13 are closed.

1. Freeze the protocol, sampling frame, corpus candidates, codebook, annotation
   schema, duplicate policy, and analysis plan.
2. Inventory and hash all known binding, documentation, and test cases used for
   leakage screening.
3. Complete independent annotation, disagreement review, adjudication, and
   structural validation without system-output access.
4. Freeze and hash the final reference corpus.
5. Freeze the system artifact by commit SHA, package/version information,
   model-spec revision/hash, and configuration. Record the exact implemented
   rule inventory; do not claim unimplemented R3/F1-A coverage.
6. Freeze a read-only evaluation adapter that serializes existing extraction,
   assessment, trace, Finding, and coverage values without recalculation or
   production-model changes.
7. Run the binding and regression suites only as a separate readiness check.
   If readiness fails, stop before evaluating the holdout and record the
   failure; do not modify the holdout.
8. Execute the frozen system on the frozen independent corpus in the approved
   environment and preserve raw inputs, logs, structured outputs, console
   reports, commands, exit status, timestamps, and hashes.
9. Repeat execution according to the approved reproducibility plan.
10. Compare output to the reference with the frozen analysis implementation.
11. Produce the pre-registered tables before examining or categorizing
    individual errors.
12. Conduct the error analysis in §11 without changing the primary reference,
    matching rules, denominators, or acceptance interpretation.

If the system, reference, matching algorithm, or analysis code changes after
unblinding, the change creates a new experimental version. The original result
must remain reproducible and reported; a rerun must be labeled as such and
must not replace the original silently.

## 10. Data-leakage controls

The leakage register must include model-spec cases, approval proposals,
documentation examples, test fixtures, source-code literals, issue/PR examples,
pilot cases, and any corpus item viewed during implementation or debugging.

Before annotation and again before evaluation freeze:

- compare canonical exact text hashes;
- compare whitespace/punctuation-normalized forms for screening only;
- run a pre-approved lexical near-duplicate screen;
- manually review flagged pairs for meaning-preserving paraphrase or copied
  structure; and
- record the disposition of every flagged evaluation candidate.

The researcher must approve the near-duplicate method and decision rule. A
similarity score must not automatically remove a case without review, and no
cutoff is defined by this proposal.

Annotators must not query the system under test for evaluation cases. Model
developers must not see evaluation labels before the implementation freeze.
Evaluation failures must not be used to tune the same artifact and then be
reported as independent validation. If tuning occurs, those cases become
development data and a new untouched evaluation sample is required for a new
independent claim.

Sampling may deliberately include approved constructions and vague literals,
but the selection mechanism and enrichment must be disclosed. Enriched
results must not be presented as prevalence estimates for naturally occurring
requirements.

## 11. Error analysis

Error analysis begins only after primary measures are frozen and computed.
For every mismatch, preserve the case ID, reference output, system output,
exact source span where applicable, affected measure, and adjudicated category.

Use only researcher-approved categories derived from contract layers, for
example:

- corpus/reference defect;
- supported detector miss or extra observation;
- Evidence boundary, Rule-ID, or graph-link error;
- quantitative component/link error;
- processing-status or diagnostic error;
- `UNKNOWN` materiality/propagation error;
- C/V/U calculation or state/value error;
- trace decision/effect/reference error;
- `SIGNAL` creation, ordering, or provenance error;
- bounded-disclosure/reporting error; or
- unsupported grammar/semantic coverage limitation.

An error may receive multiple layer labels when propagation is involved, but
the report must distinguish a root annotation/model error from downstream
consequences. For example, one missed acceptance observation may cause an
Evidence error, a V-tier difference, and trace differences; those outputs are
all measured in their own units but must not be misreported as independent
root causes.

If review finds a reference error, retain the original reference, correction,
rationale, approver, and version. Report primary results against the frozen
reference and any corrected sensitivity result separately according to the
pre-approved amendment policy.

## 12. Reproducibility and reporting package

Subject to confidentiality and licensing constraints, the validation package
must contain or identify:

- approved protocol and decision record;
- sampling frame, source inventory, inclusion/exclusion log, and corpus hashes;
- leakage inventory and duplicate-review log;
- codebook, annotation schema, tool version, raw annotations, disagreements,
  adjudications, and reference release;
- frozen repository commit SHA, dependency lock/environment manifest, Python
  version, operating system, locale, encoding, parser resources, and command;
- evaluation-adapter and analysis-code versions and tests;
- raw structured outputs, console outputs, logs, exit status, timestamps, and
  hashes for every run;
- metric definitions, matching implementation, complete denominators, and
  machine-readable result tables;
- error ledger and reference-amendment history; and
- a limitations statement reproducing the approved bounded non-claims.

The experimental report must show results per feature family, characteristic,
construction stratum, and coverage class. It must disclose empty or small
denominators, missing data, exclusions, annotation disagreement, and deviations
from protocol. It must not report only favorable subsets or only a combined
summary.

Confidential data may be replaced in a public package by approved hashes and
audit metadata, but the researcher must approve how independent verification
remains possible. Redacted or paraphrased text cannot be substituted for the
exact text when calculating span measures.

## 13. Researcher decision gates

No gate below is resolved by this proposal. The experiment remains blocked
until the researcher records an explicit decision for each item.

| Gate | Decision required before execution |
| --- | --- |
| `G1 — Validation claim` | Approve the research questions, bounded claims, non-claims, unit of analysis, and intended population/sampling frame. |
| `G2 — Corpus sources` | Approve source domains/types, provenance requirements, licensing/confidentiality handling, collection window, and natural/synthetic case policy. |
| `G3 — Corpus size and composition` | Approve total size, pilot/development/evaluation split, construction strata, supported versus coverage-challenge composition, source balance, and treatment of repeated/mixed/`UNKNOWN` cases. No size or proportion is set here. |
| `G4 — Requirement-type metadata` | Decide whether descriptive human-assigned requirement types are recorded, define their taxonomy if used, and confirm they do not affect `RQD-023`, applicability, or scoring. |
| `G5 — Independence and annotation` | Approve annotator count, qualifications, independence/conflict rules, training, pilot procedure, blinding, adjudicator, and unresolved-case policy. |
| `G6 — Annotation artifacts` | Approve codebook, schema/serialization format, annotation tool, offset convention, limitation vocabulary, provenance/versioning, and reference-validation implementation. |
| `G7 — Leakage controls` | Approve the development-artifact inventory, exact/near-duplicate screening method, manual-review rule, prior-exposure policy, and disposition of flagged cases. No similarity cutoff is set here. |
| `G8 — Measures` | Approve observation matching, span/link matching, overlap diagnostic, agreement statistics, micro/macro summaries, trace/finding matching, stratification, and reproducibility comparisons. |
| `G9 — Evaluation artifact` | Approve the system commit/release, model-spec revision, environment, rule inventory, evaluation adapter, canonical serialization, repetition plan, and readiness criteria. |
| `G10 — Acceptance interpretation` | Define in advance how every reported measure and contract-violation count will be interpreted, which are primary/secondary, any confidence intervals or statistical tests, and any acceptance thresholds. This proposal defines none. |
| `G11 — Critical invariants` | Decide whether any Evidence-integrity, state/value, fabricated-Evidence, prohibited-`QUALITY_PROBLEM`, trace-integrity, disclosure, or determinism violation is independently disqualifying. No zero-tolerance rule is invented here. |
| `G12 — Amendments and reruns` | Approve handling of reference errors, protocol deviations, failed readiness, implementation changes after unblinding, corrected sensitivity analyses, and the conditions requiring a new untouched holdout. |
| `G13 — Reporting and release` | Approve reporting tables, error taxonomy, artifact retention, public/private release boundaries, independent audit access, and the exact wording of conclusions. |

Approval must identify the protocol version and must not be inferred from the
absence of objections. Thresholds or acceptance rules selected after viewing
evaluation results cannot support a pre-registered acceptance claim.

## 14. Unresolved dependencies and execution blockers

The following are intentionally unresolved by SRM-13 at proposal time:

1. Researcher decisions for all gates in §13, especially corpus size and
   composition, annotator/adjudicator process, measures, and acceptance
   interpretation.
2. An independently sourced corpus with approved rights, provenance, and no
   prohibited development leakage.
3. A frozen annotation codebook, limitation vocabulary, machine-readable
   schema, annotation tool, and independently reviewed reference derivation/
   validation implementation.
4. Named qualified annotators and an adjudicator who meet the approved
   independence policy.
5. A frozen implementation commit/release and environment representing the
   completed SRM-11/SRM-12 bounded model, plus an exact runtime rule inventory.
6. A read-only evaluation adapter and canonical serializer for the existing
   extraction, assessment, trace, Finding, and coverage contracts. It must not
   recalculate results or require production detector changes.
7. A frozen metric/matching implementation and analysis plan validated on
   non-evaluation cases.
8. A decision on handling confidential source text while retaining auditable
   exact-span evaluation.
9. Pre-registered acceptance interpretation and any thresholds. None exist in
   this proposal or in the cited SRM-13 obligations.

Until these dependencies are resolved and the reference corpus is frozen, no
experimental execution, expected C/V/U generation, acceptance conclusion, or
claim of independent validation is authorized.
