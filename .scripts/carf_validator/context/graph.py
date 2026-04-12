"""Grafo de relacionamentos entre documentos."""

from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum, auto

from .registry import DocumentRegistry


class RelationshipType(Enum):
    """Tipos de relacionamentos entre documentos."""
    LINKS_TO = auto()          # Link markdown genérico
    IMPLEMENTS = auto()        # Feature implementa RF/UC
    REFERENCES = auto()        # Documento referencia outro
    TRACES_TO = auto()         # UC rastreia para RF/US/RNF
    CHILD_OF = auto()          # Hierarquia de diretório


@dataclass
class Relationship:
    """Representa um relacionamento entre dois documentos."""
    source: Path
    target: Path
    rel_type: RelationshipType
    line_number: Optional[int] = None
    is_valid: bool = True
    error: Optional[str] = None
    target_raw: Optional[str] = None  # Target original do link
    link_text: Optional[str] = None   # Texto do link


class RelationshipGraph:
    """Grafo de relacionamentos entre documentos."""

    def __init__(self, registry: DocumentRegistry, root_dir: Path):
        """
        Inicializa grafo.

        Args:
            registry: Registry de documentos
            root_dir: Diretório raiz
        """
        self.registry = registry
        self.root_dir = root_dir
        self._outgoing: Dict[Path, List[Relationship]] = defaultdict(list)
        self._incoming: Dict[Path, List[Relationship]] = defaultdict(list)
        self._orphans: Set[Path] = set()
        self._isolated: Set[Path] = set()
        self._broken_links: List[Relationship] = []

    def build(self) -> None:
        """Constrói grafo de relacionamentos a partir dos documentos."""
        all_paths = set()
        has_outgoing = set()
        has_incoming = set()

        # Processa todos os documentos
        for doc in self.registry.all_documents():
            all_paths.add(doc.path)

            # Processa links
            for link in doc.links:
                if link.is_external:
                    continue

                rel = Relationship(
                    source=doc.path,
                    target=link.resolved_path if link.resolved_path else Path(link.target),
                    rel_type=RelationshipType.LINKS_TO,
                    line_number=link.line_number,
                    target_raw=link.target,
                    link_text=link.text,
                )

                # Verifica se target existe
                if link.resolved_path and link.resolved_path.exists():
                    rel.is_valid = True
                    has_outgoing.add(doc.path)
                    has_incoming.add(link.resolved_path)
                else:
                    rel.is_valid = False
                    rel.error = link.error_message or "arquivo não existe"
                    self._broken_links.append(rel)

                self._outgoing[doc.path].append(rel)
                if link.resolved_path:
                    self._incoming[link.resolved_path].append(rel)

        # Calcula órfãos e isolados
        self._orphans = all_paths - has_incoming
        self._isolated = all_paths - has_outgoing

    def get_outgoing(self, path: Path) -> List[Relationship]:
        """
        Retorna relacionamentos saindo de um documento.

        Args:
            path: Path do documento

        Returns:
            Lista de relacionamentos
        """
        return self._outgoing.get(path, [])

    def get_incoming(self, path: Path) -> List[Relationship]:
        """
        Retorna relacionamentos entrando em um documento.

        Args:
            path: Path do documento

        Returns:
            Lista de relacionamentos
        """
        return self._incoming.get(path, [])

    def get_orphans(self) -> Set[Path]:
        """
        Retorna documentos sem links entrando.

        Returns:
            Set de paths
        """
        return self._orphans.copy()

    def get_isolated(self) -> Set[Path]:
        """
        Retorna documentos sem links saindo.

        Returns:
            Set de paths
        """
        return self._isolated.copy()

    def get_completely_isolated(self) -> Set[Path]:
        """
        Retorna documentos sem links entrando nem saindo.

        Returns:
            Set de paths
        """
        return self._orphans & self._isolated

    def get_broken_links(self) -> List[Relationship]:
        """
        Retorna todos os links quebrados.

        Returns:
            Lista de relacionamentos inválidos
        """
        return self._broken_links.copy()

    def has_link_from_to(self, source: Path, target: Path) -> bool:
        """
        Verifica se existe link de source para target.

        Args:
            source: Documento fonte
            target: Documento destino

        Returns:
            True se existe link
        """
        for rel in self.get_outgoing(source):
            if rel.target == target and rel.is_valid:
                return True
        return False
