# CONCEPTS - Conceitos Fundamentais

Documentos ultra-compactos explicando conceitos core do Keycloak e sua customização no projeto CARF.

## Arquivos

### [01-keycloak-themes.md](./01-keycloak-themes.md)
Sistema de themes do Keycloak explicando estrutura de diretórios (login/account/email/common), theme.properties com herança via parent, templates FreeMarker com variáveis context (realm, url, msg, user, login), recursos estáticos (CSS/JS/imagens), internacionalização via messages_*.properties, e deployment via volume mount (dev) ou COPY no Dockerfile (prod).

### [02-keycloak-spis.md](./02-keycloak-spis.md)
Service Provider Interfaces do Keycloak para extensões server-side via plugins Java implementando interfaces como Authenticator, EventListenerProvider, ProtocolMapper, UserStorageProvider permitindo custom authentication flows, event logging, claims customizados no JWT, e integração com user stores externos.

### [03-realm-customization.md](./03-realm-customization.md)
Configuração de realms incluindo clients OAuth2 (public PKCE para SPAs, confidential para backends), roles (realm-wide e client-specific), user attributes (tenants, current_tenant), protocol mappers (tenant_id no JWT), authentication flows (browser, direct grant, client credentials), e realm-export.json para versionamento.

### [04-oauth2-oidc-flows.md](./04-oauth2-oidc-flows.md)
OAuth2 grant types (authorization_code + PKCE para SPAs/mobile, client_credentials para M2M, refresh_token), OIDC endpoints (authorize, token, userinfo, jwks_uri, end_session), JWT structure (header RS256, payload com sub/iss/exp/iat/tenant_id/roles, signature), token lifecycle (access 5min, refresh 30min, ID token), e logout via end_session endpoint com id_token_hint.

### [05-multi-tenancy-strategy.md](./05-multi-tenancy-strategy.md)
Multi-tenancy via user attributes (tenants array, current_tenant string) mapeados para JWT claim tenant_id via protocol mapper User Attribute, permitindo tenant switcher no frontend chamando Admin API para atualizar current_tenant seguido de token refresh, com backend extraindo tenant_id do JWT para Row-Level Security PostgreSQL via SET app.tenant_id garantindo isolamento completo de dados entre prefeituras.
