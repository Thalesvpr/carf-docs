"""Modelos base para representação de documentos."""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from enum import Enum, auto
from pathlib import Path
from typing import Optional, List, Dict, Any


class DocumentType(Enum):
    """Tipos de documentos reconhecidos no repositório."""
    RF = auto()           # Requisito Funcional
    RNF = auto()          # Requisito Não-Funcional
    US = auto()           # User Story
    UC = auto()           # Use Case
    UC_FA = auto()        # Use Case - Fluxo Alternativo
    UC_FE = auto()        # Use Case - Fluxo de Exceção
    ADR = auto()          # Architecture Decision Record
    README = auto()       # README files
    ENTITY = auto()       # Domain entity
    VALUE_OBJECT = auto() # Value object
    AGGREGATE = auto()    # Aggregate root
    FEATURE = auto()      # Feature documentation
    HOW_TO = auto()       # How-to guides
    CONCEPT = auto()      # Conceptual documentation
    BUSINESS_RULE = auto()    # Business rules
    WORKFLOW = auto()     # Workflow documentation
    ARCHITECTURE = auto() # Architecture documentation
    PATTERN = auto()      # Architecture pattern
    API = auto()          # API documentation
    UNKNOWN = auto()      # Unrecognized type


@dataclass
class Frontmatter:
    """Frontmatter YAML parseado do cabeçalho do documento."""
    modules: List[str] = field(default_factory=list)
    epic: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def empty(cls) -> Frontmatter:
        """Cria frontmatter vazio."""
        return cls()

    def has_modules(self) -> bool:
        """Verifica se tem módulos definidos."""
        return len(self.modules) > 0

    def has_epic(self) -> bool:
        """Verifica se tem epic definido."""
        return self.epic is not None and self.epic.strip() != ""


@dataclass
class Metadata:
    """Metadata do footer do documento."""
    last_update: Optional[date] = None
    status: Optional[str] = None
    file_status: Optional[str] = None
    decision_date: Optional[date] = None
    decider: Optional[str] = None
    last_revision: Optional[date] = None
    version: Optional[str] = None
    license: Optional[str] = None


@dataclass
class Link:
    """Representa um link markdown encontrado no conteúdo."""
    text: str
    target: str
    line_number: int
    source_file: Path
    is_external: bool = False
    resolved_path: Optional[Path] = None
    is_valid: bool = False
    error_message: Optional[str] = None

    def is_internal(self) -> bool:
        """Verifica se é link interno."""
        return not self.is_external

    def is_broken(self) -> bool:
        """Verifica se é link quebrado."""
        return self.is_internal() and not self.is_valid


@dataclass
class ContentMetrics:
    """Métricas de conteúdo do documento."""
    char_count: int = 0
    word_count: int = 0
    line_count: int = 0
    paragraph_count: int = 0
    sentence_count: int = 0
    avg_words_per_sentence: float = 0.0
    bullet_count: int = 0
    code_block_count: int = 0
