# SRM-13 — Researcher Approval Package

- **Decision status:** `PROPOSED — REQUIRES RESEARCHER DECISION`
- **Issue:** [#81 — SRM-13](https://github.com/rKiselyk/requirements-quality-assessment/issues/81)
- **Protocol under review:**
  [`srm-13-validation-protocol-proposal.md`](srm-13-validation-protocol-proposal.md)
- **Experiment status:** not started

## 1. Purpose and decision boundary

This package turns the existing SRM-13 protocol gates into a concise approval
record. It does not approve any gate, replace the protocol, create an
evaluation corpus or reference labels, define expected C/V/U values, implement
evaluation code, or authorize access to holdout results.

The validation target remains the researcher-approved bounded, Ukrainian,
single-requirement `RequirementQualityProfile(C, V, U)` and its existing
feature, Evidence, uncertainty, trace, `SIGNAL` Finding, and disclosure
contracts. C, V, and U remain independent. There is no scalar requirement or
file-quality score, confirmed-defect conversion, `QUALITY_PROBLEM`, confirmed
`U=0`, R3/F1-A runtime claim, exhaustive linguistic-coverage claim, or
software-product-quality claim.

The following timing labels distinguish a decision from the evidence needed to
close it:

- **NOW:** the researcher can approve the stated policy from the protocol and
  this record.
- **ARTIFACT:** the policy can be selected now, but final gate approval requires
  review of the named concrete artifact.
- **PRE-HOLDOUT:** the gate must be closed before the frozen system output or
  any holdout comparison/result is opened. Where the protocol sets an earlier
  boundary, that earlier boundary still applies.

## 2. Gate overview

No row below records approval. Every proposed choice is explicitly subject to
researcher decision.

| Gate | What the researcher must decide | What the protocol already fixes | What remains genuinely undecided and proposed disposition | Evidence required for final approval | Dependencies and timing |
| --- | --- | --- | --- | --- | --- |
| **G1 — Validation claim** | Approve the research questions, unit, bounded claims/non-claims, and intended population/sampling frame. | One trimmed non-empty Ukrainian line is one requirement; C/V/U are compared independently; the eight research questions and bounded/non-claim set are stated; development-visible cases are not independent observations. | The intended population and permissible generalization remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** approve the eight questions and bounded claims/non-claims as written; limit conclusions to the population actually defined by the approved source and sampling frame. | Signed decision citing the protocol version, approved RQs/non-claims, and a written target-population/sampling-frame statement. | No predecessor. **NOW** for claims; final wording precedes G2/G3 and is **PRE-HOLDOUT**. |
| **G2 — Corpus sources** | Approve source domains/types, provenance, rights/confidentiality, collection window/boundaries, and natural versus researcher-authored policy. | Eligibility requires Ukrainian software-requirement-like text, unchanged one-line representation, auditable provenance, no development use, pre-output stratum assignment, and annotatability under the bounded codebook. | Actual sources, access rights, time/project boundaries, redistribution, confidentiality, and authored-case treatment remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** use naturally occurring independent cases as the evaluation core; keep any researcher-authored enrichment outside the natural core and report it as a separate, non-prevalence stratum. If exact text cannot be public, use controlled audit access rather than paraphrasing span-evaluation text. | Versioned source inventory; permissions/licence and confidentiality record; collection procedure and window; provenance fields; natural/authored designation; public/private handling plan. | Depends on G1; constrains G3, G7, and G13. **NOW** for source policy, **ARTIFACT** for inventory/rights, before collection and **PRE-HOLDOUT**. |
| **G3 — Corpus size and composition** | Approve total size, partitioning, construction strata, supported/challenge composition, source balance, and treatment of repeated, mixed, and `UNKNOWN` cases. | Required strata and a separate coverage-challenge stratum are defined; supported and challenge results remain separate; pilot/training cases are permanently development-visible; difficult or `UNKNOWN` cases cannot be removed after results are seen. | Every count, proportion, balance, and sample-size justification remains open. **PROPOSED — REQUIRES RESEARCHER DECISION:** select either (A) a quota-stratified holdout, or (B) a natural-distribution core plus a separately reported enriched supported/challenge supplement. Option B preserves an observable natural core while ensuring bounded edge cases are exercised, but it requires strictly separate reporting and supports no prevalence claim from the supplement. | Approved sample-size rationale without invented assumptions; composition matrix with counts/quotas; partition manifest; source/stratum balance plan; inclusion/exclusion and mixed/repeated/`UNKNOWN` handling rules. | Depends on G1/G2 and, if used, G4; informs G5/G8/G10. **NOW** for design, **ARTIFACT** for final manifest, freeze before annotation/evaluation and **PRE-HOLDOUT**. |
| **G4 — Requirement-type metadata** | Decide whether to record human-assigned descriptive types and, if so, approve a taxonomy. | No automatic type classification is in scope; types cannot change `RQD-023`, applicability, observations, or C/V/U. | Whether types add useful descriptive stratification remains open. **PROPOSED — REQUIRES RESEARCHER DECISION:** omit type metadata unless a stated analysis need exists; if retained, make it annotation-only, version a finite taxonomy, and demonstrate that it is not an input to reference derivation or scoring. | Explicit omit/include decision; if included, taxonomy/codebook section, assignment guidance, and an invariance statement/test showing no effect on applicability or C/V/U. | Depends on G1/G2; an included taxonomy becomes part of G6 and G8 stratification. **NOW**; **ARTIFACT** only if included; **PRE-HOLDOUT**. |
| **G5 — Independence and annotation** | Approve annotator/adjudicator count and qualifications, independence/conflicts, training/pilot, blinding, adjudication, and unresolved-case policy. | Primary labels are independent and locked before cross-review; case order is randomized with opaque IDs; annotators do not see system output, test expectations, or each other's labels; raw labels and disagreements are retained; adjudication cites the approved rule/codebook; model-undetermined cases are not forced. | Staffing, competence criteria, allowed conflicts, training, pilot design, adjudicator separation, and unresolved-case disposition remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** choose either (A) two independent primaries plus a separate adjudicator, or (B) three independent primaries plus a separate adjudicator. A is leaner; B supplies more independent labels but costs more. In either case, detector implementers are not independent primaries for their rules unless the conflict is explicitly approved and disclosed. | Named/pseudonymous role roster; qualification and language/domain criteria; conflict/prior-exposure declarations; training/pilot plan and logs; locked-submission/blinding procedure; adjudication and unresolved-case policy. | Depends on G2/G3; its role policy informs G6, while actual annotation cannot begin until G6 closes. Policy is **NOW**; roster and operating proof are **ARTIFACT**; close before evaluation annotation and **PRE-HOLDOUT**. |
| **G6 — Annotation artifacts** | Approve codebook, concrete schema/serialization, tool, offsets, limitation vocabulary, provenance/versioning, and independent reference validation. | The logical schema, required distinctions, zero-based end-exclusive Unicode code-point offsets, exact source round-trip, exact rational values, allowed Finding scope, immutable provenance, and independence from production derivation are specified. | Concrete codebook, controlled limitation vocabulary, storage format, tool behavior, validator implementation, and versions do not exist in approved frozen form. **PROPOSED — REQUIRES RESEARCHER DECISION:** use a versioned machine-readable record such as JSON Lines plus immutable manifests/hashes, provided it preserves the protocol schema exactly; mechanically derive or validate only fields fixed by human labels, using reviewed code independent of production. | Frozen codebook; schema and serialization specification; limitation vocabulary; tool/version and user instructions; validator/reference-derivation review and non-evaluation tests; offset/reference-integrity validation report; hashes. | Depends on G1/G4/G5; enables G8 and final annotation. Policy is **NOW**, closure is **ARTIFACT**, before evaluation annotation and **PRE-HOLDOUT**. |
| **G7 — Leakage controls** | Approve the development inventory, exact/near-duplicate method, manual review, prior-exposure policy, and flagged-case disposition. | Binding, documentation, fixture, source-literal, issue/PR, pilot, and debugging cases enter the leakage register; exact and normalized screening plus a pre-approved lexical screen and manual review are required; no score auto-removes a case; tuning converts holdout cases to development data. | The lexical method, flagging cutoff if any, meaning-preserving review rule, reviewer, and case-disposition rule remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** use deterministic exact/normalized checks plus a versioned lexical near-duplicate screen; validate and select any flagging cutoff only on non-evaluation examples; require documented human disposition of every flag and prior exposure. No automatic exclusion cutoff is proposed. | Hashed development-artifact inventory; method/version and validation examples; approved flagging rule/cutoff or explicit no-cutoff method; reviewer guidance; prior-exposure declarations; complete flagged-pair disposition log from both screening passes. | Depends on G2/G3/G6; affects G12. Policy is **NOW**, method and logs are **ARTIFACT**; first pass before annotation, second before reference freeze, and always **PRE-HOLDOUT**. |
| **G8 — Measures** | Approve observation, Evidence, trace/Finding, state/value, agreement, stratification, overlap-diagnostic, and reproducibility comparisons. | Typed-content observation matching, strict joint matching, deterministic multiset pairing, exact span/link rules, exact C/V/U state-and-`Fraction` comparisons, trace/Finding integrity, family/characteristic/stratum reporting, denominators, and supported/challenge separation are specified. Partial overlap is diagnostic only. | The character-overlap diagnostic, any chance-corrected agreement statistic, final micro/macro set, canonical serialization, and cross-environment comparison remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** approve the protocol's exact family-level/component measures as primary; make micro/macro summaries and a pre-specified overlap measure secondary; report raw per-field agreement/disagreement in all cases and add a chance-corrected statistic only if its data assumptions and interpretation are separately justified. | Preregistered measure dictionary with primary/secondary labels and denominators; frozen typed-content/link serialization; matching/analysis implementation and tests on non-evaluation cases; approved overlap and agreement-statistic rationale; table shells. | Depends on G3/G6 and coordinates with G9/G10. Policy is **NOW**, analysis implementation is **ARTIFACT**, and all choices are **PRE-HOLDOUT**. |
| **G9 — Evaluation artifact** | Approve the exact system/model/environment, rule inventory, read-only adapter, canonical serialization, repetition plan, and readiness criteria. | The artifact is frozen by commit/spec/environment; R3/F1-A cannot be claimed; the adapter serializes without recalculation or production changes; binding/regression cases are readiness-only; readiness failure stops before holdout execution. | The exact commit/release, hashes, environment, adapter, serializer, run count/environment coverage, and readiness criteria remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** freeze the completed bounded implementation by commit and model-spec hash; publish an exact supported/unimplemented rule inventory; require the existing binding and regression suites to pass as readiness evidence, not validation evidence. Choose either (A) repeated runs in one frozen environment, or (B) repeated runs plus a separately specified cross-environment check; B supports a broader reproducibility statement but increases environment-control work. | Immutable artifact manifest; commit/spec/dependency/environment/configuration hashes; rule inventory; reviewed adapter and serializer with non-evaluation tests; approved repetition matrix; readiness command, criteria, and signed run record. | Depends on G6/G8; feeds G10/G11/G12. Policy is **NOW**, closure is **ARTIFACT**, and readiness must pass before any holdout execution. |
| **G10 — Acceptance interpretation** | Predefine interpretation of every measure/violation, primary versus secondary status, statistical analysis if any, and any acceptance thresholds. | No threshold, target accuracy, confidence interval, test, or pass/fail rule is approved; post-result selection cannot support a preregistered acceptance claim; C/V/U cannot be collapsed. | The study currently has no justified acceptance rule. **PROPOSED — REQUIRES RESEARCHER DECISION:** choose (A) descriptive bounded validation with no accept/reject claim or thresholds, or (B) a preregistered acceptance study with separately justified per-measure thresholds/statistical assumptions fixed before results. A is decision-ready without inventing scientific cutoffs but cannot yield a pass/fail validation claim; B can, but only after the researcher supplies a defensible basis. | Signed interpretation matrix for every primary/secondary measure and contract count; conclusion vocabulary; if B, documented rationale for each threshold, interval, test, and assumption independent of holdout results. | Depends on G1/G3/G8 and must align with G11/G13. **NOW** to choose A or B; any B artifacts and the whole gate are strictly **PRE-HOLDOUT**. |
| **G11 — Critical invariants** | Decide whether specified integrity, prohibited-output, disclosure, or determinism failures independently invalidate readiness/run/acceptance. | The protocol requires counts for Evidence, state/value, fabricated-Evidence, trace, Finding, disclosure, and reproducibility violations, but invents no zero-tolerance rule. | Which violations are disqualifying, at what level, and whether a stopped run may be repaired or rerun remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** choose (A) treat source/Evidence round-trip failure, invalid state/value substitution, fabricated Evidence, prohibited `QUALITY_PROBLEM`, broken mandatory trace references, missing bounded disclosure, and non-deterministic canonical output as independently disqualifying integrity failures; or (B) report all as non-automatic acceptance inputs. A protects contract validity but is a substantive zero-tolerance decision; B avoids that rule but permits an accepted result with integrity violations. | Approved invariant-to-disposition matrix stating readiness, run-validity, and acceptance effects; machine-check/report fields; linkage to amendment/rerun policy. | Depends on G8/G9/G10; constrains G12/G13. **NOW** for the policy, validation checks are **ARTIFACT**, and closure is **PRE-HOLDOUT**. |
| **G12 — Amendments and reruns** | Approve handling of reference defects, deviations, readiness failures, post-unblinding changes, sensitivity analyses, and triggers for a new untouched holdout. | Original artifacts/results are retained; reference corrections are versioned and sensitivity results remain separate; post-unblinding system/reference/matching/analysis changes create a new experimental version; tuning on holdout requires a new untouched evaluation sample for a new independent claim. | Exact deviation classes, approval authority, repair/rerun triggers, and presentation precedence remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** retain the frozen-reference result as primary and label corrected-reference output as sensitivity analysis; stop on failed readiness; require a new version for any post-unblinding implementation, matching, analysis, or acceptance-rule change; require a new untouched holdout after tuning. | Versioned amendment/deviation SOP; decision authority and log schema; rerun/new-holdout trigger matrix; report template showing original and corrected analyses without replacement. | Depends on G7/G9/G10/G11; constrains G13. **NOW** for policy, SOP is **ARTIFACT**, and the policy is **PRE-HOLDOUT**. |
| **G13 — Reporting and release** | Approve report tables, error taxonomy, retention, public/private boundaries, audit access, and exact conclusion wording. | Required package contents, disaggregated reporting, denominators, exclusions/disagreements/deviations, bounded non-claims, and no favorable-subset-only reporting are specified. Exact text cannot be paraphrased for span evaluation. | Retention duration/location, release model, audit access, confidentiality controls, final table layouts, taxonomy wording, and conclusions remain open. **PROPOSED — REQUIRES RESEARCHER DECISION:** use a hybrid release: publish protocol, decisions, methods, code/hashes, aggregate tables, and releasable cases; provide controlled independent-audit access to restricted exact text and labels where rights prevent publication. Pre-approve conclusion templates consistent with the G10 path. | Frozen table shells and error taxonomy; data-management/retention plan; public/private artifact matrix; audit-access procedure; approved conclusion templates and limitations text. | Depends on G2/G8/G10/G11/G12 and evidence from all other gates. Policy and templates are **NOW/ARTIFACT** and **PRE-HOLDOUT**; final populated report/release follows execution. |

## 3. Decisions needing additional explanation

### 3.1 G2–G3: source realism and deliberate coverage are different claims

A natural-distribution corpus answers questions about the sampled sources. An
enriched corpus is useful for exercising rare bounded constructions,
coverage-challenge cases, repeated observations, mixed states, and `UNKNOWN`,
but its proportions cannot be interpreted as natural prevalence. If the
researcher selects G3 option B, the core and supplement need separate IDs,
denominators, tables, and conclusion language. Neither may contain a binding
case, development fixture, documentation/example case, pilot/training case, or
meaning-preserving near-duplicate of one.

### 3.2 G5–G7: independence requires both role separation and case separation

Blinding system output does not by itself create independence. The approval
record must also cover annotator conflicts, prior exposure, locked primary
submissions, pilot-case exclusion, developer access to labels, and the two
leakage-screening passes. A model-undetermined case must follow the approved
unresolved/exclusion policy and remain in corpus accounting; it cannot be
forced into a label or quietly discarded.

### 3.3 G8: approve exact matching separately from diagnostic similarity

The protocol already defines exact identities for observations, Evidence,
links, assessments, traces, and Findings. Character overlap is useful only for
diagnosing a missed boundary; it cannot turn a partial span, wrong Rule ID, or
wrong link into an exact match. Likewise, a numeric difference between two
computed characteristic values cannot cross an `UNKNOWN` boundary or replace
exact C/V/U state-and-value comparison.

### 3.4 G10–G11: performance interpretation and contract validity are distinct

G10 asks what measured performance means. G11 asks whether particular contract
violations invalidate a run or acceptance independently of aggregate
performance. Selecting descriptive validation under G10 option A does not
answer G11: the researcher must still decide whether a structurally invalid or
non-deterministic output can support any validation conclusion. Conversely, a
G11 integrity rule is not a target accuracy or annotator-agreement cutoff.

### 3.5 G12: corrections cannot retroactively restore independence

A documented reference correction can support a sensitivity analysis while
preserving the original frozen result. It does not authorize silent replacement
of the primary analysis. If holdout failures are used to change the system,
matching logic, analysis, or acceptance interpretation, those cases have
become development-visible; a new independent claim requires a new untouched
holdout under the approved policy.

## 4. Approval sequence

The following sequence separates immediate policy decisions from later
artifact approvals and protects the holdout boundary:

1. **Approve now:** G1; G2 source policy; G3 design option; G4; G5 role model;
   G7 screening policy; G8 primary/secondary measure policy; G9 reproducibility
   option; G10 interpretation path; G11 invariant policy; G12 amendment policy;
   and G13 release model.
2. **Review concrete artifacts before their gates close:** G2 source inventory
   and rights; G3 composition/partition manifest; G5 roster and procedures; G6
   complete annotation package; G7 leakage implementation and logs; G8 frozen
   analysis plan/implementation; G9 frozen system bundle; G10/G11 interpretation
   matrices; G12 SOP; and G13 report/release templates.
3. **Before any system-output access:** close every gate, freeze and hash the
   corpus/reference/system/analysis artifacts, pass readiness, and record the
   approval against exact versions. No threshold, matching rule, denominator,
   invariant disposition, or conclusion wording may be chosen after viewing
   holdout results for a preregistered claim.

## 5. Approval record

For each gate, the researcher should record `APPROVE`, `APPROVE WITH STATED
CHANGES`, or `DO NOT APPROVE`, identify the exact protocol/package and artifact
versions reviewed, and sign/date the decision. Silence or absence of objections
is not approval. Until all thirteen gates and their required artifacts are
explicitly approved, issue #81 remains open and no independent-validation or
acceptance conclusion is authorized.
