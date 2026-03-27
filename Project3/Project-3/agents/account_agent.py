import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.base_agent import BaseAgent
from tools.account_tools import AccountTools

class AccountAgent(BaseAgent):
    def __init__(self):
        super().__init__("Account Agent", "Investigate customer account, plan, billing and status")
        self.tools = AccountTools()

    def run(self, customer_id: str, shared_context: dict):
        self._start()
        self._log("Task", f"Investigating account for customer {customer_id}")

        _, customer = self.tools.lookup_customer(customer_id)
        if not customer:
            self._log("Error", "Customer not found in database")
            self.findings["error"] = "Customer not found"
            self._finish()
            return self.findings

        self._log("Found", f"Customer: {customer['full_name']} | Plan: {customer['plan_id']} | Status: {customer['account_status']}")

        _, status   = self.tools.check_account_status(customer_id)
        _, billing  = self.tools.get_billing_history(customer_id)
        _, features = self.tools.list_enabled_features(customer_id)

        self.findings = {
            "customer_id":      customer_id,
            "full_name":        customer["full_name"],
            "email":            customer["email"],
            "company":          customer["company_name"],
            "plan_id":          customer["plan_id"],
            "plan_name":        customer.get("plan_details", {}).get("plan_name", customer["plan_id"]),
            "account_status":   customer["account_status"],
            "suspension_reason":customer.get("suspension_reason"),
            "seats_used":       customer["seats_used"],
            "enabled_features": features or [],
            "billing_health":   billing.get("payment_health") if billing else "unknown",
            "overdue_payments": billing.get("overdue_count", 0) if billing else 0,
            "overdue_amount":   billing.get("overdue_amount", 0) if billing else 0,
            "billing_records":  billing.get("records", []) if billing else [],
            "last_login":       status.get("last_login") if status else "unknown"
        }

        system_prompt = """You are the Account Agent in a customer support AI system.
Your job is to summarize ONLY the data provided to you from the database.
STRICT RULES:
- ONLY use the exact data given below. Do NOT add any information not present in the data.
- Do NOT make assumptions or add generic statements.
- Do NOT mention features or details not explicitly listed.
- If a field is None or unknown, say so directly.
- Keep your summary to 2-3 sentences maximum.
- Be factual and precise."""

        user_prompt = f"""Summarize this customer's account status based ONLY on this database data:

Customer Name: {self.findings['full_name']}
Company: {self.findings['company']}
Plan: {self.findings['plan_name']}
Account Status: {self.findings['account_status']}
Suspension Reason: {self.findings['suspension_reason']}
Seats Used: {self.findings['seats_used']}
Billing Health: {self.findings['billing_health']}
Overdue Payments Count: {self.findings['overdue_payments']}
Overdue Amount: ${self.findings['overdue_amount']}
Enabled Features: {', '.join(self.findings['enabled_features']) if self.findings['enabled_features'] else 'None'}
Last Login: {self.findings['last_login']}

Write a 2-3 sentence factual summary using ONLY the above data."""

        self._log("LLM Call", "Generating account summary from database data...")
        self.findings["llm_summary"] = self._ask_llm(system_prompt, user_prompt)

        shared_context["account"]       = self.findings
        shared_context["customer_name"] = customer["full_name"]
        shared_context["plan_id"]       = customer["plan_id"]

        elapsed = self._finish()
        self.findings["time_taken"] = elapsed
        return self.findings