"""New session dialog for creating or resuming sessions."""

from pathlib import Path
from typing import Optional, TYPE_CHECKING

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QFrame,
    QListWidget,
    QListWidgetItem,
    QTabWidget,
    QWidget,
    QCheckBox,
    QGroupBox,
)
from PySide6.QtCore import Qt, Signal

from ...models.session import CurationSession, SessionConfig
from ..theme import COLORS

if TYPE_CHECKING:
    from ..settings_store import SettingsStore


class NewSessionDialog(QDialog):
    """Dialog for creating a new session or resuming an existing one."""

    session_created = Signal(CurationSession)
    session_resumed = Signal(str)  # Session ID

    def __init__(
        self,
        existing_sessions: list[CurationSession] | None = None,
        settings_store: "SettingsStore | None" = None,
        parent: QWidget | None = None,
    ):
        """Initialize the dialog.

        Args:
            existing_sessions: List of existing sessions for resume
            settings_store: Settings store for remembering last directory
            parent: Parent widget
        """
        super().__init__(parent)
        self.existing_sessions = existing_sessions or []
        self.settings_store = settings_store
        self.selected_session: Optional[CurationSession] = None
        self._setup_ui()
        self._load_saved_settings()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("File Curator - Session")
        self.setMinimumSize(600, 500)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header
        header = QLabel("File Curator")
        header.setStyleSheet(
            f"font-size: 24px; font-weight: 600; color: {COLORS.text_primary};"
        )
        layout.addWidget(header)

        subtitle = QLabel("Curate your documentation files with ease")
        subtitle.setStyleSheet(f"color: {COLORS.text_secondary}; margin-bottom: 16px;")
        layout.addWidget(subtitle)

        # Tab widget
        tabs = QTabWidget()

        # New session tab
        new_tab = self._create_new_session_tab()
        tabs.addTab(new_tab, "New Session")

        # Resume tab
        resume_tab = self._create_resume_tab()
        tabs.addTab(resume_tab, "Resume Session")

        layout.addWidget(tabs)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("toolButton")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self._on_start)
        button_layout.addWidget(self.start_button)

        layout.addLayout(button_layout)

    def _create_new_session_tab(self) -> QWidget:
        """Create the new session tab.

        Returns:
            Tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(16)

        # Session name
        name_layout = QVBoxLayout()
        name_label = QLabel("Session Name")
        name_label.setObjectName("metadataLabel")
        name_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., documentation-review-2026")
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # Root path
        path_layout = QVBoxLayout()
        path_label = QLabel("Root Directory")
        path_label.setObjectName("metadataLabel")
        path_layout.addWidget(path_label)

        path_input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select directory to scan...")
        path_input_layout.addWidget(self.path_input)

        browse_button = QPushButton("Browse")
        browse_button.setObjectName("toolButton")
        browse_button.clicked.connect(self._browse_directory)
        path_input_layout.addWidget(browse_button)
        path_layout.addLayout(path_input_layout)
        layout.addLayout(path_layout)

        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)

        self.require_justification_check = QCheckBox(
            "Require justification for rejections"
        )
        self.require_justification_check.setChecked(True)
        options_layout.addWidget(self.require_justification_check)

        self.skip_returns_check = QCheckBox("Skipped files return to queue")
        self.skip_returns_check.setChecked(True)
        options_layout.addWidget(self.skip_returns_check)

        layout.addWidget(options_group)

        layout.addStretch()
        return tab

    def _create_resume_tab(self) -> QWidget:
        """Create the resume session tab.

        Returns:
            Tab widget
        """
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 16, 0, 0)
        layout.setSpacing(16)

        if not self.existing_sessions:
            empty_label = QLabel("No existing sessions found")
            empty_label.setStyleSheet(
                f"color: {COLORS.text_muted}; padding: 40px; text-align: center;"
            )
            empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(empty_label)
        else:
            sessions_label = QLabel("Select a session to resume")
            sessions_label.setObjectName("metadataLabel")
            layout.addWidget(sessions_label)

            self.sessions_list = QListWidget()
            for session in self.existing_sessions:
                item = QListWidgetItem()
                progress_pct = session.progress_percent
                text = (
                    f"{session.name}\n"
                    f"{session.root_path} | {progress_pct:.0f}% complete\n"
                    f"Created: {session.created_at.strftime('%Y-%m-%d %H:%M')}"
                )
                item.setText(text)
                item.setData(Qt.ItemDataRole.UserRole, session.id)
                self.sessions_list.addItem(item)

            self.sessions_list.itemDoubleClicked.connect(self._on_session_selected)
            layout.addWidget(self.sessions_list)

        return tab

    def _load_saved_settings(self) -> None:
        """Load saved settings like last directory."""
        if not self.settings_store:
            return

        # Load last directory
        last_dir = self.settings_store.get_last_directory()
        if last_dir and Path(last_dir).exists():
            self.path_input.setText(last_dir)

        # If there's a last session, switch to resume tab and select it
        last_session_id = self.settings_store.get_last_session_id()
        if last_session_id and hasattr(self, "sessions_list"):
            for i in range(self.sessions_list.count()):
                item = self.sessions_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == last_session_id:
                    self.sessions_list.setCurrentItem(item)
                    break

    def _browse_directory(self) -> None:
        """Open directory browser."""
        # Start from last directory if available
        start_dir = self.path_input.text() or str(Path.home())

        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Root Directory",
            start_dir,
            QFileDialog.Option.ShowDirsOnly,
        )
        if directory:
            self.path_input.setText(directory)

    def _on_start(self) -> None:
        """Handle start button click."""
        # Check if we're creating new or resuming
        if self.name_input.text() and self.path_input.text():
            # Create new session
            config = SessionConfig(
                require_justification_on_reject=self.require_justification_check.isChecked(),
                skip_returns_to_queue=self.skip_returns_check.isChecked(),
            )
            session = CurationSession.create(
                name=self.name_input.text(),
                root_path=Path(self.path_input.text()),
                config=config,
            )
            self.selected_session = session
            self.session_created.emit(session)
            self.accept()
        elif hasattr(self, "sessions_list"):
            current = self.sessions_list.currentItem()
            if current:
                session_id = current.data(Qt.ItemDataRole.UserRole)
                self.session_resumed.emit(session_id)
                self.accept()

    def _on_session_selected(self, item: QListWidgetItem) -> None:
        """Handle session double-click.

        Args:
            item: Selected item
        """
        session_id = item.data(Qt.ItemDataRole.UserRole)
        self.session_resumed.emit(session_id)
        self.accept()

    def get_session(self) -> Optional[CurationSession]:
        """Get the created session.

        Returns:
            Created session or None
        """
        return self.selected_session
