import os
import sqlite3
from typing import List, Dict, Any
from urllib.parse import quote_plus

import psycopg2
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Vijaya$1")
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), "expense_tracker.db")


def build_database_url() -> str:
    return (
        f"postgresql://{quote_plus(DB_USER)}:{quote_plus(DB_PASSWORD)}@"
        f"{DB_HOST}:{DB_PORT}/{quote_plus(DB_NAME)}"
    )


DATABASE_URL = os.getenv("DATABASE_URL") or build_database_url()


def get_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn, "postgres"
    except Exception:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        return conn, "sqlite"


def get_default_categories() -> List[str]:
    return [
        "Utilities",
        "Kids School Fees",
        "Groceries",
        "Transportation",
        "Entertainment",
        "Health",
        "Savings",
        "Others",
    ]


def create_tables() -> None:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            if backend == "postgres":
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS categories (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL UNIQUE
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS expenses (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        amount NUMERIC(10, 2) NOT NULL,
                        category_id INTEGER NOT NULL REFERENCES categories(id),
                        expense_date DATE NOT NULL,
                        notes TEXT
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS earnings (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        amount NUMERIC(10, 2) NOT NULL,
                        source VARCHAR(255) NOT NULL,
                        earning_date DATE NOT NULL,
                        notes TEXT
                    )
                    """
                )
                for category_name in get_default_categories():
                    cur.execute(
                        "INSERT INTO categories (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                        (category_name,),
                    )

                cur.execute("SELECT COUNT(*) FROM expenses")
                expense_count = cur.fetchone()[0]
                if expense_count == 0:
                    for title, amount, expense_date, notes, category_name in [
                        ("Electric Bill", 85.50, "2026-07-15", "Monthly utility bill", "Utilities"),
                        ("Groceries", 120.25, "2026-07-16", "Weekly food shopping", "Groceries"),
                        ("School Fees", 300.00, "2026-07-17", "Child school payment", "Kids School Fees"),
                    ]:
                        cur.execute(
                            """
                            INSERT INTO expenses (title, amount, category_id, expense_date, notes)
                            SELECT %s, %s, c.id, %s, %s
                            FROM categories c
                            WHERE c.name = %s
                            LIMIT 1
                            """,
                            (title, amount, expense_date, notes, category_name),
                        )

                cur.execute("SELECT COUNT(*) FROM earnings")
                earning_count = cur.fetchone()[0]
                if earning_count == 0:
                    for title, amount, source, earning_date, notes in [
                        ("Salary", 2500.00, "Job", "2026-07-15", "Monthly salary"),
                        ("Freelance", 350.00, "Side work", "2026-07-16", "Client payment"),
                    ]:
                        cur.execute(
                            """
                            INSERT INTO earnings (title, amount, source, earning_date, notes)
                            VALUES (%s, %s, %s, %s, %s)
                            """,
                            (title, amount, source, earning_date, notes),
                        )
            else:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        amount REAL NOT NULL,
                        category_id INTEGER NOT NULL,
                        expense_date TEXT NOT NULL,
                        notes TEXT
                    )
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS earnings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        amount REAL NOT NULL,
                        source TEXT NOT NULL,
                        earning_date TEXT NOT NULL,
                        notes TEXT
                    )
                    """
                )
                for category_name in get_default_categories():
                    cur.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (category_name,))
                cur.execute("SELECT COUNT(*) FROM expenses")
                expense_count = cur.fetchone()[0]
                if expense_count == 0:
                    for title, amount, expense_date, notes, category_name in [
                        ("Electric Bill", 85.50, "2026-07-15", "Monthly utility bill", "Utilities"),
                        ("Groceries", 120.25, "2026-07-16", "Weekly food shopping", "Groceries"),
                        ("School Fees", 300.00, "2026-07-17", "Child school payment", "Kids School Fees"),
                    ]:
                        cur.execute(
                            """
                            INSERT INTO expenses (title, amount, category_id, expense_date, notes)
                            SELECT ?, ?, c.id, ?, ?
                            FROM categories c
                            WHERE c.name = ?
                            """,
                            (title, amount, expense_date, notes, category_name),
                        )

                cur.execute("SELECT COUNT(*) FROM earnings")
                earning_count = cur.fetchone()[0]
                if earning_count == 0:
                    for title, amount, source, earning_date, notes in [
                        ("Salary", 2500.00, "Job", "2026-07-15", "Monthly salary"),
                        ("Freelance", 350.00, "Side work", "2026-07-16", "Client payment"),
                    ]:
                        cur.execute(
                            "INSERT INTO earnings (title, amount, source, earning_date, notes) VALUES (?, ?, ?, ?, ?)",
                            (title, amount, source, earning_date, notes),
                        )
        conn.commit()
    finally:
        conn.close()


def get_categories() -> List[Dict[str, Any]]:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM categories ORDER BY name")
            return [{"id": row[0], "name": row[1]} for row in cur.fetchall()]
    finally:
        conn.close()


def add_expense(title: str, amount: float, category_name: str, expense_date: str, notes: str = "") -> Dict[str, Any]:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
            category_row = cur.fetchone()
            if not category_row:
                cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id", (category_name,))
                category_id = cur.fetchone()[0]
            else:
                category_id = category_row[0]

            if backend == "postgres":
                cur.execute(
                    """
                    INSERT INTO expenses (title, amount, category_id, expense_date, notes)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (title, amount, category_id, expense_date, notes),
                )
                expense_id = cur.fetchone()[0]
            else:
                cur.execute(
                    "INSERT INTO expenses (title, amount, category_id, expense_date, notes) VALUES (?, ?, ?, ?, ?)",
                    (title, amount, category_id, expense_date, notes),
                )
                expense_id = cur.lastrowid
        conn.commit()
        return {"id": expense_id, "message": "Expense added"}
    finally:
        conn.close()


def update_expense(expense_id: int, title: str, amount: float, category_name: str, expense_date: str, notes: str = "") -> Dict[str, Any]:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM categories WHERE name = %s", (category_name,))
            category_row = cur.fetchone()
            if not category_row:
                cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id", (category_name,))
                category_id = cur.fetchone()[0]
            else:
                category_id = category_row[0]

            if backend == "postgres":
                cur.execute(
                    """
                    UPDATE expenses
                    SET title = %s, amount = %s, category_id = %s, expense_date = %s, notes = %s
                    WHERE id = %s
                    """,
                    (title, amount, category_id, expense_date, notes, expense_id),
                )
            else:
                cur.execute(
                    "UPDATE expenses SET title = ?, amount = ?, category_id = ?, expense_date = ?, notes = ? WHERE id = ?",
                    (title, amount, category_id, expense_date, notes, expense_id),
                )
        conn.commit()
        return {"id": expense_id, "message": "Expense updated"}
    finally:
        conn.close()


def delete_expense(expense_id: int) -> Dict[str, Any]:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            if backend == "postgres":
                cur.execute("DELETE FROM expenses WHERE id = %s", (expense_id,))
            else:
                cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return {"id": expense_id, "message": "Expense deleted"}
    finally:
        conn.close()


def get_expenses() -> List[Dict[str, Any]]:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            if backend == "postgres":
                cur.execute(
                    """
                    SELECT e.id, e.title, e.amount, e.expense_date, e.notes, c.name AS category_name
                    FROM expenses e
                    JOIN categories c ON e.category_id = c.id
                    ORDER BY e.expense_date DESC, e.id DESC
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT e.id, e.title, e.amount, e.expense_date, e.notes, c.name AS category_name
                    FROM expenses e
                    JOIN categories c ON e.category_id = c.id
                    ORDER BY e.expense_date DESC, e.id DESC
                    """
                )
            rows = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "amount": float(row[2]),
                    "expense_date": row[3].strftime("%Y-%m-%d") if row[3] else "",
                    "notes": row[4] or "",
                    "category_name": row[5],
                }
                for row in rows
            ]
    finally:
        conn.close()


def get_earnings() -> List[Dict[str, Any]]:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            if backend == "postgres":
                cur.execute(
                    """
                    SELECT id, title, amount, source, earning_date, notes
                    FROM earnings
                    ORDER BY earning_date DESC, id DESC
                    """
                )
            else:
                cur.execute(
                    """
                    SELECT id, title, amount, source, earning_date, notes
                    FROM earnings
                    ORDER BY earning_date DESC, id DESC
                    """
                )
            rows = cur.fetchall()
            return [
                {
                    "id": row[0],
                    "title": row[1],
                    "amount": float(row[2]),
                    "source": row[3],
                    "earning_date": row[4].strftime("%Y-%m-%d") if row[4] else "",
                    "notes": row[5] or "",
                }
                for row in rows
            ]
    finally:
        conn.close()


def add_earning(title: str, amount: float, source: str, earning_date: str, notes: str = "") -> Dict[str, Any]:
    conn, backend = get_connection()
    try:
        with conn.cursor() as cur:
            if backend == "postgres":
                cur.execute(
                    """
                    INSERT INTO earnings (title, amount, source, earning_date, notes)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (title, amount, source, earning_date, notes),
                )
                earning_id = cur.fetchone()[0]
            else:
                cur.execute(
                    "INSERT INTO earnings (title, amount, source, earning_date, notes) VALUES (?, ?, ?, ?, ?)",
                    (title, amount, source, earning_date, notes),
                )
                earning_id = cur.lastrowid
        conn.commit()
        return {"id": earning_id, "message": "Earning added"}
    finally:
        conn.close()


def calculate_dashboard_summary(expenses: List[Dict[str, Any]], earnings: List[Dict[str, Any]] | None = None) -> Dict[str, Any]:
    total_expenses = sum(float(item.get("amount", 0)) for item in expenses)
    total_earnings = sum(float(item.get("amount", 0)) for item in (earnings or []))
    by_category: Dict[str, float] = {}
    for item in expenses:
        category = item.get("category_name", "Uncategorized")
        by_category[category] = by_category.get(category, 0.0) + float(item.get("amount", 0))

    return {
        "total_expenses": round(total_expenses, 2),
        "total_earnings": round(total_earnings, 2),
        "net_balance": round(total_earnings - total_expenses, 2),
        "expense_count": len(expenses),
        "by_category": {k: round(v, 2) for k, v in sorted(by_category.items())},
    }


def get_dashboard_data() -> Dict[str, Any]:
    expenses = get_expenses()
    earnings = get_earnings()
    return {
        "expenses": expenses,
        "earnings": earnings,
        "summary": calculate_dashboard_summary(expenses, earnings),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("index.html")


@app.route("/api/categories")
def categories_api():
    return jsonify({"categories": get_categories()})


@app.route("/api/dashboard")
def dashboard_api():
    return jsonify(get_dashboard_data())


@app.route("/api/expenses", methods=["GET", "POST"])
def expenses_api():
    if request.method == "GET":
        return jsonify(get_dashboard_data())

    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "").strip()
    amount = payload.get("amount")
    category_name = payload.get("category", "").strip()
    expense_date = payload.get("expense_date", "").strip()
    notes = payload.get("notes", "").strip()

    if not title or not amount or not category_name or not expense_date:
        return jsonify({"error": "Please fill in all fields."}), 400

    result = add_expense(title, float(amount), category_name, expense_date, notes)
    return jsonify(result)


@app.route("/api/earnings", methods=["POST"])
def earnings_api():
    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "").strip()
    amount = payload.get("amount")
    source = payload.get("source", "").strip()
    earning_date = payload.get("earning_date", "").strip()
    notes = payload.get("notes", "").strip()

    if not title or not amount or not source or not earning_date:
        return jsonify({"error": "Please fill in all fields."}), 400

    result = add_earning(title, float(amount), source, earning_date, notes)
    return jsonify(result)


@app.route("/api/expenses/<int:expense_id>", methods=["PUT", "DELETE"])
def expense_detail_api(expense_id: int):
    if request.method == "DELETE":
        return jsonify(delete_expense(expense_id))

    payload = request.get_json(silent=True) or {}
    title = payload.get("title", "").strip()
    amount = payload.get("amount")
    category_name = payload.get("category", "").strip()
    expense_date = payload.get("expense_date", "").strip()
    notes = payload.get("notes", "").strip()

    if not title or not amount or not category_name or not expense_date:
        return jsonify({"error": "Please fill in all fields."}), 400

    result = update_expense(expense_id, title, float(amount), category_name, expense_date, notes)
    return jsonify(result)


try:
    create_tables()
except Exception as exc:
    print(f"Database initialization skipped: {exc}")


if __name__ == "__main__":
    app.run(debug=True)
