"""Document parser for extracting metadata from markdown files."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import re

from .frontmatter import FrontmatterParser, Frontmatter


@dataclass
class DocumentInfo:
    """Parsed document information."""

    path: Path
    identifier: Optional[str]  # RF-001, UC-002, etc.
    title: Optional[str]  # Title from H1
    frontmatter: Optional[Frontmatter]
    word_count: int

    @property
    def filename(self) -> str:
        """Get filename without extension."""
        return self.path.stem

    @property
    def display_id(self) -> str:
        """Get display ID (identifier or filename)."""
        return self.identifier or self.filename


class DocumentParser:
    """Parser for markdown documents."""

    # Pattern to extract identifier from filename or title
    ID_PATTERN = re.compile(r"^(RF|US|UC|RNF|ADR)-(\d+)", re.IGNORECASE)

    # Pattern to extract H1 title
    TITLE_PATTERN = re.compile(r"^#\s+(.+?)(?:\s*\n|$)", re.MULTILINE)

    # Pattern for identifier in title (e.g., "# RF-001: Title")
    TITLE_ID_PATTERN = re.compile(
        r"^#\s+(RF|US|UC|RNF|ADR)-(\d+)[:\-\s]+(.+?)(?:\s*\n|$)",
        re.MULTILINE | re.IGNORECASE,
    )

    def __init__(self):
        self.frontmatter_parser = FrontmatterParser()

    def parse(self, file_path: Path) -> Optional[DocumentInfo]:
        """Parse document and extract metadata."""
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return None

        frontmatter = self.frontmatter_parser.parse(content)
        identifier = self._extract_identifier(file_path, content)
        title = self._extract_title(content)
        word_count = self._count_words(content)

        return DocumentInfo(
            path=file_path,
            identifier=identifier,
            title=title,
            frontmatter=frontmatter,
            word_count=word_count,
        )

    def _extract_identifier(
        self, file_path: Path, content: str
    ) -> Optional[str]:
        """Extract document identifier (RF-001, UC-002, etc.)."""
        # Try filename first
        match = self.ID_PATTERN.match(file_path.stem)
        if match:
            prefix = match.group(1).upper()
            number = match.group(2)
            return f"{prefix}-{number}"

        # Try title
        match = self.TITLE_ID_PATTERN.search(content)
        if match:
            prefix = match.group(1).upper()
            number = match.group(2)
            return f"{prefix}-{number}"

        return None

    def _extract_title(self, content: str) -> Optional[str]:
        """Extract title from H1 heading."""
        # Skip frontmatter
        if content.startswith("---"):
            end = content.find("---", 3)
            if end != -1:
                content = content[end + 3:]

        # Try title with identifier first
        match = self.TITLE_ID_PATTERN.search(content)
        if match:
            return match.group(3).strip()

        # Try plain H1
        match = self.TITLE_PATTERN.search(content)
        if match:
            return match.group(1).strip()

        return None

    def _count_words(self, content: str) -> int:
        """Count words in content (excluding code blocks and frontmatter)."""
        # Remove frontmatter
        if content.startswith("---"):
            end = content.find("---", 3)
            if end != -1:
                content = content[end + 3:]

        # Remove code blocks
        content = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
        content = re.sub(r"`[^`]+`", "", content)

        # Count words
        words = re.findall(r"\b\w+\b", content)
        return len(words)

    def parse_files(self, files: List[Path]) -> List[DocumentInfo]:
        """Parse multiple files."""
        results = []
        for file_path in files:
            info = self.parse(file_path)
            if info:
                results.append(info)
        return results
