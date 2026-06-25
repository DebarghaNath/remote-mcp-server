import sqlite3
import os
import json
from fastmcp import FastMCP

# File Paths
DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP(name="ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '', 
                note TEXT DEFAULT ''
            )      
        """)
init_db()

@mcp.tool()
def add_expense(date: str, amount: float, category: str, subcategory: str = "", note: str = "") -> dict:
    """
    Adds a new financial expense to the local SQLite database tracker.
    
    Args:
        date: The date of the transaction in YYYY-MM-DD format.
        amount: The monetary value of the expense (must be a number).
        category: The main budget category (e.g., 'Food', 'Utilities', 'Entertainment').
        subcategory: Optional. A more specific classification (e.g., 'Groceries', 'Restaurant').
        note: Optional. Any extra context or description about the purchase.
    """
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
    return {"status": "ok", "id": cur.lastrowid}

@mcp.tool()
def list_expense(start_date: str, end_date: str) -> list[dict]:
    """
    Retrieves the complete history of all recorded expenses from the database between two dates.
    Dates must be in YYYY-MM-DD format.
    """
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC", 
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date: str, end_date: str, category: str = None) -> list[dict]:
    """
    Summarizes the total expenses grouped by category between a start_date and end_date (YYYY-MM-DD).
    Optional: Pass a specific category name to filter by.
    """
    with sqlite3.connect(DB_PATH) as c:
        query = """
                SELECT category, SUM(amount) AS total_amount
                FROM expenses
                WHERE date BETWEEN ? AND ?
                """
        params = [start_date, end_date]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " GROUP BY category ORDER BY category ASC"
        
        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.resource("expense://categories", mime_type="application/json")
def categories() -> str:
    """Returns the list of valid categories from the local configurations file."""
    if not os.path.exists(CATEGORIES_PATH):
        return '["Food", "Utilities", "Entertainment", "Housing", "Transportation"]'
        
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    
if __name__ == "__main__":
    print("🚀 Launching Remote Expense Tracker Server on port 8000...")
    mcp.run(transport="sse", host="0.0.0.0", port=8000)