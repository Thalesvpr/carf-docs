"""Progress header showing session info and progress."""

from typing import Any

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
)
from PySide6.QtCore import Qt

from ..theme import COLORS


class ProgressHeader(QFrame):
    """Header widget showing session progress."""

    def __init__(self, parent: QWidget | None = None):
        """Initialize the progress header.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("headerFrame")
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(16)

        # Left side - session info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)

        self.title_label = QLabel("CARF Toolkit")
        self.title_label.setObjectName("headerTitle")
        info_layout.addWidget(self.title_label)

        self.subtitle_label = QLabel("No directory loaded")
        self.subtitle_label.setObjectName("headerSubtitle")
        info_layout.addWidget(self.subtitle_label)

        layout.addLayout(info_layout)

        layout.addStretch()

        # Center - progress bar
        progress_layout = QVBoxLayout()
        progress_layout.setSpacing(4)

        progress_top = QHBoxLayout()
        self.progress_label = QLabel("Progress")
        self.progress_label.setObjectName("metadataLabel")
        progress_top.addWidget(self.progress_label)

        progress_top.addStretch()

        self.progress_count = QLabel("0/0")
        self.progress_count.setObjectName("metadataLabel")
        progress_top.addWidget(self.progress_count)

        progress_layout.addLayout(progress_top)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setMinimumWidth(300)
        self.progress_bar.setMaximumHeight(8)
        progress_layout.addWidget(self.progress_bar)

        layout.addLayout(progress_layout)

        layout.addStretch()

        # Right side - stats
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(24)

        # Approved
        approved_layout = QVBoxLayout()
        approved_layout.setSpacing(2)
        self.approved_count = QLabel("0")
        self.approved_count.setStyleSheet(
            f"color: {COLORS.accent_approve}; font-size: 18px; font-weight: 600;"
        )
        self.approved_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        approved_layout.addWidget(self.approved_count)
        approved_label = QLabel("Approved")
        approved_label.setObjectName("metadataLabel")
        approved_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        approved_layout.addWidget(approved_label)
        stats_layout.addLayout(approved_layout)

        # Rejected
        rejected_layout = QVBoxLayout()
        rejected_layout.setSpacing(2)
        self.rejected_count = QLabel("0")
        self.rejected_count.setStyleSheet(
            f"color: {COLORS.accent_reject}; font-size: 18px; font-weight: 600;"
        )
        self.rejected_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rejected_layout.addWidget(self.rejected_count)
        rejected_label = QLabel("Rejected")
        rejected_label.setObjectName("metadataLabel")
        rejected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rejected_layout.addWidget(rejected_label)
        stats_layout.addLayout(rejected_layout)

        # Remaining
        remaining_layout = QVBoxLayout()
        remaining_layout.setSpacing(2)
        self.remaining_count = QLabel("0")
        self.remaining_count.setStyleSheet(
            f"color: {COLORS.text_secondary}; font-size: 18px; font-weight: 600;"
        )
        self.remaining_count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        remaining_layout.addWidget(self.remaining_count)
        remaining_label = QLabel("Remaining")
        remaining_label.setObjectName("metadataLabel")
        remaining_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        remaining_layout.addWidget(remaining_label)
        stats_layout.addLayout(remaining_layout)

        layout.addLayout(stats_layout)

    def set_session(self, session: Any) -> None:
        """Set the session/progress info to display.

        Args:
            session: Object with name, root_path (optional), total_files,
                     approved_count, rejected_count, pending_count attributes
        """
        if session is None:
            self.title_label.setText("CARF Toolkit")
            self.subtitle_label.setText("No directory loaded")
            self.progress_bar.setValue(0)
            self.progress_count.setText("0/0")
            self.approved_count.setText("0")
            self.rejected_count.setText("0")
            self.remaining_count.setText("0")
            return

        self.title_label.setText(session.name)
        root_path = getattr(session, "root_path", None)
        self.subtitle_label.setText(str(root_path) if root_path else "")
        self.update_progress(session)

    def update_progress(self, session: Any) -> None:
        """Update progress display.

        Args:
            session: Object with total_files, approved_count, rejected_count, pending_count
        """
        total = session.total_files
        decided = session.approved_count + session.rejected_count
        skipped = getattr(session, "skipped_count", 0)
        remaining = session.pending_count + skipped

        self.progress_bar.setMaximum(total if total > 0 else 1)
        self.progress_bar.setValue(decided)
        self.progress_count.setText(f"{decided}/{total}")
        self.approved_count.setText(str(session.approved_count))
        self.rejected_count.setText(str(session.rejected_count))
        self.remaining_count.setText(str(remaining))

    def set_progress(
        self,
        total: int,
        approved: int,
        rejected: int,
        pending: int,
        skipped: int,
    ) -> None:
        """Set progress values directly.

        Args:
            total: Total files
            approved: Approved count
            rejected: Rejected count
            pending: Pending count
            skipped: Skipped count
        """
        decided = approved + rejected
        remaining = pending + skipped

        self.progress_bar.setMaximum(total if total > 0 else 1)
        self.progress_bar.setValue(decided)
        self.progress_count.setText(f"{decided}/{total}")
        self.approved_count.setText(str(approved))
        self.rejected_count.setText(str(rejected))
        self.remaining_count.setText(str(remaining))
