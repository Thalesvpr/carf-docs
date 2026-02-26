---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
---

# RF-149: Visibilidade de Camadas

## Descricao

Sistema deve permitir controlar visibilidade de cada camada individualmente no mapa atraves de interface simples, mostrando ou ocultando layers conforme necessidade de analise ou apresentacao. Painel de camadas inclui checkbox ou toggle de visibilidade adjacente a cada layer permitindo ativacao e desativacao com unico clique, com estado visual refletindo claramente se camada esta visivel. Atualizacao de visibilidade no mapa ocorre imediatamente apos mudanca sem latencia perceptivel, adicionando ou removendo layer instantaneamente. Sistema implementa persistencia de preferencias salvando estado de cada camada na sessao do usuario ou localStorage, restaurando configuracao ao recarregar aplicacao. Funcionalidade respeita visibilidade padrao configurada na criacao da camada como estado inicial para novos usuarios ou sessoes limpas.

## Criterios de Aceitacao

1. Checkbox ou toggle por camada
2. Atualizacao imediata no mapa
3. Persistencia de preferencias na sessao
4. Respeito a visibilidade padrao inicial
5. Estado visual claro (visivel/oculto)

## Rastreabilidade

- Modulos: REURBWEB
- Requisitos dependentes: RF-127, RF-130
