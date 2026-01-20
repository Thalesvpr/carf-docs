"""Markdown viewer widget using QWebEngineView."""

import markdown
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl, Qt

from ..theme import get_markdown_css


class MarkdownViewer(QFrame):
    """Widget for rendering Markdown content beautifully."""

    def __init__(self, parent: QWidget | None = None):
        """Initialize the Markdown viewer.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("previewFrame")
        self._markdown = markdown.Markdown(
            extensions=[
                "tables",
                "fenced_code",
                "codehilite",
                "toc",
                "nl2br",
                "sane_lists",
            ],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "guess_lang": False,
                }
            },
        )
        self._css = get_markdown_css()
        self._current_content = ""
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the UI components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Web view for rendering
        self.web_view = QWebEngineView()
        self.web_view.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        # Configure settings
        settings = self.web_view.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)  # For scroll support
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)

        layout.addWidget(self.web_view)

        # Set initial empty content
        self.set_markdown("")

    def set_markdown(self, content: str) -> None:
        """Set and render markdown content.

        Args:
            content: Markdown string to render
        """
        self._current_content = content
        self._markdown.reset()
        html_content = self._markdown.convert(content)
        self._set_html(html_content)

    def set_html(self, html: str) -> None:
        """Set raw HTML content.

        Args:
            html: HTML string to display
        """
        self._set_html(html)

    def _set_html(self, body: str) -> None:
        """Set HTML with styling.

        Args:
            body: HTML body content
        """
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
{self._css}
    </style>
    <script>
        function scrollToLine(lineNumber) {{
            // Find elements that might contain line references
            var elements = document.querySelectorAll('[data-line]');
            for (var i = 0; i < elements.length; i++) {{
                if (elements[i].dataset.line == lineNumber) {{
                    elements[i].scrollIntoView({{ behavior: 'smooth', block: 'center' }});
                    elements[i].classList.add('highlight-line');
                    setTimeout(function() {{
                        elements[i].classList.remove('highlight-line');
                    }}, 3000);
                    return;
                }}
            }}
            // Fallback: scroll by estimated line height
            var lineHeight = 24;
            window.scrollTo({{ top: (lineNumber - 1) * lineHeight, behavior: 'smooth' }});
        }}
    </script>
</head>
<body>
{body}
</body>
</html>"""
        self.web_view.setHtml(html, QUrl("file:///"))

    def scroll_to_line(self, line_number: int) -> None:
        """Scroll to a specific line number.

        Args:
            line_number: Line number to scroll to
        """
        self.web_view.page().runJavaScript(f"scrollToLine({line_number});")

    def clear(self) -> None:
        """Clear the viewer content."""
        self.set_markdown("")

    def set_loading(self) -> None:
        """Show a loading state."""
        self._set_html(
            '<p style="text-align: center; color: #a0a0a0; padding-top: 100px;">'
            "Loading...</p>"
        )

    def set_empty_message(self, message: str = "No file selected") -> None:
        """Show an empty state message.

        Args:
            message: Message to display
        """
        # Replace newlines with <br> for proper display
        formatted_message = message.replace("\n", "<br>")
        self._set_html(
            f'<p style="text-align: center; color: #a0a0a0; padding-top: 100px;">'
            f"{formatted_message}</p>"
        )

    def set_error(self, error: str) -> None:
        """Show an error message.

        Args:
            error: Error message to display
        """
        self._set_html(
            f'<div style="background-color: #2a1a1a; border: 1px solid #e94560; '
            f'border-radius: 8px; padding: 16px; margin: 24px;">'
            f'<h3 style="color: #e94560; margin-top: 0;">Error</h3>'
            f"<p>{error}</p></div>"
        )
