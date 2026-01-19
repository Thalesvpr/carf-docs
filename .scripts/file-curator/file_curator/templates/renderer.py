"""Template renderer for file cards and reports."""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..models.file_item import FileItem, FileStatus
from .loader import TemplateLoader


class TemplateRenderer:
    """Renders templates with file data."""

    def __init__(self, loader: Optional[TemplateLoader] = None):
        """Initialize the renderer.

        Args:
            loader: TemplateLoader instance
        """
        self.loader = loader or TemplateLoader()

    def render_review_card(
        self,
        item: FileItem,
        content_preview: str = "",
        validation_issues: str = "",
    ) -> str:
        """Render a review card for a file.

        Args:
            item: FileItem to render
            content_preview: Preview of file content
            validation_issues: Validation issues string

        Returns:
            Rendered markdown string
        """
        template = self.loader.load("review_card")

        # Format modules list
        modules = ", ".join(item.frontmatter_modules) if item.frontmatter_modules else "None"

        # Format last update
        last_update = (
            item.updated_at.strftime("%Y-%m-%d %H:%M")
            if item.updated_at
            else "Unknown"
        )

        # Use file's own status if available
        file_status = item.file_status or item.status.value.capitalize()

        return template.safe_substitute(
            file_title=item.title or item.filename,
            relative_path=item.relative_path,
            doc_type=item.doc_type or "Unknown",
            modules=modules,
            epic=item.frontmatter_epic or "None",
            status=file_status,
            last_update=last_update,
            word_count=str(item.word_count),
            content_preview=content_preview or "_No preview available._",
            validation_issues=validation_issues or "_No issues found._",
        )

    def render_custom(
        self, template_name: str, variables: dict[str, Any]
    ) -> str:
        """Render a custom template with variables.

        Args:
            template_name: Name of the template
            variables: Dictionary of template variables

        Returns:
            Rendered string
        """
        template = self.loader.load(template_name)
        # Convert all values to strings
        str_vars = {k: str(v) if v is not None else "" for k, v in variables.items()}
        return template.safe_substitute(str_vars)

    def render_file_list(self, items: list[FileItem]) -> str:
        """Render a list of files as a markdown table.

        Args:
            items: List of FileItems

        Returns:
            Markdown table string
        """
        if not items:
            return "_No files._"

        lines = [
            "| File | Type | Status | Words |",
            "|------|------|--------|-------|",
        ]

        for item in items:
            status = item.file_status or item.status.value
            lines.append(
                f"| `{item.relative_path}` | {item.doc_type or '-'} | "
                f"{status} | {item.word_count} |"
            )

        return "\n".join(lines)

    def render_status_summary(self, counts: dict) -> str:
        """Render a status summary.

        Args:
            counts: Dictionary with status counts

        Returns:
            Formatted summary string
        """
        return f"""**Progress:** {counts.get('decided', 0)}/{counts.get('total', 0)} files decided ({counts.get('progress_percent', 0):.1f}%)

- Approved: {counts.get('approved', 0)}
- Rejected: {counts.get('rejected', 0)}
- Skipped: {counts.get('skipped', 0)}
- Pending: {counts.get('pending', 0)}"""
