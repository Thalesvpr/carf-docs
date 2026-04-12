---
type: leaf
status: review
updated: 2026-02-07
---

# Integracao com GEOAPI Swagger

Secao /dev/swagger/ do WEBDOCS renderiza documentacao interativa da API GEOAPI consumindo especificacao OpenAPI diretamente do backend. Integracao permite testar endpoints usando token JWT real do desenvolvedor logado.

Especificacao OpenAPI e gerada automaticamente pela GEOAPI via Swashbuckle a partir dos controllers .NET com XML comments. Endpoint /swagger/v1/swagger.json retorna JSON atualizado refletindo estado atual da API.

Componente SwaggerEmbed.astro executa fetch da especificacao durante SSR, inicializa swagger-ui-dist com spec inline, e configura requestInterceptor para adicionar header Authorization: Bearer com token do cookie de sessao.

Autorizacao verifica role dev antes de renderizar. Usuarios sem role recebem mensagem explicando necessidade de acesso de desenvolvedor.

Cache da especificacao em memoria por 5 minutos reduz carga no backend. Invalidacao via query param ?refresh=true forca novo fetch.

## Componente SwaggerEmbed.astro

Componente em src/components/SwaggerEmbed.astro aceita prop class opcional. Verifica query param refresh para invalidar cache. Executa getSwaggerSpec com tratamento de erro exibindo mensagem e link para retry. Script client-side inicializa SwaggerUIBundle com spec, deepLinking, presets apis e StandaloneLayout, filtro habilitado, tryItOutEnabled. RequestInterceptor extrai token do cookie. ResponseInterceptor loga warnings para responses 400+.

Detalhes de customizacao visual, cache e pagina em 04-geoapi-swagger-detalhes.md.
