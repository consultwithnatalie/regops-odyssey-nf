from __future__ import annotations

import json
import os
import re
from datetime import date
from html import escape
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

from coach import external_ai_feedback, rubric_feedback, voice_coach_html
from content import COACH_RUBRICS, CURRICULUM, GLOSSARY, PRICING, QUIZ, SCENARIO, SQL_CHALLENGES
from database import dashboard_data, execute_select, move_task, read_table, reset_demo, save_lead

APP_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="RegOps Odyssey | Product Consulting Academy",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
.block-container {padding-top: 1.1rem; padding-bottom: 3rem; max-width: 1500px;}
.hero {background:linear-gradient(135deg,#07172d 0%,#123b63 62%,#0f766e 100%); color:white; padding:34px; border-radius:22px; margin-bottom:20px; box-shadow:0 12px 32px rgba(7,23,45,.18)}
.hero h1 {font-size:3rem; margin:0 0 8px 0; line-height:1.05;}
.hero p {font-size:1.08rem; max-width:900px; color:#e8f3ff;}
.eyebrow {font-size:.8rem; text-transform:uppercase; letter-spacing:.14em; color:#8de6d9; font-weight:800;}
.card {background:white; border:1px solid #dfe8f2; border-radius:16px; padding:18px; height:100%; box-shadow:0 5px 18px rgba(16,35,63,.06)}
.darkcard {background:#0c213e; color:white; border-radius:16px; padding:18px; height:100%;}
.darkcard p {color:#cbd8e8;}
.badge {display:inline-block; padding:5px 10px; border-radius:999px; background:#dff7f3; color:#0f5b55; font-size:.78rem; font-weight:800; margin-right:5px; margin-bottom:5px;}
.mission {border-left:5px solid #2dd4bf; background:#f5fbfa; padding:14px 16px; border-radius:8px; margin:8px 0 14px 0;}
.warning {border-left:5px solid #f1b84b; background:#fff8e8; padding:14px 16px; border-radius:8px;}
.success {border-left:5px solid #38a169; background:#effaf3; padding:14px 16px; border-radius:8px;}
.metric-label {font-size:.82rem; color:#52677f; text-transform:uppercase; letter-spacing:.06em; font-weight:700;}
.small {font-size:.86rem;color:#5a6d84;}
.stButton>button {border-radius:10px; font-weight:700;}
[data-testid="stSidebar"] {background:#07172d;}
[data-testid="stSidebar"] * {color:#eef6ff;}
[data-testid="stSidebar"] .stSelectbox label {color:#eef6ff;}
hr {border:none;border-top:1px solid #dfe8f2;margin:20px 0;}
</style>
""",
    unsafe_allow_html=True,
)

if "completed" not in st.session_state:
    st.session_state.completed = set()
if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = None
if "lab_notes" not in st.session_state:
    st.session_state.lab_notes = {}


def mark_complete(module_id: str) -> None:
    st.session_state.completed.add(module_id)


def progress_value() -> float:
    return len(st.session_state.completed) / len(CURRICULUM)


def safe_email(value: str) -> bool:
    return bool(re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", value.strip()))


def page_header(title: str, subtitle: str, eyebrow: str = "RegOps Odyssey") -> None:
    st.markdown(
        f"""<div class="hero"><div class="eyebrow">{escape(eyebrow)}</div><h1>{escape(title)}</h1><p>{escape(subtitle)}</p></div>""",
        unsafe_allow_html=True,
    )


def stage_route(client_type: str, product: str, risk: str, pep: bool, sanctions: bool) -> tuple[pd.DataFrame, list[str], str]:
    required_docs = ["Proof of Legal Existence", "Registered Address Evidence", "Authorized Signatory List", "Tax Information"]
    if client_type in {"Private Company", "Partnership", "Fund", "Trust"}:
        required_docs += ["Ownership and Control Evidence", "Ultimate Beneficial Owner Identification"]
    if client_type == "Trust":
        required_docs += ["Trust Deed", "Settlor / Trustee / Beneficiary Details"]
    if product in {"Institutional Investment Account", "Treasury & FX"}:
        required_docs += ["Source of Funds Evidence", "Investment Purpose and Expected Activity"]
    if risk == "High" or pep or sanctions:
        required_docs += ["Enhanced Due Diligence Rationale", "Source of Wealth Evidence", "Senior Approval Record"]

    stages = [
        (1, "Request Intake", "Client Service", "Capture purpose, client type, products, jurisdictions and contacts."),
        (2, "Operations Validation", "Operations", "Validate completeness, duplicates, routing and service eligibility."),
        (3, "KYC Collection", "KYC", "Collect required client, party, ownership and evidence information."),
        (4, "KYC Verification", "KYC", "Verify evidence, ownership, identity and screening results."),
    ]
    if risk == "High" or pep or sanctions:
        stages.append((5, "Compliance Review", "Compliance + Head of Compliance", "Resolve alerts, complete EDD and record authorized approval."))
    else:
        stages.append((5, "Compliance Rules Check", "Compliance", "Confirm standard policy requirements are satisfied."))
    stages += [
        (6, "Account Setup", "Operations", "Create account and product records after all blocking controls pass."),
        (7, "Client Confirmation", "Client Service", "Issue confirmation, archive evidence and schedule ongoing review."),
    ]
    outcome = "Block and escalate" if sanctions else "Enhanced review required" if (risk == "High" or pep) else "Standard route"
    return pd.DataFrame(stages, columns=["Stage", "Name", "Owner", "Control / Outcome"]), sorted(set(required_docs)), outcome


with st.sidebar:
    st.markdown("## 🧭 RegOps Odyssey")
    st.caption("Financial-services product consulting, BI, data, configuration and delivery labs")
    st.progress(progress_value(), text=f"Learning progress: {len(st.session_state.completed)}/{len(CURRICULUM)} missions")
    page = st.radio(
        "Navigate",
        [
            "Home",
            "Mission Map",
            "KYC Journey Lab",
            "SQL Data Vault",
            "BI Control Tower",
            "Integration Bridge",
            "Agile Mission Control",
            "Configuration Forge",
            "Quality & Gap Analysis",
            "Product Consultant Studio",
            "Odyssey AI Coach",
            "Capstone & Completion",
            "Revenue Launchpad",
            "Glossary & Resources",
        ],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Fictional learning data only. Not affiliated with or endorsed by Fenergo or Kaha Consulting.")


if page == "Home":
    page_header(
        "RegOps Odyssey",
        "A marketable, adventure-based learning system where aspiring product consultants build real evidence in Agile delivery, financial services onboarding, KYC/AML, SQL, BI, integrations, SaaS configuration, testing, demonstrations and stakeholder leadership.",
        "Final product brand • Free-to-run training platform",
    )

    c1, c2, c3, c4 = st.columns(4)
    for col, value, label in [
        (c1, "10", "Skill missions"),
        (c2, "22–27", "Guided learning hours"),
        (c3, "7", "Hands-on workspaces"),
        (c4, "1", "Portfolio capstone"),
    ]:
        with col:
            st.markdown(f"<div class='card'><div style='font-size:2rem;font-weight:900'>{value}</div><div class='metric-label'>{label}</div></div>", unsafe_allow_html=True)

    st.markdown("### What learners actually do")
    cols = st.columns(3)
    cards = [
        ("🧩 Configure", "Build an onboarding route, evidence rules, high-risk approvals, reusable components and tenant working practices."),
        ("🗃️ Query", "Use SQL against an original client, product, document, journey, task, integration and transaction database."),
        ("📊 Explain", "Read a BI control tower, find root causes and present executive recommendations."),
        ("🔌 Integrate", "Map CRM data into a CLM-style case, validate JSON and design exception handling."),
        ("🧪 Prove", "Run negative tests, edge cases, spikes, fit-gap analysis and release-readiness checks."),
        ("🎤 Lead", "Gather requirements, control scope, demonstrate solutions, support change and transfer knowledge."),
    ]
    for i, (title, text) in enumerate(cards):
        with cols[i % 3]:
            st.markdown(f"<div class='card'><h3>{title}</h3><p>{text}</p></div>", unsafe_allow_html=True)

    st.markdown("### Final expedition")
    st.markdown(
        f"""<div class='mission'><b>{SCENARIO['program']}</b><br>{SCENARIO['problem']}<br><br><b>Client:</b> {SCENARIO['client']}</div>""",
        unsafe_allow_html=True,
    )
    st.write("The learner finishes with a journey design, relational data model, rules, integration mapping, Agile backlog, test evidence, BI dashboard interpretation, demo script and release recommendation.")

    st.markdown("### Fenergo and Kaha foundational lens")
    st.write(
        "The curriculum uses public industry context to teach the kind of lifecycle thinking associated with Fenergo-enabled programs: onboarding, KYC/AML, ongoing review, rules, evidence, integrations and operational control. It also reflects Kaha Consulting’s publicly described implementation approach across readiness, blueprinting, testing and deployment. Every lab, screen, rule and scenario in RegOps Odyssey is original and fictional."
    )

    st.markdown("### Why this can earn revenue")
    st.write(
        "The free tier demonstrates value and captures interest. Paid access can unlock the full learning path, reusable templates, interview simulations, portfolio review, guided cohorts and team licensing. The Revenue Launchpad contains the working offer structure and configurable checkout calls to action."
    )

elif page == "Mission Map":
    page_header("Mission Map", "Each segment is time-boxed to 1–2 or 2–3 hours and ends with proof a learner can show, discuss or add to a portfolio.")
    for mission in CURRICULUM:
        complete = mission["id"] in st.session_state.completed
        with st.expander(f"{'✅' if complete else '🧭'} {mission['id']} — {mission['title']} · {mission['duration']} · {mission['level']}"):
            st.markdown(f"**Mission:** {mission['mission']}")
            st.markdown(" ".join(f"<span class='badge'>{escape(skill)}</span>" for skill in mission["skills"]), unsafe_allow_html=True)
            for segment, text in mission["segments"]:
                st.markdown(f"**{segment}:** {text}")
            st.markdown(f"**Portfolio evidence:** {mission['deliverable']}")
            notes = st.text_area("Mission notes", key=f"notes_{mission['id']}", placeholder="Capture decisions, questions, evidence and next actions.")
            if notes:
                st.session_state.lab_notes[mission["id"]] = notes
            if st.button("Mark mission complete", key=f"complete_{mission['id']}", disabled=complete):
                mark_complete(mission["id"])
                st.rerun()

elif page == "KYC Journey Lab":
    page_header("KYC Journey Lab", "Configure a client- and product-onboarding route using original, fictional data and risk-based controls.", "Mission M03 + M07")
    left, right = st.columns([1, 1.35])
    with left:
        client_type = st.selectbox("Client type", ["Private Company", "Listed Company", "Partnership", "Fund", "Trust", "Bank", "Fintech"])
        product = st.selectbox("Product", ["Institutional Investment Account", "Current Account", "Secured Loan", "Unsecured Loan", "Treasury & FX", "Merchant Settlement"])
        jurisdiction = st.selectbox("Primary jurisdiction", ["United States", "Ireland", "United Kingdom", "Luxembourg", "South Africa", "Singapore", "Norway", "Egypt"])
        risk = st.select_slider("Initial risk rating", options=["Low", "Medium", "High"], value="Medium")
        pep = st.checkbox("Potential PEP connection")
        sanctions = st.checkbox("Potential sanctions match")
        st.caption("A potential match is an alert for investigation—not a conclusion about a person or entity.")
    stages, docs, outcome = stage_route(client_type, product, risk, pep, sanctions)
    with right:
        st.metric("Routing result", outcome)
        st.dataframe(stages, use_container_width=True, hide_index=True)
    st.markdown("### Dynamic evidence checklist")
    doc_df = pd.DataFrame({"Required evidence": docs, "Purpose": ["Support identity, ownership, risk, product or approval requirements." for _ in docs]})
    st.dataframe(doc_df, use_container_width=True, hide_index=True)

    st.markdown("### Rule-design challenge")
    st.code(
        "IF Risk = High OR PEP Alert = True\nTHEN create Compliance Review task; require EDD evidence; block Account Setup until authorized approval\nELSE continue standard compliance rules check",
        language="text",
    )
    rationale = st.text_area("Explain your configuration decision", placeholder="State the trigger, evidence, decision owner, blocking control, exception path and intended business outcome.")
    if st.button("Evaluate rationale"):
        result = rubric_feedback("KYC/AML Rationale", rationale)
        st.metric("Consulting score", f"{result['score']}/100", result["level"])
        st.write(result["summary"])
        for item in result["next_moves"]:
            st.write("•", item)
    if st.button("Complete M03 KYC & AML Investigation"):
        mark_complete("M03")
        st.success("Mission M03 recorded as complete.")

elif page == "SQL Data Vault":
    page_header("SQL Data Vault", "Run read-only SQL against the fictional RegOps Odyssey database and convert results into business decisions.", "Mission M04")
    with st.expander("Database schema", expanded=False):
        schema = pd.DataFrame(
            [
                ("clients", "Client type, country, region, risk, screening flags, owner and review date"),
                ("products", "Product family and risk weight"),
                ("client_products", "Many-to-many client/product relationship"),
                ("documents", "Evidence type, status, verification and expiry"),
                ("journeys", "Stage, SLA, age, high-risk gate, reopen count and status"),
                ("tasks", "Sprint, owner, work type, status, story points and due date"),
                ("transactions", "Amount, country, channel, date and training alert flag"),
                ("integrations", "Route, object, volume, errors and latency"),
                ("requirements", "Persona, acceptance criteria, priority, status and owner"),
            ],
            columns=["Table", "Contains"],
        )
        st.dataframe(schema, use_container_width=True, hide_index=True)

    challenge_title = st.selectbox("Choose a challenge", [c["title"] for c in SQL_CHALLENGES])
    challenge = next(c for c in SQL_CHALLENGES if c["title"] == challenge_title)
    st.markdown(f"<div class='mission'><b>Challenge:</b> {challenge['prompt']}<br><span class='small'>Hint: {challenge['hint']}</span></div>", unsafe_allow_html=True)
    query = st.text_area("SQL editor", value=challenge["starter"], height=220)
    if st.button("Run query", type="primary"):
        try:
            result = execute_select(query)
            st.success(f"Query returned {len(result):,} rows.")
            st.dataframe(result, use_container_width=True, hide_index=True)
            st.download_button("Download query result", result.to_csv(index=False).encode("utf-8"), "regops_sql_result.csv", "text/csv")
        except Exception as exc:
            st.error(str(exc))
    interpretation = st.text_area("Business interpretation", placeholder="What happened, why it matters, what should be investigated, and who should act?")
    if st.button("Score interpretation"):
        result = rubric_feedback("Solution Design", interpretation)
        st.metric("Interpretation score", f"{result['score']}/100", result["level"])
        st.write(result["summary"])
        for move in result["next_moves"]:
            st.write("•", move)
    if st.button("Complete M04 SQL Data Vault"):
        mark_complete("M04")
        st.success("Mission M04 recorded as complete.")

elif page == "BI Control Tower":
    page_header("BI Control Tower", "Filter operational data, identify the constraint behind onboarding delays and build an executive storyline.", "Mission M05")
    data = dashboard_data()
    journeys = data["journeys"].copy()
    clients = data["clients"].copy()
    documents = data["documents"].copy()
    tasks = data["tasks"].copy()
    integrations = data["integrations"].copy()

    f1, f2, f3 = st.columns(3)
    regions = f1.multiselect("Region", sorted(clients["region"].unique()), default=sorted(clients["region"].unique()))
    risks = f2.multiselect("Risk", ["Low", "Medium", "High"], default=["Low", "Medium", "High"])
    statuses = f3.multiselect("Journey status", sorted(journeys["status"].unique()), default=sorted(journeys["status"].unique()))
    filtered = journeys[journeys["region"].isin(regions) & journeys["risk_rating"].isin(risks) & journeys["status"].isin(statuses)].copy()
    filtered["sla_exposure"] = filtered["days_open"] - filtered["sla_days"]
    filtered_clients = set(filtered["client_id"].tolist())
    filtered_docs = documents[documents["client_id"].isin(filtered_clients)]

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Open journeys", int((filtered["status"] == "Open").sum()))
    k2.metric("High risk", int((filtered["risk_rating"] == "High").sum()))
    k3.metric("Over SLA", int((filtered["sla_exposure"] > 0).sum()))
    k4.metric("Evidence gaps", int(filtered_docs["status"].isin(["Missing", "Expired"]).sum()))
    failure_rate = 100 * integrations["error_count"].sum() / max(1, integrations["records_processed"].sum())
    k5.metric("Integration errors", f"{failure_rate:.1f}%")

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            filtered.groupby(["region", "risk_rating"], as_index=False).size(),
            x="region", y="size", color="risk_rating", barmode="stack",
            title="Journey population by region and risk",
            labels={"size": "Journeys", "region": "Region", "risk_rating": "Risk"},
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        stage_age = filtered.groupby("current_stage", as_index=False)["days_open"].mean().sort_values("days_open", ascending=False)
        fig = px.bar(stage_age, x="days_open", y="current_stage", orientation="h", title="Average age by current stage", labels={"days_open": "Average days open", "current_stage": "Stage"})
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        task_summary = tasks.groupby("status", as_index=False)["story_points"].sum()
        fig = px.pie(task_summary, names="status", values="story_points", hole=.45, title="Story-point distribution")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        route_summary = integrations.groupby(["source_system", "target_system"], as_index=False).agg(records=("records_processed", "sum"), errors=("error_count", "sum"), latency=("latency_ms", "mean"))
        route_summary["failure_rate"] = 100 * route_summary["errors"] / route_summary["records"].clip(lower=1)
        fig = px.scatter(route_summary, x="latency", y="failure_rate", size="records", hover_name="source_system", hover_data=["target_system"], title="Integration reliability map", labels={"latency": "Average latency (ms)", "failure_rate": "Failure rate (%)"})
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Executive exception list")
    exception_view = filtered[(filtered["sla_exposure"] > 0) | (filtered["risk_rating"] == "High")][["client_name", "region", "risk_rating", "current_stage", "days_open", "sla_days", "sla_exposure", "assigned_owner"]].sort_values(["sla_exposure", "days_open"], ascending=False)
    st.dataframe(exception_view, use_container_width=True, hide_index=True)
    story = st.text_area("Write the executive storyline", placeholder="Situation: ...\nComplication: ...\nResolution: ...\nDecision requested: ...")
    if st.button("Evaluate executive storyline"):
        result = rubric_feedback("Demo Presentation", story)
        st.metric("Storyline score", f"{result['score']}/100", result["level"])
        for move in result["next_moves"]:
            st.write("•", move)
    if st.button("Complete M05 BI Control Tower"):
        mark_complete("M05")
        st.success("Mission M05 recorded as complete.")

elif page == "Integration Bridge":
    page_header("Integration Bridge", "Map client data across a Dynamics-style CRM, onboarding case, screening service and BI route, then test failures.", "Mission M06")
    default_payload = {
        "correlationId": "REG-OD-2026-1042",
        "source": "Dynamics CRM",
        "client": {
            "legalName": "Asteria Global Holdings",
            "registrationNumber": "IE-884219",
            "countryCode": "IE",
            "clientType": "Private Company",
            "products": ["INVESTMENT_ACCOUNT", "TREASURY_FX"],
            "riskRating": "High",
        },
    }
    left, right = st.columns([1.1, 1])
    with left:
        payload_text = st.text_area("Inbound JSON", json.dumps(default_payload, indent=2), height=330)
    with right:
        st.markdown("#### Target field mapping")
        mapping = pd.DataFrame(
            [
                ("client.legalName", "case.client.legal_name", "Required; trim whitespace"),
                ("client.registrationNumber", "case.client.external_id", "Required; duplicate check"),
                ("client.countryCode", "case.client.country", "ISO two-letter code"),
                ("client.clientType", "case.client.type", "Translate to configured enumeration"),
                ("client.products[]", "case.products[].code", "Validate product code"),
                ("client.riskRating", "case.risk.initial_rating", "Allowed: Low, Medium, High"),
                ("correlationId", "case.integration.correlation_id", "Required for traceability"),
            ],
            columns=["Source", "Target", "Validation"],
        )
        st.dataframe(mapping, use_container_width=True, hide_index=True)

    if st.button("Validate and transform", type="primary"):
        try:
            payload = json.loads(payload_text)
            errors = []
            client = payload.get("client", {})
            if not payload.get("correlationId"):
                errors.append("Missing correlationId")
            if not client.get("legalName"):
                errors.append("Missing legalName")
            if len(client.get("countryCode", "")) != 2:
                errors.append("countryCode must contain two characters")
            valid_products = {"INVESTMENT_ACCOUNT", "CURRENT_ACCOUNT", "SECURED_LOAN", "UNSECURED_LOAN", "TREASURY_FX", "MERCHANT_SETTLEMENT"}
            unknown = [p for p in client.get("products", []) if p not in valid_products]
            if unknown:
                errors.append("Unknown product code(s): " + ", ".join(unknown))
            if client.get("riskRating") not in {"Low", "Medium", "High"}:
                errors.append("Invalid riskRating")

            transformed = {
                "case": {
                    "client": {
                        "legal_name": client.get("legalName", "").strip(),
                        "external_id": client.get("registrationNumber"),
                        "country": client.get("countryCode"),
                        "type": client.get("clientType"),
                    },
                    "products": [{"code": p} for p in client.get("products", [])],
                    "risk": {"initial_rating": client.get("riskRating")},
                    "integration": {"correlation_id": payload.get("correlationId"), "source": payload.get("source")},
                }
            }
            if errors:
                st.error("Validation failed")
                for err in errors:
                    st.write("•", err)
            else:
                st.success("Payload passed validation and is ready for case creation.")
                st.json(transformed)
        except json.JSONDecodeError as exc:
            st.error(f"Invalid JSON: {exc}")

    st.markdown("### Bridge Collapse challenge")
    edge = st.selectbox("Failure scenario", ["Duplicate message", "Screening timeout", "Partial client update", "Invalid country code", "Downstream BI outage"])
    recommendations = {
        "Duplicate message": "Use an idempotency key or correlation ID, detect the prior successful transaction, and return the existing case result rather than creating a second case.",
        "Screening timeout": "Place the request in a retryable state, preserve the correlation ID, use bounded retries with backoff, then route to an exception queue with ownership and SLA.",
        "Partial client update": "Define field-level update rules, protect verified values, record provenance, and reconcile source and target versions before overwriting data.",
        "Invalid country code": "Reject before case creation, return a field-specific validation message, and monitor recurring source-data defects.",
        "Downstream BI outage": "Keep the operational transaction independent, queue the event, replay safely after recovery, and reconcile event counts to the source system.",
    }
    st.info(recommendations[edge])
    if st.button("Complete M06 Integration Bridge"):
        mark_complete("M06")
        st.success("Mission M06 recorded as complete.")

elif page == "Agile Mission Control":
    page_header("Agile Mission Control", "Manage a live fictional backlog, move work through delivery and practice scope decisions.", "Mission M01")
    tasks = read_table("tasks")
    selected_sprint = st.selectbox("Sprint", sorted(tasks["sprint"].unique()))
    sprint_tasks = tasks[tasks["sprint"] == selected_sprint]
    status_order = ["Backlog", "Ready", "In Progress", "Review", "Done"]
    cols = st.columns(5)
    for col, status in zip(cols, status_order):
        with col:
            subset = sprint_tasks[sprint_tasks["status"] == status]
            st.markdown(f"#### {status} · {len(subset)}")
            for _, row in subset.iterrows():
                st.markdown(
                    f"<div class='card'><b>#{row['task_id']} {escape(row['title'])}</b><br><span class='small'>{escape(row['owner'])} · {row['story_points']} pts · due {row['due_date']}</span></div>",
                    unsafe_allow_html=True,
                )
    st.divider()
    m1, m2, m3 = st.columns(3)
    task_id = m1.selectbox("Work item", sprint_tasks["task_id"].astype(int).tolist(), format_func=lambda x: f"#{x} — {sprint_tasks.loc[sprint_tasks['task_id'] == x, 'title'].iloc[0]}")
    new_status = m2.selectbox("Move to", status_order)
    if m3.button("Update board", type="primary"):
        move_task(int(task_id), new_status)
        st.success("Work item updated.")
        st.rerun()

    st.markdown("### Scope Storm")
    scope_request = st.selectbox("New request arrives mid-sprint", [
        "Add a new jurisdiction before release",
        "Change the approved risk model thresholds",
        "Improve wording on the client confirmation screen",
        "Add a second screening provider",
    ])
    decision = st.radio("Your delivery decision", ["Accept into current sprint", "Swap with an equal-sized item", "Add to backlog", "Raise formal change control"])
    if st.button("Review scope decision"):
        high_impact = scope_request in {"Add a new jurisdiction before release", "Change the approved risk model thresholds", "Add a second screening provider"}
        if high_impact and decision in {"Add to backlog", "Raise formal change control"}:
            st.success("Strong control: the request affects policy, integrations, testing or release scope and should be assessed before commitment.")
        elif not high_impact and decision in {"Swap with an equal-sized item", "Add to backlog"}:
            st.success("Reasonable: a lower-impact change can be traded transparently or scheduled without destabilizing the sprint.")
        else:
            st.warning("Explain capacity, dependency, test impact, approval needs and what existing commitment would change.")
    if st.button("Complete M01 Agile Launch Bay"):
        mark_complete("M01")
        st.success("Mission M01 recorded as complete.")

elif page == "Configuration Forge":
    page_header("Configuration Forge", "Design reusable configuration and protect a shared SaaS tenant from conflicts, brittle rules and uncontrolled releases.", "Mission M07")
    st.markdown("### Configuration components")
    components_df = pd.DataFrame(
        [
            ("Journey", "Institutional Investment Account", "Stages, entry criteria, exit criteria and exception routes", "Journey-PC-INV-001"),
            ("Rule", "High-risk approval", "Risk/PEP/sanctions trigger and blocking approval", "Rule-KYC-HR-001"),
            ("Document set", "Corporate standard evidence", "Reusable data and evidence requirements", "Docs-CORP-STD-001"),
            ("Data object", "Client party", "Legal entity, ownership, address, tax and risk attributes", "Data-PARTY-001"),
            ("Integration", "CRM client intake", "Field mapping, validation, idempotency and reconciliation", "Int-CRM-CLM-001"),
            ("Dashboard event", "Journey stage changed", "Event sent to reporting route with timestamps and ownership", "Evt-JRN-STG-001"),
        ],
        columns=["Type", "Component", "Design responsibility", "Naming standard"],
    )
    st.dataframe(components_df, use_container_width=True, hide_index=True)

    st.markdown("### Tenant working agreement builder")
    a, b = st.columns(2)
    with a:
        owner = st.text_input("Component owner", "Product Consultant")
        change_id = st.text_input("Change reference", "ADO-1842")
        environment = st.selectbox("Environment", ["Development", "Test", "UAT", "Production"])
    with b:
        dependency = st.text_input("Known dependencies", "High-risk rule, document set, BI event")
        promotion = st.selectbox("Promotion method", ["Packaged and versioned", "Manual controlled change", "Automated pipeline"])
        rollback = st.text_input("Rollback plan", "Restore prior version and replay test pack")
    agreement = f"Owner: {owner}\nChange: {change_id}\nEnvironment: {environment}\nDependencies: {dependency}\nPromotion: {promotion}\nRollback: {rollback}"
    st.code(agreement, language="text")

    st.markdown("### Shared Tenant Maze")
    conflict = st.selectbox("Conflict", ["Two people editing one rule", "Unlabeled duplicate components", "UAT fix made directly in production", "Migration pack missing a dependency"])
    controls = {
        "Two people editing one rule": "Assign one change owner, stop parallel edits, record the baseline, coordinate a merge decision, version the component and rerun dependent tests.",
        "Unlabeled duplicate components": "Apply naming and ownership standards, compare use and dependencies, select the reusable source of truth, retire duplicates through controlled change.",
        "UAT fix made directly in production": "Record the incident, restore environment alignment, recreate the fix in the source environment, test it, then promote through the approved path.",
        "Migration pack missing a dependency": "Stop release, compare dependency manifests, add the missing component, rerun deployment and regression checks, and update the release checklist.",
    }
    st.info(controls[conflict])
    if st.button("Complete M07 Configuration Forge"):
        mark_complete("M07")
        st.success("Mission M07 recorded as complete.")

elif page == "Quality & Gap Analysis":
    page_header("Quality & Gap Analysis Cavern", "Test the happy path, negative paths, boundaries, integrations and configuration gaps before approving release.", "Mission M08")
    st.markdown("### Use-case test designer")
    test_case = st.selectbox("Scenario", [
        "Required ownership document is missing",
        "Potential duplicate client is found",
        "Ownership changes after KYC verification",
        "Head of Compliance rejects high-risk onboarding",
        "Screening service returns multiple possible matches",
        "Client requests a product unsupported in one jurisdiction",
    ])
    expected = st.text_area("Expected system behavior", placeholder="Trigger, status, user message, owner, evidence, downstream impact and exit condition.")
    if st.button("Assess test design"):
        keywords = ["status", "task", "owner", "block", "evidence", "message", "audit", "exit"]
        hits = [k for k in keywords if k in expected.lower()]
        score = round(100 * len(hits) / len(keywords))
        st.metric("Test completeness", f"{score}/100")
        if score >= 75:
            st.success("The test covers control behavior and operational handling. Add exact data conditions and expected timestamps where relevant.")
        else:
            st.warning("A resilient test should state the resulting status, blocking behavior, user task, owner, evidence/audit result, message and exit condition.")

    st.markdown("### Spike and fit-gap register")
    fit = st.selectbox("Fit assessment", ["Standard configuration", "Configuration extension", "Integration solution", "Process workaround", "Product engineering gap"])
    option = st.text_area("Option and recommendation", placeholder="Requirement, options considered, outcome, risks, recommendation and follow-up owner.")
    if st.button("Generate fit-gap record"):
        record = {
            "scenario": test_case,
            "fit_assessment": fit,
            "recommendation": option,
            "decision_status": "Proposed",
            "required_evidence": ["Spike notes", "Configuration/integration impact", "Test evidence", "Stakeholder decision"],
        }
        st.json(record)
    if st.button("Complete M08 Quality & Gap Analysis"):
        mark_complete("M08")
        st.success("Mission M08 recorded as complete.")

elif page == "Product Consultant Studio":
    page_header("Product Consultant Studio", "Practice the full consulting cycle: discovery, analysis, solution design, demonstration, approval, change and knowledge transfer.", "Mission M09")
    tab1, tab2, tab3, tab4 = st.tabs(["Requirements", "Solution Design", "Demo & Approval", "Change & Knowledge"])
    with tab1:
        stakeholder_statement = st.text_area("Raw stakeholder statement", "We need high-risk clients to go through more checks, but we cannot slow down every client.")
        persona = st.text_input("Primary persona", "Compliance Officer")
        user_need = st.text_input("Testable need", "Route only qualifying high-risk cases to enhanced review")
        business_value = st.text_input("Business value", "Maintain stronger controls without adding unnecessary delay to standard cases")
        acceptance = st.text_area("Acceptance criteria", "1. High-risk, PEP-alert or sanctions-alert cases create an enhanced review task.\n2. Account setup is blocked until authorized approval.\n3. Standard-risk cases do not receive the enhanced-review task.\n4. All decisions retain timestamp, owner and evidence.")
        if st.button("Build requirement", key="build_req"):
            st.markdown(
                f"**User story:** As a {persona}, I need to {user_need.lower()} so that {business_value.lower()}.\n\n**Acceptance criteria**\n{acceptance}"
            )
    with tab2:
        requirements = read_table("requirements")
        st.dataframe(requirements, use_container_width=True, hide_index=True)
        selected_req = st.selectbox("Requirement to design", requirements["req_id"].tolist(), format_func=lambda x: requirements.loc[requirements["req_id"] == x, "title"].iloc[0])
        journey_decision = st.text_area("Journey decision", placeholder="Where is this requirement handled in the journey?")
        data_decision = st.text_area("Data decision", placeholder="What data object, attributes, provenance or relationships are needed?")
        rule_decision = st.text_area("Rule decision", placeholder="What condition, action, priority and exception apply?")
        integration_decision = st.text_area("Integration decision", placeholder="What systems exchange data and how are errors reconciled?")
        if st.button("Create design summary"):
            summary = {
                "requirement": requirements.loc[requirements["req_id"] == selected_req, "title"].iloc[0],
                "journey": journey_decision,
                "data": data_decision,
                "rule": rule_decision,
                "integration": integration_decision,
                "review_questions": ["Is the decision testable?", "Does it reuse standard capability?", "What is the exception path?", "What could be affected elsewhere?"],
            }
            st.json(summary)
    with tab3:
        demo_goal = st.text_input("Demo outcome", "Secure approval of the high-risk routing design")
        demo_script = st.text_area("Demo script", "Today I will show how the proposed journey separates standard and high-risk cases, preserves evidence, and prevents account setup before authorized approval...")
        objection = st.selectbox("Stakeholder objection", ["This adds too much time", "We need more flexibility", "Why can’t the system auto-approve?", "Can we add another country now?"])
        if st.button("Coach my demo"):
            result = rubric_feedback("Demo Presentation", demo_script + " " + demo_goal + " " + objection)
            st.metric("Demo score", f"{result['score']}/100", result["level"])
            for move in result["next_moves"]:
                st.write("•", move)
    with tab4:
        st.markdown("**Change actions**")
        st.checkbox("Identify impacted roles and current-state pain points")
        st.checkbox("Explain what changes, what stays the same and why")
        st.checkbox("Update procedures, training and support ownership")
        st.checkbox("Pilot with measurable adoption and quality criteria")
        st.checkbox("Capture feedback and feed valid product gaps to engineering")
        st.checkbox("Complete knowledge transfer and confirm operational readiness")
        feedback = st.text_area("Constructive feedback to a junior consultant", placeholder="Observation, impact, expected standard, specific next action and support offered.")
        if st.button("Evaluate feedback quality"):
            result = rubric_feedback("Stakeholder Management", feedback)
            st.metric("Feedback score", f"{result['score']}/100", result["level"])
            for move in result["next_moves"]:
                st.write("•", move)
    if st.button("Complete M09 Product Consultant Command"):
        mark_complete("M09")
        st.success("Mission M09 recorded as complete.")

elif page == "Odyssey AI Coach":
    page_header("Odyssey AI Coach", "A voice-enabled and written practice environment that scores consulting answers, speaks feedback and assigns the next learning task.", "AI-assisted learning layer")
    mode = st.selectbox("Practice mode", list(COACH_RUBRICS.keys()))
    st.markdown("### Live voice practice")
    components.html(voice_coach_html(mode), height=360, scrolling=False)
    st.caption("The voice console uses browser speech recognition and speech synthesis. The written coach below works in every supported browser.")

    st.markdown("### Written adaptive coach")
    prompt = COACH_RUBRICS[mode]["task"]
    st.markdown(f"<div class='mission'><b>Your task:</b> {escape(prompt)}</div>", unsafe_allow_html=True)
    answer = st.text_area("Your response", height=220, placeholder="Respond as though you are speaking to a client or project team.")
    if st.button("Get coaching", type="primary"):
        built_in = rubric_feedback(mode, answer)
        st.metric("Readiness score", f"{built_in['score']}/100", built_in["level"])
        st.write(built_in["summary"])
        if built_in["covered"]:
            st.write("**Concepts demonstrated:**", ", ".join(built_in["covered"]))
        for move in built_in["next_moves"]:
            st.write("•", move)
        st.info("Next task: " + built_in["next_task"])
        enhanced = external_ai_feedback(mode, answer)
        if enhanced:
            st.markdown("#### Connected model feedback")
            st.write(enhanced)
        else:
            st.caption("Using the built-in adaptive rubric. A private OpenAI-compatible endpoint can be connected through environment variables without changing the course experience.")

elif page == "Capstone & Completion":
    page_header("Final Expedition", "Combine journey, data, rules, integrations, Agile delivery, testing, BI and consulting leadership into one portfolio-ready implementation case.", "Mission M10")
    st.markdown(f"### {SCENARIO['program']}")
    st.write(SCENARIO["problem"])
    st.markdown("**Required business outcomes**")
    for outcome in SCENARIO["outcomes"]:
        st.write("•", outcome)

    st.markdown("### Capstone evidence checklist")
    checklist_items = [
        "Situation–Complication–Resolution problem statement",
        "Stakeholder map and discovery plan",
        "Journey with standard, high-risk and exception paths",
        "Relational data model and field dictionary",
        "KYC/AML rule and evidence matrix",
        "CRM-to-onboarding-to-screening integration mapping",
        "Agile epic, stories, acceptance criteria and sprint board",
        "Negative, edge-case and integration test pack",
        "BI control tower with executive interpretation",
        "Demo script, decision log, approval and release recommendation",
        "Change, training and knowledge-transfer plan",
    ]
    checked = []
    cols = st.columns(2)
    for i, item in enumerate(checklist_items):
        with cols[i % 2]:
            checked.append(st.checkbox(item, key=f"cap_{i}"))
    completion_pct = round(100 * sum(checked) / len(checked))
    st.progress(completion_pct / 100, text=f"Capstone evidence: {completion_pct}%")

    st.markdown("### Knowledge check")
    responses = []
    for i, q in enumerate(QUIZ):
        responses.append(st.radio(q["question"], q["options"], index=None, key=f"quiz_{i}"))
    if st.button("Score knowledge check"):
        score = 0
        for response, q in zip(responses, QUIZ):
            if response is not None and q["options"].index(response) == q["answer"]:
                score += 1
        st.session_state.quiz_score = score
        st.metric("Knowledge check", f"{score}/{len(QUIZ)}")
        for q in QUIZ:
            st.caption(q["explanation"])

    st.markdown("### Completion record")
    learner_name = st.text_input("Learner name", "Natalie Frost")
    eligible = completion_pct == 100 and st.session_state.quiz_score is not None and st.session_state.quiz_score >= 3
    if eligible:
        if st.button("Complete M10 Final Expedition"):
            mark_complete("M10")
            st.success("Mission M10 recorded as complete.")
        certificate = f"""<!doctype html><html><head><meta charset='utf-8'><style>body{{font-family:Arial;background:#07172d;padding:60px}}.cert{{background:white;border:12px solid #0f766e;padding:70px;text-align:center}}h1{{font-size:44px;color:#10233f}}h2{{font-size:32px;color:#0f766e}}p{{font-size:18px;line-height:1.6}}</style></head><body><div class='cert'><div>REGOPS ODYSSEY</div><h1>Completion Record</h1><p>This recognizes</p><h2>{escape(learner_name)}</h2><p>for completing the RegOps Odyssey Product Consulting learning experience and demonstrating foundational capability in Agile delivery, financial-services onboarding, KYC/AML, SQL, BI, integrations, SaaS configuration, testing and product consulting.</p><p><b>Date:</b> {date.today().strftime('%B %d, %Y')}</p><p><small>Training completion record; not a regulated professional certification.</small></p></div></body></html>"""
        st.download_button("Download completion record", certificate.encode("utf-8"), "RegOps_Odyssey_Completion_Record.html", "text/html")
    else:
        st.warning("Complete every capstone evidence item and score at least 3/4 on the knowledge check to unlock the completion record.")

elif page == "Revenue Launchpad":
    page_header("Revenue Launchpad", "Convert the training environment into a lead generator, self-paced product, guided cohort and team enablement offer.", "Monetization system")
    st.markdown("### Offer ladder")
    cols = st.columns(4)
    env_urls = {
        "Explorer": "",
        "Career Pass": os.getenv("CAREER_PASS_URL", ""),
        "Consultant Lab": os.getenv("CONSULTANT_LAB_URL", ""),
        "Guided Cohort": os.getenv("COHORT_URL", ""),
    }
    for col, tier in zip(cols, PRICING):
        with col:
            items = "".join(f"<li>{escape(x)}</li>" for x in tier["includes"])
            st.markdown(f"<div class='card'><h3>{tier['name']}</h3><div style='font-size:1.8rem;font-weight:900'>{tier['price']}</div><p class='small'>{tier['audience']}</p><ul>{items}</ul></div>", unsafe_allow_html=True)
            if env_urls[tier["name"]]:
                st.link_button(tier["cta"], env_urls[tier["name"]], use_container_width=True)
            else:
                st.button(tier["cta"], key=f"tier_{tier['name']}", use_container_width=True, disabled=tier["name"] != "Explorer")

    st.markdown("### Lead capture")
    with st.form("lead_form"):
        c1, c2 = st.columns(2)
        name = c1.text_input("Name")
        email = c2.text_input("Email")
        interest = st.selectbox("Primary interest", ["Free exploration", "Career Pass", "Consultant Lab", "Guided Cohort", "Team license"])
        submitted = st.form_submit_button("Join the learning list", type="primary")
        if submitted:
            if not name.strip() or not safe_email(email):
                st.error("Enter a name and valid email address.")
            else:
                save_lead(name, email, interest)
                st.success("Interest recorded in the local training database.")

    st.markdown("### Revenue design")
    revenue_df = pd.DataFrame(
        [
            ("Self-paced sales", "Career Pass and Consultant Lab", "Automated", "Course unlock + templates"),
            ("Cohorts", "Four-week guided implementation lab", "Monthly or quarterly", "Live sessions + capstone review"),
            ("Career services", "Portfolio critique and mock demonstration", "Add-on", "Individual feedback"),
            ("Teams", "Banks, consultancies, nonprofits and workforce programs", "Annual / cohort", "Private cohort + reporting"),
            ("Sponsorship", "Fintech, training or recruiting partners", "Campaign", "Branded challenge without changing curriculum integrity"),
        ],
        columns=["Revenue stream", "Offer", "Cadence", "Value"],
    )
    st.dataframe(revenue_df, use_container_width=True, hide_index=True)

    st.markdown("### Launch sequence")
    launch = pd.DataFrame(
        [
            ("Week 1", "Deploy free app, connect checkout URLs, add privacy/terms, publish one free mission."),
            ("Week 2", "Invite 10–20 founding learners, observe friction, collect testimonials and improve instructions."),
            ("Week 3", "Open Career Pass and Consultant Lab; post one SQL, BI or onboarding challenge each week."),
            ("Week 4", "Run the first guided cohort and convert the strongest capstones into permission-based case-study examples."),
            ("Month 2+", "Pitch workforce programs, community organizations and small consultancies on team access and facilitated cohorts."),
        ],
        columns=["Timing", "Action"],
    )
    st.dataframe(launch, use_container_width=True, hide_index=True)
    st.caption("Payment processing, taxes, consumer disclosures and access control must be configured before paid public launch.")

    with st.expander("Local admin — training leads"):
        leads = read_table("leads")
        st.dataframe(leads, use_container_width=True, hide_index=True)
        if not leads.empty:
            st.download_button("Export leads", leads.to_csv(index=False).encode("utf-8"), "regops_odyssey_leads.csv", "text/csv")
        if st.button("Reset all fictional demo data"):
            reset_demo()
            st.success("Demo database reset.")

elif page == "Glossary & Resources":
    page_header("Glossary & Resources", "Foundational terms, practice tools and responsible-use boundaries for the learning environment.")
    for term, definition in GLOSSARY.items():
        st.markdown(f"**{term}:** {definition}")
    st.markdown("### Free-tool operating model")
    tools = pd.DataFrame(
        [
            ("Streamlit Community Cloud", "Host the public learning application", "Core deployment"),
            ("GitHub", "Version control, public portfolio and deployment source", "Core delivery"),
            ("SQLite", "Embedded fictional training database", "Core data lab"),
            ("Plotly", "Interactive BI visualizations", "Core reporting"),
            ("Browser Web Speech APIs", "Live speech recognition and spoken feedback where supported", "Core voice practice"),
            ("Azure Boards / Trello", "Optional external Agile practice", "Extension"),
            ("Airtable", "Optional no-code compliance and workflow exercise", "Extension"),
            ("OpenAI-compatible model endpoint", "Optional generative coaching enhancement", "Bring your own endpoint"),
        ],
        columns=["Tool", "Role", "Use"],
    )
    st.dataframe(tools, use_container_width=True, hide_index=True)
    st.markdown("### Responsible-use boundaries")
    st.markdown(
        """
- All clients, transactions, risks and alerts in this program are fictional.
- The platform teaches transferable product-consulting and configuration concepts; it does not provide access to proprietary Fenergo or Kaha systems, training, data or certification.
- KYC/AML exercises are educational and do not replace legal, regulatory, compliance or financial-crime advice.
- A potential screening match is treated as an alert for authorized investigation, never as proof of wrongdoing.
- Do not place real client, identity, financial, confidential or regulated data into a public training deployment.
        """
    )
