import argparse
from agents.orchestrator import OrchestratorAgent
from monitoring.metrics import Metrics

metrics = Metrics()

def run_query(query: str, customer_id: str, issue_raised_at: str = None):
    orchestrator = OrchestratorAgent()
    result = orchestrator.run(query, customer_id, issue_raised_at)
    escalated = result["findings"].get("escalation", {}).get("should_escalate", False)
    metrics.record_session(query, result["agents_used"],
                           result["total_tokens"], result["total_time"], escalated)
    return result

def generate_answer(result: dict):
    findings   = result["findings"]
    account    = findings.get("account",    {})
    feature    = findings.get("feature",    {})
    contract   = findings.get("contract",   {})
    escalation = findings.get("escalation", {})

    # ── Guard — Suspended account ─────────────────────────────
    if account.get("account_status") == "suspended":
        lines = []
        lines.append(f"Customer : {account.get('full_name','Unknown')} | Plan: {account.get('plan_name','Unknown')} | Status: SUSPENDED")
        lines.append("")
        lines.append(f"Your account is currently suspended.")
        lines.append(f"Reason   : {account.get('suspension_reason', 'Overdue payments')}")
        lines.append(f"Overdue  : ${round(account.get('overdue_amount', 0), 2)}")
        lines.append(f"Payments : {account.get('overdue_payments', 0)} overdue payments")
        lines.append("")
        lines.append("You cannot access any features until your account is reactivated.")
        lines.append("Please contact our billing team to resolve your outstanding payments.")
        if escalation.get("ticket_id"):
            lines.append("")
            lines.append(f"Ticket   : {escalation.get('ticket_id')}")
            lines.append(f"Priority : {escalation.get('priority')}")
            lines.append(f"Team     : {escalation.get('assigned_team')}")
        return "\n".join(lines)

    # ── Guard — Inactive account ──────────────────────────────
    if account.get("account_status") == "inactive":
        return "Your account is inactive. Please contact support to reactivate it."

    # ── Build complete database context ───────────────────────
    plan_prices = {
        "plan_starter":    29.99,
        "plan_pro":        99.99,
        "plan_enterprise": 299.99
    }
    plan_id       = account.get("plan_id", "")
    monthly_price = plan_prices.get(plan_id, 0)

    context = f"""
CUSTOMER DATABASE DATA:
Name             : {account.get('full_name', 'Unknown')}
Company          : {account.get('company', 'Unknown')}
Plan Name        : {account.get('plan_name', 'Unknown')}
Plan ID          : {plan_id}
Monthly Price    : ${monthly_price}/month
Account Status   : {account.get('account_status', 'Unknown')}
Seats Used       : {account.get('seats_used', 'Unknown')}
Max Seats        : {'10' if plan_id == 'plan_starter' else '25' if plan_id == 'plan_pro' else 'Unlimited'}
Seats Remaining  : {10 - int(account.get('seats_used', 0)) if plan_id == 'plan_starter' else 25 - int(account.get('seats_used', 0)) if plan_id == 'plan_pro' else 'Unlimited'}
Billing Health   : {account.get('billing_health', 'Unknown')}
Overdue Payments : {account.get('overdue_payments', 0)}
Overdue Amount   : ${round(account.get('overdue_amount', 0), 2)}
Last Login       : {account.get('last_login', 'Unknown')}
Enabled Features : {', '.join(account.get('enabled_features', []))}
Support Tier     : {'Community' if plan_id == 'plan_starter' else 'Priority' if plan_id == 'plan_pro' else 'Dedicated'}
"""

    if feature and feature.get("display_name"):
        context += f"""
FEATURE DATABASE DATA:
Feature Name     : {feature.get('display_name', 'Unknown')}
Available on Plan: {feature.get('feature_available_on_plan', False)}
Available on     : {', '.join(feature.get('available_on_plans', []))}
Setup Guide      : {feature.get('setup_guide', 'Not available')}
Capabilities     : {', '.join(feature.get('capabilities', []))}
Limitations      : {', '.join(feature.get('limitations', []))}
Common Issues    : {feature.get('common_issues', 'None')}
Mismatch Found   : {feature.get('has_mismatch', False)}
Mismatch Detail  : {list(feature.get('mismatches_detected', {}).values())[0].get('mismatch_detail', 'None') if feature.get('mismatches_detected') else 'None'}
"""

    if contract and contract.get("contract_found"):
        context += f"""
CONTRACT DATABASE DATA:
Contract ID      : {contract.get('contract_id', 'None')}
SLA Response     : {contract.get('sla_first_response_hours', 'Unknown')} hours
SLA Resolution   : {contract.get('sla_resolution_hours', 'Unknown')} hours
SLA Violated     : {contract.get('sla_violated', False)}
Breach Hours     : {contract.get('breach_hours', 0)}
"""

    if escalation and escalation.get("should_escalate"):
        context += f"""
ESCALATION DATA:
Escalated        : {escalation.get('should_escalate', False)}
Ticket ID        : {escalation.get('ticket_id', 'None')}
Priority         : {escalation.get('priority', 'None')}
Team             : {escalation.get('assigned_team', 'None')}
Reason           : {escalation.get('reason', 'None')}
"""

    # ── Ask LLM to answer the exact question ──────────────────
    from llm.llm_factory import get_llm
    from langchain_core.messages import SystemMessage, HumanMessage

    system_prompt = """You are a customer support agent for TechCorp.
Answer the customer's EXACT question using ONLY the database data provided below.

STRICT RULES:
1. Answer the customer's exact question directly in the first sentence
2. Use ONLY data provided — never add anything not in the data
3. Keep response to maximum 3 sentences
4. Never show floating point numbers — always round to 2 decimal places
5. If asked about price — state the exact monthly price from the data
6. If asked about features — list exactly what is in enabled_features
7. If asked about seats — calculate seats remaining from the data
8. If the answer is not in the data — say I do not have that information
9. Never make up information"""

    user_prompt = f"""Customer Question: {result['query']}

{context}

Answer the customer's exact question using only the above data."""

    try:
        llm, _ = get_llm()
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        response     = llm.invoke(messages)
        final_answer = response.content.strip()

        header = f"Customer : {account.get('full_name','Unknown')} | Plan: {account.get('plan_name','Unknown')} | Status: {account.get('account_status','Unknown').capitalize()}"

        result_lines = [header, "", final_answer]

        if escalation.get("should_escalate"):
            result_lines.append("")
            result_lines.append(f"Ticket   : {escalation.get('ticket_id')} | Priority: {escalation.get('priority')} | Team: {escalation.get('assigned_team')}")

        return "\n".join(result_lines)

    except Exception as e:
        lines = [f"Customer : {account.get('full_name','Unknown')} | Plan: {account.get('plan_name','Unknown')}"]
        lines.append("")
        if account.get("llm_summary"): lines.append(account["llm_summary"])
        if feature.get("llm_summary"): lines.append(feature["llm_summary"])
        if contract.get("llm_summary"):lines.append(contract["llm_summary"])
        return "\n".join(lines)



#Parser reads what I have typed
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--query",      type=str, required=True)
    parser.add_argument("--customer",   type=str, default="CUST_001")
    parser.add_argument("--issue-date", type=str, default=None)
    args = parser.parse_args()
     
    #run_query function is called 
    result = run_query(args.query, args.customer, args.issue_date)
    answer = generate_answer(result)

    print("\n" + "="*60)
    print("ANSWER")
    print("="*60)
    print(answer)
    print("="*60)
    print(f"\nAgents used  : {', '.join(result['agents_used'])}")
    print(f"Total tokens : {result['total_tokens']}")
    print(f"Total time   : {result['total_time']}s")