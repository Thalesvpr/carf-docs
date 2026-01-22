---
type: leaf
title: "Package.json - @carf/tscore"
status: review
updated: 2026-01-21
source: "CENTRAL/LIBRARIES/01-tscore.md"
---

# Package.json - @carf/tscore

Configuracao completa do package.json para a biblioteca core TypeScript.

## Configuracao Completa

```json
{
  "name": "@carf/tscore",
  "version": "0.1.0",
  "description": "Biblioteca core TypeScript compartilhada do ecossistema CARF - validacoes, types e autenticacao",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    },
    "./validations": {
      "types": "./dist/validations/index.d.ts",
      "import": "./dist/validations/index.js"
    },
    "./types": {
      "types": "./dist/types/index.d.ts",
      "import": "./dist/types/index.js"
    },
    "./auth": {
      "types": "./dist/auth/index.d.ts",
      "import": "./dist/auth/index.js"
    },
    "./auth/react": {
      "types": "./dist/auth/react/index.d.ts",
      "import": "./dist/auth/react/index.js"
    },
    "./auth/vue": {
      "types": "./dist/auth/vue/index.d.ts",
      "import": "./dist/auth/vue/index.js"
    }
  },
  "files": [
    "dist",
    "README.md"
  ],
  "scripts": {
    "build": "bun build ./src/index.ts --outdir ./dist --target node --format esm && tsc --emitDeclarationOnly",
    "test": "bun test",
    "test:coverage": "bun test --coverage",
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist",
    "prepublishOnly": "bun run build"
  },
  "dependencies": {
    "zod": "3.22.4"
  },
  "peerDependencies": {
    "react": "18.2.0",
    "vue": "3.4.15"
  },
  "peerDependenciesMeta": {
    "react": {
      "optional": true
    },
    "vue": {
      "optional": true
    }
  },
  "devDependencies": {
    "typescript": "5.3.3",
    "bun-types": "1.0.25",
    "@types/node": "20.11.5",
    "eslint": "8.56.0",
    "@typescript-eslint/eslint-plugin": "6.19.0",
    "@typescript-eslint/parser": "6.19.0"
  },
  "publishConfig": {
    "registry": "https://npm.pkg.github.com"
  },
  "repository": {
    "type": "git",
    "url": "https://github.com/carf/carf-tscore.git"
  },
  "keywords": [
    "carf",
    "typescript",
    "validation",
    "cpf",
    "cnpj",
    "keycloak",
    "auth"
  ],
  "author": "CARF Team",
  "license": "MIT",
  "engines": {
    "node": ">=18.0.0"
  }
}
```

## Dependencias

### Producao

| Pacote | Versao | Justificativa |
|:-------|:-------|:--------------|
| zod | 3.22.4 | Validacao de schemas TypeScript-first com inferencia de tipos |

### Peer Dependencies (Opcionais)

| Pacote | Versao | Quando Necessario |
|:-------|:-------|:------------------|
| react | 18.2.0 | Usar hooks de `@carf/tscore/auth/react` |
| vue | 3.4.15 | Usar composables de `@carf/tscore/auth/vue` |

### Desenvolvimento

| Pacote | Versao | Uso |
|:-------|:-------|:----|
| typescript | 5.3.3 | Compilador e type checking |
| bun-types | 1.0.25 | Types para runtime Bun |
| @types/node | 20.11.5 | Types Node.js |
| eslint | 8.56.0 | Linting |
| @typescript-eslint/* | 6.19.0 | ESLint para TypeScript |

## Scripts

### `build`

Compila TypeScript para JavaScript ES Modules:

```bash
bun run build
```

**Saida:**
- `dist/*.js` - Modulos JavaScript
- `dist/*.d.ts` - Declaracoes TypeScript

### `test`

Executa suite de testes com Bun:

```bash
bun test
```

### `test:coverage`

Executa testes com relatorio de cobertura:

```bash
bun test --coverage
```

**Meta:** >= 80% de cobertura

### `type-check`

Valida tipos sem gerar arquivos:

```bash
bun run type-check
```

## Instalacao em Projetos Consumidores

### Configurar Registry

Criar `.npmrc` na raiz do projeto:

```ini
@carf:registry=https://npm.pkg.github.com
//npm.pkg.github.com/:_authToken=${GITHUB_TOKEN}
```

### Instalar

```bash
# Instalar biblioteca
bun add @carf/tscore

# Se usar React hooks
bun add react@18.2.0

# Se usar Vue composables
bun add vue@3.4.15
```

## Versionamento

Segue Semantic Versioning (SemVer):

- **MAJOR** (1.0.0): Breaking changes (alteracao de assinaturas, remocao de metodos)
- **MINOR** (0.2.0): Novas features backward-compatible
- **PATCH** (0.1.1): Bug fixes

## Publicacao

```bash
# 1. Atualizar versao
npm version patch  # ou minor, major

# 2. Push tag
git push --follow-tags

# 3. CI/CD publica automaticamente
# ou manual: npm publish
```
