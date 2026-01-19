# CLIENTS

Configuração dos seis clients Keycloak para as aplicações do ecossistema CARF, cada um com settings específicos para seu tipo de autenticação.

O [GEOWEB](./01-geoweb.md) é SPA React usando public client com PKCE. O [REURBCAD](./02-reurbcad.md) é app mobile React Native também public com PKCE e deep links. O [GEOAPI](./03-geoapi.md) é backend .NET configurado como bearer-only para validação de tokens. O [GEOGIS](./04-geogis.md) é plugin QGIS como confidential client com service account para client credentials flow. O [WEBDOCS](./05-webdocs.md) é portal de documentação Astro com auth para seção dev. O [ADMIN](./06-admin.md) é console Next.js com acesso à Admin API do Keycloak.

---

**Última atualização:** 2026-01-17
**Status do arquivo**: Review

<!-- GENERATED:START - Nao edite abaixo desta linha -->
## Arquivos (6 arquivos)

| ID | Titulo |
|:---|:-------|
| [01-geoweb](./01-geoweb.md) | Client GEOWEB |
| [02-reurbcad](./02-reurbcad.md) | Client REURBCAD |
| [03-geoapi](./03-geoapi.md) | Client GEOAPI |
| [04-geogis](./04-geogis.md) | Client GEOGIS |
| [05-webdocs](./05-webdocs.md) | Client WEBDOCS |
| [06-admin](./06-admin.md) | Client ADMIN |

*Gerado automaticamente em 2026-01-17 11:57*
<!-- GENERATED:END -->

---

**Status:** Review
**Atualizado:** 2026-01-19
**Descrição:** 
