import sqlite3

DB_NAME = "ledger_system.db"

def initialize_database():
    """Forces the creation of a strictly typed relational table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Customer_Name TEXT NOT NULL,
            Date TEXT NOT NULL,
            Product TEXT NOT NULL,
            Quantity REAL NOT NULL,
            Amount REAL NOT NULL,
            Status TEXT DEFAULT 'Pending Payment'
        )
    ''')
    conn.commit()
    conn.close()

def commit_records_to_db(validated_data):
    """Safely inserts human-verified data into the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for row in validated_data:
        # Failsafe to prevent garbage data from entering the database
        if "error" in row or not row.get("Customer_Name") or row.get("Customer_Name") == "ERROR":
            continue
            
        cursor.execute('''
            INSERT INTO transactions (Customer_Name, Date, Product, Quantity, Amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (row.get('Customer_Name'), row.get('Date'), row.get('Product'), row.get('Quantity', 0), row.get('Amount', 0)))
    
    conn.commit()
    conn.close()
    
