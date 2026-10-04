"""HTTP adapter tests using the real accepted analysis pipeline."""

from fastapi.testclient import TestClient

from requirements_quality_assessment.api.app import app


client = TestClient(app)

COMPLETE_REQUIREMENT = (
    "Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с."
)
VAGUE_REQUIREMENT = "Система повинна швидко оновити статус."


def _analyze(requirements):
    return client.post("/api/v1/analyze", json={"requirements": requirements})


def test_health_does_not_run_model():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_single_requirement_runs_real_pipeline_end_to_end():
    response = _analyze([{"id": "R-USER-1", "text": COMPLETE_REQUIREMENT}])
    assert response.status_code == 200
    body = response.json()
    assert body["contract_version"] == "research-api-v1"
    assert body["analysis_case"] == "INITIAL"
    result = body["requirements"][0]
    assert result["requirement"] == {
        "id": "R-USER-1", "source_line": 1, "text": COMPLETE_REQUIREMENT,
    }
    assert result["quality_profile"]["completeness"]["assessment_rule_id"] == "CALC-C-MVP-001"
    assert result["quality_profile"]["verifiability"]["assessment_rule_id"] == "CALC-V-MVP-001"
    assert result["quality_profile"]["unambiguity"]["assessment_rule_id"] == "CALC-U-MVP-001"
    assert body["specification"]["quality_profile"]["completeness"]["total_count"] == 1


def test_multi_requirement_analysis_preserves_order_and_supplied_ids():
    response = _analyze([
        {"id": "EXT-A", "text": COMPLETE_REQUIREMENT},
        {"id": "EXT-B", "text": VAGUE_REQUIREMENT},
    ])
    assert response.status_code == 200
    requirements = response.json()["requirements"]
    assert [item["requirement"]["id"] for item in requirements] == ["EXT-A", "EXT-B"]
    assert [item["requirement"]["source_line"] for item in requirements] == [1, 2]
    assert response.json()["specification"]["quality_profile"]["unambiguity"]["total_count"] == 2


def test_omitted_ids_are_generated_deterministically_by_request_position():
    response = _analyze([{"text": COMPLETE_REQUIREMENT}, {"text": VAGUE_REQUIREMENT}])
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
    response = _analyze([{"id": "R1"}])
    assert response.status_code == 422
    body = response.json()["error"]
    assert body["code"] == "MALFORMED_REQUIREMENT_INPUT"
    assert body["path"][-1] == "text"


def test_blank_text_is_rejected():
    response = _analyze([{"text": " \t "}])
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

    invalid = _analyze([{"id": 12, "text": ["not", "text"]}])
    assert invalid.status_code == 422
    assert invalid.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"
    assert len(invalid.json()["error"]["details"]["issues"]) == 2


def test_duplicate_resolved_ids_are_rejected():
    response = _analyze([
        {"id": "R002", "text": COMPLETE_REQUIREMENT},
        {"text": VAGUE_REQUIREMENT},
    ])
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "MALFORMED_REQUIREMENT_INPUT"


def test_evidence_findings_and_exact_values_are_serialized_losslessly():
    response = _analyze([{"text": VAGUE_REQUIREMENT}])
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
    payload = [{"id": "DET-1", "text": COMPLETE_REQUIREMENT}]
    first = _analyze(payload)
    second = _analyze(payload)
    assert first.status_code == second.status_code == 200
    assert first.json() == second.json()


def test_initial_response_marks_nonconstructible_sections_unavailable():
    body = _analyze([{"text": COMPLETE_REQUIREMENT}]).json()
    sections = {item["section"]: item for item in body["section_availability"]}
    assert sections["requirements"]["availability"] == "AVAILABLE"
    assert sections["specification"]["availability"] == "AVAILABLE"
    assert sections["product_quality"] == {
        "section": "product_quality",
        "availability": "UNAVAILABLE",
        "reason_code": "EXTERNAL_EVIDENCE_NOT_SUPPLIED",
    }
    assert sections["reassessment"]["availability"] == "UNAVAILABLE"
