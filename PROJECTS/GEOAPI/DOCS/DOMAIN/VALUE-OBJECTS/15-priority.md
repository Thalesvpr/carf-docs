---
type: leaf
status: review
updated: 2026-02-08
---

# Priority

Value object enum imutavel representando nivel de prioridade de anotacoes do tipo ISSUE e REMINDER. Persiste na coluna priority varchar(10) da tabela annotations, nullable. Obrigatorio quando annotation_type e ISSUE ou REMINDER, opcional para NOTE e WARNING.

## Valores Permitidos

| Valor | Descricao | SLA Sugerido |
|-------|-----------|-------------|
| LOW | Baixa prioridade. Pendencia menor sem impacto no workflow. | 30 dias |
| NORMAL | Prioridade padrao. Requer atencao em prazo razoavel. | 15 dias |
| HIGH | Alta prioridade. Impacta aprovacao ou progresso de trabalho. | 5 dias |
| URGENT | Urgente. Requer atencao imediata. Bloqueia workflow ate resolucao. | 1 dia |

Priority influencia a ordenacao de pendencias em dashboards e a frequencia de notificacoes de lembrete enviadas aos responsaveis.
