"""Edit action for in-TUI editing."""

from typing import Any

from ..models.file_item import FileItem
from .base import BaseAction


class EditAction(BaseAction):
    """Action to edit review observations and metadata."""

    @property
    def name(self) -> str:
        return "edit"

    @property
    def description(self) -> str:
        return "Edit observations and tags"

    @property
    def shortcut(self) -> str:
        return "e"

    async def execute(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the edit action.

        This action signals that the editor screen should be opened.
        The actual editing happens in the TUI.

        Args:
            item: FileItem being edited
            context: Contains current observations, tags, etc.

        Returns:
            Result indicating editor should open
        """
        return {
            "success": True,
            "action": "open_editor",
            "current_observations": context.get("observations", ""),
            "current_justification": context.get("justification", ""),
            "current_tags": context.get("tags", []),
            "message": f"Opening editor for: {item.relative_path}",
        }

    def apply_edits(
        self,
        observations: str = "",
        justification: str = "",
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        """Apply edits from the editor.

        Args:
            observations: New observations text
            justification: New justification text
            tags: New tags list

        Returns:
            Dictionary with updated values
        """
        return {
            "observations": observations.strip(),
            "justification": justification.strip(),
            "tags": tags or [],
        }
