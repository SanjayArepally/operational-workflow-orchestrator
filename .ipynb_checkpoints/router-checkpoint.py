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


def route_event(event: Dict[str, str]) -> Dict[str, str]:
    """Return workflow classification details for an event.

    The event is expected to be normalized already. Unknown event types are
    routed to manual review so a human can inspect them.
    """

    workflow_category, next_action, notes = ROUTING_TABLE.get(
        event.get("event_type"),
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
