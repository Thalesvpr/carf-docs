---
type: leaf
status: review
updated: 2026-02-07
---

# Integracao com GEOAPI Health

Status page do WEBDOCS consome endpoints /health dos servicos CARF para exibir disponibilidade em tempo real. Integracao via fetch server-side durante SSR garante informacoes atuais sem expor URLs internas ao cliente.

Endpoint /health da GEOAPI retorna JSON com status (healthy, degraded, unhealthy), checks individuais (database, keycloak, minio), e timestamp. Response inclui latencia de cada dependencia.

Componente StatusPage.astro executa fetch para cada servico configurado em src/config/services.ts durante SSR. Timeout de 5 segundos previne bloqueio por servico lento. Servicos sem resposta sao marcados como unknown.

Servicos monitorados: GEOAPI verificando /health, Keycloak verificando /.well-known/openid-configuration, MinIO verificando /minio/health/live. Client-side polling opcional a cada 30 segundos, desabilitado por padrao.

## Formato de Resposta

Response JSON com campos status (string), timestamp (ISO 8601), version (semver), uptime (string), e checks (sub-checks).

| Check | Detalhes incluidos |
|-------|-------------------|
| database | connections, maxConnections, pendingQueries |
| keycloak | realm, tokenEndpoint (reachable/unreachable) |
| minio | bucket, availableSpace |
| redis | message (se degraded), memoryUsage |

## Status Possiveis

| Status | Descricao | Cor |
|--------|-----------|-----|
| healthy | Operando normalmente | Verde |
| degraded | Operando com problemas | Amarelo |
| unhealthy | Indisponivel | Vermelho |
| unknown | Nao verificavel | Cinza |

Detalhes do servico de health check e pagina de status em 03-geoapi-health-servico.md.
