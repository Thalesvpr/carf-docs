"""Parser for GENERATED sections in markdown files."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import re

from ..config import GENERATED_START, GENERATED_END


@dataclass
class ParsedContent:
    """Content split around GENERATED markers."""

    before: str  # Content before GENERATED:START
    generated: Optional[str]  # Content between markers (or None if no markers)
    after: str  # Content after GENERATED:END

    @property
    def has_generated_section(self) -> bool:
        """Check if file has GENERATED markers."""
        return self.generated is not None


class GeneratedSectionParser:
    """Parser for GENERATED sections."""

    def __init__(self):
        # Pattern to match the entire generated section
        # Matches both "Não" and "Nao" variants
        self.pattern = re.compile(
            r"(<!-- GENERATED:START[^>]*-->)(.*?)(<!-- GENERATED:END -->)",
            re.DOTALL,
        )

    def parse(self, content: str) -> ParsedContent:
        """Parse content into before/generated/after sections."""
        match = self.pattern.search(content)

        if not match:
            return ParsedContent(
                before=content,
                generated=None,
                after="",
            )

        start_pos = match.start()
        end_pos = match.end()

        return ParsedContent(
            before=content[:start_pos],
            generated=match.group(2),
            after=content[end_pos:],
        )

    def parse_file(self, file_path: Path) -> Optional[ParsedContent]:
        """Parse file content."""
        try:
            content = file_path.read_text(encoding="utf-8")
            return self.parse(content)
        except Exception:
            return None

    def rebuild(
        self, parsed: ParsedContent, new_generated: str
    ) -> str:
        """Rebuild content with new generated section."""
        if parsed.has_generated_section:
            # Replace existing section
            return (
                parsed.before
                + GENERATED_START
                + "\n"
                + new_generated
                + GENERATED_END
                + parsed.after
            )
        else:
            # Add new section at the end
            before = parsed.before.rstrip()
            return (
                before
                + "\n\n"
                + GENERATED_START
                + "\n"
                + new_generated
                + GENERATED_END
                + "\n"
            )
