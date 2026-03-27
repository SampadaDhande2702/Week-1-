import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from agents.account_agent import AccountAgent
from agents.feature_agent import FeatureAgent
from agents.contract_agent import ContractAgent
from agents.escalation_agent import EscalationAgent
from datetime import datetime
from monitoring.tracing_utils import Tracer
from memory.shared_context import SharedContext

class OrchestratorAgent:
    def __init__(self):
        self.name           = "Orchestrator"
        self.shared_context = {}
        self.all_findings   = {}
        self.start_time     = None
        self.total_tokens   = 0
        from llm.llm_factory import get_llm
        self.llm, self.provider = get_llm()

    def _log(self, action: str, detail: str):
        print(f"\n  [Orchestrator] {action}: {detail}")

    def _analyze_query(self, query: str):
        system_prompt = """You are the Orchestrator of a customer support system.
You have 4 specialized agents available:

1. account_agent — for questions about:
   plan, billing, payments, price, seats, users,
   account status, suspension, features enabled, last login,
   how much they pay, monthly cost, subscription

2. feature_agent — for questions about:
   dark mode, api, sso, webhooks, analytics,
   how to enable something, feature setup, feature limits,
   feature availability, what features do I have

3. contract_agent — for questions about:
   contract, SLA, waiting time, support response time,
   entitlements, violations, legal agreement

4. escalation_agent — for questions about:
   urgent issues, escalate, critical, complaint,
   need human help, SLA violated

RULES:
- Always include account_agent
- Include feature_agent if question is about any feature or how-to
- Include contract_agent if question mentions SLA or contract or waiting
- Include escalation_agent if question is urgent or needs human

Also identify the specific feature name if mentioned.
Map to exactly one of: dark_mode, api_access, sso, webhooks, advanced_analytics, seats
If no specific feature mentioned write FEATURE: none

Respond in this EXACT format only:
AGENTS: account_agent,feature_agent
FEATURE: dark_mode"""

        user_prompt = f"Customer query: {query}"

        try:
            from langchain_core.messages import SystemMessage, HumanMessage
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = self.llm.invoke(messages)
            content  = response.content.strip()
            self._log("LLM Routing", f"Decision: {content}")

            needs = {
                "account":    True,
                "feature":    False,
                "contract":   False,
                "escalation": False
            }
            feature_name = None

            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("AGENTS:"):
                    agents_str = line.replace("AGENTS:", "").strip()
                    if "feature_agent"    in agents_str: needs["feature"]    = True
                    if "contract_agent"   in agents_str: needs["contract"]   = True
                    if "escalation_agent" in agents_str: needs["escalation"] = True

                if line.startswith("FEATURE:"):
                    fname = line.replace("FEATURE:", "").strip()
                    if fname and fname.lower() != "none":
                        feature_name = fname

            return needs, feature_name

        except Exception as e:
            self._log("LLM Routing Error", f"{e} — using keyword fallback")
            return self._keyword_fallback(query)

    def _keyword_fallback(self, query: str):
        query_lower = query.lower()
        needs = {
            "account":    True,
            "feature":    any(w in query_lower for w in ["feature", "dark mode", "api", "sso", "webhook", "analytics", "enable", "setup"]),
            "contract":   any(w in query_lower for w in ["contract", "sla", "agreement", "days", "waiting"]),
            "escalation": any(w in query_lower for w in ["escalate", "urgent", "critical", "violated"])
        }
        feature_map = {
            "dark mode": "dark_mode",
            "api":       "api_access",
            "sso":       "sso",
            "webhook":   "webhooks",
            "analytics": "advanced_analytics",
            "seats":     "seats"
        }
        feature_name = None
        for keyword, fname in feature_map.items():
            if keyword in query_lower:
                feature_name = fname
                break
        return needs, feature_name

    def run(self, query: str, customer_id: str, issue_raised_at: str = None):
        self.start_time     = datetime.now()
        self.shared_context_obj = SharedContext()
        self.shared_context_obj.set("query", query)
        self.shared_context_obj.set("customer_id", customer_id)
        self.shared_context = self.shared_context_obj.all()

        self.tracer = Tracer()
        self.tracer.start_trace(query, customer_id)

        print(f"\n{'='*60}")
        print(f"  ORCHESTRATOR — New Query Received")
        print(f"  Customer: {customer_id}")
        print(f"  Query: {query[:80]}...")
        print(f"{'='*60}")

        self._log("Analyzing", "Detecting which agents are needed...")
        needs, feature_name = self._analyze_query(query)
        self._log("Plan", f"Agents needed: {[k for k,v in needs.items() if v]}")

        agents_used  = []
        total_tokens = 150

        # ── STEP 1 — Always run Account Agent first ───────────────
        self._log("Routing", "Running Account Agent first (always)")
        account_agent    = AccountAgent()
        account_findings = account_agent.run(customer_id, self.shared_context)
        self.all_findings["account"] = account_findings
        agents_used.append("Account Agent")
        total_tokens += account_agent.total_tokens
        self.shared_context_obj.set("account", account_findings)
        self.shared_context_obj.set("plan_id", account_findings.get("plan_id", ""))
        self.shared_context = self.shared_context_obj.all()

        self.tracer.trace_agent(
            agent_name  = "Account Agent",
            input_data  = {"customer_id": customer_id},
            output_data = account_findings,
            tokens      = account_agent.total_tokens,
            time_taken  = account_findings.get("time_taken", 0)
        )

        # ── STEP 2 — Check account status immediately ─────────────
        account_status = account_findings.get("account_status", "unknown")
        self._log("Status Check", f"Account status is: {account_status}")

        # ── STEP 3 — If account is suspended stop everything ──────
        if account_status == "suspended":
            self._log("Guard", "Account is SUSPENDED — skipping all other agents")
            self._log("Routing", "Going directly to Escalation Agent")

            escalation_agent    = EscalationAgent()
            escalation_findings = escalation_agent.run(customer_id, self.shared_context)
            self.all_findings["escalation"] = escalation_findings
            agents_used.append("Escalation Agent")
            total_tokens += escalation_agent.total_tokens

            elapsed           = round((datetime.now() - self.start_time).total_seconds(), 2)
            self.total_tokens = total_tokens

            self.tracer.end_trace(
                output_data  = self.all_findings,
                total_tokens = total_tokens,
                total_time   = elapsed
            )
            trace_url = self.tracer.get_trace_url()

            print(f"\n{'='*60}")
            print(f"  ORCHESTRATOR — Suspended Account Detected")
            print(f"  Agents used : {', '.join(agents_used)}")
            print(f"  Total time  : {elapsed}s")
            print(f"  Total tokens: {total_tokens}")
            print(f"{'='*60}\n")

            return {
                "query":          query,
                "customer_id":    customer_id,
                "agents_used":    agents_used,
                "findings":       self.all_findings,
                "shared_context": self.shared_context,
                "total_tokens":   total_tokens,
                "total_time":     elapsed,
                "trace_url":      trace_url,
                "timestamp":      datetime.now().isoformat()
            }

        # ── STEP 4 — If account is inactive stop everything ───────
        if account_status == "inactive":
            self._log("Guard", "Account is INACTIVE — cannot process any requests")

            elapsed           = round((datetime.now() - self.start_time).total_seconds(), 2)
            self.total_tokens = total_tokens

            self.all_findings["error"] = {
                "type":    "inactive_account",
                "message": "Account is inactive and cannot process requests"
            }

            self.tracer.end_trace(
                output_data  = self.all_findings,
                total_tokens = total_tokens,
                total_time   = elapsed
            )
            trace_url = self.tracer.get_trace_url()

            return {
                "query":          query,
                "customer_id":    customer_id,
                "agents_used":    agents_used,
                "findings":       self.all_findings,
                "shared_context": self.shared_context,
                "total_tokens":   total_tokens,
                "total_time":     elapsed,
                "trace_url":      trace_url,
                "timestamp":      datetime.now().isoformat()
            }

        # ── STEP 5 — Account is active so continue normally ───────
        self._log("Guard", "Account is ACTIVE — proceeding with full investigation")

        # ── STEP 6 — Run Feature Agent only if account is active ──
        if needs["feature"] and feature_name:
            self._log("Routing", f"Running Feature Agent for '{feature_name}'")
            feature_agent    = FeatureAgent()
            feature_findings = feature_agent.run(customer_id, feature_name, self.shared_context)
            self.all_findings["feature"] = feature_findings
            agents_used.append("Feature Agent")
            total_tokens += feature_agent.total_tokens
            self.shared_context_obj.set("feature", feature_findings)
            self.shared_context = self.shared_context_obj.all()

            self.tracer.trace_agent(
                agent_name  = "Feature Agent",
                input_data  = {"customer_id": customer_id, "feature_name": feature_name},
                output_data = feature_findings,
                tokens      = feature_agent.total_tokens,
                time_taken  = feature_findings.get("time_taken", 0)
            )

        elif needs["feature"] and not feature_name:
            self._log("Warning", "Feature keyword detected but no specific feature identified")

        # ── STEP 7 — Run Contract Agent if needed ─────────────────
        if needs["contract"] or needs["escalation"]:
            issue_time    = issue_raised_at or datetime.now().isoformat()
            self._log("Routing", "Running Contract Agent for SLA validation")
            contract_agent    = ContractAgent()
            contract_findings = contract_agent.run(customer_id, issue_time, self.shared_context)
            self.all_findings["contract"] = contract_findings
            agents_used.append("Contract Agent")
            total_tokens += contract_agent.total_tokens
            
            self.shared_context_obj.set("contract", contract_findings)
            self.shared_context = self.shared_context_obj.all()


            self.tracer.trace_agent(
                agent_name  = "Contract Agent",
                input_data  = {"customer_id": customer_id, "issue_raised_at": issue_time},
                output_data = contract_findings,
                tokens      = contract_agent.total_tokens,
                time_taken  = contract_findings.get("time_taken", 0)
            )

        # ── STEP 8 — Run Escalation Agent if needed ───────────────
        if needs["escalation"] or self.shared_context.get("contract", {}).get("sla_violated"):
            self._log("Routing", "Running Escalation Agent")
            escalation_agent    = EscalationAgent()
            escalation_findings = escalation_agent.run(customer_id, self.shared_context)
            self.all_findings["escalation"] = escalation_findings
            agents_used.append("Escalation Agent")
            total_tokens += escalation_agent.total_tokens

            self.tracer.trace_agent(
                agent_name  = "Escalation Agent",
                input_data  = {"customer_id": customer_id},
                output_data = escalation_findings,
                tokens      = escalation_agent.total_tokens,
                time_taken  = escalation_findings.get("time_taken", 0)
            )

        # ── STEP 9 — Run Escalation if feature mismatch ───────────
        elif self.shared_context.get("feature", {}).get("has_mismatch"):
            feature_findings  = self.shared_context.get("feature", {})
            mismatch_features = list(feature_findings.get("mismatches_detected", {}).keys())
            if feature_name in mismatch_features:
                self._log("Routing", "Mismatch on requested feature — Running Escalation Agent")
                escalation_agent    = EscalationAgent()
                escalation_findings = escalation_agent.run(customer_id, self.shared_context)
                self.all_findings["escalation"] = escalation_findings
                agents_used.append("Escalation Agent")
                total_tokens += escalation_agent.total_tokens
                self.shared_context_obj.set("escalation", escalation_findings)
                self.shared_context = self.shared_context_obj.all()


                self.tracer.trace_agent(
                    agent_name  = "Escalation Agent",
                    input_data  = {"customer_id": customer_id},
                    output_data = escalation_findings,
                    tokens      = escalation_agent.total_tokens,
                    time_taken  = escalation_findings.get("time_taken", 0)
                )

        # ── STEP 10 — Combine everything ──────────────────────────
        elapsed           = round((datetime.now() - self.start_time).total_seconds(), 2)
        self.total_tokens = total_tokens

        self.tracer.end_trace(
            output_data  = self.all_findings,
            total_tokens = total_tokens,
            total_time   = elapsed
        )
        trace_url = self.tracer.get_trace_url()

        print(f"\n{'='*60}")
        print(f"  ORCHESTRATOR — Investigation Complete")
        print(f"  Agents used : {', '.join(agents_used)}")
        print(f"  Total time  : {elapsed}s")
        print(f"  Total tokens: {total_tokens}")
        print(f"{'='*60}\n")

        return {
            "query":          query,
            "customer_id":    customer_id,
            "agents_used":    agents_used,
            "findings":       self.all_findings,
            "shared_context": self.shared_context,
            "total_tokens":   total_tokens,
            "total_time":     elapsed,
            "trace_url":      trace_url,
            "timestamp":      datetime.now().isoformat()
        }