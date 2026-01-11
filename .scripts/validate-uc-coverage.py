"""
Valida que todos UCs com frontmatter modules: [X]
estão linkados em PROJECTS/X/DOCS/FEATURES/*.md
"""

import re
from pathlib import Path

def parse_frontmatter(content):
    """Extract modules from frontmatter"""
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return []

    frontmatter = match.group(1)

    # Parse modules list
    modules = []
    modules_match = re.search(r'modules:\s*\[(.*?)\]', frontmatter, re.DOTALL)
    if modules_match:
        modules_str = modules_match.group(1)
        modules = [m.strip().strip('"\'') for m in modules_str.split(',') if m.strip()]

    return modules

def check_uc_coverage():
    uc_dir = Path('CENTRAL/REQUIREMENTS/USE-CASES')
    orphans = []
    total_ucs = 0

    # Iterar UCs principais
    for uc in sorted(uc_dir.glob('UC-*.md')):
        if 'FA-' in uc.name or 'FE-' in uc.name:
            continue

        total_ucs += 1

        # Parse frontmatter
        content = uc.read_text(encoding='utf-8')
        modules = parse_frontmatter(content)

        if not modules:
            print(f"WARNING: {uc.name} has no modules in frontmatter")
            continue

        # Verificar backlinks
        found_in = []
        for mod in modules:
            features_dir = Path(f'PROJECTS/{mod}/DOCS/FEATURES')
            if not features_dir.exists():
                print(f"WARNING: {mod} has no FEATURES directory")
                continue

            for feature_file in features_dir.glob('*.md'):
                fc = feature_file.read_text(encoding='utf-8')
                if uc.name in fc:
                    found_in.append(f'{mod}:{feature_file.name}')

        if not found_in:
            orphans.append((uc.name, modules))

    # Report
    print(f"\n{'='*60}")
    print(f"UC COVERAGE VALIDATION")
    print(f"{'='*60}\n")
    print(f"Total UCs analyzed: {total_ucs}")
    print(f"UCs covered: {total_ucs - len(orphans)}")
    print(f"Orphan UCs: {len(orphans)}\n")

    if orphans:
        print(f"ORPHAN UCs (not linked in PROJECTS/*/FEATURES/):\n")
        for uc, mods in orphans:
            print(f"  - {uc}")
            print(f"    Expected in modules: {', '.join(mods)}")
            print()
        print(f"\nFIX: Create feature file in PROJECTS/{{module}}/DOCS/FEATURES/ linking to orphan UC\n")
        return False
    else:
        print("All UCs covered in PROJECTS/*/FEATURES/\n")
        return True

if __name__ == '__main__':
    success = check_uc_coverage()
    exit(0 if success else 1)
