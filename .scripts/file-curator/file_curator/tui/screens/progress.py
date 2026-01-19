"""Progress dashboard screen."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Button, DataTable, ProgressBar
from textual.binding import Binding

from ...models.session import CurationSession
from ...models.file_item import FileItem, FileStatus


class ProgressScreen(Screen):
    """Screen showing curation progress and statistics."""

    CSS = """
    ProgressScreen {
        align: center middle;
    }

    ProgressScreen #progress-container {
        width: 90%;
        height: 90%;
        padding: 2;
        border: round $primary;
        background: $surface;
    }

    ProgressScreen .title {
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
    }

    ProgressScreen .section-title {
        text-style: bold;
        margin: 1 0;
    }

    ProgressScreen #stats-row {
        height: auto;
        margin: 1 0;
    }

    ProgressScreen .stat-box {
        width: 1fr;
        height: auto;
        padding: 1;
        margin: 0 1;
        border: solid $surface;
        text-align: center;
    }

    ProgressScreen .stat-box.approved {
        border: solid $success;
    }

    ProgressScreen .stat-box.rejected {
        border: solid $error;
    }

    ProgressScreen .stat-box.skipped {
        border: solid $warning;
    }

    ProgressScreen .stat-box.pending {
        border: solid $text-muted;
    }

    ProgressScreen .stat-number {
        text-style: bold;
        text-align: center;
    }

    ProgressScreen .stat-label {
        color: $text-muted;
        text-align: center;
    }

    ProgressScreen #progress-bar-container {
        height: auto;
        margin: 2 0;
    }

    ProgressScreen #files-table {
        height: 1fr;
        margin: 1 0;
    }

    ProgressScreen .button-row {
        height: auto;
        align: center middle;
        margin-top: 1;
    }

    ProgressScreen Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("enter", "close", "Close"),
        Binding("e", "export", "Export"),
    ]

    def __init__(
        self,
        session: CurationSession,
        files: list[FileItem] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.session = session
        self.files = files or []

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with Container(id="progress-container"):
            yield Static(
                f"Progress: {self.session.name}",
                classes="title",
            )

            # Stats row
            with Horizontal(id="stats-row"):
                with Vertical(classes="stat-box approved"):
                    yield Static(
                        str(self.session.approved_count),
                        classes="stat-number",
                    )
                    yield Static("Approved", classes="stat-label")

                with Vertical(classes="stat-box rejected"):
                    yield Static(
                        str(self.session.rejected_count),
                        classes="stat-number",
                    )
                    yield Static("Rejected", classes="stat-label")

                with Vertical(classes="stat-box skipped"):
                    yield Static(
                        str(self.session.skipped_count),
                        classes="stat-number",
                    )
                    yield Static("Skipped", classes="stat-label")

                with Vertical(classes="stat-box pending"):
                    yield Static(
                        str(self.session.pending_count),
                        classes="stat-number",
                    )
                    yield Static("Pending", classes="stat-label")

            # Progress bar
            with Vertical(id="progress-bar-container"):
                decided = self.session.approved_count + self.session.rejected_count
                total = self.session.total_files or 1
                progress = decided / total * 100

                yield Static(
                    f"Overall Progress: {decided}/{total} ({progress:.1f}%)",
                    classes="section-title",
                )
                yield ProgressBar(total=100, show_eta=False, id="main-progress")

            # Files table
            yield Static("Files by Status:", classes="section-title")
            yield DataTable(id="files-table")

            with Horizontal(classes="button-row"):
                yield Button("Close [Enter]", id="btn-close", variant="primary")
                yield Button("Export [E]", id="btn-export", variant="default")

    def on_mount(self) -> None:
        """Handle mount event."""
        # Set progress bar
        progress_bar = self.query_one("#main-progress", ProgressBar)
        decided = self.session.approved_count + self.session.rejected_count
        total = self.session.total_files or 1
        progress_bar.update(progress=decided / total * 100)

        # Populate files table
        table = self.query_one("#files-table", DataTable)
        table.add_column("File", key="file")
        table.add_column("Type", key="type")
        table.add_column("Status", key="status")
        table.add_column("Reviews", key="reviews")

        for item in self.files[:100]:  # Limit to first 100
            table.add_row(
                item.relative_path[:50] + ("..." if len(item.relative_path) > 50 else ""),
                item.doc_type or "-",
                item.status.value,
                str(item.review_count),
            )

        if len(self.files) > 100:
            table.add_row(
                f"... and {len(self.files) - 100} more files",
                "",
                "",
                "",
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-close":
            self.action_close()
        elif event.button.id == "btn-export":
            self.action_export()

    def action_close(self) -> None:
        """Close the screen."""
        self.dismiss({"action": "close"})

    def action_export(self) -> None:
        """Export progress report."""
        self.dismiss({"action": "export"})
