---
type: leaf
status: review
updated: 2026-02-08
---

# SyncStatus

Value object enum imutavel representando o estado de sincronizacao de uma operacao entre o app mobile REURBCAD e o servidor GEOAPI. Utilizado pela tabela sync_logs para rastrear cada operacao de sincronizacao.

## Valores Permitidos

| Valor | Descricao |
|-------|-----------|
| PENDING | Operacao local aguardando envio ao servidor. |
| SYNCED | Operacao enviada e confirmada pelo servidor. |
| CONFLICT | Conflito detectado entre versao local e servidor. Requer resolucao. |
| FAILED | Falha na sincronizacao. Sera retentada automaticamente. |

## Resolucao de Conflitos

Conflitos ocorrem quando a versao do registro no servidor diverge da versao local (coluna version). Estrategia padrao: server-wins para dados criticos (status, aprovacoes), last-write-wins para dados descritivos (observacoes, campos custom). Conflitos nao-resolvidos automaticamente sao apresentados ao usuario para decisao manual.
