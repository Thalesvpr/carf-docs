"""Script approval screen."""

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Static, Button, Markdown, Checkbox
from textual.binding import Binding

from ...models.action import ScriptAction


class ScriptApprovalScreen(Screen):
    """Screen for approving script execution."""

    CSS = """
    ScriptApprovalScreen {
        align: center middle;
    }

    ScriptApprovalScreen #approval-container {
        width: 80;
        height: auto;
        padding: 2;
        border: round $warning;
        background: $surface;
    }

    ScriptApprovalScreen .title {
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
        color: $warning;
    }

    ScriptApprovalScreen .warning {
        color: $warning;
        margin: 1 0;
    }

    ScriptApprovalScreen #command-preview {
        background: $surface-darken-1;
        padding: 1;
        margin: 1 0;
        border: solid $surface;
    }

    ScriptApprovalScreen #script-details {
        margin: 1 0;
    }

    ScriptApprovalScreen .checkbox-row {
        height: auto;
        margin: 1 0;
    }

    ScriptApprovalScreen .button-row {
        height: auto;
        align: center middle;
        margin-top: 2;
    }

    ScriptApprovalScreen Button {
        margin: 0 1;
    }

    ScriptApprovalScreen #btn-approve {
        background: $success;
    }
    """

    BINDINGS = [
        Binding("y", "approve", "Approve"),
        Binding("n", "deny", "Deny"),
        Binding("escape", "deny", "Cancel"),
    ]

    def __init__(
        self,
        script_action: ScriptAction,
        preview_text: str = "",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.script_action = script_action
        self.preview_text = preview_text
        self._use_dry_run = script_action.is_dry_run

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with Container(id="approval-container"):
            yield Static("Script Execution Approval", classes="title")

            if not self.script_action.is_dry_run:
                yield Static(
                    "WARNING: This script will modify files!",
                    classes="warning",
                )

            yield Static("Command to execute:", classes="section-label")
            yield Static(
                f"```\n{self.script_action.full_command}\n```",
                id="command-preview",
            )

            if self.preview_text:
                yield Markdown(self.preview_text, id="script-details")

            # Dry-run option (if supported)
            if self.script_action.script_name in {"carf_tree_sync"}:
                with Horizontal(classes="checkbox-row"):
                    yield Checkbox(
                        "Use dry-run mode (no changes)",
                        value=self._use_dry_run,
                        id="dry-run-checkbox",
                    )

            with Horizontal(classes="button-row"):
                yield Button("Approve [Y]", id="btn-approve", variant="success")
                yield Button("Deny [N]", id="btn-deny", variant="error")

    def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
        """Handle checkbox changes."""
        if event.checkbox.id == "dry-run-checkbox":
            self._use_dry_run = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-approve":
            self.action_approve()
        elif event.button.id == "btn-deny":
            self.action_deny()

    def action_approve(self) -> None:
        """Approve script execution."""
        self.dismiss({
            "action": "approve",
            "script_action": self.script_action,
            "dry_run": self._use_dry_run,
        })

    def action_deny(self) -> None:
        """Deny script execution."""
        self.dismiss({"action": "deny"})


class ScriptResultScreen(Screen):
    """Screen for displaying script execution results."""

    CSS = """
    ScriptResultScreen {
        align: center middle;
    }

    ScriptResultScreen #result-container {
        width: 90%;
        height: 80%;
        padding: 2;
        border: round $primary;
        background: $surface;
    }

    ScriptResultScreen .title {
        text-style: bold;
        text-align: center;
        margin-bottom: 1;
    }

    ScriptResultScreen .success {
        color: $success;
    }

    ScriptResultScreen .error {
        color: $error;
    }

    ScriptResultScreen #output-area {
        height: 1fr;
        background: $surface-darken-1;
        padding: 1;
        margin: 1 0;
        border: solid $surface;
        overflow-y: auto;
    }

    ScriptResultScreen .button-row {
        height: auto;
        align: center middle;
        margin-top: 1;
    }
    """

    BINDINGS = [
        Binding("escape", "close", "Close"),
        Binding("enter", "close", "Close"),
    ]

    def __init__(
        self,
        script_name: str,
        success: bool,
        stdout: str = "",
        stderr: str = "",
        exit_code: int = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.script_name = script_name
        self.success = success
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

    def compose(self) -> ComposeResult:
        """Compose the screen."""
        with Container(id="result-container"):
            status = "Success" if self.success else "Failed"
            status_class = "success" if self.success else "error"
            yield Static(
                f"Script Result: {self.script_name} - {status}",
                classes=f"title {status_class}",
            )

            yield Static(f"Exit code: {self.exit_code}")

            output = self.stdout or self.stderr or "No output"
            if self.stderr and self.stdout:
                output = f"{self.stdout}\n\nSTDERR:\n{self.stderr}"

            yield Static(output, id="output-area")

            with Horizontal(classes="button-row"):
                yield Button("Close [Enter]", id="btn-close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        if event.button.id == "btn-close":
            self.action_close()

    def action_close(self) -> None:
        """Close the screen."""
        self.dismiss({"action": "close"})
