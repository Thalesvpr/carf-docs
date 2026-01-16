"""Tree scanner for discovering and classifying nodes."""

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Set
import re

from ..config import EXCLUDE_DIRS, REQUIREMENT_TYPES


class NodeType(Enum):
    """Classification of tree nodes."""

    LEAF = auto()  # Directory with only files (no subdirectories with READMEs)
    INTERMEDIATE = auto()  # Directory with subdirectories that have READMEs
    ROOT = auto()  # Top-level directory (CENTRAL, PROJECTS)


@dataclass
class TreeNode:
    """Represents a node in the directory tree."""

    path: Path
    readme_path: Path
    node_type: NodeType
    parent: Optional["TreeNode"] = None
    children: List["TreeNode"] = field(default_factory=list)
    files: List[Path] = field(default_factory=list)
    depth: int = 0

    @property
    def name(self) -> str:
        """Directory name."""
        return self.path.name

    @property
    def relative_path(self) -> str:
        """Path relative to root."""
        return str(self.path)

    def has_subfolders_with_readmes(self) -> bool:
        """Check if this node has subdirectories with README files."""
        return len(self.children) > 0

    def count_files(self) -> int:
        """Count markdown files (excluding README)."""
        return len(self.files)

    def count_files_recursive(self) -> int:
        """Count all files recursively including children."""
        total = len(self.files)
        for child in self.children:
            total += child.count_files_recursive()
        return total


class TreeScanner:
    """Scans directory tree and builds node hierarchy."""

    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.nodes: Dict[Path, TreeNode] = {}
        self._file_pattern = re.compile(r"^(RF|US|UC|RNF|ADR)-\d+.*\.md$", re.IGNORECASE)

    def scan(self) -> Dict[Path, TreeNode]:
        """Scan directory tree and return all nodes."""
        self._scan_recursive(self.root_dir, depth=0)
        self._classify_nodes()
        return self.nodes

    def _should_exclude(self, path: Path) -> bool:
        """Check if directory should be excluded."""
        # Exclude hidden directories (starting with .)
        if path.name.startswith("."):
            return True
        return path.name in EXCLUDE_DIRS

    def _scan_recursive(
        self, current_path: Path, depth: int, parent: Optional[TreeNode] = None
    ) -> Optional[TreeNode]:
        """Recursively scan directory tree."""
        if not current_path.is_dir():
            return None

        if self._should_exclude(current_path):
            return None

        readme_path = current_path / "README.md"
        if not readme_path.exists():
            # Still scan children even if no README
            for child in sorted(current_path.iterdir()):
                if child.is_dir():
                    self._scan_recursive(child, depth + 1, parent)
            return None

        # Create node for this directory
        node = TreeNode(
            path=current_path,
            readme_path=readme_path,
            node_type=NodeType.LEAF,  # Default, will be reclassified
            parent=parent,
            depth=depth,
        )

        # Find markdown files (excluding README)
        for file_path in sorted(current_path.iterdir()):
            if file_path.is_file() and file_path.suffix == ".md":
                if file_path.name.lower() != "readme.md":
                    node.files.append(file_path)

        # Scan children directories
        for child_path in sorted(current_path.iterdir()):
            if child_path.is_dir() and not self._should_exclude(child_path):
                child_node = self._scan_recursive(child_path, depth + 1, node)
                if child_node is not None:
                    node.children.append(child_node)

        self.nodes[current_path] = node
        return node

    def _classify_nodes(self) -> None:
        """Classify nodes as LEAF, INTERMEDIATE, or ROOT."""
        for node in self.nodes.values():
            if node.depth == 0:
                # Top-level directories
                node.node_type = NodeType.ROOT
            elif node.has_subfolders_with_readmes():
                node.node_type = NodeType.INTERMEDIATE
            else:
                node.node_type = NodeType.LEAF

    def get_nodes_bottom_up(self) -> Iterator[TreeNode]:
        """
        Iterate nodes bottom-up (leaves first, then intermediate, then root).

        This ensures that when we process a parent node, all its children
        have already been processed and their indices are up-to-date.
        """
        # Sort by depth descending (deepest first)
        sorted_nodes = sorted(self.nodes.values(), key=lambda n: -n.depth)
        yield from sorted_nodes

    def get_leaves(self) -> Iterator[TreeNode]:
        """Get all leaf nodes."""
        for node in self.nodes.values():
            if node.node_type == NodeType.LEAF:
                yield node

    def get_intermediate(self) -> Iterator[TreeNode]:
        """Get all intermediate nodes."""
        for node in self.nodes.values():
            if node.node_type == NodeType.INTERMEDIATE:
                yield node

    def get_roots(self) -> Iterator[TreeNode]:
        """Get all root nodes."""
        for node in self.nodes.values():
            if node.node_type == NodeType.ROOT:
                yield node

    def get_node(self, path: Path) -> Optional[TreeNode]:
        """Get node by path."""
        return self.nodes.get(path)
