"""Reporter para saída no console com cores."""

import sys
from typing import Optional
from pathlib import Path

from .base import BaseReporter
from ..models.results import ValidationReport, Severity


def _sanitize_text(text: str) -> str:
    """Remove caracteres non-ASCII problemáticos."""
    return text.encode('ascii', errors='replace').decode('ascii')


class ConsoleReporter(BaseReporter):
    """Gera relatório colorido para terminal."""

    name = "console"

    # ANSI color codes
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "green": "\033[92m",
        "dim": "\033[2m",
    }

    SEVERITY_COLORS = {
        Severity.ERROR: "red",
        Severity.WARNING: "yellow",
        Severity.INFO: "blue",
    }

    SEVERITY_ICONS = {
        Severity.ERROR: "X",
        Severity.WARNING: "!",
        Severity.INFO: "i",
    }

    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors

    def report(self, report: ValidationReport, output: Optional[Path] = None) -> str:
        lines = []

        # Header
        lines.append(self._header("CARF Validation Report"))
        lines.append("")

        # Sumário
        totals = report.totals
        lines.append(self._section("Summary"))
        lines.append(f"  Files scanned: {totals.get('files_scanned', 0)}")
        lines.append(
            f"  {self._colorize('Errors', 'red')}: {totals.get('errors', 0)}"
        )
        lines.append(
            f"  {self._colorize('Warnings', 'yellow')}: {totals.get('warnings', 0)}"
        )
        lines.append(
            f"  {self._colorize('Info', 'blue')}: {totals.get('info', 0)}"
        )
        lines.append("")

        # Resultados por validador
        for result in report.results:
            if not result.issues:
                continue

            lines.append(self._section(f"[{result.validator_name}]"))

            # Stats do validador
            if result.stats:
                stats_str = ", ".join(
                    f"{k}: {v}" for k, v in result.stats.items()
                )
                lines.append(f"  {self._colorize(stats_str, 'dim')}")

            # Issues
            for issue in result.issues:
                lines.append(self._format_issue(issue))

            lines.append("")

        # Footer com resultado
        if totals.get('errors', 0) > 0:
            lines.append(self._colorize("[FAIL] Validation FAILED", "red"))
        else:
            lines.append(self._colorize("[PASS] Validation PASSED", "green"))

        # Compatibilidade com audit-brutal.py
        lines.append("")
        lines.append(f"Errors: {totals.get('errors', 0)}")
        lines.append(f"Warnings: {totals.get('warnings', 0)}")

        content = "\n".join(lines)

        if output:
            # Remove ANSI codes para arquivo
            clean_content = self._strip_colors(content)
            self._write_output(clean_content, output)

        return content

    def _header(self, text: str) -> str:
        """Formata header."""
        line = "=" * 60
        return f"{self._colorize(line, 'bold')}\n{self._colorize(text, 'bold')}\n{self._colorize(line, 'bold')}"

    def _section(self, text: str) -> str:
        """Formata nome de seção."""
        return self._colorize(text, "bold")

    def _format_issue(self, issue) -> str:
        """Formata uma issue para console."""
        color = self.SEVERITY_COLORS.get(issue.severity, "reset")
        icon = self.SEVERITY_ICONS.get(issue.severity, "•")

        parts = []

        # Ícone e código
        parts.append(f"  {self._colorize(icon, color)} [{issue.code}]")

        # Arquivo e linha
        if issue.file_path:
            location = str(issue.file_path)
            if issue.line_number:
                location += f":{issue.line_number}"
            parts.append(self._colorize(location, "dim"))

        # Mensagem
        parts.append(issue.message)

        line = " ".join(parts)

        # Contexto e sugestão em linhas extras
        extra = []
        if issue.context:
            context = _sanitize_text(issue.context)
            extra.append(f"       {self._colorize(context, 'dim')}")
        if issue.suggestion:
            suggestion = _sanitize_text(issue.suggestion)
            extra.append(f"       -> {suggestion}")

        if extra:
            line += "\n" + "\n".join(extra)

        return line

    def _colorize(self, text: str, color: str) -> str:
        """Aplica cor ANSI ao texto."""
        if not self.use_colors:
            return text
        return f"{self.COLORS.get(color, '')}{text}{self.COLORS['reset']}"

    def _strip_colors(self, text: str) -> str:
        """Remove códigos ANSI do texto."""
        import re
        return re.sub(r'\033\[[0-9;]*m', '', text)
