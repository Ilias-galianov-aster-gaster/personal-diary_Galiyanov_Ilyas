import sqlite3
from datetime import datetime

DB_NAME = 'diary.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_entry(title, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    current_date = datetime.now().strftime('%Y-%m-%d')
    cursor.execute(
        'INSERT INTO entries (title, content, created_at) VALUES (?, ?, ?)',
        (title, content, current_date)
    )
    conn.commit()
    entry_id = cursor.lastrowid
    conn.close()
    return entry_id

def get_all_entries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries ORDER BY created_at DESC, id DESC')
    entries = cursor.fetchall()
    conn.close()
    return entries

def get_entry(entry_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM entries WHERE id = ?', (entry_id,))
    entry = cursor.fetchone()
    conn.close()
    return entry

def update_entry(entry_id, title, content):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'UPDATE entries SET title = ?, content = ? WHERE id = ?',
        (title, content, entry_id)
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def delete_entry(entry_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries WHERE id = ?', (entry_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

# ---- Самостоятельные функции ----

def get_entries_count():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM entries')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def search_entries(query):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM entries WHERE title LIKE ? COLLATE NOCASE ORDER BY created_at DESC",
        (f'%{query}%',)
    )
    entries = cursor.fetchall()
    conn.close()
    return entries

def delete_all_entries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM entries')
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def get_last_week_entries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM entries WHERE created_at >= date('now', '-7 days') ORDER BY created_at DESC"
    )
    entries = cursor.fetchall()
    conn.close()
    return entries