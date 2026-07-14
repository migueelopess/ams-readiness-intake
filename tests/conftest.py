"""Pytest configuration for the database-backed tests.

Adds the `app/` package to the import path and provides a fresh, seeded in-memory SQLite
database for each test, so tests are isolated and reproducible.
"""
import os
import sys

import pytest

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
sys.path.insert(0, APP_DIR)

import database  # noqa: E402  (import after sys.path setup)


@pytest.fixture
def conn():
    """A fresh in-memory database rebuilt from schema.sql + seed_data.sql."""
    connection = database.build_database(":memory:")
    yield connection
    connection.close()
