"""
Pytest suite covering routing and validation scenarios.
The tests use Flask's test client to send requests to the API just like Postman would.
"""

import json

import pytest

from app import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_dispute_event_routes_to_investigation(client):
    response = client.post(
        "/event",
        data=json.dumps(
            {
                "event_id": "evt-1",
                "event_type": "transaction_dispute_opened",
                "source_system": "card_processor",
                "customer_id": "cust-123",
                "metadata": {"amount": 42.0},
            }
        ),
        content_type="application/json",
    )

    body = response.get_json()
    assert response.status_code == 200
    assert body["next_action"] == "initiate_investigation"


def test_kyc_failure_requests_additional_documents(client):
    response = client.post(
        "/event",
        data=json.dumps(
            {
                "event_id": "evt-2",
                "event_type": "kyc_verification_failed",
                "source_system": "kyc_vendor",
                "customer_id": "cust-999",
                "metadata": {"attempt": 2},
            }
        ),
        content_type="application/json",
    )

    body = response.get_json()
    assert response.status_code == 200
    assert body["next_action"] == "request_additional_documents"


def test_document_upload_routes_to_review_queue(client):
    response = client.post(
        "/event",
        data=json.dumps(
            {
                "event_id": "evt-3",
                "event_type": "document_uploaded",
                "source_system": "upload_portal",
                "customer_id": "cust-555",
                "metadata": {"document_type": "id_card"},
            }
        ),
        content_type="application/json",
    )

    body = response.get_json()
    assert response.status_code == 200
    assert body["next_action"] == "queue_for_review"


def test_unknown_event_falls_back_to_manual_review(client):
    response = client.post(
        "/event",
        data=json.dumps(
            {
                "event_id": "evt-4",
                "event_type": "unmapped_event",
                "source_system": "legacy_core",
                "customer_id": "cust-000",
                "metadata": {"raw": True},
            }
        ),
        content_type="application/json",
    )

    body = response.get_json()
    assert response.status_code == 200
    assert body["next_action"] == "manual_review"


def test_missing_required_fields_returns_400(client):
    response = client.post(
        "/event",
        data=json.dumps(
            {
                # event_id is missing on purpose
                "event_type": "transaction_dispute_opened",
                "source_system": "card_processor",
                "customer_id": "cust-123",
                "metadata": {"amount": 42.0},
            }
        ),
        content_type="application/json",
    )

    body = response.get_json()
    assert response.status_code == 400
    assert "event_id" in body["errors"]

def test_fraud_high_risk_freezes_account(client):
    """Test that a high risk score triggers an immediate freeze."""
    response = client.post(
        "/event",
        data=json.dumps(
            {
                "event_id": "evt-fraud-99",
                "event_type": "transaction_fraud_detected",
                "source_system": "ai_risk_engine",
                "customer_id": "cust-bad-actor",
                "metadata": {"risk_score": 95} 
            }
        ),
        content_type="application/json",
    )

    body = response.get_json()
    assert response.status_code == 200
    assert body["next_action"] == "freeze_account_immediate"
    assert "CRITICAL" in body["notes"]


def test_fraud_medium_risk_triggers_2fa(client):
    """Test that a medium risk score allows user to prove identity (Step-up Auth)."""
    response = client.post(
        "/event",
        data=json.dumps(
            {
                "event_id": "evt-fraud-50",
                "event_type": "transaction_fraud_detected",
                "source_system": "ai_risk_engine",
                "customer_id": "cust-traveler",
                "metadata": {"risk_score": 60}
            }
        ),
        content_type="application/json",
    )

    body = response.get_json()
    assert response.status_code == 200
    assert body["next_action"] == "trigger_step_up_auth"
