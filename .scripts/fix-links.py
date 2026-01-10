#!/usr/bin/env python3
"""
Script para DETECTAR e CORRIGIR links quebrados automaticamente
- Roda a verificacao de links
- Conserta automaticamente os problemas encontrados
- Output apenas console
"""

import os
import re
from collections import defaultdict

LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def find_markdown_files(root_dir):
    """Encontra todos os arquivos .md no projeto"""
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
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
        return []

def is_external_link(link):
    """Verifica se e link externo"""
    return (link.startswith('http://') or
            link.startswith('https://') or
            link.startswith('mailto:') or
            link.startswith('#'))

def resolve_link_path(source_file, link_path):
    """Resolve caminho relativo do link"""
    if '#' in link_path:
        link_path = link_path.split('#')[0]
    if not link_path:
        return None
    source_dir = os.path.dirname(source_file)
    absolute_path = os.path.normpath(os.path.join(source_dir, link_path))
    return absolute_path

def check_file_valid(file_path):
    """Verifica se arquivo existe E tem conteudo"""
    if not os.path.exists(file_path):
        return False, "arquivo nao existe"
    if os.path.isdir(file_path):
        return True, None
    try:
        size = os.path.getsize(file_path)
        if size == 0:
            return False, "arquivo vazio (0 bytes)"
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return False, "arquivo sem conteudo"
        return True, None
    except Exception as e:
        return False, f"erro ao ler arquivo: {e}"

def detect_broken_links(root_dir):
    """Detecta todos os links quebrados (fase 1: DETECCAO)"""
    markdown_files = find_markdown_files(root_dir)
    broken_by_file = defaultdict(list)
    total_internal = 0
    total_broken = 0

    for md_file in markdown_files:
        relative_md = os.path.relpath(md_file, root_dir)
        links = extract_links(md_file)

        for link_text, link_path in links:
            if is_external_link(link_path):
                continue

            total_internal += 1
            resolved = resolve_link_path(md_file, link_path)
            if resolved is None:
                continue

            is_valid, error_msg = check_file_valid(resolved)
            if not is_valid:
                total_broken += 1
                broken_by_file[md_file].append({
                    'text': link_text,
                    'link': link_path,
                    'resolved': os.path.relpath(resolved, root_dir),
                    'reason': error_msg
                })

    return broken_by_file, total_internal, total_broken

def fix_broken_links(broken_by_file, root_dir):
    """Conserta os links quebrados (fase 2: CORRECAO)"""
    total_fixed = 0

    for md_file, broken_list in broken_by_file.items():
        if not broken_list:
            continue

        relative_md = os.path.relpath(md_file, root_dir)
        print(f"[FIX] {relative_md}")
        print(f"      {len(broken_list)} link(s) para corrigir")

        # Ler arquivo
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"      [ERRO] Nao conseguiu ler arquivo: {e}")
            continue

        # Aplicar correcoes
        new_lines = []
        fixes_applied = 0

        for line in lines:
            original_line = line
            modified = False

            # Procurar links quebrados nesta linha
            for broken in broken_list:
                # Pattern: [texto](link)
                pattern = re.escape(f"[{broken['text']}]({broken['link']})")

                if re.search(pattern, line):
                    # ESTRATEGIA DE CORRECAO:
                    # Se linha só tem o link (linha de referencia), REMOVER linha
                    # Senão, converter link para texto bold: **texto**

                    line_stripped = line.strip()

                    # Casos especiais de template (CENTRAL/TEMPLATES/)
                    if 'TEMPLATES' in md_file:
                        # Templates são exemplos, remover linha inteira
                        line = ""
                        modified = True
                        fixes_applied += 1
                        break

                    # Se linha começa com emoji + link (ex: "📖 [texto](link)")
                    elif re.match(r'^\s*[\U0001F300-\U0001F9FF]\s*\[', line_stripped):
                        line = ""  # Remover linha
                        modified = True
                        fixes_applied += 1
                        break

                    # Se linha só tem link e nada mais
                    elif line_stripped == f"[{broken['text']}]({broken['link']})":
                        line = ""  # Remover linha
                        modified = True
                        fixes_applied += 1
                        break

                    # Se link está em lista ou parágrafo, converter para bold
                    else:
                        line = line.replace(
                            f"[{broken['text']}]({broken['link']})",
                            f"**{broken['text']}**"
                        )
                        modified = True
                        fixes_applied += 1
                        break

            if line.strip() or not modified:  # Manter linha se não vazia ou não modificada
                new_lines.append(line)

        # Remover linhas vazias duplicadas
        final_lines = []
        prev_empty = False
        for line in new_lines:
            is_empty = line.strip() == ''
            if is_empty and prev_empty:
                continue
            final_lines.append(line)
            prev_empty = is_empty

        # Salvar arquivo corrigido
        if fixes_applied > 0:
            try:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.writelines(final_lines)
                print(f"      [OK] {fixes_applied} correcao(oes) aplicada(s)")
                total_fixed += fixes_applied
            except Exception as e:
                print(f"      [ERRO] Nao conseguiu salvar: {e}")
        else:
            print(f"      [SKIP] Nenhuma correcao aplicada")

        print()

    return total_fixed

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir)

    print("=" * 80)
    print("AUTO-FIX DE LINKS QUEBRADOS")
    print("=" * 80)
    print(f"Raiz do projeto: {root_dir}")
    print()

    # FASE 1: DETECCAO
    print("=" * 80)
    print("FASE 1: DETECTANDO LINKS QUEBRADOS")
    print("=" * 80)
    print()

    broken_by_file, total_internal, total_broken = detect_broken_links(root_dir)

    print(f"Links internos verificados: {total_internal}")
    print(f"Links quebrados encontrados: {total_broken}")
    print(f"Arquivos com problemas: {len(broken_by_file)}")
    print()

    if total_broken == 0:
        print("=" * 80)
        print("[SUCCESS] NENHUM LINK QUEBRADO ENCONTRADO!")
        print("=" * 80)
        return

    # FASE 2: CORRECAO
    print("=" * 80)
    print("FASE 2: CORRIGINDO LINKS QUEBRADOS")
    print("=" * 80)
    print()

    total_fixed = fix_broken_links(broken_by_file, root_dir)

    # RESUMO FINAL
    print("=" * 80)
    print("RESUMO FINAL")
    print("=" * 80)
    print(f"Links quebrados detectados: {total_broken}")
    print(f"Correcoes aplicadas: {total_fixed}")
    print()

    # VERIFICACAO FINAL
    print("=" * 80)
    print("VERIFICACAO FINAL")
    print("=" * 80)
    print("Rodando verificacao novamente...")
    print()

    broken_after, total_after, broken_count_after = detect_broken_links(root_dir)

    if broken_count_after == 0:
        print("[SUCCESS] TODOS OS LINKS FORAM CORRIGIDOS!")
    else:
        print(f"[AVISO] Ainda restam {broken_count_after} link(s) quebrado(s)")
        print("        Execute novamente para corrigir ou verifique manualmente")

    print()
    print("Concluido.")
    print()

if __name__ == "__main__":
    main()
