"""Reporter para saída em Markdown."""

from typing import Optional, List
from pathlib import Path
from datetime import datetime

from .base import BaseReporter
from ..models.results import ValidationReport, ValidatorResult, ValidationIssue, Severity


class MarkdownReporter(BaseReporter):
    """Gera relatório em formato Markdown."""

    name = "markdown"

    SEVERITY_BADGES = {
        Severity.ERROR: "🔴",
        Severity.WARNING: "🟡",
        Severity.INFO: "🔵",
    }

    def report(self, report: ValidationReport, output: Optional[Path] = None) -> str:
        lines = []

        # Header
        lines.append("# CARF Validation Report")
        lines.append("")
        lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        lines.append("")

        # Sumário
        totals = report.totals
        lines.append("## Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Files scanned | {totals.get('files_scanned', 0)} |")
        lines.append(f"| 🔴 Errors | **{totals.get('errors', 0)}** |")
        lines.append(f"| 🟡 Warnings | {totals.get('warnings', 0)} |")
        lines.append(f"| 🔵 Info | {totals.get('info', 0)} |")
        lines.append("")

        # Status geral
        if totals.get('errors', 0) > 0:
            lines.append("> ❌ **Validation FAILED** - Fix errors before proceeding")
        else:
            lines.append("> ✅ **Validation PASSED**")
        lines.append("")

        # Resultados por validador
        lines.append("## Results by Validator")
        lines.append("")

        for result in report.results:
            lines.extend(self._format_validator_result(result))

        # Arquivos com mais issues
        lines.extend(self._format_hotspots(report))

        content = "\n".join(lines)

        if output:
            self._write_output(content, output)

        return content

    def _format_validator_result(self, result: ValidatorResult) -> List[str]:
        """Formata resultado de um validador."""
        lines = []

        # Header do validador
        issue_count = len(result.issues)
        error_count = sum(1 for i in result.issues if i.severity == Severity.ERROR)

        if error_count > 0:
            status = "🔴"
        elif issue_count > 0:
            status = "🟡"
        else:
            status = "✅"

        lines.append(f"### {status} {result.validator_name}")
        lines.append("")

        # Stats
        if result.stats:
            lines.append("<details>")
            lines.append("<summary>Statistics</summary>")
            lines.append("")
            for key, value in result.stats.items():
                lines.append(f"- **{key}**: {value}")
            lines.append("")
            lines.append("</details>")
            lines.append("")

        # Issues
        if result.issues:
            lines.append(f"**{issue_count} issue(s) found:**")
            lines.append("")

            # Agrupa por arquivo
            by_file = {}
            for issue in result.issues:
                key = str(issue.file_path) if issue.file_path else "(global)"
                if key not in by_file:
                    by_file[key] = []
                by_file[key].append(issue)

            for file_path, issues in sorted(by_file.items()):
                lines.append(f"<details>")
                lines.append(f"<summary><code>{file_path}</code> ({len(issues)})</summary>")
                lines.append("")

                for issue in issues:
                    lines.append(self._format_issue(issue))

                lines.append("")
                lines.append("</details>")
                lines.append("")

        else:
            lines.append("*No issues found.*")
            lines.append("")

        return lines

    def _format_issue(self, issue: ValidationIssue) -> str:
        """Formata uma issue para Markdown."""
        badge = self.SEVERITY_BADGES.get(issue.severity, "⚪")

        parts = [f"- {badge} `{issue.code}`"]

        if issue.line_number:
            parts.append(f"(line {issue.line_number})")

        parts.append(f": {issue.message}")

        line = " ".join(parts)

        if issue.context:
            line += f"\n  - Context: `{issue.context}`"
        if issue.suggestion:
            line += f"\n  - 💡 {issue.suggestion}"

        return line

    def _format_hotspots(self, report: ValidationReport) -> List[str]:
        """Formata seção de arquivos com mais issues."""
        lines = []

        # Conta issues por arquivo
        by_file = {}
        for result in report.results:
            for issue in result.issues:
                key = str(issue.file_path) if issue.file_path else "(global)"
                if key not in by_file:
                    by_file[key] = {"errors": 0, "warnings": 0, "info": 0}

                if issue.severity == Severity.ERROR:
                    by_file[key]["errors"] += 1
                elif issue.severity == Severity.WARNING:
                    by_file[key]["warnings"] += 1
                else:
                    by_file[key]["info"] += 1

        if not by_file:
            return lines

        # Top 10 arquivos por total de issues
        sorted_files = sorted(
            by_file.items(),
            key=lambda x: (x[1]["errors"], x[1]["warnings"], x[1]["info"]),
            reverse=True
        )[:10]

        lines.append("## Hotspots (files with most issues)")
        lines.append("")
        lines.append("| File | 🔴 | 🟡 | 🔵 | Total |")
        lines.append("|------|----|----|-------|-------|")

        for file_path, counts in sorted_files:
            total = counts["errors"] + counts["warnings"] + counts["info"]
            if total == 0:
                continue

            # Trunca path longo
            display_path = file_path
            if len(display_path) > 50:
                display_path = "..." + display_path[-47:]

            lines.append(
                f"| `{display_path}` | {counts['errors']} | {counts['warnings']} | {counts['info']} | {total} |"
            )

        lines.append("")

        return lines
