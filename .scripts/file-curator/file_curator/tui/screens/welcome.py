"""Welcome screen for session selection."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Input, DataTable, Label
from textual.binding import Binding

from ...models.session import CurationSession


class WelcomeScreen(Screen):
    """Welcome screen for creating or resuming sessions."""

    CSS = """
    WelcomeScreen {
        align: center middle;
    }

    WelcomeScreen #welcome-container {
        width: 80;
        height: auto;
        padding: 2;
        border: round $primary;
        background: $surface;
    }

    WelcomeScreen .title {
        text-style: bold;
        text-align: center;
        margin-bottom: 2;
    }

    WelcomeScreen .subtitle {
        text-align: center;
        color: $text-muted;
        margin-bottom: 2;
    }

    WelcomeScreen #sessions-table {
        height: 15;
        margin: 1 0;
    }

    WelcomeScreen #new-session-input {
        width: 100%;
        margin: 1 0;
    }

    WelcomeScreen .button-row {
        height: auto;
        align: center middle;
        margin-top: 1;
    }

    WelcomeScreen Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("n", "new_session", "New Session"),
        Binding("enter", "resume_session", "Resume"),
        Binding("q", "quit", "Quit"),
    ]

    def __init__(
        self,
        sessions: list[CurationSession] | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.sessions = sessions or []

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with Container(id="welcome-container"):
            yield Static("File Curator", classes="title")
            yield Static("Interactive documentation curation", classes="subtitle")

            if self.sessions:
                yield Static("Recent Sessions:", classes="section-label")
                yield DataTable(id="sessions-table")
            else:
                yield Static("No existing sessions found.", classes="section-label")

            yield Static("Create New Session:", classes="section-label")
            yield Input(
                placeholder="Enter session name...",
                id="new-session-input",
            )

            with Horizontal(classes="button-row"):
                yield Button("New Session [N]", id="btn-new", variant="primary")
                if self.sessions:
                    yield Button("Resume [Enter]", id="btn-resume", variant="default")
                yield Button("Quit [Q]", id="btn-quit", variant="error")

    def on_mount(self) -> None:
        """Handle mount event."""
        if self.sessions:
            table = self.query_one("#sessions-table", DataTable)
            table.add_column("ID", key="id")
            table.add_column("Name", key="name")
            table.add_column("Progress", key="progress")
            table.add_column("Created", key="created")

            for session in self.sessions:
                decided = session.approved_count + session.rejected_count
                progress = f"{decided}/{session.total_files}"
                created = session.created_at.strftime("%Y-%m-%d")
                table.add_row(
                    session.id,
                    session.name,
                    progress,
                    created,
                    key=session.id,
                )

            table.cursor_type = "row"

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-new":
            self.action_new_session()
        elif event.button.id == "btn-resume":
            self.action_resume_session()
        elif event.button.id == "btn-quit":
            self.action_quit()

    def action_new_session(self) -> None:
        """Create a new session."""
        input_widget = self.query_one("#new-session-input", Input)
        session_name = input_widget.value.strip()

        if not session_name:
            session_name = "curation-session"

        self.dismiss({"action": "new", "name": session_name})

    def action_resume_session(self) -> None:
        """Resume a selected session."""
        if not self.sessions:
            return

        table = self.query_one("#sessions-table", DataTable)
        if table.cursor_row is not None:
            row_key = table.get_row_at(table.cursor_row)
            if row_key:
                session_id = str(row_key[0])  # First column is ID
                self.dismiss({"action": "resume", "session_id": session_id})

    def action_quit(self) -> None:
        """Quit the application."""
        self.dismiss({"action": "quit"})

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in sessions table."""
        self.action_resume_session()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission."""
        self.action_new_session()
