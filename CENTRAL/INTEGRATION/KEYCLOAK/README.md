# KEYCLOAK

Keycloak provê autenticação centralizada OAuth2/OIDC para o ecossistema CARF, usando realm único com multi-tenancy dinâmico via atributos de usuário mapeados em claims JWT. Implementa Single Sign-On unificado para GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS e ADMIN onde usuário autentica uma vez e obtém sessão compartilhada entre todas as aplicações. Esta seção documenta especificações do sistema de autenticação enquanto guias de implementação, setup e troubleshooting estão em PROJECTS/KEYCLOAK/DOCS.

## Estrutura

A [arquitetura](./ARCHITECTURE/README.md) documenta visão geral, fluxos OAuth2/OIDC e estratégia multi-tenant. A [configuração do realm](./REALM/README.md) detalha settings e protocol mappers. Os [clients](./CLIENTS/README.md) especificam configuração de cada aplicação. O [RBAC](./RBAC/README.md) define hierarquia de roles e permissões. Os [tokens](./TOKENS/README.md) explicam estrutura e validação de JWT. A [segurança](./SECURITY/README.md) documenta boas práticas e proteção contra ataques.

## Runbooks

A pasta [RUNBOOKS](./RUNBOOKS/README.md) contém procedimentos operacionais para criar usuários e tenants, rotacionar secrets, diagnosticar falhas de autenticação, fazer backup/restore e configurar monitoramento.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Indice por Dominio (26 arquivos)

| # | Dominio | Arquivos |
|:--|:--------|:--------:|
|  | [Architecture](./ARCHITECTURE/README.md) | 3 |
|  | [Clients](./CLIENTS/README.md) | 6 |
|  | [Rbac](./RBAC/README.md) | 3 |
|  | [Realm](./REALM/README.md) | 2 |
|  | [Runbooks](./RUNBOOKS/README.md) | 6 |
|  | [Security](./SECURITY/README.md) | 3 |
|  | [Tokens](./TOKENS/README.md) | 3 |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->
