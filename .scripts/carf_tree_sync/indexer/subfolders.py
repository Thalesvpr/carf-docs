"""Indexer for subdirectories with file counts."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from .base import Indexer, IndexResult
from ..scanner.tree import TreeNode, NodeType
from ..config import DOMAIN_NAMES, REQUIREMENT_TYPES, TIMESTAMP_FORMAT


class SubfoldersIndexer(Indexer):
    """Generates index of subdirectories with file counts.

    Output format:
    ## Indice por Dominio (N requisitos)

    | # | Dominio | Arquivos |
    |:--|:--------|:--------:|
    | 01 | [Nome Legivel](./01-slug/README.md) | 16 |
    """

    name = "subfolders"
    description = "Indice de subpastas com contagem de arquivos"

    def can_index(self, node: TreeNode) -> bool:
        """Check if node has subdirectories with READMEs."""
        return node.node_type in (NodeType.INTERMEDIATE, NodeType.ROOT) and len(
            node.children
        ) > 0

    def generate(self, node: TreeNode, root_dir: Path) -> Optional[IndexResult]:
        """Generate subfolder index."""
        if not self.can_index(node):
            return None

        children = sorted(node.children, key=lambda n: n.name)
        total_files = sum(c.count_files_recursive() for c in children)

        # Determine item type label
        item_label = self._get_item_label(node, total_files)

        lines = []
        lines.append(f"## Indice por Dominio ({total_files} {item_label})")
        lines.append("")
        lines.append("| # | Dominio | Arquivos |")
        lines.append("|:--|:--------|:--------:|")

        for child in children:
            row = self._format_row(child, node.readme_path)
            lines.append(row)

        lines.append("")
        lines.append(f"*Gerado automaticamente em {datetime.now().strftime(TIMESTAMP_FORMAT)}*")

        return IndexResult(
            content="\n".join(lines) + "\n",
            item_count=len(children),
            title=f"Indice por Dominio ({total_files} {item_label})",
        )

    def _format_row(self, child: TreeNode, from_path: Path) -> str:
        """Format a single row for the table."""
        name = child.name
        file_count = child.count_files_recursive()

        # Try to get human-readable name
        display_name = DOMAIN_NAMES.get(name, self._humanize_name(name))

        # Extract number prefix if present
        number = ""
        if name[:2].isdigit():
            number = name[:2]

        # Build relative path
        rel_path = self._make_relative_path(from_path, child.readme_path)

        return f"| {number} | [{display_name}]({rel_path}) | {file_count} |"

    def _humanize_name(self, name: str) -> str:
        """Convert slug to human-readable name."""
        # Remove number prefix
        if len(name) > 3 and name[2] == "-":
            name = name[3:]

        # Replace hyphens with spaces and capitalize
        words = name.replace("-", " ").replace("_", " ").split()
        return " ".join(w.capitalize() for w in words)

    def _get_item_label(self, node: TreeNode, count: int) -> str:
        """Get appropriate item label based on parent folder."""
        parent_name = node.name.upper()

        # Check if in a known requirement type folder
        for folder_name, config in REQUIREMENT_TYPES.items():
            if folder_name in parent_name:
                return config["plural"] if count != 1 else config["singular"]

        return "arquivos" if count != 1 else "arquivo"
