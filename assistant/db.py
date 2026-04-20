"""
FRIDAY AI Assistant — SQLite Database Manager
Replaces JSON files for better performance and multi-user support.
"""

import sqlite3
import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_FILE = BASE_DIR / "data" / "friday.db"
DB_FILE.parent.mkdir(exist_ok=True)

def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Memory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Notes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Settings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# --- Memory Functions ---
def add_memory(role, content):
    conn = get_connection()
    conn.execute('INSERT INTO memory (role, content) VALUES (?, ?)', (role, content))
    conn.commit()
    conn.close()

def get_history(limit=20):
    conn = get_connection()
    rows = conn.execute('SELECT role, content FROM memory ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return [{"role": r["role"], "text": r["content"]} for r in reversed(rows)]

def clear_memory():
    conn = get_connection()
    conn.execute('DELETE FROM memory')
    conn.commit()
    conn.close()

# --- Notes Functions ---
def add_note(content):
    conn = get_connection()
    conn.execute('INSERT INTO notes (content) VALUES (?)', (content,))
    conn.commit()
    conn.close()

def get_notes(limit=10):
    conn = get_connection()
    rows = conn.execute('SELECT content, timestamp FROM notes ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
    conn.close()
    return rows

# --- Settings Functions ---
def set_setting(key, value):
    conn = get_connection()
    conn.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, value))
    conn.commit()
    conn.close()

def get_setting(key, default=None):
    conn = get_connection()
    row = conn.execute('SELECT value FROM settings WHERE key = ?', (key,)).fetchone()
    conn.close()
    return row["value"] if row else default

init_db()
