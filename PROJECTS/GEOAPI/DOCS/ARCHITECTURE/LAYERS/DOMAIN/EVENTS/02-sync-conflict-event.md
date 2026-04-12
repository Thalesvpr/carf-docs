---
type: leaf
status: review
updated: 2026-02-08
---

# SyncConflictEvent

Domain event emitido quando conflito de sincronizacao offline e detectado durante processamento de sync_logs, indicando que o app mobile tentou modificar entidade alterada por outro usuario entre download e upload. Exige resolucao manual ou automatica do conflito.

O evento e emitido pela camada de aplicacao (SyncService) ao detectar que BaseVersion do dispositivo difere do RowVersion atual da entidade no servidor.

## Payload

| Campo | Tipo | Descricao |
| --- | --- | --- |
| SyncLogId | Guid | Identificador do log de sync conflitante. |
| EntityType | EntityType | Tipo da entidade: UNIT, HOLDER, COMMUNITY. |
| EntityId | Guid | ID da entidade conflitante. |
| DeviceId | string | Identificador do dispositivo mobile. |
| AccountId | Guid | Usuario do app que fez alteracao. |
| BaseVersion | int | Version que dispositivo tinha ao modificar. |
| CurrentVersion | int | Version atual no servidor. |
| Operation | string | CREATE, UPDATE ou DELETE. |
| TenantId | Guid | Tenant do contexto. |
| OccurredAt | DateTime | Quando conflito foi detectado. |

## Handlers

| Handler | Acao |
| --- | --- |
| SyncConflictNotificationHandler | Cria notificacao push para app mobile alertando sobre conflito. |
| SyncConflictAutoResolveHandler | Tenta merge automatico de campos nao conflitantes. |
| SyncConflictQueueHandler | Enfileira conflito para revisao manual em dashboard. |

## Contexto de Emissao

Emitido pela camada de aplicacao no SyncService quando BaseVersion difere de RowVersion. Conflitos de campos distintos podem ser resolvidos automaticamente; conflitos no mesmo campo requerem decisao humana.
