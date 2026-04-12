"""File list widget showing the curation queue."""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QFrame,
    QHBoxLayout,
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor, QBrush

from ...models.file_item import FileItem, FileStatus
from ..theme import COLORS


class FileListItem(QListWidgetItem):
    """Custom list item for file display."""

    STATUS_ICONS = {
        FileStatus.PENDING: "\u25cb",  # Circle
        FileStatus.APPROVED: "\u2713",  # Checkmark
        FileStatus.REJECTED: "\u2717",  # X mark
        FileStatus.SKIPPED: "\u25b7",  # Right triangle
    }

    STATUS_COLORS = {
        FileStatus.PENDING: COLORS.status_pending,
        FileStatus.APPROVED: COLORS.status_approved,
        FileStatus.REJECTED: COLORS.status_rejected,
        FileStatus.SKIPPED: COLORS.status_skipped,
    }

    def __init__(self, file_item: FileItem):
        """Initialize the list item.

        Args:
            file_item: The FileItem to display
        """
        self.file_item = file_item
        icon = self.STATUS_ICONS.get(file_item.status, "\u25cb")
        display_name = file_item.path.name
        super().__init__(f"{icon}  {display_name}")

        # Set tooltip with full path
        self.setToolTip(file_item.relative_path)

        # Set color based on status
        color = self.STATUS_COLORS.get(file_item.status, COLORS.text_primary)
        self.setForeground(QBrush(QColor(color)))

    def update_status(self, status: FileStatus) -> None:
        """Update the displayed status.

        Args:
            status: New status
        """
        self.file_item.status = status
        icon = self.STATUS_ICONS.get(status, "\u25cb")
        display_name = self.file_item.path.name
        self.setText(f"{icon}  {display_name}")

        color = self.STATUS_COLORS.get(status, COLORS.text_primary)
        self.setForeground(QBrush(QColor(color)))


class FileListWidget(QFrame):
    """Widget displaying the file curation queue."""

    file_selected = Signal(FileItem)
    file_double_clicked = Signal(FileItem)

    def __init__(self, parent: QWidget | None = None):
        """Initialize the file list widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("fileListFrame")
        self._items: dict[str, FileListItem] = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("Queue")
        title.setObjectName("sectionTitle")
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.count_label = QLabel("0 files")
        self.count_label.setObjectName("metadataLabel")
        header_layout.addWidget(self.count_label)

        layout.addLayout(header_layout)

        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setSpacing(2)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self.list_widget)

        # Status summary
        self.status_summary = QLabel()
        self.status_summary.setObjectName("metadataLabel")
        self.status_summary.setWordWrap(True)
        layout.addWidget(self.status_summary)

    def set_files(self, files: list[FileItem]) -> None:
        """Set the list of files to display.

        Args:
            files: List of FileItems
        """
        self.list_widget.clear()
        self._items.clear()

        for file_item in files:
            list_item = FileListItem(file_item)
            self.list_widget.addItem(list_item)
            self._items[file_item.relative_path] = list_item

        self._update_counts()

    def add_file(self, file_item: FileItem) -> None:
        """Add a single file to the list.

        Args:
            file_item: FileItem to add
        """
        list_item = FileListItem(file_item)
        self.list_widget.addItem(list_item)
        self._items[file_item.relative_path] = list_item
        self._update_counts()

    def update_file_status(self, relative_path: str, status: FileStatus) -> None:
        """Update the status of a file.

        Args:
            relative_path: Path to the file
            status: New status
        """
        if relative_path in self._items:
            self._items[relative_path].update_status(status)
            self._update_counts()

    def select_file(self, relative_path: str) -> None:
        """Select a file in the list.

        Args:
            relative_path: Path to select
        """
        if relative_path in self._items:
            item = self._items[relative_path]
            self.list_widget.setCurrentItem(item)
            self.list_widget.scrollToItem(item)

    def get_selected_file(self) -> FileItem | None:
        """Get the currently selected file.

        Returns:
            Selected FileItem or None
        """
        current = self.list_widget.currentItem()
        if isinstance(current, FileListItem):
            return current.file_item
        return None

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        """Handle item click.

        Args:
            item: Clicked item
        """
        if isinstance(item, FileListItem):
            self.file_selected.emit(item.file_item)

    def _on_item_double_clicked(self, item: QListWidgetItem) -> None:
        """Handle item double-click.

        Args:
            item: Double-clicked item
        """
        if isinstance(item, FileListItem):
            self.file_double_clicked.emit(item.file_item)

    def _update_counts(self) -> None:
        """Update the count labels."""
        total = self.list_widget.count()
        self.count_label.setText(f"{total} files")

        # Count by status
        approved = sum(
            1
            for item in self._items.values()
            if item.file_item.status == FileStatus.APPROVED
        )
        rejected = sum(
            1
            for item in self._items.values()
            if item.file_item.status == FileStatus.REJECTED
        )
        pending = sum(
            1
            for item in self._items.values()
            if item.file_item.status == FileStatus.PENDING
        )
        skipped = sum(
            1
            for item in self._items.values()
            if item.file_item.status == FileStatus.SKIPPED
        )

        self.status_summary.setText(
            f"\u2713 {approved}  \u2717 {rejected}  \u25cb {pending}  \u25b7 {skipped}"
        )

    def select_next_pending(self) -> FileItem | None:
        """Select the next pending or skipped file.

        Returns:
            The selected FileItem or None
        """
        for item in self._items.values():
            if item.file_item.status in (FileStatus.PENDING, FileStatus.SKIPPED):
                self.list_widget.setCurrentItem(item)
                self.list_widget.scrollToItem(item)
                return item.file_item
        return None
