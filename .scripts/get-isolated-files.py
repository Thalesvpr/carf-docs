#!/usr/bin/env python3
"""
Extract the exact list of 58 completely isolated files
"""

from pathlib import Path
import re

def find_all_md_files():
    """Find all markdown files"""
    root = Path('.')
    return list(root.rglob('*.md'))

def has_markdown_links(file_path):
    """Check if file has outgoing markdown links"""
    try:
        content = file_path.read_text(encoding='utf-8')
        # Look for markdown links [text](path)
        pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(pattern, content)
        # Filter out external links (http/https)
        internal_links = [m for m in matches if not m[1].startswith('http')]
        return len(internal_links) > 0
    except:
        return False

def find_files_linking_to(target_file, all_files):
    """Find files that link to target_file"""
    target_name = target_file.name
    target_path = str(target_file.relative_to('.'))

    incoming = []

    for file in all_files:
        if file == target_file:
            continue

        try:
            content = file.read_text(encoding='utf-8')
            # Check if this file links to target
            if target_name in content or str(target_file.stem) in content:
                # More precise check
                pattern = r'\[([^\]]+)\]\(([^)]+)\)'
                matches = re.findall(pattern, content)
                for text, link in matches:
                    # Normalize paths
                    if target_name in link or target_file.stem in link:
                        incoming.append(file)
                        break
        except:
            continue

    return incoming

def main():
    print("Finding completely isolated files...")

    all_files = find_all_md_files()

    # Exclude certain paths
    excluded_patterns = [
        '.git',
        'node_modules',
        '.obsidian'
    ]

    filtered_files = []
    for f in all_files:
        if any(pattern in str(f) for pattern in excluded_patterns):
            continue
        filtered_files.append(f)

    isolated = []

    for file in filtered_files:
        has_outgoing = has_markdown_links(file)
        incoming = find_files_linking_to(file, filtered_files)

        if not has_outgoing and len(incoming) == 0:
            isolated.append(file)

    print(f"\nFound {len(isolated)} completely isolated files:\n")

    # Group by category
    from collections import defaultdict
    by_category = defaultdict(list)

    for file in sorted(isolated):
        path_str = str(file)

        if 'CENTRAL/VERSIONING' in path_str:
            by_category['CENTRAL/VERSIONING'].append(file)
        elif 'PROJECTS/GEOAPI' in path_str:
            by_category['PROJECTS/GEOAPI'].append(file)
        elif 'PROJECTS/GEOWEB' in path_str:
            by_category['PROJECTS/GEOWEB'].append(file)
        elif 'PROJECTS/REURBCAD' in path_str:
            by_category['PROJECTS/REURBCAD'].append(file)
        elif 'PROJECTS/GEOGIS' in path_str:
            by_category['PROJECTS/GEOGIS'].append(file)
        elif 'PROJECTS/ADMIN' in path_str:
            by_category['PROJECTS/ADMIN'].append(file)
        elif 'PROJECTS/WEBDOCS' in path_str:
            by_category['PROJECTS/WEBDOCS'].append(file)
        elif 'PROJECTS/LIB' in path_str:
            by_category['PROJECTS/LIB'].append(file)
        else:
            by_category['OTHER'].append(file)

    for category in sorted(by_category.keys()):
        files = by_category[category]
        print(f"\n[{category}] - {len(files)} files")
        print("-" * 80)
        for file in sorted(files):
            print(f"  {file}")

    print(f"\n\nTotal: {len(isolated)} isolated files")

if __name__ == '__main__':
    main()
