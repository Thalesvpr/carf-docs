---
type: leaf
status: review
updated: 2026-02-07
---

# Integracao GEOAPI Swagger - Detalhes

Customizacao visual, servico de cache e pagina do Swagger. Documento complementar a 04-geoapi-swagger.md.

## Customizacao Visual

Cores por metodo HTTP seguem padrao Swagger: GET em azul (#61affe), POST em verde (#49cc90), PUT em laranja (#fca130), DELETE em vermelho (#f93e3e). Topbar e escondido. Font family herda do Starlight via --sl-font.

Tema escuro ajusta cores de texto para --sl-color-text em summaries, parametros, responses, tabs e models. Inputs e textareas usam --sl-color-bg como background. Section headers com background semi-transparente branco. Model boxes com background semi-transparente.

## Servico de Cache

Modulo src/lib/swagger/cache.ts implementa cache em memoria com TTL de 5 minutos. Funcao getSwaggerSpec aceita forceRefresh e retorna cache se valido. Fetch usa variavel GEOAPI_SWAGGER_URL com timeout de 15 segundos. Valida presenca de campo openapi ou swagger na resposta.

Funcao invalidateCache reseta cache para null. Funcao getCacheAge retorna idade do cache em millisegundos ou null se vazio.

## Pagina do Swagger

Pagina em src/pages/dev/api/swagger.astro com prerender false para SSR. Importa DevLayout e SwaggerEmbed. Exibe titulo, email do usuario autenticado, e link para recarregar especificacao.

Variavel de ambiente GEOAPI_SWAGGER_URL define URL do endpoint swagger.json, por exemplo https://api.carf.com.br/swagger/v1/swagger.json.
