"""Review actions: Approve, Reject, Skip."""

from datetime import datetime
from typing import Any

from ..models.file_item import FileItem, FileStatus
from ..models.review import ReviewRecord, ReviewDecision, ReviewMetadata
from .base import BaseAction


class ApproveAction(BaseAction):
    """Action to approve a file."""

    @property
    def name(self) -> str:
        return "approve"

    @property
    def description(self) -> str:
        return "Approve this file"

    @property
    def shortcut(self) -> str:
        return "a"

    async def execute(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the approve action.

        Args:
            item: FileItem to approve
            context: Must contain 'session_id', optionally 'observations', 'tags'

        Returns:
            Result with 'success', 'review', 'new_status'
        """
        session_id = context.get("session_id", "")
        observations = context.get("observations", "")
        tags = context.get("tags", [])

        review = ReviewRecord(
            file_path=item.path,
            session_id=session_id,
            decision=ReviewDecision.APPROVED,
            decided_at=datetime.now(),
            observations=observations,
            tags=tags,
            metadata=ReviewMetadata(session_id=session_id),
        )

        return {
            "success": True,
            "review": review,
            "new_status": FileStatus.APPROVED,
            "message": f"Approved: {item.relative_path}",
        }


class RejectAction(BaseAction):
    """Action to reject a file."""

    def __init__(self, require_justification: bool = True):
        """Initialize the action.

        Args:
            require_justification: Whether justification is required
        """
        self.require_justification = require_justification

    @property
    def name(self) -> str:
        return "reject"

    @property
    def description(self) -> str:
        return "Reject this file"

    @property
    def shortcut(self) -> str:
        return "r"

    def validate(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> tuple[bool, str]:
        """Validate the rejection.

        Args:
            item: FileItem to validate
            context: Must contain 'justification' if required

        Returns:
            Tuple of (is_valid, message)
        """
        if self.require_justification:
            justification = context.get("justification", "").strip()
            if not justification:
                return False, "Justification is required for rejection"
        return True, ""

    async def execute(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the reject action.

        Args:
            item: FileItem to reject
            context: Must contain 'session_id', 'justification', optionally 'observations', 'tags'

        Returns:
            Result with 'success', 'review', 'new_status'
        """
        # Validate first
        is_valid, message = self.validate(item, context)
        if not is_valid:
            return {
                "success": False,
                "message": message,
            }

        session_id = context.get("session_id", "")
        justification = context.get("justification", "")
        observations = context.get("observations", "")
        tags = context.get("tags", [])

        review = ReviewRecord(
            file_path=item.path,
            session_id=session_id,
            decision=ReviewDecision.REJECTED,
            decided_at=datetime.now(),
            observations=observations,
            justification=justification,
            tags=tags,
            metadata=ReviewMetadata(session_id=session_id),
        )

        return {
            "success": True,
            "review": review,
            "new_status": FileStatus.REJECTED,
            "message": f"Rejected: {item.relative_path}",
        }


class SkipAction(BaseAction):
    """Action to skip a file (returns to queue)."""

    @property
    def name(self) -> str:
        return "skip"

    @property
    def description(self) -> str:
        return "Skip this file (will return to queue)"

    @property
    def shortcut(self) -> str:
        return "s"

    async def execute(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the skip action.

        Args:
            item: FileItem to skip
            context: Must contain 'session_id'

        Returns:
            Result with 'success', 'review', 'new_status'
        """
        session_id = context.get("session_id", "")

        review = ReviewRecord(
            file_path=item.path,
            session_id=session_id,
            decision=ReviewDecision.SKIPPED,
            decided_at=datetime.now(),
            metadata=ReviewMetadata(session_id=session_id),
        )

        return {
            "success": True,
            "review": review,
            "new_status": FileStatus.SKIPPED,
            "message": f"Skipped: {item.relative_path} (will return to queue)",
        }
