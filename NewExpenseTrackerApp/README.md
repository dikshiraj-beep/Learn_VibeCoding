# Expense Tracker App

A polished Flask-based personal finance dashboard that lets users add expenses, track earnings, and review totals in a single view.

## Project Goal
Build a lightweight web app with:
- a backend database to store expenses and earnings
- a simple HTML/CSS interface with a modern glassy design
- JavaScript-driven dashboard updates
- a summary view for totals, net balance, and category spending

## Tech Stack
- Python for backend logic
- Flask for routes and templates
- PostgreSQL with SQLite fallback for local use
- HTML, CSS, and JavaScript for the UI

## Features
- Add new expense records
- Update existing expense records
- Delete expense records
- Add earnings entries
- View expenses and earnings in separate tables
- Show total expenses, total earnings, and net balance
- Highlight categories that exceed a spending threshold
- Group expenses by category
- Store data in a database
- Display a supermarket-themed background and polished dashboard styling

## Project Structure
```text
NewExpenseTrackerApp/
│
├── ExpenseTracker.py
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   ├── app.js
│   └── finance-real.jpg
├── tests/
│   └── test_expense_tracker.py
└── README.md
```

## Database Design
The app creates these tables:

### 1. categories
```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);
```

### 2. expenses
```sql
CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    category_id INTEGER NOT NULL,
    expense_date DATE NOT NULL,
    notes TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);
```

### 3. earnings
```sql
CREATE TABLE earnings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    source VARCHAR(255) NOT NULL,
    earning_date DATE NOT NULL,
    notes TEXT
);
```

## Backend Functions
The Python backend provides:
- `create_tables()` to initialize the database schema
- `add_expense()` and `update_expense()` for managing costs
- `delete_expense()` for removing entries
- `get_expenses()` and `get_earnings()` for loading data
- `calculate_dashboard_summary()` for totals and balance
- `get_dashboard_data()` for the API payload

## UI Features
The interface includes:
- an expense entry form
- an earnings entry form
- summary cards for total expenses, total earnings, and net balance
- a category spending chart
- expense and earnings tables
- a translucent, modern dashboard layout with a supermarket background

## Routes
- `/` and `/dashboard` for the page
- `/api/categories` for category options
- `/api/dashboard` for dashboard data
- `/api/expenses` for expense CRUD actions
- `/api/earnings` for adding income entries

## Example Flow
1. Open the app in the browser.
2. Add an expense or earnings entry.
3. Review the dashboard summary and charts.
4. Continue updating the records as needed.

## Running the App
From the project folder, run:
```bash
python ExpenseTracker.py
```

Then open the app in your browser at:
```text
http://127.0.0.1:5000/
```

## Tests
The project includes basic regression tests for default categories, dashboard totals, and SQLite fallback behavior.
