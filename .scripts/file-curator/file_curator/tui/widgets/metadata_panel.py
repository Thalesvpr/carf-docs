"""Metadata panel widget for displaying file metadata."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, DataTable
from textual.reactive import reactive

from ...models.file_item import FileItem


class MetadataPanelWidget(Vertical):
    """Widget displaying detailed file metadata."""

    DEFAULT_CSS = """
    MetadataPanelWidget {
        height: auto;
        padding: 1;
        border: round $surface;
        margin: 0 1;
    }

    MetadataPanelWidget .panel-title {
        text-style: bold;
        margin-bottom: 1;
    }

    MetadataPanelWidget .metadata-row {
        height: auto;
    }

    MetadataPanelWidget .metadata-label {
        width: 15;
        color: $text-muted;
    }

    MetadataPanelWidget .metadata-value {
        color: $text;
    }
    """

    file_item: reactive[FileItem | None] = reactive(None)

    def __init__(self, file_item: FileItem | None = None, **kwargs):
        super().__init__(**kwargs)
        self.file_item = file_item

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield Static("File Metadata", classes="panel-title")
        yield DataTable(id="metadata-table", show_header=False)

    def on_mount(self) -> None:
        """Handle mount event."""
        table = self.query_one("#metadata-table", DataTable)
        table.add_column("Field", key="field")
        table.add_column("Value", key="value")
        self._update_display()

    def watch_file_item(self, item: FileItem | None) -> None:
        """Update display when file item changes."""
        self._update_display()

    def _update_display(self) -> None:
        """Update the metadata table."""
        try:
            table = self.query_one("#metadata-table", DataTable)
            table.clear()

            if self.file_item is None:
                table.add_row("No file", "selected")
                return

            item = self.file_item

            # Add metadata rows
            rows = [
                ("Path", item.relative_path),
                ("Title", item.title or "-"),
                ("Type", item.doc_type or "Unknown"),
                ("Status", item.status.value.upper()),
                ("Words", str(item.word_count)),
                ("Reviews", str(item.review_count)),
                ("Skips", str(item.skip_count)),
                ("Modules", ", ".join(item.frontmatter_modules) or "-"),
                ("Epic", item.frontmatter_epic or "-"),
                ("Hash", item.file_hash[:12] + "..." if item.file_hash else "-"),
            ]

            if item.created_at:
                rows.append(("Created", item.created_at.strftime("%Y-%m-%d %H:%M")))

            if item.updated_at:
                rows.append(("Updated", item.updated_at.strftime("%Y-%m-%d %H:%M")))

            if item.last_reviewed_at:
                rows.append(("Reviewed", item.last_reviewed_at.strftime("%Y-%m-%d %H:%M")))

            for label, value in rows:
                table.add_row(label, value)

        except Exception:
            pass  # Widget not yet mounted

    def update_item(self, item: FileItem) -> None:
        """Update the displayed item.

        Args:
            item: FileItem to display
        """
        self.file_item = item
