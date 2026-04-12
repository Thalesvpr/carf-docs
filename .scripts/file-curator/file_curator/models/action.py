"""Action data models."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class ActionType(Enum):
    """Types of actions that can be performed."""

    APPROVE = "approve"
    REJECT = "reject"
    SKIP = "skip"
    EDIT = "edit"
    VALIDATE = "validate"
    SYNC = "sync"
    EXPORT = "export"


@dataclass
class Action:
    """Represents an action performed during curation.

    Attributes:
        action_type: The type of action
        file_path: Path to the file (if applicable)
        session_id: ID of the curation session
        performed_at: When the action was performed
        details: Additional action details
    """

    action_type: ActionType
    file_path: Optional[Path] = None
    session_id: str = ""
    performed_at: datetime = field(default_factory=datetime.now)
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "action_type": self.action_type.value,
            "file_path": str(self.file_path) if self.file_path else None,
            "session_id": self.session_id,
            "performed_at": self.performed_at.isoformat(),
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Action":
        """Create from dictionary."""
        return cls(
            action_type=ActionType(data["action_type"]),
            file_path=Path(data["file_path"]) if data.get("file_path") else None,
            session_id=data.get("session_id", ""),
            performed_at=datetime.fromisoformat(data["performed_at"]),
            details=data.get("details", {}),
        )


@dataclass
class ScriptAction:
    """Represents a script execution action.

    Attributes:
        script_name: Name of the script to execute
        command: Full command to execute
        args: Command arguments
        working_dir: Working directory for execution
        requires_approval: Whether user approval is required
        is_dry_run: Whether this is a dry-run execution
        executed_at: When the script was executed
        exit_code: Exit code from execution
        stdout: Captured standard output
        stderr: Captured standard error
        approved: Whether the execution was approved
        approved_at: When the execution was approved
    """

    script_name: str
    command: str
    args: list[str] = field(default_factory=list)
    working_dir: Optional[Path] = None
    requires_approval: bool = True
    is_dry_run: bool = False
    executed_at: Optional[datetime] = None
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    approved: bool = False
    approved_at: Optional[datetime] = None

    @property
    def full_command(self) -> str:
        """Get the full command with arguments."""
        if self.args:
            return f"{self.command} {' '.join(self.args)}"
        return self.command

    @property
    def is_executed(self) -> bool:
        """Check if the script has been executed."""
        return self.executed_at is not None

    @property
    def was_successful(self) -> bool:
        """Check if the execution was successful."""
        return self.exit_code == 0

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "script_name": self.script_name,
            "command": self.command,
            "args": self.args,
            "working_dir": str(self.working_dir) if self.working_dir else None,
            "requires_approval": self.requires_approval,
            "is_dry_run": self.is_dry_run,
            "executed_at": (
                self.executed_at.isoformat() if self.executed_at else None
            ),
            "exit_code": self.exit_code,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "approved": self.approved,
            "approved_at": (
                self.approved_at.isoformat() if self.approved_at else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScriptAction":
        """Create from dictionary."""
        return cls(
            script_name=data["script_name"],
            command=data["command"],
            args=data.get("args", []),
            working_dir=Path(data["working_dir"]) if data.get("working_dir") else None,
            requires_approval=data.get("requires_approval", True),
            is_dry_run=data.get("is_dry_run", False),
            executed_at=(
                datetime.fromisoformat(data["executed_at"])
                if data.get("executed_at")
                else None
            ),
            exit_code=data.get("exit_code"),
            stdout=data.get("stdout", ""),
            stderr=data.get("stderr", ""),
            approved=data.get("approved", False),
            approved_at=(
                datetime.fromisoformat(data["approved_at"])
                if data.get("approved_at")
                else None
            ),
        )
