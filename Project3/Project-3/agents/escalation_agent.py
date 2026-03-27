import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.base_agent import BaseAgent
from tools.escalation_tools import EscalationTools

class EscalationAgent(BaseAgent):
    def __init__(self):
        super().__init__("Escalation Agent", "Decide if human intervention needed, create ticket, route to team")
        self.tools = EscalationTools()

    def run(self, customer_id: str, shared_context: dict):
        self._start()
        self._log("Task", f"Evaluating escalation need for customer {customer_id}")

        account  = shared_context.get("account",  {})
        feature  = shared_context.get("feature",  {})
        contract = shared_context.get("contract", {})

        _, existing = self.tools.check_existing_tickets(customer_id)

        should_escalate = False
        reason   = ""
        priority = "P3"
        severity = "low"
        team     = "support"
        decision_trail = []

        if contract.get("sla_violated"):
            should_escalate = True
            breach   = contract.get("breach_hours", 0)
            severity = "critical" if breach > 48 else "high"
            priority = "P1" if breach > 48 else "P2"
            team     = "engineering"
            reason   = f"SLA violated by {breach} hours against contracted {contract.get('sla_first_response_hours','?')}h limit."
            decision_trail.append(f"SLA breach: {breach} hours over limit")
            self._log("Rule Hit", f"RULE_001 — Critical SLA breach ({breach}h)")

        elif account.get("account_status") == "suspended":
            should_escalate = True
            severity = "high"
            priority = "P2"
            team     = "billing"
            reason   = f"Account suspended. Reason from database: {account.get('suspension_reason','Not specified')}"
            decision_trail.append("Account status is suspended")
            self._log("Rule Hit", "RULE_005 — Account suspended")

        elif feature.get("has_mismatch"):
            should_escalate = True
            severity = "high"
            priority = "P2"
            team     = "engineering"
            mismatch_detail = list(feature.get("mismatches_detected", {}).values())
            reason   = f"Feature mismatch: {mismatch_detail[0].get('mismatch_detail','') if mismatch_detail else 'Customer not receiving entitled features'}"
            decision_trail.append("Feature mismatch flag triggered")
            self._log("Rule Hit", "RULE_003 — Feature mismatch")

        elif account.get("overdue_payments", 0) >= 2:
            should_escalate = True
            severity = "medium"
            priority = "P3"
            team     = "billing"
            reason   = f"{account.get('overdue_payments')} overdue payments totalling ${account.get('overdue_amount', 0)}"
            decision_trail.append("Multiple overdue payments in database")
            self._log("Rule Hit", "RULE_002 — Multiple overdue payments")

        elif feature.get("mismatches_detected", {}).get("seats"):
            should_escalate = True
            severity = "medium"
            priority = "P3"
            team     = "account_mgmt"
            reason   = f"Seat limit exceeded: {feature['mismatches_detected']['seats'].get('mismatch_detail','')}"
            decision_trail.append("Seat limit exceeded per database")
            self._log("Rule Hit", "RULE_004 — Seat limit exceeded")

        else:
            self._log("Decision", "No escalation rules triggered — resolving directly")

        ticket = None
        if should_escalate:
            _, ticket  = self.tools.create_escalation_ticket(
                customer_id=customer_id,
                reason=reason,
                priority=priority,
                severity=severity,
                assigned_team=team,
                notes=f"Decision trail: {' | '.join(decision_trail)}. Account={account.get('account_status')}, Plan={account.get('plan_id')}",
                contract_id=contract.get("contract_id")
            )
            _, routing = self.tools.get_escalation_routing(severity)
            self.tools.notify_support_team(ticket["ticket_id"], team)
            self.tools.log_escalation_reason(ticket["ticket_id"], reason, decision_trail)

        system_prompt = """You are the Escalation Agent in a customer support AI system.
Your job is to communicate escalation decisions using ONLY the data provided.
STRICT RULES:
- ONLY reference data explicitly given below. Do NOT add assumptions.
- State ticket ID, priority, and team exactly as provided.
- If no escalation, clearly say the issue will be resolved directly.
- Do NOT add generic reassurances not based on the data.
- Keep response to 2-3 sentences maximum."""

        user_prompt = f"""Communicate this escalation decision using ONLY this data:

Should Escalate: {should_escalate}
Escalation Reason (from database rules): {reason if reason else 'No escalation needed'}
Priority Level: {priority}
Severity: {severity}
Assigned Team: {team}
Ticket ID: {ticket['ticket_id'] if ticket else 'N/A - No ticket created'}
Decision Trail: {', '.join(decision_trail) if decision_trail else 'No rules triggered'}
Existing Open Tickets: {existing.get('open_tickets', 0) if existing else 0}

Write a 2-3 sentence response using ONLY the above data."""

        self._log("LLM Call", "Generating escalation message from database data...")
        llm_message = self._ask_llm(system_prompt, user_prompt)

        self.findings = {
            "customer_id":     customer_id,
            "should_escalate": should_escalate,
            "reason":          reason if should_escalate else "Issue resolved without escalation",
            "priority":        priority if should_escalate else "N/A",
            "severity":        severity if should_escalate else "N/A",
            "assigned_team":   team if should_escalate else "N/A",
            "ticket":          ticket,
            "ticket_id":       ticket["ticket_id"] if ticket else None,
            "existing_tickets":existing.get("total_tickets", 0) if existing else 0,
            "decision_trail":  decision_trail,
            "llm_summary":     llm_message
        }

        shared_context["escalation"] = self.findings

        elapsed = self._finish()
        self.findings["time_taken"] = elapsed
        return self.findings