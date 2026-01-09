# Configuração do Realm Keycloak

Realm "carf" com 6 clients (geoweb, reurbcad, geoapi, geogis, webdocs, admin), 4 realm roles (field-collector, analyst, admin, super-admin) sendo admin composite de analyst+field-collector e super-admin composite de admin+analyst+field-collector, user attributes `tenants: []` (array) e `current_tenant` (string) mapeados pra JWT claims `tenant_id` e `allowed_tenants` via protocol mappers oidc-usermodel-attribute-mapper, SSO session idle 30min (1800s) e max 10h (36000s), refresh token uso único (max reuse = 0), access token 5min (300s), password policy "length(8) and digits(1) and lowerCase(1) and upperCase(1) and specialChars(1) and notUsername", brute force protection 5 tentativas com bloqueio 15min, PKCE obrigatório (code_challenge_method = S256) pra todos public clients (geoweb, reurbcad, admin).

## Clients

geoweb: publicClient=true, standardFlowEnabled=true, redirectUris=[http://localhost:5173/*, https://geoweb.carf.example.com/*], webOrigins=[+], pkce=S256. reurbcad: publicClient=true, redirectUris=[carf://callback, exp://localhost:19000/*], pkce=S256. geoapi: bearerOnly=true (não gera tokens, só valida). geogis: publicClient=false, serviceAccountsEnabled=true, clientSecret=*****, redirectUris=[http://localhost:*/, http://127.0.0.1:*/], pkce=S256. webdocs: publicClient=true, redirectUris=[http://localhost:5173/*, https://thalesvpr.github.io/carf-webdocs/*], pkce=S256. admin: publicClient=true, redirectUris=[http://localhost:3000/*, https://admin.carf.example.com/*], pkce=S256, clientRoles=[manage-users, manage-tenants, view-audit-logs].

## Protocol Mappers

Mapper "tenant_id": protocolMapper=oidc-usermodel-attribute-mapper, user.attribute=current_tenant, claim.name=tenant_id, jsonType=String, incluir em id_token+access_token+userinfo. Mapper "allowed_tenants": user.attribute=tenants, claim.name=allowed_tenants, jsonType=JSON, multivalued=true, incluir em id_token+access_token+userinfo. JWT resultante tem `{"tenant_id": "prefeitura-a", "allowed_tenants": ["prefeitura-a", "prefeitura-b"], "roles": ["analyst"]}`.

## Roles

field-collector: permissões básicas de coleta (criar unidade, foto, documento) sem aprovar ou deletar. analyst: tudo de field-collector + editar/aprovar/rejeitar + relatórios. admin: tudo de analyst + gerenciar usuários do tenant + configurações. super-admin: tudo + criar tenants + transferir usuários entre tenants + acesso a qualquer tenant via switcher especial.

---

**Última atualização:** 2026-01-09
