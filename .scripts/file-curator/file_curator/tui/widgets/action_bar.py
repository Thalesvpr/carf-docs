"""Action bar widget displaying available keyboard shortcuts."""

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Static
from textual.reactive import reactive


class ActionBarWidget(Horizontal):
    """Widget displaying available actions and their keyboard shortcuts."""

    DEFAULT_CSS = """
    ActionBarWidget {
        height: 3;
        dock: bottom;
        background: $surface;
        padding: 0 1;
    }

    ActionBarWidget .action-item {
        width: auto;
        padding: 0 2;
    }

    ActionBarWidget .action-key {
        background: $primary;
        color: $text;
        padding: 0 1;
        text-style: bold;
    }

    ActionBarWidget .action-label {
        padding: 0 1;
        color: $text-muted;
    }

    ActionBarWidget .action-separator {
        color: $surface-lighten-2;
    }
    """

    show_edit: reactive[bool] = reactive(True)
    show_scripts: reactive[bool] = reactive(True)
    custom_actions: reactive[list] = reactive(list)

    # Default actions
    DEFAULT_ACTIONS = [
        ("a", "Approve"),
        ("r", "Reject"),
        ("s", "Skip"),
        ("e", "Edit"),
        ("v", "Validate"),
        ("t", "Sync"),
        ("p", "Progress"),
        ("?", "Help"),
        ("q", "Quit"),
    ]

    def __init__(
        self,
        show_edit: bool = True,
        show_scripts: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.show_edit = show_edit
        self.show_scripts = show_scripts

    def compose(self) -> ComposeResult:
        """Compose the widget."""
        for key, label in self._get_actions():
            yield Static(f"[{key}]", classes="action-key")
            yield Static(label, classes="action-label")
            yield Static(" ", classes="action-separator")

    def _get_actions(self) -> list[tuple[str, str]]:
        """Get the list of actions to display."""
        actions = [
            ("a", "Approve"),
            ("r", "Reject"),
            ("s", "Skip"),
        ]

        if self.show_edit:
            actions.append(("e", "Edit"))

        if self.show_scripts:
            actions.extend([
                ("v", "Validate"),
                ("t", "Sync"),
            ])

        actions.extend([
            ("p", "Progress"),
            ("?", "Help"),
            ("q", "Quit"),
        ])

        return actions

    def refresh_actions(self) -> None:
        """Refresh the action bar display."""
        # Remove existing children
        self.remove_children()

        # Add new action widgets
        for key, label in self._get_actions():
            self.mount(Static(f"[{key}]", classes="action-key"))
            self.mount(Static(label, classes="action-label"))
            self.mount(Static(" ", classes="action-separator"))


class CompactActionBar(Static):
    """Compact single-line action bar."""

    DEFAULT_CSS = """
    CompactActionBar {
        height: 1;
        dock: bottom;
        background: $surface;
        color: $text-muted;
    }
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update(self._render())

    def _render(self) -> str:
        """Render the action bar."""
        actions = [
            "[A]pprove",
            "[R]eject",
            "[S]kip",
            "[E]dit",
            "[V]alidate",
            "[P]rogress",
            "[?]Help",
            "[Q]uit",
        ]
        return " | ".join(actions)
