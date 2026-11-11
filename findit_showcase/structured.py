"""Parameter-bound read-only SQL operations over fictional tasks."""

import sqlite3

FAKE_TASKS = (
    (1, "user-001", "open", "Review test deployment"),
    (2, "user-001", "done", "Prepare release notes"),
    (3, "user-001", "open", "Check knowledge article"),
    (4, "user-002", "open", "Verify a separate report"),
)


class TaskStore:
    """An illustrative substitute for FileMaker data access.

    A real service must derive authenticated_owner from verified credentials.
    """

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.connection.row_factory = sqlite3.Row

    @classmethod
    def synthetic(cls) -> "TaskStore":
        connection = sqlite3.connect(":memory:")
        connection.execute("CREATE TABLE tasks (id INTEGER PRIMARY KEY, owner_id TEXT NOT NULL, status TEXT NOT NULL, title TEXT NOT NULL)")
        connection.executemany("INSERT INTO tasks VALUES (?, ?, ?, ?)", FAKE_TASKS)
        connection.commit()
        return cls(connection)

    def count_tasks(self, authenticated_owner: str, status: str | None = None) -> int:
        if not authenticated_owner:
            raise ValueError("An authenticated owner is required")
        if status is not None and status not in {"open", "done"}:
            raise ValueError("Unsupported status")
        if status is None:
            row = self.connection.execute("SELECT COUNT(*) AS n FROM tasks WHERE owner_id = ?", (authenticated_owner,)).fetchone()
        else:
            row = self.connection.execute("SELECT COUNT(*) AS n FROM tasks WHERE owner_id = ? AND status = ?", (authenticated_owner, status)).fetchone()
        return int(row["n"])

    def list_tasks(self, authenticated_owner: str, limit: int = 10) -> list[dict]:
        if not authenticated_owner or not isinstance(limit, int) or not 1 <= limit <= 50:
            raise ValueError("Invalid authenticated owner or limit")
        rows = self.connection.execute(
            "SELECT id, status, title FROM tasks WHERE owner_id = ? ORDER BY id LIMIT ?",
            (authenticated_owner, limit),
        ).fetchall()
        return [dict(row) for row in rows]
