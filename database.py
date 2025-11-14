import sqlite3

def init_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            time TEXT,
            full_name TEXT,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_user(ip, time, full_name, username):
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (ip, time, full_name, username) VALUES (?, ?, ?, ?)",
                   (ip, time, full_name, username))
    conn.commit()
    conn.close()
