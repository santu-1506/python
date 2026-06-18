"""
Persistence layer.

Stores two things across runs:
  - the user's name
  - "learned" trigger -> response pairs (from the `learn` command)

This is deliberately a thin wrapper around sqlite3 with a small, boring
API (get/set/all/delete) so the rest of the codebase never has to know
SQL exists. If you ever want to swap this for Postgres or a flat file,
only this module changes.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "memory.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS profile (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS learned_responses (
    trigger TEXT PRIMARY KEY,
    response TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


class Memory:
    def __init__(self, db_path: Path | str = DEFAULT_DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    # ---- profile (simple key/value, e.g. user's name) ----

    def get_profile(self, key: str) -> str | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT value FROM profile WHERE key = ?", (key,)
            ).fetchone()
        return row[0] if row else None

    def set_profile(self, key: str, value: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO profile (key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
                (key, value),
            )

    # ---- learned trigger -> response pairs ----

    def add_learned_response(self, trigger: str, response: str) -> None:
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO learned_responses (trigger, response) VALUES (?, ?) "
                "ON CONFLICT(trigger) DO UPDATE SET response = excluded.response",
                (trigger.lower().strip(), response.strip()),
            )

    def all_learned_responses(self) -> dict[str, str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT trigger, response FROM learned_responses"
            ).fetchall()
        return dict(rows)

    def delete_learned_response(self, trigger: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM learned_responses WHERE trigger = ?",
                (trigger.lower().strip(),),
            )
        return cursor.rowcount > 0
