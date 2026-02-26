---
type: leaf
status: review
updated: 2026-02-07
---

# Deployment - ADMIN

## Deploy

O deploy do REURBMASTER e feito para Vercel como static SPA. O comando de build gera o diretorio dist/ contendo HTML e JS bundle otimizados via Vite. A Vercel serve arquivos estaticos via CDN com caching headers de max-age 1 year para assets e stale-while-revalidate para HTML. O routing client-side via React Router utiliza fallback para index.html configurado na Vercel com regra de rewrite que direciona todas as rotas para index.html. As variaveis de ambiente VITE_API_URL e VITE_KEYCLOAK_URL sao configuradas no Vercel dashboard. Preview deployments sao criados automaticamente em cada PR permitindo testar mudancas antes de producao. O production deployment ocorre no merge para main com healthcheck validando que a rota raiz retorna 200 antes de finalizar.

## Configuracao Vercel

| Propriedade | Valor | Descricao |
|-------------|-------|-----------|
| rewrites | todas as rotas para /index.html | Suporte a client-side routing |
| Cache-Control para /assets/ | public, max-age=31536000, immutable | Cache longo para assets estaticos |
| VITE_API_URL | URL do GEOAPI | Variavel de ambiente configurada no dashboard |
| VITE_KEYCLOAK_URL | URL do Keycloak | Variavel de ambiente configurada no dashboard |

## Build e Preview

Para gerar o build de producao, executar o comando de build via bun que gera o diretorio dist/ otimizado. Para validacao local antes de deploy, executar o comando de preview via bun que serve o build em modo producao na porta 4173. O deploy para producao pode ser acionado automaticamente via push para branch main ou manualmente via CLI da Vercel com flag de producao.
