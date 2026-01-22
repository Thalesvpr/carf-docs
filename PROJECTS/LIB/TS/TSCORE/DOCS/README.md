---
title: "Documentacao @carf/tscore"
description: "README usa listas/tabelas ao invés de prosa densa com links inline."
status: rejected
updated: 2026-01-22
source: "interno"
---

# Documentacao @carf/tscore

Documentacao tecnica completa da biblioteca core TypeScript com value objects, validacoes e tipos compartilhados.

## Secoes

| Secao | Descricao |
|:------|:----------|
| [SPECS/](./SPECS/README.md) | Especificacoes tecnicas (package.json, tsconfig) |
| [ADRs/](./ADRs/README.md) | Decisoes arquiteturais |
| [ARCHITECTURE/](./ARCHITECTURE/README.md) | Arquitetura e design |
| [CONCEPTS/](./CONCEPTS/README.md) | Value objects, validacoes, tipos |
| [API/](./API/README.md) | Referencia completa de API |
| [HOW-TO/](./HOW-TO/README.md) | Guias praticos |

## Modulos da Biblioteca

| Modulo | Export Path | Descricao |
|:-------|:------------|:----------|
| Validations | `@carf/tscore/validations` | CPF, CNPJ, Email, Phone |
| Types | `@carf/tscore/types` | Unit, Holder, Community, DTOs |
| Auth React | `@carf/tscore/auth/react` | useAuth, ProtectedRoute |
| Auth Vue | `@carf/tscore/auth/vue` | useAuth composable |

## Instalacao Rapida

```bash
# Configurar registry
echo "@carf:registry=https://npm.pkg.github.com" >> .npmrc

# Instalar
bun add @carf/tscore
```

## Status de Especificacao

| Secao | Arquivos | Status |
|:------|:---------|:-------|
| SPECS | 3 | Completo |
| ADRs | 1 | Completo |
| ARCHITECTURE | 1 | Existente |
| CONCEPTS | 3 | Existente |
| API | 3 | Completo |
| HOW-TO | 3 | Completo |

<!-- CARF-INDEX-START -->
## Subpastas

- [[PROJECTS/LIB/TS/TSCORE/DOCS/ADRs/README|ADRs]]
- [[PROJECTS/LIB/TS/TSCORE/DOCS/API/README|API]]
- [[PROJECTS/LIB/TS/TSCORE/DOCS/ARCHITECTURE/README|ARCHITECTURE]]
- [[PROJECTS/LIB/TS/TSCORE/DOCS/CONCEPTS/README|CONCEPTS]]
- [[PROJECTS/LIB/TS/TSCORE/DOCS/HOW-TO/README|HOW-TO]]
- [[PROJECTS/LIB/TS/TSCORE/DOCS/SPECS/README|SPECS]]

<!-- CARF-INDEX-END -->
