"""Parser de frontmatter YAML."""

import re
from typing import Optional, Tuple, List

from ...models.base import Frontmatter

# Padrão para frontmatter YAML entre ---
FRONTMATTER_PATTERN = re.compile(r'^---\n(.*?)\n---', re.DOTALL)

# Padrão para campo modules: [X, Y, Z]
MODULES_PATTERN = re.compile(r'modules:\s*\[(.*?)\]', re.DOTALL)

# Padrão para campo epic: value
EPIC_PATTERN = re.compile(r'epic:\s*(.+)')


def parse_frontmatter(content: str) -> Tuple[Optional[Frontmatter], str]:
    """
    Extrai frontmatter YAML do conteúdo markdown.

    Args:
        content: Conteúdo completo do arquivo markdown

    Returns:
        Tuple de (objeto Frontmatter ou None, conteúdo sem frontmatter)
    """
    match = FRONTMATTER_PATTERN.search(content)
    if not match:
        return None, content

    frontmatter_text = match.group(1)
    remaining_content = content[match.end():].strip()

    # Parse modules
    modules = _parse_modules(frontmatter_text)

    # Parse epic
    epic = _parse_epic(frontmatter_text)

    # Parse raw (todos os campos)
    raw = _parse_raw_fields(frontmatter_text)

    return Frontmatter(modules=modules, epic=epic, raw=raw), remaining_content


def _parse_modules(frontmatter_text: str) -> List[str]:
    """Extrai lista de módulos do frontmatter."""
    modules_match = MODULES_PATTERN.search(frontmatter_text)
    if not modules_match:
        return []

    modules_str = modules_match.group(1)
    # Limpa e separa módulos
    modules = [
        m.strip().strip('"\'')
        for m in modules_str.split(',')
        if m.strip()
    ]
    return modules


def _parse_epic(frontmatter_text: str) -> Optional[str]:
    """Extrai epic do frontmatter."""
    epic_match = EPIC_PATTERN.search(frontmatter_text)
    if epic_match:
        return epic_match.group(1).strip()
    return None


def _parse_raw_fields(frontmatter_text: str) -> dict:
    """Extrai todos os campos do frontmatter como dicionário."""
    raw = {}
    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if ':' in line and not line.startswith('#'):
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Tenta converter listas
            if value.startswith('[') and value.endswith(']'):
                # É uma lista
                list_content = value[1:-1]
                raw[key] = [
                    item.strip().strip('"\'')
                    for item in list_content.split(',')
                    if item.strip()
                ]
            else:
                raw[key] = value

    return raw
