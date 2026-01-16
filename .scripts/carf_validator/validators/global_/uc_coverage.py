"""Validador de cobertura de Use Cases."""

import re
from typing import List, Set, Dict

from ..base import GlobalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, ValidatorResult, Severity
from ...context.queries import ValidationContext


@validator
class UCCoverageValidator(GlobalValidator):
    """Valida que Use Cases com modules estão implementados em FEATURES."""

    name = "uc_coverage"
    description = "Verifica que Use Cases são implementados nos módulos declarados"

    # Padrão para identificador UC
    UC_PATTERN = re.compile(r'UC-\d{3}')

    def validate(self, context: ValidationContext) -> ValidatorResult:
        issues: List[ValidationIssue] = []

        # Coleta todos os UC com seus modules
        uc_modules: Dict[str, Set[str]] = {}  # UC-XXX -> {GEOWEB, GEOAPI, ...}
        uc_docs = context.get_by_type(DocumentType.UC)

        for doc in uc_docs:
            identifier = self._extract_identifier(doc.path.stem)
            if identifier and doc.frontmatter.modules:
                uc_modules[identifier] = set(doc.frontmatter.modules)

        # Coleta UCs mencionados em FEATURES por módulo
        covered_uc_by_module: Dict[str, Set[str]] = {}  # MODULE -> {UC-001, UC-002}
        feature_docs = context.get_by_type(DocumentType.FEATURE)

        for doc in feature_docs:
            # Determina módulo da feature pelo path
            module = self._get_module_from_path(doc.relative_path)
            if not module:
                continue

            if module not in covered_uc_by_module:
                covered_uc_by_module[module] = set()

            # Busca menções a UC-XXX no conteúdo
            matches = self.UC_PATTERN.findall(doc.content)
            covered_uc_by_module[module].update(matches)

        # Verifica cobertura de cada UC por módulo
        for uc_id, modules in uc_modules.items():
            for module in modules:
                covered_in_module = covered_uc_by_module.get(module, set())

                if uc_id not in covered_in_module:
                    # Encontra documento UC
                    uc_doc = None
                    for doc in uc_docs:
                        if uc_id in doc.path.stem:
                            uc_doc = doc
                            break

                    issues.append(ValidationIssue(
                        severity=Severity.INFO,
                        code="UCCOV001",
                        message=f"{uc_id} declara módulo {module} mas não é mencionado em features desse módulo",
                        file_path=uc_doc.path if uc_doc else None,
                        suggestion=f"Adicione referência a {uc_id} em FEATURES de PROJECTS/{module}",
                    ))

        return ValidatorResult(
            validator_name=self.name,
            issues=issues,
            stats={
                "total_ucs": len(uc_modules),
                "total_module_mappings": sum(len(m) for m in uc_modules.values()),
                "missing_implementations": len(issues),
            }
        )

    def _extract_identifier(self, stem: str) -> str | None:
        """Extrai identificador UC-XXX do nome do arquivo."""
        match = self.UC_PATTERN.search(stem)
        return match.group(0) if match else None

    def _get_module_from_path(self, relative_path: str) -> str | None:
        """Extrai nome do módulo do path (PROJECTS/MODULE/...)."""
        if not relative_path.startswith('PROJECTS/'):
            return None

        parts = relative_path.split('/')
        if len(parts) >= 2:
            return parts[1]

        return None
