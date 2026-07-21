import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT
)
""")

conn.commit()


def add_user(user_id, username, first_name):
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (?, ?, ?)",
        (user_id, username, first_name),
    )
    conn.commit()


def total_users():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]
