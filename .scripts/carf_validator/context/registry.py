"""Registry central de documentos."""

from pathlib import Path
from typing import Dict, List, Optional, Iterator

from ..models.base import DocumentType
from ..scanner.tree import DocumentNode


class DocumentRegistry:
    """Registry central para todos os documentos parseados."""

    def __init__(self):
        """Inicializa registry."""
        self._by_path: Dict[Path, DocumentNode] = {}
        self._by_type: Dict[DocumentType, List[DocumentNode]] = {}
        self._by_identifier: Dict[str, DocumentNode] = {}
        self._by_relative_path: Dict[str, DocumentNode] = {}

    def register(self, doc: DocumentNode) -> None:
        """
        Registra um documento em todos os índices.

        Args:
            doc: Documento a registrar
        """
        # Por path absoluto
        self._by_path[doc.path] = doc

        # Por path relativo
        self._by_relative_path[doc.relative_path] = doc

        # Por tipo
        if doc.doc_type not in self._by_type:
            self._by_type[doc.doc_type] = []
        self._by_type[doc.doc_type].append(doc)

        # Por identificador
        if doc.identifier:
            self._by_identifier[doc.identifier] = doc

    def register_all(self, documents: Dict[Path, DocumentNode]) -> None:
        """
        Registra múltiplos documentos.

        Args:
            documents: Dicionário de path -> documento
        """
        for doc in documents.values():
            self.register(doc)

    def get_by_path(self, path: Path) -> Optional[DocumentNode]:
        """
        Busca documento por path absoluto.

        Args:
            path: Path absoluto

        Returns:
            Documento ou None
        """
        return self._by_path.get(path)

    def get_by_relative_path(self, relative_path: str) -> Optional[DocumentNode]:
        """
        Busca documento por path relativo.

        Args:
            relative_path: Path relativo

        Returns:
            Documento ou None
        """
        return self._by_relative_path.get(relative_path)

    def get_by_type(self, doc_type: DocumentType) -> List[DocumentNode]:
        """
        Busca todos os documentos de um tipo.

        Args:
            doc_type: Tipo de documento

        Returns:
            Lista de documentos
        """
        return self._by_type.get(doc_type, [])

    def get_by_identifier(self, identifier: str) -> Optional[DocumentNode]:
        """
        Busca documento por identificador (RF-001, UC-002, etc.).

        Args:
            identifier: Identificador do documento

        Returns:
            Documento ou None
        """
        return self._by_identifier.get(identifier)

    def all_documents(self) -> Iterator[DocumentNode]:
        """
        Itera sobre todos os documentos registrados.

        Yields:
            Documentos registrados
        """
        yield from self._by_path.values()

    def count(self) -> int:
        """
        Conta total de documentos.

        Returns:
            Número de documentos
        """
        return len(self._by_path)

    def count_by_type(self, doc_type: DocumentType) -> int:
        """
        Conta documentos de um tipo.

        Args:
            doc_type: Tipo de documento

        Returns:
            Número de documentos do tipo
        """
        return len(self.get_by_type(doc_type))

    def get_all_types(self) -> List[DocumentType]:
        """
        Retorna todos os tipos de documentos presentes.

        Returns:
            Lista de tipos
        """
        return list(self._by_type.keys())

    def get_all_identifiers(self) -> List[str]:
        """
        Retorna todos os identificadores.

        Returns:
            Lista de identificadores
        """
        return list(self._by_identifier.keys())
