---
type: leaf
status: review
updated: 2026-02-08
---

# Priority

Value object enum representando nivel de prioridade aplicavel a diversos contextos do sistema como anotacoes e solicitacoes de legitimacao. No banco de dados, corresponde ao campo annotations.priority (varchar(10), nullable) sendo obrigatorio para tipos ISSUE e REMINDER.

A prioridade influencia SLA de resposta, ordenacao em filas de trabalho e tipo de notificacao disparada.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| LOW | Baixa prioridade para tarefas que podem aguardar sem impacto em prazos. SLA: 168h. |
| NORMAL | Prioridade padrao para fluxo regular de trabalho. SLA: 72h. |
| HIGH | Alta prioridade para situacoes que exigem atencao breve. SLA: 24h. |
| URGENT | Urgencia maxima para casos criticos que bloqueiam processos ou afetam prazos legais. SLA: 4h. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Obrigatoriedade | Obrigatorio para annotations com tipo ISSUE e REMINDER. |
| Escalacao | URGENT e HIGH permitem escalacao automatica apos timeout de SLA. |
| Notificacoes | URGENT dispara alertas imediatos via email e push; LOW apenas registra in-app. |

Usado em Annotation.Priority para definir criticidade de ISSUE e urgencia de REMINDER, em LegitimationRequest influenciando ordem de analise na fila de trabalho, e alimenta relatorios gerenciais mostrando distribuicao e compliance de SLA.
