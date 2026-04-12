"""Validador de densidade de conteúdo (parágrafos densos)."""

import re
from typing import List, Dict, Tuple

from ..base import LocalValidator
from ..registry import validator
from ...models.base import DocumentType
from ...models.results import ValidationIssue, Severity
from ...context.queries import ValidationContext
from ...scanner.tree import DocumentNode


@validator
class DensityValidator(LocalValidator):
    """Valida densidade de conteúdo: caracteres mínimos, parágrafos, palavras por sentença."""

    name = "density"
    description = "Valida densidade de parágrafos conforme arquitetura granular"

    # Regras de densidade por tipo
    DENSITY_RULES: Dict[DocumentType, Dict] = {
        DocumentType.RF: {
            "min_chars": 800,
            "max_paragraphs": 2,
            "words_per_sentence": (20, 50),
            "min_sentences": 2,
        },
        DocumentType.US: {
            "min_chars": 1000,
            "max_paragraphs": 2,
            "words_per_sentence": (25, 60),
            "min_sentences": 3,
        },
        DocumentType.ENTITY: {
            "min_chars": 1500,
            "max_paragraphs": 2,
            "words_per_sentence": (35, 100),
            "min_sentences": 2,
        },
        DocumentType.BUSINESS_RULE: {
            "min_chars": 800,
            "max_paragraphs": 3,
            "words_per_sentence": (15, 45),
            "min_sentences": 3,
        },
        DocumentType.UC: {
            "min_chars": 600,
            "max_paragraphs": 3,
            "words_per_sentence": (20, 50),
            "min_sentences": 2,
        },
    }

    # Seções de footer que não contam como parágrafos de conteúdo
    FOOTER_SECTIONS = [
        r"\*\*Fluxos Alternativos:\*\*",
        r"\*\*Fluxos de Exceção:\*\*",
        r"\*\*Regras de Negócio:\*\*",
        r"\*\*Rastreabilidade:\*\*",
        r"\*\*Critérios[^:]*:\*\*",
        r"\*\*Relacionado[^:]*:\*\*",
        r"\*\*Módulos:\*\*",
        r"\*\*Pré-condições:\*\*",
        r"\*\*Pós-condições:\*\*",
        r"\*\*Última atualização:\*\*",
        r"\*\*Status[^:]*:\*\*",
        r"\*\*Data:\*\*",
        r"\*\*Decisor:\*\*",
    ]

    def validate_document(
        self, doc: DocumentNode, context: ValidationContext
    ) -> List[ValidationIssue]:
        issues = []

        rules = self.DENSITY_RULES.get(doc.doc_type)
        if not rules:
            return issues

        # Extrai conteúdo principal (sem frontmatter, sem footer sections)
        main_content = self._extract_main_content(doc.content)

        # Valida caracteres mínimos
        char_count = len(main_content.strip())
        min_chars = rules["min_chars"]
        if char_count < min_chars:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="DENS001",
                message=f"Conteúdo principal muito curto: {char_count} caracteres (mínimo: {min_chars})",
                file_path=doc.path,
                suggestion=f"Expanda o conteúdo com mais {min_chars - char_count} caracteres",
            ))

        # Valida número de parágrafos
        paragraphs = self._count_content_paragraphs(main_content)
        max_paragraphs = rules["max_paragraphs"]
        if paragraphs > max_paragraphs:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="DENS002",
                message=f"Muitos parágrafos: {paragraphs} (máximo: {max_paragraphs})",
                file_path=doc.path,
                suggestion="Consolide em parágrafos densos conectados por vírgulas",
            ))

        # Valida densidade de sentenças
        sentences = self._analyze_sentences(main_content)
        if sentences:
            min_words, max_words = rules["words_per_sentence"]
            short_sentences = [s for s in sentences if s[0] < min_words]

            if len(short_sentences) > len(sentences) * 0.3:  # >30% curtas
                issues.append(ValidationIssue(
                    severity=Severity.INFO,
                    code="DENS003",
                    message=f"Muitas sentenças curtas ({len(short_sentences)}/{len(sentences)})",
                    file_path=doc.path,
                    suggestion=f"Prefira sentenças com {min_words}-{max_words} palavras conectadas por vírgulas",
                ))

        # Valida mínimo de sentenças
        min_sentences = rules["min_sentences"]
        if len(sentences) < min_sentences:
            issues.append(ValidationIssue(
                severity=Severity.WARNING,
                code="DENS004",
                message=f"Poucas sentenças: {len(sentences)} (mínimo: {min_sentences})",
                file_path=doc.path,
                suggestion=f"Adicione mais conteúdo descritivo com pelo menos {min_sentences} sentenças",
            ))

        return issues

    def _extract_main_content(self, content: str) -> str:
        """Extrai conteúdo principal removendo frontmatter e footers."""
        # Remove frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Remove título H1
        content = re.sub(r'^#\s+[^\n]+\n', '', content)

        # Remove seções de footer
        for pattern in self.FOOTER_SECTIONS:
            content = re.sub(pattern + r'.*$', '', content, flags=re.DOTALL | re.MULTILINE)

        # Remove separador de footer
        content = re.sub(r'\n---\n.*$', '', content, flags=re.DOTALL)

        # Remove blocos de código
        content = re.sub(r'```[\s\S]*?```', '', content)

        # Remove links de navegação
        content = re.sub(r'^\s*\[.*?\]\(.*?\)\s*$', '', content, flags=re.MULTILINE)

        return content.strip()

    def _count_content_paragraphs(self, content: str) -> int:
        """Conta parágrafos de conteúdo (blocos separados por linha em branco)."""
        # Split por linhas em branco
        blocks = re.split(r'\n\s*\n', content)

        # Filtra blocos vazios e muito curtos
        paragraphs = [b.strip() for b in blocks if b.strip() and len(b.strip()) > 50]

        return len(paragraphs)

    def _analyze_sentences(self, content: str) -> List[Tuple[int, str]]:
        """Analisa sentenças e retorna lista de (word_count, sentence)."""
        # Remove código inline
        content = re.sub(r'`[^`]+`', '', content)

        # Split por terminadores de sentença
        sentences = re.split(r'[.!?]+\s+', content)

        result = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 20:  # Ignora fragmentos
                words = len(sentence.split())
                result.append((words, sentence[:80]))

        return result
