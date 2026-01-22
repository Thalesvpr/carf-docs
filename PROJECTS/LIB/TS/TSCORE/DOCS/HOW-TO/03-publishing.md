---
type: leaf
title: "Publicacao - @carf/tscore"
status: review
updated: 2026-01-21
source: "interno"
---

# Publicacao - @carf/tscore

Guia para publicar novas versoes da biblioteca no GitHub Packages.

## Pre-requisitos

### GitHub Token

Token com permissao `write:packages`:

1. GitHub > Settings > Developer Settings > Personal Access Tokens
2. Gerar token com scopes: `write:packages`, `read:packages`
3. Salvar token em local seguro

### Configurar .npmrc

```ini
# ~/.npmrc
@carf:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=ghp_xxxxxxxxxxxxxxxxxxxx
```

Ou via variavel de ambiente:

```ini
# ~/.npmrc
@carf:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

## Versionamento Semantico

Seguir [SemVer](https://semver.org/):

| Tipo | Quando Usar | Exemplo |
|:-----|:------------|:--------|
| PATCH | Bug fixes, ajustes internos | 0.1.0 → 0.1.1 |
| MINOR | Nova feature backward-compatible | 0.1.0 → 0.2.0 |
| MAJOR | Breaking changes | 0.1.0 → 1.0.0 |

### Exemplos de Breaking Changes

- Alterar assinatura de metodo publico
- Remover metodo/propriedade publica
- Alterar comportamento de validacao existente
- Renomear exports

### Exemplos de Minor Changes

- Adicionar novo Value Object (CEP, etc.)
- Adicionar campo opcional a interface
- Novo hook React/Vue
- Nova funcao utilitaria

### Exemplos de Patch Changes

- Corrigir bug em validacao
- Melhorar mensagem de erro
- Corrigir edge case
- Atualizar documentacao

## Processo de Release

### 1. Garantir que Main esta Atualizado

```bash
git checkout main
git pull origin main
```

### 2. Verificar que Tudo Passa

```bash
# Rodar todos os checks
bun test
bun run lint
bun run type-check
bun run build

# Verificar que dist/ foi gerado
ls dist/
```

### 3. Atualizar Versao

```bash
# Patch (0.1.0 → 0.1.1)
npm version patch

# Minor (0.1.0 → 0.2.0)
npm version minor

# Major (0.1.0 → 1.0.0)
npm version major
```

Este comando:
- Atualiza `version` no package.json
- Cria commit automatico
- Cria git tag (v0.1.1)

### 4. Push com Tags

```bash
git push origin main --follow-tags
```

### 5. Publicar

**Manualmente:**

```bash
npm publish
```

**Via CI/CD (recomendado):**

O workflow automatico publica quando tag e criada.

## CI/CD Automatizado

### GitHub Actions Workflow

`.github/workflows/publish.yml`:

```yaml
name: Publish Package

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install

      - name: Run tests
        run: bun test

      - name: Run lint
        run: bun run lint

      - name: Type check
        run: bun run type-check

      - name: Build
        run: bun run build

      - name: Configure npm
        run: |
          echo "@carf:registry=https://npm.pkg.github.com" >> ~/.npmrc
          echo "//npm.pkg.github.com/:_authToken=${{ secrets.GITHUB_TOKEN }}" >> ~/.npmrc

      - name: Publish
        run: npm publish
        env:
          NODE_AUTH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Verificar Publicacao

### No GitHub

1. Ir para repositorio no GitHub
2. Aba "Packages" na sidebar direita
3. Verificar nova versao listada

### Via CLI

```bash
npm view @carf/tscore versions
```

### Instalar em Projeto

```bash
# Atualizar para ultima versao
bun add @carf/tscore@latest

# Instalar versao especifica
bun add @carf/tscore@0.2.0
```

## Comunicacao de Release

### CHANGELOG.md

Manter changelog atualizado:

```markdown
# Changelog

## [0.2.0] - 2026-01-20

### Added
- CEP value object for Brazilian postal codes
- `useToken` React hook for direct token access

### Changed
- Improved CPF validation error messages

### Fixed
- Email validation now accepts plus signs in local part

## [0.1.1] - 2026-01-15

### Fixed
- Phone validation edge case with 0800 numbers
```

### GitHub Release

1. Ir para Releases no GitHub
2. Clicar na tag recem criada
3. Adicionar release notes
4. Marcar como "Latest release"

## Rollback

Se publicou versao com problema:

### Deprecar Versao

```bash
npm deprecate @carf/tscore@0.2.0 "Bug critico, use 0.2.1"
```

### Unpublish (ate 72h apos publicacao)

```bash
npm unpublish @carf/tscore@0.2.0
```

**Atencao:** Unpublish so funciona se ninguem instalou a versao.

### Publicar Patch Corrigido

```bash
# Corrigir bug
git commit -m "fix: corrigir problema X"

# Publicar patch
npm version patch
git push origin main --follow-tags
npm publish
```

## Troubleshooting

### "402 Payment Required"

Verificar que package.json tem `publishConfig`:

```json
{
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  }
}
```

### "401 Unauthorized"

Token invalido ou sem permissao. Verificar:

1. Token tem scope `write:packages`
2. Token nao expirou
3. .npmrc configurado corretamente

### "403 Forbidden"

Usuario nao tem permissao no repositorio. Necessario:

- Ser collaborator do repositorio
- Ou ter permissao de packages na org
