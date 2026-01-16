"""Builder de árvore de documentos."""

import re
from pathlib import Path
from typing import Dict, Optional

from ..models.base import DocumentType, Frontmatter, Metadata, Link, ContentMetrics
from .traversal import FileScanner, ScanConfig
from .parsers.frontmatter import parse_frontmatter
from .parsers.links import extract_links
from .parsers.metadata import parse_metadata
from .parsers.sections import analyze_content


class DocumentNode:
    """Nó de documento na árvore."""

    def __init__(
        self,
        path: Path,
        relative_path: str,
        doc_type: DocumentType,
        content: str = "",
    ):
        self.path = path
        self.relative_path = relative_path
        self.doc_type = doc_type
        self.content = content
        self.title: Optional[str] = None
        self.frontmatter: Frontmatter = Frontmatter.empty()
        self.metadata: Metadata = Metadata()
        self.links: list[Link] = []
        self.metrics: ContentMetrics = ContentMetrics()

    @property
    def identifier(self) -> Optional[str]:
        """Extrai identificador do documento (RF-001, UC-002, etc.)."""
        patterns = {
            DocumentType.RF: r'RF-(\d{3})',
            DocumentType.RNF: r'RNF-(\d{3})',
            DocumentType.US: r'US-(\d{3})',
            DocumentType.UC: r'UC-(\d{3})',
            DocumentType.ADR: r'ADR-(\d{3})',
        }

        pattern = patterns.get(self.doc_type)
        if pattern:
            match = re.match(pattern, self.path.stem)
            if match:
                return f"{self.doc_type.name}-{match.group(1)}"

        return None

    @property
    def is_readme(self) -> bool:
        """Verifica se é README."""
        return self.doc_type == DocumentType.README

    def __repr__(self) -> str:
        return f"DocumentNode({self.relative_path}, {self.doc_type.name})"


class DocumentTreeBuilder:
    """Constrói árvore de documentos a partir do filesystem."""

    def __init__(self, root_dir: Path):
        """
        Inicializa builder.

        Args:
            root_dir: Diretório raiz do repositório
        """
        self.root_dir = root_dir
        self.documents: Dict[Path, DocumentNode] = {}

    def build(self) -> Dict[Path, DocumentNode]:
        """
        Varre filesystem e constrói árvore de documentos.

        Returns:
            Dicionário de path -> DocumentNode
        """
        config = ScanConfig.default(self.root_dir)
        scanner = FileScanner(config)

        for file_path in scanner.scan():
            doc = self._parse_document(file_path)
            if doc:
                self.documents[file_path] = doc

        return self.documents

    def _parse_document(self, path: Path) -> Optional[DocumentNode]:
        """
        Parseia um documento markdown.

        Args:
            path: Path do arquivo

        Returns:
            DocumentNode ou None se erro
        """
        try:
            content = path.read_text(encoding='utf-8')
        except Exception:
            return None

        # Detecta tipo
        doc_type = self._detect_type(path)

        # Cria nó
        relative_path = str(path.relative_to(self.root_dir)).replace('\\', '/')
        doc = DocumentNode(
            path=path,
            relative_path=relative_path,
            doc_type=doc_type,
            content=content,
        )

        # Parse frontmatter
        frontmatter, _ = parse_frontmatter(content)
        if frontmatter:
            doc.frontmatter = frontmatter

        # Parse metadata
        doc.metadata = parse_metadata(content)

        # Extrai links
        doc.links = extract_links(content, path)

        # Extrai título
        doc.title = self._extract_title(content)

        # Analisa conteúdo
        analysis = analyze_content(content)
        doc.metrics = ContentMetrics(
            char_count=analysis.char_count,
            word_count=analysis.word_count,
            paragraph_count=analysis.paragraph_count,
            sentence_count=analysis.sentence_count,
            avg_words_per_sentence=analysis.avg_words_per_sentence,
            bullet_count=analysis.bullet_count,
        )

        return doc

    def _detect_type(self, path: Path) -> DocumentType:
        """
        Detecta tipo de documento baseado em path e nome.

        Args:
            path: Path do arquivo

        Returns:
            DocumentType detectado
        """
        path_str = str(path).replace('\\', '/')
        name = path.name
        stem = path.stem

        # README
        if name == "README.md":
            return DocumentType.README

        # ADR
        if "/ADRs/" in path_str and stem.startswith("ADR-"):
            return DocumentType.ADR

        # Use Cases
        if "/USE-CASES/" in path_str:
            if "-FA-" in stem:
                return DocumentType.UC_FA
            elif "-FE-" in stem:
                return DocumentType.UC_FE
            elif stem.startswith("UC-"):
                return DocumentType.UC

        # Functional Requirements
        if "/FUNCTIONAL-REQUIREMENTS/" in path_str and stem.startswith("RF-"):
            return DocumentType.RF

        # Non-Functional Requirements
        if "/NON-FUNCTIONAL-REQUIREMENTS/" in path_str and stem.startswith("RNF-"):
            return DocumentType.RNF

        # User Stories
        if "/USER-STORIES/" in path_str and stem.startswith("US-"):
            return DocumentType.US

        # Domain Model
        if "/ENTITIES/" in path_str:
            return DocumentType.ENTITY
        if "/VALUE-OBJECTS/" in path_str:
            return DocumentType.VALUE_OBJECT
        if "/AGGREGATES/" in path_str:
            return DocumentType.AGGREGATE

        # Features
        if "/FEATURES/" in path_str and name != "README.md":
            return DocumentType.FEATURE

        # How-To
        if "/HOW-TO/" in path_str:
            return DocumentType.HOW_TO

        # Concepts
        if "/CONCEPTS/" in path_str:
            return DocumentType.CONCEPT

        # Business Rules
        if "/BUSINESS-RULES/" in path_str:
            return DocumentType.BUSINESS_RULE

        # Workflows
        if "/WORKFLOWS/" in path_str and name != "README.md":
            return DocumentType.WORKFLOW

        # Patterns
        if "/PATTERNS/" in path_str:
            return DocumentType.PATTERN

        # API
        if "/API/" in path_str and name != "README.md":
            return DocumentType.API

        # Architecture
        if "/ARCHITECTURE/" in path_str and name != "README.md":
            return DocumentType.ARCHITECTURE

        return DocumentType.UNKNOWN

    def _extract_title(self, content: str) -> Optional[str]:
        """
        Extrai título H1 do conteúdo.

        Args:
            content: Conteúdo markdown

        Returns:
            Título ou None
        """
        # Tenta padrão com ID: # RF-001: Título
        match = re.search(r'^# (?:\w+-\d+[:\s]+)?(.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Tenta H1 genérico
        match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        return None
