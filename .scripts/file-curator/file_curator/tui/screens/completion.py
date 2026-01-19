"""Completion screen shown when all files are decided."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button
from textual.binding import Binding

from ...models.session import CurationSession


class CompletionScreen(Screen):
    """Screen shown when curation is complete."""

    CSS = """
    CompletionScreen {
        align: center middle;
    }

    CompletionScreen #completion-container {
        width: 70;
        height: auto;
        padding: 2;
        border: round $success;
        background: $surface;
    }

    CompletionScreen .title {
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
        color: $success;
    }

    CompletionScreen .subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    CompletionScreen .stats-section {
        height: auto;
        margin: 1 0;
        padding: 1;
        border: solid $surface;
    }

    CompletionScreen .stat-row {
        height: auto;
    }

    CompletionScreen .stat-label {
        width: 20;
        color: $text-muted;
    }

    CompletionScreen .stat-value {
        text-style: bold;
    }

    CompletionScreen .stat-value.approved {
        color: $success;
    }

    CompletionScreen .stat-value.rejected {
        color: $error;
    }

    CompletionScreen .button-row {
        height: auto;
        align: center middle;
        margin-top: 2;
    }

    CompletionScreen Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("e", "export", "Export"),
        Binding("q", "quit", "Quit"),
        Binding("r", "restart", "New Session"),
    ]

    def __init__(self, session: CurationSession, **kwargs):
        super().__init__(**kwargs)
        self.session = session

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with Container(id="completion-container"):
            yield Static("Curation Complete!", classes="title")
            yield Static(
                f"All {self.session.total_files} files have been reviewed.",
                classes="subtitle",
            )

            with Vertical(classes="stats-section"):
                with Horizontal(classes="stat-row"):
                    yield Static("Total Files:", classes="stat-label")
                    yield Static(
                        str(self.session.total_files),
                        classes="stat-value",
                    )

                with Horizontal(classes="stat-row"):
                    yield Static("Approved:", classes="stat-label")
                    yield Static(
                        str(self.session.approved_count),
                        classes="stat-value approved",
                    )

                with Horizontal(classes="stat-row"):
                    yield Static("Rejected:", classes="stat-label")
                    yield Static(
                        str(self.session.rejected_count),
                        classes="stat-value rejected",
                    )

                approval_rate = (
                    self.session.approved_count / self.session.total_files * 100
                    if self.session.total_files > 0
                    else 0
                )
                with Horizontal(classes="stat-row"):
                    yield Static("Approval Rate:", classes="stat-label")
                    yield Static(f"{approval_rate:.1f}%", classes="stat-value")

                if self.session.completed_at:
                    with Horizontal(classes="stat-row"):
                        yield Static("Completed:", classes="stat-label")
                        yield Static(
                            self.session.completed_at.strftime("%Y-%m-%d %H:%M"),
                            classes="stat-value",
                        )

            with Horizontal(classes="button-row"):
                yield Button("Export Report [E]", id="btn-export", variant="primary")
                yield Button("New Session [R]", id="btn-restart", variant="default")
                yield Button("Quit [Q]", id="btn-quit", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-export":
            self.action_export()
        elif event.button.id == "btn-restart":
            self.action_restart()
        elif event.button.id == "btn-quit":
            self.action_quit()

    def action_export(self) -> None:
        """Export the curation report."""
        self.dismiss({"action": "export"})

    def action_restart(self) -> None:
        """Start a new session."""
        self.dismiss({"action": "restart"})

    def action_quit(self) -> None:
        """Quit the application."""
        self.dismiss({"action": "quit"})
