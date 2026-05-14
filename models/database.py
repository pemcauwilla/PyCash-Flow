import os

from dotenv import load_dotenv
import sqlite3
from pathlib import Path

from core.observer import Subject
from core.constants import Keys

class DatabaseManager(Subject):
    def __init__(self, db_name="life_manager.db"):
        super().__init__() 
        self.db_path = Path(__file__).parent / db_name
        self._create_tables()

    def _execute_query(self, query: str, params=(), fetch_all=False, fetch_one=False, as_dict=False):
        try:
            with sqlite3.connect(self.db_path) as conn:
                if as_dict:
                    conn.row_factory = sqlite3.Row
                
                cursor = conn.cursor()
                cursor.execute(query, params)
                conn.commit()
                
                if fetch_all:
                    return [dict(row) for row in cursor.fetchall()] if as_dict else cursor.fetchall()
                if fetch_one:
                    return dict(cursor.fetchone()) if as_dict and cursor.fetchone() else cursor.fetchone()
                
                return True
        except Exception as e:
            print(f"Database Error -> Query: {query} | Error: {e}")
            return [] if fetch_all else None if fetch_one else False

    def _create_tables(self):
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                amount INTEGER NOT NULL,
                date TEXT NOT NULL,
                category TEXT NOT NULL
            )
        """)
        
        self._execute_query("""
            CREATE TABLE IF NOT EXISTS budget_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL, 
                amount_value INTEGER NOT NULL,
                description TEXT
            )
        """)

        load_dotenv()

        income_value = int(os.getenv(Keys.MONTHLY_INCOME, 0))
        total_balance = int(os.getenv(Keys.TOTAL_BALANCE, 0))

        self._execute_query("""
            INSERT OR IGNORE INTO budget_config (setting_key, amount_value, description) 
            VALUES (?, ?, ?),
                   (?, ?, ?)
        """, (Keys.MONTHLY_INCOME, income_value, "Renda Mensal Fixa",
             Keys.TOTAL_BALANCE, total_balance, "Dinheiro total atual"))
        

    def add_expense(self, expense_data: dict) -> bool:
        query = """INSERT INTO expenses (name, description, amount, date, category)
                   VALUES (:name, :description, :amount, :date, :category)"""
        
        if self._execute_query(query, expense_data):
            self.notify("ADD_NEW_EXPENSE")
            return True
        return False

    def delete_expense(self, expense_id: int):
        if self._execute_query("DELETE FROM expenses WHERE id = ?", (expense_id,)):
            self.notify("UPDATED_DATA") 

    def get_all_expenses(self, year_month: str = None) -> list:
        if year_month:
            query = "SELECT * FROM expenses WHERE strftime('%Y-%m', date) = ? ORDER BY date DESC"
            return self._execute_query(query, (year_month,), fetch_all=True, as_dict=True)
            
        return self._execute_query("SELECT * FROM expenses ORDER BY date DESC", fetch_all=True, as_dict=True)
        
    def get_expenses_by_category(self, year_month: str = None) -> dict:
        if year_month:
            query = "SELECT category, SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ? GROUP BY category"
            results = self._execute_query(query, (year_month,), fetch_all=True)
        else:
            query = "SELECT category, SUM(amount) FROM expenses GROUP BY category"
            results = self._execute_query(query, fetch_all=True)
            
        return {row[0]: row[1] for row in results} if results else {}

    def get_balance_summary(self, year_month: str = None) -> dict:
        income_row = self._execute_query(
            "SELECT amount_value FROM budget_config WHERE setting_key = ?", 
            (Keys.MONTHLY_INCOME,), 
            fetch_one=True
        )
        income_cents = income_row[0] if income_row else 0
        
        total_row = self._execute_query(
            "SELECT amount_value FROM budget_config WHERE setting_key = ?", 
            (Keys.TOTAL_BALANCE,), 
            fetch_one=True
        )
        total_cents = total_row[0] if total_row else 0

        all_expenses_row = self._execute_query("SELECT SUM(amount) FROM expenses", fetch_one=True)
        all_expenses_total = all_expenses_row[0] if all_expenses_row and all_expenses_row[0] else 0

        total_gastos_mes = 0
        if year_month:
            gastos_mes_row = self._execute_query(
                "SELECT SUM(amount) FROM expenses WHERE strftime('%Y-%m', date) = ?", 
                (year_month,), 
                fetch_one=True
            )
            total_gastos_mes = gastos_mes_row[0] if gastos_mes_row and gastos_mes_row[0] else 0
        else:
            total_gastos_mes = all_expenses_total
        
        return {
            "monthly": income_cents,
            "remaining": income_cents - total_gastos_mes,
            "total": total_cents - all_expenses_total
        }
    
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager._create_tables()