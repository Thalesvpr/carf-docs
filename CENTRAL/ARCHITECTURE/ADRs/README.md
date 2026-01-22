---
type: readme
status: rejected
description: "Usa tabelas e listas extensivas ao inves de prosa corrida. Indice gerado automaticamente, mas introducao deve ser densa."
updated: 2026-01-22
---

# ADRs

Architecture Decision Records documentando decisões arquiteturais críticas do CARF. Cada ADR registra o contexto que motivou a decisão, as alternativas avaliadas com prós e contras, a decisão tomada e suas consequências.

Os ADRs são imutáveis - novas decisões criam novos registros ao invés de editar existentes, preservando o histórico e permitindo entender a evolução do sistema ao longo do tempo. Cobrem decisões de backend, frontend, mobile, infraestrutura, deployment, testing, autenticação e persistência.


<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (22 arquivos)

| ID | Titulo |
|:---|:-------|
| [ADR-001](./ADR-001-dotnet-9-backend.md) | Escolha do .NET 9 para Backend |
| [ADR-002](./ADR-002-postgresql-postgis.md) | Escolha do PostgreSQL 16 + PostGIS 3.4 como Database |
| [ADR-003](./ADR-003-keycloak-autenticacao.md) | Escolha do Keycloak para Autenticação e Autorização |
| [ADR-004](./ADR-004-react-native-mobile.md) | Escolha do React Native para Aplicação Mobile |
| [ADR-005](./ADR-005-multi-tenancy-rls.md) | Escolha de Multi-tenancy via Row-Level Security (RLS) |
| [ADR-006](./ADR-006-offline-first-watermelondb.md) | Escolha de Arquitetura Offline-First com WatermelonDB |
| [ADR-007](./ADR-007-bun-runtime-bundler.md) | Escolha do Bun como Runtime e Bundler |
| [ADR-008](./ADR-008-clean-architecture-ddd.md) | Escolha de Clean Architecture + Domain-Driven Design |
| [ADR-009](./ADR-009-cqrs-pattern.md) | Escolha do Padrão CQRS (Command Query Responsibility Segregation) |
| [ADR-010](./ADR-010-event-driven-architecture.md) | Escolha de Event-Driven Architecture com Domain Events |
| [ADR-011](./ADR-011-shared-library-tscore.md) | Biblioteca TypeScript Compartilhada @carf/tscore |
| [ADR-012](./ADR-012-vite-bundler-frontend.md) | Escolha do Vite como Bundler para Frontends React |
| [ADR-013](./ADR-013-vercel-deployment-platform.md) | Escolha do Vercel como Plataforma de Deploy para Frontends |
| [ADR-014](./ADR-014-shadcn-ui-component-library.md) | Escolha do shadcn/ui + Radix UI como Component Library |
| [ADR-015](./ADR-015-tanstack-query-server-state.md) | Escolha do TanStack Query para Server State Management |
| [ADR-016](./ADR-016-astro-starlight-documentation.md) | Escolha do Astro + Starlight para Site de Documentação |
| [ADR-017](./ADR-017-github-actions-cicd.md) | Escolha do GitHub Actions como Plataforma CI/CD |
| [ADR-018](./ADR-018-playwright-e2e-testing.md) | Escolha do Playwright para Testes End-to-End |
| [ADR-019](./ADR-019-zustand-client-state.md) | Escolha do Zustand para Client State Management |
| [ADR-020](./ADR-020-docker-kubernetes-orchestration.md) | Escolha do Docker + Kubernetes para Orquestração Backend |
| [ADR-021](./ADR-021-hangfire-background-jobs.md) | Escolha do Hangfire para Background Jobs |
| [ADR-022](./ADR-022-role-based-access-control.md) | Hierarquia de Roles com Composite Roles no Keycloak |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

<!-- CARF-INDEX-START -->
## Documentos

### Em Revisão

- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-001-dotnet-9-backend.md|ADR-001: .NET 9 para Backend]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-002-postgresql-postgis.md|ADR-002: Escolha do PostgreSQL 16 + PostGIS 3.4 como Database]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-003-keycloak-autenticacao.md|ADR-003: Escolha do Keycloak para Autenticação e Autorização]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-004-react-native-mobile.md|ADR-004: Escolha do React Native para Aplicação Mobile]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-005-multi-tenancy-rls.md|ADR-005: Escolha de Multi-tenancy via Row-Level Security (RLS)]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-006-offline-first-watermelondb.md|ADR-006: Escolha de Arquitetura Offline-First com WatermelonDB]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-007-bun-runtime-bundler.md|ADR-007: Escolha do Bun como Runtime e Bundler]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-008-clean-architecture-ddd.md|ADR-008: Escolha de Clean Architecture + Domain-Driven Design]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-009-cqrs-pattern.md|ADR-009: Escolha do Padrão CQRS (Command Query Responsibility Segregation)]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-010-event-driven-architecture.md|ADR-010: Escolha de Event-Driven Architecture com Domain Events]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-011-shared-library-tscore.md|ADR-011: Biblioteca TypeScript Compartilhada @carf/tscore]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-012-vite-bundler-frontend.md|ADR-012: Escolha do Vite como Bundler para Frontends React]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-013-vercel-deployment-platform.md|ADR-013: Escolha do Vercel como Plataforma de Deploy para Frontends]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-014-shadcn-ui-component-library.md|ADR-014: Escolha do shadcn/ui + Radix UI como Component Library]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-015-tanstack-query-server-state.md|ADR-015: Escolha do TanStack Query para Server State Management]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-016-astro-starlight-documentation.md|ADR-016: Escolha do Astro + Starlight para Site de Documentação]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-017-github-actions-cicd.md|ADR-017: Escolha do GitHub Actions como Plataforma CI/CD]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-018-playwright-e2e-testing.md|ADR-018: Escolha do Playwright para Testes End-to-End]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-019-zustand-client-state.md|ADR-019: Escolha do Zustand para Client State Management]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-020-docker-kubernetes-orchestration.md|ADR-020: Escolha do Docker + Kubernetes para Orquestração Backend]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-021-hangfire-background-jobs.md|ADR-021: Escolha do Hangfire para Background Jobs]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-022-role-based-access-control.md|ADR-022: Hierarquia de Roles com Composite Roles no Keycloak]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-023-color-palette-design-system.md|ADR-023: Paleta de Cores e Design System CARF]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-024-keycloakify-adoption.md|ADR-024: Adoção de Keycloakify para Temas Keycloak]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-025-single-realm-multi-tenancy.md|ADR-025: Single-Realm Multi-Tenancy Strategy]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-026-roles-hierarchy.md|ADR-026: Hierarquia de Roles CARF]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-027-oauth2-flows-by-client.md|ADR-027: OAuth2 Flows por Tipo de Client]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-028-token-lifetimes.md|ADR-028: Token Lifetimes e Session Configuration]]
- ○ [[CENTRAL/ARCHITECTURE/ADRs/ADR-029-security-strategy.md|ADR-029: Estrategia de Seguranca Keycloak]]

<!-- CARF-INDEX-END -->
