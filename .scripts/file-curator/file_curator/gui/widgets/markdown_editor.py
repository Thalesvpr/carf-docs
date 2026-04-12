"""Split-pane Markdown editor with live preview."""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QPlainTextEdit,
    QFrame,
    QLabel,
    QPushButton,
)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextDocument

from .markdown_viewer import MarkdownViewer
from ..theme import COLORS


class MarkdownHighlighter(QSyntaxHighlighter):
    """Simple syntax highlighter for Markdown."""

    def __init__(self, document: QTextDocument):
        """Initialize the highlighter.

        Args:
            document: Document to highlight
        """
        super().__init__(document)
        self._setup_formats()

    def _setup_formats(self) -> None:
        """Set up text formats for different elements."""
        # Heading format
        self.heading_format = QTextCharFormat()
        self.heading_format.setFontWeight(QFont.Weight.Bold)
        self.heading_format.setForeground(QColor(COLORS.accent_approve))

        # Bold format
        self.bold_format = QTextCharFormat()
        self.bold_format.setFontWeight(QFont.Weight.Bold)
        self.bold_format.setForeground(QColor(COLORS.text_primary))

        # Italic format
        self.italic_format = QTextCharFormat()
        self.italic_format.setFontItalic(True)
        self.italic_format.setForeground(QColor(COLORS.text_secondary))

        # Code format
        self.code_format = QTextCharFormat()
        self.code_format.setFontFamily("JetBrains Mono")
        self.code_format.setBackground(QColor(COLORS.background))
        self.code_format.setForeground(QColor(COLORS.accent_skip))

        # Link format
        self.link_format = QTextCharFormat()
        self.link_format.setForeground(QColor(COLORS.accent_approve))
        self.link_format.setFontUnderline(True)

    def highlightBlock(self, text: str) -> None:
        """Highlight a block of text.

        Args:
            text: Text to highlight
        """
        # Headings
        if text.startswith("#"):
            self.setFormat(0, len(text), self.heading_format)
            return

        # Process inline elements
        i = 0
        while i < len(text):
            # Code blocks (backticks)
            if text[i] == "`":
                end = text.find("`", i + 1)
                if end > i:
                    self.setFormat(i, end - i + 1, self.code_format)
                    i = end + 1
                    continue

            # Bold (**text**)
            if text[i : i + 2] == "**":
                end = text.find("**", i + 2)
                if end > i:
                    self.setFormat(i, end - i + 2, self.bold_format)
                    i = end + 2
                    continue

            # Italic (*text*)
            if text[i] == "*" and (i == 0 or text[i - 1] != "*"):
                end = text.find("*", i + 1)
                if end > i and text[end : end + 1] != "*":
                    self.setFormat(i, end - i + 1, self.italic_format)
                    i = end + 1
                    continue

            # Links [text](url)
            if text[i] == "[":
                bracket_end = text.find("]", i)
                if bracket_end > i and text[bracket_end + 1 : bracket_end + 2] == "(":
                    paren_end = text.find(")", bracket_end)
                    if paren_end > bracket_end:
                        self.setFormat(i, paren_end - i + 1, self.link_format)
                        i = paren_end + 1
                        continue

            i += 1


class MarkdownEditor(QFrame):
    """Split-pane Markdown editor with live preview."""

    content_changed = Signal(str)
    save_requested = Signal()

    def __init__(self, parent: QWidget | None = None):
        """Initialize the editor.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("editorFrame")
        self._debounce_timer = QTimer()
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.setInterval(300)
        self._debounce_timer.timeout.connect(self._update_preview)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QFrame()
        toolbar.setStyleSheet(
            f"background-color: {COLORS.surface}; "
            f"border-bottom: 1px solid {COLORS.divider};"
        )
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("Edit Review")
        title.setObjectName("sectionTitle")
        toolbar_layout.addWidget(title)

        toolbar_layout.addStretch()

        self.save_button = QPushButton("Save")
        self.save_button.setObjectName("toolButton")
        self.save_button.clicked.connect(self.save_requested.emit)
        toolbar_layout.addWidget(self.save_button)

        layout.addWidget(toolbar)

        # Splitter for editor and preview
        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        # Editor pane
        editor_frame = QFrame()
        editor_frame.setStyleSheet("border: none;")
        editor_layout = QVBoxLayout(editor_frame)
        editor_layout.setContentsMargins(0, 0, 0, 0)
        editor_layout.setSpacing(0)

        # Editor label
        editor_label = QLabel("Markdown")
        editor_label.setObjectName("metadataLabel")
        editor_label.setStyleSheet(
            f"padding: 8px 12px; background-color: {COLORS.background};"
        )
        editor_layout.addWidget(editor_label)

        # Text editor
        self.editor = QPlainTextEdit()
        self.editor.setFont(QFont("JetBrains Mono", 12))
        self.editor.setTabStopDistance(32)
        self.editor.textChanged.connect(self._on_text_changed)
        self._highlighter = MarkdownHighlighter(self.editor.document())
        editor_layout.addWidget(self.editor)

        self.splitter.addWidget(editor_frame)

        # Preview pane
        preview_frame = QFrame()
        preview_frame.setStyleSheet("border: none;")
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        preview_layout.setSpacing(0)

        # Preview label
        preview_label = QLabel("Preview")
        preview_label.setObjectName("metadataLabel")
        preview_label.setStyleSheet(
            f"padding: 8px 12px; background-color: {COLORS.background};"
        )
        preview_layout.addWidget(preview_label)

        # Markdown viewer
        self.preview = MarkdownViewer()
        preview_layout.addWidget(self.preview)

        self.splitter.addWidget(preview_frame)

        # Set initial sizes (50/50)
        self.splitter.setSizes([500, 500])

        layout.addWidget(self.splitter)

    def set_content(self, content: str) -> None:
        """Set the editor content.

        Args:
            content: Markdown content
        """
        self.editor.setPlainText(content)
        self.preview.set_markdown(content)

    def get_content(self) -> str:
        """Get the current editor content.

        Returns:
            Markdown content
        """
        return self.editor.toPlainText()

    def clear(self) -> None:
        """Clear the editor."""
        self.editor.clear()
        self.preview.clear()

    def _on_text_changed(self) -> None:
        """Handle text changes with debouncing."""
        self._debounce_timer.start()

    def _update_preview(self) -> None:
        """Update the preview pane."""
        content = self.editor.toPlainText()
        self.preview.set_markdown(content)
        self.content_changed.emit(content)

    def set_read_only(self, read_only: bool) -> None:
        """Set whether the editor is read-only.

        Args:
            read_only: True to make read-only
        """
        self.editor.setReadOnly(read_only)
        self.save_button.setEnabled(not read_only)
