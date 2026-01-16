"""Validador de bullets apenas em seções de footer."""

import re
from typing import List, Tuple

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class ContentBulletsValidator(LocalValidator):
    """Valida que bullets aparecem apenas em seções de footer."""

    name = "content_bullets"
    description = "Valida que bullets são usados apenas em seções estruturadas de footer"

    # Seções onde bullets são PERMITIDOS
    ALLOWED_BULLET_SECTIONS = [
        "Fluxos Alternativos",
        "Fluxos de Exceção",
        "Regras de Negócio",
        "Rastreabilidade",
        "Critérios de Aceitação",
        "Relacionamentos",
        "Relacionado",
        "Módulos",
        "Pré-condições",
        "Pós-condições",
        "Atores",
        "Referências",
        "Ver também",
        "Dependências",
        "Estrutura",
        "Aplicações",
        "Bibliotecas",
        "Domínios",
    ]

    # Tipos que devem ter prosa contínua (bullets só no footer)
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

        # Analisa posição de bullets vs seções permitidas
        bullet_issues = self._find_invalid_bullets(doc.content)

        for line_num, line_text in bullet_issues:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="BULLET001",
                message="Bullet encontrado fora de seção estruturada",
                file_path=doc.path,
                line_number=line_num,
                context=line_text[:60],
                suggestion="Use prosa contínua no corpo. Bullets apenas em seções como Rastreabilidade, Critérios, etc.",
            ))

        return issues

    def _find_invalid_bullets(self, content: str) -> List[Tuple[int, str]]:
        """Encontra bullets que estão fora de seções permitidas."""
        lines = content.split('\n')
        invalid_bullets = []

        in_allowed_section = False
        in_code_block = False
        in_frontmatter = False
        past_separator = False

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Track frontmatter
            if stripped == '---':
                if i == 1:
                    in_frontmatter = True
                elif in_frontmatter:
                    in_frontmatter = False
                else:
                    past_separator = True
                continue

            if in_frontmatter:
                continue

            # Track code blocks
            if stripped.startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Check for section headers
            if self._is_allowed_section_header(stripped):
                in_allowed_section = True
                continue

            # Check for any H2/H3 header (resets section context)
            if stripped.startswith('## ') or stripped.startswith('### '):
                in_allowed_section = False
                continue

            # Após separador ---, bullets são permitidos no footer
            if past_separator:
                continue

            # Check for bullet
            if self._is_bullet_line(stripped):
                if not in_allowed_section:
                    invalid_bullets.append((i, line))

        return invalid_bullets

    def _is_allowed_section_header(self, line: str) -> bool:
        """Verifica se é um header de seção que permite bullets."""
        # Headers markdown ## ou ###
        for section in self.ALLOWED_BULLET_SECTIONS:
            if re.search(rf'^##\s*{section}', line, re.IGNORECASE):
                return True
            if re.search(rf'^###\s*{section}', line, re.IGNORECASE):
                return True

        # Headers em negrito **Seção:**
        for section in self.ALLOWED_BULLET_SECTIONS:
            if re.search(rf'\*\*{section}[^:]*:\*\*', line, re.IGNORECASE):
                return True

        return False

    def _is_bullet_line(self, line: str) -> bool:
        """Verifica se a linha é um bullet."""
        # Bullets markdown: -, *, +, ou numerados
        if re.match(r'^[-*+]\s+', line):
            return True
        if re.match(r'^\d+\.\s+', line):
            return True
        return False
