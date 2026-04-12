"""Info panel showing file metadata with editable fields."""

from datetime import date
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
    QComboBox,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt, Signal

from ...models.file_item import FileItem, FileStatus
from ...scanner.parser import update_file_metadata
from ..theme import COLORS


class MetadataRow(QFrame):
    """A single row in the metadata panel."""

    def __init__(
        self, label: str, value: str = "", parent: QWidget | None = None
    ):
        """Initialize the row.

        Args:
            label: Label text
            value: Value text
            parent: Parent widget
        """
        super().__init__(parent)
        self.setStyleSheet("background: transparent; border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(2)

        self.label_widget = QLabel(label)
        self.label_widget.setObjectName("metadataLabel")
        layout.addWidget(self.label_widget)

        self.value_widget = QLabel(value)
        self.value_widget.setObjectName("metadataValue")
        self.value_widget.setWordWrap(True)
        self.value_widget.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self.value_widget)

    def set_value(self, value: str) -> None:
        """Set the value text.

        Args:
            value: Value to display
        """
        self.value_widget.setText(value)


class StatusBadge(QFrame):
    """Status badge widget."""

    STATUS_STYLES = {
        FileStatus.PENDING: (COLORS.status_pending, "#ffffff"),
        FileStatus.APPROVED: (COLORS.status_approved, "#1a1a2e"),
        FileStatus.REJECTED: (COLORS.status_rejected, "#ffffff"),
        FileStatus.SKIPPED: (COLORS.status_skipped, "#1a1a2e"),
    }

    def __init__(self, status: FileStatus | None = None, parent: QWidget | None = None):
        """Initialize the badge.

        Args:
            status: Initial status
            parent: Parent widget
        """
        super().__init__(parent)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.addWidget(self.label)

        if status:
            self.set_status(status)

    def set_status(self, status: FileStatus) -> None:
        """Set the status to display.

        Args:
            status: Status to display
        """
        bg_color, text_color = self.STATUS_STYLES.get(
            status, (COLORS.status_pending, "#ffffff")
        )
        self.setStyleSheet(
            f"background-color: {bg_color}; "
            f"border-radius: 4px; "
            f"border: none;"
        )
        self.label.setStyleSheet(
            f"color: {text_color}; "
            f"font-weight: 600; "
            f"font-size: 12px; "
            f"background: transparent;"
        )
        self.label.setText(status.value.upper())


class InfoPanel(QFrame):
    """Panel displaying editable file metadata."""

    status_changed = Signal(str)  # Emits new status string
    description_changed = Signal(str)  # Emits new description

    def __init__(self, parent: QWidget | None = None):
        """Initialize the info panel.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("metadataFrame")
        self._current_file: Optional[FileItem] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Header
        title = QLabel("File Info")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        # Status dropdown (editable)
        status_row = QHBoxLayout()
        status_label = QLabel("Status")
        status_label.setObjectName("metadataLabel")
        status_row.addWidget(status_label)
        status_row.addStretch()

        self.status_combo = QComboBox()
        self.status_combo.addItems(["Review", "Approved", "Rejected"])
        self.status_combo.setMinimumWidth(120)
        self.status_combo.currentTextChanged.connect(self._on_status_changed)
        status_row.addWidget(self.status_combo)
        layout.addLayout(status_row)

        # Last updated (read-only)
        self.updated_row = MetadataRow("Atualizado")
        layout.addWidget(self.updated_row)

        # Description (editable)
        desc_label = QLabel("Descricao")
        desc_label.setObjectName("metadataLabel")
        layout.addWidget(desc_label)

        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Enter description...")
        self.description_input.editingFinished.connect(self._on_description_changed)
        layout.addWidget(self.description_input)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet(f"background-color: {COLORS.divider};")
        sep.setMaximumHeight(1)
        layout.addWidget(sep)

        # Scroll area for metadata
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("border: none; background: transparent;")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(8)

        # Metadata rows
        self.path_row = MetadataRow("Path")
        scroll_layout.addWidget(self.path_row)

        self.type_row = MetadataRow("Type")
        scroll_layout.addWidget(self.type_row)

        self.words_row = MetadataRow("Words")
        scroll_layout.addWidget(self.words_row)

        self.size_row = MetadataRow("Size")
        scroll_layout.addWidget(self.size_row)

        self.modified_row = MetadataRow("Modified")
        scroll_layout.addWidget(self.modified_row)

        # Separator for links section
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet(f"background-color: {COLORS.divider};")
        sep2.setMaximumHeight(1)
        scroll_layout.addWidget(sep2)

        # Links section
        links_title = QLabel("Links")
        links_title.setObjectName("sectionTitle")
        scroll_layout.addWidget(links_title)

        self.links_row = MetadataRow("Total")
        scroll_layout.addWidget(self.links_row)

        self.broken_links_row = MetadataRow("Broken")
        scroll_layout.addWidget(self.broken_links_row)

        self.external_links_row = MetadataRow("External")
        scroll_layout.addWidget(self.external_links_row)

        scroll_layout.addStretch()
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def set_file(self, file_item: FileItem | None) -> None:
        """Set the file to display metadata for.

        Args:
            file_item: FileItem to display
        """
        self._current_file = file_item

        if file_item is None:
            self._clear()
            return

        # Block signals while updating
        self.status_combo.blockSignals(True)
        self.description_input.blockSignals(True)

        # Set status dropdown
        file_status = file_item.file_status or "Review"
        index = self.status_combo.findText(file_status)
        if index >= 0:
            self.status_combo.setCurrentIndex(index)
        else:
            self.status_combo.setCurrentIndex(0)  # Default to Review

        # Set updated date
        self.updated_row.set_value(file_item.file_last_updated or "-")

        # Set description
        self.description_input.setText(file_item.file_description or "")

        # Set other metadata
        self.path_row.set_value(file_item.relative_path)
        self.type_row.set_value(file_item.doc_type or "Unknown")
        self.words_row.set_value(str(file_item.word_count))
        self.size_row.set_value(self._format_file_size(file_item.path))
        self.modified_row.set_value(
            file_item.updated_at.strftime("%Y-%m-%d %H:%M")
            if file_item.updated_at
            else "Unknown"
        )

        # Links info
        links = file_item.links or []
        total_links = len(links)
        internal_links = [link for link in links if not link.is_external]
        broken_links = [link for link in internal_links if not link.is_valid]
        external_links = [link for link in links if link.is_external]

        self.links_row.set_value(str(total_links))
        if broken_links:
            self.broken_links_row.set_value(f"{len(broken_links)} (broken)")
            self.broken_links_row.value_widget.setStyleSheet(
                f"color: {COLORS.accent_reject};"
            )
        else:
            self.broken_links_row.set_value("0")
            self.broken_links_row.value_widget.setStyleSheet("")
        self.external_links_row.set_value(str(len(external_links)))

        # Unblock signals
        self.status_combo.blockSignals(False)
        self.description_input.blockSignals(False)

    def _clear(self) -> None:
        """Clear all metadata fields."""
        self.status_combo.setCurrentIndex(0)
        self.updated_row.set_value("-")
        self.description_input.clear()
        self.path_row.set_value("-")
        self.type_row.set_value("-")
        self.words_row.set_value("-")
        self.size_row.set_value("-")
        self.modified_row.set_value("-")
        self.links_row.set_value("-")
        self.broken_links_row.set_value("-")
        self.broken_links_row.value_widget.setStyleSheet("")
        self.external_links_row.set_value("-")

    def _format_file_size(self, path: Path) -> str:
        """Format file size in human-readable format.

        Args:
            path: Path to the file

        Returns:
            Formatted size string
        """
        try:
            size = path.stat().st_size
            for unit in ["B", "KB", "MB", "GB"]:
                if size < 1024:
                    return f"{size:.1f} {unit}"
                size /= 1024
            return f"{size:.1f} TB"
        except (OSError, IOError):
            return "Unknown"

    def _on_status_changed(self, new_status: str) -> None:
        """Handle status dropdown change.

        Args:
            new_status: New status value
        """
        if self._current_file:
            self.status_changed.emit(new_status)

    def _on_description_changed(self) -> None:
        """Handle description field change."""
        if self._current_file:
            new_desc = self.description_input.text()
            self.description_changed.emit(new_desc)

    def refresh(self) -> None:
        """Refresh display with current file data."""
        if self._current_file:
            self.set_file(self._current_file)
