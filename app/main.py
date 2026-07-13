"""AMS Readiness Intake — command-line demonstration flow.

A quick, dependency-free way to see the business rules run against the seeded SQLite database
(useful when Streamlit is not installed). Shows the readiness result for each seeded assessment,
a role-controlled submission, and the RFC rule.

Run:  python app/main.py
"""
import database
import readiness_rules as rules

REF = rules.DEFAULT_REFERENCE_DATE


def main():
    conn = database.build_database()  # fresh, reproducible
    print(f"AMS Readiness Intake — reference date {REF.isoformat()}\n")

    for a in conn.execute("SELECT id, name FROM assessment ORDER BY id"):
        res = rules.readiness_result(conn, a["id"], REF)
        print(f"Assessment {a['id']} — {a['name']}")
        print(f"  status: {res['status']}  score: {res['readiness_score']*100:.0f}%")
        if res["missing_critical_information"]:
            print("  missing:", ", ".join(res["missing_critical_information"]))
        if res["stale_critical_evidence"]:
            print("  stale:", ", ".join(res["stale_critical_evidence"]))
        print()

    # Role-controlled submission (REQ-005 / REQ-008)
    print("Submission attempts on assessment 1 (complete):")
    ok_c, reasons_c = rules.submit_assessment(conn, 1, user_id=2, reference_date=REF)  # Bob = Contributor
    print(f"  Contributor (bob): allowed={ok_c} reasons={reasons_c}")
    ok_t, reasons_t = rules.submit_assessment(conn, 1, user_id=1, reference_date=REF)  # Alice = Transition Lead
    print(f"  Transition Lead (alice): allowed={ok_t} reasons={reasons_t}")

    # RFC rule (CR-01)
    print("\nRFC (CR-01):")
    try:
        rules.raise_rfc(conn, 1, user_id=2, title="x", content="y")  # Contributor -> denied
    except PermissionError as e:
        print(f"  Contributor raising RFC -> denied: {e}")
    rfc_id = rules.raise_rfc(conn, 1, user_id=1, title="Clarify SLA", content="What is the P1 SLA?")
    print(f"  Transition Lead raised RFC id={rfc_id}")

    conn.close()


if __name__ == "__main__":
    main()
