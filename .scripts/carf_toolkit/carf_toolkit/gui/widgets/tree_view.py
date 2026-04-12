"""Tree view widget showing folder hierarchy with files."""

from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTreeWidget,
    QTreeWidgetItem,
    QLabel,
    QFrame,
    QLineEdit,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QBrush, QIcon

from ...models.file_item import FileItem, FileStatus
from ..theme import COLORS


class TreeViewWidget(QFrame):
    """Widget displaying hierarchical folder/file tree."""

    file_selected = Signal(FileItem)
    file_double_clicked = Signal(FileItem)

    STATUS_ICONS = {
        FileStatus.PENDING: "○",  # Circle
        FileStatus.APPROVED: "✓",  # Checkmark
        FileStatus.REJECTED: "✗",  # X mark
        FileStatus.SKIPPED: "○",  # Circle (same as pending)
    }

    STATUS_COLORS = {
        FileStatus.PENDING: COLORS.status_pending,
        FileStatus.APPROVED: COLORS.status_approved,
        FileStatus.REJECTED: COLORS.status_rejected,
        FileStatus.SKIPPED: COLORS.status_skipped,
    }

    def __init__(self, parent: QWidget | None = None):
        """Initialize the tree view widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("treeFrame")
        self._files: dict[str, FileItem] = {}
        self._tree_items: dict[str, QTreeWidgetItem] = {}
        self._folder_items: dict[str, QTreeWidgetItem] = {}
        self._root_path: Optional[Path] = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Tree View")
        title.setObjectName("sectionTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Search/filter input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search files...")
        self.search_input.textChanged.connect(self._on_search_changed)
        layout.addWidget(self.search_input)

        # Tree widget
        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderHidden(True)
        self.tree_widget.setIndentation(16)
        self.tree_widget.setAnimated(False)
        self.tree_widget.setRootIsDecorated(False)  # Hide root decorations
        self.tree_widget.itemClicked.connect(self._on_item_clicked)
        self.tree_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.tree_widget.itemExpanded.connect(self._on_item_expanded)
        self.tree_widget.itemCollapsed.connect(self._on_item_collapsed)
        layout.addWidget(self.tree_widget)

        # Status summary
        self.status_summary = QLabel()
        self.status_summary.setObjectName("metadataLabel")
        self.status_summary.setWordWrap(True)
        layout.addWidget(self.status_summary)

    def set_root_path(self, root_path: Path) -> None:
        """Set the root path for the tree.

        Args:
            root_path: Root directory path
        """
        self._root_path = root_path

    def set_files(self, files: list[FileItem]) -> None:
        """Set the list of files to display.

        Args:
            files: List of FileItems
        """
        self.tree_widget.clear()
        self._files.clear()
        self._tree_items.clear()
        self._folder_items.clear()

        # Build tree structure
        for file_item in files:
            self._files[file_item.relative_path] = file_item
            self._add_file_to_tree(file_item)

        # Expand first two levels
        self._expand_to_level(2)

        self._update_counts()

    def _add_file_to_tree(self, file_item: FileItem) -> None:
        """Add a file to the tree.

        Args:
            file_item: FileItem to add
        """
        parts = Path(file_item.relative_path).parts

        # Build folder hierarchy
        parent = self.tree_widget.invisibleRootItem()
        current_path = ""

        for i, part in enumerate(parts[:-1]):
            current_path = str(Path(current_path) / part) if current_path else part

            if current_path not in self._folder_items:
                folder_item = QTreeWidgetItem(parent)
                folder_item.setText(0, f"▸ {part}")  # Simple arrow
                folder_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "folder", "path": current_path})
                folder_item.setForeground(0, QBrush(QColor(COLORS.text_secondary)))
                self._folder_items[current_path] = folder_item
            else:
                folder_item = self._folder_items[current_path]

            parent = folder_item

        # Add file
        filename = parts[-1]
        icon = self.STATUS_ICONS.get(file_item.status, "○")
        display_text = f"{icon} {filename}"

        file_tree_item = QTreeWidgetItem(parent)
        file_tree_item.setText(0, display_text)
        file_tree_item.setData(0, Qt.ItemDataRole.UserRole, {"type": "file", "path": file_item.relative_path})
        file_tree_item.setToolTip(0, file_item.relative_path)

        # Set color based on status
        color = self.STATUS_COLORS.get(file_item.status, COLORS.text_primary)
        file_tree_item.setForeground(0, QBrush(QColor(color)))

        self._tree_items[file_item.relative_path] = file_tree_item

    def _expand_to_level(self, level: int) -> None:
        """Expand tree items to a specific level.

        Args:
            level: Maximum depth to expand
        """
        def expand_item(item: QTreeWidgetItem, current_level: int):
            if current_level < level:
                item.setExpanded(True)
                for i in range(item.childCount()):
                    expand_item(item.child(i), current_level + 1)

        for i in range(self.tree_widget.topLevelItemCount()):
            expand_item(self.tree_widget.topLevelItem(i), 0)

    def update_file_status(self, relative_path: str, status: FileStatus) -> None:
        """Update the status of a file.

        Args:
            relative_path: Path to the file
            status: New status
        """
        if relative_path not in self._tree_items:
            return

        tree_item = self._tree_items[relative_path]
        file_item = self._files.get(relative_path)

        if file_item:
            file_item.status = status

        # Update display
        filename = Path(relative_path).name
        icon = self.STATUS_ICONS.get(status, "○")
        tree_item.setText(0, f"{icon} {filename}")

        color = self.STATUS_COLORS.get(status, COLORS.text_primary)
        tree_item.setForeground(0, QBrush(QColor(color)))

        self._update_counts()

    def select_file(self, relative_path: str) -> None:
        """Select a file in the tree.

        Args:
            relative_path: Path to select
        """
        if relative_path in self._tree_items:
            item = self._tree_items[relative_path]
            self.tree_widget.setCurrentItem(item)
            self.tree_widget.scrollToItem(item)

            # Expand parents
            parent = item.parent()
            while parent:
                parent.setExpanded(True)
                parent = parent.parent()

    def get_selected_file(self) -> FileItem | None:
        """Get the currently selected file.

        Returns:
            Selected FileItem or None
        """
        current = self.tree_widget.currentItem()
        if current:
            data = current.data(0, Qt.ItemDataRole.UserRole)
            if data and data.get("type") == "file":
                return self._files.get(data.get("path"))
        return None

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        """Handle item click.

        Args:
            item: Clicked item
            column: Column index
        """
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data.get("type") == "file":
            file_item = self._files.get(data.get("path"))
            if file_item:
                self.file_selected.emit(file_item)

    def _on_item_double_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        """Handle item double-click.

        Args:
            item: Double-clicked item
            column: Column index
        """
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data.get("type") == "file":
            file_item = self._files.get(data.get("path"))
            if file_item:
                self.file_double_clicked.emit(file_item)
        elif data and data.get("type") == "folder":
            # Toggle expansion
            item.setExpanded(not item.isExpanded())

    def _on_item_expanded(self, item: QTreeWidgetItem) -> None:
        """Handle item expansion.

        Args:
            item: Expanded item
        """
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data.get("type") == "folder":
            text = item.text(0)
            if text.startswith("▸"):  # Right arrow
                item.setText(0, "▾" + text[1:])  # Down arrow

    def _on_item_collapsed(self, item: QTreeWidgetItem) -> None:
        """Handle item collapse.

        Args:
            item: Collapsed item
        """
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data and data.get("type") == "folder":
            text = item.text(0)
            if text.startswith("▾"):  # Down arrow
                item.setText(0, "▸" + text[1:])  # Right arrow

    def _on_search_changed(self, text: str) -> None:
        """Handle search text change.

        Args:
            text: Search text
        """
        search_text = text.lower().strip()

        def filter_item(item: QTreeWidgetItem) -> bool:
            """Recursively filter tree items."""
            data = item.data(0, Qt.ItemDataRole.UserRole)

            if data and data.get("type") == "file":
                path = data.get("path", "").lower()
                matches = not search_text or search_text in path
                item.setHidden(not matches)
                return matches
            else:
                # Folder - show if any child matches
                any_visible = False
                for i in range(item.childCount()):
                    if filter_item(item.child(i)):
                        any_visible = True
                item.setHidden(not any_visible)
                if any_visible:
                    item.setExpanded(True)
                return any_visible

        for i in range(self.tree_widget.topLevelItemCount()):
            filter_item(self.tree_widget.topLevelItem(i))

    def _update_counts(self) -> None:
        """Update the count labels."""
        total = len(self._files)

        approved = sum(
            1 for f in self._files.values()
            if f.status == FileStatus.APPROVED
        )
        rejected = sum(
            1 for f in self._files.values()
            if f.status == FileStatus.REJECTED
        )
        pending = sum(
            1 for f in self._files.values()
            if f.status == FileStatus.PENDING
        )
        skipped = sum(
            1 for f in self._files.values()
            if f.status == FileStatus.SKIPPED
        )

        self.status_summary.setText(
            f"{total} files | \u2713 {approved}  \u2717 {rejected}  \u25cb {pending}  \u25b7 {skipped}"
        )

    def select_next_pending(self) -> FileItem | None:
        """Select the next pending or skipped file.

        Returns:
            The selected FileItem or None
        """
        for relative_path, file_item in self._files.items():
            if file_item.status in (FileStatus.PENDING, FileStatus.SKIPPED):
                self.select_file(relative_path)
                return file_item
        return None
