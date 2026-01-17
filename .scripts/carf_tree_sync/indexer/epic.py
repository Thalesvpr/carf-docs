"""Indexer for grouping documents by epic."""

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .base import Indexer, IndexResult
from ..scanner.tree import TreeNode, NodeType
from ..parser.document import DocumentParser, DocumentInfo
from ..config import TIMESTAMP_FORMAT


class EpicIndexer(Indexer):
    """Generates index grouped by epic from frontmatter.

    Output format:
    ## Indice por Epica

    ### Epica: Nome da Epica

    | ID | Titulo |
    |:---|:-------|
    | [US-001](./path.md) | Titulo |
    """

    name = "epic"
    description = "Indice de documentos agrupados por epica"

    def __init__(self):
        self.doc_parser = DocumentParser()

    def can_index(self, node: TreeNode) -> bool:
        """Check if any files have epic in frontmatter."""
        for file_path in node.files:
            doc = self.doc_parser.parse(file_path)
            if doc and doc.frontmatter and doc.frontmatter.epic:
                return True
        return False

    def generate(self, node: TreeNode, root_dir: Path) -> Optional[IndexResult]:
        """Generate epic-based index."""
        # Group documents by epic
        by_epic: Dict[str, List[DocumentInfo]] = defaultdict(list)
        no_epic: List[DocumentInfo] = []

        for file_path in node.files:
            doc = self.doc_parser.parse(file_path)
            if not doc:
                continue

            if doc.frontmatter and doc.frontmatter.epic:
                by_epic[doc.frontmatter.epic].append(doc)
            else:
                no_epic.append(doc)

        if not by_epic:
            return None

        lines = []
        lines.append("## Indice por Epica")
        lines.append("")

        total_count = 0

        # Sort epics alphabetically
        for epic in sorted(by_epic.keys()):
            docs = sorted(by_epic[epic], key=lambda d: self._sort_key(d))
            total_count += len(docs)

            lines.append(f"### Epica: {epic}")
            lines.append("")
            lines.append("| ID | Titulo |")
            lines.append("|:---|:-------|")

            for doc in docs:
                row = self._format_row(doc, node.readme_path)
                lines.append(row)

            lines.append("")

        # Add documents without epic
        if no_epic:
            lines.append("### Sem Epica")
            lines.append("")
            lines.append("| ID | Titulo |")
            lines.append("|:---|:-------|")

            for doc in sorted(no_epic, key=lambda d: self._sort_key(d)):
                row = self._format_row(doc, node.readme_path)
                lines.append(row)
                total_count += 1

            lines.append("")

        lines.append(f"*Gerado automaticamente em {datetime.now().strftime(TIMESTAMP_FORMAT)}*")

        return IndexResult(
            content="\n".join(lines) + "\n",
            item_count=total_count,
            title=f"Indice por Epica ({len(by_epic)} epicas)",
        )

    def _sort_key(self, doc: DocumentInfo) -> tuple:
        """Generate sort key for document."""
        if doc.identifier:
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
        rel_path = self._make_relative_path(from_path, doc.path)
        return f"| [{display_id}]({rel_path}) | {title} |"
