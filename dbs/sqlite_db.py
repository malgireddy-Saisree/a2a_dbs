# db/sqlite_db.py

import sqlite3

conn = sqlite3.connect("a2a.db", check_same_thread=False)
cursor = conn.cursor()

# -------------------------------
# Create tables
# -------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount INTEGER
)
""")

# -------------------------------
# Insert sample data
# -------------------------------
users_data = [
    (1, "Sai"),
    (2, "John"),
    (3, "Alice"),
    (4, "Bob")
]

orders_data = [
    (1, 1, 500),
    (2, 1, 300),
    (3, 2, 700),
    (4, 3, 200),
    (5, 4, 900),
    (6, 2, 400)
]

cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?)", users_data)
cursor.executemany("INSERT OR IGNORE INTO orders VALUES (?, ?, ?)", orders_data)

conn.commit()

# -------------------------------
# Run query function
# -------------------------------
def run(query):
    cursor.execute(query)
    return cursor.fetchall()

# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("📋 USERS TABLE:")
    users = run("SELECT * FROM users")
    for row in users:
        print(row)

    print("\n📦 ORDERS TABLE:")
    orders = run("SELECT * FROM orders")
    for row in orders:
        print(row)

    print("\n💰 TOTAL ORDERS PER USER:")
    result = run("""
        SELECT user_id, SUM(amount)
        FROM orders
        GROUP BY user_id
    """)
    for row in result:
        print(row)

# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()