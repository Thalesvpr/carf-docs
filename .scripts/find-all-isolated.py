#!/usr/bin/env python3
"""
Find ALL completely isolated files (not just first 20)
"""

from pathlib import Path
import re
from collections import defaultdict

def find_markdown_files():
    """Find all markdown files"""
    root = Path('.')
    excluded = ['.git', 'node_modules', '.obsidian']

    files = []
    for md_file in root.rglob('*.md'):
        if any(exc in str(md_file) for exc in excluded):
            continue
        files.append(md_file)

    return files

def extract_links(file_path):
    """Extract markdown links from a file"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except:
        return []

    # Pattern for markdown links [text](path)
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)

    # Filter out external links
    internal_links = []
    for text, link in matches:
        if link.startswith('http://') or link.startswith('https://'):
            continue
        if link.startswith('#'):  # Internal anchor
            continue
        internal_links.append(link)

    return internal_links

def main():
    print("Analyzing all markdown files...")

    all_files = find_markdown_files()
    print(f"Found {len(all_files)} markdown files")

    # Build outgoing links map
    outgoing_links = {}
    for file in all_files:
        links = extract_links(file)
        outgoing_links[file] = links

    # Build incoming links map by checking all files
    incoming_links = defaultdict(set)

    for source_file in all_files:
        links = outgoing_links.get(source_file, [])

        for link in links:
            # Resolve link relative to source_file
            try:
                if link.startswith('./') or link.startswith('../'):
                    target_path = (source_file.parent / link).resolve()
                else:
                    target_path = Path(link).resolve()

                # Find matching file
                for candidate in all_files:
                    if candidate.resolve() == target_path:
                        incoming_links[candidate].add(source_file)
                        break
            except:
                pass

    # Find completely isolated files
    isolated = []

    for file in all_files:
        has_outgoing = len(outgoing_links.get(file, [])) > 0
        has_incoming = len(incoming_links.get(file, [])) > 0

        if not has_outgoing and not has_incoming:
            isolated.append(file)

    print(f"Found {len(isolated)} completely isolated files\n")

    # Group by category
    by_category = defaultdict(list)

    for file in isolated:
        path_str = str(file)

        if 'CENTRAL\\VERSIONING' in path_str or 'CENTRAL/VERSIONING' in path_str:
            by_category['CENTRAL/VERSIONING'].append(file)
        elif 'PROJECTS\\GEOAPI' in path_str or 'PROJECTS/GEOAPI' in path_str:
            by_category['GEOAPI'].append(file)
        elif 'PROJECTS\\GEOWEB' in path_str or 'PROJECTS/GEOWEB' in path_str:
            by_category['GEOWEB'].append(file)
        elif 'PROJECTS\\GEOGIS' in path_str or 'PROJECTS/GEOGIS' in path_str:
            by_category['GEOGIS'].append(file)
        elif 'PROJECTS\\REURBCAD' in path_str or 'PROJECTS/REURBCAD' in path_str:
            by_category['REURBCAD'].append(file)
        elif 'PROJECTS\\ADMIN' in path_str or 'PROJECTS/ADMIN' in path_str:
            by_category['ADMIN'].append(file)
        elif 'PROJECTS\\WEBDOCS' in path_str or 'PROJECTS/WEBDOCS' in path_str:
            by_category['WEBDOCS'].append(file)
        elif 'PROJECTS\\LIB' in path_str or 'PROJECTS/LIB' in path_str:
            by_category['LIB'].append(file)
        else:
            by_category['OTHER'].append(file)

    for category in sorted(by_category.keys()):
        files = by_category[category]
        print(f"\n## {category} ({len(files)} files)")
        print("=" * 80)
        for f in sorted(files):
            print(f"  {f}")

    print(f"\n\nTOTAL: {len(isolated)} completely isolated files")

if __name__ == '__main__':
    main()
