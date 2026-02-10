---
type: leaf
status: review
updated: 2026-02-08
---

# Decision

Value object enum representando a decisao de analista em parecer tecnico sobre solicitacao de legitimacao fundiaria, determinando proximos passos no workflow. No banco de dados, corresponde ao campo legitimation_requests.decision (varchar(30), nullable).

A decisao e registrada em LegitimationResponse e determina a transicao de status do processo.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| APPROVED | Aprovado sem ressalvas, podendo avancar para proxima etapa. |
| REJECTED | Rejeitado com justificativa obrigatoria, retornando status para DRAFT. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Justificativa obrigatoria | REJECTED exige campo decision_reason preenchido com fundamentacao. |
| Progressao automatica | APPROVED permite avanco automatico no workflow. |
| Registro em resposta | Toda decisao deve estar vinculada a uma LegitimationResponse. |

Usado em legitimation_requests.decision registrando parecer, valida que REJECTED tem justificativa detalhada, dispara notificacoes diferentes conforme decisao, e alimenta metricas de taxa de aprovacao por analista.
