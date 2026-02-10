---
type: leaf
status: rejected
updated: 2026-02-08
description: Valor SUCCESS diverge do DOCS/DOMAIN/VALUE-OBJECTS/17-sync-status.md que usa SYNCED. Necessario alinhar nome do valor entre os dois arquivos.
---

# SyncStatus

Value object enum representando o estado de sincronizacao de operacoes offline do aplicativo mobile REURBCAD com o servidor GEOAPI, permitindo rastreamento e resolucao de conflitos em cenarios de conectividade intermitente. No banco de dados, e utilizado no contexto da tabela sync_logs para rastrear cada operacao.

O fluxo de sincronizacao envia operacoes CREATE, UPDATE e DELETE do dispositivo para o servidor, que valida versoes e aplica mudancas ou detecta conflitos.

## Valores Permitidos

| Valor | Descricao |
| --- | --- |
| PENDING | Operacao enviada pelo dispositivo aguardando processamento no servidor. |
| SUCCESS | Sincronizacao completada com sucesso e dados persistidos. |
| CONFLICT | Conflito detectado: BaseVersion do dispositivo difere do RowVersion atual no servidor. |
| FAILED | Falha no processamento por erro de validacao, constraint violada ou exception. |

## Regras de Validacao

| Regra | Descricao |
| --- | --- |
| Estado final | SUCCESS e CONFLICT resolvido sao estados finais. |
| Intervencao manual | CONFLICT com campos iguais alterados requer resolucao manual. |
| Retry permitido | FAILED pode ser reenviado apos correcao dos dados. |

## Metodos Principais

| Metodo | Retorno | Descricao |
| --- | --- | --- |
| IsResolved() | bool | Verifica se esta em estado final. |
| RequiresUserIntervention() | bool | Determina se CONFLICT precisa resolucao manual. |
| CanRetry() | bool | Verifica se FAILED pode ser reenviado. |

Usado em SyncLog.Status para rastrear cada operacao enviada pelo mobile. Dispara SyncConflictEvent quando detecta BaseVersion diferente do RowVersion, permitindo merge automatico para campos distintos ou resolucao manual pelo tecnico de campo.
