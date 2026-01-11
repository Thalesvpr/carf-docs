#!/usr/bin/env python3
"""
Fix all remaining broken links in documentation
"""

from pathlib import Path
import re

def fix_geoweb_overview():
    """Fix GEOWEB OVERVIEW.md broken feature links"""
    file_path = Path('PROJECTS/GEOWEB/DOCS/OVERVIEW.md')
    content = file_path.read_text(encoding='utf-8')

    # Remove broken feature links, replace with text
    old_text = '''Ver [FEATURES/](./FEATURES/README.md) para lista completa:
- [Map Integration](./FEATURES/map-integration.md) - Mapa interativo Leaflet
- [Offline Sync](./FEATURES/offline-sync.md) - Sincronização offline'''

    new_text = '''Ver [FEATURES/](./FEATURES/README.md) para lista completa de funcionalidades implementadas.'''

    content = content.replace(old_text, new_text)
    file_path.write_text(content, encoding='utf-8')
    print(f"[OK] Fixed {file_path}")

def fix_reurbcad_overview():
    """Fix REURBCAD OVERVIEW.md broken links"""
    file_path = Path('PROJECTS/REURBCAD/DOCS/OVERVIEW.md')
    content = file_path.read_text(encoding='utf-8')

    # Fix broken CONCEPTS link
    content = content.replace(
        '- [Offline-First Architecture](./CONCEPTS/offline-first.md)',
        '- Offline-First Architecture via WatermelonDB'
    )

    # Fix broken FEATURES link
    old_text = '''Ver [FEATURES/](./FEATURES/README.md):
- [Map Integration](./FEATURES/map-integration.md) - Mapas offline'''

    new_text = '''Ver [FEATURES/](./FEATURES/README.md) para funcionalidades implementadas.'''

    content = content.replace(old_text, new_text)
    file_path.write_text(content, encoding='utf-8')
    print(f"[OK] Fixed {file_path}")

def fix_geoapi_client_readme():
    """Fix GEOAPI-CLIENT README.md broken concept links"""
    file_path = Path('PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/README.md')
    content = file_path.read_text(encoding='utf-8')

    # Replace broken links with plain text
    content = content.replace(
        '- [02-interceptors.md](./CONCEPTS/02-interceptors.md)',
        '- Interceptors - Request/response interceptors'
    )
    content = content.replace(
        '- [03-type-safety.md](./CONCEPTS/03-type-safety.md)',
        '- Type Safety - TypeScript types gerados'
    )
    content = content.replace(
        '- [04-offline-support.md](./CONCEPTS/04-offline-support.md)',
        '- Offline Support - Queue de requisições'
    )

    file_path.write_text(content, encoding='utf-8')
    print(f"[OK] Fixed {file_path}")

def fix_tscore_concepts_readme():
    """Fix TSCORE CONCEPTS README.md broken link"""
    file_path = Path('PROJECTS/LIB/TS/TSCORE/DOCS/CONCEPTS/README.md')
    content = file_path.read_text(encoding='utf-8')

    # Replace broken link with plain text
    content = content.replace(
        '- **[Autenticação Keycloak](./02-keycloak-auth.md)** - Integração OAuth2/OIDC',
        '- **Autenticação Keycloak** - Integração OAuth2/OIDC (em desenvolvimento)'
    )

    file_path.write_text(content, encoding='utf-8')
    print(f"[OK] Fixed {file_path}")

def fix_ui_components_howto():
    """Fix UI-COMPONENTS HOW-TO broken link pattern"""
    file_path = Path('PROJECTS/LIB/TS/UI-COMPONENTS/DOCS/HOW-TO/01-setup-dev-environment.md')
    content = file_path.read_text(encoding='utf-8')

    # Fix malformed regex pattern in link
    # This is likely a malformed markdown link, replace entire section
    pattern = r'\[([^\]]+)\]\(\[\^"\'`\]\*\)'
    if re.search(pattern, content):
        content = re.sub(pattern, r'\1', content)
        file_path.write_text(content, encoding='utf-8')
        print(f"[OK] Fixed malformed link in {file_path}")

def fix_root_readme():
    """Fix root README.md folder links"""
    file_path = Path('README.md')
    content = file_path.read_text(encoding='utf-8')

    # Fix WEBDOCS folder link - point to README.md
    content = content.replace(
        '[Docs](./PROJECTS/WEBDOCS/DOCS/)',
        '[Docs](./PROJECTS/WEBDOCS/README.md)'
    )

    # Fix TSCORE folder link - point to README.md
    content = content.replace(
        '[Docs](./PROJECTS/LIB/TS/TSCORE/DOCS/)',
        '[Docs](./PROJECTS/LIB/TS/TSCORE/DOCS/README.md)'
    )

    file_path.write_text(content, encoding='utf-8')
    print(f"[OK] Fixed {file_path}")

def main():
    print("="*80)
    print("FIXING ALL BROKEN LINKS")
    print("="*80)

    fix_geoweb_overview()
    fix_reurbcad_overview()
    fix_geoapi_client_readme()
    fix_tscore_concepts_readme()
    fix_ui_components_howto()
    fix_root_readme()

    print("="*80)
    print("[OK] All broken links fixed!")
    print("="*80)

if __name__ == '__main__':
    main()
