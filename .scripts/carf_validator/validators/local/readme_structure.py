"""Validador de estrutura de README e detecção de index files."""

import re
from typing import List

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class ReadmeStructureValidator(LocalValidator):
    """Valida estrutura específica de README e detecta index files proibidos."""

    name = "readme_structure"
    description = "Valida estrutura de README e proíbe arquivos index"

    # Padrões de seção estrutura permitidos
    STRUCTURE_SECTION_PATTERNS = [
        r"## Estrutura",
        r"## Aplicações",
        r"## Bibliotecas",
        r"## Domínios",
        r"## Índice",
        r"## Arquivos",
    ]

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        # REGRA CRÍTICA: Não deve haver arquivos index.md
        filename = doc.path.name.lower()
        if filename == 'index.md':
            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="README001",
                message="Arquivo index.md não permitido - use README.md",
                file_path=doc.path,
                suggestion="Renomeie para README.md",
            ))
            return issues  # Não continua validação de index

        # Validações específicas para README
        if doc.doc_type != DocumentType.README:
            return issues

        lines = doc.content.split('\n')

        # Remove frontmatter para encontrar conteúdo
        start_idx = 0
        if lines and lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    start_idx = i + 1
                    break

        # Encontra primeira linha de conteúdo
        first_content_idx = start_idx
        for i in range(start_idx, len(lines)):
            if lines[i].strip():
                first_content_idx = i
                break

        # Verifica H1 como primeira linha de conteúdo
        if first_content_idx < len(lines):
            first_line = lines[first_content_idx].strip()
            if not first_line.startswith('# '):
                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    code="README002",
                    message="README deve começar com título H1",
                    file_path=doc.path,
                    line_number=first_content_idx + 1,
                    context=first_line[:50],
                    suggestion="Adicione # TÍTULO na primeira linha",
                ))

            # Verifica se H1 é UPPERCASE ou Nome - Descrição
            elif not re.match(r'^# [A-Z][A-Z0-9-]*$|^# [A-Z].*-.*$', first_line):
                # Permite também títulos normais com primeira letra maiúscula
                if not re.match(r'^# [A-Z]', first_line):
                    issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        code="README003",
                        message="Título README deve começar com letra maiúscula",
                        file_path=doc.path,
                        line_number=first_content_idx + 1,
                        context=first_line[:50],
                        suggestion="Use # NOME ou # Nome - Descrição",
                    ))

            # Verifica linha em branco após H1
            if first_content_idx + 1 < len(lines):
                next_line = lines[first_content_idx + 1].strip()
                if next_line:
                    issues.append(ValidationIssue(
                        severity=Severity.INFO,
                        code="README004",
                        message="Falta linha em branco após título H1",
                        file_path=doc.path,
                        line_number=first_content_idx + 2,
                        suggestion="Adicione uma linha em branco após o título",
                    ))

        # Verifica seção de estrutura em READMEs de diretório
        has_structure_section = any(
            re.search(pattern, doc.content, re.IGNORECASE)
            for pattern in self.STRUCTURE_SECTION_PATTERNS
        )

        # READMEs de pastas que contêm subdiretórios devem ter seção estrutura
        # (Detectado por presença de links para subpastas)
        has_subfolder_links = bool(re.search(r'\]\(\./[A-Z0-9-]+/', doc.content))

        if has_subfolder_links and not has_structure_section:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="README005",
                message="README com subpastas sem seção de estrutura",
                file_path=doc.path,
                suggestion="Adicione ## Estrutura, ## Domínios ou similar",
            ))

        # Verifica separador antes do footer
        content = doc.content
        if '**Última atualização:**' in content:
            # Deve ter --- antes do footer
            footer_match = re.search(r'\*\*Última atualização:\*\*', content)
            if footer_match:
                before_footer = content[:footer_match.start()]
                if not re.search(r'\n---\s*\n\s*$', before_footer):
                    issues.append(ValidationIssue(
                        severity=Severity.INFO,
                        code="README006",
                        message="Falta separador --- antes do footer",
                        file_path=doc.path,
                        suggestion="Adicione uma linha --- antes de **Última atualização:**",
                    ))

        # Verifica links bold em listas de estrutura
        if has_structure_section:
            # Padrão esperado: - **[NAME/](./path)** - Descrição
            list_items = re.findall(r'^-\s+\[[^\]]+\]\([^)]+\)', content, re.MULTILINE)
            non_bold_items = [
                item for item in list_items
                if not re.match(r'^-\s+\*\*\[', item)
            ]

            if non_bold_items and len(non_bold_items) > 2:
                issues.append(ValidationIssue(
                    severity=Severity.INFO,
                    code="README007",
                    message=f"Links de estrutura sem negrito ({len(non_bold_items)} itens)",
                    file_path=doc.path,
                    suggestion="Use - **[NOME/](./path)** - Descrição",
                ))

        return issues
