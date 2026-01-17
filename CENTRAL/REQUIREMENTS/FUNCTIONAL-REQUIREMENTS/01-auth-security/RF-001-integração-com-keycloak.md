---
modules: [GEOAPI, GEOWEB, REURBCAD, GEOGIS]
epic: security
---

# RF-001: Integração com Keycloak

Sistema deve integrar-se com Keycloak para autenticação OAuth2/OIDC permitindo configuração de realm específico no ambiente Keycloak onde cada tenant possui isolamento adequado garantindo segurança multi-tenant, implementação suporta múltiplos Identity Providers externos incluindo Google Microsoft GitHub e outros provedores compatíveis com SAML ou OIDC permitindo que usuários autentiquem usando credenciais corporativas existentes, funcionalidade de SSO (Single Sign-On) deve estar plenamente funcional garantindo que usuário autenticado em um módulo (GEOWEB REURBCAD GEOGIS) não precise re-autenticar ao acessar outros módulos do ecossistema desde que compartilhem mesmo realm Keycloak, integração implementada nos módulos GEOAPI GEOWEB REURBCAD GEOGIS garantindo autenticação consistente em toda plataforma, configuração inclui definição de client IDs secrets redirect URIs e escopos OAuth2 apropriados para cada aplicação cliente.

---

**Última atualização:** 2025-12-30
**Status do arquivo**: Review
