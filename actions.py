"""
Action Executors.
In a real Northslope/Palantir deployment, these would be API calls to external systems 
(e.g., Core Banking, Salesforce, Twilio). 
Here, we mock them to demonstrate the "Write-Back" loop.
"""

def execute_action(action_key: str, context: dict) -> str:
    """
    Takes the decision from the Router and performs the physical side-effect.
    """
    customer_id = context.get("customer_id", "UNKNOWN")

    # 1. The "Kill Switch" (High Importance)
    if action_key == "freeze_account_immediate":
        # Real world: requests.post(f"https://core-banking/api/users/{customer_id}/lock")
        return f"⚡ EXECUTION: Sent LOCK command to Core Banking for user {customer_id}. Latency: 12ms."

    # 2. The "Friction" (Medium Importance)
    elif action_key == "trigger_step_up_auth":
        # Real world: Send SMS via Twilio
        return f"⚠️ EXECUTION: SMS 2FA code sent to user {customer_id}. Session flagged."

    # 3. Standard Ops
    elif action_key == "initiate_investigation":
        return f"✅ EXECUTION: Ticket #9902 created in Jira for Ops Team."

    # Default fallback
    return f"ℹ️ EXECUTION: Action '{action_key}' logged to audit trail."