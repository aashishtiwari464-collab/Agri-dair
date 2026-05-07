import sqlite3

DB_NAME = "ledger_system.db"

def initialize_database():
    """Creates the table if it does not exist. This is your schema enforcement."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Notice the strict data typing. This prevents garbage data from entering your system.
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
    """Takes the human-approved list of dictionaries and inserts them."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    for row in validated_data:
        # Skip empty rows or errors
        if "error" in row or not row.get("Customer_Name"):
            continue
            
        cursor.execute('''
            INSERT INTO transactions (Customer_Name, Date, Product, Quantity, Amount)
            VALUES (?, ?, ?, ?, ?)
        ''', (row['Customer_Name'], row['Date'], row['Product'], row['Quantity'], row['Amount']))
    
    conn.commit()
    conn.close()
  
