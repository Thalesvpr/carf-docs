---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-036: Uptime

## Descricao

GEOAPI e REURBWEB devem manter alta disponibilidade conforme SLA estabelecido. Health checks verificam conectividade com todos componentes criticos da arquitetura.

## Metricas

- Disponibilidade: 99.5% mensal (max 3.65h downtime/mes)
- Health checks: a cada 1-5 minutos de multiplas localizacoes
- Monitoramento: 24/7 via UptimeRobot, Pingdom ou Datadog

## Criterios de Aceitacao

1. Health checks implementados verificando banco, cache e storage
2. Alertas automaticos com escalacao apos 5 minutos sem resposta
3. Status page publico informando disponibilidade e incidentes
