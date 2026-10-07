"""Integrated server-side acceptance chain behind Research UI v1.

These tests use the real FastAPI adapter and accepted application services. They
do not render React and do not replace any scientific service with a mock.
"""

from fastapi.testclient import TestClient

from requirements_quality_assessment.api.app import app
from requirements_quality_assessment.full_model.controlled_scenario import (
    CONTROLLED_SCENARIO_ID,
    CONTROLLED_SCENARIO_VERSION,
    V1_R001,
    V2_R002,
)


client = TestClient(app)

INITIAL_REQUIREMENT = (
    "Якщо сервіс недоступний, система повинна відповісти не більше ніж за 2 с."
)


def _post(payload):
    response = client.post("/api/v1/analyze", json=payload)
    assert response.status_code == 200, response.text
    return response.json()


def _sections(body):
    return {item["section"]: item for item in body["section_availability"]}


def _assert_no_floats(value):
    if isinstance(value, dict):
        for nested in value.values():
            _assert_no_floats(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_no_floats(nested)
    else:
        assert not isinstance(value, float)


def test_real_api_acceptance_chain_for_initial_demo_and_formal_reassessment():
    initial = _post({
        "case": "INITIAL",
        "requirements": [{"text": INITIAL_REQUIREMENT, "source_line": 1}],
    })
    assert initial["analysis_case"] == "INITIAL"
    assert initial["full_model"] is None
    assert initial["reassessment_context"] is None
    assert initial["requirements"][0]["requirement"] == {
        "id": "R001",
        "source_line": 1,
        "text": INITIAL_REQUIREMENT,
    }
    initial_sections = _sections(initial)
    assert initial_sections["product_quality"]["reason_code"] == (
        "EXTERNAL_EVIDENCE_NOT_SUPPLIED"
    )
    assert initial_sections["risk"]["reason_code"] == (
        "CONFIRMED_PROBLEM_AND_RISK_INPUTS_NOT_AVAILABLE"
    )
    assert initial_sections["corrective_actions"]["reason_code"] == (
        "CONFIRMED_PROBLEM_NOT_AVAILABLE"
    )
    assert initial_sections["process"]["reason_code"] == (
        "FULL_MODEL_LIFECYCLE_NOT_INVOKED"
    )
    assert initial_sections["reassessment"]["availability"] == "UNAVAILABLE"
    assert initial_sections["comparison"]["availability"] == "UNAVAILABLE"
    assert initial["specification"]["quality_profile"]["completeness"]["value"] == {
        "numerator": 1,
        "denominator": 1,
    }
    assert "overall_score" not in initial
    _assert_no_floats(initial)

    controlled_request = {
        "case": "CONTROLLED_DEMO",
        "scenario": {
            "id": CONTROLLED_SCENARIO_ID,
            "version": CONTROLLED_SCENARIO_VERSION,
        },
    }
    controlled = _post(controlled_request)
    assert controlled["analysis_case"] == "CONTROLLED_DEMO"
    assert controlled["controlled_scenario"] == controlled_request["scenario"]
    assert all(
        _sections(controlled)[section]["availability"] == "AVAILABLE"
        for section in (
            "product_quality",
            "risk",
            "corrective_actions",
            "process",
            "reassessment",
            "comparison",
        )
    )
    full_model = controlled["full_model"]
    assert full_model is not None
    assert full_model["process_v1"]
    assert full_model["process_v2"]
    assert full_model["process_transition"]
    assert len(full_model["checkpoint_evaluations"]) == 2
    assert full_model["reassessment"]["status"] == "AVAILABLE"
    assert len(full_model["comparisons"]) == 4
    assert controlled["reassessment_context"]["context_digest"].startswith("sha256:")
    assert full_model["prediction"]["predicted_value"] == {
        "numerator": 5,
        "denominator": 6,
    }
    assert full_model["quantitative_risk_assessments"][0]["local_risk"] == {
        "numerator": 1,
        "denominator": 16,
    }
    _assert_no_floats(controlled)

    reassessment = _post({
        "case": "REASSESSMENT",
        "requirements": [
            {"text": V1_R001, "source_line": 1},
            {"text": V2_R002, "source_line": 2},
        ],
        "prior_context": controlled["reassessment_context"],
    })
    assert reassessment["analysis_case"] == "REASSESSMENT"
    assert [item["requirement"]["text"] for item in reassessment["requirements"]] == [
        V1_R001,
        V2_R002,
    ]
    assert reassessment["full_model"]["reassessment"]["status"] == "AVAILABLE"
    comparisons = reassessment["full_model"]["comparisons"]
    assert len(comparisons) == 4
    assert all(item["status"] == "AVAILABLE" for item in comparisons)
    assert {
        item["comparison_subject"]["result_family"] for item in comparisons
    } == {
        "QB_CONSISTENCY",
        "CONFIRMED_PROBLEM",
        "BOUNDED_RISK",
        "PRODUCT_QUALITY",
    }
    assert all("STRUCTURED_CHANGE_ONLY" in item["claims"] for item in comparisons)
    required_non_claims = {
        "NO_DIRECTIONAL_QUALITY_INTERPRETATION",
        "NO_CAUSAL_EFFECT_INFERENCE",
        "NO_ACTION_SUCCESS_INFERENCE",
        "NO_STAKEHOLDER_INTENT_VALIDATION",
    }
    assert required_non_claims <= {
        non_claim
        for item in comparisons
        for non_claim in item["non_claims"]
    }
    assert reassessment["limitations"][0] == "NO_ARBITRARY_V1_V2_COMPARISON"
    _assert_no_floats(reassessment)
