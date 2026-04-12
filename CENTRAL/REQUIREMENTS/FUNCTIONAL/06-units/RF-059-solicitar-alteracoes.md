---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-059: Solicitar Alteracoes

## Descricao

Sistema deve permitir que usuarios com perfil MANAGER solicitem alteracoes em unidades pendentes quando identificarem problemas que nao justifiquem rejeicao completa. Solicitacao inclui campo obrigatorio de texto detalhando modificacoes necessarias com orientacao clara sobre quais campos precisam correcao. Status alterado para CHANGES_REQUESTED com notificacao automatica ao analista responsavel incluindo descricao e link para edicao. Mecanismo intermediario entre aprovacao e rejeicao otimiza fluxo colaborativo conforme WORKFLOW-MESTRE.

## Criterios de Aceitacao

1. Botao de solicitar alteracoes visivel para MANAGER
2. Campo de texto obrigatorio com descricao das alteracoes
3. Status alterado para CHANGES_REQUESTED
4. Notificacao automatica ao analista com link de edicao
5. Historico registra todas solicitacoes e correcoes

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-056, RF-057, RF-058
