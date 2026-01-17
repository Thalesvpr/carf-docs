"""Validador de estrutura de seções obrigatórias."""

import re
from typing import List, Dict

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class StructureValidator(LocalValidator):
    """Valida seções obrigatórias por tipo de documento."""

    name = "structure"
    description = "Valida estrutura de seções obrigatórias por tipo de documento"

    # Regras de estrutura por tipo
    STRUCTURE_RULES: Dict[DocumentType, Dict] = {
        DocumentType.UC: {
            "required_sections": [
                r"##\s+Regras de Negócio",
                r"##\s+Rastreabilidade",
            ],
        },
        DocumentType.RF: {
            "required_sections": [
                r"##\s+Critérios de Aceitação",
            ],
        },
        DocumentType.US: {
            "required_phrases": ["Como ", "quero ", "para que "],
        },
        DocumentType.FEATURE: {
            "required_sections": [
                r"##\s+(?:Validações|Validation)",
                r"##\s+(?:API Integration|Integração API)",
                r"##\s+(?:Relacionamentos|Domain Model)",
            ],
        },
        DocumentType.HOW_TO: {
            "required_sections": [
                r"##\s+Pré-requisitos",
                r"##\s+Passos",
            ],
        },
    }

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        rules = self.STRUCTURE_RULES.get(doc.doc_type)
        if not rules:
            return issues

        content = doc.content

        # Valida seções obrigatórias
        if "required_sections" in rules:
            for section_pattern in rules["required_sections"]:
                if not re.search(section_pattern, content, re.IGNORECASE):
                    issues.append(ValidationIssue(
                        severity=Severity.ERROR,
                        code="STRUCT001",
                        message=f"Seção obrigatória ausente: {section_pattern}",
                        file_path=doc.path,
                        suggestion=f"Adicione a seção correspondente ao padrão",
                    ))

        # Valida frases obrigatórias
        if "required_phrases" in rules:
            for phrase in rules["required_phrases"]:
                if phrase.lower() not in content.lower():
                    issues.append(ValidationIssue(
                        severity=Severity.WARNING,
                        code="STRUCT002",
                        message=f"Frase obrigatória ausente: '{phrase}'",
                        file_path=doc.path,
                        suggestion=f"Use o padrão 'Como [role], quero [feature], para que [benefit]'",
                    ))

        return issues
