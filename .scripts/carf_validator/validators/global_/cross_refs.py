"""Validador de referências cruzadas entre PROJECTS e CENTRAL."""

from typing import List

from ..base import GlobalValidator
from ..registry import validator
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class CrossRefsValidator(GlobalValidator):
    """Valida direção correta de referências cruzadas entre PROJECTS e CENTRAL."""

    name = "cross_refs"
    description = "Valida que PROJECTS referencia CENTRAL (não o inverso)"

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        projects_docs_with_central_refs = 0
        projects_docs_without_refs = 0

        # Verifica que documentos em PROJECTS referenciam CENTRAL
        for doc in context.get_all_documents():
            if not context.is_in_projects(doc):
                continue

            # Verifica se este documento tem links para CENTRAL
            has_central_ref = False
            outgoing = context.get_links_from(doc.path)

            for rel in outgoing:
                target_doc = context.get_document(rel.target)

                if target_doc and context.is_in_central(target_doc):
                    has_central_ref = True
                    break

                # Verifica por path string
                if rel.target_raw and 'CENTRAL/' in rel.target_raw:
                    has_central_ref = True
                    break

            if has_central_ref:
                projects_docs_with_central_refs += 1
            else:
                # Nem todo arquivo precisa referenciar CENTRAL,
                # mas documentos de especificação deveriam
                if self._should_reference_central(doc):
                    projects_docs_without_refs += 1
                    issues.append(ValidationIssue(
                        severity=Severity.INFO,
                        code="XREF001",
                        message="Documento PROJECTS sem referência a CENTRAL",
                        file_path=doc.path,
                        suggestion="Considere adicionar link para requisito/UC correspondente em CENTRAL",
                    ))

        # Resumo de cobertura de referências
        total_projects = projects_docs_with_central_refs + projects_docs_without_refs

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "projects_with_central_refs": projects_docs_with_central_refs,
                "projects_without_refs": projects_docs_without_refs,
                "ref_coverage_percent": (
                    round(projects_docs_with_central_refs / total_projects * 100, 1)
                    if total_projects > 0 else 100
                ),
            }
        )

    def _should_reference_central(self, doc) -> bool:
        """Determina se o documento deveria referenciar CENTRAL."""
        from ...models.base import DocumentType

        # Documentos que deveriam ter rastreabilidade para CENTRAL
        traceable_types = {
            DocumentType.FEATURE,
            DocumentType.ENTITY,
            DocumentType.WORKFLOW,
        }

        return doc.doc_type in traceable_types
