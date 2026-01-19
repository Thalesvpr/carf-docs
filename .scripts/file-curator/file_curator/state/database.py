"""SQLite database operations."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator, Optional

from .schema import create_schema, get_schema_version, SCHEMA_VERSION


class Database:
    """SQLite database manager.

    Provides connection management, schema creation, and basic operations
    for the file curator database.
    """

    def __init__(self, db_path: Path | str):
        """Initialize the database.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        self._connection: Optional[sqlite3.Connection] = None
        self._ensure_directory()

    def _ensure_directory(self) -> None:
        """Ensure the database directory exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    @property
    def connection(self) -> sqlite3.Connection:
        """Get or create the database connection."""
        if self._connection is None:
            self._connection = sqlite3.connect(
                str(self.db_path),
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
            )
            self._connection.row_factory = sqlite3.Row
            # Enable foreign keys
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection

    def initialize(self) -> None:
        """Initialize the database schema."""
        current_version = get_schema_version(self.connection)
        if current_version < SCHEMA_VERSION:
            create_schema(self.connection)

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Cursor]:
        """Context manager for database transactions.

        Yields:
            Database cursor

        Example:
            with db.transaction() as cursor:
                cursor.execute("INSERT INTO ...")
        """
        cursor = self.connection.cursor()
        try:
            yield cursor
            self.connection.commit()
        except Exception:
            self.connection.rollback()
            raise

    def execute(
        self, sql: str, params: tuple | dict = ()
    ) -> sqlite3.Cursor:
        """Execute a SQL statement.

        Args:
            sql: SQL statement
            params: Query parameters

        Returns:
            Database cursor
        """
        return self.connection.execute(sql, params)

    def executemany(
        self, sql: str, params_list: list[tuple | dict]
    ) -> sqlite3.Cursor:
        """Execute a SQL statement with multiple parameter sets.

        Args:
            sql: SQL statement
            params_list: List of parameter sets

        Returns:
            Database cursor
        """
        return self.connection.executemany(sql, params_list)

    def fetchone(
        self, sql: str, params: tuple | dict = ()
    ) -> Optional[sqlite3.Row]:
        """Execute a query and return one row.

        Args:
            sql: SQL query
            params: Query parameters

        Returns:
            Row or None
        """
        cursor = self.execute(sql, params)
        return cursor.fetchone()

    def fetchall(
        self, sql: str, params: tuple | dict = ()
    ) -> list[sqlite3.Row]:
        """Execute a query and return all rows.

        Args:
            sql: SQL query
            params: Query parameters

        Returns:
            List of rows
        """
        cursor = self.execute(sql, params)
        return cursor.fetchall()

    def commit(self) -> None:
        """Commit the current transaction."""
        self.connection.commit()

    def rollback(self) -> None:
        """Rollback the current transaction."""
        self.connection.rollback()

    def table_exists(self, table_name: str) -> bool:
        """Check if a table exists.

        Args:
            table_name: Name of the table

        Returns:
            True if the table exists
        """
        row = self.fetchone(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        return row is not None

    def get_table_count(self, table_name: str) -> int:
        """Get the row count for a table.

        Args:
            table_name: Name of the table

        Returns:
            Number of rows
        """
        row = self.fetchone(f"SELECT COUNT(*) as count FROM {table_name}")
        return row["count"] if row else 0

    def vacuum(self) -> None:
        """Vacuum the database to reclaim space."""
        self.execute("VACUUM")

    def __enter__(self) -> "Database":
        """Context manager entry."""
        self.initialize()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.close()
