"""Create and interact with the fictional RegOps Odyssey training database."""

from __future__ import annotations

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pandas as pd

DB_PATH = Path(__file__).resolve().parent / "data" / "regops_odyssey.db"


def _dater(base: date, days: int) -> str:
    return (base + timedelta(days=days)).isoformat()


def init_database(force: bool = False) -> Path:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DB_PATH.exists() and not force:
        return DB_PATH

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript(
        """
        PRAGMA foreign_keys = ON;
        CREATE TABLE clients (
            client_id INTEGER PRIMARY KEY,
            client_name TEXT NOT NULL,
            client_type TEXT NOT NULL,
            country TEXT NOT NULL,
            region TEXT NOT NULL,
            risk_rating TEXT NOT NULL,
            pep_flag INTEGER NOT NULL,
            sanctions_hit INTEGER NOT NULL,
            onboarding_status TEXT NOT NULL,
            review_date TEXT NOT NULL,
            assigned_owner TEXT NOT NULL,
            source_system TEXT NOT NULL,
            created_date TEXT NOT NULL
        );
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            product_name TEXT NOT NULL,
            product_family TEXT NOT NULL,
            risk_weight INTEGER NOT NULL
        );
        CREATE TABLE client_products (
            client_product_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            status TEXT NOT NULL,
            requested_date TEXT NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(client_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        CREATE TABLE documents (
            document_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            doc_type TEXT NOT NULL,
            status TEXT NOT NULL,
            expiry_date TEXT,
            verified INTEGER NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(client_id)
        );
        CREATE TABLE journeys (
            journey_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            journey_type TEXT NOT NULL,
            current_stage TEXT NOT NULL,
            sla_days INTEGER NOT NULL,
            days_open INTEGER NOT NULL,
            high_risk_gate INTEGER NOT NULL,
            reopened_stages INTEGER NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(client_id)
        );
        CREATE TABLE tasks (
            task_id INTEGER PRIMARY KEY,
            journey_id INTEGER NOT NULL,
            sprint INTEGER NOT NULL,
            owner TEXT NOT NULL,
            task_type TEXT NOT NULL,
            title TEXT NOT NULL,
            status TEXT NOT NULL,
            story_points INTEGER NOT NULL,
            due_date TEXT NOT NULL,
            FOREIGN KEY(journey_id) REFERENCES journeys(journey_id)
        );
        CREATE TABLE transactions (
            txn_id INTEGER PRIMARY KEY,
            client_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            country TEXT NOT NULL,
            channel TEXT NOT NULL,
            txn_date TEXT NOT NULL,
            alert_flag INTEGER NOT NULL,
            FOREIGN KEY(client_id) REFERENCES clients(client_id)
        );
        CREATE TABLE integrations (
            integration_id INTEGER PRIMARY KEY,
            source_system TEXT NOT NULL,
            target_system TEXT NOT NULL,
            object_name TEXT NOT NULL,
            run_date TEXT NOT NULL,
            last_status TEXT NOT NULL,
            records_processed INTEGER NOT NULL,
            error_count INTEGER NOT NULL,
            latency_ms INTEGER NOT NULL
        );
        CREATE TABLE requirements (
            req_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            persona TEXT NOT NULL,
            acceptance_criteria TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            owner TEXT NOT NULL
        );
        CREATE TABLE leads (
            lead_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            interest TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )

    clients = [
        (1, "Asteria Global Holdings", "Private Company", "Ireland", "EMEA", "High", 1, 0, "In Review", _dater(date.today(), 18), "Maya Chen", "Dynamics CRM", _dater(date.today(), -42)),
        (2, "BluePeak Renewable Fund", "Fund", "Luxembourg", "EMEA", "Medium", 0, 0, "Onboarding", _dater(date.today(), 66), "Ethan Ross", "Salesforce", _dater(date.today(), -27)),
        (3, "Cedar Ridge Manufacturing", "Private Company", "United States", "Americas", "Low", 0, 0, "Approved", _dater(date.today(), 310), "Natalie Frost", "Dynamics CRM", _dater(date.today(), -19)),
        (4, "Delta Meridian Trust", "Trust", "United Kingdom", "EMEA", "High", 0, 1, "Escalated", _dater(date.today(), -8), "Maya Chen", "Partner Portal", _dater(date.today(), -61)),
        (5, "Everstone Capital Partners", "Partnership", "United States", "Americas", "Medium", 0, 0, "Onboarding", _dater(date.today(), 94), "Natalie Frost", "Salesforce", _dater(date.today(), -22)),
        (6, "Fjordline Shipping AS", "Private Company", "Norway", "EMEA", "Medium", 0, 0, "In Review", _dater(date.today(), 45), "Amina Yusuf", "Dynamics CRM", _dater(date.today(), -34)),
        (7, "Golden Baobab Trading", "Private Company", "South Africa", "Africa", "High", 0, 0, "Onboarding", _dater(date.today(), 12), "Thabo Ndlovu", "Partner Portal", _dater(date.today(), -49)),
        (8, "Harborlight Family Office", "Family Office", "Singapore", "APAC", "Medium", 1, 0, "In Review", _dater(date.today(), 27), "Priya Shah", "Salesforce", _dater(date.today(), -37)),
        (9, "Ionix Payments Ltd", "Fintech", "Ireland", "EMEA", "Low", 0, 0, "Approved", _dater(date.today(), 350), "Ethan Ross", "Dynamics CRM", _dater(date.today(), -15)),
        (10, "Juniper Municipal Treasury", "Public Entity", "Canada", "Americas", "Low", 0, 0, "Onboarding", _dater(date.today(), 140), "Natalie Frost", "Partner Portal", _dater(date.today(), -11)),
        (11, "Kestrel Mining Group", "Listed Company", "Australia", "APAC", "High", 0, 0, "In Review", _dater(date.today(), -3), "Priya Shah", "Dynamics CRM", _dater(date.today(), -55)),
        (12, "Lumina Health Ventures", "Fund", "United States", "Americas", "Medium", 0, 0, "Onboarding", _dater(date.today(), 75), "Natalie Frost", "Salesforce", _dater(date.today(), -29)),
        (13, "Mosaic Infrastructure PLC", "Listed Company", "United Kingdom", "EMEA", "Low", 0, 0, "Approved", _dater(date.today(), 280), "Amina Yusuf", "Dynamics CRM", _dater(date.today(), -21)),
        (14, "Nile Bridge Commodities", "Private Company", "Egypt", "Africa", "High", 0, 0, "Escalated", _dater(date.today(), 5), "Thabo Ndlovu", "Partner Portal", _dater(date.today(), -72)),
        (15, "Orchid Digital Assets", "Fintech", "Singapore", "APAC", "High", 1, 0, "In Review", _dater(date.today(), 20), "Priya Shah", "Salesforce", _dater(date.today(), -46)),
        (16, "Prairie Community Bank", "Bank", "United States", "Americas", "Medium", 0, 0, "Onboarding", _dater(date.today(), 120), "Natalie Frost", "Dynamics CRM", _dater(date.today(), -17)),
        (17, "Quartz Aviation Leasing", "Private Company", "Ireland", "EMEA", "Medium", 0, 0, "In Review", _dater(date.today(), 41), "Ethan Ross", "Salesforce", _dater(date.today(), -39)),
        (18, "Redwood Pension Trustees", "Trust", "United Kingdom", "EMEA", "Low", 0, 0, "Approved", _dater(date.today(), 330), "Maya Chen", "Partner Portal", _dater(date.today(), -25)),
    ]
    cur.executemany("INSERT INTO clients VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", clients)

    products = [
        (1, "Institutional Investment Account", "Investments", 4),
        (2, "Current Account", "Deposits", 2),
        (3, "Secured Loan", "Lending", 3),
        (4, "Unsecured Loan", "Lending", 5),
        (5, "Treasury & FX", "Markets", 4),
        (6, "Merchant Settlement", "Payments", 5),
    ]
    cur.executemany("INSERT INTO products VALUES (?,?,?,?)", products)

    random.seed(14)
    cp_id = 1
    for client_id in range(1, 19):
        count = random.choice([1, 1, 2, 2, 3])
        for product_id in random.sample(range(1, 7), count):
            cur.execute(
                "INSERT INTO client_products VALUES (?,?,?,?,?)",
                (cp_id, client_id, product_id, random.choice(["Requested", "In Setup", "Active"]), _dater(date.today(), -random.randint(5, 60))),
            )
            cp_id += 1

    doc_types = ["Certificate of Incorporation", "Ownership Register", "Proof of Address", "Authorized Signatory List", "Source of Funds Evidence", "Tax Form"]
    statuses = ["Verified", "Verified", "Verified", "Pending", "Missing", "Expired"]
    doc_id = 1
    for client_id in range(1, 19):
        for doc_type in random.sample(doc_types, random.choice([3, 4, 5, 6])):
            status = random.choice(statuses)
            cur.execute(
                "INSERT INTO documents VALUES (?,?,?,?,?,?)",
                (doc_id, client_id, doc_type, status, _dater(date.today(), random.randint(-80, 500)), 1 if status == "Verified" else 0),
            )
            doc_id += 1

    stages = ["Request Intake", "Operations Validation", "KYC Collection", "KYC Verification", "Compliance Review", "Account Setup", "Client Confirmation"]
    journey_rows = []
    for client_id, client in enumerate(clients, start=1):
        # client tuple index 5 = risk, 8 = status
        risk = client[5]
        onboarding_status = client[8]
        days_open = random.randint(8, 76)
        sla = 25 if risk == "High" else 20
        journey_rows.append((client_id, client_id, "Investment Account Onboarding", random.choice(stages), sla, days_open, 1 if risk == "High" else 0, random.randint(0, 3), "Closed" if onboarding_status == "Approved" else "Open"))
    cur.executemany("INSERT INTO journeys VALUES (?,?,?,?,?,?,?,?,?)", journey_rows)

    task_titles = [
        ("Story", "Confirm client type and product scope"),
        ("Task", "Map CRM fields to case data"),
        ("Task", "Configure required-document rule"),
        ("Task", "Create high-risk approval gate"),
        ("Test", "Run missing-document negative test"),
        ("Test", "Validate duplicate-client response"),
        ("Demo", "Prepare stakeholder walkthrough"),
    ]
    owners = ["Natalie Frost", "Maya Chen", "Ethan Ross", "Amina Yusuf", "Priya Shah", "Thabo Ndlovu"]
    statuses_task = ["Backlog", "Ready", "In Progress", "Review", "Done"]
    task_id = 1
    for journey_id in range(1, 19):
        for task_type, title in random.sample(task_titles, random.choice([3, 4, 5])):
            cur.execute(
                "INSERT INTO tasks VALUES (?,?,?,?,?,?,?,?,?)",
                (task_id, journey_id, random.choice([1, 2, 3]), random.choice(owners), task_type, title, random.choice(statuses_task), random.choice([1, 2, 3, 5, 8]), _dater(date.today(), random.randint(-10, 24))),
            )
            task_id += 1

    txn_id = 1
    tx_countries = ["United States", "United Kingdom", "Ireland", "Singapore", "South Africa", "UAE", "Cayman Islands", "Luxembourg"]
    for client_id in range(1, 19):
        for _ in range(random.randint(3, 8)):
            amount = round(random.uniform(5000, 850000), 2)
            country = random.choice(tx_countries)
            alert = int(amount > 600000 or country in {"UAE", "Cayman Islands"})
            cur.execute(
                "INSERT INTO transactions VALUES (?,?,?,?,?,?,?)",
                (txn_id, client_id, amount, country, random.choice(["Wire", "ACH", "Card", "Internal Transfer"]), _dater(date.today(), -random.randint(1, 90)), alert),
            )
            txn_id += 1

    integration_routes = [
        ("Dynamics CRM", "Onboarding CLM", "Client"),
        ("Salesforce", "Onboarding CLM", "Client"),
        ("Partner Portal", "Onboarding CLM", "Application"),
        ("Onboarding CLM", "Screening Service", "Party"),
        ("Document Service", "Onboarding CLM", "Document"),
        ("Onboarding CLM", "BI Warehouse", "Journey Event"),
    ]
    integration_id = 1
    for run_offset in range(12):
        for source, target, obj in integration_routes:
            processed = random.randint(45, 450)
            errors = random.randint(0, 18) if source != "Onboarding CLM" else random.randint(0, 10)
            cur.execute(
                "INSERT INTO integrations VALUES (?,?,?,?,?,?,?,?,?)",
                (integration_id, source, target, obj, _dater(date.today(), -run_offset), "Failed" if errors > 12 else "Success", processed, errors, random.randint(180, 3200)),
            )
            integration_id += 1

    requirements = [
        (1, "Reuse verified client data across product journeys", "Operations Analyst", "Given verified data exists, when a new product is requested, then approved reusable data is prefilled and its provenance is retained.", "Must", "Approved", "Product Consultant"),
        (2, "Route high-risk clients to Head of Compliance", "Compliance Officer", "When risk is High, the account setup stage cannot begin until Head of Compliance approval is recorded.", "Must", "In Review", "Compliance Lead"),
        (3, "Expose missing evidence in executive reporting", "Program Sponsor", "Dashboard shows open journeys with missing or expired evidence and supports drill-down to client and document.", "Should", "Ready", "BI Lead"),
        (4, "Prevent duplicate client creation", "KYC Analyst", "Potential duplicates are displayed before case creation using legal name, registration number, and country; authorized users can resolve the match.", "Must", "In Progress", "Integration Lead"),
        (5, "Send client confirmation after account setup", "Client Service", "After setup succeeds, a confirmation task and approved communication are created within five minutes.", "Could", "Backlog", "Client Service Lead"),
        (6, "Reconcile integration failures", "Technology Support", "Each failed message has a correlation ID, error category, retry status, owner, and final reconciliation result.", "Must", "Ready", "Integration Lead"),
    ]
    cur.executemany("INSERT INTO requirements VALUES (?,?,?,?,?,?,?)", requirements)

    conn.commit()
    conn.close()
    return DB_PATH


def get_connection(read_only: bool = False) -> sqlite3.Connection:
    init_database()
    if read_only:
        return sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True, check_same_thread=False)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def read_table(table_name: str) -> pd.DataFrame:
    allowed = {"clients", "products", "client_products", "documents", "journeys", "tasks", "transactions", "integrations", "requirements", "leads"}
    if table_name not in allowed:
        raise ValueError("Unknown table")
    with get_connection(read_only=True) as conn:
        return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)


def execute_select(query: str) -> pd.DataFrame:
    normalized = " ".join(query.strip().lower().split())
    forbidden = [" insert ", " update ", " delete ", " drop ", " alter ", " create ", " replace ", " pragma ", " attach ", " detach ", " vacuum "]
    padded = f" {normalized} "
    if not (normalized.startswith("select") or normalized.startswith("with")):
        raise ValueError("Only SELECT or read-only CTE queries are allowed in the learning lab.")
    if any(word in padded for word in forbidden):
        raise ValueError("The learning lab blocks data-changing SQL. Use SELECT statements only.")
    with get_connection(read_only=True) as conn:
        return pd.read_sql_query(query, conn)


def move_task(task_id: int, new_status: str) -> None:
    valid = {"Backlog", "Ready", "In Progress", "Review", "Done"}
    if new_status not in valid:
        raise ValueError("Invalid status")
    with get_connection() as conn:
        conn.execute("UPDATE tasks SET status = ? WHERE task_id = ?", (new_status, task_id))
        conn.commit()


def save_lead(name: str, email: str, interest: str) -> None:
    with get_connection() as conn:
        conn.execute("INSERT INTO leads(name, email, interest) VALUES (?,?,?)", (name.strip(), email.strip().lower(), interest))
        conn.commit()


def reset_demo() -> None:
    init_database(force=True)


def dashboard_data() -> dict[str, Any]:
    with get_connection(read_only=True) as conn:
        clients = pd.read_sql_query("SELECT * FROM clients", conn)
        journeys = pd.read_sql_query("SELECT * FROM journeys", conn)
        documents = pd.read_sql_query("SELECT * FROM documents", conn)
        tasks = pd.read_sql_query("SELECT * FROM tasks", conn)
        integrations = pd.read_sql_query("SELECT * FROM integrations", conn)
    merged = journeys.merge(clients[["client_id", "client_name", "region", "risk_rating", "assigned_owner"]], on="client_id", how="left")
    return {"clients": clients, "journeys": merged, "documents": documents, "tasks": tasks, "integrations": integrations}
