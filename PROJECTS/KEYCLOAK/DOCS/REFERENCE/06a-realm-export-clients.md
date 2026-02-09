---
type: leaf
status: review
updated: 2026-02-07
---

# Realm Export - Clients e Client Scopes

Secoes do realm-export.json referentes a clients e client scopes do realm CARF.

## Campos de Client

| Campo | Tipo | Descricao |
|:------|:-----|:----------|
| clientId | string | Identificador unico |
| publicClient | boolean | true para SPAs, false para confidential |
| secret | string | Secret para confidenciais |
| standardFlowEnabled | boolean | Authorization Code flow |
| serviceAccountsEnabled | boolean | Client Credentials flow |
| bearerOnly | boolean | Apenas validacao de tokens |
| redirectUris | array | URIs de redirect permitidas |
| webOrigins | array | CORS origins permitidas |

## Clients do Realm CARF

| Client | Tipo | Flow | Descricao |
|:-------|:-----|:-----|:----------|
| geoweb | publico | Auth Code + PKCE | Frontend React |
| reurbcad | publico | Auth Code + PKCE | Mobile React Native |
| geoapi | bearer-only | Validacao tokens | Backend .NET |
| geogis | confidential | Auth Code + Credentials | Plugin QGIS |
| webdocs | publico | Auth Code + PKCE | Portal Documentacao |
| admin | publico | Auth Code + PKCE | Frontend Administrativo |

Todos exceto geoapi usam PKCE com S256. Todos compartilham defaultClientScopes: web-origins, acr, profile, roles, email e carf-tenant.

## Client Scope carf-tenant

O scope carf-tenant injeta informacoes de tenant nos tokens via tres protocol mappers oidc-usermodel-attribute-mapper:

| Mapper | User Attribute | Claim | Tipo | Multivalued |
|:-------|:---------------|:------|:-----|:------------|
| tenant_id | current_tenant | tenant_id | String | nao |
| allowed_tenants | tenants | allowed_tenants | JSON | sim |
| community_ids | community_ids | community_ids | JSON | sim |

Todos emitem claims em id_token, access_token e userinfo. O carf-tenant integra os defaultDefaultClientScopes com role_list, profile, email, roles, web-origins e acr.

Ver [06-realm-export-schema](./06-realm-export-schema.md) para estrutura raiz e [06b-realm-export-roles](./06b-realm-export-roles.md) para roles.
