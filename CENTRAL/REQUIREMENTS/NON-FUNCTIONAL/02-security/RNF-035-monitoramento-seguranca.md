---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-035: Monitoramento de Seguranca

## Descricao

Sistema deve monitorar eventos de seguranca com alertas automaticos para padroes suspeitos. Permite resposta rapida a incidentes antes de danos significativos.

## Metricas

- Forca bruta: alerta apos 5+ falhas de login em 10 minutos do mesmo IP
- Logs: agregados em ELK Stack ou Loki+Grafana
- Alerting: integracao com PagerDuty/Opsgenie ou Slack/Teams

## Criterios de Aceitacao

1. Alertas para multiplas tentativas de login falhadas por IP
2. Notificacao imediata para mudancas em permissoes criticas
3. Dashboard de seguranca com metricas de acesso e erros
