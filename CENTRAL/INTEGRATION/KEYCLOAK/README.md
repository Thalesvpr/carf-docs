# KEYCLOAK

Keycloak provê autenticação centralizada OAuth2 OIDC ecossistema CARF usando realm único carf multi-tenancy dinâmico via atributos usuário mapeados claims JWT permitindo isolamento dados município PostgreSQL Row-Level Security implementando Single Sign-On unificado seis aplicações GEOWEB REURBCAD GEOAPI GEOGIS WEBDOCS ADMIN usuário autentica única vez obtendo sessão válida compartilhada eliminando necessidade múltiplos logins autorização RBAC hierárquica cinco roles super-admin admin manager analyst field-collector protocol mappers customizados injetando claims tenant_id allowed_tenants tokens JWT validados middleware backend configuração realm carf token lifetimes access cinco minutos refresh trinta dias SSO session oito horas ambiente desenvolvimento docker-compose Keycloak PostgreSQL mock SMTP seis clients pré-configurados geoweb-client reurbcad-client geoapi-client geogis-client webdocs-client admin-client settings específicos PKCE bearer-only confidential estratégia isolamento user attributes JWT claims middleware backend PostgreSQL RLS produção high-availability cluster load balancer cache Infinispan rotação secrets HTTPS rate limiting brute force protection auditoria eventos troubleshooting invalid token CORS misconfiguration RLS policies.

## Documentos

- **[01-architecture.md](./01-architecture.md)** - Flows OAuth2 OIDC sequence diagrams
- **[02-realm-configuration.md](./02-realm-configuration.md)** - Realm carf token lifetimes
- **[03-docker-setup.md](./03-docker-setup.md)** - Ambiente desenvolvimento local
- **[04-multi-tenancy.md](./04-multi-tenancy.md)** - Estratégia isolamento RLS
- **[05-client-configurations.md](./05-client-configurations.md)** - Seis clients OAuth2
- **[06-rbac-permissions.md](./06-rbac-permissions.md)** - Matriz autorização roles
- **[07-token-management.md](./07-token-management.md)** - Ciclo vida tokens
- **[08-production-deployment.md](./08-production-deployment.md)** - Setup high-availability cluster
- **[09-security-best-practices.md](./09-security-best-practices.md)** - Rotação secrets auditoria
- **[10-troubleshooting.md](./10-troubleshooting.md)** - Diagnóstico problemas comuns
- **[11-admin-frontend.md](./11-admin-frontend.md)** - Admin Console gestão usuários
- **[12-integration-testing.md](./12-integration-testing.md)** - Testes integração Keycloak

## Runbooks

- **[runbooks/01-create-user.md](./runbooks/01-create-user.md)** - Admin Console roles tenant
- **[runbooks/02-create-tenant.md](./runbooks/02-create-tenant.md)** - Novo município RLS
- **[runbooks/03-rotate-secrets.md](./runbooks/03-rotate-secrets.md)** - Client secrets zero-downtime
- **[runbooks/04-troubleshoot-auth.md](./runbooks/04-troubleshoot-auth.md)** - Diagnóstico falhas login
- **[runbooks/05-backup-restore.md](./runbooks/05-backup-restore.md)** - Export realm disaster recovery
- **[runbooks/06-monitoring.md](./runbooks/06-monitoring.md)** - Health checks Prometheus Grafana

---

**Última atualização:** 2026-01-11
