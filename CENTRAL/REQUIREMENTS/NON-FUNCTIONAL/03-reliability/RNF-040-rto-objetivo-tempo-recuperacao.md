---
id: RNF-040
type: RNF
modules: []
status: approved
created: 2026-01-23
updated: 2026-01-23
---

# RNF-040: RTO (Recovery Time Objective)

## Descricao

Tempo maximo aceitavel de downtime em caso de disaster recovery. Runbook documentado garante restauracao de servicos criticos dentro do periodo estabelecido.

## Metricas

- RTO: maximo 4 horas
- Automacao: minimo 80% dos passos via scripts
- Ambiente DR: hot, warm ou cold standby disponivel

## Criterios de Aceitacao

1. Runbook de DR completo e versionado com tempos estimados
2. Testes de DR trimestrais com relatorio de tempo medido
3. Infrastructure as Code (Terraform/Pulumi) para provisionamento
