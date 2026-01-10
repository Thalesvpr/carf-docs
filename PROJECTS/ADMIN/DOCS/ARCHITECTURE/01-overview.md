# Overview da Arquitetura - ADMIN

## Visão Geral

ADMIN é console administrativo React SPA construído com Vite 5 e shadcn/ui fornecendo interface para operações privilegiadas (gerenciar usuários, tenants, visualizar audit logs, configurar sistema, executar operações batch) restrito a usuários com role ADMIN ou SUPER_ADMIN autenticados via Keycloak PKCE flow, comunica-se com GEOAPI `/api/admin/*` endpoints que fazem proxy seguro para Keycloak Admin API mantendo client_secret no backend, usa TanStack Query para server state management e Zustand para client state, implementa @carf/tscore para auth e validações, usa shadcn/ui para componentes visuais, e deploy para Vercel como static SPA com client-side routing via React Router v6.

## Diagrama de Arquitetura

```
┌────────────────────────────────────────────────────────────┐
│                    Admin User (Browser)                    │
│              https://admin.carf.gov.br                     │
└──────────────┬─────────────────────────────────────────────┘
               │
               │ HTTPS + JWT
               ▼
┌────────────────────────────────────────────────────────────┐
│                      Vercel CDN                             │
│                Static SPA Hosting                          │
│            (HTML + JS bundle servido)                      │
└──────────────┬─────────────────────────────────────────────┘
               │ Static files
               ▼
┌────────────────────────────────────────────────────────────┐
│              ADMIN Console (React SPA + Vite)               │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  Presentation Layer (React Components)           │     │
│  │  - UserManagementPage                            │     │
│  │  - TenantManagementPage                          │     │
│  │  - AuditLogsPage                                 │     │
│  └────────┬─────────────────────────────────────────┘     │
│           │                                                │
│  ┌────────▼─────────────────────────────────────────┐     │
│  │  State Management Layer                          │     │
│  │  - TanStack Query (server state/cache)           │     │
│  │  - Zustand (client state)                        │     │
│  └────────┬─────────────────────────────────────────┘     │
│           │                                                │
│  ┌────────▼─────────────────────────────────────────┐     │
│  │  API Client Layer (@carf/geoapi-client)          │     │
│  │  - Automatic JWT injection via interceptor       │     │
│  │  - Retry logic + error handling                  │     │
│  └────────┬─────────────────────────────────────────┘     │
└───────────┼──────────────────────────────────────────────┘
            │ HTTPS + JWT Bearer
            ▼
┌────────────────────────────────────────────────────────────┐
│               GEOAPI Backend (.NET 9)                       │
│                                                            │
│  ┌──────────────────────────────────────────────────┐     │
│  │  /api/admin/* Endpoints                          │     │
│  │  (Proxy seguro para Keycloak Admin API)          │     │
│  │                                                   │     │
│  │  - POST /api/admin/users                         │     │
│  │  - DELETE /api/admin/users/:id                   │     │
│  │  - GET /api/admin/audit-logs                     │     │
│  │  - POST /api/admin/tenants                       │     │
│  └────────┬─────────────────────────────────────────┘     │
│           │ JWT validation + role check               │     │
└───────────┼──────────────────────────────────────────────┘
            │ client_secret (confidential)
            ▼
┌────────────────────────────────────────────────────────────┐
│            Keycloak Admin API                               │
│         (Gerenciamento de usuários/roles)                  │
└────────────────────────────────────────────────────────────┘
```

## Funcionalidades Principais

### 1. Gerenciamento de Usuários

- Listar todos os usuários do sistema
- Criar novo usuário com role específica
- Editar informações de usuário
- Desabilitar/habilitar usuário
- Resetar senha
- Atribuir/remover roles

### 2. Gerenciamento de Tenants

- Listar municípios (tenants)
- Criar novo município
- Editar configurações de município
- Visualizar estatísticas por município
- Deletar município (com validação de dependências)

### 3. Audit Logs

- Visualizar timeline de todas as operações
- Filtrar por usuário, tenant, data, tipo de operação
- Exportar logs para CSV/PDF
- Buscar por entity_id ou request_id

### 4. Configurações do Sistema

- Gerenciar feature flags
- Configurar limites de rate limiting
- Ajustar timeout de sessões
- Configurar notificações

### 5. Operações Batch

- Importar usuários via CSV
- Executar scripts de manutenção
- Gerar relatórios consolidados

## Segurança

### Autenticação

- JWT tokens via Keycloak
- Refresh automático de tokens
- Session timeout configurável

### Autorização

- RBAC com 2 níveis:
  - **ADMIN:** Gerencia próprio tenant
  - **SUPER_ADMIN:** Gerencia todos os tenants

### Audit Trail

- Todas operações administrativas são logadas
- Quem, quando, o quê, tenant_id
- Logs imutáveis

