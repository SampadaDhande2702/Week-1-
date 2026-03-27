import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.tool_base import ToolBase
from database import db_loader

class AccountTools(ToolBase):
    def __init__(self):
        super().__init__("AccountTools")

   #Fetches the detailed customer information
    def lookup_customer(self, customer_id: str):
        start = __import__('time').time()
        latency = self._simulate_latency(100, 400)
        try:
            if self._simulate_failure():
                raise Exception("Database timeout")
            result = db_loader.get_customer(customer_id)
            if not result:
                return self._log("lookup_customer", {"customer_id": customer_id},
                                 None, latency, False, "Customer not found"), None
            plan = db_loader.get_plan(result["plan_id"])
            result["plan_details"] = plan
            log = self._log("lookup_customer", {"customer_id": customer_id}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("lookup_customer", {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None
    #Fetches their billing information
    def get_billing_history(self, customer_id: str):
        latency = self._simulate_latency(150, 500)
        try:
            if self._simulate_failure():
                raise Exception("Billing service unavailable")
            result = db_loader.get_billing_history(customer_id)
            overdue = [p for p in result if p["status"] == "overdue"]
            summary = {
                "total_payments": len(result),
                "overdue_count": len(overdue),
                "overdue_amount": sum(p["amount"] for p in overdue),
                "payment_health": "good" if len(overdue) == 0 else "at_risk" if len(overdue) <= 1 else "critical",
                "records": result
            }
            log = self._log("get_billing_history", {"customer_id": customer_id}, summary, latency, True)
            return log, summary
        except Exception as e:
            log = self._log("get_billing_history", {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None

   #Fethes account status whether it is working or not
    def check_account_status(self, customer_id: str):
        latency = self._simulate_latency(100, 300)
        try:
            result = db_loader.get_account_status(customer_id)
            if not result:
                return self._log("check_account_status", {"customer_id": customer_id},
                                 None, latency, False, "Account not found"), None
            log = self._log("check_account_status", {"customer_id": customer_id}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("check_account_status", {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None

   #It fetches how many features are enabled for the customer and which are they
    def list_enabled_features(self, customer_id: str):
        latency = self._simulate_latency(100, 300)
        try:
            status = db_loader.get_account_status(customer_id)
            if not status:
                return self._log("list_enabled_features", {"customer_id": customer_id},
                                 None, latency, False, "Account not found"), None
            features = status.get("enabled_features", [])
            log = self._log("list_enabled_features", {"customer_id": customer_id}, features, latency, True)
            return log, features
        except Exception as e:
            log = self._log("list_enabled_features", {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None