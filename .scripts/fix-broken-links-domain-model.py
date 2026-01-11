"""Fix broken links in DOMAIN-MODEL READMEs"""
from pathlib import Path

# Fix VALUE-OBJECTS README
vo_readme = Path('CENTRAL/DOMAIN-MODEL/VALUE-OBJECTS/README.md')
content = vo_readme.read_text(encoding='utf-8')

# Fix incorrectly numbered links
replacements = {
    './02-cnpj.md': './02-geo-polygon.md',  # 02 is geo-polygon not cnpj
    './03-geo-polygon.md': './02-geo-polygon.md',  # duplicate, use correct number
    './04-coordinates.md': './07-geo-point.md',  # coordinates doesn't exist, closest is geo-point
    './05-unit-status.md': './03-unit-status.md',  # 05 is permissions-matrix, unit-status is 03
    './06-sync-status.md': './17-sync-status.md',  # 06 is spatial-overlap, sync-status is 17
    './21-legitimation-status.md': './22-legitimation-status.md',  # 21 is api-key-value
    './21-api-key-value.md': './21-api-key-value.md',  # keep this correct
    './22-decision.md': './23-decision.md',  # decision is 23
    './23-certificate-situation.md': './24-certificate-situation.md',  # certificate is 24
    './24-role.md': './25-role.md',  # role is 25
}

for old, new in replacements.items():
    content = content.replace(old, new)

vo_readme.write_text(content, encoding='utf-8')
print("Fixed VALUE-OBJECTS/README.md")

# Remove broken links from OVERVIEW.md files (features that don't exist)
overview_files = [
    'PROJECTS/ADMIN/DOCS/OVERVIEW.md',
    'PROJECTS/GEOGIS/DOCS/OVERVIEW.md',
]

for file_path_str in overview_files:
    file_path = Path(file_path_str)
    if not file_path.exists():
        continue

    content = file_path.read_text(encoding='utf-8')

    # Remove "Ver FEATURES section" for files that don't have FEATURES yet
    # Replace with simple text
    if 'ADMIN' in file_path_str:
        old_text = '''Ver [FEATURES/](./FEATURES/README.md):

- [Tenant Management](./FEATURES/tenant-management.md)
- [User Management](./FEATURES/user-management.md)'''
        new_text = '''Features documentadas em desenvolvimento.'''
        content = content.replace(old_text, new_text)

    elif 'GEOGIS' in file_path_str:
        old_text = '''Ver [FEATURES/](./FEATURES/README.md):

- [Shapefile Import/Export](./FEATURES/shapefile-operations.md)
- [Topological Validation](./FEATURES/topology-validation.md)'''
        new_text = '''Features principais:
- Shapefile Import/Export - Importação e exportação batch com validação topológica
- Topological Validation - Detecção de overlaps, gaps, slivers'''
        content = content.replace(old_text, new_text)

    file_path.write_text(content, encoding='utf-8')
    print(f"Fixed {file_path.name}")

print("\nDone!")
