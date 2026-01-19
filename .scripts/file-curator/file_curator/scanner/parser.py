"""Frontmatter and metadata parsing."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import yaml


@dataclass
class LinkInfo:
    """Information about a link in the document."""
    text: str
    target: str
    line_number: int
    is_external: bool = False
    is_valid: bool = True
    resolved_path: Optional[Path] = None


class FrontmatterParser:
    """Parser for YAML frontmatter in markdown files."""

    # Pattern to match YAML frontmatter
    FRONTMATTER_PATTERN = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n",
        re.DOTALL,
    )

    # Pattern to extract title from first H1
    TITLE_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)

    # Pattern to extract footer metadata (CARF format: **Key:** Value or **Key**: Value)
    FOOTER_METADATA_PATTERN = re.compile(
        r"\*\*([^*:]+)\*\*\s*:\s*(.+?)(?=\n|$)",
        re.MULTILINE,
    )

    # Pattern to extract markdown links [text](target)
    LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    # Pattern to identify document type from filename
    DOC_TYPE_PATTERNS = {
        "RF": re.compile(r"^(\d+-)?RF-", re.IGNORECASE),
        "UC": re.compile(r"^(\d+-)?UC-", re.IGNORECASE),
        "US": re.compile(r"^(\d+-)?US-", re.IGNORECASE),
        "ADR": re.compile(r"^(\d+-)?ADR-", re.IGNORECASE),
        "README": re.compile(r"^README", re.IGNORECASE),
        "TEST": re.compile(r"^(\d+-)?(TEST|TC)-", re.IGNORECASE),
        "SPEC": re.compile(r"^(\d+-)?SPEC-", re.IGNORECASE),
    }

    def parse_file(self, path: Path) -> dict[str, Any]:
        """Parse a markdown file for frontmatter and metadata.

        Args:
            path: Path to the markdown file

        Returns:
            Dictionary with parsed metadata
        """
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, IOError, UnicodeDecodeError):
            return self._empty_result()

        return self.parse_content(content, path.name, path)

    def parse_content(
        self, content: str, filename: str = "", source_path: Optional[Path] = None
    ) -> dict[str, Any]:
        """Parse content for frontmatter and metadata.

        Args:
            content: Markdown content
            filename: Original filename for doc_type detection
            source_path: Path to source file for link resolution

        Returns:
            Dictionary with parsed metadata
        """
        result = self._empty_result()

        # Parse frontmatter
        frontmatter = self._extract_frontmatter(content)
        if frontmatter:
            result["frontmatter"] = frontmatter
            result["modules"] = self._extract_list(frontmatter, "modules")
            result["epic"] = frontmatter.get("epic")
            result["status"] = frontmatter.get("status")
            result["tags"] = self._extract_list(frontmatter, "tags")

        # Parse footer metadata (CARF format)
        footer_metadata = self._extract_footer_metadata(content)
        result["footer_metadata"] = footer_metadata
        result["file_status"] = footer_metadata.get("Status do arquivo")
        result["last_updated"] = footer_metadata.get("Última atualização")

        # Extract title
        result["title"] = self._extract_title(content, frontmatter)

        # Detect document type
        result["doc_type"] = self._detect_doc_type(filename, frontmatter)

        # Count words (excluding frontmatter)
        result["word_count"] = self._count_words(content)

        # Extract content preview
        result["content_preview"] = self._extract_preview(content)

        # Extract links
        result["links"] = self._extract_links(content, source_path)

        return result

    def _empty_result(self) -> dict[str, Any]:
        """Return an empty result dictionary."""
        return {
            "frontmatter": {},
            "footer_metadata": {},
            "title": None,
            "doc_type": None,
            "modules": [],
            "epic": None,
            "status": None,
            "file_status": None,
            "last_updated": None,
            "tags": [],
            "word_count": 0,
            "content_preview": "",
            "links": [],
        }

    def _extract_frontmatter(self, content: str) -> dict[str, Any]:
        """Extract YAML frontmatter from content.

        Args:
            content: Markdown content

        Returns:
            Parsed frontmatter dictionary or empty dict
        """
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            return {}

        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}

    def _extract_footer_metadata(self, content: str) -> dict[str, str]:
        """Extract footer metadata in CARF format (**Key:** Value).

        Args:
            content: Markdown content

        Returns:
            Dictionary of key-value pairs from footer
        """
        # Look for metadata after the last --- separator
        parts = content.rsplit("---", 1)
        if len(parts) < 2:
            # No separator, search whole content
            search_content = content
        else:
            # Search after the separator
            search_content = parts[1]

        metadata = {}
        for match in self.FOOTER_METADATA_PATTERN.finditer(search_content):
            key = match.group(1).strip()
            value = match.group(2).strip()
            metadata[key] = value

        return metadata

    def _extract_title(
        self, content: str, frontmatter: dict[str, Any]
    ) -> Optional[str]:
        """Extract title from frontmatter or first H1.

        Args:
            content: Markdown content
            frontmatter: Parsed frontmatter

        Returns:
            Title string or None
        """
        # Check frontmatter first
        if frontmatter.get("title"):
            return str(frontmatter["title"])

        # Look for first H1
        # Skip frontmatter when searching
        search_content = self.FRONTMATTER_PATTERN.sub("", content)
        match = self.TITLE_PATTERN.search(search_content)
        if match:
            return match.group(1).strip()

        return None

    def _detect_doc_type(
        self, filename: str, frontmatter: dict[str, Any]
    ) -> Optional[str]:
        """Detect document type from filename or frontmatter.

        Args:
            filename: Name of the file
            frontmatter: Parsed frontmatter

        Returns:
            Document type string or None
        """
        # Check frontmatter first
        if frontmatter.get("doc_type"):
            return str(frontmatter["doc_type"]).upper()

        if frontmatter.get("type"):
            return str(frontmatter["type"]).upper()

        # Check filename patterns
        for doc_type, pattern in self.DOC_TYPE_PATTERNS.items():
            if pattern.match(filename):
                return doc_type

        return None

    def _extract_list(
        self, frontmatter: dict[str, Any], key: str
    ) -> list[str]:
        """Extract a list field from frontmatter.

        Args:
            frontmatter: Parsed frontmatter
            key: Key to extract

        Returns:
            List of strings
        """
        value = frontmatter.get(key)
        if value is None:
            return []
        if isinstance(value, list):
            return [str(v) for v in value]
        if isinstance(value, str):
            # Handle comma-separated values
            return [v.strip() for v in value.split(",") if v.strip()]
        return []

    def _count_words(self, content: str) -> int:
        """Count words in content, excluding frontmatter.

        Args:
            content: Markdown content

        Returns:
            Word count
        """
        # Remove frontmatter
        text = self.FRONTMATTER_PATTERN.sub("", content)
        # Remove code blocks
        text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        # Remove inline code
        text = re.sub(r"`[^`]+`", "", text)
        # Remove links but keep text
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        # Remove images
        text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
        # Count words
        words = text.split()
        return len(words)

    def _extract_preview(self, content: str, max_chars: int = 500) -> str:
        """Extract a preview of the content.

        Args:
            content: Markdown content
            max_chars: Maximum characters to include

        Returns:
            Preview string
        """
        # Remove frontmatter
        text = self.FRONTMATTER_PATTERN.sub("", content)
        # Remove the title (first H1)
        text = self.TITLE_PATTERN.sub("", text, count=1)
        # Clean up whitespace
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = text.strip()

        if len(text) <= max_chars:
            return text

        # Truncate at word boundary
        truncated = text[:max_chars]
        last_space = truncated.rfind(" ")
        if last_space > max_chars * 0.8:
            truncated = truncated[:last_space]

        return truncated + "..."

    def _extract_links(
        self, content: str, source_path: Optional[Path] = None
    ) -> list[LinkInfo]:
        """Extract all markdown links from content.

        Args:
            content: Markdown content
            source_path: Path to source file for resolving relative links

        Returns:
            List of LinkInfo objects
        """
        links = []
        lines = content.split("\n")

        for line_num, line in enumerate(lines, 1):
            for match in self.LINK_PATTERN.finditer(line):
                text = match.group(1)
                target = match.group(2)

                # Check if external
                is_external = (
                    target.startswith("http://")
                    or target.startswith("https://")
                    or target.startswith("mailto:")
                    or target.startswith("#")
                    or target.startswith("tel:")
                )

                link = LinkInfo(
                    text=text,
                    target=target,
                    line_number=line_num,
                    is_external=is_external,
                )

                # Resolve internal links
                if not is_external and source_path:
                    # Remove anchor
                    clean_target = target.split("#")[0] if "#" in target else target
                    if clean_target:
                        try:
                            resolved = (source_path.parent / clean_target).resolve()
                            link.resolved_path = resolved
                            link.is_valid = resolved.exists() and resolved.is_file()
                        except Exception:
                            link.is_valid = False

                links.append(link)

        return links


class ParsedContent:
    """Container for parsed content data."""

    def __init__(self, data: dict):
        """Initialize from parser result dictionary."""
        self.title = data.get("title")
        self.doc_type = data.get("doc_type")
        self.modules = data.get("modules", [])
        self.epic = data.get("epic")
        self.status = data.get("status")
        self.tags = data.get("tags", [])
        self.word_count = data.get("word_count", 0)
        self.content_preview = data.get("content_preview", "")
        self.frontmatter = data.get("frontmatter", {})
        # Footer metadata (CARF format)
        self.footer_metadata = data.get("footer_metadata", {})
        self.file_status = data.get("file_status")
        self.last_updated = data.get("last_updated")
        # Links
        self.links: list[LinkInfo] = data.get("links", [])


class ContentParser:
    """High-level content parser for markdown files.

    Wraps FrontmatterParser with a cleaner interface.
    """

    def __init__(self):
        """Initialize the content parser."""
        self._parser = FrontmatterParser()

    def parse(self, path: Path) -> ParsedContent:
        """Parse a markdown file.

        Args:
            path: Path to the file

        Returns:
            ParsedContent with extracted metadata
        """
        data = self._parser.parse_file(path)
        return ParsedContent(data)

    def parse_content(self, content: str, filename: str = "") -> ParsedContent:
        """Parse markdown content string.

        Args:
            content: Markdown content
            filename: Optional filename for doc_type detection

        Returns:
            ParsedContent with extracted metadata
        """
        data = self._parser.parse_content(content, filename)
        return ParsedContent(data)


def update_file_status(path: Path, new_status: str) -> bool:
    """Update the file status in a markdown file's footer metadata.

    Looks for **Status do arquivo**: <value> and updates it.

    Args:
        path: Path to the markdown file
        new_status: New status value (e.g., "Approved", "Rejected", "Review")

    Returns:
        True if updated successfully, False otherwise
    """
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, IOError, UnicodeDecodeError):
        return False

    # Pattern to match the status line
    status_pattern = re.compile(
        r"(\*\*Status do arquivo\*\*\s*:\s*)(.+?)(\s*$)",
        re.MULTILINE,
    )

    match = status_pattern.search(content)
    if not match:
        # Status line doesn't exist - try to add it
        # Look for the footer section (after last ---)
        if "\n---\n" in content:
            # Add status after the last ---
            parts = content.rsplit("\n---\n", 1)
            if len(parts) == 2:
                new_content = (
                    parts[0] + "\n---\n" +
                    f"**Status do arquivo**: {new_status}\n" +
                    parts[1]
                )
            else:
                return False
        else:
            # Add footer section at the end
            new_content = (
                content.rstrip() + "\n\n---\n\n" +
                f"**Status do arquivo**: {new_status}\n"
            )
    else:
        # Replace existing status
        new_content = status_pattern.sub(
            rf"\g<1>{new_status}\3",
            content,
        )

    try:
        path.write_text(new_content, encoding="utf-8")
        return True
    except (OSError, IOError):
        return False


def update_file_metadata(path: Path, updates: dict[str, str]) -> bool:
    """Update multiple footer metadata fields in a markdown file.

    Args:
        path: Path to the markdown file
        updates: Dictionary of key-value pairs to update

    Returns:
        True if updated successfully, False otherwise
    """
    try:
        content = path.read_text(encoding="utf-8")
    except (OSError, IOError, UnicodeDecodeError):
        return False

    for key, value in updates.items():
        # Pattern to match the metadata line
        pattern = re.compile(
            rf"(\*\*{re.escape(key)}\*\*\s*:\s*)(.+?)(\s*$)",
            re.MULTILINE,
        )

        match = pattern.search(content)
        if match:
            # Replace existing value
            content = pattern.sub(rf"\g<1>{value}\3", content)
        else:
            # Add new field before the last line of footer metadata
            # or at end of file
            footer_pattern = re.compile(r"(\n---\n.*?)$", re.DOTALL)
            footer_match = footer_pattern.search(content)
            if footer_match:
                # Insert before end of footer section
                insert_pos = footer_match.end()
                content = (
                    content[:insert_pos].rstrip() +
                    f"\n**{key}**: {value}" +
                    content[insert_pos:]
                )
            else:
                # Add footer section
                content = (
                    content.rstrip() + "\n\n---\n\n" +
                    f"**{key}**: {value}\n"
                )

    try:
        path.write_text(content, encoding="utf-8")
        return True
    except (OSError, IOError):
        return False
