---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-065: Rollback de Deploy

## Descricao

Deploys de GEOAPI e GEOWEB devem ser revertiveis em menos de 5 minutos. Permite mitigar rapidamente incidentes causados por versoes defeituosas.

## Metricas

- Tempo de rollback: maximo 5 minutos
- Versionamento: imagens Docker com tag de commit SHA
- Historico: revisoes mantidas pelo Kubernetes

## Criterios de Aceitacao

1. kubectl rollout undo reverte para versao anterior
2. Migracoes de banco com scripts de downgrade quando possivel
3. Runbook documentado com procedimento de rollback testado
