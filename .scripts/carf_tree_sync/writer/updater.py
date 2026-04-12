"""README updater for writing generated content."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from ..parser.generated import GeneratedSectionParser, ParsedContent
from ..indexer.base import IndexResult


@dataclass
class UpdateResult:
    """Result of a README update operation."""

    path: Path
    updated: bool
    dry_run: bool
    old_content: Optional[str]
    new_content: Optional[str]
    message: str

    @property
    def changed(self) -> bool:
        """Check if content actually changed."""
        return self.old_content != self.new_content


class ReadmeUpdater:
    """Updates README files with generated content."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.parser = GeneratedSectionParser()

    def update(
        self,
        readme_path: Path,
        index_results: List[IndexResult],
    ) -> UpdateResult:
        """Update README with generated index content.

        Args:
            readme_path: Path to README.md file
            index_results: List of IndexResult objects to include

        Returns:
            UpdateResult with operation details
        """
        if not readme_path.exists():
            return UpdateResult(
                path=readme_path,
                updated=False,
                dry_run=self.dry_run,
                old_content=None,
                new_content=None,
                message="Arquivo nao existe",
            )

        try:
            old_content = readme_path.read_text(encoding="utf-8")
        except Exception as e:
            return UpdateResult(
                path=readme_path,
                updated=False,
                dry_run=self.dry_run,
                old_content=None,
                new_content=None,
                message=f"Erro ao ler: {e}",
            )

        # Parse existing content
        parsed = self.parser.parse(old_content)

        # Build new generated section
        generated_content = self._build_generated_content(index_results)

        # Rebuild full content
        new_content = self.parser.rebuild(parsed, generated_content)

        # Check if content changed
        if old_content == new_content:
            return UpdateResult(
                path=readme_path,
                updated=False,
                dry_run=self.dry_run,
                old_content=old_content,
                new_content=new_content,
                message="Sem alteracoes",
            )

        # Write if not dry run
        if not self.dry_run:
            try:
                readme_path.write_text(new_content, encoding="utf-8")
            except Exception as e:
                return UpdateResult(
                    path=readme_path,
                    updated=False,
                    dry_run=self.dry_run,
                    old_content=old_content,
                    new_content=new_content,
                    message=f"Erro ao escrever: {e}",
                )

        # Determine what changed
        change_desc = self._describe_changes(parsed, index_results)

        return UpdateResult(
            path=readme_path,
            updated=True,
            dry_run=self.dry_run,
            old_content=old_content,
            new_content=new_content,
            message=change_desc,
        )

    def _build_generated_content(
        self, index_results: List[IndexResult]
    ) -> str:
        """Build the content for the generated section."""
        parts = []

        for result in index_results:
            parts.append(result.content)

        return "\n".join(parts)

    def _describe_changes(
        self,
        parsed: ParsedContent,
        index_results: List[IndexResult],
    ) -> str:
        """Describe what changed."""
        if not parsed.has_generated_section:
            return "Secao gerada adicionada"

        total_items = sum(r.item_count for r in index_results)
        return f"Atualizado ({total_items} itens)"
