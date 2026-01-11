#!/usr/bin/env python3
"""
Connect the final 13 completely isolated files
"""

from pathlib import Path

def connect_keycloak_files():
    """Connect KEYCLOAK SRC-CODE technical files"""
    readme = Path('PROJECTS/KEYCLOAK/README.md')

    if not readme.exists():
        # KEYCLOAK doesn't have a main README, create reference in DOCS
        docs_readme = Path('CENTRAL/INTEGRATION/KEYCLOAK/README.md')
        if docs_readme.exists():
            content = docs_readme.read_text(encoding='utf-8')
            if 'BUILD.md' not in content:
                insertion = '''
## Documentação Técnica do Tema

Ver arquivos no diretório SRC-CODE do tema customizado:
- [BUILD.md](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/BUILD.md) - Instruções de build do tema
- [CHANGELOG.md](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/CHANGELOG.md) - Histórico de versões do tema
- [tests/README.md](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/tests/README.md) - Testes do tema customizado

### Recursos do Tema

- [Imagens](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/login/resources/img/README.md) - Assets de imagens do tema
- [JavaScript](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/login/resources/js/README.md) - Scripts customizados do tema

'''
                content = content.replace('\n---\n\n**Última atualização:**', insertion + '---\n\n**Última atualização:**')
                docs_readme.write_text(content, encoding='utf-8')
                return True
    return False

def connect_tscore_changelog():
    """Connect TSCORE CHANGELOG"""
    readme = Path('PROJECTS/LIB/TS/TSCORE/DOCS/README.md')
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        if 'CHANGELOG' not in content:
            insertion = '\n## Changelog\n\nVer [CHANGELOG.md](../SRC-CODE/carf-tscore/CHANGELOG.md) para histórico completo de versões e mudanças.\n\n'
            content = content.replace('\n---\n\n**Última atualização:**', insertion + '---\n\n**Última atualização:**')
            readme.write_text(content, encoding='utf-8')
            return True
    return False

def connect_webdocs_structure():
    """Connect WEBDOCS SRC-CODE structure files"""
    readme = Path('PROJECTS/WEBDOCS/SRC-CODE/carf-webdocs/README.md')

    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        if 'webdocs/src/README.md' not in content:
            insertion = '''
## Estrutura do Projeto

Ver documentação da estrutura VitePress:
- [webdocs/src/README.md](./webdocs/src/README.md) - Estrutura de diretórios do VitePress
- [webdocs/src/public/README.md](./webdocs/src/public/README.md) - Assets públicos

### Conteúdo Público

- [api/](./webdocs/src/public/api/README.md) - Exemplos de endpoints da API
- [funcionalidades/](./webdocs/src/public/funcionalidades/README.md) - Demonstrações de features
- [requisitos/](./webdocs/src/public/requisitos/README.md) - Documentação de requisitos
- [roadmap/](./webdocs/src/public/roadmap/README.md) - Roadmap do projeto

### Scripts

- [scripts/](./webdocs/src/scripts/README.md) - Scripts de build e deploy

'''
            # Find a good place to insert - after any existing sections
            if '## ' in content:
                # Insert before last section or at end
                parts = content.rsplit('\n## ', 1)
                if len(parts) == 2:
                    content = parts[0] + insertion + '\n## ' + parts[1]
                else:
                    content = content.rstrip() + '\n\n' + insertion
            else:
                content = content.rstrip() + '\n\n' + insertion

            readme.write_text(content, encoding='utf-8')
            return True
    return False

def main():
    print("Connecting final 13 completely isolated files...")
    print("=" * 80)

    updates = []

    print("\n[1/3] KEYCLOAK technical files...")
    if connect_keycloak_files():
        updates.append('KEYCLOAK docs')
        print("  [OK] 5 files connected via CENTRAL/INTEGRATION/KEYCLOAK/README.md")
    else:
        print("  [SKIP] Already connected")

    print("\n[2/3] TSCORE CHANGELOG...")
    if connect_tscore_changelog():
        updates.append('TSCORE CHANGELOG')
        print("  [OK] Connected via TSCORE/DOCS/README.md")
    else:
        print("  [SKIP] Already connected")

    print("\n[3/3] WEBDOCS structure files...")
    if connect_webdocs_structure():
        updates.append('WEBDOCS structure')
        print("  [OK] 7 files connected via WEBDOCS SRC-CODE README")
    else:
        print("  [SKIP] Already connected")

    print("\n" + "=" * 80)
    print(f"Total categories updated: {len(updates)}")
    print("\nAll 13 files should now be connected!")

if __name__ == '__main__':
    main()
