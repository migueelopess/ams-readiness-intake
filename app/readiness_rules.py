"""Business rules for the AMS Readiness Intake module.

Pure logic over a SQLite connection, so it can be exercised by the application (app.py / main.py)
and by the automated database-backed tests (tests/). Each rule maps to a requirement:

- REQ-010 : evidence must have source, owner and freshness_date        -> evidence_is_valid / add_evidence
- REQ-004 : evidence older than 90 days is stale                       -> is_stale
- REQ-003 : identify missing critical information                      -> missing_critical_areas
- REQ-005 / REQ-008 : only a Transition Lead can submit                -> can_submit / submit_assessment
- REQ-006 : readiness result and score                                 -> readiness_score / readiness_result
- REQ-011 / REQ-008 : only a Transition Lead can raise an RFC          -> raise_rfc
- REQ-012 : respond to an RFC / capture knowledge                      -> respond_rfc
"""
from datetime import date

# Mandatory readiness areas (a complete assessment needs non-stale evidence in each).
REQUIRED_AREAS = ["monitoring", "DR", "access", "integrations", "SLA"]
MAX_AGE_DAYS = 90
DEFAULT_REFERENCE_DATE = date(2026, 7, 1)  # deterministic reference for the seed/boundary cases


def _to_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


# --- REQ-010: mandatory evidence fields ---------------------------------------------------------
def evidence_is_valid(source, owner, freshness_date) -> bool:
    """True only when the three mandatory fields are present and non-empty."""
    if not source or not str(source).strip():
        return False
    if not owner or not str(owner).strip():
        return False
    if not freshness_date or not str(freshness_date).strip():
        return False
    return True


def add_evidence(conn, assessment_id, area, source, owner, freshness_date,
                 category=None, criticality=None):
    """Insert an evidence item, rejecting it if a mandatory field is missing (REQ-010)."""
    if not evidence_is_valid(source, owner, freshness_date):
        raise ValueError("Evidence requires source, owner and freshness_date")
    cur = conn.execute(
        "INSERT INTO evidence (assessment_id, area, source, owner, freshness_date, category, criticality) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (assessment_id, area, source, owner, freshness_date, category, criticality),
    )
    conn.commit()
    return cur.lastrowid


# --- REQ-004: stale evidence (90-day rule) ------------------------------------------------------
def is_stale(freshness_date, reference_date=DEFAULT_REFERENCE_DATE, max_age_days=MAX_AGE_DAYS) -> bool:
    """True when the evidence is older than max_age_days. Exactly max_age_days is NOT stale."""
    age = (_to_date(reference_date) - _to_date(freshness_date)).days
    return age > max_age_days


# --- REQ-003: missing critical information ------------------------------------------------------
def covered_areas(conn, assessment_id, reference_date=DEFAULT_REFERENCE_DATE):
    """Areas that have at least one non-stale evidence item."""
    rows = conn.execute(
        "SELECT area, freshness_date FROM evidence WHERE assessment_id = ?",
        (assessment_id,),
    ).fetchall()
    covered = set()
    for r in rows:
        if not is_stale(r["freshness_date"], reference_date):
            covered.add(r["area"])
    return covered


def missing_critical_areas(conn, assessment_id, reference_date=DEFAULT_REFERENCE_DATE):
    """Required areas with no complete, non-stale evidence."""
    covered = covered_areas(conn, assessment_id, reference_date)
    return [area for area in REQUIRED_AREAS if area not in covered]


def stale_critical_evidence(conn, assessment_id, reference_date=DEFAULT_REFERENCE_DATE):
    """Evidence items in required areas that are stale (baseline: these block submission)."""
    rows = conn.execute(
        "SELECT id, area, freshness_date FROM evidence WHERE assessment_id = ?",
        (assessment_id,),
    ).fetchall()
    return [dict(r) for r in rows if r["area"] in REQUIRED_AREAS and is_stale(r["freshness_date"], reference_date)]


# --- helpers ------------------------------------------------------------------------------------
def get_role(conn, user_id):
    row = conn.execute("SELECT role FROM user_role WHERE id = ?", (user_id,)).fetchone()
    return row["role"] if row else None


# --- REQ-005 / REQ-008: submission (role + completeness + freshness) ----------------------------
def can_submit(conn, assessment_id, user_id, reference_date=DEFAULT_REFERENCE_DATE):
    """Return (allowed: bool, reasons: list[str]). Baseline: stale critical evidence blocks."""
    reasons = []
    if get_role(conn, user_id) != "Transition Lead":
        reasons.append("unauthorized: only a Transition Lead can submit")
    missing = missing_critical_areas(conn, assessment_id, reference_date)
    if missing:
        reasons.append("missing critical information: " + ", ".join(missing))
    stale = stale_critical_evidence(conn, assessment_id, reference_date)
    if stale:
        reasons.append("stale critical evidence in: " + ", ".join(sorted({s["area"] for s in stale})))
    return (len(reasons) == 0, reasons)


def submit_assessment(conn, assessment_id, user_id, reference_date=DEFAULT_REFERENCE_DATE):
    """Set status to 'submitted' only if allowed; otherwise leave as draft and return reasons."""
    allowed, reasons = can_submit(conn, assessment_id, user_id, reference_date)
    if allowed:
        conn.execute("UPDATE assessment SET status = 'submitted' WHERE id = ?", (assessment_id,))
        conn.commit()
    return allowed, reasons


# --- REQ-006: readiness result and score --------------------------------------------------------
def readiness_score(conn, assessment_id, reference_date=DEFAULT_REFERENCE_DATE) -> float:
    """Deterministic score = complete non-stale required areas / total required areas (0..1)."""
    covered = covered_areas(conn, assessment_id, reference_date)
    complete = sum(1 for area in REQUIRED_AREAS if area in covered)
    return round(complete / len(REQUIRED_AREAS), 2)


def readiness_result(conn, assessment_id, reference_date=DEFAULT_REFERENCE_DATE):
    """Return a dict with status, missing areas, stale evidence and score (REQ-006)."""
    missing = missing_critical_areas(conn, assessment_id, reference_date)
    stale = stale_critical_evidence(conn, assessment_id, reference_date)
    score = readiness_score(conn, assessment_id, reference_date)
    ready = not missing and not stale
    return {
        "status": "ready" if ready else "not ready",
        "missing_critical_information": missing,
        "stale_critical_evidence": [s["area"] for s in stale],
        "readiness_score": score,
    }


# --- REQ-011 / REQ-008 / REQ-012: RFC tool (change request CR-01) -------------------------------
def raise_rfc(conn, assessment_id, user_id, title, content, created_date="2026-07-01"):
    """Only a Transition Lead can raise an RFC (REQ-008/REQ-011). Returns the new RFC id."""
    if get_role(conn, user_id) != "Transition Lead":
        raise PermissionError("Only a Transition Lead can raise an RFC")
    if not title or not content:
        raise ValueError("An RFC requires a title and content")
    cur = conn.execute(
        "INSERT INTO rfc (assessment_id, title, content, raised_by, status, created_date) "
        "VALUES (?, ?, ?, ?, 'open', ?)",
        (assessment_id, title, content, user_id, created_date),
    )
    conn.commit()
    return cur.lastrowid


def respond_rfc(conn, rfc_id, user_id, comment, is_knowledge=False, created_date="2026-07-01"):
    """Add a response to an open RFC and (optionally) flag it as reusable knowledge (REQ-012)."""
    cur = conn.execute(
        "INSERT INTO rfc_response (rfc_id, author, comment, is_knowledge, created_date) "
        "VALUES (?, ?, ?, ?, ?)",
        (rfc_id, user_id, comment, 1 if is_knowledge else 0, created_date),
    )
    conn.commit()
    return cur.lastrowid


def mark_rfc_answered(conn, rfc_id, user_id):
    """A Transition Lead marks an RFC as answered when it has at least one response."""
    if get_role(conn, user_id) != "Transition Lead":
        raise PermissionError("Only a Transition Lead can close an RFC")
    n = conn.execute("SELECT COUNT(*) FROM rfc_response WHERE rfc_id = ?", (rfc_id,)).fetchone()[0]
    if n == 0:
        raise ValueError("An RFC needs at least one response before it can be answered")
    conn.execute("UPDATE rfc SET status = 'answered' WHERE id = ?", (rfc_id,))
    conn.commit()
    return True
