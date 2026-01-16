"""Parser de seções e análise de conteúdo."""

import re
from typing import List, Tuple
from dataclasses import dataclass


@dataclass
class ContentAnalysis:
    """Resultado da análise de conteúdo."""
    body: str
    char_count: int
    word_count: int
    paragraph_count: int
    sentence_count: int
    avg_words_per_sentence: float
    bullet_count: int
    bullet_lines: List[int]
    short_sentences: List[Tuple[int, str]]


def extract_content_body(content: str) -> str:
    """
    Extrai corpo do conteúdo removendo frontmatter e footer.

    Args:
        content: Conteúdo completo

    Returns:
        Corpo do conteúdo sem frontmatter e footer
    """
    body = content

    # Remove frontmatter
    frontmatter_match = re.match(r'^---\n.*?\n---\n', body, re.DOTALL)
    if frontmatter_match:
        body = body[frontmatter_match.end():]

    # Remove footer (tudo após último ---)
    footer_match = re.search(r'\n---\n\s*\*\*(?:Última atualização|Versão).*$', body, re.DOTALL)
    if footer_match:
        body = body[:footer_match.start()]

    return body.strip()


def count_paragraphs(content: str) -> int:
    """
    Conta parágrafos no conteúdo.

    Args:
        content: Conteúdo a analisar

    Returns:
        Número de parágrafos
    """
    body = extract_content_body(content)

    # Remove título H1
    body = re.sub(r'^#\s+.+\n\n?', '', body)

    # Remove seções de footer (Fluxos, Regras, etc.)
    body = re.sub(r'\*\*(?:Fluxos|Regras|Rastreabilidade|Módulos|Relacionado)[^*]*\*\*:.*$',
                  '', body, flags=re.DOTALL | re.MULTILINE)

    if not body.strip():
        return 0

    # Split por linhas em branco duplas
    paragraphs = re.split(r'\n\s*\n', body.strip())
    # Filtra parágrafos vazios e headers
    paragraphs = [p for p in paragraphs if p.strip() and not p.strip().startswith('#')]

    return len(paragraphs)


def analyze_sentences(content: str) -> Tuple[int, float, List[Tuple[int, str]]]:
    """
    Analisa sentenças no conteúdo.

    Args:
        content: Conteúdo a analisar

    Returns:
        Tuple de (contagem, média palavras/sentença, sentenças curtas)
    """
    body = extract_content_body(content)

    # Remove código
    body = re.sub(r'```[\s\S]*?```', '', body)
    body = re.sub(r'`[^`]+`', '', body)

    # Remove título H1
    body = re.sub(r'^#\s+.+\n', '', body)

    # Remove headers
    body = re.sub(r'^##?\s+.+$', '', body, flags=re.MULTILINE)

    # Remove bullets
    body = re.sub(r'^\s*[-*+]\s+', '', body, flags=re.MULTILINE)

    if not body.strip():
        return 0, 0.0, []

    # Split por sentenças
    sentences = re.split(r'[.!?]+', body)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not sentences:
        return 0, 0.0, []

    # Calcula palavras por sentença
    word_counts = [len(s.split()) for s in sentences]
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0

    # Encontra sentenças curtas (<10 palavras)
    short_sentences = []
    lines = content.split('\n')
    for i, (sentence, wc) in enumerate(zip(sentences, word_counts)):
        if wc < 10 and wc > 0:
            # Encontra linha
            for line_num, line in enumerate(lines, 1):
                if sentence[:30] in line:
                    short_sentences.append((line_num, sentence[:50]))
                    break

    return len(sentences), avg_words, short_sentences


def count_bullets(content: str) -> Tuple[int, List[int]]:
    """
    Conta linhas com bullets no conteúdo.

    Args:
        content: Conteúdo a analisar

    Returns:
        Tuple de (contagem, lista de números de linha)
    """
    lines = content.split('\n')
    bullet_lines = []

    for i, line in enumerate(lines, 1):
        if re.match(r'^\s*[-*+]\s+', line):
            bullet_lines.append(i)

    return len(bullet_lines), bullet_lines


def find_bullets_in_content(content: str) -> List[Tuple[int, str]]:
    """
    Encontra bullets que estão no conteúdo principal (não em seções de footer).

    Args:
        content: Conteúdo do documento

    Returns:
        Lista de (linha, texto) para bullets no conteúdo principal
    """
    lines = content.split('\n')
    bullets_in_content = []

    # Seções onde bullets são permitidos
    allowed_sections = [
        r'\*\*Fluxos Alternativos:?\*\*',
        r'\*\*Fluxos de Exceção:?\*\*',
        r'\*\*Regras de Negócio:?\*\*',
        r'\*\*Rastreabilidade:?\*\*',
        r'\*\*Critérios[^*]*:?\*\*',
        r'\*\*Relacionado[^*]*:?\*\*',
        r'\*\*Módulos:?\*\*',
        r'## Estrutura',
        r'## Aplicações',
        r'## Bibliotecas',
        r'## Domínios',
    ]

    in_allowed_section = False

    for i, line in enumerate(lines, 1):
        # Verifica se entramos em seção permitida
        for pattern in allowed_sections:
            if re.search(pattern, line):
                in_allowed_section = True
                break

        # Verifica se é um novo header (sai de seção permitida)
        if re.match(r'^##?\s+', line) and not any(re.search(p, line) for p in allowed_sections):
            in_allowed_section = False

        # Se é bullet e não está em seção permitida
        if re.match(r'^\s*[-*+]\s+', line) and not in_allowed_section:
            bullets_in_content.append((i, line.strip()))

    return bullets_in_content


def analyze_content(content: str) -> ContentAnalysis:
    """
    Análise completa do conteúdo.

    Args:
        content: Conteúdo do documento

    Returns:
        Objeto ContentAnalysis com todas as métricas
    """
    body = extract_content_body(content)

    # Contagens básicas
    char_count = len(body)
    word_count = len(body.split())
    paragraph_count = count_paragraphs(content)

    # Análise de sentenças
    sentence_count, avg_words, short_sentences = analyze_sentences(content)

    # Contagem de bullets
    bullet_count, bullet_lines = count_bullets(content)

    return ContentAnalysis(
        body=body,
        char_count=char_count,
        word_count=word_count,
        paragraph_count=paragraph_count,
        sentence_count=sentence_count,
        avg_words_per_sentence=avg_words,
        bullet_count=bullet_count,
        bullet_lines=bullet_lines,
        short_sentences=short_sentences,
    )
