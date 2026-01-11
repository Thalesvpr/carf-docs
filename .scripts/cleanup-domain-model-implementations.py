"""
Script para remover seções "Implementações por projeto" de arquivos DOMAIN-MODEL
e substituir por menção abstrata de módulos conforme Opção C - Híbrido em Camadas
"""

import re
from pathlib import Path

def cleanup_implementations_section(file_path):
    """Remove seção Implementações e substitui por menção abstrata de módulos"""
    content = file_path.read_text(encoding='utf-8')

    # Pattern para encontrar seção Implementações até final do arquivo
    # Captura tudo ANTES da seção Implementações
    pattern = r'(.*?)\n\*\*Implementações?( por projeto)?:\*\*.*'

    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"  [SKIP] Secao 'Implementacoes' nao encontrada em {file_path.name}")
        return False

    # Conteúdo antes da seção Implementações
    before_section = match.group(1).rstrip()

    # Determinar quais módulos baseado no nome/contexto do arquivo
    # Para simplificar, vamos usar conjunto padrão para entities gerais
    modules_text = "\n\n**Módulos:** GEOAPI, GEOWEB, REURBCAD, GEOGIS\n"

    # Casos especiais baseados no nome do arquivo
    filename = file_path.stem
    if 'base-' in filename:
        modules_text = "\n\n**Módulos:** Todos os projetos (classe base fundamental)\n"
    elif filename in ['33-session', '34-api-key']:
        modules_text = "\n\n**Módulos:** GEOAPI (backend), GEOGIS (autenticação plugin)\n"
    elif filename in ['29-wms-server', '30-wms-layer']:
        modules_text = "\n\n**Módulos:** GEOAPI (backend), GEOWEB (renderização mapas)\n"
    elif filename == '06-pdf-templates':
        modules_text = "\n\n**Módulos:** GEOAPI (backend - geração PDF)\n"

    # Reconstruir arquivo
    new_content = before_section + modules_text + "\n---\n\n**Última atualização:** 2026-01-10\n"

    file_path.write_text(new_content, encoding='utf-8')
    return True

def main():
    base_path = Path('CENTRAL/DOMAIN-MODEL')

    directories = {
        'ENTITIES': 35,
        'VALUE-OBJECTS': 25,
        'AGGREGATES': 3,
        'EVENTS': 19
    }

    total_processed = 0
    total_errors = 0

    for dir_name, expected_count in directories.items():
        dir_path = base_path / dir_name
        print(f"\n{'='*60}")
        print(f"Processing {dir_name}/")
        print(f"{'='*60}")

        if not dir_path.exists():
            print(f"  [ERROR] Diretorio nao encontrado: {dir_path}")
            continue

        # Processar todos .md exceto README.md (será tratado separadamente)
        md_files = sorted([f for f in dir_path.glob('*.md') if f.name != 'README.md'])

        print(f"  Encontrados {len(md_files)} arquivos (esperados ~{expected_count})")

        for file_path in md_files:
            print(f"  Processando {file_path.name}...", end=' ')
            try:
                if cleanup_implementations_section(file_path):
                    print("[OK]")
                    total_processed += 1
                else:
                    print("[SKIP]")
                    total_errors += 1
            except Exception as e:
                print(f"[ERROR] {e}")
                total_errors += 1

    # Processar READMEs separadamente
    print(f"\n{'='*60}")
    print("Processing READMEs")
    print(f"{'='*60}")

    for dir_name in ['ENTITIES', 'VALUE-OBJECTS', 'AGGREGATES', 'EVENTS']:
        readme_path = base_path / dir_name / 'README.md'
        if readme_path.exists():
            print(f"  Processando {dir_name}/README.md...", end=' ')
            try:
                cleanup_readme(readme_path)
                print("[OK]")
                total_processed += 1
            except Exception as e:
                print(f"[ERROR] {e}")
                total_errors += 1

    print(f"\n{'='*60}")
    print(f"RESUMO:")
    print(f"  [OK] Processados: {total_processed}")
    print(f"  [SKIP/ERROR] Erros: {total_errors}")
    print(f"{'='*60}\n")

def cleanup_readme(file_path):
    """Limpa seção Implementações de arquivos README"""
    content = file_path.read_text(encoding='utf-8')

    # Pattern para READMEs - remove seção "## Implementações" até próxima seção ou final
    pattern = r'(.*?)\n## Implementações.*?(?=\n##|$)'

    match = re.search(pattern, content, re.DOTALL)
    if not match:
        print(f"  [SKIP] Secao '## Implementacoes' nao encontrada")
        return

    before_section = match.group(1).rstrip()

    # Buscar conteúdo após seção Implementações (próxima seção ## ou final)
    after_pattern = r'## Implementações.*?\n(##.*)'
    after_match = re.search(after_pattern, content, re.DOTALL)
    after_section = "\n\n" + after_match.group(1) if after_match else ""

    new_content = before_section + after_section

    # Adicionar atualização no final se não tiver
    if "**Última atualização:**" not in new_content:
        new_content += "\n\n---\n\n**Última atualização:** 2026-01-10\n"
    else:
        new_content = re.sub(
            r'\*\*Última atualização:\*\* \d{4}-\d{2}-\d{2}',
            '**Última atualização:** 2026-01-10',
            new_content
        )

    file_path.write_text(new_content, encoding='utf-8')

if __name__ == '__main__':
    main()
