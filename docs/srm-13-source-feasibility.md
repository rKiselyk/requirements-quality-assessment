# SRM-13 — G2 source feasibility

- **Status:** `EXPLORATORY / RESEARCHER_APPROVAL_REQUIRED / CORPUS_NOT_CREATED`
- **Binding context:**
  [`srm-13-researcher-decisions.md`](srm-13-researcher-decisions.md) and the
  G2, G3, G7, and G13 provisions of
  [`srm-13-validation-protocol-proposal.md`](srm-13-validation-protocol-proposal.md)
- **Approved G2 source policies:**
  [`srm-13-g2-source-decisions.md`](srm-13-g2-source-decisions.md)
- **Issue:** [#81 — SRM-13](https://github.com/rKiselyk/requirements-quality-assessment/issues/81)

## 1. Purpose and evidence convention

This note tests whether a small, diverse set of public sources could support
the later G2 natural corpus. It is not a source inventory, a sampling frame, a
collection authorization, or a selected corpus. It does not set a collection
window, source balance, size, quota, or G3 pilot design.

The assessments below use these evidence labels:

- **Verified** means that the linked source document, repository, or
  source-specific terms state the fact directly.
- **Estimate** is a deliberately coarse feasibility indication from visible
  pages or enumerated directives. It is not an eligible-case count. Exact
  quantity remains `UNKNOWN` until a rights-cleared development-only pilot can
  apply the one-line and inclusion rules without rewriting source text.
- **Unresolved** means that the source does not establish the fact, or that a
  researcher or rights determination is still required.

Classifications have the following limited meaning:

- `PROMISING`: content, provenance, audit access, and an affirmative reuse
  basis are visible; the researcher must still approve the source and the
  exact use.
- `NEEDS_RIGHTS_REVIEW`: content and provenance appear feasible, but public
  access does not establish the needed right to retain or release exact text.
- `UNSUITABLE`: the inspected material does not fit the natural-requirement
  source policy well enough to justify further G2 work.

## 2. Candidate summary

| Candidate project/document | Source organization and type | Date/version | Usable-content evidence and quantity | Rights and independent audit | Independence and development exposure | Classification |
| --- | --- | --- | --- | --- | --- | --- |
| [Prozorro `requestForProposal` development plan and technical implementation requirements](https://prozorro-api-docs.readthedocs.io/uk/master/features/request_for_proposal.html) ([repository](https://github.com/ProzorroUKR/openprocurement.api)) | **Verified:** `ProzorroUKR/openprocurement.api`, public open-project API documentation and an implementation plan. The repository describes itself as the API interface to the OpenProcurement database. | **Verified:** live `master` documentation; no document date is shown. A commit SHA must be pinned if approved. | **Verified:** the page has numbered Ukrainian directives to create modules and schemas, move and configure state logic, preserve unaffected modules, add tests, and add documentation. **Estimate:** at least 12 visibly separate directives; exact eligible one-line quantity `UNKNOWN`. | **Verified:** the repository labels itself Apache-2.0, and its [licence](https://github.com/ProzorroUKR/openprocurement.api/blob/master/LICENSE.txt) expressly includes documentation source and permits reproduction and distribution subject to its conditions. Git history and a pin-able commit support independent audit. No confidentiality designation was found on the inspected page. | A distinct procurement-platform codebase, not one of the government-service or hardware procurements below. A targeted repository scan found no project name, document title, or inspected distinctive phrase in current development artifacts; this is only a feasibility check, not G7 screening. | `PROMISING` — clearly requirement-like Ukrainian project directives, versionable provenance, public audit, and an explicit repository licence. |
| [Modernization of the online service for awarding sports titles](https://tapas.org.ua/wp-content/uploads/2023/12/Lot-2-TV_zvannia_2023.pdf) | **Verified:** technical requirements naming the Eurasia Foundation/TAPAS as customer and the Ministry of Youth and Sports of Ukraine as recipient; government-service modernization specification. | **Verified:** Kyiv, 2023; no revision identifier is shown. | **Verified:** 65-page document whose contents identify general, functional, integration, software, reliability, security, interface, and operating requirements. The body contains explicit Ukrainian system obligations and quantitative constraints. **Estimate:** dozens of plausible requirement lines; exact eligible quantity `UNKNOWN`, especially where PDF bullets or clauses span physical lines. | **Verified:** the TAPAS site footer states “all rights reserved” but also permits use of site materials when the site is cited; see the statement on this [TAPAS page](https://tapas.org.ua/components/elektronni-posluhy/). The public PDF gives direct audit access and no confidentiality marking was found. **Unresolved:** whether that general permission covers retention and later release of an exact-text derived research corpus, and what attribution form is required. | A separate sports-administration system. It shares the TAPAS programme and common public-sector specification style with other TAPAS documents, so documents from that programme must be treated as one source family until G7 manual review establishes otherwise. No targeted local match was found. | `PROMISING` — rich natural requirements, strong provenance, public audit, and an affirmative site-use statement, conditional on researcher confirmation that the statement covers the planned exact-text use. |
| [Online platform for accommodating internally displaced persons in temporary accommodation](https://www.unhcr.org/ua/sites/ua/files/legacy-pdf/%D0%94%D0%BE%D0%B4%D0%B0%D1%82%D0%BE%D0%BA-%D0%90-%D0%A2%D0%B5%D1%85%D0%BD%D1%96%D1%87%D0%BD%D0%B5-%D0%B7%D0%B0%D0%B2%D0%B4%D0%B0%D0%BD%D0%BD%D1%8F-%D0%A2%D0%97.pdf) | **Verified:** technical requirements hosted by UNHCR Ukraine, naming Ukraine's Ministry for Reintegration as customer and the state as project/IP owner; humanitarian/government web platform. The document does not identify its drafter. | **Verified:** no revision identifier; its schedule calls for an MVP in November–December 2024 and a final version by May 2025. | **Verified:** 12 pages of role, workflow, reporting, performance, integration, security, accessibility, interface, test, and support requirements, including quantitative constraints. **Estimate:** dozens of plausible requirement lines; exact eligible quantity `UNKNOWN`. | **Verified:** [UNHCR's terms](https://www.unhcr.org/ua/terms-amp-conditions) allow attributed extracts for research or study but require prior written permission for substantial reproduction; the PDF itself also attributes project IP to the state. Direct public access permits inspection while the link remains live. **Unresolved:** which rights holder can authorize corpus retention/release, whether planned extraction is “substantial,” and whether a stable audit copy may be kept. The source concerns a vulnerable population and includes security requirements, so the absence of person-level case data and operational-sensitivity risks must be checked before use. | Organizationally and functionally distinct from the other candidates. The document mentions integration with Trembita, but that dependency does not establish shared authorship. No targeted local match was found; full prior-exposure declarations and G7 screening remain mandatory. | `NEEDS_RIGHTS_REVIEW` — excellent content fit and direct audit access, but the site's extract-only research permission does not clearly authorize the likely corpus use. |
| [Software/hardware complex for Suspilne's audiovisual television archive](https://corp.suspilne.media/media/documents/zagalni-dokumenti/Obgruntuvannia/Tekhnichne_zavdannya_Arkhiv_video_2022.pdf) | **Verified:** АТ «Національна суспільна телерадіокомпанія України» (Suspilne); procurement technical assignment for an audiovisual archive and related software, hardware, integration, and support. | **Verified:** the linked filename and a separate [procurement justification](https://corp.suspilne.media/media/documents/zagalni-dokumenti/Obgruntuvannia/Prohramno_aparatnoho_kompleksu_audiovizualnoho_arkhivu_telebachennya.pdf) place the procurement in 2022; no revision identifier is shown. | **Verified:** 40-page table with Ukrainian functional, capacity, availability, integration, installation, and support obligations, including measurable file-processing and storage constraints. **Estimate:** dozens of plausible software/system requirement lines within a larger mixed procurement; exact eligible quantity `UNKNOWN`. | **Verified:** the PDF is directly accessible from Suspilne's corporate site, whose footer asserts АТ «НСТУ» copyright. No reuse licence or source-specific permission was found on the document or landing site. Public inspection is feasible while the URL persists, but retention, redistribution, and a durable audit copy are unresolved. No personal data was observed in inspected requirement passages; third-party product and commercial details are present. | An independent broadcaster and specialist media-archive project, materially different from public-service web portals. No targeted local match was found. Product-specific language and procurement boilerplate still require G7 review against other tender documents. | `NEEDS_RIGHTS_REVIEW` — strong and distinctive natural requirements, but accessibility alone supplies no reuse permission. |
| [Zhytomyr “Safe City” landfill IP-video-surveillance system](https://zt-rada.gov.ua/files/upload/sitefiles/_29.pdf) ([source page](https://zt-rada.gov.ua/?pages=658)) | **Verified:** Zhytomyr City Council; technical assignment for design, creation, and deployment of a departmental IP-video-surveillance system with software, network, equipment, and service requirements. | **Verified:** the source page is dated 15 June 2017 and groups this document with the 2017–2019 “Safe City” programme; the PDF itself shows no date or revision. The page date must not be silently treated as the PDF's approval date. | **Verified:** 8 pages containing Ukrainian system, access-control, scalability, interoperability, web-client, licence-count, retention, availability, and support obligations alongside substantial hardware and installation content. **Estimate:** more than 10 plausible software/system clauses, but exact eligible quantity and the software-only yield are `UNKNOWN`. | **Verified:** the council page and PDF provide direct public audit access. No reuse licence or permission was found on the page or PDF. **Unresolved:** retention/release rights and whether infrastructure/security details warrant additional handling even though the council published them. | A municipal infrastructure project, independent in organization and domain from the other candidates. The “Safe City” page contains several related phases and assignments, so only one project boundary should be used until copied/template text is screened. No targeted local match was found. | `NEEDS_RIGHTS_REVIEW` — potentially useful domain diversity, but rights are unestablished and the software-requirement yield may be low after excluding hardware/service clauses. |

## 3. Boundary case not recommended for the shortlist

The public [Trembita 2.0 pilot repository](https://github.com/Trembita-installation/t2.0-client-instruction)
identifies the Ministry of Digital Transformation as system holder, State
Enterprise “Diia” as administrator, a 90-day pilot beginning 7 July 2025, and
a file named
[`01_VYMOGY.md`](https://github.com/Trembita-installation/t2.0-client-instruction/blob/main/01_VYMOGY.md)
for pilot technical requirements. Its visible repository structure is
dominated by participant prerequisites, installation, configuration,
application forms, and pilot operating instructions. The repository page does
not display a licence.

Classification: `UNSUITABLE` for the natural core. The material is valuable
operational documentation, but it does not presently provide a clean source of
software-product requirements, and its reuse terms are unresolved. It should
not be included merely to increase source count. A later G3 pilot could revisit
a specifically identified system-requirement artifact if one is found and
rights-cleared; this repository alone is insufficient.

## 4. Independence and preliminary exposure finding

The five retained candidates concern independently named software projects and
five visibly different organizational settings: a procurement-platform
codebase, a TAPAS/ministry service, a UNHCR-hosted ministry platform, a public
broadcaster, and a municipal council. This is project diversity, not proof of
statistical or authorship independence.

A targeted, case-insensitive scan of the current repository's `docs`, `src`,
and `tests` content found no candidate project name, document title, or
inspected distinctive phrase. That negative scan does not close G7. Before any
candidate can enter a pilot or holdout, the approved leakage procedure must
cover the complete development inventory, commit history and issue/PR examples,
annotator/developer prior exposure, exact and normalized text, a versioned
near-duplicate screen, and documented manual disposition of every flag.

Particular independence risks are already visible:

- TAPAS and other donor-funded government specifications may reuse shared
  templates or consultants; they must not be counted as independent merely
  because the recipient system differs.
- Public procurements often repeat legal, security, architecture, and support
  boilerplate across unrelated buyers.
- Related phases on the Zhytomyr “Safe City” page are one programme family
  unless evidence supports a narrower independent-project boundary.
- A dependency or integration reference, such as the IDP platform's planned
  Trembita integration, is not itself evidence of common authorship, but it
  must be recorded for manual review.

## 5. Proposed diversity and G3 pilot gaps

If the researcher accepts the source types and rights dispositions, a useful
feasibility shortlist is:

1. Prozorro open-project implementation requirements as the clearest
   licence-and-provenance case;
2. the TAPAS sports-title service as a functional public-service
   modernization specification;
3. the UNHCR/MinReintegration IDP platform after rights resolution;
4. the Suspilne archive after rights resolution, for media-processing and
   quantitative non-functional requirements; and
5. the Zhytomyr system only if rights and software-only yield justify the
   additional municipal-infrastructure domain.

This set is diverse by project purpose and document setting, but it remains
heavily public-sector and procurement-oriented. It has no verified private
commercial, mobile-product, embedded, safety-critical, or agile backlog source.
Those are population gaps, not reasons to add unverified material. Any final G1
population claim must be limited to the approved source frame.

The later development-only G3 pilot must measure, without setting quotas in
advance here:

- how many source clauses survive the exact one-line/no-rewriting rule;
- the frequency of table cells, bullet fragments, multi-sentence clauses, and
  PDF extraction or Unicode defects;
- software-requirement yield after hardware, procurement-administration,
  supplier-qualification, and service-only text is excluded;
- coverage of the approved construction strata, including completed absence,
  mixed/repeated observations, `UNKNOWN`, and coverage-challenge cases;
- template and near-duplicate rates within and across source families; and
- whether public URLs, permitted archived copies, hashes, and provenance
  metadata provide durable independent audit access.

No candidate quantity, balance, quota, or holdout allocation is approved by
this feasibility review.

## 6. Researcher choices required before collection

The researcher must make or commission the following concrete decisions before
collection begins:

1. **Source taxonomy and shortlist:** confirm that open-project implementation
   plans and mixed software/hardware procurement assignments are permitted
   source types, and select which candidate projects proceed to rights review
   and a development-only pilot.
2. **Rights standard:** decide what evidence is sufficient to retain exact
   source text, create annotations/derived records, publish releasable cases,
   and provide a durable independent-audit copy. Confirm the Apache-2.0
   obligations for Prozorro and the scope of the TAPAS attribution permission;
   obtain written permission where the UNHCR, Suspilne, or Zhytomyr terms do
   not cover the planned use.
3. **Audit fallback:** decide whether a live public URL alone is sufficiently
   durable. Where publication is not permitted, define lawful controlled access
   to the exact text; exclude any source for which adequate access cannot be
   established under G13.
4. **Project/source-family boundaries:** approve whether donor programme,
   procurement template, related programme phase, and shared-author risks make
   documents one source family for sampling and reporting.
5. **Version and collection procedure:** approve how immutable document
   versions, hashes, provenance, removals/updates, and a future collection
   window will be recorded. In particular, pin the Prozorro commit rather than
   sampling a moving `master` page.
6. **Pilot authorization:** only after the preceding choices, approve a
   development-only G3 pilot plan. Pilot text and near-duplicates then become
   permanently development-visible and cannot enter the holdout.

This document does not close G1, G2, G3, G7, G13, issue #81, or the broader
validation work.
