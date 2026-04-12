"""File enrichment with metadata."""

from datetime import datetime
from pathlib import Path

from ..models.file_item import FileItem
from .parser import FrontmatterParser


class FileEnricher:
    """Enriches FileItem objects with parsed metadata."""

    def __init__(self, parser: FrontmatterParser | None = None):
        """Initialize the enricher.

        Args:
            parser: FrontmatterParser instance (created if not provided)
        """
        self.parser = parser or FrontmatterParser()

    def enrich(self, item: FileItem) -> FileItem:
        """Enrich a FileItem with parsed metadata.

        Args:
            item: FileItem to enrich

        Returns:
            New FileItem with metadata populated
        """
        if not item.path.exists():
            return item

        parsed = self.parser.parse_file(item.path)

        return FileItem(
            path=item.path,
            relative_path=item.relative_path,
            file_hash=item.file_hash,
            title=parsed.get("title") or item.title,
            doc_type=parsed.get("doc_type") or item.doc_type,
            frontmatter_modules=parsed.get("modules", []) or item.frontmatter_modules,
            frontmatter_epic=parsed.get("epic") or item.frontmatter_epic,
            word_count=parsed.get("word_count", 0) or item.word_count,
            status=item.status,
            review_count=item.review_count,
            skip_count=item.skip_count,
            created_at=item.created_at,
            updated_at=datetime.now(),
            last_reviewed_at=item.last_reviewed_at,
        )

    def enrich_all(self, items: list[FileItem]) -> list[FileItem]:
        """Enrich multiple FileItems.

        Args:
            items: List of FileItems to enrich

        Returns:
            List of enriched FileItems
        """
        return [self.enrich(item) for item in items]

    def get_content_preview(self, item: FileItem, max_chars: int = 500) -> str:
        """Get content preview for a file.

        Args:
            item: FileItem to get preview for
            max_chars: Maximum characters

        Returns:
            Content preview string
        """
        if not item.path.exists():
            return ""

        try:
            content = item.path.read_text(encoding="utf-8")
            return self.parser._extract_preview(content, max_chars)
        except (OSError, IOError, UnicodeDecodeError):
            return ""

    def get_full_metadata(self, item: FileItem) -> dict:
        """Get full parsed metadata for a file.

        Args:
            item: FileItem to parse

        Returns:
            Dictionary with all parsed metadata
        """
        if not item.path.exists():
            return {}

        return self.parser.parse_file(item.path)
