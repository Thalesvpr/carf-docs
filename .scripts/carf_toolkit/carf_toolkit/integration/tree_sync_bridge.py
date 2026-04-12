"""Bridge to integrate carf_tree_sync functionality."""

import sys
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class SyncPreview:
    """Preview of changes to be made by tree sync."""
    path: Path
    old_content: str
    new_content: str
    has_changes: bool
    message: str


class TreeSyncBridge:
    """Bridge to carf_tree_sync for syncing README trees."""

    def __init__(self, root_path: Optional[Path] = None):
        """Initialize the tree sync bridge.

        Args:
            root_path: Root directory for tree sync
        """
        self.root_path = root_path
        self._available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if carf_tree_sync is available."""
        try:
            # Add scripts directory to path if needed
            scripts_dir = Path(__file__).parent.parent.parent.parent
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))

            from carf_tree_sync import TreeSyncPipeline
            return True
        except ImportError:
            return False

    @property
    def is_available(self) -> bool:
        """Check if tree sync is available."""
        return self._available

    def set_root_path(self, root_path: Path) -> None:
        """Set the root path for tree sync.

        Args:
            root_path: Root directory path
        """
        self.root_path = root_path

    def can_sync(self, file_path: Path) -> bool:
        """Check if a file can be synced (is a README with markers).

        Args:
            file_path: Path to the file

        Returns:
            True if file can be synced
        """
        if not self._available:
            return False

        # Must be a README file
        if not file_path.name.lower().startswith("readme"):
            return False

        # Check if it has the generated section markers
        try:
            content = file_path.read_text(encoding="utf-8")
            return "<!-- GENERATED:START" in content or self._has_syncable_children(file_path)
        except Exception:
            return False

    def _has_syncable_children(self, readme_path: Path) -> bool:
        """Check if the README's directory has files that could be indexed.

        Args:
            readme_path: Path to the README file

        Returns:
            True if directory has markdown files or subdirectories
        """
        parent_dir = readme_path.parent

        # Check for markdown files (excluding README)
        md_files = [f for f in parent_dir.glob("*.md") if not f.name.lower().startswith("readme")]
        if md_files:
            return True

        # Check for subdirectories with READMEs
        for subdir in parent_dir.iterdir():
            if subdir.is_dir() and (subdir / "README.md").exists():
                return True

        return False

    def preview_sync(self, file_path: Path) -> Optional[SyncPreview]:
        """Preview what changes would be made by syncing.

        Args:
            file_path: Path to the README file

        Returns:
            SyncPreview with diff information, or None if not syncable
        """
        if not self._available or not self.root_path:
            return None

        if not self.can_sync(file_path):
            return None

        try:
            # Add scripts directory to path if needed
            scripts_dir = Path(__file__).parent.parent.parent.parent
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))

            from carf_tree_sync.scanner.tree import TreeScanner, NodeType
            from carf_tree_sync.indexer import FilesIndexer, SubfoldersIndexer
            from carf_tree_sync.parser.generated import GeneratedSectionParser
            from carf_tree_sync.writer.updater import ReadmeUpdater

            # Find the node for this README
            scanner = TreeScanner(self.root_path)
            nodes = scanner.scan()

            readme_dir = file_path.parent
            node = nodes.get(readme_dir)

            if node is None:
                return SyncPreview(
                    path=file_path,
                    old_content="",
                    new_content="",
                    has_changes=False,
                    message="Directory not found in tree scan"
                )

            # Generate indices
            indexers = [FilesIndexer(), SubfoldersIndexer()]
            index_results = []

            for indexer in indexers:
                if indexer.can_index(node):
                    result = indexer.generate(node, self.root_path)
                    if result:
                        index_results.append(result)

            if not index_results:
                return SyncPreview(
                    path=file_path,
                    old_content="",
                    new_content="",
                    has_changes=False,
                    message="No indices to generate"
                )

            # Read current content
            old_content = file_path.read_text(encoding="utf-8")

            # Parse and rebuild
            parser = GeneratedSectionParser()
            parsed = parser.parse(old_content)

            # Combine index results
            combined_content = "\n\n".join(r.content for r in index_results)

            new_content = parser.rebuild(parsed, combined_content)

            has_changes = old_content != new_content

            return SyncPreview(
                path=file_path,
                old_content=old_content,
                new_content=new_content,
                has_changes=has_changes,
                message="Changes detected" if has_changes else "No changes needed"
            )

        except Exception as e:
            return SyncPreview(
                path=file_path,
                old_content="",
                new_content="",
                has_changes=False,
                message=f"Error: {str(e)}"
            )

    def apply_sync(self, file_path: Path) -> tuple[bool, str]:
        """Apply tree sync to a README file.

        Args:
            file_path: Path to the README file

        Returns:
            Tuple of (success, message)
        """
        preview = self.preview_sync(file_path)

        if preview is None:
            return False, "File cannot be synced"

        if not preview.has_changes:
            return True, "No changes needed"

        try:
            file_path.write_text(preview.new_content, encoding="utf-8")
            return True, "Tree sync applied successfully"
        except Exception as e:
            return False, f"Failed to write file: {str(e)}"

    def sync_all(self, dry_run: bool = False) -> dict:
        """Sync all README files in the tree.

        Args:
            dry_run: If True, don't actually write changes

        Returns:
            Dictionary with sync results
        """
        if not self._available or not self.root_path:
            return {"error": "Tree sync not available"}

        try:
            from carf_tree_sync import TreeSyncPipeline

            pipeline = TreeSyncPipeline(
                root_dir=self.root_path,
                dry_run=dry_run,
                verbose=False
            )
            report = pipeline.run()

            return {
                "total_nodes": report.total_nodes,
                "updated_nodes": report.updated_nodes,
                "unchanged_nodes": report.unchanged_nodes,
                "error_nodes": report.error_nodes,
                "dry_run": report.dry_run,
                "results": [
                    {
                        "path": str(r.path),
                        "updated": r.updated,
                        "message": r.message,
                    }
                    for r in report.results
                ]
            }

        except Exception as e:
            return {"error": str(e)}
