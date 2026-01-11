#!/usr/bin/env python3
"""
Connect all remaining isolated files systematically
"""

from pathlib import Path

def link_src_code_readmes():
    """Link SRC-CODE READMEs from project main READMEs"""

    updates = []

    # GEOAPI SRC-CODE README
    geoapi_readme = Path('PROJECTS/GEOAPI/DOCS/README.md')
    if geoapi_readme.exists():
        content = geoapi_readme.read_text(encoding='utf-8')
        if 'SRC-CODE' not in content and '../SRC-CODE' not in content:
            # Add reference to SRC-CODE
            footer_marker = '**Última atualização:**'
            if footer_marker in content:
                insertion = '\n## Código Fonte\n\nVer [carf-geoapi README](../SRC-CODE/carf-geoapi/README.md) para instruções de build, instalação e desenvolvimento local.\n\n---\n\n'
                content = content.replace(f'\n---\n\n{footer_marker}', insertion + footer_marker)
                geoapi_readme.write_text(content, encoding='utf-8')
                updates.append('GEOAPI/DOCS/README.md')

    # GEOGIS SRC-CODE README
    geogis_readme = Path('PROJECTS/GEOGIS/DOCS/README.md')
    if geogis_readme.exists():
        content = geogis_readme.read_text(encoding='utf-8')
        if 'SRC-CODE' not in content and '../SRC-CODE' not in content:
            footer_marker = '**Última atualização:**'
            if footer_marker in content:
                insertion = '\n## Código Fonte\n\nVer [carf-geogis README](../SRC-CODE/carf-geogis/README.md) para instruções de instalação do plugin e desenvolvimento local.\n\n---\n\n'
                content = content.replace(f'\n---\n\n{footer_marker}', insertion + footer_marker)
                geogis_readme.write_text(content, encoding='utf-8')
                updates.append('GEOGIS/DOCS/README.md')

    return updates

def link_architecture_files():
    """Link isolated ARCHITECTURE files from project READMEs"""

    updates = []

    # GEOWEB ARCHITECTURE/01-keycloak-integration.md
    geoweb_arch_readme = Path('PROJECTS/GEOWEB/DOCS/ARCHITECTURE/README.md')
    if geoweb_arch_readme.exists():
        content = geoweb_arch_readme.read_text(encoding='utf-8')
        if '01-keycloak-integration.md' not in content:
            # Add link to keycloak integration
            content = content.replace(
                '## Documentação',
                '## Integração Keycloak\n\n- **[01-keycloak-integration.md](./01-keycloak-integration.md)** - Integração OAuth2/OIDC Keycloak no GEOWEB\n\n## Documentação'
            )
            geoweb_arch_readme.write_text(content, encoding='utf-8')
            updates.append('GEOWEB/DOCS/ARCHITECTURE/README.md')

    return updates

def main():
    print("Connecting remaining isolated files...")
    print("=" * 80)

    all_updates = []

    print("\n[1/2] Linking SRC-CODE READMEs...")
    updates = link_src_code_readmes()
    all_updates.extend(updates)
    for file in updates:
        print(f"  [OK] {file}")

    print("\n[2/2] Linking ARCHITECTURE files...")
    updates = link_architecture_files()
    all_updates.extend(updates)
    for file in updates:
        print(f"  [OK] {file}")

    print("\n" + "=" * 80)
    print(f"Total files updated: {len(all_updates)}")

    if all_updates:
        print("\nUpdated files:")
        for file in all_updates:
            print(f"  - {file}")

if __name__ == '__main__':
    main()
