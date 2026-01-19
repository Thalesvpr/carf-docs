"""Repository classes for database access."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from ..models.file_item import FileItem, FileStatus
from ..models.session import CurationSession, SessionConfig
from ..models.review import ReviewRecord, ReviewDecision, ReviewMetadata
from .database import Database


class SessionRepository:
    """Repository for CurationSession operations."""

    def __init__(self, db: Database):
        """Initialize the repository.

        Args:
            db: Database instance
        """
        self.db = db

    def create(self, session: CurationSession) -> CurationSession:
        """Create a new session.

        Args:
            session: Session to create

        Returns:
            Created session
        """
        self.db.execute(
            """
            INSERT INTO sessions (
                id, name, root_path, config_json, created_at, updated_at,
                completed_at, total_files, approved_count, rejected_count,
                skipped_count, pending_count
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.id,
                session.name,
                str(session.root_path),
                json.dumps(session.config.to_dict()),
                session.created_at.isoformat(),
                session.updated_at.isoformat(),
                session.completed_at.isoformat() if session.completed_at else None,
                session.total_files,
                session.approved_count,
                session.rejected_count,
                session.skipped_count,
                session.pending_count,
            ),
        )
        self.db.commit()
        return session

    def get(self, session_id: str) -> Optional[CurationSession]:
        """Get a session by ID.

        Args:
            session_id: Session ID

        Returns:
            Session or None
        """
        row = self.db.fetchone(
            "SELECT * FROM sessions WHERE id = ?", (session_id,)
        )
        if not row:
            return None
        return self._row_to_session(row)

    def get_by_name(self, name: str) -> Optional[CurationSession]:
        """Get a session by name.

        Args:
            name: Session name

        Returns:
            Session or None
        """
        row = self.db.fetchone(
            "SELECT * FROM sessions WHERE name = ?", (name,)
        )
        if not row:
            return None
        return self._row_to_session(row)

    def list_all(self) -> list[CurationSession]:
        """List all sessions.

        Returns:
            List of sessions ordered by creation date (newest first)
        """
        rows = self.db.fetchall(
            "SELECT * FROM sessions ORDER BY created_at DESC"
        )
        return [self._row_to_session(row) for row in rows]

    def update(self, session: CurationSession) -> None:
        """Update a session.

        Args:
            session: Session to update
        """
        session.updated_at = datetime.now()
        self.db.execute(
            """
            UPDATE sessions SET
                name = ?, root_path = ?, config_json = ?, updated_at = ?,
                completed_at = ?, total_files = ?, approved_count = ?,
                rejected_count = ?, skipped_count = ?, pending_count = ?
            WHERE id = ?
            """,
            (
                session.name,
                str(session.root_path),
                json.dumps(session.config.to_dict()),
                session.updated_at.isoformat(),
                session.completed_at.isoformat() if session.completed_at else None,
                session.total_files,
                session.approved_count,
                session.rejected_count,
                session.skipped_count,
                session.pending_count,
                session.id,
            ),
        )
        self.db.commit()

    def delete(self, session_id: str) -> None:
        """Delete a session and all associated data.

        Args:
            session_id: Session ID
        """
        with self.db.transaction() as cursor:
            # Delete reviews
            cursor.execute(
                "DELETE FROM reviews WHERE session_id = ?", (session_id,)
            )
            # Delete files
            cursor.execute(
                "DELETE FROM files WHERE session_id = ?", (session_id,)
            )
            # Delete actions
            cursor.execute(
                "DELETE FROM actions WHERE session_id = ?", (session_id,)
            )
            # Delete script executions
            cursor.execute(
                "DELETE FROM script_executions WHERE session_id = ?", (session_id,)
            )
            # Delete session
            cursor.execute(
                "DELETE FROM sessions WHERE id = ?", (session_id,)
            )

    def update_counts(self, session_id: str) -> None:
        """Recalculate and update session file counts.

        Args:
            session_id: Session ID
        """
        counts = self.db.fetchone(
            """
            SELECT
                COUNT(*) as total,
                SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved,
                SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) as rejected,
                SUM(CASE WHEN status = 'skipped' THEN 1 ELSE 0 END) as skipped,
                SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending
            FROM files WHERE session_id = ?
            """,
            (session_id,),
        )
        if counts:
            self.db.execute(
                """
                UPDATE sessions SET
                    total_files = ?, approved_count = ?, rejected_count = ?,
                    skipped_count = ?, pending_count = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    counts["total"],
                    counts["approved"],
                    counts["rejected"],
                    counts["skipped"],
                    counts["pending"],
                    datetime.now().isoformat(),
                    session_id,
                ),
            )
            self.db.commit()

    def _row_to_session(self, row) -> CurationSession:
        """Convert a database row to a CurationSession."""
        config_dict = json.loads(row["config_json"])
        return CurationSession(
            id=row["id"],
            name=row["name"],
            root_path=Path(row["root_path"]),
            config=SessionConfig.from_dict(config_dict),
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
            completed_at=(
                datetime.fromisoformat(row["completed_at"])
                if row["completed_at"]
                else None
            ),
            total_files=row["total_files"],
            approved_count=row["approved_count"],
            rejected_count=row["rejected_count"],
            skipped_count=row["skipped_count"],
            pending_count=row["pending_count"],
        )


class FileRepository:
    """Repository for FileItem operations."""

    def __init__(self, db: Database):
        """Initialize the repository.

        Args:
            db: Database instance
        """
        self.db = db

    def create(self, session_id: str, item: FileItem) -> int:
        """Create a new file record.

        Args:
            session_id: Session ID
            item: FileItem to create

        Returns:
            Created file ID
        """
        cursor = self.db.execute(
            """
            INSERT INTO files (
                session_id, path, relative_path, file_hash, title, doc_type,
                frontmatter_modules, frontmatter_epic, word_count, status,
                review_count, skip_count, created_at, updated_at, last_reviewed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session_id,
                str(item.path),
                item.relative_path,
                item.file_hash,
                item.title,
                item.doc_type,
                json.dumps(item.frontmatter_modules),
                item.frontmatter_epic,
                item.word_count,
                item.status.value,
                item.review_count,
                item.skip_count,
                item.created_at.isoformat(),
                item.updated_at.isoformat() if item.updated_at else None,
                item.last_reviewed_at.isoformat() if item.last_reviewed_at else None,
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def create_many(self, session_id: str, items: list[FileItem]) -> None:
        """Create multiple file records.

        Args:
            session_id: Session ID
            items: List of FileItems to create
        """
        params = [
            (
                session_id,
                str(item.path),
                item.relative_path,
                item.file_hash,
                item.title,
                item.doc_type,
                json.dumps(item.frontmatter_modules),
                item.frontmatter_epic,
                item.word_count,
                item.status.value,
                item.review_count,
                item.skip_count,
                item.created_at.isoformat(),
                item.updated_at.isoformat() if item.updated_at else None,
                item.last_reviewed_at.isoformat() if item.last_reviewed_at else None,
            )
            for item in items
        ]
        self.db.executemany(
            """
            INSERT INTO files (
                session_id, path, relative_path, file_hash, title, doc_type,
                frontmatter_modules, frontmatter_epic, word_count, status,
                review_count, skip_count, created_at, updated_at, last_reviewed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            params,
        )
        self.db.commit()

    def get(self, file_id: int) -> Optional[FileItem]:
        """Get a file by ID.

        Args:
            file_id: File ID

        Returns:
            FileItem or None
        """
        row = self.db.fetchone("SELECT * FROM files WHERE id = ?", (file_id,))
        if not row:
            return None
        return self._row_to_file_item(row)

    def get_by_path(
        self, session_id: str, relative_path: str
    ) -> Optional[FileItem]:
        """Get a file by session and relative path.

        Args:
            session_id: Session ID
            relative_path: Relative path of the file

        Returns:
            FileItem or None
        """
        row = self.db.fetchone(
            "SELECT * FROM files WHERE session_id = ? AND relative_path = ?",
            (session_id, relative_path),
        )
        if not row:
            return None
        return self._row_to_file_item(row)

    def list_by_session(
        self, session_id: str, status: Optional[FileStatus] = None
    ) -> list[FileItem]:
        """List files for a session.

        Args:
            session_id: Session ID
            status: Optional status filter

        Returns:
            List of FileItems
        """
        if status:
            rows = self.db.fetchall(
                """
                SELECT * FROM files
                WHERE session_id = ? AND status = ?
                ORDER BY relative_path
                """,
                (session_id, status.value),
            )
        else:
            rows = self.db.fetchall(
                """
                SELECT * FROM files
                WHERE session_id = ?
                ORDER BY relative_path
                """,
                (session_id,),
            )
        return [self._row_to_file_item(row) for row in rows]

    def update_status(
        self,
        session_id: str,
        relative_path: str,
        status: FileStatus,
        increment_review: bool = True,
    ) -> None:
        """Update a file's status.

        Args:
            session_id: Session ID
            relative_path: Relative path of the file
            status: New status
            increment_review: Whether to increment review count
        """
        now = datetime.now().isoformat()
        if status == FileStatus.SKIPPED:
            self.db.execute(
                """
                UPDATE files SET
                    status = ?, skip_count = skip_count + 1, updated_at = ?
                WHERE session_id = ? AND relative_path = ?
                """,
                (status.value, now, session_id, relative_path),
            )
        elif increment_review:
            self.db.execute(
                """
                UPDATE files SET
                    status = ?, review_count = review_count + 1,
                    last_reviewed_at = ?, updated_at = ?
                WHERE session_id = ? AND relative_path = ?
                """,
                (status.value, now, now, session_id, relative_path),
            )
        else:
            self.db.execute(
                """
                UPDATE files SET status = ?, updated_at = ?
                WHERE session_id = ? AND relative_path = ?
                """,
                (status.value, now, session_id, relative_path),
            )
        self.db.commit()

    def update(self, session_id: str, item: FileItem) -> None:
        """Update a file record.

        Args:
            session_id: Session ID
            item: FileItem to update
        """
        self.db.execute(
            """
            UPDATE files SET
                file_hash = ?, title = ?, doc_type = ?,
                frontmatter_modules = ?, frontmatter_epic = ?,
                word_count = ?, status = ?, review_count = ?,
                skip_count = ?, updated_at = ?, last_reviewed_at = ?
            WHERE session_id = ? AND relative_path = ?
            """,
            (
                item.file_hash,
                item.title,
                item.doc_type,
                json.dumps(item.frontmatter_modules),
                item.frontmatter_epic,
                item.word_count,
                item.status.value,
                item.review_count,
                item.skip_count,
                datetime.now().isoformat(),
                item.last_reviewed_at.isoformat() if item.last_reviewed_at else None,
                session_id,
                item.relative_path,
            ),
        )
        self.db.commit()

    def get_file_id(self, session_id: str, relative_path: str) -> Optional[int]:
        """Get the database ID for a file.

        Args:
            session_id: Session ID
            relative_path: Relative path of the file

        Returns:
            File ID or None
        """
        row = self.db.fetchone(
            "SELECT id FROM files WHERE session_id = ? AND relative_path = ?",
            (session_id, relative_path),
        )
        return row["id"] if row else None

    def _row_to_file_item(self, row) -> FileItem:
        """Convert a database row to a FileItem."""
        return FileItem(
            path=Path(row["path"]),
            relative_path=row["relative_path"],
            file_hash=row["file_hash"],
            title=row["title"],
            doc_type=row["doc_type"],
            frontmatter_modules=json.loads(row["frontmatter_modules"]),
            frontmatter_epic=row["frontmatter_epic"],
            word_count=row["word_count"],
            status=FileStatus(row["status"]),
            review_count=row["review_count"],
            skip_count=row["skip_count"],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=(
                datetime.fromisoformat(row["updated_at"])
                if row["updated_at"]
                else None
            ),
            last_reviewed_at=(
                datetime.fromisoformat(row["last_reviewed_at"])
                if row["last_reviewed_at"]
                else None
            ),
        )


class ReviewRepository:
    """Repository for ReviewRecord operations."""

    def __init__(self, db: Database):
        """Initialize the repository.

        Args:
            db: Database instance
        """
        self.db = db

    def create(self, file_id: int, review: ReviewRecord) -> int:
        """Create a new review record.

        Args:
            file_id: File ID
            review: ReviewRecord to create

        Returns:
            Created review ID
        """
        cursor = self.db.execute(
            """
            INSERT INTO reviews (
                file_id, session_id, decision, decided_at, observations,
                justification, tags, rendered_markdown, metadata_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                file_id,
                review.session_id,
                review.decision.value,
                review.decided_at.isoformat(),
                review.observations,
                review.justification,
                json.dumps(review.tags),
                review.rendered_markdown,
                json.dumps(review.metadata.to_dict()),
            ),
        )
        self.db.commit()
        return cursor.lastrowid

    def get_latest(
        self, session_id: str, relative_path: str
    ) -> Optional[ReviewRecord]:
        """Get the latest review for a file.

        Args:
            session_id: Session ID
            relative_path: Relative path of the file

        Returns:
            ReviewRecord or None
        """
        row = self.db.fetchone(
            """
            SELECT r.* FROM reviews r
            JOIN files f ON r.file_id = f.id
            WHERE r.session_id = ? AND f.relative_path = ?
            ORDER BY r.decided_at DESC
            LIMIT 1
            """,
            (session_id, relative_path),
        )
        if not row:
            return None
        return self._row_to_review(row, relative_path)

    def list_by_session(self, session_id: str) -> list[ReviewRecord]:
        """List all reviews for a session.

        Args:
            session_id: Session ID

        Returns:
            List of ReviewRecords
        """
        rows = self.db.fetchall(
            """
            SELECT r.*, f.relative_path FROM reviews r
            JOIN files f ON r.file_id = f.id
            WHERE r.session_id = ?
            ORDER BY r.decided_at DESC
            """,
            (session_id,),
        )
        return [self._row_to_review(row, row["relative_path"]) for row in rows]

    def _row_to_review(self, row, relative_path: str) -> ReviewRecord:
        """Convert a database row to a ReviewRecord."""
        return ReviewRecord(
            file_path=Path(relative_path),
            session_id=row["session_id"],
            decision=ReviewDecision(row["decision"]),
            decided_at=datetime.fromisoformat(row["decided_at"]),
            observations=row["observations"],
            justification=row["justification"],
            tags=json.loads(row["tags"]),
            rendered_markdown=row["rendered_markdown"],
            metadata=ReviewMetadata.from_dict(json.loads(row["metadata_json"])),
        )
