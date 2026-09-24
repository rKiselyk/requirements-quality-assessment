# SRM-13 — Researcher Policy Decision Record

- **Decision status:**
  `RESEARCHER_POLICY_DECISIONS_APPROVED / ARTIFACT_APPROVAL_PENDING / EXPERIMENT_NOT_STARTED`
- **Researcher decision date:** 2026-09-24
- **Protocol:**
  [`srm-13-validation-protocol-proposal.md`](srm-13-validation-protocol-proposal.md)
- **Approval package:**
  [`srm-13-approval-package.md`](srm-13-approval-package.md)
- **Issue:** [#81 — SRM-13](https://github.com/rKiselyk/requirements-quality-assessment/issues/81)

## 1. Decision effect

The researcher approves the policy choices below for the existing G1–G13
protocol gates. This record does not approve the later corpus, codebook,
taxonomy definitions, annotation or analysis artifacts, validator, sample
size, similarity cutoff, frozen system artifact, acceptance threshold,
experimental result, conclusion, or release.

No gate is fully closed by this policy record alone. Each gate closes only
after its listed concrete artifact or final determination exists, is reviewed
against an identified version, and is explicitly approved. Until all gates
close, no holdout-system-output access, expected C/V/U generation, acceptance
conclusion, or claim of independent experimental validation is authorized.

Approved binding cases, development fixtures and pilot cases, and independent
holdout data remain separate. Development-visible cases and their
near-duplicates cannot enter the holdout or its performance measures.

## 2. Gate decisions and closure conditions

| Gate | Approved policy | Pending concrete artifact or final determination | Prerequisite for closing the gate |
| --- | --- | --- | --- |
| **G1 — Validation claim** | Validate only the bounded independent C/V/U model: approved features, exact Evidence, processing and assessment states, trace, `SIGNAL` Findings, and bounded disclosures. No broader linguistic, defect, scalar-quality, product-quality, or population claim is authorized. The intended population is limited to the approved public-source sampling frame. | Final population wording against the actual G2 source inventory. | Researcher approval of the versioned population/sampling-frame statement and confirmation that every planned conclusion remains within it. |
| **G2 — Corpus sources** | Use public Ukrainian software specifications, technical assignments, and open-project documents from multiple independent projects. Natural requirements are the primary source. Provenance, collection period, reuse rights, and independent-audit access are mandatory. | Actual source inventory, project independence record, collection period, provenance, reuse-rights evidence, and source-specific audit-access disposition. | Researcher approval of the frozen source inventory and rights/audit record; any source lacking lawful and adequate audit access is excluded under G13. |
| **G3 — Corpus size and composition** | Use a natural core plus a separately identified and reported enriched supplement. Determine sizes and quotas only after a separate development-only pilot. The pilot may improve methodology, tools, and implementation before freezing, but a scientific-rule change requires separate approval. Pilot cases and their near-duplicates never enter the holdout. | Development-only pilot plan and results; total size; core/supplement quotas; source and construction-stratum composition; partition manifest; treatment counts for mixed, repeated, coverage-challenge, and `UNKNOWN` cases. | Separate researcher approval of the size rationale, quotas, composition, and frozen partition manifest after the pilot and before holdout annotation/evaluation. |
| **G4 — Requirement-type metadata** | Record a descriptive two-level, human-assigned taxonomy: a base requirement type and an optional non-functional subtype. It is annotation-only and cannot affect `RQD-023`, applicability, observations, or C/V/U. | Exact base-type and optional-subtype definitions, allowed values, assignment guidance, and representation in the codebook/schema. | Researcher approval of the taxonomy section in the frozen codebook and confirmation that reference derivation and scoring do not consume it. |
| **G5 — Independence and annotation** | Use two independent primary annotators plus a separate adjudicator. All must be experienced in requirements engineering and proficient in Ukrainian. Developers neither annotate nor adjudicate. Primary labels are blind, submitted independently, and immutable. A truly model-undetermined field may be excluded only from its affected metric under a frozen policy with full accounting; a legitimate `UNKNOWN` is evaluated as `UNKNOWN`, not excluded or converted to zero. | Named/pseudonymous roster; qualification and conflict/prior-exposure records; training and development-pilot procedure; blind locked-submission workflow; adjudication procedure; exact field-level exclusion/accounting policy for model-undetermined cases. | Researcher approval of the roster and frozen annotation/adjudication/unresolved-field procedures before holdout annotation begins. |
| **G6 — Annotation artifacts** | Use a versioned codebook and JSON Lines reference records, with primary annotations separated from adjudication records. Reference derivation and structural validation must be independent, reviewed, non-production implementations and must not call production detectors or calculators. | Frozen codebook; exact JSONL schema; primary/adjudication record definitions; annotation tool; limitation vocabulary; provenance/versioning rules; independent derivation/validator implementation, review, and non-evaluation validation evidence. | Researcher approval of the complete hashed annotation package and a successful source-offset/reference-integrity validation report before reference freeze. |
| **G7 — Leakage controls** | Screen exact hashes, normalized forms, and versioned near-duplicates; manually review and document every flag; control declared prior exposure; screen before annotation and again before reference freeze. No similarity cutoff is approved or invented by this decision. | Hashed development-artifact inventory; exact normalization and near-duplicate method/version; flagging rule; reviewer guidance; prior-exposure records; complete disposition logs from both passes. If a numeric cutoff is later proposed, it remains a separate researcher decision. | Researcher approval of the screening method and development inventory before annotation, followed by approval of the final screening/disposition log before reference freeze. |
| **G8 — Measures** | Report primary feature-observation, Evidence span/link, processing/state, C/V/U, trace, Finding, and reproducibility measures separately. Secondary overlap or distance diagnostics cannot replace exact matching. Report the natural core and enriched supplement separately. | Frozen measure dictionary with primary/secondary labels, denominators, stratification, agreement summaries, any secondary diagnostic, canonical matching/serialization, table shells, and tested non-production analysis implementation. | Researcher approval of the preregistered analysis plan and hashed matching/analysis implementation validated only on non-evaluation cases, before holdout-system-output access. |
| **G9 — Evaluation artifact** | Repeat execution in one frozen environment and retain exact artifact, input, command, environment, run, and result provenance. | Final repeat count; exact system commit/model-spec/environment/configuration and rule inventory; artifact manifest; read-only adapter and canonical serializer; readiness criteria and record. | Researcher approval of the repeat count and immutable artifact manifest, plus successful readiness completion, before executing the system on the holdout. |
| **G10 — Acceptance interpretation** | Use descriptive validation. No acceptance threshold, overall pass/fail performance claim, or post-result acceptance rule is authorized. C, V, and U remain separate. | Preregistered interpretation matrix for every measure and contract-violation count, primary/secondary labels, and bounded conclusion wording consistent with descriptive validation. | Researcher approval of the interpretation matrix and conclusion templates before holdout-system-output access. |
| **G11 — Critical invariants** | Critical integrity and prohibited-output violations independently limit claims of contract conformity. Preserve and report the original result rather than repairing it silently. | Exact per-field, per-run, and conclusion-level disposition matrix for Evidence integrity, state/value substitution, fabricated Evidence, prohibited `QUALITY_PROBLEM`, trace integrity, disclosure, and determinism violations. | Separate researcher approval of the frozen disposition matrix and its linkage to G12 rerun/reporting rules before holdout-system-output access. |
| **G12 — Amendments and reruns** | Retain frozen primary results. Version reference corrections and report corrected sensitivity analyses separately. Any post-unblinding system, reference, matching, analysis, or interpretation change creates a new experimental version. Tuning on holdout data requires a new untouched holdout for a new independent claim. | Amendment/deviation procedure; approval authority; version and log schema; failed-readiness and rerun trigger matrix; report layout preserving original and sensitivity results. | Researcher approval of the frozen amendment/rerun procedure before holdout-system-output access. |
| **G13 — Reporting and release** | Use a hybrid public/controlled-access release. Publish every artifact that rights permit and provide an approved independent-audit path for restricted exact source text. Exclude a source when lawful and adequate audit access cannot be established. | Source-specific public/private matrix; retention plan; controlled-access and independent-audit procedure; reporting tables and error taxonomy; bounded conclusion and limitation templates; final release inventory. | Researcher approval of the data-management, audit-access, reporting, and release plan before holdout-system-output access, followed by separate approval of any populated report and release after execution. |

## 3. Current authorization boundary

This decision authorizes preparation of the pending artifacts and the separate
development-only pilot within the policies above. It does not authorize the
holdout experiment. Issue #81 and the broader milestone issue #68 remain open;
neither this record nor the approval package is an experimental validation or
an acceptance conclusion.
