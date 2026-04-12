---
type: leaf
status: review
updated: 2026-02-07
---

# GEOAPI Health - Servico e Pagina

Detalhes do servico de health check e pagina de status. Documento complementar a 03-geoapi-health.md.

## Servico de Health Check

Modulo src/lib/health/service.ts exporta funcao checkService que recebe Service e retorna HealthResult com status, latency opcional, message opcional, e checks opcionais.

Se servico nao possui healthEndpoint, retorna unknown. Caso contrario, executa fetch com AbortSignal.timeout e headers opcionais. Verificacao inclui status code (unhealthy se diferente do esperado), body contains (degraded se ausente), e latencia (propaga status do JSON se disponivel).

Funcao checkAllServices executa Promise.all sobre todos servicos com endpoint, retorna Map de serviceId para HealthResult.

## Pagina de Status

Pagina em src/pages/status.astro renderiza com SSR verificando status em cada request. Calcula status geral: unhealthy se qualquer servico unhealthy, degraded se nenhum unhealthy mas algum degraded, healthy caso contrario.

Renderiza titulo, timestamp, banner com status geral colorido, e componente StatusGrid com servicos e resultados.
