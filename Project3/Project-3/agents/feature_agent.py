import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.base_agent import BaseAgent
from tools.feature_tools import FeatureTools

class FeatureAgent(BaseAgent):
    def __init__(self):
        super().__init__("Feature Agent", "Check feature availability, docs, usage and mismatches")
        self.tools = FeatureTools()

    def run(self, customer_id: str, feature_name: str, shared_context: dict):
        self._start()
        self._log("Task", f"Investigating feature '{feature_name}' for customer {customer_id}")

        plan_id = shared_context.get("plan_id", "plan_starter")

        _, matrix     = self.tools.get_feature_matrix()
        _, docs       = self.tools.get_feature_documentation(feature_name)
        _, limits     = self.tools.check_feature_limits(feature_name, plan_id)
        _, config     = self.tools.validate_configuration(feature_name, customer_id)
        _, mismatches = self.tools.detect_mismatch(customer_id)

        available_on = docs.get("available_on", []) if docs else []
        is_available = plan_id in available_on

        self.findings = {
            "customer_id":               customer_id,
            "feature_name":              feature_name,
            "plan_id":                   plan_id,
            "feature_available_on_plan": is_available,
            "available_on_plans":        available_on,
            "display_name":              docs.get("display_name") if docs else feature_name,
            "description":               docs.get("description") if docs else "Not found",
            "capabilities":              docs.get("capabilities", []) if docs else [],
            "limitations":               docs.get("limitations", []) if docs else [],
            "setup_guide":               docs.get("setup_guide") if docs else "Not available",
            "expected_behavior":         docs.get("expected_behavior") if docs else "Not available",
            "common_issues":             docs.get("common_issues") if docs else "None documented",
            "plan_limit":                limits if limits else "Not applicable",
            "configuration":             config if config else {"status": "unchecked"},
            "mismatches_detected":       mismatches if mismatches else {},
            "has_mismatch":              len(mismatches) > 0 if mismatches else False,
            "upgrade_required":          not is_available
        }

        system_prompt = """You are the Feature Agent in a customer support AI system.
Your job is to answer the customer's query using ONLY the database data provided.
STRICT RULES:
- ONLY use the exact data given. Do NOT add information not in the data.
- Do NOT make up features, plans, prices, or capabilities.
- If feature is not available on their plan, say exactly which plans have it based on the data.
- If there is a mismatch, explain it using only the mismatch details provided.
- Give the setup guide EXACTLY as stored in the database — do not rephrase or add steps.
- Keep response to 3-4 sentences maximum.
- Be direct and specific — no generic advice."""

        user_prompt = f"""Answer the customer's question using ONLY this database data:

Customer Query: {shared_context.get('query', 'Feature inquiry')}
Feature: {feature_name}
Customer Plan: {plan_id}
Feature Display Name: {self.findings['display_name']}

SEAT SPECIFIC DATA (if feature is seats):
Current Users: {self.findings['configuration'].get('detail', '') if self.findings['configuration'] else ''}
Entitled Limit: {self.findings['plan_limit']}
Mismatch Detected: {self.findings['has_mismatch']}
Mismatch Details: {self.findings['mismatches_detected']}

GENERAL FEATURE DATA:
Feature Available on Plan: {is_available}
Plans with this feature: {', '.join(available_on) if available_on else 'None'}
Description: {self.findings['description']}
Capabilities: {', '.join(self.findings['capabilities']) if self.findings['capabilities'] else 'Not listed'}
Limitations: {', '.join(self.findings['limitations']) if self.findings['limitations'] else 'None listed'}
Setup Guide: {self.findings['setup_guide']}
Expected Behavior: {self.findings['expected_behavior']}
Common Issues: {self.findings['common_issues']}
Plan Limit: {self.findings['plan_limit']}
Configuration Status: {self.findings['configuration']}

IMPORTANT: If the question is about seats or users:
- State exactly how many users they have vs how many seats their plan allows
- State how many additional seats are needed
- Recommend upgrading their plan
- Do NOT say seats feature is unavailable — seats exist on all plans but have limits

Write a 3 sentence response using ONLY the above data"""

        self._log("LLM Call", "Generating feature response from database data...")
        self.findings["llm_summary"] = self._ask_llm(system_prompt, user_prompt)

        shared_context["feature"] = self.findings

        elapsed = self._finish()
        self.findings["time_taken"] = elapsed
        return self.findings