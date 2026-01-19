"""CLI entry point for file-curator - Simplified version."""

import argparse
import sys
from pathlib import Path

from .config.settings import CuratorConfig


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="file-curator",
        description="Lightweight GUI for curating documentation files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  file-curator                    Start GUI application
  file-curator --root ./docs      Start with specific directory
  file-curator --scan ./CENTRAL   Scan CENTRAL directory on startup

Files are curated by updating their metadata footer directly:
  **Status:** Review/Approved/Rejected
  **Atualizado:** YYYY-MM-DD
  **Descrição:** optional description
        """,
    )

    parser.add_argument(
        "--root", "-r",
        type=Path,
        default=None,
        help="Directory to curate (opens file dialog if not specified)",
    )

    parser.add_argument(
        "--scan", "-s",
        type=Path,
        help="Alias for --root",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.3.0",
    )

    args = parser.parse_args()

    # Get root path from args
    root_path = args.root or args.scan

    # Start GUI
    return cmd_gui(root_path)


def cmd_gui(root_path: Path | None) -> int:
    """Start the GUI application."""
    try:
        from .gui.app import main as gui_main

        # Use package-relative data directory (inside .scripts/file-curator/)
        package_dir = Path(__file__).parent.parent  # file-curator/
        data_dir = package_dir / "data"

        return gui_main(data_dir=data_dir, project_root=root_path)
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("Install with: pip install PySide6 markdown rich pyyaml")
        return 1


if __name__ == "__main__":
    sys.exit(main())
