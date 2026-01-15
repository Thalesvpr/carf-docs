# INTEGRATION

Documentação de integrações com serviços externos essenciais para o funcionamento do sistema CARF.

O [Keycloak](./KEYCLOAK/README.md) é o provedor de autenticação centralizada OAuth2/OIDC, oferecendo Single Sign-On para todas as aplicações do ecossistema com suporte a multi-tenancy via atributos de usuário mapeados em claims JWT.

O [banco de dados](./DATABASE/README.md) usa PostgreSQL 16 com extensão PostGIS 3.4 para dados geoespaciais e Row-Level Security para isolamento automático de dados entre tenants.

## Estrutura

- **[KEYCLOAK/](./KEYCLOAK/README.md)** - Autenticação OAuth2/OIDC e SSO multi-tenant
- **[DATABASE/](./DATABASE/README.md)** - PostgreSQL + PostGIS com Row-Level Security

---

**Última atualização:** 2026-01-14
