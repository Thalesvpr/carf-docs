"""Editor screen for editing observations and justification."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, TextArea, Input, Label
from textual.binding import Binding


class EditorScreen(Screen):
    """Screen for editing review observations, justification, and tags."""

    CSS = """
    EditorScreen {
        align: center middle;
    }

    EditorScreen #editor-container {
        width: 90%;
        height: 90%;
        padding: 2;
        border: round $primary;
        background: $surface;
    }

    EditorScreen .title {
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
    }

    EditorScreen .section-label {
        margin-top: 1;
        color: $text-muted;
    }

    EditorScreen TextArea {
        height: 8;
        margin: 1 0;
    }

    EditorScreen #observations-area {
        height: 10;
    }

    EditorScreen #justification-area {
        height: 8;
    }

    EditorScreen #tags-input {
        width: 100%;
        margin: 1 0;
    }

    EditorScreen .button-row {
        height: auto;
        align: center middle;
        margin-top: 2;
    }

    EditorScreen Button {
        margin: 0 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+s", "save", "Save"),
        Binding("escape", "cancel", "Cancel"),
    ]

    def __init__(
        self,
        file_path: str = "",
        observations: str = "",
        justification: str = "",
        tags: list[str] | None = None,
        require_justification: bool = False,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.file_path = file_path
        self.initial_observations = observations
        self.initial_justification = justification
        self.initial_tags = tags or []
        self.require_justification = require_justification

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with Container(id="editor-container"):
            yield Static(f"Edit Review: {self.file_path}", classes="title")

            yield Label("Observations:", classes="section-label")
            yield TextArea(
                self.initial_observations,
                id="observations-area",
            )

            yield Label("Justification:", classes="section-label")
            yield TextArea(
                self.initial_justification,
                id="justification-area",
            )

            yield Label("Tags (comma-separated):", classes="section-label")
            yield Input(
                value=", ".join(self.initial_tags),
                placeholder="e.g., needs-review, documentation, api",
                id="tags-input",
            )

            if self.require_justification:
                yield Static(
                    "Note: Justification is required for rejection",
                    classes="section-label",
                )

            with Horizontal(classes="button-row"):
                yield Button("Save [Ctrl+S]", id="btn-save", variant="primary")
                yield Button("Cancel [Esc]", id="btn-cancel", variant="default")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-save":
            self.action_save()
        elif event.button.id == "btn-cancel":
            self.action_cancel()

    def action_save(self) -> None:
        """Save and return values."""
        observations = self.query_one("#observations-area", TextArea).text
        justification = self.query_one("#justification-area", TextArea).text
        tags_input = self.query_one("#tags-input", Input).value

        # Parse tags
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]

        # Validate if justification is required
        if self.require_justification and not justification.strip():
            # Show error - for now just don't dismiss
            return

        self.dismiss({
            "action": "save",
            "observations": observations,
            "justification": justification,
            "tags": tags,
        })

    def action_cancel(self) -> None:
        """Cancel editing."""
        self.dismiss({"action": "cancel"})


class RejectEditorScreen(EditorScreen):
    """Specialized editor for rejection with required justification."""

    def __init__(
        self,
        file_path: str = "",
        observations: str = "",
        tags: list[str] | None = None,
        **kwargs,
    ):
        super().__init__(
            file_path=file_path,
            observations=observations,
            justification="",
            tags=tags,
            require_justification=True,
            **kwargs,
        )

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with Container(id="editor-container"):
            yield Static(f"Reject: {self.file_path}", classes="title")
            yield Static(
                "Please provide a justification for rejection.",
                classes="section-label",
            )

            yield Label("Justification (required):", classes="section-label")
            yield TextArea(
                "",
                id="justification-area",
            )

            yield Label("Observations:", classes="section-label")
            yield TextArea(
                self.initial_observations,
                id="observations-area",
            )

            yield Label("Tags (comma-separated):", classes="section-label")
            yield Input(
                value=", ".join(self.initial_tags),
                placeholder="e.g., needs-work, incomplete",
                id="tags-input",
            )

            with Horizontal(classes="button-row"):
                yield Button("Reject [Ctrl+S]", id="btn-save", variant="error")
                yield Button("Cancel [Esc]", id="btn-cancel", variant="default")
