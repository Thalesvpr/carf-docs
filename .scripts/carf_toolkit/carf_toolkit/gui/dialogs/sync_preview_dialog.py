"""Sync preview dialog for tree sync operations."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QPlainTextEdit,
    QFrame,
    QWidget,
    QSplitter,
)
from PySide6.QtCore import Signal, Qt

from ...integration.tree_sync_bridge import SyncPreview
from ..theme import COLORS


class SyncPreviewDialog(QDialog):
    """Dialog for previewing and confirming tree sync changes."""

    sync_confirmed = Signal()
    sync_cancelled = Signal()

    def __init__(
        self,
        preview: SyncPreview,
        parent: QWidget | None = None,
    ):
        """Initialize the dialog.

        Args:
            preview: SyncPreview with diff information
            parent: Parent widget
        """
        super().__init__(parent)
        self.preview = preview
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("Sync Tree Preview")
        self.setMinimumSize(800, 600)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()
        icon = QLabel("\U0001f333")  # Tree emoji
        icon.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon)

        header_text = QLabel("Sync Tree Preview")
        header_text.setStyleSheet(
            f"font-size: 18px; font-weight: 600; color: {COLORS.text_primary};"
        )
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # File info
        file_info = QLabel(f"File: {self.preview.path}")
        file_info.setObjectName("metadataLabel")
        layout.addWidget(file_info)

        # Status message
        if self.preview.has_changes:
            status_text = "Changes detected - review below and confirm to apply"
            status_color = COLORS.accent_skip
        else:
            status_text = self.preview.message
            status_color = COLORS.accent_approve

        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"color: {status_color}; font-weight: 600;")
        layout.addWidget(status_label)

        if self.preview.has_changes:
            # Diff view with splitter
            splitter = QSplitter(Qt.Orientation.Horizontal)

            # Old content
            old_frame = QFrame()
            old_layout = QVBoxLayout(old_frame)
            old_layout.setContentsMargins(0, 0, 0, 0)

            old_label = QLabel("Current Content")
            old_label.setObjectName("sectionTitle")
            old_layout.addWidget(old_label)

            old_text = QPlainTextEdit()
            old_text.setReadOnly(True)
            old_text.setPlainText(self.preview.old_content)
            old_text.setStyleSheet(
                f"font-family: 'JetBrains Mono', monospace; font-size: 11px;"
            )
            old_layout.addWidget(old_text)

            splitter.addWidget(old_frame)

            # New content
            new_frame = QFrame()
            new_layout = QVBoxLayout(new_frame)
            new_layout.setContentsMargins(0, 0, 0, 0)

            new_label = QLabel("New Content")
            new_label.setObjectName("sectionTitle")
            new_layout.addWidget(new_label)

            new_text = QPlainTextEdit()
            new_text.setReadOnly(True)
            new_text.setPlainText(self.preview.new_content)
            new_text.setStyleSheet(
                f"font-family: 'JetBrains Mono', monospace; font-size: 11px; "
                f"background-color: {COLORS.background};"
            )
            new_layout.addWidget(new_text)

            splitter.addWidget(new_frame)

            layout.addWidget(splitter)
        else:
            # No changes message
            no_changes = QLabel("No changes are needed for this file.")
            no_changes.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_changes.setStyleSheet(
                f"color: {COLORS.text_secondary}; padding: 40px;"
            )
            layout.addWidget(no_changes)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("toolButton")
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)

        if self.preview.has_changes:
            self.apply_button = QPushButton("Apply Changes")
            self.apply_button.setObjectName("syncButton")
            self.apply_button.clicked.connect(self._on_confirm)
            button_layout.addWidget(self.apply_button)
        else:
            self.ok_button = QPushButton("OK")
            self.ok_button.clicked.connect(self.accept)
            button_layout.addWidget(self.ok_button)

        layout.addLayout(button_layout)

    def _on_confirm(self) -> None:
        """Handle confirm button click."""
        self.sync_confirmed.emit()
        self.accept()

    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        self.sync_cancelled.emit()
        self.reject()
