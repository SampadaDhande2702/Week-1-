import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.tool_base import ToolBase
from database import db_loader
from datetime import datetime

class ContractTools(ToolBase):
    def __init__(self):
        super().__init__("ContractTools")

    def lookup_contract(self, customer_id: str):
        latency = self._simulate_latency(150, 400)
        try:
            result = db_loader.get_contract_by_customer(customer_id)
            if not result:
                return self._log("lookup_contract", {"customer_id": customer_id},
                                 None, latency, False, "No contract found for customer"), None
            log = self._log("lookup_contract", {"customer_id": customer_id}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("lookup_contract", {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None

    def get_contract_terms(self, contract_id: str):
        latency = self._simulate_latency(150, 400)
        try:
            result = db_loader.get_contract(contract_id)
            if not result:
                return self._log("get_contract_terms", {"contract_id": contract_id},
                                 None, latency, False, "Contract not found"), None
            log = self._log("get_contract_terms", {"contract_id": contract_id}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("get_contract_terms", {"contract_id": contract_id}, None, latency, False, str(e))
            return log, None

    def validate_sla_compliance(self, customer_id: str, issue_raised_at: str):
        latency = self._simulate_latency(200, 600)
        try:
            contract = db_loader.get_contract_by_customer(customer_id)
            if not contract:
                return self._log("validate_sla_compliance",
                                 {"customer_id": customer_id}, None, latency, False,
                                 "No contract found"), None
            issue_time = datetime.fromisoformat(issue_raised_at)
            now = datetime.now()
            hours_elapsed = (now - issue_time).total_seconds() / 3600
            sla_hours = contract["sla_first_response_hours"]
            violated = hours_elapsed > sla_hours
            breach_hours = round(hours_elapsed - sla_hours, 1) if violated else 0
            result = {
                "contract_id": contract["contract_id"],
                "sla_first_response_hours": sla_hours,
                "hours_elapsed": round(hours_elapsed, 1),
                "sla_violated": violated,
                "breach_hours": breach_hours,
                "severity": "critical" if breach_hours > 48 else "high" if breach_hours > 24 else "medium"
            }
            log = self._log("validate_sla_compliance",
                            {"customer_id": customer_id, "issue_raised_at": issue_raised_at},
                            result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("validate_sla_compliance",
                            {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None

    def get_included_features(self, contract_id: str):
        latency = self._simulate_latency(100, 300)
        try:
            entitlements = db_loader.get_entitlements(contract_id)
            if not entitlements:
                return self._log("get_included_features", {"contract_id": contract_id},
                                 None, latency, False, "Entitlements not found"), None
            log = self._log("get_included_features", {"contract_id": contract_id},
                            entitlements, latency, True)
            return log, entitlements
        except Exception as e:
            log = self._log("get_included_features", {"contract_id": contract_id},
                            None, latency, False, str(e))
            return log, None

    def write_violation(self, customer_id: str, contract_id: str, details: dict):
        latency = self._simulate_latency(100, 300)
        try:
            import uuid
            violation_id = f"VIOL_{uuid.uuid4().hex[:6].upper()}"
            violation = {
                "violation_id": violation_id,
                "customer_id": customer_id,
                "contract_id": contract_id,
                "created_at": datetime.now().isoformat(),
                **details
            }
            db_loader.save_violation(violation_id, violation)
            log = self._log("write_violation", {"customer_id": customer_id}, violation, latency, True)
            return log, violation
        except Exception as e:
            log = self._log("write_violation", {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None