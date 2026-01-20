"""CLI entry point for CARF Toolkit."""

import argparse
import sys
from pathlib import Path


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="carf-toolkit",
        description="Unified documentation toolkit with validation and tree sync",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  carf-toolkit                    Start GUI application
  carf-toolkit --root ./docs      Start with specific directory
  carf-toolkit --scan ./CENTRAL   Scan CENTRAL directory on startup

Features:
  - Full markdown preview with syntax highlighting
  - Tree view navigation with folder hierarchy
  - Integrated validation from carf_validator
  - Tree sync from carf_tree_sync
  - Export data to JSON, CSV, or Markdown
        """,
    )

    parser.add_argument(
        "--root", "-r",
        type=Path,
        default=None,
        help="Directory to open (opens file dialog if not specified)",
    )

    parser.add_argument(
        "--scan", "-s",
        type=Path,
        help="Alias for --root",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
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

        # Use package-relative data directory
        package_dir = Path(__file__).parent.parent  # carf_toolkit/
        data_dir = package_dir / "data"

        return gui_main(data_dir=data_dir, project_root=root_path)
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("Install with: pip install PySide6 markdown rich pyyaml")
        return 1


if __name__ == "__main__":
    sys.exit(main())
