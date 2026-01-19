"""Script suggestion and execution."""

from pathlib import Path
from typing import Any, Optional

from ..models.action import ScriptAction
from ..models.file_item import FileItem
from .base import BaseAction


class ScriptSuggester:
    """Suggests relevant scripts based on file type and context."""

    # Map of doc types to suggested scripts
    SUGGESTIONS = {
        "RF": ["carf_validator"],
        "UC": ["carf_validator"],
        "US": ["carf_validator"],
        "ADR": ["carf_validator"],
        "README": ["carf_validator", "carf_tree_sync"],
        "TEST": ["carf_validator"],
        "SPEC": ["carf_validator"],
    }

    # Scripts that support dry-run
    DRY_RUN_SCRIPTS = {"carf_tree_sync"}

    def suggest(self, item: FileItem) -> list[str]:
        """Suggest scripts for a file.

        Args:
            item: FileItem to get suggestions for

        Returns:
            List of suggested script names
        """
        suggestions = []

        # Always suggest validator for markdown files
        if item.extension == ".md":
            suggestions.append("carf_validator")

        # Add doc-type specific suggestions
        if item.doc_type and item.doc_type in self.SUGGESTIONS:
            for script in self.SUGGESTIONS[item.doc_type]:
                if script not in suggestions:
                    suggestions.append(script)

        # Suggest tree_sync for READMEs
        if item.is_readme:
            if "carf_tree_sync" not in suggestions:
                suggestions.append("carf_tree_sync")

        return suggestions

    def supports_dry_run(self, script_name: str) -> bool:
        """Check if a script supports dry-run mode.

        Args:
            script_name: Name of the script

        Returns:
            True if the script supports dry-run
        """
        return script_name in self.DRY_RUN_SCRIPTS


class SafeExecutor:
    """Safely executes scripts with approval workflow."""

    def __init__(
        self,
        scripts_dir: Optional[Path] = None,
        require_approval: bool = True,
        default_dry_run: bool = True,
    ):
        """Initialize the executor.

        Args:
            scripts_dir: Path to .scripts directory
            require_approval: Whether to require approval before execution
            default_dry_run: Whether to default to dry-run mode
        """
        self.scripts_dir = scripts_dir
        self.require_approval = require_approval
        self.default_dry_run = default_dry_run
        self.suggester = ScriptSuggester()

    def create_action(
        self,
        script_name: str,
        args: list[str] | None = None,
        working_dir: Optional[Path] = None,
        is_dry_run: Optional[bool] = None,
    ) -> ScriptAction:
        """Create a script action.

        Args:
            script_name: Name of the script
            args: Command arguments
            working_dir: Working directory
            is_dry_run: Whether to use dry-run mode

        Returns:
            ScriptAction ready for approval/execution
        """
        # Determine command
        if self.scripts_dir:
            command = f"python -m {script_name}"
        else:
            command = f"python -m .scripts.{script_name}"

        # Determine dry-run
        if is_dry_run is None:
            is_dry_run = (
                self.default_dry_run
                and self.suggester.supports_dry_run(script_name)
            )

        # Add dry-run flag if needed
        final_args = list(args or [])
        if is_dry_run and "--dry-run" not in final_args:
            final_args.append("--dry-run")

        return ScriptAction(
            script_name=script_name,
            command=command,
            args=final_args,
            working_dir=working_dir,
            requires_approval=self.require_approval,
            is_dry_run=is_dry_run,
        )

    def validate_script(self, script_name: str) -> tuple[bool, str]:
        """Validate that a script exists and is safe to run.

        Args:
            script_name: Name of the script

        Returns:
            Tuple of (is_valid, message)
        """
        known_scripts = {
            "carf_validator",
            "carf_tree_sync",
            "doc_generator",
        }

        if script_name not in known_scripts:
            return False, f"Unknown script: {script_name}"

        return True, ""

    async def execute(
        self,
        action: ScriptAction,
        capture_output: bool = True,
    ) -> ScriptAction:
        """Execute a script action.

        Args:
            action: ScriptAction to execute
            capture_output: Whether to capture stdout/stderr

        Returns:
            Updated ScriptAction with execution results
        """
        import asyncio
        from datetime import datetime

        # Validate script
        is_valid, message = self.validate_script(action.script_name)
        if not is_valid:
            action.exit_code = 1
            action.stderr = message
            return action

        # Check approval
        if action.requires_approval and not action.approved:
            action.exit_code = 1
            action.stderr = "Execution requires approval"
            return action

        # Build command
        cmd = action.full_command
        cwd = str(action.working_dir) if action.working_dir else None

        try:
            # Execute command
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE if capture_output else None,
                stderr=asyncio.subprocess.PIPE if capture_output else None,
                cwd=cwd,
            )

            stdout, stderr = await process.communicate()

            action.executed_at = datetime.now()
            action.exit_code = process.returncode
            if capture_output:
                action.stdout = stdout.decode("utf-8", errors="replace")
                action.stderr = stderr.decode("utf-8", errors="replace")

        except Exception as e:
            action.executed_at = datetime.now()
            action.exit_code = 1
            action.stderr = str(e)

        return action

    def get_preview(self, action: ScriptAction) -> str:
        """Get a preview of what the script will do.

        Args:
            action: ScriptAction to preview

        Returns:
            Formatted preview string
        """
        lines = [
            f"Script: {action.script_name}",
            f"Command: {action.full_command}",
        ]

        if action.working_dir:
            lines.append(f"Working directory: {action.working_dir}")

        if action.is_dry_run:
            lines.append("Mode: DRY RUN (no changes will be made)")
        else:
            lines.append("Mode: LIVE (changes will be applied)")

        return "\n".join(lines)


class ValidateAction(BaseAction):
    """Action to run the validator on a file."""

    def __init__(self, executor: SafeExecutor):
        """Initialize the action.

        Args:
            executor: SafeExecutor instance
        """
        self.executor = executor

    @property
    def name(self) -> str:
        return "validate"

    @property
    def description(self) -> str:
        return "Run carf_validator on this file"

    @property
    def shortcut(self) -> str:
        return "v"

    async def execute(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the validate action.

        Args:
            item: FileItem to validate
            context: Contains 'working_dir', 'approved'

        Returns:
            Result with script output
        """
        action = self.executor.create_action(
            "carf_validator",
            args=[str(item.path)],
            working_dir=context.get("working_dir"),
            is_dry_run=False,  # Validator is always read-only
        )

        if context.get("approved", False):
            action.approved = True
            action = await self.executor.execute(action)

            return {
                "success": action.was_successful,
                "action": "validation_complete",
                "stdout": action.stdout,
                "stderr": action.stderr,
                "exit_code": action.exit_code,
                "message": (
                    "Validation passed"
                    if action.was_successful
                    else "Validation found issues"
                ),
            }
        else:
            return {
                "success": True,
                "action": "request_approval",
                "script_action": action,
                "preview": self.executor.get_preview(action),
                "message": "Approval required to run validator",
            }


class SyncAction(BaseAction):
    """Action to run tree_sync on a README."""

    def __init__(self, executor: SafeExecutor):
        """Initialize the action.

        Args:
            executor: SafeExecutor instance
        """
        self.executor = executor

    @property
    def name(self) -> str:
        return "sync"

    @property
    def description(self) -> str:
        return "Run carf_tree_sync to update README index"

    @property
    def shortcut(self) -> str:
        return "t"

    def validate(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> tuple[bool, str]:
        """Validate the sync action.

        Args:
            item: FileItem to validate
            context: Additional context

        Returns:
            Tuple of (is_valid, message)
        """
        if not item.is_readme:
            return False, "Sync is only available for README files"
        return True, ""

    async def execute(
        self,
        item: FileItem,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the sync action.

        Args:
            item: FileItem (README) to sync
            context: Contains 'working_dir', 'approved', 'dry_run'

        Returns:
            Result with script output
        """
        # Validate first
        is_valid, message = self.validate(item, context)
        if not is_valid:
            return {
                "success": False,
                "message": message,
            }

        dry_run = context.get("dry_run", True)
        action = self.executor.create_action(
            "carf_tree_sync",
            args=[str(item.path.parent)],
            working_dir=context.get("working_dir"),
            is_dry_run=dry_run,
        )

        if context.get("approved", False):
            action.approved = True
            action = await self.executor.execute(action)

            return {
                "success": action.was_successful,
                "action": "sync_complete",
                "stdout": action.stdout,
                "stderr": action.stderr,
                "exit_code": action.exit_code,
                "is_dry_run": action.is_dry_run,
                "message": (
                    "Sync completed (dry-run)"
                    if action.is_dry_run
                    else "Sync completed"
                )
                if action.was_successful
                else "Sync failed",
            }
        else:
            return {
                "success": True,
                "action": "request_approval",
                "script_action": action,
                "preview": self.executor.get_preview(action),
                "message": "Approval required to run sync",
            }
