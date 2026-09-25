# SRM-13 — G2 Prozorro Source Decision Package

- **Package status:**
  `DECISION_PROPOSED / RESEARCHER_APPROVAL_PENDING / CORPUS_NOT_CREATED`
- **Candidate:** Prozorro `requestForProposal` open-project documentation
- **Binding source policy:**
  [`srm-13-g2-source-decisions.md`](srm-13-g2-source-decisions.md)
- **Source-specific evidence review:**
  [`srm-13-g2-priority-source-review.md`](srm-13-g2-priority-source-review.md)
- **Protocol and gate decisions:**
  [`srm-13-validation-protocol-proposal.md`](srm-13-validation-protocol-proposal.md)
  and [`srm-13-researcher-decisions.md`](srm-13-researcher-decisions.md)

## 1. Purpose and decision boundary

This package makes the Prozorro source review ready for an explicit researcher
decision. Every procedure below is **proposed**, not approved. No requirement
record has been extracted, no extracted-text hash has been computed, and no
source has been admitted to a pilot or holdout.

Licence evidence and proposed compliance steps are documented separately from
legal conclusions. A qualified reviewer must determine whether the repository
licence covers the reviewed documentation and whether the proposed use meets
all applicable obligations.

## 2. Pinned source and existing evidence

| Field | Evidence |
| --- | --- |
| Organization | `ProzorroUKR` |
| Repository/project | [`ProzorroUKR/openprocurement.api`](https://github.com/ProzorroUKR/openprocurement.api) |
| Document | `requestForProposal` development plan and technical implementation requirements |
| Pinned commit | [`3fec5a97c31913aefc3f05e0ad6b929fd8148b4c`](https://github.com/ProzorroUKR/openprocurement.api/commit/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c) |
| Pinned path | [`docs/source/features/request_for_proposal.rst`](https://github.com/ProzorroUKR/openprocurement.api/blob/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/docs/source/features/request_for_proposal.rst) |
| Pinned raw URL | [`raw.githubusercontent.com/.../request_for_proposal.rst`](https://raw.githubusercontent.com/ProzorroUKR/openprocurement.api/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/docs/source/features/request_for_proposal.rst) |
| Retrieved | 2026-09-24 23:36:21 EEST (`2026-09-24T20:36:21Z`) |
| Retrieved size | 8,733 bytes |
| Original-file SHA-256 | `45ba9e25bd55b44f80201436ff1985feb47a8c7e06bdaec979db98d162679c81` |
| Extracted-text SHA-256 | **PENDING canonical-procedure approval; not computed** |

The pinned commit/path is the source-version authority. The moving
[Read the Docs page](https://prozorro-api-docs.readthedocs.io/uk/master/features/request_for_proposal.html)
is useful for inspection but is not proposed as the version authority.

## 3. Licence evidence and compliance proposal

### 3.1 Documented evidence

- The pinned commit contains
  [`LICENSE.txt`](https://github.com/ProzorroUKR/openprocurement.api/blob/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/LICENSE.txt),
  which contains the Apache License, Version 2.0.
- Apache-2.0 defines source form to include documentation source and grants,
  subject to its terms, rights to reproduce, prepare derivative works, display,
  sublicense, and distribute the work. The official
  [Apache-2.0 text](https://www.apache.org/licenses/LICENSE-2.0) is the external
  reference; the repository copy is the source-specific evidence.
- Section 4 requires a licence copy for recipients, prominent change notices in
  modified files, retention of applicable copyright/patent/trademark/
  attribution notices, and reproduction of applicable `NOTICE` attributions.
  Section 6 grants no general trademark permission beyond customary source
  identification and reproducing `NOTICE` content.
- A recursive inspection of the complete pinned commit tree on 2026-09-24 found
  `LICENSE.txt` at the repository root and no file named `NOTICE` or
  `NOTICE.txt`. The reviewed RST contained no embedded licence, copyright, or
  notice line. This is commit-specific evidence, not a statement that no other
  obligation exists.

### 3.2 Proposed compliance record

If a qualified reviewer confirms that Apache-2.0 covers the RST, the source
record and every distributed research artifact containing its exact text should:

1. identify `ProzorroUKR/openprocurement.api`, the pinned commit/path, original
   URL, retrieval timestamp, byte length, and original-file hash;
2. include or accompany a copy of Apache-2.0 and link to the pinned repository
   licence;
3. preserve every applicable source notice; record that no `NOTICE` file was
   found in the pinned tree, while rechecking this fact if the approved source
   version changes;
4. mark the extracted research representation and annotations as research-made
   transformations rather than upstream files;
5. use the Prozorro/OpenProcurement names only as reasonably necessary to
   identify provenance, without implying endorsement or using logos; and
6. document separately whether exact text, mapped extraction, annotations, and
   release files are treated as copies, derivative works, or separable records,
   without relying on that characterization to avoid compliance.

### 3.3 Questions requiring qualified rights review

- Does the root repository licence legally cover this documentation file even
  though the file has no individual licence header?
- Does the proposed retained exact copy, mapped text extraction, annotation
  package, and public/controlled release satisfy Apache-2.0 and any applicable
  Ukrainian law or third-party rights?
- Are there applicable attribution or provenance notices outside `LICENSE.txt`
  that must accompany the documentation despite the absence of `NOTICE`?
- Does any planned presentation use a protected name or mark beyond reasonable
  provenance identification?

This package proposes compliance documentation; it does not answer those legal
questions.

## 4. Proposed immutable-copy and independent-audit procedure

Subject to the qualified rights determination, the researcher should approve
the following G2.3/G13 procedure:

1. Treat the pinned Git commit/path and the existing original-file SHA-256 as
   the source-version identity.
2. Retain an access-controlled, read-only copy of the exact 8,733 downloaded
   bytes together with the source URL, commit, path, retrieval timestamp, byte
   length, SHA-256, repository licence, and the commit-tree `NOTICE` check.
3. Keep that original byte copy separate from any later extracted text. Never
   overwrite it; a later upstream version becomes a new append-only source
   version.
4. For ordinary independent audit, direct an auditor to the pinned raw Git URL
   and require SHA-256 verification against the recorded value.
5. If the upstream host becomes unavailable or returns different bytes, provide
   the retained exact copy through the researcher-approved controlled-access
   process, together with the same provenance and hash. Access terms must permit
   the auditor to verify the exact text and offsets without substituting a
   paraphrase or redaction.
6. Record every audit-copy access and the version/hash supplied. Public release
   of the retained copy is allowed only if the rights/compliance decision says
   so; otherwise use the approved controlled path.

The retained mirror is a proposed resilience measure, not an already created
corpus artifact. The public Git object alone remains dependent on GitHub
availability, while the controlled fallback remains dependent on lawful
retention and an approved access process.

## 5. Proposed project and source-family identifiers

- **Project ID:** `PROZORRO-OPENPROCUREMENT-RFP`
- **Source-family ID:** `PROZORRO-OPENPROCUREMENT-DOCS`

Supporting evidence is the named `requestForProposal` feature, its single
repository/path, the repository's OpenProcurement API purpose, and the shared
documentation/version history. The family deliberately groups this item with
other OpenProcurement documentation that may share authors, templates, or
implementation language; a new document must not be treated as independent
merely because it has another page path.

The researcher must confirm or revise both IDs. Authorship, copied text, shared
templates, related repositories, and earlier/later feature phases remain to be
checked. This grouping supports but does not replace G7. No G7 pass or holdout
independence is claimed.

## 6. Preliminary confidentiality disposition

### Proposed disposition

`PROVISIONALLY_PUBLIC_TECHNICAL_DOCUMENT / LINE_LEVEL_REVIEW_PENDING`

The pinned RST is intentionally published in a public source repository. The
source-specific review found no confidentiality marking, credentials,
person-level records, or secret values; its visible content concerns modules,
state logic, configuration schemas, tests, and documentation work.

Before any source approval, a reviewer must inspect the complete pinned file
for credentials/tokens, personal data, non-public endpoints, vulnerability-
enabling operational detail, third-party confidential text, and any line whose
release status differs from the document-level disposition. Public availability
is evidence of publication, not by itself a confidentiality or security
approval.

## 7. Canonical RST representation options

| Option | Original-line identity | Markup and list handling | Nested fragments | Exact-text round-trip | Unicode offsets | Consequence |
| --- | --- | --- | --- | --- | --- | --- |
| **A. Raw physical RST line** | One decoded physical source line at the pinned path; remove only its line terminator. | Preserve indentation, list markers, roles, backticks, emphasis markers, and targets literally. | Still exclude incomplete fragments; parent and child lines cannot be joined. | Direct equality to the stored raw line is strongest. | Offsets are direct in the unnormalized decoded line, but they include markup and structural indentation. | Highest audit simplicity, but the assessed text contains authoring syntax and may not be a natural-language requirement as rendered. |
| **B. Verified single-line visible-text projection** | One raw physical line remains the sole source anchor; a deterministic mapping emits only visible text from that same line. | Remove only approved structural tokens, such as leading indentation/list marker and supported inline-markup delimiters; preserve visible wording and punctuation exactly. Every emitted code point maps to its source position. | Exclude any item needing a parent, continuation, substitution, directive, or another line. Never reconstruct it. | Raw bytes and raw line remain available; the projected line round-trips through a stored monotonic source map. Projection alone cannot recreate removed syntax. | Assessment offsets address projected, unnormalized Unicode code points; the map also records corresponding raw-line code-point and UTF-8 byte intervals. | Best balance between natural text and auditability, but it is a research transformation requiring explicit approval, a versioned mapper, and structural validation. |
| **C. Rendered HTML/plain-text output** | Renderers may combine or rearrange physical lines and resolve cross-references; original source-line identity is not inherent. | Markup disappears according to the Sphinx/docutils version and configuration. | Rendering can make dependent fragments look self-contained without proving that they were one source line. | Requires a verified renderer-to-source map that is not presently available. | Rendered offsets do not directly identify raw-source offsets. | Not suitable as the canonical representation unless a versioned, validated source map is separately approved. |
| **D. RST logical list item or paragraph** | Treats wrapped/continued source lines as one logical block. | Parser may join lines and inherit parent-list context. | Encourages combining parents, children, or continuation lines. | Cannot satisfy the approved no-joining rule when more than one physical line contributes. | Offsets span several source lines and require synthetic separators. | Reject for this source under the current original-one-line policy. |

No option authorizes selection of a list label, heading, component-name bullet,
or other fragment that is not a complete requirement on its own.

## 8. Recommended extraction and eligibility procedure for approval

### Recommendation

Approve **Option B, verified single-line visible-text projection**, with Option
A retained as the immutable audit anchor. This is a proposal for researcher and
qualified-rights review, not an operative extraction authorization.

If approved, the versioned procedure should be:

1. Verify the exact input bytes against the recorded original-file SHA-256,
   then decode UTF-8 strictly. Do not apply Unicode normalization, character
   substitution, typographic correction, case folding, or whitespace cleanup.
2. Enumerate physical source lines using the file's actual line terminators.
   A candidate may consume exactly one physical line; remove only its line
   terminator for the raw-line value. Never concatenate a continuation, parent,
   child, label, or adjacent line.
3. Parse only a frozen, documented subset of single-line RST syntax. The mapper
   may omit structural indentation, one leading list marker, and supported
   inline-markup delimiters/targets. It must copy every visible Ukrainian text
   code point and punctuation mark unchanged and in order from that same line.
4. Emit a monotonic map for every projected Unicode code point to the raw-line
   Unicode code-point interval and UTF-8 byte interval that produced it.
   Removed structural tokens map to no output. No output character may be
   invented.
5. Reject a line if markup is malformed, ambiguous, unsupported, resolved from
   another line/file, or cannot be mapped deterministically. In particular,
   reject substitutions, directives, implicit cross-line content, and an inline
   reference whose visible wording cannot be separated from its target without
   a verified same-line map.
6. Apply G2.1 eligibility without system output. The projected line must be
   non-empty Ukrainian text, be presented as a software requirement,
   constraint, acceptance statement, or explicit verification statement, and
   be complete without inherited parent/list context. Exclude headings,
   introductions, component-name fragments, link-only lines, and every item
   that would require joining or reconstruction.
7. Store, when collection is separately authorized, the commit/path, one-based
   physical line number, exact raw line, projected line, mapper version, and
   source map. Verify that re-running the mapper on the raw line reproduces the
   projected line and map byte-for-byte.
8. Define assessment spans as zero-based, half-open intervals over the
   projected line's unnormalized Unicode code points, and preserve the mapping
   back to raw code-point and UTF-8 byte intervals. This offset proposal must be
   reconciled with the still-pending G6 offset convention before annotation.
9. Only after the procedure, implementation, and structural tests are approved
   may an extracted-text artifact and its hash be created. Approval does not by
   itself authorize holdout collection.

This procedure preserves the immutable original while preventing rendered text
or parser convenience from silently changing the one-line unit. Its main cost
is a mapping artifact and conservative exclusion of otherwise useful but
structurally ambiguous items.

This package does not close G1, G2, G3, G7, G13, issue #81, or issue #68.

## 9. Researcher decision matrix

| PROPOSED | EVIDENCE | RESEARCHER_DECISION_REQUIRED | REMAINING_BLOCKER |
| --- | --- | --- | --- |
| Use commit `3fec5a97…` and the pinned RST path as the source version. | Immutable Git commit/path, retrieval timestamp, 8,733-byte size, and recorded original-file SHA-256. | Approve or reject this exact version identity. | None beyond explicit decision; any later version must be a new source-register entry. |
| Treat Apache-2.0 as the candidate lawful basis for retention, annotation, permitted publication, and audit. | Root `LICENSE.txt`; Apache-2.0's source-form definition includes documentation source and its grant supplies relevant rights subject to conditions. | Qualified reviewer confirms that the licence covers this file and confirms compliance for each planned action. | Legal scope/sufficiency and any external third-party rights remain unresolved. |
| Carry licence/provenance, change notices, applicable source notices, and restrained name use; record no `NOTICE` in the pinned tree. | Section 4/6 conditions; complete pinned tree contains no `NOTICE`; reviewed RST has no file-level notice. | Approve the exact attribution/licence/change-notice template. | Recheck if source version or release form changes. |
| Use pinned public Git retrieval plus a lawful read-only controlled fallback copy for independent audit. | Commit URL, raw URL, and original-file hash provide independent byte verification today. | Approve retention, access controls, audit logging, and public-versus-controlled release path. | Qualified rights confirmation and operating procedure are pending. |
| Assign project `PROZORRO-OPENPROCUREMENT-RFP` and family `PROZORRO-OPENPROCUREMENT-DOCS`. | Named feature, repository, path, and shared OpenProcurement documentation context. | Confirm or revise both identifiers and family boundary. | Authorship/template/reuse evidence and G7 screening remain pending. |
| Record `PROVISIONALLY_PUBLIC_TECHNICAL_DOCUMENT / LINE_LEVEL_REVIEW_PENDING`. | Public repository; no marking, credentials, person-level records, or secrets observed in the source review. | Approve disposition after complete confidentiality/operational-sensitivity check. | Document-wide and later line-level review remain pending. |
| Approve Option B with raw Option A audit anchor and the nine-step eligibility/mapping procedure. | One-line G2 rule; RST markup/nesting risks; proposed monotonic same-line source map and conservative exclusions. | Approve, amend, or reject the canonical representation, mapper scope, offset convention, and eligibility rules. | No extraction or extracted-text hash until approval; G6 offset convention must align. |
| Keep source approval separate from holdout eligibility. | Binding G7 requires prior-exposure controls and two screening passes. | Later approve the G7 method, inventory, and dispositions independently. | Prozorro has not passed G7 and is not approved for holdout inclusion. |
