---
type: leaf
status: review
updated: 2026-02-08
---

# ResponseAddedEvent

Domain event emitido quando parecer tecnico ou juridico e adicionado ao processo de legitimacao. Analise formal contribuindo para decisao final.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| RequestId | Guid | Processo. |
| ResponseId | Guid | LegitimationResponse. |
| ResponseType | string | PARECER_TECNICO, DECISAO, CONTESTACAO, CORRECAO. |
| ResponderId | Guid | Analista. |
| TenantId | Guid | Tenant. |

## Handlers

| Handler | Acao |
| --- | --- |
| ResponseNotificationHandler | Notifica requerente se NEEDS_CORRECTION. |
| ResponseStatusHandler | Atualiza status conforme decisao. |
| ResponseMetricsHandler | Incrementa contador por analista. |

## Contexto de Emissao

Emitido no metodo AddResponse(). Pode transicionar status conforme decisao.
