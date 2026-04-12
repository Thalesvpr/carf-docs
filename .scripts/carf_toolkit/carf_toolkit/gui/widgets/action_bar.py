"""Action bar with approve/reject/skip and tool buttons."""

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QKeySequence, QShortcut

from ..theme import COLORS


class ActionBar(QFrame):
    """Action bar with curation and tool buttons."""

    approve_clicked = Signal()
    reject_clicked = Signal()
    skip_clicked = Signal()
    edit_clicked = Signal()
    sync_clicked = Signal()
    tools_clicked = Signal()

    def __init__(self, parent: QWidget | None = None):
        """Initialize the action bar.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setStyleSheet(
            f"background-color: {COLORS.surface}; "
            f"border-top: 1px solid {COLORS.divider}; "
            f"border-radius: 0px;"
        )
        self._is_readme = False
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Left side - action buttons
        self.reject_button = QPushButton("\u2717 Reject")
        self.reject_button.setObjectName("rejectButton")
        self.reject_button.setToolTip("Reject file (R)")
        self.reject_button.clicked.connect(self.reject_clicked.emit)
        self.reject_button.setMinimumWidth(100)
        layout.addWidget(self.reject_button)

        self.skip_button = QPushButton("\u25b7 Skip")
        self.skip_button.setObjectName("skipButton")
        self.skip_button.setToolTip("Skip for now (S)")
        self.skip_button.clicked.connect(self.skip_clicked.emit)
        self.skip_button.setMinimumWidth(90)
        layout.addWidget(self.skip_button)

        self.approve_button = QPushButton("\u2713 Approve")
        self.approve_button.setObjectName("approveButton")
        self.approve_button.setToolTip("Approve file (A)")
        self.approve_button.clicked.connect(self.approve_clicked.emit)
        self.approve_button.setMinimumWidth(100)
        layout.addWidget(self.approve_button)

        # Spacer
        layout.addItem(
            QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        # Right side - tools
        self.edit_button = QPushButton("\u270e Edit")
        self.edit_button.setObjectName("toolButton")
        self.edit_button.setToolTip("Edit file (E)")
        self.edit_button.clicked.connect(self.edit_clicked.emit)
        layout.addWidget(self.edit_button)

        self.sync_button = QPushButton("\U0001f333 Sync Tree")
        self.sync_button.setObjectName("syncButton")
        self.sync_button.setToolTip("Sync README tree structure")
        self.sync_button.clicked.connect(self.sync_clicked.emit)
        self.sync_button.setVisible(False)  # Only show for README files
        layout.addWidget(self.sync_button)

        self.tools_button = QPushButton("\u2699 Tools")
        self.tools_button.setObjectName("toolButton")
        self.tools_button.setToolTip("Open tools menu")
        self.tools_button.clicked.connect(self.tools_clicked.emit)
        layout.addWidget(self.tools_button)

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable all action buttons.

        Args:
            enabled: Whether to enable buttons
        """
        self.approve_button.setEnabled(enabled)
        self.reject_button.setEnabled(enabled)
        self.skip_button.setEnabled(enabled)
        self.edit_button.setEnabled(enabled)
        self.sync_button.setEnabled(enabled and self._is_readme)
        self.tools_button.setEnabled(enabled)

    def set_file_loaded(self, loaded: bool) -> None:
        """Update button states based on whether a file is loaded.

        Args:
            loaded: Whether a file is currently loaded
        """
        self.approve_button.setEnabled(loaded)
        self.reject_button.setEnabled(loaded)
        self.skip_button.setEnabled(loaded)
        self.edit_button.setEnabled(loaded)
        self.sync_button.setEnabled(loaded and self._is_readme)

    def set_is_readme(self, is_readme: bool) -> None:
        """Set whether the current file is a README.

        Args:
            is_readme: True if current file is a README
        """
        self._is_readme = is_readme
        self.sync_button.setVisible(is_readme)
        self.sync_button.setEnabled(is_readme)
