---
type: leaf
status: review
updated: 2026-02-08
---

# Sync Commands

Os commands de sincronizacao implementam o lado de escrita do protocolo de sync entre REURBCAD e GEOAPI. O PushChangesCommand processa batch de operacoes offline com deteccao de conflitos por campo, enquanto ResolveConflictCommand permite resolucao manual de conflitos pendentes.

---

## PushChangesCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| Operations | List de SyncOperation | sim | Batch de operacoes locais |

Cada SyncOperation contem:

| Campo | Tipo | Descricao |
|-------|------|-----------|
| EntityType | string | UNIT, HOLDER ou DOCUMENT |
| LocalId | string | ID local do WatermelonDB |
| Operation | string | CREATE, UPDATE ou DELETE |
| Payload | object | Dados da entidade |
| ClientTimestamp | DateTime | Timestamp da operacao no client |

O handler processa operacoes sequencialmente na ordem recebida. Para cada operacao, valida regras de negocio conforme o tipo de entidade, detecta conflitos comparando version do registro no servidor com a versao esperada pelo client e registra a operacao em sync_logs para rastreabilidade.

O resultado para cada operacao inclui localId, status (SUCCESS quando processada sem conflito, CONFLICT quando detectada divergencia, ERROR quando validacao falha), serverId (UUID atribuido pelo servidor em CREATE) e conflictData (objeto nullable com serverVersion e clientVersion dos campos divergentes quando CONFLICT).

A deteccao de conflito compara campo a campo: se o servidor tem version diferente da esperada pelo client e ambos alteraram o mesmo campo desde a ultima sincronizacao, o conflito e sinalizado para aquele campo especifico.

---

## ResolveConflictCommand

| Parametro | Tipo | Obrigatorio | Descricao |
|-----------|------|-------------|-----------|
| EntityType | string | sim | Tipo da entidade em conflito |
| EntityId | Guid | sim | ID do servidor da entidade |
| Resolution | object | sim | Campos resolvidos com valores escolhidos |

O handler aplica os valores resolvidos sobre o registro do servidor, incrementa version e marca o conflito como resolvido em sync_logs com conflict_resolved igual a true. Emite SyncConflictResolvedEvent com EntityType, EntityId e campos resolvidos.
