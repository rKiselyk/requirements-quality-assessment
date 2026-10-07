"""HTTP adapter tests using the real accepted analysis pipeline."""

from importlib import import_module

from fastapi.testclient import TestClient

from requirements_quality_assessment.api.app import app
from requirements_quality_assessment.full_model.controlled_scenario import (
    CONTROLLED_SCENARIO_ID,
    CONTROLLED_SCENARIO_VERSION,
    V1_R001,
    V2_R002,
)


client = TestClient(app)
app_module = import_module("requirements_quality_assessment.api.app")

COMPLETE_REQUIREMENT = (
    "Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с."
)
VAGUE_REQUIREMENT = "Система повинна швидко оновити статус."


def _analyze(requirements):
    return client.post(
        "/api/v1/analyze",
        json={"case": "INITIAL", "requirements": requirements},
    )


def _controlled_demo(extra=None):
    payload = {
        "case": "CONTROLLED_DEMO",
        "scenario": {
            "id": CONTROLLED_SCENARIO_ID,
            "version": CONTROLLED_SCENARIO_VERSION,
        },
    }
    if extra:
        payload.update(extra)
    return client.post("/api/v1/analyze", json=payload)


def test_health_does_not_run_model():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_single_requirement_runs_real_pipeline_end_to_end():
    response = _analyze([{"text": COMPLETE_REQUIREMENT, "source_line": 1}])
    assert response.status_code == 200
    body = response.json()
    assert body["contract_version"] == "research-api-v1"
    assert body["analysis_case"] == "INITIAL"
    result = body["requirements"][0]
    assert result["requirement"] == {
        "id": "R001", "source_line": 1, "text": COMPLETE_REQUIREMENT,
    }
    assert result["quality_profile"]["completeness"]["assessment_rule_id"] == "CALC-C-MVP-001"
    assert result["quality_profile"]["verifiability"]["assessment_rule_id"] == "CALC-V-MVP-001"
    assert result["quality_profile"]["unambiguity"]["assessment_rule_id"] == "CALC-U-MVP-001"
    assert body["specification"]["quality_profile"]["completeness"]["total_count"] == 1


def test_multi_requirement_analysis_generates_canonical_ids_in_source_order():
    response = _analyze([
        {"text": COMPLETE_REQUIREMENT, "source_line": 1},
        {"text": VAGUE_REQUIREMENT, "source_line": 3},
    ])
    assert response.status_code == 200
    requirements = response.json()["requirements"]
    assert [item["requirement"]["id"] for item in requirements] == ["R001", "R002"]
    assert [item["requirement"]["source_line"] for item in requirements] == [1, 3]
    assert response.json()["specification"]["quality_profile"]["unambiguity"]["total_count"] == 2
    second = requirements[1]
    assert second["trace"]["requirement_id"] == "R002"
    assert all(item["requirement_id"] == "R002" for item in second["evidence"])


def test_source_lines_must_be_positive_unique_and_strictly_increasing():
    invalid_collections = (
        [
            {"text": COMPLETE_REQUIREMENT, "source_line": 1},
            {"text": VAGUE_REQUIREMENT, "source_line": 1},
        ],
        [
            {"text": COMPLETE_REQUIREMENT, "source_line": 3},
            {"text": VAGUE_REQUIREMENT, "source_line": 2},
        ],
        [{"text": COMPLETE_REQUIREMENT, "source_line": 0}],
        [{"text": COMPLETE_REQUIREMENT, "source_line": "1"}],
    )
    for requirements in invalid_collections:
        response = _analyze(requirements)
        assert response.status_code == 422
        assert response.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"


def test_requirement_ids_are_generated_deterministically_by_request_position():
    response = _analyze([
        {"text": COMPLETE_REQUIREMENT, "source_line": 1},
        {"text": VAGUE_REQUIREMENT, "source_line": 2},
    ])
    assert response.status_code == 200
    assert [item["requirement"]["id"] for item in response.json()["requirements"]] == [
        "R001", "R002"
    ]


def test_empty_requirements_collection_has_stable_error():
    response = _analyze([])
    assert response.status_code == 422
    assert response.json() == {"error": {
        "code": "EMPTY_SPECIFICATION",
        "details": {"requirement_count": 0},
        "path": ["body", "requirements"],
    }}


def test_missing_text_is_rejected_without_discarding_item():
    response = _analyze([{"source_line": 1}])
    assert response.status_code == 422
    body = response.json()["error"]
    assert body["code"] == "MALFORMED_REQUIREMENT_INPUT"
    assert body["path"][-1] == "text"


def test_blank_text_is_rejected():
    response = _analyze([{"text": " \t ", "source_line": 1}])
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"


def test_malformed_json_and_invalid_field_types_are_machine_readable():
    malformed = client.post(
        "/api/v1/analyze",
        content=b'{"requirements": [',
        headers={"content-type": "application/json"},
    )
    assert malformed.status_code == 422
    assert malformed.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"

    invalid = _analyze([
        {"id": 12, "text": ["not", "text"], "source_line": 1}
    ])
    assert invalid.status_code == 422
    assert invalid.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"
    assert len(invalid.json()["error"]["details"]["issues"]) == 2


def test_client_cannot_replace_canonical_requirement_identity():
    response = _analyze([
        {"id": "CLIENT-ID", "text": COMPLETE_REQUIREMENT, "source_line": 1}
    ])
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"


def test_evidence_findings_and_exact_values_are_serialized_losslessly():
    response = _analyze([{"text": VAGUE_REQUIREMENT, "source_line": 1}])
    assert response.status_code == 200
    result = response.json()["requirements"][0]
    vague = result["features"]["vague_term_occurrences"]
    assert vague["status"] == "DETECTED"
    evidence = next(item for item in result["evidence"] if item["text"] == "швидко")
    assert result["requirement"]["text"][evidence["start_offset"]:evidence["end_offset"]] == evidence["text"]
    unambiguity = result["quality_profile"]["unambiguity"]
    assert unambiguity["value"] == {"numerator": 1, "denominator": 2}
    assert unambiguity["findings"][0]["kind"] == "SIGNAL"
    assert evidence["evidence_id"] in unambiguity["findings"][0]["evidence_refs"]


def test_same_input_produces_identical_complete_json():
    payload = [{"text": COMPLETE_REQUIREMENT, "source_line": 1}]
    first = _analyze(payload)
    second = _analyze(payload)
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()


def test_initial_response_marks_nonconstructible_sections_unavailable():
    body = _analyze([{"text": COMPLETE_REQUIREMENT, "source_line": 1}]).json()
    sections = {item["section"]: item for item in body["section_availability"]}
    assert sections["requirements"]["availability"] == "AVAILABLE"
    assert sections["specification"]["availability"] == "AVAILABLE"
    assert sections["product_quality"] == {
        "section": "product_quality",
        "availability": "UNAVAILABLE",
        "reason_code": "EXTERNAL_EVIDENCE_NOT_SUPPLIED",
    }
    assert sections["reassessment"]["availability"] == "UNAVAILABLE"


def test_case_is_required_and_invalid_case_is_rejected():
    missing = client.post(
        "/api/v1/analyze",
        json={"requirements": [{"text": COMPLETE_REQUIREMENT, "source_line": 1}]},
    )
    invalid = client.post(
        "/api/v1/analyze",
        json={
            "case": "OTHER",
            "requirements": [{"text": COMPLETE_REQUIREMENT, "source_line": 1}],
        },
    )
    assert missing.status_code == invalid.status_code == 422
    assert missing.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"
    assert invalid.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"


def test_controlled_demo_executes_real_accepted_full_model_path():
    response = _controlled_demo()
    assert response.status_code == 200
    body = response.json()
    assert body["analysis_case"] == "CONTROLLED_DEMO"
    assert body["controlled_scenario"] == {
        "id": CONTROLLED_SCENARIO_ID,
        "version": CONTROLLED_SCENARIO_VERSION,
    }
    assert body["full_model"]["prediction"]["predicted_value"] == {
        "numerator": 5,
        "denominator": 6,
    }
    assert body["full_model"]["quantitative_risk_assessments"][0]["local_risk"] == {
        "numerator": 1,
        "denominator": 16,
    }
    assert len(body["full_model"]["checkpoint_evaluations"]) == 2


def test_controlled_demo_exposes_genuine_lifecycle_sections_and_records():
    body = _controlled_demo().json()
    sections = {item["section"]: item for item in body["section_availability"]}
    for name in (
        "product_quality", "risk", "corrective_actions", "process",
        "reassessment", "comparison",
    ):
        assert sections[name]["availability"] == "AVAILABLE"
        assert sections[name]["reason_code"] is None
    assert body["full_model"]["reassessment"]["status"] == "AVAILABLE"
    assert len(body["full_model"]["comparisons"]) == 4
    assert body["reassessment_context"]["context_digest"].startswith("sha256:")


def test_controlled_demo_preserves_canonical_evidence_reuse_decisions():
    body = _controlled_demo().json()
    prior_decisions = body["reassessment_context"]["evidence_reuse_decisions"]
    canonical_decisions = body["full_model"]["reassessment"]["context"][
        "evidence_reuse_decisions"
    ]

    assert prior_decisions == canonical_decisions
    assert all("status" not in decision for decision in prior_decisions)
    assert all("applicability" not in decision for decision in prior_decisions)

    pairs = (
        ("initial_specification", "initial_specification"),
        ("initial_specification_assessment", "initial_specification_assessment"),
        ("corrective_action_resolution", "corrective_action_resolution"),
        ("action_application", "action_application"),
        ("external_revision", "external_revision"),
        ("revised_specification", "revised_specification"),
        ("predecessor_process_state", "process_v1"),
        ("successor_process_state", "process_v2"),
        ("process_transition", "process_transition"),
        ("comparisons", "comparisons"),
    )
    for context_field, model_field in pairs:
        assert body["reassessment_context"][context_field] == body["full_model"][
            model_field
        ]


def test_controlled_demo_rejects_unknown_scenario_and_overrides():
    unknown = client.post(
        "/api/v1/analyze",
        json={
            "case": "CONTROLLED_DEMO",
            "scenario": {"id": "UNKNOWN", "version": "1"},
        },
    )
    override = _controlled_demo({"observed_value": "999"})
    assert unknown.status_code == override.status_code == 422
    assert unknown.json()["error"]["code"] == "INVALID_CONTROLLED_DEMO_REQUEST"
    assert override.json()["error"]["code"] == "INVALID_CONTROLLED_DEMO_REQUEST"


def test_reassessment_executes_real_path_from_stateless_canonical_context():
    demo = _controlled_demo()
    assert demo.status_code == 200
    prior_context = demo.json()["reassessment_context"]
    response = client.post(
        "/api/v1/analyze",
        json={
            "case": "REASSESSMENT",
            "requirements": [
                {"text": V1_R001, "source_line": 1},
                {"text": V2_R002, "source_line": 2},
            ],
            "prior_context": prior_context,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["analysis_case"] == "REASSESSMENT"
    assert [item["requirement"]["text"] for item in body["requirements"]] == [
        V1_R001, V2_R002,
    ]
    assert [item["requirement"]["source_line"] for item in body["requirements"]] == [
        1, 2,
    ]
    assert [item["requirement"]["id"] for item in body["requirements"]] == [
        "R001", "R002",
    ]
    assert body["full_model"]["reassessment"]["status"] == "AVAILABLE"
    comparisons = body["full_model"]["comparisons"]
    assert len(comparisons) == 4
    assert all(item["status"] == "AVAILABLE" for item in comparisons)
    assert [item["comparison_kind"] for item in comparisons] == [
        "INCREASED", "STATE_CHANGED", "STATE_CHANGED", "STATE_CHANGED"
    ]
    assert body["full_model"]["process_transition"]["transition_id"] == {
        "transition_id": "PROCESS-TRANSITION-TC06"
    }


def test_reassessment_rejects_initial_response_as_prior_context():
    initial = _analyze([
        {"text": COMPLETE_REQUIREMENT, "source_line": 1}
    ]).json()
    response = client.post(
        "/api/v1/analyze",
        json={
            "case": "REASSESSMENT",
            "requirements": [
                {"text": V1_R001, "source_line": 1},
                {"text": V2_R002, "source_line": 2},
            ],
            "prior_context": initial,
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_REASSESSMENT_CONTEXT"


def test_reassessment_rejects_missing_or_changed_lifecycle_prerequisites():
    context = _controlled_demo().json()["reassessment_context"]
    del context["action_application"]
    missing = client.post(
        "/api/v1/analyze",
        json={
            "case": "REASSESSMENT",
            "requirements": [
                {"text": V1_R001, "source_line": 1},
                {"text": V2_R002, "source_line": 2},
            ],
            "prior_context": context,
        },
    )
    assert missing.status_code == 422
    assert missing.json()["error"]["code"] == "INVALID_REASSESSMENT_CONTEXT"

    context = _controlled_demo().json()["reassessment_context"]
    context["evidence_reuse_decisions"] = []
    changed = client.post(
        "/api/v1/analyze",
        json={
            "case": "REASSESSMENT",
            "requirements": [
                {"text": V1_R001, "source_line": 1},
                {"text": V2_R002, "source_line": 2},
            ],
            "prior_context": context,
        },
    )
    assert changed.status_code == 422
    assert changed.json()["error"]["code"] == "INVALID_REASSESSMENT_CONTEXT"
    assert changed.json()["error"]["details"]["reason_code"] == (
        "PRIOR_LIFECYCLE_CONTEXT_MISMATCH"
    )


def test_reassessment_rejects_arbitrary_revised_specification():
    context = _controlled_demo().json()["reassessment_context"]
    response = client.post(
        "/api/v1/analyze",
        json={
            "case": "REASSESSMENT",
            "requirements": [
                {"text": V1_R001, "source_line": 1},
                {"text": "Довільна нова вимога.", "source_line": 2},
            ],
            "prior_context": context,
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "INVALID_REASSESSMENT_CONTEXT"
    assert response.json()["error"]["details"]["reason_code"] == (
        "REVISED_SPECIFICATION_MISMATCH"
    )


def test_accepted_precondition_failure_has_stable_safe_error(monkeypatch):
    def reject(_request):
        raise ValueError("sensitive implementation detail")

    monkeypatch.setattr(app_module, "run_initial", reject)
    response = _analyze([{"text": COMPLETE_REQUIREMENT, "source_line": 1}])
    assert response.status_code == 422
    assert response.json()["error"] == {
        "code": "ANALYSIS_VALIDATION_FAILED",
        "details": {"reason_code": "ACCEPTED_APPLICATION_PRECONDITION_FAILED"},
        "path": None,
    }
    assert "sensitive" not in response.text


def test_unexpected_failure_does_not_expose_internal_details(monkeypatch):
    def fail(_request):
        raise RuntimeError("C:\\secret\\source.py traceback")

    monkeypatch.setattr(app_module, "run_initial", fail)
    safe_client = TestClient(app, raise_server_exceptions=False)
    response = safe_client.post(
        "/api/v1/analyze",
        json={
            "case": "INITIAL",
            "requirements": [{"text": COMPLETE_REQUIREMENT, "source_line": 1}],
        },
    )
    assert response.status_code == 500
    assert response.json()["error"]["code"] == "ANALYSIS_INTERNAL_FAILURE"
    assert "secret" not in response.text
    assert "traceback" not in response.text.lower()


def test_openapi_uses_discriminated_three_case_request_contract():
    openapi = app.openapi()
    schema = openapi["paths"]["/api/v1/analyze"]["post"]["requestBody"][
        "content"
    ]["application/json"]["schema"]
    assert schema["discriminator"]["propertyName"] == "case"
    assert set(schema["discriminator"]["mapping"]) == {
        "INITIAL", "CONTROLLED_DEMO", "REASSESSMENT"
    }
    assert len(schema["oneOf"]) == 3

    requirement = openapi["components"]["schemas"]["RequirementInput"]
    assert set(requirement["required"]) == {"text", "source_line"}
    assert requirement["properties"]["source_line"]["exclusiveMinimum"] == 0

    response = openapi["components"]["schemas"]["AnalyzeResponse"]
    full_model = response["properties"]["full_model"]
    assert {
        item.get("$ref") for item in full_model["anyOf"] if "$ref" in item
    } == {"#/components/schemas/FullModelRecordsResponse"}
    families = openapi["components"]["schemas"]["FullModelRecordsResponse"]
    assert {
        "criterion_binding",
        "observed_product_quality",
        "risk_assessments",
        "corrective_action_resolution",
        "reassessment",
        "comparisons",
        "process_transition",
        "checkpoint_evaluations",
    } <= set(families["properties"])
    assert families["additionalProperties"] is False
