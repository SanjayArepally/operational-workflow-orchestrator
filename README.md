# Workflow Event Orchestrator

A beginner-friendly practice project that mirrors the kind of workflow automation work a Forward Deployed Product Engineer (FDPE) at Spring Labs might perform. The API receives raw JSON events from customer systems, validates and normalizes them, classifies the workflow category, and recommends the next action.

## Why this project matters
Spring Labs builds AI-native workflow automation for banks and fintechs. FDPEs often:
- Map customer event payloads to internal workflows.
- Normalize and validate JSON so downstream automation is reliable.
- Debug routing behavior when a new event type arrives.
- Share reproducible examples with teammates via Postman collections.

This tiny Flask API is a sandbox for those skills.

## Project structure
- `app.py` – Flask server exposing `/health` and `/event` endpoints.
- `schema.py` – validation and normalization helpers for incoming JSON.
- `router.py` – rule engine that maps `event_type` values to workflow categories and actions.
- `test_router.py` – pytest coverage for happy paths and validation failures.
- `Workflow_Event_Orchestrator.postman_collection.json` – Postman collection for easy manual testing.
- `requirements.txt` – Python dependencies.

## Setup
1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the API**
   ```bash
   python app.py
   ```
   The server listens on `http://0.0.0.0:5000`.

3. **Health check**
   ```bash
   curl http://localhost:5000/health
   ```

## Using the `/event` endpoint
Send a JSON body containing these required fields: `event_id`, `event_type`, `source_system`, `customer_id`, and `metadata` (a dictionary). Example request:

```bash
curl -X POST http://localhost:5000/event \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt-123",
    "event_type": "transaction_dispute_opened",
    "source_system": "card_processor",
    "customer_id": "cust-42",
    "metadata": {"amount": 42.00}
  }'
```

Example response:
```json
{
  "normalized_event": {
    "event_id": "evt-123",
    "event_type": "transaction_dispute_opened",
    "source_system": "card_processor",
    "customer_id": "cust-42",
    "metadata": {"amount": 42.0}
  },
  "workflow_category": "dispute",
  "next_action": "initiate_investigation",
  "notes": "Dispute opened: start the investigation flow."
}
```

### Routing rules
- `transaction_dispute_opened` → workflow `dispute`, action `initiate_investigation`
- `kyc_verification_failed` → workflow `compliance`, action `request_additional_documents`
- `document_uploaded` → workflow `document`, action `queue_for_review`
- anything else → workflow `unknown`, action `manual_review`

### Validation behavior
- Missing required fields return HTTP 400 with an `errors` object describing what to fix.
- Strings are trimmed to remove accidental whitespace.
- `metadata` must be a JSON object (Python `dict`).

## Running tests
```bash
pytest
```

## Postman collection
Import `Workflow_Event_Orchestrator.postman_collection.json` into Postman. Set `base_url` to your running server (e.g., `http://localhost:5000`). The collection includes:
- `GET /health`
- `POST /event` examples for dispute, KYC failure, and an unknown event
- A simple test script that checks `workflow_category` exists in responses

## How this mirrors FDPE work at Spring Labs
- **JSON debugging**: You learn how a small typo or missing field triggers validation errors.
- **Workflow mapping**: Routing rules show how event types translate to next actions.
- **Automation mindset**: The code is structured so you could swap in a more advanced rule engine later.
- **Postman usage**: Sharing a collection keeps teammates aligned on expected payloads.

Use this project to practice iterating quickly, adding new event types, and confirming behavior with both automated tests and Postman.
