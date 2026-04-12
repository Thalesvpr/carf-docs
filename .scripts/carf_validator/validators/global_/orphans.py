"""Validador de arquivos órfãos."""

from typing import List

from ..base import GlobalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class OrphansValidator(GlobalValidator):
    """Detecta arquivos que não recebem links de nenhum outro documento."""

    name = "orphans"
    description = "Detecta arquivos sem referências (órfãos)"

    # Tipos que devem estar linkados
    MUST_BE_LINKED = {
        DocumentType.RF,
        DocumentType.RNF,
        DocumentType.US,
        DocumentType.UC,
        DocumentType.ENTITY,
        DocumentType.FEATURE,
        DocumentType.BUSINESS_RULE,
    }

    # Arquivos permitidos serem órfãos (entry points)
    ALLOWED_ORPHANS = {
        "README.md",
        "CHANGELOG.md",
        "LICENSE.md",
        "CONTRIBUTING.md",
    }

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        orphans = context.get_orphans()

        for path in orphans:
            doc = context.get_document(path)
            if not doc:
                continue

            # Ignora arquivos permitidos serem órfãos
            if doc.path.name in self.ALLOWED_ORPHANS:
                continue

            # Ignora READMEs (são entry points)
            if doc.doc_type == DocumentType.README:
                continue

            # Determina severidade baseado no tipo
            if doc.doc_type in self.MUST_BE_LINKED:
                severity = Severity.WARNING
                message = f"Documento órfão ({doc.doc_type.name}): nenhum link aponta para este arquivo"
            else:
                severity = Severity.INFO
                message = "Arquivo sem referências de outros documentos"

            issues.append(ValidationIssue(
                severity=severity,
                code="ORPHAN001",
                message=message,
                file_path=path,
                suggestion="Adicione referência a este arquivo em documentos relacionados",
            ))

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "total_orphans": len(orphans),
                "critical_orphans": sum(
                    1 for p in orphans
                    if (doc := context.get_document(p)) and doc.doc_type in self.MUST_BE_LINKED
                ),
            }
        )
