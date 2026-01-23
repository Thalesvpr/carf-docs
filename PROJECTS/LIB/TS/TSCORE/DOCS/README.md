---
type: readme
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
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Subpastas (6)

| Pasta | Descrição |
|-------|-----------|
| [ADRs](./ADRs/README.md) | ... |
| [API](./API/README.md) | ... |
| [ARCHITECTURE](./ARCHITECTURE/README.md) | ... |
| [CONCEPTS](./CONCEPTS/README.md) | ... |
| [HOW-TO](./HOW-TO/README.md) | ... |
| [SPECS](./SPECS/README.md) | ... |

<!-- CARF-INDEX-END -->
