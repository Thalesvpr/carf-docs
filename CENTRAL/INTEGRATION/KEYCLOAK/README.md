# Keycloak - Autenticação CARF

Provedor centralizado de autenticação OAuth2/OIDC para as 6 aplicações CARF (GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS, ADMIN) usando realm único "carf" com multi-tenancy dinâmico via atributos de usuário (`tenants: []` e `current_tenant`) integrado com PostgreSQL RLS através do claim `tenant_id` no JWT token.

## Setup Rápido

`docker-compose up -d` no diretório atual sobe Keycloak + PostgreSQL com realm "carf" importado automaticamente via `realm-export.json`. Acesse http://localhost:8080 com admin/admin. Os 6 clients já estão configurados: geoweb (SPA PKCE), reurbcad (Mobile PKCE), geoapi (Bearer-only), geogis (Client credentials), webdocs (Público), admin (SPA PKCE).

## Arquitetura

Um realm "carf" com 6 clients, 4 roles (field-collector, analyst, admin, super-admin), usuários com atributos `tenants: ["prefeitura-a"]` e `current_tenant: "prefeitura-a"` que viram claims no JWT (`tenant_id` e `allowed_tenants`). Frontend tem dropdown pra trocar tenant, chama backend `/api/auth/switch-tenant`, backend atualiza `current_tenant` no Keycloak via Admin API, usuário faz refresh do token e pega novo `tenant_id`. Middleware backend seta `SET app.tenant_id = {tenant_id}` no PostgreSQL, RLS policy filtra dados automaticamente com `WHERE tenant_id = current_setting('app.tenant_id')::uuid`.

## Documentos

[01-architecture.md](./01-architecture.md) explica OAuth2/OIDC, SSO e flows. [02-realm-configuration.md](./02-realm-configuration.md) detalha configuração dos 6 clients e protocol mappers. [03-docker-setup.md](./03-docker-setup.md) tem docker-compose completo. [04-multi-tenancy.md](./04-multi-tenancy.md) mostra código completo do tenant switcher. [05-client-configurations.md](./05-client-configurations.md) tem config individual de cada client. [06-rbac-permissions.md](./06-rbac-permissions.md) define hierarquia de roles. [07-token-management.md](./07-token-management.md) explica refresh e revogação. [08-production-deployment.md](./08-production-deployment.md) deploy K8s. [09-security-best-practices.md](./09-security-best-practices.md) segurança. [10-troubleshooting.md](./10-troubleshooting.md) erros comuns. [11-admin-frontend.md](./11-admin-frontend.md) carf-admin Next.js com Keycloak Admin API. [12-integration-testing.md](./12-integration-testing.md) testes.

## Arquivos

[realm-export.json](./realm-export.json) = exportação completa do realm. [docker-compose.yml](./docker-compose.yml) = Keycloak + PostgreSQL. [.env.example](./.env.example) = variáveis de ambiente. `clients/*.json` = configs individuais dos 6 clients.

---

**Última atualização:** 2026-01-09
