"""
Generate traceability-matrix.md showing UC→RF→US→RNF mappings
"""

import re
from pathlib import Path

def parse_frontmatter(content):
    """Extract epic and modules from frontmatter"""
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, []

    frontmatter = match.group(1)

    # Parse epic
    epic_match = re.search(r'epic:\s*(.+)', frontmatter)
    epic = epic_match.group(1).strip() if epic_match else 'other'

    # Parse modules list
    modules = []
    modules_match = re.search(r'modules:\s*\[(.*?)\]', frontmatter, re.DOTALL)
    if modules_match:
        modules_str = modules_match.group(1)
        modules = [m.strip().strip('"\'') for m in modules_str.split(',') if m.strip()]

    return epic, modules

def extract_rastreabilidade(content):
    """Extract RF, US, RNF references from rastreabilidade section"""
    rfs = []
    uss = []
    rnfs = []

    # Find rastreabilidade section
    match = re.search(r'\*\*Rastreabilidade:\*\*\s*\n((?:- [^\n]+\n)+)', content)
    if not match:
        return rfs, uss, rnfs

    rastro_text = match.group(1)

    # Extract RF references
    rf_matches = re.findall(r'RF-\d{3}', rastro_text)
    rfs = sorted(list(set(rf_matches)))

    # Extract US references
    us_matches = re.findall(r'US-\d{3}', rastro_text)
    uss = sorted(list(set(us_matches)))

    # Extract RNF references
    rnf_matches = re.findall(r'RNF-\d{3}', rastro_text)
    rnfs = sorted(list(set(rnf_matches)))

    return rfs, uss, rnfs

def find_req_file(req_type, req_num):
    """Find the actual filename for a requirement"""
    if req_type == 'RF':
        dir_path = Path('CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS')
    elif req_type == 'US':
        dir_path = Path('CENTRAL/REQUIREMENTS/USER-STORIES')
    elif req_type == 'RNF':
        dir_path = Path('CENTRAL/REQUIREMENTS/NON-FUNCTIONAL-REQUIREMENTS')
    else:
        return None

    # Look for file starting with the requirement number
    pattern = f'{req_type}-{req_num}-*.md'
    matches = list(dir_path.glob(pattern))

    if matches:
        return matches[0]
    return None

def get_req_title(req_file):
    """Extract title from requirement file"""
    if not req_file or not req_file.exists():
        return None

    content = req_file.read_text(encoding='utf-8')
    title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
    return title_match.group(1) if title_match else None

def generate_traceability_matrix():
    uc_dir = Path('CENTRAL/REQUIREMENTS/USE-CASES')

    # Collect UC data
    ucs = []
    for uc_file in sorted(uc_dir.glob('UC-*.md')):
        # Skip FA and FE files
        if 'FA-' in uc_file.name or 'FE-' in uc_file.name:
            continue

        content = uc_file.read_text(encoding='utf-8')

        # Extract title
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else uc_file.stem

        # Extract metadata
        epic, modules = parse_frontmatter(content)

        # Extract rastreabilidade
        rfs, uss, rnfs = extract_rastreabilidade(content)

        ucs.append({
            'filename': uc_file.name,
            'title': title,
            'epic': epic,
            'modules': modules,
            'rfs': rfs,
            'uss': uss,
            'rnfs': rnfs
        })

    # Generate markdown
    output = []
    output.append("# Matriz de Rastreabilidade\n")
    output.append("Mapa completo mostrando dependências UC → RF → US → RNF para todos os 11 casos de uso principais do sistema CARF.\n")
    output.append("---\n")

    for uc in ucs:
        output.append(f"\n## {uc['title']}\n")
        output.append(f"**Módulos:** {', '.join(uc['modules'])}\n")
        output.append(f"**Épica:** {uc['epic']}\n")

        # Requisitos Funcionais
        if uc['rfs']:
            output.append(f"\n### Requisitos Funcionais ({len(uc['rfs'])})\n")
            for rf_id in uc['rfs']:
                rf_file = find_req_file('RF', rf_id.split('-')[1])
                if rf_file:
                    title = get_req_title(rf_file)
                    if title:
                        # Remove the RF-XXX prefix from title if present
                        title = re.sub(r'^RF-\d{3}:\s*', '', title)
                        output.append(f"- [{rf_id}: {title}](./FUNCTIONAL-REQUIREMENTS/{rf_file.name})\n")
                    else:
                        output.append(f"- [{rf_id}](./FUNCTIONAL-REQUIREMENTS/{rf_file.name})\n")
                else:
                    output.append(f"- {rf_id} (arquivo não encontrado)\n")

        # User Stories
        if uc['uss']:
            output.append(f"\n### User Stories ({len(uc['uss'])})\n")
            for us_id in uc['uss']:
                us_file = find_req_file('US', us_id.split('-')[1])
                if us_file:
                    title = get_req_title(us_file)
                    if title:
                        # Remove the US-XXX prefix from title if present
                        title = re.sub(r'^US-\d{3}:\s*', '', title)
                        output.append(f"- [{us_id}: {title}](./USER-STORIES/{us_file.name})\n")
                    else:
                        output.append(f"- [{us_id}](./USER-STORIES/{us_file.name})\n")
                else:
                    output.append(f"- {us_id} (arquivo não encontrado)\n")

        # Requisitos Não-Funcionais
        if uc['rnfs']:
            output.append(f"\n### Requisitos Não-Funcionais ({len(uc['rnfs'])})\n")
            for rnf_id in uc['rnfs']:
                rnf_file = find_req_file('RNF', rnf_id.split('-')[1])
                if rnf_file:
                    title = get_req_title(rnf_file)
                    if title:
                        # Remove the RNF-XXX prefix from title if present
                        title = re.sub(r'^RNF-\d{3}:\s*', '', title)
                        output.append(f"- [{rnf_id}: {title}](./NON-FUNCTIONAL-REQUIREMENTS/{rnf_file.name})\n")
                    else:
                        output.append(f"- [{rnf_id}](./NON-FUNCTIONAL-REQUIREMENTS/{rnf_file.name})\n")
                else:
                    output.append(f"- {rnf_id} (arquivo não encontrado)\n")

        # Implementado em
        output.append("\n### Implementado em\n")
        for module in uc['modules']:
            features_dir = Path(f'PROJECTS/{module}/DOCS/FEATURES')
            if features_dir.exists():
                # Find feature file that links to this UC
                for feature_file in features_dir.glob('*.md'):
                    content = feature_file.read_text(encoding='utf-8')
                    if uc['filename'] in content:
                        output.append(f"- [{module}: {feature_file.stem.replace('-', ' ').title()}](../../PROJECTS/{module}/DOCS/FEATURES/{feature_file.name})\n")
                        break

        output.append("\n---\n")

    # Summary statistics
    output.append("\n## Estatísticas\n")

    total_rfs = sum(len(uc['rfs']) for uc in ucs)
    total_uss = sum(len(uc['uss']) for uc in ucs)
    total_rnfs = sum(len(uc['rnfs']) for uc in ucs)

    output.append(f"- **Total de UCs:** {len(ucs)}\n")
    output.append(f"- **Total de RFs referenciados:** {total_rfs}\n")
    output.append(f"- **Total de USs referenciados:** {total_uss}\n")
    output.append(f"- **Total de RNFs referenciados:** {total_rnfs}\n")
    output.append(f"- **Média de RFs por UC:** {total_rfs / len(ucs):.1f}\n")
    output.append(f"- **Média de USs por UC:** {total_uss / len(ucs):.1f}\n")

    output.append("\n---\n")
    output.append("**Última atualização:** 2026-01-10\n")

    # Write file
    output_file = Path('CENTRAL/REQUIREMENTS/traceability-matrix.md')
    output_file.write_text(''.join(output), encoding='utf-8')
    print(f"Created {output_file} with {len(ucs)} UCs mapped to {total_rfs} RFs, {total_uss} USs, {total_rnfs} RNFs")

if __name__ == '__main__':
    generate_traceability_matrix()
