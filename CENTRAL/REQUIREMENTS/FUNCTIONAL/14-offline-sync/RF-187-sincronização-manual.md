---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBCAD
  - GEOAPI
---

# RF-187: Sincronizacao Manual

## Descricao

Sistema deve disponibilizar botao de sincronizacao manual acessivel na interface do aplicativo mobile permitindo ao usuario acionar processo de sincronizacao entre dispositivo local e servidor central no momento apropriado. Indicador de progresso visivel informa andamento incluindo registros sendo enviados (push), registros sendo recebidos (pull), percentual concluido e etapa atual. Ao concluir, sistema apresenta feedback detalhado de sucesso indicando quantidade de registros sincronizados, ou feedback de erro especificando natureza do problema como falha de conexao, timeout, erro de validacao ou conflitos detectados. Abordagem preferivel em contextos de conectividade limitada onde usuario deseja controlar consumo de dados moveis ou aguardar disponibilidade de WiFi.

## Criterios de Aceitacao

1. Botao de sincronizacao acessivel
2. Indicador de progresso detalhado
3. Feedback de sucesso com quantidades
4. Feedback de erro especifico
5. Controle de consumo de dados

## Rastreabilidade

- Modulos: REURBCAD, GEOAPI
- Requisitos dependentes: RF-182, RF-192, RF-193
