"""Main curation screen for reviewing files."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer
from textual.widgets import Static, Footer, Header
from textual.binding import Binding
from textual.reactive import reactive

from ...models.file_item import FileItem, FileStatus
from ...models.session import CurationSession
from ..widgets.file_card import FileCardWidget
from ..widgets.action_bar import CompactActionBar
from ..widgets.progress_bar import MiniProgressWidget
from ..widgets.metadata_panel import MetadataPanelWidget


class CurationScreen(Screen):
    """Main screen for the curation flow."""

    CSS = """
    CurationScreen {
        layout: grid;
        grid-size: 3 3;
        grid-columns: 1fr 2fr 1fr;
        grid-rows: 3 1fr 3;
    }

    CurationScreen #header-bar {
        column-span: 3;
        background: $surface;
        padding: 0 1;
        height: 3;
    }

    CurationScreen #session-info {
        text-style: bold;
    }

    CurationScreen #left-panel {
        row-span: 1;
        padding: 1;
        border-right: solid $surface;
    }

    CurationScreen #main-panel {
        row-span: 1;
        padding: 1;
    }

    CurationScreen #right-panel {
        row-span: 1;
        padding: 1;
        border-left: solid $surface;
    }

    CurationScreen #footer-bar {
        column-span: 3;
        dock: bottom;
        height: 3;
    }

    CurationScreen .panel-title {
        text-style: bold;
        margin-bottom: 1;
    }

    CurationScreen #queue-list {
        height: auto;
        max-height: 20;
    }

    CurationScreen .queue-item {
        padding: 0 1;
    }

    CurationScreen .queue-item-current {
        background: $primary;
    }

    CurationScreen .queue-item-skipped {
        color: $warning;
    }
    """

    BINDINGS = [
        Binding("a", "approve", "Approve", show=True),
        Binding("enter", "approve", "Approve", show=False),
        Binding("r", "reject", "Reject", show=True),
        Binding("backspace", "reject", "Reject", show=False),
        Binding("s", "skip", "Skip", show=True),
        Binding("space", "skip", "Skip", show=False),
        Binding("e", "edit", "Edit", show=True),
        Binding("v", "validate", "Validate", show=True),
        Binding("t", "sync", "Sync", show=True),
        Binding("p", "progress", "Progress", show=True),
        Binding("question_mark", "help", "Help", show=True),
        Binding("q", "quit", "Quit", show=True),
        Binding("ctrl+s", "save", "Save", show=False),
    ]

    current_item: reactive[FileItem | None] = reactive(None)
    session: reactive[CurationSession | None] = reactive(None)

    def __init__(
        self,
        session: CurationSession | None = None,
        current_item: FileItem | None = None,
        upcoming_items: list[FileItem] | None = None,
        content_preview: str = "",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.session = session
        self.current_item = current_item
        self.upcoming_items = upcoming_items or []
        self.content_preview = content_preview
        self._observations = ""
        self._justification = ""
        self._tags: list[str] = []

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        # Header
        with Horizontal(id="header-bar"):
            yield Static("", id="session-info")
            yield MiniProgressWidget(id="mini-progress")

        # Left panel - Queue
        with Vertical(id="left-panel"):
            yield Static("Queue", classes="panel-title")
            with ScrollableContainer(id="queue-list"):
                yield Static("Loading...", id="queue-content")

        # Main panel - File card
        with ScrollableContainer(id="main-panel"):
            yield FileCardWidget(id="file-card")

        # Right panel - Metadata
        with Vertical(id="right-panel"):
            yield MetadataPanelWidget(id="metadata-panel")

        # Footer
        with Horizontal(id="footer-bar"):
            yield CompactActionBar()

    def on_mount(self) -> None:
        """Handle mount event."""
        self._update_display()

    def watch_session(self, session: CurationSession | None) -> None:
        """Update when session changes."""
        self._update_header()

    def watch_current_item(self, item: FileItem | None) -> None:
        """Update when current item changes."""
        self._update_file_card()
        self._update_metadata()

    def _update_display(self) -> None:
        """Update all display elements."""
        self._update_header()
        self._update_file_card()
        self._update_queue()
        self._update_metadata()

    def _update_header(self) -> None:
        """Update header information."""
        try:
            session_info = self.query_one("#session-info", Static)
            if self.session:
                session_info.update(f"Session: {self.session.name} ({self.session.id})")
            else:
                session_info.update("No session")

            progress = self.query_one("#mini-progress", MiniProgressWidget)
            if self.session:
                decided = self.session.approved_count + self.session.rejected_count
                progress.update_progress(decided, self.session.total_files)
        except Exception:
            pass

    def _update_file_card(self) -> None:
        """Update the file card."""
        try:
            card = self.query_one("#file-card", FileCardWidget)
            if self.current_item:
                card.update_item(
                    self.current_item,
                    preview=self.content_preview,
                )
        except Exception:
            pass

    def _update_queue(self) -> None:
        """Update the queue list."""
        try:
            queue_content = self.query_one("#queue-content", Static)
            if not self.upcoming_items:
                queue_content.update("Queue is empty")
                return

            lines = []
            for i, item in enumerate(self.upcoming_items[:10]):
                prefix = "> " if i == 0 else "  "
                status_marker = "*" if item.status == FileStatus.SKIPPED else " "
                lines.append(f"{prefix}{status_marker} {item.filename}")

            if len(self.upcoming_items) > 10:
                lines.append(f"  ... and {len(self.upcoming_items) - 10} more")

            queue_content.update("\n".join(lines))
        except Exception:
            pass

    def _update_metadata(self) -> None:
        """Update the metadata panel."""
        try:
            panel = self.query_one("#metadata-panel", MetadataPanelWidget)
            if self.current_item:
                panel.update_item(self.current_item)
        except Exception:
            pass

    def update_current(
        self,
        item: FileItem,
        preview: str = "",
        upcoming: list[FileItem] | None = None,
    ) -> None:
        """Update the current item being reviewed.

        Args:
            item: Current FileItem
            preview: Content preview
            upcoming: Upcoming items in queue
        """
        self.current_item = item
        self.content_preview = preview
        if upcoming is not None:
            self.upcoming_items = upcoming
        self._observations = ""
        self._justification = ""
        self._tags = []
        self._update_display()

    def update_session_stats(self, session: CurationSession) -> None:
        """Update session statistics.

        Args:
            session: Updated session
        """
        self.session = session
        self._update_header()

    # Action handlers
    def action_approve(self) -> None:
        """Handle approve action."""
        if self.current_item:
            self.dismiss({
                "action": "approve",
                "item": self.current_item,
                "observations": self._observations,
                "tags": self._tags,
            })

    def action_reject(self) -> None:
        """Handle reject action."""
        if self.current_item:
            # Need justification for rejection - open editor
            self.dismiss({
                "action": "reject_request",
                "item": self.current_item,
            })

    def action_skip(self) -> None:
        """Handle skip action."""
        if self.current_item:
            self.dismiss({
                "action": "skip",
                "item": self.current_item,
            })

    def action_edit(self) -> None:
        """Handle edit action."""
        if self.current_item:
            self.dismiss({
                "action": "edit",
                "item": self.current_item,
                "observations": self._observations,
                "justification": self._justification,
                "tags": self._tags,
            })

    def action_validate(self) -> None:
        """Handle validate action."""
        if self.current_item:
            self.dismiss({
                "action": "validate",
                "item": self.current_item,
            })

    def action_sync(self) -> None:
        """Handle sync action."""
        if self.current_item and self.current_item.is_readme:
            self.dismiss({
                "action": "sync",
                "item": self.current_item,
            })

    def action_progress(self) -> None:
        """Show progress screen."""
        self.dismiss({"action": "progress"})

    def action_help(self) -> None:
        """Show help screen."""
        self.dismiss({"action": "help"})

    def action_quit(self) -> None:
        """Quit the application."""
        self.dismiss({"action": "quit"})

    def action_save(self) -> None:
        """Save current state."""
        self.dismiss({"action": "save"})

    def set_edit_values(
        self,
        observations: str = "",
        justification: str = "",
        tags: list[str] | None = None,
    ) -> None:
        """Set values from editor.

        Args:
            observations: Observations text
            justification: Justification text
            tags: Tags list
        """
        self._observations = observations
        self._justification = justification
        self._tags = tags or []
