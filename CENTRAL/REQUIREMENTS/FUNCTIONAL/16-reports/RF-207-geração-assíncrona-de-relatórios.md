---
type: rf
status: approved
updated: 2026-01-25
modules:
  - GEOWEB
  - GEOAPI
---

# RF-207: Geracao Assincrona de Relatorios

## Descricao

Sistema deve implementar processamento assincrono para geracao de relatorios complexos ou volumosos atraves de fila de jobs gerenciada por sistema como BullMQ, onde requisicoes que demandam processamento intensivo sao enfileiradas e executadas em background por workers dedicados sem bloquear interface. Quando relatorio exige tempo superior a limite configuravel (tipicamente 30 segundos), sistema retorna resposta indicando geracao em andamento com identificador unico para acompanhamento. Ao concluir, notificacao automatica ao usuario via in-app e email com link direto para download. Arquivo armazenado temporariamente com link valido por periodo configuravel (tipicamente 7 dias), apos removido automaticamente para liberar armazenamento.

## Criterios de Aceitacao

1. Fila de jobs com BullMQ ou similar
2. Limite de tempo configuravel para async
3. Identificador unico para acompanhamento
4. Notificacao in-app e email ao concluir
5. Link temporario com expiracao

## Rastreabilidade

- Modulos: GEOWEB, GEOAPI
- Requisitos dependentes: RF-203, RF-204, RF-205
