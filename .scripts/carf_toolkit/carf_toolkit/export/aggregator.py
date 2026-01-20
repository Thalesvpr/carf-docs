"""Data aggregator for exporting file data."""

import json
import csv
import io
from enum import Enum
from pathlib import Path
from typing import Optional
from datetime import datetime

from ..models.file_item import FileItem, FileStatus


class ExportFormat(Enum):
    """Export format options."""
    JSON = "json"
    CSV = "csv"
    MARKDOWN = "markdown"


class DataAggregator:
    """Aggregates file data for export."""

    def __init__(self, files: list[FileItem], root_path: Optional[Path] = None):
        """Initialize the aggregator.

        Args:
            files: List of FileItems to aggregate
            root_path: Root directory path
        """
        self.files = files
        self.root_path = root_path

    def get_statistics(self) -> dict:
        """Get aggregated statistics.

        Returns:
            Dictionary with statistics
        """
        total = len(self.files)

        # Count by status
        by_status = {}
        for file_item in self.files:
            status = file_item.file_status or "Review"
            by_status[status] = by_status.get(status, 0) + 1

        # Count by type
        by_type = {}
        for file_item in self.files:
            doc_type = file_item.doc_type or "Unknown"
            by_type[doc_type] = by_type.get(doc_type, 0) + 1

        # Validation stats
        total_errors = sum(f.error_count for f in self.files)
        total_warnings = sum(f.warning_count for f in self.files)
        total_broken_links = sum(f.broken_links_count for f in self.files)

        # Files with issues
        files_with_errors = sum(1 for f in self.files if f.error_count > 0)
        files_with_broken_links = sum(1 for f in self.files if f.broken_links_count > 0)

        return {
            "total_files": total,
            "by_status": by_status,
            "by_type": by_type,
            "validation": {
                "total_errors": total_errors,
                "total_warnings": total_warnings,
                "files_with_errors": files_with_errors,
            },
            "links": {
                "total_broken": total_broken_links,
                "files_with_broken_links": files_with_broken_links,
            },
            "generated_at": datetime.now().isoformat(),
        }

    def export(
        self,
        format: ExportFormat = ExportFormat.JSON,
        include_validation: bool = True,
        scope: str = "all",  # "all", "review", "approved", "rejected"
    ) -> str:
        """Export data in the specified format.

        Args:
            format: Export format (JSON, CSV, or Markdown)
            include_validation: Whether to include validation data
            scope: Which files to include

        Returns:
            Exported data as string
        """
        # Filter files by scope
        filtered_files = self._filter_by_scope(scope)

        if format == ExportFormat.JSON:
            return self._export_json(filtered_files, include_validation)
        elif format == ExportFormat.CSV:
            return self._export_csv(filtered_files, include_validation)
        elif format == ExportFormat.MARKDOWN:
            return self._export_markdown(filtered_files, include_validation)
        else:
            return self._export_json(filtered_files, include_validation)

    def _filter_by_scope(self, scope: str) -> list[FileItem]:
        """Filter files by scope.

        Args:
            scope: Scope filter

        Returns:
            Filtered list of files
        """
        if scope == "all":
            return self.files

        scope_map = {
            "review": ("Review", None, ""),
            "approved": ("Approved",),
            "rejected": ("Rejected",),
        }

        valid_statuses = scope_map.get(scope, ("Review", None, ""))

        return [
            f for f in self.files
            if f.file_status in valid_statuses or (
                scope == "review" and not f.file_status
            )
        ]

    def _export_json(self, files: list[FileItem], include_validation: bool) -> str:
        """Export as JSON.

        Args:
            files: Files to export
            include_validation: Include validation data

        Returns:
            JSON string
        """
        stats = self.get_statistics()

        data = {
            "statistics": stats,
            "files": [
                self._file_to_dict(f, include_validation)
                for f in files
            ]
        }

        return json.dumps(data, indent=2, ensure_ascii=False)

    def _export_csv(self, files: list[FileItem], include_validation: bool) -> str:
        """Export as CSV.

        Args:
            files: Files to export
            include_validation: Include validation data

        Returns:
            CSV string
        """
        output = io.StringIO()

        fieldnames = [
            "path", "title", "type", "status", "updated",
            "words", "links", "broken_links"
        ]
        if include_validation:
            fieldnames.extend(["errors", "warnings"])

        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()

        for file_item in files:
            row = {
                "path": file_item.relative_path,
                "title": file_item.title or "",
                "type": file_item.doc_type or "",
                "status": file_item.file_status or "Review",
                "updated": file_item.file_last_updated or "",
                "words": file_item.word_count,
                "links": len(file_item.links) if file_item.links else 0,
                "broken_links": file_item.broken_links_count,
            }
            if include_validation:
                row["errors"] = file_item.error_count
                row["warnings"] = file_item.warning_count

            writer.writerow(row)

        return output.getvalue()

    def _export_markdown(self, files: list[FileItem], include_validation: bool) -> str:
        """Export as Markdown table.

        Args:
            files: Files to export
            include_validation: Include validation data

        Returns:
            Markdown string
        """
        stats = self.get_statistics()

        lines = [
            "# CARF Toolkit Export Report",
            "",
            f"Generated: {stats['generated_at']}",
            "",
            "## Statistics",
            "",
            f"- **Total Files:** {stats['total_files']}",
            "",
            "### By Status",
            "",
        ]

        for status, count in stats["by_status"].items():
            lines.append(f"- {status}: {count}")

        lines.extend([
            "",
            "### By Type",
            "",
        ])

        for doc_type, count in stats["by_type"].items():
            lines.append(f"- {doc_type}: {count}")

        if include_validation:
            lines.extend([
                "",
                "### Validation",
                "",
                f"- Total Errors: {stats['validation']['total_errors']}",
                f"- Total Warnings: {stats['validation']['total_warnings']}",
                f"- Files with Errors: {stats['validation']['files_with_errors']}",
                "",
                "### Links",
                "",
                f"- Broken Links: {stats['links']['total_broken']}",
                f"- Files with Broken Links: {stats['links']['files_with_broken_links']}",
            ])

        lines.extend([
            "",
            "## Files",
            "",
        ])

        # Table header
        if include_validation:
            lines.append("| Path | Title | Type | Status | Words | Errors | Warnings |")
            lines.append("|------|-------|------|--------|-------|--------|----------|")
        else:
            lines.append("| Path | Title | Type | Status | Words |")
            lines.append("|------|-------|------|--------|-------|")

        for file_item in files:
            path = file_item.relative_path
            title = (file_item.title or "-")[:50]
            doc_type = file_item.doc_type or "-"
            status = file_item.file_status or "Review"
            words = file_item.word_count

            if include_validation:
                errors = file_item.error_count
                warnings = file_item.warning_count
                lines.append(f"| `{path}` | {title} | {doc_type} | {status} | {words} | {errors} | {warnings} |")
            else:
                lines.append(f"| `{path}` | {title} | {doc_type} | {status} | {words} |")

        return "\n".join(lines)

    def _file_to_dict(self, file_item: FileItem, include_validation: bool) -> dict:
        """Convert a FileItem to dictionary for export.

        Args:
            file_item: FileItem to convert
            include_validation: Include validation data

        Returns:
            Dictionary representation
        """
        data = {
            "path": file_item.relative_path,
            "title": file_item.title,
            "type": file_item.doc_type,
            "status": file_item.file_status or "Review",
            "updated": file_item.file_last_updated,
            "description": file_item.file_description,
            "word_count": file_item.word_count,
            "links": {
                "total": len(file_item.links) if file_item.links else 0,
                "broken": file_item.broken_links_count,
            },
        }

        if include_validation:
            data["validation"] = {
                "errors": file_item.error_count,
                "warnings": file_item.warning_count,
                "issues": [
                    {
                        "severity": issue.severity,
                        "code": issue.code,
                        "message": issue.message,
                        "line": issue.line_number,
                    }
                    for issue in file_item.validation_issues
                ]
            }

        return data
