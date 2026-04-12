"""Combined right panel containing Info and Validation panels."""

from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QScrollArea,
    QSplitter,
)
from PySide6.QtCore import Qt, Signal

from ...models.file_item import FileItem, ValidationIssue
from .info_panel import InfoPanel
from .validation_panel import ValidationPanel
from ..theme import COLORS


class CombinedRightPanel(QFrame):
    """Combined panel with file info and validation results."""

    # Signals forwarded from child panels
    status_changed = Signal(str)
    description_changed = Signal(str)
    issue_clicked = Signal(ValidationIssue)
    validate_requested = Signal()

    def __init__(self, parent: QWidget | None = None):
        """Initialize the combined panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("combinedPanel")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Use splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Info panel (top)
        self.info_panel = InfoPanel()
        self.info_panel.status_changed.connect(self.status_changed.emit)
        self.info_panel.description_changed.connect(self.description_changed.emit)
        splitter.addWidget(self.info_panel)

        # Validation panel (bottom)
        validation_container = QFrame()
        validation_container.setStyleSheet(
            f"background-color: {COLORS.surface}; "
            f"border: 1px solid {COLORS.border}; "
            f"border-radius: 8px;"
        )
        validation_layout = QVBoxLayout(validation_container)
        validation_layout.setContentsMargins(12, 12, 12, 12)
        validation_layout.setSpacing(0)

        self.validation_panel = ValidationPanel()
        self.validation_panel.issue_clicked.connect(self.issue_clicked.emit)
        self.validation_panel.validate_requested.connect(self.validate_requested.emit)
        validation_layout.addWidget(self.validation_panel)

        splitter.addWidget(validation_container)

        # Set initial sizes (60% info, 40% validation)
        splitter.setSizes([300, 200])

        layout.addWidget(splitter)

    def set_file(self, file_item: FileItem | None) -> None:
        """Set the file to display.

        Args:
            file_item: FileItem to display
        """
        self.info_panel.set_file(file_item)
        self.validation_panel.set_file(file_item)

    def show_validation_issues(self, issues: list[ValidationIssue]) -> None:
        """Display validation issues.

        Args:
            issues: List of ValidationIssue objects
        """
        self.validation_panel.show_issues(issues)

    def refresh(self) -> None:
        """Refresh display with current file data."""
        self.info_panel.refresh()

    def clear(self) -> None:
        """Clear the panel."""
        self.info_panel.set_file(None)
        self.validation_panel.clear()
