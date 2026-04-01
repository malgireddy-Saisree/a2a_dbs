# dbs/sqlite_db.py

import sqlite3

# -------------------------------
# CONNECT TO DATABASE (PERSISTENT)
# -------------------------------
conn = sqlite3.connect("a2a.db", check_same_thread=False)
cursor = conn.cursor()

# -------------------------------
# CREATE TABLES
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
# INSERT SAMPLE DATA (SAFE)
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
# RUN QUERY FUNCTION (UPDATED)
# -------------------------------
def run(query):
    try:
        cursor.execute(query)

        # ✅ If SELECT → fetch data
        if query.strip().lower().startswith("select"):
            return cursor.fetchall()

        # ✅ For INSERT / UPDATE / DELETE → commit
        else:
            conn.commit()
            return "✅ Query executed successfully"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# -------------------------------
# MAIN FUNCTION (TESTING)
# -------------------------------
def main():
    print("📋 USERS TABLE:")
    print(run("SELECT * FROM users"))

    print("\n➕ INSERT NEW USER:")
    print(run("INSERT INTO users VALUES (5, 'Tulasi')"))

    print("\n📋 USERS AFTER INSERT:")
    print(run("SELECT * FROM users"))

    print("\n🗑 DELETE USER:")
    print(run("DELETE FROM users WHERE id = 5"))

    print("\n📋 FINAL USERS:")
    print(run("SELECT * FROM users"))


# -------------------------------
# RUN FILE DIRECTLY
# -------------------------------
if __name__ == "__main__":
    main()