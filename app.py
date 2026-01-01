"""
Flask application that exposes two endpoints:
- GET /health for uptime checks
- POST /event to validate incoming events and route them through the rule engine
"""

from flask import Flask, jsonify, request

from router import route_event
from schema import validate_and_normalize_event
from actions import execute_action


app = Flask(__name__)


@app.get("/health")
def health() -> dict:
    """Simple healthcheck used by monitoring or uptime tools."""
    return {"service": "workflow_event_orchestrator", "status": "ok"}


@app.post("/event")
def handle_event():
    """Validate, normalize, route, and EXECUTE an incoming event."""
    payload = request.get_json(silent=True)
    normalized, errors = validate_and_normalize_event(payload)

    if errors:
        return jsonify({"errors": errors}), 400

    # 1. DECIDE (The Brain)
    routing_details = route_event(normalized)

    # 2. ACT (The Hands) <--- THIS IS THE NEW PART
    # We take the "next_action" from the decision and execute it immediately.
    execution_result = execute_action(
        routing_details["next_action"],
        normalized
    )

    response_body = {
        "normalized_event": normalized,
        **routing_details,
        "execution_log": execution_result # We return proof that we did something.
    }

    return jsonify(response_body), 200


if __name__ == "__main__":
    # Change port=5000 to port=5001 to avoid the macOS AirPlay conflict
    app.run(host="0.0.0.0", port=5001, debug=True)
