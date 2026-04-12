"""Script approval dialog for safe execution."""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QCheckBox,
    QFrame,
    QWidget,
    QPlainTextEdit,
)
from PySide6.QtCore import Qt, Signal

from ...integration.registry import ScriptInfo
from ...models.action import ScriptAction
from ..theme import COLORS


class ScriptApprovalDialog(QDialog):
    """Dialog for approving script execution."""

    execution_approved = Signal(ScriptAction)
    execution_cancelled = Signal()

    def __init__(
        self,
        action: ScriptAction,
        script_info: ScriptInfo | None = None,
        parent: QWidget | None = None,
    ):
        """Initialize the dialog.

        Args:
            action: ScriptAction to approve
            script_info: Optional script metadata
            parent: Parent widget
        """
        super().__init__(parent)
        self.action = action
        self.script_info = script_info
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("Script Execution Request")
        self.setMinimumSize(500, 400)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Warning header
        header_layout = QHBoxLayout()
        warning_icon = QLabel("\u26a0\ufe0f")
        warning_icon.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(warning_icon)

        header_text = QLabel("Script Execution Request")
        header_text.setStyleSheet(
            f"font-size: 18px; font-weight: 600; color: {COLORS.accent_skip};"
        )
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Script info section
        info_frame = QFrame()
        info_frame.setStyleSheet(
            f"background-color: {COLORS.background}; "
            f"border: 1px solid {COLORS.border}; "
            f"border-radius: 8px; "
            f"padding: 16px;"
        )
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(12)

        # Script name
        name_row = QHBoxLayout()
        name_label = QLabel("Script:")
        name_label.setObjectName("metadataLabel")
        name_label.setMinimumWidth(80)
        name_row.addWidget(name_label)
        name_value = QLabel(self.action.script_name)
        name_value.setStyleSheet(f"font-weight: 600; color: {COLORS.text_primary};")
        name_row.addWidget(name_value)
        name_row.addStretch()
        info_layout.addLayout(name_row)

        # Command
        cmd_row = QHBoxLayout()
        cmd_label = QLabel("Command:")
        cmd_label.setObjectName("metadataLabel")
        cmd_label.setMinimumWidth(80)
        cmd_row.addWidget(cmd_label)
        cmd_value = QLabel(self.action.full_command)
        cmd_value.setStyleSheet(
            f"font-family: 'JetBrains Mono', monospace; "
            f"font-size: 12px; "
            f"color: {COLORS.text_primary};"
        )
        cmd_value.setWordWrap(True)
        cmd_row.addWidget(cmd_value)
        info_layout.addLayout(cmd_row)

        # Working directory
        if self.action.working_dir:
            wd_row = QHBoxLayout()
            wd_label = QLabel("Directory:")
            wd_label.setObjectName("metadataLabel")
            wd_label.setMinimumWidth(80)
            wd_row.addWidget(wd_label)
            wd_value = QLabel(str(self.action.working_dir))
            wd_value.setStyleSheet(f"color: {COLORS.text_secondary};")
            wd_value.setWordWrap(True)
            wd_row.addWidget(wd_value)
            info_layout.addLayout(wd_row)

        layout.addWidget(info_frame)

        # Script description
        if self.script_info:
            desc_frame = QFrame()
            desc_frame.setStyleSheet(
                f"background-color: {COLORS.surface}; "
                f"border: 1px solid {COLORS.border}; "
                f"border-radius: 8px; "
                f"padding: 16px;"
            )
            desc_layout = QVBoxLayout(desc_frame)

            desc_title = QLabel("This script will:")
            desc_title.setObjectName("metadataLabel")
            desc_layout.addWidget(desc_title)

            desc_text = QLabel(self.script_info.description)
            desc_text.setWordWrap(True)
            desc_layout.addWidget(desc_text)

            # Show if destructive or read-only
            if self.script_info.is_destructive:
                warning_text = QLabel("\u26a0\ufe0f This script modifies files")
                warning_text.setStyleSheet(f"color: {COLORS.accent_reject};")
                desc_layout.addWidget(warning_text)
            else:
                safe_text = QLabel("\u2713 Read-only, no modifications")
                safe_text.setStyleSheet(f"color: {COLORS.accent_approve};")
                desc_layout.addWidget(safe_text)

            layout.addWidget(desc_frame)

        # Dry-run checkbox
        if self.script_info and self.script_info.supports_dry_run:
            self.dry_run_check = QCheckBox("Use dry-run mode (no actual changes)")
            self.dry_run_check.setChecked(self.action.is_dry_run)
            self.dry_run_check.stateChanged.connect(self._on_dry_run_changed)
            layout.addWidget(self.dry_run_check)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("toolButton")
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)

        self.execute_button = QPushButton("Execute")
        if self.script_info and self.script_info.is_destructive and not self.action.is_dry_run:
            self.execute_button.setObjectName("rejectButton")
        else:
            self.execute_button.setObjectName("approveButton")
        self.execute_button.clicked.connect(self._on_execute)
        button_layout.addWidget(self.execute_button)

        layout.addLayout(button_layout)

    def _on_dry_run_changed(self, state: int) -> None:
        """Handle dry-run checkbox change.

        Args:
            state: Check state
        """
        self.action.is_dry_run = state == Qt.CheckState.Checked.value

        # Update button style based on mode
        if self.script_info and self.script_info.is_destructive and not self.action.is_dry_run:
            self.execute_button.setObjectName("rejectButton")
        else:
            self.execute_button.setObjectName("approveButton")
        self.execute_button.style().unpolish(self.execute_button)
        self.execute_button.style().polish(self.execute_button)

    def _on_execute(self) -> None:
        """Handle execute button click."""
        self.action.approved = True
        self.execution_approved.emit(self.action)
        self.accept()

    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        self.execution_cancelled.emit()
        self.reject()

    def get_action(self) -> ScriptAction:
        """Get the (possibly modified) action.

        Returns:
            ScriptAction
        """
        return self.action
