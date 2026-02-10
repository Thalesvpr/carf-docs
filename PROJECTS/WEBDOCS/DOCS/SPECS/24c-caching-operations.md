---
type: leaf
status: review
updated: 2026-02-07
---

# Caching Strategy - Operacoes e Troubleshooting

Invalidacao de cache, metricas e resolucao de problemas. Arquivo relacionado com 24a-caching-headers.md e 24b-caching-application.md.

## Invalidacao Manual

| Recurso | Metodo | Efeito |
|---------|--------|--------|
| Swagger spec | Acessar /api/swagger?refresh=true | Invalida cache in-memory e busca nova spec |
| JWKS | JWT validation failure | jwksCache.invalidate e retry automatico |

## Invalidacao Automatica por Deploy

Na Vercel, novo deploy cria novo edge cache. Assets imutaveis tem hash que muda gerando nova URL e novo cache. Cache in-memory e limpo no restart do servidor, primeira request apos deploy e cache miss (cold start).

## Metricas de Cache

| Fonte | Metrica | Descricao |
|-------|---------|-----------|
| Vercel Analytics | cache_hit_rate | Percentual de requests servidas do edge |
| Vercel Analytics | origin_requests | Requests que chegam ao servidor |
| Aplicacao | swagger_cache_hits | Contador de cache hits |
| Aplicacao | swagger_cache_misses | Contador de cache misses |
| Aplicacao | jwks_refreshes | Contador de refreshes de JWKS |

## Troubleshooting

| Problema | Causa | Solucao |
|----------|-------|---------|
| Conteudo desatualizado apos deploy | Browser cache com max-age alto | Hard refresh com Ctrl+Shift+R ou limpar cache |
| Swagger desatualizado | Cache in-memory nao invalidado | Acessar /api/swagger?refresh=true |
| JWT validation falha com nova chave | JWKS cache com chave antiga | Invalidar JWKS cache via codigo ou restart |
| Conteudo protegido cacheado | CDN cacheando pagina /dev/ | Verificar headers Cache-Control private |
