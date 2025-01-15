import mysql.connector

def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="skribble"
    )

def create_tables():
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS users (
                    id VARCHAR(36) PRIMARY KEY,
                    email VARCHAR(320) UNIQUE,
                    name TEXT,
                    avatar TEXT
                );
                CREATE TABLE IF NOT EXISTS notebooks (
                    user_id VARCHAR(255),
                    notebook_id VARCHAR(36) PRIMARY KEY,
                    notebook_name TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                CREATE TABLE IF NOT EXISTS notes (
                    user_id VARCHAR(255),
                    notebook_id VARCHAR(36),
                    note_id VARCHAR(36) PRIMARY KEY,
                    note_name TEXT,
                    note_content LONGTEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (notebook_id) REFERENCES notebooks(notebook_id)
                );
            """,
            multi=True
        )
        conn.commit()
        conn.close()

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
    mutate("INSERT INTO notebooks VALUES (%s, %s, %s)", (user_id, notebook_id, notebook_name))

def delete_notebook(user_id, notebook_id):
    mutate("DELETE FROM notes WHERE user_id =%s AND notebook_id =%s", (user_id, notebook_id))
    mutate("DELETE FROM notebooks WHERE user_id =%s AND notebook_id =%s", (user_id, notebook_id))

def get_notebooks(user_id):
    return query("SELECT * FROM notebooks WHERE user_id =%s", (user_id, ))

def get_notebook(user_id, notebook_id):
    return query("SELECT * FROM notebooks WHERE user_id =%s AND notebook_id =%s", (user_id, notebook_id))

def add_note(user_id, notebook_id, note_id, note_name, note_content = ""):
    mutate("INSERT INTO notes VALUES (%s, %s, %s, %s, %s)", (user_id, notebook_id, note_id, note_name, note_content))

def edit_note(user_id, notebook_id, note_id, note_content):
    mutate("UPDATE notes SET note_content =%s WHERE user_id =%s AND notebook_id =%s AND note_id =%s", (note_content, user_id, notebook_id, note_id))

def edit_note_title(user_id, notebook_id, note_id, note_title):
    mutate("UPDATE notes SET note_name =%s WHERE user_id =%s AND notebook_id =%s AND note_id =%s", (note_title, user_id, notebook_id, note_id))

def delete_note(user_id, notebook_id, note_id):
    mutate("DELETE FROM notes WHERE user_id =%s AND notebook_id =%s AND note_id =%s", (user_id, notebook_id, note_id))

def get_notes(user_id, notebook_id):
    return query("SELECT * FROM notes WHERE user_id =%s AND notebook_id =%s", (user_id, notebook_id))

def get_note(user_id, notebook_id, note_id):
    return query("SELECT * FROM notes WHERE user_id =%s AND notebook_id =%s AND note_id =%s", (user_id, notebook_id, note_id))
