# SRM-13 — G2 Priority-Source Evidence and Approval-Readiness Review

- **Review status:**
  `SOURCE_EVIDENCE_REVIEWED / SOURCE_APPROVAL_PENDING / CORPUS_NOT_CREATED`
- **Review scope:** Prozorro `requestForProposal` documentation and the TAPAS
  sports-title modernization specification only
- **Evidence retrieval:** 2026-09-24 23:36:21 EEST
  (`2026-09-24T20:36:21Z`)
- **Binding source policy:**
  [`srm-13-g2-source-decisions.md`](srm-13-g2-source-decisions.md)
- **Earlier feasibility review:**
  [`srm-13-source-feasibility.md`](srm-13-source-feasibility.md)
- **Researcher gate decisions:**
  [`srm-13-researcher-decisions.md`](srm-13-researcher-decisions.md)
- **Protocol:**
  [`srm-13-validation-protocol-proposal.md`](srm-13-validation-protocol-proposal.md)

## 1. Scope and evidence convention

This review applies the approved G2.1–G2.6 policies to the two first-priority
sources. It records evidence needed for a later source approval or rejection;
it does not approve either source, create a source register, collect
requirements, or establish that either source passed G7.

Statements below use these labels:

- **Source statement:** a statement made by the candidate document, its source
  repository, or its publishing site.
- **Documented evidence:** an observation verified from a cited source or a
  reproducible property computed from the retrieved bytes.
- **Researcher decision:** an already approved rule from the binding G2/G7/G13
  context.
- **Unresolved question:** evidence or approval still required before the source
  can be accepted or rejected for G2.

Hashes are lowercase SHA-256 values computed from the downloaded response body.
The downloads and any review-time extraction were kept outside the repository;
no candidate requirement text was added to the project. An original-file hash
identifies the retrieved bytes but does not itself establish reuse permission
or an adequate audit-access mechanism.

## 2. Prozorro `requestForProposal`

### 2.1 Exact identification and version

- **Source statement:** the document is titled `requestForProposal` and labels
  its substantive section as a development plan and technical implementation
  requirements. It belongs to the
  [`ProzorroUKR/openprocurement.api`](https://github.com/ProzorroUKR/openprocurement.api)
  project, whose repository identifies the software as an API interface to the
  OpenProcurement database.
- **Documented evidence:** source organization: **ProzorroUKR**; project:
  **openprocurement.api**; document type: open-project implementation
  documentation containing a development plan and technical requirements.
- **Documented evidence:** the human-readable moving page is
  [`requestForProposal`](https://prozorro-api-docs.readthedocs.io/uk/master/features/request_for_proposal.html).
  The exact reviewed source is
  [`docs/source/features/request_for_proposal.rst` at commit
  `3fec5a97c31913aefc3f05e0ad6b929fd8148b4c`](https://github.com/ProzorroUKR/openprocurement.api/blob/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/docs/source/features/request_for_proposal.rst).
  GitHub reports that commit with committer time 2025-12-26 04:12:26 UTC; the
  [commit object](https://github.com/ProzorroUKR/openprocurement.api/commit/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c)
  supplies the version identifier. The document has no separate author-stated
  release number or approval date.
- **Documented evidence:** retrieval time: 2026-09-24 23:36:21 EEST. The pinned
  [raw source](https://raw.githubusercontent.com/ProzorroUKR/openprocurement.api/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/docs/source/features/request_for_proposal.rst)
  was 8,733 bytes and had original-file SHA-256
  `45ba9e25bd55b44f80201436ff1985feb47a8c7e06bdaec979db98d162679c81`.
- **Documented evidence:** extracted-text hash: **PENDING**. The source is UTF-8
  reStructuredText, but no researcher-approved rule yet defines whether the
  canonical candidate text is raw markup, rendered text, or a specified
  extraction. Computing a corpus extraction hash before that choice would
  create an unapproved representation.

### 2.2 Immutable auditability

- **Documented evidence:** the Git commit and path identify an immutable Git
  object independently retrievable through the repository UI and the pinned raw
  URL. This is materially stronger than the moving Read the Docs `master` page.
- **Source statement:** the repository publishes its source and history on
  GitHub under the
  [Apache License 2.0](https://github.com/ProzorroUKR/openprocurement.api/blob/3fec5a97c31913aefc3f05e0ad6b929fd8148b4c/LICENSE.txt).
- **Researcher decision:** G2.3 nevertheless requires the researcher-approved
  source record to identify the permitted immutable-copy and audit-access
  mechanism; public Git availability does not by itself complete that approval.
- **Unresolved question:** confirm that the pinned raw Git object is the
  approved audit copy, or specify a separately retained immutable copy and its
  lawful independent-access procedure.

### 2.3 Rights and action-specific readiness

The repository licence is affirmative evidence, but this review does not issue
a legal conclusion. Compliance must be confirmed for the intended artifacts.

| Planned action | Documented evidence | Approval readiness and unresolved point |
| --- | --- | --- |
| Retain exact source text | Apache-2.0 grants reproduction rights for the licensed work, subject to its terms; the repository places `LICENSE.txt` beside the documentation source. | **Potentially supportable.** Confirm that this documentation file is within the licensed work and record the licence and retained notices with the exact copy. |
| Create and retain annotations | Apache-2.0 grants permission to prepare derivative works, subject to its terms. Whether a particular annotation record is legally a derivative work need not be assumed because either characterization must be covered by the approved data-management plan. | **Potentially supportable.** Researcher/rights review must confirm the lawful basis and attribution treatment for annotations linked to exact text. |
| Publish exact text and annotations | Apache-2.0 permits distribution of the work and derivative works subject to section 4 conditions, including providing the licence, marking modified files, retaining applicable notices, and handling any applicable `NOTICE`; section 6 does not grant trademark permission. | **Potentially supportable, not yet approved.** Define the release form and verify its licence, notice, modification, attribution, and name/logo treatment. |
| Provide independent audit access | The pinned Git object is publicly readable and versioned, and the licence supplies affirmative copying/distribution evidence subject to its conditions. | **Technically feasible.** Researcher approval is still required for the exact public or controlled audit mechanism and retention plan. |

### 2.4 Project/source-family proposal and independence

- **Proposed project ID:** `PROZORRO-OPENPROCUREMENT-RFP`.
- **Proposed source-family ID:** `PROZORRO-OPENPROCUREMENT-DOCS`.
- **Documented evidence:** the organization, repository, path, and named
  `requestForProposal` feature support treating this as one identifiable
  OpenProcurement implementation project and one repository-documentation
  family.
- **Documented evidence:** it is organizationally and technically distinct from
  the TAPAS/Ministry of Youth and Sports service reviewed below.
- **Unresolved question:** other OpenProcurement repositories and feature pages
  may share authors, templates, or requirement text. The proposed family must
  be widened if documented authorship or reuse evidence warrants it.
- **Researcher decision:** these identifiers and the apparent cross-project
  distinction are proposals only. They neither establish textual independence
  nor replace the two G7 screens, prior-exposure declarations, and manual flag
  dispositions.

### 2.5 Original-one-line suitability

- **Documented evidence:** the pinned RST contains nested numbered lists,
  subordinate bullets, inline cross-references, and list introductions. Some
  lines are self-contained implementation directives, while some subordinate
  entries are fragments such as component names and only make sense with a
  parent item.
- **Specific risk:** the raw RST and rendered HTML do not expose identical text:
  markup is removed or transformed during rendering. Selecting rendered text
  without an approved mapping would weaken exact source round-tripping;
  selecting a fragment with its parent would violate the no-joining rule.
- **Researcher decision:** an eligible case must already be one complete,
  non-empty Ukrainian requirement line. No paraphrasing, joining, or
  reconstruction is allowed.
- **Unresolved question:** approve the canonical representation and extraction
  method, then exclude any item that is incomplete on its own source line. The
  eligible quantity remains `UNKNOWN` until that rule is applied without using
  system output.

### 2.6 Preliminary confidentiality and operational sensitivity

- **Documented evidence:** no confidentiality designation, credentials,
  person-level records, or secret values were observed in the inspected RST.
  The document is intentionally published in a public software repository and
  describes module structure, state logic, configuration schemas, tests, and
  documentation tasks.
- **Specific risk:** public implementation details can still be operationally
  sensitive or become outdated; public availability is not a confidentiality
  disposition.
- **Unresolved question:** before inclusion, complete and record a source-wide
  confidentiality/secret/operational-sensitivity review for the exact pinned
  file and decide whether any lines require exclusion.

### 2.7 Exact actions remaining before source approval or rejection

1. Researcher approves or changes the proposed document, project, and
   source-family identifiers and the pinned commit/path as the reviewed version.
2. Researcher or qualified rights reviewer confirms that the repository licence
   covers the documentation and approves the action-specific licence,
   attribution, notice, modification, and trademark handling.
3. Researcher approves the immutable-copy retention and independent-audit
   mechanism under G2.3/G13.
4. Researcher approves the canonical RST representation, extraction method and
   version, and original-one-line eligibility procedure; only then is the
   extracted-text hash computed.
5. The source-specific confidentiality disposition is completed.
6. The approved G7 development inventory, prior-exposure process, duplicate and
   near-duplicate screens, and manual dispositions are completed separately.
7. On that evidence, the researcher records an explicit G2 source approval or
   rejection. The existing `PROMISING` feasibility classification is not that
   decision.

## 3. TAPAS sports-title modernization specification

### 3.1 Exact identification and version

- **Source statement:** the PDF is titled **“Технічні вимоги на модернізацію
  електронної-комунікаційної системи «Онлайн сервіс для переведення у публічну
  площину процесу присвоєння спортивних звань з видів спорту, офіційно визнаних
  в Україні»”**. It identifies **Eurasia Foundation**, accredited as implementer
  of the TAPAS international technical-assistance project, as the customer and
  the **Ministry of Youth and Sports of Ukraine** as recipient.
- **Documented evidence:** organization/program: **Eurasia Foundation / TAPAS**;
  recipient organization: **Ministry of Youth and Sports of Ukraine**;
  project: modernization of the online sports-title service; document type:
  technical requirements/specification.
- **Documented evidence:** the exact reviewed source URL is
  [`Lot-2-TV_zvannia_2023.pdf`](https://tapas.org.ua/wp-content/uploads/2023/12/Lot-2-TV_zvannia_2023.pdf).
  The document states “Kyiv, 2023,” contains 65 pages, and has no visible
  revision identifier. Its PDF metadata title is `ТЕХНІЧНІ ВИМОГИ 2023 на
  TAPAS.docx`; the producer is the Google Docs renderer, with no creation or
  modification date in the PDF metadata. The server reported `Last-Modified:
  Mon, 18 Dec 2023 14:59:35 GMT`, which is transport metadata, not an
  author-approved document version.
- **Documented evidence:** retrieval time: 2026-09-24 23:36:21 EEST. The PDF was
  4,266,596 bytes and had original-file SHA-256
  `28e53c7decd70c5f71dfe70c08b85113bc4d8dcc72951a77664b7350faa2029e`.
- **Documented evidence:** extracted-text hash: **PENDING**. No
  researcher-approved PDF extraction tool/version, layout policy, or treatment
  of diagrams and visual line wrapping exists yet.

### 3.2 Requirement-content evidence and immutable auditability

- **Source statement:** the document says that it defines technical and
  quantitative characteristics and contains the recipient's functional,
  non-functional, software, implementation, and warranty-service requirements.
- **Documented evidence:** the contents and body include role, functional,
  integration, software, reliability, security, interface, operating, and
  documentation requirements, including explicit system obligations and
  quantitative constraints. This confirms substantive fit for G2.1 but does
  not establish one-line eligibility or an approved quantity.
- **Documented evidence:** the live TAPAS URL supplies current public access,
  but it is mutable and therefore is not by itself an immutable audit copy.
- **Documented evidence:** the Internet Archive index reports a
  [2024-12-09 17:14:28 UTC capture](https://web.archive.org/web/20241209171428id_/https://tapas.org.ua/wp-content/uploads/2023/12/Lot-2-TV_zvannia_2023.pdf).
  On 2026-09-24 the archived response was explicitly marked as truncated by
  length and returned only 1,048,576 bytes, versus 4,266,596 bytes for the live
  PDF. It failed PDF cross-reference validation and is not an exact, usable
  immutable copy.
- **Unresolved question:** no complete independently hosted immutable copy was
  verified. A lawful retained copy, rights-holder-issued version, or another
  complete independently auditable mechanism is required before approval.

### 3.3 Rights and action-specific readiness

The TAPAS site states that all rights are reserved and that use of site
materials is permitted with a link to the site; the statement is visible in the
footer of the [TAPAS electronic-services page](https://tapas.org.ua/components/elektronni-posluhy/).
It does not expressly define “use,” identify corpus/annotation uses, or state
the extent of permitted copying. The PDF does not contain a source-specific
reuse licence.

| Planned action | Documented evidence | Approval readiness and unresolved point |
| --- | --- | --- |
| Retain exact source text | The site provides an affirmative but general permission to use site materials when linking to the site; it also reserves all rights. | **Unresolved.** Confirm in writing whether exact PDF and extracted requirement text may be retained, for how long, by whom, and with what link/attribution. |
| Create and retain annotations | Neither the footer statement nor the PDF expressly addresses annotations, derived records, or exact-text links embedded in annotations. | **Unresolved.** Obtain an authorized determination or permission covering annotation creation and retention. |
| Publish exact text and annotations | The general “use with link” statement does not specify permissible extent, redistribution format, derivative annotations, or whether the PDF is a “site material” covered by the statement. | **Unresolved.** Obtain source-specific confirmation of what exact text and annotations may be released and the required attribution/link wording; otherwise use only a separately approved restricted path if lawful. |
| Provide independent audit access | The live PDF is public, but mutable. The only verified third-party archive capture is incomplete. | **Blocked.** Establish lawful access to a complete immutable exact copy and approve a public or controlled independent-audit procedure under G13. |

- **Unresolved question:** identify the rights holder and the person or
  organization authorized to grant or interpret permission. The customer,
  recipient, site operator, document drafter, and owner of the specification
  may not be the same entity; their roles must not be inferred from the public
  URL.

### 3.4 Project/source-family proposal and independence

- **Proposed project ID:** `TAPAS-MMS-SPORTS-TITLES-2023`.
- **Proposed source-family ID:** `TAPAS-GOVERNMENT-SERVICE-SPECIFICATIONS`.
- **Documented evidence:** the named service, ministry recipient, TAPAS customer
  context, and 2023 modernization scope support treating this as one
  identifiable project distinct from the Prozorro API implementation project.
- **Specific uncertainty:** TAPAS and other donor-funded government-service
  specifications may share a programme, procurement template, drafter,
  contractor, or copied technical clauses. The broad provisional family is
  intentionally conservative until authorship and reuse evidence is obtained.
- **Researcher decision:** organizational and domain differences do not prove
  textual independence. The proposed IDs do not establish a G7 result.

### 3.5 Original-one-line suitability

- **Documented evidence:** the PDF uses paragraphs, nested bullets, tables,
  headings, diagrams, and page-spanning visual layout. Many requirements span
  multiple displayed or extracted lines; some bullets depend on an introductory
  clause, and the appendices describe workflows graphically.
- **Specific risk:** a PDF text extractor can introduce reading-order changes,
  line breaks, page numbers, or merged table cells. Joining wrapped lines or a
  parent clause with a subordinate bullet would violate the approved
  no-joining/no-rewriting rule even when the resulting sentence appears
  semantically natural.
- **Researcher decision:** only a complete requirement that already satisfies
  the original-one-line rule may be selected. Diagrams, fragments, and
  multi-line clauses cannot be reconstructed into cases.
- **Unresolved question:** approve a canonical PDF representation, extraction
  tool/version, visual-to-text line identity rule, and exclusion procedure.
  Until applied independently of system output, the eligible quantity remains
  `UNKNOWN` and may be materially smaller than the visible requirement count.

### 3.6 Preliminary confidentiality and operational sensitivity

- **Documented evidence:** no confidentiality marking was found in the
  searchable PDF text. The inspected document describes organizational roles,
  application workflows, interfaces, reliability, access control, information
  protection, logging, and protection of personal data. It did not expose
  actual applicant records, credentials, or secret values in the inspected
  searchable text.
- **Specific risk:** detailed current/future workflow appendices and security,
  role, and integration requirements can reveal operational design even without
  containing personal records. Embedded diagrams or non-searchable content may
  require separate visual review.
- **Unresolved question:** the researcher must record whether each eligible
  line is non-confidential and operationally safe for the chosen public or
  controlled release path. Public posting alone is not that determination.

### 3.7 Exact actions remaining before source approval or rejection

1. Identify the rights holder and an authorized contact; obtain a written,
   action-specific determination for exact-text retention, annotation,
   publication, and independent audit, including exact attribution/link terms.
2. Obtain an author- or rights-holder-confirmed version/revision, or explicitly
   approve the 2023 PDF identified by its URL, retrieval timestamp, byte length,
   and SHA-256 as the reviewed version despite the missing revision identifier.
3. Establish lawful access to a complete immutable exact copy. The truncated
   Internet Archive capture is insufficient. Approve the public or controlled
   independent-audit mechanism under G2.3/G13.
4. Approve the PDF extraction tool/version, canonical text and line-identity
   rules, and original-one-line eligibility procedure; only then compute the
   extracted-text hash.
5. Confirm or revise the project/source-family identifiers after checking
   drafter, contractor, programme-template, and copied-clause relationships.
6. Complete the document-wide confidentiality and operational-sensitivity
   review, including visual appendices and embedded content.
7. Complete the separate approved G7 inventory, prior-exposure controls,
   duplicate and near-duplicate screens, and manual dispositions.
8. On that evidence, the researcher records an explicit G2 source approval or
   rejection. The existing `PROMISING` feasibility classification is not that
   decision.

## 4. Approval-readiness result

| Source | Evidence now established | Current approval blocker |
| --- | --- | --- |
| Prozorro `requestForProposal` | Exact repository/path and commit; immutable public Git object; original-file hash; requirement-content fit; explicit repository Apache-2.0 evidence; provisional project/family IDs | Action-specific licence-compliance approval, canonical RST/extraction and one-line procedure, approved audit-retention mechanism, confidentiality disposition, and later G7 evidence |
| TAPAS sports-title specification | Exact PDF URL; document identity, organizations, year and transport metadata; original-file hash; requirement-content fit; site-level attribution statement; provisional project/family IDs; proof that the available third-party archive capture is incomplete | Source-specific rights authority and permission for all four actions, complete immutable audit copy/access, authoritative version disposition, canonical PDF extraction and one-line procedure, confidentiality/sensitivity disposition, and later G7 evidence |

Neither source is approved for the independent corpus, neither has passed G7,
and no G1, G2, G3, G7, or G13 gate or issue #81/#68 is closed by this review.
