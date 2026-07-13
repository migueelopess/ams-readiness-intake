"""AMS Readiness Intake — Evidence validation slice (Option A).

Streamlit UI. A user enters evidence metadata (source, owner, freshness date, area, criticality).
The app validates the mandatory fields (REQ-010), flags stale evidence older than 90 days
(REQ-004), and shows the readiness result: missing critical information and a readiness score
(REQ-003 / REQ-006).

Run:  streamlit run app/app.py
"""
import os
import sqlite3
from datetime import date

import streamlit as st

import database
import readiness_rules as rules

REFERENCE_DATE = rules.DEFAULT_REFERENCE_DATE  # 2026-07-01, matches the seed data


def get_conn():
    if not os.path.exists(database.DEFAULT_DB_PATH):
        database.build_database()
    conn = sqlite3.connect(database.DEFAULT_DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


st.set_page_config(page_title="AMS Readiness Intake", page_icon="✅")
st.title("AMS Readiness Intake — Evidence Validation")
st.caption(f"Reference date for freshness (90-day rule): {REFERENCE_DATE.isoformat()}")

conn = get_conn()

# --- Sidebar: choose assessment, reset -----------------------------------------------------------
with st.sidebar:
    st.header("Assessment")
    assessments = conn.execute("SELECT id, name, status FROM assessment ORDER BY id").fetchall()
    labels = {f"{a['id']} — {a['name']} ({a['status']})": a["id"] for a in assessments}
    chosen = st.selectbox("Select assessment", list(labels.keys()))
    assessment_id = labels[chosen]
    if st.button("Reset test database"):
        database.reset_database()
        st.success("Database reset to the seeded baseline.")
        st.rerun()

# --- Section 1: add evidence (3+ inputs, 2+ validation rules) ------------------------------------
st.subheader("1. Add evidence")
with st.form("add_evidence"):
    area = st.selectbox("Area", rules.REQUIRED_AREAS)
    source = st.text_input("Source *")
    owner = st.text_input("Owner *")
    freshness_date = st.date_input("Freshness date *", value=date(2026, 6, 15))
    criticality = st.selectbox("Criticality", ["high", "medium", "low"])
    submitted = st.form_submit_button("Add evidence")

if submitted:
    # Validation rule 1 (REQ-010): mandatory fields
    if not rules.evidence_is_valid(source, owner, freshness_date.isoformat()):
        st.error("Rejected: source, owner and freshness date are mandatory (REQ-010).")
    else:
        rules.add_evidence(conn, assessment_id, area, source, owner,
                           freshness_date.isoformat(), category=area, criticality=criticality)
        # Validation rule 2 (REQ-004): freshness / stale
        if rules.is_stale(freshness_date.isoformat(), REFERENCE_DATE):
            st.warning(f"Evidence added, but flagged STALE (older than {rules.MAX_AGE_DAYS} days).")
        else:
            st.success("Evidence added and is current.")

# --- Evidence list -------------------------------------------------------------------------------
st.subheader("2. Evidence for this assessment")
rows = conn.execute(
    "SELECT area, source, owner, freshness_date FROM evidence WHERE assessment_id = ? ORDER BY area",
    (assessment_id,),
).fetchall()
if rows:
    st.table([
        {
            "area": r["area"],
            "source": r["source"],
            "owner": r["owner"],
            "freshness_date": r["freshness_date"],
            "stale": "yes" if rules.is_stale(r["freshness_date"], REFERENCE_DATE) else "no",
        }
        for r in rows
    ])
else:
    st.info("No evidence yet.")

# --- Section 3: readiness result (output area) ---------------------------------------------------
st.subheader("3. Readiness result")
result = rules.readiness_result(conn, assessment_id, REFERENCE_DATE)
col1, col2 = st.columns(2)
col1.metric("Status", result["status"])
col2.metric("Readiness score", f"{result['readiness_score'] * 100:.0f}%")
if result["missing_critical_information"]:
    st.error("Missing critical information: " + ", ".join(result["missing_critical_information"]))
if result["stale_critical_evidence"]:
    st.warning("Stale critical evidence in: " + ", ".join(result["stale_critical_evidence"]))
if result["status"] == "ready":
    st.success("All critical areas are covered with current evidence.")

conn.close()
