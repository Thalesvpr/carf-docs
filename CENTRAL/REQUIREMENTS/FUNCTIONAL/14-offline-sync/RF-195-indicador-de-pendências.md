---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
---

# RF-195: Indicador de Pendencias

## Descricao

Sistema deve exibir indicador visual proeminente de pendencias de sincronizacao atraves de badge numerico sobre icone de sincronizacao na interface principal, mostrando quantidade total de registros locais criados ou modificados que ainda nao foram transmitidos ao servidor central. Ao tocar no indicador, usuario acessa listagem detalhada de registros pendentes organizada por tipo de entidade (unidades, titulares, fotos) e tipo de operacao (criacao, edicao, delecao), incluindo identificacao de cada registro. Contador atualizado em tempo real sempre que usuario cria, edita ou completa sincronizacao, refletindo estado atual preciso de dados nao sincronizados. Indicador serve funcao critica de awareness situacional lembrando usuario sobre trabalho local nao persistido e motivando sincronizacao quando conectividade disponivel.

## Criterios de Aceitacao

1. Badge numerico sobre icone de sync
2. Listagem detalhada por tipo de entidade
3. Segmentacao por tipo de operacao
4. Atualizacao em tempo real
5. Identificacao de cada registro pendente

## Rastreabilidade

- Modulos: REURBCAD
- Requisitos dependentes: RF-184, RF-185, RF-186
