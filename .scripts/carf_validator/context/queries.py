"""Interface de queries para validadores."""

import re
from pathlib import Path
from typing import List, Optional, Set

from ..models.base import DocumentType
from ..scanner.tree import DocumentNode
from .registry import DocumentRegistry
from .graph import RelationshipGraph


class ValidationContext:
    """Interface de queries para validadores acessarem documentos e relacionamentos."""

    def __init__(self, registry: DocumentRegistry, graph: RelationshipGraph, root_dir: Path):
        """
        Inicializa contexto.

        Args:
            registry: Registry de documentos
            graph: Grafo de relacionamentos
            root_dir: Diretório raiz
        """
        self.registry = registry
        self.graph = graph
        self.root_dir = root_dir

    # === Queries de Documentos ===

    def get_document(self, path: Path) -> Optional[DocumentNode]:
        """Busca documento por path."""
        return self.registry.get_by_path(path)

    def get_by_identifier(self, identifier: str) -> Optional[DocumentNode]:
        """Busca documento por identificador."""
        return self.registry.get_by_identifier(identifier)

    def get_all_of_type(self, doc_type: DocumentType) -> List[DocumentNode]:
        """Busca todos os documentos de um tipo."""
        return self.registry.get_by_type(doc_type)

    def get_by_type(self, doc_type: DocumentType) -> List[DocumentNode]:
        """Alias para get_all_of_type."""
        return self.registry.get_by_type(doc_type)

    def get_all_documents(self) -> List[DocumentNode]:
        """Retorna todos os documentos."""
        return list(self.registry.all_documents())

    def count_documents(self) -> int:
        """Conta total de documentos."""
        return self.registry.count()

    # === Queries de Relacionamentos ===

    def get_links_from(self, path: Path):
        """Retorna relacionamentos saindo de um documento."""
        return self.graph.get_outgoing(path)

    def get_links_to(self, path: Path):
        """Retorna relacionamentos entrando em um documento."""
        return self.graph.get_incoming(path)

    def get_broken_links(self):
        """Retorna links quebrados como objetos Relationship."""
        return self.graph.get_broken_links()

    def get_orphans(self) -> Set[Path]:
        """Retorna documentos sem links entrando."""
        return self.graph.get_orphans()

    def get_isolated(self) -> Set[Path]:
        """Retorna documentos sem links saindo."""
        return self.graph.get_isolated()

    def get_completely_isolated(self) -> Set[Path]:
        """Retorna documentos completamente isolados."""
        return self.graph.get_completely_isolated()

    # === Queries de Path ===

    def is_in_central(self, doc: DocumentNode) -> bool:
        """Verifica se documento está em CENTRAL."""
        return doc.relative_path.startswith("CENTRAL/")

    def is_in_projects(self, doc: DocumentNode) -> bool:
        """Verifica se documento está em PROJECTS."""
        return doc.relative_path.startswith("PROJECTS/")

    def get_project_name(self, doc: DocumentNode) -> Optional[str]:
        """Extrai nome do projeto de path PROJECTS/NOME/..."""
        parts = doc.relative_path.split("/")
        if len(parts) >= 2 and parts[0] == "PROJECTS":
            return parts[1]
        return None

    def get_domain_folder(self, doc: DocumentNode) -> Optional[str]:
        """Extrai pasta de domínio (01-auth-security, etc.)."""
        parts = doc.relative_path.split("/")
        for part in parts:
            if re.match(r'\d{2}-', part):
                return part
        return None

    # === Queries de Conteúdo ===

    def find_references_to(self, identifier: str) -> List[DocumentNode]:
        """Encontra documentos que referenciam um identificador."""
        pattern = re.compile(rf'\b{re.escape(identifier)}\b')
        results = []
        for doc in self.registry.all_documents():
            if pattern.search(doc.content):
                results.append(doc)
        return results

    def find_documents_linking_to_central(self) -> List[DocumentNode]:
        """Encontra documentos em PROJECTS que linkam para CENTRAL."""
        results = []
        for doc in self.registry.all_documents():
            if not self.is_in_projects(doc):
                continue
            for link in doc.links:
                if link.is_external:
                    continue
                if "CENTRAL/" in link.target or "../CENTRAL/" in link.target:
                    results.append(doc)
                    break
        return results

    def find_documents_in_central_linking_to_projects(self) -> List[DocumentNode]:
        """Encontra documentos em CENTRAL que linkam para PROJECTS."""
        results = []
        for doc in self.registry.all_documents():
            if not self.is_in_central(doc):
                continue
            for link in doc.links:
                if link.is_external:
                    continue
                if "PROJECTS/" in link.target or "../PROJECTS/" in link.target:
                    results.append(doc)
                    break
        return results

    # === Queries de Cobertura ===

    def get_rfs_not_in_features(self) -> List[DocumentNode]:
        """Encontra RFs não mencionados em nenhuma FEATURE."""
        all_rfs = self.get_all_of_type(DocumentType.RF)
        all_features = self.get_all_of_type(DocumentType.FEATURE)

        # Coleta todas as menções de RF nas features
        covered_rfs = set()
        for feature in all_features:
            rf_refs = re.findall(r'RF-\d{3}', feature.content)
            covered_rfs.update(rf_refs)

        # Encontra RFs não cobertos
        uncovered = []
        for rf in all_rfs:
            if rf.identifier and rf.identifier not in covered_rfs:
                uncovered.append(rf)

        return uncovered

    def get_ucs_not_in_features(self) -> List[DocumentNode]:
        """Encontra UCs não mencionados em nenhuma FEATURE."""
        all_ucs = self.get_all_of_type(DocumentType.UC)
        all_features = self.get_all_of_type(DocumentType.FEATURE)

        # Coleta todas as menções de UC/nomes de arquivo nas features
        covered_ucs = set()
        for feature in all_features:
            # Busca por identificador e nome do arquivo
            uc_refs = re.findall(r'UC-\d{3}', feature.content)
            covered_ucs.update(uc_refs)

            # Também busca por nome do arquivo
            for uc in all_ucs:
                if uc.path.name in feature.content:
                    covered_ucs.add(uc.identifier)

        # Encontra UCs não cobertos
        uncovered = []
        for uc in all_ucs:
            if uc.identifier and uc.identifier not in covered_ucs:
                uncovered.append(uc)

        return uncovered
