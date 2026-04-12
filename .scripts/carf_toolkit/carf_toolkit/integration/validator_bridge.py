"""Bridge to integrate carf_validator functionality."""

import sys
from pathlib import Path
from typing import Optional

from ..models.file_item import FileItem, ValidationIssue


class ValidatorBridge:
    """Bridge to carf_validator for running validations."""

    def __init__(self, root_path: Optional[Path] = None):
        """Initialize the validator bridge.

        Args:
            root_path: Root directory for validation
        """
        self.root_path = root_path
        self._pipeline = None
        self._context = None
        self._available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if carf_validator is available."""
        try:
            # Add scripts directory to path if needed
            scripts_dir = Path(__file__).parent.parent.parent.parent
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))

            from carf_validator import ValidationPipeline
            return True
        except ImportError:
            return False

    @property
    def is_available(self) -> bool:
        """Check if validator is available."""
        return self._available

    def set_root_path(self, root_path: Path) -> None:
        """Set the root path for validation.

        Args:
            root_path: Root directory path
        """
        self.root_path = root_path
        self._pipeline = None
        self._context = None

    def _ensure_pipeline(self) -> bool:
        """Ensure the validation pipeline is initialized.

        Returns:
            True if pipeline is ready, False otherwise
        """
        if not self._available or not self.root_path:
            return False

        if self._pipeline is None:
            try:
                from carf_validator import ValidationPipeline
                self._pipeline = ValidationPipeline(
                    root_path=self.root_path,
                    disabled_validators={"orphans", "isolation"}  # Skip slow validators
                )
            except Exception:
                return False

        return True

    def validate_file(self, file_item: FileItem) -> list[ValidationIssue]:
        """Validate a single file.

        Args:
            file_item: FileItem to validate

        Returns:
            List of ValidationIssue objects
        """
        if not self._available:
            return []

        issues = []

        try:
            # Add scripts directory to path if needed
            scripts_dir = Path(__file__).parent.parent.parent.parent
            if str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))

            from carf_validator.scanner.tree import DocumentTreeBuilder
            from carf_validator.validators.registry import ValidatorRegistry
            from carf_validator.context.registry import DocumentRegistry
            from carf_validator.context.graph import RelationshipGraph
            from carf_validator.context.queries import ValidationContext
            from carf_validator.models.results import Severity

            # Parse the document
            builder = DocumentTreeBuilder(self.root_path)
            doc_node = builder._parse_document(file_item.path)

            if doc_node is None:
                return []

            # Create minimal context for local validators
            registry = DocumentRegistry(self.root_path)
            registry.add(doc_node)

            graph = RelationshipGraph()
            graph.add_document(doc_node)

            context = ValidationContext(registry, graph, self.root_path)

            # Run local validators only
            validator_registry = ValidatorRegistry.instance()

            for validator_cls in validator_registry.get_local_validators():
                try:
                    validator = validator_cls()
                    result = validator.validate(context)

                    for issue in result.issues:
                        # Only include issues for this file
                        if issue.file_path and issue.file_path == file_item.path:
                            severity_map = {
                                Severity.ERROR: "error",
                                Severity.WARNING: "warning",
                                Severity.INFO: "info",
                            }
                            issues.append(ValidationIssue(
                                severity=severity_map.get(issue.severity, "info"),
                                code=issue.code,
                                message=issue.message,
                                line_number=issue.line_number,
                                validator_name=validator.name,
                                suggestion=issue.suggestion,
                            ))
                except Exception:
                    continue

        except Exception:
            pass

        return issues

    def run_full_validation(self) -> dict:
        """Run full validation on all files.

        Returns:
            Dictionary with validation report data
        """
        if not self._ensure_pipeline():
            return {"error": "Validator not available"}

        try:
            report = self._pipeline.run()

            return {
                "total_files": report.total_files_scanned,
                "total_errors": report.total_errors,
                "total_warnings": report.total_warnings,
                "total_infos": report.total_infos,
                "passed": report.passed,
                "duration_ms": report.total_duration_ms,
                "issues_by_file": {
                    str(path): [
                        {
                            "severity": issue.severity.value,
                            "code": issue.code,
                            "message": issue.message,
                            "line_number": issue.line_number,
                        }
                        for issue in issues
                    ]
                    for path, issues in report.get_issues_by_file().items()
                }
            }
        except Exception as e:
            return {"error": str(e)}

    def get_validator_names(self) -> list[str]:
        """Get list of available validator names.

        Returns:
            List of validator names
        """
        if not self._available:
            return []

        try:
            from carf_validator.validators.registry import ValidatorRegistry
            registry = ValidatorRegistry.instance()
            return registry.get_validator_names()
        except Exception:
            return []
