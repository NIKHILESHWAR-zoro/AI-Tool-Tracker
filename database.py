import sqlite3
from contextlib import closing

DB_PATH = "tools.db"


def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tools (
                id TEXT PRIMARY KEY,
                title TEXT,
                url TEXT,
                hn_link TEXT,
                summary TEXT,
                category TEXT,
                points INTEGER,
                created_at TEXT
            )
        """)
        conn.commit()


def is_new(tool_id):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        row = conn.execute("SELECT 1 FROM tools WHERE id = ?", (tool_id,)).fetchone()
        return row is None


def save_tool(tool):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("""
            INSERT OR IGNORE INTO tools (id, title, url, hn_link, summary, category, points, created_at)
            VALUES (:id, :title, :url, :hn_link, :summary, :category, :points, :created_at)
        """, tool)
        conn.commit()


def get_all_tools(limit=200):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM tools ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]
