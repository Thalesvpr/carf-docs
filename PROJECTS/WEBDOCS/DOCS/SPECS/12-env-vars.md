---
type: leaf
status: review
updated: 2026-02-07
---

# Variaveis de Ambiente

Variaveis de ambiente do WEBDOCS. Prefixo PUBLIC_ exposto ao cliente, demais server-side only.

## Obrigatorias

| Variavel | Exemplo | Descricao |
|----------|---------|-----------|
| PUBLIC_SITE_URL | https://docs.carf.com.br | URL publica, https em producao |
| KEYCLOAK_URL | https://auth.carf.com.br | URL base do Keycloak |
| KEYCLOAK_REALM | carf | Nome do realm |
| KEYCLOAK_CLIENT_ID | carf-webdocs | Public client com PKCE |

## Opcionais

| Variavel | Default | Descricao |
|----------|---------|-----------|
| GEOAPI_URL | https://api.carf.com.br | URL da GeoAPI |
| GEOAPI_SWAGGER_PATH | /swagger/v1/swagger.json | Path da spec OpenAPI |
| STATUS_POLL_INTERVAL_MS | 30000 | Polling status page (>= 5000) |
| CACHE_TTL_SECONDS | 300 | TTL cache dados externos |
| LOG_LEVEL | info | debug, info, warn, error |

## Health Check

| Variavel | Default |
|----------|---------|
| GEOAPI_HEALTH_URL | https://api.carf.com.br/health |
| KEYCLOAK_HEALTH_URL | openid-configuration endpoint |
| MINIO_HEALTH_URL | https://storage.carf.com.br/minio/health/live |
| POSTGRES_HEALTH_URL | null, via GeoAPI |

## Por Ambiente

| Variavel | Dev | Staging | Prod |
|----------|-----|---------|------|
| PUBLIC_SITE_URL | localhost:4321 | docs.staging.carf.com.br | docs.carf.com.br |
| KEYCLOAK_URL | localhost:8080 | auth.staging | auth.carf.com.br |
| LOG_LEVEL | debug | info | warn |

## Decap CMS e Seguranca

GITHUB_CLIENT_ID e GITHUB_CLIENT_SECRET para OAuth do Decap CMS. Validacao em src/lib/config/env.ts com Zod, erro fatal se obrigatoria ausente. Sempre importar do modulo env. PUBLIC_ visivel no client-side, nunca para sensiveis. Usar secrets management do Vercel. Desenvolvimento usa .env.local ignorado pelo git.
