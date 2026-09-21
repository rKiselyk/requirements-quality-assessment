# SRM-03 — Extended structural feature detection rules

**Status: PROPOSED_PENDING_RESEARCHER_APPROVAL.** This is a scientific and
operational proposal for SRM-04, not an amendment to the approved MVP v0.1
contract. No rule or new example in this document is an executable or binding
test case until the researcher resolves the listed decisions and records the
approved rule in [model-spec.md](model-spec.md).

## 1. Purpose and scientific boundary

The target is **one Ukrainian-language sentence representing one requirement**.
Its clauses, conditions, actions, expected results, criteria and method phrases
remain inside one `Requirement`. The frozen reader continues to treat each
trimmed, non-empty UTF-8 input line as one requirement, even if the line has
several grammatical sentences. SRM-03 proposes no sentence rejection or
requirement splitting.

The scope is structural observations in the existing `condition_context`,
`expected_result`, `acceptance_criterion` and `verification_method` families,
plus the relationships needed to interpret several clauses in one requirement.
The existing `quantitative_constraint` and `vague_term_occurrence` families are
unchanged. Complex numeric grammar belongs to SRM-05/06; linguistic ambiguity
to SRM-07/08; type-specific applicability and characteristic calculations to
SRM-09/10/11. No new score, defect conversion, risk calculation, corrective
action or reassessment rule is proposed here.

Throughout this document, **source-supported principle** means that a cited
dissertation passage motivates the observation. **Proposed rule** means a
possible deterministic specialization of that principle; the dissertation
does not itself approve its Ukrainian grammar. **Unresolved** identifies a
decision that cannot be filled by parser output or implementation judgment.

## 2. Source traceability and existing MVP baseline

Sources were read in the requested order. [SRM-02](srm-02-individual-requirement-model.md)
is the current researcher-approved *local scope*, especially T01–T04, T07,
T13, G01 and `RQD-006`. [model-spec.md](model-spec.md) remains the authority
for *executable MVP behavior*, especially §§7.2–7.5, 7.7, 7.9, 7.11,
7.14.2–7.14.7, 7.15.6–7.15.8 and 7.16. The dissertation excerpts are
scientific context, not executable grammar:

| Local source | Relevant support and limit |
| --- | --- |
| [§2.1](reference/2.1_Властивості_вимог.docx), Table 2.1 (Completeness, Singularity, Verifiability rows), ¶11–12, Table 2.3 | A local requirement can need condition, expected reaction and fulfilment criterion; verifiability may use a criterion, oracle, analysis or inspection method. Independent obligations matter to singularity. The table does not define Ukrainian clause segmentation or a singularity detector. |
| [§2.3](reference/2.3_Система_метрик.docx), ¶4–6, Table 2.7, ¶17–21, ¶39–42 | Separates primary observations from measures and indicators; requires reproducibility, applicability and source context; permits nonnumeric operationalized results. It supplies no exact extended syntax, attachment algorithm or per-requirement score. |
| [§3.1](reference/3.1_Статичні_методи.docx), Table 3.1, ¶9–13, ¶32–34 | Supports static textual/structural analysis and traceable observations; external artifact or expert evidence is needed for some conclusions. Its set/product indicators and defect records are not local detector rules. |
| [§3.3](reference/3.3_Метод_оцінювання.docx), ¶10–11, ¶17–19, ¶30–36 | Supports source provenance, separate missingness and explainability; it does not supply Ukrainian grammar, local C/V/U formulas or a structural relation data type. |
| [§3.2](reference/3.2_Динамічні_методи.docx), ¶5–10, Table 3.4 | Used narrowly for the requirement → criterion → verification-procedure distinction. Test execution and product observations are outside this task. |
| [Worked application](reference/Приклад_застосування_моделі.docx), §8 Table 7, R5′ | Illustrates several condition/result clauses in one source requirement. Its illustrative text does not make inherited normative force or attachment executable. |

The local excerpts of Chapters 2–3 and the worked application are available.
The complete dissertation and Chapter 1 are not in `docs/reference/`, as
already recorded in SRM-02. The body of [Issue #71](https://github.com/rKiselyk/requirements-quality-assessment/issues/71)
could not be retrieved in this environment; the supplied SRM-03 request is the
issue scope used here. No claim below depends on unseen issue or dissertation
text.

**Existing approved MVP behavior (unchanged):** the six `RequirementFeatures`
collections are `condition_contexts`, `expected_results`,
`acceptance_criteria`, `quantitative_constraints`, `verification_methods`, and
`vague_term_occurrences`. `COND-UK-001` accepts its five exact marker surfaces
only in its leading/postposed templates. `RESULT-UK-001` accepts its five
normative surfaces only with the approved parser-assisted single-result grammar.
`ACCEPT-QUANT-001` composes an accepted result with contained, judgeable
`QUANT-001`/`QUANT-UK-001` Evidence. `VERIFY-UK-001` recognizes its three
specified verification-role constructions. These IDs retain their meanings;
none is renamed or widened here. The directly related detector modules and
tests are `condition_context.py`, `expected_result.py`,
`acceptance_criterion.py`, `verification_method.py` and their corresponding
`tests/test_*_detector.py` files. They confirm the narrow boundaries, including
mixed accepted/unresolved processing and source-offset round trips.

## 3. Structural gap inventory

| Area | Supported need | MVP boundary / decision missing |
| --- | --- | --- |
| A. Conditions and contexts | Several explicit conditions can govern one or several behaviors (§2.1 Table 2.1; worked R5′). | `COND-UK-001` does not resolve general internal/postposed subordinate clauses, nested or coordinated scope. No new marker inventory is justified here. |
| B. Expected results | Observable coordinated and nonmodal clauses occur in worked R5′; §2.1 requires an expected reaction. | `RESULT-UK-001` requires a supported modal and one determinate result scope. Inherited normative force and independent coordinated predicates are unresolved. |
| C. Nonnumeric criteria | §2.1 Table 2.1 and §3.2 Table 3.4 permit an expected behavior/oracle without a numeric threshold. | `ACCEPT-QUANT-001` only recognizes linked quantitative criteria; the exact test of nonnumeric judgeability is absent. |
| D. Verification methods | §2.1 Table 2.1 and §2.3 ¶17–21 distinguish reproducible methods from observable criteria. | `VERIFY-UK-001` has only three role constructions. Additional exact Ukrainian surface and role rules need approval; a method word is insufficient. |
| E. Multiple clauses | The six-family representation allows multiple observations; §2.1 singularity concerns independent obligations. | There is no approved rule to decide when coordinated material is one versus several observations or an independent-obligation finding. |
| F. Attachment | Conditions, criteria and methods need traceable targets (§2.1 Table 2.1; §3.2 ¶5–7). | MVP only has narrow condition anchor and quantitative Evidence containment. No general relation object or cross-clause attachment procedure is approved. |
| G. Actor/action/object | §2.1 describes expected behavior and possible independent actions. | Model-spec §7.11 explicitly defers `has_actor`, `has_action`, `has_object`. Parser annotations alone do not justify a new family. |

## 4. Proposed rule registry

All six IDs below are **provisional proposals, not allocated production IDs**.
The approved rule-ID policy in model-spec §7.7 applies only after approval: an
ID must have immutable meaning, versioned provenance and tests. The examples
in this registry are synthetic research examples unless expressly called
source-attested. Each proposed procedure is conditional on its listed missing
scientific decisions; it is not permission to fill those gaps in SRM-04.

Shared mechanics, if approved: operate within one original trimmed
`Requirement.text`; consume only source-aligned parser-neutral annotations
where specified; retain distinct observations in source order; use exact
zero-based Unicode code-point `[start_offset,end_offset)` spans; exclude
surrounding whitespace and sentence-final punctuation; retain punctuation
inside a semantic span only when needed; preserve accepted observations plus
unresolved candidates as `INCOMPLETE / DETECTED`. These reuse model-spec
§§7.5, 7.14.2 and 7.15.6–7.15.8 rather than changing them.

### 4.1 `COND-UK-002` — subordinate and coordinated explicit conditions

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve explicit governing conditions in a multi-clause requirement without assigning them to the wrong result. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Singularity rows; worked application §8 Table 7 R5′; model-spec §7.14.3 general-family discussion. |
| 3. MVP limitation | `COND-UK-001` covers only its edge templates and does not resolve internal/postposed `якщо`, nested or coordinated attachment. |
| 4. Feature / Feature ID | Existing `condition_contexts[]` / `condition_context`; no new family. |
| 5. Proposed Rule ID | `COND-UK-002` (provisional; `COND-UK-001` unchanged). |
| 6. Ukrainian construction | Explicit `якщо` subordinate clause after the behavior; separately, coordinated condition clauses under an explicit source marker. No new marker or generated morphology is admitted by this draft. |
| 7. Parser annotations | Proposed use of source-aligned sentence/token offsets, clause head, dependency relation and coordination/marker information from model-spec §7.15.6. Exact admissible relations and their parser reliability are **UNRESOLVED**. |
| 8. Recognition procedure | Find an approved exact condition marker; determine its complete subordinate/clausal extent and governing result through an approved parser-neutral relation; accept only when both extent and target are unique under an approved attachment rule. Otherwise retain a candidate diagnostic. Matching `якщо` alone never establishes detection. |
| 9. Evidence / offsets | Proposed Evidence is the minimal exact marker-headed condition clause (e.g. `якщо сервіс недоступний`), with offsets into the original trimmed text, not normalized text. A coordinated member without a repeated marker needs an approved multi-span or inherited-marker policy before Evidence can be accepted. |
| 10. Attachment semantics | Condition may govern one or more results only if a separately approved relation proves each link; one condition is not automatically global to the sentence. |
| 11. Positive example | `Система повинна зберегти запит, якщо сервіс недоступний.` → proposed condition span `[32,55)` `якщо сервіс недоступний`, if its governing relation is approved. |
| 12. Negative example | `Система повинна показати слово «якщо» у довідці.` → the quoted word is no condition. |
| 13. False-positive boundary | A marker in quoted text, a definition, a narrative aside or a clause whose target is unknown is not accepted. No nearest-token rule. |
| 14. UNRESOLVED behavior | Unknown clause extent, inherited marker, competing targets, missing required annotations or parser failure: no new accepted Evidence for that candidate; `INCOMPLETE` diagnostic with exact candidate span when available. |
| 15. Applicability | Detect explicit text only; criterion applicability remains `UNKNOWN` unless an independent approved rule states otherwise. |
| 16. Known limitations | No exhaustive Ukrainian condition grammar; multiple sentences within one line are not split or validated here. |
| 17. Dependencies | Attachment decision `ATTACH-UK-001`; SRM-04 implementation; no SRM-05/06 quantitative context expansion. |
| 18. Scientific approval | `PROPOSED_PENDING_RESEARCHER_APPROVAL`; **blocked** on exact grammar, span and attachment decisions. |

### 4.2 `RESULT-UK-002` — coordinated results with explicit normative scope

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve each separately observable result when one explicit normative construction governs coordinated predicates. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Singularity rows; model-spec §7.14.4 family-level statement that each independent coordinated result is a separate observation. |
| 3. MVP limitation | `RESULT-UK-001` leaves coordinated predicate/`conj` scope unresolved. |
| 4. Feature / Feature ID | Existing `expected_results[]` / `expected_result`. |
| 5. Proposed Rule ID | `RESULT-UK-002` (provisional). |
| 6. Ukrainian construction | One explicit `повинен`/`повинна`/`повинні`/`має`/`мають` governing two overt, coordinated behavior predicates, e.g. `Система повинна зберегти запит і повідомити оператора.` |
| 7. Parser annotations | Existing parser-neutral subject, normative anchor, lexical predicate, dependency/coordination, morphology, offsets and sentence boundary. The exact admissible coordination graph is **UNRESOLVED**. |
| 8. Recognition procedure | First establish the explicit normative chain by the existing approved logic; then identify source-explicit coordinated predicate heads and their essential complements. Accept separate observations only if the same normative scope and clause partition are uniquely established. Do not accept a second predicate merely because it follows `і`/`та`. |
| 9. Evidence / offsets | Each accepted result needs exact source fragments sufficient to show inherited normative force. For the second member, a single contiguous substring may omit the shared subject/modal; using multiple `Evidence` references or one covering span is a **researcher decision**. Never synthesize `Система повинна` into the second member's text. |
| 10. Attachment semantics | Shared condition or criterion attaches to both results only if its grammatical scope is demonstrably shared; otherwise links remain uncertain. |
| 11. Positive example | `Система повинна зберегти запит і повідомити оператора.` → candidate spans `[0,30)` `Система повинна зберегти запит` and `[33,53)` `повідомити оператора`; whether those spans are sufficient Evidence is part of the pending shared-scope decision. |
| 12. Negative example | `Система повинна показати напис «зберегти і повідомити».` → coordinated words in a quoted label are not two results. |
| 13. False-positive boundary | Coordinated objects, quoted text, dependent subactions or uncertain negation cannot be promoted to independent expected results. |
| 14. UNRESOLVED behavior | If normative inheritance, subject, clause division, negation or exact Evidence cannot be established, retain the accepted first clause only if independently valid and mark the rest `INCOMPLETE`; do not infer a second result. |
| 15. Applicability | Structural detection does not decide whether more than one result is a singularity defect or change C/V applicability. |
| 16. Known limitations | Independence of obligations is semantic and may need review; parser `conj` alone is not proof. |
| 17. Dependencies | `ATTACH-UK-001`; possible singularity decision in SRM-09/10; SRM-04 after approval. |
| 18. Scientific approval | `PROPOSED_PENDING_RESEARCHER_APPROVAL`; **blocked** on coordination and Evidence rules. |

### 4.3 `RESULT-UK-003` — nonmodal expected results under requirement force

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Represent overt observable results expressed without an MVP normative modal, including worked R5′. |
| 2. Exact source | §2.1 Table 2.1, Completeness row; worked application §8 Table 7 R5′; model-spec §7.14.4 family-level R5′ spans and its explicit first-production exclusion. |
| 3. MVP limitation | `RESULT-UK-001` intentionally does not infer obligation from an indicative verb or inherited context. |
| 4. Feature / Feature ID | Existing `expected_results[]` / `expected_result`. |
| 5. Proposed Rule ID | `RESULT-UK-003` (provisional). |
| 6. Ukrainian construction | Overt nonmodal observable behavior clauses such as R5′ `події зберігаються у черзі` and `UI показує статус degraded` within one requirement sentence. |
| 7. Parser annotations | Source-aligned clause boundaries, subject/predicate/complements, coordination and condition relations; these establish structure but **not** normative force by themselves. |
| 8. Recognition procedure | Delimit each candidate clause and test an independently approved source rule for its requirement/expected-result force. Only after that rule succeeds could the complete minimal clause be accepted. No rule deriving force from line location, indicative mood or a neighboring clause is approved here. |
| 9. Evidence / offsets | Proposed result Evidence would be each exact complete behavior clause; R5′ spans and offsets are recorded in model-spec §7.14.4, but are semantic illustrations, not `RESULT-UK-003` production Evidence. |
| 10. Attachment semantics | Each candidate result must have its own proven condition and criterion links; semicolon or source order does not by itself transfer a condition. |
| 11. Positive example | Source-attested R5′ `Якщо GPS-провайдер не відповідає 15 с, події зберігаються у черзі, UI показує статус degraded, виконується повторна спроба з backoff; після 2 хв формують alert.` illustrates result candidates `[39,65)`, `[67,93)`, `[95,132)` and `[145,159)`, conditional on an approved force rule; condition candidates are `[0,37)` and `[134,144)`. |
| 12. Negative example | `У журналі зазначено, що події зберігаються у черзі.` is descriptive reporting, not automatically a required result. |
| 13. False-positive boundary | An arbitrary indicative verb, reported observation, documentation statement or parser clause is insufficient. |
| 14. UNRESOLVED behavior | Until normative-force and coordination-scope rules are approved, apparent nonmodal candidates remain `UNRESOLVED`; no accepted Evidence is created under this proposed ID. |
| 15. Applicability | No change to requirement type or C criterion applicability. |
| 16. Known limitations | A text-only line may not reveal whether present-tense behavior is normative or descriptive. |
| 17. Dependencies | Researcher force decision; `ATTACH-UK-001`; SRM-04 only after approval. |
| 18. Scientific approval | `PROPOSED_PENDING_RESEARCHER_APPROVAL`; **scientifically blocked** on normative-force semantics. |

### 4.4 `ACCEPT-UK-001` — nonnumeric, observable acceptance criterion

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Preserve an explicit nonnumeric oracle against which fulfilment of a specified result can be judged. |
| 2. Exact source | §2.1 Table 2.1, Completeness and Verifiability rows; §2.3 ¶17–21; §3.2 Table 3.4 (expected behavior or condition); model-spec §7.14.5 family-level discussion. |
| 3. MVP limitation | `ACCEPT-QUANT-001` needs a contained, judgeable numeric anchor and cannot recognize a nonnumeric oracle. |
| 4. Feature / Feature ID | Existing `acceptance_criteria[]` / `acceptance_criterion`. |
| 5. Proposed Rule ID | `ACCEPT-UK-001` (provisional; `ACCEPT-QUANT-001` unchanged). |
| 6. Ukrainian construction | A complete expected behavior with an explicitly specified observable state/output under a stated condition, e.g. `Якщо сервіс недоступний, система повинна показати повідомлення «Сервіс недоступний».` The quoted message is an illustration, not an approved universal oracle pattern. |
| 7. Parser annotations | Result clause, explicit condition boundary and source-aligned object/complement; accepted result and attachment outcomes are prerequisites. Exact sufficiency grammar is **UNRESOLVED**. |
| 8. Recognition procedure | Require an accepted expected-result observation; identify an explicit nonnumeric expected observation/state; require an approved criterion-sufficiency test and deterministic link to the judged result. A result observation alone never implies an acceptance criterion. |
| 9. Evidence / offsets | Proposed criterion Evidence is the exact minimal complete judged behavior clause; separately accepted condition Evidence is referenced through an approved relationship, never copied into a fabricated contiguous span. Original text offsets and independent `acceptance_criterion` Evidence ID are required. |
| 10. Attachment semantics | Criterion must target the result it judges; if it could judge several results, preserve all independently justified links or uncertainty according to §5. |
| 11. Positive example | The explicit-message sentence above has condition `[0,23)` and proposed criterion/result `[25,83)`; it is a nonnumeric criterion case only if the researcher approves that output as sufficient and the relation as unambiguous. |
| 12. Negative example | `Система повинна показати зрозуміле повідомлення.` has no specified observable content or separately approved sufficiency rule. |
| 13. False-positive boundary | No automatic equivalence of expected result and acceptance criterion; method name, numeric context, subjective adjective or a mere link to a test is insufficient. |
| 14. UNRESOLVED behavior | Unknown judgeability, missing/ambiguous target, blocked result parser or uncertain condition scope: diagnostic and `INCOMPLETE`, not a criterion or quality defect. |
| 15. Applicability | A nonnumeric criterion can be relevant without making every requirement's criterion universally mandatory; SRM-09 governs type-specific applicability. |
| 16. Known limitations | Static text cannot prove test procedure quality or actual execution; oracle sufficiency can depend on domain context. |
| 17. Dependencies | `RESULT-UK-002/003` only if used as the result source, `ATTACH-UK-001`, SRM-09/10 applicability/assessment, SRM-04 implementation. |
| 18. Scientific approval | `PROPOSED_PENDING_RESEARCHER_APPROVAL`; **blocked** on exact judgeability and attachment rules. |

### 4.5 `VERIFY-UK-002` — further explicit method-role constructions

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Detect an explicitly stated verification procedure when its grammatical role is clear but it is outside `VERIFY-UK-001` constructions A–C. |
| 2. Exact source | §2.1 Table 2.1, Verifiability row; §2.3 ¶17–21; §3.2 ¶5–10/Table 3.4; model-spec §§7.9 and 7.14.7. |
| 3. MVP limitation | Only `перевіряється`/`перевіряються` instrument, exact verification label and exact `визначено` test declaration are allocated. |
| 4. Feature / Feature ID | Existing `verification_methods[]` / `verification_method`. |
| 5. Proposed Rule ID | `VERIFY-UK-002` (provisional). |
| 6. Ukrainian construction | A named test, analysis, inspection or experiment in an explicit verification-role clause outside A–C. This draft does **not** add a verb, preposition, lemma, English term or method category to the approved vocabulary; exact surfaces must be selected from attested sources or approved separately. |
| 7. Parser annotations | Existing parser-neutral lemma, morphology, dependency role, sentence/segment and offsets; exact additional relations are **UNRESOLVED**. |
| 8. Recognition procedure | First reject `VERIFY-UK-001` coverage/duplicates; require an approved named-method candidate, an approved new governing construction, a proven verification means/role and a deterministic phrase boundary. Without every element, preserve an unresolved candidate. Method-word presence alone is never enough. |
| 9. Evidence / offsets | Proposed Evidence is the exact minimal named procedure phrase, without governing predicate or unrelated behavior, at original source offsets. `спосіб розрахунку SLA` remains an unresolved candidate under current knowledge; it is not promoted by this proposal. |
| 10. Attachment semantics | An explicit method may verify a criterion or a result only when its target is established; a method observation does not assert sufficiency. |
| 11. Positive example | Candidate: `Виконання підтверджується інспекцією журналу.` with candidate method span `[26,44)` `інспекцією журналу`. The verb `підтверджується` is **not** approved; this is a research question, not expected production detection. |
| 12. Negative example | `Система створює тестовий випадок.` names an artifact/system behavior, not an explicit means of checking fulfilment. |
| 13. False-positive boundary | Artifact link, future promise, isolated method noun, discussion about testing and apparently testable behavior remain outside the method family. |
| 14. UNRESOLVED behavior | Until a precise attested surface, role grammar and reproducibility boundary are approved, candidates outside A–C remain unresolved or outside the narrow scan; no `VERIFY-UK-002` accepted Evidence. |
| 15. Applicability | A requirement need not name a method; absence is not zero Verifiability or a defect. |
| 16. Known limitations | A named method does not establish complete inputs, environment, repeatability or adequacy. |
| 17. Dependencies | Researcher vocabulary/role decision; `ATTACH-UK-001` for target relation; SRM-04, with no change to `VERIFY-UK-001`. |
| 18. Scientific approval | `PROPOSED_PENDING_RESEARCHER_APPROVAL`; **blocked** on exact construction and method sufficiency. |

### 4.6 `ATTACH-UK-001` — explicit within-requirement relationship

| Required item | Proposal / limit |
| --- | --- |
| 1. Scientific purpose | Explain which accepted condition, constraint, criterion or method concerns which accepted result while retaining uncertainty. |
| 2. Exact source | §2.1 Table 2.1, Completeness/Verifiability rows; §2.3 ¶4–5, 17–21; §3.2 ¶5–7; §3.3 ¶10–11 and ¶30–36; model-spec §§7.3, 7.14.2 and 7.14.5.1. |
| 3. MVP limitation | `COND-UK-001` establishes only narrow anchor presence, and `ACCEPT-QUANT-001` links by complete Evidence containment. `FeatureObservation` has no general relation field. |
| 4. Feature / Feature ID | **No new feature family or Feature ID proposed.** This is a prospective relationship among existing observations, subject to an approved domain representation. |
| 5. Proposed Rule ID | `ATTACH-UK-001` (provisional relationship-rule ID, not a detector allocation). |
| 6. Ukrainian construction | Within one sentence, explicit grammar can make a condition govern one result or a criterion/method refer to a stated result. No universal source-order construction is approved. |
| 7. Parser annotations | Parser-neutral token/clause boundaries and dependencies, plus exact source offsets and the accepted observation/Evidence references; exact admissible relation paths are **UNRESOLVED**. |
| 8. Recognition procedure | Form candidate pairs only inside the same requirement; preserve existing approved containment links; for new links, require an approved typed grammatical relation with determinate endpoints. Record every independently justified link. If no approved path decides a pair, do not choose by proximity. |
| 9. Evidence / offsets | A relationship would cite its endpoint observations and their already accepted exact Evidence. Parser edges are diagnostics/provenance, never accepted Evidence. A relation-only source token can become Evidence only if a separately approved existing-family observation justifies its own exact span. |
| 10. Attachment semantics | Distinguish unique supported target, several independently justified targets, competing plausible targets, missing target information and unsupported/invalid parse (§5). These are conceptual outcomes, not an approved enum. |
| 11. Positive example | `Якщо сервіс недоступний, система повинна зберегти запит.` has condition `[0,23)` and result `[25,55)`; its `COND-UK-001`/`RESULT-UK-001` observations are approved, but a stored general relation is not. |
| 12. Negative example | `Система повинна зберегти запит і повідомити оператора при перевірці.` does not license choosing one target for `при перевірці` by nearest words. |
| 13. False-positive boundary | Linear adjacency, punctuation alone, same requirement ID and parser `conj` alone are not semantic attachment proof. |
| 14. UNRESOLVED behavior | Preserve endpoints already accepted independently; withhold unsupported links; capture candidate span/reason as diagnostic when source-bound; do not turn missing relation into `NOT_DETECTED` or a defect. |
| 15. Applicability | Relation availability does not change feature or criterion applicability; `UNKNOWN`/`NOT_APPLICABLE` stay distinct. |
| 16. Known limitations | The current domain has no relation record, target IDs or relationship-level uncertainty state. Multiple plausible parses and implicit scope may need researcher review. |
| 17. Dependencies | Researcher-approved relation semantics and domain shape before SRM-04; quantitative attachment beyond containment remains SRM-05/06. |
| 18. Scientific approval | `PROPOSED_PENDING_RESEARCHER_APPROVAL`; **blocked** on relation grammar, cardinality and domain representation. |

## 5. Multi-clause and attachment semantics

One sentence can contain several accepted observations in one requirement.
Each must retain its own source span and rule. The number of clauses or results
does not by itself establish a second requirement, a singularity defect or a
quality score. Under §2.1 Table 2.1, *independent obligations* are relevant to
singularity, but the dissertation and MVP contract supply no detector for
logical independence. That decision is reserved for SRM-09/10.

The following are **proposed review distinctions**, not new domain enum values:

| Relationship case | Required interpretation before implementation |
| --- | --- |
| Supported unambiguous attachment | One approved source-explicit structural path identifies one endpoint; preserve source rule and both exact endpoint Evidence references. Approved `ACCEPT-QUANT-001` containment remains an example of a narrow existing path, not a general rule. |
| Multiple scientifically justified relationships | Preserve every separately proven pair, such as a clearly shared condition governing two accepted results; never collapse them to one arbitrary target. A relation cardinality and evidence contract must first be approved. |
| Ambiguous attachment | Two or more plausible targets exist without an approved disambiguator; preserve candidates and `INCOMPLETE` diagnostics, not a chosen pair. |
| Missing attachment information | A phrase or observation exists, but the text lacks an explicit target or accepted relation; retain any independently accepted observation and mark the proposed link unknown. Do not infer absence of the feature. |
| Unsupported syntax or unreliable parser output | Missing/invalid required annotation, unresolved clause boundary or offset failure prevents new accepted relation Evidence; follow model-spec §7.15.8 parser-failure semantics. |

No nearest-token, nearest-clause, shortest-distance, first-result, last-result
or global-to-sentence fallback is justified by the cited sources. Punctuation
may delimit candidates under approved family rules; it does not by itself
establish semantic scope. Conditions and result clauses may each be plural;
every condition-to-result, criterion-to-result, constraint-to-result and
method-to-result/criterion link needs its own approved rule. The approved
`ACCEPT-QUANT-001` complete-containment check remains exactly as specified;
`ATTACH-UK-001` cannot reinterpret it or the quantitative observation.

## 6. Evidence and domain-contract implications

The approved `Evidence` fields remain `evidence_id`, `requirement_id`,
`feature_id`, `text`, `start_offset`, `end_offset`, `rule_id`. Every accepted
fragment must satisfy
`Requirement.text[start_offset:end_offset] == Evidence.text` using zero-based
Unicode code-point offsets after reader trimming. Evidence is exact original
text with punctuation preserved where the accepted span contains it; normalized
views and parser tokens cannot replace it. Repeated equal fragments at different
offsets remain distinct. Cross-family overlap is allowed when each observation
has its own approved justification and Evidence ID. Parser diagnostics and
`DiagnosticSpan` are not accepted Evidence.

Current `FeatureObservation` can reference several Evidence items, but it has
no typed target or relation. SRM-04 must not encode a link by overloading
`evidence_refs`, by inserting parser-native objects, or by treating identical
spans as proof of attachment. The researcher must choose whether a relation is
needed in the domain, its endpoint identifiers, cardinality, lifecycle,
uncertainty representation and whether it is part of
`RequirementExtractionResult` or another approved structure. No actor, action
or object family follows from this need: model-spec §7.11 keeps those fields
deferred. Predicate/subject annotations can be internal detector inputs only.

Detection remains `DETECTED`, `NOT_DETECTED` or `UNRESOLVED`, derived from
observations plus processing completeness. A mixed accepted/unresolved family
is `INCOMPLETE / DETECTED` with diagnostics; a fully blocked family is
`INCOMPLETE / UNRESOLVED`. `NOT_DETECTED` means the approved scan completed and
found no observation, not that an applicable quality criterion failed. The
separate `APPLICABLE`, `NOT_APPLICABLE`, `UNKNOWN` states remain unchanged.
Structural observations do not create `QUALITY_PROBLEM`; `FIND-U-VAGUE-001`
remains the only approved MVP observation-to-`SIGNAL` conversion. No C/V/U
formula, exact `Fraction` value, applicability rule or reporter behavior is
changed by this document.

## 7. Ukrainian positive, negative and unresolved reference cases

**All rows marked `PROPOSED_PENDING_RESEARCHER_APPROVAL` are new, synthetic
research cases, not binding tests or claims of current detector output.**
`DETECTED` in a proposed row is a *target outcome conditional on approval of
the rule and its blockers*; `UNRESOLVED` is the intended conservative outcome
when a stated blocker remains. Source spans are quoted exactly from each
trimmed sentence; accepted offset pairs would be calculated and verified
against that original text under §7.5 before SRM-04 tests. `—` means no
accepted Evidence for the target candidate.

| Case / original Ukrainian sentence | Target observation; relevant exact source span | Proposed Rule ID; expected outcome | Scientific justification | Approval status |
| --- | --- | --- | --- | --- |
| P01 `Система повинна зберегти запит, якщо сервіс недоступний.` | Postposed condition `[32,55)` `якщо сервіс недоступний` | `COND-UK-002`; conditional `DETECTED` with unique approved link | §2.1 Table 2.1 requires a condition; extends the same source marker beyond MVP edge template. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P02 `Система повинна показати слово «якщо» у довідці.` | Quoted marker candidate `[32,36)` `якщо`; no accepted Evidence | `COND-UK-002`; `NOT_DETECTED` for extended condition after complete scan | A literal mention is not a governing condition (§2.1 Table 2.1). | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P03 `Система повинна зберегти запит і повідомити оператора.` | Candidate results `[0,30)` `Система повинна зберегти запит` and `[33,53)` `повідомити оператора`; second needs approved shared-anchor Evidence | `RESULT-UK-002`; conditional two `DETECTED` observations | §2.1 Table 2.1 singularity/Completeness and model-spec §7.14.4 require preserving independent coordinated results. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P04 `Система повинна показати напис «зберегти і повідомити».` | Quoted candidate `[32,53)` `зберегти і повідомити`; no accepted extra-result Evidence | `RESULT-UK-002`; `NOT_DETECTED` for extra result | Quoted label content is not another required action. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P05 `Якщо сервіс недоступний, події зберігаються у черзі.` | Condition `[0,23)` `Якщо сервіс недоступний`; nonmodal result candidate `[25,51)` `події зберігаються у черзі` | `RESULT-UK-003`; `UNRESOLVED` until normative-force rule approved | Worked R5′ illustrates nonmodal observable behavior, but indicative syntax does not establish normative force. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P06 `У журналі зазначено, що події зберігаються у черзі.` | Descriptive candidate `[24,50)` `події зберігаються у черзі`; no accepted Evidence | `RESULT-UK-003`; `NOT_DETECTED` only if a future force test can exclude it completely | §2.1's expected reaction is distinct from a report of existing behavior. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P07 `Якщо сервіс недоступний, система повинна показати повідомлення «Сервіс недоступний».` | Condition `[0,23)` `Якщо сервіс недоступний`; nonnumeric oracle/result `[25,83)` `система повинна показати повідомлення «Сервіс недоступний»` | `ACCEPT-UK-001`; conditional `DETECTED` | §2.1 Table 2.1 and §3.2 Table 3.4 permit expected behavior as criterion; exact-output sufficiency still needs approval. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P08 `Система повинна показати зрозуміле повідомлення.` | Candidate `[0,47)` `Система повинна показати зрозуміле повідомлення`; no accepted criterion Evidence | `ACCEPT-UK-001`; `UNRESOLVED` if judgeability cannot be excluded, never accepted on the adjective alone | Expected result and sufficient criterion are distinct (model-spec §7.14.5). | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P09 `Виконання підтверджується інспекцією журналу.` | Named-method candidate `[26,44)` `інспекцією журналу`; new governing verb is unapproved | `VERIFY-UK-002`; `UNRESOLVED` until verb/role grammar approved | §2.1 Table 2.1 supports inspection as a method category, not this production construction. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P10 `Система створює тестовий випадок.` | Artifact candidate `[16,32)` `тестовий випадок`; no accepted method Evidence | `VERIFY-UK-002`; `NOT_DETECTED` after complete role check | §2.3 separates observation from a verification procedure. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P11 `Якщо сервіс недоступний, система повинна зберегти запит і повідомити оператора.` | Condition `[0,23)`; result candidates `[25,55)` and `[58,78)` | `ATTACH-UK-001`; conditional two links only if shared scope is independently proven | §2.1 condition/reaction and singularity principles require preserving multiplicity without splitting requirement. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P12 `Система повинна зберегти запит і повідомити оператора при перевірці.` | Attachment candidate `[54,67)` `при перевірці`; no accepted proposed link Evidence | `ATTACH-UK-001`; `UNRESOLVED` | A postposed phrase can modify more than one action; source order gives no approved target. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P13 `Система повинна зберегти запит; перевірка: інспекція журналу.` | Result `[0,30)`; method `[43,60)`; target link remains separate | `ATTACH-UK-001`; method `DETECTED` by existing `VERIFY-UK-001` if parser requirements hold, relation `UNRESOLVED` until new link rule | A named method can be observed without proving which criterion it verifies (§2.1/§3.2). | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |
| P14 `Система повинна зберегти запит і повідомити оператора.` with required parser annotation unavailable | Affected extension candidate `[0,53)`; no accepted extension Evidence | `RESULT-UK-002`; `INCOMPLETE / UNRESOLVED` for proposed rule | Model-spec §7.15.8 forbids treating parser failure as absence. | `PROPOSED_PENDING_RESEARCHER_APPROVAL` |

MVP regression anchors below are **existing approved behavior**, not new SRM-03
reference cases; their exact results remain governed by model-spec §§7.14.3–7.14.7:

| Existing sentence | Target observation; relevant exact source span | Existing Rule ID; approved outcome | Source / status |
| --- | --- | --- | --- |
| `Якщо сервіс недоступний, система повинна зберегти запит.` | Condition `[0,23)` `Якщо сервіс недоступний`; result `[25,55)` `система повинна зберегти запит` | `COND-UK-001`, `RESULT-UK-001`; both `DETECTED` | model-spec §§7.14.3.1, 7.14.4.1; **EXISTING_APPROVED_MVP** |
| `Система повинна відповісти не більше ніж за 2 с.` | Complete criterion `[0,47)` `Система повинна відповісти не більше ніж за 2 с` | `ACCEPT-QUANT-001`; `DETECTED` | model-spec §7.14.5.1; **EXISTING_APPROVED_MVP** |
| `Виконання перевіряється навантажувальним тестом.` | Method `[24,47)` `навантажувальним тестом` | `VERIFY-UK-001`; `DETECTED` | model-spec §7.14.7.1; **EXISTING_APPROVED_MVP** |
| `Система контролює обробку запитів.` | Apparent candidate `[0,33)`; no accepted Evidence | `RESULT-UK-001`; `UNRESOLVED` | model-spec §7.14.4.1; **EXISTING_APPROVED_MVP** |

## 8. Compatibility with MVP v0.1

The reader, six-family registry, approved detectors, exact Evidence contract,
parser-neutral boundary, C/V/U calculators, `RequirementQualityProfile`,
specification aggregation and console presentation are unchanged. Existing
`COND-UK-001`, `RESULT-UK-001`, `ACCEPT-QUANT-001`, `VERIFY-UK-001`,
`QUANT-001`, `QUANT-UK-001` and `UK-VAGUE-001` keep their approved scope and
IDs. New candidate rules must be distinguishable from those baselines and
must not alter their prior binding cases. One non-empty line remains one
requirement. A recognized extra clause is an observation within that object,
not a new requirement ID. An unsupported extra candidate is neither evidence
of absence nor a confirmed defect. No new actor/action/object feature is
introduced merely because the parser exposes a dependency tree.

## 9. Dependencies and SRM-04 implementation handoff

SRM-04 may implement only the subset of proposals for which the researcher has
approved exact grammar, Evidence boundaries, diagnostic/status handling,
relationships and domain representation in `model-spec.md`. For each such
rule, SRM-04 should use the existing extractor boundary and parser-neutral
annotations, create source-aligned tests from approved cases, preserve
MVP regression cases and keep calculators independent of parser/extractor
implementation. The proposed reference cases above must not be treated as
binding tests before approval. Any approved extension must specify how its
observations coexist with the existing rule in the same family, including
source ordering, overlap/deduplication and mixed `INCOMPLETE` processing.

`COND-UK-002`, `RESULT-UK-002/003`, `ACCEPT-UK-001`, `VERIFY-UK-002` and
`ATTACH-UK-001` are **not** a complete implementation plan. Quantitative
grammar and constraint roles remain SRM-05/06; wider ambiguity remains
SRM-07/08; applicability, singularity, Finding conversion and C/V/U changes
remain SRM-09/10/11. If the researcher excludes a candidate rule, SRM-04 must
leave that extension unimplemented and preserve current `UNRESOLVED` behavior
where the approved baseline requires it.

## 10. Researcher decisions required

All decisions below are **PENDING_RESEARCHER_APPROVAL**. An unresolved item
blocks only its affected proposed behavior; the frozen MVP remains valid.

| Decision | Exact question / scientific blocker for SRM-04 |
| --- | --- |
| D01 condition grammar | Which additional positions/coordination structures for the existing condition markers are scientifically supported? Approve exact parser-neutral relation paths, clause boundaries, nested/shared scope, negative cases and new diagnostics. |
| D02 coordinated-result grammar | When does an explicit modal govern multiple independent results? Approve predicate/subject inheritance, negation handling, one-versus-several observation policy, and exact Evidence for a member whose modal/subject is elsewhere. |
| D03 nonmodal normative force | What explicit evidence distinguishes required present-tense behavior from a descriptive statement in one line? Approve or exclude `RESULT-UK-003`; worked R5′ alone is insufficient as a general rule. |
| D04 nonnumeric judgeability | Which textually observable output/state is sufficient for an acceptance criterion, and under what context? Approve a finite deterministic rule, its counterexamples and result/condition linkage; do not equate every result with a criterion. |
| D05 extended verification grammar | Which exact source-attested Ukrainian surfaces and grammatical roles beyond `VERIFY-UK-001` are allowed? Define reproducibility/name boundary, phrase span, exclusions and parser-failure diagnostics. |
| D06 attachment relation | Approve admissible condition/constraint/criterion/method → result paths; one-to-many cardinality; handling of several plausible targets, absent targets and unreliable parses. No distance fallback. |
| D07 domain representation | Decide whether accepted relationships need a typed record; if yes define endpoint IDs, provenance, uncertainty, ordering, compatibility with the six existing feature families and `RequirementExtractionResult`. Parser edges must not escape as scientific Evidence. |
| D08 rule interaction and cases | Approve rule IDs and version, source overlap/deduplication, mixed outcomes and a compact set of positive/negative/unresolved Ukrainian cases with exact offset fixtures. Validate proposed P01–P14 before making any binding tests. |
| D09 singularity boundary | Decide whether independent obligations are only structural context here or a separate local singularity assessment under SRM-09/10. No automatic defect or new characteristic follows from clause count. |

Until D01–D08 are resolved for a particular proposal, **that proposal is not
ready for SRM-04 production implementation**. D09 blocks singularity-specific
behavior, not the approved MVP or purely structural observations whose own
rules have been approved. No missing choice may be supplied by an NLP library,
an example sentence, a numeric score or a convenience heuristic.
