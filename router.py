"""
Routing rules and workflow classification logic.
This mimics a tiny rule engine that looks at an event_type and decides
which workflow bucket the event should follow inside a bank or fintech.
"""

from typing import Dict, Tuple


# Simple mapping to keep the routing easy to explain.
ROUTING_TABLE: Dict[str, Tuple[str, str, str]] = {
    "transaction_dispute_opened": (
        "dispute",
        "initiate_investigation",
        "Dispute opened: start the investigation flow."
    ),
    "kyc_verification_failed": (
        "compliance",
        "request_additional_documents",
        "KYC failed: collect more documents to satisfy compliance."
    ),
    "document_uploaded": (
        "document",
        "queue_for_review",
        "Document uploaded: send to review queue."
    ),
}


# ... keeping existing imports and ROUTING_TABLE ...

def route_event(event: Dict[str, str]) -> Dict[str, str]:
    """Return workflow classification details for an event."""
    
    event_type = event.get("event_type")
    metadata = event.get("metadata", {})

    # --- OUR NEW LOGIC STARTS HERE ---
    # This shows we can implement business rules, not just static routing.
    
    if event_type == "transaction_fraud_detected":
        risk_score = metadata.get("risk_score", 0)
        
        # Conditional Logic: High risk freezes account; Medium risk asks for 2FA.
        if risk_score >= 90:
            return {
                "workflow_category": "security_ops",
                "next_action": "freeze_account_immediate",
                "notes": f"CRITICAL: High risk score ({risk_score}). Account frozen automatically."
            }
        elif risk_score >= 50:
            return {
                "workflow_category": "security_ops",
                "next_action": "trigger_step_up_auth",
                "notes": f"WARN: Medium risk score ({risk_score}). Require 2FA verification."
            }
        else:
             return {
                "workflow_category": "analytics",
                "next_action": "log_for_review",
                "notes": f"INFO: Low risk score ({risk_score}). Logged for weekly audit."
            }
    # --- OUR NEW LOGIC ENDS HERE ---

    # Fallback to the original static table for everything else
    workflow_category, next_action, notes = ROUTING_TABLE.get(
        event_type,
        (
            "unknown",
            "manual_review",
            "Unknown event type: fallback to a human review path."
        ),
    )

    return {
        "workflow_category": workflow_category,
        "next_action": next_action,
        "notes": notes,
    }