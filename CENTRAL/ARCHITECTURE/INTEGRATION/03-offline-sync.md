---
type: leaf
status: approved
updated: 2026-01-24
---

# Offline Sync

Estrategia de sincronizacao entre REURBCAD mobile e GEOAPI para operacao em areas sem conectividade. O Agente de Campo so tem acesso aos dados apos o Analista publicar seu trabalho no backend. Antes de operar offline, o agente realiza download unico e temporario do pacote contendo ortofoto e poligonos do tenant designado. Dados coletados em campo sao armazenados localmente em WatermelonDB e sincronizados quando conexao esta disponivel.

Sincronizacao usa pull-push model. Pull baixa mudancas do servidor desde ultima sync usando timestamp de versao. Push envia mudancas locais em batch ordenado por dependencia. Conflitos sao detectados por versao do registro e resolvidos com estrategia last-write-wins para campos simples e merge para colecoes.

## Fila de Upload

Operacoes pendentes ficam em fila persistente ordenada por prioridade e timestamp. Unidades aprovadas tem prioridade sobre rascunhos. Fotos sao comprimidas antes do upload. Retry automatico com backoff exponencial em caso de falha. Notificacao ao usuario quando sync completa ou falha definitivamente.
