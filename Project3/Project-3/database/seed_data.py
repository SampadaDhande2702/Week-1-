import json
import os

BASE = os.path.dirname(__file__)

def write(folder, filename, data):
    path = os.path.join(BASE, folder, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Created {folder}/{filename}")

def seed_customers():
    customers = {
        "CUST_001": {
            "customer_id": "CUST_001",
            "full_name": "Alice Johnson",
            "email": "alice@acmecorp.com",
            "phone": "+1-415-555-0101",
            "company_name": "Acme Corp",
            "plan_id": "plan_pro",
            "account_status": "active",
            "suspension_reason": None,
            "seats_used": 8,
            "created_at": "2023-06-15",
            "updated_at": "2024-01-10"
        },
        "CUST_002": {
            "customer_id": "CUST_002",
            "full_name": "Bob Smith",
            "email": "bob@startupxyz.com",
            "phone": "+1-415-555-0102",
            "company_name": "Startup XYZ",
            "plan_id": "plan_starter",
            "account_status": "active",
            "suspension_reason": None,
            "seats_used": 2,
            "created_at": "2024-01-01",
            "updated_at": "2024-03-01"
        },
        "CUST_003": {
            "customer_id": "CUST_003",
            "full_name": "Carol Davis",
            "email": "carol@enterpriseco.com",
            "phone": "+1-415-555-0103",
            "company_name": "Enterprise Co",
            "plan_id": "plan_enterprise",
            "account_status": "active",
            "suspension_reason": None,
            "seats_used": 12,
            "created_at": "2022-11-20",
            "updated_at": "2024-02-15"
        },
        "CUST_004": {
            "customer_id": "CUST_004",
            "full_name": "David Lee",
            "email": "david@techventures.com",
            "phone": "+1-415-555-0104",
            "company_name": "Tech Ventures",
            "plan_id": "plan_pro",
            "account_status": "suspended",
            "suspension_reason": "Overdue payment for 3 consecutive months",
            "seats_used": 5,
            "created_at": "2023-03-10",
            "updated_at": "2024-03-20"
        },
        "CUST_005": {
            "customer_id": "CUST_005",
            "full_name": "Eva Martinez",
            "email": "eva@growthco.com",
            "phone": "+1-415-555-0105",
            "company_name": "Growth Co",
            "plan_id": "plan_starter",
            "account_status": "active",
            "suspension_reason": None,
            "seats_used": 10,
            "created_at": "2024-02-01",
            "updated_at": "2024-03-01"
        }
    }
    write("customers", "customers.json", customers)

def seed_plans():
    plans = {
        "plan_starter": {
            "plan_id": "plan_starter",
            "plan_name": "Starter",
            "monthly_price": 29.99,
            "billing_cycle": "monthly",
            "max_seats": 10,
            "api_call_limit": 0,
            "storage_gb": 10,
            "support_tier": "community",
            "features_included": ["dark_mode", "basic_dashboard", "email_reports"]
        },
        "plan_pro": {
            "plan_id": "plan_pro",
            "plan_name": "Pro",
            "monthly_price": 99.99,
            "billing_cycle": "monthly",
            "max_seats": 25,
            "api_call_limit": 1000,
            "storage_gb": 100,
            "support_tier": "priority",
            "features_included": ["dark_mode", "basic_dashboard", "email_reports",
                                   "api_access", "advanced_analytics", "sso", "webhooks"]
        },
        "plan_enterprise": {
            "plan_id": "plan_enterprise",
            "plan_name": "Enterprise",
            "monthly_price": 299.99,
            "billing_cycle": "monthly",
            "max_seats": -1,
            "api_call_limit": -1,
            "storage_gb": -1,
            "support_tier": "dedicated",
            "features_included": ["dark_mode", "basic_dashboard", "email_reports",
                                   "api_access", "advanced_analytics", "sso", "webhooks",
                                   "custom_integrations", "audit_logs", "priority_support"]
        }
    }
    write("customers", "billing.json", seed_billing())
    write("customers", "account_status.json", seed_account_status())
    return plans

def seed_billing():
    return {
        "CUST_001": [
            {"payment_id": "PAY_001", "invoice_id": "INV_2024_001", "amount": 99.99,
             "due_date": "2024-01-01", "payment_date": "2023-12-28", "status": "paid",
             "payment_method": "card", "failure_reason": None},
            {"payment_id": "PAY_002", "invoice_id": "INV_2024_002", "amount": 99.99,
             "due_date": "2024-02-01", "payment_date": "2024-01-30", "status": "paid",
             "payment_method": "card", "failure_reason": None},
            {"payment_id": "PAY_003", "invoice_id": "INV_2024_003", "amount": 99.99,
             "due_date": "2024-03-01", "payment_date": "2024-02-28", "status": "paid",
             "payment_method": "card", "failure_reason": None}
        ],
        "CUST_002": [
            {"payment_id": "PAY_004", "invoice_id": "INV_2024_004", "amount": 29.99,
             "due_date": "2024-01-01", "payment_date": "2024-01-01", "status": "paid",
             "payment_method": "paypal", "failure_reason": None},
            {"payment_id": "PAY_005", "invoice_id": "INV_2024_005", "amount": 29.99,
             "due_date": "2024-02-01", "payment_date": "2024-02-01", "status": "paid",
             "payment_method": "paypal", "failure_reason": None}
        ],
        "CUST_003": [
            {"payment_id": "PAY_006", "invoice_id": "INV_2024_006", "amount": 299.99,
             "due_date": "2024-01-01", "payment_date": "2023-12-30", "status": "paid",
             "payment_method": "bank_transfer", "failure_reason": None},
            {"payment_id": "PAY_007", "invoice_id": "INV_2024_007", "amount": 299.99,
             "due_date": "2024-02-01", "payment_date": "2024-01-31", "status": "paid",
             "payment_method": "bank_transfer", "failure_reason": None}
        ],
        "CUST_004": [
            {"payment_id": "PAY_008", "invoice_id": "INV_2024_008", "amount": 99.99,
             "due_date": "2024-01-01", "payment_date": None, "status": "overdue",
             "payment_method": "card", "failure_reason": "Card declined"},
            {"payment_id": "PAY_009", "invoice_id": "INV_2024_009", "amount": 99.99,
             "due_date": "2024-02-01", "payment_date": None, "status": "overdue",
             "payment_method": "card", "failure_reason": "Card declined"},
            {"payment_id": "PAY_010", "invoice_id": "INV_2024_010", "amount": 99.99,
             "due_date": "2024-03-01", "payment_date": None, "status": "overdue",
             "payment_method": "card", "failure_reason": "Card declined"}
        ],
        "CUST_005": [
            {"payment_id": "PAY_011", "invoice_id": "INV_2024_011", "amount": 29.99,
             "due_date": "2024-02-01", "payment_date": "2024-02-01", "status": "paid",
             "payment_method": "card", "failure_reason": None}
        ]
    }

def seed_account_status():
    return {
        "CUST_001": {
            "status": "active",
            "enabled_features": ["dark_mode", "basic_dashboard", "email_reports",
                                  "api_access", "advanced_analytics", "sso", "webhooks"],
            "last_login": "2024-03-20",
            "trial": False
        },
        "CUST_002": {
            "status": "active",
            "enabled_features": ["dark_mode", "basic_dashboard", "email_reports"],
            "last_login": "2024-03-19",
            "trial": False
        },
        "CUST_003": {
            "status": "active",
            "enabled_features": ["dark_mode", "basic_dashboard", "email_reports",
                                  "api_access", "advanced_analytics", "sso", "webhooks",
                                  "custom_integrations", "audit_logs", "priority_support"],
            "last_login": "2024-03-21",
            "trial": False
        },
        "CUST_004": {
            "status": "suspended",
            "enabled_features": [],
            "last_login": "2024-01-15",
            "trial": False
        },
        "CUST_005": {
            "status": "active",
            "enabled_features": ["dark_mode", "basic_dashboard", "email_reports"],
            "last_login": "2024-03-18",
            "trial": False
        }
    }

def seed_features():
    features = {
        "dark_mode": {
            "feature_name": "dark_mode",
            "display_name": "Dark Mode",
            "available_on": ["plan_starter", "plan_pro", "plan_enterprise"],
            "description": "Switch the UI theme to dark for better visibility in low light environments.",
            "capabilities": [
                "Toggle between light and dark themes",
                "Persists across sessions",
                "Applies to all pages and dashboards"
            ],
            "limitations": [
                "Does not apply to exported PDFs",
                "Email reports always sent in light mode"
            ],
            "setup_guide": "Go to Settings → Appearance → Theme → Select Dark → Save",
            "expected_behavior": "UI switches to dark theme immediately after saving",
            "common_issues": "If theme reverts on refresh, clear browser cache and re-apply",
            "documentation_url": "https://docs.techcorp.com/features/dark-mode"
        },
        "api_access": {
            "feature_name": "api_access",
            "display_name": "API Access",
            "available_on": ["plan_pro", "plan_enterprise"],
            "description": "Programmatic access to TechCorp data via REST API for automation workflows.",
            "capabilities": [
                "Full REST API access",
                "OAuth2 authentication",
                "Webhook support",
                "Rate limited by plan"
            ],
            "limitations": [
                "Not available on Starter plan",
                "Rate limits apply based on plan",
                "No GraphQL support currently"
            ],
            "setup_guide": "Go to Settings → API → Generate API Key → Copy key → Use in Authorization header",
            "expected_behavior": "API returns 200 responses within rate limits, 429 when exceeded",
            "common_issues": "Rate limit errors after 1000 calls indicate Pro plan limit reached",
            "documentation_url": "https://docs.techcorp.com/features/api-access"
        },
        "sso": {
            "feature_name": "sso",
            "display_name": "Single Sign-On (SSO)",
            "available_on": ["plan_pro", "plan_enterprise"],
            "description": "Enable SSO via SAML 2.0 or OAuth2 for seamless team authentication.",
            "capabilities": [
                "SAML 2.0 support",
                "OAuth2 / OIDC support",
                "Auto-provisioning of users",
                "Role mapping from IdP"
            ],
            "limitations": [
                "Requires IT admin setup",
                "Not available on Starter plan"
            ],
            "setup_guide": "Go to Settings → Security → SSO → Upload IdP metadata → Test connection → Enable",
            "expected_behavior": "Users redirected to IdP login page on sign in",
            "common_issues": "Metadata mismatch causes login failures — re-upload IdP XML",
            "documentation_url": "https://docs.techcorp.com/features/sso"
        },
        "advanced_analytics": {
            "feature_name": "advanced_analytics",
            "display_name": "Advanced Analytics",
            "available_on": ["plan_pro", "plan_enterprise"],
            "description": "In-depth analytics with custom reports, funnels, and retention analysis.",
            "capabilities": [
                "Custom report builder",
                "Funnel analysis",
                "Retention cohorts",
                "Data export to CSV"
            ],
            "limitations": [
                "Data retention limited to 12 months on Pro",
                "Not available on Starter plan"
            ],
            "setup_guide": "Navigate to Analytics → Advanced → Enable Custom Reports",
            "expected_behavior": "Custom dashboards load within 5 seconds",
            "common_issues": "Slow load times indicate large date ranges — reduce to under 90 days",
            "documentation_url": "https://docs.techcorp.com/features/analytics"
        },
        "webhooks": {
            "feature_name": "webhooks",
            "display_name": "Webhooks",
            "available_on": ["plan_pro", "plan_enterprise"],
            "description": "Real-time event notifications sent to your endpoint via HTTP POST.",
            "capabilities": [
                "Real-time event delivery",
                "Retry on failure",
                "Signature verification",
                "Event filtering"
            ],
            "limitations": [
                "Max 10 webhook endpoints on Pro",
                "Payload size limit 1MB"
            ],
            "setup_guide": "Go to Settings → Webhooks → Add Endpoint → Select events → Save",
            "expected_behavior": "Events delivered within 30 seconds of trigger",
            "common_issues": "Endpoint must return 200 within 5 seconds or delivery is retried",
            "documentation_url": "https://docs.techcorp.com/features/webhooks"
        }
    }
    write("features", "features.json", features)

def seed_feature_limits():
    limits = {
        "api_access": {
            "plan_starter": {"enabled": False, "limit": 0, "unit": "calls/month"},
            "plan_pro": {"enabled": True, "limit": 1000, "unit": "calls/month"},
            "plan_enterprise": {"enabled": True, "limit": -1, "unit": "calls/month"}
        },
        "dark_mode": {
            "plan_starter": {"enabled": True, "limit": -1, "unit": "unlimited"},
            "plan_pro": {"enabled": True, "limit": -1, "unit": "unlimited"},
            "plan_enterprise": {"enabled": True, "limit": -1, "unit": "unlimited"}
        },
        "sso": {
            "plan_starter": {"enabled": False, "limit": 0, "unit": "connections"},
            "plan_pro": {"enabled": True, "limit": 1, "unit": "connections"},
            "plan_enterprise": {"enabled": True, "limit": -1, "unit": "connections"}
        },
        "advanced_analytics": {
            "plan_starter": {"enabled": False, "limit": 0, "unit": "reports"},
            "plan_pro": {"enabled": True, "limit": 50, "unit": "reports/month"},
            "plan_enterprise": {"enabled": True, "limit": -1, "unit": "reports/month"}
        },
        "webhooks": {
            "plan_starter": {"enabled": False, "limit": 0, "unit": "endpoints"},
            "plan_pro": {"enabled": True, "limit": 10, "unit": "endpoints"},
            "plan_enterprise": {"enabled": True, "limit": -1, "unit": "endpoints"}
        },
        "seats": {
            "plan_starter": {"enabled": True, "limit": 10, "unit": "users"},
            "plan_pro": {"enabled": True, "limit": 25, "unit": "users"},
            "plan_enterprise": {"enabled": True, "limit": -1, "unit": "users"}
        }
    }
    write("features", "feature_limits.json", limits)

def seed_feature_usage():
    usage = {
        "CUST_001": {
            "api_access": {
                "current_usage": 1200,
                "entitled_limit": 1000,
                "unit": "calls/month",
                "is_configured": True,
                "configuration_status": "correct",
                "mismatch_flag": True,
                "mismatch_detail": "Customer has used 1200 API calls but plan limit is 1000. Rate limiting is triggering correctly per plan terms. Documentation states unlimited but actual limit is 1000."
            },
            "dark_mode": {
                "current_usage": 1,
                "entitled_limit": -1,
                "unit": "unlimited",
                "is_configured": True,
                "configuration_status": "correct",
                "mismatch_flag": False,
                "mismatch_detail": None
            },
            "sso": {
                "current_usage": 1,
                "entitled_limit": 1,
                "unit": "connections",
                "is_configured": True,
                "configuration_status": "correct",
                "mismatch_flag": False,
                "mismatch_detail": None
            }
        },
        "CUST_002": {
            "dark_mode": {
                "current_usage": 0,
                "entitled_limit": -1,
                "unit": "unlimited",
                "is_configured": False,
                "configuration_status": "unchecked",
                "mismatch_flag": False,
                "mismatch_detail": None
            },
            "api_access": {
                "current_usage": 0,
                "entitled_limit": 0,
                "unit": "calls/month",
                "is_configured": False,
                "configuration_status": "not_available",
                "mismatch_flag": False,
                "mismatch_detail": "API access is not available on Starter plan. Customer needs to upgrade to Pro or Enterprise."
            }
        },
        "CUST_005": {
            "seats": {
                "current_usage": 15,
                "entitled_limit": 10,
                "unit": "users",
                "is_configured": True,
                "configuration_status": "misconfigured",
                "mismatch_flag": True,
                "mismatch_detail": "Customer has 15 users but Starter plan only allows 10 seats. 5 additional seats needed."
            }
        }
    }
    write("features", "feature_usage.json", usage)

def seed_contracts():
    contracts = {
        "CONT_001": {
            "contract_id": "CONT_001",
            "customer_id": "CUST_003",
            "plan_id": "plan_enterprise",
            "start_date": "2023-01-01",
            "end_date": "2025-12-31",
            "auto_renew": True,
            "sla_first_response_hours": 24,
            "sla_resolution_hours": 72,
            "contracted_features": ["api_access", "sso", "advanced_analytics",
                                     "webhooks", "custom_integrations", "audit_logs"],
            "custom_api_limit": -1,
            "custom_seats": -1,
            "pricing_terms": "custom",
            "custom_price": 249.99,
            "signed_by": "Carol Davis"
        },
        "CONT_002": {
            "contract_id": "CONT_002",
            "customer_id": "CUST_001",
            "plan_id": "plan_pro",
            "start_date": "2023-06-15",
            "end_date": "2024-06-14",
            "auto_renew": True,
            "sla_first_response_hours": 48,
            "sla_resolution_hours": 120,
            "contracted_features": ["api_access", "sso", "advanced_analytics", "webhooks"],
            "custom_api_limit": None,
            "custom_seats": None,
            "pricing_terms": "standard",
            "custom_price": None,
            "signed_by": "Alice Johnson"
        }
    }
    write("contracts", "contracts.json", contracts)

def seed_sla_terms():
    sla_terms = {
        "plan_starter": {
            "first_response_hours": 72,
            "resolution_hours": 168,
            "support_channel": "email only",
            "availability": "business hours"
        },
        "plan_pro": {
            "first_response_hours": 48,
            "resolution_hours": 120,
            "support_channel": "email + chat",
            "availability": "business hours + weekends"
        },
        "plan_enterprise": {
            "first_response_hours": 24,
            "resolution_hours": 72,
            "support_channel": "email + chat + phone",
            "availability": "24/7"
        }
    }
    write("contracts", "sla_terms.json", sla_terms)

def seed_entitlements():
    entitlements = {
        "CONT_001": {
            "contract_id": "CONT_001",
            "customer_id": "CUST_003",
            "guaranteed_features": ["api_access", "sso", "advanced_analytics",
                                     "webhooks", "custom_integrations", "audit_logs"],
            "api_limit": "unlimited",
            "seats": "unlimited",
            "sla_first_response": "24 hours",
            "sla_resolution": "72 hours",
            "special_terms": "Dedicated account manager assigned",
            "feature_entitlement_vs_usage": {
                "api_access": {"entitled": "unlimited", "actual": "unlimited", "match": True},
                "sso": {"entitled": "included", "actual": "configured", "match": True}
            }
        },
        "CONT_002": {
            "contract_id": "CONT_002",
            "customer_id": "CUST_001",
            "guaranteed_features": ["api_access", "sso", "advanced_analytics", "webhooks"],
            "api_limit": "1000 calls/month",
            "seats": "25",
            "sla_first_response": "48 hours",
            "sla_resolution": "120 hours",
            "special_terms": "None",
            "feature_entitlement_vs_usage": {
                "api_access": {"entitled": "1000/month", "actual": "1200/month", "match": False,
                               "note": "Customer exceeding contracted API limit"}
            }
        }
    }
    write("contracts", "entitlements.json", entitlements)

def seed_violations():
    violations = {
        "VIOL_001": {
            "violation_id": "VIOL_001",
            "contract_id": "CONT_001",
            "customer_id": "CUST_003",
            "violation_type": "sla_breach",
            "issue_description": "Critical production outage reported. No response from support for 10 days.",
            "issue_raised_at": "2024-03-01T09:00:00",
            "first_response_at": None,
            "resolved_at": None,
            "sla_limit_hours": 24,
            "actual_response_hours": 240,
            "breach_hours": 216,
            "sla_response_met": False,
            "sla_resolution_met": False,
            "violation_confirmed": True,
            "violation_summary": "SLA critically breached. Customer waited 240 hours (10 days) against contracted 24-hour SLA. Breach of 216 hours confirmed. Immediate escalation required.",
            "financial_impact": "$500/day in lost revenue claimed by customer"
        }
    }
    write("contracts", "violations.json", violations)

def seed_routing_rules():
    rules = {
        "RULE_001": {
            "rule_id": "RULE_001",
            "rule_name": "Critical SLA Breach",
            "condition_field": "breach_hours",
            "condition_operator": "gte",
            "condition_value": 24,
            "severity_level": "critical",
            "priority": "P1",
            "route_to_team": "engineering",
            "auto_escalate": True,
            "rule_description": "Any SLA breach over 24 hours is critical and escalates immediately to engineering"
        },
        "RULE_002": {
            "rule_id": "RULE_002",
            "rule_name": "Payment Overdue",
            "condition_field": "payment_status",
            "condition_operator": "eq",
            "condition_value": "overdue",
            "severity_level": "medium",
            "priority": "P3",
            "route_to_team": "billing",
            "auto_escalate": False,
            "rule_description": "Overdue payments routed to billing team for follow up"
        },
        "RULE_003": {
            "rule_id": "RULE_003",
            "rule_name": "Feature Mismatch Detected",
            "condition_field": "mismatch_flag",
            "condition_operator": "eq",
            "condition_value": True,
            "severity_level": "high",
            "priority": "P2",
            "route_to_team": "engineering",
            "auto_escalate": False,
            "rule_description": "Customer not receiving entitled features — engineering investigation needed"
        },
        "RULE_004": {
            "rule_id": "RULE_004",
            "rule_name": "Seat Limit Exceeded",
            "condition_field": "seats_exceeded",
            "condition_operator": "eq",
            "condition_value": True,
            "severity_level": "medium",
            "priority": "P3",
            "route_to_team": "account_mgmt",
            "auto_escalate": False,
            "rule_description": "Customer exceeding seat limit — account management to discuss upgrade"
        },
        "RULE_005": {
            "rule_id": "RULE_005",
            "rule_name": "Account Suspended",
            "condition_field": "account_status",
            "condition_operator": "eq",
            "condition_value": "suspended",
            "severity_level": "high",
            "priority": "P2",
            "route_to_team": "billing",
            "auto_escalate": True,
            "rule_description": "Suspended accounts escalated to billing immediately"
        }
    }
    write("escalations", "routing_rules.json", rules)

def seed_escalation_tickets():
    write("escalations", "escalation_tickets.json", {})

def seed_escalation_log():
    write("escalations", "escalation_log.json", [])

if __name__ == "__main__":
    print("Seeding all JSON database files...")
    print()
    seed_customers()
    plans = seed_plans()
    write("customers", "billing.json", seed_billing())
    write("customers", "account_status.json", seed_account_status())
    seed_features()
    seed_feature_limits()
    seed_feature_usage()
    seed_contracts()
    seed_sla_terms()
    seed_entitlements()
    seed_violations()
    seed_routing_rules()
    seed_escalation_tickets()
    seed_escalation_log()
    print()
    print("All database files seeded successfully!")
    print("Your JSON database is ready for all 5 test scenarios.")