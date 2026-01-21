---
title: "Package.json - @carf/geoapi-client"
status: review
updated: 2026-01-21
source: "CENTRAL/LIBRARIES/02-geoapi-client.md"
---

# Package.json - @carf/geoapi-client

Configuracao completa do package.json para o cliente HTTP da GEOAPI.

## Configuracao Completa

```json
{
  "name": "@carf/geoapi-client",
  "version": "0.1.0",
  "description": "Cliente HTTP type-safe para a GEOAPI do ecossistema CARF",
  "type": "module",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js"
    }
  },
  "files": [
    "dist",
    "README.md"
  ],
  "scripts": {
    "build": "bun build ./src/index.ts --outdir ./dist --target node --format esm && tsc --emitDeclarationOnly",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "type-check": "tsc --noEmit",
    "clean": "rm -rf dist",
    "prepublishOnly": "bun run build"
  },
  "dependencies": {
    "@carf/tscore": "0.1.0",
    "axios": "1.6.5",
    "axios-retry": "4.0.0"
  },
  "devDependencies": {
    "typescript": "5.3.3",
    "vitest": "1.2.0",
    "axios-mock-adapter": "1.22.0",
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
    "url": "https://github.com/carf/carf-geoapi-client.git"
  },
  "keywords": [
    "carf",
    "geoapi",
    "http-client",
    "typescript",
    "axios"
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
| @carf/tscore | 0.1.0 | Types, validacoes e auth Keycloak |
| axios | 1.6.5 | Cliente HTTP robusto com interceptors |
| axios-retry | 4.0.0 | Retry automatico com exponential backoff |

### Desenvolvimento

| Pacote | Versao | Uso |
|:-------|:-------|:----|
| typescript | 5.3.3 | Compilador e type checking |
| vitest | 1.2.0 | Framework de testes |
| axios-mock-adapter | 1.22.0 | Mock de requisicoes HTTP em testes |
| @types/node | 20.11.5 | Types Node.js |
| eslint | 8.56.0 | Linting |

## Scripts

### `build`

Compila TypeScript para JavaScript ES Modules:

```bash
bun run build
```

**Saida:**
- `dist/index.js` - Modulo JavaScript
- `dist/index.d.ts` - Declaracoes TypeScript

### `test`

Executa suite de testes com Vitest:

```bash
bun test
```

### `test:coverage`

Executa testes com relatorio de cobertura:

```bash
bun test:coverage
```

**Meta:** >= 80% de cobertura

### `test:watch`

Modo watch para desenvolvimento:

```bash
bun run test:watch
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
# Instalar biblioteca (inclui @carf/tscore como dependencia)
bun add @carf/geoapi-client
```

## Estrutura de Arquivos

```
src/
├── index.ts              # Entry point - exports GeoApiClient
├── client.ts             # Classe principal GeoApiClient
├── api/                  # APIs por dominio
│   ├── index.ts
│   ├── units.ts          # UnitsApi
│   ├── holders.ts        # HoldersApi
│   ├── communities.ts    # CommunitiesApi
│   ├── legitimation.ts   # LegitimationApi
│   ├── documents.ts      # DocumentsApi
│   └── reports.ts        # ReportsApi
├── interceptors/         # Axios interceptors
│   ├── auth.ts           # Adiciona token JWT
│   ├── retry.ts          # Retry logic
│   └── error.ts          # Error handling
├── errors/               # Classes de erro
│   ├── index.ts
│   ├── api-error.ts
│   ├── validation-error.ts
│   ├── not-found-error.ts
│   └── ...
└── types/                # Types internos
    ├── config.ts
    ├── request.ts
    └── response.ts
```

## Versionamento

Segue Semantic Versioning (SemVer):

- **MAJOR**: Breaking changes na API publica
- **MINOR**: Novas features backward-compatible
- **PATCH**: Bug fixes

## Publicacao

```bash
# 1. Atualizar versao
npm version patch  # ou minor, major

# 2. Push com tags
git push origin main --follow-tags

# 3. CI/CD publica automaticamente
```
