"""File card widget for displaying file information."""

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.widgets import Static, Markdown
from textual.reactive import reactive

from ...models.file_item import FileItem, FileStatus


class FileCardWidget(Container):
    """Widget displaying a file as a review card with markdown content."""

    DEFAULT_CSS = """
    FileCardWidget {
        height: auto;
        padding: 1;
        border: round $primary;
        margin: 1;
    }

    FileCardWidget .card-header {
        height: auto;
        padding: 0 1;
        background: $surface;
    }

    FileCardWidget .card-title {
        text-style: bold;
        color: $text;
    }

    FileCardWidget .card-path {
        color: $text-muted;
    }

    FileCardWidget .card-meta {
        height: auto;
        padding: 0 1;
        color: $text-muted;
    }

    FileCardWidget .card-status {
        padding: 0 1;
    }

    FileCardWidget .card-status.pending {
        background: $warning;
        color: $text;
    }

    FileCardWidget .card-status.approved {
        background: $success;
        color: $text;
    }

    FileCardWidget .card-status.rejected {
        background: $error;
        color: $text;
    }

    FileCardWidget .card-status.skipped {
        background: $primary;
        color: $text;
    }

    FileCardWidget .card-content {
        height: auto;
        padding: 1;
        margin-top: 1;
        border-top: solid $surface;
    }
    """

    file_item: reactive[FileItem | None] = reactive(None)
    content_preview: reactive[str] = reactive("")
    validation_issues: reactive[str] = reactive("")

    def __init__(
        self,
        file_item: FileItem | None = None,
        content_preview: str = "",
        validation_issues: str = "",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.file_item = file_item
        self.content_preview = content_preview
        self.validation_issues = validation_issues

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        with Vertical():
            yield Static("", id="card-header", classes="card-header")
            yield Static("", id="card-path", classes="card-path")
            yield Static("", id="card-meta", classes="card-meta")
            yield Static("", id="card-status", classes="card-status")
            yield Markdown("", id="card-content", classes="card-content")

    def watch_file_item(self, item: FileItem | None) -> None:
        """Update display when file item changes."""
        self._update_display()

    def watch_content_preview(self, preview: str) -> None:
        """Update display when preview changes."""
        self._update_display()

    def watch_validation_issues(self, issues: str) -> None:
        """Update display when issues change."""
        self._update_display()

    def _update_display(self) -> None:
        """Update all display elements."""
        if self.file_item is None:
            return

        item = self.file_item

        # Update header
        header = self.query_one("#card-header", Static)
        header.update(item.title or item.filename)

        # Update path
        path = self.query_one("#card-path", Static)
        path.update(f"`{item.relative_path}`")

        # Update meta
        meta = self.query_one("#card-meta", Static)
        modules = ", ".join(item.frontmatter_modules) if item.frontmatter_modules else "None"
        meta.update(
            f"Type: {item.doc_type or 'Unknown'} | "
            f"Modules: {modules} | "
            f"Words: {item.word_count}"
        )

        # Update status
        status = self.query_one("#card-status", Static)
        status.update(f"Status: {item.status.value.upper()}")
        status.set_classes(f"card-status {item.status.value}")

        # Update content
        content = self.query_one("#card-content", Markdown)
        markdown_content = self._build_markdown()
        content.update(markdown_content)

    def _build_markdown(self) -> str:
        """Build the markdown content for display."""
        if self.file_item is None:
            return ""

        item = self.file_item
        sections = []

        # Preview section
        if self.content_preview:
            sections.append("### Content Preview\n")
            sections.append(self.content_preview)
            sections.append("\n")

        # Validation issues
        if self.validation_issues:
            sections.append("### Validation Issues\n")
            sections.append(self.validation_issues)
        else:
            sections.append("### Validation\n")
            sections.append("_No issues found._")

        # Stats
        sections.append("\n### Statistics\n")
        sections.append(f"- Reviews: {item.review_count}")
        sections.append(f"- Skips: {item.skip_count}")

        if item.frontmatter_epic:
            sections.append(f"- Epic: {item.frontmatter_epic}")

        return "\n".join(sections)

    def update_item(
        self,
        item: FileItem,
        preview: str = "",
        issues: str = "",
    ) -> None:
        """Update the displayed item.

        Args:
            item: FileItem to display
            preview: Content preview
            issues: Validation issues
        """
        self.file_item = item
        self.content_preview = preview
        self.validation_issues = issues
