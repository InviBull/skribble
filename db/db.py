import sqlite3
import utils.error as err

def create_connection():
    try:
        return sqlite3.connect("skribble.db")
    except sqlite3.Error as e:
        err.ConnectError("Couldn't connect to Database")

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
                CREATE TABLE IF NOT EXISTS notebooks (
                    user_id TEXT,
                    notebook_id TEXT,
                    notebook_name TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                CREATE TABLE IF NOT EXISTS notes (
                    user_id TEXT,
                    notebook_id TEXT,
                    note_id TEXT,
                    note_name TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (notebook_id) REFERENCES notebooks(notebook_id)
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

def add_notebook(user_id, notebook_id, notebook_name):
    mutate("INSERT INTO notebooks VALUES (?, ?, ?)", (user_id, notebook_id, notebook_name))

def delete_notebook(user_id, notebook_id):
    mutate("DELETE FROM notebooks WHERE user_id = ? AND notebook_id = ?", (user_id, notebook_id))

def get_notebooks(user_id):
    return query("SELECT * FROM notebooks WHERE user_id = ?", (user_id))

def get_notebook(user_id, notebook_id):
    return query("SELECT * FROM notebooks WHERE user_id = ? AND notebook_id = ?", (user_id, notebook_id))

def add_note(user_id, notebook_id, note_id, note_name):
    mutate("INSERT INTO notes VALUES (?, ?, ?, ?)", (user_id, notebook_id, note_id, note_name))

def delete_notebook(user_id, notebook_id, note_id):
    mutate("DELETE FROM notes WHERE user_id = ? AND notebook_id = ? AND note_id = ?", (user_id, notebook_id, note_id))

def get_notes(user_id, notebook_id):
    return query("SELECT * FROM notes WHERE user_id = ? AND notebook_id = ?", (user_id, notebook_id))

def get_note(user_id, notebook_id, note_id):
    return query("SELECT * FROM notes WHERE user_id = ? AND notebook_id = ? AND note_id = ?", (user_id, notebook_id, note_id))
