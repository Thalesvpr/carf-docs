---
title: "LIB - Bibliotecas Compartilhadas"
description: "Bibliotecas TypeScript compartilhadas entre aplicacoes do ecossistema CARF"
status: review
updated: 2026-01-20
source: "interno"
---

# LIB - Bibliotecas Compartilhadas

Bibliotecas TypeScript compartilhadas entre todas as aplicacoes do ecossistema CARF: GEOWEB, REURBCAD, ADMIN, etc.

## Bibliotecas

Ver **[TS/](./TS/README.md)** para indice completo. Resumo:

| Pacote | Descricao |
|:-------|:----------|
| @carf/tscore | Value objects, validacoes e tipos compartilhados |
| @carf/geoapi-client | HTTP client type-safe para GEOAPI |
| @carf/ui | Componentes React baseados em shadcn/ui |

## Arquitetura

```
LIB/
└── TS/                           # Bibliotecas TypeScript
    ├── TSCORE/                   # @carf/tscore
    │   └── DOCS/                 # Documentacao
    │       ├── SPECS/            # Especificacoes tecnicas
    │       ├── ARCHITECTURE/     # Arquitetura
    │       ├── CONCEPTS/         # Conceitos
    │       ├── API/              # Referencia de API
    │       └── HOW-TO/           # Guias praticos
    ├── GEOAPI-CLIENT/            # @carf/geoapi-client
    │   └── DOCS/                 # Documentacao
    └── UI-COMPONENTS/            # @carf/ui
        └── DOCS/                 # Documentacao
```

## Publicacao

Todas as bibliotecas sao publicadas no GitHub Packages com scope `@carf`:

```bash
# Configurar registry
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/tscore @carf/geoapi-client @carf/ui
```

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/README|TS]]

<!-- CARF-INDEX-END -->
