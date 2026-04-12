"""Parser de metadata do footer de documentos."""

import re
from datetime import datetime, date
from typing import Optional

from ...models.base import Metadata

# Padrões para campos de metadata
LAST_UPDATE_PATTERN = re.compile(r'\*\*Última atualização:\*\*\s*(\d{4}-\d{2}-\d{2})')
STATUS_PATTERN = re.compile(r'\*\*Status:\*\*\s*(.+)')
FILE_STATUS_PATTERN = re.compile(r'\*\*Status do arquivo\*\*:\s*(.+)')
DECISION_DATE_PATTERN = re.compile(r'\*\*Data:\*\*\s*(\d{4}-\d{2}-\d{2})')
DECIDER_PATTERN = re.compile(r'\*\*Decisor:\*\*\s*(.+)')
LAST_REVISION_PATTERN = re.compile(r'\*\*Última revisão:\*\*\s*(\d{4}-\d{2}-\d{2})')
VERSION_PATTERN = re.compile(r'\*\*Versão:\*\*\s*(.+)')
LICENSE_PATTERN = re.compile(r'\*\*Licença:\*\*\s*(.+)')


def parse_metadata(content: str) -> Metadata:
    """
    Extrai metadata do footer do documento.

    Args:
        content: Conteúdo completo do arquivo markdown

    Returns:
        Objeto Metadata com campos extraídos
    """
    metadata = Metadata()

    # Parse última atualização
    match = LAST_UPDATE_PATTERN.search(content)
    if match:
        metadata.last_update = _parse_date(match.group(1))

    # Parse status
    match = STATUS_PATTERN.search(content)
    if match:
        metadata.status = match.group(1).strip()

    # Parse status do arquivo
    match = FILE_STATUS_PATTERN.search(content)
    if match:
        metadata.file_status = match.group(1).strip()

    # Parse data (para ADRs)
    match = DECISION_DATE_PATTERN.search(content)
    if match:
        metadata.decision_date = _parse_date(match.group(1))

    # Parse decisor (para ADRs)
    match = DECIDER_PATTERN.search(content)
    if match:
        metadata.decider = match.group(1).strip()

    # Parse última revisão
    match = LAST_REVISION_PATTERN.search(content)
    if match:
        metadata.last_revision = _parse_date(match.group(1))

    # Parse versão
    match = VERSION_PATTERN.search(content)
    if match:
        metadata.version = match.group(1).strip()

    # Parse licença
    match = LICENSE_PATTERN.search(content)
    if match:
        metadata.license = match.group(1).strip()

    return metadata


def _parse_date(date_str: str) -> Optional[date]:
    """
    Converte string de data para objeto date.

    Args:
        date_str: String no formato YYYY-MM-DD

    Returns:
        Objeto date ou None se inválido
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def has_metadata_footer(content: str) -> bool:
    """
    Verifica se o documento tem footer de metadata.

    Args:
        content: Conteúdo do documento

    Returns:
        True se tiver última atualização definida
    """
    return bool(LAST_UPDATE_PATTERN.search(content))


def has_separator_before_footer(content: str) -> bool:
    """
    Verifica se tem separador --- antes do footer de metadata.

    Args:
        content: Conteúdo do documento

    Returns:
        True se tiver separador seguido de metadata
    """
    # Procura por --- seguido de metadata
    pattern = r'\n---\n+\*\*(?:Última atualização|Versão|Status)'
    return bool(re.search(pattern, content))
