"""AMS Readiness Intake — Streamlit UI.

Two tabs:
1. Evidence validation slice (Option A) — enter evidence metadata (source, owner, freshness date,
   area, criticality); validate mandatory fields (REQ-010); flag stale evidence >90 days (REQ-004);
   show the readiness result: missing critical information and readiness score (REQ-003 / REQ-006).
2. RFC (Request for Comment) — added by change request CR-01. Raise an RFC (only a Transition Lead,
   REQ-008/REQ-011), respond to it (Contributor, REQ-012) and mark it answered.

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
st.title("AMS Readiness Intake")
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

tab_evidence, tab_rfc = st.tabs(["Evidence validation", "RFC (Request for Comment)"])

# ================================ TAB 1 — EVIDENCE VALIDATION ====================================
with tab_evidence:
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

# ================================ TAB 2 — RFC (CR-01) ===========================================
with tab_rfc:
    st.subheader("Request for Comment (RFC)")
    st.caption("Structured, IETF-style documentation — only a Transition Lead can raise an RFC.")

    # Acting user (to demonstrate the role rule visibly)
    users = conn.execute("SELECT id, username, role FROM user_role ORDER BY id").fetchall()
    user_labels = {f"{u['username']} ({u['role']})": u["id"] for u in users}
    acting_label = st.selectbox("Acting as", list(user_labels.keys()))
    acting_user = user_labels[acting_label]

    # Raise an RFC (REQ-011 / REQ-008)
    st.markdown("**Raise an RFC**")
    with st.form("raise_rfc"):
        rfc_title = st.text_input("Title *")
        rfc_content = st.text_area("Request / content *")
        raise_clicked = st.form_submit_button("Raise RFC")
    if raise_clicked:
        try:
            if not rfc_title or not rfc_content:
                st.error("An RFC requires a title and content.")
            else:
                new_id = rules.raise_rfc(conn, assessment_id, acting_user, rfc_title, rfc_content,
                                         created_date=REFERENCE_DATE.isoformat())
                st.success(f"RFC #{new_id} raised (status: open).")
        except PermissionError as e:
            st.error(f"Denied (REQ-008): {e}")

    # List RFCs for the assessment
    st.markdown("**RFCs for this assessment**")
    rfcs = conn.execute(
        "SELECT r.id, r.title, r.status, u.username AS raiser "
        "FROM rfc r JOIN user_role u ON u.id = r.raised_by "
        "WHERE r.assessment_id = ? ORDER BY r.id", (assessment_id,),
    ).fetchall()
    if not rfcs:
        st.info("No RFCs for this assessment yet.")
    else:
        for rfc in rfcs:
            with st.expander(f"RFC #{rfc['id']} — {rfc['title']}  [{rfc['status']}] (by {rfc['raiser']})"):
                responses = conn.execute(
                    "SELECT rr.comment, rr.is_knowledge, u.username AS author "
                    "FROM rfc_response rr JOIN user_role u ON u.id = rr.author "
                    "WHERE rr.rfc_id = ? ORDER BY rr.id", (rfc["id"],),
                ).fetchall()
                if responses:
                    for resp in responses:
                        tag = " ⭐ knowledge" if resp["is_knowledge"] else ""
                        st.write(f"- **{resp['author']}**: {resp['comment']}{tag}")
                else:
                    st.caption("No responses yet.")

                # Respond to the RFC (REQ-012)
                with st.form(f"respond_{rfc['id']}"):
                    comment = st.text_input("Add a response", key=f"c_{rfc['id']}")
                    is_knowledge = st.checkbox("Mark as reusable knowledge (FAQ)", key=f"k_{rfc['id']}")
                    resp_clicked = st.form_submit_button("Add response")
                if resp_clicked and comment:
                    rules.respond_rfc(conn, rfc["id"], acting_user, comment, is_knowledge,
                                      created_date=REFERENCE_DATE.isoformat())
                    st.success("Response added.")
                    st.rerun()

                # Mark answered (only Transition Lead)
                if rfc["status"] == "open" and st.button("Mark answered", key=f"a_{rfc['id']}"):
                    try:
                        rules.mark_rfc_answered(conn, rfc["id"], acting_user)
                        st.success("RFC marked as answered.")
                        st.rerun()
                    except (PermissionError, ValueError) as e:
                        st.error(str(e))

conn.close()
