#!/usr/bin/env python3
"""Script para padronizar metadados em todos os arquivos markdown."""

import re
from pathlib import Path
from datetime import date


# Diretórios a ignorar
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".obsidian", ".scripts", "data"}


def extract_metadata(content: str) -> dict:
    """Extrai metadados existentes do conteúdo."""
    metadata = {
        "status": "Review",
        "updated": date.today().isoformat(),
        "description": "",
    }

    # Padrões para extrair valores
    patterns = [
        (r"\*\*Status do arquivo\*\*\s*:\s*(.+)", "status"),
        (r"\*\*Status\*\*\s*:\s*(.+)", "status"),
        (r"\*\*Última atualização\*\*\s*:\s*(.+)", "updated"),
        (r"\*\*Atualizado\*\*\s*:\s*(.+)", "updated"),
        (r"\*\*Descrição\*\*\s*:\s*(.+)", "description"),
    ]

    for pattern, key in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = match.group(1).strip()
            if value:
                metadata[key] = value

    return metadata


def remove_metadata_section(content: str) -> str:
    """Remove a seção de metadados do final do arquivo.

    Procura pela última ocorrência de '---' seguida de linhas **Key:** Value
    e remove tudo dali pra frente.
    """
    # Encontra a última ocorrência de --- seguida por metadados até o fim
    # Usa [\s\S]* para capturar tudo incluindo newlines
    pattern = re.compile(r'\n---\n[\s\S]*$')

    # Verifica se o que vem depois do --- são só metadados
    match = pattern.search(content)
    if match:
        after_separator = match.group()[5:]  # Pula '\n---\n'
        # Verifica se são só linhas vazias e **Key:** Value
        lines = after_separator.strip().split('\n')
        is_metadata = all(
            line.strip() == '' or
            line.strip() == '---' or
            re.match(r'\*\*[^*]+[:\*]+', line.strip())
            for line in lines
        )
        if is_metadata:
            return content[:match.start()].rstrip()

    return content.rstrip()


def create_metadata_section(metadata: dict) -> str:
    """Cria a seção de metadados padronizada."""
    return f"""

---

**Status:** {metadata['status']}
**Atualizado:** {metadata['updated']}
**Descrição:** {metadata['description']}
"""


def process_file(file_path: Path, dry_run: bool = False) -> dict:
    """Processa um arquivo markdown."""
    result = {
        "path": str(file_path),
        "action": "skipped",
        "metadata": {},
    }

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        result["action"] = "error"
        result["error"] = str(e)
        return result

    # Extrai metadados existentes
    metadata = extract_metadata(content)
    result["metadata"] = metadata

    # Remove metadados antigos
    clean_content = remove_metadata_section(content)

    # Cria nova seção de metadados
    new_metadata = create_metadata_section(metadata)

    # Novo conteúdo
    new_content = clean_content + new_metadata

    # Verifica se mudou
    if content.rstrip() == new_content.rstrip():
        result["action"] = "unchanged"
        return result

    if not dry_run:
        file_path.write_text(new_content, encoding="utf-8")
        result["action"] = "updated"
    else:
        result["action"] = "would_update"

    return result


def scan_files(root: Path) -> list[Path]:
    """Escaneia todos os arquivos markdown."""
    files = []

    for item in root.rglob("*.md"):
        # Ignora diretórios especiais
        if any(ignored in item.parts for ignored in IGNORE_DIRS):
            continue

        files.append(item)

    return sorted(files)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Padroniza metadados em arquivos markdown"
    )
    parser.add_argument(
        "root",
        type=Path,
        nargs="?",
        default=Path.cwd(),
        help="Diretório raiz (default: atual)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra o que seria feito sem modificar"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostra detalhes"
    )
    parser.add_argument(
        "--file", "-f",
        type=Path,
        help="Processa apenas um arquivo específico"
    )

    args = parser.parse_args()

    if args.file:
        # Processa um único arquivo
        result = process_file(args.file, dry_run=args.dry_run)
        print(f"[{result['action']}] {args.file}")
        if args.verbose:
            print(f"  Metadata: {result['metadata']}")
        return

    root = args.root.resolve()
    print(f"Escaneando: {root}")

    files = scan_files(root)
    print(f"Encontrados: {len(files)} arquivos .md")

    stats = {"updated": 0, "unchanged": 0, "error": 0, "would_update": 0}

    for file_path in files:
        result = process_file(file_path, dry_run=args.dry_run)
        stats[result["action"]] = stats.get(result["action"], 0) + 1

        if args.verbose or result["action"] in ("updated", "would_update", "error"):
            rel_path = file_path.relative_to(root)
            print(f"  [{result['action']:12}] {rel_path}")
            if result.get("error"):
                print(f"               Error: {result['error']}")

    print()
    print("Resumo:")
    if args.dry_run:
        print(f"  Seria atualizado: {stats.get('would_update', 0)}")
    else:
        print(f"  Atualizados: {stats.get('updated', 0)}")
    print(f"  Sem mudanças: {stats.get('unchanged', 0)}")
    print(f"  Erros: {stats.get('error', 0)}")


if __name__ == "__main__":
    main()
