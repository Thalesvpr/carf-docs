"""Theme definitions and styling for CARF Toolkit GUI."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ColorPalette:
    """Dark gray theme color palette - soft and easy on the eyes."""

    # Backgrounds - soft dark grays
    background: str = "#1e1e1e"
    surface: str = "#2d2d2d"
    surface_light: str = "#3d3d3d"

    # Primary colors - neutral gray-blue
    primary: str = "#4a4a4a"
    primary_hover: str = "#5a5a5a"
    primary_pressed: str = "#3a3a3a"

    # Accent colors - softer, more pleasant
    accent_approve: str = "#4ade80"
    accent_approve_hover: str = "#22c55e"
    accent_reject: str = "#f87171"
    accent_reject_hover: str = "#ef4444"
    accent_skip: str = "#fbbf24"
    accent_skip_hover: str = "#f59e0b"
    accent_info: str = "#60a5fa"

    # Text colors - clean whites and grays
    text_primary: str = "#ffffff"
    text_secondary: str = "#a1a1a1"
    text_muted: str = "#6b6b6b"

    # Border and dividers
    border: str = "#404040"
    border_light: str = "#505050"
    divider: str = "#333333"

    # Status colors
    status_pending: str = "#6b7280"
    status_approved: str = "#4ade80"
    status_rejected: str = "#f87171"
    status_skipped: str = "#fbbf24"

    # Scrollbar
    scrollbar_bg: str = "#2d2d2d"
    scrollbar_handle: str = "#4a4a4a"
    scrollbar_handle_hover: str = "#5a5a5a"


# Default palette instance
COLORS = ColorPalette()


def get_stylesheet() -> str:
    """Generate the complete Qt stylesheet."""
    return f"""
/* Main Application */
QMainWindow, QWidget {{
    background-color: {COLORS.background};
    color: {COLORS.text_primary};
    font-family: "Inter", "Segoe UI", "SF Pro Display", sans-serif;
    font-size: 14px;
}}

/* Panels and Frames */
QFrame {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 8px;
}}

QFrame#fileListFrame, QFrame#metadataFrame, QFrame#treeFrame {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 8px;
    padding: 8px;
}}

QFrame#previewFrame {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 8px;
}}

/* Header */
QFrame#headerFrame {{
    background-color: {COLORS.surface};
    border: none;
    border-bottom: 1px solid {COLORS.divider};
    border-radius: 0px;
    padding: 12px 16px;
}}

/* Labels */
QLabel {{
    color: {COLORS.text_primary};
    background: transparent;
    border: none;
}}

QLabel#headerTitle {{
    font-size: 18px;
    font-weight: 600;
    color: {COLORS.text_primary};
}}

QLabel#headerSubtitle {{
    font-size: 13px;
    color: {COLORS.text_secondary};
}}

QLabel#sectionTitle {{
    font-size: 12px;
    font-weight: 600;
    color: {COLORS.text_secondary};
    text-transform: uppercase;
    letter-spacing: 1px;
}}

QLabel#metadataLabel {{
    font-size: 12px;
    color: {COLORS.text_secondary};
}}

QLabel#metadataValue {{
    font-size: 13px;
    color: {COLORS.text_primary};
}}

/* Buttons */
QPushButton {{
    background-color: {COLORS.primary};
    color: {COLORS.text_primary};
    border: none;
    border-radius: 6px;
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
}}

QPushButton:hover {{
    background-color: {COLORS.primary_hover};
}}

QPushButton:pressed {{
    background-color: {COLORS.primary_pressed};
}}

QPushButton:disabled {{
    background-color: {COLORS.border};
    color: {COLORS.text_muted};
}}

QPushButton#approveButton {{
    background-color: #22c55e;
    color: #ffffff;
    font-weight: 700;
    font-size: 14px;
    border: none;
}}

QPushButton#approveButton:hover {{
    background-color: #16a34a;
}}

QPushButton#rejectButton {{
    background-color: #ef4444;
    color: #ffffff;
    font-weight: 700;
    font-size: 14px;
    border: none;
}}

QPushButton#rejectButton:hover {{
    background-color: #dc2626;
}}

QPushButton#skipButton {{
    background-color: #f59e0b;
    color: #ffffff;
    font-weight: 700;
    font-size: 14px;
    border: none;
}}

QPushButton#skipButton:hover {{
    background-color: #d97706;
}}

QPushButton#toolButton {{
    background-color: transparent;
    border: 1px solid {COLORS.border};
    padding: 8px 16px;
}}

QPushButton#toolButton:hover {{
    background-color: {COLORS.surface_light};
    border-color: {COLORS.border_light};
}}

QPushButton#syncButton {{
    background-color: #3b82f6;
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#syncButton:hover {{
    background-color: #2563eb;
}}

QPushButton#validateButton {{
    background-color: #8b5cf6;
    color: #ffffff;
    font-weight: 600;
}}

QPushButton#validateButton:hover {{
    background-color: #7c3aed;
}}

/* Progress Bar */
QProgressBar {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 4px;
    height: 8px;
    text-align: center;
}}

QProgressBar::chunk {{
    background-color: {COLORS.accent_approve};
    border-radius: 3px;
}}

/* Tree Widget - Minimalist */
QTreeWidget {{
    background-color: {COLORS.surface};
    border: none;
    border-radius: 6px;
    outline: none;
}}

QTreeWidget::item {{
    padding: 4px 4px;
    border: none;
    margin: 0;
}}

QTreeWidget::item:selected {{
    background-color: {COLORS.primary};
}}

QTreeWidget::item:hover:!selected {{
    background-color: {COLORS.surface_light};
}}

/* Hide all branch indicators */
QTreeWidget::branch {{
    background: transparent;
    border: none;
    image: none;
}}

QTreeWidget::branch:has-children:closed {{
    image: none;
}}

QTreeWidget::branch:has-children:open {{
    image: none;
}}

/* List Widget */
QListWidget {{
    background-color: {COLORS.surface};
    border: none;
    border-radius: 6px;
    outline: none;
}}

QListWidget::item {{
    padding: 8px 12px;
    border-radius: 4px;
    margin: 2px 4px;
}}

QListWidget::item:selected {{
    background-color: {COLORS.primary};
}}

QListWidget::item:hover:!selected {{
    background-color: {COLORS.surface_light};
}}

/* Scroll Areas */
QScrollArea {{
    background-color: transparent;
    border: none;
}}

QScrollBar:vertical {{
    background-color: {COLORS.scrollbar_bg};
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}}

QScrollBar::handle:vertical {{
    background-color: {COLORS.scrollbar_handle};
    border-radius: 4px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: {COLORS.scrollbar_handle_hover};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background-color: {COLORS.scrollbar_bg};
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}}

QScrollBar::handle:horizontal {{
    background-color: {COLORS.scrollbar_handle};
    border-radius: 4px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background-color: {COLORS.scrollbar_handle_hover};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* Text Edit / Plain Text Edit */
QPlainTextEdit, QTextEdit {{
    background-color: {COLORS.surface};
    color: {COLORS.text_primary};
    border: 1px solid {COLORS.border};
    border-radius: 6px;
    padding: 8px;
    font-family: "JetBrains Mono", "Consolas", "Monaco", monospace;
    font-size: 13px;
}}

QPlainTextEdit:focus, QTextEdit:focus {{
    border-color: {COLORS.primary_hover};
}}

/* Line Edit */
QLineEdit {{
    background-color: {COLORS.surface};
    color: {COLORS.text_primary};
    border: 1px solid {COLORS.border};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
}}

QLineEdit:focus {{
    border-color: {COLORS.primary_hover};
}}

QLineEdit::placeholder {{
    color: {COLORS.text_muted};
}}

/* Combo Box */
QComboBox {{
    background-color: {COLORS.surface};
    color: {COLORS.text_primary};
    border: 1px solid {COLORS.border};
    border-radius: 6px;
    padding: 8px 12px;
    font-size: 14px;
}}

QComboBox:hover {{
    border-color: {COLORS.border_light};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 6px;
    selection-background-color: {COLORS.primary};
}}

/* Splitter */
QSplitter::handle {{
    background-color: {COLORS.divider};
}}

QSplitter::handle:horizontal {{
    width: 2px;
}}

QSplitter::handle:vertical {{
    height: 2px;
}}

/* Tab Widget */
QTabWidget::pane {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 6px;
    margin-top: -1px;
}}

QTabBar::tab {{
    background-color: {COLORS.background};
    color: {COLORS.text_secondary};
    border: 1px solid {COLORS.border};
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    padding: 8px 16px;
    margin-right: 2px;
}}

QTabBar::tab:selected {{
    background-color: {COLORS.surface};
    color: {COLORS.text_primary};
}}

QTabBar::tab:hover:!selected {{
    background-color: {COLORS.surface_light};
}}

/* Dialog */
QDialog {{
    background-color: {COLORS.background};
}}

/* Menu */
QMenu {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 6px;
    padding: 4px;
}}

QMenu::item {{
    padding: 8px 24px;
    border-radius: 4px;
}}

QMenu::item:selected {{
    background-color: {COLORS.primary};
}}

/* Tooltips */
QToolTip {{
    background-color: {COLORS.surface};
    color: {COLORS.text_primary};
    border: 1px solid {COLORS.border};
    border-radius: 4px;
    padding: 6px 10px;
    font-size: 12px;
}}

/* Group Box */
QGroupBox {{
    background-color: {COLORS.surface};
    border: 1px solid {COLORS.border};
    border-radius: 8px;
    margin-top: 16px;
    padding: 16px;
    font-weight: 600;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: {COLORS.text_secondary};
}}

/* Check Box */
QCheckBox {{
    color: {COLORS.text_primary};
    spacing: 8px;
}}

QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border: 2px solid {COLORS.border};
    border-radius: 4px;
    background-color: {COLORS.surface};
}}

QCheckBox::indicator:checked {{
    background-color: {COLORS.accent_approve};
    border-color: {COLORS.accent_approve};
}}

QCheckBox::indicator:hover {{
    border-color: {COLORS.border_light};
}}

/* Status Bar */
QStatusBar {{
    background-color: {COLORS.surface};
    border-top: 1px solid {COLORS.divider};
    color: {COLORS.text_secondary};
    font-size: 12px;
}}

QStatusBar::item {{
    border: none;
}}
"""


def get_markdown_css() -> str:
    """Generate CSS for markdown rendering in QWebEngineView."""
    return f"""
body {{
    background-color: {COLORS.surface};
    color: {COLORS.text_primary};
    font-family: "Inter", "Segoe UI", "SF Pro Display", -apple-system, sans-serif;
    font-size: 15px;
    line-height: 1.7;
    padding: 24px;
    margin: 0;
    max-width: 100%;
}}

h1, h2, h3, h4, h5, h6 {{
    color: {COLORS.text_primary};
    font-weight: 600;
    margin-top: 24px;
    margin-bottom: 16px;
    line-height: 1.25;
}}

h1 {{
    font-size: 2em;
    border-bottom: 1px solid {COLORS.border};
    padding-bottom: 0.3em;
}}

h2 {{
    font-size: 1.5em;
    border-bottom: 1px solid {COLORS.border};
    padding-bottom: 0.3em;
}}

h3 {{
    font-size: 1.25em;
}}

h4 {{
    font-size: 1em;
}}

p {{
    margin-top: 0;
    margin-bottom: 16px;
}}

a {{
    color: {COLORS.accent_approve};
    text-decoration: none;
}}

a:hover {{
    text-decoration: underline;
}}

code {{
    background-color: {COLORS.background};
    border: 1px solid {COLORS.border};
    border-radius: 4px;
    padding: 2px 6px;
    font-family: "JetBrains Mono", "Consolas", "Monaco", monospace;
    font-size: 0.9em;
}}

pre {{
    background-color: {COLORS.background};
    border: 1px solid {COLORS.border};
    border-radius: 8px;
    padding: 16px;
    overflow-x: auto;
    line-height: 1.45;
}}

pre code {{
    background-color: transparent;
    border: none;
    padding: 0;
    font-size: 13px;
}}

blockquote {{
    border-left: 4px solid {COLORS.primary};
    margin: 16px 0;
    padding: 0 16px;
    color: {COLORS.text_secondary};
}}

ul, ol {{
    margin-top: 0;
    margin-bottom: 16px;
    padding-left: 2em;
}}

li {{
    margin-bottom: 4px;
}}

li > ul, li > ol {{
    margin-top: 4px;
    margin-bottom: 0;
}}

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 16px 0;
}}

th, td {{
    border: 1px solid {COLORS.border};
    padding: 8px 12px;
    text-align: left;
}}

th {{
    background-color: {COLORS.background};
    font-weight: 600;
}}

tr:nth-child(even) {{
    background-color: rgba(255, 255, 255, 0.02);
}}

hr {{
    border: none;
    border-top: 1px solid {COLORS.border};
    margin: 24px 0;
}}

img {{
    max-width: 100%;
    height: auto;
    border-radius: 8px;
}}

/* Task lists */
input[type="checkbox"] {{
    margin-right: 8px;
}}

/* Status badges */
.status-approved {{
    background-color: {COLORS.accent_approve};
    color: #1a1a2e;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.85em;
}}

.status-rejected {{
    background-color: {COLORS.accent_reject};
    color: #ffffff;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.85em;
}}

.status-pending {{
    background-color: {COLORS.status_pending};
    color: #ffffff;
    padding: 2px 8px;
    border-radius: 4px;
    font-weight: 600;
    font-size: 0.85em;
}}

/* Selection */
::selection {{
    background-color: {COLORS.primary};
    color: {COLORS.text_primary};
}}

/* Line highlighting for scroll-to-line feature */
.highlight-line {{
    background-color: rgba(251, 191, 36, 0.2);
    display: block;
    padding: 2px 0;
    margin: 0 -24px;
    padding-left: 24px;
    padding-right: 24px;
}}
"""
