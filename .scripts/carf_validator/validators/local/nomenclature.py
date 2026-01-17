"""Validador de nomenclatura técnica consistente."""

import re
from typing import List, Dict

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class NomenclatureValidator(LocalValidator):
    """Valida uso consistente de terminologia técnica."""

    name = "nomenclature"
    description = "Valida uso consistente de termos técnicos"

    # Regras de nomenclatura: padrão incorreto -> correção
    NOMENCLATURE_RULES: Dict[str, Dict[str, str]] = {
        r"REURB[^-SE\s]": {
            "message": "REURB deve ser qualificado como REURB-S ou REURB-E",
            "correct": "REURB-S (social) ou REURB-E (econômico)",
        },
        r"\bPostgres\b": {
            "message": "Use 'PostgreSQL' ao invés de 'Postgres'",
            "correct": "PostgreSQL",
        },
        r"\bKeyCloak\b": {
            "message": "Use 'Keycloak' ao invés de 'KeyCloak'",
            "correct": "Keycloak",
        },
        r"\breact-native\b": {
            "message": "Use 'React Native' ao invés de 'react-native' em prosa",
            "correct": "React Native",
        },
        r"\bDotNet\b": {
            "message": "Use '.NET' ao invés de 'DotNet'",
            "correct": ".NET",
        },
        r"\bNodejs\b": {
            "message": "Use 'Node.js' ao invés de 'Nodejs'",
            "correct": "Node.js",
        },
        r"\bTypescript\b": {
            "message": "Use 'TypeScript' ao invés de 'Typescript'",
            "correct": "TypeScript",
        },
        r"\bJavascript\b": {
            "message": "Use 'JavaScript' ao invés de 'Javascript'",
            "correct": "JavaScript",
        },
        r"\bPostgis\b": {
            "message": "Use 'PostGIS' ao invés de 'Postgis'",
            "correct": "PostGIS",
        },
    }

    # Tipos de documento a verificar
    APPLICABLE_TYPES = {
        DocumentType.README,
        DocumentType.RF,
        DocumentType.RNF,
        DocumentType.US,
        DocumentType.UC,
        DocumentType.ENTITY,
        DocumentType.FEATURE,
        DocumentType.BUSINESS_RULE,
        DocumentType.WORKFLOW,
        DocumentType.CONCEPT,
        DocumentType.HOW_TO,
    }

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        # Pula ADRs (podem ter convenções próprias)
        if doc.doc_type == DocumentType.ADR:
            return issues

        if doc.doc_type not in self.APPLICABLE_TYPES:
            return issues

        content = doc.content

        # Remove blocos de código para não validar código
        content_clean = re.sub(r'```[\s\S]*?```', '', content)
        content_clean = re.sub(r'`[^`]+`', '', content_clean)

        for pattern, rule in self.NOMENCLATURE_RULES.items():
            matches = list(re.finditer(pattern, content_clean))

            for match in matches:
                # Encontra número da linha
                line_num = content[:match.start()].count('\n') + 1

                # Pega contexto
                start = max(0, match.start() - 25)
                end = min(len(content), match.end() + 25)
                context_text = content[start:end].replace('\n', ' ')

                issues.append(ValidationIssue(
                    severity=Severity.WARNING,
                    code="NOMEN001",
                    message=rule["message"],
                    file_path=doc.path,
                    line_number=line_num,
                    context=f"...{context_text}...",
                    suggestion=f"Use: {rule['correct']}",
                ))

        return issues
