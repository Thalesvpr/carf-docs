"""Classes base para validadores."""

from abc import ABC, abstractmethod
import time
from typing import List

from ..models.results import ValidatorResult, ValidationIssue
from ..context.queries import ValidationContext
from ..scanner.tree import DocumentNode


class BaseValidator(ABC):
    """Interface base para todos os validadores."""

    name: str = "base"
    description: str = ""

    @abstractmethod
    def validate(self, context: ValidationContext) -> ValidatorResult:
        """
        Executa validação e retorna resultados.

        Args:
            context: Contexto de validação

        Returns:
            Resultado da validação
        """
        pass


class LocalValidator(BaseValidator):
    """Validador que opera em documentos individuais."""

    @abstractmethod
    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        """
        Valida um único documento.

        Args:
            doc: Documento a validar
            context: Contexto de validação

        Returns:
            Lista de issues encontrados
        """
        pass

    def validate(self, context: ValidationContext) -> ValidatorResult:
        """
        Executa validação em todos os documentos.

        Args:
            context: Contexto de validação

        Returns:
            Resultado da validação
        """
        start = time.time()

        issues = []
        docs_checked = 0

        for doc in context.get_all_documents():
            doc_issues = self.validate_document(doc, context)
            issues.extend(doc_issues)
            docs_checked += 1

        duration = (time.time() - start) * 1000

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={"documents_checked": docs_checked},
            duration_ms=duration,
        )


class GlobalValidator(BaseValidator):
    """Validador que opera no grafo completo de documentos."""

    @abstractmethod
    def validate(self, context: ValidationContext) -> ValidatorResult:
        """
        Executa validação global.

        Args:
            context: Contexto de validação

        Returns:
            Resultado da validação
        """
        pass
