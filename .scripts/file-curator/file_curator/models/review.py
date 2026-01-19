"""Review record data models."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional


class ReviewDecision(Enum):
    """Decision made during review."""

    APPROVED = "approved"
    REJECTED = "rejected"
    SKIPPED = "skipped"

    @property
    def emoji(self) -> str:
        """Get emoji representation of the decision."""
        return {
            ReviewDecision.APPROVED: "\u2705",  # checkmark
            ReviewDecision.REJECTED: "\u274c",  # x mark
            ReviewDecision.SKIPPED: "\u23ed\ufe0f",  # skip forward
        }[self]

    @property
    def label(self) -> str:
        """Get human-readable label."""
        return self.value.capitalize()


@dataclass
class ReviewMetadata:
    """Metadata about a review action.

    Attributes:
        reviewer: Name or identifier of the reviewer
        session_id: ID of the curation session
        duration_seconds: Time spent reviewing (if tracked)
        previous_decision: Previous decision if this is a re-review
    """

    reviewer: str = "anonymous"
    session_id: str = ""
    duration_seconds: Optional[float] = None
    previous_decision: Optional[ReviewDecision] = None

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "reviewer": self.reviewer,
            "session_id": self.session_id,
            "duration_seconds": self.duration_seconds,
            "previous_decision": (
                self.previous_decision.value if self.previous_decision else None
            ),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewMetadata":
        """Create from dictionary."""
        return cls(
            reviewer=data.get("reviewer", "anonymous"),
            session_id=data.get("session_id", ""),
            duration_seconds=data.get("duration_seconds"),
            previous_decision=(
                ReviewDecision(data["previous_decision"])
                if data.get("previous_decision")
                else None
            ),
        )


@dataclass
class ReviewRecord:
    """Record of a file review.

    Attributes:
        file_path: Path to the reviewed file
        session_id: ID of the curation session
        decision: The review decision
        decided_at: When the decision was made
        observations: User-editable observations
        justification: User-editable justification (esp. for rejections)
        tags: User-assigned tags
        rendered_markdown: The persisted review card markdown
        metadata: Additional review metadata
    """

    file_path: Path
    session_id: str
    decision: ReviewDecision
    decided_at: datetime = field(default_factory=datetime.now)
    observations: str = ""
    justification: str = ""
    tags: list[str] = field(default_factory=list)
    rendered_markdown: str = ""
    metadata: ReviewMetadata = field(default_factory=ReviewMetadata)

    @property
    def is_final(self) -> bool:
        """Check if this is a final decision (not skipped)."""
        return self.decision in (ReviewDecision.APPROVED, ReviewDecision.REJECTED)

    @property
    def has_observations(self) -> bool:
        """Check if observations were provided."""
        return bool(self.observations.strip())

    @property
    def has_justification(self) -> bool:
        """Check if justification was provided."""
        return bool(self.justification.strip())

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "file_path": str(self.file_path),
            "session_id": self.session_id,
            "decision": self.decision.value,
            "decided_at": self.decided_at.isoformat(),
            "observations": self.observations,
            "justification": self.justification,
            "tags": self.tags,
            "rendered_markdown": self.rendered_markdown,
            "metadata": self.metadata.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewRecord":
        """Create from dictionary."""
        return cls(
            file_path=Path(data["file_path"]),
            session_id=data["session_id"],
            decision=ReviewDecision(data["decision"]),
            decided_at=datetime.fromisoformat(data["decided_at"]),
            observations=data.get("observations", ""),
            justification=data.get("justification", ""),
            tags=data.get("tags", []),
            rendered_markdown=data.get("rendered_markdown", ""),
            metadata=ReviewMetadata.from_dict(data.get("metadata", {})),
        )

    def to_markdown(self) -> str:
        """Generate markdown representation of the review."""
        tags_str = ", ".join(f"`{tag}`" for tag in self.tags) if self.tags else "None"

        return f"""---
file: {self.file_path}
decision: {self.decision.value}
decided_at: {self.decided_at.isoformat()}
session_id: {self.session_id}
tags: {self.tags}
---

# Review: {self.file_path.name}

## Decision: {self.decision.emoji} {self.decision.label}

## Observations
{self.observations if self.observations else "_No observations recorded._"}

## Justification
{self.justification if self.justification else "_No justification provided._"}

## Tags
{tags_str}
"""
