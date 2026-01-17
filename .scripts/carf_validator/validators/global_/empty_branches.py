"""Validador de ramos sem folhas (pastas vazias ou só com README)."""

from pathlib import Path
from typing import List, Set

from ..base import GlobalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class EmptyBranchesValidator(GlobalValidator):
    """Detecta pastas que têm README mas nenhum arquivo de conteúdo."""

    name = "empty_branches"
    description = "Detecta pastas sem arquivos de conteúdo (ramos sem folhas)"

    # Pastas que são exceções (podem estar vazias)
    ALLOWED_EMPTY = {
        "CONFIGS",
        "PROVISIONING",
        "SRC-CODE",  # Código fonte pode não ter docs
    }

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        # Agrupa documentos por diretório
        dirs_with_content: Set[Path] = set()
        dirs_with_readme: Set[Path] = set()

        for doc in context.get_all_documents():
            parent = doc.path.parent

            if doc.doc_type == DocumentType.README:
                dirs_with_readme.add(parent)
            else:
                # Arquivo de conteúdo - marca este dir e todos os pais
                dirs_with_content.add(parent)
                # Marca pais também (eles têm conteúdo indiretamente)
                for ancestor in parent.parents:
                    if ancestor == context.root_dir or str(context.root_dir) in str(ancestor):
                        dirs_with_content.add(ancestor)
                    else:
                        break

        # Encontra diretórios com README mas sem conteúdo
        empty_branches = dirs_with_readme - dirs_with_content

        for dir_path in sorted(empty_branches):
            # Verifica se é exceção
            if dir_path.name in self.ALLOWED_EMPTY:
                continue

            # Verifica se algum pai é exceção
            if any(p.name in self.ALLOWED_EMPTY for p in dir_path.parents):
                continue

            # Caminho relativo para exibição
            try:
                rel_path = dir_path.relative_to(context.root_dir)
            except ValueError:
                rel_path = dir_path

            readme_path = dir_path / "README.md"

            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="BRANCH001",
                message=f"Pasta '{rel_path}' tem README mas nenhum arquivo de conteúdo",
                file_path=readme_path if readme_path.exists() else dir_path,
                suggestion="Adicione arquivos de conteúdo ou remova a pasta se não for necessária",
            ))

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "total_dirs_with_readme": len(dirs_with_readme),
                "empty_branches": len(empty_branches),
            }
        )
