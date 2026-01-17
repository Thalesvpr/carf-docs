# Configurações dos 6 Clients

geoweb (SPA React): public client, standard flow, PKCE S256, redirectUris=[http://localhost:5173/*, https://geoweb.carf.example.com/*], webOrigins=[+], scopes=[openid, profile, email, roles, carf-tenant]. reurbcad (Mobile React Native): public client, standard flow, PKCE S256, redirectUris=[carf://callback, carf://oauth/callback, exp://localhost:19000/*], deep links configurados pra capturar callback OAuth. geoapi (Backend .NET): bearer-only, não gera tokens apenas valida JWT usando public key do Keycloak (JWKS endpoint https://keycloak:8080/realms/carf/protocol/openid-connect/certs), extrai claims tenant_id e roles pra autorização. geogis (Plugin QGIS): confidential client, service account enabled, client_secret necessário, pode fazer client credentials flow (POST /token com client_id+client_secret) pra obter token sem user ou standard flow com browser local (abre http://localhost:random_port/ pra callback). webdocs (Portal Docs): public client, principalmente conteúdo público, auth opcional pra seções internas protegidas, PKCE S256. admin (Console Admin Next.js): public client, PKCE S256, redirectUris=[http://localhost:3000/*, https://admin.carf.example.com/*], client roles [manage-users, manage-tenants, view-audit-logs], usa Keycloak Admin API (@keycloak/keycloak-admin-client npm package) pra gestão de tenants e usuários.

---

**Última atualização:** 2026-01-09
**Status do arquivo**: Review
