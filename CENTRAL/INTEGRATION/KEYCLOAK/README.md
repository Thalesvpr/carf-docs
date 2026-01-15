# KEYCLOAK

Keycloak provê autenticação centralizada OAuth2/OIDC para o ecossistema CARF, usando um realm único com multi-tenancy dinâmico via atributos de usuário mapeados em claims JWT.

Implementa Single Sign-On unificado para as aplicações GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS e ADMIN. O usuário autentica uma única vez e obtém sessão válida compartilhada.

A autorização usa RBAC hierárquica com cinco roles: super-admin, admin, manager, analyst e field-collector. Protocol mappers customizados injetam claims tenant_id e allowed_tenants nos tokens JWT, validados pelo middleware backend e usados nas policies RLS do PostgreSQL.

O ambiente de desenvolvimento usa Docker Compose com seis clients pré-configurados, cada um com settings específicos para PKCE, bearer-only ou confidential conforme o tipo de aplicação.

## Documentos

- **[01-architecture.md](./01-architecture.md)** - Flows OAuth2/OIDC e sequence diagrams
- **[02-realm-configuration.md](./02-realm-configuration.md)** - Configuração do realm e token lifetimes
- **[03-docker-setup.md](./03-docker-setup.md)** - Ambiente de desenvolvimento local
- **[04-multi-tenancy.md](./04-multi-tenancy.md)** - Estratégia de isolamento com RLS
- **[05-client-configurations.md](./05-client-configurations.md)** - Configuração dos seis clients OAuth2
- **[06-rbac-permissions.md](./06-rbac-permissions.md)** - Matriz de autorização e roles
- **[07-token-management.md](./07-token-management.md)** - Ciclo de vida dos tokens
- **[08-production-deployment.md](./08-production-deployment.md)** - Setup de cluster high-availability
- **[09-security-best-practices.md](./09-security-best-practices.md)** - Rotação de secrets e auditoria
- **[10-troubleshooting.md](./10-troubleshooting.md)** - Diagnóstico de problemas comuns
- **[11-admin-frontend.md](./11-admin-frontend.md)** - Admin Console para gestão de usuários
- **[12-integration-testing.md](./12-integration-testing.md)** - Testes de integração

## Runbooks

- **[runbooks/01-create-user.md](./runbooks/01-create-user.md)** - Criar usuário com roles e tenant
- **[runbooks/02-create-tenant.md](./runbooks/02-create-tenant.md)** - Criar novo município
- **[runbooks/03-rotate-secrets.md](./runbooks/03-rotate-secrets.md)** - Rotação de client secrets
- **[runbooks/04-troubleshoot-auth.md](./runbooks/04-troubleshoot-auth.md)** - Diagnóstico de falhas de login
- **[runbooks/05-backup-restore.md](./runbooks/05-backup-restore.md)** - Backup e disaster recovery
- **[runbooks/06-monitoring.md](./runbooks/06-monitoring.md)** - Health checks e métricas

---

**Última atualização:** 2026-01-14
