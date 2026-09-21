# SRM-05B — Scalar Quantitative Research Decisions

**Issue:** #73  
**Research slice:** first bounded extension of scalar quantitative syntax  
**Document status:** `DRAFT_FOR_RESEARCHER_REVIEW`

This document is a research decision package. It inventories evidence, exposes
decision gates, and recommends a bounded next step. It does not approve a new
scientific rule, allocate a new Rule ID, define binding expected outputs, or
authorize implementation.

## 1. Purpose and audited baseline

The purpose of SRM-05B is to determine whether the currently available sources
justify one small extension to the approved scalar syntax. The task-supplied
baseline is `main` after merged PR #91, merge commit
`f90915f7a3f966f24ba7786136c312de38ede688`. No Git operation was performed in
this research slice.

The audit was limited to the requested material:

| Audited material | Use in this package |
| --- | --- |
| `model-spec.md` §7.14.5.1 | Preserves result-containment, judgeability, Evidence, diagnostics, and the non-judgeability of `до`. |
| `model-spec.md` §§7.14.6.1–7.14.6.6 | Defines the authoritative comparator, numeric, unit, linkage, precedence, negative, and first-production contracts. |
| `model-spec.md` §§7.6, 7.15.10, 7.15.12, and the `RQD-008` row in §18 | Defines the linked quantitative domain, representation constraints, and the open research boundary. |
| `srm-05-quantitative-research.md` §§3 and 5–9 | Supplies the audited baseline, research gaps, candidate cases, Slice 1 boundary, and decision gates. |
| `reference/2.2_Взаємозвязок_вимог_і_якості.docx`, directly cited passages in §2.2 | Confirms `95 % ... не довше ніж за 2 с` and `Час відгуку ≤ 2 с при 500 одночасних користувачах`. |
| `reference/3.2_Динамічні_методи.docx`, directly cited §3.2 passages | Confirms `не довше 2 с` and the semantic category “допустимий діапазон”; it supplies no literal range grammar. |
| `reference/Приклад_застосування_моделі.docx`, directly cited §2/Table 1 and §8/Table 7 passages | Confirms `не рідше ... 5 с`, `не більше 3 с`, `не більше ніж за 4 с`, `до 300`, `не нижче 99,9 %`, `2 хв`, `15 хв`, and the `TLS 1.3`/`OAuth 2.0` negatives. |
| `quantitative.py`, its domain model, and directly related test cases | Read-only confirmation of the documented baseline. Existing code is not treated as scientific authorization for any extension. |

The audit found no source contradiction that can be resolved inside this slice.
It did find an evidence limitation: the supplied sources demonstrate the
already approved scalar forms, but they do not supply a positive
natural-language requirement example for any candidate new comparator, a
decimal-point measured value, a signed/grouped/exponent value, or an additional
exact unit surface.

## 2. Existing approved scalar contract

The following contract is `EXISTING_APPROVED` and is the protected baseline.

| Area | Existing approved contract |
| --- | --- |
| Rule allocation | `QUANT-001` accepts symbolic `≤` plus an approved value, optionally with an approved unit, and the lower-precedence value + unit fallback. `QUANT-UK-001` accepts the six lexical surfaces `не довше ніж`, `не довше`, `не більше ніж`, `не більше`, `не нижче`, and `до`. |
| Comparator normalization | `≤`, `не довше ніж`, `не довше`, `не більше ніж`, and `не більше` map to `LESS_THAN_OR_EQUAL / INCLUSIVE`; `не нижче` maps to `GREATER_THAN_OR_EQUAL / INCLUSIVE`; `до` maps only to `UPPER_BOUND / UNRESOLVED`. |
| Numeric syntax | ASCII integers and one decimal comma between digits. Raw source is preserved before exact conversion to `Decimal`; no rounding or binary floating point is allowed. |
| Unit surfaces | `с`, `секунд` → `SECOND`; `хв`, `хвилин` → `MINUTE`; `%` → `PERCENT`. These are exact surfaces and labels, not an ontology. |
| Candidate precedence | Ukrainian lexical comparator candidate, then symbolic `≤`, then value + unit fallback. A contained fallback does not duplicate a higher-precedence anchor. |
| Deferred-frequency protection | The exact construction `не рідше одного разу на <approved value> <approved duration unit>` is protected from the fallback. Protection is not acceptance, rejection of its meaning, or written-number normalization. |
| Evidence | One contiguous original-source anchor, start-inclusive/end-exclusive Unicode code-point offsets, exact spelling and punctuation within the anchor, stable per-rule source-order IDs, and component refs whose de-duplicated union is the top-level refs. |
| Technical negatives | `TLS 1.3` and `OAuth 2.0` remain bounded technical-version negatives. This is not a general version or identifier ontology. |
| Acceptance interaction | `ACCEPT-QUANT-001` remains limited to accepted `RESULT-UK-001` Evidence containing a judgeable accepted anchor. `до` is not judgeable. Comparator-free accepted value + unit targets do not imply `=`. |
| Quality-model boundary | Quantitative observations and diagnostics do not by themselves create Findings, `QUALITY_PROBLEM`, applicability, confidence, severity, or a new C/V/U contribution. |

The current linked domain contains comparator labels
`LESS_THAN_OR_EQUAL`, `GREATER_THAN_OR_EQUAL`, `NOT_LESS_FREQUENT`, and
`UPPER_BOUND`; inclusivity states `INCLUSIVE` and `UNRESOLVED`; unit labels
`SECOND`, `MINUTE`, and `PERCENT`; and an exact `Decimal` value. Strict
comparators, equality, and exclusive inclusivity have no approved domain value.

## 3. Comparator decision matrix

“Candidate normalized meaning” below is a question for researcher review, not
an approved mapping. Source attestation means attestation as a requirement or
requirement-like bound in the supplied scientific sources; occurrence in a
formula or explanatory prose is not enough.

| Surface | Source-attested requirement example | Candidate normalized meaning | Boundary inclusivity | Restrictions that would be necessary | False-positive and Evidence concerns | Status and decision still required |
| --- | --- | --- | --- | --- | --- | --- |
| `≤` | Yes: `Час відгуку ≤ 2 с ...` | `LESS_THAN_OR_EQUAL` | `INCLUSIVE` | Existing approved numeric syntax; unit optional | Evidence starts at `≤` and ends after the linked value/unit | `EXISTING_APPROVED`; no decision in this slice |
| `не довше ніж`, `не довше` | Yes: duration requirements ending in `2 с` | `LESS_THAN_OR_EQUAL` | `INCLUSIVE` | Duration construction; approved optional `за` behavior only where specified | Whole-token lexical match; Evidence includes fixed grammatical material and value/unit | `EXISTING_APPROVED`; no decision in this slice |
| `не більше ніж`, `не більше` | Yes: `... не більше 3 с` and `... не більше ніж за 4 с` | `LESS_THAN_OR_EQUAL` | `INCLUSIVE` | Existing approved contiguous construction | Reject separated/inserted lexical material; preserve comparator precedence | `EXISTING_APPROVED`; no decision in this slice |
| `не нижче` | Yes: `не нижче 99,9 %` | `GREATER_THAN_OR_EQUAL` | `INCLUSIVE` | Existing approved contiguous construction | Percent semantics do not supply an unexpressed denominator | `EXISTING_APPROVED`; no decision in this slice |
| `до` | Yes: `до 300` in a load-context phrase | `UPPER_BOUND` only | `UNRESOLVED` | No metric or unit restriction is currently inferred | Direction is evidenced; endpoint inclusion is not. Evidence begins at `до` and ends after the linked value/unit if present | `EXISTING_APPROVED` for `UPPER_BOUND / UNRESOLVED`; any narrower interpretation is `PROPOSED_RESEARCH_DECISION` |
| `не рідше` | Yes, only in `не рідше одного разу на 5 с` | Domain label `NOT_LESS_FREQUENT`; numeric direction remains representation-dependent | Not an endpoint-inclusivity decision | Would require written-count and frequency-versus-interval decisions, both outside this slice | Fallback must remain suppressed inside the protected construction | `SOURCE_ATTESTED_NOT_ALLOCATED`; production extension is `DEFERRED` by this slice's mandatory boundary |
| `<` | No natural-language requirement example; corpus occurrence is outside this contract | Possible strict upper bound | Would require `EXCLUSIVE`, which is absent | A researcher must specify permitted metric/value/unit contexts | Formula, markup, arrows, and code-like text are major false positives; exact anchor boundary is undecided | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; mapping and domain extension require approval |
| `>` | No natural-language requirement example; corpus occurrence is outside this contract | Possible strict lower bound | Would require `EXCLUSIVE`, which is absent | A researcher must specify permitted metric/value/unit contexts | Formula, markup, and code-like text are major false positives; exact anchor boundary is undecided | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; mapping and domain extension require approval |
| `=` | No natural-language requirement example; corpus occurrence is outside this contract | Possible equality/target | Not representable by the current inclusivity contract | Equality, tolerance, measurement precision, and target semantics must be separated | Assignment, formula, key/value, and identifier text can look like equality | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; comparator/domain and tolerance decisions are required |
| `≥` | No natural-language requirement example; corpus occurrence is outside this contract | Possible `GREATER_THAN_OR_EQUAL` | Possible `INCLUSIVE`, but not approved for this surface | Researcher must approve the symbol as requirement syntax and its allowed anchor shape | Formula/model-checkpoint occurrence is not requirement evidence | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; mathematical symmetry with `≤` is not authorization |
| `не менше` | No occurrence in the supplied corpus | Possible `GREATER_THAN_OR_EQUAL` | Possible `INCLUSIVE`, but not approved | Metric-sensitive uses and exact token/whitespace policy must be bounded | General prose and count constructions may create false positives | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; source evidence and mapping approval are required |
| `не пізніше` | No occurrence in the supplied corpus | Possible upper temporal/deadline bound | Unresolved | Must distinguish duration, clock time, date/deadline, and event ordering | Without a time ontology it can attach to a date, event, or duration incorrectly | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; this is not ready for scalar allocation |
| `щонайменше` | Occurs only in explanatory prose, not as a requirement bound | Possible lower bound | Unresolved | Must identify allowed numeric construction and distinguish discourse use | Explanatory quantification can be mistaken for a requirement constraint | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; prose occurrence is insufficient |

No candidate row changes `ACCEPT-QUANT-001`. Even if a future surface is mapped
to an existing judgeable comparator label, its acceptance effect requires an
explicit acceptance gate; it cannot be inherited accidentally from the label.

## 4. `до` inclusivity analysis

The source-attested construction `при навантаженні до 300 одночасних запитів`
establishes that `до` introduces an upper-directed bound. Neither the sentence
nor the cited dissertation discussion states whether the endpoint `300` is
included. It also does not define a general measurement convention from which
inclusivity can be derived. The sources therefore support the present
`UPPER_BOUND` label but no narrower endpoint decision.

| Alternative | Scientific support and consequence | Status |
| --- | --- | --- |
| Preserve `UPPER_BOUND / UNRESOLVED` for every currently accepted `до` anchor | Fully consistent with the authoritative model, the source evidence, the current domain invariant, and non-judgeability under `ACCEPT-QUANT-001` | `EXISTING_APPROVED` |
| Approve inclusive meaning only for the exact load construction `при навантаженні до <value> <population phrase>` | The construction itself is source-attested, but endpoint inclusion is not. It also depends on context/count/population roles expressly outside this slice | `PROPOSED_RESEARCH_DECISION`; not supported strongly enough for approval here |
| Approve inclusive meaning for duration or unit-bearing `до <value> <unit>` | No directly cited source example supplies this construction or its endpoint convention | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Defer all endpoint interpretation pending measurement-context research | Scientifically conservative, but it is not a new rule; it leaves the current observation and diagnostic behavior intact | `DEFERRED` as future research; current behavior remains `EXISTING_APPROVED` |

This package does not select a narrower interpretation. It preserves
`UPPER_BOUND / UNRESOLVED`, does not map `до` to `LESS_THAN_OR_EQUAL`, and does
not change `ACCEPT-QUANT-001` judgeability.

## 5. Numeric syntax decision matrix

| Numeric surface | Scientific-source support | Candidate normalization and boundary | False-positive controls and protected behavior | Domain sufficiency | Status and decision still required |
| --- | --- | --- | --- | --- | --- |
| ASCII integer | Positive measured/count examples: `2`, `3`, `4`, `15`, `300`, `500` | Existing exact base-10 `Decimal`; boundary is the contiguous ASCII digit run within an approved anchor | Version/identifier/formula/document-reference exclusions remain; standalone ambiguous digits remain diagnostic under the existing rule | Existing `NumericValueComponent` suffices | `EXISTING_APPROVED` |
| One decimal comma | Positive measured example `99,9 %` | Preserve raw `99,9`; normalize exactly to `Decimal("99.9")`; comma between digits belongs to the number | Multiple commas, ranges, and grouping are not admitted | Existing domain suffices | `EXISTING_APPROVED` |
| Decimal-point measured value | No positive measured-value example. `1.3` and `2.0` occur only in `TLS 1.3` and `OAuth 2.0` | A possible candidate would span one digit run, one `.`, and a following digit run only inside an otherwise approved anchor | The two technical-version negatives must remain excluded; a bounded rule must not become general number parsing | Exact `Decimal` could represent the value, but detector disambiguation and scientific authorization are missing | `UNSUPPORTED_BY_AVAILABLE_SOURCES`; a positive requirement example and exact version/identifier boundary are required |
| Signed value | No source support | Sign ownership, whitespace, unary/binary meaning, and whether the sign belongs to Evidence are undecided | Hyphens, dashes, list markers, ranges, subtraction, and identifiers are false-positive risks | `Decimal` can represent a sign, but syntax and semantics are unapproved | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Digit grouping | No source support | Group separator, grouping width, locale, and raw-to-`Decimal` normalization are undecided | Spaces may separate tokens or populations; comma already has decimal meaning; punctuation may be formatting | Domain could hold the normalized magnitude, but parsing policy is absent | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Exponent notation | No source support | Mantissa, exponent marker, sign, exponent bounds, and normalization are undecided | Identifiers, versions, scientific prose, and codes can resemble exponent syntax | `Decimal` could represent a value, but accepted surface and safety limits are absent | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| `TLS 1.3`, `OAuth 2.0` | Source-attested as technical versions | No quantitative value normalization | Preserve as exact bounded negatives; do not generalize to an identifier ontology | No observation is required for these numeric strings | `EXISTING_APPROVED` protected negative behavior |

No general number parser is justified. In particular, representability by
`Decimal` is not evidence that a source surface is approved.

## 6. Unit surface decision matrix

| Surface or candidate | Source/authority basis | Spelling or inflection | Normalized unit label | Conversion or dimensional consequence | Status |
| --- | --- | --- | --- | --- | --- |
| `с` | Source-attested in duration requirements | Exact abbreviation only | `SECOND` | No conversion; duration use does not create a general time ontology | `EXISTING_APPROVED` |
| `секунд` | Authoritative operational example in `model-spec.md` §7.6; not dissertation-corpus attestation | Exact inflected surface only | `SECOND` | No alias generation or conversion | `EXISTING_APPROVED` |
| `хв` | Source-attested in §8/Table 7 examples | Exact abbreviation only | `MINUTE` | No conversion to seconds | `EXISTING_APPROVED` |
| `хвилин` | Source-attested in the application material and already allocated | Exact inflected surface only | `MINUTE` | No conversion to seconds | `EXISTING_APPROVED` |
| `%` | Source-attested with `95 %` and `99,9 %` | Exact symbol; approved adjacent or source-supported spaced form | `PERCENT` | No inferred denominator, population, fraction scaling, or percentile meaning | `EXISTING_APPROVED` |
| Other second inflections such as `секунда`, `секунди` | No directly relevant source-attested bounded requirement example in the audited material | Would be new exact spellings, not automatic aliases | Mapping to `SECOND` would itself need approval | Must not imply conversion or inflection generation | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Other minute inflections such as `хвилина`, `хвилини`, `хвилинами` | No directly relevant source-attested bounded requirement example in the audited material | Would be new exact spellings, not automatic aliases | Mapping to `MINUTE` would itself need approval | Must not imply conversion or inflection generation | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| New abbreviations or dimensions such as milliseconds, hours, bytes, or rates | No directly relevant source support in this slice | New surface vocabulary | May require a new `UnitLabel`, not an alias | Would raise dimensional, compound-unit, and possibly conversion questions | `UNSUPPORTED_BY_AVAILABLE_SOURCES` and outside a safe first extension |

The four requested duration surfaces and `%` are therefore an inventory of the
complete approved unit-surface set for this slice. A new spelling is distinct
from a new normalized label; both are distinct from conversion and from
dimensional interpretation. None may be inferred from another.

## 7. Evidence and uncertainty consequences

The following matrix states the minimum questions a future proposal must close.
It does not define binding behavior.

| Proposed extension family | Candidate start/end boundary | Original-source Evidence requirement | Exact negatives to protect | Unresolved candidate class | Precedence interaction | Existing fields / Rule-ID consequence | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| New symbolic comparator `<`, `>`, `=`, or `≥` | Start at the comparator symbol; end after the contiguous approved value and optional approved unit; outside whitespace and sentence-final punctuation excluded | Exact original symbol/value/unit span with source offsets; no normalized text substituted | Formula, model checkpoint, state transition, markup, code-like assignment, `TLS 1.3`, `OAuth 2.0` | Symbol adjacent to digits where requirement-bound role cannot be established | Must occupy symbolic-comparator stage above fallback; overlap policy with existing `≤` must be explicit | `≥` might fit existing `GREATER_THAN_OR_EQUAL`; strict/equality forms need new comparator/inclusivity representation. Reuse or new Rule ID requires researcher approval | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| New lexical comparator `не менше`, `не пізніше`, or `щонайменше` | Start at the first complete lexical token; end after only approved fixed material plus linked value/unit | Exact original spelling, Unicode form, whitespace, and offsets; matching-view indices cannot become Evidence offsets | Explanatory prose, unrelated negation, separated words, date/event wording, and longer joined words | Compatible words and value occur but the governed quantity or construction is ambiguous | Must precede symbolic and fallback candidates; longest/overlap behavior against existing `не ...` forms must be specified | `не менше` might reuse a label only after approval; `не пізніше` may require new semantics. Rule ID is not allocated | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Narrower `до` inclusivity | Existing Evidence remains from `до` through linked value/unit; no context phrase may be absorbed without a separate context rule | Existing `QUANT-UK-001` source round-trip must remain intact | Joined-word cases, separated candidates, and load-context quantities outside eligible result Evidence | Every `до` case whose endpoint convention is not explicitly governed | Existing lexical precedence remains first; fallback stays suppressed inside the accepted anchor | Current domain forces `UPPER_BOUND / UNRESOLVED`; any inclusive/exclusive change requires a domain/model decision and likely a Rule-ID/acceptance review | `PROPOSED_RESEARCH_DECISION`; evidence is insufficient |
| Decimal-point measured value | Numeric subspan would start at the first mantissa digit and end after the final fractional digit; enclosing Evidence would retain the full approved comparator/value/unit or value/unit anchor | Preserve raw decimal point and the complete anchor; exact conversion only after Evidence creation | Exact `TLS 1.3` and `OAuth 2.0` negatives, plus identifiers/versions governed by any newly approved bounded rule | Point-number inside a plausible anchor whose version/identifier role cannot be resolved | Must participate in existing comparator-first/fallback-last precedence without making version strings fallback values | Existing numeric component suffices; detector and possible Rule-ID reuse need approval | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Signed value | Boundary ownership must explicitly include or exclude the sign and any intervening whitespace | Raw sign/value and full anchor; Unicode minus versus hyphen policy must be stated | Lists, subtraction, ranges, dashes, identifiers | Sign-like punctuation with ambiguous unary meaning | Must not be decomposed into an unsigned fallback | `Decimal` suffices only after syntax approval; Rule ID undecided | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Digit-grouped value | Boundary must include every approved group separator and digit group | Exact grouped source plus full anchor; normalization must be lossless and documented | Ordinary token spaces, decimal comma, lists, multiple independent counts | Separator pattern that could be token spacing rather than grouping | Must be recognized before separate numeric candidates or fallback duplication | Numeric component may suffice; parser policy and Rule ID undecided | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Exponent value | Boundary must include approved mantissa, exponent marker, and exponent sign/digits | Exact exponent source plus full anchor; no binary-float intermediary | Identifiers, version strings, symbolic formulas | Exponent-like text without an approved measurement relation | Must be protected from partial mantissa/exponent fallback matches | Numeric component may suffice; syntax limits and Rule ID undecided | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| Additional exact unit surface mapped to an existing label | Start at value for fallback Evidence or at comparator for comparator Evidence; end after the exact unit token | Preserve the exact unit spelling; normalized label never replaces it | Longer joined words, derived adjectives, unapproved inflections, and count/population nouns | Unit-like token whose dimension or grammatical role is unclear | Existing comparator anchors remain above fallback; unit expansion must not create a duplicate fallback | Existing `UnitLabel` may suffice only after explicit mapping approval; Rule ID reuse is a researcher decision | `UNSUPPORTED_BY_AVAILABLE_SOURCES` |
| New unit label or dimensional form | Same anchor boundary only after the exact unit grammar is approved | Raw source and component refs must remain exact | Compound units, rates, prefixes, and implicit conversions | Any surface with uncertain dimension or compound structure | Precedence cannot solve dimensional ambiguity | Requires a domain decision and potentially a new Rule ID; no label is allocated here | `DEFERRED` |

For every future extension, unresolved processing remains separate from accepted
Evidence. A diagnostic span is not Evidence and cannot create an observation,
Finding, applicability value, or score. Accepted plus unresolved candidates
must continue to preserve mixed state rather than discarding uncertainty.

## 8. Illustrative positive/negative/unresolved cases

Every case below is `ILLUSTRATIVE_NOT_APPROVED`. These are research prompts,
not tests, implementation authorization, or binding expected outputs.

| Kind | Candidate text | Research use |
| --- | --- | --- |
| `ILLUSTRATIVE_NOT_APPROVED` — possible `≥` positive | `Доступність має бути ≥ 99,9 %.` | Ask whether `≥` is admitted as a requirement comparator and whether its current label would make it judgeable. |
| `ILLUSTRATIVE_NOT_APPROVED` — symbolic negative | `Перехід стану A > B описано в моделі.` | Require a rule that does not treat a formula/model statement as a requirement bound merely because it contains `>`. |
| `ILLUSTRATIVE_NOT_APPROVED` — symbolic unresolved | `Профіль ≥ 3 активний.` | Determine whether the symbol/value is a bound, label, or formula before Evidence can be accepted. |
| `ILLUSTRATIVE_NOT_APPROVED` — lexical possible positive | `Кількість успішних спроб має бути не менше 3.` | Ask for source support, exact mapping, and whether a unitless comparator/value anchor is in scope. |
| `ILLUSTRATIVE_NOT_APPROVED` — lexical negative | `Документ пояснює щонайменше три підходи.` | Prevent explanatory prose from becoming a requirement constraint. |
| `ILLUSTRATIVE_NOT_APPROVED` — deadline unresolved | `Звіт має бути готовий не пізніше 10.` | Require a decision among clock time, date, duration, label, or invalid/incomplete value. |
| `ILLUSTRATIVE_NOT_APPROVED` — `до` preserved | `Система повинна відповісти до 2 с.` | Preserve an upper-bound observation with unresolved inclusivity and no new acceptance authorization. |
| `ILLUSTRATIVE_NOT_APPROVED` — `до` context ambiguity | `Система працює при навантаженні до 300 запитів.` | Ask whether the quantity is context, a constraint, or both; do not use it to settle endpoint inclusivity. |
| `ILLUSTRATIVE_NOT_APPROVED` — decimal-point possible positive | `Час відповіді має бути не більше 1.5 с.` | Ask whether one narrowly bounded measured decimal-point form can be separated from version identifiers. |
| `ILLUSTRATIVE_NOT_APPROVED` — decimal-point negative | `Система підтримує TLS 1.3.` | Preserve the existing technical-version negative. |
| `ILLUSTRATIVE_NOT_APPROVED` — decimal-point unresolved | `Профіль 1.5 має бути активний.` | Require role disambiguation; do not accept a general decimal parser. |
| `ILLUSTRATIVE_NOT_APPROVED` — signed possible positive | `Температура має бути не нижче -5.` | Ask whether signs, a temperature metric, and a missing unit can be handled without expanding metric/unit scope. |
| `ILLUSTRATIVE_NOT_APPROVED` — signed negative | `Пункт -5 описує виняток.` | Protect list/reference-like uses. |
| `ILLUSTRATIVE_NOT_APPROVED` — grouped unresolved | `Ліміт має бути не більше 1 000.` | Decide whether the space is grouping and which locale/group widths are permitted. |
| `ILLUSTRATIVE_NOT_APPROVED` — exponent unresolved | `Похибка має бути не більше 1e-3.` | Decide whether exponent notation is admissible and what exact normalization and Evidence apply. |
| `ILLUSTRATIVE_NOT_APPROVED` — new inflection possible positive | `Операція має завершитися за 1 секунду.` | Ask whether the exact new surface maps to `SECOND`; do not infer an inflection family. |
| `ILLUSTRATIVE_NOT_APPROVED` — unit negative | `Секундний таймер активовано.` | Prevent a derived adjective from matching an exact unit token. |
| `ILLUSTRATIVE_NOT_APPROVED` — unit unresolved | `Значення має бути 10 м.` | Require a dimension decision; do not guess minute, metre, or another unit. |

## 9. Explicit researcher decision gates

No extension may proceed until the researcher explicitly records all applicable
answers in the authoritative model specification:

1. **Candidate selection:** approve one exact surface construction, or approve
   `NO_EXTENSION_READY` pending new evidence.
2. **Source gate:** identify a positive requirement or requirement-like source
   example and explain why it supports the proposed surface and semantics.
3. **Syntax gate:** define exact characters/tokens, Unicode and whitespace
   policy, punctuation, start/end boundaries, and hard exclusions.
4. **Semantic gate:** define the normalized comparator/value/unit meaning,
   inclusivity, and any restrictions without relying on similarity to an
   existing form.
5. **Negative gate:** approve exact deterministic negatives, including the
   continuing protection of `TLS 1.3` and `OAuth 2.0` where relevant.
6. **Uncertainty gate:** distinguish determinate exclusion from an unresolved
   candidate and define diagnostic code/span and mixed-state behavior.
7. **Precedence gate:** state how the new candidate interacts with Ukrainian
   lexical candidates, symbolic candidates, value + unit fallback, the
   protected deferred-frequency construction, and overlaps.
8. **Representation gate:** confirm that existing comparator, inclusivity,
   numeric, and unit fields suffice, or separately approve the smallest domain
   addition.
9. **Evidence gate:** define exact original-source Evidence, component refs,
   top-level refs, ID ordering, and source round-trip.
10. **Acceptance gate:** explicitly decide whether the new observation is
    judgeable. Do not change `ACCEPT-QUANT-001` or inherit judgeability merely
    because a normalized label is already judgeable.
11. **Rule-ID gate:** decide whether unchanged semantics and Evidence permit an
    existing ID or whether a new ID is necessary. This package allocates none.
12. **Quality-model gate:** separately authorize any Finding,
    `QUALITY_PROBLEM`, applicability, or C/V/U effect. This package proposes
    none.

## 10. Proposed smallest implementable first slice

**Recommendation: `NO_EXTENSION_READY`.**

No candidate new scalar surface has both (a) a positive requirement example in
the available scientific sources and (b) sufficiently specified semantics,
boundaries, negatives, and uncertainty behavior:

- the new comparator candidates lack source-attested requirement bounds;
- a narrower `до` interpretation lacks endpoint-inclusivity evidence and the
  only candidate restriction depends on excluded context/count roles;
- decimal-point measured values lack a positive measured example, while the
  available point-number examples are protected versions;
- signed, grouped, and exponent values lack source support;
- no additional exact unit surface is justified by the audited passages; and
- the one source-attested but unallocated comparator, `не рідше`, depends on
  written-out-number and frequency grammar expressly excluded from SRM-05B.

`NO_EXTENSION_READY` is separable from metric, context, range, and acceptance
work because it changes none of them. It preserves the existing scalar anchor
set while the researcher obtains or selects positive evidence for one future
bounded construction. A later proposal can remain scalar-only if it uses an
already expressible comparator/value/unit shape, defines its own exact lexical
boundary and negatives, and leaves metric/context/range attachment and
acceptance judgeability unchanged unless separately approved.

## 11. Open questions and blockers

The exact blockers to implementation are:

1. No researcher-selected extension candidate exists.
2. No positive scientific-source requirement example supports any proposed new
   comparator, measured decimal-point syntax, signed/grouped/exponent syntax,
   or exact unit surface.
3. `до` endpoint inclusivity remains scientifically unresolved; the sole
   source-attested load construction cannot settle it.
4. Strict comparators and equality lack approved comparator labels and, for
   strict bounds, an `EXCLUSIVE` domain state.
5. Equality would additionally require a tolerance/precision decision that is
   absent and must not be inferred.
6. Decimal-point acceptance lacks an approved bounded distinction from
   versions and identifiers beyond the two exact protected negatives.
7. New unit spellings lack an approved exact-surface-to-label mapping; new
   dimensions would require a separate domain decision.
8. No decision states whether any new form would be judgeable under
   `ACCEPT-QUANT-001`; current `до` non-judgeability must remain unchanged.
9. Exact diagnostic treatment for each unsupported-but-plausible candidate is
   not approved.
10. Existing Rule IDs may not be reused, and a new Rule ID may not be
    allocated, until semantics and Evidence boundaries are approved.

Metric identification/attachment, context and population roles, nested or
compound constraints, generic ranges, written-out numbers, frequency grammar,
broader acceptance criteria, new C/V/U calculations, `QUALITY_PROBLEM`
inference, and parser/dependency upgrades remain outside this slice. P21 remains
only an approved composition regression and supplies no permission to widen the
acceptance grammar.

## 12. Final status

**Final status: `DRAFT_FOR_RESEARCHER_REVIEW`.**

Proposed decisions requiring researcher approval are the selection of one
candidate surface, its source basis, normalized meaning, inclusivity, exact
syntax/Evidence boundary, negatives, unresolved behavior, precedence, domain
sufficiency, acceptance effect, and Rule-ID disposition.

The existing comparator, integer/decimal-comma, and five exact unit-surface
contracts are source-supported or authoritatively approved as documented.
`не рідше` is source-attested but not allocated and is deferred from this
slice. The candidate new comparators, measured decimal-point syntax, signed,
grouped, exponent syntax, and additional unit surfaces are unsupported by the
available sources for production extension.

The `до` decision remains unresolved: retain `UPPER_BOUND / UNRESOLVED`, do not
convert it to `<=`, and do not change `ACCEPT-QUANT-001` judgeability.

The recommended smallest next slice is `NO_EXTENSION_READY`. Implementation is
blocked until the researcher supplies or selects positive evidence for one
narrow candidate and closes the applicable gates above.
