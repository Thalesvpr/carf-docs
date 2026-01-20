"""File item data model."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, Any


class FileStatus(Enum):
    """Status of a file in the curation queue."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SKIPPED = "skipped"

    def is_decided(self) -> bool:
        """Check if this status represents a final decision."""
        return self in (FileStatus.APPROVED, FileStatus.REJECTED)


@dataclass
class LinkInfo:
    """Information about a link in the document."""
    text: str
    target: str
    line_number: int
    is_external: bool = False
    is_valid: bool = True
    resolved_path: Optional[Path] = None


@dataclass
class ValidationIssue:
    """A single validation issue."""
    severity: str  # "error", "warning", "info"
    code: str
    message: str
    line_number: Optional[int] = None
    validator_name: str = ""
    suggestion: Optional[str] = None


@dataclass
class FileItem:
    """Represents a file in the documentation tree.

    Attributes:
        path: Absolute path to the file
        relative_path: Path relative to the project root
        file_hash: SHA256 hash for change detection
        title: Extracted title from the file
        doc_type: Document type (RF, UC, US, ADR, README, etc.)
        frontmatter_modules: List of modules from frontmatter
        frontmatter_epic: Epic reference from frontmatter
        word_count: Number of words in the file
        status: Current curation status
        review_count: Number of times this file has been reviewed
        skip_count: Number of times this file has been skipped
        created_at: When the file was first scanned
        updated_at: When the file was last modified
        last_reviewed_at: When the file was last reviewed
        file_status: Status from file footer metadata
        file_last_updated: Last updated date from footer
        file_description: Description from footer
        footer_metadata: All footer metadata
        links: Links in the document
        validation_issues: Validation issues for this file
    """

    path: Path
    relative_path: str
    file_hash: str
    title: Optional[str] = None
    doc_type: Optional[str] = None
    frontmatter_modules: list[str] = field(default_factory=list)
    frontmatter_epic: Optional[str] = None
    word_count: int = 0
    status: FileStatus = FileStatus.PENDING
    review_count: int = 0
    skip_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    last_reviewed_at: Optional[datetime] = None
    # File's own metadata (from footer)
    file_status: Optional[str] = None
    file_last_updated: Optional[str] = None
    file_description: Optional[str] = None
    footer_metadata: dict = field(default_factory=dict)
    # Links in the document
    links: list[LinkInfo] = field(default_factory=list)
    # Validation issues
    validation_issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def filename(self) -> str:
        """Get the filename without path."""
        return self.path.name

    @property
    def extension(self) -> str:
        """Get the file extension."""
        return self.path.suffix

    @property
    def is_readme(self) -> bool:
        """Check if this is a README file."""
        return self.filename.lower().startswith("readme")

    @property
    def is_decided(self) -> bool:
        """Check if a final decision has been made."""
        return self.status.is_decided()

    @property
    def needs_review(self) -> bool:
        """Check if this file needs review (pending or skipped)."""
        return self.status in (FileStatus.PENDING, FileStatus.SKIPPED)

    @property
    def error_count(self) -> int:
        """Count of validation errors."""
        return sum(1 for i in self.validation_issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        """Count of validation warnings."""
        return sum(1 for i in self.validation_issues if i.severity == "warning")

    @property
    def broken_links_count(self) -> int:
        """Count of broken internal links."""
        return sum(1 for link in self.links if not link.is_external and not link.is_valid)

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "path": str(self.path),
            "relative_path": self.relative_path,
            "file_hash": self.file_hash,
            "title": self.title,
            "doc_type": self.doc_type,
            "frontmatter_modules": self.frontmatter_modules,
            "frontmatter_epic": self.frontmatter_epic,
            "word_count": self.word_count,
            "status": self.status.value,
            "file_status": self.file_status,
            "file_last_updated": self.file_last_updated,
            "file_description": self.file_description,
            "review_count": self.review_count,
            "skip_count": self.skip_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "broken_links": self.broken_links_count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "FileItem":
        """Create from dictionary."""
        return cls(
            path=Path(data["path"]),
            relative_path=data["relative_path"],
            file_hash=data["file_hash"],
            title=data.get("title"),
            doc_type=data.get("doc_type"),
            frontmatter_modules=data.get("frontmatter_modules", []),
            frontmatter_epic=data.get("frontmatter_epic"),
            word_count=data.get("word_count", 0),
            status=FileStatus(data.get("status", "pending")),
            file_status=data.get("file_status"),
            file_last_updated=data.get("file_last_updated"),
            file_description=data.get("file_description"),
            review_count=data.get("review_count", 0),
            skip_count=data.get("skip_count", 0),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else datetime.now()
            ),
            updated_at=(
                datetime.fromisoformat(data["updated_at"])
                if data.get("updated_at")
                else None
            ),
        )
