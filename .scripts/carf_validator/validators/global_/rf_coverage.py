"""Validador de cobertura de Requisitos Funcionais."""

import re
from typing import List, Set

from ..base import GlobalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class RFCoverageValidator(GlobalValidator):
    """Valida que todos os RF estão cobertos por FEATURES."""

    name = "rf_coverage"
    description = "Verifica que Requisitos Funcionais são implementados em Features"

    # Padrão para identificador RF
    RF_PATTERN = re.compile(r'RF-\d{3}')

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        # Coleta todos os RF
        all_rfs: Set[str] = set()
        rf_docs = context.get_by_type(DocumentType.RF)

        for doc in rf_docs:
            identifier = self._extract_identifier(doc.path.stem)
            if identifier:
                all_rfs.add(identifier)

        # Coleta RFs mencionados em FEATURES
        covered_rfs: Set[str] = set()
        feature_docs = context.get_by_type(DocumentType.FEATURE)

        for doc in feature_docs:
            # Busca menções a RF-XXX no conteúdo
            matches = self.RF_PATTERN.findall(doc.content)
            covered_rfs.update(matches)

            # Busca também no frontmatter (se tiver campo rf ou requirements)
            if doc.frontmatter.raw:
                raw_str = str(doc.frontmatter.raw)
                matches = self.RF_PATTERN.findall(raw_str)
                covered_rfs.update(matches)

        # Identifica RFs não cobertos
        uncovered = all_rfs - covered_rfs

        for rf_id in sorted(uncovered):
            # Encontra o documento RF
            rf_doc = None
            for doc in rf_docs:
                if rf_id in doc.path.stem:
                    rf_doc = doc
                    break

            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="RFCOV001",
                message=f"RF sem cobertura em FEATURES: {rf_id}",
                file_path=rf_doc.path if rf_doc else None,
                suggestion=f"Adicione referência a {rf_id} em documento FEATURE correspondente",
            ))

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "total_rfs": len(all_rfs),
                "covered_rfs": len(covered_rfs),
                "uncovered_rfs": len(uncovered),
                "coverage_percent": (
                    round(len(covered_rfs) / len(all_rfs) * 100, 1)
                    if all_rfs else 100
                ),
            }
        )

    def _extract_identifier(self, stem: str) -> str | None:
        """Extrai identificador RF-XXX do nome do arquivo."""
        match = self.RF_PATTERN.search(stem)
        return match.group(0) if match else None
