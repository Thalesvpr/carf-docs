---
type: leaf
status: review
updated: 2026-02-08
---

# CommunityArchivedEvent

Domain event emitido por Community aggregate root quando comunidade e arquivada apos conclusao de processo de regularizacao ou cancelamento definitivo. Exige limpeza de recursos ativos e preservacao de historico para auditoria.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| CommunityId | Guid | Comunidade arquivada. |
| Reason | string | Motivo: REGULARIZACAO_CONCLUIDA, CANCELADO_SEM_VIABILIDADE, etc. |
| Justification | string | Justificativa textual detalhada. |
| ArchivedBy | Guid | AccountId que executou arquivamento. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Timestamp UTC. |

## Handlers

| Handler | Acao |
| --- | --- |
| ArchiveAuthorizationHandler | Revoga todas CommunityAuthorizations ativas. |
| ArchiveMetricsHandler | Decrementa contador de comunidades ativas. |
| ArchiveStorageHandler | Move documentos para storage de arquivo frio. |

## Contexto de Emissao

Emitido pelo agregado Community no metodo Archive(). Soft delete e aplicado preenchendo deleted_at, preservando historico.
