#!/usr/bin/env python3
"""
Simple script to list completely isolated files
"""

from pathlib import Path
import re

def main():
    # Run check-links.py and parse output
    import subprocess
    result = subprocess.run(
        ['python', '.scripts/check-links.py'],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )

    output = result.stdout

    # Find the completely isolated section
    lines = output.split('\n')

    in_isolated_section = False
    isolated_files = []

    for line in lines:
        if 'COMPLETAMENTE ISOLADOS' in line:
            in_isolated_section = True
            continue

        if in_isolated_section:
            if 'ORFAOS' in line or 'ISOLADOS (' in line:
                break

            # Extract file paths
            if line.strip().startswith('- '):
                file_path = line.strip()[2:]  # Remove "- "
                isolated_files.append(file_path)

    print(f"Found {len(isolated_files)} completely isolated files:\n")

    # Group by project
    from collections import defaultdict
    by_project = defaultdict(list)

    for file in isolated_files:
        if 'CENTRAL/VERSIONING' in file or 'CENTRAL\\VERSIONING' in file:
            by_project['CENTRAL/VERSIONING'].append(file)
        elif 'PROJECTS/GEOAPI' in file or 'PROJECTS\\GEOAPI' in file:
            by_project['GEOAPI'].append(file)
        elif 'PROJECTS/GEOWEB' in file or 'PROJECTS\\GEOWEB' in file:
            by_project['GEOWEB'].append(file)
        elif 'PROJECTS/GEOGIS' in file or 'PROJECTS\\GEOGIS' in file:
            by_project['GEOGIS'].append(file)
        elif 'PROJECTS/REURBCAD' in file or 'PROJECTS\\REURBCAD' in file:
            by_project['REURBCAD'].append(file)
        elif 'PROJECTS/ADMIN' in file or 'PROJECTS\\ADMIN' in file:
            by_project['ADMIN'].append(file)
        elif 'PROJECTS/WEBDOCS' in file or 'PROJECTS\\WEBDOCS' in file:
            by_project['WEBDOCS'].append(file)
        elif 'PROJECTS/LIB' in file or 'PROJECTS\\LIB' in file:
            by_project['LIB'].append(file)
        else:
            by_project['OTHER'].append(file)

    for project in sorted(by_project.keys()):
        files = by_project[project]
        print(f"\n## {project} ({len(files)} files)")
        print("-" * 80)
        for f in files:
            print(f)

    print(f"\n\nTotal: {len(isolated_files)} files")

if __name__ == '__main__':
    main()
