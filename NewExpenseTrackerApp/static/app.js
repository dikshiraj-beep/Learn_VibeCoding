let editingExpenseId = null;

async function loadCategories() {
    const response = await fetch('/api/categories');
    const data = await response.json();
    const select = document.getElementById('category');
    select.innerHTML = '';
    data.categories.forEach(category => {
        const option = document.createElement('option');
        option.value = category.name;
        option.textContent = category.name;
        select.appendChild(option);
    });
}

function renderChart(summary) {
    const chart = document.getElementById('category-chart');
    chart.innerHTML = '';
    const entries = Object.entries(summary.by_category || {});
    if (!entries.length) {
        chart.innerHTML = '<p class="chart-empty">No expense data yet.</p>';
        return;
    }

    const maxValue = Math.max(...entries.map(([, value]) => value), 1);
    entries.forEach(([name, value]) => {
        const row = document.createElement('div');
        row.className = 'row';

        const label = document.createElement('div');
        label.className = 'row-label';
        label.textContent = name;

        const track = document.createElement('div');
        track.className = 'track';

        const fill = document.createElement('div');
        fill.className = 'fill';
        if (value > 200) {
            fill.classList.add('over-limit');
        }
        fill.style.width = `${Math.max(8, (value / maxValue) * 100)}%`;
        fill.textContent = `${value}`;

        const overLimitLabel = document.createElement('div');
        overLimitLabel.className = 'over-limit-label';
        if (value > 200) {
            const excess = value - 200;
            overLimitLabel.textContent = `+${excess}`;
        }

        track.appendChild(fill);
        row.appendChild(label);
        row.appendChild(track);
        row.appendChild(overLimitLabel);
        chart.appendChild(row);
    });
}

async function loadDashboard() {
    const response = await fetch('/api/dashboard');
    const data = await response.json();
    const warningBanner = document.getElementById('warning-banner');
    const totalExpenses = Number(data.summary.total_expenses || 0);
    const totalEarnings = Number(data.summary.total_earnings || 0);
    const netBalance = Number(data.summary.net_balance || 0);
    document.getElementById('total-expenses').textContent = `${totalExpenses}`;
    document.getElementById('total-earnings').textContent = `${totalEarnings}`;
    document.getElementById('net-balance').textContent = `${netBalance}`;
    document.getElementById('expense-count').textContent = `${data.summary.expense_count}`;
    warningBanner.hidden = totalExpenses <= 500;
    renderChart(data.summary);

    const tbody = document.getElementById('expense-list');
    tbody.innerHTML = '';
    data.expenses.forEach(expense => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${expense.title}</td>
            <td>${expense.amount}</td>
            <td>${expense.category_name}</td>
            <td>${expense.expense_date}</td>
            <td>${expense.notes}</td>
            <td class="actions">
                <button type="button" onclick="startEdit(${expense.id}, '${expense.title}', ${expense.amount}, '${expense.category_name}', '${expense.expense_date}', '${expense.notes}')">Edit</button>
                <button type="button" class="secondary" onclick="deleteExpense(${expense.id})">Delete</button>
            </td>
        `;
        tbody.appendChild(row);
    });

    const earningsTbody = document.getElementById('earnings-list');
    earningsTbody.innerHTML = '';
    (data.earnings || []).forEach(earning => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${earning.title}</td>
            <td>${earning.amount}</td>
            <td>${earning.source}</td>
            <td>${earning.earning_date}</td>
            <td>${earning.notes}</td>
        `;
        earningsTbody.appendChild(row);
    });
}

function startEdit(id, title, amount, category, date, notes) {
    editingExpenseId = id;
    document.getElementById('title').value = title;
    document.getElementById('amount').value = amount;
    document.getElementById('category').value = category;
    document.getElementById('expense_date').value = date;
    document.getElementById('notes').value = notes;
    document.getElementById('submit-btn').textContent = 'Update Expense';
}

async function deleteExpense(id) {
    await fetch(`/api/expenses/${id}`, { method: 'DELETE' });
    await loadDashboard();
}

document.getElementById('expense-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const payload = {
        title: document.getElementById('title').value,
        amount: document.getElementById('amount').value,
        category: document.getElementById('category').value,
        expense_date: document.getElementById('expense_date').value,
        notes: document.getElementById('notes').value,
    };

    const url = editingExpenseId ? `/api/expenses/${editingExpenseId}` : '/api/expenses';
    const method = editingExpenseId ? 'PUT' : 'POST';

    await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    editingExpenseId = null;
    event.target.reset();
    document.getElementById('submit-btn').textContent = 'Add Expense';
    await loadDashboard();
});

document.getElementById('earning-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const payload = {
        title: document.getElementById('earning-title').value,
        amount: document.getElementById('earning-amount').value,
        source: document.getElementById('earning-source').value,
        earning_date: document.getElementById('earning-date').value,
        notes: document.getElementById('earning-notes').value,
    };

    await fetch('/api/earnings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });

    event.target.reset();
    await loadDashboard();
});

loadCategories();
loadDashboard();
