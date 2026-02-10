---
type: leaf
status: review
updated: 2026-02-07
---

# Deploy para Vercel

Guia para configurar e executar deploy do WEBDOCS na plataforma Vercel.

## Configuracao Inicial

Conectar repositorio GitHub ao Vercel via dashboard. Criar novo projeto selecionando repositorio do WEBDOCS. Vercel detecta automaticamente framework Astro e configura build settings padrao. Root directory deve apontar para SRC-CODE/carf-webdocs se repositorio e monorepo.

## Configuracao de Build (vercel.json)

| Propriedade | Valor |
|---|---|
| framework | astro |
| buildCommand | bun run build |
| installCommand | bun install |
| outputDirectory | dist |
| regions | gru1 |

Headers configurados por rota: rotas /api/ usam Cache-Control no-store must-revalidate; rotas /_astro/ usam cache publico imutavel com max-age de um ano; todas rotas incluem X-Content-Type-Options nosniff, X-Frame-Options DENY e Referrer-Policy strict-origin-when-cross-origin.

Rewrites mapeiam /health para /api/health. Redirects permanentes mapeiam /docs para /guia/ e /swagger para /dev/api/swagger/. Functions em src/pages/api/ tem maxDuration de 30 segundos e status page tem 60 segundos.

## Variaveis de Ambiente

| Variavel | Producao | Preview |
|---|---|---|
| PUBLIC_APP_URL | https://docs.carf.com.br | https://preview-webdocs.vercel.app |
| KEYCLOAK_URL | https://auth.carf.com.br | https://auth-staging.carf.com.br |
| KEYCLOAK_REALM | carf | carf-staging |
| KEYCLOAK_CLIENT_ID | webdocs | webdocs-preview |
| GEOAPI_URL | https://api.carf.com.br | https://api-staging.carf.com.br |
| GEOAPI_SWAGGER_URL | URL swagger producao | URL swagger staging |

Configurar em Settings, Environment Variables no dashboard Vercel. Marcar variaveis sensiveis como sensitive.

## Deploy e Rollback

Deploy automatico acontece em push para branch main via webhook. Preview deployments criados para PRs com URL unica no formato webdocs-git-BRANCH-carf.vercel.app. Rollback manual via CLI Vercel com comando vercel rollback seguido da URL do deployment, ou via dashboard em Deployments selecionando deploy anterior e Promote to Production.

## Health Check

API route em src/pages/api/health.ts retorna JSON com status healthy, timestamp e versao (commit SHA do Vercel). Endpoint acessivel via /health gracas ao rewrite configurado.

## Checklist

| Item |
|---|
| Repositorio conectado ao Vercel |
| vercel.json na raiz do projeto |
| Variaveis de ambiente configuradas (prod e preview) |
| Dominio customizado configurado |
| DNS apontando para Vercel |
| SSL certificado ativo |
| Health check funcionando |
| Preview deployment testado |
