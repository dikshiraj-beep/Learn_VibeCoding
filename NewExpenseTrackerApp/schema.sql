CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    amount NUMERIC(10, 2) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    expense_date DATE NOT NULL,
    notes TEXT
);

INSERT INTO categories (name) VALUES
('Utilities'),
('Kids School Fees'),
('Groceries'),
('Transportation'),
('Entertainment'),
('Health'),
('Savings')
ON CONFLICT (name) DO NOTHING;

INSERT INTO expenses (title, amount, category_id, expense_date, notes)
SELECT 'Electric Bill', 85.50, c.id, '2026-07-15', 'Monthly utility bill'
FROM categories c WHERE c.name = 'Utilities';

INSERT INTO expenses (title, amount, category_id, expense_date, notes)
SELECT 'Groceries', 120.25, c.id, '2026-07-16', 'Weekly food shopping'
FROM categories c WHERE c.name = 'Groceries';

INSERT INTO expenses (title, amount, category_id, expense_date, notes)
SELECT 'School Fees', 300.00, c.id, '2026-07-17', 'Child school payment'
FROM categories c WHERE c.name = 'Kids School Fees';
