---
type: readme
title: "Especificacoes Tecnicas - @carf/tscore"
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
status: rejected
updated: 2026-01-22
source: "interno"
---

# Especificacoes Tecnicas - @carf/tscore

Documentacao tecnica detalhada das configuracoes de projeto necessarias para build, desenvolvimento e publicacao da biblioteca.

## Documentos

| ID | Titulo | Descricao |
|:---|:-------|:----------|
| 01-package-json | Package.json | Dependencias, exports e configuracao npm |
| 02-tsconfig | TSConfig | Configuracao do compilador TypeScript |
| 03-exports-map | Exports Map | Subpath exports e tree-shaking |

## Visao Geral

A biblioteca @carf/tscore e configurada para:

- **Build**: Bun + TypeScript para compilacao rapida
- **Output**: ES Modules (ESM) com TypeScript declarations
- **Publicacao**: GitHub Packages (@carf scope)
- **Peer Dependencies**: React e Vue opcionais

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
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (3)

| Documento | Status |
|-----------|--------|
| [Package.json - @carf/tscore](./01-package-json.md) | ⚠ |
| [TSConfig - @carf/tscore](./02-tsconfig.md) | ⚠ |
| [Exports Map - @carf/tscore](./03-exports-map.md) | ⚠ |

<!-- CARF-INDEX-END -->
