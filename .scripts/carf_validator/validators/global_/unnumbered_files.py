"""Validador de arquivos sem numeração obrigatória."""

import re
from pathlib import Path
from typing import List

from ..base import GlobalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class UnnumberedFilesValidator(GlobalValidator):
    """Detecta arquivos sem prefixo numérico obrigatório."""

    name = "unnumbered_files"
    description = "Detecta arquivos sem numeração obrigatória (XX-nome.md)"

    # Padrões de numeração válidos
    NUMBER_PATTERNS = [
        r"^(\d{2})-",                    # 01-nome.md
        r"^(\d{3})-",                    # 001-nome.md
        r"^(RF)-(\d{3})",                # RF-001
        r"^(RNF)-(\d{3})",               # RNF-001
        r"^(US)-(\d{3})",                # US-001
        r"^(UC)-(\d{3})",                # UC-001
        r"^(ADR)-(\d{3})",               # ADR-001
    ]

    # Arquivos isentos de numeração
    EXEMPT_FILES = {
        "README.md",
        "CHANGELOG.md",
        "LICENSE.md",
        "CONTRIBUTING.md",
        "index.md",
        "index-by-epic.md",
        "index-by-module.md",
    }

    # Pastas onde numeração não é obrigatória
    EXEMPT_DIRS = {
        "SRC-CODE",
        ".scripts",
        ".obsidian",
        ".github",
        "node_modules",
    }

    def _is_numbered(self, filename: str) -> bool:
        """Verifica se arquivo tem prefixo numérico válido."""
        for pattern in self.NUMBER_PATTERNS:
            if re.match(pattern, filename):
                return True
        return False

    def _is_exempt(self, path: Path, root: Path) -> bool:
        """Verifica se arquivo/pasta é isento de numeração."""
        if path.name in self.EXEMPT_FILES:
            return True

        # Verifica se está em pasta isenta
        try:
            rel_parts = path.relative_to(root).parts
            for part in rel_parts:
                if part in self.EXEMPT_DIRS:
                    return True
        except ValueError:
            pass

        return False

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        for doc in context.get_all_documents():
            # Ignora READMEs
            if doc.doc_type == DocumentType.README:
                continue

            # Ignora arquivos isentos
            if self._is_exempt(doc.path, context.root_dir):
                continue

            # Verifica se tem numeração
            if not self._is_numbered(doc.path.name):
                try:
                    rel_path = doc.path.relative_to(context.root_dir)
                except ValueError:
                    rel_path = doc.path

                # Sugere formato baseado no tipo
                if doc.doc_type == DocumentType.RF:
                    suggestion = "Use formato RF-XXX-nome.md"
                elif doc.doc_type == DocumentType.RNF:
                    suggestion = "Use formato RNF-XXX-nome.md"
                elif doc.doc_type == DocumentType.US:
                    suggestion = "Use formato US-XXX-nome.md"
                elif doc.doc_type == DocumentType.UC:
                    suggestion = "Use formato UC-XXX-nome.md"
                elif doc.doc_type == DocumentType.ADR:
                    suggestion = "Use formato ADR-XXX-nome.md"
                else:
                    suggestion = "Use formato XX-nome.md (ex: 01-nome.md)"

                issues.append(ValidationIssue(
                    severity=Severity.ERROR,
                    code="NUM001",
                    message=f"Arquivo sem numeração obrigatória: {doc.path.name}",
                    file_path=doc.path,
                    suggestion=suggestion,
                ))

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "unnumbered_files": len(issues),
            }
        )
