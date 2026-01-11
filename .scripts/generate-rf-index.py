"""
Generate FUNCTIONAL-REQUIREMENTS/index-by-epic.md by parsing all RF frontmatter
"""

import re
from pathlib import Path
from collections import defaultdict

def generate_rf_index():
    rf_dir = Path('CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS')

    # Extract data from all RFs
    requirements = []

    for rf_file in sorted(rf_dir.glob('RF-*.md')):
        content = rf_file.read_text(encoding='utf-8')

        # Extract frontmatter
        match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            continue

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

        # Extract title from H1
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else rf_file.stem

        requirements.append({
            'filename': rf_file.name,
            'epic': epic,
            'modules': modules,
            'title': title
        })

    # Group by epic
    by_epic = defaultdict(list)
    for req in requirements:
        by_epic[req['epic']].append(req)

    # Sort epics by count (descending)
    sorted_epics = sorted(by_epic.items(), key=lambda x: len(x[1]), reverse=True)

    # Generate markdown
    output = []
    output.append("# Requisitos Funcionais por Épica\n")
    output.append(f"Índice dos {len(requirements)} requisitos funcionais do sistema CARF organizados por épica arquitetural.\n")
    output.append("---\n")

    for epic, reqs in sorted_epics:
        epic_title = epic.title() if epic else "Other"
        output.append(f"\n## {epic_title} ({len(reqs)} RFs)\n")

        for req in sorted(reqs, key=lambda x: x['filename']):
            modules_str = ", ".join(req['modules']) if req['modules'] else "N/A"
            output.append(f"- [{req['title']}](./{req['filename']}) - {modules_str}\n")

    output.append("\n---\n")
    output.append("**Última atualização:** 2026-01-10\n")

    # Write file
    output_file = Path('CENTRAL/REQUIREMENTS/FUNCTIONAL-REQUIREMENTS/index-by-epic.md')
    output_file.write_text(''.join(output), encoding='utf-8')
    print(f"Created {output_file} with {len(requirements)} RFs across {len(by_epic)} epics")

if __name__ == '__main__':
    generate_rf_index()
