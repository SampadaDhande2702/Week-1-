from datetime import datetime

class Metrics:
    def __init__(self):
        self.data = {
            "total_queries": 0,
            "total_tokens": 0,
            "total_time": 0.0,
            "escalations": 0,
            "agents_invoked": 0,
            "tool_calls": 0,
            "tool_failures": 0,
            "sessions": []
        }

    def record_session(self, query: str, agents_used: list,
                       tokens: int, time_taken: float, escalated: bool):
        self.data["total_queries"] += 1
        self.data["total_tokens"] += tokens
        self.data["total_time"] += time_taken
        self.data["agents_invoked"] += len(agents_used)
        if escalated:
            self.data["escalations"] += 1
        session = {
            "query": query[:60],
            "agents_used": agents_used,
            "tokens": tokens,
            "time_taken": time_taken,
            "escalated": escalated,
            "timestamp": datetime.now().isoformat()
        }
        self.data["sessions"].append(session)
        return session

    def get_metrics(self):
        return self.data

    def get_averages(self):
        total = self.data["total_queries"]
        if total == 0:
            return {"avg_tokens": 0, "avg_time": 0}
        return {
            "avg_tokens": round(self.data["total_tokens"] / total),
            "avg_time": round(self.data["total_time"] / total, 2)
        }