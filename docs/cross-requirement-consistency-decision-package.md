# Cross-Requirement Consistency v0.1 Researcher Decision Package

- **Branch:** research/cross-requirement-analysis
- **Research baseline:** docs/cross-requirement-analysis-research.md and
  docs/model-spec.md at the current branch revision
- **Document status:** RESEARCH_ONLY / PROPOSED_FOR_RESEARCHER_REVIEW
- **Approval effect:** none until the researcher explicitly accepts the
  decisions listed in the final checklist
- **Implementation effect:** none; this document does not authorize production
  code, classes, detectors, tests, pipeline changes, or reporter changes

## Purpose, authority, and decision language

This package proposes the minimum scientific contract needed before a bounded
Cross-Requirement Consistency analysis can be architected. It evaluates the
hypothesis:

    Consistency v0.1 =
        bounded direct quantitative constraint conflict analysis

The source hierarchy remains:

1. dissertation material in docs/reference/;
2. the implementation authority in docs/model-spec.md;
3. the verified findings in docs/cross-requirement-analysis-research.md; and
4. production code and tests only as evidence of the present boundary.

The source locations used most heavily are:

- 2.1_Властивості_вимог.docx, section 2.1 paragraphs 5, 14-16 and
  Table 2.2;
- 2.3_Система_метрик.docx, section 2.3 paragraphs 4-6, 16, 28-30 and
  39-41, plus Tables 2.7-2.9;
- 3.1_Статичні_методи.docx, section 3.1 paragraphs 10-11 and 32-34;
- 3.3_Метод_оцінювання.docx, section 3.3 paragraphs 10-20 and 34-50;
- 4.1_Процесна_модель.docx, 4.2_Модель_якості.docx, and
  4.3_Модель_ризиків.docx for provenance, missing-data, profile, and
  confirmation boundaries; and
- model-spec.md sections 4.1, 7.5-7.6, 7.14.6, 7.15-7.17, 12-15, and 18-19.

The two decision columns have different purposes:

- **Source status** states what kind of support exists:
  SOURCE_DEFINED, DIRECTLY_DERIVABLE, RESEARCHER_OPERATIONALIZATION, or
  DEFERRED.
- **Status** records the decision state:
  SOURCE_DEFINED, DIRECTLY_DERIVABLE, RESEARCHER_APPROVAL_PROPOSED,
  RESEARCHER_APPROVED, DEFERRED, or BLOCKED.

No row in this package has status RESEARCHER_APPROVED. That status is defined
for future use but may be assigned only after an explicit researcher decision.

### Verification of the previous research conclusions

The previous conclusions were checked against the cited sections of
docs/cross-requirement-analysis-research.md and its primary source map. They
remain valid:

| Previously accepted conclusion | Verification |
| --- | --- |
| R_conf contains requirements participating in at least one confirmed conflict, not pairs or findings. | Verified against 2.3_Система_метрик.docx paragraphs 28-30 and Table 2.8; source-defined. |
| M_cons = 1 - \|R_conf\| / \|R\| is source-defined but not executable without further rules. | Verified; the operands and formula are defined, but comparison, confirmation, coverage, and missing-data rules are not. |
| Logical, terminological, and resource conflicts are distinct source-supported classes. | Verified against 2.1_Властивості_вимог.docx paragraphs 14-16. |
| Quantitative incompatibility can be a concrete conflict manifestation. | Verified; it is not established as a fourth peer class. |
| Candidate relations cannot enter R_conf without confirmation. | Verified against 2.3_Система_метрик.docx paragraphs 28-30. |
| Existing quantitative observations are the strongest reusable first-slice input. | Verified against model-spec.md section 7.14.6; comparability is still unapproved. |
| Duplication and M_unique are separate from Consistency. | Verified against the separate R_dup and M_unique source definitions. |
| Local C_i, V_i, and U_i remain separate from specification Consistency. | Verified against the individual-versus-set property distinction and the frozen calculation rules. |
| The existing per-requirement Finding is insufficient for cross-results. | Verified from its single requirement and local-characteristic boundary. |
| Missing or unresolved evidence cannot silently become consistency, conflict, zero, or another number. | Verified throughout the dissertation missing-data rules and model-spec.md sections 14-15. |

The remainder of this package operationalizes only the bounded hypothesis.
Every new operational choice remains proposed, not approved.

## 1. Scope of Consistency v0.1

The hypothesis is scientifically viable only as a narrow direct-conflict
slice. The sources support quantitative incompatibility and the current model
already preserves exact typed observations. They do not provide a general
semantic identity, context-overlap, dependency, terminology, resource, or unit
conversion model.

### Proposed in-scope boundary

Consistency v0.1 would assess pairs of quantitative observations from two
different requirements when all of the following hold:

1. metric and context components are present and resolved;
2. their normalized metric texts are exactly equal;
3. their normalized context texts are exactly equal;
4. both unit labels are present, resolved, and exactly the same approved label;
5. both values are present and represented by exact Decimal values;
6. both comparators have approved inclusive bound semantics:
   LESS_THAN_OR_EQUAL or GREATER_THAN_OR_EQUAL; and
7. the two admissible value sets can therefore be constructed without semantic
   inference.

The slice would report direct quantitative bound incompatibility as a
manifestation of logical conflict. It would not claim to assess the full
logical-conflict class.

### Explicitly out of scope

The following remain deferred:

- general logical contradiction or incompatible behavior;
- terminological inconsistency, synonymy, and definition conflict;
- resource, capacity, dependency, and trade-off conflicts;
- semantic duplication, R_dup, and M_unique;
- traceability and specification coverage;
- implicit domain or common-sense conflicts;
- unit conversion and dimensional reasoning;
- context overlap weaker than exact normalized identity;
- equality, exclusive bounds, ranges, tolerances, distributions, percentiles,
  statistical uncertainty, and measurement procedures;
- frequency constraints using NOT_LESS_FREQUENT;
- generic UPPER_BOUND interpretation while inclusivity is unresolved;
- relationships among several observations inside one requirement;
- severity, risk, probability, priority, confidence scores, and corrective
  actions; and
- product-quality inference or an overall specification score.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D001 | Is bounded quantitative constraint conflict analysis a defensible first executable slice? | RESEARCHER_OPERATIONALIZATION built on source-defined quantitative incompatibility and typed observations | Adopt the hypothesis only with the seven in-scope gates above. | It is the narrowest current data path capable of a deterministic simultaneity test. | Approval would authorize preparation of binding quantitative reference cases, not implementation. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D002 | What conflict class does the slice represent? | DIRECTLY_DERIVABLE | Treat direct quantitative bound incompatibility as a manifestation of logical conflict, not as a fourth peer class. | The source taxonomy has logical, terminological, and resource classes; quantitative incompatibility describes a manifestation. | Future reporting must preserve both the logical class and bounded quantitative subtype without claiming full logical coverage. | DIRECTLY_DERIVABLE |
| CRA-D003 | Which adjacent classes enter v0.1? | DEFERRED | Exclude every item in the out-of-scope list. | Each requires a rule, ontology, dependency model, or evidence source not currently approved. | No omitted class may affect R_conf or M_cons in this slice. | DEFERRED |
| CRA-D004 | Does this package approve production work? | SOURCE_DEFINED project/research boundary | No. It approves, at most, a scientific contract after researcher review. | Architecture and implementation must follow approved science. | Production code, tests, and current pipeline behavior remain unchanged. | SOURCE_DEFINED |

## 2. Unit of cross-analysis

Let R be the ordered sequence of non-empty requirements produced by the
approved RequirementReader policy. The conceptual requirement comparison
universe for this pairwise slice is:

    P_R = { {r_i, r_j} | r_i in R, r_j in R, i < j }

The braces denote an unordered semantic pair. Source order supplies a canonical
representation: the earlier requirement is left and the later requirement is
right. Thus (R001, R017) and (R017, R001) are one comparison.

For a requirement pair, the bounded comparison members are the Cartesian
product of the quantitative observations attached to the two requirements.
Observation order is the accepted extraction order. No observation is compared
with another observation from the same requirement in v0.1.

The pair universe is conceptual. A future implementation may avoid
materializing every pair only if it proves that its candidate selection is
observationally equivalent to evaluating this declared universe under the same
rules and coverage profile.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D005 | What is the minimum cross-analysis unit? | RESEARCHER_OPERATIONALIZATION | Use an unordered pair of distinct requirements. | The selected conflict is symmetric and direct; self-comparison is not cross-analysis. | Arbitrary multi-requirement conflicts remain outside v0.1. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D006 | Are reversed requirement pairs distinct? | DIRECTLY_DERIVABLE plus ordering operationalization | No; canonicalize by input/source order, earlier first. | Reversal does not change joint satisfiability. | Each requirement pair is considered once and has one stable orientation. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D007 | What is compared inside a requirement pair? | RESEARCHER_OPERATIONALIZATION | Evaluate every cross-requirement quantitative-observation pair in extraction order. | It avoids silently selecting one observation when several exist. | One requirement pair can yield multiple cross-results. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D008 | Are within-requirement observation comparisons covered? | DEFERRED | No. | Their relationship grammar is not approved and the requested unit is cross-requirement. | Multiple observations in one requirement are independent comparison members only against observations in the other requirement. | DEFERRED |
| CRA-D009 | May candidate selection prune the conceptual universe? | DIRECTLY_DERIVABLE obligation; algorithm deferred | Only if equivalence to the declared coverage is demonstrated. | An optimization must not change the scientific claim. | Candidate-selection completeness becomes an architecture and validation obligation. | DIRECTLY_DERIVABLE |

## 3. Candidate versus confirmed conflict

Candidate generation is not a scientific assessment state. It is an optional
upstream retrieval or optimization activity. Candidate records, if later
introduced, belong to a review or processing queue and never enter R_conf.

For one quantitative-observation pair, the proposed assessment states are:

- CONFIRMED_CONFLICT: all applicability and identity gates are resolved and the
  approved conflict predicate proves empty intersection;
- CONFIRMED_NON_CONFLICT: all gates are resolved and the approved predicate
  proves non-empty intersection;
- ASSESSMENT_UNRESOLVED: the pair could be in scope, but a required identity or
  comparison input is absent or unresolved; and
- OUTSIDE_V0_1_APPLICABILITY: resolved information proves that the pair is not
  covered by the bounded rule.

OUTSIDE_V0_1_APPLICABILITY is an applicability disposition, not evidence that
the requirements are non-conflicting. CONFIRMED_NON_CONFLICT is also
rule-relative: it means only that this particular admissible-set comparison is
jointly satisfiable.

The word unresolved has a second meaning in the dissertation phrase
“confirmed unresolved conflict”: a confirmed conflict that has not been
remediated or closed. This package keeps the meanings separate:

- ASSESSMENT_UNRESOLVED means the evidence cannot determine conflict state;
- open confirmed conflict means a conflict has been determined but has not
  been dispositioned.

Conflict remediation and an OPEN/RESOLVED lifecycle are deferred. At the
v0.1 assessment snapshot, every emitted CONFIRMED_CONFLICT is treated as an
open confirmed conflict for R_conf construction.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D010 | Is candidate a scientific assessment state? | SOURCE_DEFINED candidate-versus-confirmed separation | No; keep candidate generation separate. | The dissertation forbids treating model candidates as facts. | Candidate counts never affect R_conf or M_cons. | SOURCE_DEFINED |
| CRA-D011 | What states describe an observation-pair assessment? | RESEARCHER_OPERATIONALIZATION | Use the four states/dispositions defined above. | They separate proof of conflict, proof of bounded joint satisfiability, insufficient evidence, and rule inapplicability. | Unknown cannot collapse into either conflict or non-conflict. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D012 | Can the bounded deterministic rule confirm automatically? | RESEARCHER_OPERATIONALIZATION | Yes, but only after the rule, inputs, and binding cases are approved and all gates are resolved. | Empty intersection is mechanically conclusive under an approved identity and interval contract. | Human review is not mandatory for this one rule; unsupported semantic cases still require future confirmation procedures. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D013 | What happens when required evidence is insufficient? | DIRECTLY_DERIVABLE with state-name operationalization | Produce ASSESSMENT_UNRESOLVED with exact reasons and provenance. | Missing information is not a negative or positive finding. | The result cannot enter R_conf and can withhold M_cons under CRA-D024. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D014 | Is conflict remediation lifecycle in v0.1? | DEFERRED | No; evaluate one versioned assessment snapshot and treat confirmed conflicts as open at that snapshot. | No resolution workflow or historical state contract is approved. | Removing a requirement from R_conf after remediation requires a future lifecycle decision and reassessment. | DEFERRED |

## 4. R_conf construction

For an assessment snapshot, define:

    C_confirmed =
        the set of CONFIRMED_CONFLICT cross-results under the approved rule

    R_conf =
        union over c in C_confirmed of Participants(c)

R_conf is a mathematical set. A requirement therefore appears once regardless
of how many confirmed conflicts or observations involve it. A confirmed
conflict between R001 and R017 adds both R001 and R017.

Within this proposed slice, the constructed set is more precisely
R_conf[QB-v0.1]. It is not asserted to be the complete full-scope R_conf until
all source-defined conflict classes have approved coverage.

The set may be constructed and retained from confirmed results even when the
overall metric is withheld because other comparisons are unresolved. In that
case it is an observed partial set, not a claim that no other requirement
belongs in the final set.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D015 | What is R_conf? | SOURCE_DEFINED | Requirements participating in at least one open confirmed conflict at the assessment snapshot. | This is the dissertation operand definition. | It is neither a pair set nor finding count. | SOURCE_DEFINED |
| CRA-D016 | How often is one requirement counted? | DIRECTLY_DERIVABLE | Once, by set union. | Repeated conflicts do not create repeated set members. | The numerator is bounded by the denominator. | DIRECTLY_DERIVABLE |
| CRA-D017 | Does a two-requirement conflict add both participants? | DIRECTLY_DERIVABLE | Yes. | Both requirements participate in the conflict. | R001 versus R017 contributes two distinct members unless already present. | DIRECTLY_DERIVABLE |
| CRA-D018 | What happens for an empty specification? | SOURCE_DEFINED through the zero-denominator/empty-applicability convention | R_conf is empty, but M_cons is NOT_APPLICABLE and has no numeric value. | The formula is undefined at \|R\| = 0 and source policy forbids substituting zero. | No value 0 or 1 is emitted. | SOURCE_DEFINED |
| CRA-D019 | What happens for exactly one requirement? | RESEARCHER_OPERATIONALIZATION | R_conf is empty and M_cons is NOT_APPLICABLE. | No cross-requirement pair exists; returning 1 would overclaim observed consistency. | The profile records total_requirement_count = 1 and zero eligible pairs. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D020 | What happens when no comparison is observable/applicable? | RESEARCHER_OPERATIONALIZATION | R_conf is empty and M_cons is NOT_APPLICABLE. | The bounded property was not observed; absence of an applicable comparison is not a successful assessment. | No numeric consistency claim is made. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D021 | What happens when some comparisons are assessment-unresolved? | RESEARCHER_OPERATIONALIZATION | Preserve the observed partial R_conf, label it partial, and do not treat it as complete. | Confirmed evidence remains valid, but unresolved comparisons could add members. | Numeric propagation is decided separately in CRA-D024. | RESEARCHER_APPROVAL_PROPOSED |

## 5. M_cons calculation contract

The source-defined formula is:

    M_cons = 1 - |R_conf| / |R|
           = (|R| - |R_conf|) / |R|

The proposed executable contract is deliberately strict.

The executable value proposed by this package is coverage-qualified:

    M_cons[QB-v0.1] =
        1 - |R_conf[QB-v0.1]| / |R|

QB-v0.1 means only the bounded quantitative-bound rule in this package. The
formula is unchanged, but the conflict-participant set is explicitly limited
to the declared coverage. The value must never be labeled as proof of full
logical, terminological, and resource Consistency. An unqualified full-scope
M_cons remains scientifically unavailable until the wider source-defined
conflict universe has approved coverage.

M_cons[QB-v0.1] is COMPUTED only when:

1. there are at least two requirements;
2. at least one observation pair is applicable to the bounded comparison rule;
3. quantitative-observation extraction is resolved for every requirement, so
   the accepted observation list is complete under the current extractor
   contract;
4. every potentially applicable observation pair has a resolved disposition;
5. no result is ASSESSMENT_UNRESOLVED; and
6. R_conf was constructed only from CONFIRMED_CONFLICT results.

If any potentially applicable comparison is ASSESSMENT_UNRESOLVED, the
Consistency aggregate is UNKNOWN with value absent. This rule intentionally
does not copy the mixed COMPUTED plus UNKNOWN behavior of AGG-MVP-001.
Consistency is not a mean of independent pair values: an unresolved comparison
can change membership of one or two requirements in the global set R_conf.

When computed, the value is an exact reduced Fraction. No rounding or decimal
presentation rule is introduced here.

Required observability metadata is:

- total_requirement_count;
- requirements_with_quantitative_observations_count;
- requirements_participating_in_applicable_comparisons_count;
- unresolved_quantitative_extraction_count;
- total_requirement_pair_count;
- total_observation_pair_count considered;
- applicable_comparison_count;
- confirmed_conflict_count;
- confirmed_non_conflict_count;
- assessment_unresolved_count;
- outside_applicability_count;
- observed R_conf count and whether the set is complete;
- analysis rule identifier and version; and
- coverage profile identifier and version.

These are conceptual scientific fields, not approved Python names.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D022 | What are the denominator and numerator? | SOURCE_DEFINED | Denominator is all requirements R accepted by RequirementReader; numerator is the distinct complete R_conf set. | The source formula counts requirements on both sides. | Observation and pair counts never replace either operand. | SOURCE_DEFINED |
| CRA-D023 | What numeric representation is used? | RESEARCHER_OPERATIONALIZATION consistent with current exact arithmetic | Use exact reduced Fraction and no rounding. | Both cardinalities are integers and the project preserves exact results. | A later reporter may format only under a separately approved presentation contract. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D024 | May M_cons be computed with any ASSESSMENT_UNRESOLVED comparison? | RESEARCHER_OPERATIONALIZATION | No; return aggregate UNKNOWN with value absent. | An unresolved pair may add new R_conf members, so the source numerator is not known. | Strict withholding prevents a partial lower bound from being mislabeled as the metric. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D025 | What if the universe contains no applicable comparison? | RESEARCHER_OPERATIONALIZATION | Return NOT_APPLICABLE with value absent. | The bounded property was not observed. | A value of 1 is prohibited. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D026 | Is observability metadata mandatory with M_cons? | DIRECTLY_DERIVABLE obligation; field set operationalized | Yes, use the minimum metadata listed above. | The dissertation requires evidence sufficiency, coverage, provenance, and unavailable-state visibility. | The numeric value cannot be presented without its coverage and counts. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D027 | Does AGG-MVP-001 govern M_cons? | DIRECTLY_DERIVABLE | No. | AGG-MVP-001 averages independent local C/V/U values; M_cons is a direct set-cardinality formula with cross-coupled unknowns. | Its mixed-state policy cannot be copied automatically. | DIRECTLY_DERIVABLE |
| CRA-D028 | Is a partial R_conf itself a valid M_cons numerator? | DIRECTLY_DERIVABLE under CRA-D024 | No. | It is an evidence-backed lower bound on observed membership, not the complete source-defined operand. | It may be reported for audit only while the metric remains UNKNOWN. | DIRECTLY_DERIVABLE |
| CRA-D066 | May the bounded slice publish an unqualified full-scope M_cons? | DIRECTLY_DERIVABLE scope limit plus researcher operationalization | No. Publish only M_cons[QB-v0.1] with its coverage profile; reserve unqualified M_cons for approved coverage of the source-defined conflict universe. | R_conf from one quantitative subtype is not known to contain participants in terminological, resource, or other logical conflicts. | The bounded value is executable after approval without being misrepresented as universal Consistency. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D067 | What if quantitative-observation extraction is unresolved for any requirement? | RESEARCHER_OPERATIONALIZATION | Return aggregate UNKNOWN even if no unresolved observation pair was materialized. | An unextracted observation could introduce an applicable comparison and new R_conf members. | Resolved NOT_DETECTED may remain outside the slice, but unresolved extraction withholds the metric. | RESEARCHER_APPROVAL_PROPOSED |

## 6. Quantitative comparison identity

### 6.1 Bounded text normalization

For identity only, the proposed normalization N(text) is:

1. Unicode NFC normalization;
2. Unicode case folding;
3. replacement of each run of Unicode whitespace with one ASCII space; and
4. removal of leading and trailing whitespace.

Every other character, including punctuation, remains significant. There is
no stemming, lemmatization, morphology, transliteration, punctuation removal,
synonym dictionary, ontology, embedding, or fuzzy threshold.

Evidence identity is not semantic identity. Evidence IDs are local to one
RequirementExtractionResult and cannot establish that two source phrases mean
the same thing. Exact source Evidence remains mandatory for provenance.

### 6.2 Comparison key

For one fully resolved observation q, define the bounded comparison key:

    K(q) = (
        N(metric_text(q)),
        N(context_text(q)),
        unit_label(q)
    )

Two observations can reach the conflict predicate only when their keys are
exactly equal and all required components are resolved.

This key is a deliberately narrow proxy for “same constrained subject.” It is
not a universal semantic-subject identity. In particular, час відповіді and
час відгуку are not identical under N and are therefore outside this rule,
even if a domain expert might regard them as synonyms.

### 6.3 Component decisions

**Metric.** A metric component must be present, resolved, and supported by its
own Evidence. Exact normalized text equality is required. A missing or
unresolved metric makes a potentially relevant pair ASSESSMENT_UNRESOLVED.
Two present, resolved, unequal metric texts put that observation pair outside
v0.1 applicability.

**Context.** A context component must be present, resolved, and supported by
its own Evidence. Exact normalized text equality is required. Missing or
unresolved context is not interpreted as global context; it yields
ASSESSMENT_UNRESOLVED. Two resolved unequal contexts put the pair outside
v0.1 applicability.

**Unit.** SECOND is comparable only with SECOND, MINUTE only with MINUTE, and
PERCENT only with PERCENT when the metric/context key is otherwise complete.
Different resolved labels put the pair outside this bounded rule. No conversion
is performed, including 60 seconds to 1 minute. Missing or unresolved unit
information yields ASSESSMENT_UNRESOLVED.

**Comparator.** LESS_THAN_OR_EQUAL and GREATER_THAN_OR_EQUAL are the only
supported comparators. NOT_LESS_FREQUENT is outside the numeric bound rule.
UPPER_BOUND yields ASSESSMENT_UNRESOLVED because its inclusivity is explicitly
unresolved. A missing or unresolved comparator likewise yields
ASSESSMENT_UNRESOLVED.

**Value.** Each side must have a resolved exact Decimal numeric value.
Missing or unresolved values yield ASSESSMENT_UNRESOLVED. Decimal values are
compared exactly; no tolerance is invented.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D029 | What bounded text normalization defines identity? | RESEARCHER_OPERATIONALIZATION | Use N exactly as specified in section 6.1. | It absorbs only representation differences with explicit deterministic rules. | Any semantic equivalence beyond N is unsupported. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D030 | What establishes metric identity? | RESEARCHER_OPERATIONALIZATION | Present, resolved metric components with exact N-normalized text equality. | No metric vocabulary or synonym rule is approved. | час відповіді and час відгуку do not compare in v0.1. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D031 | Do Evidence IDs establish cross-requirement identity? | DIRECTLY_DERIVABLE | No; use Evidence only as provenance. | IDs are local and evidence location is not semantic equivalence. | Cross identity is decided by the bounded key, not identifier coincidence. | DIRECTLY_DERIVABLE |
| CRA-D032 | What establishes context identity? | RESEARCHER_OPERATIONALIZATION | Present, resolved context components with exact N-normalized text equality. | Simultaneous applicability cannot be inferred from absent or merely similar text. | Different resolved contexts are outside scope; missing/unresolved context is assessment-unresolved. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D033 | Which units are compatible? | RESEARCHER_OPERATIONALIZATION constrained by the no-conversion source rule | Only exact equality of the approved UnitLabel. | The current model defines labels but no conversion or dimensional ontology. | SECOND and MINUTE are outside the bounded rule even when values could be converted. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D034 | Which comparators are supported? | SOURCE_DEFINED semantics plus bounded selection | Only inclusive LESS_THAN_OR_EQUAL and GREATER_THAN_OR_EQUAL reach the predicate. NOT_LESS_FREQUENT is outside; UPPER_BOUND is assessment-unresolved. | Only the two inclusive comparators have complete numeric-bound semantics. | No implicit inclusivity or generic comparator is introduced. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D035 | What value semantics are supported? | SOURCE_DEFINED Decimal representation plus operational gate | Require a resolved Decimal on both sides and compare exactly. | The current contract supplies exact values but no tolerance model. | Missing values are unresolved; “approximately equal” is unsupported. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D036 | What is the v0.1 constrained-subject identity? | RESEARCHER_OPERATIONALIZATION | Exact equality of K(q) = normalized metric, normalized context, and exact unit label. | It is the minimum reproducible proxy available without a semantic ontology. | The rule's claim must always be qualified as bounded textual identity. | RESEARCHER_APPROVAL_PROPOSED |

## 7. Quantitative conflict definition

For an observation q with exact value v, define its admissible set only for the
two approved comparator forms:

    A(q) = (-infinity, v]   when comparator is LESS_THAN_OR_EQUAL

    A(q) = [v, +infinity)   when comparator is GREATER_THAN_OR_EQUAL

For two observations q1 and q2 with equal complete keys K(q1) = K(q2):

    QuantitativeConflict(q1, q2)
        iff A(q1) intersection A(q2) is empty

For the bounded forms, this reduces to:

- two upper bounds are confirmed non-conflicting;
- two lower bounds are confirmed non-conflicting;
- an upper bound x <= u and lower bound x >= l conflict iff l > u;
- the mixed pair is confirmed non-conflicting iff l <= u; and
- equality l = u is non-conflicting because the shared endpoint satisfies both
  inclusive constraints.

“Confirmed non-conflict” remains local to this one observation-pair rule. It
does not assert that the two requirements have no other conflict.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D037 | How is one supported constraint interpreted? | RESEARCHER_OPERATIONALIZATION using source-defined inclusive comparator semantics | Map inclusive upper and lower bounds to the two admissible sets above. | The mapping preserves the approved comparator meanings exactly. | Unsupported comparators have no admissible-set construction in v0.1. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D038 | What confirms a quantitative conflict? | RESEARCHER_OPERATIONALIZATION | Equal complete keys plus empty admissible-set intersection. | Conflict means the two obligations cannot be satisfied simultaneously, not merely that numbers differ. | The predicate is deterministic and explainable. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D039 | How are same-direction bounds classified? | DIRECTLY_DERIVABLE after CRA-D037 | Confirmed non-conflict. | Two inclusive upper half-lines or two inclusive lower half-lines always intersect. | One bound may be stricter without causing contradiction. | DIRECTLY_DERIVABLE |
| CRA-D040 | How is a shared inclusive endpoint classified? | DIRECTLY_DERIVABLE after CRA-D037 | Confirmed non-conflict. | The shared endpoint satisfies both constraints. | The conflict comparison uses strict l > u, not l >= u. | DIRECTLY_DERIVABLE |

### Required decision examples

All examples assume two different requirements. “Same metric/context” means
equality under the proposed key rules, not inferred semantics.

| Case | Inputs | Classification | Reason |
| --- | --- | --- | --- |
| A | x <= 2 and x >= 5, same complete key | confirmed conflict | [5,+infinity) and (-infinity,2] have empty intersection. |
| B | x <= 5 and x >= 2, same complete key | confirmed non-conflict | [2,+infinity) and (-infinity,5] overlap on [2,5]. |
| C | x <= 2 and x <= 5, same complete key | confirmed non-conflict | The two upper half-lines overlap. |
| D | x >= 5 and x >= 2, same complete key | confirmed non-conflict | The two lower half-lines overlap. |
| E | Same numeric bounds but different resolved contexts | outside v0.1 applicability | The context components are deterministically unequal; no context-overlap semantics is inferred. |
| F | Same metric/context/value but different resolved units | outside v0.1 applicability | Exact UnitLabel equality is required and conversion is forbidden. |
| G | One bound has unresolved inclusivity | unresolved | UPPER_BOUND cannot be mapped to an inclusive or exclusive admissible set. |
| H | One observation lacks metric | unresolved | Metric identity cannot be established or rejected. |
| I | One observation lacks context | unresolved | Missing context is not assumed global or equal. |
| J | One requirement contains multiple quantitative observations | outside v0.1 applicability as one combined-constraint case | v0.1 does not infer relationships among co-located observations. Each cross-requirement observation pair is nevertheless classified independently as A-I rules permit. |

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D041 | Are Cases A-J the proposed classifications? | RESEARCHER_OPERATIONALIZATION | Accept the classifications in the table as decision examples. | They expose positive, negative, non-applicable, unresolved, and multi-observation boundaries. | After approval they can seed, but do not yet constitute, binding reference cases. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D042 | Are these binding executable reference cases now? | RESEARCHER_OPERATIONALIZATION dependencies are unapproved | No. | Their expected outcomes depend on approval of CRA-D029 through CRA-D041 and require full requirement/evidence fixtures. | Test-case authoring must not begin in this research round. | BLOCKED |

## 8. Cross-result scientific contract

A future cross-result must preserve enough information to reproduce and explain
the assessment without consulting mutable detector state. The minimum
conceptual contract is:

- stable result identifier;
- assessment snapshot or source-set version identity;
- canonical participating requirement IDs;
- relation class and bounded conflict subtype;
- assessment state or applicability disposition;
- governing comparison and confirmation Rule ID plus version;
- qualified references to both participating quantitative observations;
- qualified Evidence references from every participant;
- the resolved comparison key components used by the rule;
- comparator labels and exact Decimal values used by the rule;
- human-readable explanation of conflict, non-conflict, inapplicability, or
  uncertainty;
- complete unresolved reason codes and their evidence/diagnostic provenance;
- coverage profile identifier and version; and
- deterministic order keys.

For v0.1, the proposed relation meaning is
DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY, classified as a bounded logical
conflict manifestation. The exact production vocabulary and serialized field
names remain architectural decisions.

A quantitative-observation reference must identify both the owning requirement
and the observation unambiguously. The recommended scientific identity is:

    (requirement_id, quantitative_feature_id, observation_source_order)

This does not add a production field now. If architecture later supplies a
stable observation ID with equivalent provenance and ordering, it may satisfy
the same requirement.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D043 | What must every cross-result preserve? | SOURCE_DEFINED provenance obligations plus operational field set | Preserve every conceptual item listed above. | A cross-result must be independently explainable, reproducible, and uncertainty-aware. | A production schema cannot omit participants, governing rule, evidence, state, reasons, or coverage. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D044 | What relation does a confirmed result represent? | RESEARCHER_OPERATIONALIZATION | Direct quantitative bound incompatibility as a bounded logical conflict manifestation. | It accurately names the rule without claiming all logical conflict detection. | Taxonomy expansion requires separate decisions. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D045 | Must result identifiers be stable? | DIRECTLY_DERIVABLE | Yes, across repeated analysis of the same versioned inputs and rule set. | Stable findings are needed for traceability and review. | Exact encoding or hashing is deferred to architecture. | DIRECTLY_DERIVABLE |
| CRA-D046 | How is an observation referenced conceptually? | RESEARCHER_OPERATIONALIZATION | Qualify it by requirement, quantitative feature, and source-order observation index, or an exactly equivalent stable identity. | Existing observations have no globally safe cross-record identity. | Architecture must validate the reference against the owning extraction result. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D047 | Are severity, probability, risk, confidence score, or corrective action part of the result? | SOURCE_DEFINED separation | No. | Those are separate models and no numeric or categorical rules are approved. | The result carries evidence sufficiency and confirmation state only. | SOURCE_DEFINED |

## 9. Evidence provenance

Evidence IDs remain local to their RequirementExtractionResult. A cross-result
therefore references source evidence as:

    CrossEvidenceRef = (requirement_id, evidence_id)

The owning requirement ID is semantically mandatory, not optional display
metadata. Validation must establish that:

1. the requirement is one of the result participants;
2. the evidence exists in that requirement's extraction result;
3. its span and source text remain unchanged;
4. the referenced feature/observation legitimately uses that evidence; and
5. evidence from both sides needed by the explanation is preserved.

Existing Evidence IDs are not mutated or prefixed merely to make them globally
unique. Cross-record uniqueness belongs to the compound reference.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D048 | How is Evidence referenced across records? | DIRECTLY_DERIVABLE with representation operationalization | Use the conceptual pair (requirement_id, evidence_id). | An unqualified Evidence ID can be ambiguous across extraction results. | Every evidence lookup and explanation remains anchored to one requirement. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D049 | Should existing Evidence IDs be made globally unique? | DIRECTLY_DERIVABLE | No. | The compound reference solves provenance without changing the accepted single-requirement contract. | No Evidence mutation or baseline refactor is authorized. | DIRECTLY_DERIVABLE |
| CRA-D050 | What validation must a cross-evidence reference satisfy? | SOURCE_DEFINED provenance obligation plus operational invariants | Apply all five validation conditions above. | Preserving a string ID alone is insufficient evidence integrity. | Invalid or foreign references must make the future result construction fail rather than silently detach provenance. | RESEARCHER_APPROVAL_PROPOSED |

## 10. Relation to local C/V/U

Cross-requirement Consistency and local Completeness, Verifiability, and
Unambiguity answer different questions at different units of analysis.
A requirement can have a fully computed local profile and still conflict with
another requirement. Conversely, an UNKNOWN local characteristic does not by
itself establish a cross conflict.

The proposed formal rule is:

    A cross-requirement consistency result does not retroactively alter
    C_i, V_i, or U_i.

It contributes only to a separate specification-level Consistency assessment.
Any future dual effect would require a separately sourced and approved
calculation rule.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D051 | Does a cross-result alter C_i, V_i, or U_i? | DIRECTLY_DERIVABLE from the source level distinction and frozen rules | No. Formally preserve the current local values. | No source defines a cross-conflict contribution to any local formula. | Existing calculators, profiles, traces, and tests remain unchanged. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D052 | Where does the result contribute? | SOURCE_DEFINED property-level distinction plus boundary operationalization | To a separate specification-level Consistency assessment. | Consistency is a property of the requirement set. | It cannot be folded into a local characteristic or its mean. | RESEARCHER_APPROVAL_PROPOSED |

## 11. Relation to the existing SpecificationQualityProfile

The existing SpecificationQualityProfile(C_file, V_file, U_file) continues to
mean exactly the aggregation of local C/V/U profiles under AGG-MVP-001. It does
not become an implicitly complete description of every specification-level
property.

Three placement options were evaluated:

| Option | Scientific boundary | Disposition |
| --- | --- | --- |
| A | Extend the existing SpecificationQualityProfile with Consistency. | Not recommended. It changes a closed C/V/U aggregate contract and mixes local-property means with a relationship-based set metric. |
| B | Define a future broader conceptual SpecificationAssessment that composes the unchanged C/V/U profile with a separate Consistency assessment. | Recommended. It preserves both meanings and allows each property to retain its own state, evidence, findings, and observability. |
| C | Keep Consistency entirely outside any broader specification assessment. | Rejected as the long-term scientific boundary; Consistency is itself a specification-set property, though implementation placement remains deferred. |

Option B names a conceptual boundary only. It does not approve a Python class,
constructor, module, pipeline stage, or reporter layout.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D053 | Does the current SpecificationQualityProfile change meaning? | DIRECTLY_DERIVABLE | No; it remains C_file, V_file, and U_file only. | That contract and its aggregation semantics are already approved. | No current aggregation or reporter change follows from this package. | DIRECTLY_DERIVABLE |
| CRA-D054 | Which future boundary should contain Consistency? | RESEARCHER_OPERATIONALIZATION | Select Option B: a broader conceptual SpecificationAssessment composed from the unchanged local aggregate profile and separate set-level assessments. | It keeps heterogeneous formulas, states, evidence, and coverage explicit. | Architecture may later name the type differently but must preserve this separation. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D055 | Does the broader assessment combine properties into one scalar? | SOURCE_DEFINED prohibition | No. | The dissertation favors multidimensional profiles and no weighting formula is approved. | M_cons remains one property indicator, not a file-quality score. | SOURCE_DEFINED |

## 12. UNKNOWN and observability contract

The decision sequence for each observation pair is:

1. If either comparator is NOT_LESS_FREQUENT, return
   OUTSIDE_V0_1_APPLICABILITY.
2. If any resolved required key component is deterministically unequal, return
   OUTSIDE_V0_1_APPLICABILITY; that mismatch is sufficient even if another
   component is unavailable.
3. Otherwise, if metric/context/unit/value is missing or unresolved, or the
   comparator is missing or unrecognized, return ASSESSMENT_UNRESOLVED.
4. If the comparator is UPPER_BOUND or otherwise lacks the semantics needed
   for an admissible set, return ASSESSMENT_UNRESOLVED.
5. If the complete keys match and all supported comparison inputs are
   resolved, apply the conflict predicate.

This order prevents a resolved mismatch from being mislabeled unknown while
also preventing a missing identity component from being treated as a proven
mismatch.

At specification level:

- no requirement pair or no applicable observation comparison produces
  NOT_APPLICABLE with no M_cons value;
- unresolved quantitative extraction for any requirement produces UNKNOWN
  even when it prevented an observation pair from being materialized;
- one or more applicable comparisons, resolved extraction for every
  requirement, and no ASSESSMENT_UNRESOLVED result permits computation;
- any ASSESSMENT_UNRESOLVED result produces UNKNOWN with no M_cons value; and
- confirmed results remain reportable even when the aggregate is UNKNOWN.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D056 | What does unresolved quantitative input produce? | DIRECTLY_DERIVABLE with state operationalization | ASSESSMENT_UNRESOLVED with component-specific reasons. | Unknown cannot become conflict or non-conflict. | The pair does not enter R_conf. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D057 | What does resolved key inequality produce? | RESEARCHER_OPERATIONALIZATION | OUTSIDE_V0_1_APPLICABILITY, not confirmed non-conflict. | The selected rule does not assess different constrained subjects or scopes. | It is counted in coverage metadata only. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D058 | What if the pair could contain a conflict but confirmation is impossible? | SOURCE_DEFINED missing-data boundary plus state operationalization | ASSESSMENT_UNRESOLVED. | Neither polarity is justified. | It withholds M_cons under the strict proposed policy. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D059 | May absence of detected conflict be reported as universal Consistency? | DIRECTLY_DERIVABLE | No. | The rule covers only declared constructions and exact identities. | Any value or non-conflict output must carry the bounded coverage non-claim. | DIRECTLY_DERIVABLE |

## 13. Deterministic ordering

Deterministic order is scientific reproducibility metadata, not severity or
risk ranking.

The proposed order is:

1. requirements by approved input processing order, preserving source line
   order;
2. each pair earlier requirement first, later requirement second;
3. observation pairs by left observation source order, then right observation
   source order;
4. cross-results by requirement-pair key, observation-pair key, relation type,
   Rule ID, and stable result ID;
5. Evidence references by canonical participant order, then source span start,
   span end, and evidence ID as a tie-breaker; and
6. multiple conflicts involving one requirement remain in the same global
   order; they are not ranked by apparent importance.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D060 | How are requirement pairs ordered? | RESEARCHER_OPERATIONALIZATION | By source/input processing order, earlier participant first. | This order already has stable domain meaning. | Reversed input to the symmetric predicate cannot create a duplicate result. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D061 | How are cross-results ordered? | RESEARCHER_OPERATIONALIZATION | Use the hierarchy in items 1-4 above. | It is reproducible without severity or hash ordering. | Repeated analysis yields stable output ordering. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D062 | How are evidence references ordered? | RESEARCHER_OPERATIONALIZATION | Participant order, then source-span order, then evidence ID. | Explanations read in source order and remain deterministic on ties. | Both participants' evidence is preserved without global ID mutation. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D063 | How are several conflicts involving one requirement prioritized? | SOURCE_DEFINED separation | They are not prioritized; retain the same deterministic global order. | No severity, risk, or priority model is approved. | Ordering must not imply importance. | SOURCE_DEFINED |

## 14. Non-claims

Every v0.1 result, including a computed M_cons, must be accompanied by these
non-claims:

- absence of a detected conflict is not proof of universal semantic
  consistency;
- only the supported bounded quantitative constructions were evaluated;
- confirmed non-conflict applies only to one supported observation pair;
- unsupported semantic equivalence is not inferred;
- no synonym, terminology, ontology, embedding, or fuzzy match is assumed;
- no unit conversion or dimensional equivalence is inferred;
- no context overlap beyond exact normalized identity is inferred;
- no implicit domain or common-sense knowledge is supplied;
- no general logical, terminological, resource, duplication, coverage, or
  traceability claim is made;
- no severity, risk, probability, confidence score, priority, or corrective
  action is inferred;
- no software-product quality or defect-probability conclusion is produced;
- M_cons is not a combined specification-quality score; and
- UNKNOWN and NOT_APPLICABLE are not numeric values and never mean zero.

| Decision ID | Question | Source status | Proposed decision | Rationale | Consequence | Status |
| --- | --- | --- | --- | --- | --- | --- |
| CRA-D064 | Which claims are prohibited? | SOURCE_DEFINED and DIRECTLY_DERIVABLE limits consolidated above | Require the complete non-claim set above with every published v0.1 assessment. | A narrow detector must not be presented as universal semantic analysis. | Reporter design must later preserve these qualifications without changing their meaning. | RESEARCHER_APPROVAL_PROPOSED |
| CRA-D065 | Does a computed value prove the specification is conflict-free? | DIRECTLY_DERIVABLE | No; it quantifies confirmed conflict participation only within the approved coverage. | Unsupported and out-of-scope relations remain unassessed. | Even M_cons = 1 is a bounded observation, not universal proof. | DIRECTLY_DERIVABLE |

## 15. End-of-round report

### Branch

research/cross-requirement-analysis

No new branch was created. Nothing was merged.

### Files created or modified

- Created docs/cross-requirement-consistency-decision-package.md.
- No production code, tests, model specification, current C/V/U contract,
  detector, reporter, or aggregation file was changed.

### Source-defined conclusions

- Consistency is a requirement-set property and covers logical,
  terminological, and resource conflict.
- R_conf is the set of requirements participating in at least one confirmed
  conflict; members are not pairs or findings.
- M_cons = 1 - \|R_conf\| / \|R\|.
- Candidates do not enter R_conf.
- Missing evidence is distinct from negative evidence and from
  non-applicability.
- Quantitative observations preserve metric, comparator, Decimal value, unit,
  context, unresolved components, and Evidence.
- LESS_THAN_OR_EQUAL and GREATER_THAN_OR_EQUAL are inclusive;
  UPPER_BOUND inclusivity is unresolved; NOT_LESS_FREQUENT is distinct.
- No unit conversion is currently approved.
- Duplication and M_unique are separate.
- No scalar specification-quality score is authorized.

### Proposed researcher decisions

The package recommends:

- a pairwise direct quantitative-bound slice;
- exact normalized metric and context identity;
- exact UnitLabel equality and no conversions;
- inclusive lower/upper admissible sets and empty-intersection conflict;
- a four-way result state/applicability distinction;
- deterministic automatic confirmation for this rule after approval;
- a coverage-qualified M_cons[QB-v0.1], never an unqualified full-scope claim;
- strict metric withholding for unresolved extraction or any
  assessment-unresolved comparison;
- mandatory observability metadata;
- compound cross-record Evidence references;
- no retroactive C/V/U effects;
- Option B, a future broader conceptual SpecificationAssessment; and
- stable source-based ordering and explicit non-claims.

### Deferred questions

General logical conflict, terminology, resources/dependencies, semantic
duplication, traceability, coverage, domain knowledge, semantic equivalence,
unit conversion, richer numeric constraints, within-requirement constraint
relations, conflict remediation lifecycle, severity/risk/confidence, product
quality, architecture, persistence, UI/reporting, and implementation all remain
deferred.

### Blockers before binding quantitative reference cases

Binding reference cases remain blocked until the researcher explicitly
approves:

1. the v0.1 scope and pair/observation comparison universe;
2. the state and confirmation model;
3. normalization, metric/context identity, unit, comparator, and value gates;
4. the admissible-set and conflict predicate;
5. UNKNOWN/NOT_APPLICABLE propagation and M_cons computation gates;
6. the cross-result, observation-reference, Evidence, and coverage contracts;
   and
7. the local/specification result boundaries and required non-claims.

After those approvals, the next research-only step should construct full
positive, negative, unresolved, and outside-applicability reference
requirements with exact expected Evidence and traceability. Architecture and
production work remain blocked until that later package is accepted.

### Readiness

This decision package is ready for researcher review. It is not ready for
architecture or implementation because every new operationalization remains
RESEARCHER_APPROVAL_PROPOSED.

## 16. Researcher Approval Checklist

Only the following grouped decisions require explicit researcher approval.
Every item states a recommended default; none is approved by this document.

- [ ] **Scope and analysis universe — CRA-D001, D005-D007.** Approve direct
  pairwise bounded quantitative conflict, unordered source-ordered requirement
  pairs, and all cross-requirement observation pairs. **Recommended default:**
  approve, because this is the narrowest reproducible slice supported by
  current structured data.

- [ ] **Scientific state model — CRA-D011-D013.** Approve
  CONFIRMED_CONFLICT, CONFIRMED_NON_CONFLICT, ASSESSMENT_UNRESOLVED, and
  OUTSIDE_V0_1_APPLICABILITY; keep candidates separate; permit deterministic
  confirmation only for the fully approved rule. **Recommended default:**
  approve, because it prevents candidates and missing evidence from becoming
  facts.

- [ ] **Single-requirement/no-observation behavior — CRA-D019-D021.**
  Approve NOT_APPLICABLE for one requirement or no applicable comparison, and
  preservation of partial R_conf when other comparisons are unresolved.
  **Recommended default:** approve, because returning 1 would imply coverage
  that does not exist.

- [ ] **M_cons execution and claim — CRA-D023-D026, D066-D067.** Approve exact
  Fraction arithmetic, the coverage-qualified M_cons[QB-v0.1] label, strict
  UNKNOWN propagation for unresolved extraction or any
  ASSESSMENT_UNRESOLVED comparison, NOT_APPLICABLE when no comparison applies,
  and mandatory observability metadata. **Recommended default:** approve the
  strict, qualified policy, because incomplete extraction or unresolved pairs
  can change R_conf membership, the conflict coverage is bounded, and
  AGG-MVP-001 is not the same mathematical operation.

- [ ] **Text normalization — CRA-D029.** Approve NFC, case folding, whitespace
  collapse, and trim while preserving all other characters. **Recommended
  default:** approve, because it removes only explicit representation variance
  and introduces no semantic vocabulary.

- [ ] **Metric and context identity — CRA-D030, D032, D036.** Approve exact
  normalized metric and context text plus exact unit label as the complete
  bounded comparison key. **Recommended default:** approve, because anything
  broader requires a separately validated ontology or overlap rule.

- [ ] **Unit, comparator, and value gates — CRA-D033-D035.** Approve exact unit
  equality, only inclusive LESS_THAN_OR_EQUAL/GREATER_THAN_OR_EQUAL, no
  conversion, UPPER_BOUND as unresolved, NOT_LESS_FREQUENT as outside scope,
  and exact Decimal values. **Recommended default:** approve, because these are
  the only semantics currently complete enough for deterministic comparison.

- [ ] **Conflict mathematics — CRA-D037-D038, D041.** Approve the inclusive
  half-line admissible sets, empty-intersection predicate, and Cases A-J as
  decision examples. **Recommended default:** approve, because the predicate
  directly tests simultaneous satisfiability and distinguishes differing
  values from contradictions.

- [ ] **Cross-result contract — CRA-D043, D044, D046.** Approve the minimum
  conceptual fields, the direct quantitative-bound subtype, and qualified
  source-order observation references. **Recommended default:** approve,
  because every result must be reproducible and explainable before a class is
  designed.

- [ ] **Evidence contract — CRA-D048, D050.** Approve
  (requirement_id, evidence_id) references and the five cross-record validation
  invariants. **Recommended default:** approve, because existing Evidence IDs
  are intentionally local and should not be mutated.

- [ ] **Local-quality boundary — CRA-D051-D052.** Approve no retroactive
  changes to C_i, V_i, or U_i and a separate specification-level Consistency
  result. **Recommended default:** approve, because no source provides a local
  contribution rule for cross-conflicts.

- [ ] **Specification boundary — CRA-D054.** Select Option B: a future broader
  conceptual SpecificationAssessment that composes the unchanged C/V/U profile
  with separate set-level assessments. **Recommended default:** Option B,
  because it preserves the accepted profile while allowing heterogeneous
  set-level evidence and states.

- [ ] **UNKNOWN/applicability boundary — CRA-D056-D058.** Approve unresolved
  required inputs as ASSESSMENT_UNRESOLVED and resolved key mismatches as
  OUTSIDE_V0_1_APPLICABILITY, never as confirmed non-conflict.
  **Recommended default:** approve, because it preserves the difference
  between unavailable knowledge and a rule that does not apply.

- [ ] **Deterministic order — CRA-D060-D062.** Approve source-order
  requirement pairs, observation-pair result ordering, and participant/span
  Evidence ordering. **Recommended default:** approve, because it is stable,
  explainable, and does not imply severity.

- [ ] **Required non-claims — CRA-D064.** Approve publication of the complete
  bounded-coverage non-claim set with every v0.1 assessment. **Recommended
  default:** approve, because the narrow slice cannot support a universal
  semantic Consistency claim.
