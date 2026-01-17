"""Scanner de filesystem e parsing de documentos."""

from .traversal import FileScanner, ScanConfig
from .tree import DocumentTreeBuilder

__all__ = [
    "FileScanner",
    "ScanConfig",
    "DocumentTreeBuilder",
]
