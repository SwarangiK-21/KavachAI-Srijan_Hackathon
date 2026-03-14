import sqlite3

def init_kavach_db():
    conn = sqlite3.connect('kavach_local.db')
    cursor = conn.cursor()
    # Table to store trusted patterns for contacts
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trusted_contacts (
            phone_number TEXT PRIMARY KEY,
            avg_duration REAL,
            common_hour INTEGER
        )
    ''')
    # Seed it with one example (e.g., 'Mom')
    cursor.execute("INSERT OR REPLACE INTO trusted_contacts VALUES ('9876543210', 120.5, 18)")
    conn.commit()
    conn.close()
    print("✅ SQLite Database initialized!")

init_kavach_db()