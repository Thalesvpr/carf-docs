---
type: leaf
status: review
updated: 2026-02-07
---

# Caching Strategy - Cache de Aplicacao

Cache in-memory no nivel da aplicacao para dados dinamicos. Arquivo relacionado com 24a-caching-headers.md e 24c-caching-operations.md.

## Swagger Spec Cache

Implementacao em src/lib/cache/swagger-cache.ts usando Map em memoria. Chave swagger_spec_version, TTL de 300 segundos (5 minutos), invalidacao manual via query param refresh=true ou restart do servidor. Limite de 1 spec por ambiente.

Classe SwaggerCache com Map privado e TTL default de 5 minutos. Metodo get recebe chave, funcao fetcher e TTL opcional. Verifica se entrada existe e nao expirou (cache hit retorna dados). Em cache miss ou expiracao executa fetcher, salva resultado com timestamp e TTL, retorna dados. Metodos invalidate para chave especifica e invalidateAll para limpar tudo.

Uso no endpoint src/pages/api/swagger.ts: verifica query param refresh para invalidacao forcada, chama swaggerCache.get com chave geoapi_swagger e fetcher que faz fetch da spec OpenAPI no GEOAPI_URL/swagger/v1/swagger.json. Retorna Response JSON com header Cache-Control public max-age 60.

## JWKS Cache

Implementacao em src/lib/auth/jwks-cache.ts usando jose library createRemoteJWKSet. TTL de 86400 segundos (24 horas). Triggers de invalidacao: JWT validation falha com unknown key, ou 24 horas desde ultima atualizacao.

Classe JWKSCache com entrada privada e TTL de 24 horas. Metodo getJWKS verifica se cache valido, se nao cria novo JWKS apontando para URL do Keycloak /realms/REALM/protocol/openid-connect/certs usando createRemoteJWKSet. Jose faz cache interno adicional. Metodo invalidate limpa cache. Chaves publicas mudam raramente mas devem ser atualizadas em rotacao.

## Status Page

Pagina de status nao usa cache, sempre server-rendered com SSR em cada request. Headers forcados no response: Cache-Control no-cache no-store must-revalidate, Pragma no-cache, Expires 0. Health checks executados em cada request contra todos os servicos.
