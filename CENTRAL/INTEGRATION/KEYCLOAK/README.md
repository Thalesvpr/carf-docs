# KEYCLOAK

Provedor centralizado de autenticação OAuth2/OIDC para as seis aplicações CARF usando realm único "carf" com multi-tenancy dinâmico via atributos de usuário que viram claims JWT integrados com PostgreSQL RLS isolando dados por tenant automaticamente. Implementa SSO unificado entre GEOWEB REURBCAD GEOAPI GEOGIS WEBDOCS e ADMIN com seis clients pré-configurados (SPA PKCE para web, Mobile PKCE para app, Bearer-only para backend, Client credentials para plugins, Público para docs). Realm possui cinco roles RBAC (super-admin admin manager analyst field-collector) hierárquicos com protocol mappers customizados gerando tokens com tenant_id e allowed_tenants permitindo troca dinâmica de contexto via dropdown frontend e refresh token. Backend middleware extrai claims JWT e configura sessão PostgreSQL com SET app.tenant_id aplicando Row Level Security policies que filtram queries por tenant sem código adicional nas aplicações. Customizações específicas CARF incluem temas visuais login/account/email em português brasileiro com validação CPF/CNPJ via tscore library, Docker image personalizada com temas embedados, e scripts automação completa via Makefile permitindo quick-start ambiente desenvolvimento com make dev.

## Documentação Técnica

### Conceitos Fundamentais
1. **[01-architecture.md](./01-architecture.md)** - Arquitetura Keycloak com SSO, multi-tenancy e flows OAuth2
2. **[02-realm-configuration.md](./02-realm-configuration.md)** - Configuração do realm "carf"
3. **[03-docker-setup.md](./03-docker-setup.md)** - Setup local com Docker Compose
4. **[04-multi-tenancy.md](./04-multi-tenancy.md)** - Multi-tenancy dinâmico via JWT claims
5. **[05-client-configurations.md](./05-client-configurations.md)** - 6 clients pré-configurados (GEOWEB, REURBCAD, GEOAPI, GEOGIS, WEBDOCS, ADMIN)
6. **[06-rbac-permissions.md](./06-rbac-permissions.md)** - Roles RBAC hierárquicos (super-admin, admin, manager, analyst, field-collector)

### Operação e Deploy
7. **[07-token-management.md](./07-token-management.md)** - Gerenciamento de tokens JWT (access, refresh, protocol mappers)
8. **[08-production-deployment.md](./08-production-deployment.md)** - Deploy produção (PostgreSQL backend, cluster HA)
9. **[09-security-best-practices.md](./09-security-best-practices.md)** - Boas práticas segurança (rotação secrets, HTTPS, rate limiting)
10. **[10-troubleshooting.md](./10-troubleshooting.md)** - Troubleshooting comum (invalid token, CORS, RLS)
11. **[11-admin-frontend.md](./11-admin-frontend.md)** - Admin Console (criar users, tenants, roles)
12. **[12-integration-testing.md](./12-integration-testing.md)** - Testes E2E de integração OAuth2

## Guias de Integração por Projeto

Exemplos de código para integração Keycloak estão documentados na pasta EXAMPLES de cada projeto com implementações específicas incluindo inicialização de cliente OAuth2 configuração de endpoints PKCE flow para SPAs client credentials para plugins e bearer-only para backends mostrando setup completo de AuthContext providers protected routes e token management strategies adaptadas para cada stack tecnológico React .NET React Native Python seguindo padrões estabelecidos em client-configurations.md e architecture.md deste diretório CENTRAL/INTEGRATION/KEYCLOAK.

## Runbooks Operacionais

- **[runbooks/01-create-user.md](./runbooks/01-create-user.md)** - Criar usuário via Admin Console
- **[runbooks/02-create-tenant.md](./runbooks/02-create-tenant.md)** - Criar novo tenant e atribuir a usuários
- **[runbooks/03-rotate-secrets.md](./runbooks/03-rotate-secrets.md)** - Rotacionar client secrets e tokens
- **[runbooks/04-troubleshoot-auth.md](./runbooks/04-troubleshoot-auth.md)** - Troubleshooting autenticação failed
- **[runbooks/05-backup-restore.md](./runbooks/05-backup-restore.md)** - Backup e restore configuração Keycloak
- **[runbooks/06-monitoring.md](./runbooks/06-monitoring.md)** - Monitoramento health e métricas

## Tema Customizado CARF

Ver arquivos no diretório de código-fonte do tema:
- **[BUILD.md](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/BUILD.md)** - Instruções de build do tema customizado
- **[CHANGELOG.md](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/CHANGELOG.md)** - Histórico de versões do tema
- **[tests/README.md](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/tests/README.md)** - Testes do tema customizado

### Recursos do Tema

- **[Imagens](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/login/resources/img/README.md)** - Assets de imagens (logo, ícones, backgrounds)
- **[JavaScript](../../../PROJECTS/KEYCLOAK/SRC-CODE/carf-keycloak/themes/carf/login/resources/js/README.md)** - Scripts customizados (validação CPF/CNPJ)

---

**Última atualização:** 2026-01-10
