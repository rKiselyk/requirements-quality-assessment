# SRM-05F — Quantitative Boundaries and Deferred Forms Research

**Issue:** #73 (`SRM-05`)  
**Document status:** `RESEARCH_ONLY / PROPOSED_FOR_RESEARCHER_REVIEW`  
**Decision effect:** none; this document inventories evidence and prepares
research questions only  
**Rule-ID effect:** none; no Rule ID or Evidence ID is allocated

## 1. Research objective

This document inventories quantitative constructions that are not completely
resolved by the current scalar, metric, context, and exact R3 contracts. It
separates:

- original-source evidence from the supplied DOCX corpus;
- authoritative examples and synthetic boundary cases in
  [`model-spec.md`](model-spec.md);
- already approved behavior from unapproved source semantics; and
- deterministic negatives from unresolved candidates and explicitly deferred
  grammar.

The purpose is to identify the smallest source-supported scientific question
that could be prepared for researcher approval after SRM-05E. This document
does not approve an expansion, select an implementation phase, change the
authoritative model, implement a rule, or allocate an identifier.

The disposition vocabulary is fixed as follows:

- `APPROVED_EXISTING`: approval follows from the current authoritative model,
  not merely from appearance in an original source;
- `SOURCE_ATTESTED_NOT_APPROVED`: the construction occurs in an original
  source, but the relevant positive grammar or relationship is not approved;
- `DEFERRED`: the model explicitly places the form outside the present grammar;
- `UNRESOLVED`: the form or candidate is recognized, but a required semantic
  decision remains open; and
- `DETERMINISTIC_NEGATIVE`: an approved negative rule accounts for the form
  without creating the proposed quantitative observation.

## 2. Authoritative baseline

The following statuses are authoritative and protected.

| Item | Current status | Consequence for this research |
| --- | --- | --- |
| `QUANT-001` / `QUANT-UK-001` | Existing approved and implemented scalar contracts | Preserve grammar, precedence, normalized comparator labels, Evidence boundaries, diagnostics, and fallback behavior. |
| `QUANT-METRIC-001` | `RESEARCHER_APPROVED / IMPLEMENTED_AND_ACCEPTED` | Preserve the exact response-time metric prefix and its enrichment of one existing symbolic scalar observation. |
| `QUANT-CONTEXT-001` | `RESEARCHER_APPROVED / IMPLEMENTED_AND_ACCEPTED` | Preserve exact C0, literal `500`, its context-only role, the one enriched observation, and the embedded-number diagnostic. |
| Exact bounded R3 | `RESEARCHER_APPROVED / NOT_IMPLEMENTED / RULE_ID_NOT_ALLOCATED` | Preserve the exact 160-code-point source contract and the separate relationship representation. Do not implement or allocate it here. |
| `RQD-008` | `PARTIALLY_APPROVED / OPEN` | Exact R3 implementation and all broader metric, context, count, written-number, frequency, range, and ambiguity grammar remain open. |
| SRM-05 issue #73 | `OPEN` | This research does not close it. |

The current scalar baseline accepts ASCII integers and one decimal comma
between digits. It accepts only the unit surfaces `с`, `хв`, `хвилин`,
`секунд`, and `%`, normalized to `SECOND`, `MINUTE`, and `PERCENT`. Numeric and
unit grammar approved for one rule is not automatically inherited by another
rule. In particular, C0 accepts the exact context count text `500`, and exact
R3 fixes `95`, `4`, and `300`; neither contract creates a variable numeric
slot.

Comparator normalization is unchanged:

- `≤`, `не довше ніж`, `не довше`, `не більше ніж`, and `не більше` map to
  `LESS_THAN_OR_EQUAL / INCLUSIVE` in their approved contracts;
- `не нижче` maps to `GREATER_THAN_OR_EQUAL / INCLUSIVE`;
- `до` maps to `UPPER_BOUND / UNRESOLVED` and must not be rewritten as `≤`;
- `NOT_LESS_FREQUENT` is an approved domain label, but no positive production
  grammar is allocated for `не рідше`; and
- `<`, `>`, `=`, and `≥` have no approved natural-language quantitative
  comparator mapping in the current contract.

The existing evidence-first representation remains unchanged. A scalar
observation may be valid without all five components. `None` without an entry
in `unresolved_components` means that the component was not expressed inside
the accepted anchor; `None` with an unresolved entry requires an independently
approved candidate-recognition rule. Exact R3 is a separate approved future
relationship record, not an extension of the scalar tuple.

## 3. Original-source inventory

### 3.1 Original sources inspected

The following repository DOCX files were inspected through their paragraph and
table structures. Their role is research evidence and traceability, not direct
implementation authority.

| Original source | Relevant location | Material verified |
| --- | --- | --- |
| [`reference/2.2_Взаємозвязок_вимог_і_якості.docx`](reference/2.2_Взаємозвязок_вимог_і_якості.docx) | §2.2 paragraph containing the `95 %` example; Table 2.4 performance row; Table 2.5 semantic row | Percent-of-requests duration target; exact symbolic response-time and load-context example; distinction between numeric thresholds, load conditions, and units. |
| [`reference/2.3_Система_метрик.docx`](reference/2.3_Система_метрик.docx) | §2.3 paragraph beginning `Друга група метрик...` | A useful quality requirement contains an observable quantity, unit, measurement conditions, and admissible limit. |
| [`reference/3.2_Динамічні_методи.docx`](reference/3.2_Динамічні_методи.docx) | §3.2 paragraph with `95 % ... не довше 2 с`; Table 3.4 | A distributional percent-of-requests example; `допустимий діапазон` as a criterion category, not literal range syntax. |
| [`reference/Приклад_застосування_моделі.docx`](reference/Приклад_застосування_моделі.docx) | §2 initial specification, Table 1; §8, Table 7, rows `R1 → R1′` through `R6 → R6′` | Frequency, percentile, lexical bounds, decimal comma, load bound, value-plus-duration forms, conflicting values, and protected technical versions. |

The relevant source strings were checked against the original DOCX text. The
inventory below does not treat formulas, model coefficients, document section
numbers, dates, or bibliography data as requirement constraints merely because
they contain digits or mathematical symbols.

### 3.2 Source-backed construction inventory

The inventory is split into two linked tables to keep all required fields
readable. Table 1 records wording, provenance, and quantitative components.
Table 2 records Evidence and decision status. `SOURCE_ATTESTED` means present
in an original DOCX. `MODEL_SPEC_EXAMPLE` and `SYNTHETIC_TEST_CASE` are not
original-source evidence.

#### Table 1 — wording, provenance, and present interpretation

| ID | Exact wording | Source location | Provenance | Current approved behavior | Comparator and inclusivity | Numeric representation | Unit or dimension |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Q01 | `Час відгуку ≤ 2 с при 500 одночасних користувачах` | §2.2, Table 2.5, row `Семантичний (S)` | `SOURCE_ATTESTED` | Exact metric + symbolic scalar + C0 context enrichment is implemented and accepted. One quantitative observation is retained. | `≤` → `LESS_THAN_OR_EQUAL / INCLUSIVE`; bare `500` has no comparator. | `2` is an approved integer scalar; context count is the exact literal `500`, not a variable slot. | `с` → `SECOND`; `користувачах` is a population noun, not a unit. |
| Q02 | `95 % запитів мають оброблятися не довше ніж за 2 с` | §2.2, paragraph containing the semantic-content example | `SOURCE_ATTESTED` | Inner `95 %` value/unit and `не довше ніж за 2 с` scalar anchors are supported by the scalar baseline. The full proportion-to-duration relationship and its metric/context roles are not approved. | `не довше ніж` → `LESS_THAN_OR_EQUAL / INCLUSIVE` for the duration anchor. | Approved integers `95` and `2`; no denominator algorithm follows from `95`. | `%` → `PERCENT`; `с` → `SECOND`; `запитів` names a population, not a count unit. |
| Q03 | `95 % запитів мають завершуватися не довше 2 с` | §3.2, paragraph discussing repeated observations and distributional criteria | `SOURCE_ATTESTED` | Inner percent and duration anchors are within existing scalar forms. The complete distributional measurement procedure is not approved. | `не довше` → `LESS_THAN_OR_EQUAL / INCLUSIVE` for duration. | Approved integers `95` and `2`; no sampling or aggregation rule is created. | `%` → `PERCENT`; `с` → `SECOND`; request population remains lexical context. |
| Q04 | `не рідше одного разу на 5 с` within row `R1 → R1′` | Application example §8, Table 7, row `R1 → R1′` | `SOURCE_ATTESTED` | The entire construction is protected from value+unit fallback. It creates no quantitative Evidence, observation, or diagnostic under the first-production baseline. | Surface meaning label `NOT_LESS_FREQUENT` exists; numeric direction and positive grammar are not approved. Inclusivity is not a boundary decision. | `5` is an approved integer form in general, but `одного` is not parsed as numeric `1`. | `с` → `SECOND`; `разу` is a count noun, not an approved unit. |
| Q05 | `95-й перцентиль затримки від отримання GPS-події до відображення в UI — не більше 3 с` within row `R1 → R1′` | Application example §8, Table 7, row `R1 → R1′` | `SOURCE_ATTESTED` | `не більше 3 с` is an accepted scalar anchor. The percentile phrase is preserved as a metric qualifier in research, but no general percentile metric-link rule is approved. | `не більше` → `LESS_THAN_OR_EQUAL / INCLUSIVE`. | `3` is an approved integer scalar. `95-й` is an ordinal qualifier, not a `PERCENT` observation. | `с` → `SECOND`; percentile is not a unit conversion from `%`. |
| Q06 | `Після отримання події про перекриття дороги новий маршрут для 95 % запитів має бути сформований не більше ніж за 4 с при навантаженні до 300 одночасних запитів.` | Application example §8, Table 7, row `R2 → R2′` | `SOURCE_ATTESTED` | The three scalar observations are implemented; the exact five-role R3 relationship is researcher-approved but not implemented and has no Rule ID. | Duration: `LESS_THAN_OR_EQUAL / INCLUSIVE`. Load member: `UPPER_BOUND / UNRESOLVED`. | Exact integers `95`, `4`, and `300`; exact R3 does not generalize them. | `%` → `PERCENT`; `с` → `SECOND`; `одночасних запитів` is not a count unit. |
| Q07 | `до 300` inside Q06 | Same row as Q06 | `SOURCE_ATTESTED` | Accepted as a separate partial scalar and, in approved exact R3 science, referenced as the load-bound member without mutation. | `до` → `UPPER_BOUND / UNRESOLVED`; never `≤`. | Approved ASCII integer `300`. | No unit. The following count/population phrase is not promoted into a unit. |
| Q08 | `Місячна доступність сервісу — не нижче 99,9 %` within row `R4 → R4′` | Application example §8, Table 7, row `R4 → R4′` | `SOURCE_ATTESTED` | `не нижче 99,9 %` is an accepted scalar anchor. The leading availability phrase, monthly measurement window, exceptions, and SLA calculation are not covered by the exact metric-link rule. | `не нижче` → `GREATER_THAN_OR_EQUAL / INCLUSIVE`. | Approved single decimal comma `99,9`, parsed exactly as decimal `99.9` without rounding. | `%` → `PERCENT`; `Місячна` expresses a possible measurement window, not a unit. |
| Q09 | `Якщо GPS-провайдер не відповідає 15 с` and `після 2 хв формують alert` within row `R5 → R5′` | Application example §8, Table 7, row `R5 → R5′` | `SOURCE_ATTESTED` | `15 с` and `2 хв` are eligible value+unit fallback observations when not consumed by a higher-precedence comparator anchor. The surrounding temporal/condition relationships are not approved quantitative linkage grammar. | No approved comparator is expressed in either value+unit anchor. | Approved integers `15` and `2`. | `с` → `SECOND`; `хв` → `MINUTE`; no conversion between them. |
| Q10 | `У двох частинах документа задано різний час завершення неактивної сесії: 15 і 30 хвилин.` | Application example §2, Table 1, row `R6` | `SOURCE_ATTESTED` | `30 хвилин` fits value+unit fallback. The separate `15` forms no accepted anchor and is an unresolved numeric candidate under the scalar baseline. No approved coordination rule propagates `хвилин` backward, merges the values, or interprets a range. | No comparator. | Two approved integer surfaces occur, but shared-unit coordination is not approved. | `хвилин` → `MINUTE` only where explicitly adjacent; no implicit shared unit for `15`. |
| Q11 | `Встановити єдине значення timeout 15 хв ...; суперечливе значення 30 хв вилучити.` | Application example §8, Table 7, row `R6 → R6′` | `SOURCE_ATTESTED` | Each explicit value+unit phrase is independently eligible under scalar fallback. Conflict resolution and semantic roles of retained versus removed values are not quantitative linkage grammar. | No comparator. | Approved integers `15` and `30`. | Each `хв` → `MINUTE`; no conversion. |
| Q12 | `TLS 1.3` and `OAuth 2.0/OIDC` | Application example §8, Table 7, row `R3 → R3′` | `SOURCE_ATTESTED` | Protected technical-version handling creates no quantitative observation and no unresolved numeric diagnostic for `1.3` or `2.0`. | None. | Decimal-point forms are identifiers here, not measured values. | None. Protocol/version identity is not a dimension. |
| Q13 | `допустимий діапазон` | §3.2, Table 3.4, row `Критерій aᵢ` | `SOURCE_ATTESTED` | Establishes only a semantic category of acceptable criterion. It supplies no literal requirement range endpoints or syntax. | None supplied. | No numeric endpoints supplied. | No unit supplied. |
| Q14 | `не більше 2 секунд` | [`model-spec.md`](model-spec.md) §7.6 operational example | `MODEL_SPEC_EXAMPLE`, not original DOCX evidence | Approved operational scalar form under the existing lexical and unit baseline. | `не більше` → `LESS_THAN_OR_EQUAL / INCLUSIVE`. | Approved integer `2`. | `секунд` → `SECOND`; approval does not generate other inflections. |
| Q15 | `Система використовує профіль 95.` | [`model-spec.md`](model-spec.md) §7.14.6.5-.6 | `SYNTHETIC_TEST_CASE` | Produces no observation; emits `QUANT_UNRESOLVED_NUMERIC_CANDIDATE` over `95`; family processing is `INCOMPLETE`, derived outcome `UNRESOLVED`. | None. | ASCII integer candidate lacks an accepted comparator/value or value/unit relation. | None. |
| Q16 | `Час відгуку ≤ 2.5 с при 500 одночасних користувачах` | [`model-spec.md`](model-spec.md) §7.14.6.8 binding C0 cases | `SYNTHETIC_TEST_CASE` | No C0 match; preserve baseline behavior without inventing a new diagnostic. Decimal-point measured-value grammar is not approved. | The symbol itself is approved only when linked to an approved numeric value. | `2.5` is unsupported as a measured value. | `с` is approved, but does not make the unsupported number acceptable. |
| Q17 | Substitute `500,5`, `500.0`, `+500`, `1 000`, or `5e2` for C0's `500` | [`model-spec.md`](model-spec.md) §7.14.6.8 binding C0 cases | `SYNTHETIC_TEST_CASE` | No C0 match. The exact context rule does not inherit primary-scalar numeric syntax. General behavior beyond independently approved baseline rules is not asserted. | None for the context count. | Decimal comma, decimal point, sign, grouping, and exponent are all ineligible replacements for exact C0 `500`. | `користувачах` remains a population noun, not a unit. |

#### Table 2 — Evidence, unresolved behavior, and disposition

| ID | Evidence boundary, if established | Current partial or unresolved behavior | Remaining scientific decision | Recommended disposition |
| --- | --- | --- | --- | --- |
| Q01 | Metric `[0,11)`; scalar `[12,17)`; context `[18,49)`; embedded diagnostic candidate `[22,25)` | The accepted observation has metric, scalar, and context, but the preserved `500` diagnostic keeps quantitative processing `INCOMPLETE / DETECTED`. `500` is not accepted Evidence. | None for exact C0. Variable counts, alternate nouns, punctuation, and generic context grammar remain separate questions. | `APPROVED_EXISTING` |
| Q02 | Scalar Evidence boundaries exist for the inner percent and duration anchors; no approved Evidence span owns the full population-to-duration relationship. | The scalar observations do not encode which requests satisfy which bound or define a measurement procedure. | Whether an exact non-R3 population qualifier relationship is needed; its Evidence, cardinality, measurement boundary, and downstream non-use. | `SOURCE_ATTESTED_NOT_APPROVED` |
| Q03 | Scalar anchors may preserve `95 %` and `не довше 2 с`; no relationship Evidence is established. | The source explains distributional verification, but no sampling, denominator, repeated-run, or aggregation contract is approved for extraction. | Whether this explanatory example is eligible as requirement grammar at all, and if so whether it is exact-only. | `SOURCE_ATTESTED_NOT_APPROVED` |
| Q04 | The protected construction is matched as a whole for exclusion, but creates no accepted Evidence. The original table cell contains editorial prefix text before the refined requirement; a future accepted source boundary is not fixed here. | The nested `5 с` fallback and numeric diagnostic are suppressed. `одного` remains unparsed; frequency versus interval representation is unresolved. | Exact accepted boundary; fixed lexical treatment of `одного разу`; comparator/value/unit representation; metric linkage; status and Evidence ownership. | `DETERMINISTIC_NEGATIVE` for current scalar production; positive frequency grammar remains `DEFERRED`. |
| Q05 | Existing scalar boundary covers `не більше 3 с`; no approved percentile-metric Evidence boundary. | Scalar is accepted; percentile metric qualifier remains outside current metric grammar. | Whether any exact percentile metric link should be approved, without converting it to a percentage observation or adding a measurement algorithm. | `SOURCE_ATTESTED_NOT_APPROVED` for the full construction; scalar anchor is `APPROVED_EXISTING`. |
| Q06 | Existing scalars: `[62,66)`, `[96,116)`, `[134,140)`. Approved future R3 role Evidence: `[58,74)` and `[117,159)`, with final IDs and Rule ID unallocated. | `до 300` keeps member-local unresolved inclusivity. Exact R3 attachment is resolved scientifically but absent from production. | A separate implementation contract, final production representation names, and Rule/Evidence ID allocation outside issue #73. No broader grammar follows. | `APPROVED_EXISTING` scientific contract; explicitly `NOT_IMPLEMENTED`. |
| Q07 | Existing `QUANT-UK-001` scalar Evidence `[134,140)` only; it must not be enlarged to `[134,159)`. | Comparator inclusivity, count dimension, metric, context, and independent judgeability remain unresolved or absent. | No decision may convert the following noun phrase into a unit or resolve endpoint inclusion without new approval. | `APPROVED_EXISTING` partial observation with `UNRESOLVED` inclusivity. |
| Q08 | Accepted scalar Evidence is the exact `не нижче 99,9 %` anchor; no approved Evidence owns `Місячна доступність сервісу` or SLA procedure under quantitative linkage. | Scalar is complete for comparator/value/unit; metric, time window, exceptions, and calculation remain outside the accepted anchor. | Exact metric/context linkage, if desired, plus measurement and exception semantics; none can be inferred from `%`. | `SOURCE_ATTESTED_NOT_APPROVED` for the full construction; scalar anchor is `APPROVED_EXISTING`. |
| Q09 | Each explicit `15 с` or `2 хв` value+unit phrase can own its own scalar Evidence; no approved surrounding relationship boundary. | Accepted partial observations do not by themselves express timeout semantics, condition scope, escalation, or conversion. | Whether exact temporal roles merit a separate rule; metric/context and structural interaction would need explicit contracts. | `APPROVED_EXISTING` for the scalar phrases; broader relationships `DEFERRED`. |
| Q10 | `30 хвилин` supplies an explicit contiguous value+unit candidate. `15` is diagnostic-only and has no accepted Evidence; no approved boundary links it to the later unit. | The mixed result is one accepted fallback plus an unresolved numeric candidate, hence `INCOMPLETE / DETECTED`. `15` cannot silently inherit `MINUTE`; coordination and conflict semantics are not represented. | Whether shared-unit coordination is supported, how many observations it creates, and whether the phrase is a range, conflict, or two values. | `SOURCE_ATTESTED_NOT_APPROVED` |
| Q11 | Separate explicit `15 хв` and `30 хв` boundaries are available. | Two accepted scalar fallbacks do not encode that one is retained and the other removed. | No additional quantitative decision is required unless retained/removed semantic roles are to be modeled. | `APPROVED_EXISTING` for the two scalar phrases; action relationship `DEFERRED`. |
| Q12 | No quantitative Evidence for version numbers. | No unresolved diagnostic. This negative is specific to recognized technical versions, not a general identifier ontology. | Any broader technical-identifier grammar would require its own evidence and boundaries. | `DETERMINISTIC_NEGATIVE` |
| Q13 | No numeric range Evidence exists because the source supplies no endpoints or literal range syntax. | A meaningful range concept is source-attested, but no detector grammar can be derived from the category label. | Obtain actual source-attested endpoint syntax before proposing any range grammar, inclusivity, ordering, or representation. | `DEFERRED` |
| Q14 | One contiguous comparator/value/unit anchor under existing baseline rules. | No unresolved component is introduced merely because a metric or context is absent. | None for this exact operational example; no original-source status, inflection family, or alias expansion follows. | `APPROVED_EXISTING` |
| Q15 | Diagnostic span is exactly `95`; no accepted Evidence. | Candidate remains unresolved rather than negative or score zero. | A future identifier/profile negative would need a separately approved recognition rule. | `UNRESOLVED` |
| Q16 | No C0 Evidence; no new boundary is approved for `2.5`. | Exact downstream baseline behavior is preserved without inventing a decimal-point diagnostic policy. | Whether decimal point may ever denote a measured value, exact parsing rules, and collision handling with versions. | `DEFERRED` at numeric-grammar level; `DETERMINISTIC_NEGATIVE` for C0. |
| Q17 | No C0 context Evidence for any substitution. | The binding C0 negative does not establish general scalar or diagnostic outcomes for each unsupported form. | Separate scientific evidence for each representation, leading-zero/sign/grouping/exponent policy, and rule-specific eligibility. | `DEFERRED` at numeric-grammar level; `DETERMINISTIC_NEGATIVE` for C0. |

## 4. Comparator and inclusivity matrix

| Surface | Source status | Direction | Inclusivity | Current production status | Boundary that must remain explicit |
| --- | --- | --- | --- | --- | --- |
| `≤` | Original requirement example in §2.2 | Upper bound | `INCLUSIVE` | Approved in `QUANT-001` | Only this symbolic comparator is allocated; `<`, `>`, `=`, and `≥` do not inherit its mapping. |
| `не довше ніж` | Original §2.2 example and R2′ | Upper duration bound | `INCLUSIVE` | Approved in `QUANT-UK-001` | Exact contiguous lexical construction, including `за` where it belongs to the duration phrase. |
| `не довше` | Original §3.2 explanatory example | Upper duration bound | `INCLUSIVE` | Approved in `QUANT-UK-001` | No broader adjective/adverb synonym family follows. |
| `не більше` | Original R1′ | Upper bound | `INCLUSIVE` | Approved in `QUANT-UK-001` | Does not approve `більше`, other inflections, or omitted negation. |
| `не більше ніж` | Original R2′ | Upper bound | `INCLUSIVE` | Approved in `QUANT-UK-001` | Exact lexical order only. |
| `не нижче` | Original R4′ | Lower bound | `INCLUSIVE` | Approved in `QUANT-UK-001` | Does not authorize `≥` or other lower-bound phrases. |
| `не рідше` | Original R1′ frequency construction | Frequency relation; numeric direction depends on frequency versus interval representation | `None`, not a boundary-inclusion decision | Label exists; positive production grammar deferred and protected from fallback | Must not be reduced to `≤ 5 с`, `≥ 1`, or another scalar boundary without a scientific decision. |
| `до` | Original R2′ load construction | Upper-directed boundary | `UNRESOLVED` | Approved partial scalar in `QUANT-UK-001` | Must remain `UPPER_BOUND / UNRESOLVED`; no conversion to `LESS_THAN_OR_EQUAL`. |
| `<`, `>`, `=`, `≥` | Occur elsewhere in formulas or model checkpoints, not in supplied natural-language requirement bounds for this contract | Not assigned | Not assigned | Not approved as production comparators | Mathematical-document occurrence is not requirement-detector evidence. |
| `не менше`, `не пізніше` | Not found in the supplied corpus | Not assigned | Not assigned | Not approved | No vocabulary may be added by synonym analogy. |
| `щонайменше` | Explanatory prose only | Not assigned | Not assigned | Not approved | Prose occurrence is not a requirement-bound example. |

The matrix distinguishes comparator resolution from observation completeness.
The unresolved inclusivity of `до` is local to its comparator component and is
not a new processing status. Exact R3 can have a resolved relationship while
its `до 300` member remains `UPPER_BOUND / UNRESOLVED`.

## 5. Numeric representation

| Numeric form | Evidence classification | Current contract | Boundary decision still open |
| --- | --- | --- | --- |
| ASCII integer | Source-attested as `2`, `3`, `4`, `5`, `15`, `30`, `95`, `300`, and `500` | Approved in scalar anchors. Exact C0 and R3 retain their literal values and do not create variable slots. | Rule-specific admissibility, zero, leading zeros, and count roles cannot be inferred from scalar approval. |
| Single decimal comma | Source-attested as `99,9 %`; bounded generalized metric/C0 cases also use approved decimal-comma primary values | Approved as one comma between digits; preserve raw text; parse to exact `Decimal`; no rounding. | Population counts and other rules do not automatically inherit this grammar. |
| Decimal point | Source-attested only in protected versions `TLS 1.3` and `OAuth 2.0`; measured `2.5` is synthetic | Not approved as measured numeric syntax; recognized versions are deterministic negatives. | A future measured form needs collision rules separating values from versions and identifiers. |
| Grouped number | No source-attested requirement example; `1 000` is synthetic in the C0 boundary set | Not approved. | Separator repertoire, locale, grouping validation, Evidence boundary, and rule-specific eligibility. |
| Signed number | Negative coefficients occur in analytical calculations, not supplied requirement constraints; `+500` is synthetic in the C0 boundary set | Not approved for quantitative requirement anchors. | Sign semantics, Unicode minus versus hyphen, leading sign, and identifier collisions. |
| Scientific notation | No source-attested requirement example; `5e2` is synthetic in the C0 boundary set | Not approved. | Mantissa/exponent grammar, case, sign, units, and identifier collision. |
| Written-out number | Source-attested `одного` in Q04 | Explicitly outside the MVP scalar baseline; must not be parsed as numeric `1`. | Whether it remains fixed lexical material inside one exact frequency rule or becomes numeric data; general written-number grammar is not justified. |
| Ordinal | Source-attested `95-й` in Q05 | Preserved as a percentile metric qualifier; not a `PERCENT` quantitative observation. | Any exact percentile metric-link and measurement contract. No general ordinal grammar follows. |
| Technical version or identifier | Source-attested `TLS 1.3` and `OAuth 2.0/OIDC` | Deterministically excluded from quantitative observation and unresolved diagnostic in the approved examples. | A general identifier ontology is not approved. |
| Bare numeric candidate | Synthetic `профіль 95` and embedded C0 `500` demonstrate different contracts | Unresolved diagnostic unless an approved negative accounts for the token; C0 separately preserves its exact embedded-number diagnostic. | New negative categories or suppression rules require explicit approval. |

Approval of a representation in one row does not imply approval in another.
In particular, decimal comma is an approved scalar form but is a binding C0
negative when substituted for the exact population text `500`. Conversely,
decimal-point versions are deterministically excluded only under their approved
technical-version cases; that exclusion is not evidence for decimal-point
measurements.

## 6. Units and dimensions

### 6.1 Approved surfaces and labels

| Surface | Normalized label | Evidence basis | Current limitation |
| --- | --- | --- | --- |
| `с` | `SECOND` | Original §2.2 and application-example duration constructions | No generated plural, alias, or conversion. |
| `хв` | `MINUTE` | Application-example R5′ and R6′ | No conversion to seconds. |
| `хвилин` | `MINUTE` | Application-example initial R6 | No automatic propagation across coordination and no generated inflections. |
| `секунд` | `SECOND` | Authoritative model-spec §7.6 operational example; not original-corpus evidence | Approval is exact and does not relabel it as `SOURCE_ATTESTED`. |
| `%` | `PERCENT` | Original §2.2 and application-example constructions | A percent unit alone does not establish denominator, metric, percentile, window, or measurement algorithm. |

These labels are not a unit ontology. They provide no conversion relation,
dimensional algebra, alias generation, tolerance, or measurement procedure.

### 6.2 Source surfaces requiring new decisions

| Source surface | Why it is not an approved unit | Required scientific decision |
| --- | --- | --- |
| `користувачах` in exact C0 | It names the population inside an approved context; C0 expressly forbids an independent count observation or count unit. | Any count dimension outside exact C0, including variable cardinality and judgeability. |
| `запитів` / `одночасних запитів` | They name a request population and workload. Exact R3 preserves them in role Evidence but does not manufacture a unit. | Whether a future count dimension exists, its Evidence boundary, and whether it is context, metric, unit, or relationship content. |
| `разу` in Q04 | It is a written count noun inside a frequency construction. | Whether the phrase is fixed grammatical material or a count component; no general count-unit ontology is supported. |
| `95-й перцентиль` | It qualifies a latency metric, not the numeric unit `%`. | Exact percentile metric representation and measurement semantics, if pursued. |
| `Місячна` | It may express a measurement window for availability, not a scalar unit. | Window boundary, attachment, and calculation contract. |
| Compound or rate units | No source-approved compound-unit representation exists. | Do not infer requests/second, events/second, or reciprocal time from Q04 or Q06. |

## 7. Ranges and frequency

### 7.1 Ranges

No inspected original source supplies a literal requirement range with two
numeric endpoints. The source phrase `допустимий діапазон` in §3.2 Table 3.4
names a semantic category only. It does not establish:

- endpoint separators such as hyphen, dash, ellipsis, or words;
- open or closed endpoints;
- endpoint ordering;
- shared or repeated units;
- range Evidence boundaries;
- interaction with scalar observations; or
- invalid or reversed-range behavior.

`до 300` is one upper-directed bound, not a two-ended range. The coordinated
`15 і 30 хвилин` source is a conflict between two stated values, not approved
range syntax. Generic range grammar therefore remains `DEFERRED` pending an
actual source-attested construction.

### 7.2 Frequency

The exact source-attested frequency substring is:

```text
не рідше одного разу на 5 с
```

It appears inside the original R1′ table cell:

```text
Замість «у реальному часі»: координати активного транспортного засобу повинні оновлюватися не рідше одного разу на 5 с; 95-й перцентиль затримки від отримання GPS-події до відображення в UI — не більше 3 с.
```

The approved first-production contract deliberately recognizes the protected
shape
`не рідше одного разу на <approved numeric value> <approved duration unit>`
only to prevent a false `value + unit` fallback. For the original `5 с` phrase:

- no Evidence is emitted;
- no quantitative observation is emitted;
- no unresolved numeric-candidate diagnostic is emitted;
- processing remains `COMPLETE` and the derived outcome is `NOT_DETECTED` when
  no other scalar anchor exists;
- `одного` is not parsed as numeric `1`; and
- no frequency, interval, rate, or compliance meaning is calculated.

This is a deterministic first-production exclusion, not a conclusion that the
source is non-quantitative. A future positive decision must not silently turn
the protected exclusion into general written-number parsing or into a compound
unit such as events per second.

The source and model support a narrow future question, but not its answer. The
following points remain open:

1. whether positive recognition is limited to the exact `5 с` source or may
   reuse the protected variable-value/unit shape;
2. whether the accepted Evidence covers only the frequency substring or
   requires the governing update phrase;
3. whether `одного разу` is fixed lexical material or a represented count;
4. whether value `5` and unit `SECOND` represent a maximum interval while
   comparator label `NOT_LESS_FREQUENT` preserves the source direction;
5. whether a dedicated relationship is required to avoid conflating frequency
   with duration;
6. whether metric linkage to the update behavior is necessary; and
7. how the positive rule supersedes the exclusion without changing fallback,
   diagnostics, or unrelated observations.

## 8. Partial and negative cases

| Category | Representative case | Current behavior | Required preservation |
| --- | --- | --- | --- |
| Accepted complete observation | Exact C0 response-time observation after metric and context enrichment | Metric, comparator, value, unit, and context are populated on one observation. The separate embedded `500` diagnostic remains, so family processing is still `INCOMPLETE / DETECTED`. | Observation completeness must not suppress an independently required diagnostic. |
| Accepted scalar observation with no unresolved component | `не нижче 99,9 %`, `15 с`, or `2 хв` | Explicit anchor components are stored. Unexpressed metric/context/comparator fields remain `None` without automatically becoming unresolved. | Do not treat absent components as score zero or invent diagnostic entries. |
| Accepted partial observation | `до 300` | Comparator and value are accepted; inclusivity is `UNRESOLVED`; unit, metric, and context are absent. | Preserve the observation and member-local uncertainty; do not normalize to `≤`. |
| Unresolved numeric candidate | Synthetic `Система використовує профіль 95.` | No Evidence or observation; one diagnostic over `95`; `INCOMPLETE / UNRESOLVED`. | Do not convert the candidate to an observation merely because it contains digits. |
| Accepted observation plus unresolved candidate | Exact C0 | The response-time observation is accepted while `500` remains diagnostic-only. | Preserve mixed `INCOMPLETE / DETECTED`; do not suppress or promote `500`. |
| Deterministically excluded source form | `TLS 1.3`, `OAuth 2.0/OIDC` | No observation and no unresolved diagnostic for the protected version numbers. | Do not generalize this into an undocumented identifier ontology. |
| Deterministically excluded but meaningful source form | `не рідше одного разу на 5 с` | Protected span produces no fallback observation or diagnostic. | `NOT_DETECTED` means no accepted first-production anchor, not absence of quantitative meaning. |
| Unsupported but meaningful source construction | Full Q02/Q03 population-to-duration statements; percentile metric in Q05; shared-unit coordination in Q10 | Inner scalar anchors may be accepted, while the larger relationship remains unrepresented. | Do not claim full semantic approval from scalar success. |
| Explicitly deferred scientific grammar | Generic ranges, written numbers, decimal-point measurements, grouping, signs, scientific notation, count ontology, compound units | No general grammar is approved. Exact-rule negatives may coexist with this broader deferral. | Do not invent aliases, conversions, tolerances, measurement procedures, or diagnostics. |

No row changes diagnostics, processing status, fallback, acceptance,
characteristic calculations, Findings, reporting, or aggregation.

## 9. F0 F1 F2 comparison

These are research candidates, not approved phases.

| Option | Scientific evidence | Missing decisions | Required representation | Evidence implications | Negative cases | Backward-compatibility risks | Approval readiness |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **F0 — preserve the current baseline and explicitly defer unsupported expansions** | Complete authoritative scalar, metric, C0, and exact R3 contracts; original sources establish additional meaningful constructions without supplying complete grammar. | No new positive semantics. The researcher would only confirm that unapproved forms remain deferred. | None. Keep current scalar tuple and approved future exact R3 record unchanged. | No new Evidence or IDs. Preserve current accepted Evidence, diagnostics, exclusions, and exact R3 unallocated spans. | All existing deterministic negatives remain. Source-attested but unapproved constructions remain unrepresented rather than reclassified as meaningless. | Lowest risk. Main cost is deliberate semantic under-coverage, especially frequency, percentile metric linkage, shared-unit coordination, and the non-R3 percent-of-requests example. | `READY_FOR_RESEARCHER_REVIEW` as a conservative deferral. |
| **F1 — approve one exact source-attested construction without general grammar** | The strongest minimum candidate is exact `не рідше одного разу на 5 с`: it is original-source text, already protected as a whole, uses approved integer `5` and unit `с`, and has an existing normalized label `NOT_LESS_FREQUENT`. | Exact input boundary; fixed versus represented role of `одного разу`; interval/frequency semantics; scalar versus relationship representation; metric linkage; Evidence owner; exact positive and non-match behavior; effect on the existing exclusion. | Potentially one exact bounded observation or relationship. It must not require general written-number parsing, a count-unit ontology, or a reusable frequency grammar. | Would require a new approved Evidence boundary and later a separately allocated Rule ID. Existing protected-exclusion behavior must remain for every non-exact case. | Versions, percentile wording, changed count word, changed value/unit, punctuation/spacing variants, multiple frequencies, and hard-boundary splits need explicit exact non-match treatment. | Risk of accidentally accepting nested `5 с` as an ordinary duration, parsing `одного` as `1`, reversing comparator direction, or changing diagnostic/fallback precedence. | `PREPARABLE`, but not approval-ready until the listed semantic and Evidence questions are answered. No F1 approval is recorded here. |
| **F2 — approve a bounded family only if a common contract is supported** | The protected shape already distinguishes `не рідше одного разу на <approved value> <approved duration unit>` from fallback, and the scalar registry has approved numeric/unit surfaces. Only `5 с` is original-source-attested in this frequency role. | Whether scalar numeric and unit variants are scientifically valid frequency substitutions; zero/decimal values; all four duration-unit surfaces; meaning of `одного`; rate versus maximum interval; metric attachment; ambiguity; multiple occurrences; morphology and boundaries. | A bounded frequency family may require a dedicated relation rather than the one-value scalar shape. The protected exclusion pattern alone does not prove representational sufficiency. | Family-level Evidence and precedence would need a complete contract. No current Rule ID may be broadened silently. | Every value/unit combination not directly sourced, altered lexical token, inflection, count other than fixed `одного`, compound unit, and competing attachment must be classified. | Highest broadening risk. It may incorrectly inherit decimal-comma and duration units from scalar grammar, create observations formerly suppressed by the protected exclusion, or imply a count/rate ontology. | `NOT_READY`. One source construction does not establish a common positive family contract. |

F0 is the only option that can be reviewed without resolving new semantics. F1
is the smallest plausible expansion question. F2 lacks sufficient evidence for
a family-level positive contract. This comparison does not select or approve
any option.

## 10. Smallest next scientific decision

The smallest source-supported expansion question that can be prepared next is:

> Should only the exact source-attested construction `не рідше одного разу на
> 5 с` receive a positive quantitative representation, while `одного разу`
> remains fixed lexical material rather than general numeric or count-unit
> grammar, and while every current scalar fallback, diagnostic, and negative
> remains unchanged outside that exact construction?

This is an F1-sized question, not an F1 recommendation or approval. It is
smaller than a percentile-metric decision, a second population-to-duration
relationship, shared-unit coordination, or range grammar because:

- the exact source phrase exists;
- the current model already protects its complete lexical shape;
- the numeric `5`, duration surface `с`, and label `NOT_LESS_FREQUENT` already
  exist independently in the authoritative model; and
- a future rule can be explicitly prohibited from parsing `одного` as a
  general written-out number.

It is not yet approval-ready. A proposal must first answer the seven open
points in §7.2 and provide exact positive, negative, Evidence, precedence, and
representation contracts. In particular, the researcher must decide whether
the relationship can be represented without falsely claiming that “not less
frequently” is the same operator as an inclusive upper duration bound.

If the researcher does not want that additional representation in MVP v0.1,
the smallest complete decision is F0: explicitly defer all remaining forms
while retaining their source traceability.

## 11. Explicit exclusions and blockers

Nothing in this document authorizes:

- changing C0, exact R3, or any current scalar grammar;
- changing comparator normalization or resolving `до` inclusivity;
- changing Evidence ownership, source slicing, offsets, ordering, or identity;
- allocating R3's Rule ID, a frequency Rule ID, or any Evidence ID;
- implementing R3 or any F1/F2 candidate in issue #73;
- parsing `одного` as numeric `1`;
- interpreting frequency as a generic reciprocal-time or compound-unit value;
- adding `<`, `>`, `=`, `≥`, comparator synonyms, morphology, or aliases;
- accepting decimal-point measurements, grouped numbers, signed numbers,
  scientific notation, written-out numbers, or shared-unit coordination;
- deriving generic range syntax from `допустимий діапазон`;
- creating a count-unit ontology from `користувачах`, `запитів`, or `разу`;
- inferring unit conversions, tolerances, sampling, denominators, measurement
  windows, percentile algorithms, SLA calculations, or pass/fail procedures;
- modifying the existing `500` diagnostic, processing status, or fallback
  precedence;
- changing condition/result detection, including the exact R3 structural
  disposition B;
- changing `ACCEPT-QUANT-001`, C/V/U, Findings, `QUALITY_PROBLEM`, reporter, or
  aggregation behavior;
- changing [`model-spec.md`](model-spec.md) or prior research records;
- closing `RQD-008` or issue #73; or
- creating a baseline, tag, release, branch, commit, push, or pull request.

The principal blockers are scientific, not technical:

1. no literal two-ended range construction exists in the inspected sources;
2. one frequency example does not justify a family of value and unit variants;
3. the fixed written form `одного` has no approved numeric representation;
4. frequency and maximum interval are related but not interchangeable without
   an explicit representation decision;
5. source-attested population and count nouns are not approved units;
6. decimal-point measured values cannot be accepted without collision rules
   for protected technical versions;
7. shared-unit coordination has no approved observation-cardinality rule; and
8. no new ambiguity diagnostic or processing transition is approved for these
   constructions.

## 12. Researcher approval questions

### 12.1 Scope decision

1. Confirm F0 as an explicit deferral, or direct preparation of the exact F1
   frequency proposal?
2. If F1 is prepared, is the positive input the exact frequency substring, the
   refined requirement after the editorial `Замість ...:` prefix, or the entire
   original R1′ table-cell wording?
3. Must every punctuation, spacing, casing, and surrounding-text difference be
   a deterministic non-match, as in exact R3?

### 12.2 Frequency semantics and representation

4. May `одного разу` remain fixed lexical material without producing numeric
   value `1` or a count unit?
5. Does the represented numeric component remain value `5` with unit `SECOND`,
   while `NOT_LESS_FREQUENT` preserves the source frequency direction?
6. Would that representation falsely imply a scalar duration boundary, and if
   so is one dedicated exact relationship record required?
7. Is metric linkage to the coordinate-update behavior required, or may the
   exact frequency anchor remain a valid partial observation?
8. What exact Evidence span owns the positive construction, and does it replace
   only the current exclusion for that one exact source?
9. Must `inclusivity = None` remain binding for `NOT_LESS_FREQUENT`?

### 12.3 Status and negative behavior

10. For an exact F1 positive, should quantitative processing remain
    `COMPLETE / DETECTED` with no new diagnostic?
11. For every non-exact form, should the existing protected exclusion and
    baseline scalar behavior continue independently, without a new frequency
    diagnostic?
12. Which variations are deterministic negatives, and which are unresolved
    candidates, if any?

### 12.4 Boundaries beyond F1

13. Confirm that decimal-point measurements, grouped, signed, scientific, and
    written-out general numeric grammar remain deferred.
14. Confirm that no generic range grammar is supportable until a literal
    source-attested range is available.
15. Confirm that `користувачах`, `запитів`, and `разу` remain outside a count-unit
    ontology.
16. Confirm that F2 is not approval-ready from the current one-example
    frequency evidence.
17. Confirm that exact R3 remains approved but unimplemented, with no Rule ID,
    and that this next decision must not implement or broaden it.

Until those questions receive an explicit researcher decision, F1 remains a
prepared research direction only, F2 remains deferred, `RQD-008` remains
`PARTIALLY_APPROVED / OPEN`, and SRM-05 issue #73 remains `OPEN`.
