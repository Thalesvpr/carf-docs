"""Modelos semânticos para o sistema de validação CARF."""

from .base import (
    DocumentType,
    Frontmatter,
    Link,
    Metadata,
)
from .results import (
    Severity,
    ValidationIssue,
    ValidatorResult,
    ValidationReport,
)

__all__ = [
    "DocumentType",
    "Frontmatter",
    "Link",
    "Metadata",
    "Severity",
    "ValidationIssue",
    "ValidatorResult",
    "ValidationReport",
]
