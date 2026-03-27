import streamlit as st
import sys
import os
import yaml

#This is how app.py is connected to main.py
sys.path.append(os.path.dirname(__file__))
from main import run_query

st.set_page_config(
    page_title="TechCorp Support AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Session state ─────────────────────────────────────────────
if "messages"  not in st.session_state: st.session_state.messages  = []
if "metrics"   not in st.session_state: st.session_state.metrics   = {"queries":0,"agents":0,"tokens":0,"escalations":0}
if "provider"  not in st.session_state: st.session_state.provider  = "Groq · Llama 3.3"
if "customer"  not in st.session_state: st.session_state.customer  = "CUST_001"

# ── Provider switching ────────────────────────────────────────
PROVIDER_MAP = {
    "Groq · Llama 3.3":  "groq",
    "Gemini 2.0 Flash":  "gemini",
    "Ollama · local":    "ollama"
}

def switch_provider(selected: str):
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    new = PROVIDER_MAP[selected]
    if config["llm"]["provider"] != new:
        config["llm"]["provider"] = new
        with open("config.yaml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)

# ── Customer profiles ─────────────────────────────────────────
CUSTOMERS = {
    "CUST_001": {
        "label":   "CUST_001 · Alice Johnson",
        "plan":    "Pro Plan",
        "status":  "Active",
        "company": "Acme Corp",
        "color":   "#4ade80"
    },
    "CUST_002": {
        "label":   "CUST_002 · Bob Smith",
        "plan":    "Starter Plan",
        "status":  "Active",
        "company": "Startup XYZ",
        "color":   "#a5b4fc"
    },
    "CUST_003": {
        "label":   "CUST_003 · Carol Davis",
        "plan":    "Enterprise Plan",
        "status":  "Active",
        "company": "Enterprise Co",
        "color":   "#fbbf24"
    },
    "CUST_004": {
        "label":   "CUST_004 · David Lee",
        "plan":    "Pro Plan",
        "status":  "Suspended",
        "company": "Tech Ventures",
        "color":   "#f87171"
    },
    "CUST_005": {
        "label":   "CUST_005 · Eva Martinez",
        "plan":    "Starter Plan",
        "status":  "Active",
        "company": "Growth Co",
        "color":   "#a5b4fc"
    },
}

# ── Scenarios ─────────────────────────────────────────────────
SCENARIOS = {
    "✦ Custom query":               ("", None),
    "S1 · Enable dark mode":        ("How do I enable dark mode in my account?",                                                             None),
    "S2 · API on Starter plan":     ("I'm on the Starter plan but I need API access for automation. What are my options?",                    None),
    "S3 · Pro rate limit conflict": ("Pro plan says unlimited API calls but I'm getting rate limit errors after 1000 calls. Is this a bug?",  None),
    "S4 · SLA violated 10 days":    ("I've been waiting 10 days on a critical production issue. My contract has a 24h SLA. Please escalate.", "2024-03-01T09:00:00"),
    "S5 · 15 users only 10 seats":  ("We have 15 users but our plan shows only 10 seats. Help me understand the licensing and fix this.",     None),
}

# ── Theme ─────────────────────────────────────────────────────
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: #0a0f1e !important;
    color: #cbd5e1 !important;
}
[data-testid="stSidebar"] {
    background-color: #0d1117 !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
.customer-card {
    background: #0d1117;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
}
.customer-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    font-weight: 700;
    flex-shrink: 0;
}
.customer-info { flex: 1; }
.customer-name { font-size: 15px; font-weight: 700; color: #f1f5f9; }
.customer-sub  { font-size: 12px; color: #475569; margin-top: 2px; }
.customer-badge {
    font-size: 11px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
}
.user-msg {
    background: #6366f1;
    color: #fff !important;
    padding: 12px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 18%;
    font-size: 14px;
    line-height: 1.65;
}
.answer-box {
    background: #0d1117;
    border: 1px solid #1e293b;
    border-left: 3px solid #6366f1;
    border-radius: 4px 14px 14px 14px;
    padding: 16px 20px;
    font-size: 14px;
    line-height: 1.8;
    color: #cbd5e1;
    margin-bottom: 10px;
}
            
.lf-link {
    color: #818cf8 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-decoration: none !important;
    cursor: pointer !important;
}
.lf-link:hover {
    color: #a5b4fc !important;
    text-decoration: underline !important;
}            
.agent-card {
    background: #0d1117;
    border: 1px solid #1e293b;
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 6px;
}
.agent-top {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 14px;
    border-bottom: 1px solid #161b27;
}
.agent-body {
    padding: 8px 14px;
    font-size: 12px;
    color: #475569;
    background: #080c14;
    line-height: 1.6;
}
.badge { font-size:11px; font-weight:700; padding:3px 10px; border-radius:20px; }
.badge-account    { background:#0d2818; color:#4ade80; border:1px solid #14532d; }
.badge-feature    { background:#13111f; color:#a5b4fc; border:1px solid #2d2a5e; }
.badge-contract   { background:#1c1408; color:#fbbf24; border:1px solid #451a03; }
.badge-escalation { background:#1c0a0a; color:#f87171; border:1px solid #450a0a; }
.agent-task { font-size:12px; color:#334155; flex:1; }
.chip {
    display:inline-block; background:#161b27; color:#7dd3fc;
    font-family:monospace; font-size:11px; padding:1px 7px;
    border-radius:4px; border:1px solid #1e293b;
}
.resolved { padding:7px 14px; font-size:11px; font-weight:700;
    color:#4ade80; background:#0a1f12; border-top:1px solid #14532d; }
.escalated { padding:7px 14px; font-size:11px; font-weight:700;
    color:#f87171; background:#130a0a; border-top:1px solid #450a0a; }
.total-row {
    display:flex; background:#0d1117; border:1px solid #1e293b;
    border-radius:10px; overflow:hidden; margin-top:4px;
}
.total-cell { flex:1; padding:9px 14px; border-right:1px solid #161b27; }
.total-cell:last-child { border-right:none; display:flex; align-items:center; justify-content:flex-end; }
.tkey { font-size:10px; color:#334155; text-transform:uppercase; letter-spacing:.06em; font-weight:700; }
.tval { font-size:14px; font-weight:700; color:#e2e8f0; margin-top:2px; }
.lf-link { font-size:11px; color:#818cf8; font-weight:600; cursor:pointer; }
div[data-testid="stTextInput"] input {
    background: #161b27 !important;
    border: 1.5px solid #1e293b !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
}
div[data-testid="stButton"] button {
    background: #6366f1 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}
div[data-testid="stButton"] button:hover { background: #4f46e5 !important; }
div[data-testid="stSelectbox"] > div {
    background: #161b27 !important;
    border: 1px solid #1e293b !important;
    color: #cbd5e1 !important;
    border-radius: 9px !important;
}
div[data-testid="stMetricValue"] { color: #e2e8f0 !important; font-weight:700 !important; }
div[data-testid="stMetricLabel"] { color: #475569 !important; font-size:11px !important; }
div[data-testid="stMetric"] {
    background:#161b27 !important;
    border:1px solid #1e293b !important;
    border-radius:9px !important;
    padding:10px 12px !important;
}
h1,h2,h3 { color: #f1f5f9 !important; }
hr { border-color: #1e293b !important; }
div[data-testid="stRadio"] label { color: #475569 !important; font-size:13px !important; }
div[data-testid="stRadio"] label:hover { color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────
def clean_summary(text):
    if not text:
        return None
    if any(x in text for x in ["LLM call failed", "RESOURCE_EXHAUSTED", "HTTPConnection", "Error calling"]):
        return None
    return text

def agent_card_html(name, task, body, strip=None):
    badge_map = {
        "Account Agent":    "badge-account",
        "Feature Agent":    "badge-feature",
        "Contract Agent":   "badge-contract",
        "Escalation Agent": "badge-escalation",
    }
    cls = badge_map.get(name, "badge-feature")
    strip_html = ""
    if strip == "resolved":
        strip_html = '<div class="resolved">● Resolved · No escalation needed</div>'
    elif strip == "escalated":
        strip_html = '<div class="escalated">● Escalated · Human intervention required</div>'
    return f"""
    <div class="agent-card">
        <div class="agent-top">
            <span class="badge {cls}">{name}</span>
            <span class="agent-task">{task}</span>
        </div>
        <div class="agent-body">{body}</div>
        {strip_html}
    </div>"""

def render_customer_card(cid):
    c = CUSTOMERS[cid]
    initials = "".join([w[0] for w in c["label"].split("·")[1].strip().split()[:2]])
    status_color = "#4ade80" if c["status"] == "Active" else "#f87171"
    status_bg    = "#0d2818" if c["status"] == "Active" else "#1c0a0a"
    status_border= "#14532d" if c["status"] == "Active" else "#450a0a"
    st.markdown(f"""
    <div class="customer-card">
        <div class="customer-avatar" style="background:{c['color']}22;color:{c['color']}">
            {initials}
        </div>
        <div class="customer-info">
            <div class="customer-name">{c['label'].split('·')[1].strip()}</div>
            <div class="customer-sub">{c['company']} &nbsp;·&nbsp; {c['plan']}</div>
        </div>
        <span class="customer-badge" style="background:{status_bg};color:{status_color};border:1px solid {status_border}">
            {c['status']}
        </span>
    </div>""", unsafe_allow_html=True)

def render_response(result):
    findings   = result["findings"]
    account    = findings.get("account",    {})
    feature    = findings.get("feature",    {})
    contract   = findings.get("contract",   {})
    escalation = findings.get("escalation", {})
    agents     = result["agents_used"]
    escalated  = escalation.get("should_escalate", False)

    answer_lines = []
    answer_lines.append(f"<b>{account.get('full_name','Customer')}</b> &nbsp;·&nbsp; {account.get('plan_name','?')} Plan &nbsp;·&nbsp; {account.get('account_status','?').capitalize()}<br><br>")

    acc_sum  = clean_summary(account.get("llm_summary"))
    feat_sum = clean_summary(feature.get("llm_summary"))
    cont_sum = clean_summary(contract.get("llm_summary"))
    esc_sum  = clean_summary(escalation.get("llm_summary"))

    if acc_sum:  answer_lines.append(f"{acc_sum}<br><br>")
    if feat_sum: answer_lines.append(f"{feat_sum}<br>")
    if cont_sum: answer_lines.append(f"<br>{cont_sum}<br>")
    if esc_sum:  answer_lines.append(f"<br>{esc_sum}<br>")

    if not any([acc_sum, feat_sum, cont_sum, esc_sum]):
        if feature.get("feature_available_on_plan"):
            answer_lines.append(f"<b>{feature.get('display_name','Feature')}</b> is available on your plan.<br>")
            answer_lines.append(f"Setup: <b>{feature.get('setup_guide','See documentation')}</b><br>")
        elif feature.get("display_name"):
            answer_lines.append(f"<b>{feature.get('display_name','Feature')}</b> is not available on your current plan.<br>")
            answer_lines.append(f"Available on: <b>{', '.join(feature.get('available_on_plans',[]))}</b> — please upgrade.<br>")
        if contract.get("sla_violated"):
            answer_lines.append(f"<br>SLA violated by <b>{contract.get('breach_hours',0)}</b> hours.<br>")
        if escalation.get("should_escalate"):
            answer_lines.append(f"<br>Issue escalated to <b>{escalation.get('assigned_team','?')}</b> team.<br>")

    if escalation.get("should_escalate"):
        answer_lines.append(f"<br><b>Ticket:</b> {escalation.get('ticket_id','?')} &nbsp;·&nbsp; <b>Priority:</b> {escalation.get('priority','?')} &nbsp;·&nbsp; <b>Team:</b> {escalation.get('assigned_team','?')}")

    st.markdown(f'<div class="answer-box">{"".join(answer_lines)}</div>', unsafe_allow_html=True)

    cards_html = ""
    for i, name in enumerate(agents):
        is_last = i == len(agents) - 1
        if name == "Account Agent":
            task = f"Verified profile · {account.get('plan_name','?')} plan · {account.get('account_status','?')} · {account.get('billing_health','?')} billing"
            body = f'<span class="chip">lookup_customer()</span> · <span class="chip">get_billing_history()</span> · <span class="chip">check_account_status()</span> · <span class="chip">list_enabled_features()</span><br>Customer <b style="color:#f1f5f9">{account.get("full_name","?")}</b> · Plan: <b style="color:#f1f5f9">{account.get("plan_name","?")}</b> · Billing: <b style="color:#f1f5f9">{account.get("billing_health","?")}</b>'
            strip = None
        elif name == "Feature Agent":
            avail    = "available on plan" if feature.get("feature_available_on_plan") else "NOT available on plan"
            mismatch = "mismatch detected" if feature.get("has_mismatch") else "no mismatch"
            task = f'{feature.get("display_name","?")} · {avail} · {mismatch}'
            body = f'<span class="chip">get_feature_matrix()</span> · <span class="chip">get_feature_documentation("{feature.get("feature_name","?")}")</span> · <span class="chip">check_feature_limits()</span> · <span class="chip">validate_configuration()</span> · <span class="chip">detect_mismatch()</span><br>Feature <b style="color:#f1f5f9">{feature.get("display_name","?")}</b> — {avail} · {mismatch}'
            strip = "resolved" if is_last and not escalated else None
        elif name == "Contract Agent":
            violated = contract.get("sla_violated", False)
            breach   = contract.get("breach_hours", 0)
            task = f'Contract {contract.get("contract_id","N/A")} · SLA violated: {violated} · {breach}h breach'
            body = f'<span class="chip">lookup_contract()</span> · <span class="chip">get_contract_terms()</span> · <span class="chip">validate_sla_compliance()</span> · <span class="chip">get_included_features()</span><br>Contract: <b style="color:#f1f5f9">{contract.get("contract_id","None")}</b> · SLA: <b style="color:#f1f5f9">{contract.get("sla_first_response_hours","?")}h</b> · Violated: <b style="color:{"#f87171" if violated else "#4ade80"}">{violated}</b>'
            strip = None
        elif name == "Escalation Agent":
            ticket = escalation.get("ticket_id","N/A")
            team   = escalation.get("assigned_team","N/A")
            prio   = escalation.get("priority","N/A")
            task = f'Ticket {ticket} · {team} team · {prio} priority'
            body = f'<span class="chip">check_existing_tickets()</span> · <span class="chip">create_escalation_ticket()</span> · <span class="chip">get_escalation_routing()</span> · <span class="chip">notify_support_team()</span> · <span class="chip">log_escalation_reason()</span><br>Ticket: <b style="color:#f1f5f9">{ticket}</b> · Team: <b style="color:#f1f5f9">{team}</b> · Priority: <b style="color:#fbbf24">{prio}</b>'
            strip = "escalated" if escalated else "resolved"
        else:
            task  = "Investigation complete"
            body  = "Agent completed investigation."
            strip = None
        cards_html += agent_card_html(name, task, body, strip)

    st.markdown(cards_html, unsafe_allow_html=True)
    
    trace_url = result.get("trace_url", "https://cloud.langfuse.com")

    st.markdown(f"""
    <div class="total-row">
        <div class="total-cell"><div class="tkey">Total time</div><div class="tval">{result['total_time']}s</div></div>
        <div class="total-cell"><div class="tkey">Total tokens</div><div class="tval">{result['total_tokens']}</div></div>
        <div class="total-cell"><div class="tkey">Agents used</div><div class="tval">{len(agents)} of 5</div></div>
        <div class="total-cell">
            <a href="{trace_url}" 
            target="_blank" 
            rel="noopener noreferrer"
            onclick="window.open('{trace_url}', '_blank'); return false;"
            class="lf-link"
            style="color:#818cf8;font-size:11px;font-weight:600;text-decoration:none;cursor:pointer">
            View Langfuse trace ↗
            </a>
        </div>
    </div>""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 TechCorp Support AI")
    st.caption("Multi-Agent Intelligence System")
    st.divider()

    st.markdown("**LLM Provider**")
    provider = st.selectbox(
        "",
        ["Groq · Llama 3.3", "Gemini 2.0 Flash", "Ollama · local"],
        index=["Groq · Llama 3.3", "Gemini 2.0 Flash", "Ollama · local"].index(st.session_state.provider),
        label_visibility="collapsed"
    )
    if provider != st.session_state.provider:
        st.session_state.provider = provider
        switch_provider(provider)
        st.success(f"Switched to {provider}!")

    st.divider()

    st.markdown("**Select Customer**")
    customer_label = st.selectbox(
        "",
        [c["label"] for c in CUSTOMERS.values()],
        label_visibility="collapsed"
    )
    selected_customer_id = [k for k, v in CUSTOMERS.items() if v["label"] == customer_label][0]
    st.session_state.customer = selected_customer_id
    render_customer_card(selected_customer_id)

    st.divider()
    st.markdown("**Test Scenarios**")
    scenario = st.radio("", list(SCENARIOS.keys()), label_visibility="collapsed")

    st.divider()
    st.markdown("**Session Stats**")
    m = st.session_state.metrics
    c1, c2 = st.columns(2)
    c1.metric("Queries",     m["queries"])
    c2.metric("Agents",      m["agents"])
    c1.metric("Tokens",      m["tokens"])
    c2.metric("Escalations", m["escalations"])

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ── Main ──────────────────────────────────────────────────────
st.markdown("## Support Intelligence System")
st.caption(f"Powered by **{provider}** · 5 Specialized Agents · JSON Knowledge Base")
st.divider()

# ── Chat history ──────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        cid  = msg.get("customer_id", "CUST_001")
        cust = CUSTOMERS.get(cid, {})
        name = cust.get("label","").split("·")[1].strip() if "·" in cust.get("label","") else "Customer"
        st.markdown(f'<div class="user-msg"><small style="opacity:.7">{name}</small><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.container():
            render_response(msg["result"])
        st.divider()

# ── Input ─────────────────────────────────────────────────────
scenario_query, scenario_date = SCENARIOS[scenario]


#Customer id
active_customer = st.session_state.customer
cust_info = CUSTOMERS[active_customer]

st.markdown(f"""
<div style="background:#0d1117;border:1px solid #1e293b;border-radius:10px;
padding:10px 16px;margin-bottom:10px;font-size:13px;color:#475569;display:flex;align-items:center;gap:10px">
    <span style="color:#6366f1;font-weight:700">Sending as:</span>
    <span style="color:#f1f5f9;font-weight:600">{cust_info['label'].split('·')[1].strip()}</span>
    <span>·</span>
    <span>{cust_info['plan']}</span>
    <span>·</span>
    <span style="color:{'#4ade80' if cust_info['status']=='Active' else '#f87171'}">{cust_info['status']}</span>
</div>""", unsafe_allow_html=True)

with st.form("chat_form", clear_on_submit=True):
    col_inp, col_btn = st.columns([5, 1])
    with col_inp:

        #We get user input
        user_input = st.text_input(
            "",
            value=scenario_query,
            placeholder="Type any query or pick a scenario from the sidebar...",
            label_visibility="collapsed"
        )
    with col_btn:
        submitted = st.form_submit_button("Send", use_container_width=True)

if submitted and user_input:
    st.session_state.messages.append({
        "role":        "user",
        "content":     user_input,
        "customer_id": active_customer
    })
    with st.spinner(f"🔍 Investigating for {cust_info['label'].split('·')[1].strip()} with {provider}..."):
        try:

            #here the run_query function is called which is in main.py and the result is stored in variable
            result    = run_query(user_input, active_customer, scenario_date)
            escalated = result["findings"].get("escalation", {}).get("should_escalate", False)
            st.session_state.messages.append({"role": "assistant", "result": result})
            m = st.session_state.metrics
            m["queries"]     += 1
            m["agents"]       = len(result["agents_used"])
            m["tokens"]      += result["total_tokens"]
            m["escalations"] += 1 if escalated else 0
        except Exception as e:
            st.error(f"❌ {provider} failed: {str(e)[:200]}")
            st.info("💡 Switch to Groq · Llama 3.3 which is free and working perfectly.")
    st.rerun()