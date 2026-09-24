# SRM-13 — G2 Source Policy Decision Record

- **Decision status:**
  `G2_POLICY_APPROVED / SOURCE_INVENTORY_PENDING / CORPUS_NOT_CREATED`
- **Researcher decision date:** 2026-09-24
- **Protocol:**
  [`srm-13-validation-protocol-proposal.md`](srm-13-validation-protocol-proposal.md)
- **Researcher policy decisions:**
  [`srm-13-researcher-decisions.md`](srm-13-researcher-decisions.md)
- **Source-feasibility review:**
  [`srm-13-source-feasibility.md`](srm-13-source-feasibility.md)
- **Issue:** [#81 — SRM-13](https://github.com/rKiselyk/requirements-quality-assessment/issues/81)

## 1. Approved G2 source policies

### G2.1 — Eligible document and requirement types

Selection is approved at the individual-requirement level from:

- software specifications and technical assignments;
- open-project implementation documentation; and
- mixed software/hardware technical assignments, limited to their eligible
  software-system requirements.

Hardware-only, procurement-administration, supplier-qualification,
installation-only, and purely organizational-service content is excluded.
Every selected requirement must preserve its original Ukrainian one-line text
without paraphrasing, joining lines, or reconstructing incomplete fragments.

### G2.2 — Source-specific rights standard

Every source requires a documented lawful basis assessed separately for:

- retention of exact source text;
- creation and retention of annotations;
- permitted publication; and
- access to the exact source text for independent audit.

A public URL alone does not establish permission for all four actions.
Unresolved permissions remain explicitly unresolved and cannot be treated as
approval. The previously approved G13 hybrid public/controlled-access policy
applies: publish what rights permit and provide an approved controlled-access
audit path for restricted exact text.

### G2.3 — Immutable audit copy

Every included source must have lawful access to an immutable audit copy. Its
record must identify the original URL, retrieval date, document version or
commit, hashes, provenance, and the permitted audit-access mechanism. A live
URL alone is insufficient.

If lawful and adequate access to the exact source text cannot be established,
the source is excluded from the independent corpus under G13.

### G2.4 — Project and source-family independence

The source model preserves this hierarchy:

```text
requirement -> document -> project -> source family
```

Documents are grouped into a source family only on documented grounds, such as
shared templates, authorship, contractors, programmes, reused specifications,
or related project phases. Common subject matter or public-sector affiliation
alone does not prove textual dependence. Uncertain relationships must remain
explicitly uncertain.

Source-family assessment does not replace G7. Exact, normalized, and approved
near-duplicate screening, prior-exposure controls, manual review, and recorded
flag dispositions remain separate mandatory leakage controls.

### G2.5 — Source versioning and collection

A versioned source register is required with:

- source and document IDs;
- original URL and provenance;
- project and source-family IDs;
- retrieval date and time;
- author-stated version or pinned commit, where available;
- original-file hash;
- extracted-text hash;
- text-extraction method and version;
- extraction or encoding issues;
- rights basis and audit-access mechanism; and
- append-only version history.

Earlier document versions must not be overwritten. Every included requirement
must reference its exact source version.

The collection window and eligibility rules require researcher approval before
the independent sample is formed. This decision sets no collection dates or
limits.

### G2.6 — Candidate review sequence

Staged source-specific feasibility and rights review is authorized in this
order:

1. First priority: Prozorro and the TAPAS sports-title specification.
2. Second priority: the UNHCR/MinReintegration platform, Suspilne archive, and
   Zhytomyr Safe City.

The currently identified Trembita pilot instructions are excluded from the
natural-core shortlist. If approved sources prove insufficient in quantity or
diversity, additional independent projects may be sought under the same
G2.1–G2.5 rules.

These priorities authorize further review only. They do not approve any
candidate for corpus inclusion and do not change the feasibility note's
`PROMISING`, `NEEDS_RIGHTS_REVIEW`, or `UNSUITABLE` classifications.

## 2. Authorization boundary

These decisions authorize source-specific feasibility, rights, provenance,
versioning, audit-access, and independence review; preparation of the pending
source register and rights/audit record; and later preparation of a separately
approved development-only G3 pilot plan.

They do not authorize collection or freezing of the independent corpus,
reference annotation, expected C/V/U values, system execution on candidate
holdout requirements, corpus sizes or quotas, holdout annotation, access to
holdout system output, or any claim that independent validation has begun or
succeeded.

G2 is **not fully closed**. Issues #81 and #68 remain open.

## 3. Pending evidence for final G2 approval

Final G2 closure still requires a researcher-approved, versioned source
inventory and source-specific evidence recording:

- the approved collection window and final eligibility procedure;
- exact document versions, provenance, retrieval timestamps, and hashes;
- lawful bases for exact-text retention, annotations, publication, and audit;
- permitted immutable-copy and public or controlled audit mechanisms;
- project and source-family assignments with documented grounds and
  uncertainties;
- source-specific confidentiality and exclusion dispositions; and
- the final inclusion or exclusion of every reviewed candidate.

Any source without lawful and adequate exact-text audit access must be
excluded. No feasibility classification supplies this missing approval.

## 4. Gate dependencies

- **G1:** the final intended-population and sampling-frame wording must be
  bounded by the source inventory that G2 eventually approves.
- **G3:** size, source balance, strata, quotas, and the natural-core/enriched
  composition remain pending until a separately approved development-only
  pilot; pilot cases and near-duplicates cannot enter the holdout.
- **G7:** the source hierarchy and family record support, but do not replace,
  the approved two-pass leakage screening and prior-exposure controls.
- **G13:** publication and controlled access follow the approved hybrid release
  policy; restricted exact text cannot be replaced by paraphrases for span
  evaluation, and a source lacking lawful adequate audit access is excluded.

This record approves G2 source policy only. It does not approve the pending G2,
G3, G7, or G13 artifacts or close any of those gates.
