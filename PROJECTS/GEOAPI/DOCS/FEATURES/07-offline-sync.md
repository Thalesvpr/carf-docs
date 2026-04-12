---
type: leaf
status: review
updated: 2026-02-08
---

# Offline Sync Feature

A feature de sincronizacao offline implementa o protocolo de comunicacao entre o app mobile REURBCAD e o servidor GEOAPI, permitindo que agentes de campo trabalhem sem conectividade e sincronizem dados quando a conexao estiver disponivel. O protocolo usa delta sync baseado em timestamp para minimizar payload e resolucao de conflitos por campo para maximizar preservacao de dados.

## User Stories

US-060 Pull de Mudancas: o app mobile solicita todas as alteracoes ocorridas desde a ultima sincronizacao informando o timestamp via parametro since. O servidor retorna colecoes separadas de registros criados, atualizados e excluidos para units, holders e communities.

US-061 Push de Operacoes: o app mobile envia batch de operacoes realizadas offline (CREATE, UPDATE, DELETE) para processamento sequencial. O servidor valida regras de negocio para cada operacao e retorna status individual (SUCCESS, CONFLICT, ERROR) com dados de conflito quando aplicavel.

US-062 Resolucao de Conflitos: quando o servidor detecta que um campo foi editado tanto no servidor quanto no client desde a ultima sincronizacao, retorna CONFLICT com serverVersion e clientVersion dos campos divergentes. O app exibe diff visual lado a lado permitindo escolha campo a campo.

## Endpoints

| Metodo | Rota | Descricao |
|--------|------|-----------|
| GET | /api/sync/changes?since= | Pull mudancas desde timestamp |
| POST | /api/sync/push | Push batch de operacoes |
| GET | /api/sync/status | Status da ultima sync |

## Regras de Negocio

RN-060: pull retorna apenas registros modificados apos o timestamp since, filtrados pelo tenant do usuario autenticado. RN-061: push processa operacoes sequencialmente na ordem recebida, validando regras de negocio para cada uma independentemente. RN-062: deteccao de conflito compara campo a campo usando version do registro, identificando divergencias entre a versao do servidor e a versao do client. RN-063: cada resultado do push inclui localId para correlacao com o ID local do WatermelonDB e serverId para registros criados. RN-064: response do pull inclui serverTimestamp para uso como parametro since no proximo pull e hasMore indicando se existem mais mudancas para paginar. RN-065: apenas usuarios com role field-coordinator ou field-cadastrator podem acessar endpoints de sync.

## Permissoes

| Acao | field-cadastrator | field-coordinator | analyst | manager | admin | super-admin |
|------|-------------------|-------------------|---------|---------|-------|-------------|
| Pull mudancas | sim | sim | nao | nao | nao | nao |
| Push operacoes | sim | sim | nao | nao | nao | nao |
| Status sync | sim | sim | nao | nao | nao | nao |
