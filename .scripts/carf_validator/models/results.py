"""Modelos de resultados de validação."""

from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import List, Optional, Dict, Any


class Severity(Enum):
    """Níveis de severidade de validação."""
    ERROR = auto()    # Deve ser corrigido
    WARNING = auto()  # Deveria ser corrigido
    INFO = auto()     # Informacional


@dataclass
class ValidationIssue:
    """Issue única de validação encontrada."""
    severity: Severity
    code: str          # e.g., "LINK001", "META002"
    message: str
    file_path: Optional[Path] = None
    line_number: Optional[int] = None
    context: Optional[str] = None  # Texto ao redor para contexto
    suggestion: Optional[str] = None  # Como corrigir

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        return {
            "severity": self.severity.name,
            "code": self.code,
            "message": self.message,
            "file": str(self.file_path) if self.file_path else None,
            "line": self.line_number,
            "context": self.context,
            "suggestion": self.suggestion,
        }

    def __str__(self) -> str:
        """Representação string do issue."""
        parts = [f"[{self.code}] {self.message}"]
        if self.file_path:
            parts.append(f"  File: {self.file_path}")
        if self.line_number:
            parts.append(f"  Line: {self.line_number}")
        if self.suggestion:
            parts.append(f"  Fix: {self.suggestion}")
        return "\n".join(parts)


@dataclass
class ValidatorResult:
    """Resultado de execução de um validador."""
    validator_name: str
    issues: List[ValidationIssue] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)
    duration_ms: float = 0.0

    @property
    def error_count(self) -> int:
        """Conta erros."""
        return sum(1 for i in self.issues if i.severity == Severity.ERROR)

    @property
    def warning_count(self) -> int:
        """Conta warnings."""
        return sum(1 for i in self.issues if i.severity == Severity.WARNING)

    @property
    def info_count(self) -> int:
        """Conta infos."""
        return sum(1 for i in self.issues if i.severity == Severity.INFO)

    @property
    def has_errors(self) -> bool:
        """Verifica se tem erros."""
        return self.error_count > 0

    @property
    def has_warnings(self) -> bool:
        """Verifica se tem warnings."""
        return self.warning_count > 0

    def add_error(self, code: str, message: str, **kwargs) -> None:
        """Adiciona um erro."""
        self.issues.append(ValidationIssue(
            severity=Severity.ERROR,
            code=code,
            message=message,
            **kwargs
        ))

    def add_warning(self, code: str, message: str, **kwargs) -> None:
        """Adiciona um warning."""
        self.issues.append(ValidationIssue(
            severity=Severity.WARNING,
            code=code,
            message=message,
            **kwargs
        ))

    def add_info(self, code: str, message: str, **kwargs) -> None:
        """Adiciona uma info."""
        self.issues.append(ValidationIssue(
            severity=Severity.INFO,
            code=code,
            message=message,
            **kwargs
        ))


@dataclass
class ValidationReport:
    """Relatório completo de validação de todos os validadores."""
    results: List[ValidatorResult] = field(default_factory=list)
    total_files_scanned: int = 0
    scan_duration_ms: float = 0.0
    validation_duration_ms: float = 0.0

    @property
    def total_errors(self) -> int:
        """Total de erros."""
        return sum(r.error_count for r in self.results)

    @property
    def total_warnings(self) -> int:
        """Total de warnings."""
        return sum(r.warning_count for r in self.results)

    @property
    def total_infos(self) -> int:
        """Total de infos."""
        return sum(r.info_count for r in self.results)

    @property
    def passed(self) -> bool:
        """Verifica se passou (sem erros)."""
        return self.total_errors == 0

    @property
    def total_duration_ms(self) -> float:
        """Duração total."""
        return self.scan_duration_ms + self.validation_duration_ms

    def get_all_issues(self) -> List[ValidationIssue]:
        """Retorna todos os issues de todos os validadores."""
        all_issues = []
        for result in self.results:
            all_issues.extend(result.issues)
        return all_issues

    def get_issues_by_file(self) -> Dict[Path, List[ValidationIssue]]:
        """Agrupa issues por arquivo."""
        by_file: Dict[Path, List[ValidationIssue]] = {}
        for issue in self.get_all_issues():
            if issue.file_path:
                if issue.file_path not in by_file:
                    by_file[issue.file_path] = []
                by_file[issue.file_path].append(issue)
        return by_file

    @property
    def totals(self) -> Dict[str, int]:
        """Retorna totais como dicionário."""
        return {
            "files_scanned": self.total_files_scanned,
            "errors": self.total_errors,
            "warnings": self.total_warnings,
            "info": self.total_infos,
        }
