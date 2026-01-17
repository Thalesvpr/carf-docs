"""Validador de isolamento CENTRAL/PROJECTS."""

from typing import List

from ..base import GlobalValidator
from ..registry import validator
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class IsolationValidator(GlobalValidator):
    """Valida isolamento: CENTRAL não pode linkar para PROJECTS."""

    name = "isolation"
    description = "Valida que CENTRAL (fonte de verdade) não depende de PROJECTS"

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        # Itera todos os documentos em CENTRAL
        for doc in context.get_all_documents():
            if not context.is_in_central(doc):
                continue

            # Verifica links de saída deste documento
            outgoing = context.get_links_from(doc.path)

            for rel in outgoing:
                # Verifica se o alvo está em PROJECTS
                target_doc = context.get_document(rel.target)

                if target_doc and context.is_in_projects(target_doc):
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        code="ISOL001",
                        message=f"CENTRAL linka para PROJECTS: {rel.target_raw}",
                        file_path=doc.path,
                        line_number=rel.line_number,
                        context=f"Link: [{rel.link_text}]({rel.target_raw})",
                        suggestion="CENTRAL é fonte única de verdade e não deve depender de PROJECTS",
                    ))

                # Verifica link por path string mesmo se arquivo não existe
                elif rel.target_raw and 'PROJECTS/' in rel.target_raw:
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        code="ISOL002",
                        message=f"CENTRAL referencia PROJECTS: {rel.target_raw}",
                        file_path=doc.path,
                        line_number=rel.line_number,
                        context=f"Link: [{rel.link_text}]",
                        suggestion="Remova a referência a PROJECTS de documentos em CENTRAL",
                    ))

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "isolation_violations": len(issues),
            }
        )
