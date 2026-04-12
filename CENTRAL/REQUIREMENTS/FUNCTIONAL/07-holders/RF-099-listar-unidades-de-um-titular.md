---
type: rf
status: approved
updated: 2026-01-25
modules:
  - REURBWEB
  - GEOAPI
---

# RF-099: Listar Unidades de um Titular

## Descricao

Sistema deve apresentar lista completa de unidades vinculadas a um titular especifico mostrando codigo, endereco, comunidade, tipo de relacionamento e status da unidade. Listagem facilita identificacao de titulares com multiplas propriedades e deteccao de irregularidades como mesmo titular em unidades distantes. Interface oferece filtros por tipo de relacionamento e status. Cada item clicavel navega para visualizacao detalhada da unidade. Links bidirecionais entre titular e unidades associadas.

## Criterios de Aceitacao

1. Lista de unidades por titular
2. Exibicao de tipo de relacionamento e status
3. Filtros por relacionamento e status
4. Navegacao para detalhes da unidade
5. Links bidirecionais titular-unidades

## Rastreabilidade

- Modulos: REURBWEB, GEOAPI
- Requisitos dependentes: RF-061, RF-052
