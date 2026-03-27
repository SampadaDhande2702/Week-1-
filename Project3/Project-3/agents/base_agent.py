from datetime import datetime
from llm.llm_factory import get_llm

class BaseAgent:
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.findings = {}
        self.logs = []
        self.start_time = None
        self.end_time = None
        self.total_tokens = 0
        self.llm, self.provider = get_llm()

    def _start(self):
        self.start_time = datetime.now()
        print(f"\n  [{self.name}] Starting...")

    def _finish(self):
        self.end_time = datetime.now()
        elapsed = round((self.end_time - self.start_time).total_seconds(), 2)
        print(f"  [{self.name}] Done in {elapsed}s")
        return elapsed

    def _log(self, action: str, detail: str):
        entry = {
            "agent": self.name,
            "action": action,
            "detail": detail,
            "timestamp": datetime.now().isoformat()
        }
        self.logs.append(entry)
        print(f"  [{self.name}] {action}: {detail}")

    def _ask_llm(self, system_prompt: str, user_prompt: str) -> str:
        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm.invoke(messages)
            content = response.content if hasattr(response, "content") else str(response)
            in_tokens  = len(system_prompt.split()) + len(user_prompt.split())
            out_tokens = len(content.split())
            self.total_tokens += in_tokens + out_tokens
            self._log("LLM Response", f"{out_tokens} tokens generated")
            return content
        except Exception as e:
            self._log("LLM Error", str(e))
            return f"LLM call failed: {str(e)}"

    def get_findings(self):
        return self.findings

    def get_logs(self):
        return self.logs

    def get_summary(self):
        return {
            "agent": self.name,
            "role": self.role,
            "findings": self.findings,
            "logs": self.logs,
            "total_tokens": self.total_tokens
        }