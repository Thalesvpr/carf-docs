#!/usr/bin/env python3
"""
Script UNICO para verificar links em arquivos Markdown
- Verifica se arquivo existe MESMO
- Verifica se arquivo tem CONTEUDO (nao vazio)
- Output APENAS console (sem criar arquivos)
"""

import os
import re
from collections import defaultdict

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def find_markdown_files(root_dir):
    """Encontra todos os arquivos .md no projeto"""
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        # Ignorar pastas desnecessarias
        dirs[:] = [d for d in dirs if d not in [
            '.git', 'node_modules', '.obsidian', 'dist', 'build', 'out',
            '.next', '.cache', 'coverage', '.vscode', '.idea'
        ]]

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
        print(f"[ERRO] Nao conseguiu ler {file_path}: {e}")
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
    """
    Verifica se arquivo:
    1. Existe MESMO
    2. Tem conteudo DENTRO (nao vazio)
    """
    # Verifica existencia
    if not os.path.exists(file_path):
        return False, "arquivo nao existe"

    # Se for diretorio, ok
    if os.path.isdir(file_path):
        return True, None

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
        return False, f"erro ao ler arquivo: {e}"

def main():
    # Raiz do projeto (parent de .scripts/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    print("=" * 80)
    print("VERIFICADOR DE LINKS MARKDOWN - VERSAO UNICA")
    print("=" * 80)
    print(f"Raiz do projeto: {root_dir}")
    print()

    # Encontrar arquivos markdown
    markdown_files = find_markdown_files(root_dir)
    print(f"[*] Encontrados {len(markdown_files)} arquivos .md")
    print()

    # Estatisticas
    total_internal_links = 0
    total_broken_links = 0
    broken_by_file = defaultdict(list)

    # Verificar cada arquivo
    for md_file in markdown_files:
        relative_md = os.path.relpath(md_file, root_dir)
        links = extract_links(md_file)

        if not links:
            continue

        for link_text, link_path in links:
            # Ignorar externos
            if is_external_link(link_path):
                continue

            total_internal_links += 1

            # Resolver caminho
            resolved = resolve_link_path(md_file, link_path)
            if resolved is None:
                continue

            # VERIFICACAO ROBUSTA: existe E tem conteudo
            is_valid, error_msg = check_file_valid(resolved)

            if not is_valid:
                total_broken_links += 1
                broken_by_file[relative_md].append({
                    'text': link_text,
                    'link': link_path,
                    'resolved': os.path.relpath(resolved, root_dir),
                    'reason': error_msg
                })

    # RESULTADOS
    print("=" * 80)
    print("RESULTADOS")
    print("=" * 80)
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

    print()
    print("Verificacao concluida.")
    print()

if __name__ == "__main__":
    main()
