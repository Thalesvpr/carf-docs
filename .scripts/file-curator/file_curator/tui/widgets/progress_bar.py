"""Progress bar widget for curation progress."""

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static, ProgressBar, Label
from textual.reactive import reactive


class ProgressBarWidget(Vertical):
    """Widget displaying curation progress."""

    DEFAULT_CSS = """
    ProgressBarWidget {
        height: auto;
        padding: 1;
        border: round $surface;
        margin: 0 1;
    }

    ProgressBarWidget .progress-label {
        text-style: bold;
        margin-bottom: 1;
    }

    ProgressBarWidget .progress-stats {
        height: auto;
        margin-top: 1;
    }

    ProgressBarWidget .stat-approved {
        color: $success;
    }

    ProgressBarWidget .stat-rejected {
        color: $error;
    }

    ProgressBarWidget .stat-skipped {
        color: $warning;
    }

    ProgressBarWidget .stat-pending {
        color: $text-muted;
    }
    """

    total: reactive[int] = reactive(0)
    approved: reactive[int] = reactive(0)
    rejected: reactive[int] = reactive(0)
    skipped: reactive[int] = reactive(0)
    pending: reactive[int] = reactive(0)

    def __init__(
        self,
        total: int = 0,
        approved: int = 0,
        rejected: int = 0,
        skipped: int = 0,
        pending: int = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.total = total
        self.approved = approved
        self.rejected = rejected
        self.skipped = skipped
        self.pending = pending

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield Static("Progress", classes="progress-label")
        yield ProgressBar(total=100, show_eta=False, id="main-progress")
        with Horizontal(classes="progress-stats"):
            yield Static("", id="stat-decided", classes="stat-decided")
            yield Static(" | ", classes="stat-separator")
            yield Static("", id="stat-approved", classes="stat-approved")
            yield Static(" | ", classes="stat-separator")
            yield Static("", id="stat-rejected", classes="stat-rejected")
            yield Static(" | ", classes="stat-separator")
            yield Static("", id="stat-skipped", classes="stat-skipped")
            yield Static(" | ", classes="stat-separator")
            yield Static("", id="stat-pending", classes="stat-pending")

    def on_mount(self) -> None:
        """Handle mount event."""
        self._update_display()

    def watch_total(self, value: int) -> None:
        """Watch total changes."""
        self._update_display()

    def watch_approved(self, value: int) -> None:
        """Watch approved changes."""
        self._update_display()

    def watch_rejected(self, value: int) -> None:
        """Watch rejected changes."""
        self._update_display()

    def watch_skipped(self, value: int) -> None:
        """Watch skipped changes."""
        self._update_display()

    def watch_pending(self, value: int) -> None:
        """Watch pending changes."""
        self._update_display()

    def _update_display(self) -> None:
        """Update all display elements."""
        try:
            # Calculate progress
            decided = self.approved + self.rejected
            progress = (decided / self.total * 100) if self.total > 0 else 0

            # Update progress bar
            progress_bar = self.query_one("#main-progress", ProgressBar)
            progress_bar.update(progress=progress)

            # Update stats
            self.query_one("#stat-decided", Static).update(
                f"Decided: {decided}/{self.total}"
            )
            self.query_one("#stat-approved", Static).update(
                f"Approved: {self.approved}"
            )
            self.query_one("#stat-rejected", Static).update(
                f"Rejected: {self.rejected}"
            )
            self.query_one("#stat-skipped", Static).update(
                f"Skipped: {self.skipped}"
            )
            self.query_one("#stat-pending", Static).update(
                f"Pending: {self.pending}"
            )
        except Exception:
            pass  # Widget not yet mounted

    def update_stats(
        self,
        total: int = 0,
        approved: int = 0,
        rejected: int = 0,
        skipped: int = 0,
        pending: int = 0,
    ) -> None:
        """Update all stats at once.

        Args:
            total: Total file count
            approved: Approved count
            rejected: Rejected count
            skipped: Skipped count
            pending: Pending count
        """
        self.total = total
        self.approved = approved
        self.rejected = rejected
        self.skipped = skipped
        self.pending = pending


class MiniProgressWidget(Static):
    """Compact progress indicator."""

    DEFAULT_CSS = """
    MiniProgressWidget {
        height: 1;
        background: $surface;
        color: $text;
    }
    """

    def __init__(
        self,
        decided: int = 0,
        total: int = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._decided = decided
        self._total = total
        self.update(self._render())

    def _render(self) -> str:
        """Render the progress."""
        if self._total == 0:
            return "Progress: 0/0 (0%)"

        pct = self._decided / self._total * 100
        bar_width = 20
        filled = int(pct / 100 * bar_width)
        bar = "#" * filled + "-" * (bar_width - filled)

        return f"[{bar}] {self._decided}/{self._total} ({pct:.0f}%)"

    def update_progress(self, decided: int, total: int) -> None:
        """Update progress values.

        Args:
            decided: Number of decided files
            total: Total files
        """
        self._decided = decided
        self._total = total
        self.update(self._render())
