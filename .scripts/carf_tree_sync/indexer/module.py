"""Indexer for grouping documents by module."""

from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from .base import Indexer, IndexResult
from ..scanner.tree import TreeNode, NodeType
from ..parser.document import DocumentParser, DocumentInfo
from ..config import MODULE_ORDER, TIMESTAMP_FORMAT


class ModuleIndexer(Indexer):
    """Generates index grouped by module from frontmatter.

    Output format:
    ## Indice por Modulo

    ### GEOWEB

    | ID | Titulo |
    |:---|:-------|
    | [RF-001](./path.md) | Titulo |
    """

    name = "module"
    description = "Indice de documentos agrupados por modulo"

    def __init__(self):
        self.doc_parser = DocumentParser()

    def can_index(self, node: TreeNode) -> bool:
        """Check if any files have modules in frontmatter."""
        for file_path in node.files:
            doc = self.doc_parser.parse(file_path)
            if doc and doc.frontmatter and doc.frontmatter.modules:
                return True
        return False

    def generate(self, node: TreeNode, root_dir: Path) -> Optional[IndexResult]:
        """Generate module-based index."""
        # Group documents by module
        by_module: Dict[str, List[DocumentInfo]] = defaultdict(list)
        no_module: List[DocumentInfo] = []

        for file_path in node.files:
            doc = self.doc_parser.parse(file_path)
            if not doc:
                continue

            if doc.frontmatter and doc.frontmatter.modules:
                for module in doc.frontmatter.modules:
                    by_module[module.upper()].append(doc)
            else:
                no_module.append(doc)

        if not by_module:
            return None

        lines = []
        lines.append("## Indice por Modulo")
        lines.append("")

        total_count = 0

        # Order modules according to MODULE_ORDER, then alphabetically for unknown
        module_names = list(by_module.keys())
        ordered_modules = []

        for module in MODULE_ORDER:
            if module in module_names:
                ordered_modules.append(module)
                module_names.remove(module)

        # Add remaining modules alphabetically
        ordered_modules.extend(sorted(module_names))

        for module in ordered_modules:
            docs = sorted(by_module[module], key=lambda d: self._sort_key(d))
            # Remove duplicates (same doc might appear if it has same module listed twice)
            seen = set()
            unique_docs = []
            for doc in docs:
                if doc.path not in seen:
                    seen.add(doc.path)
                    unique_docs.append(doc)

            total_count += len(unique_docs)

            lines.append(f"### {module}")
            lines.append("")
            lines.append("| ID | Titulo |")
            lines.append("|:---|:-------|")

            for doc in unique_docs:
                row = self._format_row(doc, node.readme_path)
                lines.append(row)

            lines.append("")

        # Add documents without module
        if no_module:
            lines.append("### Sem Modulo")
            lines.append("")
            lines.append("| ID | Titulo |")
            lines.append("|:---|:-------|")

            for doc in sorted(no_module, key=lambda d: self._sort_key(d)):
                row = self._format_row(doc, node.readme_path)
                lines.append(row)
                total_count += 1

            lines.append("")

        lines.append(f"*Gerado automaticamente em {datetime.now().strftime(TIMESTAMP_FORMAT)}*")

        return IndexResult(
            content="\n".join(lines) + "\n",
            item_count=total_count,
            title=f"Indice por Modulo ({len(ordered_modules)} modulos)",
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
