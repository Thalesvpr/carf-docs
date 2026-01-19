"""Template renderer for file cards and reports."""

from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from ..models.file_item import FileItem, FileStatus
from ..models.review import ReviewRecord, ReviewDecision
from ..models.session import CurationSession
from .loader import TemplateLoader


class TemplateRenderer:
    """Renders templates with file and session data."""

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

        return template.safe_substitute(
            file_title=item.title or item.filename,
            relative_path=item.relative_path,
            doc_type=item.doc_type or "Unknown",
            modules=modules,
            epic=item.frontmatter_epic or "None",
            status=item.status.value.capitalize(),
            last_update=last_update,
            word_count=str(item.word_count),
            content_preview=content_preview or "_No preview available._",
            validation_issues=validation_issues or "_No issues found._",
        )

    def render_decision_record(self, review: ReviewRecord) -> str:
        """Render a decision record.

        Args:
            review: ReviewRecord to render

        Returns:
            Rendered markdown string
        """
        template = self.loader.load("decision_record")

        # Format tags
        tags = ", ".join(f"`{tag}`" for tag in review.tags) if review.tags else "None"

        return template.safe_substitute(
            relative_path=str(review.file_path),
            decision=review.decision.value,
            decided_at=review.decided_at.isoformat(),
            file_title=review.file_path.name,
            decision_emoji=review.decision.emoji,
            decision_label=review.decision.label,
            observations=review.observations or "_No observations recorded._",
            justification=review.justification or "_No justification provided._",
            tags=tags,
        )

    def render_summary_report(
        self,
        session: CurationSession,
        decisions_by_type: str = "",
        recent_activity: str = "",
    ) -> str:
        """Render a session summary report.

        Args:
            session: CurationSession to render
            decisions_by_type: Formatted decisions by doc type
            recent_activity: Formatted recent activity list

        Returns:
            Rendered markdown string
        """
        template = self.loader.load("summary_report")

        total = session.total_files or 1  # Avoid division by zero
        approved_pct = round(session.approved_count / total * 100, 1)
        rejected_pct = round(session.rejected_count / total * 100, 1)
        remaining = session.skipped_count + session.pending_count
        remaining_pct = round(remaining / total * 100, 1)

        # Create progress bar
        decided = session.approved_count + session.rejected_count
        progress_pct = int(decided / total * 100)
        filled = progress_pct // 5
        progress_bar = f"[{'#' * filled}{'-' * (20 - filled)}] {progress_pct}%"

        return template.safe_substitute(
            session_name=session.name,
            session_id=session.id,
            root_path=str(session.root_path),
            created_at=session.created_at.strftime("%Y-%m-%d %H:%M"),
            completed_at=(
                session.completed_at.strftime("%Y-%m-%d %H:%M")
                if session.completed_at
                else "In Progress"
            ),
            total_files=str(session.total_files),
            approved_count=str(session.approved_count),
            approved_percent=str(approved_pct),
            rejected_count=str(session.rejected_count),
            rejected_percent=str(rejected_pct),
            remaining_count=str(remaining),
            remaining_percent=str(remaining_pct),
            progress_bar=progress_bar,
            decisions_by_type=decisions_by_type or "_No data available._",
            recent_activity=recent_activity or "_No recent activity._",
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
            lines.append(
                f"| `{item.relative_path}` | {item.doc_type or '-'} | "
                f"{item.status.value} | {item.word_count} |"
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
