"""
Lint script para validar isolamento de CENTRAL/ conforme Opção C - Híbrido em Camadas

Validações:
1. CENTRAL/ não deve ter markdown links para PROJECTS/
2. CENTRAL/ não deve ter code blocks com paths PROJECTS/
3. PROJECTS/*/DOCS/OVERVIEW.md deve existir
4. PROJECTS/*/DOCS/FEATURES/*.md devem linkar para CENTRAL/REQUIREMENTS/

Exit code:
- 0: Tudo OK
- 1: Violações encontradas
"""

import re
import sys
from pathlib import Path

def check_central_markdown_links():
    """Check for markdown links from CENTRAL to PROJECTS"""
    violations = []
    central_path = Path('CENTRAL')

    for md_file in central_path.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8')

        # Find markdown links to PROJECTS/
        pattern = r'\[([^\]]+)\]\(([^)]*PROJECTS/[^)]*)\)'
        matches = re.finditer(pattern, content)

        for match in matches:
            text = match.group(1)
            link = match.group(2)
            violations.append({
                'file': str(md_file.relative_to(Path('.'))),
                'type': 'markdown_link',
                'text': text,
                'link': link
            })

    return violations

def check_central_code_blocks():
    """Check for code blocks with PROJECTS/ paths"""
    violations = []
    central_path = Path('CENTRAL')

    for md_file in central_path.rglob('*.md'):
        content = md_file.read_text(encoding='utf-8')

        # Find inline code blocks with PROJECTS/
        pattern = r'`PROJECTS/[^`]+`'
        matches = re.finditer(pattern, content)

        for match in matches:
            code = match.group(0)
            violations.append({
                'file': str(md_file.relative_to(Path('.'))),
                'type': 'code_block',
                'code': code
            })

    return violations

def check_overview_files():
    """Check that PROJECTS/*/DOCS/OVERVIEW.md exists"""
    missing = []
    projects_path = Path('PROJECTS')

    expected_projects = ['GEOAPI', 'GEOWEB', 'REURBCAD', 'GEOGIS', 'ADMIN']

    for project in expected_projects:
        overview_path = projects_path / project / 'DOCS' / 'OVERVIEW.md'
        if not overview_path.exists():
            missing.append(str(overview_path))

    return missing

def check_features_link_to_central():
    """Check that FEATURES link to CENTRAL/REQUIREMENTS"""
    warnings = []
    projects_path = Path('PROJECTS')

    for project_dir in projects_path.iterdir():
        if not project_dir.is_dir():
            continue

        features_dir = project_dir / 'DOCS' / 'FEATURES'
        if not features_dir.exists():
            continue

        for feature_file in features_dir.glob('*.md'):
            if feature_file.name == 'README.md':
                continue

            content = feature_file.read_text(encoding='utf-8')

            # Check if links to CENTRAL/REQUIREMENTS
            if 'CENTRAL/REQUIREMENTS' not in content:
                warnings.append({
                    'file': str(feature_file.relative_to(Path('.'))),
                    'message': 'Feature does not link to CENTRAL/REQUIREMENTS'
                })

    return warnings

def main():
    print("="*80)
    print("LINT: Central Isolation Validation")
    print("="*80)
    print()

    total_errors = 0
    total_warnings = 0

    # Check 1: Markdown links
    print("[1/4] Checking markdown links CENTRAL -> PROJECTS...")
    markdown_violations = check_central_markdown_links()
    if markdown_violations:
        print(f"  [ERROR] Found {len(markdown_violations)} markdown link(s)")
        for v in markdown_violations[:5]:  # Show first 5
            print(f"    - {v['file']}: [{v['text']}]({v['link']})")
        if len(markdown_violations) > 5:
            print(f"    ... and {len(markdown_violations) - 5} more")
        total_errors += len(markdown_violations)
    else:
        print("  [OK] No markdown links to PROJECTS/")
    print()

    # Check 2: Code blocks
    print("[2/4] Checking code blocks with PROJECTS/ paths...")
    code_violations = check_central_code_blocks()
    if code_violations:
        print(f"  [ERROR] Found {len(code_violations)} code block(s)")
        for v in code_violations[:5]:
            print(f"    - {v['file']}: {v['code']}")
        if len(code_violations) > 5:
            print(f"    ... and {len(code_violations) - 5} more")
        total_errors += len(code_violations)
    else:
        print("  [OK] No code blocks with PROJECTS/ paths")
    print()

    # Check 3: OVERVIEW.md exists
    print("[3/4] Checking PROJECTS/*/DOCS/OVERVIEW.md exists...")
    missing_overviews = check_overview_files()
    if missing_overviews:
        print(f"  [ERROR] Missing {len(missing_overviews)} OVERVIEW.md file(s)")
        for m in missing_overviews:
            print(f"    - {m}")
        total_errors += len(missing_overviews)
    else:
        print("  [OK] All OVERVIEW.md files exist")
    print()

    # Check 4: Features link to CENTRAL
    print("[4/4] Checking FEATURES link to CENTRAL/REQUIREMENTS...")
    feature_warnings = check_features_link_to_central()
    if feature_warnings:
        print(f"  [WARNING] Found {len(feature_warnings)} feature(s) without CENTRAL links")
        for w in feature_warnings[:5]:
            print(f"    - {w['file']}")
        if len(feature_warnings) > 5:
            print(f"    ... and {len(feature_warnings) - 5} more")
        total_warnings += len(feature_warnings)
    else:
        print("  [OK] All features link to CENTRAL")
    print()

    # Summary
    print("="*80)
    print("SUMMARY")
    print("="*80)
    print(f"  Errors: {total_errors}")
    print(f"  Warnings: {total_warnings}")
    print()

    if total_errors > 0:
        print("[FAIL] Validation failed with errors")
        return 1
    elif total_warnings > 0:
        print("[PASS] Validation passed with warnings")
        return 0
    else:
        print("[PASS] All validations passed!")
        return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
