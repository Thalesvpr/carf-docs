---
type: leaf
status: review
updated: 2026-02-07
---

# Swagger Embutido - Detalhes

Detalhes do componente, servico de cache e layout. Documento complementar a 02-swagger-embutido.md.

## Componente SwaggerPage

Pagina em src/pages/dev/api/swagger.astro importa DevLayout e funcao getSwaggerSpec. Frontmatter obtem spec via await e serializa como JSON. Template renderiza div com id swagger-ui. Script client-side inicializa SwaggerUIBundle com spec deserializada, presets apis e StandaloneLayout, e requestInterceptor que extrai token do cookie carf_access_token para header Authorization.

## Servico de Cache

Modulo src/lib/swagger/cache.ts implementa cache em memoria com TTL de 5 minutos. Funcao getSwaggerSpec aceita forceRefresh e retorna cache se valido. Fetch usa variavel GEOAPI_SWAGGER_URL com timeout de 10 segundos. Funcao invalidateCache reseta cache.

## Layout DevLayout

Layout em src/layouts/DevLayout.astro extende BaseLayout verificando role dev. Inclui CSS e scripts do swagger-ui-dist versao 5 via unpkg CDN.

## Variavel de Ambiente

GEOAPI_SWAGGER_URL define URL da especificacao OpenAPI, por exemplo https://api.carf.com.br/swagger/v1/swagger.json.
