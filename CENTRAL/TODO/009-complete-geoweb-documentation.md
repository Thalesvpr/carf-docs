# 009 - Complete GEOWEB Documentation (Missing 13 Files)

🔴 **Prioridade:** Crítica
📅 **Criado em:** 2026-01-09
⏱️ **Estimativa:** 2 dias

## Descrição

GEOWEB tem apenas 3 arquivos de documentação. Frontend web é crítico, precisa de documentação completa de arquitetura FSD (Feature-Sliced Design), integrações e deployment.

## Status Atual

**Completude:** 18% (3/16 arquivos)

**Existem:**
- [X] DOCS/README.md
- [X] DOCS/ARCHITECTURE/01-keycloak-integration.md
- [X] DOCS/HOW-TO/01-setup-keycloak.md

## Checklist - Arquivos Faltando

### ARCHITECTURE/ (4 faltando)
- [ ] README.md
- [ ] 01-overview.md (Feature-Sliced Design)
- [ ] 03-data-flow.md (request flow, state management)
- [ ] 04-integration.md (GEOAPI, Keycloak, libs)
- [ ] 05-deployment.md (Vite build, Docker, hosting)

### CONCEPTS/ (4 faltando)
- [ ] README.md
- [ ] 01-key-concepts.md (FSD, React Query, Zustand)
- [ ] 02-terminology.md (layers, features, entities, widgets)
- [ ] 03-design-principles.md (component design, hooks)

### HOW-TO/ (4 faltando)
- [ ] README.md
- [ ] 01-setup-dev-environment.md
- [ ] 02-build-and-run.md
- [ ] 03-testing.md (Vitest, Testing Library)
- [ ] 04-troubleshooting.md

### CODE (1 faltando)
- [ ] SRC-CODE/carf-geoweb/README.md

## Conteúdo Específico Necessário

### 01-overview.md
- Diagrama Feature-Sliced Design
- Layers: app, pages, features, entities, shared
- Stack: React 18, Vite, TypeScript, TanStack Query, Zustand
- Integrações: Leaflet maps, Keycloak auth

### 03-data-flow.md
- Component → Hook → Query/Mutation → API Client → GEOAPI
- State management (Zustand)
- Server state (React Query)
- Auth flow (Keycloak)

### 04-integration.md
- @carf/tscore (auth, validations, types)
- @carf/geoapi-client (HTTP client)
- @carf/ui (components)
- GEOAPI backend
- Keycloak

### 05-deployment.md
- Vite build
- Docker container
- Static hosting (Nginx)
- Environment variables
- GitHub Actions CI/CD

## Localização

`PROJECTS/GEOWEB/DOCS/`

## Referências do Template

Ver: `CENTRAL/TEMPLATES/PROJECT-DOCS-TEMPLATE.md`
