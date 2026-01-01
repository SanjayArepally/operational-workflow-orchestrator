# Operational Workflow Orchestrator

An event-driven decision engine that ingests raw signals, applies conditional business logic, and executes operational actions in real-time.

**Status:** Ready for Deployment ⚡

---

## 📖 Project Context
This project is an advanced extension of the **Spring Labs Forward Deployed Product Engineer (FDPE)** reference architecture.

While the original architecture serves as a "Passive Router" (classifying events for human review), I re-engineered this system to function as a **"Closed-Loop Operational Node."** It allows for:
1.  **Nuanced Decision Making:** Moving beyond static 1-to-1 mapping to conditional logic thresholds.
2.  **Automated Intervention:** Instantly executing "Write-Back" operations (e.g., locking accounts) to reduce time-to-resolution from hours to milliseconds.

### My Key Contributions
| Feature | Original Architecture | My Operational Extension |
| :--- | :--- | :--- |
| **Logic Engine** | Static Mapping (Event A → Action A) | **Conditional Logic** (Event A + Risk > 90 → Action B) |
| **Execution** | Returns JSON Recommendation | **Active Write-Back** (Mocks API calls to Core Banking) |
| **Scope** | Dispute & Compliance Routing | **High-Velocity Fraud Response** |

---

## 🛠️ Project Structure

- `app.py` – Flask server exposing `/health` and `/event` endpoints. **(Updated to include Execution Loop)**
- `router.py` – Rule engine extended with **fraud risk thresholds** and conditional logic.
- `actions.py` – **[NEW]** Operational layer that mocks external API calls (e.g., `freeze_account`, `send_sms`).
- `schema.py` – Validation and normalization helpers (Enforces strict ontology).
- `test_router.py` – Pytest suite covering happy paths, validation failures, and **new risk logic**.
- `Workflow_Event_Orchestrator.postman_collection.json` – Updated Postman collection for manual testing.
- `requirements.txt` – Python dependencies.

---

## 🚀 Quick Start


```bash
# ### 1. Setup
Install dependencies
pip install -r requirements.txt
2. Run the Engine
Bash

python app.py
Note: The server listens on port 5001 to avoid conflicts with macOS AirPlay services.

3. Health Check
Bash

curl http://localhost:5001/health
⚡ Operational Scenarios
Scenario A: The "Kill Switch" (Critical Fraud)
Context: The system receives a high-risk signal (Score > 90) from the AI Risk Engine. Action: The Logic Engine overrides standard processing and triggers an immediate Account Freeze.

Request:

Bash

curl -X POST http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "hack-101",
    "event_type": "transaction_fraud_detected",
    "source_system": "ai_risk_engine",
    "customer_id": "hacker_007",
    "metadata": {"risk_score": 99}
  }'
Response (Note the Execution Log):

JSON

{
  "workflow_category": "security_ops",
  "next_action": "freeze_account_immediate",
  "execution_log": "⚡ EXECUTION: Sent LOCK command to Core Banking for user hacker_007. Latency: 12ms."
}
Scenario B: Standard Dispute (Base Workflow)
Context: A customer initiates a transaction dispute. Action: The system routes this to the Operations Queue for human review.

Request:

Bash

curl -X POST http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "evt-123",
    "event_type": "transaction_dispute_opened",
    "source_system": "card_processor",
    "customer_id": "cust-42",
    "metadata": {"amount": 42.00}
  }'
Response:

JSON

{
  "next_action": "initiate_investigation",
  "execution_log": "✅ EXECUTION: Ticket #9902 created in Jira for Ops Team."
}
🧪 Testing
The project includes a comprehensive test suite covering both the base routing rules and the new conditional logic thresholds.

Bash

pytest
Current Status: 7/7 Tests Passed (Includes test_fraud_high_risk_freezes_account and test_fraud_medium_risk_triggers_2fa).

📬 Postman Collection
For easier testing, a Postman collection is included.

Import Workflow_Event_Orchestrator.postman_collection.json.

Important: Ensure your environment base_url is set to http://localhost:5001.

The collection includes pre-configured requests for:

Critical Fraud Events (High Risk)

Standard Disputes

Health Checks

👏 Attribution
This project is built upon the excellent Spring Labs Engineering Challenge foundation. I have significantly extended the original architecture to demonstrate Forward Deployed Engineering principles (specifically Operational Write-Back and Conditional Logic).

* **Original Repository:** (https://github.com/MWJACK96/workflow_event_orchestrator.git)
