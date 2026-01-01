# Operational Workflow Orchestrator

An event-driven decision engine that ingests raw signals, applies conditional business logic, and executes operational actions in real-time.

**Status:** Ready for Deployment ⚡

---

## 📖 Project Overview
This project is an advanced extension of the **Spring Labs Forward Deployed Product Engineer (FDPE)** reference architecture.

While traditional workflow engines function as "passive routers" (flagging issues for human review), this system is designed as a **"Closed-Loop Operational Node."** It doesn't just analyze data; it takes autonomous action on high-stakes signals to reduce time-to-resolution from hours to milliseconds.

### Core Capabilities
1.  **Event Ingestion & Normalization:** Validates messy JSON payloads against a strict ontology (`schema.py`).
2.  **Conditional Business Logic:** Implements dynamic routing rules rather than static mapping.
    * *Example:* Differentiates between "Suspicious Activity" (requires 2FA) and "Critical Fraud" (requires immediate lock).
3.  **Automated Operational Write-Back:** A dedicated execution layer (`actions.py`) that mocks downstream API calls to external systems (e.g., Core Banking, CRM) to resolve threats instantly.

---

## 🛠️ Architecture

**Stack:** Python 3.12, Flask, Pytest

| Component | Responsibility | Status |
| :--- | :--- | :--- |
| **Ingest** (`app.py`) | API Gateway receiving JSON payloads. | **Enhanced** (Added Execution Loop) |
| **Ontology** (`schema.py`) | Enforces data types and structure. | Base Implementation |
| **Logic** (`router.py`) | Determines the "Next Best Action." | **Advanced** (Added Fraud Risk Thresholds) |
| **Action** (`actions.py`) | Executes the decision (Side-Effects). | **[NEW]** Mocks external API calls |

---

## 🚀 Quick Start

# 1. Setup
## Install dependencies
pip install -r requirements.txt

#2. Run the Engine
python app.py
The server listens on port 5001 to prevent conflicts with macOS AirPlay services.

#3. Health Check
curl http://localhost:5001/health

⚡ Operational Scenarios
Scenario A: The "Kill Switch" (Critical Fraud)
Simulate a high-risk fraud event where the AI Risk Score is > 90. The system detects the threat and automatically locks the account.

Request:
curl -X POST http://localhost:5001/event \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": "hack-101",
    "event_type": "transaction_fraud_detected",
    "source_system": "ai_risk_engine",
    "customer_id": "hacker_007",
    "metadata": {"risk_score": 99}
  }'
Response (Note the execution_log):

JSON

{
  "workflow_category": "security_ops",
  "next_action": "freeze_account_immediate",
  "execution_log": "⚡ EXECUTION: Sent LOCK command to Core Banking for user hacker_007. Latency: 12ms."
}

Scenario B: Standard Dispute (Base Workflow)
Simulate a standard customer dispute that requires human investigation.

Request:
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

pytest
Current Status: 7/7 Tests Passed (Includes test_fraud_high_risk_freezes_account and test_fraud_medium_risk_triggers_2fa).

#📬 Postman Collection
For easier testing, a Postman collection is included.

Import Workflow_Event_Orchestrator.postman_collection.json.

Necessary: Ensure your environment base_url is set to http://localhost:5001.

The collection includes pre-configured requests for:

Critical Fraud Events (High Risk)

Standard Disputes

Health Checks

👏 Attribution
The Spring Labs Engineering Challenge originally inspired this project. I have significantly extended it to demonstrate Forward Deployed Engineering principles, explicitly focusing on the transition from insight (identifying a problem) to action (solving it programmatically).
* **Original Repository:** (https://github.com/MWJACK96/workflow_event_orchestrator.git)
