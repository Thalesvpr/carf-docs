# ADRs

Architecture Decision Records documentando decisões arquiteturais críticas do CARF com contexto (por que decisão foi necessária), opções consideradas (alternativas avaliadas com prós/contras), decisão tomada (solução escolhida), consequências (impactos positivos e negativos), e status (proposed/accepted/deprecated/superseded). ADRs são imutáveis - novas decisões criam novos ADRs ao invés de editar existentes preservando histórico decisões arquiteturais permitindo rastreabilidade compreensão evolução sistema ao longo tempo cobrindo decisões backend frontend mobile infraestrutura deployment testing state management authentication persistence offline-first patterns architectural patterns garantindo documentação completa rationale decisões técnicas críticas facilitando onboarding novos desenvolvedores permitindo revisão decisões passadas contexto original.

## Architecture Decision Records

- **[ADR-001-dotnet-9-backend.md](./ADR-001-dotnet-9-backend.md)** - .NET 9 backend vs Node.js Java Python Go
- **[ADR-002-postgresql-postgis.md](./ADR-002-postgresql-postgis.md)** - PostgreSQL PostGIS vs SQL Server MongoDB
- **[ADR-003-keycloak-autenticacao.md](./ADR-003-keycloak-autenticacao.md)** - Keycloak autenticação vs Auth0 implementação própria
- **[ADR-004-react-native-mobile.md](./ADR-004-react-native-mobile.md)** - React Native mobile vs Flutter native iOS Android
- **[ADR-005-multi-tenancy-rls.md](./ADR-005-multi-tenancy-rls.md)** - Multi-tenancy RLS vs schema separation database separation
- **[ADR-006-offline-first-watermelondb.md](./ADR-006-offline-first-watermelondb.md)** - Offline-first WatermelonDB vs Realm SQLite puro
- **[ADR-007-bun-runtime-bundler.md](./ADR-007-bun-runtime-bundler.md)** - Bun runtime bundler vs Node.js Vite Webpack
- **[ADR-008-clean-architecture-ddd.md](./ADR-008-clean-architecture-ddd.md)** - Clean Architecture DDD vs layered tradicional
- **[ADR-009-cqrs-pattern.md](./ADR-009-cqrs-pattern.md)** - CQRS pattern vs CRUD tradicional
- **[ADR-010-event-driven-architecture.md](./ADR-010-event-driven-architecture.md)** - Event-Driven Architecture vs request response síncrono
- **[ADR-011-shared-library-tscore.md](./ADR-011-shared-library-tscore.md)** - Shared library @carf/tscore vs código duplicado monorepo
- **[ADR-012-vite-bundler-frontend.md](./ADR-012-vite-bundler-frontend.md)** - Vite bundler frontend vs Webpack Rollup Parcel
- **[ADR-013-vercel-deployment-platform.md](./ADR-013-vercel-deployment-platform.md)** - Vercel deployment platform vs Netlify AWS Amplify
- **[ADR-014-shadcn-ui-component-library.md](./ADR-014-shadcn-ui-component-library.md)** - shadcn/ui component library vs Material-UI Ant Design
- **[ADR-015-tanstack-query-server-state.md](./ADR-015-tanstack-query-server-state.md)** - TanStack Query server state vs SWR RTK Query
- **[ADR-016-astro-starlight-documentation.md](./ADR-016-astro-starlight-documentation.md)** - Astro Starlight documentation vs VitePress Docusaurus
- **[ADR-017-github-actions-cicd.md](./ADR-017-github-actions-cicd.md)** - GitHub Actions CI/CD vs GitLab CI Jenkins
- **[ADR-018-playwright-e2e-testing.md](./ADR-018-playwright-e2e-testing.md)** - Playwright E2E testing vs Cypress TestCafe
- **[ADR-019-zustand-client-state.md](./ADR-019-zustand-client-state.md)** - Zustand client state vs Redux Context API Jotai
- **[ADR-020-docker-kubernetes-orchestration.md](./ADR-020-docker-kubernetes-orchestration.md)** - Docker Kubernetes orchestration vs Docker Swarm ECS
- **[ADR-021-hangfire-background-jobs.md](./ADR-021-hangfire-background-jobs.md)** - Hangfire background jobs vs custom schedulers cloud functions

---

**Última atualização:** 2026-01-11
