"""Validador de formato de links."""

import re
from typing import List

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class LinkFormatValidator(LocalValidator):
    """Valida formato de links: paths relativos, diretórios UPPERCASE, etc."""

    name = "link_format"
    description = "Valida formato de links internos"

    # Padrão de path absoluto Windows
    WINDOWS_ABSOLUTE = re.compile(r'\]\([A-Za-z]:\\')

    # Padrão de path absoluto Unix
    UNIX_ABSOLUTE = re.compile(r'\]\(/[^/]')

    # Padrão de link interno válido (relativo)
    VALID_INTERNAL = re.compile(r'\]\(\./|\]\(\.\./')

    # Padrão de link externo
    EXTERNAL_LINK = re.compile(r'\]\(https?://|\]\(mailto:|\]\(#')

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        lines = doc.content.split('\n')

        for i, line in enumerate(lines, 1):
            # Encontra todos os links na linha
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', line)

            for link_text, link_target in links:
                # Pula links externos
                if self._is_external(link_target):
                    continue

                # Pula âncoras internas
                if link_target.startswith('#'):
                    continue

                # Verifica path absoluto Windows
                if re.match(r'^[A-Za-z]:\\', link_target):
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        code="LINK001",
                        message="Link com path absoluto Windows",
                        file_path=doc.path,
                        line_number=i,
                        context=f"[{link_text}]({link_target[:30]}...)",
                        suggestion="Use path relativo: ./pasta/arquivo.md",
                    ))
                    continue

                # Verifica path absoluto Unix
                if re.match(r'^/[^/]', link_target):
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        code="LINK002",
                        message="Link com path absoluto Unix",
                        file_path=doc.path,
                        line_number=i,
                        context=f"[{link_text}]({link_target[:30]})",
                        suggestion="Use path relativo: ./pasta/arquivo.md",
                    ))
                    continue

                # Verifica se é path relativo válido
                if not link_target.startswith('./') and not link_target.startswith('../'):
                    # Pode ser link sem prefixo (arquivo.md)
                    if '/' in link_target and not link_target.startswith('#'):
                        issues.append(ValidationIssue(
                            severity=Severity.WARNING,
                            code="LINK003",
                            message="Link deve usar prefixo relativo ./",
                            file_path=doc.path,
                            line_number=i,
                            context=f"[{link_text}]({link_target[:30]})",
                            suggestion=f"Use ./{link_target}",
                        ))

                # Verifica convenção de diretórios UPPERCASE
                # Links para pastas em CENTRAL devem ser UPPERCASE
                if '/CENTRAL/' in str(doc.path) or doc.relative_path.startswith('CENTRAL'):
                    dir_match = re.match(r'\./([a-z][a-z0-9-]*?)/', link_target)
                    if dir_match:
                        dir_name = dir_match.group(1)
                        if not dir_name.isupper():
                            issues.append(ValidationIssue(
                                severity=Severity.INFO,
                                code="LINK004",
                                message=f"Diretório '{dir_name}' deveria ser UPPERCASE",
                                file_path=doc.path,
                                line_number=i,
                                context=f"[{link_text}]({link_target[:30]})",
                                suggestion=f"Use ./{dir_name.upper()}/",
                            ))

                # Verifica link para README
                if link_target.endswith('/'):
                    issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        code="LINK005",
                        message="Link para diretório sem README.md",
                        file_path=doc.path,
                        line_number=i,
                        context=f"[{link_text}]({link_target})",
                        suggestion=f"Use {link_target}README.md",
                    ))

        return issues

    def _is_external(self, target: str) -> bool:
        """Verifica se é link externo."""
        return (
            target.startswith('http://') or
            target.startswith('https://') or
            target.startswith('mailto:') or
            target.startswith('ftp://')
        )
