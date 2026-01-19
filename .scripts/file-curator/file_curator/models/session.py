"""Session data models."""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


@dataclass
class SessionConfig:
    """Configuration for a curation session.

    Attributes:
        include_patterns: Glob patterns for files to include
        exclude_dirs: Directories to exclude from scanning
        require_observations: Whether observations are required
        require_justification_on_reject: Whether justification is required for rejections
        skip_returns_to_queue: Whether skipped files return to the queue
    """

    include_patterns: list[str] = field(default_factory=lambda: ["**/*.md"])
    exclude_dirs: list[str] = field(
        default_factory=lambda: [
            ".git",
            ".obsidian",
            ".scripts",
            "SRC-CODE",
            "node_modules",
            "file-curator",
        ]
    )
    require_observations: bool = False
    require_justification_on_reject: bool = True
    skip_returns_to_queue: bool = True

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "include_patterns": self.include_patterns,
            "exclude_dirs": self.exclude_dirs,
            "require_observations": self.require_observations,
            "require_justification_on_reject": self.require_justification_on_reject,
            "skip_returns_to_queue": self.skip_returns_to_queue,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "SessionConfig":
        """Create from dictionary."""
        return cls(
            include_patterns=data.get("include_patterns", ["**/*.md"]),
            exclude_dirs=data.get(
                "exclude_dirs",
                [".git", ".obsidian", ".scripts", "SRC-CODE", "node_modules"],
            ),
            require_observations=data.get("require_observations", False),
            require_justification_on_reject=data.get(
                "require_justification_on_reject", True
            ),
            skip_returns_to_queue=data.get("skip_returns_to_queue", True),
        )


@dataclass
class CurationSession:
    """Represents a curation session.

    Attributes:
        id: Unique session identifier
        name: Human-readable session name
        root_path: Root directory being curated
        config: Session configuration
        created_at: When the session was created
        updated_at: When the session was last updated
        completed_at: When the session was completed (all files decided)
        total_files: Total number of files in the session
        approved_count: Number of approved files
        rejected_count: Number of rejected files
        skipped_count: Number of currently skipped files
        pending_count: Number of pending files
    """

    id: str
    name: str
    root_path: Path
    config: SessionConfig = field(default_factory=SessionConfig)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    total_files: int = 0
    approved_count: int = 0
    rejected_count: int = 0
    skipped_count: int = 0
    pending_count: int = 0

    @classmethod
    def create(cls, name: str, root_path: Path, config: Optional[SessionConfig] = None) -> "CurationSession":
        """Create a new session with a generated ID."""
        return cls(
            id=str(uuid.uuid4())[:8],
            name=name,
            root_path=root_path,
            config=config or SessionConfig(),
        )

    @property
    def is_complete(self) -> bool:
        """Check if all files have been decided (approved or rejected)."""
        decided = self.approved_count + self.rejected_count
        return decided == self.total_files and self.total_files > 0

    @property
    def progress_percent(self) -> float:
        """Calculate progress as a percentage."""
        if self.total_files == 0:
            return 0.0
        decided = self.approved_count + self.rejected_count
        return (decided / self.total_files) * 100

    @property
    def remaining_count(self) -> int:
        """Get count of files still needing decisions."""
        return self.pending_count + self.skipped_count

    def update_counts(
        self,
        total: int = 0,
        approved: int = 0,
        rejected: int = 0,
        skipped: int = 0,
        pending: int = 0,
    ) -> None:
        """Update file counts."""
        self.total_files = total
        self.approved_count = approved
        self.rejected_count = rejected
        self.skipped_count = skipped
        self.pending_count = pending
        self.updated_at = datetime.now()

        if self.is_complete and not self.completed_at:
            self.completed_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "root_path": str(self.root_path),
            "config": self.config.to_dict(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "total_files": self.total_files,
            "approved_count": self.approved_count,
            "rejected_count": self.rejected_count,
            "skipped_count": self.skipped_count,
            "pending_count": self.pending_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "CurationSession":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            root_path=Path(data["root_path"]),
            config=SessionConfig.from_dict(data.get("config", {})),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            completed_at=(
                datetime.fromisoformat(data["completed_at"])
                if data.get("completed_at")
                else None
            ),
            total_files=data.get("total_files", 0),
            approved_count=data.get("approved_count", 0),
            rejected_count=data.get("rejected_count", 0),
            skipped_count=data.get("skipped_count", 0),
            pending_count=data.get("pending_count", 0),
        )
