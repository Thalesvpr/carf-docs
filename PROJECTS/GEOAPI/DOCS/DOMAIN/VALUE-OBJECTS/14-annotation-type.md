---
type: leaf
status: review
updated: 2026-02-08
---

# AnnotationType

Value object enum imutavel representando o tipo de anotacao vinculada a uma entidade. Persiste na coluna annotation_type varchar(30) da tabela annotations com CHECK constraint. Determina comportamento, visualizacao e campos obrigatorios adicionais.

## Valores Permitidos

| Valor | Descricao | Priority | DueDate |
|-------|-----------|----------|---------|
| NOTE | Nota informativa simples sem acao requerida. | opcional | nao aplicavel |
| WARNING | Alerta sobre situacao que merece atencao. | opcional | nao aplicavel |
| ISSUE | Problema que requer resolucao. Rastreavel via IsResolved. | obrigatorio | opcional |
| REMINDER | Lembrete com prazo. Dispara notificacao ao se aproximar. | obrigatorio | obrigatorio |

## Comportamentos por Tipo

NOTE e WARNING sao informativos sem workflow de resolucao. ISSUE permite marcar como resolvido via Resolve(accountId) e aparece em dashboards de pendencias. REMINDER agenda verificacao de prazo via Hangfire e dispara notificacao push quando DueDate se aproxima.
