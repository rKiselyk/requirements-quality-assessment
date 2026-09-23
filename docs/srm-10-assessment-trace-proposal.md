# SRM-10 — Minimum Assessment Trace Contract Proposal

**Decision status:** `PROPOSED_FOR_RESEARCHER_REVIEW`  
**Issue:** `#78 — SRM-10`  
**Scope:** one requirement assessed as the SRM-02 bounded `RequirementQualityProfile(C, V, U)`.

## 1. Decision requested

Approve a structured companion trace that connects each existing `CharacteristicAssessment` to the existing extraction result without changing any detector, formula, value, Finding rule, or applicability decision.

```text
CharacteristicAssessment(state, exact value)
→ CharacteristicTrace(governing rule and decision path)
→ FeatureInputTrace(rule effect and outcome reference)
→ FeatureDetectionOutcome(observations, processing, diagnostics)
→ accepted observation.evidence_refs
→ RequirementExtractionResult.evidence
→ exact Evidence span in Requirement.text
```

For completed absence, the path ends at a completed empty detector outcome; it creates no `Evidence`. For unresolved processing, the path ends at `DetectionDiagnostic` and optional `DiagnosticSpan`, never at fake `Evidence`.

## 2. Scope invariants

The proposal reuses existing domain concepts and:

- preserves `CALC-C-MVP-001`, `CALC-V-MVP-001`, and `CALC-U-MVP-001` exactly;
- preserves exact `Fraction` values and `COMPUTED` / `UNKNOWN` / `NOT_APPLICABLE`;
- retains the `RQD-023` applicability simplification;
- preserves `FIND-U-VAGUE-001` as `SIGNAL` only;
- adds no characteristic, scalar score, detector, vocabulary, threshold, coefficient, risk, confidence, severity, or corrective action; and
- does not implement or claim runtime support for R3 or F1-A.

The trace explains decisions already made by approved rules. It is not a second calculation model.

## 3. Proposed structures

```text
RequirementAssessmentRecord
  extraction_result: RequirementExtractionResult
  quality_profile: RequirementQualityProfile
  trace: RequirementAssessmentTrace

RequirementAssessmentTrace
  requirement_id: str
  characteristics: tuple[CharacteristicTrace, CharacteristicTrace,
                         CharacteristicTrace]
  coverage_profile_id: str

CharacteristicTrace
  characteristic_id: CharacteristicId
  governing_rule_id: str
  decision_code: TraceDecisionCode
  inputs: tuple[FeatureInputTrace, ...]
  finding_refs: tuple[str, ...]

FeatureInputTrace
  feature_id: FeatureId
  applicability: CriterionApplicability | None
  observation_indexes: tuple[int, ...]
  diagnostic_indexes: tuple[int, ...]
  effect_code: TraceEffectCode
```

`RequirementAssessmentRecord` is the minimum reporter input. It composes immutable values; it does not copy requirement text, Evidence, observations, diagnostics, assessments, or Findings.

## 4. Field contract

### 4.1 `RequirementAssessmentRecord`

| Field | Meaning | Required/optional | Source | Cardinality | Validation rule |
| --- | --- | --- | --- | --- | --- |
| `extraction_result` | Requirement, six feature outcomes, and accepted Evidence registry | Required | Existing domain boundary or manually constructed domain value | 1 | Valid `RequirementExtractionResult`; all existing Evidence round-trip/reference invariants hold |
| `quality_profile` | Authoritative assessment state, exact value, assessment Rule ID, Findings, and explanation | Required | Existing calculators/profile assembly | 1 | Valid profile containing exactly C, V, U |
| `trace` | Links the profile to extraction inputs | Required | Calculators or calculator-level trace builder executing the same rules | 1 | Valid jointly against the other two fields; cannot alter them |

### 4.2 `RequirementAssessmentTrace`

| Field | Meaning | Required/optional | Source | Cardinality | Validation rule |
| --- | --- | --- | --- | --- | --- |
| `requirement_id` | Joins trace to source artifact | Required | `extraction_result.requirement.id` | 1 | Equals extraction requirement ID and every referenced Finding/Evidence requirement ID |
| `characteristics` | Trace for each independent profile component | Required | Approved profile structure | Exactly 3 | One each in C, V, U order; no duplicates or other characteristics |
| `coverage_profile_id` | Selects canonical bounded-coverage disclosures | Required | This contract | 1 | Exactly `MVP-V0.1-BOUNDED-CVU-001` |

### 4.3 `CharacteristicTrace`

| Field | Meaning | Required/optional | Source | Cardinality | Validation rule |
| --- | --- | --- | --- | --- | --- |
| `characteristic_id` | Selects authoritative assessment in the profile | Required | Existing `CharacteristicId` | 1 | Matches profile component and governing rule |
| `governing_rule_id` | Rule executed or attempted, including a withheld result | Required | Approved calculation rule | 1 | C=`CALC-C-MVP-001`; V=`CALC-V-MVP-001`; U=`CALC-U-MVP-001`; for `COMPUTED`, equals `assessment_rule_id` |
| `decision_code` | Approved rule branch producing, withholding, or establishing non-applicability | Required | Governing rule | 1 | Allowed for the characteristic and consistent with state, exact value, inputs, and diagnostics under §6 |
| `inputs` | Exhaustive feature outcomes consulted by the rule | Required | Existing extraction result | C=3; V=3; U=1 | Exactly the §5 families, no duplicates; all indexes resolve |
| `finding_refs` | References Findings already in the assessment | Required; may be empty | `assessment.findings[].finding_id` | 0..n | Every and only assessment Finding, in existing order; C/V empty in current scope |

The trace does not duplicate `state`, `value`, `assessment_rule_id`, Findings, or explanation. The existing assessment remains authoritative. `governing_rule_id` is separate because the current envelope permits `assessment_rule_id=None` for `UNKNOWN`, while a withheld result must still name the attempted approved rule.

### 4.4 `FeatureInputTrace`

| Field | Meaning | Required/optional | Source | Cardinality | Validation rule |
| --- | --- | --- | --- | --- | --- |
| `feature_id` | Selects an existing `FeatureDetectionOutcome` | Required | Existing `FeatureId`/`RequirementFeatures` mapping | 1 | Authorized input family for this characteristic |
| `applicability` | Preserves applicability only where the rule allocates it | Required field; nullable | `RQD-023` and `CALC-C-MVP-001` | 1 value or `None` | C=`APPLICABLE`; V/U=`None`; detection never determines applicability |
| `observation_indexes` | References accepted observations without copying them | Required; may be empty | Outcome's immutable ordered observations | 0..n | Zero-based, unique, ascending, in range; includes all accepted observations, including non-selecting/mixed observations |
| `diagnostic_indexes` | References unresolved reasons without converting them to Evidence/Findings | Required; may be empty | Outcome's immutable ordered diagnostics | 0..n | Zero-based, unique, ascending, in range; includes all diagnostics |
| `effect_code` | States how the input family affected the rule result | Required | Approved calculation/propagation rule | Exactly 1 per family | Assigned by the characteristic-specific precedence in §6; agrees with observations, processing, diagnostics, and decision code |

Tuple indexes are local references into one immutable extraction result, not durable cross-run IDs. They are proposed because observations and diagnostics currently have no IDs. Existing observation `evidence_refs` remain the only links to accepted `Evidence`; diagnostic candidate spans remain non-Evidence.

## 5. Required input families and applicability

| Characteristic | Required trace inputs | Applicability |
| --- | --- | --- |
| C | `condition_context`, `expected_result`, `acceptance_criterion` | `APPLICABLE` for all three under retained MVP simplification |
| V | `acceptance_criterion`, `quantitative_constraint`, `verification_method` | `None`; alternative evidence paths, not mandatory criteria |
| U | `vague_term_occurrence` | `None`; signal detector, not applicability criterion |

No current C/V/U rule establishes characteristic-level `NOT_APPLICABLE`. The contract can represent it only as `state=NOT_APPLICABLE`, `value=None`, `decision_code=CHARACTERISTIC_NOT_APPLICABLE`, no `QUALITY_PROBLEM`, and a `governing_rule_id` naming an approved non-applicability rule. Because no such rule exists, this state is invalid for current-rule records. This preserves the state without inventing a rule.

## 6. Rule-specific decision and effect codes

### 6.1 Completeness

Decision codes:

- `C_CRITERION_RATIO_COMPUTED`: all inputs completed; existing exact ratio.
- `C_REQUIRED_INPUT_UNRESOLVED`: a required input is incomplete; `UNKNOWN`, value `None`.

Input effect codes:

- `C_PRESENT_1`: accepted observation(s), contributing exactly 1.
- `C_COMPLETED_ABSENCE_0`: complete empty outcome, contributing exactly 0 without Evidence.
- `C_REQUIRED_UNRESOLVED`: incomplete outcome; observations and diagnostics remain referenced, and the result is withheld.

The three effects must reproduce the approved branch/value under `CALC-C-MVP-001`; repeated observations contribute at most 1. For a same-family mixed outcome, `C_REQUIRED_UNRESOLVED` takes precedence over `C_PRESENT_1`: accepted observations remain preserved, but incomplete processing of any required C family withholds the assessment.

### 6.2 Verifiability

Decision codes:

- `V_FULL_ACCEPTANCE_TIER`: accepted acceptance criterion; exact value `1`.
- `V_PARTIAL_LOWER_TIER`: no accepted acceptance criterion and accepted quantitative/method evidence; exact value `1/2`.
- `V_COMPLETED_NO_EVIDENCE_TIER`: all relevant processing complete and all paths absent; exact value `0`.
- `V_MATERIAL_INPUT_UNRESOLVED`: a candidate could change tier; `UNKNOWN`, value `None`.

Input effect codes are `V_SELECTS_FULL_TIER`, `V_SELECTS_LOWER_TIER`, `V_PRESENT_NONSELECTING`, `V_COMPLETED_ABSENCE`, `V_UNRESOLVED_MATERIAL`, and `V_UNRESOLVED_NON_MATERIAL`. No additional mixed-state code is required.

Exactly one code is assigned to each of the three V families by this precedence:

1. If a family has accepted observations, use an accepted-observation code, even when that same outcome is `INCOMPLETE` and has diagnostics:
   - acceptance criterion → `V_SELECTS_FULL_TIER`;
   - lower-tier family under `V_PARTIAL_LOWER_TIER` → `V_SELECTS_LOWER_TIER`;
   - lower-tier family under `V_FULL_ACCEPTANCE_TIER` or `V_MATERIAL_INPUT_UNRESOLVED` → `V_PRESENT_NONSELECTING`.
2. Otherwise, a complete empty family uses `V_COMPLETED_ABSENCE`.
3. Otherwise, the family is incomplete and empty. Use `V_UNRESOLVED_MATERIAL` if resolving its candidate could change the final numeric class; use `V_UNRESOLVED_NON_MATERIAL` if an already accepted path fixes that class.

`V_PRESENT_NONSELECTING` has two bounded uses: accepted lower-tier evidence is non-selecting because accepted acceptance already fixes `V=1`, or it is provisional evidence while a material unresolved acceptance candidate withholds the assessment. In the second use, it must not be described as selecting a final `1/2` tier or as a computed result.

Diagnostics on a family that also has accepted observations are always preserved by `diagnostic_indexes`, but are non-material within that family: the accepted observation already establishes the highest tier that the same family can supply, so resolving another same-family candidate cannot change its tier contribution. This materiality is explained by the accepted-observation effect code together with the referenced diagnostics and the characteristic `decision_code`; it does not require a second effect code. Cross-family materiality remains governed by V1–V4:

- V1: accepted acceptance fixes `V=1`; every unresolved lower-tier empty family is `V_UNRESOLVED_NON_MATERIAL`, and accepted lower-tier families are `V_PRESENT_NONSELECTING`.
- V2: no accepted evidence plus an unresolved lower-tier candidate yields `UNKNOWN`; each incomplete empty lower-tier family that could establish `1/2` is `V_UNRESOLVED_MATERIAL`.
- V3: acceptance is complete/absent and accepted lower-tier evidence fixes `V=1/2`; accepted lower-tier families use `V_SELECTS_LOWER_TIER`, while an incomplete empty lower-tier sibling uses `V_UNRESOLVED_NON_MATERIAL`.
- V4: an incomplete empty acceptance family is `V_UNRESOLVED_MATERIAL`; accepted lower-tier families use `V_PRESENT_NONSELECTING` as preserved provisional evidence, and the assessment remains `UNKNOWN` because acceptance could change the class from `1/2` to `1`.

### 6.3 Unambiguity

Decision codes:

- `U_SUPPORTED_SIGNAL_TIER`: accepted occurrence(s); exact value `1/2` regardless of count.
- `U_COMPLETED_SIGNAL_ABSENCE_TIER`: complete empty scan; exact value `1` without absence Evidence.
- `U_MATERIAL_INPUT_UNRESOLVED`: no occurrence and processing could surface one; `UNKNOWN`, value `None`.

Input effect codes are `U_SIGNAL_PRESENT`, `U_COMPLETED_SIGNAL_ABSENCE`, and `U_UNRESOLVED_MATERIAL`. For a same-family mixed outcome, `U_SIGNAL_PRESENT` takes precedence: it retains accepted occurrences and all diagnostics, whose resolution cannot lower the class below `1/2`.

For `U_SUPPORTED_SIGNAL_TIER`, each occurrence maps one-to-one to an assessment Finding with `kind=SIGNAL`, `code=VAGUE_TERM_SIGNAL`, `rule_id=FIND-U-VAGUE-001`, `criterion_id=None`, and exactly that occurrence's `evidence_refs`, in existing source/Finding order. No `QUALITY_PROBLEM` or `U=0` is valid.

## 7. Absence, Evidence, and diagnostics

A completed absence is valid only for `processing_status=COMPLETE`, `observations=()`, and `diagnostics=()`. Its trace indexes are empty; there is no trace-level `evidence_refs` field from which fake Evidence could be created.

Every existing entry in each referenced observation's `evidence_refs` resolves exactly once in `extraction_result.evidence`, matches the family and requirement, and satisfies:

```text
Requirement.text[Evidence.start_offset:Evidence.end_offset] == Evidence.text
```

Every referenced diagnostic retains its rule ID, code, explanation, and optional candidate span. A candidate span round-trips to the requirement text but remains explicitly non-Evidence.

## 8. Bounded coverage profile

`MVP-V0.1-BOUNDED-CVU-001` requires these canonical disclosures:

1. Coverage is limited to implemented bounded six-family extraction and approved C/V/U rules, not exhaustive Ukrainian linguistic/semantic analysis.
2. `NOT_DETECTED`/completed absence mean no accepted observation under completed implemented rules, not universal semantic absence.
3. C/V values, including low values or zero, are rule outputs and not confirmed defects.
4. `U=1` means absence of the supported signal class, not proof of unique interpretation; `U=1/2` is signal presence, not confirmed ambiguity; current U never produces `0`.
5. `FIND-U-VAGUE-001` is `SIGNAL` only; no current `QUALITY_PROBLEM`, severity, confidence, risk, or corrective action exists.
6. R3 and F1-A are researcher-approved but unimplemented and are not claimed as runtime coverage.
7. The record is a multidimensional C/V/U profile, not a scalar requirement score or product-quality prediction.

The reporter may format these statements but may not select, weaken, strengthen, or infer different claims from values.

## 9. Proposed binding reference-case matrix

These rows become binding only if this proposal is approved; they reuse existing model-spec facts.

| Case | Existing facts | Required trace result |
| --- | --- | --- |
| Positive | Case A: all C observations; V acceptance evidence; U complete/no signal | C three `C_PRESENT_1`, value `1`; V full tier, value `1`; U completed signal absence, value `1`, no fake Evidence |
| Completed absence | Case E: relevant C/V/U outcomes complete and empty | C value `0` with three absence effects; V value `0` with three absence effects; U value `1` with absence effect; all refs empty |
| Unresolved | Case D: method candidate unresolved; no accepted V evidence | V material unresolved, `UNKNOWN`/`None`; method references diagnostic, whose candidate span is not Evidence |
| SIGNAL | Case B: accepted `швидко` occurrence | U signal tier, value `1/2`; one occurrence ref, one `FIND-U-VAGUE-001` Finding ref, exact Evidence, kind `SIGNAL` |
| V1 same-family mixed | §7.16.6/V1: accepted acceptance; quantitative accepted/incomplete; method complete/absent | V full tier, value `1`; acceptance=`V_SELECTS_FULL_TIER`; quantitative=`V_PRESENT_NONSELECTING` with observations and non-material diagnostics preserved; method=`V_COMPLETED_ABSENCE` |
| V3 unresolved lower sibling | V3: acceptance complete/absent; accepted quantitative evidence; method incomplete/empty | V partial tier, value `1/2`; quantitative=`V_SELECTS_LOWER_TIER`; method=`V_UNRESOLVED_NON_MATERIAL`; method diagnostics remain visible |
| V4 provisional lower evidence | V4: acceptance incomplete/empty; accepted quantitative evidence; method complete/absent | V material unresolved, `UNKNOWN`/`None`; acceptance=`V_UNRESOLVED_MATERIAL`; quantitative=`V_PRESENT_NONSELECTING` as provisional evidence, not a selected final tier; method=`V_COMPLETED_ABSENCE` |

## 10. Reporter consumption contract

The reporter may render requirement context, authoritative assessment fields, referenced observations/Evidence, completed absence, diagnostics, Findings, canonical coverage disclosures, and existing ordering. It must not calculate a value, choose a tier, decide diagnostic materiality, assign applicability, create a Finding, synthesize Evidence, classify a defect, or combine C/V/U.

## 11. Explicit scientific decision gates

Researcher approval is required for this package, specifically:

1. the companion structures and joint validation against existing extraction/profile values;
2. local `(feature_id, tuple index)` observation/diagnostic references instead of new IDs;
3. required trace `governing_rule_id`, including `UNKNOWN`, without changing the nullable assessment field;
4. the decision/effect codes and validation rules;
5. completed-empty outcomes as sole current absence provenance, without Evidence;
6. one-to-one U occurrence → `FIND-U-VAGUE-001` provenance validation;
7. `MVP-V0.1-BOUNDED-CVU-001` and its non-claims; and
8. the seven §9 reference rows as binding trace cases.

Until approved, this document defines no production contract and must not be recorded as researcher approval in `model-spec.md`.

## 12. Blockers and contradictions

No contradiction was found with the approved formulas, exact values, `RQD-023`, or SIGNAL-only boundary.

One representation gap requires gate §11.2: observations and diagnostics have no stable IDs. Local immutable tuple indexes are the smallest feasible references; rejecting them requires a separate ID-allocation decision and a larger domain contract.

`NOT_APPLICABLE` is representable but unreachable under current rules because no approved rule establishes it. The trace must not invent one merely to exercise the state.
