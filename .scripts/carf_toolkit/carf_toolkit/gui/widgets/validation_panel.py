"""Validation panel showing validation issues."""

from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QBrush

from ...models.file_item import FileItem, ValidationIssue
from ..theme import COLORS


class ValidationIssueItem(QListWidgetItem):
    """Custom list item for validation issues."""

    SEVERITY_ICONS = {
        "error": "\u2717",    # X mark
        "warning": "\u26a0",  # Warning sign
        "info": "\u2139",     # Info sign
    }

    SEVERITY_COLORS = {
        "error": COLORS.accent_reject,
        "warning": COLORS.accent_skip,
        "info": COLORS.accent_info,
    }

    def __init__(self, issue: ValidationIssue):
        """Initialize the list item.

        Args:
            issue: ValidationIssue to display
        """
        self.issue = issue
        icon = self.SEVERITY_ICONS.get(issue.severity, "\u2022")
        line_info = f" (L{issue.line_number})" if issue.line_number else ""
        display_text = f"{icon} {issue.code}{line_info}\n   {issue.message}"
        super().__init__(display_text)

        # Set color based on severity
        color = self.SEVERITY_COLORS.get(issue.severity, COLORS.text_primary)
        self.setForeground(QBrush(QColor(color)))

        # Set tooltip with suggestion if available
        if issue.suggestion:
            self.setToolTip(f"Suggestion: {issue.suggestion}")


class ValidationPanel(QFrame):
    """Panel showing validation issues for a file."""

    issue_clicked = Signal(ValidationIssue)  # Emits clicked issue
    validate_requested = Signal()  # Emits when validate button clicked

    def __init__(self, parent: QWidget | None = None):
        """Initialize the validation panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("validationFrame")
        self._current_file: Optional[FileItem] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(8)

        # Header with validate button
        header_layout = QHBoxLayout()

        title = QLabel("Validation")
        title.setObjectName("sectionTitle")
        header_layout.addWidget(title)

        header_layout.addStretch()

        self.validate_button = QPushButton("\U0001f50d Validate")
        self.validate_button.setObjectName("validateButton")
        self.validate_button.setToolTip("Run validation on this file")
        self.validate_button.clicked.connect(self.validate_requested.emit)
        header_layout.addWidget(self.validate_button)

        layout.addLayout(header_layout)

        # Summary label
        self.summary_label = QLabel("No issues")
        self.summary_label.setObjectName("metadataLabel")
        layout.addWidget(self.summary_label)

        # Issues list
        self.issues_list = QListWidget()
        self.issues_list.setAlternatingRowColors(True)
        self.issues_list.itemClicked.connect(self._on_issue_clicked)
        layout.addWidget(self.issues_list)

    def set_file(self, file_item: FileItem | None) -> None:
        """Set the file to display validation issues for.

        Args:
            file_item: FileItem to display
        """
        self._current_file = file_item
        self.issues_list.clear()

        if file_item is None:
            self.summary_label.setText("No file selected")
            return

        issues = file_item.validation_issues or []
        self.show_issues(issues)

    def show_issues(self, issues: list[ValidationIssue]) -> None:
        """Display a list of validation issues.

        Args:
            issues: List of ValidationIssue objects
        """
        self.issues_list.clear()

        if not issues:
            self.summary_label.setText("No issues found")
            self.summary_label.setStyleSheet(f"color: {COLORS.accent_approve};")
            return

        # Count by severity
        errors = sum(1 for i in issues if i.severity == "error")
        warnings = sum(1 for i in issues if i.severity == "warning")
        infos = sum(1 for i in issues if i.severity == "info")

        # Update summary
        parts = []
        if errors:
            parts.append(f"\u2717 {errors} errors")
        if warnings:
            parts.append(f"\u26a0 {warnings} warnings")
        if infos:
            parts.append(f"\u2139 {infos} info")

        self.summary_label.setText(" | ".join(parts))

        if errors:
            self.summary_label.setStyleSheet(f"color: {COLORS.accent_reject};")
        elif warnings:
            self.summary_label.setStyleSheet(f"color: {COLORS.accent_skip};")
        else:
            self.summary_label.setStyleSheet(f"color: {COLORS.text_secondary};")

        # Group issues by validator
        issues_by_validator: dict[str, list[ValidationIssue]] = {}
        for issue in issues:
            validator = issue.validator_name or "unknown"
            if validator not in issues_by_validator:
                issues_by_validator[validator] = []
            issues_by_validator[validator].append(issue)

        # Add items grouped by validator
        for validator, validator_issues in issues_by_validator.items():
            # Add separator/header for validator group
            header_item = QListWidgetItem(f"--- {validator} ({len(validator_issues)}) ---")
            header_item.setFlags(Qt.ItemFlag.NoItemFlags)
            header_item.setForeground(QBrush(QColor(COLORS.text_muted)))
            self.issues_list.addItem(header_item)

            # Add issues
            for issue in validator_issues:
                item = ValidationIssueItem(issue)
                self.issues_list.addItem(item)

    def _on_issue_clicked(self, item: QListWidgetItem) -> None:
        """Handle issue item click.

        Args:
            item: Clicked item
        """
        if isinstance(item, ValidationIssueItem):
            self.issue_clicked.emit(item.issue)

    def clear(self) -> None:
        """Clear the validation panel."""
        self.issues_list.clear()
        self.summary_label.setText("No issues")
        self.summary_label.setStyleSheet("")
