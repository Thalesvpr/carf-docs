# KEYCLOAK

Keycloak provê autenticação centralizada OAuth2/OIDC para o ecossistema CARF, usando um realm único com multi-tenancy dinâmico via atributos de usuário mapeados em claims JWT.

Implementa Single Sign-On unificado para as aplicações GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS e ADMIN. O usuário autentica uma única vez e obtém sessão válida compartilhada.

A autorização usa RBAC hierárquica com cinco roles: super-admin, admin, manager, analyst e field-collector. Protocol mappers customizados injetam claims tenant_id e allowed_tenants nos tokens JWT, validados pelo middleware backend e usados nas policies RLS do PostgreSQL.

O ambiente de desenvolvimento usa Docker Compose com seis clients pré-configurados, cada um com settings específicos para PKCE, bearer-only ou confidential conforme o tipo de aplicação.

## Runbooks

- **[runbooks/01-create-user.md](./runbooks/01-create-user.md)** - Criar usuário com roles e tenant
- **[runbooks/02-create-tenant.md](./runbooks/02-create-tenant.md)** - Criar novo município
- **[runbooks/03-rotate-secrets.md](./runbooks/03-rotate-secrets.md)** - Rotação de client secrets
- **[runbooks/04-troubleshoot-auth.md](./runbooks/04-troubleshoot-auth.md)** - Diagnóstico de falhas de login
- **[runbooks/05-backup-restore.md](./runbooks/05-backup-restore.md)** - Backup e disaster recovery
- **[runbooks/06-monitoring.md](./runbooks/06-monitoring.md)** - Health checks e métricas

---

**Última atualização:** 2026-01-15
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (12 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-architecture](./01-architecture.md) | Arquitetura de Autenticação Keycloak |
| [02-realm-configuration](./02-realm-configuration.md) | Configuração do Realm Keycloak |
| [03-docker-setup](./03-docker-setup.md) | Docker Setup Keycloak |
| [04-multi-tenancy](./04-multi-tenancy.md) | Multi-Tenancy Dinâmico |
| [05-client-configurations](./05-client-configurations.md) | Configurações dos 6 Clients |
| [06-rbac-permissions](./06-rbac-permissions.md) | RBAC e Permissões |
| [07-token-management](./07-token-management.md) | Gerenciamento de Tokens |
| [08-production-deployment](./08-production-deployment.md) | Deploy em Produção |
| [09-security-best-practices](./09-security-best-practices.md) | Segurança - Best Practices |
| [10-troubleshooting](./10-troubleshooting.md) | Troubleshooting |
| [11-admin-frontend](./11-admin-frontend.md) | Admin Frontend (carf-admin) |
| [12-integration-testing](./12-integration-testing.md) | Testes de Integração Keycloak |

*Gerado automaticamente em 2026-01-15 17:41*
<!-- GENERATED:END -->
