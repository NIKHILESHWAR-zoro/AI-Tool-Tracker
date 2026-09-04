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
        conn.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id TEXT PRIMARY KEY,
                username TEXT,
                joined_at TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        conn.commit()


def add_subscriber(chat_id, username=None):
    """Register a chat ID as a subscriber if not already registered.
    Returns True if this was a new subscriber, False if already known."""
    with closing(sqlite3.connect(DB_PATH)) as conn:
        existing = conn.execute(
            "SELECT 1 FROM subscribers WHERE chat_id = ?", (str(chat_id),)
        ).fetchone()
        if existing:
            return False
        conn.execute(
            "INSERT INTO subscribers (chat_id, username, joined_at) VALUES (?, ?, datetime('now'))",
            (str(chat_id), username),
        )
        conn.commit()
        return True


def get_all_subscribers():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        rows = conn.execute("SELECT chat_id FROM subscribers").fetchall()
        return [r[0] for r in rows]


def get_meta(key, default=None):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        row = conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return row[0] if row else default


def set_meta(key, value):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute(
            "INSERT INTO meta (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, str(value)),
        )
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
