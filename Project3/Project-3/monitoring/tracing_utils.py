from datetime import datetime
from monitoring.langfuse_config import get_langfuse, create_trace, flush

class Tracer:
    def __init__(self):
        self.traces   = []
        self.trace    = None
        self.trace_id = None
        self.trace_url= None
        self.spans    = {}

    def start_trace(self, query: str, customer_id: str):
        try:
            self.trace = create_trace(
                name      = "customer-support-investigation",
                user_id   = customer_id,
                input_data= {"query": query, "customer_id": customer_id}
            )
            self.trace_id  = self.trace.id
            self.trace_url = f"https://cloud.langfuse.com/trace/{self.trace_id}"
            print(f"  [Langfuse] Trace started: {self.trace_url}")
        except Exception as e:
            print(f"  [Langfuse] Error starting trace: {e}")

    def trace_agent(self, agent_name: str, input_data: dict,
                    output_data: dict, tokens: int, time_taken: float):
        entry = {
            "type":       "agent",
            "agent":      agent_name,
            "input":      input_data,
            "output":     output_data,
            "tokens":     tokens,
            "time_taken": time_taken,
            "timestamp":  datetime.now().isoformat()
        }
        self.traces.append(entry)

        if self.trace:
            try:
                span = self.trace.span(
                    name    = agent_name,
                    input   = input_data,
                    output  = output_data,
                    metadata= {
                        "tokens":     tokens,
                        "time_taken": time_taken,
                        "type":       "agent"
                    }
                )
                self.spans[agent_name] = span
            except Exception as e:
                print(f"  [Langfuse] Error tracing agent: {e}")

        return entry

    def trace_tool(self, tool_name: str, function: str,
                   inputs: dict, output: dict,
                   latency: float, success: bool):
        entry = {
            "type":     "tool",
            "tool":     tool_name,
            "function": function,
            "inputs":   inputs,
            "output":   output,
            "latency":  latency,
            "success":  success,
            "timestamp":datetime.now().isoformat()
        }
        self.traces.append(entry)

        if self.trace:
            try:
                self.trace.span(
                    name    = f"{tool_name}.{function}",
                    input   = inputs,
                    output  = output,
                    metadata= {
                        "latency": latency,
                        "success": success,
                        "type":    "tool"
                    }
                )
            except Exception as e:
                print(f"  [Langfuse] Error tracing tool: {e}")

        return entry

    def trace_decision(self, decision: str, reason: str, agent: str):
        entry = {
            "type":      "decision",
            "decision":  decision,
            "reason":    reason,
            "agent":     agent,
            "timestamp": datetime.now().isoformat()
        }
        self.traces.append(entry)

        if self.trace:
            try:
                self.trace.event(
                    name    = f"decision_{agent}",
                    input   = {"decision": decision},
                    output  = {"reason": reason},
                    metadata= {"agent": agent, "type": "decision"}
                )
            except Exception as e:
                print(f"  [Langfuse] Error tracing decision: {e}")

        return entry

    def end_trace(self, output_data: dict, total_tokens: int, total_time: float):
        if self.trace:
            try:
                self.trace.update(
                    output  = output_data,
                    metadata= {
                        "total_tokens": total_tokens,
                        "total_time":   total_time
                    }
                )
                flush()
                print(f"  [Langfuse] Trace completed: {self.trace_url}")
            except Exception as e:
                print(f"  [Langfuse] Error ending trace: {e}")

    def get_trace_url(self):
        return self.trace_url

    def get_all_traces(self):
        return self.traces

    def get_summary(self):
        agents    = [t for t in self.traces if t["type"] == "agent"]
        tools     = [t for t in self.traces if t["type"] == "tool"]
        decisions = [t for t in self.traces if t["type"] == "decision"]
        return {
            "total_traces":    len(self.traces),
            "agents_traced":   len(agents),
            "tools_traced":    len(tools),
            "decisions_traced":len(decisions),
            "trace_url":       self.trace_url,
            "traces":          self.traces
        }