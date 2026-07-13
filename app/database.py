"""SQLite access and reproducible setup for the AMS Readiness Intake module.

The database is always rebuilt from `schema.sql` + `seed_data.sql`, so the test data is
reproducible. Tests can use an in-memory database via `build_database(":memory:")`.
"""
import os
import sqlite3

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(APP_DIR, "schema.sql")
SEED_PATH = os.path.join(APP_DIR, "seed_data.sql")
DEFAULT_DB_PATH = os.path.join(APP_DIR, "readiness.db")


def _run_sql_file(conn: sqlite3.Connection, path: str) -> None:
    with open(path, "r", encoding="utf-8") as fh:
        conn.executescript(fh.read())


def build_database(db_path: str = DEFAULT_DB_PATH, seed: bool = True) -> sqlite3.Connection:
    """Create a fresh database from schema (+ seed) and return an open connection.

    Passing db_path=":memory:" gives an isolated in-memory database (used by the tests).
    A file database is recreated from scratch so every run is reproducible.
    """
    if db_path != ":memory:" and os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    _run_sql_file(conn, SCHEMA_PATH)
    if seed:
        _run_sql_file(conn, SEED_PATH)
    conn.commit()
    return conn


def reset_database(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    """Reset the file database back to the seeded baseline."""
    return build_database(db_path, seed=True)


if __name__ == "__main__":
    conn = build_database()
    n_users = conn.execute("SELECT COUNT(*) FROM user_role").fetchone()[0]
    n_assess = conn.execute("SELECT COUNT(*) FROM assessment").fetchone()[0]
    n_evi = conn.execute("SELECT COUNT(*) FROM evidence").fetchone()[0]
    print(f"Database built at {DEFAULT_DB_PATH}: {n_users} users, {n_assess} assessments, {n_evi} evidence items.")
