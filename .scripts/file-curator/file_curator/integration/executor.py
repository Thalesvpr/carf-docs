"""Safe script executor with approval workflow."""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from ..models.action import ScriptAction
from .registry import AvailableScriptsRegistry, ScriptInfo


class ExecutionResult:
    """Result of a script execution."""

    def __init__(
        self,
        success: bool,
        exit_code: int,
        stdout: str = "",
        stderr: str = "",
        executed_at: Optional[datetime] = None,
        duration_ms: float = 0,
    ):
        self.success = success
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.executed_at = executed_at or datetime.now()
        self.duration_ms = duration_ms

    @property
    def output(self) -> str:
        """Get combined output."""
        parts = []
        if self.stdout:
            parts.append(self.stdout)
        if self.stderr:
            parts.append(f"STDERR:\n{self.stderr}")
        return "\n".join(parts)


class SafeScriptExecutor:
    """Safely executes scripts with approval workflow.

    Provides:
    - Script validation before execution
    - Approval workflow for destructive scripts
    - Dry-run mode support
    - Output capture
    - Execution history
    """

    def __init__(
        self,
        registry: Optional[AvailableScriptsRegistry] = None,
        working_dir: Optional[Path] = None,
        require_approval: bool = True,
        default_dry_run: bool = True,
        on_output: Optional[Callable[[str], None]] = None,
    ):
        """Initialize the executor.

        Args:
            registry: Script registry
            working_dir: Default working directory
            require_approval: Whether to require approval for destructive scripts
            default_dry_run: Whether to default to dry-run mode
            on_output: Callback for real-time output
        """
        self.registry = registry or AvailableScriptsRegistry()
        self.working_dir = working_dir
        self.require_approval = require_approval
        self.default_dry_run = default_dry_run
        self.on_output = on_output
        self.history: list[ScriptAction] = []

    def create_action(
        self,
        script_name: str,
        args: list[str] | None = None,
        working_dir: Optional[Path] = None,
        dry_run: Optional[bool] = None,
    ) -> ScriptAction:
        """Create a script action for approval.

        Args:
            script_name: Name of the script
            args: Command arguments
            working_dir: Working directory (uses default if not specified)
            dry_run: Override dry-run setting

        Returns:
            ScriptAction ready for approval
        """
        script_info = self.registry.get(script_name)

        # Determine if dry-run should be used
        use_dry_run = dry_run
        if use_dry_run is None:
            use_dry_run = (
                self.default_dry_run
                and script_info is not None
                and script_info.supports_dry_run
            )

        # Build command
        command = f"{sys.executable} -m .scripts.{script_name}"

        # Add dry-run flag if needed
        final_args = list(args or [])
        if use_dry_run and "--dry-run" not in final_args:
            final_args.append("--dry-run")

        # Determine if approval is required
        needs_approval = (
            self.require_approval
            and script_info is not None
            and script_info.is_destructive
            and not use_dry_run
        )

        return ScriptAction(
            script_name=script_name,
            command=command,
            args=final_args,
            working_dir=working_dir or self.working_dir,
            requires_approval=needs_approval,
            is_dry_run=use_dry_run,
        )

    def validate(self, action: ScriptAction) -> tuple[bool, str]:
        """Validate a script action before execution.

        Args:
            action: ScriptAction to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if script is registered
        if not self.registry.is_available(action.script_name):
            return False, f"Unknown script: {action.script_name}"

        # Check approval for destructive scripts
        if action.requires_approval and not action.approved:
            return False, "Approval required for this script"

        return True, ""

    async def execute(
        self,
        action: ScriptAction,
        timeout: float = 300.0,
    ) -> ExecutionResult:
        """Execute a script action.

        Args:
            action: ScriptAction to execute
            timeout: Timeout in seconds

        Returns:
            ExecutionResult with output and status
        """
        # Validate first
        is_valid, error = self.validate(action)
        if not is_valid:
            return ExecutionResult(
                success=False,
                exit_code=1,
                stderr=error,
            )

        # Build full command
        cmd = action.full_command
        cwd = str(action.working_dir) if action.working_dir else None

        start_time = datetime.now()

        try:
            # Create subprocess
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
            )

            # Wait with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ExecutionResult(
                    success=False,
                    exit_code=-1,
                    stderr=f"Execution timed out after {timeout}s",
                    executed_at=start_time,
                )

            end_time = datetime.now()
            duration_ms = (end_time - start_time).total_seconds() * 1000

            # Update action with results
            action.executed_at = start_time
            action.exit_code = process.returncode
            action.stdout = stdout.decode("utf-8", errors="replace")
            action.stderr = stderr.decode("utf-8", errors="replace")

            # Add to history
            self.history.append(action)

            # Call output callback if provided
            if self.on_output and action.stdout:
                self.on_output(action.stdout)

            return ExecutionResult(
                success=process.returncode == 0,
                exit_code=process.returncode or 0,
                stdout=action.stdout,
                stderr=action.stderr,
                executed_at=start_time,
                duration_ms=duration_ms,
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                exit_code=1,
                stderr=str(e),
                executed_at=start_time,
            )

    def approve(self, action: ScriptAction) -> ScriptAction:
        """Approve a script action for execution.

        Args:
            action: ScriptAction to approve

        Returns:
            Approved ScriptAction
        """
        action.approved = True
        action.approved_at = datetime.now()
        return action

    def get_preview(self, action: ScriptAction) -> str:
        """Get a preview of what the script will do.

        Args:
            action: ScriptAction to preview

        Returns:
            Formatted preview string
        """
        script_info = self.registry.get(action.script_name)

        lines = [
            f"**Script:** {action.script_name}",
            f"**Command:** `{action.full_command}`",
        ]

        if action.working_dir:
            lines.append(f"**Working Directory:** {action.working_dir}")

        if action.is_dry_run:
            lines.append("**Mode:** DRY RUN (no changes will be made)")
        elif script_info and script_info.is_destructive:
            lines.append("**Mode:** LIVE (files will be modified)")
        else:
            lines.append("**Mode:** LIVE")

        if script_info:
            lines.append(f"\n{script_info.description}")

        if action.requires_approval:
            lines.append("\n**Requires approval before execution**")

        return "\n".join(lines)

    def get_history(self, limit: int = 10) -> list[ScriptAction]:
        """Get recent execution history.

        Args:
            limit: Maximum number of entries

        Returns:
            List of recent ScriptActions
        """
        return self.history[-limit:]

    def clear_history(self) -> None:
        """Clear execution history."""
        self.history.clear()
