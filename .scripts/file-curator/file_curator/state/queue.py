"""Curation queue management."""

from typing import Optional

from ..models.file_item import FileItem, FileStatus
from .database import Database
from .repository import FileRepository


class CurationQueue:
    """Manages the queue of files to be curated.

    Implements the key guarantee: skipped files return to the queue
    and are prioritized over pending files.
    """

    def __init__(self, db: Database, session_id: str):
        """Initialize the queue.

        Args:
            db: Database instance
            session_id: Session ID
        """
        self.db = db
        self.session_id = session_id
        self.file_repo = FileRepository(db)
        self._current_index = 0
        self._queue_cache: list[FileItem] = []
        self._cache_valid = False

    def refresh(self) -> None:
        """Refresh the queue from the database."""
        self._cache_valid = False
        self._queue_cache = []

    def _load_queue(self) -> list[FileItem]:
        """Load the queue from database.

        Returns:
            List of files needing review, skipped files first
        """
        if self._cache_valid:
            return self._queue_cache

        # Get skipped files first (they have priority)
        skipped = self.file_repo.list_by_session(
            self.session_id, FileStatus.SKIPPED
        )
        # Then pending files
        pending = self.file_repo.list_by_session(
            self.session_id, FileStatus.PENDING
        )

        # Combine with skipped first
        self._queue_cache = skipped + pending
        self._cache_valid = True
        return self._queue_cache

    def get_next(self) -> Optional[FileItem]:
        """Get the next file to review.

        Returns:
            Next FileItem or None if queue is empty
        """
        queue = self._load_queue()
        if not queue:
            return None
        if self._current_index >= len(queue):
            self._current_index = 0
        return queue[self._current_index] if queue else None

    def peek(self, count: int = 5) -> list[FileItem]:
        """Peek at the next files in the queue.

        Args:
            count: Number of files to peek

        Returns:
            List of upcoming files
        """
        queue = self._load_queue()
        start = self._current_index
        return queue[start : start + count]

    def advance(self) -> None:
        """Advance to the next file in the queue."""
        self._current_index += 1
        queue = self._load_queue()
        if self._current_index >= len(queue):
            self._current_index = 0

    def mark_decided(self, relative_path: str, status: FileStatus) -> None:
        """Mark a file as decided and refresh the queue.

        Args:
            relative_path: Relative path of the file
            status: New status (APPROVED, REJECTED, or SKIPPED)
        """
        self.file_repo.update_status(
            self.session_id, relative_path, status
        )
        self.refresh()

    def get_remaining_count(self) -> int:
        """Get the number of files still needing decisions.

        Returns:
            Count of pending + skipped files
        """
        queue = self._load_queue()
        return len(queue)

    def get_skipped_count(self) -> int:
        """Get the number of skipped files.

        Returns:
            Count of skipped files
        """
        queue = self._load_queue()
        return sum(1 for f in queue if f.status == FileStatus.SKIPPED)

    def get_pending_count(self) -> int:
        """Get the number of pending files.

        Returns:
            Count of pending files
        """
        queue = self._load_queue()
        return sum(1 for f in queue if f.status == FileStatus.PENDING)

    def is_complete(self) -> bool:
        """Check if all files have been decided.

        Returns:
            True if no files are pending or skipped
        """
        return self.get_remaining_count() == 0

    def get_progress(self) -> dict:
        """Get queue progress statistics.

        Returns:
            Dictionary with progress info
        """
        # Count by status
        approved = len(
            self.file_repo.list_by_session(self.session_id, FileStatus.APPROVED)
        )
        rejected = len(
            self.file_repo.list_by_session(self.session_id, FileStatus.REJECTED)
        )
        skipped = self.get_skipped_count()
        pending = self.get_pending_count()
        total = approved + rejected + skipped + pending

        return {
            "total": total,
            "approved": approved,
            "rejected": rejected,
            "skipped": skipped,
            "pending": pending,
            "decided": approved + rejected,
            "remaining": skipped + pending,
            "progress_percent": (
                ((approved + rejected) / total * 100) if total > 0 else 0
            ),
        }

    def find_by_path(self, relative_path: str) -> Optional[FileItem]:
        """Find a file in the queue by path.

        Args:
            relative_path: Relative path to find

        Returns:
            FileItem or None
        """
        return self.file_repo.get_by_path(self.session_id, relative_path)

    def jump_to(self, relative_path: str) -> bool:
        """Jump to a specific file in the queue.

        Args:
            relative_path: Relative path to jump to

        Returns:
            True if the file was found and jumped to
        """
        queue = self._load_queue()
        for i, item in enumerate(queue):
            if item.relative_path == relative_path:
                self._current_index = i
                return True
        return False
