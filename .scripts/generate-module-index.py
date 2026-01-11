"""
Generate index-by-module.md organizing all requirements by project module
"""

import re
from pathlib import Path
from collections import defaultdict

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

def collect_requirements(directory, pattern, req_type):
    """Collect requirements from a directory"""
    requirements = []
    req_dir = Path(directory)

    for req_file in sorted(req_dir.glob(pattern)):
        content = req_file.read_text(encoding='utf-8')
        epic, modules = parse_frontmatter(content)

        if epic is None:
            continue

        # Extract title from H1
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else req_file.stem

        requirements.append({
            'filename': req_file.name,
            'type': req_type,
            'epic': epic,
            'modules': modules,
            'title': title,
            'rel_path': f'{req_type}/{req_file.name}'
        })

    return requirements

def generate_module_index():
    # Collect all requirements
    ucs = collect_requirements('CENTRAL/REQUIREMENTS/USE-CASES', 'UC-*.md', 'USE-CASES')
    # Filter out FA and FE
    ucs = [uc for uc in ucs if 'FA-' not in uc['filename'] and 'FE-' not in uc['filename']]

    rfs = collect_requirements('CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS', 'RF-*.md', 'FUNCTIONAL-REQUIREMENTS')
    uss = collect_requirements('CENTRAL/REQUIREMENTS/USER-STORIES', 'US-*.md', 'USER-STORIES')
    rnfs = collect_requirements('CENTRAL/REQUIREMENTS/NON-FUNCTIONAL-REQUIREMENTS', 'RNF-*.md', 'NON-FUNCTIONAL-REQUIREMENTS')

    all_reqs = ucs + rfs + uss + rnfs

    # Group by module
    by_module = defaultdict(lambda: {'UCs': [], 'RFs': [], 'USs': [], 'RNFs': []})

    for req in all_reqs:
        for module in req['modules']:
            if req['type'] == 'USE-CASES':
                by_module[module]['UCs'].append(req)
            elif req['type'] == 'FUNCTIONAL-REQUIREMENTS':
                by_module[module]['RFs'].append(req)
            elif req['type'] == 'USER-STORIES':
                by_module[module]['USs'].append(req)
            elif req['type'] == 'NON-FUNCTIONAL-REQUIREMENTS':
                by_module[module]['RNFs'].append(req)

    # Generate markdown
    output = []
    output.append("# Requirements por Módulo\n")
    output.append("Índice completo de todos os requirements organizados por módulo implementador (GEOWEB, REURBCAD, GEOAPI, GEOGIS, ADMIN, KEYCLOAK).\n")
    output.append("---\n")

    # Module order
    module_order = ['GEOWEB', 'REURBCAD', 'GEOAPI', 'GEOGIS', 'ADMIN', 'KEYCLOAK']

    for module in module_order:
        if module not in by_module:
            output.append(f"\n## {module}\n")
            output.append("Nenhum requirement associado.\n")
            continue

        data = by_module[module]
        total = len(data['UCs']) + len(data['RFs']) + len(data['USs']) + len(data['RNFs'])

        output.append(f"\n## {module} ({total} requirements)\n")

        # Use Cases
        if data['UCs']:
            output.append(f"\n### Use Cases ({len(data['UCs'])})\n")
            for req in sorted(data['UCs'], key=lambda x: x['filename']):
                output.append(f"- [{req['title']}](./{req['rel_path']}) - {req['epic']}\n")

        # Functional Requirements
        if data['RFs']:
            output.append(f"\n### Functional Requirements ({len(data['RFs'])})\n")
            for req in sorted(data['RFs'], key=lambda x: x['filename']):
                output.append(f"- [{req['title']}](./{req['rel_path']}) - {req['epic']}\n")

        # User Stories
        if data['USs']:
            output.append(f"\n### User Stories ({len(data['USs'])})\n")
            for req in sorted(data['USs'], key=lambda x: x['filename']):
                output.append(f"- [{req['title']}](./{req['rel_path']}) - {req['epic']}\n")

        # Non-Functional Requirements
        if data['RNFs']:
            output.append(f"\n### Non-Functional Requirements ({len(data['RNFs'])})\n")
            for req in sorted(data['RNFs'], key=lambda x: x['filename']):
                output.append(f"- [{req['title']}](./{req['rel_path']}) - {req['epic']}\n")

    output.append("\n---\n")

    # Summary table
    output.append("\n## Resumo por Módulo\n")
    output.append("| Módulo | UCs | RFs | USs | RNFs | Total |\n")
    output.append("|--------|-----|-----|-----|------|-------|\n")

    for module in module_order:
        if module not in by_module:
            output.append(f"| {module} | 0 | 0 | 0 | 0 | 0 |\n")
        else:
            data = by_module[module]
            total = len(data['UCs']) + len(data['RFs']) + len(data['USs']) + len(data['RNFs'])
            output.append(f"| {module} | {len(data['UCs'])} | {len(data['RFs'])} | {len(data['USs'])} | {len(data['RNFs'])} | {total} |\n")

    output.append("\n---\n")
    output.append("**Última atualização:** 2026-01-10\n")

    # Write file
    output_file = Path('CENTRAL/REQUIREMENTS/index-by-module.md')
    output_file.write_text(''.join(output), encoding='utf-8')

    total_reqs = len(all_reqs)
    print(f"Created {output_file} with {total_reqs} requirements across {len(by_module)} modules")

if __name__ == '__main__':
    generate_module_index()
