"""Validador de padrão de título."""

import re
from typing import List, Dict, Optional

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class TitleValidator(LocalValidator):
    """Valida padrão de título H1 por tipo de documento."""

    name = "title"
    description = "Valida formato do título H1 por tipo de documento"

    # Padrões de título por tipo
    TITLE_PATTERNS: Dict[DocumentType, str] = {
        DocumentType.ADR: r"^# ADR-\d{3}:",
        DocumentType.UC: r"^# UC-\d{3}:",
        DocumentType.RF: r"^# RF-\d{3}:",
        DocumentType.RNF: r"^# RNF-\d{3}:",
        DocumentType.US: r"^# US-\d{3}:",
        DocumentType.README: r"^# [A-Z]",  # README começa com letra maiúscula
    }

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        pattern = self.TITLE_PATTERNS.get(doc.doc_type)
        if not pattern:
            return issues

        lines = doc.content.split('\n')

        # Pula frontmatter se existir
        start_line = 0
        if lines and lines[0] == '---':
            for i, line in enumerate(lines[1:], 1):
                if line == '---':
                    start_line = i + 1
                    break

        # Encontra primeira linha não vazia após frontmatter
        first_content_line = None
        first_line_num = 0
        for i, line in enumerate(lines[start_line:], start_line + 1):
            if line.strip():
                first_content_line = line
                first_line_num = i
                break

        if not first_content_line:
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="TITLE001",
                message="Documento sem título H1",
                file_path=doc.path,
                suggestion="Adicione um título H1 no início do documento",
            ))
            return issues

        # Verifica se começa com H1
        if not first_content_line.startswith('# '):
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="TITLE002",
                message="Primeira linha de conteúdo não é título H1",
                file_path=doc.path,
                line_number=first_line_num,
                context=first_content_line[:50],
                suggestion="Documento deve começar com # Título",
            ))
            return issues

        # Verifica padrão específico do tipo
        if not re.match(pattern, first_content_line):
            expected = self._get_expected_format(doc.doc_type)
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="TITLE003",
                message=f"Título não segue padrão esperado para {doc.doc_type.name}",
                file_path=doc.path,
                line_number=first_line_num,
                context=first_content_line[:50],
                suggestion=f"Use formato: {expected}",
            ))

        return issues

    def _get_expected_format(self, doc_type: DocumentType) -> str:
        """Retorna formato esperado para o tipo."""
        formats = {
            DocumentType.ADR: "# ADR-NNN: Título",
            DocumentType.UC: "# UC-NNN: Título",
            DocumentType.RF: "# RF-NNN: Título",
            DocumentType.RNF: "# RNF-NNN: Título",
            DocumentType.US: "# US-NNN: Título",
            DocumentType.README: "# NOME ou # Nome - Descrição",
        }
        return formats.get(doc_type, "# Título")
