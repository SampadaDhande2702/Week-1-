import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from tools.tool_base import ToolBase
from database import db_loader
from datetime import datetime
import uuid

class EscalationTools(ToolBase):
    def __init__(self):
        super().__init__("EscalationTools")

    def create_escalation_ticket(self, customer_id: str, reason: str,
                                  priority: str, severity: str,
                                  assigned_team: str, notes: str,
                                  contract_id: str = None, sla_id: str = None):
        latency = self._simulate_latency(200, 500)
        try:
            ticket_id = f"TICKET_{uuid.uuid4().hex[:6].upper()}"
            ticket = {
                "ticket_id": ticket_id,
                "customer_id": customer_id,
                "contract_id": contract_id,
                "sla_id": sla_id,
                "reason": reason,
                "severity": severity,
                "priority": priority,
                "status": "open",
                "assigned_team": assigned_team,
                "escalation_notes": notes,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "resolved_at": None
            }
            db_loader.save_ticket(ticket_id, ticket)
            log = self._log("create_escalation_ticket", {"customer_id": customer_id,
                            "priority": priority}, ticket, latency, True)
            return log, ticket
        except Exception as e:
            log = self._log("create_escalation_ticket", {"customer_id": customer_id},
                            None, latency, False, str(e))
            return log, None

    def get_escalation_routing(self, issue_type: str):
        latency = self._simulate_latency(100, 200)
        try:
            rules = db_loader.get_routing_rules()
            matched = [r for r in rules.values() if issue_type.lower() in r["rule_name"].lower()]
            result = matched[0] if matched else list(rules.values())[0]
            log = self._log("get_escalation_routing", {"issue_type": issue_type}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("get_escalation_routing", {"issue_type": issue_type}, None, latency, False, str(e))
            return log, None

    def notify_support_team(self, ticket_id: str, team: str):
        latency = self._simulate_latency(100, 300)
        try:
            result = {
                "ticket_id": ticket_id,
                "team_notified": team,
                "notification_sent_at": datetime.now().isoformat(),
                "channel": "email + slack",
                "status": "delivered"
            }
            log = self._log("notify_support_team", {"ticket_id": ticket_id, "team": team},
                            result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("notify_support_team", {"ticket_id": ticket_id},
                            None, latency, False, str(e))
            return log, None

    def log_escalation_reason(self, ticket_id: str, reason: str, decision_trail: list):
        latency = self._simulate_latency(100, 200)
        try:
            log_entry = {
                "ticket_id": ticket_id,
                "reason": reason,
                "decision_trail": decision_trail,
                "logged_at": datetime.now().isoformat()
            }
            db_loader.save_escalation_log(log_entry)
            log = self._log("log_escalation_reason", {"ticket_id": ticket_id},
                            log_entry, latency, True)
            return log, log_entry
        except Exception as e:
            log = self._log("log_escalation_reason", {"ticket_id": ticket_id},
                            None, latency, False, str(e))
            return log, None

    def check_existing_tickets(self, customer_id: str):
        latency = self._simulate_latency(100, 300)
        try:
            tickets = db_loader.get_tickets_by_customer(customer_id)
            open_tickets = {tid: t for tid, t in tickets.items() if t["status"] == "open"}
            result = {
                "total_tickets": len(tickets),
                "open_tickets": len(open_tickets),
                "tickets": tickets
            }
            log = self._log("check_existing_tickets", {"customer_id": customer_id}, result, latency, True)
            return log, result
        except Exception as e:
            log = self._log("check_existing_tickets", {"customer_id": customer_id},
                            None, latency, False, str(e))
            return log, None