---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-074: Criar Lote

## Descricao

Sistema deve permitir criacao de lotes representando subdivisoes dentro de quadras. Lote e unidade territorial intermediaria entre quadra e unidade habitacional utilizada em parcelamento formal. Formulario captura codigo identificador, area em metros quadrados e geometria espacial do poligono delimitador, alem de vinculacao obrigatoria a quadra existente. Geometria do lote deve estar contida na geometria da quadra quando ambas definidas, com validacao automatica alertando sobre lotes que extrapolam limites da quadra.

## Criterios de Aceitacao

1. Formulario com codigo, area e geometria
2. Vinculacao obrigatoria a quadra
3. Validacao de contencao espacial
4. Codigo unico por quadra
5. Hierarquia quadra-lote-unidade

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-070
