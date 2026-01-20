"""Main application window for CARF Toolkit."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSplitter,
    QStackedWidget,
    QMessageBox,
    QMenu,
    QFileDialog,
)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QKeySequence, QShortcut

from ..models.file_item import FileItem, FileStatus, ValidationIssue
from ..scanner.discovery import DeterministicScanner
from ..scanner.parser import ContentParser, update_file_status, update_file_metadata
from ..integration.validator_bridge import ValidatorBridge
from ..integration.tree_sync_bridge import TreeSyncBridge

from .widgets import (
    TreeViewWidget,
    MarkdownViewer,
    MarkdownEditor,
    CombinedRightPanel,
    ActionBar,
    ProgressHeader,
)
from .dialogs import (
    ExportDialog,
    RejectionDialog,
    SyncPreviewDialog,
)
from .theme import COLORS
from .settings_store import SettingsStore


class MainWindow(QMainWindow):
    """Main application window with tree view, preview, and metadata panels."""

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
        self.settings_store = SettingsStore(data_dir / "settings.json")

        # Current state
        self.root_path: Optional[Path] = project_root
        self.all_files: list[FileItem] = []
        self.current_index: int = 0
        self.current_file: Optional[FileItem] = None
        self.content_parser = ContentParser()

        # Integration bridges
        self.validator_bridge = ValidatorBridge()
        self.tree_sync_bridge = TreeSyncBridge()

        self._setup_ui()
        self._setup_shortcuts()
        self._setup_menu()

        # If project_root provided, scan immediately
        if project_root:
            QTimer.singleShot(100, lambda: self._scan_directory(project_root))

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        self.setWindowTitle("CARF Toolkit")
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

        # Left panel - tree view
        self.tree_view = TreeViewWidget()
        self.tree_view.setMinimumWidth(250)
        self.tree_view.setMaximumWidth(400)
        self.tree_view.file_selected.connect(self._on_file_selected)
        self.tree_view.file_double_clicked.connect(self._on_file_double_clicked)
        content_splitter.addWidget(self.tree_view)

        # Center - stacked widget for viewer/editor
        self.center_stack = QStackedWidget()

        # Viewer mode (real file content)
        self.markdown_viewer = MarkdownViewer()
        self.center_stack.addWidget(self.markdown_viewer)

        # Editor mode
        self.markdown_editor = MarkdownEditor()
        self.markdown_editor.save_requested.connect(self._on_editor_save)
        self.center_stack.addWidget(self.markdown_editor)

        content_splitter.addWidget(self.center_stack)

        # Right panel - combined info + validation
        self.right_panel = CombinedRightPanel()
        self.right_panel.setMinimumWidth(280)
        self.right_panel.setMaximumWidth(400)
        self.right_panel.status_changed.connect(self._on_status_changed_from_panel)
        self.right_panel.description_changed.connect(self._on_description_changed)
        self.right_panel.issue_clicked.connect(self._on_issue_clicked)
        self.right_panel.validate_requested.connect(self._on_validate_file)
        content_splitter.addWidget(self.right_panel)

        # Set splitter sizes
        content_splitter.setSizes([280, 750, 320])

        main_layout.addWidget(content_splitter, 1)

        # Action bar
        self.action_bar = ActionBar()
        self.action_bar.approve_clicked.connect(self._on_approve)
        self.action_bar.reject_clicked.connect(self._on_reject)
        self.action_bar.skip_clicked.connect(self._on_skip)
        self.action_bar.edit_clicked.connect(self._on_edit)
        self.action_bar.sync_clicked.connect(self._on_sync_tree)
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
        QShortcut(QKeySequence("A"), self).activated.connect(self._on_approve)

        # Reject - R
        QShortcut(QKeySequence("R"), self).activated.connect(self._on_reject)

        # Skip - S
        QShortcut(QKeySequence("S"), self).activated.connect(self._on_skip)

        # Edit - E
        QShortcut(QKeySequence("E"), self).activated.connect(self._on_edit)

        # Navigate - J/K (vim-like)
        QShortcut(QKeySequence("J"), self).activated.connect(self._select_next)
        QShortcut(QKeySequence("K"), self).activated.connect(self._select_previous)

        # Escape - exit editor mode
        QShortcut(QKeySequence("Escape"), self).activated.connect(self._exit_editor)

        # Validate - V
        QShortcut(QKeySequence("V"), self).activated.connect(self._on_validate_file)

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

        export_action = QAction("Export Data...", self)
        export_action.setShortcut(QKeySequence("Ctrl+E"))
        export_action.triggered.connect(self._show_export_dialog)
        file_menu.addAction(export_action)

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

        # Tools menu
        tools_menu = menubar.addMenu("Tools")

        validate_action = QAction("Validate Current File", self)
        validate_action.setShortcut(QKeySequence("V"))
        validate_action.triggered.connect(self._on_validate_file)
        tools_menu.addAction(validate_action)

        validate_all_action = QAction("Validate All Files", self)
        validate_all_action.triggered.connect(self._on_validate_all)
        tools_menu.addAction(validate_all_action)

        tools_menu.addSeparator()

        sync_tree_action = QAction("Sync Tree (README only)", self)
        sync_tree_action.triggered.connect(self._on_sync_tree)
        tools_menu.addAction(sync_tree_action)

        sync_all_action = QAction("Sync All READMEs", self)
        sync_all_action.triggered.connect(self._on_sync_all)
        tools_menu.addAction(sync_all_action)

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

    def _show_export_dialog(self) -> None:
        """Show the export dialog."""
        if not self.all_files:
            QMessageBox.information(self, "Export", "No files to export.")
            return

        dialog = ExportDialog(self.all_files, self.root_path, self)
        dialog.exec()

    def _show_about(self) -> None:
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About CARF Toolkit",
            "CARF Toolkit v0.1.0\n\n"
            "Unified documentation tool integrating:\n"
            "- carf_validator for validation\n"
            "- carf_tree_sync for README tree sync\n\n"
            "Keyboard shortcuts:\n"
            "  A - Approve\n"
            "  R - Reject\n"
            "  S - Skip (next file)\n"
            "  E - Toggle editor\n"
            "  V - Validate file\n"
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

        # Update bridges
        self.validator_bridge.set_root_path(directory)
        self.tree_sync_bridge.set_root_path(directory)
        self.tree_view.set_root_path(directory)

        self.markdown_viewer.set_loading()
        self.setWindowTitle(f"CARF Toolkit - {directory.name} (Scanning...)")

        # Scan files
        scanner = DeterministicScanner(
            directory,
            include_patterns=["**/*.md"],
            exclude_dirs={".git", "node_modules", "__pycache__", ".obsidian", "data", ".scripts"},
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
                file_item.file_status = parsed.file_status
                file_item.file_last_updated = parsed.last_updated
                file_item.file_description = parsed.description
                file_item.footer_metadata = parsed.footer_metadata
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

    def _update_ui_after_scan(self) -> None:
        """Update UI after scanning."""
        if not self.all_files:
            self.setWindowTitle(f"CARF Toolkit - {self.root_path.name if self.root_path else 'No files'}")
            self.markdown_viewer.set_empty_message("No markdown files found.")
            self.action_bar.set_file_loaded(False)
            return

        self.setWindowTitle(f"CARF Toolkit - {self.root_path.name}")

        # Update progress
        self._update_progress()

        # Load tree view
        self.tree_view.set_files(self.all_files)

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
        """Find the next pending file from a given index."""
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
        self.tree_view.select_file(file_item.relative_path)

    def _load_file(self, file_item: FileItem) -> None:
        """Load a file for review - shows full file content.

        Args:
            file_item: File to load
        """
        self.current_file = file_item
        self.action_bar.set_file_loaded(True)
        self.action_bar.set_is_readme(file_item.is_readme)

        # Load REAL file content (not template)
        try:
            content = file_item.path.read_text(encoding="utf-8")
            self.markdown_viewer.set_markdown(content)
            self.markdown_editor.set_content(content)
        except Exception as e:
            self.markdown_viewer.set_error(str(e))

        # Update right panel
        self.right_panel.set_file(file_item)

        self.file_changed.emit(file_item)

    def _on_file_selected(self, file_item: FileItem) -> None:
        """Handle file selection from tree.

        Args:
            file_item: Selected file
        """
        # Find index of this file
        for i, f in enumerate(self.all_files):
            if f.relative_path == file_item.relative_path:
                self.current_index = i
                break
        self._load_file(file_item)

    def _on_file_double_clicked(self, file_item: FileItem) -> None:
        """Handle file double-click (open in external editor)."""
        import subprocess
        import platform

        try:
            if platform.system() == "Windows":
                subprocess.Popen(["start", "", str(file_item.path)], shell=True)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", str(file_item.path)])
            else:
                subprocess.Popen(["xdg-open", str(file_item.path)])
        except Exception:
            pass

    def _on_approve(self) -> None:
        """Handle approve action."""
        if not self.current_file:
            return
        self._record_decision("Approved")

    def _on_reject(self) -> None:
        """Handle reject action."""
        if not self.current_file:
            return

        dialog = RejectionDialog(
            self.current_file.filename,
            require_justification=False,
            parent=self,
        )
        dialog.rejection_confirmed.connect(self._on_rejection_confirmed)
        dialog.exec()

    def _on_rejection_confirmed(self, justification: str) -> None:
        """Handle confirmed rejection."""
        self._record_decision("Rejected", justification=justification)

    def _on_skip(self) -> None:
        """Handle skip action - just move to next file."""
        if not self.current_file:
            return
        self._advance_to_next()

    def _record_decision(self, new_status: str, justification: str = "") -> None:
        """Record a review decision by updating the file directly."""
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

            # Update tree view
            self.tree_view.update_file_status(file_item.relative_path, file_item.status)

            # Update progress
            self._update_progress()

            # Refresh right panel
            self.right_panel.refresh()

            # Advance to next file
            self._advance_to_next()
        else:
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to update file: {file_item.relative_path}",
            )

    def _on_status_changed_from_panel(self, new_status: str) -> None:
        """Handle status change from info panel dropdown."""
        if not self.current_file:
            return

        success = update_file_status(self.current_file.path, new_status)
        if success:
            self.current_file.file_status = new_status
            if new_status == "Approved":
                self.current_file.status = FileStatus.APPROVED
            elif new_status == "Rejected":
                self.current_file.status = FileStatus.REJECTED
            else:
                self.current_file.status = FileStatus.PENDING

            self.tree_view.update_file_status(self.current_file.relative_path, self.current_file.status)
            self._update_progress()

    def _on_description_changed(self, new_description: str) -> None:
        """Handle description change from info panel."""
        if not self.current_file:
            return

        success = update_file_metadata(self.current_file.path, {"Descricao": new_description})
        if success:
            self.current_file.file_description = new_description

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
                    "All files have been reviewed!\n\nSession complete."
                )
                self.current_file = None
                self.action_bar.set_file_loaded(False)
                self.right_panel.set_file(None)

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
            self.center_stack.setCurrentIndex(1)
        else:
            self._exit_editor()

    def _exit_editor(self) -> None:
        """Exit editor mode."""
        if self.center_stack.currentIndex() == 1:
            self.center_stack.setCurrentIndex(0)

    def _on_editor_save(self) -> None:
        """Handle editor save - save to actual file."""
        if not self.current_file:
            return

        content = self.markdown_editor.get_content()

        try:
            self.current_file.path.write_text(content, encoding="utf-8")
            self.markdown_viewer.set_markdown(content)

            # Re-parse the file
            parsed = self.content_parser.parse(self.current_file.path)
            self.current_file.title = parsed.title
            self.current_file.word_count = parsed.word_count
            self.current_file.links = parsed.links

            self.right_panel.refresh()
            self._exit_editor()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save file: {e}")

    def _on_validate_file(self) -> None:
        """Validate the current file."""
        if not self.current_file or not self.root_path:
            return

        if not self.validator_bridge.is_available:
            QMessageBox.information(
                self,
                "Validator",
                "carf_validator is not available.\n"
                "Make sure it's installed in the scripts directory.",
            )
            return

        issues = self.validator_bridge.validate_file(self.current_file)
        self.current_file.validation_issues = issues
        self.right_panel.show_validation_issues(issues)

    def _on_validate_all(self) -> None:
        """Validate all files."""
        if not self.validator_bridge.is_available:
            QMessageBox.information(
                self,
                "Validator",
                "carf_validator is not available.",
            )
            return

        result = self.validator_bridge.run_full_validation()

        if "error" in result:
            QMessageBox.warning(self, "Validation Error", result["error"])
        else:
            QMessageBox.information(
                self,
                "Validation Complete",
                f"Scanned {result['total_files']} files\n"
                f"Errors: {result['total_errors']}\n"
                f"Warnings: {result['total_warnings']}",
            )

    def _on_issue_clicked(self, issue: ValidationIssue) -> None:
        """Handle click on a validation issue - scroll to line."""
        if issue.line_number:
            self.markdown_viewer.scroll_to_line(issue.line_number)

    def _on_sync_tree(self) -> None:
        """Sync tree for current README file."""
        if not self.current_file or not self.current_file.is_readme:
            QMessageBox.information(
                self,
                "Sync Tree",
                "Tree sync is only available for README files.",
            )
            return

        if not self.tree_sync_bridge.is_available:
            QMessageBox.information(
                self,
                "Tree Sync",
                "carf_tree_sync is not available.",
            )
            return

        preview = self.tree_sync_bridge.preview_sync(self.current_file.path)

        if preview is None:
            QMessageBox.information(self, "Sync Tree", "Cannot sync this file.")
            return

        dialog = SyncPreviewDialog(preview, self)
        dialog.sync_confirmed.connect(self._apply_sync)
        dialog.exec()

    def _apply_sync(self) -> None:
        """Apply the tree sync."""
        if not self.current_file:
            return

        success, message = self.tree_sync_bridge.apply_sync(self.current_file.path)

        if success:
            # Reload the file
            self._load_file(self.current_file)
        else:
            QMessageBox.warning(self, "Sync Error", message)

    def _on_sync_all(self) -> None:
        """Sync all README files."""
        if not self.tree_sync_bridge.is_available:
            QMessageBox.information(self, "Tree Sync", "carf_tree_sync is not available.")
            return

        result = self.tree_sync_bridge.sync_all(dry_run=False)

        if "error" in result:
            QMessageBox.warning(self, "Sync Error", result["error"])
        else:
            QMessageBox.information(
                self,
                "Sync Complete",
                f"Processed {result['total_nodes']} nodes\n"
                f"Updated: {result['updated_nodes']}\n"
                f"Unchanged: {result['unchanged_nodes']}",
            )
            # Rescan to refresh
            self._rescan()

    def _on_tools(self) -> None:
        """Show tools menu."""
        menu = QMenu(self)

        validate_action = QAction("Validate File (V)", self)
        validate_action.triggered.connect(self._on_validate_file)
        menu.addAction(validate_action)

        menu.addSeparator()

        export_action = QAction("Export Data...", self)
        export_action.triggered.connect(self._show_export_dialog)
        menu.addAction(export_action)

        menu.addSeparator()

        rescan_action = QAction("Rescan Directory (F5)", self)
        rescan_action.triggered.connect(self._rescan)
        menu.addAction(rescan_action)

        button = self.action_bar.tools_button
        menu.exec(button.mapToGlobal(button.rect().bottomLeft()))

    def _rescan(self) -> None:
        """Rescan the current directory."""
        if self.root_path:
            self._scan_directory(self.root_path)

    def _filter_files(self, status_filter: Optional[str]) -> None:
        """Filter the tree view by status."""
        if status_filter is None:
            self.tree_view.set_files(self.all_files)
        else:
            filtered = [
                f for f in self.all_files
                if f.file_status == status_filter or
                   (status_filter == "Review" and f.file_status in (None, "", "Review"))
            ]
            self.tree_view.set_files(filtered)

    def closeEvent(self, event) -> None:
        """Handle window close."""
        # Save window geometry
        geo = self.geometry()
        self.settings_store.set_window_geometry(geo.x(), geo.y(), geo.width(), geo.height())
        event.accept()
