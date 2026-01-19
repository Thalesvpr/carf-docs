"""Main Textual application for File Curator."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Static, Footer, Header

from ..config.settings import CuratorConfig
from ..models.file_item import FileItem, FileStatus
from ..models.session import CurationSession, SessionConfig
from ..models.review import ReviewRecord, ReviewDecision
from ..scanner.discovery import DeterministicScanner
from ..scanner.enricher import FileEnricher
from ..state.database import Database
from ..state.repository import SessionRepository, FileRepository, ReviewRepository
from ..state.queue import CurationQueue
from ..templates.renderer import TemplateRenderer
from ..actions.scripts import SafeExecutor

from .screens.welcome import WelcomeScreen
from .screens.curation import CurationScreen
from .screens.editor import EditorScreen, RejectEditorScreen
from .screens.script_approval import ScriptApprovalScreen, ScriptResultScreen
from .screens.progress import ProgressScreen
from .screens.completion import CompletionScreen


class FileCuratorApp(App):
    """Main Textual application for file curation."""

    TITLE = "File Curator"
    SUB_TITLE = "Interactive documentation curation"

    CSS_PATH = "styles/curator.tcss"

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", show=False),
    ]

    def __init__(
        self,
        root_path: Path,
        config: Optional[CuratorConfig] = None,
        session_id: Optional[str] = None,
        session_name: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.root_path = root_path.resolve()
        self.config = config or CuratorConfig()
        self.initial_session_id = session_id
        self.initial_session_name = session_name

        # Initialize components
        self.db: Optional[Database] = None
        self.session_repo: Optional[SessionRepository] = None
        self.file_repo: Optional[FileRepository] = None
        self.review_repo: Optional[ReviewRepository] = None
        self.queue: Optional[CurationQueue] = None
        self.enricher = FileEnricher()
        self.renderer = TemplateRenderer()
        self.executor = SafeExecutor()

        # Current state
        self.current_session: Optional[CurationSession] = None
        self.current_item: Optional[FileItem] = None
        self._edit_values: dict[str, Any] = {}

    def compose(self) -> ComposeResult:
        """Compose the app."""
        yield Header()
        yield Static("Loading...", id="main-content")
        yield Footer()

    async def on_mount(self) -> None:
        """Handle app mount."""
        # Initialize database
        db_path = self.config.get_db_path(self.root_path)
        self.db = Database(db_path)
        self.db.initialize()

        # Initialize repositories
        self.session_repo = SessionRepository(self.db)
        self.file_repo = FileRepository(self.db)
        self.review_repo = ReviewRepository(self.db)

        # Show appropriate screen
        if self.initial_session_id:
            # Resume existing session
            await self._resume_session(self.initial_session_id)
        elif self.initial_session_name:
            # Create new session with given name
            await self._create_session(self.initial_session_name)
        else:
            # Show welcome screen
            await self._show_welcome()

    async def _show_welcome(self) -> None:
        """Show the welcome screen."""
        sessions = self.session_repo.list_all() if self.session_repo else []
        result = await self.push_screen_wait(WelcomeScreen(sessions=sessions))

        if result["action"] == "new":
            await self._create_session(result["name"])
        elif result["action"] == "resume":
            await self._resume_session(result["session_id"])
        elif result["action"] == "quit":
            self.exit()

    async def _create_session(self, name: str) -> None:
        """Create a new curation session."""
        if not self.session_repo or not self.file_repo:
            return

        # Create session
        session_config = SessionConfig(
            include_patterns=self.config.scan.include_patterns,
            exclude_dirs=self.config.scan.exclude_dirs,
            require_observations=self.config.review.require_observations,
            require_justification_on_reject=self.config.review.require_justification_on_reject,
            skip_returns_to_queue=self.config.review.skip_returns_to_queue,
        )
        session = CurationSession.create(name, self.root_path, session_config)
        self.session_repo.create(session)

        # Scan files
        scanner = DeterministicScanner(
            self.root_path,
            include_patterns=session_config.include_patterns,
            exclude_dirs=session_config.exclude_dirs,
        )
        files = scanner.scan()

        # Enrich files
        files = self.enricher.enrich_all(files)

        # Save files to database
        self.file_repo.create_many(session.id, files)

        # Update session counts
        self.session_repo.update_counts(session.id)
        session = self.session_repo.get(session.id)

        if session:
            self.current_session = session
            self.queue = CurationQueue(self.db, session.id)
            await self._show_curation()

    async def _resume_session(self, session_id: str) -> None:
        """Resume an existing session."""
        if not self.session_repo:
            return

        session = self.session_repo.get(session_id)
        if not session:
            await self._show_welcome()
            return

        self.current_session = session
        self.queue = CurationQueue(self.db, session.id)

        # Check if complete
        if session.is_complete:
            await self._show_completion()
        else:
            await self._show_curation()

    async def _show_curation(self) -> None:
        """Show the main curation screen."""
        if not self.queue or not self.current_session:
            return

        # Get next item
        self.current_item = self.queue.get_next()
        if not self.current_item:
            await self._show_completion()
            return

        # Get preview
        preview = self.enricher.get_content_preview(self.current_item)

        # Get upcoming items
        upcoming = self.queue.peek(10)

        result = await self.push_screen_wait(
            CurationScreen(
                session=self.current_session,
                current_item=self.current_item,
                upcoming_items=upcoming,
                content_preview=preview,
            )
        )

        await self._handle_curation_result(result)

    async def _handle_curation_result(self, result: dict) -> None:
        """Handle result from curation screen."""
        action = result.get("action")

        if action == "approve":
            await self._handle_approve(result)
        elif action == "reject_request":
            await self._show_reject_editor(result)
        elif action == "skip":
            await self._handle_skip(result)
        elif action == "edit":
            await self._show_editor(result)
        elif action == "validate":
            await self._handle_validate(result)
        elif action == "sync":
            await self._handle_sync(result)
        elif action == "progress":
            await self._show_progress()
        elif action == "help":
            await self._show_help()
        elif action == "save":
            self._save_state()
            await self._show_curation()
        elif action == "quit":
            self._save_state()
            self.exit()

    async def _handle_approve(self, result: dict) -> None:
        """Handle approve action."""
        if not self.queue or not self.file_repo or not self.review_repo or not self.current_session:
            return

        item = result.get("item")
        if not item:
            return

        # Create review record
        review = ReviewRecord(
            file_path=item.path,
            session_id=self.current_session.id,
            decision=ReviewDecision.APPROVED,
            observations=result.get("observations", ""),
            tags=result.get("tags", []),
        )

        # Save review
        file_id = self.file_repo.get_file_id(self.current_session.id, item.relative_path)
        if file_id:
            self.review_repo.create(file_id, review)

        # Update status
        self.queue.mark_decided(item.relative_path, FileStatus.APPROVED)
        self.session_repo.update_counts(self.current_session.id)
        self.current_session = self.session_repo.get(self.current_session.id)

        # Continue curation
        await self._show_curation()

    async def _handle_skip(self, result: dict) -> None:
        """Handle skip action."""
        if not self.queue or not self.current_session:
            return

        item = result.get("item")
        if not item:
            return

        self.queue.mark_decided(item.relative_path, FileStatus.SKIPPED)
        self.session_repo.update_counts(self.current_session.id)
        self.current_session = self.session_repo.get(self.current_session.id)

        await self._show_curation()

    async def _show_reject_editor(self, result: dict) -> None:
        """Show editor for rejection justification."""
        item = result.get("item")
        if not item:
            return

        editor_result = await self.push_screen_wait(
            RejectEditorScreen(
                file_path=item.relative_path,
                observations=self._edit_values.get("observations", ""),
                tags=self._edit_values.get("tags", []),
            )
        )

        if editor_result["action"] == "save":
            await self._handle_reject({
                "item": item,
                "justification": editor_result["justification"],
                "observations": editor_result["observations"],
                "tags": editor_result["tags"],
            })
        else:
            await self._show_curation()

    async def _handle_reject(self, result: dict) -> None:
        """Handle reject action."""
        if not self.queue or not self.file_repo or not self.review_repo or not self.current_session:
            return

        item = result.get("item")
        if not item:
            return

        # Create review record
        review = ReviewRecord(
            file_path=item.path,
            session_id=self.current_session.id,
            decision=ReviewDecision.REJECTED,
            justification=result.get("justification", ""),
            observations=result.get("observations", ""),
            tags=result.get("tags", []),
        )

        # Save review
        file_id = self.file_repo.get_file_id(self.current_session.id, item.relative_path)
        if file_id:
            self.review_repo.create(file_id, review)

        # Update status
        self.queue.mark_decided(item.relative_path, FileStatus.REJECTED)
        self.session_repo.update_counts(self.current_session.id)
        self.current_session = self.session_repo.get(self.current_session.id)

        await self._show_curation()

    async def _show_editor(self, result: dict) -> None:
        """Show the editor screen."""
        item = result.get("item")
        if not item:
            return

        editor_result = await self.push_screen_wait(
            EditorScreen(
                file_path=item.relative_path,
                observations=result.get("observations", ""),
                justification=result.get("justification", ""),
                tags=result.get("tags", []),
            )
        )

        if editor_result["action"] == "save":
            self._edit_values = {
                "observations": editor_result["observations"],
                "justification": editor_result["justification"],
                "tags": editor_result["tags"],
            }

        await self._show_curation()

    async def _handle_validate(self, result: dict) -> None:
        """Handle validate action."""
        item = result.get("item")
        if not item:
            await self._show_curation()
            return

        # Create script action
        action = self.executor.create_action(
            "carf_validator",
            args=["--file", str(item.path)],
            working_dir=self.root_path,
            is_dry_run=False,
        )

        # Show approval screen
        approval_result = await self.push_screen_wait(
            ScriptApprovalScreen(
                script_action=action,
                preview_text=self.executor.get_preview(action),
            )
        )

        if approval_result["action"] == "approve":
            action.approved = True
            exec_result = await self.executor.execute(action)

            await self.push_screen_wait(
                ScriptResultScreen(
                    script_name=action.script_name,
                    success=exec_result.success,
                    stdout=exec_result.stdout,
                    stderr=exec_result.stderr,
                    exit_code=exec_result.exit_code,
                )
            )

        await self._show_curation()

    async def _handle_sync(self, result: dict) -> None:
        """Handle sync action."""
        item = result.get("item")
        if not item or not item.is_readme:
            await self._show_curation()
            return

        # Create script action
        action = self.executor.create_action(
            "carf_tree_sync",
            args=[str(item.path.parent)],
            working_dir=self.root_path,
            is_dry_run=True,
        )

        # Show approval screen
        approval_result = await self.push_screen_wait(
            ScriptApprovalScreen(
                script_action=action,
                preview_text=self.executor.get_preview(action),
            )
        )

        if approval_result["action"] == "approve":
            action.approved = True
            action.is_dry_run = approval_result.get("dry_run", True)
            exec_result = await self.executor.execute(action)

            await self.push_screen_wait(
                ScriptResultScreen(
                    script_name=action.script_name,
                    success=exec_result.success,
                    stdout=exec_result.stdout,
                    stderr=exec_result.stderr,
                    exit_code=exec_result.exit_code,
                )
            )

        await self._show_curation()

    async def _show_progress(self) -> None:
        """Show progress screen."""
        if not self.current_session or not self.file_repo:
            return

        files = self.file_repo.list_by_session(self.current_session.id)
        result = await self.push_screen_wait(
            ProgressScreen(session=self.current_session, files=files)
        )

        if result["action"] == "export":
            await self._export_report()

        await self._show_curation()

    async def _show_completion(self) -> None:
        """Show completion screen."""
        if not self.current_session:
            return

        result = await self.push_screen_wait(
            CompletionScreen(session=self.current_session)
        )

        if result["action"] == "export":
            await self._export_report()
            await self._show_completion()
        elif result["action"] == "restart":
            self.current_session = None
            await self._show_welcome()
        elif result["action"] == "quit":
            self.exit()

    async def _show_help(self) -> None:
        """Show help screen."""
        # Simple notification for now
        self.notify("Help: Use A to approve, R to reject, S to skip, Q to quit")
        await self._show_curation()

    async def _export_report(self) -> None:
        """Export curation report to JSON."""
        if not self.current_session or not self.file_repo or not self.review_repo:
            return

        files = self.file_repo.list_by_session(self.current_session.id)
        reviews = self.review_repo.list_by_session(self.current_session.id)

        report = {
            "session": self.current_session.to_dict(),
            "files": [f.to_dict() for f in files],
            "reviews": [r.to_dict() for r in reviews],
            "exported_at": datetime.now().isoformat(),
        }

        # Save to file
        export_dir = self.config.get_data_path(self.root_path) / "exports"
        export_dir.mkdir(parents=True, exist_ok=True)
        export_path = export_dir / f"{self.current_session.id}-report.json"

        with open(export_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        self.notify(f"Report exported to {export_path}")

    def _save_state(self) -> None:
        """Save current state."""
        if self.current_session and self.session_repo:
            self.session_repo.update_counts(self.current_session.id)
        if self.db:
            self.db.commit()

    def on_unmount(self) -> None:
        """Handle app unmount."""
        self._save_state()
        if self.db:
            self.db.close()
