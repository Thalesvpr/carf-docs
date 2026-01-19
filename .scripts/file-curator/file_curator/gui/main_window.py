"""Main application window for File Curator - Simplified version without database."""

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
    QFileDialog,
    QLabel,
    QProgressBar,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QKeySequence, QShortcut

from ..models.file_item import FileItem, FileStatus
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
    ScriptApprovalDialog,
    SettingsDialog,
    RejectionDialog,
)
from .theme import COLORS
from .settings_store import SettingsStore

from ..logging.console import SessionLogger


class MainWindow(QMainWindow):
    """Main application window - simplified without database."""

    file_changed = Signal(FileItem)

    def __init__(
        self,
        data_dir: Path,
        project_root: Optional[Path] = None,
        parent: QWidget | None = None,
    ):
        """Initialize the main window.

        Args:
            data_dir: Data directory path
            project_root: Optional initial project root to scan
            parent: Parent widget
        """
        super().__init__(parent)
        self.data_dir = data_dir

        # Initialize components
        self.template_loader = TemplateLoader(
            user_templates_dir=data_dir.parent / "templates"
        )
        self.template_renderer = TemplateRenderer(self.template_loader)
        self.script_registry = AvailableScriptsRegistry()
        self.logger = SessionLogger(data_dir / "logs")
        self.settings_store = SettingsStore(data_dir / "settings.json")

        # Current state - simple list-based
        self.root_path: Optional[Path] = project_root
        self.all_files: list[FileItem] = []
        self.current_index: int = 0
        self.current_file: Optional[FileItem] = None
        self.content_parser = ContentParser()

        self._setup_ui()
        self._setup_shortcuts()
        self._setup_menu()

        # If project_root provided, scan immediately
        if project_root:
            QTimer.singleShot(100, lambda: self._scan_directory(project_root))

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

        # Header with progress
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
        self.markdown_viewer.set_empty_message(
            "No directory selected.\n\nUse File > Open Directory to start."
        )

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

        open_dir_action = QAction("Open Directory...", self)
        open_dir_action.setShortcut(QKeySequence.StandardKey.Open)
        open_dir_action.triggered.connect(self._show_open_dialog)
        file_menu.addAction(open_dir_action)

        rescan_action = QAction("Rescan", self)
        rescan_action.setShortcut(QKeySequence("F5"))
        rescan_action.triggered.connect(self._rescan)
        file_menu.addAction(rescan_action)

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

        # Filter submenu
        filter_menu = view_menu.addMenu("Filter by Status")

        show_all_action = QAction("Show All", self)
        show_all_action.triggered.connect(lambda: self._filter_files(None))
        filter_menu.addAction(show_all_action)

        show_review_action = QAction("Show Review Only", self)
        show_review_action.triggered.connect(lambda: self._filter_files("Review"))
        filter_menu.addAction(show_review_action)

        show_approved_action = QAction("Show Approved Only", self)
        show_approved_action.triggered.connect(lambda: self._filter_files("Approved"))
        filter_menu.addAction(show_approved_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def show_welcome(self) -> None:
        """Show the welcome dialog / open directory."""
        # Try to open last directory
        last_dir = self.settings_store.get_last_directory()
        if last_dir and Path(last_dir).exists():
            self._scan_directory(Path(last_dir))
        else:
            QTimer.singleShot(100, self._show_open_dialog)

    def _show_open_dialog(self) -> None:
        """Show directory selection dialog."""
        last_dir = self.settings_store.get_last_directory()
        start_dir = last_dir if last_dir and Path(last_dir).exists() else str(Path.home())

        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Documentation Directory",
            start_dir,
        )

        if directory:
            self._scan_directory(Path(directory))

    def _show_settings_dialog(self) -> None:
        """Show the settings dialog."""
        dialog = SettingsDialog({}, self)
        dialog.exec()

    def _show_about(self) -> None:
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About File Curator",
            "File Curator v0.3.0 (Simplified)\n\n"
            "A lightweight tool for curating documentation files.\n"
            "Changes are saved directly to file metadata.\n\n"
            "Keyboard shortcuts:\n"
            "  A - Approve\n"
            "  R - Reject\n"
            "  S - Skip (next file)\n"
            "  E - Toggle editor\n"
            "  J/K - Navigate files\n"
            "  F5 - Rescan directory",
        )

    def _scan_directory(self, directory: Path) -> None:
        """Scan a directory for markdown files.

        Args:
            directory: Directory to scan
        """
        self.root_path = directory
        self.settings_store.set_last_directory(str(directory))

        self.markdown_viewer.set_loading()
        self.setWindowTitle(f"File Curator - {directory.name} (Scanning...)")

        # Scan files
        scanner = DeterministicScanner(
            directory,
            include_patterns=["**/*.md"],
            exclude_dirs={".git", "node_modules", "__pycache__", ".obsidian", "data"},
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
                file_item.file_description = parsed.description
                file_item.footer_metadata = parsed.footer_metadata
                # Links
                file_item.links = parsed.links

                # Set internal status based on file status
                if parsed.file_status == "Approved":
                    file_item.status = FileStatus.APPROVED
                elif parsed.file_status == "Rejected":
                    file_item.status = FileStatus.REJECTED
                else:
                    file_item.status = FileStatus.PENDING
            except Exception:
                pass

        self.all_files = files
        self.current_index = 0

        self._update_ui_after_scan()

        # Log
        self.logger.log_session_start(
            directory.name,
            f"Scanned {len(files)} files",
        )

    def _update_ui_after_scan(self) -> None:
        """Update UI after scanning."""
        if not self.all_files:
            self.setWindowTitle(f"File Curator - {self.root_path.name if self.root_path else 'No files'}")
            self.markdown_viewer.set_empty_message("No markdown files found.")
            self.action_bar.set_file_loaded(False)
            return

        self.setWindowTitle(f"File Curator - {self.root_path.name}")

        # Update progress
        self._update_progress()

        # Load file list
        self.file_list.set_files(self.all_files)

        # Find first pending file or just show first file
        pending_index = self._find_next_pending(0)
        if pending_index >= 0:
            self.current_index = pending_index
        else:
            self.current_index = 0

        self._load_current_file()

    def _update_progress(self) -> None:
        """Update progress display based on file statuses."""
        total = len(self.all_files)
        approved = sum(1 for f in self.all_files if f.file_status == "Approved")
        rejected = sum(1 for f in self.all_files if f.file_status == "Rejected")
        pending = total - approved - rejected

        # Create a simple session-like object for the progress header
        class SimpleProgress:
            pass

        progress = SimpleProgress()
        progress.name = self.root_path.name if self.root_path else "Files"
        progress.total_files = total
        progress.approved_count = approved
        progress.rejected_count = rejected
        progress.pending_count = pending

        self.progress_header.set_session(progress)

    def _find_next_pending(self, from_index: int) -> int:
        """Find the next pending file from a given index.

        Args:
            from_index: Index to start searching from

        Returns:
            Index of next pending file, or -1 if none found
        """
        for i in range(from_index, len(self.all_files)):
            if self.all_files[i].file_status in (None, "Review", ""):
                return i
        # Wrap around
        for i in range(0, from_index):
            if self.all_files[i].file_status in (None, "Review", ""):
                return i
        return -1

    def _load_current_file(self) -> None:
        """Load the file at current_index."""
        if not self.all_files or self.current_index >= len(self.all_files):
            self.current_file = None
            self.action_bar.set_file_loaded(False)
            self.markdown_viewer.set_empty_message("No file selected")
            return

        file_item = self.all_files[self.current_index]
        self._load_file(file_item)
        self.file_list.select_file(file_item.relative_path)

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
        self.logger.log_file_presented(
            file_item.relative_path,
            self.current_index + 1,
            len(self.all_files),
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
        # Find index of this file
        for i, f in enumerate(self.all_files):
            if f.relative_path == file_item.relative_path:
                self.current_index = i
                break
        self._load_file(file_item)

    def _on_approve(self) -> None:
        """Handle approve action."""
        if not self.current_file:
            return

        self._record_decision("Approved")

    def _on_reject(self) -> None:
        """Handle reject action."""
        if not self.current_file:
            return

        # Show rejection dialog for justification
        dialog = RejectionDialog(
            self.current_file.filename,
            require_justification=False,
            parent=self,
        )
        dialog.rejection_confirmed.connect(self._on_rejection_confirmed)
        dialog.exec()

    def _on_rejection_confirmed(self, justification: str) -> None:
        """Handle confirmed rejection.

        Args:
            justification: Rejection justification
        """
        self._record_decision("Rejected", justification=justification)

    def _on_skip(self) -> None:
        """Handle skip action - just move to next file."""
        if not self.current_file:
            return

        # Log skip
        self.logger.log_decision(
            "SKIPPED",
            self.current_file.relative_path,
            "",
        )

        # Move to next file
        self._advance_to_next()

    def _record_decision(
        self,
        new_status: str,
        justification: str = "",
    ) -> None:
        """Record a review decision by updating the file directly.

        Args:
            new_status: The new status ("Approved", "Rejected")
            justification: Optional justification for rejection
        """
        if not self.current_file:
            return

        file_item = self.current_file

        # Update the file's metadata directly
        success = update_file_status(file_item.path, new_status)

        if success:
            # Update local state
            file_item.file_status = new_status
            if new_status == "Approved":
                file_item.status = FileStatus.APPROVED
            elif new_status == "Rejected":
                file_item.status = FileStatus.REJECTED

            # Log the decision
            self.logger.log_decision(
                new_status.upper(),
                file_item.relative_path,
                justification,
            )

            # Update file list
            self.file_list.update_file_status(file_item.relative_path, file_item.status)

            # Update progress
            self._update_progress()

            # Advance to next file
            self._advance_to_next()
        else:
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to update file: {file_item.relative_path}",
            )

    def _advance_to_next(self) -> None:
        """Advance to the next pending file."""
        next_index = self._find_next_pending(self.current_index + 1)

        if next_index >= 0 and next_index != self.current_index:
            self.current_index = next_index
            self._load_current_file()
        else:
            # Check if all done
            pending_count = sum(
                1 for f in self.all_files
                if f.file_status in (None, "Review", "")
            )

            if pending_count == 0:
                self.markdown_viewer.set_empty_message(
                    "All files have been reviewed!\n\n"
                    "Session complete."
                )
                self.current_file = None
                self.action_bar.set_file_loaded(False)
                self.metadata_panel.set_file(None)

                # Log completion
                self.logger.log_session_complete(
                    self.root_path.name if self.root_path else "session"
                )
            else:
                # Just stay on current file
                pass

    def _select_next(self) -> None:
        """Select the next file in the list."""
        if self.current_index < len(self.all_files) - 1:
            self.current_index += 1
            self._load_current_file()

    def _select_previous(self) -> None:
        """Select the previous file in the list."""
        if self.current_index > 0:
            self.current_index -= 1
            self._load_current_file()

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

        # Rescan action
        rescan_action = QAction("Rescan Directory", self)
        rescan_action.triggered.connect(self._rescan)
        menu.addAction(rescan_action)

        # Show menu at button
        button = self.action_bar.tools_button
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def _rescan(self) -> None:
        """Rescan the current directory."""
        if self.root_path:
            self._scan_directory(self.root_path)

    def _filter_files(self, status_filter: Optional[str]) -> None:
        """Filter the file list by status.

        Args:
            status_filter: Status to filter by, or None to show all
        """
        if status_filter is None:
            self.file_list.set_files(self.all_files)
        else:
            filtered = [
                f for f in self.all_files
                if f.file_status == status_filter or
                   (status_filter == "Review" and f.file_status in (None, "", "Review"))
            ]
            self.file_list.set_files(filtered)

    def _run_validator(self) -> None:
        """Run the validator script on current file."""
        if not self.current_file or not self.root_path:
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
            working_dir=self.root_path,
        )

        action = executor.create_action(
            "carf_validator",
            args=["--file", self.current_file.relative_path],
            dry_run=False,
        )

        dialog = ScriptApprovalDialog(action, script_info, self)
        dialog.exec()

    def closeEvent(self, event) -> None:
        """Handle window close.

        Args:
            event: Close event
        """
        # Save window geometry
        geo = self.geometry()
        self.settings_store.set_window_geometry(geo.x(), geo.y(), geo.width(), geo.height())

        # Log session end
        if self.root_path:
            self.logger.log_session_end(self.root_path.name)

        event.accept()
