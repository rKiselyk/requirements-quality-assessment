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
    "identity_checks": [
      {
        "field_name": "product_ref",
        "expected": {"id": "...", "version": "..."},
        "actual": {"id": "...", "version": "..."},
        "matches": true
      }
    ]
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

## Explicit evidence-reuse checks

`evidence_reuse.identity_checks` is mandatory. It must contain these nine
entries exactly once each: `product_ref`,
`observation_source_kind`, `collection_ref`, `metric_ref`, `unit`,
`context_identity`, `applicability`, `process_stage`, and
`source_contract_permission`.

Every entry supplies `field_name`, `expected`, `actual`, and a JSON boolean
`matches`. Missing, duplicate, unknown, or contradictory entries
are rejected. The adapter compares both supplied values with the actual typed
request graph before reconstructing `ExactIdentityCheck`; it passes through
the caller's `matches` value and never creates `matches=true` itself. A false
assertion or mismatched value therefore fails rather than becoming permission
to reuse evidence.

The JSON value shapes are:

- references such as `product_ref`: `{"id": "...", "version": "..."}`;
- enum values (`observation_source_kind`, `unit`, `applicability`, and
  `process_stage`): their contract string;
- `source_contract_permission`: JSON boolean;
- `context_identity`: `normalization_contract_ref` plus `normalized_text`;
- `metric_ref`: `registry_ref`, `metric_id`,
  `normalization_contract_ref`, and `normalized_source_metric`;
- `collection_ref`: collection `id`/`version`, nested product and environment
  references, and `source_kind`.

For valid exact reuse, the caller explicitly supplies the same serialized
graph value as `expected` and `actual` and explicitly supplies `matches: true`.
The reassessment rebuilder independently validates the resulting typed
nine-check set.

## Optional extensions

TC-01 through TC-04 are optional and omitted unless explicitly supplied to the
programmatic `FullModelRequest`. The current JSON adapter covers the core path.
In particular, TC-02 requires an explicitly injected in-process predictor;
there is no default predictor, registry, import-by-name mechanism, or executable
code field in JSON. TC-01 and TC-03 retain their rich typed provenance
contracts programmatically. TC-04 retains its explicit policy contract
programmatically. A future approved serialization boundary may add these to
JSON without weakening their existing contracts.

Each programmatic TC-04 `CheckpointExtensionInput` explicitly identifies both
the result version (`v1` or `v2`) and a typed `MetricId`. The service selects
exactly that metric and rejects a target that is missing or resolves to more
than one profile entry; it never defaults the checkpoint target to QB.
