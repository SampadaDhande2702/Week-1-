import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.base_agent import BaseAgent
from tools.contract_tools import ContractTools
from datetime import datetime

class ContractAgent(BaseAgent):
    def __init__(self):
        super().__init__("Contract Agent", "Retrieve contracts, validate SLA, check entitlements")
        self.tools = ContractTools()

    def run(self, customer_id: str, issue_raised_at: str, shared_context: dict):
        self._start()
        self._log("Task", f"Reviewing contract and SLA for customer {customer_id}")

        _, contract = self.tools.lookup_contract(customer_id)
        if not contract:
            self._log("Info", "No contract found — using standard plan SLA terms")
            self.findings = {
                "contract_found": False,
                "sla_violated":   False,
                "message":        "No custom contract found. Standard plan terms apply."
            }
            shared_context["contract"] = self.findings
            self._finish()
            return self.findings

        _, terms        = self.tools.get_contract_terms(contract["contract_id"])
        _, sla          = self.tools.validate_sla_compliance(customer_id, issue_raised_at)
        _, entitlements = self.tools.get_included_features(contract["contract_id"])

        violation = None
        if sla and sla.get("sla_violated"):
            self._log("Alert", f"SLA VIOLATED — {sla['breach_hours']} hours over limit!")
            _, violation = self.tools.write_violation(
                customer_id,
                contract["contract_id"],
                {
                    "violation_type":  "sla_breach",
                    "breach_hours":    sla["breach_hours"],
                    "sla_limit_hours": sla["sla_first_response_hours"],
                    "hours_elapsed":   sla["hours_elapsed"],
                    "severity":        sla["severity"]
                }
            )

        self.findings = {
            "customer_id":              customer_id,
            "contract_found":           True,
            "contract_id":              contract["contract_id"],
            "plan_id":                  contract["plan_id"],
            "start_date":               contract["start_date"],
            "end_date":                 contract["end_date"],
            "sla_first_response_hours": contract["sla_first_response_hours"],
            "sla_resolution_hours":     contract["sla_resolution_hours"],
            "contracted_features":      contract["contracted_features"],
            "pricing_terms":            contract["pricing_terms"],
            "signed_by":                contract["signed_by"],
            "sla_check":                sla if sla else {},
            "sla_violated":             sla.get("sla_violated", False) if sla else False,
            "breach_hours":             sla.get("breach_hours", 0) if sla else 0,
            "severity":                 sla.get("severity", "low") if sla else "low",
            "entitlements":             entitlements if entitlements else {},
            "violation_written":        violation is not None,
            "violation":                violation
        }

        system_prompt = """You are the Contract Agent in a customer support AI system.
Your job is to explain contract and SLA status using ONLY the database data provided.
STRICT RULES:
- ONLY use the exact contract data given. Do NOT add assumptions.
- State SLA hours exactly as in the contract data.
- If SLA is violated, state the breach hours exactly as calculated.
- Do NOT add legal advice or generic statements about contracts.
- Keep response to 3 sentences maximum."""

        user_prompt = f"""Explain the contract and SLA situation using ONLY this database data:

Contract ID: {self.findings['contract_id']}
Contract Start: {self.findings['start_date']}
Contract End: {self.findings['end_date']}
SLA First Response Limit: {self.findings['sla_first_response_hours']} hours
SLA Resolution Limit: {self.findings['sla_resolution_hours']} hours
Contracted Features: {', '.join(self.findings['contracted_features'])}
Pricing Terms: {self.findings['pricing_terms']}
SLA Violated: {self.findings['sla_violated']}
Hours Elapsed Since Issue: {sla.get('hours_elapsed', 'unknown') if sla else 'unknown'}
Breach Hours (hours over SLA limit): {self.findings['breach_hours']}
Severity: {self.findings['severity']}

Write a 3 sentence response using ONLY the above data."""

        self._log("LLM Call", "Generating contract summary from database data...")
        self.findings["llm_summary"] = self._ask_llm(system_prompt, user_prompt)

        shared_context["contract"] = self.findings

        elapsed = self._finish()
        self.findings["time_taken"] = elapsed
        return self.findings