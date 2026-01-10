#!/usr/bin/env python3
"""
Script MELHORADO para verificar links em arquivos Markdown
- Varre TODOS os arquivos .md sem discriminação (exceto node_modules/.git)
- Verifica se arquivo existe MESMO
- Detecta links com mudança de nível (../../PROJECTS, ../CENTRAL, etc)
- Output detalhado para debug
"""

import os
import re
from collections import defaultdict

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def find_markdown_files(root_dir):
    """Encontra TODOS os arquivos .md (ignora pastas de build/cache)"""
    # Lista de pastas para ignorar (mesmas do Obsidian)
    IGNORED_DIRS = {
        '.git',
        'node_modules',
        'dist',
        'build',
        '.next',
        '.cache',
        'bin',
        'obj'
    }

    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        # Ignorar pastas de build/cache
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))

    return sorted(markdown_files)

def extract_links(file_path):
    """Extrai todos os links markdown de um arquivo"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            return LINK_PATTERN.findall(content)
    except Exception as e:
        return []

def is_external_link(link):
    """Verifica se e link externo"""
    return (link.startswith('http://') or
            link.startswith('https://') or
            link.startswith('mailto:') or
            link.startswith('#'))

def resolve_link_path(source_file, link_path):
    """Resolve caminho relativo do link"""
    # Remove ancora (#section)
    if '#' in link_path:
        link_path = link_path.split('#')[0]

    if not link_path:  # Link so com ancora
        return None

    # Resolve caminho absoluto
    source_dir = os.path.dirname(source_file)
    absolute_path = os.path.normpath(os.path.join(source_dir, link_path))

    return absolute_path

def check_file_valid(file_path):
    """Verifica se arquivo existe e tem conteudo"""
    # Verifica existencia
    if not os.path.exists(file_path):
        return False, "arquivo nao existe"

    # Se for diretorio, ERRO - links devem apontar para arquivos
    if os.path.isdir(file_path):
        return False, "link aponta para pasta (deve apontar para arquivo)"

    # Verifica se arquivo tem conteudo
    try:
        size = os.path.getsize(file_path)
        if size == 0:
            return False, "arquivo vazio (0 bytes)"

        # Verifica se consegue ler
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return False, "arquivo sem conteudo"

        return True, None
    except Exception as e:
        return False, f"erro ao ler: {e}"

def main():
    # Raiz do projeto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    print("=" * 80)
    print("VERIFICADOR DE LINKS MARKDOWN - VERSAO MELHORADA")
    print("=" * 80)
    print(f"Raiz: {root_dir}")
    print()

    # Encontrar TODOS os arquivos markdown
    markdown_files = find_markdown_files(root_dir)
    print(f"[*] Encontrados {len(markdown_files)} arquivos .md")
    print()

    # Estatisticas
    total_internal_links = 0
    total_broken_links = 0
    broken_by_file = defaultdict(list)
    files_checked = 0

    # Rastreamento de arquivos linkados e isolados
    linked_files = set()  # Arquivos que RECEBEM links de outros
    files_with_outgoing_links = set()  # Arquivos que TEM links saindo
    all_md_files_set = set(os.path.normpath(f) for f in markdown_files)

    # Verificar cada arquivo
    for md_file in markdown_files:
        relative_md = os.path.relpath(md_file, root_dir)
        links = extract_links(md_file)

        if not links:
            continue

        files_checked += 1

        for link_text, link_path in links:
            # Ignorar externos
            if is_external_link(link_path):
                continue

            total_internal_links += 1

            # Resolver caminho
            resolved = resolve_link_path(md_file, link_path)
            if resolved is None:
                continue

            # Registrar que este arquivo TEM links saindo
            normalized_source = os.path.normpath(md_file)
            files_with_outgoing_links.add(normalized_source)

            # VERIFICACAO: existe E tem conteudo
            is_valid, error_msg = check_file_valid(resolved)

            if not is_valid:
                total_broken_links += 1
                broken_by_file[relative_md].append({
                    'text': link_text,
                    'link': link_path,
                    'resolved': os.path.relpath(resolved, root_dir),
                    'reason': error_msg
                })
            else:
                # Se o link e valido e aponta para um .md, registrar
                normalized_target = os.path.normpath(resolved)
                if normalized_target in all_md_files_set:
                    linked_files.add(normalized_target)

    # RESULTADOS
    print("=" * 80)
    print("RESULTADOS")
    print("=" * 80)
    print(f"Arquivos .md encontrados: {len(markdown_files)}")
    print(f"Arquivos com links: {files_checked}")
    print(f"Links internos verificados: {total_internal_links}")
    print(f"Links quebrados: {total_broken_links}")
    print(f"Arquivos com problemas: {len(broken_by_file)}")
    print()

    if total_broken_links > 0:
        print("=" * 80)
        print("DETALHES DOS LINKS QUEBRADOS")
        print("=" * 80)
        print()

        for file_path in sorted(broken_by_file.keys()):
            broken_list = broken_by_file[file_path]
            print(f"[ARQUIVO] {file_path}")
            print(f"          {len(broken_list)} link(s) quebrado(s)")
            print()

            for item in broken_list:
                print(f"  [X] Texto: {item['text']}")
                print(f"      Link: {item['link']}")
                print(f"      Resolve para: {item['resolved']}")
                print(f"      Motivo: {item['reason']}")
                print()

            print("-" * 80)
            print()
    else:
        print("=" * 80)
        print("[SUCCESS] NENHUM LINK QUEBRADO!")
        print("=" * 80)

    # ANALISE DE ARQUIVOS ORFAOS E ISOLADOS
    orphan_files = []  # Ninguem linka para ele
    isolated_files = []  # Nao linka para ninguem
    completely_isolated = []  # Ambos

    for md_file in markdown_files:
        normalized = os.path.normpath(md_file)
        relative = os.path.relpath(md_file, root_dir)

        is_orphan = normalized not in linked_files
        is_isolated = normalized not in files_with_outgoing_links

        if is_orphan and is_isolated:
            completely_isolated.append(relative)
        elif is_orphan:
            orphan_files.append(relative)
        elif is_isolated:
            isolated_files.append(relative)

    # Relatorio de arquivos orfaos/isolados
    if orphan_files or isolated_files or completely_isolated:
        print("=" * 80)
        print("ANALISE DE CONECTIVIDADE")
        print("=" * 80)
        print()

        if completely_isolated:
            print(f"[!] COMPLETAMENTE ISOLADOS ({len(completely_isolated)} arquivos)")
            print("    Nao linkam para ninguem E ninguem linka para eles")
            print()
            for file in sorted(completely_isolated)[:20]:  # Mostrar ate 20
                print(f"    - {file}")
            if len(completely_isolated) > 20:
                print(f"    ... e mais {len(completely_isolated) - 20} arquivos")
            print()
            print("-" * 80)
            print()

        if orphan_files:
            print(f"[!] ORFAOS ({len(orphan_files)} arquivos)")
            print("    Ninguem linka para eles (mas eles linkam para outros)")
            print()
            for file in sorted(orphan_files)[:20]:  # Mostrar ate 20
                print(f"    - {file}")
            if len(orphan_files) > 20:
                print(f"    ... e mais {len(orphan_files) - 20} arquivos")
            print()
            print("-" * 80)
            print()

        if isolated_files:
            print(f"[!] ISOLADOS ({len(isolated_files)} arquivos)")
            print("    Nao linkam para ninguem (mas outros linkam para eles)")
            print()
            for file in sorted(isolated_files)[:20]:  # Mostrar ate 20
                print(f"    - {file}")
            if len(isolated_files) > 20:
                print(f"    ... e mais {len(isolated_files) - 20} arquivos")
            print()

    print()
    print("Verificacao concluida.")
    print()

if __name__ == "__main__":
    main()
