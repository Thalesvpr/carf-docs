#!/usr/bin/env python3
"""
Final script to connect all remaining isolated files
"""

from pathlib import Path

def update_geoweb_src_link():
    """Link GEOWEB SRC-CODE README"""
    readme = Path('PROJECTS/GEOWEB/DOCS/README.md')
    content = readme.read_text(encoding='utf-8')

    if '../SRC-CODE' not in content:
        insertion = '\n## Código Fonte\n\nVer [carf-geoweb README](../SRC-CODE/carf-geoweb/README.md) para instruções de build, instalação e desenvolvimento local.\n\n---\n\n'
        content = content.replace('\n---\n\n**Última atualização:**', insertion + '**Última atualização:**')
        readme.write_text(content, encoding='utf-8')
        return True
    return False

def update_reurbcad_docs():
    """Update REURBCAD documentation READMEs"""

    # Link main sections from REURBCAD/DOCS/README.md
    readme = Path('PROJECTS/REURBCAD/DOCS/README.md')
    content = readme.read_text(encoding='utf-8')

    if '## Documentação' not in content or 'ARCHITECTURE/README.md' not in content:
        insertion = '''
## Documentação

- **[Arquitetura](./ARCHITECTURE/README.md)** - Decisões técnicas de integração Keycloak offline-first
- **[Conceitos](./CONCEPTS/README.md)** - Autenticação offline, secure storage, sync
- **[Guias Práticos](./HOW-TO/README.md)** - Setup Keycloak mobile, handle callbacks, test offline
- **[Camadas](./LAYERS/README.md)** - Estrutura de código React Native (AuthService, Storage, Sync)

'''
        # Find where to insert (before Stack Tecnológico)
        content = content.replace('## Stack Tecnológico', insertion + '## Stack Tecnológico')
        readme.write_text(content, encoding='utf-8')

    # ARCHITECTURE/README.md
    arch = Path('PROJECTS/REURBCAD/DOCS/ARCHITECTURE/README.md')
    arch_content = """# ARCHITECTURE - REURBCAD

Arquitetura do aplicativo mobile REURBCAD React Native + Expo.

## Integração Keycloak

- **[01-keycloak-integration.md](./01-keycloak-integration.md)** - OAuth2/OIDC em React Native, deep linking, PKCE flow, token storage seguro

**Mobile-specific challenges:**
- Deep linking para callback OAuth
- Secure storage via expo-secure-store
- Offline token refresh
- Biometric authentication

---

**Última atualização:** 2026-01-10
"""
    arch.write_text(arch_content, encoding='utf-8')

    # CONCEPTS/README.md
    concepts = Path('PROJECTS/REURBCAD/DOCS/CONCEPTS/README.md')
    if concepts.exists():
        concepts_content = concepts.read_text(encoding='utf-8')
        if '01-authentication.md' not in concepts_content:
            concepts_content = """# CONCEPTS - REURBCAD

Conceitos fundamentais do REURBCAD React Native.

## Autenticação e Segurança

- **[01-authentication.md](./01-authentication.md)** - OAuth2 em React Native, deep linking, authorization code flow
- **[02-offline-authentication.md](./02-offline-authentication.md)** - Autenticação offline, cached tokens, biometric unlock
- **[03-secure-storage.md](./03-secure-storage.md)** - expo-secure-store, Keychain (iOS), KeyStore (Android)

## Offline-First

**WatermelonDB** - SQLite local database, reactive queries, sync protocol

**Sync Strategy** - Last-write-wins, conflict detection, merge strategies

---

**Última atualização:** 2026-01-10
"""
            concepts.write_text(concepts_content, encoding='utf-8')

    # HOW-TO/README.md
    howto = Path('PROJECTS/REURBCAD/DOCS/HOW-TO/README.md')
    howto_content = """# HOW-TO - REURBCAD

Guias práticos para desenvolvimento do REURBCAD React Native.

## Autenticação

- **[01-setup-keycloak.md](./01-setup-keycloak.md)** - Configurar Keycloak redirect URIs para deep links (exp://...)
- **[02-handle-callbacks.md](./02-handle-callbacks.md)** - Configurar deep linking, Linking.addEventListener, parse authorization code
- **[03-test-offline.md](./03-test-offline.md)** - Testar autenticação offline, biometric, token refresh

## Desenvolvimento Local

**Setup:**
1. `npm install` ou `yarn install`
2. Configurar `.env` com KEYCLOAK_URL, GEOAPI_URL
3. `npx expo start` para iniciar Metro bundler
4. Executar em emulador ou device físico

**Build:**
- Android: `eas build --platform android`
- iOS: `eas build --platform ios`

---

**Última atualização:** 2026-01-10
"""
    howto.write_text(howto_content, encoding='utf-8')

    # LAYERS/README.md
    layers = Path('PROJECTS/REURBCAD/DOCS/LAYERS/README.md')
    layers_content = """# LAYERS - REURBCAD

Estrutura de camadas do código React Native do REURBCAD.

## Camadas da Aplicação

### Auth Service

- **[01-auth-service.md](./01-auth-service.md)** - AuthService class, OAuth2 flow, token management, secure storage

**Responsabilidades:**
- Gerenciar OAuth2 authorization code flow
- Store tokens em expo-secure-store
- Refresh tokens automaticamente
- Biometric authentication

### Offline Storage

**WatermelonDB:**
- Models (Unit, Holder, Community, Photo)
- Sync adapter para GEOAPI
- Query reactive observers

### Sync Service

**Conflict Resolution:**
- Detect conflits via timestamps
- Merge strategies (last-write-wins, manual)
- Batch sync para performance

### UI Components

**React Native components:**
- Navigation stack (React Navigation)
- Maps (react-native-maps)
- Camera (expo-camera)
- Forms com validation

---

**Última atualização:** 2026-01-10
"""
    layers.write_text(layers_content, encoding='utf-8')

    # Link SRC-CODE
    readme = Path('PROJECTS/REURBCAD/DOCS/README.md')
    content = readme.read_text(encoding='utf-8')
    if '../SRC-CODE' not in content:
        insertion = '\n## Código Fonte\n\nVer [carf-reurbcad README](../SRC-CODE/carf-reurbcad/README.md) para instruções de build, instalação e desenvolvimento mobile.\n\n---\n\n'
        content = content.replace('\n---\n\n**Última atualização:**', insertion + '**Última atualização:**')
        readme.write_text(content, encoding='utf-8')

    return True

def update_webdocs_features():
    """Link WEBDOCS FEATURES README"""
    # Create minimal README linking from WEBDOCS/DOCS/README.md
    main_readme = Path('PROJECTS/WEBDOCS/DOCS/README.md')
    if main_readme.exists():
        content = main_readme.read_text(encoding='utf-8')
        if 'FEATURES/' not in content:
            insertion = '\n## Features\n\nVer [FEATURES/](./FEATURES/README.md) para exemplos interativos de documentação.\n\n'
            content = content.replace('\n---\n', insertion + '---\n')
            main_readme.write_text(content, encoding='utf-8')

    # Link SRC-CODE
    if '..SRC-CODE' not in content:
        insertion = '\n## Código Fonte\n\nVer [carf-webdocs README](../SRC-CODE/carf-webdocs/README.md) para build e deploy do VitePress.\n\n---\n\n'
        content = content.replace('\n---\n\n**Última atualização:**', insertion + '**Última atualização:**')
        main_readme.write_text(content, encoding='utf-8')

    return True

def link_keycloak_files():
    """Link KEYCLOAK SRC-CODE files from KEYCLOAK README"""
    readme = Path('PROJECTS/KEYCLOAK/README.md')
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        if 'BUILD.md' not in content:
            insertion = '''
## Documentação Técnica

Ver também arquivos no SRC-CODE:
- [BUILD.md](./SRC-CODE/carf-keycloak/BUILD.md) - Instruções de build do tema customizado
- [CHANGELOG.md](./SRC-CODE/carf-keycloak/CHANGELOG.md) - Histórico de mudanças
- [tests/README.md](./SRC-CODE/carf-keycloak/tests/README.md) - Testes do tema

'''
            content = content.replace('\n---\n', insertion + '---\n')
            readme.write_text(content, encoding='utf-8')
            return True
    return False

def link_tscore_changelog():
    """Link TSCORE CHANGELOG"""
    readme = Path('PROJECTS/LIB/TS/TSCORE/DOCS/README.md')
    if readme.exists():
        content = readme.read_text(encoding='utf-8')
        if 'CHANGELOG' not in content:
            insertion = '\n## Changelog\n\nVer [CHANGELOG.md](../SRC-CODE/carf-tscore/CHANGELOG.md) para histórico de versões.\n\n'
            content = content.replace('\n---\n', insertion + '---\n')
            readme.write_text(content, encoding='utf-8')
            return True
    return False

def main():
    print("Final connection of all remaining isolated files...")
    print("=" * 80)

    updates = []

    print("\n[1/6] GEOWEB SRC-CODE link...")
    if update_geoweb_src_link():
        updates.append('GEOWEB/DOCS/README.md')
        print("  [OK] Linked")

    print("\n[2/6] REURBCAD documentation...")
    if update_reurbcad_docs():
        updates.extend(['REURBCAD/DOCS/README.md', 'REURBCAD/DOCS/ARCHITECTURE/README.md',
                       'REURBCAD/DOCS/CONCEPTS/README.md', 'REURBCAD/DOCS/HOW-TO/README.md',
                       'REURBCAD/DOCS/LAYERS/README.md'])
        print("  [OK] Updated")

    print("\n[3/6] WEBDOCS features...")
    if update_webdocs_features():
        updates.append('WEBDOCS/DOCS/README.md')
        print("  [OK] Linked")

    print("\n[4/6] KEYCLOAK technical docs...")
    if link_keycloak_files():
        updates.append('KEYCLOAK/README.md')
        print("  [OK] Linked")

    print("\n[5/6] TSCORE changelog...")
    if link_tscore_changelog():
        updates.append('LIB/TS/TSCORE/DOCS/README.md')
        print("  [OK] Linked")

    print("\n" + "=" * 80)
    print(f"Total updates: {len(updates)}")

if __name__ == '__main__':
    main()
