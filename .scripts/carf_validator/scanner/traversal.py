"""Scanner de filesystem para arquivos Markdown."""

from pathlib import Path
from typing import Iterator, Set, List
from dataclasses import dataclass, field


@dataclass
class ScanConfig:
    """Configuração para varredura de diretórios."""
    root_dir: Path
    include_patterns: List[str] = field(default_factory=lambda: ["**/*.md"])
    exclude_dirs: Set[str] = field(default_factory=lambda: {
        ".git",
        "node_modules",
        "dist",
        "build",
        ".next",
        ".cache",
        "bin",
        "obj",
        "SRC-CODE",
        ".obsidian",
        ".vscode",
        ".idea",
        "__pycache__",
        ".pytest_cache",
    })
    exclude_files: Set[str] = field(default_factory=set)

    @classmethod
    def default(cls, root_dir: Path) -> "ScanConfig":
        """Cria configuração padrão."""
        return cls(root_dir=root_dir)


class FileScanner:
    """Scanner de filesystem para arquivos Markdown."""

    def __init__(self, config: ScanConfig):
        """
        Inicializa scanner.

        Args:
            config: Configuração de varredura
        """
        self.config = config

    def scan(self) -> Iterator[Path]:
        """
        Varre filesystem e retorna arquivos markdown.

        Yields:
            Paths de arquivos markdown encontrados
        """
        for pattern in self.config.include_patterns:
            for file_path in self.config.root_dir.glob(pattern):
                if self._should_include(file_path):
                    yield file_path

    def _should_include(self, path: Path) -> bool:
        """
        Verifica se path deve ser incluído.

        Args:
            path: Path a verificar

        Returns:
            True se deve ser incluído
        """
        # Verifica diretórios excluídos
        for parent in path.parents:
            if parent.name in self.config.exclude_dirs:
                return False

        # Verifica arquivos excluídos
        if path.name in self.config.exclude_files:
            return False

        return True

    def count(self) -> int:
        """
        Conta arquivos que serão escaneados.

        Returns:
            Número de arquivos
        """
        return sum(1 for _ in self.scan())


def find_markdown_files(root_dir: Path, exclude_dirs: Set[str] = None) -> List[Path]:
    """
    Função utilitária para encontrar arquivos markdown.

    Args:
        root_dir: Diretório raiz
        exclude_dirs: Diretórios a excluir

    Returns:
        Lista de paths de arquivos markdown
    """
    if exclude_dirs is None:
        exclude_dirs = ScanConfig.default(root_dir).exclude_dirs

    config = ScanConfig(root_dir=root_dir, exclude_dirs=exclude_dirs)
    scanner = FileScanner(config)
    return list(scanner.scan())
