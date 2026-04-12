---
type: leaf
status: review
updated: 2026-02-07
---

# Environment Variables - Operacoes

Variaveis de ambiente do Keycloak para HTTP, proxy, health, logging, cache e temas.

## HTTP e HTTPS

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_HTTP_ENABLED | Habilita HTTP porta 8080 | false |
| KC_HTTP_PORT | Porta HTTP | 8080 |
| KC_HTTP_RELATIVE_PATH | Path base | / |
| KC_HTTPS_PORT | Porta HTTPS | 8443 |
| KC_HTTPS_CERTIFICATE_FILE | Caminho do certificado | - |
| KC_HTTPS_CERTIFICATE_KEY_FILE | Caminho da chave privada | - |

## Proxy

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_PROXY | Modo de proxy | none |

Valores: none (sem proxy), edge (proxy termina TLS), reencrypt (re-encrypta para Keycloak) e passthrough (TLS pass-through). Atras de nginx/traefik usar edge.

## Health e Metrics

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_HEALTH_ENABLED | Endpoints /health | false |
| KC_METRICS_ENABLED | Metricas Prometheus | false |

Endpoints: /health, /health/live (liveness), /health/ready (readiness), /metrics.

## Logging

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_LOG_LEVEL | Nivel de log | info |
| KC_LOG | Formato de output | console |
| KC_LOG_CONSOLE_FORMAT | Formato console | default |
| KC_LOG_FILE | Arquivo de log | - |

Producao: warn com json. Desenvolvimento: debug.

## Cache e Features

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_CACHE | Tipo de cache | ispn |
| KC_CACHE_STACK | Stack de rede | - |
| KC_FEATURES | Features adicionais | - |
| KC_FEATURES_DISABLED | Features desabilitadas | - |

## Temas

| Variavel | Descricao | Padrao |
|:---------|:----------|:-------|
| KC_SPI_THEME_STATIC_MAX_AGE | Cache de assets (segundos) | 2592000 |
| KC_SPI_THEME_CACHE_THEMES | Cache de temas | true |
| KC_SPI_THEME_CACHE_TEMPLATES | Cache de templates | true |

Para desenvolvimento usar KC_CACHE local e desabilitar caches de tema. Para realm import, montar arquivo em /opt/keycloak/data/import/ e usar --import-realm.

Ver [05-environment-variables](./05-environment-variables.md) para credenciais, database e hostname.
