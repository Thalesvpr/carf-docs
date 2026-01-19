"""Main application window for File Curator."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QStackedWidget,
    QMessageBox,
    QMenu,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QKeySequence, QShortcut

from ..models.file_item import FileItem, FileStatus
from ..models.session import CurationSession
from ..models.review import ReviewRecord, ReviewDecision, ReviewMetadata
from ..state.database import Database
from ..state.repository import SessionRepository, FileRepository, ReviewRepository
from ..state.queue import CurationQueue
from ..scanner.discovery import DeterministicScanner
from ..scanner.parser import ContentParser, update_file_status
from ..templates.renderer import TemplateRenderer
from ..templates.loader import TemplateLoader
from ..integration.registry import AvailableScriptsRegistry
from ..integration.executor import SafeScriptExecutor

from .widgets import (
    FileListWidget,
    MarkdownViewer,
    MarkdownEditor,
    MetadataPanel,
    ActionBar,
    ProgressHeader,
)
from .dialogs import (
    NewSessionDialog,
    ScriptApprovalDialog,
    SettingsDialog,
    RejectionDialog,
)
from .theme import COLORS
from .settings_store import SettingsStore

from ..logging.console import SessionLogger


class MainWindow(QMainWindow):
    """Main application window."""

    session_changed = Signal(CurationSession)
    file_changed = Signal(FileItem)

    def __init__(
        self,
        db: Database,
        data_dir: Path,
        parent: QWidget | None = None,
    ):
        """Initialize the main window.

        Args:
            db: Database instance
            data_dir: Data directory path
            parent: Parent widget
        """
        super().__init__(parent)
        self.db = db
        self.data_dir = data_dir

        # Initialize repositories
        self.session_repo = SessionRepository(db)
        self.file_repo = FileRepository(db)
        self.review_repo = ReviewRepository(db)

        # Initialize components
        self.template_loader = TemplateLoader(
            user_templates_dir=data_dir.parent / "templates"
        )
        self.template_renderer = TemplateRenderer(self.template_loader)
        self.script_registry = AvailableScriptsRegistry()
        self.logger = SessionLogger(data_dir / "logs")
        self.settings_store = SettingsStore(data_dir / "settings.json")

        # Current state
        self.current_session: Optional[CurationSession] = None
        self.current_queue: Optional[CurationQueue] = None
        self.current_file: Optional[FileItem] = None
        self.content_parser = ContentParser()

        self._setup_ui()
        self._setup_shortcuts()
        self._setup_menu()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("File Curator")
        self.setMinimumSize(1200, 800)

        # Restore saved window geometry or use default
        saved_geo = self.settings_store.get_window_geometry()
        if saved_geo:
            self.setGeometry(
                saved_geo["x"], saved_geo["y"],
                saved_geo["width"], saved_geo["height"]
            )
        else:
            self.resize(1400, 900)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.progress_header = ProgressHeader()
        main_layout.addWidget(self.progress_header)

        # Main content area
        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left panel - file list
        self.file_list = FileListWidget()
        self.file_list.setMinimumWidth(250)
        self.file_list.setMaximumWidth(400)
        self.file_list.file_selected.connect(self._on_file_selected)
        content_splitter.addWidget(self.file_list)

        # Center - stacked widget for viewer/editor
        self.center_stack = QStackedWidget()

        # Viewer mode
        self.markdown_viewer = MarkdownViewer()
        self.center_stack.addWidget(self.markdown_viewer)

        # Editor mode
        self.markdown_editor = MarkdownEditor()
        self.markdown_editor.save_requested.connect(self._on_editor_save)
        self.center_stack.addWidget(self.markdown_editor)

        content_splitter.addWidget(self.center_stack)

        # Right panel - metadata
        self.metadata_panel = MetadataPanel()
        self.metadata_panel.setMinimumWidth(250)
        self.metadata_panel.setMaximumWidth(350)
        content_splitter.addWidget(self.metadata_panel)

        # Set splitter sizes
        content_splitter.setSizes([280, 750, 300])

        main_layout.addWidget(content_splitter, 1)

        # Action bar
        self.action_bar = ActionBar()
        self.action_bar.approve_clicked.connect(self._on_approve)
        self.action_bar.reject_clicked.connect(self._on_reject)
        self.action_bar.skip_clicked.connect(self._on_skip)
        self.action_bar.edit_clicked.connect(self._on_edit)
        self.action_bar.tools_clicked.connect(self._on_tools)
        self.action_bar.set_file_loaded(False)
        main_layout.addWidget(self.action_bar)

        # Initial state
        self.markdown_viewer.set_empty_message("No file selected")

    def _setup_shortcuts(self) -> None:
        """Set up keyboard shortcuts."""
        # Approve - A
        approve_shortcut = QShortcut(QKeySequence("A"), self)
        approve_shortcut.activated.connect(self._on_approve)

        # Reject - R
        reject_shortcut = QShortcut(QKeySequence("R"), self)
        reject_shortcut.activated.connect(self._on_reject)

        # Skip - S
        skip_shortcut = QShortcut(QKeySequence("S"), self)
        skip_shortcut.activated.connect(self._on_skip)

        # Edit - E
        edit_shortcut = QShortcut(QKeySequence("E"), self)
        edit_shortcut.activated.connect(self._on_edit)

        # Navigate - J/K (vim-like)
        next_shortcut = QShortcut(QKeySequence("J"), self)
        next_shortcut.activated.connect(self._select_next)

        prev_shortcut = QShortcut(QKeySequence("K"), self)
        prev_shortcut.activated.connect(self._select_previous)

        # Escape - exit editor mode
        escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        escape_shortcut.activated.connect(self._exit_editor)

    def _setup_menu(self) -> None:
        """Set up the menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New Session", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._show_new_session_dialog)
        file_menu.addAction(new_action)

        open_action = QAction("Open Session", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self._show_new_session_dialog)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        settings_action = QAction("Settings", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self._show_settings_dialog)
        file_menu.addAction(settings_action)

        file_menu.addSeparator()

        quit_action = QAction("Quit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        # View menu
        view_menu = menubar.addMenu("View")

        toggle_editor_action = QAction("Toggle Editor", self)
        toggle_editor_action.setShortcut(QKeySequence("E"))
        toggle_editor_action.triggered.connect(self._on_edit)
        view_menu.addAction(toggle_editor_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def show_welcome(self) -> None:
        """Show the welcome/new session dialog."""
        QTimer.singleShot(100, self._show_new_session_dialog)

    def _show_new_session_dialog(self) -> None:
        """Show the new session dialog."""
        existing = self.session_repo.list_all()
        dialog = NewSessionDialog(existing, self.settings_store, self)
        dialog.session_created.connect(self._on_session_created)
        dialog.session_resumed.connect(self._on_session_resumed)
        dialog.exec()

    def _show_settings_dialog(self) -> None:
        """Show the settings dialog."""
        dialog = SettingsDialog({}, self)
        dialog.exec()

    def _show_about(self) -> None:
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About File Curator",
            "File Curator v0.2.0\n\n"
            "A professional GUI for curating documentation files.\n"
            '"Tinder for files"\n\n'
            "Keyboard shortcuts:\n"
            "  A - Approve\n"
            "  R - Reject\n"
            "  S - Skip\n"
            "  E - Toggle editor\n"
            "  J/K - Navigate files",
        )

    def _on_session_created(self, session: CurationSession) -> None:
        """Handle new session creation.

        Args:
            session: Created session
        """
        # Save session
        self.session_repo.create(session)
        self.logger.log_session_start(session.id, session.name)

        # Scan files
        self._scan_session(session)

    def _on_session_resumed(self, session_id: str) -> None:
        """Handle session resume.

        Args:
            session_id: Session ID to resume
        """
        session = self.session_repo.get(session_id)
        if session:
            self._load_session(session)
            self.logger.log_session_resume(session.id, session.name)

    def _scan_session(self, session: CurationSession) -> None:
        """Scan files for a session.

        Args:
            session: Session to scan
        """
        self.markdown_viewer.set_loading()
        self.setWindowTitle(f"File Curator - {session.name} (Scanning...)")

        # Scan files
        scanner = DeterministicScanner(
            session.root_path,
            session.config.include_patterns,
            session.config.exclude_dirs,
        )

        files = scanner.scan()

        # Parse content for each file
        for file_item in files:
            try:
                parsed = self.content_parser.parse(file_item.path)
                file_item.title = parsed.title
                file_item.doc_type = parsed.doc_type
                file_item.frontmatter_modules = parsed.modules
                file_item.frontmatter_epic = parsed.epic
                file_item.word_count = parsed.word_count
                # Footer metadata from the file itself
                file_item.file_status = parsed.file_status
                file_item.file_last_updated = parsed.last_updated
                file_item.footer_metadata = parsed.footer_metadata
                # Links
                file_item.links = parsed.links
            except Exception:
                pass

        # Save files to database
        self.file_repo.create_many(session.id, files)

        # Update session counts
        session.total_files = len(files)
        session.pending_count = len(files)
        self.session_repo.update(session)

        self._load_session(session)

    def _load_session(self, session: CurationSession) -> None:
        """Load a session into the UI.

        Args:
            session: Session to load
        """
        self.current_session = session
        self.current_queue = CurationQueue(self.db, session.id)

        # Save to settings for history
        self.settings_store.set_last_session_id(session.id)
        self.settings_store.set_last_directory(str(session.root_path))
        self.settings_store.add_recent_session(
            session.id, session.name, str(session.root_path)
        )

        # Update UI
        self.setWindowTitle(f"File Curator - {session.name}")
        self.progress_header.set_session(session)

        # Load file list
        files = self.file_repo.list_by_session(session.id)
        self.file_list.set_files(files)

        # Select first pending file
        next_file = self.current_queue.get_next()
        if next_file:
            self._load_file(next_file)
            self.file_list.select_file(next_file.relative_path)
        else:
            self.markdown_viewer.set_empty_message("All files have been reviewed!")
            self.action_bar.set_file_loaded(False)

        self.session_changed.emit(session)

    def _load_file(self, file_item: FileItem) -> None:
        """Load a file for review.

        Args:
            file_item: File to load
        """
        self.current_file = file_item
        self.action_bar.set_file_loaded(True)
        self.metadata_panel.set_file(file_item)

        # Generate review card
        try:
            content_preview = self._get_content_preview(file_item.path)
            review_card = self.template_renderer.render_review_card(
                file_item,
                content_preview=content_preview,
            )
            self.markdown_viewer.set_markdown(review_card)
            self.markdown_editor.set_content(review_card)
        except Exception as e:
            self.markdown_viewer.set_error(str(e))

        # Log file presentation
        if self.current_session:
            progress = self.current_queue.get_progress() if self.current_queue else {}
            self.logger.log_file_presented(
                file_item.relative_path,
                progress.get("decided", 0) + 1,
                progress.get("total", 0),
            )

        self.file_changed.emit(file_item)

    def _get_content_preview(self, path: Path, max_lines: int = 50) -> str:
        """Get a preview of file content.

        Args:
            path: Path to the file
            max_lines: Maximum lines to include

        Returns:
            Content preview string
        """
        try:
            content = path.read_text(encoding="utf-8")
            lines = content.split("\n")
            if len(lines) > max_lines:
                preview = "\n".join(lines[:max_lines])
                return f"```markdown\n{preview}\n\n... ({len(lines) - max_lines} more lines)\n```"
            return f"```markdown\n{content}\n```"
        except Exception:
            return "_Unable to read file content._"

    def _on_file_selected(self, file_item: FileItem) -> None:
        """Handle file selection from list.

        Args:
            file_item: Selected file
        """
        self._load_file(file_item)

    def _on_approve(self) -> None:
        """Handle approve action."""
        if not self.current_file or not self.current_session:
            return

        self._record_decision(ReviewDecision.APPROVED)

    def _on_reject(self) -> None:
        """Handle reject action."""
        if not self.current_file or not self.current_session:
            return

        # Show rejection dialog if justification required
        if self.current_session.config.require_justification_on_reject:
            dialog = RejectionDialog(
                self.current_file.filename,
                require_justification=True,
                parent=self,
            )
            dialog.rejection_confirmed.connect(self._on_rejection_confirmed)
            dialog.exec()
        else:
            self._record_decision(ReviewDecision.REJECTED)

    def _on_rejection_confirmed(self, justification: str) -> None:
        """Handle confirmed rejection.

        Args:
            justification: Rejection justification
        """
        self._record_decision(ReviewDecision.REJECTED, justification=justification)

    def _on_skip(self) -> None:
        """Handle skip action."""
        if not self.current_file or not self.current_session:
            return

        self._record_decision(ReviewDecision.SKIPPED)

    def _record_decision(
        self,
        decision: ReviewDecision,
        observations: str = "",
        justification: str = "",
    ) -> None:
        """Record a review decision.

        Args:
            decision: The decision made
            observations: Optional observations
            justification: Optional justification
        """
        if not self.current_file or not self.current_session or not self.current_queue:
            return

        file_item = self.current_file
        session = self.current_session

        # Map decision to file status
        status_map = {
            ReviewDecision.APPROVED: FileStatus.APPROVED,
            ReviewDecision.REJECTED: FileStatus.REJECTED,
            ReviewDecision.SKIPPED: FileStatus.SKIPPED,
        }
        new_status = status_map[decision]

        # Map decision to file status string for the file itself
        file_status_map = {
            ReviewDecision.APPROVED: "Approved",
            ReviewDecision.REJECTED: "Rejected",
            ReviewDecision.SKIPPED: "Review",  # Skip keeps as Review
        }
        file_status_str = file_status_map[decision]

        # Update the file's own metadata (Status do arquivo)
        if decision != ReviewDecision.SKIPPED:
            update_file_status(file_item.path, file_status_str)

        # Update file status in database
        self.file_repo.update_status(
            session.id,
            file_item.relative_path,
            new_status,
        )

        # Create review record
        file_id = self.file_repo.get_file_id(session.id, file_item.relative_path)
        if file_id:
            review = ReviewRecord(
                file_path=file_item.path,
                session_id=session.id,
                decision=decision,
                observations=observations,
                justification=justification,
                metadata=ReviewMetadata(session_id=session.id),
            )
            self.review_repo.create(file_id, review)

        # Log the decision
        self.logger.log_decision(
            decision.value.upper(),
            file_item.relative_path,
            observations or justification,
        )

        # Update counts
        self.session_repo.update_counts(session.id)
        session = self.session_repo.get(session.id)
        if session:
            self.current_session = session
            self.progress_header.update_progress(session)

        # Update file list
        self.file_list.update_file_status(file_item.relative_path, new_status)

        # Refresh queue and advance
        self.current_queue.refresh()
        self._advance_to_next()

    def _advance_to_next(self) -> None:
        """Advance to the next file in the queue."""
        if not self.current_queue:
            return

        next_file = self.current_queue.get_next()
        if next_file:
            self._load_file(next_file)
            self.file_list.select_file(next_file.relative_path)
        else:
            # All done!
            self.markdown_viewer.set_empty_message(
                "All files have been reviewed!\n\n"
                "Session complete."
            )
            self.current_file = None
            self.action_bar.set_file_loaded(False)
            self.metadata_panel.set_file(None)

            # Log completion
            if self.current_session:
                self.logger.log_session_complete(self.current_session.id)

    def _select_next(self) -> None:
        """Select the next file in the list."""
        current = self.file_list.list_widget.currentRow()
        if current < self.file_list.list_widget.count() - 1:
            self.file_list.list_widget.setCurrentRow(current + 1)
            item = self.file_list.list_widget.currentItem()
            if item:
                from .widgets.file_list import FileListItem
                if isinstance(item, FileListItem):
                    self._load_file(item.file_item)

    def _select_previous(self) -> None:
        """Select the previous file in the list."""
        current = self.file_list.list_widget.currentRow()
        if current > 0:
            self.file_list.list_widget.setCurrentRow(current - 1)
            item = self.file_list.list_widget.currentItem()
            if item:
                from .widgets.file_list import FileListItem
                if isinstance(item, FileListItem):
                    self._load_file(item.file_item)

    def _on_edit(self) -> None:
        """Toggle between viewer and editor mode."""
        if self.center_stack.currentIndex() == 0:
            # Switch to editor
            self.center_stack.setCurrentIndex(1)
        else:
            # Switch to viewer
            self._exit_editor()

    def _exit_editor(self) -> None:
        """Exit editor mode."""
        if self.center_stack.currentIndex() == 1:
            self.center_stack.setCurrentIndex(0)

    def _on_editor_save(self) -> None:
        """Handle editor save."""
        content = self.markdown_editor.get_content()
        self.markdown_viewer.set_markdown(content)
        self._exit_editor()

    def _on_tools(self) -> None:
        """Show tools menu."""
        menu = QMenu(self)

        # Validate action
        validate_action = QAction("Run Validator", self)
        validate_action.triggered.connect(self._run_validator)
        menu.addAction(validate_action)

        menu.addSeparator()

        # Refresh action
        refresh_action = QAction("Refresh File List", self)
        refresh_action.triggered.connect(self._refresh_files)
        menu.addAction(refresh_action)

        # Show menu at button
        button = self.action_bar.tools_button
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def _run_validator(self) -> None:
        """Run the validator script on current file."""
        if not self.current_file or not self.current_session:
            return

        script_info = self.script_registry.get("carf_validator")
        if not script_info:
            QMessageBox.warning(
                self,
                "Script Not Found",
                "The carf_validator script is not available.",
            )
            return

        executor = SafeScriptExecutor(
            registry=self.script_registry,
            working_dir=self.current_session.root_path,
        )

        action = executor.create_action(
            "carf_validator",
            args=["--file", self.current_file.relative_path],
            dry_run=False,
        )

        dialog = ScriptApprovalDialog(action, script_info, self)
        dialog.exec()

    def _refresh_files(self) -> None:
        """Refresh the file list."""
        if self.current_session:
            files = self.file_repo.list_by_session(self.current_session.id)
            self.file_list.set_files(files)

    def closeEvent(self, event) -> None:
        """Handle window close.

        Args:
            event: Close event
        """
        # Save window geometry
        geo = self.geometry()
        self.settings_store.set_window_geometry(geo.x(), geo.y(), geo.width(), geo.height())

        # Log session end
        if self.current_session:
            self.logger.log_session_end(self.current_session.id)

        # Close database
        self.db.close()

        event.accept()
