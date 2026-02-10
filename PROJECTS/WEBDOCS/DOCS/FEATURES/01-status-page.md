---
type: leaf
status: review
updated: 2026-02-07
---

# Status Page

Pagina /status/ exibe disponibilidade em tempo real dos servicos CARF permitindo usuarios verificarem se sistema esta operacional. Implementacao combina checks server-side durante SSR com polling opcional client-side.

Layout apresenta card para cada servico com indicador visual de status (verde healthy, amarelo degraded, vermelho unhealthy, cinza unknown), nome, latencia, e timestamp. Secao inferior mostra historico de incidentes recentes.

## Configuracao de Servicos

Servicos monitorados configurados em src/config/services.ts com variaveis de ambiente para URLs.

| Servico | ID | Endpoint | Critico | Nota |
|---------|-----|----------|---------|------|
| GeoAPI | geoapi | GEOAPI_HEALTH_URL | Sim | Esperado: 200 com { status: healthy } |
| Autenticacao | keycloak | KEYCLOAK_HEALTH_URL | Sim | Esperado: 200 com issuer |
| Armazenamento | minio | MINIO_HEALTH_URL | Nao | Esperado: 200 |
| Banco de Dados | postgres | via geoapi | Sim | Verificado indiretamente |

Polling usa intervalo 30s, 2 retries com delay 1000ms, toggle pelo usuario.

## Estados de Status

| Estado | Condicao | Cor | Label |
|--------|----------|-----|-------|
| online | Response 200 dentro do timeout | #22c55e | Operacional |
| degraded | Response 200 com latencia acima de 2000ms | #eab308 | Degradado |
| offline | Response diferente de 200 ou timeout | #ef4444 | Indisponivel |
| unknown | Erro de rede ou primeira verificacao | #6b7280 | Desconhecido |

Health check executa durante SSR com Promise.allSettled paralelo. Historico em collection Decap CMS com frontmatter de data, servicos afetados, descricao, e status.

Interfaces de dados e detalhes tecnicos em 01-status-page-detalhes.md.
