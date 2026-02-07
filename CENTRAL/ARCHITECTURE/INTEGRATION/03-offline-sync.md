---
type: leaf
status: approved
updated: 2026-01-24
---

# Offline Sync

Estrategia de sincronizacao entre REURBCAD mobile e GEOAPI para operacao em areas sem conectividade. A equipe de campo (Coordenador e Cadastrador) so tem acesso aos dados apos o Analista publicar seu trabalho no backend. Antes de operar offline, o usuario de campo realiza download unico e temporario do pacote contendo ortofoto e poligonos do tenant designado. Dados coletados em campo sao armazenados localmente em WatermelonDB e sincronizados quando conexao esta disponivel.

Sincronizacao usa pull-push model. Pull baixa mudancas do servidor desde ultima sync usando timestamp de versao. Push envia mudancas locais em batch ordenado por dependencia. Conflitos sao detectados por versao do registro e resolvidos com estrategia last-write-wins para campos simples e merge para colecoes.

## Fila de Upload

Operacoes pendentes ficam em fila persistente ordenada por prioridade e timestamp. Unidades aprovadas tem prioridade sobre rascunhos. Fotos sao comprimidas antes do upload. Retry automatico com backoff exponencial em caso de falha. Notificacao ao usuario quando sync completa ou falha definitivamente.

## Contrato do Endpoint de Pull

O endpoint de pull (GET /api/sync/changes) recebe o parametro since como timestamp ISO 8601 representando o momento da ultima sincronizacao bem-sucedida. O servidor retorna um objeto contendo tres colecoes: units, holders e communities. Cada colecao e subdividida em tres arrays: created contendo registros completos criados desde o timestamp informado, updated contendo registros completos modificados desde o timestamp e deleted contendo apenas os UUIDs de registros removidos. O campo serverTimestamp na raiz da response contem o timestamp do servidor no momento da consulta, que o client deve armazenar e enviar como since no proximo pull. O campo hasMore como boolean indica se existem mais mudancas alem das retornadas, implementando paginacao de sync para volumes grandes. Quando hasMore e true, o client deve fazer outro pull usando o serverTimestamp retornado ate receber hasMore false.

Registros retornados respeitam as autorizacoes de comunidade do usuario: apenas dados de comunidades para as quais o usuario ou sua equipe tem CommunityAuthorization sao incluidos. Registros de outros tenants nunca sao retornados independente de qualquer parametro.

## Contrato do Endpoint de Push

O endpoint de push (POST /api/sync/push) recebe no body um array de operacoes. Cada operacao contem entityType indicando o tipo da entidade (UNIT, HOLDER, DOCUMENT), localId como string contendo o ID local do WatermelonDB, operation como enum (CREATE, UPDATE, DELETE), payload como objeto contendo os dados da entidade conforme schema do servidor e clientTimestamp como ISO 8601 indicando quando a operacao foi executada localmente.

O servidor processa as operacoes sequencialmente na ordem recebida, respeitando dependencias implicitas (holder deve existir antes de ser vinculado a unit). Para cada operacao, valida regras de negocio (CPF valido, campos obrigatorios, status permitido) e persiste ou rejeita. A response contem um array results com um resultado por operacao enviada. Cada resultado inclui localId para correlacao, status como SUCCESS, CONFLICT ou ERROR, serverId como UUID atribuido pelo servidor quando a operacao e CREATE bem-sucedido, e conflictData como objeto nullable contendo os campos divergentes entre a versao do client e do servidor quando status e CONFLICT.

Operacoes com status ERROR incluem errorCode (conforme tabela de error codes da GEOAPI) e message com descricao legivel do problema. O client deve tratar cada erro individualmente: erros de validacao exigem correcao do usuario, erros de conflito entram no fluxo de resolucao de conflitos, erros de autorizacao indicam perda de acesso a comunidade.

## Contrato do Endpoint de Status

O endpoint de status (GET /api/sync/status) retorna um objeto com lastSyncAt como timestamp ISO 8601 da ultima sincronizacao bem-sucedida registrada no servidor para o usuario corrente, pendingConflicts como inteiro contendo a quantidade de conflitos aguardando resolucao manual e pendingOperations como inteiro contendo operacoes na fila do servidor ainda nao processadas para o tenant do usuario. Esse endpoint e usado pelo app para exibir indicadores de sincronizacao na interface.
