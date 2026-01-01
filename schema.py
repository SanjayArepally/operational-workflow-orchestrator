"""
Payload validation and normalization helpers.
The goal is to keep the rules easy to read for beginners who are exploring
how incoming JSON from customer systems is cleaned up before routing.
"""

from typing import Any, Dict, Tuple


REQUIRED_FIELDS = {
    "event_id": str,
    "event_type": str,
    "source_system": str,
    "customer_id": str,
    "metadata": dict,
}


def _coerce_to_str(value: Any) -> str:
    """Convert a value to string and strip whitespace for consistent handling."""
    return str(value).strip()


def validate_and_normalize_event(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, str]]:
    """Validate required fields and return a normalized representation.

    Returns a tuple of (normalized_event, errors). If errors is not empty, callers
    should treat the request as invalid and return a 400 response.
    """

    normalized: Dict[str, Any] = {}
    errors: Dict[str, str] = {}

    if not isinstance(payload, dict):
        return normalized, {"payload": "Request body must be a JSON object."}

    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in payload:
            errors[field] = "Field is required."
            continue

        value = payload[field]
        if not isinstance(value, expected_type):
            errors[field] = f"Expected {expected_type.__name__}."
            continue

        # Normalize strings by trimming whitespace. Metadata is kept as-is once type-checked.
        if expected_type is str:
            normalized[field] = _coerce_to_str(value)
        else:
            normalized[field] = value

    return normalized, errors
