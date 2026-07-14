"""Automated database-backed tests for the AMS Readiness Intake module.

Each test loads reproducible data from the seeded SQLite database (via the `conn` fixture) and
validates how the application behaves when reading/validating stored data. Test IDs map to the
traceability matrix (docs/07) and the automated-test table (docs/12).

Coverage: AT-001 happy, AT-002 negative, AT-003 boundary/validation, AT-004 role/security,
AT-005 RFC role/security (change request CR-01).
"""
from datetime import date

import readiness_rules as rules

REF = date(2026, 7, 1)  # deterministic reference date matching the seed data


# --- AT-001 — Happy path (REQ-003 / REQ-005 / REQ-006) ------------------------------------------
def test_at001_complete_assessment_is_ready(conn):
    """A complete assessment loaded from the DB is recognised as ready (100%)."""
    result = rules.readiness_result(conn, assessment_id=1, reference_date=REF)
    assert result["status"] == "ready"
    assert result["missing_critical_information"] == []
    assert result["readiness_score"] == 1.0


# --- AT-002 — Negative (REQ-003) ---------------------------------------------------------------
def test_at002_missing_critical_evidence_detected(conn):
    """An assessment with missing DR evidence is detected as not ready."""
    missing = rules.missing_critical_areas(conn, assessment_id=2, reference_date=REF)
    assert "DR" in missing
    result = rules.readiness_result(conn, assessment_id=2, reference_date=REF)
    assert result["status"] == "not ready"


# --- AT-003 — Boundary / validation (REQ-004) --------------------------------------------------
def test_at003_freshness_boundary_90_vs_91(conn):
    """Evidence exactly 90 days old is not stale; 91 days old is stale."""
    assert rules.is_stale("2026-04-02", REF) is False   # exactly 90 days
    assert rules.is_stale("2026-04-01", REF) is True     # 91 days
    # In assessment 3, DR (91 days) is stale, while access (90 days) is not.
    stale_areas = {s["area"] for s in rules.stale_critical_evidence(conn, 3, REF)}
    assert "DR" in stale_areas
    assert "access" not in stale_areas


# --- AT-004 — Role / security (REQ-005 / REQ-008) ----------------------------------------------
def test_at004_only_transition_lead_can_submit(conn):
    """A Contributor cannot submit; a Transition Lead can submit a complete assessment."""
    ok_contributor, reasons = rules.can_submit(conn, assessment_id=1, user_id=2, reference_date=REF)  # bob
    assert ok_contributor is False
    assert any("unauthorized" in r for r in reasons)

    allowed, _ = rules.submit_assessment(conn, assessment_id=1, user_id=1, reference_date=REF)  # alice (TL)
    assert allowed is True
    status = conn.execute("SELECT status FROM assessment WHERE id = 1").fetchone()["status"]
    assert status == "submitted"


# --- AT-005 — RFC role/security + persistence (CR-01: REQ-011 / REQ-008 / REQ-012) --------------
def test_at005_rfc_role_and_persistence(conn):
    """Only a Transition Lead can raise an RFC; RFC and its response persist and link."""
    import pytest
    # Contributor is denied
    with pytest.raises(PermissionError):
        rules.raise_rfc(conn, assessment_id=1, user_id=2, title="x", content="y")

    # Transition Lead raises, Contributor responds, TL marks answered
    rfc_id = rules.raise_rfc(conn, assessment_id=1, user_id=1, title="Clarify SLA", content="What is the P1 SLA?")
    rules.respond_rfc(conn, rfc_id, user_id=2, comment="P1 = 4h", is_knowledge=True)
    assert rules.mark_rfc_answered(conn, rfc_id, user_id=1) is True

    row = conn.execute(
        "SELECT r.status, COUNT(rr.id) AS n "
        "FROM rfc r LEFT JOIN rfc_response rr ON rr.rfc_id = r.id "
        "WHERE r.id = ? GROUP BY r.id", (rfc_id,),
    ).fetchone()
    assert row["status"] == "answered"
    assert row["n"] == 1
