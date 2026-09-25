# QB-v0.1 Binding Quantitative Reference Cases

- **Branch:** research/cross-requirement-analysis
- **Research phase:** BINDING_QUANTITATIVE_REFERENCE_CASE_RESEARCH
- **Scientific authority:** the researcher-approved
  cross-requirement-consistency-decision-package.md, approval date 2026-09-25
- **Document status:** PROPOSED_BINDING_CORPUS_FOR_RESEARCHER_APPROVAL
- **Implementation effect:** none
- **Production change authorization:** none

## 1. Purpose and binding boundary

This corpus defines expected scientific results for the approved QB-v0.1
bounded quantitative-bound Consistency contract. It validates, as far as the
frozen extractor permits, the path:

    requirement text
    -> current quantitative extraction
    -> bounded identity/applicability
    -> cross-result state
    -> R_conf[QB-v0.1]
    -> M_cons[QB-v0.1]

The corpus does not define Python classes, modules, services, interfaces,
reporter layouts, or production Rule IDs. It does not change the approved
science.

### 1.1 Binding-status vocabulary

- **BINDING_END_TO_END_REFERENCE_CASE:** requirement text and every expected
  quantitative extraction detail were verified against the current production
  QuantitativeBaselineDetector. The reader IDs follow the current
  RequirementReader contract.
- **BINDING_DOMAIN_CONTRACT_REFERENCE_CASE:** the case begins from an explicit
  domain observation/evidence projection because the current extractor cannot
  emit all required resolved components. It binds cross-analysis science, not
  text extraction.
- **ILLUSTRATIVE_ONLY:** explanatory material that is not a test oracle.
- **REJECTED_FIXTURE:** an attempted text fixture whose observed extraction
  does not meet its intended scientific purpose.

Only the first two statuses are binding.

### 1.2 Approved states and aggregate values

The only cross states/dispositions used here are:

- CONFIRMED_CONFLICT;
- COMPATIBLE_WITHIN_RULE;
- ASSESSMENT_UNRESOLVED; and
- OUTSIDE_V0_1_APPLICABILITY.

The only aggregate states used here are COMPUTED, UNKNOWN, and NOT_APPLICABLE.
COMPUTED values are exact reduced Fraction values. UNKNOWN and NOT_APPLICABLE
have no numeric value.

The full source-level M_cons remains non-executable. Every executable numeric
result in this corpus is:

    M_cons[QB-v0.1] = 1 - |R_conf[QB-v0.1]| / |R|

### 1.3 Common bounded non-claim

Every binding case incorporates non-claim NC-QB-BASE:

> The result describes only QB-v0.1 supported quantitative observations under
> the approved exact bounded identity and comparison rule. It does not prove
> universal logical, terminological, resource, semantic, or specification
> Consistency; infer synonymy, context overlap, unit conversion, risk,
> severity, probability, corrective action, or product quality; or produce an
> overall specification-quality score.

COMPATIBLE_WITHIN_RULE means joint satisfiability only under the one cited
QB-v0.1 comparison. M_cons[QB-v0.1] = 1 retains NC-QB-BASE.

## 2. Frozen extractor verification

### 2.1 Verification method

The following current tests were executed without source changes:

    .venv/Scripts/python.exe -m pytest -q
        tests/test_quantitative_detector.py
        tests/test_quantitative_metric_detector.py
        tests/test_quantitative_context_detector.py

Result:

    121 passed

Additional read-only exploratory calls invoked QuantitativeBaselineDetector
directly with the exact texts catalogued below. No exploratory file was
committed.

### 2.2 Binding extractor findings

The frozen baseline has four consequences for this corpus:

1. QUANT-METRIC-001 attaches metric Evidence only to the exact prefix
   Час відгуку followed by one eligible symbolic LESS_THAN_OR_EQUAL bound.
2. QUANT-CONTEXT-001 attaches context Evidence only to the exact suffix
   при 500 одночасних користувачах.
3. The numeric token 500 in that accepted context also produces
   QUANT_UNRESOLVED_NUMERIC_CANDIDATE, so the quantitative outcome is
   INCOMPLETE even though the linked observation has metric and context.
4. GREATER_THAN_OR_EQUAL, UPPER_BOUND, and the protected frequency construction
   do not receive the required linked metric/context under the current
   detector.

Therefore no current text fixture can simultaneously provide:

- a complete resolved metric;
- a complete resolved context;
- a supported lower bound; and
- resolved quantitative extraction.

No current text fixture can produce a COMPUTED M_cons[QB-v0.1] through the full
end-to-end path. This is an observed baseline limitation, not a reopened
scientific decision. Computed, conflict, normalization, resolved-context
inequality, and NOT_LESS_FREQUENT branches are consequently bound at the domain
contract boundary.

End-to-end cases still bind exact extraction, observable cross-results, strict
UNKNOWN propagation, and NOT_APPLICABLE behavior.

## 3. Fixture conventions and reusable extraction records

### 3.1 Reader and offset conventions

Each input block represents one UTF-8 file with one listed requirement per
physical line and no hidden blank lines. The first non-empty line is R001,
the second is R002, and so on; source_line equals the displayed line number.
Offsets are zero-based half-open Unicode code-point intervals [start,end).

For current-extractor Evidence, the evidence ID and Rule ID are shown exactly.
For domain-contract projections, M, B, and C are fixture-local Evidence IDs for
metric, bound, and context. A cross reference is always qualified, for example
(R001,M). Fixture-local IDs are not proposed production IDs.

### 3.2 Observability metadata notation

Every case supplies the following ordered tuple:

    META(
      N_R, N_Rq, N_Ra, N_P, N_Q,
      N_A, N_C, N_W, N_U, N_O, N_X,
      N_Rconf, Rconf_complete
    )

where:

- N_R = total_requirement_count;
- N_Rq = requirements_with_quantitative_observations_count;
- N_Ra = requirements_participating_in_applicable_comparisons_count;
- N_P = total_requirement_pair_count;
- N_Q = total_observation_pair_count considered;
- N_A = applicable_comparison_count;
- N_C = confirmed_conflict_count;
- N_W = compatible_within_rule_count;
- N_U = assessment_unresolved_count;
- N_O = outside_applicability_count;
- N_X = unresolved_quantitative_extraction_count;
- N_Rconf = observed |R_conf[QB-v0.1]|; and
- Rconf_complete states whether the observed bounded set is complete.

For every row:

    N_Q = N_C + N_W + N_U + N_O
    N_A = N_C + N_W
    analysis_contract = QB-v0.1 / CRA-D037-D038
    coverage_profile = QB-v0.1

These are scientific metadata names for this corpus, not production field
names or a production Rule ID.

### 3.3 Verified end-to-end extraction templates

The following records are exact current-detector outputs. Component references
use the Evidence IDs in the same row.

| Template | Requirement text | Processing/status | Evidence and diagnostic spans | Observation |
| --- | --- | --- | --- | --- |
| E-U2-S-C | Час відгуку ≤ 2 с при 500 одночасних користувачах | INCOMPLETE / DETECTED | QUANT-METRIC-001:E001 = Час відгуку [0,11); QUANT-001:E001 = ≤ 2 с [12,17); QUANT-CONTEXT-001:E001 = при 500 одночасних користувачах [18,49); diagnostic 500 [22,25) | metric ref QUANT-METRIC-001:E001; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; context ref QUANT-CONTEXT-001:E001; unresolved_components=() |
| E-U5-S-C | Час відгуку ≤ 5 с при 500 одночасних користувачах | INCOMPLETE / DETECTED | QUANT-METRIC-001:E001 = Час відгуку [0,11); QUANT-001:E001 = ≤ 5 с [12,17); QUANT-CONTEXT-001:E001 = при 500 одночасних користувачах [18,49); diagnostic 500 [22,25) | metric ref QUANT-METRIC-001:E001; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("5"); SECOND; context ref QUANT-CONTEXT-001:E001; unresolved_components=() |
| E-U1-M-C | Час відгуку ≤ 1 хв при 500 одночасних користувачах | INCOMPLETE / DETECTED | QUANT-METRIC-001:E001 = Час відгуку [0,11); QUANT-001:E001 = ≤ 1 хв [12,18); QUANT-CONTEXT-001:E001 = при 500 одночасних користувачах [19,50); diagnostic 500 [23,26) | metric ref QUANT-METRIC-001:E001; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("1"); MINUTE; context ref QUANT-CONTEXT-001:E001; unresolved_components=() |
| E-U2-S-NC | Час відгуку ≤ 2 с | COMPLETE / DETECTED | QUANT-METRIC-001:E001 = Час відгуку [0,11); QUANT-001:E001 = ≤ 2 с [12,17) | metric ref METRIC:E001; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; context=None; unresolved_components=() |
| E-U5-S-NC | Час відгуку ≤ 5 с | COMPLETE / DETECTED | QUANT-METRIC-001:E001 = Час відгуку [0,11); QUANT-001:E001 = ≤ 5 с [12,17) | metric ref METRIC:E001; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("5"); SECOND; context=None; unresolved_components=() |
| E-U2-S-NM | ≤ 2 с | COMPLETE / DETECTED | QUANT-001:E001 = ≤ 2 с [0,5) | metric=None; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; context=None; unresolved_components=() |
| E-U5-S-NM | ≤ 5 с | COMPLETE / DETECTED | QUANT-001:E001 = ≤ 5 с [0,5) | metric=None; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("5"); SECOND; context=None; unresolved_components=() |
| E-UPPER | до 300 | COMPLETE / DETECTED | QUANT-UK-001:E001 = до 300 [0,6) | metric=None; UPPER_BOUND/UNRESOLVED; Decimal("300"); unit=None; context=None; unresolved_components=() |
| E-MULTI | Час відгуку ≤ 2 с та ≤ 5 с | COMPLETE / DETECTED | QUANT-001:E001 = ≤ 2 с [12,17); QUANT-001:E002 = ≤ 5 с [21,26) | two observations in source order; each has metric=None/context=None; values Decimal("2") and Decimal("5"); SECOND |
| E-U3-S-NM | ≤ 3 с | COMPLETE / DETECTED | QUANT-001:E001 = ≤ 3 с [0,5) | metric=None; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("3"); SECOND; context=None |
| E-NONE-1 | Система формує звіт. | COMPLETE / NOT_DETECTED | no quantitative Evidence; no diagnostic | no observation |
| E-NONE-2 | Система зберігає журнал. | COMPLETE / NOT_DETECTED | no quantitative Evidence; no diagnostic | no observation |
| E-X95 | Система використовує профіль 95. | INCOMPLETE / UNRESOLVED | no quantitative Evidence; QUANT_UNRESOLVED_NUMERIC_CANDIDATE = 95 [29,31) | no observation |

For the first three templates, the observation top-level Evidence references
are ordered metric, scalar, context. The exact cross references for an
instantiation owned by R001 are therefore:

    (R001,QUANT-METRIC-001:E001)
    (R001,QUANT-001:E001)
    (R001,QUANT-CONTEXT-001:E001)

### 3.4 Binding domain-projection templates

These templates are deliberately not claims about current detector output.
They bind the cross-analysis input contract using fixture-local Evidence. All
listed components are resolved unless marked unresolved.

| Template | Requirement text and exact Evidence | Accepted observation |
| --- | --- | --- |
| D-U2-S | Час відгуку ≤ 2 с при 500 одночасних користувачах; M=Час відгуку [0,11), B=≤ 2 с [12,17), C=при 500 одночасних користувачах [18,49) | metric Час відгуку; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; context при 500 одночасних користувачах |
| D-U5-S | Час відгуку ≤ 5 с при 500 одночасних користувачах; M [0,11), B=≤ 5 с [12,17), C [18,49) | same key; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("5"); SECOND |
| D-U1-S | Час відгуку ≤ 1 с при 500 одночасних користувачах; M [0,11), B=≤ 1 с [12,17), C [18,49) | same key; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("1"); SECOND |
| D-U1-M | Час відгуку ≤ 1 хв при 500 одночасних користувачах; M [0,11), B=≤ 1 хв [12,18), C=при 500 одночасних користувачах [19,50) | metric/context as above; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("1"); MINUTE |
| D-L5-S | Час відгуку не нижче 5 с при 500 одночасних користувачах; M [0,11), B=не нижче 5 с [12,24), C=при 500 одночасних користувачах [25,56) | metric/context as above; GREATER_THAN_OR_EQUAL/INCLUSIVE; Decimal("5"); SECOND |
| D-L2-S | Час відгуку не нижче 2 с при 500 одночасних користувачах; M [0,11), B=не нижче 2 с [12,24), C [25,56) | same key; GREATER_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND |
| D-SYN-U2 | Час відповіді ≤ 2 с при 500 одночасних користувачах; M=Час відповіді [0,13), B [14,19), C [20,51) | normalized metric час відповіді; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; standard context |
| D-CTX-U2 | Час відгуку ≤ 2 с під час пікового навантаження; M [0,11), B [12,17), C=під час пікового навантаження [18,47) | normalized metric час відгуку; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; normalized context під час пікового навантаження |
| D-FREQ | Час відгуку не рідше одного разу на 5 с при 500 одночасних користувачах; M [0,11), B=не рідше одного разу на 5 с [12,39), C [40,71) | standard metric/context; NOT_LESS_FREQUENT; Decimal("5"); SECOND |
| D-UNRES-M | ≤ 2 с при 500 одночасних користувачах; B [0,5), C [6,37) | metric=None with unresolved METRIC; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; standard context |
| D-UNRES-C | Час відгуку ≤ 2 с; M [0,11), B [12,17) | standard metric; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND; context=None with unresolved CONTEXT |
| D-NORM-1 | ЧАС  ДІЙ ≤ 2 с ПІД ЧАС  ДІЙ; M=ЧАС  ДІЙ [0,8), B [9,14), C=ПІД ЧАС  ДІЙ [15,27) | N(metric)=час дій; N(context)=під час дій; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("2"); SECOND |
| D-NORM-2 | час дій ≤ 5 с під час дій, where й is decomposed; M=час дій [0,8), B [9,14), C=під час дій [15,27) | N(metric)=час дій; N(context)=під час дій; LESS_THAN_OR_EQUAL/INCLUSIVE; Decimal("5"); SECOND |
| D-NONE | Система формує звіт. | quantitative extraction COMPLETE/NOT_DETECTED; no observation |

For any instantiation, the observation Evidence union is the ordered tuple of
its populated M, B, and C IDs. Cross-result Evidence is the participant-
qualified sequence (requirement_id,evidence_id), participant first, then span.

## 4. Binding reference cases

Unless a case says otherwise:

- requirement and observation order is source order;
- the comparison key is
  (normalized metric, normalized context, exact UnitLabel);
- the conflict subtype is DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY only for a
  CONFIRMED_CONFLICT; all other states have no confirmed conflict subtype;
- domain projections have resolved extraction, so N_X=0;
- result IDs below are corpus IDs, not production identifiers; and
- NC-QB-BASE applies.

For every case, the **Expected cross-result(s)** entry is also the binding
identity/applicability decision. Each named pair is the exact canonical
participant-ID tuple retained by that cross-result, regardless of state. The
confirmed conflict subtype is
DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY only where the state is
CONFIRMED_CONFLICT; otherwise it is absent. Template references bind all
listed normalized metric/context, UnitLabel, comparator, Decimal value, and
Evidence fields without repeating their span table in every case.

### RC-QB-001 — simple incompatible bounds

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** primary positive conflict; approved analogue of x <= 2 and
  x >= 5.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-L5-S.
- **Expected observations/Evidence:** instantiate both domain templates with
  owner-qualified refs (R001,M/B/C) and (R002,M/B/C). Both normalize to metric
  час відгуку, context при 500 одночасних користувачах, UnitLabel SECOND;
  comparators are LESS_THAN_OR_EQUAL and GREATER_THAN_OR_EQUAL; values are
  Decimal("2") and Decimal("5").
- **Identity/applicability:** keys equal; comparison applicable.
- **Expected cross-result:** XR-RC-QB-001-001, participants (R001,R002),
  CONFIRMED_CONFLICT, subtype DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY.
  The admissible sets (-infinity,2] and [5,+infinity) have empty intersection.
- **Expected bounded set/aggregate:** R_conf[QB-v0.1]={R001,R002};
  aggregate COMPUTED; M_cons[QB-v0.1]=Fraction(0,1).
- **Metadata:** META(2,2,2,1,1,1,1,0,0,0,0,2,true).
- **Rationale/traceability:** CRA-D001, D005-D007, D011-D012, D015-D017,
  D022-D024, D026, D033-D038, D043-D050, D060-D062, D066.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-002 — reversed source ordering

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** prove that lower-bound-first source order changes only canonical
  participant orientation.
- **Input requirement set:** line 1/R001 = D-L5-S; line 2/R002 = D-U2-S.
- **Expected observations/Evidence:** R001 owns D-L5-S refs and R002 owns
  D-U2-S refs; normalized keys are identical; values are exact Decimal("5")
  and Decimal("2").
- **Identity/applicability:** applicable; canonical pair is (R001,R002).
- **Expected cross-result:** XR-RC-QB-002-001, participants (R001,R002),
  CONFIRMED_CONFLICT with the same empty-intersection proof as RC-QB-001.
- **Expected bounded set/aggregate:** R_conf[QB-v0.1]={R001,R002};
  COMPUTED; M_cons[QB-v0.1]=Fraction(0,1).
- **Metadata:** META(2,2,2,1,1,1,1,0,0,0,0,2,true).
- **Rationale/traceability:** CRA-D005-D006, D011-D012, D016-D017,
  D037-D038, D060-D062.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-003 — shared requirement in overlapping conflicts

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** prove set semantics when one requirement participates in two
  conflicts.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-L5-S;
  line 3/R003 = D-U1-S.
- **Expected observations/Evidence:** one resolved observation per requirement
  with owner-qualified M/B/C refs; all keys normalize to
  (час відгуку, при 500 одночасних користувачах, SECOND).
- **Expected cross-results, in order:**
  1. XR-RC-QB-003-001 (R001,R002) = CONFIRMED_CONFLICT;
  2. XR-RC-QB-003-002 (R001,R003) = COMPATIBLE_WITHIN_RULE because two upper
     half-lines intersect; and
  3. XR-RC-QB-003-003 (R002,R003) = CONFIRMED_CONFLICT.
- **Expected bounded set/aggregate:** set union yields
  R_conf[QB-v0.1]={R001,R002,R003}; R002 is counted once, not twice;
  COMPUTED; M_cons[QB-v0.1]=Fraction(0,1).
- **Metadata:** META(3,3,3,3,3,3,2,1,0,0,0,3,true).
- **Rationale/traceability:** CRA-D007, D015-D017, D021-D024, D037-D040,
  D060-D061.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-004 — overlapping inclusive upper and lower bounds

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** prove that differing numbers do not imply conflict.
- **Input requirement set:** line 1/R001 = D-U5-S; line 2/R002 = D-L2-S.
- **Expected observations/Evidence:** resolved owner-qualified D-U5-S and
  D-L2-S projections; identical normalized key; exact Decimal("5") and
  Decimal("2").
- **Identity/applicability:** applicable.
- **Expected cross-result:** XR-RC-QB-004-001 (R001,R002) =
  COMPATIBLE_WITHIN_RULE because (-infinity,5] intersects [2,+infinity) on
  [2,5]. No confirmed conflict subtype or participants are emitted.
- **Expected bounded set/aggregate:** R_conf[QB-v0.1]=empty set; COMPUTED;
  M_cons[QB-v0.1]=Fraction(1,1).
- **Metadata:** META(2,2,2,1,1,1,0,1,0,0,0,0,true).
- **Rationale/traceability:** CRA-D011, D033-D040, D041 Case B.
- **Bounded non-claim:** NC-QB-BASE; the requirements are not declared
  universally consistent.

### RC-QB-005 — current-extractor same-key upper bounds

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind exact context identity, same-unit identity, an observed
  COMPATIBLE_WITHIN_RULE result, and strict extraction-uncertainty propagation.
- **Input requirement set:** line 1/R001 = E-U2-S-C; line 2/R002 = E-U5-S-C.
- **Expected extraction/Evidence:** exact E-U2-S-C and E-U5-S-C rows in
  Section 3.3, including owner-qualified metric/scalar/context Evidence and
  diagnostic 500 for each requirement.
- **Normalized key:** both observations =
  (час відгуку, при 500 одночасних користувачах, SECOND).
- **Expected cross-result:** XR-RC-QB-005-001 (R001,R002) =
  COMPATIBLE_WITHIN_RULE; two upper half-lines intersect.
- **Expected bounded set/aggregate:** observed partial
  R_conf[QB-v0.1]=empty set, Rconf_complete=false; aggregate UNKNOWN;
  M_cons[QB-v0.1] absent because N_X=2.
- **Metadata:** META(2,2,2,1,1,1,0,1,0,0,2,0,false).
- **Rationale/traceability:** CRA-D007, D011, D021, D024, D026, D030,
  D032-D037, D039, D067.
- **Bounded non-claim:** NC-QB-BASE; the observed compatible result does not
  override incomplete extraction.

### RC-QB-006 — two supported lower bounds

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind same-direction GREATER_THAN_OR_EQUAL behavior.
- **Input requirement set:** line 1/R001 = D-L5-S; line 2/R002 = D-L2-S.
- **Expected observations/Evidence:** resolved D-L5-S and D-L2-S projections;
  same normalized key and SECOND; exact values Decimal("5") and Decimal("2").
- **Expected cross-result:** XR-RC-QB-006-001 (R001,R002) =
  COMPATIBLE_WITHIN_RULE because [5,+infinity) and [2,+infinity) intersect.
- **Expected bounded set/aggregate:** empty R_conf[QB-v0.1]; COMPUTED;
  M_cons[QB-v0.1]=Fraction(1,1).
- **Metadata:** META(2,2,2,1,1,1,0,1,0,0,0,0,true).
- **Rationale/traceability:** CRA-D034, D037, D039, D041 Case D.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-007 — shared inclusive endpoint

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind inclusive endpoint semantics.
- **Input requirement set:** line 1/R001 = D-U5-S; line 2/R002 = D-L5-S.
- **Expected observations/Evidence:** resolved template projections with equal
  key and Decimal("5") on both sides.
- **Expected cross-result:** XR-RC-QB-007-001 (R001,R002) =
  COMPATIBLE_WITHIN_RULE because value 5 satisfies both constraints.
- **Expected bounded set/aggregate:** empty R_conf[QB-v0.1]; COMPUTED;
  M_cons[QB-v0.1]=Fraction(1,1).
- **Metadata:** META(2,2,2,1,1,1,0,1,0,0,0,0,true).
- **Rationale/traceability:** CRA-D034, D037-D040, D041 shared-endpoint case.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-008 — representation-only identity normalization

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind NFC, case-folding, Unicode-whitespace collapse, and trim.
- **Input requirement set:** line 1/R001 = D-NORM-1; line 2/R002 = D-NORM-2.
- **Expected observations/Evidence:** exact spans from Section 3.4.
  N(metric)=час дій and N(context)=під час дій on both sides despite case,
  repeated spaces, and decomposed й. Both units are SECOND; values are exact
  Decimal("2") and Decimal("5").
- **Identity/applicability:** keys equal; applicable.
- **Expected cross-result:** XR-RC-QB-008-001 =
  COMPATIBLE_WITHIN_RULE because both are upper bounds.
- **Expected bounded set/aggregate:** empty R_conf[QB-v0.1]; COMPUTED;
  M_cons[QB-v0.1]=Fraction(1,1).
- **Metadata:** META(2,2,2,1,1,1,0,1,0,0,0,0,true).
- **Rationale/traceability:** CRA-D029-D032, D036, D039.
- **Bounded non-claim:** NC-QB-BASE; normalization establishes textual identity
  only, not general semantic equivalence.

### RC-QB-009 — semantic metric synonym is outside

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** prohibit synonym inference.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-SYN-U2.
- **Expected observations/Evidence:** exact template spans and qualified refs.
  Normalized metrics are час відгуку and час відповіді; contexts and units
  match.
- **Identity/applicability:** resolved metric inequality makes the pair
  OUTSIDE_V0_1_APPLICABILITY.
- **Expected cross-result:** XR-RC-QB-009-001 = OUTSIDE_V0_1_APPLICABILITY;
  not COMPATIBLE_WITHIN_RULE and no confirmed subtype/participants.
- **Expected bounded set/aggregate:** empty complete R_conf[QB-v0.1];
  NOT_APPLICABLE; no numeric M_cons[QB-v0.1].
- **Metadata:** META(2,2,0,1,1,0,0,0,0,1,0,0,true).
- **Rationale/traceability:** CRA-D025, D029-D031, D036, D057.
- **Bounded non-claim:** NC-QB-BASE; no synonym relation is inferred.

### RC-QB-010 — resolved different contexts are outside

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind exact context identity and prohibit inferred overlap.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-CTX-U2.
- **Expected observations/Evidence:** exact domain template spans. Normalized
  contexts are при 500 одночасних користувачах and
  під час пікового навантаження; metric and unit match.
- **Expected cross-result:** XR-RC-QB-010-001 =
  OUTSIDE_V0_1_APPLICABILITY, not COMPATIBLE_WITHIN_RULE.
- **Expected bounded set/aggregate:** empty complete R_conf[QB-v0.1];
  NOT_APPLICABLE; no numeric metric.
- **Metadata:** META(2,2,0,1,1,0,0,0,0,1,0,0,true).
- **Rationale/traceability:** CRA-D025, D032, D036, D057.
- **Bounded non-claim:** NC-QB-BASE; context overlap is not inferred.

### RC-QB-011 — current-extractor different units

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind no-conversion behavior under actual extraction and strict
  extraction-uncertainty propagation.
- **Input requirement set:** line 1/R001 = E-U2-S-C; line 2/R002 = E-U1-M-C.
- **Expected extraction/Evidence:** exact Section 3.3 templates, including
  diagnostics 500 [22,25) and 500 [23,26).
- **Identity/applicability:** metric/context match; SECOND differs from MINUTE;
  OUTSIDE_V0_1_APPLICABILITY. No 60-second/1-minute conversion is attempted.
- **Expected cross-result:** XR-RC-QB-011-001 =
  OUTSIDE_V0_1_APPLICABILITY, not COMPATIBLE_WITHIN_RULE.
- **Expected bounded set/aggregate:** observed empty
  R_conf[QB-v0.1], incomplete; UNKNOWN with no metric because N_X=2.
- **Metadata:** META(2,2,0,1,1,0,0,0,0,1,2,0,false).
- **Rationale/traceability:** CRA-D024, D026, D033, D036, D057, D067.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-012 — resolved different units with no applicable comparison

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind aggregate NOT_APPLICABLE when the only resolved observation
  pair is outside due to UnitLabel inequality.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-U1-M.
- **Expected observations/Evidence:** exact domain template spans; identical
  normalized metric/context; SECOND versus MINUTE.
- **Expected cross-result:** XR-RC-QB-012-001 =
  OUTSIDE_V0_1_APPLICABILITY.
- **Expected bounded set/aggregate:** empty complete R_conf[QB-v0.1];
  NOT_APPLICABLE; M_cons[QB-v0.1] absent.
- **Metadata:** META(2,2,0,1,1,0,0,0,0,1,0,0,true).
- **Rationale/traceability:** CRA-D020, D025, D033, D057.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-013 — accepted observations with missing metric

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind missing-metric handling from current extraction.
- **Input requirement set:** line 1/R001 = E-U2-S-NM; line 2/R002 = E-U5-S-NM.
- **Expected extraction/Evidence:** each requirement has exactly one
  QUANT-001:E001 bound Evidence [0,5), COMPLETE/DETECTED, metric=None and
  context=None.
- **Identity/applicability:** metric identity cannot be established;
  ASSESSMENT_UNRESOLVED. Missing metric is not a resolved mismatch.
- **Expected cross-result:** XR-RC-QB-013-001 =
  ASSESSMENT_UNRESOLVED with reasons MISSING_METRIC and MISSING_CONTEXT; no
  confirmed subtype/participants.
- **Expected bounded set/aggregate:** observed empty partial
  R_conf[QB-v0.1]; UNKNOWN; numeric metric absent.
- **Metadata:** META(2,2,0,1,1,0,0,0,1,0,0,0,false).
- **Rationale/traceability:** CRA-D013, D024, D030, D032, D056, D058.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-014 — linked metric with missing context

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind the rule that missing context is not global context.
- **Input requirement set:** line 1/R001 = E-U2-S-NC; line 2/R002 = E-U5-S-NC.
- **Expected extraction/Evidence:** exact Section 3.3 templates;
  COMPLETE/DETECTED; normalized metric час відгуку; context=None.
- **Identity/applicability:** context identity cannot be established;
  ASSESSMENT_UNRESOLVED.
- **Expected cross-result:** XR-RC-QB-014-001 =
  ASSESSMENT_UNRESOLVED with reason MISSING_CONTEXT.
- **Expected bounded set/aggregate:** observed empty partial bounded set;
  UNKNOWN; no M_cons[QB-v0.1].
- **Metadata:** META(2,2,0,1,1,0,0,0,1,0,0,0,false).
- **Rationale/traceability:** CRA-D013, D024, D032, D056, D058.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-015 — explicit unresolved metric and context components

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind explicit component-level uncertainty, which the current
  detector representation supports but does not currently emit.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-UNRES-M;
  line 3/R003 = D-UNRES-C.
- **Expected observations/Evidence:** exact Section 3.4 spans. R002 has
  unresolved_components=(METRIC); R003 has
  unresolved_components=(CONTEXT). All values/comparators/units are otherwise
  resolved.
- **Expected cross-results:** all three canonical pairs are
  ASSESSMENT_UNRESOLVED. R001-R002 cites UNRESOLVED_METRIC; R001-R003 cites
  UNRESOLVED_CONTEXT; R002-R003 cites both.
- **Expected bounded set/aggregate:** observed empty partial
  R_conf[QB-v0.1]; UNKNOWN; no numeric metric.
- **Metadata:** META(3,3,0,3,3,0,0,0,3,0,0,0,false).
- **Rationale/traceability:** CRA-D007, D013, D024, D030, D032, D056, D058.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-016 — unresolved UPPER_BOUND inclusivity

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind current UPPER_BOUND/UNRESOLVED extraction and prohibit
  implicit inclusive interpretation.
- **Input requirement set:** line 1/R001 = E-UPPER; line 2/R002 = E-U2-S-NM.
- **Expected extraction/Evidence:** R001 QUANT-UK-001:E001 = до 300 [0,6),
  UPPER_BOUND/UNRESOLVED, Decimal("300"), unit=None; R002 exact E-U2-S-NM.
  Both outcomes are COMPLETE/DETECTED.
- **Expected cross-result:** XR-RC-QB-016-001 =
  ASSESSMENT_UNRESOLVED, with unresolved comparator semantics plus missing
  identity/unit inputs. UPPER_BOUND is never mapped to LESS_THAN_OR_EQUAL.
- **Expected bounded set/aggregate:** observed empty partial bounded set;
  UNKNOWN; no numeric metric.
- **Metadata:** META(2,2,0,1,1,0,0,0,1,0,0,0,false).
- **Rationale/traceability:** CRA-D013, D024, D034, D056, D058.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-017 — NOT_LESS_FREQUENT is outside

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind the unsupported comparator-class disposition.
- **Input requirement set:** line 1/R001 = D-FREQ; line 2/R002 = D-U5-S.
- **Expected observations/Evidence:** exact Section 3.4 projections; equal
  normalized metric/context/unit; R001 comparator NOT_LESS_FREQUENT with
  Decimal("5"), R002 LESS_THAN_OR_EQUAL with Decimal("5").
- **Expected cross-result:** XR-RC-QB-017-001 =
  OUTSIDE_V0_1_APPLICABILITY before interval construction.
- **Expected bounded set/aggregate:** empty complete bounded set;
  NOT_APPLICABLE; no numeric metric.
- **Metadata:** META(2,2,0,1,1,0,0,0,0,1,0,0,true).
- **Rationale/traceability:** CRA-D025, D034, D057.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-018 — multiple accepted observations in one requirement

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind source-ordered Cartesian comparison and prohibit a
  within-requirement relation.
- **Input requirement set:** line 1/R001 = E-MULTI; line 2/R002 = E-U3-S-NM.
- **Expected extraction/Evidence:** R001 has QUANT-001:E001 [12,17) and
  QUANT-001:E002 [21,26), values Decimal("2") and Decimal("5"); R002 has
  QUANT-001:E001 [0,5), value Decimal("3"). All are SECOND and
  COMPLETE/DETECTED, with metric/context missing.
- **Expected cross-results:** exactly two, ordered by R001 observation order:
  XR-RC-QB-018-001 compares 2 with 3 and XR-RC-QB-018-002 compares 5 with 3;
  both are ASSESSMENT_UNRESOLVED. No R001-observation-1 versus
  R001-observation-2 result exists.
- **Expected bounded set/aggregate:** observed empty partial bounded set;
  UNKNOWN; no numeric metric.
- **Metadata:** META(2,2,0,1,2,0,0,0,2,0,0,0,false).
- **Rationale/traceability:** CRA-D007-D008, D013, D024, D046, D056,
  D060-D062.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-019 — three requirements, all applicable and compatible

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind the computed aggregate value 1 without making a universal
  Consistency claim.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-U5-S;
  line 3/R003 uses D-U1-S with Decimal("8") and bound Evidence ≤ 8 с at
  [12,17), all other spans unchanged.
- **Expected observations/Evidence:** three resolved upper bounds with identical
  normalized metric/context/unit. The R003 exact source text is
  Час відгуку ≤ 8 с при 500 одночасних користувачах; M [0,11), B [12,17),
  C [18,49).
- **Expected cross-results:** canonical pairs (R001,R002), (R001,R003), and
  (R002,R003) are each COMPATIBLE_WITHIN_RULE.
- **Expected bounded set/aggregate:** R_conf[QB-v0.1]=empty set; COMPUTED;
  M_cons[QB-v0.1]=Fraction(1,1).
- **Metadata:** META(3,3,3,3,3,3,0,3,0,0,0,0,true).
- **Rationale/traceability:** CRA-D015-D017, D022-D026, D039, D060-D061,
  D065-D066.
- **Bounded non-claim:** NC-QB-BASE is mandatory even though the exact bounded
  value is 1.

### RC-QB-020 — one conflict pair among three requirements

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind exact Fraction(1,3) with all non-conflict comparisons
  deterministically outside rather than unresolved.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-L5-S;
  line 3/R003 = D-U1-M.
- **Expected observations/Evidence:** exact domain template spans. R001/R002
  share the complete SECOND key; R003 has MINUTE.
- **Expected cross-results:** (R001,R002)=CONFIRMED_CONFLICT;
  (R001,R003)=OUTSIDE_V0_1_APPLICABILITY; and
  (R002,R003)=OUTSIDE_V0_1_APPLICABILITY.
- **Expected bounded set/aggregate:** R_conf[QB-v0.1]={R001,R002}; COMPUTED;
  M_cons[QB-v0.1]=1-2/3=Fraction(1,3).
- **Metadata:** META(3,3,2,3,3,1,1,0,0,2,0,2,true).
- **Rationale/traceability:** CRA-D015-D017, D022-D026, D033, D038, D057.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-021 — conflict plus isolated non-quantitative requirement

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** prove that the denominator is all reader-accepted requirements,
  not only requirements with observations.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-L5-S;
  line 3/R003 = D-NONE.
- **Expected observations/Evidence:** R001/R002 are resolved templates; R003
  has COMPLETE/NOT_DETECTED quantitative extraction and no Evidence or
  observation.
- **Expected cross-results:** only (R001,R002)=CONFIRMED_CONFLICT. Requirement
  pairs involving R003 contribute zero observation pairs, not unresolved
  results.
- **Expected bounded set/aggregate:** R_conf[QB-v0.1]={R001,R002}; denominator
  |R|=3; COMPUTED; M_cons[QB-v0.1]=Fraction(1,3).
- **Metadata:** META(3,2,2,3,1,1,1,0,0,0,0,2,true).
- **Rationale/traceability:** CRA-D019-D026, D067.
- **Bounded non-claim:** NC-QB-BASE; R003 is counted in the denominator without
  being declared semantically consistent.

### RC-QB-022 — confirmed conflict plus material unresolved comparisons

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind strict UNKNOWN propagation while preserving an observed
  partial conflict-participant set.
- **Input requirement set:** line 1/R001 = D-U2-S; line 2/R002 = D-L5-S;
  line 3/R003 is D-UNRES-C with bound Decimal("1").
- **Expected observations/Evidence:** R001/R002 resolved; R003 metric and bound
  Evidence follow D-UNRES-C, value Decimal("1"), context unresolved.
- **Expected cross-results:** (R001,R002)=CONFIRMED_CONFLICT;
  (R001,R003)=ASSESSMENT_UNRESOLVED; and
  (R002,R003)=ASSESSMENT_UNRESOLVED.
- **Expected bounded set/aggregate:** observed partial
  R_conf[QB-v0.1]={R001,R002}, Rconf_complete=false; aggregate UNKNOWN;
  M_cons[QB-v0.1] absent. Fraction(1,3) must not be emitted.
- **Metadata:** META(3,3,2,3,3,1,1,0,2,0,0,2,false).
- **Rationale/traceability:** CRA-D013, D021, D024, D028, D032, D056, D058.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-023 — compatible result plus material unresolved comparisons

- **Binding status:** BINDING_DOMAIN_CONTRACT_REFERENCE_CASE.
- **Purpose:** bind UNKNOWN when no conflict is observed but a material
  comparison remains unresolved.
- **Input requirement set:** line 1/R001 = D-U5-S; line 2/R002 = D-L2-S;
  line 3/R003 is D-UNRES-C with bound Decimal("1").
- **Expected observations/Evidence:** R001/R002 resolved; R003 context
  unresolved with exact D-UNRES-C spans.
- **Expected cross-results:** (R001,R002)=COMPATIBLE_WITHIN_RULE;
  the two pairs involving R003 are ASSESSMENT_UNRESOLVED.
- **Expected bounded set/aggregate:** observed empty partial
  R_conf[QB-v0.1]; UNKNOWN; no numeric metric. The observed compatible result
  cannot produce value 1.
- **Metadata:** META(3,3,2,3,3,1,0,1,2,0,0,0,false).
- **Rationale/traceability:** CRA-D011, D021, D024, D028, D056, D058.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-024 — unresolved quantitative extraction without observations

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind CRA-D067 when incomplete extraction prevents an observation
  pair from being materialized.
- **Input requirement set:** line 1/R001 = E-X95; line 2/R002 = E-NONE-1.
- **Expected extraction/Evidence:** R001 is INCOMPLETE/UNRESOLVED, no
  quantitative Evidence or observation, diagnostic 95 [29,31); R002 is
  COMPLETE/NOT_DETECTED with no Evidence or observation.
- **Expected cross-results:** none materialized; N_Q=0. This does not mean there
  is no potential bounded conflict.
- **Expected bounded set/aggregate:** observed empty partial
  R_conf[QB-v0.1]; UNKNOWN; M_cons[QB-v0.1] absent.
- **Metadata:** META(2,0,0,1,0,0,0,0,0,0,1,0,false).
- **Rationale/traceability:** CRA-D021, D024, D026, D067.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-025 — empty specification

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind the empty reader input.
- **Input requirement set:** empty UTF-8 file; no requirement IDs.
- **Expected extraction/observations/Evidence:** none.
- **Expected cross-results:** none.
- **Expected bounded set/aggregate:** R_conf[QB-v0.1]=empty set;
  NOT_APPLICABLE; no M_cons[QB-v0.1] value.
- **Metadata:** META(0,0,0,0,0,0,0,0,0,0,0,0,true).
- **Rationale/traceability:** CRA-D018, D022, D025-D026.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-026 — exactly one requirement

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** bind the approved no-cross-pair behavior.
- **Input requirement set:** line 1/R001 = E-NONE-1.
- **Expected extraction/Evidence:** COMPLETE/NOT_DETECTED; no observation or
  quantitative Evidence.
- **Expected cross-results:** none because N_P=0.
- **Expected bounded set/aggregate:** empty complete R_conf[QB-v0.1];
  NOT_APPLICABLE; no numeric metric.
- **Metadata:** META(1,0,0,0,0,0,0,0,0,0,0,0,true).
- **Rationale/traceability:** CRA-D019, D025-D026.
- **Bounded non-claim:** NC-QB-BASE.

### RC-QB-027 — multiple requirements with no applicable comparison

- **Binding status:** BINDING_END_TO_END_REFERENCE_CASE.
- **Purpose:** distinguish no applicable comparison from
  COMPATIBLE_WITHIN_RULE.
- **Input requirement set:** line 1/R001 = E-NONE-1; line 2/R002 = E-NONE-2.
- **Expected extraction/Evidence:** both outcomes COMPLETE/NOT_DETECTED; no
  quantitative observations, Evidence, or diagnostics.
- **Expected cross-results:** none; the requirement pair exists but contributes
  zero observation pairs.
- **Expected bounded set/aggregate:** empty complete R_conf[QB-v0.1];
  NOT_APPLICABLE; no numeric metric.
- **Metadata:** META(2,0,0,1,0,0,0,0,0,0,0,0,true).
- **Rationale/traceability:** CRA-D020, D025-D026, D057.
- **Bounded non-claim:** NC-QB-BASE.

## 5. Rejected end-to-end candidate fixtures

These fixtures are not binding cases. Their observed behavior was verified and
is preserved so later work does not silently reuse them.

| Rejected fixture | Intended purpose | Observed frozen-extractor behavior | Disposition/replacement |
| --- | --- | --- | --- |
| RF-QB-001: Час відгуку не нижче 5 с при 500 одночасних користувачах | End-to-end lower-bound conflict | QUANT-UK-001:E001 = не нижче 5 с [12,24), GREATER_THAN_OR_EQUAL/INCLUSIVE, Decimal("5"), SECOND; metric/context absent; diagnostic 500 [29,32); INCOMPLETE | Rejected for end-to-end conflict; replaced by domain cases RC-QB-001-RC-QB-004 and RC-QB-006-RC-QB-007. |
| RF-QB-002: ЧАС  ВІДГУКУ ≤ 2 с при 500 одночасних користувачах | Representation-only metric normalization | Only QUANT-001:E001 = ≤ 2 с [13,18); metric/context absent; diagnostic 500 [23,26); INCOMPLETE | Rejected end-to-end; normalization is bound by RC-QB-008. |
| RF-QB-003: Час відповіді ≤ 2 с при 500 одночасних користувачах | Semantic-synonym OUTSIDE result | Only QUANT-001:E001 = ≤ 2 с [14,19); metric/context absent; diagnostic 500 [24,27); INCOMPLETE, so the text would be unresolved rather than a resolved metric mismatch | Rejected end-to-end; synonym boundary is bound by RC-QB-009. |
| RF-QB-004: Час відгуку ≤ 2 с під час пікового навантаження | Resolved different quantitative context | Metric and upper bound are accepted, but quantitative context remains absent; COMPLETE | Rejected as a resolved-context fixture; replaced by RC-QB-010. |
| RF-QB-005: не рідше одного разу на 5 с | NOT_LESS_FREQUENT observation | Protected frequency construction yields COMPLETE/NOT_DETECTED with no observation, Evidence, or diagnostic | Rejected end-to-end; comparator disposition is bound by RC-QB-017. |

The systematic full-key context diagnostic described in Section 2.2 is an
additional corpus limitation: E-U2-S-C, E-U5-S-C, and E-U1-M-C are valid
end-to-end extraction fixtures, but none can yield a computed aggregate because
their quantitative extraction is INCOMPLETE.

## 6. Traceability matrix

In this matrix C means CONFIRMED_CONFLICT, W means
COMPATIBLE_WITHIN_RULE, U means ASSESSMENT_UNRESOLVED, and O means
OUTSIDE_V0_1_APPLICABILITY.

| Reference case | Principal decision IDs | Inputs / expected observations | Cross-state sequence | R_conf[QB-v0.1] effect | Aggregate state/value | Coverage purpose |
| --- | --- | --- | --- | --- | --- | --- |
| RC-QB-001 | D001,D005,D011,D012,D037,D038,D066 | U2-S + L5-S, same complete key | C | add R001,R002 | COMPUTED / 0 | simple conflict |
| RC-QB-002 | D006,D060 | L5-S then U2-S | C | add R001,R002 | COMPUTED / 0 | reversed source order |
| RC-QB-003 | D007,D021,D061 | U2-S, L5-S, U1-S | C,W,C | union R001,R002,R003 once | COMPUTED / 0 | overlapping conflicts and set semantics |
| RC-QB-004 | D011,D037-D041 | U5-S + L2-S | W | none | COMPUTED / 1 | overlapping mixed bounds |
| RC-QB-005 | D024,D026,D032,D039,D067 | exact extractor U2-S-C + U5-S-C | W | observed empty, incomplete | UNKNOWN / absent | exact context plus incomplete extraction |
| RC-QB-006 | D034,D037,D039 | L5-S + L2-S | W | none | COMPUTED / 1 | two lower bounds |
| RC-QB-007 | D037,D040 | U5-S + L5-S | W | none | COMPUTED / 1 | inclusive shared endpoint |
| RC-QB-008 | D029,D030,D032,D036 | normalized case/space/NFC variants | W | none | COMPUTED / 1 | representation-only identity |
| RC-QB-009 | D030,D057 | час відгуку + час відповіді synonym surfaces | O | none | NOT_APPLICABLE | no synonym inference |
| RC-QB-010 | D032,D057 | standard + peak-load contexts | O | none | NOT_APPLICABLE | resolved context inequality |
| RC-QB-011 | D024,D033,D057,D067 | extractor SECOND + MINUTE | O | observed empty, incomplete | UNKNOWN / absent | no conversion plus extraction uncertainty |
| RC-QB-012 | D020,D025,D033,D057 | resolved SECOND + MINUTE | O | none | NOT_APPLICABLE | no applicable comparison |
| RC-QB-013 | D013,D030,D032,D056,D058 | extractor bounds with metric/context missing | U | observed empty, incomplete | UNKNOWN / absent | missing metric |
| RC-QB-014 | D013,D032,D056,D058 | extractor metric present/context missing | U | observed empty, incomplete | UNKNOWN / absent | missing context |
| RC-QB-015 | D007,D030,D032,D056,D058 | resolved + unresolved metric + unresolved context | U,U,U | observed empty, incomplete | UNKNOWN / absent | explicit unresolved components |
| RC-QB-016 | D034,D056,D058 | extractor UPPER_BOUND + upper bound | U | observed empty, incomplete | UNKNOWN / absent | unresolved inclusivity |
| RC-QB-017 | D025,D034,D057 | NOT_LESS_FREQUENT + supported upper | O | none | NOT_APPLICABLE | unsupported comparator class |
| RC-QB-018 | D007,D046,D061,D062 | two observations by one in source order | U,U | observed empty, incomplete | UNKNOWN / absent | Cartesian comparisons; no within relation |
| RC-QB-019 | D023,D026,D066 | three resolved upper bounds | W,W,W | empty complete set | COMPUTED / 1 | exact all-compatible aggregate |
| RC-QB-020 | D023,D026,D033,D066 | conflict in SECOND; third MINUTE | C,O,O | add R001,R002 | COMPUTED / 1/3 | one conflict among three |
| RC-QB-021 | D019-D026,D067 | conflict plus COMPLETE/NOT_DETECTED requirement | C | add R001,R002 | COMPUTED / 1/3 | denominator includes isolated requirement |
| RC-QB-022 | D021,D024,D056,D058 | conflict plus unresolved context | C,U,U | partial R001,R002 | UNKNOWN / absent | conflict plus material unknown |
| RC-QB-023 | D021,D024,D056,D058 | compatible plus unresolved context | W,U,U | observed empty, incomplete | UNKNOWN / absent | zero conflicts plus material unknown |
| RC-QB-024 | D024,D026,D067 | unresolved extraction + no observation | none materialized | observed empty, incomplete | UNKNOWN / absent | extraction uncertainty without pair |
| RC-QB-025 | D025,D026 | empty file | none | empty | NOT_APPLICABLE | empty specification |
| RC-QB-026 | D019,D025,D026 | one COMPLETE/NOT_DETECTED requirement | none | empty | NOT_APPLICABLE | one requirement |
| RC-QB-027 | D020,D025,D026,D057 | two COMPLETE/NOT_DETECTED requirements | none | empty | NOT_APPLICABLE | multiple requirements, no applicable comparison |

Every listed cross-result preserves the canonical participant IDs named by its
pair, even when it is W, U, or O. Only C participants enter
R_conf[QB-v0.1].

## 7. Coverage audit of all 41 researcher-approved decisions

The classification describes this corpus, not implementation readiness.

| Decision | Coverage classification | Binding coverage or validation target |
| --- | --- | --- |
| CRA-D001 | COVERED_BY_BINDING_CASE | RC-QB-001 through RC-QB-027 collectively bind the bounded slice. |
| CRA-D005 | COVERED_BY_BINDING_CASE | Every cross case uses distinct unordered requirement pairs. |
| CRA-D006 | COVERED_BY_BINDING_CASE | RC-QB-002 binds canonical source ordering. |
| CRA-D007 | COVERED_BY_BINDING_CASE | RC-QB-003, RC-QB-015, and RC-QB-018 bind all cross-observation pairs. |
| CRA-D011 | COVERED_BY_BINDING_CASE | C: RC-QB-001; W: RC-QB-004; U: RC-QB-013; O: RC-QB-009. |
| CRA-D012 | COVERED_BY_BINDING_CASE | RC-QB-001-RC-QB-003 bind mechanically conclusive conflict results. |
| CRA-D013 | COVERED_BY_BINDING_CASE | RC-QB-013-RC-QB-016 preserve reasons and uncertainty. |
| CRA-D019 | COVERED_BY_BINDING_CASE | RC-QB-026; denominator participation also RC-QB-021. |
| CRA-D020 | COVERED_BY_BINDING_CASE | RC-QB-012 and RC-QB-027. |
| CRA-D021 | COVERED_BY_BINDING_CASE | RC-QB-022 preserves partial R_conf[QB-v0.1]. |
| CRA-D023 | COVERED_BY_BINDING_CASE | Exact Fraction values 0, 1, and 1/3 are bound. |
| CRA-D024 | COVERED_BY_BINDING_CASE | RC-QB-005, RC-QB-022-RC-QB-024. |
| CRA-D025 | COVERED_BY_BINDING_CASE | RC-QB-012, RC-QB-017, RC-QB-025-RC-QB-027. |
| CRA-D026 | COVERED_BY_BINDING_CASE | Every case supplies the complete META tuple and coverage profile. |
| CRA-D066 | COVERED_BY_BINDING_CASE | All numeric cases use M_cons[QB-v0.1]; NC-QB-BASE excludes full M_cons claims. |
| CRA-D067 | COVERED_BY_BINDING_CASE | RC-QB-005, RC-QB-011, and RC-QB-024. |
| CRA-D029 | COVERED_BY_BINDING_CASE | RC-QB-008 binds NFC, case, and whitespace normalization. |
| CRA-D030 | COVERED_BY_BINDING_CASE | RC-QB-008 equality; RC-QB-009 inequality; RC-QB-013 missing metric. |
| CRA-D032 | COVERED_BY_BINDING_CASE | RC-QB-005 equality; RC-QB-010 inequality; RC-QB-014-RC-QB-015 missing/unresolved. |
| CRA-D033 | COVERED_BY_BINDING_CASE | RC-QB-005 same unit; RC-QB-011-RC-QB-012 unequal units. |
| CRA-D034 | COVERED_BY_BINDING_CASE | Supported bounds in RC-QB-001-RC-QB-007; UPPER_BOUND RC-QB-016; frequency RC-QB-017. |
| CRA-D035 | COVERED_BY_BINDING_CASE | All numeric templates preserve exact Decimal values. |
| CRA-D036 | COVERED_BY_BINDING_CASE | Equal and unequal complete key cases RC-QB-001, RC-QB-008-RC-QB-012. |
| CRA-D037 | COVERED_BY_BINDING_CASE | RC-QB-001, RC-QB-004, RC-QB-006, and RC-QB-007 bind all supported half-lines. |
| CRA-D038 | COVERED_BY_BINDING_CASE | RC-QB-001-RC-QB-003 bind empty intersections. |
| CRA-D041 | COVERED_BY_BINDING_CASE | A: 001; B: 004; C: 005; D: 006; E: 010; F: 012; G: 016; H: 013/015; I: 014/015; J: 018. |
| CRA-D043 | STRUCTURAL_ONLY | Every case specifies result ID, participants, state, subtype, evidence, explanation, reasons, contract, and coverage; final schema remains architectural. |
| CRA-D044 | COVERED_BY_BINDING_CASE | Confirmed cases use DIRECT_QUANTITATIVE_BOUND_INCOMPATIBILITY only. |
| CRA-D046 | COVERED_BY_BINDING_CASE | Template instantiation plus RC-QB-018 binds requirement/observation source order. |
| CRA-D048 | COVERED_BY_BINDING_CASE | Every Evidence-bearing case uses participant-qualified references. |
| CRA-D050 | REQUIRES_ARCHITECTURE_VALIDATION | Corpus specifies ownership/span invariants; constructor-level rejection cannot be validated before architecture. |
| CRA-D051 | NON_CLAIM_ONLY | Every case states no C_i/V_i/U_i mutation; no local expected value is changed. |
| CRA-D052 | STRUCTURAL_ONLY | Aggregate expectations are separate Consistency results. |
| CRA-D054 | REQUIRES_ARCHITECTURE_VALIDATION | SpecificationAssessment composition is intentionally not represented here. |
| CRA-D056 | COVERED_BY_BINDING_CASE | RC-QB-013-RC-QB-016, RC-QB-022-RC-QB-024. |
| CRA-D057 | COVERED_BY_BINDING_CASE | RC-QB-009-RC-QB-012 and RC-QB-017. |
| CRA-D058 | COVERED_BY_BINDING_CASE | RC-QB-013-RC-QB-016 and aggregate UNKNOWN cases. |
| CRA-D060 | COVERED_BY_BINDING_CASE | RC-QB-002 and every canonical pair list. |
| CRA-D061 | COVERED_BY_BINDING_CASE | RC-QB-003 and RC-QB-018 bind multi-result order. |
| CRA-D062 | COVERED_BY_BINDING_CASE | Section 3 exact spans and participant/span ordering. |
| CRA-D064 | NON_CLAIM_ONLY | NC-QB-BASE is incorporated into every binding case. |

### 7.1 Coverage conclusion

Every approved executable scientific branch has at least one binding case
across the combined end-to-end and domain-contract corpus. No approved branch
is silently omitted.

The following composition gap is explicit rather than hidden:

| Gap | Classification | Reason |
| --- | --- | --- |
| Full text-to-COMPUTED M_cons[QB-v0.1] path | NOT_YET_COVERED | The only current linked quantitative context always makes extraction INCOMPLETE; no supported lower bound receives the full linked key. Computed semantics are bound at the domain-contract boundary instead. |

This gap must be considered during architecture research and before production
implementation. It must not be solved by changing a fixture, suppressing the
500 diagnostic, or assuming a missing context.

## 8. End-of-round report

### Branch

research/cross-requirement-analysis

No new branch was created. Nothing was merged.

### File created

docs/cross-requirement-consistency-reference-cases.md

No production source, tests, detector, model-specification, C/V/U,
aggregation, or reporter file was changed.

### Corpus counts

- BINDING_END_TO_END_REFERENCE_CASE: 10
- BINDING_DOMAIN_CONTRACT_REFERENCE_CASE: 17
- ILLUSTRATIVE_ONLY cases: 0
- REJECTED_FIXTURE candidates: 5
- Total binding cases: 27

### Rejected candidate fixtures

Five candidate text fixtures were rejected because the current extractor does
not attach the component needed for the intended branch:

1. linked lower bound;
2. representation-varied metric;
3. semantic-synonym metric;
4. alternative resolved quantitative context; and
5. NOT_LESS_FREQUENT observation.

Their exact observed behavior and binding replacements are recorded in
Section 5.

### Coverage result

Every executable approved QB-v0.1 branch has binding scientific reference
coverage across the combined corpus. Exact conflict, compatibility,
applicability, uncertainty, set construction, Fraction arithmetic,
NOT_APPLICABLE, ordering, provenance, and non-claim branches are covered.

The full text-to-computed-aggregate composition is not currently achievable
under the frozen extractor and is explicitly NOT_YET_COVERED end-to-end.

### Unresolved blockers

- The only linked context produces an unresolved 500 diagnostic and therefore
  INCOMPLETE quantitative extraction.
- The current extractor does not attach the required metric/context to
  GREATER_THAN_OR_EQUAL.
- The current extractor does not emit NOT_LESS_FREQUENT observations.
- Representation-varied and synonym metrics, and alternative quantitative
  contexts, do not become resolved linked components.
- The reference corpus still requires researcher approval.
- Architecture requires its own later contract and approval.

### Readiness

This corpus is ready for researcher review and approval as a mixed binding
end-to-end/domain-contract corpus with the explicit end-to-end composition
gap above.

Architecture and production implementation remain blocked. After researcher
approval of this corpus, the next authorized phase is architecture-contract
research, not implementation.
