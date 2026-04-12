"""Deterministic file discovery with 100% coverage guarantee."""

import hashlib
from pathlib import Path
from typing import Iterator

from ..models.file_item import FileItem, FileStatus


class DeterministicScanner:
    """Scanner that guarantees 100% file coverage.

    This scanner finds ALL files matching the given patterns without any
    content-based filtering or automatic selection. Files are sorted
    deterministically by path for consistent ordering.

    Attributes:
        root_path: The root directory to scan
        include_patterns: Glob patterns for files to include
        exclude_dirs: Directory names to exclude
    """

    def __init__(
        self,
        root_path: Path,
        include_patterns: list[str] | None = None,
        exclude_dirs: list[str] | None = None,
    ):
        """Initialize the scanner.

        Args:
            root_path: Root directory to scan
            include_patterns: Glob patterns (default: ["**/*.md"])
            exclude_dirs: Directories to skip (default: common excludes)
        """
        self.root_path = root_path.resolve()
        self.include_patterns = include_patterns or ["**/*.md"]
        self.exclude_dirs = set(
            exclude_dirs
            or [
                ".git",
                ".obsidian",
                ".scripts",
                "SRC-CODE",
                "node_modules",
                "file-curator",
                "__pycache__",
                ".venv",
                "venv",
            ]
        )

    def scan(self) -> list[FileItem]:
        """Scan and return all matching files.

        Returns:
            List of FileItem objects sorted by relative path
        """
        files = list(self._discover_files())
        # Sort deterministically by relative path
        files.sort(key=lambda f: f.relative_path.lower())
        return files

    def scan_iter(self) -> Iterator[FileItem]:
        """Iterate over discovered files (unsorted).

        Yields:
            FileItem objects as they are discovered
        """
        yield from self._discover_files()

    def count(self) -> int:
        """Count total matching files without loading all data.

        Returns:
            Number of matching files
        """
        return sum(1 for _ in self._discover_paths())

    def _discover_files(self) -> Iterator[FileItem]:
        """Discover files and create FileItem objects.

        Yields:
            FileItem for each matching file
        """
        for path in self._discover_paths():
            yield self._create_file_item(path)

    def _discover_paths(self) -> Iterator[Path]:
        """Discover matching file paths.

        Yields:
            Path objects for matching files
        """
        for pattern in self.include_patterns:
            for path in self.root_path.glob(pattern):
                if path.is_file() and self._should_include(path):
                    yield path

    def _should_include(self, path: Path) -> bool:
        """Check if a path should be included.

        Args:
            path: Path to check

        Returns:
            True if the path should be included
        """
        # Check if any parent directory is in the exclude list
        for parent in path.relative_to(self.root_path).parents:
            if parent.name in self.exclude_dirs:
                return False

        # Check if the file's immediate parent is excluded
        if path.parent.name in self.exclude_dirs:
            return False

        return True

    def _create_file_item(self, path: Path) -> FileItem:
        """Create a FileItem from a path.

        Args:
            path: Path to the file

        Returns:
            FileItem with basic info populated
        """
        relative_path = str(path.relative_to(self.root_path))
        file_hash = self._compute_hash(path)

        return FileItem(
            path=path,
            relative_path=relative_path,
            file_hash=file_hash,
            status=FileStatus.PENDING,
        )

    def _compute_hash(self, path: Path) -> str:
        """Compute SHA256 hash of file contents.

        Args:
            path: Path to the file

        Returns:
            Hex-encoded SHA256 hash
        """
        sha256 = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except (OSError, IOError):
            return ""

    def has_changed(self, item: FileItem) -> bool:
        """Check if a file has changed since last scan.

        Args:
            item: FileItem to check

        Returns:
            True if the file hash has changed
        """
        current_hash = self._compute_hash(item.path)
        return current_hash != item.file_hash

    def refresh_item(self, item: FileItem) -> FileItem:
        """Refresh a FileItem with current file data.

        Args:
            item: FileItem to refresh

        Returns:
            Updated FileItem
        """
        if not item.path.exists():
            return item

        new_hash = self._compute_hash(item.path)
        return FileItem(
            path=item.path,
            relative_path=item.relative_path,
            file_hash=new_hash,
            title=item.title,
            doc_type=item.doc_type,
            frontmatter_modules=item.frontmatter_modules,
            frontmatter_epic=item.frontmatter_epic,
            word_count=item.word_count,
            status=item.status,
            review_count=item.review_count,
            skip_count=item.skip_count,
            created_at=item.created_at,
            updated_at=item.updated_at,
            last_reviewed_at=item.last_reviewed_at,
        )
