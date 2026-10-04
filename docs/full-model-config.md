# Full-model CLI configuration (TC-05)

The historical command needs no config. Full-model mode requires both files:

```powershell
python -m requirements_quality_assessment --mode full-model --config full-model.json --view user requirements.txt
python -m requirements_quality_assessment --mode full-model --config full-model.json --view audit requirements.txt
```

The requirements file remains UTF-8 with one requirement per non-empty line.
The JSON file supplies every external identity and scientific input used by the
core path. Missing fields, inconsistent identities, JSON floating-point
numbers, invalid UTF-8, and malformed JSON fail with stderr and a nonzero exit;
expected errors do not print a traceback.

## Core JSON shape

All `id` and `version` values below are caller-selected placeholders. `value`
is an exact decimal string. No value shown here is a production default.

```json
{
  "artifact_v1": {"id": "...", "version": "..."},
  "artifact_v2": {"id": "...", "version": "..."},
  "assessment_v1": {"id": "...", "version": "..."},
  "assessment_v2": {"id": "...", "version": "..."},
  "process": {
    "id": "...", "v1_version": "...", "v2_version": "...",
    "stage": "REFERENCE_VERIFICATION", "transition_id": "..."
  },
  "selected_criterion": {
    "requirement_id": "R001",
    "feature_id": "QUANTITATIVE_CONSTRAINT",
    "occurrence": 0
  },
  "product": {"id": "...", "version": "..."},
  "environment": {"id": "...", "version": "..."},
  "collection": {"id": "...", "version": "...", "source_kind": "..."},
  "observation": {
    "id": "...", "slot_index": 0, "value": "...", "unit": "s",
    "context": {
      "normalization_contract": {"id": "...", "version": "..."},
      "normalized_text": "..."
    }
  },
  "events": {
    "dynamic_id": "...", "product_quality_id": "...", "risk_id": "...",
    "v1_version": "...", "v2_version": "..."
  },
  "action": {"id": "...", "creator": {"id": "...", "version": "..."}},
  "revision": {
    "identity": {"id": "...", "version": "..."},
    "provider_kind": "...",
    "provider": {"id": "...", "version": "..."},
    "replacements": [{"requirement_id": "R002", "text": "..."}],
    "reason": "...",
    "application": {
      "id": "...", "version": "...", "child_version": "...",
      "transition_id": "..."
    }
  },
  "evidence_reuse": {
    "disposition": "REUSE_ALLOWED",
    "reasons": ["EXACT_IDENTITY_AND_CONTEXT_MATCH"],
    "source_contract_permission": true
  },
  "reassessment": {"id": "...", "version": "..."},
  "component_versions": [
    {"kind": "...", "id": "...", "version": "..."}
  ],
  "comparisons": {
    "ids": ["...", "...", "...", "..."],
    "version": "..."
  }
}
```

Enum strings must be values accepted by the existing domain contracts. The
configuration adapter constructs typed references and exact values, then the
public service validates the complete graph.

## Optional extensions

TC-01 through TC-04 are optional and omitted unless explicitly supplied to the
programmatic `FullModelRequest`. The current JSON adapter covers the core path.
In particular, TC-02 requires an explicitly injected in-process predictor;
there is no default predictor, registry, import-by-name mechanism, or executable
code field in JSON. TC-01 and TC-03 retain their rich typed provenance
contracts programmatically. TC-04 retains its explicit policy contract
programmatically. A future approved serialization boundary may add these to
JSON without weakening their existing contracts.
