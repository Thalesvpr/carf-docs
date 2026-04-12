"""Indexer for files within a directory."""

from datetime import datetime
from pathlib import Path
from typing import Optional, List

from .base import Indexer, IndexResult
from ..scanner.tree import TreeNode, NodeType
from ..parser.document import DocumentParser, DocumentInfo
from ..config import REQUIREMENT_TYPES, TIMESTAMP_FORMAT


class FilesIndexer(Indexer):
    """Generates index of files in a directory.

    Output format:
    ## Arquivos (N requisitos)

    | ID | Titulo |
    |:---|:-------|
    | [RF-001](./RF-001-xxx.md) | Titulo do Requisito |
    """

    name = "files"
    description = "Indice de arquivos com ID e titulo"

    def __init__(self):
        self.doc_parser = DocumentParser()

    def can_index(self, node: TreeNode) -> bool:
        """Check if node has files to index."""
        return len(node.files) > 0

    def generate(self, node: TreeNode, root_dir: Path) -> Optional[IndexResult]:
        """Generate file index."""
        if not self.can_index(node):
            return None

        # Parse all files
        docs = self._parse_and_sort(node.files)

        if not docs:
            return None

        # Determine item type label
        item_label = self._get_item_label(node, len(docs))

        lines = []
        lines.append(f"## Arquivos ({len(docs)} {item_label})")
        lines.append("")
        lines.append("| ID | Titulo |")
        lines.append("|:---|:-------|")

        for doc in docs:
            row = self._format_row(doc, node.readme_path)
            lines.append(row)

        lines.append("")
        lines.append(f"*Gerado automaticamente em {datetime.now().strftime(TIMESTAMP_FORMAT)}*")

        return IndexResult(
            content="\n".join(lines) + "\n",
            item_count=len(docs),
            title=f"Arquivos ({len(docs)} {item_label})",
        )

    def _parse_and_sort(self, files: List[Path]) -> List[DocumentInfo]:
        """Parse files and sort by identifier."""
        docs = []
        for file_path in files:
            doc = self.doc_parser.parse(file_path)
            if doc:
                docs.append(doc)

        # Sort by identifier (RF-001 before RF-002, etc.)
        return sorted(docs, key=lambda d: self._sort_key(d))

    def _sort_key(self, doc: DocumentInfo) -> tuple:
        """Generate sort key for document."""
        if doc.identifier:
            # Parse prefix and number
            parts = doc.identifier.split("-")
            if len(parts) >= 2:
                prefix = parts[0]
                try:
                    number = int(parts[1])
                    return (prefix, number)
                except ValueError:
                    pass
        return (doc.filename, 0)

    def _format_row(self, doc: DocumentInfo, from_path: Path) -> str:
        """Format a single row for the table."""
        display_id = doc.display_id
        title = doc.title or doc.filename

        # Build relative path
        rel_path = self._make_relative_path(from_path, doc.path)

        return f"| [{display_id}]({rel_path}) | {title} |"

    def _get_item_label(self, node: TreeNode, count: int) -> str:
        """Get appropriate item label based on parent folder."""
        # First check the path string for requirement type folder names
        path_str = str(node.path).upper()
        for folder_name, config in REQUIREMENT_TYPES.items():
            if folder_name in path_str:
                return config["plural"] if count != 1 else config["singular"]

        # Walk up parent nodes as fallback
        current = node.parent
        while current:
            for folder_name, config in REQUIREMENT_TYPES.items():
                if folder_name in current.name.upper():
                    return config["plural"] if count != 1 else config["singular"]
            current = current.parent

        return "arquivos" if count != 1 else "arquivo"
