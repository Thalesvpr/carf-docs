"""Validador de frontmatter YAML."""

from typing import List

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class FrontmatterValidator(LocalValidator):
    """Valida campos obrigatórios de frontmatter baseado no tipo de documento."""

    name = "frontmatter"
    description = "Valida presença e campos obrigatórios do frontmatter YAML"

    # Tipos que requerem campo modules
    REQUIRES_MODULES = {
        DocumentType.UC, DocumentType.RF, DocumentType.US, DocumentType.RNF
    }

    # Tipos que requerem campo epic
    REQUIRES_EPIC = {
        DocumentType.UC, DocumentType.RF, DocumentType.US
    }

    # Módulos válidos
    VALID_MODULES = {
        "GEOAPI", "GEOWEB", "REURBCAD", "GEOGIS",
        "ADMIN", "KEYCLOAK", "WEBDOCS"
    }

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        # Skip tipos que não precisam de frontmatter
        if doc.doc_type in {DocumentType.README, DocumentType.UNKNOWN, DocumentType.ADR}:
            return issues

        # Verifica se frontmatter existe
        has_frontmatter = (
            doc.frontmatter.has_modules() or
            doc.frontmatter.has_epic() or
            bool(doc.frontmatter.raw)
        )

        if doc.doc_type in self.REQUIRES_MODULES and not has_frontmatter:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="FRONT001",
                message="Frontmatter ausente",
                file_path=doc.path,
                suggestion="Adicione frontmatter com modules: [PROJETO] e epic: categoria",
            ))
            return issues

        # Verifica campo modules
        if doc.doc_type in self.REQUIRES_MODULES:
            if not doc.frontmatter.has_modules():
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    code="FRONT002",
                    message="Campo 'modules' ausente no frontmatter",
                    file_path=doc.path,
                    suggestion="Adicione modules: [GEOWEB] ou projeto apropriado",
                ))
            else:
                # Valida módulos
                for module in doc.frontmatter.modules:
                    if module not in self.VALID_MODULES:
                        issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            code="FRONT004",
                            message=f"Módulo desconhecido: {module}",
                            file_path=doc.path,
                            suggestion=f"Use um dos módulos válidos: {', '.join(sorted(self.VALID_MODULES))}",
                        ))

        # Verifica campo epic
        if doc.doc_type in self.REQUIRES_EPIC and not doc.frontmatter.has_epic():
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="FRONT003",
                message="Campo 'epic' ausente no frontmatter",
                file_path=doc.path,
                suggestion="Adicione epic: categoria (ex: security, units, etc.)",
            ))

        return issues
