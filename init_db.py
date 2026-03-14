import sqlite3

def init_kavach_db():
    conn = sqlite3.connect('kavach_local.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trusted_contacts (
            phone_number    TEXT PRIMARY KEY,
            contact_name    TEXT,
            avg_duration    REAL,
            common_hour     INTEGER,
            avg_frequency   REAL,
            known_origin    INTEGER
        )
    ''')

    # Seed with sample trusted contacts
    contacts = [
        ('9876543210', 'Mom',      120.5, 18, 7.0, 0),
        ('9123456780', 'Boss',     90.0,  10, 4.0, 0),
        ('9988776655', 'Bank',     45.0,  11, 2.0, 0),
    ]
    cursor.executemany(
        "INSERT OR REPLACE INTO trusted_contacts VALUES (?,?,?,?,?,?)",
        contacts
    )

    conn.commit()
    conn.close()
    print("✅ SQLite Database initialized with trusted contact profiles!")

if __name__ == "__main__":
    init_kavach_db()