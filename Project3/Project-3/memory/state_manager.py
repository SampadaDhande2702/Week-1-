from datetime import datetime

class StateManager:
    def __init__(self):
        self.state = {
            "current_customer_id": None,
            "current_query": None,
            "agents_invoked": [],
            "decisions": [],
            "escalated": False,
            "resolved": False,
            "session_start": datetime.now().isoformat()
        }

    def set_customer(self, customer_id: str):
        self.state["current_customer_id"] = customer_id

    def set_query(self, query: str):
        self.state["current_query"] = query

    def add_agent(self, agent_name: str):
        self.state["agents_invoked"].append({
            "agent": agent_name,
            "invoked_at": datetime.now().isoformat()
        })

    def add_decision(self, decision: str, reason: str):
        self.state["decisions"].append({
            "decision": decision,
            "reason": reason,
            "timestamp": datetime.now().isoformat()
        })

    def set_escalated(self, value: bool):
        self.state["escalated"] = value

    def set_resolved(self, value: bool):
        self.state["resolved"] = value

    def get_state(self):
        return self.state

    def reset(self):
        self.__init__()