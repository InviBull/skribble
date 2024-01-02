import sqlite3

def create_connection():
    return sqlite3.connect("skribble.db")

def create_tables():
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.executescript(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE,
                    name TEXT,
                    avatar TEXT
                );
            """
        )

def query(query, params=()):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

def mutate(query, params=()):
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(query, params)
        cur.fetchall()
        conn.commit()
