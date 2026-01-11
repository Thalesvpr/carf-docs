#!/usr/bin/env python3
"""
Analyze the 97 completely isolated files and categorize them
"""

from pathlib import Path
import re
from collections import defaultdict

def find_isolated_files():
    """Find all completely isolated files (no incoming or outgoing links)"""

    # Read check-links.py output to get isolated files
    # For now, manually categorize the main areas we saw

    isolated_by_category = defaultdict(list)

    root = Path('.')

    # CENTRAL/DOMAIN-MODEL
    domain_model_dirs = [
        'CENTRAL/DOMAIN-MODEL/BUSINESS-RULES/LEGITIMATION-RULES',
        'CENTRAL/DOMAIN-MODEL/ENTITIES',
        'CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS'
    ]

    for dir_path in domain_model_dirs:
        path = Path(dir_path)
        if path.exists():
            for md_file in path.glob('*.md'):
                if md_file.stem.startswith('00-') or md_file.stem.startswith('01-') or md_file.stem in ['reurb-e-requirements', 'reurb-s-requirements', '05-contestation', '04-custom-data-schema', '05-permissions-matrix', '06-spatial-overlap-matrix']:
                    isolated_by_category['DOMAIN-MODEL'].append(str(md_file))

    # CENTRAL/SECURITY
    security_dirs = [
        'CENTRAL/SECURITY/INCIDENTS',
        'CENTRAL/SECURITY/POLICIES',
        'CENTRAL/SECURITY/STANDARDS',
        'CENTRAL/SECURITY/CHECKLISTS'
    ]

    for dir_path in security_dirs:
        path = Path(dir_path)
        if path.exists():
            for md_file in path.rglob('*.md'):
                isolated_by_category['SECURITY'].append(str(md_file))

    # CENTRAL/TESTING
    testing_path = Path('CENTRAL/TESTING')
    if testing_path.exists():
        for md_file in testing_path.rglob('*.md'):
            isolated_by_category['TESTING'].append(str(md_file))

    # CENTRAL/MONITORING
    monitoring_path = Path('CENTRAL/MONITORING')
    if monitoring_path.exists():
        for md_file in monitoring_path.rglob('*.md'):
            isolated_by_category['MONITORING'].append(str(md_file))

    # CENTRAL/DEPLOYMENT
    deployment_orphans = [
        'CENTRAL/ARCHITECTURE/DEPLOYMENT/02-containerization.md',
        'CENTRAL/ARCHITECTURE/DEPLOYMENT/04-cicd-pipeline.md'
    ]
    for file_path in deployment_orphans:
        if Path(file_path).exists():
            isolated_by_category['DEPLOYMENT'].append(file_path)

    # CENTRAL/ARCHITECTURE/QUALITY
    quality_path = Path('CENTRAL/ARCHITECTURE/QUALITY')
    if quality_path.exists():
        for md_file in quality_path.rglob('*.md'):
            isolated_by_category['QUALITY'].append(str(md_file))

    # CENTRAL/TEMPLATES
    templates_path = Path('CENTRAL/TEMPLATES')
    if templates_path.exists():
        for md_file in templates_path.rglob('*.md'):
            isolated_by_category['TEMPLATES'].append(str(md_file))

    # CENTRAL/TODO
    todo_path = Path('CENTRAL/TODO')
    if todo_path.exists():
        for md_file in todo_path.rglob('*.md'):
            isolated_by_category['TODO'].append(str(md_file))

    return isolated_by_category

def suggest_connections(category, files):
    """Suggest where files should be linked from"""
    suggestions = {
        'DOMAIN-MODEL': {
            'link_from': 'CENTRAL/DOMAIN-MODEL/ENTITIES/README.md, CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/README.md, CENTRAL/DOMAIN-MODEL/BUSINESS-RULES/README.md',
            'action': 'Add to index pages in their respective READMEs'
        },
        'SECURITY': {
            'link_from': 'CENTRAL/SECURITY/README.md',
            'action': 'Create CENTRAL/SECURITY/README.md index linking all security docs'
        },
        'TESTING': {
            'link_from': 'CENTRAL/TESTING/README.md',
            'action': 'Create or update CENTRAL/TESTING/README.md index'
        },
        'MONITORING': {
            'link_from': 'CENTRAL/MONITORING/README.md',
            'action': 'Create CENTRAL/MONITORING/README.md index'
        },
        'DEPLOYMENT': {
            'link_from': 'CENTRAL/ARCHITECTURE/DEPLOYMENT/README.md',
            'action': 'Link from DEPLOYMENT/README.md'
        },
        'QUALITY': {
            'link_from': 'CENTRAL/ARCHITECTURE/QUALITY/README.md',
            'action': 'Create or update QUALITY/README.md index'
        },
        'TEMPLATES': {
            'link_from': 'CENTRAL/TEMPLATES/README.md',
            'action': 'Create CENTRAL/TEMPLATES/README.md index'
        },
        'TODO': {
            'link_from': 'CENTRAL/TODO/README.md',
            'action': 'Create CENTRAL/TODO/README.md index'
        }
    }

    return suggestions.get(category, {})

def main():
    print("="*80)
    print("ANALYZING 97 COMPLETELY ISOLATED FILES")
    print("="*80)
    print()

    isolated = find_isolated_files()

    total = sum(len(files) for files in isolated.values())

    print(f"Total isolated files found: {total}")
    print()

    for category, files in sorted(isolated.items()):
        print(f"\n[{category}] - {len(files)} files")
        print("-" * 80)

        for file in sorted(files)[:10]:  # Show first 10
            print(f"  - {file}")

        if len(files) > 10:
            print(f"  ... and {len(files) - 10} more")

        suggestion = suggest_connections(category, files)
        if suggestion:
            print(f"\n  [SUGGESTION]")
            print(f"    Link from: {suggestion.get('link_from', 'N/A')}")
            print(f"    Action: {suggestion.get('action', 'N/A')}")

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total categories: {len(isolated)}")
    print(f"Total isolated files: {total}")
    print()
    print("Next steps:")
    print("1. Create missing README.md index files")
    print("2. Link isolated files from their category READMEs")
    print("3. Link category READMEs from parent indices")
    print("="*80)

if __name__ == '__main__':
    main()
