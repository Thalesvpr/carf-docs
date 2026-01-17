"""
carf_tree_sync - Sistema de sincronizacao de indices para READMEs do CARF.

Este modulo implementa sincronizacao bottom-up de indices em arquivos README.md,
garantindo que ao processar um no pai, todos os filhos ja estejam atualizados.

Uso:
    python -m carf_tree_sync --root /c/DEV/CARF
    python -m carf_tree_sync --dry-run
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .scanner.tree import TreeScanner, TreeNode, NodeType
from .indexer import (
    Indexer,
    IndexResult,
    SubfoldersIndexer,
    FilesIndexer,
    EpicIndexer,
    ModuleIndexer,
)
from .writer.updater import ReadmeUpdater, UpdateResult


__version__ = "1.0.0"


@dataclass
class SyncReport:
    """Report of sync operation."""

    total_nodes: int = 0
    updated_nodes: int = 0
    unchanged_nodes: int = 0
    error_nodes: int = 0
    results: List[UpdateResult] = field(default_factory=list)
    dry_run: bool = False

    def add_result(self, result: UpdateResult) -> None:
        """Add an update result to the report."""
        self.results.append(result)
        self.total_nodes += 1

        if result.updated:
            self.updated_nodes += 1
        elif "Erro" in result.message:
            self.error_nodes += 1
        else:
            self.unchanged_nodes += 1


class TreeSyncPipeline:
    """Main pipeline for syncing README indices."""

    def __init__(
        self,
        root_dir: Path,
        dry_run: bool = False,
        verbose: bool = False,
    ):
        self.root_dir = Path(root_dir).resolve()
        self.dry_run = dry_run
        self.verbose = verbose

        # Initialize components
        self.scanner = TreeScanner(self.root_dir)
        self.updater = ReadmeUpdater(dry_run=dry_run)

        # Initialize indexers
        self.indexers: List[Indexer] = [
            SubfoldersIndexer(),
            FilesIndexer(),
        ]

    def run(self) -> SyncReport:
        """Run the sync pipeline."""
        report = SyncReport(dry_run=self.dry_run)

        # Phase 1: Scan tree
        nodes = self.scanner.scan()

        if self.verbose:
            print(f"Encontrados {len(nodes)} nos com README")

        # Phase 2: Process bottom-up
        for node in self.scanner.get_nodes_bottom_up():
            result = self._process_node(node)
            if result:
                report.add_result(result)

        return report

    def _process_node(self, node: TreeNode) -> Optional[UpdateResult]:
        """Process a single node."""
        # Collect applicable index results
        index_results: List[IndexResult] = []

        for indexer in self.indexers:
            if indexer.can_index(node):
                result = indexer.generate(node, self.root_dir)
                if result:
                    index_results.append(result)

        if not index_results:
            return None

        # Update README
        return self.updater.update(node.readme_path, index_results)


def sync_tree(
    root_dir: Path,
    dry_run: bool = False,
    verbose: bool = False,
) -> SyncReport:
    """Convenience function to run sync pipeline.

    Args:
        root_dir: Root directory to sync
        dry_run: If True, don't write changes
        verbose: If True, print progress

    Returns:
        SyncReport with results
    """
    pipeline = TreeSyncPipeline(
        root_dir=root_dir,
        dry_run=dry_run,
        verbose=verbose,
    )
    return pipeline.run()
