---
title: "Especificacoes Tecnicas - @carf/geoapi-client"
description: "Configuracoes de projeto, dependencias e build para o cliente HTTP"
status: review
updated: 2026-01-20
source: "interno"
---

# Especificacoes Tecnicas - @carf/geoapi-client

Documentacao tecnica detalhada das configuracoes de projeto necessarias para build, desenvolvimento e publicacao do cliente HTTP.

## Documentos

| ID | Titulo | Descricao |
|:---|:-------|:----------|
| 01-package-json | Package.json | Dependencias, exports e configuracao npm |
| 02-client-config | Configuracao do Cliente | Interface unificada de configuracao |

## Visao Geral

O @carf/geoapi-client e configurado para:

- **Build**: Bun + TypeScript com Vitest para testes
- **Output**: ES Modules (ESM) com TypeScript declarations
- **Publicacao**: GitHub Packages (@carf scope)
- **Dependencias**: axios para HTTP, @carf/tscore para types/auth

## Requisitos de Ambiente

```bash
# Versoes minimas
node >= 18.0.0
bun >= 1.0.0
```

## Comandos Principais

```bash
# Instalar dependencias
bun install

# Build
bun run build

# Testes
bun test

# Type check
tsc --noEmit
```

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/SPECS/01-package-json.md|Package.json - @carf/geoapi-client]]
- ○ [[PROJECTS/LIB/TS/GEOAPI-CLIENT/DOCS/SPECS/02-client-config.md|Configuracao do Cliente - @carf/geoapi-client]]

<!-- CARF-INDEX-END -->
