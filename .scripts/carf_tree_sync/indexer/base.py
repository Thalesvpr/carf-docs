"""Base indexer interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from ..scanner.tree import TreeNode


@dataclass
class IndexResult:
    """Result of index generation."""

    content: str  # Generated markdown content
    item_count: int  # Number of items in index
    title: str  # Section title (e.g., "Indice por Dominio (42 requisitos)")


class Indexer(ABC):
    """Abstract base class for indexers."""

    name: str = "base"
    description: str = "Base indexer"

    @abstractmethod
    def can_index(self, node: TreeNode) -> bool:
        """Check if this indexer applies to the given node."""
        pass

    @abstractmethod
    def generate(self, node: TreeNode, root_dir: Path) -> Optional[IndexResult]:
        """Generate index content for the node."""
        pass

    def _make_relative_path(
        self, from_path: Path, to_path: Path
    ) -> str:
        """Create relative path from one location to another."""
        try:
            # Get relative path
            rel = to_path.relative_to(from_path.parent)
            return "./" + str(rel).replace("\\", "/")
        except ValueError:
            # Not relative, try another approach
            try:
                from_parts = from_path.parent.parts
                to_parts = to_path.parts

                # Find common prefix
                common_len = 0
                for i, (a, b) in enumerate(zip(from_parts, to_parts)):
                    if a == b:
                        common_len = i + 1
                    else:
                        break

                # Build relative path
                ups = len(from_parts) - common_len
                downs = to_parts[common_len:]

                parts = [".."] * ups + list(downs)
                return "/".join(parts)
            except Exception:
                return str(to_path)
