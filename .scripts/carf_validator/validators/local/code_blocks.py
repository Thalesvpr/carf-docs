"""Validador que proibe code blocks nao-bash em documentacao."""

import re
from typing import List

from ..base import LocalValidator
from ..registry import validator
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class CodeBlocksValidator(LocalValidator):
    """Detecta code blocks nao-bash em documentos (somente bash permitido)."""

    name = "code_blocks"
    description = "Detecta code blocks nao-bash (somente bash permitido)"

    # Linguagens permitidas
    ALLOWED_LANGUAGES = {'bash', 'sh', 'shell', 'zsh'}

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        content = doc.content

        # Encontra todos os code blocks com sua linguagem
        # Padrão: ```linguagem ... ``` ou ``` ... ```
        code_block_pattern = r'```(\w*)\n[\s\S]*?```'
        matches = re.findall(code_block_pattern, content)

        # Filtra code blocks que NAO sao bash
        forbidden_blocks = []
        for lang in matches:
            lang_lower = lang.lower() if lang else ''
            if lang_lower not in self.ALLOWED_LANGUAGES and lang_lower != '':
                forbidden_blocks.append(lang_lower)
            elif lang_lower == '':
                # Code block sem linguagem especificada
                forbidden_blocks.append('(sem linguagem)')

        if forbidden_blocks:
            # Conta por tipo
            from collections import Counter
            counts = Counter(forbidden_blocks)
            details = ', '.join(f"{lang}: {cnt}" for lang, cnt in counts.most_common())

            issues.append(ValidationIssue(
                severity=Severity.ERROR,
                code="CODE001",
                message=f"Documento contem {len(forbidden_blocks)} code block(s) nao-bash ({details})",
                file_path=doc.path,
                suggestion="Somente code blocks bash/sh sao permitidos. Extraia outros para arquivos separados (.yaml, .sql, etc.)",
            ))

        return issues
