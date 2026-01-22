---
type: readme
title: "Bibliotecas TypeScript"
description: "Bibliotecas TypeScript compartilhadas do ecossistema CARF"
status: review
updated: 2026-01-20
source: "interno"
---

# Bibliotecas TypeScript

Bibliotecas TypeScript compartilhadas entre GEOWEB, REURBCAD, ADMIN e outras aplicacoes.

## Bibliotecas Disponiveis

| Biblioteca | Pacote | Descricao | Status |
|:-----------|:-------|:----------|:-------|
| [TSCORE](./TSCORE/README.md) | @carf/tscore | Value objects e validacoes | Especificado |
| [GEOAPI-CLIENT](./GEOAPI-CLIENT/README.md) | @carf/geoapi-client | HTTP client para GEOAPI | Especificado |
| [UI-COMPONENTS](./UI-COMPONENTS/README.md) | @carf/ui | Componentes React | Especificado |

## Dependencias

```
@carf/ui
    └── @carf/tscore (types)
        └── zod (validations)

@carf/geoapi-client
    ├── @carf/tscore (types)
    └── axios (http)
```

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/GEOAPI-CLIENT/README|GEOAPI-CLIENT]]
- [[PROJECTS/LIB/TS/TSCORE/README|TSCORE]]
- [[PROJECTS/LIB/TS/UI-COMPONENTS/README|UI-COMPONENTS]]

<!-- CARF-INDEX-END -->
