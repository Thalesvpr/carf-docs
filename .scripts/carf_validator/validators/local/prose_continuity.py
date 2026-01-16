"""Validador de continuidade de prosa."""

import re
from typing import List, Tuple

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class ProseContinuityValidator(LocalValidator):
    """Valida continuidade de prosa: detecta fragmentação excessiva."""

    name = "prose_continuity"
    description = "Detecta quebras excessivas de prosa e parágrafos órfãos"

    # Tipos que devem ter prosa contínua
    PROSE_TYPES = {
        DocumentType.RF,
        DocumentType.US,
        DocumentType.UC,
        DocumentType.ENTITY,
        DocumentType.BUSINESS_RULE,
        DocumentType.FEATURE,
    }

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        if doc.doc_type not in self.PROSE_TYPES:
            return issues

        content = self._extract_prose_content(doc.content)

        # Detecta quebras excessivas de linha
        excessive_breaks = self._find_excessive_breaks(content)
        if excessive_breaks:
            issues.append(ValidationIssue(
                severity=Severity.INFO,
                code="PROSE001",
                message=f"Quebras excessivas de linha ({excessive_breaks} ocorrências)",
                file_path=doc.path,
                suggestion="Consolide parágrafos - use 1 linha em branco entre parágrafos",
            ))

        # Detecta parágrafos órfãos (muito curtos)
        orphan_paragraphs = self._find_orphan_paragraphs(content)
        for line_num, text in orphan_paragraphs:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="PROSE002",
                message="Parágrafo órfão (muito curto/isolado)",
                file_path=doc.path,
                line_number=line_num,
                context=text[:60],
                suggestion="Integre ao parágrafo anterior usando vírgulas",
            ))

        # Verifica ratio vírgulas/períodos (prosa densa usa mais vírgulas)
        comma_ratio = self._check_comma_ratio(content)
        if comma_ratio is not None and comma_ratio < 1.0:
            issues.append(ValidationIssue(
                severity=Severity.INFO,
                code="PROSE003",
                message=f"Baixa densidade de vírgulas (ratio: {comma_ratio:.1f})",
                file_path=doc.path,
                suggestion="Prefira sentenças longas conectadas por vírgulas ao invés de sentenças curtas separadas",
            ))

        return issues

    def _extract_prose_content(self, content: str) -> str:
        """Extrai apenas conteúdo de prosa."""
        # Remove frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Remove título H1
        content = re.sub(r'^#\s+[^\n]+\n', '', content)

        # Remove blocos de código
        content = re.sub(r'```[\s\S]*?```', '', content)

        # Remove seções de footer (após ---)
        content = re.sub(r'\n---\n.*$', '', content, flags=re.DOTALL)

        # Remove seções bold de footer
        footer_patterns = [
            r'\*\*Fluxos Alternativos:\*\*.*$',
            r'\*\*Fluxos de Exceção:\*\*.*$',
            r'\*\*Regras de Negócio:\*\*.*$',
            r'\*\*Rastreabilidade:\*\*.*$',
            r'\*\*Critérios[^:]*:\*\*.*$',
            r'\*\*Última atualização:\*\*.*$',
        ]
        for pattern in footer_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.MULTILINE)

        return content

    def _find_excessive_breaks(self, content: str) -> int:
        """Conta ocorrências de 3+ quebras de linha seguidas."""
        matches = re.findall(r'\n{3,}', content)
        return len(matches)

    def _find_orphan_paragraphs(self, content: str) -> List[Tuple[int, str]]:
        """Encontra parágrafos muito curtos (órfãos)."""
        orphans = []
        lines = content.split('\n')

        current_para = []
        para_start_line = 1

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            if not stripped:
                if current_para:
                    # Analisa parágrafo acumulado
                    para_text = ' '.join(current_para)
                    words = len(para_text.split())

                    # Parágrafo muito curto (< 15 palavras) é órfão
                    if 5 < words < 15:
                        orphans.append((para_start_line, para_text))

                    current_para = []
            else:
                if not current_para:
                    para_start_line = i
                current_para.append(stripped)

        # Último parágrafo
        if current_para:
            para_text = ' '.join(current_para)
            words = len(para_text.split())
            if 5 < words < 15:
                orphans.append((para_start_line, para_text))

        return orphans

    def _check_comma_ratio(self, content: str) -> float | None:
        """Calcula ratio de vírgulas para períodos."""
        commas = content.count(',')
        periods = content.count('.')

        if periods < 2:
            return None

        return commas / periods
