import os
import sqlite3
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import ExpenseTracker as tracker


def test_default_categories_include_common_options():
    categories = tracker.get_default_categories()
    assert "Utilities" in categories
    assert "Kids School Fees" in categories
    assert "Groceries" in categories
    assert "Others" in categories


def test_dashboard_summary_totals_expenses():
    expenses = [
        {"amount": "10.50"},
        {"amount": "20.00"},
        {"amount": "5.25"},
    ]

    summary = tracker.calculate_dashboard_summary(expenses)
    assert summary["total_expenses"] == 35.75
    assert summary["expense_count"] == 3


def test_dashboard_summary_includes_earnings():
    expenses = [{"amount": "10.50"}]
    earnings = [{"amount": "50.00"}]

    summary = tracker.calculate_dashboard_summary(expenses, earnings)
    assert summary["total_earnings"] == 50.0
    assert summary["net_balance"] == 39.5


def test_get_connection_falls_back_to_sqlite(monkeypatch):
    def raise_error(*args, **kwargs):
        raise RuntimeError("postgres unavailable")

    monkeypatch.setattr(tracker.psycopg2, "connect", raise_error)
    conn, backend = tracker.get_connection()

    assert backend == "sqlite"
    assert isinstance(conn, sqlite3.Connection)
    conn.close()
