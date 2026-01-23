---
type: adr
status: current
updated: 2026-01-22
---

# ADR-002: WatermelonDB para Operacao Offline

## Contexto

Agentes de campo coletam dados em comunidades frequentemente sem conectividade movel. Aplicativo deve funcionar completamente offline por dias e sincronizar quando conexao estiver disponivel. Escolha de banco local impacta performance, capacidade de armazenamento e complexidade de sincronizacao.

## Decisao

Adotamos WatermelonDB como banco local no REURBCAD. WatermelonDB usa SQLite internamente com camada reativa em JavaScript otimizada para React Native. Modelo de sincronizacao pull-push nativo simplifica resolucao de conflitos. Lazy loading de registros evita carregar dataset inteiro em memoria.

## Consequencias

Performance excelente com milhares de registros mesmo em dispositivos modestos. Sync nativo reduz codigo customizado de resolucao de conflitos. Curva de aprendizado para desenvolvedores nao familiarizados com modelo reativo. Migracoes de schema requerem cuidado especial em dispositivos ja instalados.

## Alternativas Rejeitadas

SQLite puro foi descartado por requerer implementacao manual de sincronizacao e camada reativa. Realm foi rejeitado por modelo de licenciamento e dependencia de servico cloud proprietario. AsyncStorage foi descartado por limitacoes de capacidade e ausencia de queries estruturadas.
