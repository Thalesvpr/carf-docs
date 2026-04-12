---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-042: Zero Downtime Deployment

## Descricao

Deploys devem ocorrer sem downtime perceptivel via rolling update no Kubernetes. Novas versoes sao introduzidas gradualmente enquanto antigas continuam servindo.

## Metricas

- Strategy: RollingUpdate com maxUnavailable = 0
- Rollback: automatico se error rate > 5% por 2 minutos
- Migracoes: apenas aditivas durante deploy

## Criterios de Aceitacao

1. Readiness probes implementados validando banco e dependencias
2. Rollback automatico via kubectl rollout undo quando falhar
3. Zero erros 5xx durante processo de deployment
