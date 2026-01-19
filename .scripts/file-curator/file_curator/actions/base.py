"""Base action protocol."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from ..models.file_item import FileItem
from ..models.review import ReviewRecord


class BaseAction(ABC):
    """Base class for all actions."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Get the action name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get the action description."""
        pass

    @property
    def shortcut(self) -> Optional[str]:
        """Get the keyboard shortcut."""
        return None

    @abstractmethod
    async def execute(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the action.

        Args:
            item: FileItem to act on
            context: Additional context (session_id, etc.)

        Returns:
            Result dictionary with keys like 'success', 'message', etc.
        """
        pass

    def validate(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> tuple[bool, str]:
        """Validate whether the action can be performed.

        Args:
            item: FileItem to validate
            context: Additional context

        Returns:
            Tuple of (is_valid, message)
        """
        return True, ""
