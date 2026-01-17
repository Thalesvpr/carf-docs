# Arquitetura ADMIN - React SPA

Console administrativo React para gerenciamento do ecossistema CARF.

## Documentos Disponíveis

- [01-overview.md](./01-overview.md) - Visão geral da arquitetura React SPA
- [02-layers.md](./02-layers.md) - Camadas (Presentation, State, API)
- [03-data-flow.md](./03-data-flow.md) - Fluxo de dados (UI → TanStack Query → GEOAPI)
- [04-integration.md](./04-integration.md) - Integração com GEOAPI e Keycloak
- [05-deployment.md](./05-deployment.md) - Deploy para Vercel/Netlify

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

Ver documentação completa em GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md

## Ver Também

- Segurança Admin: GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md
- carf-admin README: ADMIN/SRC-CODE/carf-admin/README.md
- Keycloak Setup: CENTRAL/INTEGRATION/KEYCLOAK/README.md

---

**Última atualização:** 2026-01-15

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (5 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-overview](./01-overview.md) | Overview da Arquitetura - ADMIN |
| [02-layers](./02-layers.md) | Layers - ADMIN |
| [03-data-flow](./03-data-flow.md) | Data Flow - ADMIN |
| [04-integration](./04-integration.md) | Integration - ADMIN |
| [05-deployment](./05-deployment.md) | Deployment - ADMIN |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
**Status do arquivo**: Incompleto
Descrição: Falta parágrafo denso introdutório; Muitas listas com bullets (19) antes do rodapé - considerar converter para parágrafo denso.
