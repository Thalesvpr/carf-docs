"""
Generate USER-STORIES/index-by-epic.md by parsing all US frontmatter
"""

import re
from pathlib import Path
from collections import defaultdict

def generate_us_index():
    us_dir = Path('CENTRAL/REQUIREMENTS/USER-STORIES')

    # Extract data from all USs
    stories = []

    for us_file in sorted(us_dir.glob('US-*.md')):
        content = us_file.read_text(encoding='utf-8')

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
        title = title_match.group(1) if title_match else us_file.stem

        stories.append({
            'filename': us_file.name,
            'epic': epic,
            'modules': modules,
            'title': title
        })

    # Group by epic
    by_epic = defaultdict(list)
    for story in stories:
        by_epic[story['epic']].append(story)

    # Sort epics by count (descending)
    sorted_epics = sorted(by_epic.items(), key=lambda x: len(x[1]), reverse=True)

    # Generate markdown
    output = []
    output.append("# User Stories por Épica\n")
    output.append(f"Índice das {len(stories)} user stories do sistema CARF organizadas por épica arquitetural em formato BDD.\n")
    output.append("---\n")

    for epic, stories_list in sorted_epics:
        epic_title = epic.title() if epic else "Other"
        output.append(f"\n## {epic_title} ({len(stories_list)} USs)\n")

        for story in sorted(stories_list, key=lambda x: x['filename']):
            modules_str = ", ".join(story['modules']) if story['modules'] else "N/A"
            output.append(f"- [{story['title']}](./{story['filename']}) - {modules_str}\n")

    output.append("\n---\n")
    output.append("**Última atualização:** 2026-01-10\n")

    # Write file
    output_file = Path('CENTRAL/REQUIREMENTS/USER-STORIES/index-by-epic.md')
    output_file.write_text(''.join(output), encoding='utf-8')
    print(f"Created {output_file} with {len(stories)} USs across {len(by_epic)} epics")

if __name__ == '__main__':
    generate_us_index()
