import json
import os

BASE = os.path.dirname(__file__)

def _load(folder, filename):
    path = os.path.join(BASE, folder, filename)
    with open(path, "r") as f:
        return json.load(f)

def _save(folder, filename, data):
    path = os.path.join(BASE, folder, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# ─── ACCOUNT AGENT ───────────────────────────────────────────

def get_customer(customer_id: str):
    data = _load("customers", "customers.json")
    return data.get(customer_id, None)

def get_all_customers():
    return _load("customers", "customers.json")

def get_plan(plan_id: str):
    customers = _load("customers", "customers.json")
    for c in customers.values():
        if c["plan_id"] == plan_id:
            pass
    plans = {
        "plan_starter": {"plan_id": "plan_starter", "plan_name": "Starter", "monthly_price": 29.99, "max_seats": 10, "api_call_limit": 0, "support_tier": "community"},
        "plan_pro":     {"plan_id": "plan_pro",     "plan_name": "Pro",     "monthly_price": 99.99, "max_seats": 25, "api_call_limit": 1000, "support_tier": "priority"},
        "plan_enterprise": {"plan_id": "plan_enterprise", "plan_name": "Enterprise", "monthly_price": 299.99, "max_seats": -1, "api_call_limit": -1, "support_tier": "dedicated"}
    }
    return plans.get(plan_id, None)

def get_billing_history(customer_id: str):
    data = _load("customers", "billing.json")
    return data.get(customer_id, [])

def get_account_status(customer_id: str):
    data = _load("customers", "account_status.json")
    return data.get(customer_id, None)

# ─── FEATURE AGENT ───────────────────────────────────────────

def get_feature(feature_name: str):
    data = _load("features", "features.json")
    return data.get(feature_name, None)

def get_all_features():
    return _load("features", "features.json")

def get_feature_limits(feature_name: str, plan_id: str = None):
    data = _load("features", "feature_limits.json")
    feature_data = data.get(feature_name, None)
    if feature_data and plan_id:
        return feature_data.get(plan_id, None)
    return feature_data

def get_feature_usage(customer_id: str, feature_name: str = None):
    data = _load("features", "feature_usage.json")
    customer_usage = data.get(customer_id, {})
    if feature_name:
        return customer_usage.get(feature_name, None)
    return customer_usage

def get_all_mismatches(customer_id: str):
    usage = get_feature_usage(customer_id)
    return {
        feature: info
        for feature, info in usage.items()
        if info.get("mismatch_flag") == True
    }

# ─── CONTRACT AGENT ──────────────────────────────────────────

def get_contract(contract_id: str):
    data = _load("contracts", "contracts.json")
    return data.get(contract_id, None)

def get_contract_by_customer(customer_id: str):
    data = _load("contracts", "contracts.json")
    for contract in data.values():
        if contract["customer_id"] == customer_id:
            return contract
    return None

def get_sla_terms(plan_id: str):
    data = _load("contracts", "sla_terms.json")
    return data.get(plan_id, None)

def get_entitlements(contract_id: str):
    data = _load("contracts", "entitlements.json")
    return data.get(contract_id, None)

def get_violations(customer_id: str = None):
    data = _load("contracts", "violations.json")
    if customer_id:
        return {
            vid: v for vid, v in data.items()
            if v["customer_id"] == customer_id
        }
    return data

def save_violation(violation_id: str, violation_data: dict):
    data = _load("contracts", "violations.json")
    data[violation_id] = violation_data
    _save("contracts", "violations.json", data)

# ─── ESCALATION AGENT ────────────────────────────────────────

def get_routing_rules():
    return _load("escalations", "routing_rules.json")

def get_routing_rule(rule_id: str):
    data = _load("escalations", "routing_rules.json")
    return data.get(rule_id, None)

def get_all_tickets():
    return _load("escalations", "escalation_tickets.json")

def get_tickets_by_customer(customer_id: str):
    data = _load("escalations", "escalation_tickets.json")
    return {
        tid: t for tid, t in data.items()
        if t["customer_id"] == customer_id
    }

def save_ticket(ticket_id: str, ticket_data: dict):
    data = _load("escalations", "escalation_tickets.json")
    data[ticket_id] = ticket_data
    _save("escalations", "escalation_tickets.json", data)

def save_escalation_log(log_entry: dict):
    data = _load("escalations", "escalation_log.json")
    data.append(log_entry)
    _save("escalations", "escalation_log.json", data)

def get_escalation_log():
    return _load("escalations", "escalation_log.json")