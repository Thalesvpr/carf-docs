"""Parser e resolução de links Markdown."""

import re
from pathlib import Path
from typing import List, Optional

from ...models.base import Link

# Padrão para links markdown [texto](destino)
LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')


def extract_links(content: str, source_file: Path) -> List[Link]:
    """
    Extrai todos os links markdown do conteúdo.

    Args:
        content: Conteúdo do arquivo markdown
        source_file: Path do arquivo fonte

    Returns:
        Lista de objetos Link
    """
    links = []
    lines = content.split('\n')

    for line_num, line in enumerate(lines, 1):
        for match in LINK_PATTERN.finditer(line):
            text = match.group(1)
            target = match.group(2)

            # Determina se é externo
            external = is_external_link(target)

            link = Link(
                text=text,
                target=target,
                line_number=line_num,
                source_file=source_file,
                is_external=external,
            )

            # Resolve path se for interno
            if not external:
                resolved = resolve_link_path(source_file, target)
                if resolved:
                    link.resolved_path = resolved
                    link.is_valid = resolved.exists()
                    if not link.is_valid:
                        link.error_message = "arquivo não existe"
                    elif resolved.is_dir():
                        link.is_valid = False
                        link.error_message = "link aponta para diretório"

            links.append(link)

    return links


def is_external_link(link_target: str) -> bool:
    """
    Verifica se é link externo.

    Args:
        link_target: Target do link

    Returns:
        True se for externo
    """
    return (
        link_target.startswith('http://') or
        link_target.startswith('https://') or
        link_target.startswith('mailto:') or
        link_target.startswith('#') or
        link_target.startswith('tel:')
    )


def resolve_link_path(source_file: Path, link_target: str) -> Optional[Path]:
    """
    Resolve path relativo do link para path absoluto.

    Args:
        source_file: Arquivo fonte do link
        link_target: Target do link (relativo)

    Returns:
        Path absoluto resolvido ou None
    """
    # Remove âncora (#section)
    if '#' in link_target:
        link_target = link_target.split('#')[0]

    if not link_target:
        # Link só com âncora
        return None

    # Resolve caminho
    source_dir = source_file.parent
    try:
        resolved = (source_dir / link_target).resolve()
        return resolved
    except Exception:
        return None


def is_bold_link(line: str, link_text: str, link_target: str) -> bool:
    """
    Verifica se o link está em bold.

    Args:
        line: Linha contendo o link
        link_text: Texto do link
        link_target: Target do link

    Returns:
        True se link estiver em bold (**[text](target)**)
    """
    pattern = rf'\*\*\[{re.escape(link_text)}\]\({re.escape(link_target)}\)\*\*'
    return bool(re.search(pattern, line))


def is_relative_path(link_target: str) -> bool:
    """
    Verifica se é path relativo.

    Args:
        link_target: Target do link

    Returns:
        True se for path relativo
    """
    if is_external_link(link_target):
        return False

    # Verifica paths absolutos Windows (C:\, D:\, etc.)
    if re.match(r'^[A-Za-z]:\\', link_target):
        return False

    # Verifica paths absolutos Unix (/path/to/file)
    if link_target.startswith('/') and not link_target.startswith('//'):
        return False

    return True
