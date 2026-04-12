---
type: rnf
status: approved
updated: 2026-01-25
---

# RNF-038: Backup de Dados

## Descricao

Sistema deve implementar backup automatico com multiplas camadas de protecao. Inclui banco PostgreSQL e object storage com fotos e documentos.

## Metricas

- Incremental: diario em horario de baixa atividade
- Full: semanal aos domingos
- Retencao: 30 dias (7 diarios + 4 semanais)

## Criterios de Aceitacao

1. Backups armazenados em regiao diferente da producao
2. Teste de restore mensal documentado com tempo medido
3. Alertas automaticos para falhas de backup
