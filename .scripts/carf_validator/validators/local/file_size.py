"""Validador de tamanho de arquivo (contagem de palavras)."""

from typing import List, Dict

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class FileSizeValidator(LocalValidator):
    """Valida contagem de palavras contra limites por tipo."""

    name = "file_size"
    description = "Valida contagem mínima e máxima de palavras por tipo de documento"

    # Regras de tamanho por tipo (palavras)
    SIZE_RULES: Dict[DocumentType, Dict[str, int]] = {
        DocumentType.README: {"min": 50, "max": 500},
        DocumentType.ADR: {"min": 200, "max": 800},
        DocumentType.UC: {"min": 150, "max": 800},
        DocumentType.RF: {"min": 80, "max": 400},
        DocumentType.RNF: {"min": 60, "max": 350},
        DocumentType.US: {"min": 60, "max": 300},
        DocumentType.ENTITY: {"min": 150, "max": 600},
        DocumentType.FEATURE: {"min": 200, "max": 1000},
        DocumentType.HOW_TO: {"min": 150, "max": 900},
        DocumentType.CONCEPT: {"min": 100, "max": 600},
        DocumentType.BUSINESS_RULE: {"min": 100, "max": 800},
        DocumentType.WORKFLOW: {"min": 150, "max": 1000},
        DocumentType.PATTERN: {"min": 200, "max": 900},
    }

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        rules = self.SIZE_RULES.get(doc.doc_type)
        if not rules:
            return issues

        word_count = doc.metrics.word_count
        min_words = rules["min"]
        max_words = rules["max"]

        if word_count < min_words:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="SIZE001",
                message=f"Documento muito curto: {word_count} palavras (mínimo: {min_words})",
                file_path=doc.path,
                suggestion=f"Adicione mais {min_words - word_count} palavras de conteúdo",
            ))
        elif word_count > max_words:
            issues.append(ValidationIssue(
                severity=Severity.INFO,
                code="SIZE002",
                message=f"Documento muito longo: {word_count} palavras (máximo: {max_words})",
                file_path=doc.path,
                suggestion=f"Considere dividir em documentos menores (excede em {word_count - max_words} palavras)",
            ))

        return issues
