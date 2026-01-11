# ADMIN - Console Administrativo React SPA

**[📋 Overview de Implementação](./OVERVIEW.md)** - Mapeamento completo de requirements, domain model e arquitetura técnica

Documentação do console administrativo CARF.

## Visão Geral

ADMIN é uma **SPA React** que consome endpoints `/api/admin/*` do **GEOAPI** para gestão de tenants, usuários e configurações do sistema CARF.

### Por que SPA React (não Next.js)?

Next.js foi **descartado por segurança**:
- Keycloak Admin Client API requer `client_secret` confidencial
- Secrets no frontend (mesmo Next.js Server Actions) podem vazar
- Backend .NET oferece melhor isolamento e auditoria

### Arquitetura Segura

```
carf-admin (SPA React)  →  GEOAPI /api/admin/*  →  Keycloak Admin API
     ↓ PKCE flow             ↓ confidential           ↓ client_secret
  (sem secret)           (backend seguro)          (isolado)
```

### Características

- **React 18** - UI library
- **Vite** - Build tool (fast HMR)
- **TypeScript** - Type safety completo
- **@carf/tscore** - Biblioteca compartilhada (auth, validations, types)
- **shadcn/ui** - Component library
- **TanStack Query** - Server state management
- **Zustand** - Client state management
- **Tailwind CSS** - Utility-first styling
- **Keycloak.js** - Autenticação OAuth2 PKCE

## Segurança

Ver documentação completa: [Arquitetura de Segurança Admin](../../GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md)

**7 Camadas de Segurança no Backend (GEOAPI):**
1. OAuth2 JWT authentication
2. Role-based authorization (super-admin/admin only)
3. Tenant validation
4. Rate limiting (100 req/min)
5. CORS restrito
6. Auditoria completa
7. Keycloak Admin Client confidential

## Documentação

- [Features Implementadas](./FEATURES/README.md) - Casos de uso mapeados
- [Conceitos Fundamentais](./CONCEPTS/README.md) - Conceitos técnicos
- [Guias Práticos](./HOW-TO/README.md) - Tutoriais e instruções
- [Arquitetura](./ARCHITECTURE/README.md) - Decisões técnicas
- [carf-admin README](../SRC-CODE/carf-admin/README.md) - Setup e instalação
- [Segurança Admin](../../GEOAPI/DOCS/ARCHITECTURE/02-admin-security.md) - 7 camadas

---

**Última atualização:** 2026-01-09
