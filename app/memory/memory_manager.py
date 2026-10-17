import re
import sqlite3
from pathlib import Path


class MemoryManager:

    MAX_KEY_LENGTH = 100
    MAX_VALUE_LENGTH = 1000

    SENSITIVE_PATTERNS = [
        r"password",
        r"passwd",
        r"passcode",
        r"\bpin\b",
        r"\botp\b",
        r"one[- _]?time[- _]?password",
        r"secret[- _]?key",
        r"api[- _]?key",
        r"access[- _]?token",
        r"authorization[- _]?token",
        r"private[- _]?key",
        r"credit[- _]?card",
        r"debit[- _]?card",
        r"\bcvv\b",
    ]

    def __init__(self):
        self.db_path = Path("workspace") / "memory.db"
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.db_path) as connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_key TEXT UNIQUE NOT NULL,
                    memory_value TEXT NOT NULL
                )
            """)

    def _contains_sensitive_data(self, text: str) -> bool:
        return any(
            re.search(pattern, text, re.IGNORECASE)
            for pattern in self.SENSITIVE_PATTERNS
        )

    def remember(self, key: str, value: str) -> bool:
        if not isinstance(key, str) or not isinstance(value, str):
            print("Memory key and value must be text.")
            return False

        key = key.strip().lower()
        value = value.strip()

        if not key or not value:
            print("Memory key and value cannot be empty.")
            return False

        if len(key) > self.MAX_KEY_LENGTH:
            print("Memory key is too long.")
            return False

        if len(value) > self.MAX_VALUE_LENGTH:
            print("Memory value is too long.")
            return False

        if (
            self._contains_sensitive_data(key)
            or self._contains_sensitive_data(value)
        ):
            print(
                "Memory blocked: sensitive information "
                "must not be stored."
            )
            return False

        try:
            with sqlite3.connect(self.db_path) as connection:
                connection.execute("""
                    INSERT INTO memories (memory_key, memory_value)
                    VALUES (?, ?)
                    ON CONFLICT(memory_key)
                    DO UPDATE SET memory_value = excluded.memory_value
                """, (key, value))

            print(f"Memory saved: {key}")
            return True

        except sqlite3.Error:
            print("Memory error: database operation failed.")
            return False

    def recall(self, key: str):
        if not isinstance(key, str):
            print("Memory key must be text.")
            return None

        key = key.strip().lower()

        if not key:
            print("Memory key cannot be empty.")
            return None

        if len(key) > self.MAX_KEY_LENGTH:
            print("Memory key is too long.")
            return None

        try:
            with sqlite3.connect(self.db_path) as connection:
                result = connection.execute("""
                    SELECT memory_value
                    FROM memories
                    WHERE memory_key = ?
                """, (key,)).fetchone()

            if result is None:
                print(f"No memory found for: {key}")
                return None

            print(f"{key}: {result[0]}")
            return result[0]

        except sqlite3.Error:
            print("Memory error: database operation failed.")
            return None

    def list_memories(self) -> list:
        """Return all saved memories as (key, value) pairs."""
        try:
            with sqlite3.connect(self.db_path) as connection:
                rows = connection.execute("""
                    SELECT memory_key, memory_value
                    FROM memories
                    ORDER BY memory_key
                """).fetchall()

            if not rows:
                print("No saved memories.")
                return []

            print("\n--- SAVED MEMORIES ---")
            for key, value in rows:
                print(f"{key}: {value}")
            print("--- END MEMORIES ---\n")

            return rows

        except sqlite3.Error:
            print("Memory error: could not list memories.")
            return []

    def forget(self, key: str) -> bool:
        """Delete one memory by its exact key."""
        if not isinstance(key, str):
            print("Memory key must be text.")
            return False

        key = key.strip().lower()

        if not key:
            print("Memory key cannot be empty.")
            return False

        if len(key) > self.MAX_KEY_LENGTH:
            print("Memory key is too long.")
            return False

        try:
            with sqlite3.connect(self.db_path) as connection:
                cursor = connection.execute("""
                    DELETE FROM memories
                    WHERE memory_key = ?
                """, (key,))

            if cursor.rowcount == 0:
                print(f"No memory found for: {key}")
                return False

            print(f"Memory deleted: {key}")
            return True

        except sqlite3.Error:
            print("Memory error: could not delete memory.")
            return False
