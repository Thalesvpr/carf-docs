"""
Script para remover links e menções a PROJECTS/ de ARCHITECTURE, BUSINESS-RULES e API
conforme Opção C - Híbrido em Camadas
"""

import re
from pathlib import Path

def cleanup_adr_implementation_section(file_path):
    """Remove seção ## Implementação de ADRs"""
    content = file_path.read_text(encoding='utf-8')

    # Pattern para remover seção ## Implementação até próxima seção ## ou ---
    pattern = r'\n## Implementação.*?(?=\n##|\n---|$)'

    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return False  # Não tem seção Implementação

    # Remover a seção
    new_content = re.sub(pattern, '', content, flags=re.DOTALL)

    file_path.write_text(new_content, encoding='utf-8')
    return True

def cleanup_markdown_links_to_projects(file_path):
    """Transforma [PROJETO](../../PROJECTS/...) em apenas PROJETO (texto simples)"""
    content = file_path.read_text(encoding='utf-8')

    # Pattern para links markdown apontando para PROJECTS/
    # Captura: [texto qualquer](../../PROJECTS/caminho/qualquer)
    # Substitui por: apenas o texto
    pattern = r'\[([@\w\-/]+)\]\([^)]*PROJECTS/[^)]*\)'

    # Contar quantas substituições
    matches = re.findall(pattern, content)
    if not matches:
        return False

    # Substituir links por texto simples
    new_content = re.sub(pattern, r'\1', content)

    file_path.write_text(new_content, encoding='utf-8')
    return True

def cleanup_code_blocks_with_paths(file_path):
    """Remove code blocks inline que contêm paths PROJECTS/"""
    content = file_path.read_text(encoding='utf-8')

    # Pattern para code blocks inline com PROJECTS/
    pattern = r'`PROJECTS/[^`]+`'

    matches = re.findall(pattern, content)
    if not matches:
        return False

    # Substituir por texto descritivo genérico
    new_content = re.sub(pattern, '(caminho de implementação)', content)

    file_path.write_text(new_content, encoding='utf-8')
    return True

def cleanup_business_rules_implementations(file_path):
    """Remove seções de implementação em BUSINESS-RULES similar a DOMAIN-MODEL"""
    content = file_path.read_text(encoding='utf-8')

    # Pattern para lista de implementações com code blocks
    # Procura por linhas começando com "- Backend .NET:" ou "- Frontend React:" com code block
    pattern = r'\n- (Backend|Frontend|Mobile|Plugin|Documentação gerada):.*?`PROJECTS/[^`]+`'

    matches = re.findall(pattern, content)
    if not matches:
        return False

    # Remover todas essas linhas
    new_content = re.sub(pattern, '', content)

    file_path.write_text(new_content, encoding='utf-8')
    return True

def main():
    base_path = Path('CENTRAL')

    # Processar ADRs
    print("="*60)
    print("Processing ARCHITECTURE/ADRs")
    print("="*60)

    adr_path = base_path / 'ARCHITECTURE' / 'ADRs'
    if adr_path.exists():
        adr_files = sorted(adr_path.glob('ADR-*.md'))
        print(f"  Encontrados {len(adr_files)} ADRs")

        processed = 0
        for file_path in adr_files:
            print(f"  Processando {file_path.name}...", end=' ')
            removed_impl = cleanup_adr_implementation_section(file_path)
            removed_links = cleanup_markdown_links_to_projects(file_path)

            if removed_impl or removed_links:
                print("[OK]")
                processed += 1
            else:
                print("[SKIP]")

        print(f"  Total processados: {processed}/{len(adr_files)}")

    # Processar BUSINESS-RULES
    print("\n" + "="*60)
    print("Processing BUSINESS-RULES")
    print("="*60)

    br_path = base_path / 'BUSINESS-RULES'
    if br_path.exists():
        br_files = sorted(br_path.rglob('*.md'))
        print(f"  Encontrados {len(br_files)} arquivos")

        processed = 0
        for file_path in br_files:
            print(f"  Processando {file_path.relative_to(br_path)}...", end=' ')
            removed_impls = cleanup_business_rules_implementations(file_path)
            removed_links = cleanup_markdown_links_to_projects(file_path)
            removed_codeblocks = cleanup_code_blocks_with_paths(file_path)

            if removed_impls or removed_links or removed_codeblocks:
                print("[OK]")
                processed += 1
            else:
                print("[SKIP]")

        print(f"  Total processados: {processed}/{len(br_files)}")

    # Processar API
    print("\n" + "="*60)
    print("Processing API")
    print("="*60)

    api_path = base_path / 'API'
    if api_path.exists():
        api_files = sorted(api_path.rglob('*.md'))
        print(f"  Encontrados {len(api_files)} arquivos")

        processed = 0
        for file_path in api_files:
            print(f"  Processando {file_path.relative_to(api_path)}...", end=' ')
            removed_links = cleanup_markdown_links_to_projects(file_path)
            removed_codeblocks = cleanup_code_blocks_with_paths(file_path)

            if removed_links or removed_codeblocks:
                print("[OK]")
                processed += 1
            else:
                print("[SKIP]")

        print(f"  Total processados: {processed}/{len(api_files)}")

    print("\n" + "="*60)
    print("Cleanup concluido!")
    print("="*60)

if __name__ == '__main__':
    main()
