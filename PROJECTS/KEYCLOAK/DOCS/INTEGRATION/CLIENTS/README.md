---
type: readme
status: review
updated: 2026-02-07
---

# CLIENTS

Configuracao dos seis clients OAuth2/OIDC no realm CARF, cada um com tipo e flow especifico para seu modelo de ameacas. Todos usam PKCE S256 e o scope customizado carf-tenant que injeta claims tenant_id, allowed_tenants e community_ids no JWT.

Quatro clients sao public: [REURBWEB](./01-reurbweb.md) SPA React para analistas, [REURBCAD](./02-reurbcad.md) app mobile React Native com deep links carf:// e suporte offline via offline_access, [WEBDOCS](./05-webdocs.md) portal VitePress com auth para secao /dev/, e [ADMIN](./06-reurbmaster.md) console Next.js para gestao de tenants e usuarios. O [GEOAPI](./03-geoapi.md) e bearer-only (.NET) que apenas valida tokens JWT sem participar de fluxos de login. O [GEOGIS](./04-geogis.md) e o unico confidential, suportando tanto Authorization Code com PKCE (usuario humano) quanto Client Credentials (M2M).

<!-- CARF-INDEX-START -->
> ⚠️ **Índice gerado automaticamente.** Não edite manualmente.
> Use os links abaixo para referenciar documentos desta pasta.

## Documentos (6)

| Documento | Status |
|-----------|--------|
| [Client REURBWEB](./01-reurbweb.md) | ⚠ |
| [Client REURBCAD](./02-reurbcad.md) | ⚠ |
| [Client GEOAPI](./03-geoapi.md) | ⚠ |
| [Client GEOGIS](./04-geogis.md) | ⚠ |
| [Client WEBDOCS](./05-webdocs.md) | ⚠ |
| [Client REURBMASTER](./06-reurbmaster.md) | ⚠ |

<!-- CARF-INDEX-END -->
