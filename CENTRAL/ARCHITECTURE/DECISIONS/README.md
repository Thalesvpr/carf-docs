---
type: readme
status: current
updated: 2026-01-22
---

# DECISIONS

Architecture Decision Records (ADRs) documentando decisoes arquiteturais significativas do CARF, incluindo contexto, alternativas avaliadas, decisao tomada e consequencias esperadas.

Cada ADR segue formato padronizado que registra o contexto e problema que motivou a decisao, as alternativas consideradas com pros e contras de cada uma, a decisao final tomada e as consequencias positivas e negativas resultantes. Este registro historico permite que novos membros da equipe compreendam o racional por tras da arquitetura atual.

As decisoes cobrem escolhas fundamentais de tecnologia e arquitetura. O [multi-tenancy](./01-multi-tenancy.md) explica a escolha de Row-Level Security sobre schema-per-tenant. O [offline-first](./02-offline-first.md) justifica a adocao de WatermelonDB para o app mobile. A [autenticacao](./03-authentication.md) documenta por que Keycloak foi escolhido como identity provider.

O [backend stack](./04-backend-stack.md) registra a decisao por .NET 9 e Clean Architecture. O [frontend stack](./05-frontend-stack.md) documenta a escolha de React com TypeScript. O [database](./06-database.md) justifica PostgreSQL com PostGIS para dados geoespaciais. O [mobile stack](./07-mobile-stack.md) explica a escolha de React Native com Expo. O [estilo arquitetural](./08-architecture-style.md) documenta a adocao de Clean Architecture combinada com CQRS. O [git workflow](./09-git.md) justifica trunk-based development. O [github](./10-github.md) documenta escolha da plataforma e configuracoes.

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (8)

| Documento | Status |
|-----------|--------|
| [ADR-001: Row-Level Security para Multi-Tenancy](./01-multi-tenancy.md) | ⚠ |
| [ADR-002: WatermelonDB para Operacao Offline](./02-offline-first.md) | ⚠ |
| [ADR-003: Keycloak como Identity Provider](./03-authentication.md) | ⚠ |
| [ADR-004: .NET 9 para Backend](./04-backend-stack.md) | ⚠ |
| [ADR-005: React com TypeScript para Frontend](./05-frontend-stack.md) | ⚠ |
| [ADR-006: PostgreSQL com PostGIS](./06-database.md) | ⚠ |
| [ADR-007: React Native com Expo para Mobile](./07-mobile-stack.md) | ⚠ |
| [ADR-008: Clean Architecture com CQRS](./08-architecture-style.md) | ⚠ |

<!-- CARF-INDEX-END -->
