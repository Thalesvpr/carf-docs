"""Validador de links quebrados."""

from typing import List

from ..base import GlobalValidator
from ..registry import validator
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class BrokenLinksValidator(GlobalValidator):
    """Valida que todos os links internos apontam para arquivos existentes."""

    name = "broken_links"
    description = "Detecta links para arquivos inexistentes"

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        broken = context.get_broken_links()

        for relationship in broken:
            source_doc = context.get_document(relationship.source)
            source_name = source_doc.relative_path if source_doc else str(relationship.source)

            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="BLINK001",
                message=f"Link quebrado: {relationship.target_raw}",
                file_path=relationship.source,
                line_number=relationship.line_number,
                context=f"Link text: '{relationship.link_text}'",
                suggestion=f"Verifique se o arquivo existe ou corrija o caminho",
            ))

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "total_broken": len(broken),
            }
        )
