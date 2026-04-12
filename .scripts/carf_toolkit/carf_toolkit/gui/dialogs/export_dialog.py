"""Export dialog for aggregating and exporting data."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QPlainTextEdit,
    QFrame,
    QWidget,
    QFileDialog,
    QApplication,
    QCheckBox,
)
from PySide6.QtCore import Qt

from ...models.file_item import FileItem
from ...export.aggregator import DataAggregator, ExportFormat
from ..theme import COLORS


class ExportDialog(QDialog):
    """Dialog for exporting aggregated data."""

    def __init__(
        self,
        files: list[FileItem],
        root_path: Optional[Path] = None,
        parent: QWidget | None = None,
    ):
        """Initialize the dialog.

        Args:
            files: List of FileItems to export
            root_path: Root directory path
            parent: Parent widget
        """
        super().__init__(parent)
        self.files = files
        self.root_path = root_path
        self.aggregator = DataAggregator(files, root_path)
        self._setup_ui()
        self._update_preview()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("Export Data")
        self.setMinimumSize(700, 600)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("Export Data")
        header.setStyleSheet(
            f"font-size: 20px; font-weight: 600; color: {COLORS.text_primary};"
        )
        layout.addWidget(header)

        # Options row
        options_layout = QHBoxLayout()

        # Format selector
        format_label = QLabel("Format:")
        format_label.setObjectName("metadataLabel")
        options_layout.addWidget(format_label)

        self.format_combo = QComboBox()
        self.format_combo.addItems(["JSON", "CSV", "Markdown"])
        self.format_combo.currentTextChanged.connect(self._update_preview)
        self.format_combo.setMinimumWidth(120)
        options_layout.addWidget(self.format_combo)

        options_layout.addSpacing(24)

        # Scope selector
        scope_label = QLabel("Scope:")
        scope_label.setObjectName("metadataLabel")
        options_layout.addWidget(scope_label)

        self.scope_combo = QComboBox()
        self.scope_combo.addItems(["All Files", "Review Only", "Approved Only", "Rejected Only"])
        self.scope_combo.currentTextChanged.connect(self._update_preview)
        self.scope_combo.setMinimumWidth(140)
        options_layout.addWidget(self.scope_combo)

        options_layout.addSpacing(24)

        # Include validation checkbox
        self.include_validation = QCheckBox("Include validation data")
        self.include_validation.setChecked(True)
        self.include_validation.stateChanged.connect(self._update_preview)
        options_layout.addWidget(self.include_validation)

        options_layout.addStretch()
        layout.addLayout(options_layout)

        # Preview area
        preview_label = QLabel("Preview")
        preview_label.setObjectName("sectionTitle")
        layout.addWidget(preview_label)

        self.preview_text = QPlainTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setStyleSheet(
            f"font-family: 'JetBrains Mono', monospace; font-size: 12px;"
        )
        layout.addWidget(self.preview_text)

        # Statistics summary
        stats = self.aggregator.get_statistics()
        stats_text = (
            f"Total: {stats['total_files']} files | "
            f"Errors: {stats['validation']['total_errors']} | "
            f"Warnings: {stats['validation']['total_warnings']} | "
            f"Broken Links: {stats['links']['total_broken']}"
        )
        stats_label = QLabel(stats_text)
        stats_label.setObjectName("metadataLabel")
        layout.addWidget(stats_label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.setObjectName("toolButton")
        self.copy_button.clicked.connect(self._copy_to_clipboard)
        button_layout.addWidget(self.copy_button)

        self.save_button = QPushButton("Save to File")
        self.save_button.clicked.connect(self._save_to_file)
        button_layout.addWidget(self.save_button)

        self.close_button = QPushButton("Close")
        self.close_button.setObjectName("toolButton")
        self.close_button.clicked.connect(self.accept)
        button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)

    def _get_format(self) -> ExportFormat:
        """Get the selected export format."""
        format_map = {
            "JSON": ExportFormat.JSON,
            "CSV": ExportFormat.CSV,
            "Markdown": ExportFormat.MARKDOWN,
        }
        return format_map.get(self.format_combo.currentText(), ExportFormat.JSON)

    def _get_scope(self) -> str:
        """Get the selected scope."""
        scope_map = {
            "All Files": "all",
            "Review Only": "review",
            "Approved Only": "approved",
            "Rejected Only": "rejected",
        }
        return scope_map.get(self.scope_combo.currentText(), "all")

    def _update_preview(self) -> None:
        """Update the preview text."""
        export_format = self._get_format()
        scope = self._get_scope()
        include_validation = self.include_validation.isChecked()

        content = self.aggregator.export(
            format=export_format,
            include_validation=include_validation,
            scope=scope,
        )

        # Truncate for preview if too long
        max_preview = 10000
        if len(content) > max_preview:
            content = content[:max_preview] + "\n\n... (truncated for preview)"

        self.preview_text.setPlainText(content)

    def _copy_to_clipboard(self) -> None:
        """Copy export content to clipboard."""
        export_format = self._get_format()
        scope = self._get_scope()
        include_validation = self.include_validation.isChecked()

        content = self.aggregator.export(
            format=export_format,
            include_validation=include_validation,
            scope=scope,
        )

        clipboard = QApplication.clipboard()
        clipboard.setText(content)

        # Update button text temporarily
        self.copy_button.setText("Copied!")
        from PySide6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self.copy_button.setText("Copy to Clipboard"))

    def _save_to_file(self) -> None:
        """Save export content to a file."""
        export_format = self._get_format()

        # Determine file extension
        ext_map = {
            ExportFormat.JSON: ("JSON Files (*.json)", ".json"),
            ExportFormat.CSV: ("CSV Files (*.csv)", ".csv"),
            ExportFormat.MARKDOWN: ("Markdown Files (*.md)", ".md"),
        }
        filter_str, ext = ext_map.get(export_format, ("All Files (*)", ""))

        # Show save dialog
        default_name = f"carf-export{ext}"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Export",
            str(self.root_path / default_name) if self.root_path else default_name,
            filter_str,
        )

        if file_path:
            scope = self._get_scope()
            include_validation = self.include_validation.isChecked()

            content = self.aggregator.export(
                format=export_format,
                include_validation=include_validation,
                scope=scope,
            )

            try:
                Path(file_path).write_text(content, encoding="utf-8")
                self.save_button.setText("Saved!")
                from PySide6.QtCore import QTimer
                QTimer.singleShot(2000, lambda: self.save_button.setText("Save to File"))
            except Exception as e:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(self, "Error", f"Failed to save file: {e}")
