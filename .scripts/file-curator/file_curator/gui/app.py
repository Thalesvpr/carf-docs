"""Main application entry point for File Curator GUI."""

import sys
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .main_window import MainWindow
from .theme import get_stylesheet
from ..state.database import Database


def _get_package_data_dir() -> Path:
    """Get the data directory relative to the package installation."""
    # Get the directory where this module is located
    module_dir = Path(__file__).parent.parent.parent  # file-curator/
    return module_dir / "data"


class FileCuratorApp:
    """File Curator application manager."""

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
        self.project_root = project_root or Path.cwd()

        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        (self.data_dir / "sessions").mkdir(exist_ok=True)
        (self.data_dir / "logs").mkdir(exist_ok=True)

        # Database path
        self.db_path = self.data_dir / "curator.db"

        self.app: Optional[QApplication] = None
        self.main_window: Optional[MainWindow] = None
        self.db: Optional[Database] = None

    def run(self) -> int:
        """Run the application.

        Returns:
            Exit code
        """
        # Create Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("File Curator")
        self.app.setApplicationVersion("0.2.0")
        self.app.setOrganizationName("CARF Project")

        # Set application-wide font
        font = QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        self.app.setFont(font)

        # Apply stylesheet
        self.app.setStyleSheet(get_stylesheet())

        # Initialize database
        self.db = Database(self.db_path)
        self.db.initialize()

        # Create main window
        self.main_window = MainWindow(self.db, self.data_dir)
        self.main_window.show()

        # Show welcome dialog
        self.main_window.show_welcome()

        # Run event loop
        return self.app.exec()

    def cleanup(self) -> None:
        """Clean up resources."""
        if self.db:
            self.db.close()


def main(data_dir: Optional[Path] = None, project_root: Optional[Path] = None) -> int:
    """Main entry point for the GUI application.

    Args:
        data_dir: Optional data directory path
        project_root: Optional project root path

    Returns:
        Exit code
    """
    app = FileCuratorApp(data_dir, project_root)
    try:
        return app.run()
    finally:
        app.cleanup()
