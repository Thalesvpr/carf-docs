"""CLI entry point for file-curator."""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config.settings import CuratorConfig
from .state.database import Database
from .state.repository import SessionRepository, FileRepository, ReviewRepository


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="file-curator",
        description="Professional GUI for curating documentation files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  file-curator                    Start GUI application
  file-curator --tui              Start TUI (text-based) interface
  file-curator --new audit-2026   Create new session named 'audit-2026'
  file-curator --resume abc123    Resume session with ID 'abc123'
  file-curator --list             List all sessions
  file-curator --stats abc123     Show stats for session
  file-curator --export abc123    Export session to JSON
        """,
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Root directory to curate (default: current directory)",
    )

    parser.add_argument(
        "--config",
        type=Path,
        help="Path to config file (YAML or JSON)",
    )

    parser.add_argument(
        "--tui",
        action="store_true",
        help="Use text-based TUI instead of GUI",
    )

    # Session management
    session_group = parser.add_mutually_exclusive_group()
    session_group.add_argument(
        "--new",
        metavar="NAME",
        help="Create a new session with the given name",
    )
    session_group.add_argument(
        "--resume",
        metavar="ID",
        help="Resume an existing session by ID",
    )
    session_group.add_argument(
        "--list",
        action="store_true",
        help="List all sessions",
    )

    # Reporting
    parser.add_argument(
        "--stats",
        metavar="ID",
        help="Show statistics for a session",
    )
    parser.add_argument(
        "--export",
        metavar="ID",
        help="Export session to JSON",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Output file for export (default: stdout)",
    )

    # Other options
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.2.0",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    # Load config
    config = CuratorConfig.load(args.config) if args.config else CuratorConfig()
    root_path = args.root.resolve()

    # Handle non-interactive commands
    if args.list:
        return cmd_list(root_path, config)

    if args.stats:
        return cmd_stats(root_path, config, args.stats)

    if args.export:
        return cmd_export(root_path, config, args.export, args.output)

    # Start TUI or GUI
    if args.tui:
        return cmd_tui(root_path, config, args.new, args.resume)
    else:
        return cmd_gui(root_path, config)


def cmd_list(root_path: Path, config: CuratorConfig) -> int:
    """List all sessions."""
    db_path = config.get_db_path(root_path)

    if not db_path.exists():
        print("No sessions found. Database does not exist.")
        return 0

    with Database(db_path) as db:
        repo = SessionRepository(db)
        sessions = repo.list_all()

        if not sessions:
            print("No sessions found.")
            return 0

        print(f"{'ID':<10} {'Name':<30} {'Progress':<15} {'Created':<12}")
        print("-" * 70)

        for session in sessions:
            decided = session.approved_count + session.rejected_count
            progress = f"{decided}/{session.total_files}"
            created = session.created_at.strftime("%Y-%m-%d")
            print(f"{session.id:<10} {session.name:<30} {progress:<15} {created:<12}")

    return 0


def cmd_stats(root_path: Path, config: CuratorConfig, session_id: str) -> int:
    """Show statistics for a session."""
    db_path = config.get_db_path(root_path)

    if not db_path.exists():
        print("Error: Database does not exist.")
        return 1

    with Database(db_path) as db:
        repo = SessionRepository(db)
        session = repo.get(session_id)

        if not session:
            print(f"Error: Session '{session_id}' not found.")
            return 1

        decided = session.approved_count + session.rejected_count
        progress_pct = (decided / session.total_files * 100) if session.total_files else 0

        print(f"Session: {session.name} ({session.id})")
        print(f"Root: {session.root_path}")
        print(f"Created: {session.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()
        print("Statistics:")
        print(f"  Total files:  {session.total_files}")
        print(f"  Approved:     {session.approved_count}")
        print(f"  Rejected:     {session.rejected_count}")
        print(f"  Skipped:      {session.skipped_count}")
        print(f"  Pending:      {session.pending_count}")
        print(f"  Progress:     {progress_pct:.1f}%")

        if session.completed_at:
            print(f"  Completed:    {session.completed_at.strftime('%Y-%m-%d %H:%M')}")

    return 0


def cmd_export(
    root_path: Path,
    config: CuratorConfig,
    session_id: str,
    output: Optional[Path],
) -> int:
    """Export session to JSON."""
    db_path = config.get_db_path(root_path)

    if not db_path.exists():
        print("Error: Database does not exist.", file=sys.stderr)
        return 1

    with Database(db_path) as db:
        session_repo = SessionRepository(db)
        file_repo = FileRepository(db)
        review_repo = ReviewRepository(db)

        session = session_repo.get(session_id)
        if not session:
            print(f"Error: Session '{session_id}' not found.", file=sys.stderr)
            return 1

        files = file_repo.list_by_session(session_id)
        reviews = review_repo.list_by_session(session_id)

        report = {
            "session": session.to_dict(),
            "files": [f.to_dict() for f in files],
            "reviews": [r.to_dict() for r in reviews],
            "exported_at": datetime.now().isoformat(),
        }

        json_output = json.dumps(report, indent=2)

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json_output, encoding="utf-8")
            print(f"Exported to {output}")
        else:
            print(json_output)

    return 0


def cmd_tui(
    root_path: Path,
    config: CuratorConfig,
    new_session: Optional[str],
    resume_session: Optional[str],
) -> int:
    """Start the TUI application."""
    try:
        from .tui.app import FileCuratorApp

        app = FileCuratorApp(
            root_path=root_path,
            config=config,
            session_id=resume_session,
            session_name=new_session,
        )

        app.run()
        return 0
    except ImportError as e:
        print(f"Error: TUI dependencies not available: {e}")
        print("Install with: pip install textual")
        return 1


def cmd_gui(root_path: Path, config: CuratorConfig) -> int:
    """Start the GUI application."""
    try:
        from .gui.app import main as gui_main

        # Use package-relative data directory (inside .scripts/file-curator/)
        # instead of CWD-relative to keep data in the right place
        package_dir = Path(__file__).parent.parent  # file-curator/
        data_dir = package_dir / "data"
        return gui_main(data_dir=data_dir, project_root=root_path)
    except ImportError as e:
        print(f"Error: GUI dependencies not available: {e}")
        print("Install with: pip install PySide6 markdown rich")
        return 1


if __name__ == "__main__":
    sys.exit(main())
