import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.tool_base import ToolBase
from database import db_loader

class FeatureTools(ToolBase):
    def __init__(self):
        super().__init__("FeatureTools")

    def get_feature_matrix(self):
        latency = self._simulate_latency(200, 500)
        try:
            result = db_loader.get_all_features()
            matrix = {
                name: {
                    "available_on": feat["available_on"],
                    "display_name": feat["display_name"]
                }
                for name, feat in result.items()
            }
            log = self._log("get_feature_matrix", {}, matrix, latency, True)
            return log, matrix
        except Exception as e:
            log = self._log("get_feature_matrix", {}, None, latency, False, str(e))
            return log, None

    def get_feature_documentation(self, feature_name: str):
        latency = self._simulate_latency(150, 400)
        try:
            result = db_loader.get_feature(feature_name)
            if not result:
                return self._log("get_feature_documentation", {"feature_name": feature_name},
                                 None, latency, False, f"Feature '{feature_name}' not found"), None
            log = self._log("get_feature_documentation", {"feature_name": feature_name}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("get_feature_documentation", {"feature_name": feature_name}, None, latency, False, str(e))
            return log, None

    def check_feature_limits(self, feature_name: str, plan_id: str):
        latency = self._simulate_latency(100, 300)
        try:
            result = db_loader.get_feature_limits(feature_name, plan_id)
            if not result:
                return self._log("check_feature_limits",
                                 {"feature_name": feature_name, "plan_id": plan_id},
                                 None, latency, False, "Feature/plan combo not found"), None
            log = self._log("check_feature_limits",
                            {"feature_name": feature_name, "plan_id": plan_id}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("check_feature_limits",
                            {"feature_name": feature_name, "plan_id": plan_id}, None, latency, False, str(e))
            return log, None

    def validate_configuration(self, feature_name: str, customer_id: str):
        latency = self._simulate_latency(200, 500)
        try:
            usage = db_loader.get_feature_usage(customer_id, feature_name)
            if not usage:
                result = {"configured": False, "status": "unchecked", "detail": "No usage data found"}
            else:
                result = {
                    "configured": usage.get("is_configured", False),
                    "status": usage.get("configuration_status", "unchecked"),
                    "mismatch": usage.get("mismatch_flag", False),
                    "detail": usage.get("mismatch_detail", "Configuration looks correct")
                }
            log = self._log("validate_configuration",
                            {"feature_name": feature_name, "customer_id": customer_id}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("validate_configuration",
                            {"feature_name": feature_name, "customer_id": customer_id}, None, latency, False, str(e))
            return log, None

    def detect_mismatch(self, customer_id: str):
        latency = self._simulate_latency(200, 400)
        try:
            mismatches = db_loader.get_all_mismatches(customer_id)
            log = self._log("detect_mismatch", {"customer_id": customer_id}, mismatches, latency, True)
            return log, mismatches
        except Exception as e:
            log = self._log("detect_mismatch", {"customer_id": customer_id}, None, latency, False, str(e))
            return log, None