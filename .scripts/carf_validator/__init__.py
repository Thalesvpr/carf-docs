"""
CARF Validator - Sistema de validação estrutural e semântica.

Pipeline: scan -> modeling -> context -> validation -> report
"""

from typing import List, Optional, Set
from pathlib import Path

from .models.base import DocumentType
from .models.results import ValidationReport, ValidatorResult, Severity
from .scanner.traversal import FileScanner, ScanConfig
from .scanner.tree import DocumentTreeBuilder
from .context.registry import DocumentRegistry
from .context.graph import RelationshipGraph
from .context.queries import ValidationContext
from .validators.registry import ValidatorRegistry
from .validators.base import LocalValidator, GlobalValidator
from .reporters.base import BaseReporter
from .reporters.console import ConsoleReporter
from .reporters.markdown import MarkdownReporter
from .reporters.json import JsonReporter


class ValidationPipeline:
    """Pipeline principal de validação CARF."""

    def __init__(
        self,
        root_path: Path,
        enabled_validators: Optional[Set[str]] = None,
        disabled_validators: Optional[Set[str]] = None,
    ):
        """
        Inicializa pipeline de validação.

        Args:
            root_path: Diretório raiz do repositório CARF
            enabled_validators: Se definido, apenas estes validadores rodam
            disabled_validators: Validadores a desabilitar
        """
        self.root_path = root_path.resolve()
        self.enabled_validators = enabled_validators
        self.disabled_validators = disabled_validators or set()

        # Componentes (inicializados em run())
        self._documents = {}
        self._registry = None
        self._graph = None
        self._context = None

    def run(self) -> ValidationReport:
        """
        Executa pipeline completo de validação.

        Returns:
            ValidationReport com todos os resultados
        """
        # Fase 1: Scan - varredura de arquivos
        self._scan()

        # Fase 2: Context - construção de índices e grafo
        self._build_context()

        # Fase 3: Validate - execução de validadores
        results = self._validate()

        # Fase 4: Report - consolidação de resultados
        report = self._build_report(results)

        return report

    def _scan(self) -> None:
        """Fase 1: Varredura e parsing de documentos."""
        config = ScanConfig(
            root_dir=self.root_path,
            include_patterns=["**/*.md"],
            exclude_dirs={
                ".git",
                ".obsidian",
                ".scripts",
                ".vscode",
                "node_modules",
                "__pycache__",
                ".validation-reports",
            }
        )

        scanner = FileScanner(config)
        builder = DocumentTreeBuilder(self.root_path)

        for file_path in scanner.scan():
            doc = builder._parse_document(file_path)
            if doc:
                self._documents[file_path] = doc

    def _build_context(self) -> None:
        """Fase 2: Construção de registry e grafo de relacionamentos."""
        # Registry - índices de documentos
        self._registry = DocumentRegistry()
        for doc in self._documents.values():
            self._registry.register(doc)

        # Graph - relacionamentos
        self._graph = RelationshipGraph(self._registry, self.root_path)
        self._graph.build()

        # Context - interface unificada para validadores
        self._context = ValidationContext(
            registry=self._registry,
            graph=self._graph,
            root_dir=self.root_path,
        )

    def _validate(self) -> List[ValidatorResult]:
        """Fase 3: Execução de validadores."""
        results = []
        registry = ValidatorRegistry.instance()

        # Filtra validadores habilitados (classes)
        validator_classes = registry.get_all()
        if self.enabled_validators:
            validator_classes = [v for v in validator_classes if v.name in self.enabled_validators]
        validator_classes = [v for v in validator_classes if v.name not in self.disabled_validators]

        # Instancia e executa validadores
        for validator_cls in validator_classes:
            validator = validator_cls()  # Instancia a classe

            if isinstance(validator, LocalValidator):
                # Validador local - usa método validate da classe base
                result = validator.validate(self._context)
                results.append(result)
            elif isinstance(validator, GlobalValidator):
                # Validador global
                result = validator.validate(self._context)
                results.append(result)

        return results

    def _build_report(self, results: List[ValidatorResult]) -> ValidationReport:
        """Fase 4: Consolidação de resultados."""
        return ValidationReport(
            results=results,
            total_files_scanned=len(self._documents),
        )


def get_reporter(format_name: str) -> BaseReporter:
    """Factory para obter reporter pelo nome."""
    reporters = {
        "console": ConsoleReporter,
        "markdown": MarkdownReporter,
        "json": JsonReporter,
    }
    reporter_cls = reporters.get(format_name, ConsoleReporter)
    return reporter_cls()


__all__ = [
    "ValidationPipeline",
    "get_reporter",
    "ValidationReport",
    "ValidatorResult",
    "Severity",
]
