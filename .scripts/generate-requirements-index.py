#!/usr/bin/env python3
"""
Gera índices automáticos nos README.md das pastas de requisitos.

Uso:
    python .scripts/generate-requirements-index.py

O script:
1. Escaneia subpastas de FUNCTIONAL-REQUIREMENTS, USER-STORIES, USE-CASES, NON-FUNCTIONAL-REQUIREMENTS
2. Lista arquivos .md (exceto README.md)
3. Extrai ID e título de cada arquivo
4. Atualiza seção <!-- GENERATED:START --> ... <!-- GENERATED:END --> nos READMEs
5. Atualiza README.md raiz de cada tipo com índice de subpastas
"""
import re
import sys
from datetime import datetime
from pathlib import Path

# Configuração das pastas de requisitos
REQUIREMENTS_BASE = Path("CENTRAL/REQUIREMENTS")

REQUIREMENT_TYPES = {
    "FUNCTIONAL-REQUIREMENTS": {
        "prefix": "RF",
        "title": "Requisitos Funcionais",
        "description": "Especificações funcionais do sistema CARF."
    },
    "USER-STORIES": {
        "prefix": "US",
        "title": "User Stories",
        "description": "Histórias de usuário do sistema CARF."
    },
    "USE-CASES": {
        "prefix": "UC",
        "title": "Casos de Uso",
        "description": "Casos de uso detalhados do sistema CARF."
    },
    "NON-FUNCTIONAL-REQUIREMENTS": {
        "prefix": "RNF",
        "title": "Requisitos Não-Funcionais",
        "description": "Requisitos de qualidade e restrições do sistema CARF."
    }
}

# Mapeamento de nomes de pastas para títulos legíveis
DOMAIN_NAMES = {
    # RF/US domains
    "01-auth-security": "Autenticação e Segurança",
    "02-tenants": "Gestão de Tenants",
    "03-users-teams": "Usuários e Equipes",
    "04-notifications": "Notificações",
    "05-communities": "Gestão de Comunidades",
    "06-units": "Gestão de Unidades",
    "07-holders": "Gestão de Titulares",
    "08-documents-media": "Documentos e Mídia",
    "09-layers-features": "Camadas e Features",
    "10-spatial-analysis": "Análise Espacial",
    "11-annotations": "Anotações",
    "12-surveys": "Levantamentos Topográficos",
    "13-legitimation": "Processos de Legitimação",
    "14-offline-sync": "Modo Offline e Sincronização",
    "15-data-export": "Exportação de Dados",
    "16-reports": "Relatórios",
    "17-wms-wmts": "Integrações WMS/WMTS",
    # RNF domains
    "01-performance": "Performance",
    "02-security": "Segurança",
    "03-reliability": "Confiabilidade",
    "04-usability": "Usabilidade",
    "05-scalability": "Escalabilidade",
    "06-compatibility": "Compatibilidade",
    "07-maintainability": "Manutenibilidade",
    "08-interoperability": "Interoperabilidade",
}


def extract_title_from_file(file_path: Path) -> str:
    """Extrai título do arquivo markdown (primeira linha # Título ou frontmatter title)."""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Tenta encontrar título no formato "# XX-NNN: Título"
        match = re.search(r"^#\s+\w+-\d+[:\s]+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Tenta encontrar qualquer título #
        match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if match:
            return match.group(1).strip()

        # Fallback: usa o nome do arquivo
        return file_path.stem
    except Exception:
        return file_path.stem


def extract_id_from_filename(filename: str) -> str:
    """Extrai ID (RF-001, US-001, etc) do nome do arquivo."""
    match = re.match(r"(RF|US|UC|RNF)-(\d{3})", filename)
    if match:
        return f"{match.group(1)}-{match.group(2)}"
    return filename


def get_files_in_folder(folder: Path, prefix: str) -> list[dict]:
    """Lista arquivos de requisitos em uma pasta."""
    files = []

    for md_file in sorted(folder.glob("*.md")):
        if md_file.name.lower() == "readme.md":
            continue
        if md_file.name.startswith("index"):
            continue

        file_id = extract_id_from_filename(md_file.stem)
        title = extract_title_from_file(md_file)

        files.append({
            "id": file_id,
            "title": title,
            "filename": md_file.name,
            "path": md_file
        })

    return files


def generate_files_table(files: list[dict]) -> str:
    """Gera tabela markdown com lista de arquivos."""
    if not files:
        return "*Nenhum arquivo encontrado nesta pasta.*\n"

    lines = [
        "| ID | Título |",
        "|:---|:-------|"
    ]

    for f in files:
        link = f"[{f['id']}](./{f['filename']})"
        # Escapa pipes no título
        title = f['title'].replace("|", "\\|")
        lines.append(f"| {link} | {title} |")

    return "\n".join(lines) + "\n"


def generate_subfolders_table(subfolders: list[dict]) -> str:
    """Gera tabela markdown com índice de subpastas."""
    if not subfolders:
        return "*Nenhuma subpasta encontrada.*\n"

    lines = [
        "| # | Domínio | Arquivos |",
        "|:--|:--------|:--------:|"
    ]

    for sf in subfolders:
        link = f"[{sf['name']}](./{sf['folder_name']}/README.md)"
        lines.append(f"| {sf['number']} | {link} | {sf['count']} |")

    return "\n".join(lines) + "\n"


def update_readme_generated_section(readme_path: Path, generated_content: str) -> bool:
    """Atualiza seção GENERATED no README.md."""

    if not readme_path.exists():
        # Cria README básico se não existir
        folder_name = readme_path.parent.name
        domain_title = DOMAIN_NAMES.get(folder_name, folder_name)

        content = f"""# {domain_title}

---

<!-- GENERATED:START - Não edite abaixo desta linha -->
{generated_content}
<!-- GENERATED:END -->
"""
        readme_path.write_text(content, encoding="utf-8")
        return True

    # Lê conteúdo existente
    content = readme_path.read_text(encoding="utf-8")

    # Pattern para encontrar seção GENERATED
    pattern = r"(<!-- GENERATED:START[^>]*-->).*?(<!-- GENERATED:END -->)"

    if re.search(pattern, content, re.DOTALL):
        # Atualiza seção existente
        new_content = re.sub(
            pattern,
            f"\\1\n{generated_content}\\2",
            content,
            flags=re.DOTALL
        )
        readme_path.write_text(new_content, encoding="utf-8")
        return True
    else:
        # Adiciona seção no final
        content = content.rstrip() + f"""

---

<!-- GENERATED:START - Não edite abaixo desta linha -->
{generated_content}
<!-- GENERATED:END -->
"""
        readme_path.write_text(content, encoding="utf-8")
        return True


def process_requirement_type(req_type: str, config: dict) -> dict:
    """Processa um tipo de requisito (RF, US, UC, RNF)."""
    base_path = REQUIREMENTS_BASE / req_type

    if not base_path.exists():
        print(f"  [SKIP] Pasta não existe: {base_path}")
        return {"total": 0, "subfolders": []}

    subfolders_data = []
    total_files = 0

    # Lista subpastas
    subfolders = sorted([d for d in base_path.iterdir() if d.is_dir()])

    if not subfolders:
        # Sem subpastas - arquivos estão na raiz (estrutura flat atual)
        files = get_files_in_folder(base_path, config["prefix"])
        total_files = len(files)
        print(f"  [INFO] {total_files} arquivos na raiz (estrutura flat)")
        return {"total": total_files, "subfolders": []}

    # Processa cada subpasta
    for subfolder in subfolders:
        files = get_files_in_folder(subfolder, config["prefix"])
        count = len(files)
        total_files += count

        # Extrai número da pasta (ex: "01" de "01-auth-security")
        number_match = re.match(r"(\d+)-", subfolder.name)
        number = number_match.group(1) if number_match else ""

        domain_name = DOMAIN_NAMES.get(subfolder.name, subfolder.name)

        subfolders_data.append({
            "folder_name": subfolder.name,
            "name": domain_name,
            "number": number,
            "count": count,
            "files": files
        })

        # Gera conteúdo para README da subpasta
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        generated = f"## Arquivos ({count} requisitos)\n\n"
        generated += generate_files_table(files)
        generated += f"\n*Gerado automaticamente em {timestamp}*\n"

        # Atualiza README da subpasta
        readme_path = subfolder / "README.md"
        update_readme_generated_section(readme_path, generated)
        print(f"  [OK] {subfolder.name}/README.md ({count} arquivos)")

    # Gera conteúdo para README raiz do tipo
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    generated = f"## Índice por Domínio ({total_files} requisitos)\n\n"
    generated += generate_subfolders_table(subfolders_data)
    generated += f"\n*Gerado automaticamente em {timestamp}*\n"

    # Atualiza README raiz
    readme_path = base_path / "README.md"
    update_readme_generated_section(readme_path, generated)
    print(f"  [OK] {req_type}/README.md (índice)")

    return {"total": total_files, "subfolders": subfolders_data}


def main():
    print("=" * 70)
    print("GERAÇÃO DE ÍNDICES DE REQUISITOS")
    print("=" * 70)
    print()

    if not REQUIREMENTS_BASE.exists():
        print(f"[ERROR] Pasta base não existe: {REQUIREMENTS_BASE}")
        return 1

    results = {}

    for req_type, config in REQUIREMENT_TYPES.items():
        print(f"[*] Processando {req_type}...")
        results[req_type] = process_requirement_type(req_type, config)
        print()

    # Resumo final
    print("=" * 70)
    print("RESUMO")
    print("=" * 70)

    grand_total = 0
    for req_type, data in results.items():
        total = data["total"]
        grand_total += total
        subfolders_count = len(data["subfolders"])
        if subfolders_count > 0:
            print(f"  {req_type}: {total} arquivos em {subfolders_count} pastas")
        else:
            print(f"  {req_type}: {total} arquivos (flat)")

    print(f"\n  TOTAL: {grand_total} arquivos de requisitos")
    print("=" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main())
