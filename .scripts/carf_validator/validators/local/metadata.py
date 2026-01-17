"""Validador de metadata footer."""

import re
from datetime import datetime, timedelta
from typing import List

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class MetadataValidator(LocalValidator):
    """Valida metadata footer (Última atualização, Status, etc.)."""

    name = "metadata"
    description = "Valida presença e atualidade do footer de metadata"

    # Tipos que requerem última atualização
    REQUIRES_LAST_UPDATE = {
        DocumentType.README,
        DocumentType.RF,
        DocumentType.RNF,
        DocumentType.US,
        DocumentType.UC,
        DocumentType.ENTITY,
        DocumentType.FEATURE,
        DocumentType.BUSINESS_RULE,
        DocumentType.WORKFLOW,
        DocumentType.PATTERN,
    }

    # Tipos que requerem status do arquivo
    REQUIRES_FILE_STATUS = {
        DocumentType.README,
    }

    # Campos obrigatórios para ADR
    ADR_REQUIRED_FIELDS = ["decision_date", "status", "decider"]

    # Meses para considerar desatualizado
    STALE_MONTHS = 12

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        # Detectar múltiplas datas de atualização (aplica a todos os tipos)
        date_matches = re.findall(r'\*\*Última atualização:\*\*', doc.content)
        if len(date_matches) > 1:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="META009",
                message=f"Documento tem {len(date_matches)} campos 'Última atualização'",
                file_path=doc.path,
                suggestion="Remova as datas duplicadas, mantenha apenas uma no footer",
            ))

        # Validação específica para ADR
        if doc.doc_type == DocumentType.ADR:
            issues.extend(self._validate_adr_metadata(doc))
            return issues

        # Skip tipos que não requerem metadata
        if doc.doc_type not in self.REQUIRES_LAST_UPDATE:
            return issues

        # Verifica última atualização
        if not doc.metadata.last_update:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="META001",
                message="Campo 'Última atualização' ausente",
                file_path=doc.path,
                suggestion="Adicione **Última atualização:** YYYY-MM-DD ao final do arquivo",
            ))
        else:
            # Verifica se está desatualizado
            cutoff = datetime.now().date() - timedelta(days=self.STALE_MONTHS * 30)
            if doc.metadata.last_update < cutoff:
                issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    code="META002",
                    message=f"Documento desatualizado (última atualização: {doc.metadata.last_update})",
                    file_path=doc.path,
                    suggestion="Revise e atualize o documento, depois atualize a data",
                ))

        # Verifica status do arquivo para README
        if doc.doc_type in self.REQUIRES_FILE_STATUS:
            if not doc.metadata.file_status:
                issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    code="META003",
                    message="Campo 'Status do arquivo' ausente",
                    file_path=doc.path,
                    suggestion="Adicione **Status do arquivo**: Pronto",
                ))
            else:
                # Detectar status problemáticos
                status_lower = doc.metadata.file_status.lower()
                if status_lower == 'review':
                    issues.append(ValidationIssue(
                        severity=Severity.INFO,
                        code="META010",
                        message="README aguardando revisão humana",
                        file_path=doc.path,
                        suggestion="Revise o conteúdo e mude status para 'Pronto' quando aprovado",
                    ))
                elif status_lower in ('incompleto', 'incomplete'):
                    issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        code="META007",
                        message="README marcado como 'Incompleto'",
                        file_path=doc.path,
                        suggestion="Complete o documento ou regenere o índice com carf_tree_sync",
                    ))
                elif status_lower in ('errado', 'error'):
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        code="META008",
                        message="README marcado como 'Errado'",
                        file_path=doc.path,
                        suggestion="Corrija os problemas indicados na descrição",
                    ))

        return issues

    def _validate_adr_metadata(self, doc: DocumentNode) -> List[ValidationIssue]:
        """Valida metadata específica de ADR."""
        issues = []

        if not doc.metadata.decision_date:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="META004",
                message="ADR sem campo 'Data'",
                file_path=doc.path,
                suggestion="Adicione **Data:** YYYY-MM-DD",
            ))

        if not doc.metadata.status:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="META005",
                message="ADR sem campo 'Status'",
                file_path=doc.path,
                suggestion="Adicione **Status:** Aprovado e Implementado",
            ))

        if not doc.metadata.decider:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="META006",
                message="ADR sem campo 'Decisor'",
                file_path=doc.path,
                suggestion="Adicione **Decisor:** Nome/Equipe responsável",
            ))

        return issues
