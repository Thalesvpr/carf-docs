"""Interface base para reporters."""

from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path

from ..models.results import ValidationReport


class BaseReporter(ABC):
    """Interface base para todos os reporters."""

    name: str = "base"

    @abstractmethod
    def report(self, report: ValidationReport, output: Optional[Path] = None) -> str:
        """
        Gera relatório a partir dos resultados de validação.

        Args:
            report: Resultados de validação consolidados
            output: Caminho opcional para arquivo de saída

        Returns:
            String com conteúdo do relatório
        """
        pass

    def _write_output(self, content: str, output: Optional[Path]) -> None:
        """Escreve conteúdo para arquivo se output especificado."""
        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(content, encoding='utf-8')
