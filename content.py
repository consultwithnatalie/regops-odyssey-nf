"""Curriculum and scenario content for RegOps Odyssey."""

from __future__ import annotations

CURRICULUM = [
    {
        "id": "M01",
        "title": "Agile Launch Bay",
        "duration": "1–2 hours",
        "level": "Foundation",
        "mission": "Turn a vague onboarding problem into a sprint-ready backlog.",
        "skills": ["Agile delivery", "User stories", "Acceptance criteria", "ALM hygiene", "Scope control"],
        "segments": [
            ("Briefing", "Learn Scrum roles, ceremonies, Definition of Ready, Definition of Done, and how product consultants work with delivery teams."),
            ("Build", "Break an institutional account-opening request into an epic, capabilities, user stories, tasks, dependencies, and measurable acceptance criteria."),
            ("Adventure", "The Scope Storm: three stakeholders add conflicting requirements midway through the sprint. Decide what enters the sprint, backlog, or change request."),
            ("Proof", "Create a sprint board and explain the tradeoffs in a two-minute stand-up."),
        ],
        "deliverable": "A prioritized onboarding backlog with at least six user stories, acceptance criteria, owners, dependencies, and story points.",
    },
    {
        "id": "M02",
        "title": "Financial Services Expedition",
        "duration": "2–3 hours",
        "level": "Foundation",
        "mission": "Understand the people, products, controls, and outcomes inside institutional client onboarding.",
        "skills": ["Financial services processes", "Products", "Operating model", "Client lifecycle", "Control points"],
        "segments": [
            ("Briefing", "Map prospecting, client acceptance, KYC, product suitability, approvals, account opening, maintenance, periodic review, and offboarding."),
            ("Build", "Compare onboarding requirements for a natural person, private company, listed company, trust, and fund."),
            ("Adventure", "Product Passport: route one client through current account, secured lending, investment, and treasury products while identifying shared and product-specific evidence."),
            ("Proof", "Produce a lifecycle map showing teams, handoffs, systems, decision points, evidence, and business outcomes."),
        ],
        "deliverable": "A client lifecycle blueprint with product, team, evidence, risk, and decision overlays.",
    },
    {
        "id": "M03",
        "title": "KYC & AML Investigation",
        "duration": "2–3 hours",
        "level": "Core",
        "mission": "Investigate a high-risk client and design a defensible due-diligence route.",
        "skills": ["KYC", "AML", "CDD/EDD", "UBO", "PEP and sanctions", "Risk-based controls"],
        "segments": [
            ("Briefing", "Learn identity verification, ownership and control, source of funds/wealth, screening, risk scoring, periodic review, evidence and auditability."),
            ("Build", "Create a rule matrix that determines required data, documents, screenings, approvals, and review frequency by client type, product, jurisdiction, and risk."),
            ("Adventure", "The Red Flag Room: resolve a possible PEP match, a layered ownership chain, an expiring registration document, and a high-risk jurisdiction alert."),
            ("Proof", "Write a recommendation explaining what can be automated, what requires human judgment, and what must block onboarding."),
        ],
        "deliverable": "A KYC/AML decision table, evidence checklist, risk rationale, and escalation route.",
    },
    {
        "id": "M04",
        "title": "SQL Data Vault",
        "duration": "2–3 hours",
        "level": "Core",
        "mission": "Use SQL to expose onboarding delays, control gaps, and revenue blockers.",
        "skills": ["Relational databases", "SQL", "Joins", "Aggregations", "Data quality", "Reporting logic"],
        "segments": [
            ("Briefing", "Learn tables, keys, relationships, cardinality, normalization, joins, filters, CASE statements, CTEs, window functions, and data-quality checks."),
            ("Build", "Query fictional clients, products, documents, journeys, transactions, tasks, and integrations."),
            ("Adventure", "The Missing Evidence Heist: identify high-risk clients whose journeys are open, documents are missing, and SLA exposure is increasing."),
            ("Proof", "Write five reusable queries and translate each result into a business decision."),
        ],
        "deliverable": "A SQL evidence pack with query logic, output, interpretation, and recommended action.",
    },
    {
        "id": "M05",
        "title": "BI Control Tower",
        "duration": "2–3 hours",
        "level": "Core",
        "mission": "Build a leadership view of onboarding speed, quality, risk, workload, and integration health.",
        "skills": ["BI", "KPIs", "Dashboard design", "Root-cause analysis", "Executive storytelling"],
        "segments": [
            ("Briefing", "Define leading and lagging indicators, metric ownership, denominators, thresholds, targets, and drill-down paths."),
            ("Build", "Create KPI cards and visuals for cycle time, SLA breaches, high-risk population, missing documents, rework, backlog, and integration failures."),
            ("Adventure", "Signal Hunt: find the hidden cause of a regional cycle-time spike without blaming the busiest team."),
            ("Proof", "Deliver a three-minute executive readout using Situation–Complication–Resolution."),
        ],
        "deliverable": "An interactive control tower plus a one-page executive interpretation.",
    },
    {
        "id": "M06",
        "title": "Integration Bridge",
        "duration": "2–3 hours",
        "level": "Core",
        "mission": "Design and test a resilient CRM-to-CLM-to-screening-to-reporting integration.",
        "skills": ["APIs", "JSON", "Field mapping", "Error handling", "Idempotency", "Cross-system integration"],
        "segments": [
            ("Briefing", "Learn source/target mapping, API contracts, authentication concepts, event triggers, retries, correlation IDs, reconciliation, and exception queues."),
            ("Build", "Map a Dynamics-style client record into an onboarding case and downstream screening request."),
            ("Adventure", "Bridge Collapse: repair duplicate messages, missing country codes, invalid product identifiers, timeout retries, and partial updates."),
            ("Proof", "Present the integration sequence, control points, failure handling, and operational ownership."),
        ],
        "deliverable": "A field-mapping workbook, sample JSON payload, validation rules, error catalogue, and sequence diagram.",
    },
    {
        "id": "M07",
        "title": "Configuration Forge",
        "duration": "2–3 hours",
        "level": "Advanced",
        "mission": "Configure an original SaaS onboarding environment without creating tenant conflicts or brittle rules.",
        "skills": ["Platform configuration", "Rules", "Journeys", "Data models", "Tenant practices", "Release evaluation"],
        "segments": [
            ("Briefing", "Learn configuration layers, naming standards, reusable components, environment separation, dependency control, versioning, migration, and rollback."),
            ("Build", "Configure stages, tasks, documents, risk gates, approvals, statuses, and reusable rule sets for an investment account journey."),
            ("Adventure", "The Shared Tenant Maze: two consultants edit the same component. Prevent conflict, preserve work, and establish a safe promotion path."),
            ("Proof", "Complete a configuration review explaining reuse, resilience, dependencies, test coverage, and release readiness."),
        ],
        "deliverable": "A configuration design pack and tenant working agreement.",
    },
    {
        "id": "M08",
        "title": "Quality & Gap Analysis Cavern",
        "duration": "2–3 hours",
        "level": "Advanced",
        "mission": "Prove the solution survives negative tests, edge cases, and unmet requirements.",
        "skills": ["Use cases", "Negative testing", "Edge cases", "Spikes", "Gap analysis", "QA"],
        "segments": [
            ("Briefing", "Learn happy paths, alternate paths, exception paths, boundary tests, decision tables, traceability, defect severity, and fit-gap methods."),
            ("Build", "Write use cases and test scenarios for missing evidence, duplicate clients, changed ownership, sanctions alerts, and rejected approvals."),
            ("Adventure", "The Edge-Case Cavern: select a configuration, integration, process, or product workaround for six unusual scenarios."),
            ("Proof", "Document options, outcomes, risks, recommendation, and what remains for product engineering."),
        ],
        "deliverable": "A fit-gap register, test pack, defect triage, and recommendation memo.",
    },
    {
        "id": "M09",
        "title": "Product Consultant Command",
        "duration": "2–3 hours",
        "level": "Advanced",
        "mission": "Lead discovery, solution design, demonstrations, approvals, change, and knowledge transfer.",
        "skills": ["Requirements", "Functional analysis", "Solution design", "Stakeholders", "Demos", "Change management", "SME leadership"],
        "segments": [
            ("Briefing", "Learn discovery planning, questioning, requirement quality, assumptions, scope boundaries, design authority, decision logs, approvals, and feedback loops."),
            ("Build", "Turn client statements into testable requirements, configuration decisions, demo scripts, and release evidence."),
            ("Adventure", "The Council of Stakeholders: Compliance wants more controls, Operations wants speed, Sales wants flexibility, and Engineering wants fewer exceptions."),
            ("Proof", "Run a solution demonstration, manage objections, protect scope, request approval, and assign next actions."),
        ],
        "deliverable": "A consulting pack containing discovery notes, requirements, decision log, design summary, demo script, change plan, and approval record.",
    },
    {
        "id": "M10",
        "title": "Final Expedition: Rapid Client Onboarding",
        "duration": "2–3 hours",
        "level": "Capstone",
        "mission": "Design and release a complete product solution that reduces manual onboarding work and improves time to outcome.",
        "skills": ["Journey design", "Data modeling", "Rules", "Integrations", "BI", "Agile delivery", "Product consulting"],
        "segments": [
            ("Briefing", "Receive a fictional client brief for a global investment-account onboarding transformation."),
            ("Build", "Create the journey, ERD, rule matrix, integration payload, backlog, test evidence, dashboard, and demonstration."),
            ("Adventure", "Launch Day: respond to one regulatory change, one failed integration, one scope request, and one executive question before release approval."),
            ("Proof", "Present the full solution in ten minutes and defend your design choices."),
        ],
        "deliverable": "A portfolio-ready product consulting case study proving the ability to analyze, design, configure, test, demonstrate, and release an onboarding solution.",
    },
]

SCENARIO = {
    "client": "NorthStar International Bank",
    "program": "Global Investment Account Modernization",
    "problem": (
        "Institutional onboarding relies on disconnected CRM records, spreadsheets, email approvals, "
        "manual KYC evidence checks, and delayed reporting. NorthStar wants a configurable SaaS journey "
        "that reduces rekeying, exposes risk early, and gives leadership reliable operational insight."
    ),
    "outcomes": [
        "Create one auditable case record across onboarding teams.",
        "Route standard and high-risk clients through different control paths.",
        "Reuse verified client data across products while retaining product-specific requirements.",
        "Integrate CRM, screening, document, and reporting services.",
        "Measure cycle time, SLA exposure, rework, missing evidence, and integration health.",
    ],
    "stakeholders": [
        "Client Service", "Operations", "KYC", "Compliance", "Head of Compliance", "Risk",
        "Technology", "Product", "Data & Reporting", "Sales / Pre-Sales", "Client Sponsor",
    ],
}

SQL_CHALLENGES = [
    {
        "title": "High-risk backlog",
        "prompt": "Find all open high-risk journeys, ordered by the greatest SLA exposure.",
        "hint": "Join clients and journeys; filter risk_rating and status; order by days_open minus sla_days.",
        "starter": """SELECT c.client_name, c.country, c.risk_rating, j.current_stage,\n       j.days_open, j.sla_days, (j.days_open - j.sla_days) AS days_over_sla\nFROM clients c\nJOIN journeys j ON c.client_id = j.client_id\nWHERE c.risk_rating = 'High' AND j.status = 'Open'\nORDER BY days_over_sla DESC;""",
    },
    {
        "title": "Missing evidence",
        "prompt": "Identify clients with missing or expired documents and count the evidence gaps.",
        "hint": "Filter document status and group by client.",
        "starter": """SELECT c.client_name, COUNT(*) AS evidence_gaps\nFROM clients c\nJOIN documents d ON c.client_id = d.client_id\nWHERE d.status IN ('Missing', 'Expired')\nGROUP BY c.client_name\nORDER BY evidence_gaps DESC;""",
    },
    {
        "title": "Product complexity",
        "prompt": "Show clients with more than one requested product and their average journey age.",
        "hint": "Use COUNT(DISTINCT product_id), GROUP BY, and HAVING.",
        "starter": """SELECT c.client_name, COUNT(DISTINCT cp.product_id) AS products,\n       ROUND(AVG(j.days_open), 1) AS avg_days_open\nFROM clients c\nJOIN client_products cp ON c.client_id = cp.client_id\nJOIN journeys j ON c.client_id = j.client_id\nGROUP BY c.client_name\nHAVING COUNT(DISTINCT cp.product_id) > 1\nORDER BY products DESC, avg_days_open DESC;""",
    },
    {
        "title": "Integration reliability",
        "prompt": "Calculate failure rate and average latency by source-to-target route.",
        "hint": "Divide error_count by records_processed and protect against zero.",
        "starter": """SELECT source_system, target_system,\n       SUM(records_processed) AS records,\n       SUM(error_count) AS errors,\n       ROUND(100.0 * SUM(error_count) / NULLIF(SUM(records_processed), 0), 2) AS failure_rate_pct,\n       ROUND(AVG(latency_ms), 0) AS avg_latency_ms\nFROM integrations\nGROUP BY source_system, target_system\nORDER BY failure_rate_pct DESC;""",
    },
]

QUIZ = [
    {
        "question": "A requirement says, ‘The system should be fast.’ What is the strongest next step?",
        "options": [
            "Configure the fastest available workflow",
            "Ask for a measurable response-time target, transaction volume, and conditions",
            "Move the requirement to a future sprint",
            "Ask Engineering to decide",
        ],
        "answer": 1,
        "explanation": "The consultant must turn subjective wording into measurable, testable acceptance criteria.",
    },
    {
        "question": "A client becomes high risk after a PEP match. Which design is strongest?",
        "options": [
            "Automatically reject every match",
            "Ignore the match until periodic review",
            "Pause the journey, create a review task, preserve evidence, and route to authorized approval",
            "Ask the client to self-approve",
        ],
        "answer": 2,
        "explanation": "A controlled exception path preserves evidence and routes judgment to the proper authority.",
    },
    {
        "question": "Two consultants need to change the same reusable component. What tenant practice best reduces loss of work?",
        "options": [
            "Both edit it at the same time",
            "Create separate undocumented copies",
            "Assign ownership, log the change, coordinate timing, version it, and test dependencies",
            "Wait until release day",
        ],
        "answer": 2,
        "explanation": "Shared configuration needs ownership, version control, dependency awareness, and coordinated promotion.",
    },
    {
        "question": "Which KPI best exposes rework rather than only workload?",
        "options": ["Total clients", "Tasks completed", "Average number of reopened stages per journey", "Team size"],
        "answer": 2,
        "explanation": "Reopened stages reveal work that had to be repeated after an initial completion.",
    },
]

COACH_RUBRICS = {
    "Requirements": {
        "keywords": ["actor", "need", "because", "acceptance", "measurable", "assumption", "scope", "dependency"],
        "task": "Rewrite the requirement as a user story with three measurable acceptance criteria and one explicit assumption.",
    },
    "Solution Design": {
        "keywords": ["journey", "data", "rule", "integration", "control", "exception", "audit", "reuse"],
        "task": "Explain the proposed journey, data, rule, and integration design, including one exception path and one reusable component.",
    },
    "Demo Presentation": {
        "keywords": ["outcome", "problem", "show", "evidence", "decision", "risk", "next step", "approval"],
        "task": "Deliver a two-minute demo opening: business problem, desired outcome, what you will show, and the approval or feedback needed.",
    },
    "Stakeholder Management": {
        "keywords": ["expectation", "priority", "tradeoff", "decision", "owner", "timeline", "impact", "change"],
        "task": "Respond to a stakeholder asking for new scope during the sprint. Protect delivery while preserving the relationship.",
    },
    "KYC/AML Rationale": {
        "keywords": ["identity", "ownership", "screening", "risk", "evidence", "escalation", "review", "monitoring"],
        "task": "Explain why a client was routed to enhanced due diligence and what evidence is required before approval.",
    },
}

PRICING = [
    {
        "name": "Explorer",
        "price": "$0",
        "audience": "Lead-generation experience",
        "includes": ["Two starter missions", "BI dashboard preview", "Sample SQL lab", "Career pathway assessment"],
        "cta": "Start free",
    },
    {
        "name": "Career Pass",
        "price": "$29 one-time",
        "audience": "Independent learners",
        "includes": ["All ten missions", "Templates", "SQL and BI labs", "Completion record", "Portfolio capstone"],
        "cta": "Unlock the path",
    },
    {
        "name": "Consultant Lab",
        "price": "$79 one-time",
        "audience": "Job seekers and consultants",
        "includes": ["Career Pass", "Demo scripts", "Interview simulations", "AI coaching prompts", "Portfolio review rubric"],
        "cta": "Build consultant proof",
    },
    {
        "name": "Guided Cohort",
        "price": "$199",
        "audience": "Learners wanting live feedback",
        "includes": ["Consultant Lab", "Live group sessions", "Capstone critique", "Mock client presentation", "Career positioning"],
        "cta": "Join a cohort",
    },
]

GLOSSARY = {
    "CLM": "Client Lifecycle Management: coordinated management of onboarding, due diligence, maintenance, reviews, and offboarding.",
    "KYC": "Know Your Customer: identity, ownership, purpose, risk, and evidence processes used to understand a client.",
    "AML": "Anti-Money Laundering: controls designed to detect, assess, and respond to financial-crime risk.",
    "CDD": "Customer Due Diligence: standard measures used to identify and assess a client.",
    "EDD": "Enhanced Due Diligence: additional investigation and approval for higher-risk relationships.",
    "UBO": "Ultimate Beneficial Owner: the natural person who ultimately owns or controls an entity.",
    "ALM": "Application Lifecycle Management: planning, tracking, developing, testing, releasing, and maintaining software changes.",
    "Spike": "A time-boxed investigation used to reduce uncertainty before committing to a solution.",
    "Fit-gap": "An assessment of where standard platform capability meets a requirement and where a change or workaround is needed.",
    "Tenant": "An isolated SaaS environment containing configuration, data, users, and settings for an organization or project.",
}
