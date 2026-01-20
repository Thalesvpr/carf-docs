"""Main application entry point for CARF Toolkit GUI."""

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .main_window import MainWindow
from .theme import get_stylesheet


def _get_package_data_dir() -> Path:
    """Get the data directory relative to the package installation."""
    module_dir = Path(__file__).parent.parent.parent  # carf_toolkit/
    return module_dir / "data"


class CARFToolkitApp:
    """CARF Toolkit application manager."""

    def __init__(
        self,
        data_dir: Optional[Path] = None,
        project_root: Optional[Path] = None,
    ):
        """Initialize the application.

        Args:
            data_dir: Path to data directory
            project_root: Project root path for file scanning
        """
        self.data_dir = data_dir or _get_package_data_dir()
        self.project_root = project_root

        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.app: Optional[QApplication] = None
        self.main_window: Optional[MainWindow] = None

    def run(self) -> int:
        """Run the application.

        Returns:
            Exit code
        """
        # Create Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("CARF Toolkit")
        self.app.setApplicationVersion("0.1.0")
        self.app.setOrganizationName("CARF Project")

        # Set application-wide font
        font = QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        self.app.setFont(font)

        # Apply stylesheet
        self.app.setStyleSheet(get_stylesheet())

        # Create main window
        self.main_window = MainWindow(
            data_dir=self.data_dir,
            project_root=self.project_root,
        )
        self.main_window.show()

        # Show welcome dialog
        self.main_window.show_welcome()

        # Run event loop
        return self.app.exec()


def main(data_dir: Optional[Path] = None, project_root: Optional[Path] = None) -> int:
    """Main entry point for the GUI application.

    Args:
        data_dir: Optional data directory path
        project_root: Optional project root path

    Returns:
        Exit code
    """
    app = CARFToolkitApp(data_dir, project_root)
    return app.run()
