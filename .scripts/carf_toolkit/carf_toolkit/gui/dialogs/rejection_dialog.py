"""Rejection dialog for requiring justification."""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QPlainTextEdit,
    QFrame,
    QWidget,
)
from PySide6.QtCore import Signal

from ..theme import COLORS


class RejectionDialog(QDialog):
    """Dialog for entering rejection justification."""

    rejection_confirmed = Signal(str)  # Justification text
    rejection_cancelled = Signal()

    def __init__(
        self,
        file_name: str,
        require_justification: bool = False,
        parent: QWidget | None = None,
    ):
        """Initialize the dialog.

        Args:
            file_name: Name of the file being rejected
            require_justification: Whether justification is required
            parent: Parent widget
        """
        super().__init__(parent)
        self.file_name = file_name
        self.require_justification = require_justification
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("Reject File")
        self.setMinimumSize(450, 300)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()
        icon = QLabel("\u2717")
        icon.setStyleSheet(
            f"font-size: 24px; color: {COLORS.accent_reject};"
        )
        header_layout.addWidget(icon)

        header_text = QLabel("Reject File")
        header_text.setStyleSheet(
            f"font-size: 18px; font-weight: 600; color: {COLORS.accent_reject};"
        )
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # File info
        file_frame = QFrame()
        file_frame.setStyleSheet(
            f"background-color: {COLORS.background}; "
            f"border: 1px solid {COLORS.border}; "
            f"border-radius: 8px; "
            f"padding: 12px;"
        )
        file_layout = QVBoxLayout(file_frame)
        file_layout.setSpacing(4)

        file_label = QLabel("File")
        file_label.setObjectName("metadataLabel")
        file_layout.addWidget(file_label)

        file_name_label = QLabel(self.file_name)
        file_name_label.setStyleSheet(
            f"font-weight: 600; color: {COLORS.text_primary};"
        )
        file_layout.addWidget(file_name_label)

        layout.addWidget(file_frame)

        # Justification input
        justification_label = QLabel(
            "Justification" + (" (required)" if self.require_justification else " (optional)")
        )
        justification_label.setObjectName("metadataLabel")
        layout.addWidget(justification_label)

        self.justification_input = QPlainTextEdit()
        self.justification_input.setPlaceholderText(
            "Explain why this file is being rejected..."
        )
        self.justification_input.textChanged.connect(self._update_confirm_button)
        layout.addWidget(self.justification_input)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("toolButton")
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)

        self.confirm_button = QPushButton("Reject")
        self.confirm_button.setObjectName("rejectButton")
        self.confirm_button.clicked.connect(self._on_confirm)
        if self.require_justification:
            self.confirm_button.setEnabled(False)
        button_layout.addWidget(self.confirm_button)

        layout.addLayout(button_layout)

    def _update_confirm_button(self) -> None:
        """Update confirm button state based on justification."""
        if self.require_justification:
            has_text = bool(self.justification_input.toPlainText().strip())
            self.confirm_button.setEnabled(has_text)

    def _on_confirm(self) -> None:
        """Handle confirm button click."""
        justification = self.justification_input.toPlainText().strip()
        self.rejection_confirmed.emit(justification)
        self.accept()

    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        self.rejection_cancelled.emit()
        self.reject()

    def get_justification(self) -> str:
        """Get the entered justification.

        Returns:
            Justification text
        """
        return self.justification_input.toPlainText().strip()
