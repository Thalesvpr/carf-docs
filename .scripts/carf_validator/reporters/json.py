"""Reporter para saída em JSON."""

import json
from typing import Optional, Any, Dict
from pathlib import Path
from datetime import datetime

from .base import BaseReporter
from ..models.results import ValidationReport, Severity


class JsonReporter(BaseReporter):
    """Gera relatório em formato JSON estruturado."""

    name = "json"

    def __init__(self, pretty: bool = True):
        self.pretty = pretty

    def report(self, report: ValidationReport, output: Optional[Path] = None) -> str:
        data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "validator_version": "1.0.0",
            },
            "summary": {
                "files_scanned": report.totals.get("files_scanned", 0),
                "total_issues": (
                    report.totals.get("errors", 0) +
                    report.totals.get("warnings", 0) +
                    report.totals.get("info", 0)
                ),
                "errors": report.totals.get("errors", 0),
                "warnings": report.totals.get("warnings", 0),
                "info": report.totals.get("info", 0),
                "passed": report.totals.get("errors", 0) == 0,
            },
            "validators": [],
            "issues_by_file": {},
        }

        # Resultados por validador
        for result in report.results:
            validator_data = {
                "name": result.validator_name,
                "stats": result.stats,
                "issue_count": len(result.issues),
                "issues": [
                    self._serialize_issue(issue)
                    for issue in result.issues
                ],
            }
            data["validators"].append(validator_data)

            # Agrupa por arquivo
            for issue in result.issues:
                file_key = str(issue.file_path) if issue.file_path else "__global__"
                if file_key not in data["issues_by_file"]:
                    data["issues_by_file"][file_key] = []
                data["issues_by_file"][file_key].append({
                    "validator": result.validator_name,
                    **self._serialize_issue(issue)
                })

        # Serializa
        if self.pretty:
            content = json.dumps(data, indent=2, ensure_ascii=False)
        else:
            content = json.dumps(data, ensure_ascii=False)

        if output:
            self._write_output(content, output)

        return content

    def _serialize_issue(self, issue) -> Dict[str, Any]:
        """Serializa uma issue para dicionário JSON-safe."""
        return {
            "severity": issue.severity.name.lower(),
            "code": issue.code,
            "message": issue.message,
            "file_path": str(issue.file_path) if issue.file_path else None,
            "line_number": issue.line_number,
            "context": issue.context,
            "suggestion": issue.suggestion,
        }
