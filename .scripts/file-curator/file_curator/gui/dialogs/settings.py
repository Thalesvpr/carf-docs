"""Settings dialog for application configuration."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QGroupBox,
    QWidget,
    QTabWidget,
    QComboBox,
    QSpinBox,
    QFileDialog,
)
from PySide6.QtCore import Qt, Signal

from ..theme import COLORS


class SettingsDialog(QDialog):
    """Application settings dialog."""

    settings_changed = Signal(dict)

    def __init__(
        self,
        current_settings: dict | None = None,
        parent: QWidget | None = None,
    ):
        """Initialize the dialog.

        Args:
            current_settings: Current settings values
            parent: Parent widget
        """
        super().__init__(parent)
        self.settings = current_settings or {}
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("Settings")
        self.setMinimumSize(500, 450)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("Settings")
        header.setStyleSheet(
            f"font-size: 20px; font-weight: 600; color: {COLORS.text_primary};"
        )
        layout.addWidget(header)

        # Tab widget
        tabs = QTabWidget()

        # General tab
        general_tab = self._create_general_tab()
        tabs.addTab(general_tab, "General")

        # Scanning tab
        scanning_tab = self._create_scanning_tab()
        tabs.addTab(scanning_tab, "Scanning")

        # Display tab
        display_tab = self._create_display_tab()
        tabs.addTab(display_tab, "Display")

        layout.addWidget(tabs)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("toolButton")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self._on_save)
        button_layout.addWidget(self.save_button)

        layout.addLayout(button_layout)

    def _create_general_tab(self) -> QWidget:
        """Create the general settings tab.

        Returns:
            Tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(16)

        # Data directory
        data_group = QGroupBox("Data Storage")
        data_layout = QVBoxLayout(data_group)

        data_path_layout = QHBoxLayout()
        data_label = QLabel("Data Directory:")
        data_label.setMinimumWidth(120)
        data_path_layout.addWidget(data_label)

        self.data_dir_input = QLineEdit()
        self.data_dir_input.setPlaceholderText("./data")
        data_path_layout.addWidget(self.data_dir_input)

        browse_button = QPushButton("Browse")
        browse_button.setObjectName("toolButton")
        browse_button.clicked.connect(self._browse_data_dir)
        data_path_layout.addWidget(browse_button)

        data_layout.addLayout(data_path_layout)
        layout.addWidget(data_group)

        # Behavior
        behavior_group = QGroupBox("Behavior")
        behavior_layout = QVBoxLayout(behavior_group)

        self.auto_advance_check = QCheckBox("Auto-advance after decision")
        behavior_layout.addWidget(self.auto_advance_check)

        self.confirm_reject_check = QCheckBox("Confirm before rejecting")
        behavior_layout.addWidget(self.confirm_reject_check)

        self.remember_window_check = QCheckBox("Remember window size and position")
        behavior_layout.addWidget(self.remember_window_check)

        layout.addWidget(behavior_group)

        layout.addStretch()
        return tab

    def _create_scanning_tab(self) -> QWidget:
        """Create the scanning settings tab.

        Returns:
            Tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(16)

        # Patterns
        patterns_group = QGroupBox("Include Patterns")
        patterns_layout = QVBoxLayout(patterns_group)

        patterns_info = QLabel(
            "File patterns to include (one per line, glob syntax)"
        )
        patterns_info.setObjectName("metadataLabel")
        patterns_layout.addWidget(patterns_info)

        self.patterns_input = QLineEdit()
        self.patterns_input.setPlaceholderText("**/*.md")
        patterns_layout.addWidget(self.patterns_input)

        layout.addWidget(patterns_group)

        # Exclude directories
        exclude_group = QGroupBox("Exclude Directories")
        exclude_layout = QVBoxLayout(exclude_group)

        exclude_info = QLabel("Directories to exclude (comma-separated)")
        exclude_info.setObjectName("metadataLabel")
        exclude_layout.addWidget(exclude_info)

        self.exclude_input = QLineEdit()
        self.exclude_input.setPlaceholderText(
            ".git, .obsidian, node_modules, __pycache__"
        )
        exclude_layout.addWidget(self.exclude_input)

        layout.addWidget(exclude_group)

        layout.addStretch()
        return tab

    def _create_display_tab(self) -> QWidget:
        """Create the display settings tab.

        Returns:
            Tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(16)

        # Preview
        preview_group = QGroupBox("Content Preview")
        preview_layout = QVBoxLayout(preview_group)

        preview_lines_layout = QHBoxLayout()
        preview_lines_label = QLabel("Preview lines:")
        preview_lines_label.setMinimumWidth(120)
        preview_lines_layout.addWidget(preview_lines_label)

        self.preview_lines_spin = QSpinBox()
        self.preview_lines_spin.setRange(10, 200)
        self.preview_lines_spin.setValue(50)
        preview_lines_layout.addWidget(self.preview_lines_spin)
        preview_lines_layout.addStretch()

        preview_layout.addLayout(preview_lines_layout)
        layout.addWidget(preview_group)

        # Theme
        theme_group = QGroupBox("Theme")
        theme_layout = QVBoxLayout(theme_group)

        theme_row = QHBoxLayout()
        theme_label = QLabel("Color Theme:")
        theme_label.setMinimumWidth(120)
        theme_row.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark (Default)", "Light"])
        self.theme_combo.setEnabled(False)  # Only dark theme for now
        theme_row.addWidget(self.theme_combo)
        theme_row.addStretch()

        theme_layout.addLayout(theme_row)

        coming_soon = QLabel("Additional themes coming soon")
        coming_soon.setObjectName("metadataLabel")
        theme_layout.addWidget(coming_soon)

        layout.addWidget(theme_group)

        layout.addStretch()
        return tab

    def _browse_data_dir(self) -> None:
        """Open directory browser for data directory."""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Data Directory",
            self.data_dir_input.text() or str(Path.home()),
            QFileDialog.Option.ShowDirsOnly,
        )
        if directory:
            self.data_dir_input.setText(directory)

    def _load_settings(self) -> None:
        """Load current settings into the UI."""
        self.data_dir_input.setText(self.settings.get("data_dir", "./data"))
        self.auto_advance_check.setChecked(
            self.settings.get("auto_advance", True)
        )
        self.confirm_reject_check.setChecked(
            self.settings.get("confirm_reject", False)
        )
        self.remember_window_check.setChecked(
            self.settings.get("remember_window", True)
        )
        self.patterns_input.setText(self.settings.get("include_patterns", "**/*.md"))
        self.exclude_input.setText(
            self.settings.get(
                "exclude_dirs",
                ".git, .obsidian, node_modules, __pycache__, file-curator",
            )
        )
        self.preview_lines_spin.setValue(self.settings.get("preview_lines", 50))

    def _on_save(self) -> None:
        """Handle save button click."""
        self.settings = {
            "data_dir": self.data_dir_input.text(),
            "auto_advance": self.auto_advance_check.isChecked(),
            "confirm_reject": self.confirm_reject_check.isChecked(),
            "remember_window": self.remember_window_check.isChecked(),
            "include_patterns": self.patterns_input.text(),
            "exclude_dirs": self.exclude_input.text(),
            "preview_lines": self.preview_lines_spin.value(),
        }
        self.settings_changed.emit(self.settings)
        self.accept()

    def get_settings(self) -> dict:
        """Get the current settings.

        Returns:
            Settings dictionary
        """
        return self.settings
