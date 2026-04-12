"""Frontmatter parser for extracting YAML metadata."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
import re


@dataclass
class Frontmatter:
    """Parsed frontmatter data."""

    modules: List[str] = field(default_factory=list)
    epic: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    status: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


class FrontmatterParser:
    """Parser for YAML frontmatter in markdown files."""

    FRONTMATTER_PATTERN = re.compile(
        r"^---\s*\n(.*?)\n---\s*\n",
        re.DOTALL,
    )

    def parse(self, content: str) -> Optional[Frontmatter]:
        """Parse frontmatter from markdown content."""
        match = self.FRONTMATTER_PATTERN.match(content)
        if not match:
            return None

        yaml_content = match.group(1)
        return self._parse_yaml(yaml_content)

    def _parse_yaml(self, yaml_str: str) -> Frontmatter:
        """Simple YAML parser for frontmatter (no external deps)."""
        result = Frontmatter()
        current_key = None
        list_items: List[str] = []

        for line in yaml_str.split("\n"):
            line = line.rstrip()

            if not line or line.startswith("#"):
                continue

            # List item
            if line.startswith("  - ") or line.startswith("- "):
                item = line.lstrip(" -").strip()
                if current_key:
                    list_items.append(item)
                continue

            # Key-value pair
            if ":" in line:
                # Save previous list if any
                if current_key and list_items:
                    self._set_field(result, current_key, list_items)
                    list_items = []

                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip()

                if value:
                    # Inline value
                    self._set_field(result, key, value)
                    current_key = None
                else:
                    # Expecting list
                    current_key = key

        # Handle trailing list
        if current_key and list_items:
            self._set_field(result, current_key, list_items)

        return result

    def _set_field(
        self, fm: Frontmatter, key: str, value: Any
    ) -> None:
        """Set frontmatter field."""
        key_lower = key.lower()

        if key_lower == "modules":
            if isinstance(value, list):
                fm.modules = value
            else:
                fm.modules = [value]
        elif key_lower == "epic":
            fm.epic = str(value) if value else None
        elif key_lower == "tags":
            if isinstance(value, list):
                fm.tags = value
            else:
                fm.tags = [value]
        elif key_lower == "status":
            fm.status = str(value) if value else None

        # Always store in raw
        fm.raw[key] = value

    def parse_file(self, file_path: Path) -> Optional[Frontmatter]:
        """Parse frontmatter from file."""
        try:
            content = file_path.read_text(encoding="utf-8")
            return self.parse(content)
        except Exception:
            return None
