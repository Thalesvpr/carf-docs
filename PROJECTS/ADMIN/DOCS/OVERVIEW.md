# ADMIN - Overview de Implementação

Console administrativo React para gestão de tenants, configuração de usuários, monitoramento de sistema, visualização de audit logs e configuração de templates PDF de relatórios.

## Requirements Implementados

### Use Cases Principais

- **Gestão Multi-Tenancy**: Criar/editar tenants (municípios), configurar RLS, definir quotas
- **Gestão Usuários**: CRUD de accounts, atribuição de roles, integração Keycloak Admin API
- [UC-011: Gerenciar Equipes](../../../CENTRAL/REQUIREMENTS/USE-CASES/UC-011-gerenciar-equipes-tecnicas.md) - Criação de teams cross-tenant
- **Audit Trail**: Visualização de AuditLogs para compliance LGPD
- **Configuração Templates**: Upload e edição de templates PDF customizados por tenant

## Domain Model Implementado

### Entities (admin-specific)

- [Tenant](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/07-tenant.md) - Gestão multi-tenancy
- [Account](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/08-account.md) - CRUD usuários
- [Team](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/09-team.md) - Gestão teams
- [AuditLog](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/18-audit-log.md) - Visualização read-only
- [PdfTemplate](../../../CENTRAL/DOMAIN-MODEL/ENTITIES/06-pdf-templates.md) - Upload templates

### Value Objects

- Role, Email, PhoneNumber

## Arquitetura Técnica

**Stack:**
- React 18 + TypeScript 5
- Vite (bundler)
- TanStack Query + Table (data grids)
- Zustand (state)
- shadcn/ui (componentes)
- @carf/tscore (autenticação SUPER_ADMIN only)
- @carf/geoapi-client (endpoints /api/admin/*)

**Deploy:** Vercel

**Segurança:** Apenas usuários com role SUPER_ADMIN podem acessar. Backend valida via middleware.

Ver [ARCHITECTURE/](./ARCHITECTURE/README.md).

## Features Documentadas

Features documentadas em desenvolvimento.

---

**Última atualização:** 2026-01-10
