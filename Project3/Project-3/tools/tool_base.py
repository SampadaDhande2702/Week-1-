import time
import random
from datetime import datetime

class ToolBase:
    def __init__(self, tool_name: str):
        self.tool_name = tool_name
        self.logs = []

    def _log(self, function_name: str, inputs: dict, output: any, latency: float, success: bool, error: str = None):
        log_entry = {
            "tool": self.tool_name,
            "function": function_name,
            "inputs": inputs,
            "output": output,
            "latency_seconds": round(latency, 3),
            "success": success,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.logs.append(log_entry)
        status = "OK" if success else "FAIL"
        print(f"  [TOOL] [{status}] {self.tool_name}.{function_name} — {round(latency*1000)}ms")
        return log_entry

    def _simulate_latency(self, min_ms: int = 100, max_ms: int = 500):
        delay = random.randint(min_ms, max_ms) / 1000
        time.sleep(delay)
        return delay

    def _simulate_failure(self, failure_rate: float = 0.05):
        return random.random() < failure_rate

    def get_logs(self):
        return self.logs