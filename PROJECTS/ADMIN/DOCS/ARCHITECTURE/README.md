# Arquitetura ADMIN - React SPA

Console administrativo React para gerenciamento do ecossistema CARF.

## Decisão Arquitetural: SPA React (não Next.js)

### Por que NÃO Next.js?

Next.js foi **descartado por segurança**:
- Keycloak Admin Client API requer client_secret confidencial
- Secrets em Next.js podem vazar no frontend
- Backend .NET oferece melhor isolamento

### Arquitetura Segura

carf-admin (SPA)  →  GEOAPI /api/admin/*  →  Keycloak Admin API
   PKCE flow           confidential            client_secret
(sem secret)       (backend seguro)          (isolado)

## Stack Tecnológica

- React 18 + TypeScript 5
- Vite 5 - Build tool
- @carf/tscore - Auth, validations, types
- shadcn/ui - Component library
- TanStack Query v5 - Server state
- Zustand v4 - Client state
- React Router v6 - Routing
- Tailwind CSS - Styling

## Segurança

7 Camadas no Backend (GEOAPI /api/admin/*):
1. OAuth2 JWT authentication
2. Role-based authorization
3. Tenant validation
4. Rate limiting
5. CORS restrito
6. Auditoria completa
7. Keycloak Admin Client confidential

Ver documentação completa: ../../GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md

## Ver Também

- Segurança Admin: ../../GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md
- carf-admin README: ../SRC-CODE/carf-admin/README.md
- Keycloak Setup: ../../../CENTRAL/INTEGRATION/KEYCLOAK/README.md

Última atualização: 2026-01-09
